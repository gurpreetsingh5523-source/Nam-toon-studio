# 🎬 AMRIT'S FULL SCENE GENERATION TRAINING
## Creating Complete Story Scenes (Not Just Portrait Heads!)

**ਪਿਤਾ ਜੀ**, you're absolutely right! We need FULL SCENES like Sora/Ghibli, not just head shots! 🙏

---

## ❌ THE CURRENT PROBLEM

### What We Generate Now:
```
🙍 Just character face/head
📐 512x512 portrait only
🚫 No background
🚫 No body/action
🚫 Static pose
```

### What's Wrong:
- **"Tootan wala khoo"** story needs:
  - ✅ Village well with mulberry trees
  - ✅ Children running and playing
  - ✅ Kids eating mulberries
  - ✅ Sunset over village
  - ✅ Nature scenes
  
- **Current system** only creates:
  - ❌ One character head
  - ❌ No environment
  - ❌ No actions/activities

---

## ✅ THE SOLUTION: Full Scene Generation

### Reference Styles (From Your Images):

**Image 1-4**: Anime/Ghibli Style
- Full character in environment
- Beautiful backgrounds
- Action poses (sitting, walking, playing)
- Natural lighting and atmosphere

**Image 5-6**: Historical Punjabi Settings
- Real Gurdwara/village scenes
- Multiple people
- Authentic architecture
- Cultural authenticity

**Image 7**: Traditional Activity
- Person doing action (reading)
- Period-appropriate setting
- Cultural context shown

---

## 🎨 NEW PROMPT STRUCTURE FOR FULL SCENES

### Scene 1: Village Well with Trees (Opening)
```python
scene_1_prompt = """
Anime style illustration, wide shot of old Punjabi village corner, 
ancient stone well in center with three large mulberry trees beside it,
trees heavy with purple mulberries (toot fruits), 
green leaves rustling in wind, 
sunlight rays filtering through branches,
peaceful morning atmosphere, 
Studio Ghibli art style, warm colors, detailed background,
no people visible yet, establishing shot,
4k quality, cinematic composition
"""

negative_prompt = """
cartoon, western style, modern buildings, cars, 
low quality, blurry, distorted, multiple wells
"""
```

### Scene 2: Children Running to Well
```python
scene_2_prompt = """
Anime style wide shot, group of 4-5 Punjabi village children 
running excitedly toward old village well,
children wearing colorful traditional clothes (kurta, salwar),
blue turbans on boys, dupattas on girls,
mulberry trees in background,
children's happy expressions, arms outstretched,
dust kicking up from their feet,
Studio Ghibli animation style, dynamic motion,
warm summer afternoon lighting, vibrant colors,
full body characters, rural Punjab village setting,
4k quality, detailed scene
"""
```

### Scene 3: Children Playing Around Well
```python
scene_3_prompt = """
Anime style wide scene, Punjabi village children playing near old well,
some children picking mulberries from trees,
others sitting on well's edge dangling feet,
one child climbing tree branch,
children laughing and sharing fruits,
wearing traditional colorful village clothes,
green mulberry trees providing shade,
sunlight dappled through leaves,
Studio Ghibli style, warm joyful atmosphere,
full body characters in various activities,
detailed background with village houses in distance,
4k quality, cinematic lighting
"""
```

### Scene 4: Children with Nature
```python
scene_4_prompt = """
Anime style scene, Punjabi village children sitting together 
under mulberry tree shade near well,
flock of birds flying overhead in blue sky,
squirrel climbing tree trunk,
children pointing and clapping at animals,
traditional village clothes, blue turbans,
peaceful coexistence of children and nature,
Studio Ghibli art style, warm colors,
full environmental scene showing harmony,
golden afternoon light, detailed nature elements,
4k quality, beautiful composition
"""
```

### Scene 5: Learning Friendship
```python
scene_5_prompt = """
Anime style close scene, two Punjabi village children at well,
one child drawing water with rope and bucket,
offering water to other child saying 'you drink first',
children in traditional dress, blue turbans,
caring expressions on faces,
old stone well visible, mulberry tree branches overhead,
Studio Ghibli emotional moment style,
warm lighting showing kindness and sharing,
medium shot showing characters and well,
detailed expressions and gestures,
4k quality, heartwarming scene
"""
```

### Scene 6: Sunset Closing
```python
scene_6_prompt = """
Anime style wide establishing shot, 
beautiful sunset over Punjabi village,
silhouette of old well and mulberry trees against orange sky,
children sitting on well edge in silhouette,
peaceful evening atmosphere,
Studio Ghibli nostalgic ending style,
warm golden hour lighting, purple and orange sky,
birds flying home in distance,
cinematic composition showing entire scene,
4k quality, emotional closing shot
"""
```

