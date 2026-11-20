"""Freeze the desktop application and assemble the platform's download."""
import os
import shutil
import subprocess
import sys
from pathlib import Path


def build():
    root = Path(__file__).resolve().parents[1]
    desktop = root / "desktop"
    output = desktop / "output"
    dist = root / "dist"
    version = (root / "VERSION").read_text().strip()
    mac = sys.platform == "darwin"
    windows = sys.platform == "win32"
    name = "Naam Toon Studio" if mac else "NaamToonStudio"
    mkicon = desktop / "make-icon.py"
    subprocess.run([sys.executable, str(mkicon), str(output)], check=True)
    args = [sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--windowed",
            "--name", name, "--distpath", str(dist), "--specpath", str(root / "build"),
            "--paths", str(root)]
    files = [(root / entry, ".") for entry in ("index.html", "style.css", "app.js", "LICENSE", "THIRD-PARTY.md")]
    files += [(root / entry, entry) for entry in ("assets", "fonts")]
    files += [(output / "studio-icon.png", "."), (desktop / "media", "media")]
    for source, destination in files:
        args += ["--add-data", f"{source}{os.pathsep}{destination}"]
    if mac or windows:
        extension = "icns" if mac else "ico"
        args += ["--icon", str(output / f"studio.{extension}")]
        fribidi = Path(os.environ["NAAM_FRIBIDI"])
        if mac:
            dylib = output / "libfribidi.dylib"
            shutil.copyfile(fribidi, dylib)
            subprocess.run(["install_name_tool", "-id", "@rpath/libfribidi.dylib", str(dylib)], check=True)
            fribidi = dylib
        args += ["--add-binary", f"{fribidi}{os.pathsep}."]
    if mac:
        args += ["--osx-bundle-identifier", "com.sevabots.naamtoonstudio"]
    args += [str(root / "desktop_app.py")]
    subprocess.run(args, cwd=root, check=True)

    if mac:
        import platform
        import plistlib

        app = dist / f"{name}.app"
        plist = app / "Contents" / "Info.plist"
        info = plistlib.loads(plist.read_bytes())
        info.update(CFBundleShortVersionString=version, CFBundleVersion=version)
        plist.write_bytes(plistlib.dumps(info))
        subprocess.run(["codesign", "--force", "--deep", "--sign", "-", str(app)], check=True)
        subprocess.run(["codesign", "--verify", "--deep", "--strict", str(app)], check=True)
        archive = output / f"Naam-Toon-Studio-{version}-macOS-{platform.machine()}.zip"
        subprocess.run(["ditto", "-c", "-k", "--sequesterRsrc", "--keepParent", str(app), str(archive)], check=True)
    elif windows:
        subprocess.run([os.environ["INNO_ISCC"], f"/DStudioVersion={version}", str(desktop / "studio.iss")], check=True)
    else:
        package = root / "build" / "deb"
        install = package / "opt" / "naam-toon-studio"
        shutil.copytree(dist / name, install, dirs_exist_ok=True, symlinks=True)
        metadata = package / "DEBIAN"
        metadata.mkdir(exist_ok=True)
        (metadata / "control").write_text(
            f"Package: naam-toon-studio\nVersion: {version}\nArchitecture: amd64\n"
            "Maintainer: Seva Bots <https://sevabots.com>\n"
            "Depends: libgtk-3-0t64, libwebkit2gtk-4.1-0, gir1.2-webkit2-4.1, "
            "gir1.2-gtk-3.0, libfribidi0, gstreamer1.0-libav, gstreamer1.0-plugins-good\n"
            "Description: Local storyboard editor and video renderer\n"
        )
        applications = package / "usr/share/applications"
        applications.mkdir(parents=True, exist_ok=True)
        (applications / "naam-toon-studio.desktop").write_text(
            "[Desktop Entry]\nType=Application\nName=Naam Toon Studio\n"
            "Exec=/opt/naam-toon-studio/NaamToonStudio\nIcon=naam-toon-studio\n"
            "Categories=AudioVideo;Video;\nTerminal=false\n"
        )
        icons = package / "usr/share/icons/hicolor/512x512/apps"
        icons.mkdir(parents=True, exist_ok=True)
        from PIL import Image

        Image.open(output / "studio-icon.png").resize((512, 512)).save(icons / "naam-toon-studio.png")
        subprocess.run(["dpkg-deb", "--root-owner-group", "--build", str(package),
                        str(output / f"Naam-Toon-Studio-{version}-Ubuntu-24.04-amd64.deb")], check=True)


if __name__ == "__main__":
    build()
