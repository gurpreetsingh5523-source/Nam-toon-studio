# Naam Toon Studio

Naam Toon is an MIT-licensed local production studio. It takes selected notes, a script or a shot list to an editable storyboard and exports a playable MP4. The source archive includes the web interface, Python production engine and six existing project illustrations. The sample is a fictional Punjabi village scene.

## Run locally

Install Python 3.12 and FFmpeg with `ffmpeg` and `ffprobe` on PATH. FFmpeg must include libx264 and AAC encoding. Install eSpeak NG for optional English and Punjabi narration. On macOS the studio can also use Samantha for English narration.

| Platform | FFmpeg | Launch from the extracted folder |
| --- | --- | --- |
| macOS | `brew install ffmpeg fribidi` | `./launch.sh` |
| Windows | `winget install --id Gyan.FFmpeg -e`, then reopen Command Prompt | `launch.cmd` |
| Linux (Ubuntu/Debian) | `sudo apt install ffmpeg python3-venv libfribidi0` | `./launch.sh` |

On Windows x64, install FriBiDi from [MSYS2](https://www.msys2.org/) using `pacman -S mingw-w64-ucrt-x86_64-fribidi` in its UCRT64 terminal. The launcher recognises the default MSYS2 install location. For other locations, add the UCRT64 `bin` directory to PATH.

The launcher creates a project-local Python environment and installs the Pillow wheel on first use. Models and FFmpeg are installed independently. Binaries and model weights are excluded from the versioned ZIPs. The ZIPs contain source and native launch scripts. Run `./launch.sh --smoke` or `launch.cmd --smoke` to render and verify an MP4 on your computer.

Open `http://127.0.0.1:8765`. To use a different port, pass `--port 8766`. The studio listens on loopback. Exact excerpts and the script splitter require only the studio. To add a model, start Ollama on its default local port and install a text-capable model, then reload the studio. The selected model handles planning. FFmpeg handles video assembly.

## Workflows

| Category | What you can produce |
| --- | --- |
| Source overview | Import or paste UTF-8 TXT/MD, select sources, set a focus and scene-count format, review selected excerpts and source links, then append or replace storyboard scenes. |
| Script & media | Split prose into scenes or draft with an installed text model. Attach local images, footage and audio. |
| Clip assembly | Draft a shot list and assign imported or locally generated clips. Long clips trim to scene length and short clips loop. |
| Presenter | Draft narration, select a still presenter image and add imported audio or optional system speech. |
| Animation | Create still-image animatics with push-ins, scene timing and fades through black. |

The storyboard supports editing, duplication, reordering, removal, playback and scrubbing. Undo restores the last structural storyboard change. The monitor offers a visual preview. Play the rendered MP4 to hear its audio. Uploaded audio takes precedence over synthesized speech. If neither is set, a scene uses its assigned clip's audio when available. Generated speech must fit the scene duration.

Exports are 24 fps H.264/AAC at 1280 × 720, 720 × 1280 or 720 × 720. Burned-in captions show the scene title and up to four lines of narration on one card. For longer narration, split the scene into shorter beats or turn off the card. Export progress reports actual scene renders and verification. Download the MP4 from the output player. Local render files are also stored under `exports/`, keyed by render ID.

Save Project downloads JSON with embedded media. Open Project accepts this format and the earlier offline Naam Toon storyboard project files. Browser storage is best effort for larger projects. Keep a JSON copy if the studio reports a storage limit. Each asset can be up to 18 MB with about 29 MB total encoded media. Projects can contain up to 30 scenes, with a maximum combined duration of 10 minutes per render.

Text models choose source passages and can propose headings. Source-overview narration is copied from the selected passage so it retains the original language and wording. Review model-proposed headings before export. The script and brief workflows can request English or Punjabi from compatible Ollama models.

## Generate moving video

The video model is independent of the planning model. Open **Clip assembly → Generate moving video** on a scene. Refresh the video models, choose a model, describe visible motion, select a shape and frame count, and click **Generate scene clip**. An empty seed selects a random one. When the saved result has been verified, choose **Use in scene** or download it. The regular **Video clip** menu can also reuse any generated clip in another scene.

Start a local ComfyUI instance using a working ComfyUI Python environment. The adapter was checked against ComfyUI 0.30.0 with native nodes:

```sh
python main.py --listen 127.0.0.1 --port 8188 --disable-api-nodes --disable-all-custom-nodes --disable-metadata
```

Launch Naam Toon using the instructions above. For a different ComfyUI port, set `NAAM_COMFY_PORT` in the terminal that launches Naam Toon. The connection accepts only a local loopback port and uses the built-in ComfyUI graph. Put the following weights in ComfyUI's model directories, keeping the published filenames. The adapter checks the filenames reported by the runtime before enabling each model.

| Profile | `models/diffusion_models` | `models/vae` | `models/text_encoders` |
| --- | --- | --- | --- |
| Wan 2.1 T2V 1.3B | `wan2.1_t2v_1.3B_fp16.safetensors` | `wan_2.1_vae.safetensors` | `umt5_xxl_fp8_e4m3fn_scaled.safetensors` or `umt5_xxl_fp16.safetensors` |
| Wan 2.2 T2V 5B | `wan2.2_ti2v_5B_fp16.safetensors` | `wan2.2_vae.safetensors` | Same encoder as above |

- [Wan 2.1 weights](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/tree/main/split_files)
- [Wan 2.2 weights](https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/tree/main/split_files) · [ComfyUI Wan 2.2 workflow](https://docs.comfy.org/tutorials/video/wan/wan2_2)

The profiles generate 17, 33 or 49 frames at 16 fps or 24 fps respectively. The job stores the scene ID, model and weights, prompt, seed, queue ID and output. One project render or one studio-managed generation can run at a time. FFmpeg uses at most two encoder threads per video stream. ComfyUI jobs submitted from other apps are outside these limits. Reopening the studio resumes checking queued jobs as long as the ComfyUI queue or history still has them. The studio keeps a normalized MP4 under `generated/<job-id>/clip.mp4`. Preserve that directory alongside saved JSON projects to retain local clip links, or download and import the clip explicitly when moving the project to another computer. Keep ComfyUI running until the clip has been collected.

This release tested the live ComfyUI connection, both graph routes through model validation, and end-to-end publication to the local clip library using a weight-free diagnostic graph. Neither Wan profile ran inference on the test Mac because the checkpoints, VAE and encoder were absent. A GPU and host with enough memory for the complete selected pipeline are required. Declared weights and nodes establish availability for submission. They do not certify hardware fit or output quality.

Presenter uses still portraits. Lip-sync, external stock search, PDF/URL ingestion, multimodel comparison and full nonlinear editing are outside this build.

The workflow survey compared seven tools across source-grounded explainers, generative clips, script and media editing, presenters, animatics, local model workflows, and model switching: NotebookLM, Runway, Descript, HeyGen, Toon Boom Storyboard Pro, ComfyUI and Open WebUI.

## Desktop builds

The 2.1 desktop edition uses the same studio inside the platform's web view. Its
packages include the Python runtime, Pillow, FFmpeg and FFprobe. The core
storyboard and MP4 export work offline. Optional Ollama, ComfyUI, model weights
and eSpeak NG are installed separately.

- macOS Apple Silicon: extract the ZIP and open the app icon. Builds without
  Developer ID signing and notarization can be blocked by Gatekeeper.
- Windows x64: run the Setup EXE and open Naam Toon Studio in the Start menu.
  The desktop window uses the system Microsoft Edge WebView2 runtime.
- Ubuntu 24.04 x64: install the DEB with a graphical package installer that can
  resolve dependencies, then open Naam Toon Studio from the app menu. It uses
  the system GTK, WebKitGTK and GStreamer packages.

The desktop window uses loopback port 18765 to keep autosaved projects
available across restarts. Closing the window stops the local server. An
in-progress MP4 export finishes and removes its temporary files before the
process exits. The visible studio does not require a terminal.

The [desktop workflow](.github/workflows/desktop.yml) builds the platform
packages and checks that each opens the studio page, renders a Punjabi- and
English-captioned MP4, downloads it, and exits with no temporary render
directories. See [third-party notices](THIRD-PARTY.md) for media build sources.
