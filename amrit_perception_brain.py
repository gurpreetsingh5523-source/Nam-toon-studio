#!/usr/bin/env python3
"""Amrit perception brain that fuses YOLO vision with simple audio heuristics."""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import numpy as np

try:  # Optional dependencies handled gracefully
    import cv2  # type: ignore
except ImportError:  # pragma: no cover - dependency optional at runtime
    cv2 = None

try:
    from ultralytics import YOLO  # type: ignore
except ImportError:  # pragma: no cover
    YOLO = None

try:
    import librosa  # type: ignore
except ImportError:  # pragma: no cover
    librosa = None


class AmritPerceptionBrain:
    """Runs lightweight perception on rendered videos."""

    def __init__(
        self,
        model_path: str = "yolov8x.pt",
        device: Optional[str] = None,
        workspace: Optional[Path] = None,
        confidence: float = 0.25,
    ) -> None:
        self.workspace = Path(workspace) if workspace else Path(__file__).parent
        self.model_path = model_path
        self.confidence = confidence
        self.device = device
        self.reports_dir = self.workspace / "perception_reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)

        self.vision_ready = False
        self.audio_ready = librosa is not None
        self.vision_model = None

        self._init_vision_model()
        if not self.audio_ready:
            print("[warn] Librosa not available, audio perception disabled.")

    def _init_vision_model(self) -> None:
        if YOLO is None:
            print("[warn] Ultralytics YOLO not installed. Run 'pip install ultralytics'.")
            return
        if cv2 is None:
            print("[warn] OpenCV not installed. Run 'pip install opencv-python'.")
            return
        try:
            self.vision_model = YOLO(self.model_path)
            if self.device:
                try:
                    self.vision_model.to(self.device)
                except Exception as exc:  # pragma: no cover - best effort GPU selection
                    print(f"[warn] Could not move YOLO to {self.device}: {exc}")
            self.vision_ready = True
            print("[info] Vision model ready for perception analysis.")
        except Exception as exc:  # pragma: no cover - load failure rarely tested
            print(f"[warn] Failed to load YOLO model: {exc}")

    def analyze_video(
        self,
        video_path: str,
        frame_stride: int = 10,
        max_frames: Optional[int] = 200,
        audio_window: float = 1.0,
        audio_sample_rate: Optional[int] = None,
        save_report: bool = True,
    ) -> Optional[Dict[str, Any]]:
        if cv2 is None:
            print("[warn] OpenCV unavailable, skipping perception analysis.")
            return None

        video_file = Path(video_path)
        if not video_file.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")

        cap = cv2.VideoCapture(str(video_file))  # type: ignore[arg-type]
        if not cap.isOpened():
            print(f"[warn] Could not open video: {video_path}")
            return None

        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        duration_seconds = frame_count / fps if fps else None

        timeline: List[Dict[str, Any]] = []
        object_counts: Counter[str] = Counter()
        frame_index = 0
        processed_frames = 0
        sample_stride = max(1, frame_stride)
        start_time = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_index % sample_stride != 0:
                frame_index += 1
                continue

            visuals = self._process_frame(frame) if self.vision_ready else []
            timestamp_ms = float((frame_index / fps) * 1000.0) if fps else 0.0

            for obj in visuals:
                object_counts[obj["label"]] += 1

            timeline.append(
                {
                    "frame_index": frame_index,
                    "timestamp_ms": timestamp_ms,
                    "objects": visuals,
                }
            )

            processed_frames += 1
            frame_index += 1

            if max_frames is not None and processed_frames >= max_frames:
                break

        cap.release()

        analysis_duration = time.time() - start_time
        visual_summary = self._summarize_visuals(object_counts, processed_frames)

        audio_summary = self._analyze_audio_stream(
            video_file,
            window_seconds=audio_window,
            sample_rate=audio_sample_rate,
        )

        report: Dict[str, Any] = {
            "metadata": {
                "created_at": datetime.utcnow().isoformat() + "Z",
                "video_path": str(video_file),
            },
            "video": {
                "frame_count": frame_count,
                "fps": fps,
                "duration_seconds": duration_seconds,
                "analysis_frame_stride": sample_stride,
                "analysis_frames": processed_frames,
                "analysis_time_seconds": analysis_duration,
            },
            "vision": visual_summary,
            "audio": audio_summary,
            "timeline": timeline,
        }

        if save_report:
            report_path = self._save_report(video_file, report)
            report["report_path"] = str(report_path)
            print(f"[info] Perception report saved: {report_path}")

        return report

    def _process_frame(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        if not self.vision_ready or self.vision_model is None:
            return []

        detections: List[Dict[str, Any]] = []
        try:
            results = self.vision_model(frame, verbose=False, conf=self.confidence)
            if not results:
                return detections
            result = results[0]
            for box in getattr(result, "boxes", []):
                try:
                    cls_idx = int(box.cls)
                    label = result.names.get(cls_idx, str(cls_idx)) if hasattr(result, "names") else str(cls_idx)
                    confidence = float(box.conf)
                    x1, y1, x2, y2 = [float(v) for v in box.xyxy[0].tolist()]
                    width = max(0.0, x2 - x1)
                    height = max(0.0, y2 - y1)
                    action = self._infer_action(label, width, height)
                    detections.append(
                        {
                            "label": label,
                            "confidence": round(confidence, 4),
                            "bbox": [round(x1, 2), round(y1, 2), round(x2, 2), round(y2, 2)],
                            "action": action,
                        }
                    )
                except Exception:  # pragma: no cover - skip malformed detection
                    continue
        except Exception as exc:
            print(f"[warn] Frame perception failed: {exc}")
        return detections

    @staticmethod
    def _infer_action(label: str, width: float, height: float) -> str:
        if label != "person" or height <= 0.0:
            return "static"
        aspect_ratio = height / max(width, 1.0)
        if aspect_ratio < 1.2:
            return "dynamic"
        if aspect_ratio > 2.4:
            return "upright"
        return "walking"

    @staticmethod
    def _summarize_visuals(object_counts: Counter[str], frames_sampled: int) -> Dict[str, Any]:
        if frames_sampled == 0:
            return {
                "objects_detected": 0,
                "unique_labels": [],
                "top_labels": [],
            }
        top_labels = [
            {
                "label": label,
                "count": count,
                "ratio": round(count / frames_sampled, 4),
            }
            for label, count in object_counts.most_common()
        ]
        return {
            "objects_detected": sum(object_counts.values()),
            "unique_labels": list(object_counts.keys()),
            "top_labels": top_labels,
        }

    def _analyze_audio_stream(
        self,
        video_file: Path,
        window_seconds: float,
        sample_rate: Optional[int],
    ) -> Optional[Dict[str, Any]]:
        if not self.audio_ready or librosa is None:
            return None
        try:
            audio, sr = librosa.load(str(video_file), sr=sample_rate, mono=True)
        except Exception as exc:
            print(f"[warn] Audio extraction failed: {exc}")
            return None

        window = max(1, int(window_seconds * sr))
        segments = []
        for start in range(0, len(audio), window):
            end = min(len(audio), start + window)
            chunk = audio[start:end]
            if chunk.size == 0:
                continue
            segment = self._classify_audio_chunk(chunk, sr)
            segment.update(
                {
                    "start_time": round(start / sr, 3),
                    "end_time": round(end / sr, 3),
                }
            )
            segments.append(segment)

        return self._summarize_audio_segments(segments)

    @staticmethod
    def _classify_audio_chunk(chunk: np.ndarray, sample_rate: int) -> Dict[str, Any]:
        rms = float(np.sqrt(np.mean(np.square(chunk))))
        epsilon = 1e-9
        zcr = float(np.mean(librosa.feature.zero_crossing_rate(chunk))) if librosa else 0.0
        centroid = (
            float(np.mean(librosa.feature.spectral_centroid(y=chunk, sr=sample_rate)))
            if librosa
            else 0.0
        )

        label = "background"
        if rms < 0.002:
            label = "silence"
        elif centroid > 4000 and rms > 0.01:
            label = "bell_like"
        elif centroid < 1500 and rms > 0.01:
            label = "engine_like"
        elif 1500 <= centroid <= 3500 and rms > 0.01:
            label = "water_or_activity"

        return {
            "label": label,
            "rms": round(rms + epsilon, 6),
            "zcr": round(zcr, 6),
            "centroid": round(centroid, 2),
        }

    @staticmethod
    def _summarize_audio_segments(segments: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
        segments_list = list(segments)
        if not segments_list:
            return {"segments": [], "summary": {}}

        counts = Counter(seg["label"] for seg in segments_list)
        total = sum(counts.values())
        summary = {
            "top_labels": [
                {
                    "label": label,
                    "count": count,
                    "ratio": round(count / total, 4),
                }
                for label, count in counts.most_common()
            ],
            "avg_rms": round(float(np.mean([seg["rms"] for seg in segments_list])), 6),
        }

        return {
            "segments": segments_list,
            "summary": summary,
        }

    def _save_report(self, video_file: Path, report: Dict[str, Any]) -> Path:
        report_name = f"{video_file.stem}_perception.json"
        report_path = self.reports_dir / report_name
        with open(report_path, "w", encoding="utf-8") as handle:
            json.dump(report, handle, indent=2)
        return report_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Amrit perception analysis on a video.")
    parser.add_argument("video", help="Path to the MP4 video to analyse")
    parser.add_argument("--stride", type=int, default=10, help="Frame stride for perception")
    parser.add_argument("--max-frames", type=int, default=200, help="Maximum frames to analyse")
    parser.add_argument("--no-save", action="store_true", help="Do not write a JSON report")
    args = parser.parse_args()

    brain = AmritPerceptionBrain()
    report = brain.analyze_video(
        args.video,
        frame_stride=args.stride,
        max_frames=args.max_frames,
        save_report=not args.no_save,
    )

    if report:
        print(json.dumps({k: v for k, v in report.items() if k != "timeline"}, indent=2))
        if "timeline" in report:
            print(f"[info] Timeline entries: {len(report['timeline'])}")


if __name__ == "__main__":
    main()
