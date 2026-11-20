"""Local ComfyUI submission and persistent scene clip records."""
import json
import os
import re
import secrets
import shutil
import subprocess
import tempfile
import threading
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

from engine import ROOT, run

STORE = ROOT / "generated"
LOCK = threading.Lock()
ID = re.compile(r"[a-f0-9]{32}")
NODES = ("UNETLoader", "CLIPLoader", "VAELoader", "CLIPTextEncode",
         "ModelSamplingSD3", "KSampler", "VAEDecode", "CreateVideo", "SaveVideo")
MODELS = {
    "wan21-13b": {
        "name": "Wan 2.1 T2V 1.3B", "unet": ("wan2.1_t2v_1.3B_fp16.safetensors",),
        "vae": "wan_2.1_vae.safetensors", "latent": "EmptyHunyuanLatentVideo",
        "fps": 16, "shift": 6, "cfg": 6, "steps": 20,
    },
    "wan22-5b": {
        "name": "Wan 2.2 T2V 5B", "unet": ("wan2.2_ti2v_5B_fp16.safetensors",),
        "vae": "wan2.2_vae.safetensors", "latent": "Wan22ImageToVideoLatent",
        "fps": 24, "shift": 8, "cfg": 5, "steps": 20,
    },
}
ENCODERS = ("umt5_xxl_fp8_e4m3fn_scaled.safetensors", "umt5_xxl_fp16.safetensors")
SHAPES = {"landscape": (480, 288), "portrait": (288, 480), "square": (320, 320)}
LENGTHS = (17, 33, 49)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())


