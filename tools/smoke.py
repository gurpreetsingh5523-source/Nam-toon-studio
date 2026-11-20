"""Start the studio and render the same two-scene fixture on each host."""
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.request import Request, urlopen

def check(base, directory):
    from engine import run

    def request(path, data=None):
        headers = {"Origin": base, "Content-Type": "application/json"}
        body = json.dumps(data).encode() if data is not None else None
        return urlopen(Request(base + path, data=body, headers=headers), timeout=10)

    with request("/") as page:
        assert "Naam Toon Studio" in page.read().decode()
    with request("/api/render", dict(scenes=[
        dict(title="ਪਾਣੀ ਦੀ ਸੰਭਾਲ", script="ਪਿੰਡ ਦੇ ਲੋਕ ਮੀਂਹ ਦਾ ਪਾਣੀ ਸੰਭਾਲਦੇ ਹਨ।",
             duration=1, background="field", motion="push"),
        dict(title="English title", script="A still image moves through a gentle fade.",
             duration=1, background="talab", transition="fade", actor="sant_kaur"),
    ])) as result:
        job = json.load(result)["job"]
    for _ in range(120):
        with request("/api/jobs/" + job) as result:
            state = json.load(result)
        if state["state"] != "running":
            break
        time.sleep(.25)
    assert state["state"] == "ready", state
    with request(state["url"]) as result:
        output = directory / "verified-download.mp4"
        output.write_bytes(result.read())
    probe = json.loads(run([
        "ffprobe", "-v", "error", "-show_streams", "-show_format",
        "-of", "json", str(output)
    ]))
    assert [stream["codec_name"] for stream in probe["streams"]] == ["h264", "aac"], probe
    assert (probe["streams"][0]["width"], probe["streams"][0]["height"]) == (1280, 720), probe
    assert abs(float(probe["format"]["duration"]) - 2) < .15, probe
    print(f"PASS {sys.platform}: HTTP render and download, Punjabi and English caption inputs, H.264/AAC")


def main():
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    root = Path(__file__).resolve().parents[1]
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    with tempfile.TemporaryDirectory() as tmp:
        env["NAAM_EXPORT_DIR"] = tmp
        with subprocess.Popen([sys.executable, str(root / "server.py"), "--port", "0"],
                              stdout=subprocess.PIPE, text=True, encoding="utf-8", env=env) as server:
            try:
                base = server.stdout.readline().strip().removeprefix("Open ")
                assert base.startswith("http://127.0.0.1:"), base

                check(base, Path(tmp))
            finally:
                server.terminate()


if __name__ == "__main__":
    main()
