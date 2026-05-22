#!/usr/bin/env python3
"""
generate_narrations_gcloud.py - Generate voice narrations using Google Cloud Text-to-Speech API.

Usage:
    python3 tools/generate_narrations_gcloud.py <API_KEY> [module_id]

    module_id options: planning, m_iqodh, m_g0bg0, m_j7ovf, m_b68tp, m_qk8f3, m_8e8ua, m_r6pef
    Leave module_id blank to process all modules in one shot.

Examples:
    python3 tools/generate_narrations_gcloud.py AIzaSy...              # all modules
    python3 tools/generate_narrations_gcloud.py AIzaSy... planning     # just Planning
"""

import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request

try:
    from mutagen.mp3 import MP3
except ImportError:
    print("ERROR: mutagen not installed. Run: pip install mutagen")
    sys.exit(1)

REPO_ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIBRARY_PATH = os.path.join(REPO_ROOT, 'data', 'library.json')
AUDIO_DIR    = os.path.join(REPO_ROOT, 'media', 'audio')

GCLOUD_URL   = "https://texttospeech.googleapis.com/v1/text:synthesize"
VOICE_NAME   = "en-US-Neural2-D"
LANGUAGE     = "en-US"


def get_duration(path):
    audio = MP3(path)
    return round(audio.info.length, 3)


def call_tts(api_key, text):
    payload = json.dumps({
        "input":       {"text": text},
        "voice":       {"languageCode": LANGUAGE, "name": VOICE_NAME},
        "audioConfig": {"audioEncoding": "MP3"},
    }).encode()

    req = urllib.request.Request(
        f"{GCLOUD_URL}?key={api_key}",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read())

    return base64.b64decode(result["audioContent"])


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tools/generate_narrations_gcloud.py <API_KEY> [module_id]")
        sys.exit(1)

    api_key    = sys.argv[1]
    filter_mod = sys.argv[2] if len(sys.argv) > 2 else None

    os.makedirs(AUDIO_DIR, exist_ok=True)

    with open(LIBRARY_PATH) as f:
        lib = json.load(f)

    generated = skipped = errors = 0

    for mod in lib["modules"]:
        if filter_mod and mod["id"] != filter_mod:
            continue

        print(f"\n{'='*60}")
        print(f"Module: {mod['title']}  ({len(mod['slides'])} slides)")
        print(f"{'='*60}")

        for slide in mod["slides"]:
            slide_id = slide["id"]
            title    = slide.get("title", slide_id)
            script   = (slide.get("narration") or {}).get("script", "").strip()

            if not script:
                print(f"  SKIP  {title[:55]}  (no script)")
                skipped += 1
                continue

            existing = (slide.get("narration") or {}).get("audio")
            if existing and os.path.exists(os.path.join(REPO_ROOT, existing)):
                print(f"  SKIP  {title[:55]}  (audio exists)")
                skipped += 1
                continue

            print(f"  GEN   {title[:55]} ...", end=" ", flush=True)

            try:
                mp3_bytes = call_tts(api_key, script)
                out_path  = os.path.join(AUDIO_DIR, slide_id + ".mp3")

                with open(out_path, "wb") as f:
                    f.write(mp3_bytes)

                duration = get_duration(out_path)
                rel_path = f"media/audio/{slide_id}.mp3"

                if slide.get("narration") is None:
                    slide["narration"] = {}
                slide["narration"]["audio"]    = rel_path
                slide["narration"]["mime"]     = "audio/mpeg"
                slide["narration"]["duration"] = duration

                print(f"done  ({duration:.1f}s)")
                generated += 1

                with open(LIBRARY_PATH, "w") as f:
                    json.dump(lib, f, indent=2, ensure_ascii=False)
                    f.write("\n")

                time.sleep(0.25)

            except urllib.error.HTTPError as e:
                body = e.read().decode(errors="replace")
                print(f"ERROR  HTTP {e.code}: {body[:120]}")
                errors += 1
            except Exception as e:
                print(f"ERROR  {e}")
                errors += 1

    print(f"\n{'='*60}")
    print(f"Done.  Generated: {generated}  Skipped: {skipped}  Errors: {errors}")
    print(f"library.json updated.")


if __name__ == "__main__":
    main()