#!/usr/bin/env python3
import base64, json, os, struct, sys, time, urllib.error, urllib.request
try:
    from mutagen import File as MutagenFile
except ImportError:
    print("ERROR: mutagen not installed. Run: pip install mutagen")
    sys.exit(1)

REPO_ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIBRARY_PATH = os.path.join(REPO_ROOT, 'data', 'library.json')
AUDIO_DIR    = os.path.join(REPO_ROOT, 'media', 'audio')
GEMINI_URL   = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent"
VOICE_NAME   = "Charon"
SAMPLE_RATE  = 24000
CHANNELS    = 1
BIT_DEPTH   = 16

def pcm_to_wav(pcm):
    byte_rate   = SAMPLE_RATE * 2
    data_size   = len(pcm)
    header = struct.pack('<4sI4s4sIHHIIHH4sI',
        b'RIFF', 36+data_size, b'WAVE',
        b'fmt ', 16, 1, 1,
        SAMPLE_RATE, byte_rate, 2, 16,
        b'data', data_size)
    return header + pcm

def get_duration(path):
    if path.endswith('.wav'):
        pcm_bytes = os.path.getsize(path) - 44
        return round(pcm_bytes / (SAMPLE_RATE * CHANNELS * (BIT_DEPTH // 8)), 3)
    a = MutagenFile(path)
    return round(a.info.length, 3) if a else 0.0

def call_tts(api_key, text):
    payload = json.dumps({
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOICE_NAME}}}
        }
    }).encode()
    req = urllib.request.Request(
        f"{GEMINI_URL}?key={api_key}", data=payload,
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read())
    part = result["candidates"][0]["content"]["parts"][0]["inlineData"]
    mime = part.get("mimeType", "audio/pcm")
    raw  = base64.b64decode(part["data"])
    if "wav" in mime.lower():
        return raw, "audio/wav", ".wav"
    return pcm_to_wav(raw), "audio/wav", ".wav"

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tools/generate_narrations.py <API_KEY> [module_id]")
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
        print(f"\n{'='*60}\nModule: {mod['title']} ({len(mod['slides'])} slides)\n{'='*60}")
        for slide in mod["slides"]:
            sid   = slide["id"]
            title = slide.get("title", sid)
            script = (slide.get("narration") or {}).get("script", "").strip()
            if not script:
                print(f"  SKIP  {title[:55]}  (no script)"); skipped += 1; continue
            existing = (slide.get("narration") or {}).get("audio")
            if existing and os.path.exists(os.path.join(REPO_ROOT, existing)):
                print(f"  SKIP  {title[:55]}  (audio exists)"); skipped += 1; continue
            print(f"  GEN   {title[:55]} ...", end=" ", flush=True)
            try:
                audio, mime, ext = call_tts(api_key, script)
                out = os.path.join(AUDIO_DIR, sid + ext)
                with open(out, "wb") as f: f.write(audio)
                dur = get_duration(out)
                slide["narration"]["audio"]    = f"media/audio/{sid}{ext}"
                slide["narration"]["mime"]     = mime
                slide["narration"]["duration"] = dur
                print(f"done ({dur:.1f}s)")
                generated += 1
                with open(LIBRARY_PATH, "w") as f:
                    json.dump(lib, f, indent=2, ensure_ascii=False); f.write("\n")
                time.sleep(6)
            except urllib.error.HTTPError as e:
                print(f"ERROR HTTP {e.code}: {e.read().decode(errors='replace')[:120]}")
                errors += 1
            except Exception as e:
                print(f"ERROR {e}"); errors += 1
    print(f"\n{'='*60}\nDone. Generated: {generated}  Skipped: {skipped}  Errors: {errors}")

if __name__ == "__main__":
    main()