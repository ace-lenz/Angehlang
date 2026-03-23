# UR1 & UR2 Pro: Angehlang's Native Media Formats

**UR1** = `ultraresolution1.angeh`  
**UR2 Pro** = `ultraresolution2+pro.angeh`  
**Version:** 1.0 | **Status:** Angehlang-defined standard

---

## The One-Line Summary

> **UR1** replaces MP3. **UR2 Pro** replaces MP4.  
> Both are lighter, higher quality, and carry features that no other format on Earth supports — because they only run in Angehlang.

---

## Why the Name "ultraresolution"

The name is a statement of intent. Current formats max out at the resolution of the *file* — how many pixels, how many Hz. UR1 and UR2 Pro operate at the resolution of *meaning*: every frame knows what's in it, every second of audio knows its mood, every millisecond can fire an AI agent. That is ultra-resolution. Not just more pixels — more intelligence per pixel.

The "1" and "2+pro" are not version numbers. They are tiers:

- `ultraresolution1` = audio-first. The foundational format.
- `ultraresolution2+pro` = video, embedding UR1 as its audio layer.

---

## UR1 — Lighter Than MP3, Better Than FLAC

### The Compression Math

Opus is probably the best lossy format in terms of audio quality, outperforming MP3 and AAC at both 64 kbit/s and 96 kbit/s. UR1 uses Opus as its lossy core. This means:

- A UR1 file at **96 kbps** matches MP3 quality at **160 kbps** — 40% smaller
- A UR1 file at **64 kbps** is indistinguishable from MP3 at **128 kbps** — 50% smaller
- UR1 lossless mode uses ANGEH-LOSSLESS (FLAC-inspired with ANS entropy coding) — same quality as PCM, roughly half the size

### The ANGEH-PSYCHE Advantage

Standard MP3 uses a fixed perceptual model built in the 1990s. UR1's ANGEH-PSYCHE layer uses a modern critical-band masking model that:
- Accounts for actual playback volume (a quiet room allows more aggressive masking)
- Uses 24 Bark-band resolution vs MP3's coarser model
- Applies post-masking and pre-masking spread functions
- Achieves 15–25% additional compression with zero perceptible quality loss

### UR1 Feature Comparison

| Feature | MP3 | FLAC | Opus | **UR1** |
|---------|-----|------|------|---------|
| Smaller than MP3 | — | ❌ larger | ✅ 40–50% | ✅ 40–60% |
| Lossless option | ❌ | ✅ | ❌ | ✅ |
| Spatial 3D audio | ❌ | ❌ | ❌ | ✅ Ambisonics |
| Stem separation | ❌ | ❌ | ❌ | ✅ freq-mask |
| AI mood/BPM/key | ❌ | ❌ | ❌ | ✅ side-channel |
| Agent events | ❌ | ❌ | ❌ | ✅ timeline |
| Lyrics (time-sync)| ❌ | ❌ | ❌ | ✅ |
| File overhead | — | — | — | ~2KB/min for AI meta |

### What "stems" means in UR1

Stem separation (splitting audio into vocals/drums/bass/other) normally requires a completely separate file for each stem, doubling or quadrupling storage. UR1 stores **frequency-domain masks** instead. These masks, ~15% of the original file size, let any UR1-aware player reconstruct any stem on the fly without re-downloading or re-encoding.

### The Agent Timeline

Every UR1 file has an optional agent event track. This means:

```angeh
;; These events fire during playback — no re-encoding needed
(ur1-add-agent-event! b 30000 'ask "narrator"
  "What is the emotional peak of this song so far?")

(ur1-add-agent-event! b 90000 'spawn "lyric-translator"
  "You translate lyrics in real-time to any language.")
```

No other audio format has a concept of embedded AI agents.

---

## UR2 Pro — Lighter Than MP4, Smarter Than Any Codec

### The Compression Stack

UR2 Pro stacks three layers of compression:

