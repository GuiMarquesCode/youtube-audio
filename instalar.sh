#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
command -v python3 >/dev/null || { echo 'Instale Python 3.10 ou superior.'; exit 1; }
if ! command -v ffmpeg >/dev/null || ! command -v ffprobe >/dev/null; then
    echo 'Instale antes: sudo apt install ffmpeg python3-venv'
    exit 1
fi
python3 -m venv .venv || { echo 'No Ubuntu, instale: sudo apt install python3-venv'; exit 1; }
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install --upgrade -r requirements.txt
chmod +x youtube-audio
printf '\nPronto! Execute: ./youtube-audio\n'
