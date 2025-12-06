"""
Simple ScriptWriter for the studio.
This module provides a lightweight ScriptWriter that can read a plain-text story
or a text file and produce a structured script (list of scenes). Each scene
includes a short description, inferred emotion, simple camera_plan and
dialogue entries. The goal is to give the Master Brain a deterministic,
inspectable plan to distribute to specialized brains.

This is intentionally simple / rule-based so it can run offline in CI/dry-run.
"""
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


EMOTION_KEYWORDS = {
    "happy": ["ਖੁਸ਼", "ਖੁਸ਼ੀ", "happy", "joy", "celebrate", "celebration"],
    "sad": ["ਉਦਾਸ", "ਦੁਖੀ", "sad", "sorrow", "दुःख", "regret"],
    "angry": ["ਗੁੱਸਾ", "angry", "rage", "furious"],
    "peaceful": ["ਸ਼ਾਂਤ", "peace", "calm", "serene", "peaceful"],
    "spiritual": ["ਪ੍ਰਾਰਥਨਾ", "gurbani", "prayer", "spiritual", "kirtan"]
}


class ScriptWriter:
    """Very small rule-based script writer used by MasterOrchestratorBrain.

    Methods:
    - create_script_from_text(text): returns a dict with scenes[]
    - create_script_from_file(path): convenience wrapper
    - save_script(script, path): save JSON
    """

    def __init__(self, output_dir: str = "brain_memory/scripts"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _infer_emotion(self, text: str) -> str:
        t = text.lower()
        for emo, kws in EMOTION_KEYWORDS.items():
            for kw in kws:
                if kw in t:
                    return emo
        return "neutral"

    def _split_into_scenes(self, text: str) -> List[str]:
        # Split on 'Scene' markers or blank-line paragraphs
        scenes = []
        # Try explicit Scene markers first
        parts = re.split(r"(?i)scene\s+\d+[:\.]?", text)
        parts = [p.strip() for p in parts if p.strip()]
        if len(parts) > 1:
            return parts

        # Fallback: split by double newlines
        parts = [p.strip() for p in text.split('\n\n') if p.strip()]
        return parts if parts else [text.strip()]

    def _extract_dialogues(self, block: str) -> List[Dict[str, str]]:
        # Very simple heuristic: lines containing ':' are char: text
        dialogues = []
        for line in block.splitlines():
            if ':' in line:
                parts = line.split(':', 1)
                char = parts[0].strip()
                txt = parts[1].strip()
                if txt:
                    dialogues.append({"character": char, "text": txt})
        return dialogues

    def _infer_location(self, text: str) -> Optional[str]:
        # small heuristic based on keywords
        t = text.lower()
        if any(x in t for x in ["gurudwara", "ਗੁਰੂ", "gurudwara"]):
            return "gurudwara"
        if any(x in t for x in ["village", "ਪਿੰਡ", "ਪਿੰਡ ਵਿੱਚ"]):
            return "village"
        if any(x in t for x in ["farm", "ਖੇਤੀ", "farm"]):
            return "farm"
        return "unknown"

    def _make_camera_plan(self, scene_text: str, duration: float = 6.0) -> Dict[str, Any]:
        emotion = self._infer_emotion(scene_text)
        # Simple mapping
        if emotion == "happy":
            move = {"type": "pan", "direction": "left-to-right", "speed": "medium"}
            zoom = {"start": 1.0, "end": 1.06}
        elif emotion == "sad":
            move = {"type": "tilt", "direction": "down", "speed": "slow"}
            zoom = {"start": 1.0, "end": 1.02}
        elif emotion == "spiritual":
            move = {"type": "dolly", "direction": "forward", "speed": "very_slow"}
            zoom = {"start": 1.0, "end": 1.04}
        else:
            move = {"type": "static", "direction": None, "speed": "none"}
            zoom = {"start": 1.0, "end": 1.02}

        return {
            "emotion": emotion,
            "duration": duration,
            "movement": move,
            "zoom": zoom,
            "recommended_shot": "medium" if emotion in ["happy","neutral"] else "close"
        }

    def create_script_from_text(self, text: str, default_scene_duration: float = 6.0) -> Dict[str, Any]:
        """Turn freeform text into a structured script.

        Output format:
        {
          "title": "...",
          "created_at": "...",
          "scenes": [ {scene dict}, ... ]
        }
        """
        scenes_raw = self._split_into_scenes(text)
        script = {
            "title": (text.strip().splitlines()[0])[:120] if text.strip() else "Untitled",
            "created_at": datetime.now().isoformat(),
            "scenes": []
        }

        for idx, block in enumerate(scenes_raw):
            emotion = self._infer_emotion(block)
            dialogues = self._extract_dialogues(block)
            location = self._infer_location(block)
            camera_plan = self._make_camera_plan(block, duration=default_scene_duration)

            scene = {
                "scene_id": idx,
                "raw_text": block[:2000],
                "description": block.strip().splitlines()[0][:300],
                "dialogues": dialogues,
                "emotion": emotion,
                "location": location,
                "camera_plan": camera_plan,
                "duration": camera_plan.get("duration", default_scene_duration)
            }

            script["scenes"].append(scene)

        return script

    def create_script_from_file(self, path: str, **kwargs) -> Dict[str, Any]:
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Story file not found: {path}")
        text = p.read_text(encoding='utf-8')
        return self.create_script_from_text(text, **kwargs)

    def save_script(self, script: Dict[str, Any], filename: Optional[str] = None) -> Path:
        if not filename:
            filename = f"script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        p = self.output_dir / filename
        with p.open('w', encoding='utf-8') as f:
            json.dump(script, f, ensure_ascii=False, indent=2)
        return p


if __name__ == "__main__":
    sample = """
    Scene 1: ਪਿੰਡ ਵਿੱਚ ਇੱਕ ਘਰ ਹੈ। ਕੁਲਵੰਤ ਖੁਸ਼ ਹੈ: ਕੁਲਵੰਤ: ਪਿੰਡ ਦੀ ਖੁਸ਼ੀ ਦੇਖੋ!

    Scene 2: ਉਹ ਮੰਜਾ ਤੇ ਬੈਠਦਾ ਹੈ।
    """
    sw = ScriptWriter()
    script = sw.create_script_from_text(sample)
    p = sw.save_script(script)
    print("Saved sample script to:", p)
