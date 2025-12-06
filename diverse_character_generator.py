#!/usr/bin/env python3
"""
👥 DIVERSE CHARACTER GENERATOR
Creates multiple unique characters for variety
NO AI needed - pure Python drawing
"""

from PIL import Image, ImageDraw
import random

class DiverseCharacterGenerator:
    """Generate diverse hand-drawn characters"""
    
    def __init__(self):
        # Diverse character templates
        self.characters = {
            "punjabi_man_1": {
                "skin": (255, 220, 177),
                "hair": (50, 30, 20),
                "kurta": (100, 150, 200),
                "pant": (80, 80, 100),
                "turban": (220, 100, 50),
                "beard": True
            },
            "punjabi_man_2": {
                "skin": (210, 180, 140),
                "hair": (70, 50, 30),
                "kurta": (150, 100, 180),
                "pant": (60, 60, 80),
                "turban": (180, 50, 50),
                "beard": True
            },
            "punjabi_woman_1": {
                "skin": (255, 220, 177),
                "hair": (30, 20, 10),
                "suit": (200, 50, 100),
                "dupatta": (255, 200, 150),
                "jewelry": True
            },
            "punjabi_woman_2": {
                "skin": (230, 200, 170),
                "hair": (50, 30, 20),
                "suit": (100, 180, 100),
                "dupatta": (255, 180, 200),
                "jewelry": True
            },
            "sikh_youth": {
                "skin": (240, 210, 180),
                "hair": (60, 40, 25),
                "shirt": (50, 100, 200),
                "pant": (40, 40, 60),
                "patka": (255, 140, 0),
                "beard": False
            },
            "elderly_man": {
                "skin": (220, 190, 160),
                "hair": (180, 180, 180),
                "kurta": (180, 140, 100),
                "pant": (100, 100, 120),
                "turban": (255, 255, 255),
                "beard": True
            },
            "kid_boy": {
                "skin": (255, 230, 200),
                "hair": (40, 25, 15),
                "shirt": (255, 200, 50),
                "shorts": (100, 100, 150),
                "small": True
            },
            "kid_girl": {
                "skin": (255, 230, 200),
                "hair": (30, 20, 10),
                "dress": (255, 100, 150),
                "dupatta": (200, 200, 255),
                "small": True
            }
        }
        
        print(f"✅ Diverse Character Generator ready ({len(self.characters)} characters)")
    
    def draw_punjabi_man(self, draw, x, y, char_data, frame_num=0):
        """Draw Punjabi man with turban"""
        # Walking animation
        leg_swing = int(10 * math.sin(frame_num * 0.2))
        
        # Turban (largest, distinctive)
        turban_color = char_data.get("turban", (220, 100, 50))
        draw.ellipse([x - 35, y - 100, x + 35, y - 50], fill=turban_color)
        
        # Face
        skin_color = char_data["skin"]
        draw.ellipse([x - 25, y - 70, x + 25, y - 20], fill=skin_color)
        
        # Beard
        if char_data.get("beard"):
            beard_color = char_data["hair"]
            draw.ellipse([x - 20, y - 40, x + 20, y - 10], fill=beard_color)
        
        # Eyes
        draw.ellipse([x - 15, y - 55, x - 5, y - 45], fill=(255, 255, 255))
        draw.ellipse([x + 5, y - 55, x + 15, y - 45], fill=(255, 255, 255))
        draw.ellipse([x - 12, y - 52, x - 8, y - 48], fill=(50, 30, 20))
        draw.ellipse([x + 8, y - 52, x + 12, y - 48], fill=(50, 30, 20))
        
        # Kurta/Shirt (body)
        kurta_color = char_data.get("kurta", char_data.get("shirt", (100, 150, 200)))
        draw.rectangle([x - 30, y - 20, x + 30, y + 40], fill=kurta_color)
        
        # Arms
        draw.line([(x - 30, y - 10), (x - 45, y + 20)], fill=kurta_color, width=12)
        draw.line([(x + 30, y - 10), (x + 45, y + 20)], fill=kurta_color, width=12)
        
        # Pajama/Pants/Shorts (pants)
        pant_color = char_data.get("pant", char_data.get("shorts", (80, 80, 100)))
        draw.line([(x - 15, y + 40), (x - 15, y + 80 + leg_swing)], fill=pant_color, width=18)
        draw.line([(x + 15, y + 40), (x + 15, y + 80 - leg_swing)], fill=pant_color, width=18)
        
        # Feet
        draw.ellipse([x - 25, y + 75 + leg_swing, x - 5, y + 85 + leg_swing], fill=(139, 69, 19))
        draw.ellipse([x + 5, y + 75 - leg_swing, x + 25, y + 85 - leg_swing], fill=(139, 69, 19))
    
    def draw_punjabi_woman(self, draw, x, y, char_data, frame_num=0):
        """Draw Punjabi woman with salwar kameez"""
        import math
        
        # Walking animation
        leg_swing = int(8 * math.sin(frame_num * 0.2))
        
        # Hair (long)
        hair_color = char_data["hair"]
        draw.ellipse([x - 30, y - 80, x + 30, y - 20], fill=hair_color)
        
        # Face
        skin_color = char_data["skin"]
        draw.ellipse([x - 22, y - 70, x + 22, y - 25], fill=skin_color)
        
        # Eyes (with kajal)
        draw.ellipse([x - 14, y - 55, x - 6, y - 47], fill=(255, 255, 255))
        draw.ellipse([x + 6, y - 55, x + 14, y - 47], fill=(255, 255, 255))
        draw.ellipse([x - 11, y - 52, x - 9, y - 50], fill=(0, 0, 0))
        draw.ellipse([x + 9, y - 52, x + 11, y - 50], fill=(0, 0, 0))
        
        # Bindi
        draw.ellipse([x - 2, y - 60, x + 2, y - 56], fill=(200, 0, 0))
        
        # Kameez/Dress (suit top or dress)
        suit_color = char_data.get("suit", char_data.get("dress", (200, 50, 100)))
        draw.rectangle([x - 28, y - 25, x + 28, y + 45], fill=suit_color)
        
        # Dupatta (draped over shoulders)
        dupatta_color = char_data.get("dupatta", (255, 200, 150))
        draw.polygon([
            (x - 35, y - 15),
            (x + 35, y - 15),
            (x + 25, y + 30),
            (x - 25, y + 30)
        ], fill=dupatta_color)
        
        # Arms
        draw.line([(x - 28, y - 10), (x - 40, y + 25)], fill=suit_color, width=10)
        draw.line([(x + 28, y - 10), (x + 40, y + 25)], fill=suit_color, width=10)
        
        # Salwar (pants)
        draw.line([(x - 14, y + 45), (x - 14, y + 85 + leg_swing)], fill=suit_color, width=16)
        draw.line([(x + 14, y + 45), (x + 14, y + 85 - leg_swing)], fill=suit_color, width=16)
        
        # Feet (with jutti)
        draw.ellipse([x - 24, y + 80 + leg_swing, x - 6, y + 88 + leg_swing], fill=(220, 50, 50))
        draw.ellipse([x + 6, y + 80 - leg_swing, x + 24, y + 88 - leg_swing], fill=(220, 50, 50))
        
        # Jewelry if enabled
        if char_data.get("jewelry"):
            # Necklace
            draw.arc([x - 15, y - 25, x + 15, y - 15], 0, 180, fill=(255, 215, 0), width=3)
    
    def draw_character(self, draw, x, y, character_type, frame_num=0):
        """Draw any character type"""
        import math
        
        if character_type not in self.characters:
            character_type = random.choice(list(self.characters.keys()))
        
        char_data = self.characters[character_type]
        
        # Scale down kids
        if char_data.get("small"):
            y += 20  # Move down (shorter)
        
        # Draw based on gender
        if "woman" in character_type or "girl" in character_type:
            self.draw_punjabi_woman(draw, x, y, char_data, frame_num)
        else:
            self.draw_punjabi_man(draw, x, y, char_data, frame_num)
    
    def get_random_character(self):
        """Get random character type"""
        return random.choice(list(self.characters.keys()))


# Add math import at top
import math

if __name__ == "__main__":
    print("🧪 Testing Diverse Characters...")
    
    generator = DiverseCharacterGenerator()
    
    # Create test image
    img = Image.new('RGB', (1920, 1080), color=(135, 206, 235))
    draw = ImageDraw.Draw(img)
    
    # Draw all characters in a line
    x_pos = 200
    for char_type in generator.characters.keys():
        generator.draw_character(draw, x_pos, 600, char_type, frame_num=0)
        x_pos += 220
        
        if x_pos > 1800:
            break
    
    img.save("test_diverse_characters.png")
    print("✅ Saved: test_diverse_characters.png")
