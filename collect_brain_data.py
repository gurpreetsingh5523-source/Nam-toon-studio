"""
Script to collect all brain_*.txt files and prepare them for LLM/AI training.
Outputs a single merged file: all_brain_data.txt
"""
import glob
from pathlib import Path

WORKSPACE = Path(__file__).parent
output_file = WORKSPACE / "all_brain_data.txt"

brain_files = sorted(WORKSPACE.glob("brain_*.txt"))

with open(output_file, "w", encoding="utf-8") as out:
    for bf in brain_files:
        out.write(f"===== {bf.name} =====\n")
        with open(bf, "r", encoding="utf-8") as f:
            out.write(f.read())
            out.write("\n\n")

print(f"Merged {len(brain_files)} brain files into {output_file}")
