#!/usr/bin/env python3
"""
🎨 CHARACTER SPRITE SYSTEM
Load and animate character sprites
"""

import cv2
import numpy as np
from pathlib import Path

class CharacterSprite:
    def __init__(self, name, sprite_sheet_path=None):
        self.name = name
        self.poses = {}
        self.current_pose = 'idle'
        self.frame_index = 0
        
        if sprite_sheet_path and Path(sprite_sheet_path).exists():
            self.load_sprite_sheet(sprite_sheet_path)
        else:
            self.create_default_sprites()
    
    def create_default_sprites(self):
        """Create default character sprites"""
        # Walking cycle - 8 frames
        walk_frames = []
        for i in range(8):
            frame = self.create_walk_frame(i)
            walk_frames.append(frame)
        self.poses['walk'] = walk_frames
        
        # Talking - 4 frames
        talk_frames = []
        for i in range(4):
            frame = self.create_talk_frame(i)
            talk_frames.append(frame)
        self.poses['talk'] = talk_frames
        
        # Idle - 1 frame
        self.poses['idle'] = [self.create_idle_frame()]
    
    def create_walk_frame(self, frame_num):
        """Create a walking animation frame"""
        w, h = 200, 300
        char = np.zeros((h, w, 4), dtype=np.uint8)
        
        # Body
        cv2.circle(char, (100, 80), 40, (220, 180, 150, 255), -1)  # Head
        cv2.rectangle(char, (70, 120), (130, 240), (100, 150, 255, 255), -1)  # Body
        
        # Legs (animated)
        leg_offset = int(20 * np.sin(frame_num * np.pi / 4))
        cv2.rectangle(char, (80, 240), (95, 280 + leg_offset), (100, 150, 255, 255), -1)  # Left leg
        cv2.rectangle(char, (105, 240), (120, 280 - leg_offset), (100, 150, 255, 255), -1)  # Right leg
        
        # Arms (animated)
        arm_offset = int(15 * np.cos(frame_num * np.pi / 4))
        cv2.rectangle(char, (50, 130), (70, 200 + arm_offset), (220, 180, 150, 255), -1)  # Left arm
        cv2.rectangle(char, (130, 130), (150, 200 - arm_offset), (220, 180, 150, 255), -1)  # Right arm
        
        return char
    
    def create_talk_frame(self, frame_num):
        """Create a talking animation frame"""
        w, h = 200, 300
        char = np.zeros((h, w, 4), dtype=np.uint8)
        
        # Body (same as idle)
        cv2.circle(char, (100, 80), 40, (220, 180, 150, 255), -1)  # Head
        cv2.rectangle(char, (70, 120), (130, 240), (100, 150, 255, 255), -1)  # Body
        
        # Mouth (animated)
        if frame_num % 2 == 0:
            cv2.ellipse(char, (100, 95), (8, 5), 0, 0, 180, (0, 0, 0, 255), -1)  # Open
        else:
            cv2.line(char, (92, 95), (108, 95), (0, 0, 0, 255), 2)  # Closed
        
        return char
    
    def create_idle_frame(self):
        """Create idle standing frame"""
        w, h = 200, 300
        char = np.zeros((h, w, 4), dtype=np.uint8)
        
        cv2.circle(char, (100, 80), 40, (220, 180, 150, 255), -1)  # Head
        cv2.rectangle(char, (70, 120), (130, 280), (100, 150, 255, 255), -1)  # Body
        
        return char
    
    def get_frame(self, pose='idle', frame_index=None):
        """Get current animation frame"""
        if pose not in self.poses:
            pose = 'idle'
        
        frames = self.poses[pose]
        if frame_index is None:
            frame_index = self.frame_index % len(frames)
        
        return frames[frame_index % len(frames)]
    
    def advance_frame(self):
        """Move to next frame in animation"""
        self.frame_index += 1

# Test
if __name__ == "__main__":
    char = CharacterSprite("Test")
    print(f"✅ Character created with {len(char.poses)} poses")
    print(f"   Walk frames: {len(char.poses['walk'])}")
    print(f"   Talk frames: {len(char.poses['talk'])}")
