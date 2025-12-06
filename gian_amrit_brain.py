#!/usr/bin/env python3
"""GIAN-Amrit integrated perception brain for deep scene understanding."""

from __future__ import annotations

import json
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import numpy as np

try:  # Optional dependencies loaded lazily
    import cv2  # type: ignore
except ImportError:  # pragma: no cover - runtime optional
    cv2 = None

try:
    from ultralytics import YOLO  # type: ignore
except ImportError:  # pragma: no cover
    YOLO = None

try:
    import librosa  # type: ignore
except ImportError:  # pragma: no cover
    librosa = None


class GianKnowledgeBase:
    """ਕੌਮ ਅਤੇ ਸੰਸਕਾਰ ਨਾਲ ਜੁੜਿਆ ਗਿਆਨ."""

    def __init__(self) -> None:
        self.knowledge = self._load_punjabi_knowledge()
        self.context_memory: List[Dict[str, Any]] = []
        self.learning_log: List[Dict[str, Any]] = []

    def _load_punjabi_knowledge(self) -> Dict[str, Any]:
        """ਪੰਜਾਬੀ ਸੰਸਕਾਰ ਨੂੰ ਬੇਸਲਾਈਨ ਵਜੋਂ ਲੋਡ ਕਰੋ."""
        return {
            "objects_meaning": {
                "car": {
                    "types": ["ਕਾਰ", "ਗੱਡੀ", "ਵਾਹਨ"],
                    "contexts": ["road", "garage", "wash", "accident"],
                    "actions": ["driving", "parking", "washing", "repairing"],
                    "associated_sounds": ["engine", "horn", "tire_squeal", "door_close"],
                    "cultural_significance": "ਤਰੱਕੀ ਅਤੇ ਮਿਹਨਤ ਦਾ ਪ੍ਰਤੀਕ",
                },
                "person": {
                    "types": ["ਬੰਦਾ", "ਔਰਤ", "ਬੱਚਾ", "ਬੁੱਢਾ"],
                    "contexts": ["walking", "working", "talking", "waiting"],
                    "actions": ["walking", "running", "standing", "sitting", "working"],
                    "associated_sounds": ["talking", "footsteps", "laughter", "clapping"],
                    "cultural_significance": "ਸੰਗਤ ਅਤੇ ਸਮਾਜ ਦਾ ਹਿੱਸਾ",
                },
                "bicycle": {
                    "types": ["ਸਾਈਕਲ", "ਸਵਾਰੀ"],
                    "contexts": ["road", "path", "college", "village"],
                    "actions": ["riding", "parking", "repairing"],
                    "associated_sounds": ["bell", "chain", "pedaling"],
                    "cultural_significance": "ਸਾਦਗੀ ਅਤੇ ਸਵਾਸਥ ਦਾ ਪ੍ਰਤੀਕ",
                },
            },
            "scenes_meaning": {
                "road_scene": {
                    "typical_objects": ["car", "person", "bicycle", "traffic light", "tree"],
                    "typical_activities": ["driving", "walking", "crossing", "waiting"],
                    "typical_sounds": ["traffic", "horn", "engine", "footsteps"],
                    "mood": ["busy", "active", "noisy"],
                    "story_potential": ["journey", "accident", "meeting", "chase"],
                },
                "car_wash_scene": {
                    "typical_objects": ["car", "person", "water", "brush", "hose"],
                    "typical_activities": ["washing", "cleaning", "drying", "paying"],
                    "typical_sounds": ["water_splash", "brush_scrub", "engine_off", "talking"],
                    "mood": ["wet", "clean", "service"],
                    "story_potential": ["service", "waiting", "conversation"],
                },
                "village_road": {
                    "typical_objects": ["tractor", "person", "bicycle", "animal", "tree"],
                    "typical_activities": ["ploughing", "walking", "cycling", "grazing"],
                    "typical_sounds": ["birds", "tractor", "bell", "animal_sounds"],
                    "mood": ["peaceful", "slow", "natural"],
                    "story_potential": ["village_life", "hard_work", "simplicity"],
                },
            },
            "story_templates": {
                "car_journey": [
                    "departure_preparation",
                    "road_travel",
                    "obstacle_encountered",
                    "solution_applied",
                    "destination_reached",
                ],
                "daily_life": [
                    "morning_activity",
                    "work_activity",
                    "social_interaction",
                    "evening_return",
                    "family_time",
                ],
                "service_scene": [
                    "arrival_at_service",
                    "service_in_progress",
                    "waiting_activity",
                    "service_completion",
                    "departure",
                ],
            },
        }

    def understand_objects(self, detected_objects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """ਡਿਟੈਕਟ ਕੀਤੇ ਆਬਜੈਕਟਾਂ ਤੋਂ ਸੀਨ ਨੂੰ ਸਮਝੋ."""
        understanding: Dict[str, Any] = {
            "primary_objects": [],
            "scene_type": "unknown",
            "possible_stories": [],
            "missing_elements": [],
            "cultural_context": "",
        }

        obj_names = [obj["object"] for obj in detected_objects]
        understanding["scene_type"] = self._infer_scene_type(obj_names)

        for obj_name in obj_names:
            obj_info = self.knowledge["objects_meaning"].get(obj_name)
            if obj_info:
                understanding["primary_objects"].append(
                    {
                        "name": obj_name,
                        "meaning": obj_info["cultural_significance"],
                        "possible_actions": obj_info["actions"],
                    }
                )

        scene_info = self.knowledge["scenes_meaning"].get(understanding["scene_type"], {})
        understanding["possible_stories"] = scene_info.get("story_potential", [])

        typical_objects = scene_info.get("typical_objects", [])
        if typical_objects:
            missing = set(typical_objects) - set(obj_names)
            understanding["missing_elements"] = sorted(missing)

        return understanding

    def _infer_scene_type(self, objects: List[str]) -> str:
        counts: Dict[str, int] = {}
        for obj in objects:
            counts[obj] = counts.get(obj, 0) + 1

        if "car" in counts and "person" in counts:
            if counts.get("car", 0) > 2:
                return "road_scene"
            if "water" in counts or "brush" in counts:
                return "car_wash_scene"

        if "tractor" in counts or "animal" in counts:
            return "village_road"

        if counts.get("person", 0) > 3:
            return "crowded_scene"

        return "general_scene"

    def learn_from_context(
        self, visual_data: Dict[str, Any], audio_data: Dict[str, Any], timestamp: float
    ) -> Dict[str, Any]:
        """ਨਵੇਂ ਮੋਮੈਂਟ ਤੋਂ ਸਿੱਖਣਾ."""
        entry = {
            "timestamp": datetime.fromtimestamp(timestamp).isoformat(),
            "visual_summary": visual_data,
            "audio_summary": audio_data,
            "inferred_scene": self._infer_scene_type(
                [obj["object"] for obj in visual_data.get("objects", [])]
            ),
            "patterns_found": [],
        }
        self.context_memory.append(entry)
        if len(self.context_memory) > 1000:
            self.context_memory = self.context_memory[-1000:]
        return entry


class GianVisionProcessor:
    """ਗਿਆਨ-ਅਧਾਰਿਤ ਵਿਜ਼ਨ ਪ੍ਰੋਸੈਸਰ."""

    def __init__(self, model_path: str = "yolov8x.pt", device: Optional[str] = None) -> None:
        self.model_path = model_path
        self.device = device
        self.vision_model = None
        self.model_available = False
        self.knowledge = GianKnowledgeBase()
        self.frame_history: List[Any] = []
        self.object_tracking: Dict[str, Dict[str, Any]] = {}
        self.prev_frame_gray: Optional[np.ndarray] = None
        self._load_model()

    def _load_model(self) -> None:
        if YOLO is None:
            print("[warn] YOLO unavailable, vision running in mock mode.")
            return
        if cv2 is None:
            print("[warn] OpenCV unavailable, vision running in mock mode.")
            return
        try:
            self.vision_model = YOLO(self.model_path)
            if self.device:
                try:
                    self.vision_model.to(self.device)
                except Exception as exc:  # pragma: no cover
                    print(f"[warn] Could not move YOLO to {self.device}: {exc}")
            self.model_available = True
            print("[info] GIAN vision model ready.")
        except Exception as exc:  # pragma: no cover
            print(f"[warn] Failed to load YOLO model: {exc}")

    def process_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        detections = self._detect_objects(frame)
        enhanced = self._add_movement_context(detections, frame)
        understanding = self.knowledge.understand_objects(enhanced)
        self._update_object_tracking(enhanced)
        return {
            "raw_detections": detections,
            "enhanced_detections": enhanced,
            "understanding": understanding,
            "tracking_summary": self._tracking_summary(),
            "frame_timestamp": time.time(),
        }

    def _detect_objects(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        if not self.model_available or self.vision_model is None:
            return self._mock_detections(frame)

        detections: List[Dict[str, Any]] = []
        try:
            results = self.vision_model(frame, verbose=False)
            if not results:
                return detections
            result = results[0]
            for box in getattr(result, "boxes", []):
                cls_idx = int(box.cls)
                label = result.names.get(cls_idx, str(cls_idx)) if hasattr(result, "names") else str(cls_idx)
                x1, y1, x2, y2 = [float(v) for v in box.xyxy[0].tolist()]
                confidence = float(box.conf)
                width = max(0.0, x2 - x1)
                height = max(0.0, y2 - y1)
                action = self._infer_action(label, width, height, y2)
                detections.append(
                    {
                        "object": label,
                        "confidence": confidence,
                        "position": [x1, y1, x2, y2],
                        "center": [(x1 + x2) / 2.0, (y1 + y2) / 2.0],
                        "size": {"width": width, "height": height, "area": width * height},
                        "action_guess": action,
                        "frame_portion": self._frame_portion(x1, y1, x2, y2),
                    }
                )
        except Exception as exc:  # pragma: no cover
            print(f"[warn] Vision inference failed: {exc}")
        return detections

    @staticmethod
    def _infer_action(label: str, width: float, height: float, bottom_y: float) -> str:
        if label == "person" and width > 0.0:
            aspect_ratio = height / width
            if aspect_ratio > 3.0:
                return "standing"
            if aspect_ratio > 1.5:
                return "walking"
            return "sitting"
        if label == "car":
            return "parked" if bottom_y > 400 else "moving"
        if label == "bicycle":
            return "riding/parked"
        return "present"

    @staticmethod
    def _frame_portion(x1: float, y1: float, x2: float, y2: float) -> str:
        center_x = (x1 + x2) / 2.0
        center_y = (y1 + y2) / 2.0
        horizontal = "left" if center_x < 320 else "right"
        vertical = "top" if center_y < 240 else "bottom"
        return f"{vertical}-{horizontal}"

    def _add_movement_context(
        self, detections: List[Dict[str, Any]], frame: np.ndarray
    ) -> List[Dict[str, Any]]:
        if cv2 is None:
            for det in detections:
                det["movement"] = "unknown"
            return detections

        current_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.prev_frame_gray is None:
            self.prev_frame_gray = current_gray
            for det in detections:
                det["movement"] = "first_frame"
            return detections

        flow = cv2.calcOpticalFlowFarneback(
            self.prev_frame_gray, current_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0
        )

        for det in detections:
            x1, y1, x2, y2 = map(int, det["position"])
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)
            if 0 <= center_x < flow.shape[1] and 0 <= center_y < flow.shape[0]:
                fx, fy = flow[center_y, center_x]
                magnitude = float(np.sqrt(fx * fx + fy * fy))
                if magnitude > 1.0:
                    det["movement"] = f"moving_{magnitude:.1f}"
                    det["movement_direction"] = float(np.arctan2(fy, fx) * 180.0 / np.pi)
                else:
                    det["movement"] = "stationary"
            else:
                det["movement"] = "unknown"

        self.prev_frame_gray = current_gray
        return detections

    def _update_object_tracking(self, detections: List[Dict[str, Any]]) -> None:
        now = time.time()
        for det in detections:
            obj_id = f"{det['object']}_{det['center'][0]:.0f}_{det['center'][1]:.0f}"
            track = self.object_tracking.get(obj_id)
            if not track:
                self.object_tracking[obj_id] = {
                    "object_type": det["object"],
                    "first_seen": now,
                    "last_seen": now,
                    "positions": [det["center"]],
                    "actions": [det["action_guess"]],
                    "duration": 0.0,
                }
            else:
                track["last_seen"] = now
                track["positions"].append(det["center"])
                track["actions"].append(det["action_guess"])
                track["duration"] = now - track["first_seen"]

        expired = [oid for oid, track in self.object_tracking.items() if now - track["last_seen"] > 5.0]
        for oid in expired:
            del self.object_tracking[oid]

    def _tracking_summary(self) -> Dict[str, Any]:
        summary = {
            "total_objects_tracked": len(self.object_tracking),
            "object_types": {},
            "longest_presence": 0.0,
            "most_active_object": None,
        }
        for obj_id, track in self.object_tracking.items():
            obj_type = track["object_type"]
            summary["object_types"][obj_type] = summary["object_types"].get(obj_type, 0) + 1
            if track["duration"] > summary["longest_presence"]:
                summary["longest_presence"] = track["duration"]
                summary["most_active_object"] = obj_id
        return summary

    def _mock_detections(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        h, w = frame.shape[:2]
        base_objects = [
            {
                "object": "car",
                "confidence": 0.85,
                "position": [w * 0.2, h * 0.6, w * 0.4, h * 0.8],
                "center": [w * 0.3, h * 0.7],
                "action_guess": "parked",
            },
            {
                "object": "person",
                "confidence": 0.78,
                "position": [w * 0.5, h * 0.5, w * 0.7, h * 0.9],
                "center": [w * 0.6, h * 0.7],
                "action_guess": "walking",
            },
            {
                "object": "bicycle",
                "confidence": 0.65,
                "position": [w * 0.7, h * 0.6, w * 0.9, h * 0.8],
                "center": [w * 0.8, h * 0.7],
                "action_guess": "parked",
            },
        ]
        for obj in base_objects:
            x1, y1, x2, y2 = obj["position"]
            obj["size"] = {"width": x2 - x1, "height": y2 - y1, "area": (x2 - x1) * (y2 - y1)}
            obj["frame_portion"] = self._frame_portion(x1, y1, x2, y2)
            obj["movement"] = "mock"
        return base_objects


class GianAudioProcessor:
    """ਗਿਆਨ-ਅਧਾਰਿਤ ਆਡੀਓ ਪ੍ਰੋਸੈਸਿੰਗ."""

    def __init__(self) -> None:
        self.librosa_available = librosa is not None
        if not self.librosa_available:
            print("[warn] Librosa not available, audio context will use mock output.")
        self.knowledge = GianKnowledgeBase()
        self.audio_context_history: List[Dict[str, Any]] = []

    def process_audio(
        self, audio_data: Optional[np.ndarray] = None, visual_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if audio_data is None or not self.librosa_available:
            return self._mock_audio_analysis(visual_context)

        try:
            rms = float(np.sqrt(np.mean(np.square(audio_data))))
            centroid = float(np.mean(np.abs(audio_data)))
            sound_type = self._classify_sound(rms, centroid, visual_context)
            meaning = self._sound_meaning(sound_type, visual_context)
            analysis = {
                "sound_type": sound_type,
                "loudness": rms,
                "brightness": centroid,
                "meaning": meaning,
                "matches_visual_context": self._context_match(sound_type, visual_context),
                "timestamp": time.time(),
            }
            self.audio_context_history.append(analysis)
            if len(self.audio_context_history) > 1000:
                self.audio_context_history = self.audio_context_history[-1000:]
            return analysis
        except Exception as exc:  # pragma: no cover
            print(f"[warn] Audio processing failed: {exc}")
            return self._mock_audio_analysis(visual_context)

    def _classify_sound(
        self, rms: float, spectral_centroid: float, visual_context: Optional[Dict[str, Any]]
    ) -> str:
        if visual_context:
            obj_types = [obj["object"] for obj in visual_context.get("objects", [])]
            if "car" in obj_types:
                if rms > 0.2:
                    return "engine_running"
                if 0.1 < rms <= 0.2:
                    return "car_door"
                return "car_idle"
            if "person" in obj_types and rms > 0.15:
                return "human_activity"

        if rms > 0.3:
            return "loud_noise"
        if rms > 0.15:
            return "moderate_activity"
        if rms > 0.05:
            return "background_activity"
        return "silence"

    def _sound_meaning(
        self, sound_type: str, visual_context: Optional[Dict[str, Any]]
    ) -> Dict[str, str]:
        meanings = {
            "engine_running": {"meaning": "ਕਾਰ ਚੱਲ ਰਹੀ ਹੈ", "mood": "active"},
            "car_door": {"meaning": "ਕਾਰ ਦਾ ਦਰਵਾਜ਼ਾ", "mood": "transition"},
            "human_activity": {"meaning": "ਲੋਕਾਂ ਦੀ ਹਲਚਲ", "mood": "social"},
            "loud_noise": {"meaning": "ਤੇਜ਼ ਆਵਾਜ਼", "mood": "intense"},
            "background_activity": {"meaning": "ਆਮ ਗਤੀਵਿਧੀ", "mood": "normal"},
            "silence": {"meaning": "ਸ਼ਾਂਤੀ", "mood": "calm"},
        }
        meaning = meanings.get(sound_type, {"meaning": "ਅਣਜਾਣ", "mood": "unknown"})

        if visual_context:
            scene = visual_context.get("scene_type")
            if scene == "village_road" and sound_type == "silence":
                meaning["meaning"] = "ਪਿੰਡ ਦੀ ਸ਼ਾਂਤ ਸਵੇਰ"
            if scene == "road_scene" and sound_type == "engine_running":
                meaning["meaning"] = "ਸੜਕ 'ਤੇ ਆਵਾਜਾਈ"
        return meaning

    def _context_match(self, sound_type: str, visual_context: Optional[Dict[str, Any]]) -> str:
        if not visual_context:
            return "no_visual_context"
        typical_matches = {
            "car_wash_scene": {"water_splash", "brushing", "talking"},
            "road_scene": {"engine_running", "horn", "traffic"},
            "village_road": {"birds", "animal_sounds", "tractor"},
        }
        scene = visual_context.get("scene_type", "unknown")
        if scene in typical_matches:
            return "plausible" if sound_type in typical_matches[scene] else "possible"
        return "unknown"

    def _mock_audio_analysis(self, visual_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        import random

        sound_type = random.choice(
            ["engine_running", "car_door", "human_activity", "background_activity", "silence"]
        )
        return {
            "sound_type": sound_type,
            "loudness": random.uniform(0.0, 0.5),
            "brightness": random.uniform(0.0, 1.0),
            "meaning": {"meaning": f"Mock: {sound_type}", "mood": "test"},
            "matches_visual_context": "mock",
            "timestamp": time.time(),
        }


class GianAmritBrain:
    """ਇਕਜੁੱਟ ਵਿਜ਼ਨ, ਆਡੀਓ ਅਤੇ ਗਿਆਨ ਵਾਲਾ ਦਿਮਾਗ."""

    def __init__(self, workspace: Optional[Path] = None) -> None:
        print("🧠 Initializing GIAN-Amrit Brain...")
        self.workspace = Path(workspace) if workspace else Path(__file__).parent
        self.vision = GianVisionProcessor()
        self.audio = GianAudioProcessor()
        self.knowledge = GianKnowledgeBase()
        self.memory: List[Dict[str, Any]] = []
        self.patterns_recognized: Dict[str, Dict[str, Any]] = {}
        self.current_story: Optional[Dict[str, Any]] = None
        self.scene_transitions: List[str] = []
        print("✅ GIAN system ready for perception.")

    def perceive(self, video_source: Any = 0) -> List[Dict[str, Any]]:
        if cv2 is None:
            raise RuntimeError("OpenCV required for live perception.")

        cap = cv2.VideoCapture(video_source)
        frame_count = 0
        print(f"\n👁️ GIAN perceiving input: {video_source}")
        print("   Press 'q' to quit, 's' to save story, 'l' for learning summary")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("✅ Video ended")
                break

            frame_count += 1
            visual = self.vision.process_frame(frame)
            audio = self.audio.process_audio(visual_context=visual.get("understanding"))
            fused = self._fuse_perceptions(visual, audio, frame_count)
            story_update = self._update_story(fused)
            self._learn(fused)

            display = self._overlay(frame, visual, fused, story_update)
            cv2.imshow("GIAN Amrit Brain", display)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                print("👋 Stopping perception...")
                break
            if key == ord("s"):
                self._save_story()
            if key == ord("l"):
                self._print_learning_summary()

        cap.release()
        cv2.destroyAllWindows()
        self._final_report()
        return self.memory

    def _fuse_perceptions(
        self, visual: Dict[str, Any], audio: Dict[str, Any], frame_num: int
    ) -> Dict[str, Any]:
        fused = {
            "frame": frame_num,
            "timestamp": time.time(),
            "visual_summary": {
                "objects_detected": len(visual.get("raw_detections", [])),
                "primary_objects": [obj["object"] for obj in visual.get("raw_detections", [])],
                "scene_type": visual.get("understanding", {}).get("scene_type", "unknown"),
                "story_potentials": visual.get("understanding", {}).get("possible_stories", []),
            },
            "audio_summary": {
                "sound_type": audio.get("sound_type", "unknown"),
                "sound_meaning": audio.get("meaning", {}).get("meaning", "unknown"),
                "matches_scene": audio.get("matches_visual_context", "unknown"),
            },
            "integrated_understanding": {
                "whats_happening": self._infer_activity(visual, audio),
                "emotional_tone": self._infer_emotion(visual, audio),
                "next_likely_event": self._predict_next_event(visual),
                "cultural_context": self._cultural_context(visual),
            },
        }
        self.memory.append(fused)
        return fused

    def _infer_activity(self, visual: Dict[str, Any], audio: Dict[str, Any]) -> str:
        scene = visual.get("understanding", {}).get("scene_type", "")
        sound = audio.get("sound_type", "")
        if scene == "road_scene" and sound == "engine_running":
            return "ਕਾਰ ਸੜਕ 'ਤੇ ਚੱਲ ਰਹੀ ਹੈ"
        if scene == "car_wash_scene" and "water" in sound:
            return "ਕਾਰ ਧੋਈ ਜਾ ਰਹੀ ਹੈ"
        if "person" in str(visual.get("understanding", {}).get("primary_objects", [])):
            moving = any("moving" in str(obj.get("movement", "")) for obj in visual.get("enhanced_detections", []))
            return "ਲੋਕ ਇੱਧਰ-ਉੱਧਰ ਜਾ ਰਹੇ ਹਨ" if moving else "ਲੋਕ ਖੜ੍ਹੇ ਹਨ"
        return "ਆਮ ਗਤੀਵਿਧੀ"

    def _infer_emotion(self, visual: Dict[str, Any], audio: Dict[str, Any]) -> str:
        sound_mood = audio.get("meaning", {}).get("mood", "neutral")
        activity_level = sum(
            1 for obj in visual.get("enhanced_detections", []) if "moving" in str(obj.get("movement", ""))
        )
        visual_mood = "active" if activity_level > 2 else "moderate" if activity_level > 0 else "calm"
        if sound_mood == "intense" or visual_mood == "active":
            return "ਤੀਬਰ/ਵਿਅਸਤ"
        if sound_mood == "calm" and visual_mood == "calm":
            return "ਸ਼ਾਂਤ"
        return "ਸਧਾਰਨ"

    def _predict_next_event(self, visual: Dict[str, Any]) -> str:
        tracking = visual.get("tracking_summary", {})
        objects = tracking.get("object_types", {})
        if "car" in objects and "person" in objects:
            return "ਸ਼ਾਇਦ ਕੋਈ ਕਾਰ ਵਿੱਚ ਬੈਠੇਗਾ"
        if objects.get("person", 0) > 1:
            return "ਲੋਕ ਗੱਲਬਾਤ ਕਰਨਗੇ"
        return "ਜਾਰੀ ਰਹੇਗਾ"

    def _cultural_context(self, visual: Dict[str, Any]) -> str:
        scene = visual.get("understanding", {}).get("scene_type", "")
        if scene == "village_road":
            return "ਪਿੰਡ ਦੀ ਸਾਦਗੀ"
        if scene == "road_scene":
            return "ਸ਼ਹਿਰੀ ਤਰੱਕੀ"
        if "car" in str(visual.get("understanding", {}).get("primary_objects", [])):
            return "ਆਧੁਨਿਕ ਜੀਵਨ"
        return "ਆਮ ਜੀਵਨ"

    def _update_story(self, fused: Dict[str, Any]) -> Dict[str, Any]:
        if self.current_story is None:
            self.current_story = {
                "title": "ਦੇਖੀ ਗਈ ਕਹਾਣੀ",
                "start_time": time.time(),
                "scenes": [],
                "characters": {},
                "current_scene": None,
            }

        current_scene_type = fused["visual_summary"]["scene_type"]
        scenes = self.current_story["scenes"]
        if not scenes or scenes[-1]["type"] != current_scene_type:
            new_scene = {
                "type": current_scene_type,
                "start_frame": fused["frame"],
                "description": fused["integrated_understanding"]["whats_happening"],
                "emotional_tone": fused["integrated_understanding"]["emotional_tone"],
                "duration": 0,
            }
            scenes.append(new_scene)
            self.current_story["current_scene"] = new_scene
            if len(scenes) > 1:
                self.scene_transitions.append(f"{scenes[-2]['type']}->{current_scene_type}")

        if self.current_story["current_scene"]:
            self.current_story["current_scene"]["duration"] += 1

        for obj in fused["visual_summary"]["primary_objects"]:
            self.current_story["characters"][obj] = self.current_story["characters"].get(obj, 0) + 1
        return self._finalize_story_update()

    def _finalize_story_update(self) -> Dict[str, Any]:
        assert self.current_story is not None
        main_characters = sorted(
            self.current_story["characters"].items(), key=lambda item: item[1], reverse=True
        )[:3]
        return {
            "current_scene": self.current_story["current_scene"],
            "total_scenes": len(self.current_story["scenes"]),
            "main_characters": main_characters,
        }

    def _learn(self, fused: Dict[str, Any]) -> None:
        scene = fused["visual_summary"]["scene_type"]
        sound = fused["audio_summary"]["sound_type"]
        key = f"{scene}+{sound}"
        pattern = self.patterns_recognized.get(key)
        if not pattern:
            self.patterns_recognized[key] = {
                "count": 1,
                "first_seen": time.time(),
                "typical_emotion": fused["integrated_understanding"]["emotional_tone"],
                "typical_activity": fused["integrated_understanding"]["whats_happening"],
            }
        else:
            pattern["count"] += 1

    def _overlay(
        self,
        frame: np.ndarray,
        visual: Dict[str, Any],
        fused: Dict[str, Any],
        story_update: Dict[str, Any],
    ) -> np.ndarray:
        display = frame.copy()
        h, w = display.shape[:2]

        for det in visual.get("raw_detections", []):
            x1, y1, x2, y2 = map(int, det["position"])
            color = (0, 255, 0) if det["object"] == "person" else (255, 0, 0) if det["object"] == "car" else (0, 255, 255)
            cv2.rectangle(display, (x1, y1), (x2, y2), color, 2)
            label = det["object"]
            if det.get("action_guess"):
                label += f" | {det['action_guess']}"
            if det.get("movement") and det["movement"] != "stationary":
                label += f" | {det['movement']}"
            cv2.putText(display, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        y_offset = 30
        overlay_lines = [
            f"Scene: {fused['visual_summary']['scene_type']}",
            f"Happening: {fused['integrated_understanding']['whats_happening']}",
            f"Sound: {fused['audio_summary']['sound_meaning']}",
            f"Mood: {fused['integrated_understanding']['emotional_tone']}",
            f"Story scenes: {story_update['total_scenes']}",
        ]
        for text in overlay_lines:
            cv2.putText(display, text, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(display, text, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
            y_offset += 25

        cv2.rectangle(display, (0, h - 40), (w, h), (0, 0, 0), -1)
        status = (
            f"GIAN Brain | Frames: {fused['frame']} | Memory: {len(self.memory)} | Patterns: {len(self.patterns_recognized)}"
        )
        cv2.putText(display, status, (10, h - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        context = fused["integrated_understanding"]["cultural_context"]
        if len(context) > 40:
            context = context[:37] + "..."
        cv2.putText(display, context, (w - 400, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 100), 1)
        return display

    def _save_story(self) -> None:
        if not self.current_story:
            print("❌ No story to save")
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gian_story_{timestamp}.json"
        path = self.workspace / filename
        story = {
            **self.current_story,
            "end_time": time.time(),
            "total_frames": len(self.memory),
            "scene_transitions": self.scene_transitions,
            "patterns_recognized": self.patterns_recognized,
            "gian_version": "1.0",
        }
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(story, handle, indent=2, ensure_ascii=False)
        print(f"✅ Story saved: {path}")

    def _print_learning_summary(self) -> None:
        print("\n📚 GIAN Learning Summary")
        print("=" * 40)
        print(f"Total memories: {len(self.memory)}")
        print(f"Patterns: {len(self.patterns_recognized)}")
        print(f"Transitions: {len(self.scene_transitions)}")
        if self.patterns_recognized:
            print("Top patterns:")
            for key, data in sorted(
                self.patterns_recognized.items(), key=lambda item: item[1]["count"], reverse=True
            )[:5]:
                print(f"  {key}: {data['count']} times")
                print(f"    Activity: {data['typical_activity']}")
        if self.current_story:
            chars = list(self.current_story["characters"].keys())[:3]
            print(f"Current story scenes: {len(self.current_story['scenes'])}")
            print(f"Main characters: {chars}")

    def _final_report(self) -> None:
        print("\n📊 GIAN Final Analysis Report")
        print("=" * 60)
        if not self.memory:
            print("No data collected")
            return
        scene_counts = Counter(m["visual_summary"]["scene_type"] for m in self.memory)
        print("Scenes observed:")
        for scene, count in scene_counts.most_common():
            print(f"  {scene}: {count} frames")
        sound_counts = Counter(m["audio_summary"]["sound_type"] for m in self.memory)
        print("Sounds detected:")
        for sound, count in sound_counts.most_common():
            print(f"  {sound}: {count} times")
        if self.current_story:
            duration = self.current_story.get("end_time", time.time()) - self.current_story["start_time"]
            print("Story summary:")
            print(f"  Scenes: {len(self.current_story['scenes'])}")
            print(f"  Duration: {duration:.1f}s")
            print(f"  Characters: {', '.join(list(self.current_story['characters'].keys())[:5])}")
        print("\n✅ Analysis complete")


def main() -> None:
    print(
        """
    ╔══════════════════════════════════════════════════╗
    ║         🧠 GIAN-AMRIT INTEGRATED BRAIN          ║
    ║      Amrit's Vision + Rahbar's Understanding    ║
    ║      ਦੇਖਦਾ ਹੈ, ਸਮਝਦਾ ਹੈ, ਕਹਾਣੀ ਬਣਾਉਂਦਾ ਹੈ        ║
    ╚══════════════════════════════════════════════════╝
    """
    )
    import argparse

    parser = argparse.ArgumentParser(description="Run GIAN-Amrit perception on video or camera.")
    parser.add_argument("source", help="Video file path or camera index", nargs="?", default="0")
    parser.add_argument("--no-display", action="store_true", help="Skip OpenCV window (analysis only)")
    args = parser.parse_args()

    source: Any = args.source
    if isinstance(source, str) and source.isdigit():
        source = int(source)

    brain = GianAmritBrain()
    if cv2 is None or args.no_display:
        raise RuntimeError("Display mode requires OpenCV.")
    brain.perceive(source)


if __name__ == "__main__":
    main()
