"""Offline novel-to-cinema minimal pipeline (TXT only).

Reads `novel.txt`, splits into scenes, extracts simple characters, and writes
`colab/scenes.json` describing scenes and dialogues.

Note: PDF support removed by request. Keep your story in `novel.txt` (UTF‑8).
This script is dependency-light and uses no external APIs.
"""
from pathlib import Path
import re
import json
import random
import sys


def read_text_file(path: Path) -> str:
    return path.read_text(encoding='utf-8')


# PDF support deliberately removed. Keep input in novel.txt only.


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
    # Extract Punjabi names (Gurmukhi script) - look for proper nouns
    # Common Punjabi names in this story: ਕੁਲਵੰਤ, ਅਮਨਦੀਪ, ਦਲਜੀਤ, ਦਲੀਪ, ਰਮਨਦੀਪ, ਜਸਪ੍ਰੀਤ
    
    # Hardcoded character list for this story (narrator + main characters)
    # In future: use NER or pattern matching for Punjabi names
    known_chars = ['ਕੁਲਵੰਤ', 'ਅਮਨਦੀਪ', 'ਅਮਨ', 'ਦਲਜੀਤ', 'ਦਲੀਪ', 'ਰਮਨਦੀਪ', 'ਜਸਪ੍ਰੀਤ']
    
    # Check which characters appear in text
    found = []
    for char in known_chars:
        if char in text:
            found.append(char)
    
    # Always include narrator as first character
    if 'ਕੁਲਵੰਤ' in found:
        # ਕੁਲਵੰਤ is the narrator
        chars = ['ਕੁਲਵੰਤ (Narrator)']
        found.remove('ਕੁਲਵੰਤ')
        chars.extend(found[:max_char-1])
    else:
        chars = ['Narrator'] + found[:max_char-1]
    
    if not chars or len(chars) == 0:
        chars = ['Narrator', 'Character']
    
    return chars


def sentences_from_text(text: str):
    # naive sentence split
    sents = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sents if len(s.strip()) > 0]


def build_scene_json(scenes, characters):
    out = {'scenes': []}
    
    # Narrator is always first character (if exists)
    narrator = characters[0] if characters else 'Narrator'
    
    for i, s in enumerate(scenes):
        sents = sentences_from_text(s)
        dialogues = []
        
        # Smart assignment: most sentences go to narrator, unless dialogue markers present
        for j, sent in enumerate(sents):
            # Check if sentence looks like direct speech (has quotes or dialogue markers)
            is_dialogue = any(marker in sent for marker in ['"', '"', '"', ':', '—', 'ਕਹਿ', 'ਬੋਲ', 'ਆਖ'])
            
            if is_dialogue and len(characters) > 1:
                # Assign to a character (cycle through non-narrator characters)
                char_idx = (j % (len(characters) - 1)) + 1
                char = characters[char_idx] if char_idx < len(characters) else narrator
            else:
                # Narrator speaks
                char = narrator
            
            vol = 1.0
            if '?' in sent or '।' in sent:  # Question or exclamation
                emotion = 'question'
            elif '!' in sent:
                emotion = 'exclaim'
                vol = 1.05
            else:
                emotion = 'neutral'
            
            dialogues.append({'character': char, 'text': sent, 'volume': vol, 'emotion': emotion})
        
        # Scene metadata based on content
        scene_title = f'Scene {i+1}'
        if i == 0:
            scene_title = 'ਸ਼ੁਰੂਆਤ (Introduction)'
        elif 'ਵਿਆਹ' in s:
            scene_title = 'ਵਿਆਹ (Marriage)'
        elif 'ਅੱਗ' in s or 'ਜਲ' in s:
            scene_title = 'ਹਾਦਸਾ (Tragedy)'
        elif 'ਹਸਪਤਾਲ' in s or 'ਮੌਤ' in s:
            scene_title = 'ਮੌਤ (Death)'
        
        out['scenes'].append({'scene_id': str(i), 'title': scene_title, 'dialogues': dialogues})
    
    return out


def main():
    base = Path(__file__).parent
    txt = base.parent / 'novel.txt'
    if txt.exists():
        print('Reading novel.txt')
        text = read_text_file(txt)
    else:
        print('No novel.txt found. Please create a UTF-8 text file at project root named novel.txt with your story.')
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
