#!/usr/bin/env python3
"""
🎬 CUSTOM ANIMATOR - Nam-Toon Studio
Our own animation engine (less dependent on OpenCV)
Version 1.0: Basic frame interpolation

Phase 1: Use OpenCV for rendering (CURRENT)
Phase 2: Custom easing and interpolation
Phase 3: Physics-based animation
Phase 4: Professional animation system (TARGET)
"""

import numpy as np
import math

class CustomAnimator:
    """Custom Animation Engine"""
    
    def __init__(self):
        self.fps = 30
        self.easing_functions = self.build_easing_functions()
    
    def build_easing_functions(self):
        """Create smooth animation easing functions"""
        return {
            'linear': lambda t: t,
            'ease_in': lambda t: t * t,
            'ease_out': lambda t: 1 - (1 - t) ** 2,
            'ease_in_out': lambda t: 3 * t ** 2 - 2 * t ** 3,
            'bounce': lambda t: 1 - abs(math.sin(t * math.pi * 2)),
        }
    
    def interpolate(self, start, end, progress, easing='ease_in_out'):
        """Interpolate between two values with easing"""
        ease_func = self.easing_functions.get(easing, lambda t: t)
        t = ease_func(progress)
        return start + (end - start) * t
    
    def animate_position(self, start_pos, end_pos, duration_sec, easing='ease_in_out'):
        """Generate position keyframes for smooth movement"""
        total_frames = int(duration_sec * self.fps)
        positions = []
        
        for frame in range(total_frames):
            progress = frame / total_frames
            
            x = self.interpolate(start_pos[0], end_pos[0], progress, easing)
            y = self.interpolate(start_pos[1], end_pos[1], progress, easing)
            
            positions.append((int(x), int(y)))
        
        return positions
    
    def animate_scale(self, start_scale, end_scale, duration_sec, easing='ease_in_out'):
        """Generate scale keyframes"""
        total_frames = int(duration_sec * self.fps)
        scales = []
        
        for frame in range(total_frames):
            progress = frame / total_frames
            scale = self.interpolate(start_scale, end_scale, progress, easing)
            scales.append(scale)
        
        return scales
    
    def create_walk_cycle(self, num_frames=8):
        """Create walking animation keyframes"""
        cycle = []
        
        for i in range(num_frames):
            angle = (i / num_frames) * 2 * math.pi
            
            # Leg positions
            left_leg = math.sin(angle) * 20
            right_leg = math.sin(angle + math.pi) * 20
            
            # Arm swing (opposite to legs)
            left_arm = math.sin(angle + math.pi) * 15
            right_arm = math.sin(angle) * 15
            
            # Body bob
            body_y = abs(math.sin(angle * 2)) * 5
            
            keyframe = {
                'left_leg_offset': left_leg,
                'right_leg_offset': right_leg,
                'left_arm_offset': left_arm,
                'right_arm_offset': right_arm,
                'body_y_offset': -body_y  # Negative to move up
            }
            
            cycle.append(keyframe)
        
        return cycle
    
    def create_talk_cycle(self, num_frames=4):
        """Create talking animation keyframes"""
        cycle = []
        
        for i in range(num_frames):
            # Mouth open/close
            mouth_open = abs(math.sin((i / num_frames) * math.pi))
            
            # Head slight movement
            head_tilt = math.sin((i / num_frames) * 2 * math.pi) * 2
            
            keyframe = {
                'mouth_open': mouth_open,
                'head_tilt': head_tilt
            }
            
            cycle.append(keyframe)
        
        return cycle

# Test
if __name__ == "__main__":
    animator = CustomAnimator()
    
    # Test movement
    positions = animator.animate_position((0, 0), (100, 50), 2.0, 'ease_in_out')
    print(f"✅ Generated {len(positions)} position keyframes")
    
    # Test walk cycle
    walk = animator.create_walk_cycle()
    print(f"✅ Generated {len(walk)} walk cycle frames")
    
    # Test talk cycle
    talk = animator.create_talk_cycle()
    print(f"✅ Generated {len(talk)} talk cycle frames")
    
    print("\n📊 Custom Animator Status:")
    print("   Quality: 40% (basic interpolation working)")
    print("   Using: OpenCV for rendering, custom for animation math")