def request(path, data=None, timeout=5, limit=16 * 1024 ** 2, target=None):
    port = int(os.environ.get("NAAM_COMFY_PORT", "8188"))
    req = urllib.request.Request(
        f"http://127.0.0.1:{port}{path}",
        data=None if data is None else json.dumps(data).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with OPENER.open(req, timeout=timeout) as response:
            if target is None:
                raw = response.read(limit + 1)
                if len(raw) > limit:
                    raise ValueError("ComfyUI response exceeded the size limit.")
                return json.loads(raw)
            total = 0
            with target.open("wb") as output:
                for block in iter(lambda: response.read(256 * 1024), b""):
                    total += len(block)
                    if total > limit:
                        raise ValueError("Generated clip exceeded the size limit.")
                    output.write(block)
    except urllib.error.HTTPError as error:
        raise ValueError(f"ComfyUI returned HTTP {error.code} for {path.split('?')[0]}.") from error
    except OSError as error:
        raise ValueError(f"ComfyUI is unavailable on local port {port}.") from error


def options(info, node, field):
    definition = info.get(node, {}).get("input", {}).get("required", {}).get(field, [])
    if definition and isinstance(definition[0], list):
        return definition[0]
    if len(definition) > 1 and isinstance(definition[1], dict):
        return definition[1].get("options", [])
    return []


def installed(available, names):
    for name in names:
        for path in available:
            if isinstance(path, str) and path.replace(chr(92), "/").split("/")[-1] == name:
                return path
    return ""


def discover():
    try:
        info = request("/object_info")
        if not isinstance(info, dict) or not info:
            raise ValueError("Empty node inventory.")
        problem = ""
    except (ValueError, TypeError):
        info = {}
        problem = "Start a local ComfyUI instance and refresh."
    result = []
    for key, spec in MODELS.items():
        missing = [node for node in (*NODES, spec["latent"]) if node not in info]
        local_unets = options(info, "UNETLoader", "unet_name")
        local_vaes = options(info, "VAELoader", "vae_name")
        local_encoders = options(info, "CLIPLoader", "clip_name")
        unet = installed(local_unets, spec["unet"])
        vae = installed(local_vaes, (spec["vae"],))
        encoder = installed(local_encoders, ENCODERS)
        assets = [(unet, spec["unet"][0]), (vae, spec["vae"]), (encoder, ENCODERS[0])]
        missing_weights = [fallback for available, fallback in assets if not available]
        if info and not missing and missing_weights:
            problem_for_model = "Missing weights: " + ", ".join(missing_weights)
        elif info and missing:
            problem_for_model = "Missing native nodes: " + ", ".join(missing)
        else:
            problem_for_model = problem
        if not problem_for_model and not all(shutil.which(tool) for tool in ("ffmpeg", "ffprobe")):
            problem_for_model = "Install FFmpeg and ffprobe to import the result."
        result.append(dict(id=key, name=spec["name"], mode="text-to-video", fps=spec["fps"],
                           available=not problem_for_model, reason=problem_for_model,
                           unet=unet, vae=vae, encoder=encoder))
    return result


def workflow(model, job, width, height):
    spec = MODELS[model["id"]]
    latent = dict(width=width, height=height, length=job["frames"], batch_size=1)
    if spec["latent"] == "Wan22ImageToVideoLatent":
        latent["vae"] = ["3", 0]
    config = [
        ("UNETLoader", dict(unet_name=model["unet"], weight_dtype="default")),
        ("CLIPLoader", dict(clip_name=model["encoder"], type="wan", device="default")),
        ("VAELoader", dict(vae_name=model["vae"])),
        ("CLIPTextEncode", dict(clip=["2", 0], text=job["prompt"])),
        ("CLIPTextEncode", dict(clip=["2", 0], text="still frame, flicker, text, watermark, distorted motion")),
        ("ModelSamplingSD3", dict(model=["1", 0], shift=spec["shift"])),
        (spec["latent"], latent),
        ("KSampler", dict(model=["6", 0], positive=["4", 0], negative=["5", 0],
                          latent_image=["7", 0], seed=job["seed"], steps=spec["steps"],
                          cfg=spec["cfg"], sampler_name="uni_pc", scheduler="simple", denoise=1)),
        ("VAEDecode", dict(samples=["8", 0], vae=["3", 0])),
        ("CreateVideo", dict(images=["9", 0], fps=spec["fps"])),
        ("SaveVideo", dict(video=["10", 0], filename_prefix="naam-toon/clip-" + job["id"],
                          format="mp4", codec="auto")),
    ]
    return {str(i): dict(class_type=node, inputs=inputs) for i, (node, inputs) in enumerate(config, 1)}


def path_for(job_id):
    if not isinstance(job_id, str) or not ID.fullmatch(job_id):
        raise ValueError("Invalid video job ID.")
    return STORE / job_id


def record(job):
    directory = path_for(job["id"])
    temporary = directory / "job.json.tmp"
    temporary.write_text(json.dumps(job, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(directory / "job.json")


def read_job(job_id):
    path = path_for(job_id) / "job.json"
    if not path.is_file():
        raise ValueError("Video job was not found.")
    return json.loads(path.read_text(encoding="utf-8"))


def list_jobs():
    files = sorted(STORE.glob("*/job.json"), key=lambda path: path.stat().st_mtime, reverse=True)
    return [read_job(path.parent.name) for path in files if ID.fullmatch(path.parent.name)]


def submit(data):
    prompt, scene = data.get("prompt"), data.get("scene")
    frames, shape = data.get("frames"), data.get("shape")
    seed = data.get("seed")
    if not isinstance(prompt, str) or not 0 < len(prompt.strip()) <= 2000:
        raise ValueError("Enter a motion prompt up to 2,000 characters.")
    if not isinstance(scene, str) or not ID.fullmatch(scene):
        raise ValueError("Select a valid scene.")
    if frames not in LENGTHS or shape not in SHAPES:
        raise ValueError("Choose a supported clip size and frame count.")
    if seed is None:
        seed = secrets.randbelow(2 ** 32)
    if type(seed) is not int or not 0 <= seed < 2 ** 32:
        raise ValueError("Seed must be an integer from 0 to 4,294,967,295.")
    model = next((model for model in discover() if model["id"] == data.get("model")), None)
    if not model or not model["available"]:
        raise ValueError(model["reason"] if model else "Select an available video model.")
    with LOCK:
        if any(job["state"] in ("submitting", "queued") for job in list_jobs()):
            raise ValueError("One video job is already active. Open its status before starting another.")
        job_id = uuid.uuid4().hex
        job = dict(id=job_id, scene=scene, model=model["id"], model_name=model["name"],
                   weights={key: model[key] for key in ("unet", "vae", "encoder")},
                   prompt=prompt.strip(), frames=frames, shape=shape, seed=seed, fps=model["fps"],
                   state="submitting", message="Submitting to local ComfyUI")
        path_for(job_id).mkdir(parents=True)
        record(job)
        try:
            result = request("/prompt", {"prompt": workflow(model, job, *SHAPES[shape]),
                                        "client_id": job_id}, timeout=12)
            prompt_id = str(uuid.UUID(result["prompt_id"]))
            job.update(prompt_id=prompt_id, state="queued", message="Queued on local ComfyUI")
        except (ValueError, KeyError, TypeError) as error:
            job.update(state="error", message=str(error))
        record(job)
        return job


def clip(job_id):
    job = read_job(job_id)
    path = path_for(job_id) / "clip.mp4"
    if not path.is_file() or job["state"] != "ready":
        raise ValueError("Generated clip is unavailable on this computer.")
    return path


def receive(job, item):
    folder = path_for(job["id"])
    query = urllib.parse.urlencode({key: item.get(key, "") for key in ("filename", "subfolder", "type")})
    with tempfile.TemporaryDirectory(dir=folder) as directory:
        original = Path(directory) / "original.mp4"
        converted = Path(directory) / "converted.mp4"
        request("/view?" + query, target=original, timeout=15, limit=128 * 1024 ** 2)
        run(["ffmpeg", "-v", "error", "-nostdin", "-protocol_whitelist", "file",
             "-format_whitelist", "mov", "-threads", "2", "-i", original, "-map", "0:v:0", "-an", "-c:v", "libx264",
             "-pix_fmt", "yuv420p", "-threads", "2", "-movflags", "+faststart", converted], timeout=45)
        metadata = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                                   "-show_entries", "stream=codec_name,width,height,nb_frames:format=duration",
                                   "-of", "json", converted]))
        stream = metadata["streams"][0]
        frame_count = int(stream.get("nb_frames") or 0)
        if frame_count < 2 or stream["codec_name"] != "h264":
            raise ValueError("ComfyUI did not return a valid multi-frame video.")
        converted.replace(folder / "clip.mp4")
    job.update(state="ready", message="Generated clip verified", url=f"/video-clips/{job['id']}",
               seconds=float(metadata["format"]["duration"]), width=stream["width"],
               height=stream["height"], frame_count=frame_count)