---

## 🎮 DIFFERENT ACTIVITIES (For Future Stories)

### Playing Hockey:
```python
hockey_prompt = """
Anime style action scene, Punjabi village children playing field hockey,
children in traditional clothes but active poses,
wooden hockey sticks, makeshift ball,
dust cloud from running, dynamic motion blur,
village field setting with trees in background,
Studio Ghibli sports animation style,
full body characters in action poses,
energetic atmosphere, warm lighting
"""
```

### Playing Kabaddi:
```python
kabaddi_prompt = """
Anime style dynamic scene, village children playing kabaddi,
raiders and defenders in traditional Punjabi clothes,
children grappling, running, diving,
village ground with spectators watching,
dust kicking up, intense action,
Studio Ghibli sports style with motion,
full body characters showing traditional game,
cultural authenticity, warm colors
"""
```

### Playing Football:
```python
football_prompt = """
Anime style sports scene, Punjabi village kids playing football,
makeshift goal posts, worn leather ball,
children in mix of traditional and sports wear,
running, kicking, celebrating,
village field with mulberry trees around,
Studio Ghibli dynamic action style,
dust clouds, motion blur, energetic poses,
golden afternoon light, 4k quality
"""
```

---

## 🔧 IMPLEMENTATION IN CODE

### New Function: `generate_full_scene_image()`

```python
def generate_full_scene_image(scene_data):
    """
    Generate FULL SCENE with environment, not just character portrait!
    
    This creates:
    - Complete backgrounds (villages, nature, buildings)
    - Characters IN environment doing actions
    - Wide/establishing shots
    - Cinematic composition
    """
    
    scene_num = scene_data['scene_number']
    location = scene_data.get('location', 'village')
    emotion = scene_data.get('emotion', 'neutral')
    dialogue = scene_data.get('dialogue', '')
    visual_notes = scene_data.get('visual_notes', '')
    
    # Cache key for this specific scene
    cache_key = f"scene_{scene_num}_{location}_{emotion}".replace(" ", "_")
    cache_path = Path(f"ai_assets/scenes/{cache_key}.png")
    
    # Check cache first
    if cache_path.exists():
        log.info(f"✅ Using cached scene: {cache_key}")
        return Image.open(cache_path)
    
    # Create SCENE prompt (not just character)
    prompt = create_scene_prompt(scene_data)
    negative_prompt = "portrait only, headshot, close-up face, no background, modern style, low quality, blurry"
    
    # Generate WIDE SCENE IMAGE
    log.info(f"🎬 Generating FULL SCENE: {scene_num}")
    
    with torch.no_grad():
        result = _AI_PIPE(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=30,  # More steps for quality
            guidance_scale=7.5,
            height=720,  # TALL for cinematic
            width=1280,  # WIDE for scenes
        )
    
    image = result.images[0]
    
    # Save to cache
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(cache_path)
    log.info(f"✅ Generated full scene: {cache_key}")
    
    return image

def create_scene_prompt(scene_data):
    """Create detailed prompt for FULL SCENE generation"""
    
    scene_num = scene_data['scene_number']
    dialogue = scene_data.get('dialogue', '')
    visual_notes = scene_data.get('visual_notes', '')
    location = scene_data.get('location', 'village')
    
    # Base style
    base_style = "Anime style illustration, Studio Ghibli art quality, cinematic composition, 4k quality"
    
    # Scene-specific prompts
    scene_prompts = {
        0: """wide establishing shot of old Punjabi village corner, 
              ancient stone well with three large mulberry trees,
              green leaves, purple mulberries visible,
              peaceful morning, sunlight through branches,
              no people, atmospheric scene""",
        
        1: """wide shot of village well with mulberry trees,
              beautiful detailed background, leaves moving in breeze,
              sunlight rays filtering through,
              peaceful afternoon atmosphere""",
        
        2: """dynamic scene of Punjabi children running and playing near village well,
              children wearing traditional colorful clothes,
              some picking mulberries from trees, others playing,
              full body characters in action,
              joyful expressions, mulberry trees background""",
        
        3: """wide scene showing harmony between children and nature,
              flock of birds flying, squirrel on tree,
              children clapping and pointing,
              peaceful coexistence, natural environment""",
        
        4: """medium shot of children sharing water at well,
              one child offering water to another,
              caring expressions, friendship moment,
              well and trees visible in background""",
        
        5: """wide sunset shot of village well and trees,
              children silhouettes sitting together,
              orange and purple sunset sky,
              nostalgic peaceful atmosphere,
              closing cinematic shot"""
    }
    
    # Get scene-specific details
    scene_desc = scene_prompts.get(scene_num, 
        f"{location} scene with children, traditional Punjabi village setting")
    
    # Combine
    full_prompt = f"{base_style}, {scene_desc}, warm colors, detailed environment, emotional storytelling"
    
    return full_prompt
```

