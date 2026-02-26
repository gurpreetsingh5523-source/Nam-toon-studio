#!/usr/bin/env python3
"""
🎨 PHOTOREAL PoC TEST
ਫੋਟੋਰੀਅਲ Proof-of-Concept ਟੈਸਟ

PIL ਰੈਂਡਰਰ vs Stable Diffusion ਦੀ ਤੁਲਨਾ
"""

import sys
import time
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Add workspace to path
WORKSPACE = Path(__file__).parent.absolute()
sys.path.insert(0, str(WORKSPACE))

from realistic_renderer import RealisticRenderer

print("="*70)
print("🎨 PHOTOREAL PoC TEST")
print("   PIL ਰੈਂਡਰਰ vs Stable Diffusion ਤੁਲਨਾ")
print("="*70)
print()

def create_pil_frame(scene_desc="ਪੰਜਾਬੀ ਪਿੰਡ ਵਿੱਚ ਸਿੱਖ ਪਾਤਰ"):
    """PIL ਨਾਲ ਫ੍ਰੇਮ ਬਣਾਓ"""
    print("🖌️  PIL ਰੈਂਡਰਰ ਨਾਲ ਬਣਾ ਰਿਹਾ ਹਾਂ...")
    
    start = time.time()
    
    renderer = RealisticRenderer()
    img = renderer.create_realistic_background(1920, 1080)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Add character
    renderer.draw_realistic_character(draw, 960, 550, frame=0)
    
    # Add title
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 48)
    except:
        font = ImageFont.load_default()
    
    draw.text((50, 50), "PIL ਰੈਂਡਰਰ", fill=(255, 255, 255), font=font, 
              stroke_width=3, stroke_fill=(0, 0, 0))
    
    elapsed = time.time() - start
    
    output_path = WORKSPACE / "test_pil_frame.png"
    img.save(output_path)
    
    print(f"   ✅ ਬਣ ਗਿਆ: {output_path.name}")
    print(f"   ⏱️  ਸਮਾਂ: {elapsed:.2f} ਸਕਿੰਟ")
    print()
    
    return img, elapsed, output_path


def create_sd_frame(scene_desc="Realistic Punjabi Sikh man with orange turban walking in authentic Punjab village with traditional mud houses, green wheat fields, clear blue sky, cinematic lighting, photorealistic, 4K quality"):
    """Stable Diffusion ਨਾਲ ਫ੍ਰੇਮ ਬਣਾਓ"""
    print("🎨 Stable Diffusion ਨਾਲ ਬਣਾ ਰਿਹਾ ਹਾਂ...")
    print(f"   Prompt: {scene_desc[:80]}...")
    
    try:
        import torch
        from diffusers import StableDiffusionPipeline
        
        start = time.time()
        
        # Check device
        device = "cuda" if torch.cuda.is_available() else \
                 "mps" if torch.backends.mps.is_available() else "cpu"
        print(f"   🖥️  Device: {device}")
        
        # Load model
        print("   📥 ਮਾਡਲ ਲੋਡ ਕਰ ਰਿਹਾ ਹਾਂ...")
        pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            safety_checker=None
        )
        pipe = pipe.to(device)
        pipe.enable_attention_slicing()
        
        load_time = time.time() - start
        print(f"   ✅ ਮਾਡਲ ਲੋਡ ਹੋਇਆ ({load_time:.1f} ਸਕਿੰਟ)")
        
        # Generate
        print("   🎨 ਇਮੇਜ ਬਣਾ ਰਿਹਾ ਹਾਂ...")
        gen_start = time.time()
        
        negative_prompt = "cartoon, anime, low quality, blurry, distorted, modern, cars, phones, ugly, deformed"
        
        with torch.no_grad():
            result = pipe(
                prompt=scene_desc,
                negative_prompt=negative_prompt,
                num_inference_steps=30,
                guidance_scale=7.5,
                height=512,
                width=512,
            )
        
        img = result.images[0]
        
        # Resize to 1920x1080
        img = img.resize((1920, 1080), Image.Resampling.LANCZOS)
        
        # Add title
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 48)
        except:
            font = ImageFont.load_default()
        
        draw.text((50, 50), "Stable Diffusion", fill=(255, 255, 255), font=font,
                 stroke_width=3, stroke_fill=(0, 0, 0))
        
        gen_time = time.time() - gen_start
        total_time = time.time() - start
        
        output_path = WORKSPACE / "test_sd_frame.png"
        img.save(output_path)
        
        print(f"   ✅ ਬਣ ਗਿਆ: {output_path.name}")
        print(f"   ⏱️  ਜਨਰੇਸ਼ਨ ਸਮਾਂ: {gen_time:.2f} ਸਕਿੰਟ")
        print(f"   ⏱️  ਕੁੱਲ ਸਮਾਂ: {total_time:.2f} ਸਕਿੰਟ")
        print()
        
        return img, total_time, output_path
        
    except ImportError as e:
        print(f"   ❌ Error: {e}")
        print("   💡 Run: pip install torch diffusers")
        return None, 0, None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None, 0, None


