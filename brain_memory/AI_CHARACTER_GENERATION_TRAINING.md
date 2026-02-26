# 🎨 AMRIT'S AI CHARACTER GENERATION TRAINING
## How to Create Real Character Images (Not Simple Circles!)

**ਪਿਤਾ ਜੀ**, I understand now! You want **real AI-generated character pictures**, not simple colored circles! 🙏

---

## ❌ THE PROBLEM

### Current master_builder.py (WRONG):
```python
def _generate_avatar(name, size=256):
    """Generate a simple colored circle avatar with initial"""
    # Creates THIS: 🔵 (colored circle with letter)
    # NOT THIS: 👤 (realistic character portrait)
```

### What You See in Video:
- ❌ Simple colored circles with initials (like: **ਸ**)
- ❌ No face, no clothes, no personality
- ❌ Looks like placeholder/emoji, not real character

### What You WANT:
- ✅ Real AI-generated character portrait
- ✅ Punjabi person in traditional dress
- ✅ Expressive face showing emotion
- ✅ Like Sora/Runway ML quality

---

## ✅ THE SOLUTION: Use Stable Diffusion AI

### We Already Have It!
File: `render_with_ai_images.py` contains:
- ✅ Stable Diffusion v1.5 model
- ✅ Character prompt generation
- ✅ Image caching system
- ✅ Fallback for errors

### How It Works:

#### Step 1: Load AI Model
```python
from diffusers import StableDiffusionPipeline
import torch

device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    safety_checker=None
)
pipe = pipe.to(device)
pipe.enable_attention_slicing()  # For memory efficiency
```

#### Step 2: Create Character Prompt
```python
def create_character_prompt(character_name, emotion="neutral"):
    """Create AI prompt for character portrait"""
    
    # Analyze character name for gender/role
    name_lower = character_name.lower()
    
    # Base description
    if "kaur" in name_lower or any(w in name_lower for w in ['wife', 'mother', 'daughter']):
        base = "beautiful Punjabi woman wearing colorful salwar kameez with dupatta"
    else:
        base = "handsome Punjabi man wearing traditional kurta"
    
    # Add emotion
    emotion_map = {
        'happy': 'smiling warmly, joyful expression',
        'sad': 'melancholic expression, teary eyes',
        'angry': 'fierce expression, furrowed brows',
        'peaceful': 'serene calm face, gentle smile',
        'worried': 'concerned expression, worried look',
        'neutral': 'calm neutral expression'
    }
    emotion_desc = emotion_map.get(emotion, 'calm expression')
    
    # Full prompt
    prompt = f"{base}, {emotion_desc}, detailed portrait, realistic, traditional Punjabi style, warm lighting, high quality, 4k portrait photography"
    
    # Negative prompt (what to avoid)
    negative = "cartoon, anime, low quality, blurry, distorted, ugly, deformed"
    
    return prompt, negative
```

#### Step 3: Generate Image
```python
def generate_character_image(character_name, emotion="neutral", size=(512, 512)):
    """Generate AI character portrait"""
    
    # Create prompt
    prompt, negative_prompt = create_character_prompt(character_name, emotion)
    
    # Generate with Stable Diffusion
    with torch.no_grad():
        result = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=30,  # More steps = better quality
            guidance_scale=7.5,      # How closely to follow prompt
            height=size[1],
            width=size[0]
        )
    
    # Get image
    image = result.images[0]
    
    # Validate (check if not blank)
    arr = np.array(image)
    if arr.mean() < 5:
        raise ValueError("Generated blank image!")
    
    return image
```

