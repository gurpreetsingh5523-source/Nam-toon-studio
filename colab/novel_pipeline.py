"""Offline novel-to-cinema minimal pipeline.

Reads `novel.txt` (preferred) or `novel.pdf` (if PyPDF2 available), splits into scenes,
extracts simple characters, and writes `colab/scenes.json` describing scenes and dialogues.

This is intentionally dependency-light and works without any external APIs.
"""
from pathlib import Path
import re
import json
import random
import sys


def read_text_file(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def extract_text_from_pdf(path: Path) -> str:
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(str(path))
        pages = [p.extract_text() or '' for p in reader.pages]
        return '\n\n'.join(pages)
    except Exception:
        raise RuntimeError('PyPDF2 not available or PDF parsing failed')


def split_into_scenes(text: str):
    # split on Chapter headings or double-newline blocks longer than 200 chars
    chapters = re.split(r'(?im)^chapter\s+\d+|\n\s*\n', text)
    scenes = []
    for c in chapters:
        s = c.strip()
        if not s:
            continue
        # further split by scene separators (lines with '---' or 'Scene')
        parts = re.split(r'(?m)^---+$|(?i:scene)\b', s)
        for p in parts:
            q = p.strip()
            if len(q) > 40:
                scenes.append(q)
    return scenes


def simple_character_extraction(text: str, max_char=6):
    # heuristics: find capitalized words (2+ letters) that appear often
    tokens = re.findall(r"\b[A-Z][a-z]{1,20}\b", text)
    freq = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1
    sorted_names = sorted(freq.items(), key=lambda x: -x[1])
    names = [n for n, _ in sorted_names[:max_char]]
    if not names:
        names = ['Narrator', 'Protagonist']
    return names


def sentences_from_text(text: str):
    # naive sentence split
    sents = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sents if len(s.strip()) > 0]


def build_scene_json(scenes, characters):
    out = {'scenes': []}
    for i, s in enumerate(scenes):
        sents = sentences_from_text(s)
        dialogues = []
        # assign sentences to characters round-robin with some randomness
        for j, sent in enumerate(sents):
            char = characters[(j) % len(characters)]
            vol = 1.0
            if '?' in sent:
                emotion = 'question'
            elif '!' in sent:
                emotion = 'exclaim'
                vol = 1.05
            else:
                emotion = 'neutral'
            dialogues.append({'character': char, 'text': sent, 'volume': vol, 'emotion': emotion})
        out['scenes'].append({'scene_id': str(i), 'title': f'Scene {i+1}', 'dialogues': dialogues})
    return out


def main():
    base = Path(__file__).parent
    txt = base.parent / 'novel.txt'
    pdf = base.parent / 'novel.pdf'
    if txt.exists():
        print('Reading novel.txt')
        text = read_text_file(txt)
    elif pdf.exists():
        print('Attempting to read novel.pdf')
        try:
            text = extract_text_from_pdf(pdf)
        except Exception as e:
            print('PDF read failed:', e)
            sys.exit(1)
    else:
        print('No novel.txt or novel.pdf found. Please add novel.txt with the story.')
        sys.exit(1)

    scenes = split_into_scenes(text)
    chars = simple_character_extraction(text)
    print(f'Found {len(scenes)} scenes and characters: {chars}')
    scene_json = build_scene_json(scenes, chars)
    out = base / 'scenes.json'
    out.write_text(json.dumps(scene_json, ensure_ascii=False, indent=2))
    print('Wrote', out)


if __name__ == '__main__':
    main()
