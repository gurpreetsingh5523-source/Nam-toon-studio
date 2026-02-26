#!/usr/bin/env python3
"""
🎨 REALISTIC RENDERER
Enhanced character and background rendering for movie-quality visuals
Now with AI image generation support!
Real photo backgrounds + optional character photo overlay (disabled by default)
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import math
from pathlib import Path
import sys
import os
import random

# Try to import AI generator
try:
    from ai_image_generator import AIImageGenerator
    AI_AVAILABLE = True
except:
    AI_AVAILABLE = False
    print("⚠️  AI Generator not available, using fallback rendering")

class RealisticRenderer:
    """Renders realistic characters and backgrounds"""
    
    def __init__(self, use_ai=True):
        self.skin_tone = (255, 220, 177)
        self.hair_color = (50, 30, 20)
        self.kurta_color = (100, 150, 200)  # Blue kurta
        self.pant_color = (80, 80, 100)     # Dark pants
        
        # Initialize REAL PHOTO system
        self.training_photos = Path(__file__).parent / "training_photos"
        self.available_photos = self._load_real_photos()
        self.used_photos = set()
        self.use_real_photos = len(self.available_photos) > 0
        self._current_scene_photo = None
        self._current_scene_image = None

        env_flag = os.environ.get("REALISTIC_RENDERER_USE_PHOTO_CHARACTERS", "").strip().lower()
        self.use_photo_characters = env_flag in {"1", "true", "yes", "on"}
        self.current_character = None
        self.current_character_image = None
        self.current_character_label = ""
        if self.use_photo_characters:
            print("⚠️  Character photo overlay enabled via REALISTIC_RENDERER_USE_PHOTO_CHARACTERS")
        
        if self.use_real_photos:
            print(f"✅ REAL PHOTO MODE: {len(self.available_photos)} photos available")
        
        # Initialize AI generator if available
        self.ai_generator = None
        if use_ai and AI_AVAILABLE:
            try:
                self.ai_generator = AIImageGenerator()
                if self.ai_generator.enabled:
                    print("✅ AI-powered rendering enabled")
            except Exception as e:
                print(f"⚠️  AI init failed: {e}")
                self.ai_generator = None
        
        # Initialize diverse character generator (fallback)
        try:
            from diverse_character_generator import DiverseCharacterGenerator
            self.char_generator = DiverseCharacterGenerator()
            self.use_diverse_chars = True
        except Exception as e:
            print(f"⚠️  Diverse characters failed: {e}")
            self.char_generator = None
            self.use_diverse_chars = False
    
    def _load_real_photos(self):
        """Load real photos from training data"""
        if not self.training_photos.exists():
            return []
        
        photos = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG']:
            photos.extend(self.training_photos.glob(ext))
        
        # Filter out small images
        photos = [p for p in photos if p.stat().st_size > 50000]  # > 50KB
        return photos
    
    def get_diverse_photo(self):
        """Get a different photo each time"""
        if not self.available_photos:
            return None
        
        # Get unused photos
        unused = [p for p in self.available_photos if p not in self.used_photos]
        
        # Reset if all used
        if not unused:
            self.used_photos.clear()
            unused = self.available_photos
        
        # Pick random
        photo = random.choice(unused)
        self.used_photos.add(photo)
        self.current_character = None
        return photo

    def prepare_for_scene(self, character_label: str = ""):
        """Prepare renderer for a new scene before drawing frames."""
        self.current_character_label = (character_label or "").strip()
        self.current_character = None

    def _select_character_template(self, character_label: str):
        """Choose an appropriate character template from the generator."""
        if not self.use_diverse_chars or not self.char_generator:
            return None

        label = (character_label or "").lower()
        if not label:
            return self.char_generator.get_random_character()

        female_terms = [
            "kaur", "woman", "lady", "bibi", "mother", "mom", "mata",
            "wife", "daughter", "beti", "sister", "bhen", "aunt", "aunty",
            "kudi", "girl"
        ]
        kid_terms = [
            "kid", "child", "boy", "girl", "beta", "puttar", "son",
            "beti", "daughter", "youth", "student", "kaka", "lad",
            "teen", "young"
        ]
        elder_terms = [
            "elder", "old", "senior", "baba", "grandfather", "grandpa",
            "dada", "nana", "babaji", "bapu", "uncle", "chacha",
            "tau", "granthi", "giani"
        ]

        # Kids first so "girl" maps to child before general female
        if any(term in label for term in kid_terms):
            if any(term in label for term in female_terms):
                return "kid_girl"
            return random.choice(["kid_boy", "sikh_youth"])

        if any(term in label for term in elder_terms):
            return "elderly_man"

        if any(term in label for term in female_terms):
            return random.choice(["punjabi_woman_1", "punjabi_woman_2"])

        if "teacher" in label:
            return random.choice(["punjabi_woman_2", "punjabi_man_2"])

        return random.choice(["punjabi_man_1", "punjabi_man_2", "sikh_youth"])

    def _load_scene_image(self):
        """Ensure the current scene image is loaded into memory."""
        if not self._current_scene_photo:
            return None
        if self._current_scene_image is not None:
            return self._current_scene_image
        try:
            img = Image.open(self._current_scene_photo)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            self._current_scene_image = img
        except Exception as exc:
            print(f"      ⚠️  Scene photo load failed: {exc}")
            self._current_scene_image = None
        return self._current_scene_image
        
    def create_gradient_sky(self, draw, width, height, horizon=600):
        """Create gradient sky from light blue (top) to darker blue (bottom)"""
        for y in range(horizon):
            # Gradient from light to darker
            progress = y / horizon
            r = int(135 + (50 * progress))
            g = int(206 - (40 * progress))
            b = int(250 - (15 * progress))
            draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    def draw_detailed_tree(self, draw, x, y):
        """Draw a realistic tree with bark texture and leaf clusters"""
        trunk_width = 30
        trunk_height = 100
        
        # Trunk with gradient (darker on left, lighter on right)
        for i in range(trunk_width):
            progress = i / trunk_width
            color = (
                int(70 + 30 * progress),   # Brown gradient
                int(40 + 27 * progress),
                int(20 + 13 * progress)
            )
            draw.line([(x + i, y), (x + i, y + trunk_height)], fill=color)
        
        # Bark lines for texture
        for i in range(5):
            y_pos = y + 20 * i
            draw.line([(x, y_pos), (x + trunk_width, y_pos)], 
                     fill=(50, 30, 15), width=2)
        
        # Foliage - multiple circles for leaf clusters
        foliage_positions = [
            (-25, -30), (0, -40), (25, -30),  # Top layer
            (-20, -10), (20, -10),            # Middle layer
            (-15, 10), (0, 0), (15, 10)       # Bottom layer
        ]
        
        for offset_x, offset_y in foliage_positions:
            center_x = x + trunk_width // 2 + offset_x
            center_y = y + offset_y
            
            # Dark green base
            draw.ellipse([center_x - 25, center_y - 25, 
                         center_x + 25, center_y + 25], 
                        fill=(34, 139, 34))
            
            # Lighter green highlights
            draw.ellipse([center_x - 15, center_y - 15, 
                         center_x + 15, center_y + 15], 
                        fill=(50, 180, 50))
    
    def draw_detailed_house(self, draw, x, y):
        """Draw a realistic Punjabi house with details"""
        width = 200
        height = 150
        
        # Main walls with gradient (lighter on left)
        for i in range(width):
            progress = i / width
            color = (
                int(160 + 20 * progress),  # Brown gradient
                int(90 + 10 * progress),
                int(40 + 5 * progress)
            )
            draw.line([(x + i, y), (x + i, y + height)], fill=color)
        
        # Roof (triangular, red)
        roof_peak = y - 70
        draw.polygon([
            (x - 20, y),
            (x + width // 2, roof_peak),
            (x + width + 20, y)
        ], fill=(178, 34, 34))
        
        # Roof tiles (horizontal lines)
        for i in range(5):
            y_pos = roof_peak + i * 15
            draw.line([(x, y_pos), (x + width, y_pos)], 
                     fill=(150, 20, 20), width=2)
        
        # Windows (2)
        window_y = y + 40
        # Left window
        draw.rectangle([x + 30, window_y, x + 70, window_y + 50], 
                      fill=(100, 150, 200), outline=(50, 50, 50), width=3)
        draw.line([(x + 50, window_y), (x + 50, window_y + 50)], 
                 fill=(50, 50, 50), width=2)
        draw.line([(x + 30, window_y + 25), (x + 70, window_y + 25)], 
                 fill=(50, 50, 50), width=2)
        
        # Right window
        draw.rectangle([x + 130, window_y, x + 170, window_y + 50], 
                      fill=(100, 150, 200), outline=(50, 50, 50), width=3)
        draw.line([(x + 150, window_y), (x + 150, window_y + 50)], 
                 fill=(50, 50, 50), width=2)
        draw.line([(x + 130, window_y + 25), (x + 170, window_y + 25)], 
                 fill=(50, 50, 50), width=2)
        
        # Door
        door_width = 60
        door_height = 100
        door_x = x + (width - door_width) // 2
        door_y = y + height - door_height
        
        draw.rectangle([door_x, door_y, door_x + door_width, y + height], 
                      fill=(101, 67, 33), outline=(50, 30, 15), width=3)
        
        # Door handle
        handle_x = door_x + door_width - 10
        handle_y = door_y + door_height // 2
        draw.ellipse([handle_x - 5, handle_y - 5, handle_x + 5, handle_y + 5], 
                    fill=(255, 215, 0))
        
        # Shadow
        draw.polygon([
            (x + width, y + height),
            (x + width + 30, y + height),
            (x + width + 30, y + height + 20),
            (x + width, y + height + 20)
        ], fill=(0, 0, 0, 50))
    
    def draw_ground_with_grass(self, draw, width, height, ground_y=600):
        """Draw ground with grass texture"""
        ground_height = height - ground_y
        
        # Base ground color with gradient
        for y in range(ground_height):
            progress = y / ground_height
            color = (
                int(34 + 20 * progress),
                int(139 - 20 * progress),
                int(34 + 10 * progress)
            )
            draw.line([(0, ground_y + y), (width, ground_y + y)], fill=color)
        
        # Grass blades (random vertical lines)
        import random
        random.seed(42)  # Consistent randomness
        for _ in range(500):
            x = random.randint(0, width)
            y = random.randint(ground_y, height - 20)
            blade_height = random.randint(10, 30)
            
            # Dark green grass blade
            draw.line([(x, y), (x, y + blade_height)], 
                     fill=(20, 100, 20), width=1)

    def _draw_location_elements(self, draw, width, height, location_tag):
        """Adjust background elements based on planner-provided location tags."""

        tag = (location_tag or "").lower()

        if tag in {"gurdwara", "langar"}:
            self._draw_gurdwara_complex(draw, width, height)
        elif tag in {"fields", "farm", "khet"}:
            self._draw_farmland_rows(draw, width, height)
            self._draw_village_elements(draw, width, height, include_house=False)
        elif tag == "river":
            self._draw_river_scene(draw, width, height)
        elif tag in {"city", "classroom"}:
            self._draw_city_skyline(draw, width, height)
        elif tag == "sports_ground":
            self._draw_sports_field(draw, width, height)
        else:
            self._draw_village_elements(draw, width, height)

    def _draw_village_elements(self, draw, width, height, include_house=True):
        tree_positions = [50, 250, 450, 650, 850]
        for tree_x in tree_positions:
            self.draw_detailed_tree(draw, tree_x, 500)

        if include_house:
            self.draw_detailed_house(draw, 1400, 450)

    def _draw_gurdwara_complex(self, draw, width, height):
        base_y = 520
        center_x = width // 2
        dome_color = (240, 220, 120)
        wall_color = (240, 240, 255)

        # Main hall
        hall_width = 500
        hall_height = 200
        hall_rect = [
            center_x - hall_width // 2,
            base_y - hall_height,
            center_x + hall_width // 2,
            base_y
        ]
        draw.rectangle(hall_rect, fill=wall_color, outline=(180, 180, 210), width=4)

        # Entrance
        door_width = 120
        draw.rectangle([
            center_x - door_width // 2,
            base_y - 140,
            center_x + door_width // 2,
            base_y
        ], fill=(210, 210, 230))

        # Golden dome
        dome_radius = 90
        dome_rect = [
            center_x - dome_radius,
            base_y - hall_height - 2 * dome_radius + 40,
            center_x + dome_radius,
            base_y - hall_height + 40
        ]
        draw.ellipse(dome_rect, fill=dome_color, outline=(200, 170, 80), width=3)

        # Smaller domes
        offset = hall_width // 2 - 100
        for side in (-1, 1):
            small_center = center_x + side * offset
            rect = [small_center - 55, base_y - hall_height - 80, small_center + 55, base_y - hall_height + 10]
            draw.ellipse(rect, fill=dome_color, outline=(200, 170, 80), width=3)

        # Nishan Sahib (flag)
        flag_x = center_x + hall_width // 2 + 40
        draw.line([(flag_x, base_y - hall_height - 150), (flag_x, base_y)], fill=(230, 150, 20), width=6)
        draw.polygon([
            (flag_x, base_y - hall_height - 140),
            (flag_x + 60, base_y - hall_height - 120),
            (flag_x, base_y - hall_height - 100)
        ], fill=(255, 140, 0))

    def _draw_city_skyline(self, draw, width, height):
        skyline_base = 620
        building_widths = [120, 90, 150, 110, 80, 130]
        x = 80
        colors = [(60, 70, 90), (70, 90, 110), (90, 105, 130)]
        for width_idx, b_width in enumerate(building_widths):
            b_height = random.randint(180, 280)
            color = colors[width_idx % len(colors)]
            draw.rectangle([
                x,
                skyline_base - b_height,
                x + b_width,
                skyline_base
            ], fill=color)

            # Windows
            window_color = (240, 220, 140)
            for wy in range(skyline_base - 30, skyline_base - b_height, -35):
                for wx in range(x + 10, x + b_width - 10, 25):
                    draw.rectangle([(wx, wy - 12), (wx + 12, wy)], fill=window_color)

            x += b_width + 30

    def _draw_river_scene(self, draw, width, height):
        river_y = 600
        draw.rectangle([(0, river_y), (width, height)], fill=(40, 100, 180))
        for i in range(10):
            start_x = random.randint(0, width)
            draw.line(
                [(start_x, river_y + 20 + i * 25), (start_x + 200, river_y + 20 + i * 25)],
                fill=(220, 240, 255, 180),
                width=2
            )

    def _draw_farmland_rows(self, draw, width, height):
        base_y = 620
        row_height = 30
        colors = [(110, 160, 70), (130, 180, 90)]
        for idx in range(8):
            y_top = base_y + idx * row_height
            color = colors[idx % len(colors)]
            draw.polygon([
                (0, y_top),
                (width, y_top - 60),
                (width, y_top + row_height),
                (0, y_top + row_height + 60)
            ], fill=color)

    def _draw_sports_field(self, draw, width, height):
        field_top = 600
        field_bottom = height - 40
        draw.rectangle([(80, field_top), (width - 80, field_bottom)], outline=(220, 220, 220), width=4)
        draw.line([(width // 2, field_top), (width // 2, field_bottom)], fill=(220, 220, 220), width=3)
        center_circle_radius = 80
        draw.ellipse([
            (width // 2) - center_circle_radius,
            (field_top + field_bottom) // 2 - center_circle_radius,
            (width // 2) + center_circle_radius,
            (field_top + field_bottom) // 2 + center_circle_radius
        ], outline=(220, 220, 220), width=3)

    def _apply_mood_overlay(self, image, mood_tag):
        """Apply subtle color grading based on detected mood tag."""

        tag = (mood_tag or "").lower()
        overlays = {
            "devotional": (255, 230, 180, 60),
            "happy": (255, 240, 200, 50),
            "sad": (120, 150, 210, 70),
            "tense": (200, 120, 120, 70),
            "fun": (255, 220, 180, 50),
            "hopeful": (210, 255, 210, 50),
            "adventurous": (200, 230, 255, 50),
        }

        overlay_color = overlays.get(tag)
        if not overlay_color:
            return image.convert('RGB') if image.mode != 'RGB' else image

        base = image.convert('RGBA')
        overlay = Image.new('RGBA', base.size, overlay_color)
        blended = Image.alpha_composite(base, overlay)
        return blended.convert('RGB')
    
    def draw_realistic_character(self, draw, x, y, frame, walk_cycle_len=8, img=None):
        """Draw a realistic human character with details - NOW USING REAL PHOTOS!"""
        
        # PRIORITY 1: Optional REAL PHOTO overlay (disabled by default)
        if self.use_photo_characters and self.use_real_photos and img is not None:
            scene_image = self._load_scene_image()

            if scene_image:
                try:
                    photo = scene_image.copy()

                    max_width = int(img.width * 0.45)
                    max_height = int(img.height * 0.82)
                    photo.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

                    paste_x = max(80, x - photo.width // 2)
                    paste_y = max(80, y - photo.height)

                    # Add subtle border and drop shadow for polish
                    border_size = 8
                    bordered = ImageOps.expand(photo, border=border_size, fill=(255, 255, 255))
                    shadow = Image.new('RGBA', (bordered.width, bordered.height), (0, 0, 0, 90))
                    img.paste(shadow, (paste_x + 12, paste_y + 12), shadow)
                    img.paste(bordered, (paste_x, paste_y))

                    return  # Done! Using real photo overlay

                except Exception as e:
                    print(f"      ⚠️  Photo error: {e}")
                    # Fall through to backup methods
        
        # PRIORITY 2: Use diverse character generator if available
        if self.use_diverse_chars and self.char_generator:
            # Pick character at start (frame 0) and keep same throughout scene
            if frame == 0 or self.current_character is None:
                selected = self._select_character_template(self.current_character_label)
                if not selected:
                    selected = self.char_generator.get_random_character()
                self.current_character = selected
            
            # Draw diverse character
            self.char_generator.draw_character(draw, x, y, self.current_character, frame)
            return
        
        # Fallback to old single character
        # Calculate walk cycle position
        walk_phase = frame % walk_cycle_len
        
        # Body dimensions
        head_radius = 40
        body_width = 50
        body_height = 80
        arm_length = 60
        leg_length = 70
        
        # HEAD
        head_y = y - 100
        
        # Face (skin tone)
        draw.ellipse([x - head_radius, head_y - head_radius, 
                     x + head_radius, head_y + head_radius], 
                    fill=self.skin_tone)
        
        # Hair (turban for Punjabi character)
        turban_color = (200, 100, 50)  # Orange/saffron
        draw.ellipse([x - head_radius - 5, head_y - head_radius - 10, 
                     x + head_radius + 5, head_y], 
                    fill=turban_color)
        
        # Turban wrap lines
        for i in range(3):
            y_pos = head_y - head_radius + 10 + i * 10
            draw.line([(x - head_radius, y_pos), (x + head_radius, y_pos)], 
                     fill=(180, 80, 40), width=2)
        
        # Eyes
        eye_y = head_y - 10
        # Left eye
        draw.ellipse([x - 20, eye_y - 8, x - 10, eye_y + 2], fill='white')
        draw.ellipse([x - 17, eye_y - 5, x - 13, eye_y - 1], fill='black')
        # Right eye
        draw.ellipse([x + 10, eye_y - 8, x + 20, eye_y + 2], fill='white')
        draw.ellipse([x + 13, eye_y - 5, x + 17, eye_y - 1], fill='black')
        
        # Eyebrows
        draw.arc([x - 22, eye_y - 15, x - 8, eye_y - 8], 0, 180, 
                fill='black', width=2)
        draw.arc([x + 8, eye_y - 15, x + 22, eye_y - 8], 0, 180, 
                fill='black', width=2)
        
        # Nose
        draw.line([x, eye_y + 5, x, eye_y + 15], 
                 fill=(200, 170, 140), width=3)
        draw.ellipse([x - 5, eye_y + 13, x + 5, eye_y + 18], 
                    fill=(200, 170, 140))
        
        # Mouth (smiling)
        draw.arc([x - 15, eye_y + 15, x + 15, eye_y + 30], 0, 180, 
                fill='black', width=2)
        
        # Beard (small)
        draw.arc([x - 20, eye_y + 20, x + 20, head_y + head_radius + 10], 
                0, 180, fill=(50, 30, 20), width=8)
        
        # BODY (Kurta - traditional Punjabi shirt)
        body_top = head_y + head_radius
        
        # Kurta with gradient
        for i in range(body_height):
            progress = i / body_height
            color = (
                int(self.kurta_color[0] - 20 * progress),
                int(self.kurta_color[1] - 30 * progress),
                int(self.kurta_color[2] - 40 * progress)
            )
            draw.ellipse([x - body_width - 5, body_top + i - 5, 
                         x + body_width + 5, body_top + i + 5], 
                        fill=color)
        
        # Kurta buttons
        for i in range(4):
            button_y = body_top + 15 + i * 18
            draw.ellipse([x - 5, button_y - 5, x + 5, button_y + 5], 
                        fill=(255, 215, 0))
        
        # ARMS with hands
        shoulder_y = body_top + 10
        
        # Arm swing based on walk cycle
        if walk_phase < walk_cycle_len // 2:
            left_arm_angle = -30 + (walk_phase * 10)
            right_arm_angle = 30 - (walk_phase * 10)
        else:
            left_arm_angle = 10 - ((walk_phase - walk_cycle_len // 2) * 10)
            right_arm_angle = -10 + ((walk_phase - walk_cycle_len // 2) * 10)
        
        # Left arm
        left_hand_x = x - body_width + int(arm_length * math.sin(math.radians(left_arm_angle)))
        left_hand_y = shoulder_y + int(arm_length * math.cos(math.radians(left_arm_angle)))
        draw.line([(x - body_width, shoulder_y), (left_hand_x, left_hand_y)], 
                 fill=self.kurta_color, width=12)
        # Hand
        draw.ellipse([left_hand_x - 8, left_hand_y - 8, 
                     left_hand_x + 8, left_hand_y + 8], 
                    fill=self.skin_tone)
        
        # Right arm
        right_hand_x = x + body_width + int(arm_length * math.sin(math.radians(right_arm_angle)))
        right_hand_y = shoulder_y + int(arm_length * math.cos(math.radians(right_arm_angle)))
        draw.line([(x + body_width, shoulder_y), (right_hand_x, right_hand_y)], 
                 fill=self.kurta_color, width=12)
        # Hand
        draw.ellipse([right_hand_x - 8, right_hand_y - 8, 
                     right_hand_x + 8, right_hand_y + 8], 
                    fill=self.skin_tone)
        
        # LEGS with pants and shoes
        hip_y = body_top + body_height
        
        # Leg positions based on walk cycle
        if walk_phase < walk_cycle_len // 2:
            left_leg_forward = 20 + (walk_phase * 6)
            right_leg_forward = -10 - (walk_phase * 6)
        else:
            left_leg_forward = 50 - ((walk_phase - walk_cycle_len // 2) * 6)
            right_leg_forward = -40 + ((walk_phase - walk_cycle_len // 2) * 6)
        
        # Left leg
        left_foot_x = x - 20 + int(left_leg_forward)
        left_foot_y = hip_y + leg_length
        # Thigh
        draw.line([(x - 15, hip_y), (x - 15, hip_y + leg_length // 2)], 
                 fill=self.pant_color, width=15)
        # Calf
        draw.line([(x - 15, hip_y + leg_length // 2), (left_foot_x, left_foot_y)], 
                 fill=self.pant_color, width=15)
        # Shoe
        draw.ellipse([left_foot_x - 15, left_foot_y - 8, 
                     left_foot_x + 15, left_foot_y + 8], 
                    fill=(50, 30, 20))
        
        # Right leg
        right_foot_x = x + 20 + int(right_leg_forward)
        right_foot_y = hip_y + leg_length
        # Thigh
        draw.line([(x + 15, hip_y), (x + 15, hip_y + leg_length // 2)], 
                 fill=self.pant_color, width=15)
        # Calf
        draw.line([(x + 15, hip_y + leg_length // 2), (right_foot_x, right_foot_y)], 
                 fill=self.pant_color, width=15)
        # Shoe
        draw.ellipse([right_foot_x - 15, right_foot_y - 8, 
                     right_foot_x + 15, right_foot_y + 8], 
                    fill=(50, 30, 20))
        
        # SHADOW (beneath character)
        shadow_y = y + 80
        draw.ellipse([x - 60, shadow_y, x + 60, shadow_y + 10], 
                    fill=(0, 0, 0, 80))
    
    def create_realistic_background(self, width=1920, height=1080, location_tag=None, mood_tag=None):
        """Create a complete realistic background from photo dataset when available."""

        if self.use_real_photos and self.available_photos:
            # Reset scene photo for this background
            self._current_scene_photo = self.get_diverse_photo()
            self._current_scene_image = None

            if self._current_scene_photo and self._current_scene_photo.exists():
                try:
                    scene_img = Image.open(self._current_scene_photo)
                    if scene_img.mode != 'RGB':
                        scene_img = scene_img.convert('RGB')
                    self._current_scene_image = scene_img.copy()

                    fitted = ImageOps.fit(scene_img, (width, height), Image.Resampling.LANCZOS)
                    blurred = fitted.filter(ImageFilter.GaussianBlur(radius=6))
                    background = blurred.convert('RGBA')

                    # Add dark gradient at bottom for text readability
                    gradient = Image.new('RGBA', (width, height), (0, 0, 0, 0))
                    grad_draw = ImageDraw.Draw(gradient)
                    grad_draw.rectangle(
                        [0, int(height * 0.55), width, height],
                        fill=(0, 0, 0, 110)
                    )
                    background = Image.alpha_composite(background, gradient)
                    return self._apply_mood_overlay(background.convert('RGB'), mood_tag)

                except Exception as exc:
                    print(f"⚠️  Real background failed ({exc}), using artistic fallback")
                    self._current_scene_photo = None
                    self._current_scene_image = None

        # Artistic fallback background
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img, 'RGBA')
        
        # Sky with gradient
        self.create_gradient_sky(draw, width, height, horizon=600)
        
        # Sun
        sun_x, sun_y = 1700, 150
        # Glow
        draw.ellipse([sun_x - 70, sun_y - 70, sun_x + 70, sun_y + 70], 
                    fill=(255, 255, 200, 100))
        # Core
        draw.ellipse([sun_x - 50, sun_y - 50, sun_x + 50, sun_y + 50], 
                    fill=(255, 255, 0))
        
        # Clouds
        cloud_positions = [(300, 150), (800, 100), (1300, 200)]
        for cx, cy in cloud_positions:
            # Multiple circles for fluffy cloud
            draw.ellipse([cx - 60, cy - 30, cx + 60, cy + 30], 
                        fill=(255, 255, 255, 200))
            draw.ellipse([cx - 40, cy - 40, cx + 40, cy + 20], 
                        fill=(255, 255, 255, 200))
            draw.ellipse([cx + 20, cy - 35, cx + 80, cy + 25], 
                        fill=(255, 255, 255, 200))
        
        # Ground with grass
        self.draw_ground_with_grass(draw, width, height, ground_y=600)

        # Road (dirt path)
        road_y = 650
        for i in range(30):
            progress = i / 30
            color = (
                int(128 + 20 * progress),
                int(128 - 20 * progress),
                int(100 - 10 * progress)
            )
            draw.line([(0, road_y + i), (width, road_y + i)], fill=color)

        self._draw_location_elements(draw, width, height, location_tag)

        return self._apply_mood_overlay(img, mood_tag)


# Test the renderer
if __name__ == '__main__':
    print("🎨 Testing Realistic Renderer...")
    
    renderer = RealisticRenderer()
    
    # Create background
    img = renderer.create_realistic_background(1920, 1080)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Add character at different positions
    for i in range(8):
        x = 300 + i * 200
        renderer.draw_realistic_character(draw, x, 550, frame=i)
    
    # Save
    img.save('test_realistic_render.png')
    print("✅ Saved: test_realistic_render.png")
    print("🎬 This shows 8-frame walk cycle with realistic rendering")