#### Step 4: Cache Generated Images
```python
def get_or_generate_character(character_name, emotion="neutral"):
    """Get cached character or generate new one"""
    
    # Create cache key
    cache_key = f"{character_name}_{emotion}".replace(" ", "_")
    cache_path = Path(f"ai_assets/characters/{cache_key}.png")
    
    # Check cache
    if cache_path.exists():
        print(f"✅ Using cached: {cache_key}")
        return Image.open(cache_path)
    
    # Generate new
    print(f"🎨 Generating character: {character_name} ({emotion})")
    image = generate_character_image(character_name, emotion)
    
    # Save to cache
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(cache_path)
    print(f"💾 Cached: {cache_key}.png")
    
    return image
```

---

## 🔧 FIX FOR master_builder.py

### Replace Lines 283-312 (the _generate_avatar function):

**BEFORE (Simple Circles):**
```python
def _generate_avatar(name, size=256):
    """Generate a simple colored circle avatar with initial"""
    # ... creates colored circle ...
```

**AFTER (AI-Generated Characters):**
```python
def _generate_avatar_with_ai(name, emotion="neutral", size=512):
    """Generate AI character portrait using Stable Diffusion"""
    
    try:
        # Check if AI model available
        global _AI_PIPE
        if '_AI_PIPE' not in globals() or _AI_PIPE is None:
            print("🎨 Loading Stable Diffusion AI Model...")
            from diffusers import StableDiffusionPipeline
            import torch
            
            device = "cuda" if torch.cuda.is_available() else \
                     "mps" if torch.backends.mps.is_available() else "cpu"
            
            _AI_PIPE = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                safety_checker=None
            ).to(device)
            _AI_PIPE.enable_attention_slicing()
            print("✅ AI Model loaded!")
        
        # Create cache path
        cache_dir = Path("ai_assets/characters")
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_key = f"{name}_{emotion}".replace(" ", "_").replace("/", "_")
        cache_path = cache_dir / f"{cache_key}.png"
        
        # Check cache
        if cache_path.exists():
            log.info(f"✅ Using cached character: {name}")
            return Image.open(cache_path).resize((size, size))
        
        # Create prompt
        name_lower = name.lower()
        if "kaur" in name_lower or any(w in name_lower for w in ['woman', 'mother', 'daughter', 'wife']):
            base = "beautiful Punjabi woman wearing traditional salwar kameez with dupatta"
        else:
            base = "handsome Punjabi man wearing traditional kurta"
        
        emotion_map = {
            'happy': 'smiling warmly', 'sad': 'melancholic', 'angry': 'fierce',
            'peaceful': 'serene calm', 'joyful': 'very happy smiling',
            'neutral': 'calm gentle'
        }
        emotion_desc = emotion_map.get(emotion, 'calm')
        
        prompt = f"{base}, {emotion_desc} expression, detailed portrait, realistic, warm lighting, high quality"
        negative_prompt = "cartoon, anime, low quality, blurry, distorted"
        
        # Generate
        log.info(f"🎨 Generating AI character: {name}")
        with torch.no_grad():
            result = _AI_PIPE(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=25,
                guidance_scale=7.5,
                height=512,
                width=512
            )
        
        image = result.images[0]
        
        # Validate
        arr = np.array(image)
        if arr.mean() < 5:
            raise ValueError("Generated blank image")
        
        # Save and return
        image.save(cache_path)
        log.info(f"✅ Generated and cached: {cache_key}")
        return image.resize((size, size))
        
    except Exception as e:
        log.warning(f"⚠️ AI generation failed for {name}: {e}")
        log.warning(f"   Falling back to simple avatar")
        # Fallback to simple circle (existing code)
        return _generate_simple_avatar(name, size)

def _generate_simple_avatar(name, size=256):
    """Fallback: simple colored circle (old code)"""
    # Keep existing simple circle code as fallback
    hash_val = sum(ord(c) for c in name)
    hue = (hash_val % 360) / 360.0
    import colorsys
    rgb = colorsys.hsv_to_rgb(hue, 0.6, 0.9)
    color = tuple(int(c * 255) for c in rgb)
    
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    margin = 10
    draw.ellipse([margin, margin, size-margin, size-margin], 
                 fill=color + (220,), outline=(255, 255, 255, 255), width=4)
    initial = name[0].upper() if name else '?'
    try:
        font = _get_font(int(size * 0.5))
        bbox = draw.textbbox((0, 0), initial, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        tx = (size - tw) // 2
        ty = (size - th) // 2 - bbox[1]
        draw.text((tx, ty), initial, font=font, fill=(255, 255, 255, 255))
    except Exception:
        pass
    return img
```

