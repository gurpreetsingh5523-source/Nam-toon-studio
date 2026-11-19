"""Mix narration under the score and mux onto the rendered video.

The video already carries its letterbox, titles and captions (see titles.py) —
this ffmpeg build has neither libass nor drawtext, so type is drawn in PIL.
"""
import subprocess, os
from render import LEAD

def main(src="out/video_raw.mp4", dst="out/THE_FORTY_FOURTH.mp4"):
    os.makedirs("out", exist_ok=True)
    # video already carries letterbox + titles; this pass is the audio mix only.
    # narration sits on top; score ducks under it via sidechain compression
    # narration is written from t=0, but the cut opens on a LEAD-second title card
    delay = int(LEAD * 1000)
    fc = (
        f"[1:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"adelay={delay}|{delay},"
        f"highpass=f=85,acompressor=threshold=0.10:ratio=3.2:attack=8:release=260,"
        f"volume=1.55,asplit=2[nar][nar_raw];"
        # sidechaincompress ends with its key input, so pad it or the tail gets cut
        f"[nar_raw]apad[nar_sc];"
        f"[2:a]aformat=sample_fmts=fltp:channel_layouts=stereo,volume=0.85[mus];"
        f"[mus][nar_sc]sidechaincompress=threshold=0.045:ratio=7:attack=18:release=420[duck];"
        f"[nar][duck]amix=inputs=2:duration=longest:normalize=0,"
        f"alimiter=limit=0.95,loudnorm=I=-15:TP=-1.5:LRA=11[a]"
    )
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "warning",
           "-i", src, "-i", "audio/narration.wav", "-i", "audio/score.wav",
           "-filter_complex", fc,
           "-map", "0:v", "-map", "[a]",
           "-c:v", "copy", "-movflags", "+faststart",
           "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
           "-shortest", dst]
    print(" ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)
    print(f"-> {dst}")


if __name__ == "__main__":
    main()
