---
name: youtube-content
description: "YouTube transcripts to summaries, threads, blogs."
platforms: [linux, macos, windows]
---

# YouTube Content Tool

## When to use

Use when the user shares a YouTube URL or video link, asks to summarize a video, requests a transcript, or wants to extract and reformat content from any YouTube video. Transforms transcripts into structured content (chapters, summaries, threads, blog posts).

Extract transcripts from YouTube videos and convert them into useful formats.

## Setup

```bash
pip install youtube-transcript-api
```

On Windows, if `pip install` fails with `SRE module mismatch`, the Python environment is broken. Use Node.js as fallback:
```bash
npm install -g youtube-transcript  # or use npx
```

## Helper Script

`SKILL_DIR` is the directory containing this SKILL.md file. The script accepts any standard YouTube URL format, short links (youtu.be), shorts, embeds, live links, or a raw 11-character video ID.

```bash
# JSON output with metadata
python3 SKILL_DIR/scripts/fetch_transcript.py "https://youtube.com/watch?v=VIDEO_ID"

# Plain text (good for piping into further processing)
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only

# With timestamps
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --timestamps

# Specific language with fallback chain
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --language tr,en
```

### Fallback when Python script fails

If the python script errors out (broken Python, import errors):

1. **Try the Innertube API directly** (Node.js, no dependencies):
   Run `scripts/fetch_innertube.js <VIDEO_ID>` to call YouTube's official player API and check for caption tracks.

2. **Try yt-dlp** if installed:
   ```bash
   yt-dlp --write-auto-sub --sub-lang en --skip-download --convert-subs srt "https://youtube.com/watch?v=VIDEO_ID"
   ```

3. **Try the browser**: navigate to `https://youtubetranscript.com/?v=VIDEO_ID` and check if the page shows a transcript after entering the URL. If the page shows "YouTube is currently blocking us from fetching subtitles", the video has no captions or is protected.

## Output Formats

After fetching the transcript, format it based on what the user asks for:

- **Chapters**: Group by topic shifts, output timestamped chapter list
- **Summary**: Concise 5-10 sentence overview of the entire video
- **Chapter summaries**: Chapters with a short paragraph summary for each
- **Thread**: Twitter/X thread format — numbered posts, each under 280 chars
- **Blog post**: Full article with title, sections, and key takeaways
- **Quotes**: Notable quotes with timestamps

### Example — Chapters Output

```
00:00 Introduction — host opens with the problem statement
03:45 Background — prior work and why existing solutions fall short
12:20 Core method — walkthrough of the proposed approach
24:10 Results — benchmark comparisons and key takeaways
31:55 Q&A — audience questions on scalability and next steps
```

## Workflow

1. **Fetch** the transcript using the helper script with `--text-only --timestamps`.
2. **Validate**: confirm the output is non-empty and in the expected language. If empty, try alternative approaches (Innertube API, yt-dlp, browser). If ALL approaches return nothing, the video has no captions — tell the user and stop.
3. **Chunk if needed**: if the transcript exceeds ~50K characters, split into overlapping chunks (~40K with 2K overlap) and summarize each chunk before merging.
4. **Transform** into the requested output format. If the user did not specify a format, default to a summary.
5. **Verify**: re-read the transformed output to check for coherence, correct timestamps, and completeness before presenting.

## Error Handling

There are THREE distinct failure modes:

1. **No captions at all** — the video has NO subtitle tracks (neither manual nor auto-generated). Common for: code tutorial screencasts with voiceover but no CC, music videos, shorts without text overlays. The Innertube API returns `captions: null`. Transcript extraction is impossible — tell the user flatly and suggest manual transcription or describing what they see.

   Detection: call YouTube's Innertube API via Node.js (`scripts/fetch_innertube.js`). If the response has no `captions.playerCaptionsTracklistRenderer`, the video has no captions.

2. **Transcript disabled** — the video owner manually turned off captions. Tell the user and suggest they check captions availability on the video page.

3. **No matching language** — the video has captions but not in the requested language. Retry without `--language` to fetch any available transcript, then note the actual language to the user.

### Secondary checks

- **Private/unavailable video**: relay the error and ask the user to verify the URL.
- **Private video**: check via the oEmbed API (`https://www.youtube.com/oembed?url=...&format=json`) which returns video info without auth.

### Dependency failures

- **Dependency missing**: run `pip install youtube-transcript-api` and retry.
- **Python broken** (`SRE module mismatch`, `Python was not found`): the Windows Python environment is corrupted. Fall back to the Node.js Innertube script or yt-dlp.
- **youtube-transcript-api version mismatch**: on v1.x the API is `YouTubeTranscriptApi().fetch()`, on v0.x it's `YouTubeTranscriptApi.get_transcript()`. The helper script uses v1.x. If you get `AttributeError: 'YouTubeTranscriptApi' object has no attribute 'fetch'`, the installed version is v0.x — use `get_transcript(video_id)` instead.

## Innertube API Reference

YouTube's internal player API provides caption track data when available. POST to `https://www.youtube.com/youtubei/v1/player` with:

```json
{
  "context": {
    "client": {
      "clientName": "WEB",
      "clientVersion": "2.20250314.00.00",
      "hl": "en",
      "gl": "US"
    }
  },
  "videoId": "VIDEO_ID"
}
```

Response contains `captions.playerCaptionsTracklistRenderer.captionTracks[]` with `baseUrl`, `languageCode`, `kind` ("asr" for auto-generated), and `name.simpleText`.

If `captions` is absent or `null` from the response, the video has NO caption tracks — not even auto-generated.
