# DavCut — Shotcut Fork Evaluation (30 May 2026)

## Discovery

DavCut was found at `D:\Battle\ProductivityApps\DavCut\` — it was downloaded by the user and extracted from an installer. It is a **rebranded Shotcut** (open-source video editor, GPL-3.0) with the following additions:

## Architecture

**Location:** `D:\Battle\ProductivityApps\DavCut\` (not in Program Files or AppData)
**Executable:** `davcut.exe` (7.3 MB)
**Engine:** MLT Multimedia Framework v7 (via `libmlt-7.dll`)
**GUI:** Qt6 (via `Qt6Core.dll`, `Qt6Gui.dll`, `Qt6Widgets.dll`, `Qt6Quick*.dll`, `Qt6Qml*.dll`)
**Video codecs:** FFmpeg stack (`avcodec-62.dll`, `avformat-62.dll`, `avfilter-11.dll`, `avutil-60.dll`, `swresample-6.dll`, `swscale-9.dll`)
**Standalone tools included:** `ffmpeg.exe`, `ffplay.exe`, `ffprobe.exe`, `melt.exe`, `whisper-cli.exe`, `gopro2gpx.exe`

### AI/ML Components (NOT in standard Shotcut)

| File | What | Why notable |
|------|------|-------------|
| `libwhisper.dll` | Whisper speech-to-text | Can transcribe audio → auto-captions |
| `ggml.dll` | GGML inference core | Local LLM inference (CPU) |
| `ggml-base.dll` | GGML base utilities | |
| `ggml-blas.dll` | GGML BLAS acceleration | |
| `ggml-cpu.dll` | GGML CPU optimizations | |
| `ggml-vulkan.dll` (57 MB) | GGML Vulkan GPU acceleration | Local AI on GPU |
| `libopencv_core4140.dll` | OpenCV core (v4.14) | Image/video analysis |
| `libopencv_imgproc4140.dll` | OpenCV image processing | Filter detection, scene analysis |
| `libopencv_plot4140.dll` | OpenCV plotting | |
| `libopencv_tracking4140.dll` | OpenCV object tracking | |
| `libopencv_video4140.dll` | OpenCV video analysis | |

### MLT Plugins (lib/mlt/)

Key MLT modules that give DavCut its power:

- `libmltopencv.dll` — OpenCV-based video filters
- `libmltqt6.dll` — Qt6 rendering
- `libmltavformat.dll` — FFmpeg format support
- `libmltrtaudio.dll` — Real-time audio
- `libmltrubberband.dll` — Audio pitch/time stretching
- `libmltvidstab.dll` — Video stabilization
- `libmltplus.dll` / `libmltplusgpl.dll` — Shotcut's own MLT+ framework
- `libmltmovit.dll` — GPU-accelerated OpenGL effects
- `libmltfrei0r.dll` — Frei0r video effect plugin support
- `libmltsox.dll` — SoX audio effects

## Licensing

DavCut binary is derived from Shotcut (GPL-3.0). The same license applies. The `COPYING.txt` file at `D:\Battle\ProductivityApps\DavCut\COPYING.txt` and `LICENSE` at `D:\Battle\ProductivityApps\DavCut\LICENSE` should be checked, but this is a fork of GPL-3.0 code.

## Integration Strategy

### Method 1: MLT Project File (RECOMMENDED)
TCHUEKAM writes an `.mlt` XML file describing the timeline, clips, transitions, and filters. This is the native Shotcut project format.

**Workflow:**
1. TCHUEKAM writes `project.mlt` to the footage directory
2. User opens `project.mlt` in DavCut GUI → previews → exports
3. OR TCHUEKAM runs `melt.exe project.mlt -consumer avformat:output.mp4` for headless export

**The MLT XML format structure:**
```xml
<?xml version="1.0" encoding="utf-8"?>
<mlt>
  <profile description="HD 1080p 30fps" width="1920" height="1080" frame_rate_num="30" frame_rate_den="1" display_aspect_num="16" display_aspect_den="9"/>
  <producer id="producer0" in="0" out="149">
    <property name="resource">clip01.mp4</property>
    <property name="mlt_service">avformat</property>
  </producer>
  <playlist id="playlist0">
    <entry producer="producer0" in="0" out="149"/>
  </playlist>
  <tractor id="tractor0" out="149">
    <track producer="playlist0"/>
  </tractor>
</mlt>
```

### Method 2: melt.exe CLI (Headless Render)
The `melt.exe` binary bundled with DavCut can render MLT projects without opening the GUI:
```bash
cd /d/Battle/ProductivityApps/DavCut
./melt.exe /d/footage/project.mlt -consumer avformat:/d/output.mp4
```

### Method 3: FFmpeg Direct (Simple operations)
For simple cuts/trims/concat, use the bundled `ffmpeg.exe` directly.

### Method 4: Whisper CLI (Transcription)
The bundled `whisper-cli.exe` can transcribe audio to text for auto-captions:
```bash
./whisper-cli.exe -m base /d/audio.mp3 -f srt > captions.srt
```

## Dual-Agent Pipeline Design

When integrating both TCHUEKAM CLI (Gemini) and TCHUEKAM (Hermes) into DavCut:

```
[User Prompt]
      │
      ▼
[TCHUEKAM CLI (Gemini)] ── Vision + Creativity
      │  - scans footage via ffprobe + Gemini Vision
      │  - scores clips 0-100
      │  - detects mood tag
      │  - writes voiceover script (Whisper or Gemini)
      │  - post-draft: reviews and suggests improvements
      │
      │  JSON edit plan
      ▼
[TCHUEKAM (Hermes/DeepSeek)] ── MLT Project Builder
      │  - writes MLT XML with clips, transitions, filters
      │  - runs melt.exe for headless render
      │  - or writes MLT for user to open in DavCut GUI
      ▼
[User opens project.mlt in DavCut]
      │
      ▼
[User Review] ←→ [Gemini suggests improvements via JSON]
      │
      ▼
[TCHUEKAM updates MLT XML with accepted changes]
```

## Comparison: DavCut vs Alternatives for This User

| Aspect | DavCut (Shotcut fork) | Standard Shotcut | Standard Kdenlive |
|--------|----------------------|------------------|-------------------|
| Install location | D:\Battle\ProductivityApps\ (portable) | AppData or Program Files | Program Files |
| AI components | ✅ Whisper + OpenCV + GGML | ❌ None | ❌ None |
| Headless render | ✅ melt.exe bundled | ✅ melt.exe (separate) | ❌ MLT not bundled |
| Integration potential | ✅ High (MLT XML + melt) | ✅ High (same) | ⚠️ Medium (Kdenlive project format) |
| Mobile | ❌ | ❌ | ❌ |

**Verdict:** DavCut is already the best option because (a) it's portable on D:\, (b) it has Whisper/OpenCV/GGML baked in, (c) the MLT XML format is straightforward to generate programmatically.
