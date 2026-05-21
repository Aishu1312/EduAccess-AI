"""
ocr_service.py — EduAccess-AI
OCR + Handwritten Notes Reader using EasyOCR and Tesseract.
Supports images, PDFs, handwritten text extraction, AI summarization,
and text-to-speech output.

Install: pip install easyocr pytesseract Pillow pdf2image gtts
         Also install Tesseract binary: https://github.com/UB-Mannheim/tesseract/wiki
"""

import os
import io
import base64
import tempfile
from pathlib import Path

try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False

try:
    import pytesseract
    from PIL import Image, ImageEnhance, ImageFilter
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

try:
    from pdf2image import convert_from_bytes
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    from gtts import gTTS
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False


# ─── Supported languages for EasyOCR ──────────────────────────────
LANGUAGE_MAP = {
    "en":    ["en"],
    "hi":    ["hi", "en"],
    "mr":    ["hi", "en"],           # Marathi → use Hindi model
    "ta":    ["ta", "en"],
    "te":    ["te", "en"],
    "bn":    ["bn", "en"],
    "gu":    ["gu", "en"],
    "kn":    ["kn", "en"],
    "multi": ["en", "hi", "ta"],
}


class OCRService:
    """
    Multi-engine OCR service supporting:
    - Printed text (Tesseract — fast)
    - Handwritten text (EasyOCR — accurate)
    - PDFs (convert pages → images → OCR)
    - Multi-language extraction
    - AI-powered summarization (via Gemini)
    - Text-to-speech of extracted text
    
    Usage:
        ocr = OCRService()
        result = ocr.extract_from_image(image_bytes, mode="handwritten")
        print(result["text"])
    """

    def __init__(self, default_language="en"):
        self.default_language = default_language
        self._reader_cache = {}  # Cache EasyOCR readers per language set

    # ── Core Extraction Methods ───────────────────────────────────

    def extract_from_image(self, image_bytes: bytes, mode="auto", language="en") -> dict:
        """
        Extract text from an image.
        
        Args:
            image_bytes: Raw image bytes (JPEG/PNG/WEBP)
            mode: "handwritten" | "printed" | "auto"
            language: ISO language code (en/hi/ta/te/mr/bn/gu/kn/multi)
        
        Returns:
            {"text": str, "confidence": float, "words": list, "engine": str}
        """
        try:
            image = Image.open(io.BytesIO(image_bytes))
            image = self._preprocess_image(image)

            if mode == "handwritten" or (mode == "auto" and EASYOCR_AVAILABLE):
                return self._extract_easyocr(image, language)
            elif TESSERACT_AVAILABLE:
                return self._extract_tesseract(image, language)
            else:
                return {"error": "No OCR engine available. Install easyocr or pytesseract."}

        except Exception as e:
            return {"error": str(e), "text": ""}

    def extract_from_pdf(self, pdf_bytes: bytes, language="en", max_pages=10) -> dict:
        """
        Extract text from a PDF file.
        
        Returns:
            {"text": str, "pages": list[str], "total_pages": int}
        """
        if not PDF_AVAILABLE:
            return {"error": "pdf2image not installed. Run: pip install pdf2image"}

        try:
            images = convert_from_bytes(pdf_bytes, dpi=200)[:max_pages]
            pages_text = []

            for i, img in enumerate(images):
                img_bytes = io.BytesIO()
                img.save(img_bytes, format="PNG")
                result = self.extract_from_image(img_bytes.getvalue(), language=language)
                pages_text.append(result.get("text", ""))

            full_text = "\n\n--- Page Break ---\n\n".join(pages_text)
            return {
                "text": full_text,
                "pages": pages_text,
                "total_pages": len(images),
                "engine": "easyocr+pdf2image"
            }
        except Exception as e:
            return {"error": str(e), "text": ""}

    def extract_from_base64(self, b64_string: str, file_type="image",
                             mode="auto", language="en") -> dict:
        """
        Extract text from a base64-encoded file.
        Used by Flask API endpoint /api/ocr/extract
        """
        try:
            raw_bytes = base64.b64decode(b64_string)
            if file_type == "pdf":
                return self.extract_from_pdf(raw_bytes, language=language)
            else:
                return self.extract_from_image(raw_bytes, mode=mode, language=language)
        except Exception as e:
            return {"error": str(e), "text": ""}

    # ── AI Summarization ──────────────────────────────────────────

    def summarize_extracted_text(self, text: str, level="medium",
                                  gemini_api_key: str = None) -> dict:
        """
        Send extracted OCR text to Gemini for AI summarization.
        
        Args:
            text: Extracted OCR text
            level: "beginner" | "medium" | "advanced" | "eli5"
            gemini_api_key: Optional, else reads from env GEMINI_API_KEY
        
        Returns:
            {"summary": str, "key_points": list, "level": str}
        """
        import os
        import json

        api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            return {"error": "GEMINI_API_KEY not set in environment variables"}

        level_prompts = {
            "beginner": "Summarize in very simple English, like for a 12-year-old student.",
            "medium":   "Summarize clearly for a college student.",
            "advanced": "Summarize with technical depth for an advanced learner.",
            "eli5":     "Explain Like I'm 5 years old. Use simple words and fun analogies.",
        }

        prompt = f"""
You are an AI tutor helping students understand their notes.

INSTRUCTIONS:
{level_prompts.get(level, level_prompts["medium"])}

Extract:
1. A clear 3-4 sentence summary
2. 5 key bullet-point takeaways
3. Any important formulas, dates, or names (if present)

TEXT FROM STUDENT'S NOTES:
\"\"\"
{text[:3000]}
\"\"\"

Respond ONLY in this JSON format:
{{
  "summary": "...",
  "key_points": ["point1", "point2", "point3", "point4", "point5"],
  "important_terms": ["term1", "term2"],
  "suggested_topics": ["topic to study next"]
}}
"""
        try:
            import urllib.request
            body = json.dumps({
                "contents": [{"parts": [{"text": prompt}]}]
            }).encode()

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            req = urllib.request.Request(url, data=body,
                                          headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())

            raw = data["candidates"][0]["content"]["parts"][0]["text"]
            # Strip markdown code fences if present
            raw = raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
            parsed = json.loads(raw)
            parsed["level"] = level
            return parsed

        except Exception as e:
            return {"error": str(e), "summary": text[:500], "key_points": []}

    # ── Text to Speech ─────────────────────────────────────────────

    def text_to_speech(self, text: str, language="en", output_path=None) -> str:
        """
        Convert extracted text to speech using gTTS.
        
        Returns: Path to the generated .mp3 file
        """
        if not TTS_AVAILABLE:
            return None

        if not output_path:
            tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
            output_path = tmp.name

        try:
            lang_code = language if len(language) == 2 else "en"
            tts = gTTS(text=text[:5000], lang=lang_code, slow=False)
            tts.save(output_path)
            return output_path
        except Exception as e:
            print(f"TTS error: {e}")
            return None

    # ── Private Helpers ────────────────────────────────────────────

    def _preprocess_image(self, image: "Image.Image") -> "Image.Image":
        """Enhance image quality for better OCR accuracy."""
        # Convert to RGB if needed
        if image.mode not in ("RGB", "L"):
            image = image.convert("RGB")

        # Increase contrast and sharpness for handwritten text
        image = ImageEnhance.Contrast(image).enhance(1.5)
        image = ImageEnhance.Sharpness(image).enhance(2.0)

        # Resize if too small
        w, h = image.size
        if w < 800:
            scale = 800 / w
            image = image.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

        return image

    def _extract_easyocr(self, image: "Image.Image", language="en") -> dict:
        """EasyOCR extraction — best for handwritten text."""
        langs = LANGUAGE_MAP.get(language, ["en"])
        lang_key = "_".join(langs)

        # Cache reader to avoid reloading model each time
        if lang_key not in self._reader_cache:
            self._reader_cache[lang_key] = easyocr.Reader(
                langs, gpu=False, verbose=False
            )

        reader = self._reader_cache[lang_key]

        # Convert PIL image to numpy array
        import numpy as np
        img_array = np.array(image)

        results = reader.readtext(img_array, detail=1)

        words = []
        text_parts = []
        total_conf = 0

        for (bbox, text, confidence) in results:
            words.append({"text": text, "confidence": round(confidence, 3)})
            text_parts.append(text)
            total_conf += confidence

        full_text = " ".join(text_parts)
        avg_conf = total_conf / len(results) if results else 0

        return {
            "text": full_text,
            "confidence": round(avg_conf, 3),
            "words": words,
            "engine": "easyocr",
            "language": language,
            "word_count": len(words)
        }

    def _extract_tesseract(self, image: "Image.Image", language="en") -> dict:
        """Tesseract extraction — best for printed text."""
        lang_map = {"hi": "hin", "ta": "tam", "te": "tel", "bn": "ben"}
        tess_lang = lang_map.get(language, "eng")

        config = f"--oem 3 --psm 6 -l {tess_lang}"

        try:
            raw_text = pytesseract.image_to_string(image, config=config)
            data = pytesseract.image_to_data(image, config=config,
                                              output_type=pytesseract.Output.DICT)

            words = []
            for i, word in enumerate(data["text"]):
                if word.strip() and int(data["conf"][i]) > 30:
                    words.append({"text": word, "confidence": data["conf"][i] / 100})

            return {
                "text": raw_text.strip(),
                "confidence": sum(w["confidence"] for w in words) / len(words) if words else 0,
                "words": words,
                "engine": "tesseract",
                "language": language,
                "word_count": len(words)
            }
        except Exception as e:
            return {"error": str(e), "text": ""}


# ─── Quick Test ────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    ocr = OCRService()

    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        with open(image_path, "rb") as f:
            img_bytes = f.read()

        print("🔍 Extracting text...")
        result = ocr.extract_from_image(img_bytes, mode="auto")
        print(f"\n📄 Extracted Text:\n{result['text']}")
        print(f"\n✅ Confidence: {result.get('confidence', 0):.0%}")
        print(f"🔤 Words found: {result.get('word_count', 0)}")

        if result["text"] and os.getenv("GEMINI_API_KEY"):
            print("\n🤖 Generating AI summary...")
            summary = ocr.summarize_extracted_text(result["text"], level="medium")
            print(f"\n📝 Summary: {summary.get('summary', '')}")
            print(f"\n🔑 Key Points:")
            for pt in summary.get("key_points", []):
                print(f"  • {pt}")
    else:
        print("Usage: python ocr_service.py path/to/image.jpg")
        print("       Set GEMINI_API_KEY env var for AI summarization")