def create_comparison_image(pil_img, sd_img, pil_time, sd_time):
    """ਦੋਵਾਂ ਦੀ ਤੁਲਨਾ ਇਮੇਜ ਬਣਾਓ"""
    print("📊 ਤੁਲਨਾ ਇਮੇਜ ਬਣਾ ਰਿਹਾ ਹਾਂ...")
    
    # Create side-by-side comparison
    width = 1920 * 2 + 100
    height = 1080 + 200
    
    comparison = Image.new('RGB', (width, height), color=(30, 30, 30))
    
    # Paste images
    comparison.paste(pil_img, (50, 100))
    if sd_img:
        comparison.paste(sd_img, (1970, 100))
    
    # Add labels and stats
    draw = ImageDraw.Draw(comparison)
    
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 60)
        text_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 40)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    # Title
    draw.text((width//2 - 400, 20), "PIL vs Stable Diffusion ਤੁਲਨਾ", 
              fill=(255, 255, 255), font=title_font)
    
    # PIL stats
    draw.text((50, height - 80), f"PIL ਰੈਂਡਰਰ", fill=(100, 200, 255), font=text_font)
    draw.text((50, height - 40), f"⏱️  {pil_time:.2f}s  |  💰 ਮੁਫਤ  |  ⭐⭐⭐", 
              fill=(200, 200, 200), font=text_font)
    
    # SD stats
    if sd_img:
        draw.text((1970, height - 80), f"Stable Diffusion", fill=(255, 200, 100), font=text_font)
        draw.text((1970, height - 40), f"⏱️  {sd_time:.2f}s  |  💰 ਮੁਫਤ  |  ⭐⭐⭐⭐⭐", 
                  fill=(200, 200, 200), font=text_font)
    
    output_path = WORKSPACE / "comparison_pil_vs_sd.png"
    comparison.save(output_path)
    
    print(f"   ✅ ਸੇਵ ਹੋਇਆ: {output_path.name}")
    print()
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description='ਫੋਟੋਰੀਅਲ PoC ਟੈਸਟ')
    parser.add_argument('--mode', choices=['single', 'comparison', 'both'], 
                       default='both', help='ਟੈਸਟ ਮੋਡ')
    parser.add_argument('--prompt', type=str, 
                       default="Realistic Punjabi Sikh man with orange turban walking in authentic Punjab village with traditional mud houses, green wheat fields, clear blue sky, cinematic lighting, photorealistic, 4K quality",
                       help='SD prompt')
    
    args = parser.parse_args()
    
    pil_img = None
    sd_img = None
    pil_time = 0
    sd_time = 0
    
    if args.mode in ['single', 'both']:
        # Test PIL
        pil_img, pil_time, pil_path = create_pil_frame()
        
    if args.mode in ['comparison', 'both']:
        # Test SD
        sd_img, sd_time, sd_path = create_sd_frame(args.prompt)
        
        if not pil_img:
            pil_img, pil_time, pil_path = create_pil_frame()
    
    # Create comparison
    if pil_img and sd_img:
        comp_path = create_comparison_image(pil_img, sd_img, pil_time, sd_time)
        
        print("="*70)
        print("📊 RESULTS / ਨਤੀਜੇ")
        print("="*70)
        print()
        print(f"PIL ਰੈਂਡਰਰ:")
        print(f"  ⏱️  ਸਮਾਂ: {pil_time:.2f} ਸਕਿੰਟ")
        print(f"  🎨 ਗੁਣਵੱਤਾ: ⭐⭐⭐ (ਵਧੀਆ)")
        print(f"  💰 ਕੀਮਤ: ਮੁਫਤ")
        print()
        print(f"Stable Diffusion:")
        print(f"  ⏱️  ਸਮਾਂ: {sd_time:.2f} ਸਕਿੰਟ ({sd_time/pil_time:.1f}x ਹੌਲੀ)")
        print(f"  🎨 ਗੁਣਵੱਤਾ: ⭐⭐⭐⭐⭐ (ਫੋਟੋਰੀਅਲ!)")
        print(f"  💰 ਕੀਮਤ: ਮੁਫਤ")
        print()
        print("💡 ਸਿਫਾਰਸ਼: ਹਾਈਬ੍ਰਿਡ ਅਪਰੋਚ")
        print("   - ਮੁੱਖ ਫ੍ਰੇਮ SD ਨਾਲ (ਫੋਟੋਰੀਅਲ)")
        print("   - ਬਾਕੀ PIL ਨਾਲ (ਤੇਜ਼)")
        print("   - ਸਮਾਂ + ਗੁਣਵੱਤਾ ਦਾ ਸੰਤੁਲਨ! ✅")
        print()
        print("📁 ਫਾਈਲਾਂ:")
        print(f"   {pil_path}")
        print(f"   {sd_path if sd_img else 'N/A'}")
        print(f"   {comp_path}")
        print()
        print("🎬 ਵੇਖਣ ਲਈ:")
        print(f"   open {comp_path}")
        print()
    
    elif pil_img:
        print("="*70)
        print("✅ PIL ਟੈਸਟ ਪੂਰਾ ਹੋਇਆ")
        print("="*70)
        print(f"⏱️  ਸਮਾਂ: {pil_time:.2f} ਸਕਿੰਟ")
        print(f"📁 ਫਾਈਲ: test_pil_frame.png")
        print()
    
    print("="*70)
    print("🙏 ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫ਼ਤਿਹ!")
    print("="*70)


if __name__ == '__main__':
    main()
