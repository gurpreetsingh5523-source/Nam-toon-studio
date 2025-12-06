#!/usr/bin/env python3
"""Auto-run AmritPerceptionBrain for any video missing a perception report."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Iterable, List

from amrit_perception_brain import AmritPerceptionBrain

VIDEO_DIRS = ["realistic_videos", "training_videos", "smart_videos", "realistic_videos/exports"]
REPORT_DIR = "perception_reports"


class PerceptionScheduler:
    def __init__(self, workspace: Path, frame_stride: int, max_frames: int, audio_window: float) -> None:
        self.workspace = workspace
        self.report_dir = self.workspace / REPORT_DIR
        self.report_dir.mkdir(exist_ok=True)
        self.video_dirs = [self.workspace / d for d in VIDEO_DIRS]
        self.brain = AmritPerceptionBrain(workspace=self.workspace)
        self.frame_stride = frame_stride
        self.max_frames = max_frames
        self.audio_window = audio_window

    def _existing_report_for(self, video_path: Path) -> Path:
        return self.report_dir / f"{video_path.stem}_perception.json"

    def _video_iter(self) -> Iterable[Path]:
        for directory in self.video_dirs:
            if not directory.exists():
                continue
            yield from sorted(directory.glob("*.mp4"))

    def find_pending_videos(self) -> List[Path]:
        pending: List[Path] = []
        for video in self._video_iter():
            report = self._existing_report_for(video)
            if not report.exists():
                pending.append(video)
        return pending

    def process_video(self, video: Path) -> None:
        print(f"\n🎯 Analysing video: {video.relative_to(self.workspace)}")
        report = self.brain.analyze_video(
            str(video),
            frame_stride=self.frame_stride,
            max_frames=self.max_frames,
            audio_window=self.audio_window,
            save_report=True,
        )
        if report and report.get("report_path"):
            print(f"✅ Perception report ready: {report['report_path']}")
        else:
            print("⚠️ Perception run finished but no report path returned.")

    def run_once(self) -> int:
        pending = self.find_pending_videos()
        if not pending:
            print("✨ All tracked videos already have perception reports.")
            return 0
        print(f"🔍 Videos without perception reports: {len(pending)}")
        for video in pending:
            self.process_video(video)
        return len(pending)

    def watch(self, interval_seconds: int) -> None:
        print(f"👀 Watching for new videos every {interval_seconds}s")
        try:
            while True:
                processed = self.run_once()
                if processed:
                    self._refresh_metrics()
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print("\n👋 Stopped watching")

    def _refresh_metrics(self) -> None:
        metrics_path = self.workspace / "rahbar_operational_metrics.json"
        if not metrics_path.exists():
            return
        try:
            with open(metrics_path, "r", encoding="utf-8") as handle:
                metrics = json.load(handle)
        except Exception:
            return
        reports_total = len(list(self.report_dir.glob("*.json")))
        metrics.setdefault("perception", {})["reports_total"] = reports_total
        metrics["perception"].pop("status", None)
        try:
            with open(metrics_path, "w", encoding="utf-8") as handle:
                json.dump(metrics, handle, indent=2, ensure_ascii=False)
            print("🧾 Updated rahbar_operational_metrics.json with new perception totals.")
        except Exception as exc:
            print(f"⚠️ Could not update metrics: {exc}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run perception on missing videos.")
    parser.add_argument("--workspace", default=Path(__file__).parent, type=Path)
    parser.add_argument("--watch", action="store_true", help="Keep watching for new videos")
    parser.add_argument("--interval", type=int, default=300, help="Watch interval in seconds")
    parser.add_argument("--frame-stride", type=int, default=10)
    parser.add_argument("--max-frames", type=int, default=200)
    parser.add_argument("--audio-window", type=float, default=1.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scheduler = PerceptionScheduler(
        workspace=args.workspace,
        frame_stride=args.frame_stride,
        max_frames=args.max_frames,
        audio_window=args.audio_window,
    )
    if args.watch:
        scheduler.watch(args.interval)
    else:
        processed = scheduler.run_once()
        if processed:
            scheduler._refresh_metrics()


if __name__ == "__main__":
    main()
