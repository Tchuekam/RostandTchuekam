#!/usr/bin/env node
/**
 * Fetch YouTube caption track info via the Innertube API.
 * No dependencies — uses Node.js built-in https module.
 *
 * Usage:
 *   node fetch_innertube.js <VIDEO_ID>
 *
 * Exit codes:
 *   0 — captions found, prints JSON with track info
 *   1 — no captions available
 *   2 — error (network, parse)
 */

const https = require('https');

const videoId = process.argv[2];
if (!videoId || videoId.length !== 11) {
  console.error('Usage: node fetch_innertube.js <11-char VIDEO_ID>');
  process.exit(2);
}

const postData = JSON.stringify({
  context: {
    client: {
      clientName: 'WEB',
      clientVersion: '2.20250314.00.00',
      hl: 'en',
      gl: 'US'
    }
  },
  videoId: videoId
});

const options = {
  hostname: 'www.youtube.com',
  path: '/youtubei/v1/player',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Origin': 'https://www.youtube.com',
    'X-YouTube-Client-Name': '1',
    'X-YouTube-Client-Version': '2.20250314.00.00'
  }
};

const req = https.request(options, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    try {
      const json = JSON.parse(data);
      const captions = json?.captions?.playerCaptionsTracklistRenderer?.captionTracks;
      const title = json?.videoDetails?.title || 'Unknown';
      const lengthSeconds = json?.videoDetails?.lengthSeconds || '0';

      if (!captions || captions.length === 0) {
        console.log(JSON.stringify({
          video_id: videoId,
          title: title,
          length_seconds: parseInt(lengthSeconds),
          has_captions: false,
          tracks: [],
          message: 'No captions available for this video.'
        }));
        process.exit(1);
      }

      const tracks = captions.map(t => ({
        languageCode: t.languageCode,
        kind: t.kind || 'manual',
        name: t.name?.simpleText || t.languageCode,
        baseUrl: t.baseUrl
      }));

      console.log(JSON.stringify({
        video_id: videoId,
        title: title,
        length_seconds: parseInt(lengthSeconds),
        has_captions: true,
        track_count: tracks.length,
        tracks: tracks
      }, null, 2));
    } catch (e) {
      console.error('Parse error:', e.message);
      process.exit(2);
    }
  });
});

req.on('error', (err) => {
  console.error('Network error:', err.message);
  process.exit(2);
});

req.write(postData);
req.end();
