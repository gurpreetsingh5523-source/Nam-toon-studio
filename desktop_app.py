"""Run Naam Toon in the operating system's web view."""
import argparse
import ctypes
import os
import sys
import threading
import traceback
from http.server import ThreadingHTTPServer
from pathlib import Path

import webview

ROOT = Path(__file__).resolve().parent


def data_directory():
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "Naam Toon Studio"
    if sys.platform == "win32":
        return Path(os.environ["LOCALAPPDATA"]) / "Naam Toon Studio"
    return Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")) / "naam-toon-studio"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", type=Path, metavar="DIRECTORY")
    args = parser.parse_args()
    state = args.self_test.resolve() if args.self_test else data_directory()
    state.mkdir(parents=True, exist_ok=True)
    media = ROOT / "media"
    if getattr(sys, "frozen", False):
        os.environ["NAAM_MEDIA_DIR"] = str(media)
        if sys.platform == "darwin":
            ctypes.CDLL(str(ROOT / "libfribidi.dylib"))
        elif sys.platform == "win32":
            ctypes.CDLL(str(ROOT / "libfribidi-0.dll"))
    os.environ["NAAM_EXPORT_DIR"] = str(state / "exports")
    os.environ["NAAM_GENERATED_DIR"] = str(state / "generated")

    from server import SLOTS, StudioHandler

    gui = {"linux": "gtk", "win32": "edgechromium"}.get(sys.platform)
    try:
        server = ThreadingHTTPServer(("127.0.0.1", 0 if args.self_test else 18765), StudioHandler)
    except OSError:
        webview.create_window("Naam Toon Studio", width=560, height=240,
                              html="<p>The studio could not start. Close any other open copy and try again.</p>")
        webview.start(gui=gui)
        return
    with server:
        worker = threading.Thread(target=server.serve_forever)
        worker.start()
        base = f"http://127.0.0.1:{server.server_port}"
        try:
            webview.settings["ALLOW_DOWNLOADS"] = True
            window = webview.create_window("Naam Toon Studio", base, width=1240, height=850,
                                           min_size=(780, 590), hidden=bool(args.self_test))

            def verify():
                from tools.smoke import check

                try:
                    if not window.events.loaded.wait(35):
                        raise RuntimeError("The desktop window did not load.")
                    if "Naam Toon Studio" not in window.run_js("document.title"):
                        raise RuntimeError("The desktop window loaded the wrong page.")
                    check(base, state)
                    (state / "result.txt").write_text("PASS\n", encoding="utf-8")
                except Exception:
                    (state / "result.txt").write_text(traceback.format_exc(), encoding="utf-8")
                finally:
                    window.destroy()

            webview.start(verify if args.self_test else None, gui=gui,
                          private_mode=bool(args.self_test), storage_path=str(state / "browser"),
                          icon=str(ROOT / "studio-icon.png"))
        finally:
            server.shutdown()
            worker.join()
            # Let an active export finish and remove its temporary workspace.
            with SLOTS:
                pass


if __name__ == "__main__":
    main()
