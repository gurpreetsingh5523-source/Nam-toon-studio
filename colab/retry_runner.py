#!/usr/bin/env python3
"""
Retry Runner
Reads `brain_memory/retry_instructions.json` and for each instruction applies simple overrides
to a scenes JSON (adds `audio_instructions` such as lowering music volume) and then invokes
the master builder to re-render (or dry-run) the modified scenes file.

This is a light-weight orchestrator to apply Master recommendations automatically.
"""
import json
import os
import sys
from pathlib import Path
import subprocess

ROOT = Path(__file__).parent.parent
BRAINDIR = ROOT / 'brain_memory'


def load_retries():
    f = BRAINDIR / 'retry_instructions.json'
    if not f.exists():
        print('No retry_instructions.json found. Nothing to do.')
        return []
    try:
        return json.loads(f.read_text(encoding='utf-8'))
    except Exception as e:
        print('Failed to read retry_instructions.json:', e)
        return []


def save_retries(retries: list):
    f = BRAINDIR / 'retry_instructions.json'
    try:
        with f.open('w', encoding='utf-8') as fh:
            json.dump(retries, fh, ensure_ascii=False, indent=2)
    except Exception as e:
        print('Failed to save retry_instructions.json:', e)


def apply_retry_to_scene(original_scene_path: str, out_path: str, retries: list):
    """Produce a modified scenes file with audio_instructions applied.
    For now supports only `lower_music_volume` recommendation by attaching
    `audio_instructions: { synthesize_music: { volume: x }}` to scene.
    """
    p = Path(original_scene_path)
    if not p.exists():
        raise FileNotFoundError(original_scene_path)

    data = json.loads(p.read_text(encoding='utf-8'))
    scenes = data.get('scenes', [])

    # Build a map of recommendations by scene
    rec_map = {}
    for r in retries:
        sid = r.get('scene_id')
        recs = r.get('recommendations', [])
        if not sid:
            continue
        rec_map.setdefault(sid, []).extend(recs)

    # Apply recommendations
    for sc in scenes:
        sid = sc.get('scene_id')
        if sid in rec_map:
            for rec in rec_map[sid]:
                if rec.get('action') == 'lower_music_volume':
                    mult = float(rec.get('suggested_multiplier', 0.6))
                    # Attach synth fallback to ensure renderer can act
                    sc.setdefault('audio_instructions', {})['synthesize_music'] = {
                        'volume': float(mult) * 0.2,  # scale expected absolute volume
                        'emotion': 'auto',
                        'f1': 220.0,
                        'f2': 293.0
                    }

    outp = Path(out_path)
    outp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Wrote modified scenes file: {outp}')
    return str(outp)


def increment_and_prune_retries(retries: list, applied_scene_ids: list, max_attempts: int = 3) -> list:
    """Increment attempts for applied retries and prune entries that reached max_attempts.

    Returns the updated list to be saved back to retry_instructions.json
    and prints pruning actions.
    """
    updated = []
    for r in retries:
        sid = r.get('scene_id')
        if sid in applied_scene_ids:
            r['attempts'] = int(r.get('attempts', 0)) + 1
            if r['attempts'] >= max_attempts:
                print(f"Pruning retry for scene {sid} after {r['attempts']} attempts")
                # Optionally, move to history or log (not implemented)
                continue
        updated.append(r)
    return updated


def run_master_builder(scenes_file: str, dry_run: bool = True):
    cmd = [sys.executable, str(ROOT / 'colab' / 'master_builder.py'), '--scenes', scenes_file]
    if dry_run:
        cmd.append('--dry-run')
    print('Invoking master_builder:', ' '.join(cmd))
    subprocess.run(cmd)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Apply Master retry instructions and re-run scenes')
    parser.add_argument('--scenes', type=str, default='temp_scene.json', help='Original scenes JSON')
    parser.add_argument('--out', type=str, default='temp_scene_retry.json', help='Output modified scenes JSON')
    parser.add_argument('--no-dry-run', dest='dry', action='store_false', help='Run full render (not recommended for heavy runs)')
    args = parser.parse_args()

    retries = load_retries()
    if not retries:
        print('No retries to apply. Exiting.')
        return

    modified = apply_retry_to_scene(args.scenes, args.out, retries)
    run_master_builder(modified, dry_run=args.dry)


if __name__ == '__main__':
    main()