---

## 📊 COMPARISON

### Old System (Just Portraits):
```
Input: Character name "ਸੁਨੇਹਾ"
Output: 512x512 head shot
Result: 🙍 Just face, no context
```

### New System (Full Scenes):
```
Input: Scene description with location, action, characters
Output: 1280x720 cinematic scene
Result: 🎬 Complete story frame
        - Environment (well, trees, village)
        - Characters doing actions
        - Atmospheric lighting
        - Story context visible
```

---

## 🎯 FOR "TOOTAN WALA KHOO" STORY

### What Each Scene Should Show:

**Scene 0 (Opening)**: 
- 🎬 Wide shot of village well
- 🌳 Three mulberry trees  
- ☀️ Morning light
- 🎨 Establishing atmosphere

**Scene 1 (Zoom)**:
- 🎬 Closer view of well
- 🍃 Leaves rustling
- ✨ Sunlight through branches
- 🎨 Building anticipation

**Scene 2 (Children Playing)**:
- 🎬 Wide action shot
- 👦👧 4-5 children full body
- 🏃 Running, picking fruits, playing
- 🎨 Joyful energy

**Scene 3 (Nature)**:
- 🎬 Environmental shot
- 🐦 Birds flying
- 🐿️ Squirrel climbing
- 🎨 Harmony theme

**Scene 4 (Friendship)**:
- 🎬 Medium emotional shot
- 💧 Water sharing moment
- 🤝 Caring gestures
- 🎨 Teaching moment

**Scene 5 (Sunset)**:
- 🎬 Wide cinematic closing
- 🌅 Sunset colors
- 👥 Children silhouettes
- 🎨 Nostalgic feeling

---

## 💡 KEY DIFFERENCES FROM PORTRAIT MODE

| Aspect | Portrait Mode (Old) | Scene Mode (New) |
|--------|-------------------|------------------|
| **Size** | 512x512 | 1280x720 (cinematic) |
| **Focus** | Character face only | Full environment |
| **Content** | Head/shoulders | Characters + background |
| **Action** | Static pose | Dynamic activities |
| **Context** | No story context | Complete story frame |
| **Style** | Portrait photo | Anime/Ghibli scene |
| **Reusability** | One character | Entire scene |

---

## 🚀 NEXT STEPS

1. **Replace portrait generation** with scene generation
2. **Generate 6 different scenes** for the story
3. **Each scene shows**:
   - Different location/angle
   - Different actions
   - Different lighting/time
   - Story progression

4. **Result**: Video becomes like animated movie!
   - Scene 1: Establishing shot
   - Scene 2: Action begins
   - Scene 3: Main activity
   - Scene 4: Emotional moment
   - Scene 5: Resolution
   - Scene 6: Closing shot

---

## 🎨 STYLE REFERENCES

Based on your images, we should aim for:

**Style 1**: Anime/Ghibli (Images 2-4)
- Soft colors
- Detailed backgrounds
- Expressive characters
- Natural environments

**Style 2**: Historical Documentary (Images 5-6)
- Authentic settings
- Cultural accuracy
- Period-appropriate details
- Black & white or sepia tone option

**Style 3**: Traditional Art (Image 7)
- Painting style
- Cultural context
- Activity-focused
- Artistic interpretation

---

## ✅ AMRIT'S NEW UNDERSTANDING

**Old thinking**: "Generate character portrait"  
**New thinking**: "Generate complete story scene"

**Old prompt**: "Punjabi person with turban"  
**New prompt**: "Punjabi village children playing near old well with mulberry trees, Studio Ghibli style"

**Old output**: 🙍 Face only  
**New output**: 🎬 Complete movie frame

---

**ਸੱਤ ਸ੍ਰੀ ਅਕਾਲ, ਪਿਤਾ ਜੀ!** 🙏

Now Amrit understands: We need to create **FULL SCENES** like Sora/Runway/Ghibli, not just character headshots!

Every scene should tell the story visually:
- Where it happens (location)
- What they're doing (action)  
- How it feels (atmosphere)
- Who's involved (characters in context)

**Next**: Implement scene generation system to replace portrait-only approach!

---

**Created**: November 3, 2025  
**Purpose**: Teach full scene generation vs portrait-only  
**Reference**: User's Ghibli-style and historical Punjabi images  
**Priority**: CRITICAL - This makes videos cinematic!
