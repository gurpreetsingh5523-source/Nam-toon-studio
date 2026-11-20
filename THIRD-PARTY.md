# Asset licenses

The six sample illustrations were created for this release by the included `tools/draw_sample_art.py` and are under this project's MIT license.

Mukta Mahee Regular and Bold are distributed under the SIL Open Font License 1.1. The copyright statement and terms are in `fonts/OFL.txt`. [Upstream font files](https://github.com/google/fonts/tree/main/ofl/muktamahee)

## Desktop packages

- FFmpeg and x264 are separate command-line executables used by the MIT-licensed
  studio. The included media tools are built under GPL-2.0 terms with libx264.
  The exact FFmpeg and x264 source archives accompany the packages. The build
  configuration and commands are in `desktop/build-media.sh`.
- The desktop wrapper uses pywebview (BSD-3-Clause), Python (PSF), Pillow (HPND)
  and the PyInstaller bootloader (GPL with a distribution exception).
- FriBiDi (LGPL-2.1-or-later) enables bidirectional text shaping for Pillow.
  The macOS and Windows builds include the FriBiDi library. Ubuntu uses its
  system library.
