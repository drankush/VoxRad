# FFmpeg License Compliance

## Attribution
- This application uses FFmpeg, which is licensed under the GNU General Public License (GPL) version 2 or later. 
- The full text of the license can be found in the COPYING.GPLv2 and COPYING.GPLv3 files included with this distribution.
- FFmpeg is a trademark of Fabrice Bellard, originator of the FFmpeg project.
- FFmpeg website: https://ffmpeg.org/
- The source code of FFmpeg can be obtained from: https://git.ffmpeg.org/ffmpeg.git

## Source Code
- As required by the GPL, the complete source code for this application (VOXRAD) is available here: https://github.com/drankush/voxrad/ and is licensed under GPLv3.
- The version of FFmpeg it uses is: ffmpeg version 4.2.1-tessus

## Compilation Instructions for Mac

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew install yasm pkg-config
brew install lame

cd ~
git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg
cd ffmpeg

./configure --enable-gpl --disable-nonfree --enable-libmp3lame --enable-shared --disable-static --disable-doc --disable-programs --disable-avdevice --disable-avfilter --disable-avformat --disable-avutil --disable-postproc --disable-swresample --disable-swscale --disable-everything

make -j$(sysctl -n hw.ncpu)

```
## Compilation Instructions for Windows using MSYS2 MinGW

```
$ pacman -Syu

$ pacman -S base-devel git yasm pkg-config make

$ pacman -S mingw-w64-x86_64-toolchain

$ pacman -S mingw-w64-x86_64-lame

$ git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg

$ cd ffmpeg

$ ./configure --prefix=/mingw64 --enable-gpl --enable-libmp3lame --disable-nonfree

$ make -j$(nproc)
```
- After compilation, the ffmpeg executable was placed in bin/ffmpeg/. This can be accessed at https://github.com/drankush/voxrad/bin/ffmpeg/.

---
