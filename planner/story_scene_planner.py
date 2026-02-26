#!/usr/bin/env python3
"""Simple rule-based story-to-scene planner for Rahbar cinematic pipeline.

This first version extracts scene structure, characters, locations, moods, and
rudimentary actions from free-form story text. It is intentionally lightweight
so Rahbar AI Developer can iterate quickly and replace heuristics with ML models
later on.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional

PUNJABI_RANGE = (0x0A00, 0x0A7F)

# Keyword dictionaries -------------------------------------------------------
LOCATION_KEYWORDS: Dict[str, List[str]] = {
    "gurdwara": ["gurdwara", "darbar sahib", "gurudwara", "sahib"],
    "fields": ["khet", "fields", "farm", "farming", "tractor", "mustard"],
    "home": ["ghar", "home", "house", "kitchen", "room", "parivaar"],
    "city": ["shehar", "city", "bazaar", "market", "mall"],
    "classroom": ["school", "class", "teacher", "student", "padhai"],
    "langar": ["langar", "kitchen", "seva", "deg", "parshada"],
    "sports_ground": ["cricket", "football", "khed", "playground", "stadium"],
    "river": ["river", "dariya", "sarovar", "swim", "paani", "canal"],
}

MOOD_KEYWORDS: Dict[str, List[str]] = {
    "devotional": ["ardas", "simran", "path", "gurbani", "waheguru"],
    "happy": ["khushi", "happy", "smile", "laughter", "celebration"],
    "sad": ["dukh", "sad", "ro", "tears", "loss"],
    "tense": ["dar", "fear", "tension", "conflict", "argument"],
    "fun": ["maza", "fun", "khed", "game", "laugh"],
    "adventurous": ["safar", "adventure", "explore", "climb", "mountain"],
    "romantic": ["pyar", "love", "romance", "dil"],
    "hopeful": ["umeed", "hope", "dream", "future"],
}

ACTION_KEYWORDS: Dict[str, List[str]] = {
    "walk": ["walk", "chal", "tur"],
    "run": ["run", "bhag", "dod"],
    "cricket_bat": ["cricket", "bat", "ball", "boundary"],
    "swim": ["swim", "paani", "sarovar", "river"],
    "fold_hands": ["ardas", "folded hands", "matha tek", "simran"],
    "serve_langar": ["langar", "seva", "serve"],
    "study": ["study", "padhai", "book", "teacher"],
    "play_music": ["sing", "gaana", "tabla", "harmonium", "raag"],
}

ROLE_KEYWORDS: Dict[str, Dict[str, List[str]]] = {
    "mother": {
        "keywords": ["mata", "maa", "mother", "mom", "amrit maa"],
        "gender": "female",
        "age": "adult",
        "voice": "female_adult_pa_01",
    },
    "father": {
        "keywords": ["bapu", "pitaji", "father", "dad"],
        "gender": "male",
        "age": "adult",
        "voice": "male_adult_pa_01",
    },
    "grandfather": {
        "keywords": ["dada", "nana", "grandfather", "baba ji"],
        "gender": "male",
        "age": "elder",
        "voice": "male_elder_pa_01",
    },
    "grandmother": {
        "keywords": ["dadi", "nani", "grandmother", "beji"],
        "gender": "female",
        "age": "elder",
        "voice": "female_elder_pa_01",
    },
    "teacher": {
        "keywords": ["teacher", "ustad", "sir", "madam"],
        "gender": "unknown",
        "age": "adult",
        "voice": "female_adult_pa_02",
    },
    "kid": {
        "keywords": ["puttar", "beta", "beti", "kid", "child", "son", "daughter"],
        "gender": "unknown",
        "age": "child",
        "voice": "child_neutral_pa_01",
    },
    "sikh_granthi": {
        "keywords": ["granthi", "giani", "pathi"],
        "gender": "male",
        "age": "adult",
        "voice": "male_adult_pa_02",
    },
}

DEFAULT_VOICES = {
    "male": "male_adult_pa_01",
    "female": "female_adult_pa_01",
    "child": "child_neutral_pa_01",
}

ROLE_FALLBACK = {
    "male": {"age": "adult", "voice": "male_adult_pa_01"},
    "female": {"age": "adult", "voice": "female_adult_pa_01"},
    "unknown": {"age": "adult", "voice": "narrator_pa_01"},
}


@dataclass
class CharacterPlan:
    """Representation of a character in a scene."""

    id: str
    display_name: str
    role: str
    voice_id: str
    gender: str = "unknown"
    age_group: str = "adult"
    action: Optional[str] = None
    mood_override: Optional[str] = None

    def as_dict(self) -> Dict[str, str]:
        payload = {
            "id": self.id,
            "display_name": self.display_name,
            "role": self.role,
            "voice_id": self.voice_id,
            "gender": self.gender,
            "age_group": self.age_group,
        }
        if self.action:
            payload["action"] = self.action
        if self.mood_override:
            payload["mood_override"] = self.mood_override
        return payload


@dataclass
class ScenePlan:
    scene_id: int
    title: Optional[str]
    narration: List[Dict[str, str]]
    location: Dict[str, object]
    mood: Dict[str, object]
    characters: List[CharacterPlan] = field(default_factory=list)
    props: List[str] = field(default_factory=list)
    duration_hint: Optional[float] = None

    def as_dict(self) -> Dict[str, object]:
        return {
            "scene_id": self.scene_id,
            "title": self.title,
            "narration": self.narration,
            "location": self.location,
            "mood": self.mood,
            "characters": [c.as_dict() for c in self.characters],
            "props": self.props,
            "duration_hint": self.duration_hint,
        }


class StoryScenePlanner:
    """Rule-based planner that converts script text into scene metadata."""

    def __init__(self, story_id: str = "story") -> None:
        self.story_id = story_id

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def plan(self, text: str) -> Dict[str, object]:
        paragraphs = self._split_into_scenes(text)
        scenes: List[ScenePlan] = []
        for idx, paragraph in enumerate(paragraphs, start=1):
            lines = [line for line in paragraph.splitlines() if line.strip()]
            narrations = self._build_narration(lines)
            location = self._detect_location(paragraph)
            mood = self._detect_mood(paragraph)
            characters = self._detect_characters(lines)
            action = self._detect_action(paragraph)
            if action:
                for character in characters:
                    if character.action is None:
                        character.action = action
            scene = ScenePlan(
                scene_id=idx,
                title=self._infer_title(lines, idx),
                narration=narrations,
                location=location,
                mood=mood,
                characters=characters,
                props=self._detect_props(paragraph),
                duration_hint=self._estimate_duration(narrations),
            )
            scenes.append(scene)
        language = self._detect_language(text)
        return {
            "story_id": self.story_id,
            "language": language,
            "scenes": [scene.as_dict() for scene in scenes],
        }

    # ------------------------------------------------------------------
    # Scene segmentation helpers
    # ------------------------------------------------------------------
    def _split_into_scenes(self, text: str) -> List[str]:
        if "[SCENE" in text.upper():
            pattern = re.compile(r"\[SCENE[^\]]*\]", re.IGNORECASE)
            parts = pattern.split(text)
            segments = [part.strip() for part in parts if part.strip()]
            return segments
        paragraphs = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]
        return paragraphs or [text.strip()]

    def _build_narration(self, lines: Iterable[str]) -> List[Dict[str, str]]:
        narration: List[Dict[str, str]] = []
        current_speaker = "narrator"
        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                continue
            if ":" in line:
                speaker, message = line.split(":", 1)
                current_speaker = speaker.strip()
                text = message.strip()
            else:
                text = line
            narration.append({"speaker": current_speaker or "narrator", "text": text})
        return narration

    # ------------------------------------------------------------------
    # Location / mood detection
    # ------------------------------------------------------------------
    def _detect_location(self, paragraph: str) -> Dict[str, object]:
        paragraph_lower = paragraph.lower()
        best_match = "home"
        best_confidence = 0.1
        for tag, keywords in LOCATION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in paragraph_lower:
                    confidence = 0.6 + 0.1 * len(keyword)
                    if confidence > best_confidence:
                        best_match = tag
                        best_confidence = confidence
        weather = None
        if any(key in paragraph_lower for key in ["rain", "barsaat", "rainy"]):
            weather = "rainy"
        elif any(key in paragraph_lower for key in ["fog", "kuhaar"]):
            weather = "foggy"
        elif any(key in paragraph_lower for key in ["cloud", "cloudy", "badal"]):
            weather = "cloudy"
        return {
            "tag": best_match,
            "confidence": round(min(best_confidence, 0.95), 2),
            "weather": weather,
        }

    def _detect_mood(self, paragraph: str) -> Dict[str, object]:
        paragraph_lower = paragraph.lower()
        best_match = "hopeful"
        best_confidence = 0.1
        for tag, keywords in MOOD_KEYWORDS.items():
            for keyword in keywords:
                if keyword in paragraph_lower:
                    confidence = 0.6 + 0.05 * len(keyword)
                    if confidence > best_confidence:
                        best_match = tag
                        best_confidence = confidence
        return {"tag": best_match, "confidence": round(min(best_confidence, 0.95), 2)}

    # ------------------------------------------------------------------
    # Characters, actions, props
    # ------------------------------------------------------------------
    def _detect_characters(self, lines: Iterable[str]) -> List[CharacterPlan]:
        characters: Dict[str, CharacterPlan] = {}
        for raw_line in lines:
            if ":" not in raw_line:
                continue
            speaker = raw_line.split(":", 1)[0].strip()
            identifier = self._normalize_identifier(speaker)
            role, gender, age_group, voice = self._infer_role(speaker)
            if identifier not in characters:
                characters[identifier] = CharacterPlan(
                    id=identifier,
                    display_name=speaker,
                    role=role,
                    voice_id=voice,
                    gender=gender,
                    age_group=age_group,
                )
        if not characters:
            # default narrator
            characters["narrator"] = CharacterPlan(
                id="narrator",
                display_name="Narrator",
                role="narrator",
                voice_id="narrator_pa_01",
                gender="unknown",
                age_group="adult",
            )
        return list(characters.values())

    def _detect_action(self, paragraph: str) -> Optional[str]:
        paragraph_lower = paragraph.lower()
        for action, keywords in ACTION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in paragraph_lower:
                    return action
        return None

    def _detect_props(self, paragraph: str) -> List[str]:
        props = []
        if any(word in paragraph.lower() for word in ["tabla", "dholak", "harmonium"]):
            props.append("musical_instruments")
        if "book" in paragraph.lower() or "kitab" in paragraph.lower():
            props.append("book")
        if "kitchen" in paragraph.lower() or "langar" in paragraph.lower():
            props.append("kitchen_utensils")
        if "cricket" in paragraph.lower():
            props.extend(["cricket_bat", "cricket_ball"])
        return props

    # ------------------------------------------------------------------
    # Misc helpers
    # ------------------------------------------------------------------
    def _infer_title(self, lines: Iterable[str], idx: int) -> str:
        for line in lines:
            clean = line.strip()
            if clean and not clean.endswith(":"):
                return clean[:60]
        return f"Scene {idx}"

    def _estimate_duration(self, narration: Iterable[Dict[str, str]]) -> float:
        total_chars = sum(len(entry["text"]) for entry in narration)
        # assume 14 characters per second speech speed
        return round(max(6.0, total_chars / 14.0), 1)

    def _detect_language(self, text: str) -> str:
        punjabi_chars = sum(1 for ch in text if self._is_punjabi(ch))
        if punjabi_chars > len(text) * 0.2:
            return "pa"
        return "en"

    def _normalize_identifier(self, name: str) -> str:
        return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") or "character"

    def _infer_role(self, name: str) -> tuple[str, str, str, str]:
        name_lower = name.lower()
        for role, config in ROLE_KEYWORDS.items():
            for keyword in config["keywords"]:
                if keyword in name_lower:
                    return (
                        role,
                        config.get("gender", "unknown"),
                        config.get("age", "adult"),
                        config.get("voice", DEFAULT_VOICES.get(config.get("gender", "unknown"), "narrator_pa_01")),
                    )
        # fallback
        gender = "female" if any(word in name_lower for word in ["kaur", "bibi", "madam"]) else "male"
        fallback = ROLE_FALLBACK.get(gender, ROLE_FALLBACK["unknown"])
        return ("supporting", gender, fallback["age"], fallback["voice"])

    @staticmethod
    def _is_punjabi(ch: str) -> bool:
        return PUNJABI_RANGE[0] <= ord(ch) <= PUNJABI_RANGE[1]


def plan_story(text: str, story_id: str = "story") -> Dict[str, object]:
    planner = StoryScenePlanner(story_id=story_id)
    return planner.plan(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate scene plan from story text")
    parser.add_argument("input", type=Path, help="Input story text file")
    parser.add_argument("--story-id", default="story", help="Identifier for the story")
    parser.add_argument("--output", type=Path, help="Optional path to save JSON plan")
    args = parser.parse_args()

    text = args.input.read_text(encoding="utf-8")
    plan = plan_story(text=text, story_id=args.story_id)

    if args.output:
        args.output.write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Scene plan saved to {args.output}")
    else:
        print(json.dumps(plan, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
