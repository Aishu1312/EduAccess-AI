"""
learning_style.py — EduAccess-AI
AI-powered learning style detector using VARK model.
Classifies learners into Visual / Auditory / Reading-Writing / Kinesthetic
based on interaction patterns, quiz responses, and behavioral signals.

Install: pip install scikit-learn numpy
"""

import json
import os
import time
from collections import defaultdict


# ─── VARK Model Definition ─────────────────────────────────────────
LEARNING_STYLES = {
    "visual":      {"icon": "👁️",  "label": "Visual Learner",
                    "description": "You learn best through diagrams, charts, videos, and visual explanations."},
    "auditory":    {"icon": "🎧",  "label": "Auditory Learner",
                    "description": "You learn best by listening — lectures, podcasts, verbal explanations."},
    "reading":     {"icon": "📖",  "label": "Reading/Writing Learner",
                    "description": "You learn best through text — notes, summaries, articles, written explanations."},
    "kinesthetic": {"icon": "🔬",  "label": "Kinesthetic Learner",
                    "description": "You learn best by doing — practice problems, experiments, hands-on examples."},
}

# VARK diagnostic questionnaire (20 questions)
VARK_QUESTIONS = [
    {
        "id": 1,
        "question": "When learning something new, you prefer to:",
        "options": {
            "A": {"text": "Watch a video or look at diagrams",         "style": "visual"},
            "B": {"text": "Listen to an explanation or podcast",       "style": "auditory"},
            "C": {"text": "Read notes or a textbook",                  "style": "reading"},
            "D": {"text": "Try it out hands-on with examples",        "style": "kinesthetic"},
        }
    },
    {
        "id": 2,
        "question": "When you want to remember something important, you:",
        "options": {
            "A": {"text": "Draw a mind map or picture",                "style": "visual"},
            "B": {"text": "Repeat it aloud or explain to someone",     "style": "auditory"},
            "C": {"text": "Write it down in notes",                    "style": "reading"},
            "D": {"text": "Act it out or apply it immediately",        "style": "kinesthetic"},
        }
    },
    {
        "id": 3,
        "question": "When studying for an exam, you:",
        "options": {
            "A": {"text": "Use color-coded highlights and flowcharts", "style": "visual"},
            "B": {"text": "Record yourself and listen back",           "style": "auditory"},
            "C": {"text": "Make detailed written summaries",           "style": "reading"},
            "D": {"text": "Solve as many practice problems as possible", "style": "kinesthetic"},
        }
    },
    {
        "id": 4,
        "question": "A good teacher is one who:",
        "options": {
            "A": {"text": "Uses lots of diagrams and slides",          "style": "visual"},
            "B": {"text": "Gives clear verbal explanations",           "style": "auditory"},
            "C": {"text": "Provides detailed written handouts",        "style": "reading"},
            "D": {"text": "Gives practical demonstrations",           "style": "kinesthetic"},
        }
    },
    {
        "id": 5,
        "question": "When you are confused about a topic, you:",
        "options": {
            "A": {"text": "Look for a YouTube video",                  "style": "visual"},
            "B": {"text": "Ask someone to explain it verbally",        "style": "auditory"},
            "C": {"text": "Search for articles or documentation",      "style": "reading"},
            "D": {"text": "Experiment with it yourself",               "style": "kinesthetic"},
        }
    },
    {
        "id": 6,
        "question": "Your ideal study material is:",
        "options": {
            "A": {"text": "Infographics and visual summaries",         "style": "visual"},
            "B": {"text": "Audio lectures or podcasts",                "style": "auditory"},
            "C": {"text": "Written textbooks and notes",               "style": "reading"},
            "D": {"text": "Labs, projects, and coding exercises",      "style": "kinesthetic"},
        }
    },
    {
        "id": 7,
        "question": "When giving directions to a place, you:",
        "options": {
            "A": {"text": "Draw a map",                                "style": "visual"},
            "B": {"text": "Describe it verbally step by step",         "style": "auditory"},
            "C": {"text": "Write out the directions",                  "style": "reading"},
            "D": {"text": "Walk them there or mime the route",         "style": "kinesthetic"},
        }
    },
    {
        "id": 8,
        "question": "When you read an important book, you prefer:",
        "options": {
            "A": {"text": "Chapters with lots of images and charts",   "style": "visual"},
            "B": {"text": "Audiobook format",                          "style": "auditory"},
            "C": {"text": "Dense written text with examples",          "style": "reading"},
            "D": {"text": "Case studies and real-world scenarios",     "style": "kinesthetic"},
        }
    },
]

