"""Serve the local Naam Toon studio and its render queue."""
import argparse
import json
import mimetypes
import os
import re
import tempfile
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from engine import ROOT, compose, inventory, plan
import video as generation

JOBS = {}
LOCK = threading.Lock()
SLOTS = threading.BoundedSemaphore(1)
WORKLOAD_LOCK = threading.Lock()
EXPORTS = Path(os.environ.get("NAAM_EXPORT_DIR", ROOT / "exports")).resolve()


def render_job(key, project):
    def update(message):
        with LOCK:
            JOBS[key]["message"] = message
    try:
        with tempfile.TemporaryDirectory(dir=EXPORTS) as path:
            info = compose(project, EXPORTS / f"{key}.mp4", Path(path), update, generation.clip)
        with LOCK:
            JOBS[key].update(state="ready", message="MP4 verified", info=info, url=f"/video/{key}")
    except Exception as error:
        with LOCK:
            JOBS[key].update(state="error", message=str(error))
    finally:
        SLOTS.release()


class StudioHandler(BaseHTTPRequestHandler):
    def send_bytes(self, status, body, content_type):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Security-Policy",
                         "default-src 'self'; img-src 'self' data: blob:; media-src 'self' data: blob:")
        self.end_headers()
        self.wfile.write(body)

    def reply(self, data, status=200):
        self.send_bytes(status, json.dumps(data, ensure_ascii=False).encode(), "application/json")

    def host_ok(self):
        port = self.server.server_port
        return self.headers.get("Host") in (f"127.0.0.1:{port}", f"localhost:{port}")

    def do_GET(self):
        if not self.host_ok():
            return self.reply({"error": "Use the local address shown at startup."}, 403)
        path = urlsplit(self.path).path
        if path == "/api/models":
            return self.reply(inventory())
        if path == "/api/video-models":
            return self.reply({"models": generation.discover()})
        if path == "/api/video-jobs":
            return self.reply({"jobs": generation.list_jobs()})
        inference = re.fullmatch(r"/api/video-jobs/([a-f0-9]{32})", path)
        if inference:
            try:
                return self.reply(generation.progress(inference[1]))
            except ValueError as error:
                return self.reply({"error": str(error)}, 404)
        generated = re.fullmatch(r"/video-clips/([a-f0-9]{32})", path)
        if generated:
            try:
                return self.send_video(generation.clip(generated[1]))
            except ValueError as error:
                return self.reply({"error": str(error)}, 404)
        job = re.fullmatch(r"/api/jobs/([a-f0-9]{32})", path)
        if job:
            with LOCK:
                status = dict(JOBS.get(job[1], {}))
            return self.reply(status or {"error": "Unknown render job."}, 200 if status else 404)
        video = re.fullmatch(r"/video/([a-f0-9]{32})", path)
        if video:
            target = EXPORTS / f"{video[1]}.mp4"
            if target.is_file():
                return self.send_video(target)
        if path in ("/", "/app.js", "/style.css") or re.fullmatch(r"/assets/[a-z_]+\.webp", path):
            target = ROOT / (path[1:] or "index.html")
            if target.is_file():
                return self.send_bytes(200, target.read_bytes(),
                                       mimetypes.guess_type(target)[0] or "application/octet-stream")
        self.reply({"error": "Page missing."}, 404)

    def send_video(self, target):
        length = target.stat().st_size
        request_range = self.headers.get("Range")
        start, end = 0, length - 1
        if request_range:
            match = re.fullmatch(r"bytes=(\d*)-(\d*)", request_range)
            if match and match[1]:
                start = int(match[1])
                end = min(end, int(match[2])) if match[2] else end
            elif match and match[2]:
                start = max(0, length - int(match[2]))
            if not match or not (match[1] or match[2]) or start > end:
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{length}")
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
        self.send_response(206 if request_range else 200)
        self.send_header("Content-Type", "video/mp4")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(end - start + 1))
        if request_range:
            self.send_header("Content-Range", f"bytes {start}-{end}/{length}")
        self.end_headers()
        remaining = end - start + 1
        try:
            with target.open("rb") as handle:
                handle.seek(start)
                while remaining:
                    block = handle.read(min(remaining, 256 * 1024))
                    self.wfile.write(block)
                    remaining -= len(block)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_POST(self):
        if (not self.host_ok() or self.headers.get("Origin") != "http://" + self.headers["Host"]
                or self.headers.get_content_type() != "application/json"):
            return self.reply({"error": "Use the studio's local browser page."}, 403)
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 32 * 1024 ** 2:
                return self.reply({"error": "Project payload exceeds 32 MB or is empty."}, 413)
            data = json.loads(self.rfile.read(length))
            if self.path == "/api/plan":
                return self.reply(plan(data))
            if self.path == "/api/video-jobs":
                with WORKLOAD_LOCK:
                    if not SLOTS.acquire(blocking=False):
                        return self.reply({"error": "Wait until the current render finishes."}, 429)
                    try:
                        job = generation.submit(data)
                    finally:
                        SLOTS.release()
                return self.reply(job, 202)
            if self.path == "/api/render":
                EXPORTS.mkdir(exist_ok=True)
                with WORKLOAD_LOCK:
                    if any(job["state"] in ("submitting", "queued") for job in generation.list_jobs()):
                        return self.reply({"error": "Wait until the video-generation job finishes."}, 429)
                    if not SLOTS.acquire(blocking=False):
                        return self.reply({"error": "A render is already active. Try again when it ends."}, 429)
                key = uuid.uuid4().hex
                with LOCK:
                    JOBS[key] = {"state": "running", "message": "Preparing media"}
                threading.Thread(target=render_job, args=(key, data), daemon=True).start()
                return self.reply({"job": key}, 202)
        except (ValueError, KeyError, TypeError, AttributeError) as error:
            return self.reply({"error": str(error)}, 400)
        self.reply({"error": "Route missing."}, 404)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    with ThreadingHTTPServer(("127.0.0.1", args.port), StudioHandler) as server:
        print(f"Open http://127.0.0.1:{server.server_port}", flush=True)
        server.serve_forever()
