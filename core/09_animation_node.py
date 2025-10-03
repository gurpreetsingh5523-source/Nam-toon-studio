# AmritCore - 09_animation_node.py (The Final Movement Module)

# Install necessary stable libraries
!pip install moviepy Pillow

from moviepy.editor import ImageClip, concatenate_videoclips, vfx
from PIL import Image
import os

# --- Step 1: Define the Animation Node Function ---
def create_movement_illusion(output_filename="assets/animation/movement_clip_final.mp4", duration=3):
    """
    Creates a simple, stable cross-fade animation clip for the final video.
    This simulates the character shifting slightly.
    """
    if not os.path.exists("assets/animation"):
        os.makedirs("assets/animation")
    
    print("\n--- Animation Node Status: Creating Movement Illusion ---")

    # Frame 1: Placeholder 1 (Base Scene Color)
    img1 = Image.new('RGB', (1920, 1080), color='#2A2D43') 
    img1.save("assets/animation/frame_1.png")
    
    # Frame 2: Placeholder 2 (Slightly different shade for contrast/movement)
    img2 = Image.new('RGB', (1920, 1080), color='#434657') 
    img2.save("assets/animation/frame_2.png")
    
    
    clip1 = ImageClip("assets/animation/frame_1.png").set_duration(duration / 2).set_fps(24)
    clip2 = ImageClip("assets/animation/frame_2.png").set_duration(duration / 2).set_fps(24)
    
    # Cross-fade creates the smooth movement illusion (The key to stable animation)
    final_clip = concatenate_videoclips([clip1.fx(vfx.fadeout, 0.5), clip2.fx(vfx.fadein, 0.5)])
    
    # Save the movement clip
    final_clip.write_videofile(output_filename, fps=24, verbose=False, logger=None)
    
    print(f"Animation Node Status: SUCCESS! Movement clip created as {output_filename}")
    return output_filename

# --- Step 2: Test the Node ---
create_movement_illusion()
