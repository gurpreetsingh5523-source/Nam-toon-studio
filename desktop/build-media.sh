#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")" && pwd)"
work="$root/.media-build"
prefix="$work/install"
ffmpeg=7.1.3
x264=0480cb05fa188d37ae87e8f4fd8f1aea3711f7ee
mkdir -p "$work" "$root/media"
cd "$work"
curl --fail --silent --show-error --location --retry 3 -o "ffmpeg-$ffmpeg.tar.xz" "https://ffmpeg.org/releases/ffmpeg-$ffmpeg.tar.xz"
printf '%s  %s\n' f0bf043299db9e3caacb435a712fc541fbb07df613c4b893e8b77e67baf3adbe "ffmpeg-$ffmpeg.tar.xz" | sha256sum -c -
tar -xf "ffmpeg-$ffmpeg.tar.xz"
if [[ ! -d x264/.git ]]; then
    git init -q x264
fi
git -C x264 fetch --depth 1 https://code.videolan.org/videolan/x264.git "$x264"
git -C x264 checkout --detach "$x264"
(cd x264 && ./configure --prefix="$prefix" --enable-static --disable-cli && make -j4 && make install)
cd "ffmpeg-$ffmpeg"
PKG_CONFIG_PATH="$prefix/lib/pkgconfig" ./configure --prefix="$prefix" --pkg-config-flags=--static \
    --disable-autodetect --disable-shared --enable-static --enable-gpl --enable-libx264 \
    --enable-zlib --disable-network --disable-doc --disable-ffplay --disable-debug
suffix=""
if [[ "${MSYSTEM:-}" == UCRT64 ]]; then
    suffix=".exe"
fi
make -j4 "ffmpeg$suffix" "ffprobe$suffix"
for tool in ffmpeg ffprobe; do
    cp "$tool$suffix" "$root/media/"
done
if [[ -n "$suffix" ]]; then
    cp /ucrt64/bin/zlib1.dll "$root/media/"
    if [[ -f /ucrt64/share/licenses/zlib/LICENSE ]]; then
        cp /ucrt64/share/licenses/zlib/LICENSE "$root/media/zlib-LICENSE.txt"
    fi
fi
cp COPYING.GPLv2 "$root/media/FFmpeg-GPL-2.0.txt"
cp ../x264/COPYING "$root/media/x264-GPL-2.0.txt"
git -C ../x264 archive --format=tar.gz --prefix=x264/ -o "$work/x264-$x264.tar.gz" HEAD
