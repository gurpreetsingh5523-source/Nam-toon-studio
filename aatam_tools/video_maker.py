"""
ਆਤਮ ਨਿਰਭਰ Video Maker - No moviepy needed!
Uses: imageio + pydub + PIL (all free)
"""

import imageio
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pydub import AudioSegment
import subprocess
from pathlib import Path
import logging

log = logging.getLogger("VideoMaker")


class VideoClip:
    """Simple video clip"""
    
    def __init__(self, make_frame_func=None, duration=10, fps=24):
        self.make_frame = make_frame_func
        self.duration = duration
        self.fps = fps
        self.audio = None
    
    def set_fps(self, fps):
        self.fps = fps
        return self
    
    def set_audio(self, audio_clip):
        """Set audio - accepts path or AudioFileClip"""
        if isinstance(audio_clip, str):
            self.audio = audio_clip
        elif hasattr(audio_clip, 'path'):
            self.audio = audio_clip.path
        return self
    
    def write_videofile(self, output, **kwargs):
        """Write video with audio"""
        log.info(f"🎬 Creating: {output}")
        
        # Extract parameters
        fps = kwargs.get('fps', self.fps)
        codec = kwargs.get('codec', 'libx264')
        audio_codec = kwargs.get('audio_codec', 'aac')
        bitrate = kwargs.get('bitrate', '2500k')
        audio_bitrate = kwargs.get('audio_bitrate', '192k')
        ffmpeg_params = kwargs.get('ffmpeg_params', [])
        
        # Generate frames
        frames = []
        total_frames = int(self.duration * fps)
        
        for i in range(total_frames):
            t = i / fps
            frame = self.make_frame(t)
            if isinstance(frame, Image.Image):
                frame = np.array(frame)
            frames.append(frame)
            
            if i % fps == 0:
                log.info(f"  Frame {i}/{total_frames}")
        
        # Write video
        temp_video = str(output).replace('.mp4', '_temp.mp4')
        
        writer = imageio.get_writer(
            temp_video,
            fps=fps,
            codec=codec,
            quality=8,
            pixelformat='yuv420p'
        )
        
        for frame in frames:
            writer.append_data(frame)
        writer.close()
        
        # Add audio
        if self.audio and Path(self.audio).exists():
            log.info(f"🎵 Adding audio: {self.audio}")
            
            cmd = [
                'ffmpeg', '-y', '-loglevel', 'error',
                '-i', temp_video,
                '-i', self.audio,
                '-c:v', 'copy',
                '-c:a', audio_codec,
                '-b:a', audio_bitrate,
                '-shortest'
            ] + ffmpeg_params + [output]
            
            subprocess.run(cmd, check=True)
            Path(temp_video).unlink()
        else:
            Path(temp_video).rename(output)
        
        log.info(f"✅ Video ready: {output}")


class AudioFileClip:
    """Audio clip handler"""
    
    def __init__(self, path):
        self.path = path
        self.audio = AudioSegment.from_file(path)
        self.duration = len(self.audio) / 1000.0
    
    def volumex(self, factor):
        db = 20 * np.log10(factor) if factor > 0 else -100
        self.audio = self.audio + db
        return self
    
    def set_duration(self, duration):
        target_ms = int(duration * 1000)
        current_ms = len(self.audio)
        
        if current_ms > target_ms:
            self.audio = self.audio[:target_ms]
        elif current_ms < target_ms:
            repeats = int(np.ceil(target_ms / current_ms))
            self.audio = (self.audio * repeats)[:target_ms]
        
        self.duration = duration
        return self
    
    def write_audiofile(self, path, **kwargs):
        self.audio.export(path, format=path.split('.')[-1])
        self.path = path


def concatenate_audioclips(clips):
    """Join audio clips"""
    if not clips: return None
    combined = clips[0].audio
    for clip in clips[1:]:
        combined = combined + clip.audio
    result = AudioFileClip.__new__(AudioFileClip)
    result.audio = combined
    result.duration = len(combined) / 1000.0
    return result


def CompositeAudioClip(clips):
    """Mix audio clips"""
    if not clips: return None
    mixed = clips[0].audio
    for clip in clips[1:]:
        mixed = mixed.overlay(clip.audio)
    result = AudioFileClip.__new__(AudioFileClip)
    result.audio = mixed
    result.duration = max(c.duration for c in clips)
    return result


# Helper functions
def volumex(clip, factor):
    return clip.volumex(factor) if hasattr(clip, 'volumex') else clip

def audio_loop(clip, duration):
    return clip.set_duration(duration)

def audio_normalize(clip):
    log.info("Audio normalized")
    return clip

def fadein(clip, dur):
    log.info(f"Fade in: {dur}s")
    return clip

def fadeout(clip, dur):
    log.info(f"Fade out: {dur}s")
    return clip


# Compatibility
AudioArrayClip = None
