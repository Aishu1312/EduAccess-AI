"""
emotion_service.py — EduAccess-AI
Real-time emotion & attention detection using DeepFace + OpenCV.
Detects confusion, stress, fatigue, and low attention, then
triggers adaptive content changes via callback.

Install: pip install deepface opencv-python numpy
"""

import cv2
import numpy as np
import threading
import time
from collections import deque

try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except ImportError:
    DEEPFACE_AVAILABLE = False
    print("⚠️  DeepFace not installed. Run: pip install deepface")


# ─── Emotion → Learning Action Mapping ───────────────────────────
EMOTION_ACTIONS = {
    "angry":    {"action": "simplify",   "message": "You seem frustrated. Let me try a simpler explanation."},
    "disgust":  {"action": "change_mode","message": "Let's try a different learning approach for this topic."},
    "fear":     {"action": "encourage",  "message": "Don't worry! Let's break this down step by step."},
    "sad":      {"action": "break",      "message": "You've been studying hard. Want to take a short break?"},
    "surprise": {"action": "quiz",       "message": "You look engaged! Ready for a quick quiz?"},
    "neutral":  {"action": "continue",   "message": None},
    "happy":    {"action": "advance",    "message": "Great energy! Want to try something more challenging?"},
}

ATTENTION_THRESHOLD = 0.4   # Below this = low attention
FATIGUE_WINDOW_SEC  = 30    # Rolling window for trend analysis


class EmotionService:
    """
    Webcam-based real-time emotion & attention detection.
    
    Usage:
        service = EmotionService(on_emotion_change=my_callback)
        service.start()
        ...
        service.stop()
    
    Callback receives: {"emotion": str, "confidence": float, "action": str, "message": str}
    """

    def __init__(self, on_emotion_change=None, detection_interval=2.5):
        self.on_emotion_change = on_emotion_change
        self.detection_interval = detection_interval  # seconds between detections
        self._running = False
        self._thread = None
        self._cap = None
        self._emotion_history = deque(maxlen=10)
        self._last_reported_emotion = None
        self._session_start = None
        self._stats = {
            "sessions_analyzed": 0,
            "confusion_count": 0,
            "fatigue_count": 0,
            "happy_count": 0,
            "dominant_emotion": "neutral"
        }

    # ── Public API ────────────────────────────────────────────────

    def start(self, camera_index=0):
        """Start the emotion detection loop in a background thread."""
        if not DEEPFACE_AVAILABLE:
            print("❌ DeepFace is required. Install with: pip install deepface")
            return False

        self._cap = cv2.VideoCapture(camera_index)
        if not self._cap.isOpened():
            print("❌ Could not open webcam.")
            return False

        self._running = True
        self._session_start = time.time()
        self._thread = threading.Thread(target=self._detection_loop, daemon=True)
        self._thread.start()
        print("✅ Emotion detection started.")
        return True

    def stop(self):
        """Stop detection and release webcam."""
        self._running = False
        if self._cap:
            self._cap.release()
        print("🛑 Emotion detection stopped.")

    def get_current_frame(self):
        """Get the latest webcam frame (for display in UI)."""
        if self._cap and self._cap.isOpened():
            ret, frame = self._cap.read()
            return frame if ret else None
        return None

    def get_session_stats(self):
        """Return session-level emotion statistics."""
        if self._emotion_history:
            from collections import Counter
            counts = Counter(self._emotion_history)
            self._stats["dominant_emotion"] = counts.most_common(1)[0][0]
        return self._stats

    # ── Internal Detection Loop ───────────────────────────────────

    def _detection_loop(self):
        last_check = 0
        while self._running:
            ret, frame = self._cap.read()
            if not ret:
                time.sleep(0.1)
                continue

            now = time.time()
            if now - last_check >= self.detection_interval:
                last_check = now
                emotion_data = self._analyze_frame(frame)
                if emotion_data:
                    self._process_emotion(emotion_data)

    def _analyze_frame(self, frame):
        """Run DeepFace analysis on a single frame."""
        try:
            # Resize for faster processing
            small = cv2.resize(frame, (320, 240))
            result = DeepFace.analyze(
                small,
                actions=["emotion"],
                enforce_detection=False,
                silent=True
            )
            if isinstance(result, list):
                result = result[0]

            dominant = result.get("dominant_emotion", "neutral")
            scores   = result.get("emotion", {})
            confidence = scores.get(dominant, 0) / 100.0

            return {
                "emotion": dominant,
                "confidence": round(confidence, 3),
                "all_scores": {k: round(v/100, 3) for k, v in scores.items()}
            }
        except Exception:
            return None  # Face not detected — skip this frame

    def _process_emotion(self, data):
        """Decide whether to fire callback and update stats."""
        emotion    = data["emotion"]
        confidence = data["confidence"]

        self._emotion_history.append(emotion)
        self._stats["sessions_analyzed"] += 1

        # Count specific emotional states
        if emotion in ("angry", "fear", "disgust"):
            self._stats["confusion_count"] += 1
        elif emotion == "sad":
            self._stats["fatigue_count"] += 1
        elif emotion == "happy":
            self._stats["happy_count"] += 1

        # Only fire callback on meaningful confidence + state change
        if confidence < 0.35:
            return
        if emotion == self._last_reported_emotion:
            return  # Avoid repeating the same message

        self._last_reported_emotion = emotion
        action_info = EMOTION_ACTIONS.get(emotion, EMOTION_ACTIONS["neutral"])

        if action_info["message"] and self.on_emotion_change:
            payload = {
                "emotion": emotion,
                "confidence": confidence,
                "action": action_info["action"],
                "message": action_info["message"],
                "all_scores": data.get("all_scores", {})
            }
            self.on_emotion_change(payload)


# ─── Flask Route Helper ────────────────────────────────────────────

def analyze_image_base64(image_b64: str) -> dict:
    """
    Analyze a single base64-encoded image for emotion.
    Used by the Flask API endpoint /api/emotion/analyze
    
    Returns: {"emotion": str, "confidence": float, "message": str}
    """
    if not DEEPFACE_AVAILABLE:
        return {"error": "DeepFace not installed"}

    import base64
    try:
        img_bytes = base64.b64decode(image_b64)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        result = DeepFace.analyze(frame, actions=["emotion"],
                                  enforce_detection=False, silent=True)
        if isinstance(result, list):
            result = result[0]

        dominant   = result.get("dominant_emotion", "neutral")
        confidence = result.get("emotion", {}).get(dominant, 0) / 100

        action_info = EMOTION_ACTIONS.get(dominant, EMOTION_ACTIONS["neutral"])
        return {
            "emotion":    dominant,
            "confidence": round(confidence, 3),
            "action":     action_info["action"],
            "message":    action_info["message"],
            "all_scores": {k: round(v/100, 3)
                           for k, v in result.get("emotion", {}).items()}
        }
    except Exception as e:
        return {"error": str(e), "emotion": "neutral", "confidence": 0}


# ─── Quick Test ────────────────────────────────────────────────────
if __name__ == "__main__":
    def on_emotion(data):
        print(f"\n🎭 Emotion Detected: {data['emotion'].upper()} "
              f"(confidence: {data['confidence']:.0%})")
        if data["message"]:
            print(f"💬 AI Response: {data['message']}")

    service = EmotionService(on_emotion_change=on_emotion, detection_interval=3)
    if service.start():
        print("📸 Emotion detection running. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            service.stop()
            print("\n📊 Session Stats:", service.get_session_stats())