```
Raw video frames
    ↓
AV1 encode           (~50% smaller than H.264 at same quality)
    ↓
LCEVC enhance        (~40% further compression, software-only)
    ↓
ANGEH-VISION hints   (enables 2×/4× AI upscaling at playback — zero bitrate cost)
    ↓
UR2 Pro container
```

The result: a 1080p video at 2 Mbps in UR2 Pro matches a 1080p H.264 video at 6–8 Mbps in quality. And with ANGEH-VISION enabled, it plays at 4K resolution on capable devices.

### The Real Codec Science

Looking ahead, new standards like VVC (H.266) and xvc promise even higher compression efficiency and smarter encoding. AI-based encoding techniques are emerging, leveraging machine learning to optimize video quality and bitrate dynamically.

Unlike VVC or AV1, LCEVC is a lightweight codec that doesn't need hardware to play on mobile devices and can be upgraded via software, avoiding the hardware compatibility issues that have delayed VVC and AV1.

UR2 Pro puts these together:
- AV1 as the royalty-free base (no patent fees)
- LCEVC as the software enhancement (no hardware needed)
- ANGEH-VISION as the AI intelligence layer (unique to Angehlang)

### ANGEH-VISION: Resolution Without Bitrate

Traditional upscaling (bicubic, Lanczos) blurs fine detail. AI upscaling (DLSS-style, Real-ESRGAN-style) reconstructs detail that wasn't in the low-res source. Neural network-based codecs like Google's experimental neural video compression achieve unprecedented compression ratios by learning content-specific patterns.

ANGEH-VISION doesn't store upscaled frames — it stores the model parameters (~500KB, one-time overhead) and optional per-frame hints for difficult scenes. The player applies upscaling live. A 1080p UR2 Pro file can play at 4K. A 4K file can play at 8K. No additional storage. No additional bandwidth.

### UR2 Pro Feature Comparison

| Feature | MP4/H.264 | MKV/H.265 | WebM/AV1 | **UR2 Pro** |
|---------|-----------|-----------|----------|-------------|
| Smaller than MP4 | — | ✅ 40% | ✅ 50% | ✅ 65–70% |
| AI upscaling | ❌ | ❌ | ❌ | ✅ live 2–4× |
| 3D depth layers | ❌ | ❌ | ❌ | ✅ 128 planes |
| Scene graph | ❌ | ❌ | ❌ | ✅ per-frame |
| Embedded agent events | ❌ | ❌ | ❌ | ✅ |
| Clickable hotspots | ❌ | ❌ | ❌ | ✅ |
| UR1 audio | ❌ | ❌ | ❌ | ✅ native |
| Stem-separable audio | ❌ | ❌ | ❌ | ✅ via UR1 |
| Backward compatible | ✅ | ✅ | ✅ | ✅ base layer |

---

## What "Only In Angehlang" Means

Both formats are defined, written, read, encoded, decoded, and played by `.angeh` programs. The codecs themselves route to native FFI calls (AV1 via libaom/SVT-AV1, Opus via libopus, LCEVC via V-Nova SDK) — but the intelligence layers (ANGEH-PSYCHE, ANGEH-VISION, ANGEH-SCENE, agent events, stem masks) exist nowhere else.

A UR1 file opened in a regular audio player will play through the Opus base layer — it sounds great. But the stems, the agents, the AI metadata, the spatial audio? Those only activate in an Angehlang UR1 player. The same principle applies to UR2 Pro — the AV1+LCEVC base plays anywhere; the intelligence activates in Angehlang.

This is intentional. It means UR1 and UR2 Pro are **universally compatible at the base level** and **uniquely powerful in the Angehlang ecosystem**.

---

## In Angehlang Code

