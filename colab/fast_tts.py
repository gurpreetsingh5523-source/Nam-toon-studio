"""Fast parallel TTS generator with caching for Nam-toon Studio"""
from gtts import gTTS
from pathlib import Path
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

log = logging.getLogger("fast_tts")

CACHE_DIR = Path("audio/tts_cache")
CACHE_INDEX = CACHE_DIR / "index.json"

def setup_cache():
    """Create cache directory and load index"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if CACHE_INDEX.exists():
        return json.loads(CACHE_INDEX.read_text())
    return {}

def save_cache_index(index):
    """Save cache index"""
    CACHE_INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2))

def get_cache_key(text, lang='pa'):
    """Generate cache key from text"""
    return hashlib.md5(f"{lang}:{text}".encode('utf-8')).hexdigest()

def generate_tts_single(text, output_path, lang='pa', cache_index=None):
    """Generate single TTS with caching"""
    if cache_index is None:
        cache_index = {}
    
    # Check cache
    cache_key = get_cache_key(text, lang)
    if cache_key in cache_index:
        cached_path = CACHE_DIR / cache_index[cache_key]
        if cached_path.exists():
            # Copy from cache
            import shutil
            shutil.copy2(cached_path, output_path)
            log.debug(f"TTS cache hit: {output_path}")
            return True
    
    # Generate new
    try:
        tts = gTTS(text, lang=lang)
        tts.save(output_path)
        
        # Save to cache
        cache_filename = f"{cache_key}.mp3"
        cache_path = CACHE_DIR / cache_filename
        import shutil
        shutil.copy2(output_path, cache_path)
        cache_index[cache_key] = cache_filename
        
        log.debug(f"TTS generated: {output_path}")
        return True
    except Exception as e:
        log.error(f"TTS failed for {output_path}: {e}")
        return False

def generate_tts_parallel(dialogues, output_dir="audio", lang='pa', max_workers=5):
    """
    Generate TTS for multiple dialogues in parallel
    
    Args:
        dialogues: List of dicts with 'text' key
        output_dir: Output directory
        lang: Language code
        max_workers: Number of parallel workers
    
    Returns:
        List of output paths (same order as input)
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    cache_index = setup_cache()
    
    # Prepare tasks
    tasks = []
    for i, dialogue in enumerate(dialogues):
        output_path = output_dir / f"dialogue_{i}.mp3"
        tasks.append((i, dialogue['text'], output_path))
    
    # Run in parallel
    results = [None] * len(tasks)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_idx = {
            executor.submit(generate_tts_single, text, path, lang, cache_index): (idx, path)
            for idx, text, path in tasks
        }
        
        for future in as_completed(future_to_idx):
            idx, path = future_to_idx[future]
            try:
                success = future.result()
                results[idx] = str(path) if success else None
                if success:
                    log.info(f"✓ TTS {idx+1}/{len(tasks)}: {path.name}")
            except Exception as e:
                log.error(f"TTS task {idx} failed: {e}")
                results[idx] = None
    
    # Save updated cache
    save_cache_index(cache_index)
    
    return results

if __name__ == "__main__":
    # Test
    test_dialogues = [
        {"text": "ਹੈਲੋ, ਇਹ ਇੱਕ ਟੈਸਟ ਹੈ।"},
        {"text": "ਦੂਜੀ ਲਾਈਨ ਬੋਲ ਰਿਹਾ ਹਾਂ।"},
        {"text": "ਤੀਜੀ ਅਤੇ ਆਖਰੀ ਲਾਈਨ।"}
    ]
    
    logging.basicConfig(level=logging.INFO)
    results = generate_tts_parallel(test_dialogues, max_workers=3)
    print(f"\nGenerated {len([r for r in results if r])} / {len(results)} files")
    print("Results:", results)
