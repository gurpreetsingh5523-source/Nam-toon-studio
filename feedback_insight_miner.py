#!/usr/bin/env python3
"""Analyze user feedback and surface repeating improvement themes."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List

NEGATIVE_KEYWORDS = ["cartoon", "fake", "voice", "slow", "lag", "speed", "real", "realistic", "lighting", "background", "duplicate", "same"]
POSITIVE_KEYWORDS = ["real", "smooth", "voice", "animation", "music", "color", "lighting", "diversity"]


class FeedbackInsightMiner:
    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace
        self.feedback_file = self.workspace / "user_feedback.json"
        self.output_file = self.workspace / "feedback_insights_report.json"
        self.summary_file = self.workspace / "feedback_insights_summary.md"

    def load_feedback(self) -> List[Dict[str, any]]:
        if not self.feedback_file.exists():
            raise FileNotFoundError(f"Feedback file not found: {self.feedback_file}")
        with open(self.feedback_file, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, list):
            raise ValueError("user_feedback.json should contain a list of feedback entries")
        return data

    def analyse(self, feedback: Iterable[Dict[str, any]]) -> Dict[str, any]:
        negative_counter: Counter[str] = Counter()
        positive_counter: Counter[str] = Counter()
        theme_map: defaultdict[str, List[str]] = defaultdict(list)

        for entry in feedback:
            text = str(entry.get("feedback", "")).lower()
            entry_id = entry.get("video_id", "unknown")
            for keyword in NEGATIVE_KEYWORDS:
                if keyword in text:
                    negative_counter[keyword] += 1
                    theme_map[keyword].append(entry_id)
            for keyword in POSITIVE_KEYWORDS:
                if keyword in text:
                    positive_counter[keyword] += 1

        recommendations = []
        for keyword, count in negative_counter.most_common():
            recommendations.append({
                "theme": keyword,
                "occurrences": count,
                "videos": sorted(set(theme_map[keyword])),
                "suggested_action": self._suggest_action(keyword)
            })

        insights = {
            "total_feedback": negative_counter.total() + positive_counter.total(),
            "negative_signals": negative_counter.most_common(),
            "positive_signals": positive_counter.most_common(),
            "recommendations": recommendations
        }
        return insights

    @staticmethod
    def _suggest_action(keyword: str) -> str:
        mapping = {
            "cartoon": "Increase real-photo usage and perception coverage.",
            "fake": "Audit generator outputs and enforce real-photo pipeline.",
            "voice": "Review TTS settings and regenerate tracks.",
            "slow": "Profile rendering pipeline and cache heavy assets.",
            "lag": "Profile rendering pipeline and cache heavy assets.",
            "speed": "Profile rendering pipeline and cache heavy assets.",
            "real": "Ensure perception scheduler runs for realism verification.",
            "realistic": "Ensure perception scheduler runs for realism verification.",
            "lighting": "Adjust renderer lighting presets and include variation.",
            "background": "Expand background library and ensure variety.",
            "duplicate": "Improve diversity selection logic and photo rotations.",
            "same": "Improve diversity selection logic and photo rotations."
        }
        return mapping.get(keyword, "Investigate feedback samples and plan correction.")

    def save_report(self, insights: Dict[str, any]) -> None:
        with open(self.output_file, "w", encoding="utf-8") as handle:
            json.dump(insights, handle, indent=2, ensure_ascii=False)
        print(f"✅ Saved detailed insights: {self.output_file}")

        lines = [
            "# Feedback Insights Summary",
            "",
            f"Total signals analysed: {insights.get('total_feedback', 0)}",
            "",
            "## Top Negative Themes"
        ]
        for theme, count in insights.get("negative_signals", [])[:10]:
            lines.append(f"- {theme}: {count}")
        lines.append("\n## Recommended Actions")
        for rec in insights.get("recommendations", [])[:10]:
            lines.append(f"- {rec['theme']}: {rec['suggested_action']} (videos: {', '.join(rec['videos'])})")
        with open(self.summary_file, "w", encoding="utf-8") as handle:
            handle.write("\n".join(lines))
        print(f"✅ Saved summary: {self.summary_file}")

    def run(self) -> None:
        feedback = self.load_feedback()
        if not feedback:
            print("⚠️ No feedback entries found.")
            return
        insights = self.analyse(feedback)
        self.save_report(insights)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mine user feedback for recurring issues.")
    parser.add_argument("--workspace", default=Path(__file__).parent, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    miner = FeedbackInsightMiner(workspace=args.workspace)
    miner.run()


if __name__ == "__main__":
    main()
