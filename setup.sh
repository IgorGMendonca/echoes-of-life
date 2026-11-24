#!/usr/bin/env bash
# One-time setup of a fresh machine/session for the Echoes of Life pipeline.
set -euo pipefail
command -v ffmpeg >/dev/null || { echo "ffmpeg is required"; exit 1; }
if ! command -v fluidsynth >/dev/null || [ ! -f /usr/share/sounds/sf2/FluidR3_GM.sf2 ]; then
  (apt-get install -y -q fluidsynth fluid-soundfont-gm || (apt-get update -q && apt-get install -y -q fluidsynth fluid-soundfont-gm)) >/dev/null
fi
python3 -c "import mido, PIL, numpy" 2>/dev/null || pip install -q --break-system-packages mido pillow numpy
fc-list : family | grep -c "Inter" >/dev/null || echo "warning: Inter font not installed; captions will fall back to another sans font"
# official Remotion agent skills (no redistribution licence, so fetched instead of committed)
REMOTION_SKILLS_COMMIT=a3f4098a2afd0e13f6a6f8c8760e275f75457ea9
if [ ! -d .claude/skills/remotion-markup ]; then
  tmp=$(mktemp -d)
  if git clone -q https://github.com/remotion-dev/skills "$tmp/r" && git -C "$tmp/r" checkout -q "$REMOTION_SKILLS_COMMIT" 2>/dev/null || git -C "$tmp/r" fetch -q --depth 1 origin "$REMOTION_SKILLS_COMMIT" && git -C "$tmp/r" checkout -q "$REMOTION_SKILLS_COMMIT"; then
    cp -R "$tmp/r/skills/"* .claude/skills/
  else
    echo "warning: could not fetch the Remotion skills (optional)"
  fi
  rm -rf "$tmp"
fi
echo "setup ok"