def progress(job_id):
    with LOCK:
        job = read_job(job_id)
        if job["state"] == "submitting":
            job.update(state="error", message="Studio stopped before it could record ComfyUI's queue ID.")
            record(job)
        if job["state"] != "queued":
            return job
        try:
            history = request("/history/" + job["prompt_id"])
        except ValueError as error:
            return {**job, "message": str(error) + " Job can resume when it reconnects."}
        item = history.get(job["prompt_id"])
        if not item:
            try:
                queue = request("/queue")
            except ValueError:
                return job
            current = queue.get("queue_running", []) + queue.get("queue_pending", [])
            if any(len(entry) > 1 and entry[1] == job["prompt_id"] for entry in current):
                return {**job, "message": "ComfyUI is processing or waiting to start."}
            # Completion may have raced with the queue read. Recheck history.
            try:
                item = request("/history/" + job["prompt_id"]).get(job["prompt_id"])
            except ValueError:
                return job
            if not item:
                job.update(state="error", message="ComfyUI no longer has this job in its queue or history.")
                record(job)
                return job
        if item.get("status", {}).get("status_str") != "success":
            errors = item.get("status", {}).get("messages", [])
            detail = next((value.get("exception_message", "") for label, value in errors
                           if label == "execution_error" and isinstance(value, dict)), "")
            job.update(state="error", message="ComfyUI generation failed. " + detail[:300])
        else:
            outputs = item.get("outputs", {}).get("11", {})
            videos = [asset for group in ("images", "videos", "gifs") for asset in outputs.get(group, [])
                      if asset.get("type") == "output"
                      and asset.get("subfolder", "").replace(chr(92), "/") == "naam-toon"
                      and re.fullmatch(r"clip-" + job_id + r"_\d+_\.mp4", asset.get("filename", ""))]
            if not videos:
                job.update(state="error", message="ComfyUI completed without the expected saved MP4.")
            else:
                try:
                    receive(job, videos[0])
                except (ValueError, KeyError, IndexError, OSError, subprocess.TimeoutExpired) as error:
                    job.update(state="error", message="Clip import failed. " + str(error))
        record(job)
        return job