---

## 📝 UPDATE CHARACTER GENERATION CALL

### Around Line 326-330:
```python
# BEFORE:
for char in all_characters:
    if char not in portraits:
        avatar = _generate_avatar(char)  # Old function
        
# AFTER:
for char in all_characters:
    if char not in portraits:
        # Get emotion from first dialogue of this character
        char_emotion = "neutral"
        for d in dialogues_scene1:
            if d.get('character') == char:
                char_emotion = d.get('emotion', 'neutral')
                break
        
        # Generate with AI
        avatar = _generate_avatar_with_ai(char, emotion=char_emotion, size=600)
```

---

## 🎯 WHAT THIS ACHIEVES

### Before (Current):
```
Video shows:
🔵 ਸ  ← Simple blue circle with letter "ਸ"
```

### After (With AI):
```
Video shows:
👤   ← Real Punjabi person portrait:
     - Traditional dress (kurta/salwar)
     - Expressive face showing emotion
     - Detailed realistic features
     - Warm lighting
```

---

## 🚀 INSTALLATION REQUIREMENTS

### Install Stable Diffusion:
```bash
pip install diffusers transformers accelerate
```

### First Run:
- Downloads ~4GB model (one time)
- Takes 2-3 minutes first time
- Cached locally for future use

### Subsequent Runs:
- Loads from cache in 10 seconds
- Generates new character in 5-10 seconds
- Caches each character for reuse

---

## 💡 SORA 2 COMPARISON

### What Sora Does:
1. Text-to-video generation
2. Creates full motion videos from text
3. Generates consistent characters across frames
4. Handles complex scenes with multiple elements

### What We Do (Similar Logic):
1. Text-to-image for characters (Stable Diffusion)
2. Compose images into video (MoviePy)
3. Cache characters for consistency
4. Mix with audio/music/effects

### Key Similarities:
- **Prompt Engineering**: Both use detailed text prompts
- **Style Consistency**: Both maintain character style
- **Quality Control**: Both validate output
- **Caching**: Both reuse generated assets

### Our Advantage:
- ✅ We control every step
- ✅ We can customize prompts
- ✅ We cache everything
- ✅ We mix Punjabi audio perfectly

---

## 📊 PERFORMANCE

### On M1/M2 Mac (MPS):
- Load model: ~10 seconds
- Generate character: ~5-10 seconds
- Total first time: ~15-20 seconds per character

### On NVIDIA GPU (CUDA):
- Load model: ~5 seconds
- Generate character: ~2-3 seconds
- Total first time: ~5-8 seconds per character

### On CPU (Fallback):
- Load model: ~30 seconds
- Generate character: ~30-60 seconds
- Use cached images to avoid regeneration!

---

## 🎓 AMRIT'S PROMISE

**ਪਿਤਾ ਜੀ**, I will now:

1. ✅ **Use Stable Diffusion** for all character images
2. ✅ **Generate realistic portraits** with emotions
3. ✅ **Cache images** so they load instantly next time
4. ✅ **Fallback to circles** only if AI fails
5. ✅ **Match Sora quality** for character consistency

**No more simple circles! Real AI-generated characters from now on!** 🎨

---

**Created**: November 3, 2025  
**Purpose**: Teach Amrit to use Stable Diffusion for character generation  
**Priority**: HIGH - This makes videos look professional  
**Status**: Ready to implement

---

**Next Step**: Apply this fix to `colab/master_builder.py` and regenerate video! 🚀