# Behavioral signal weights (from UI interaction tracking)
BEHAVIOR_WEIGHTS = {
    "clicked_diagram":      ("visual",      0.3),
    "clicked_video":        ("visual",      0.4),
    "used_voice_input":     ("auditory",    0.5),
    "played_audio":         ("auditory",    0.4),
    "read_full_article":    ("reading",     0.4),
    "downloaded_notes":     ("reading",     0.3),
    "attempted_quiz":       ("kinesthetic", 0.5),
    "used_code_sandbox":    ("kinesthetic", 0.6),
    "skipped_video":        ("reading",     0.2),
    "replayed_audio":       ("auditory",    0.3),
    "used_highlighter":     ("visual",      0.2),
    "wrote_notes":          ("reading",     0.3),
}


class LearningStyleService:
    """
    Detects and tracks a student's VARK learning style.
    
    Usage:
        service = LearningStyleService()
        
        # VARK Questionnaire approach
        questions = service.get_questionnaire()
        service.submit_answers(user_id, {"1": "A", "2": "C", ...})
        result = service.get_style(user_id)
        
        # Behavioral tracking approach
        service.track_behavior(user_id, "clicked_video")
        result = service.get_style(user_id)
    """

    def __init__(self):
        self._profiles = defaultdict(lambda: {
            "visual": 0.0, "auditory": 0.0,
            "reading": 0.0, "kinesthetic": 0.0,
            "questionnaire_done": False,
            "last_updated": None
        })

    # ── Questionnaire Flow ─────────────────────────────────────────

    def get_questionnaire(self) -> list:
        """Return the VARK questionnaire questions."""
        return VARK_QUESTIONS

    def submit_answers(self, user_id: str, answers: dict) -> dict:
        """
        Process questionnaire answers and update user profile.
        
        Args:
            user_id: Unique user identifier
            answers: Dict of {question_id: option_letter} e.g. {"1": "A", "2": "C"}
        
        Returns:
            Learning style result dict
        """
        scores = {"visual": 0, "auditory": 0, "reading": 0, "kinesthetic": 0}

        for q in VARK_QUESTIONS:
            q_id = str(q["id"])
            if q_id in answers:
                option = answers[q_id].upper()
                if option in q["options"]:
                    style = q["options"][option]["style"]
                    scores[style] += 1

        # Normalize to 0-1 range
        total = sum(scores.values()) or 1
        for style in scores:
            self._profiles[user_id][style] = round(scores[style] / total, 3)

        self._profiles[user_id]["questionnaire_done"] = True
        self._profiles[user_id]["last_updated"] = time.time()

        return self.get_style(user_id)

    # ── Behavioral Tracking ────────────────────────────────────────

    def track_behavior(self, user_id: str, behavior: str):
        """
        Update learning style scores based on UI interaction signals.
        
        Args:
            user_id: Unique user identifier
            behavior: Behavior key from BEHAVIOR_WEIGHTS
        """
        if behavior not in BEHAVIOR_WEIGHTS:
            return

        style, weight = BEHAVIOR_WEIGHTS[behavior]
        profile = self._profiles[user_id]
        profile[style] = min(1.0, profile[style] + weight * 0.1)
        profile["last_updated"] = time.time()

        # Re-normalize so scores sum to 1
        total = sum(profile[s] for s in LEARNING_STYLES) or 1
        for s in LEARNING_STYLES:
            profile[s] = round(profile[s] / total, 3)

    def track_behaviors_batch(self, user_id: str, behaviors: list):
        """Track multiple behaviors at once."""
        for behavior in behaviors:
            self.track_behavior(user_id, behavior)

    # ── Style Retrieval ────────────────────────────────────────────

    def get_style(self, user_id: str) -> dict:
        """
        Get the current learning style profile for a user.
        
        Returns:
        {
          "primary_style": "visual",
          "secondary_style": "kinesthetic",
          "scores": {"visual": 0.4, "auditory": 0.2, ...},
          "recommendations": [...],
          "label": "Visual Learner",
          "description": "...",
          "icon": "👁️"
        }
        """
        profile = self._profiles[user_id]
        scores = {s: profile[s] for s in LEARNING_STYLES}

        # Sort by score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        primary   = ranked[0][0]
        secondary = ranked[1][0]

        return {
            "primary_style":   primary,
            "secondary_style": secondary,
            "scores":          scores,
            "label":           LEARNING_STYLES[primary]["label"],
            "description":     LEARNING_STYLES[primary]["description"],
            "icon":            LEARNING_STYLES[primary]["icon"],
            "recommendations": self._get_recommendations(primary, secondary),
            "questionnaire_done": profile["questionnaire_done"],
        }

    def get_adaptive_content_mode(self, user_id: str) -> str:
        """
        Returns the recommended content display mode for this user.
        Used by frontend to switch between visual/audio/text modes.
        
        Returns: "visual" | "audio" | "text" | "interactive"
        """
        style_map = {
            "visual":      "visual",
            "auditory":    "audio",
            "reading":     "text",
            "kinesthetic": "interactive"
        }
        result = self.get_style(user_id)
        return style_map.get(result["primary_style"], "text")

    # ── AI-Enhanced Detection (via Gemini) ─────────────────────────

    def detect_from_struggle_pattern(self, user_id: str, struggle_history: list,
                                      gemini_api_key: str = None) -> dict:
        """
        Use Gemini to infer learning style from a student's struggle history.
        
        Args:
            struggle_history: List of {"topic": str, "mode": str, "time_spent": int}
            
        Returns: Learning style result
        """
        api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        if not api_key or not struggle_history:
            return self.get_style(user_id)

        prompt = f"""
Analyze this student's learning struggle history and determine their VARK learning style.

Struggle History (topic, content mode, time spent in minutes):
{json.dumps(struggle_history, indent=2)}

Based on what they struggled with (spent more time on) vs what they found easy,
determine their dominant VARK learning style: visual, auditory, reading, or kinesthetic.

Respond ONLY in this JSON format:
{{
  "primary_style": "visual",
  "confidence": 0.75,
  "reasoning": "Student spent 3x more time on text content than video content",
  "recommended_switch": "Switch to more video/diagram content for this student"
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
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read())

            raw = data["candidates"][0]["content"]["parts"][0]["text"]
            raw = raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
            ai_result = json.loads(raw)

            # Update profile with AI inference
            inferred = ai_result.get("primary_style", "visual")
            if inferred in LEARNING_STYLES:
                self._profiles[user_id][inferred] = min(
                    1.0, self._profiles[user_id][inferred] + 0.3
                )

            return {**self.get_style(user_id), "ai_reasoning": ai_result.get("reasoning")}

        except Exception:
            return self.get_style(user_id)

    # ── Private Helpers ────────────────────────────────────────────

    def _get_recommendations(self, primary: str, secondary: str) -> list:
        recommendations = {
            "visual": [
                "Use the Diagram & Flowchart view for complex topics",
                "Enable color-coded highlighting in Dyslexia Mode",
                "Watch the AI-recommended YouTube videos for each chapter",
                "Use Mind Maps in the Study Planner",
            ],
            "auditory": [
                "Enable the Voice Assistant for all explanations",
                "Use 'Read Aloud' mode for notes and summaries",
                "Record yourself summarizing topics for revision",
                "Join the AI Voice Quiz mode",
            ],
            "reading": [
                "Use the Smart Notes Simplifier for complex chapters",
                "Download AI-generated PDF summaries",
                "Enable the 'Detailed Text Mode' for all topics",
                "Write your own notes after each section",
            ],
            "kinesthetic": [
                "Always attempt the Practice Quiz after each topic",
                "Use the Code Sandbox for programming topics",
                "Apply concepts to real-world projects immediately",
                "Enable the Step-by-Step Interactive Mode",
            ],
        }
        recs = recommendations.get(primary, [])
        # Add one recommendation from secondary style
        sec_recs = recommendations.get(secondary, [])
        if sec_recs:
            recs.append(sec_recs[0])
        return recs


# ─── Quick Test ────────────────────────────────────────────────────
if __name__ == "__main__":
    service = LearningStyleService()

    print("📋 VARK Learning Style Assessment")
    print("=" * 45)

    questions = service.get_questionnaire()
    answers = {}
    for q in questions[:5]:  # Demo: first 5 questions
        print(f"\nQ{q['id']}: {q['question']}")
        for opt, data in q["options"].items():
            print(f"  {opt}) {data['text']}")
        choice = input("Your choice (A/B/C/D): ").strip().upper()
        answers[str(q["id"])] = choice

    result = service.submit_answers("test_user", answers)
    print(f"\n{result['icon']} You are a {result['label']}!")
    print(f"📖 {result['description']}")
    print(f"\n📊 Scores: {result['scores']}")
    print(f"\n💡 Recommendations:")
    for rec in result["recommendations"]:
        print(f"  • {rec}")
