#!/usr/bin/env bash
# One-time setup of a fresh machine/session for the Echoes of Life pipeline.
set -euo pipefail
command -v ffmpeg >/dev/null || { echo "ffmpeg is required"; exit 1; }
if ! command -v fluidsynth >/dev/null || [ ! -f /usr/share/sounds/sf2/FluidR3_GM.sf2 ]; then
  (apt-get install -y -q fluidsynth fluid-soundfont-gm || (apt-get update -q && apt-get install -y -q fluidsynth fluid-soundfont-gm)) >/dev/null
fi
python3 -c "import mido, PIL, numpy" 2>/dev/null || pip install -q --break-system-packages mido pillow numpy
fc-list | grep -q "Inter" || echo "warning: Inter font not installed; captions will fall back to another sans font"
echo "setup ok"