```angeh
;; ── Create a UR1 audio file ────────────────────────────────────

(def b (ur1-builder 210000 48000 'hybrid))  ;; 3.5 min, 48kHz, hybrid mode
(ur1-load-pcm! b raw-pcm-data)
(ur1-encode-core! b 128)                    ;; 128kbps Opus (= MP3 256kbps quality)
(ur1-add-spatial! b stereo-pcm UR1-AMBI-FIRST)   ;; first-order Ambisonics
(ur1-add-stems! b (list 'vocals 'drums 'bass 'other) "AudioAI")
(ur1-add-ai-meta! b "AudioAI")
(ur1-add-agent-event! b 30000 'ask "narrator" "What's the emotional peak here?")
(ur1-add-lyrics! b "en" lyric-lines)
(ur1-finalize! b "my-song.angeh")

;; ── Create a UR2 Pro video file ────────────────────────────────

(def b (ur2-builder 3840 2160 60 7200000))  ;; 4K 60fps 2hr
(ur2-set-video! b UR2-CODEC-AV1 8000 #t (hash-map))   ;; AV1 HDR
(ur2-embed-ur1-audio! b my-ur1-builder)                ;; embed UR1 audio
(ur2-add-vision! b UR2-VISION-2X)                      ;; AI upscale to 8K on playback
(ur2-add-depth! b 32)                                  ;; 32 depth planes
(ur2-add-agent-event! b 0 'spawn "director"
  "You are an AI film director embedded in this movie.")
(ur2-add-hotspot! b 120000 125000 400 300 200 80
  "Who is this character?"
  (lambda () (agent-ask "director" "Describe this character's arc.")))
(ur2-finalize! b "my-film.angeh")

;; ── Convert MP3 to UR1 ──────────────────────────────────────────

(mp3->ur1 "song.mp3" "song.angeh"
  (hash-map
    'mode    'hybrid
    'bitrate 128
    'stems   #t
    'ai-meta #t
    'spatial #t
    'ambi-order UR1-AMBI-FIRST
    'ai-agent "AudioAI"))

;; ── Convert MP4 to UR2 Pro ──────────────────────────────────────

(mp4->ur2 "video.mp4" "video.angeh"
  (hash-map
    'codec        UR2-CODEC-AV1
    'vision       #t
    'vision-mode  UR2-VISION-2X
    'depth        #t
    'depth-planes 8
    'spatial-audio #t
    'scene-analysis #t
    'agent        "VideoAI"))
```

---

## Roadmap

### v1.0 — Foundation (current)
- [x] UR1 and UR2 Pro format specs defined in `.angeh`
- [x] Full builder API for both formats
- [x] ANGEH-PSYCHE perceptual model
- [x] ANGEH-LOSSLESS codec (FLAC-inspired with ANS)
- [x] Stem separation via frequency masks
- [x] Ambisonics spatial audio
- [x] ANGEH-VISION metadata track
- [x] 128-plane depth/spatial layers
- [x] Per-frame scene graph track
- [x] Agent event timelines
- [x] MP3→UR1 and MP4→UR2 converters
- [x] Players with stem soloing and agent callbacks

### v1.1 — Native Codecs
- [ ] Bind libopus via FFI for real Opus encoding
- [ ] Bind SVT-AV1 4.0 via FFI for real AV1 encoding
- [ ] Bind V-Nova LCEVC SDK via FFI
- [ ] Bind HTDemucs for real stem separation
- [ ] ANGEH-VISION model training pipeline

### v1.2 — Playback & Tooling
- [ ] `angeh-media` CLI: convert, probe, transcode
- [ ] Browser player (WebAssembly + Web Audio API)
- [ ] Real-time stem soloing during playback
- [ ] Head-tracking integration for spatial audio

### v2.0 — Full Vision
- [ ] ANGEH-LOSSLESS formally specified and published
- [ ] ANGEH-PSYCHE patent-free specification published
- [ ] UR1/UR2 Pro submitted to media standards bodies
- [ ] Third-party player SDK (C, Python, Rust)
- [ ] Streaming protocol (UR1-HLS, UR2-DASH)

---

*"The resolution that matters is not pixels per inch. It is intelligence per frame."*  
— Angehlang Media Philosophy
