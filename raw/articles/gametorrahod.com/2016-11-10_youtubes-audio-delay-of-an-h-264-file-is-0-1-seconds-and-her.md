---
title: YouTube’s audio delay of an H.264 file is +0.1 seconds and here’s how to fix
  it
url: https://gametorrahod.com/youtube-s-audio-delay-of-an-h-264-file-is--0-1-seconds-and-here-s-how-to-fix-it/
author: Sirawat Pitaksarit
published: '2016-11-10'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

![](../../assets/58b126568776d9f5.png)

It probably will depends on codecs and other video’s structures, but from my trial-and-error experiment the delay is **+0.1 seconds** (you hear audio way after the picture) for H.264 .mp4 file. (Exported from Premiere Pro with H.264 preset, then run through Handbrake)

I occasionally uploads YouTube videos of [music games gameplay](https://www.youtube.com/user/5argon) as a tribute to songs I like. For most video the 0.1 seconds delay is not that noticeable, but in these kind of clips, it became really apparent that the audio is off sync. Before uploading, I have really made sure that it is dead exact.

You can use ffmpeg to fix it by make the audio come faster than the correct position with this command :

`ffmpeg -i input.mp4 -itsoffset -0.1 -i input.mp4 -map 0:v -map 1:a -vcodec copy -acodec copy delayed.mp4`


Basically this makes 2 streams, #0 is the original one and #1 is the modified one. We choose the modified one for audio. This operation completes as soon after you press enter, because it does not re-render anything.

YouTube will delay back 0.1 seconds, resulting in the correct audio position like what you hear on your computer on your original file.

Here is the metadata of that video, by the way. If yours match mine, probably the audio will be delayed by about 0.1 seconds in YouTube.

```
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from ‘input.mp4’:
Metadata:
major_brand : mp42
minor_version : 512
compatible_brands: isomiso2avc1mp41
encoder : HandBrake 0.10.1 2015030800
Duration: 00:03:05.39, start: 0.000000, bitrate: 7565 kb/s
Stream #0:0(und): Video: h264 (Main) (avc1 / 0x31637661), yuv420p(tv, bt709), 1920x1080 [SAR 1:1 DAR 16:9], 7397 kb/s, 29.97 fps, 29.97 tbr, 90k tbn, 180k tbc (default)
Metadata:
handler_name : VideoHandler
Stream #0:1(eng): Audio: aac (LC) (mp4a / 0x6134706D), 48000 Hz, stereo, fltp, 164 kb/s (default)
Metadata:
handler_name : Stereo
```


You can compare how this might matters in your video below.

Before compensation fix : [https://www.youtube.com/watch?v=SSZ7H1bUr18](https://www.youtube.com/watch?v=SSZ7H1bUr18) (That is, in your computer it sounds correct but became wrong after uploading)

After the fix : [https://youtu.be/buGYUO9CrhA](https://youtu.be/buGYUO9CrhA) (Now the clip in your computer have audio that is way too fast, but will be corrected in YouTube)

**EDIT**

Also, H.264 to Facebook seems to severely put the audio **faster** than expected. So to counter that, you need to **delay** the audio on your video file. From trial-and-error, I discovered that **0.18 seconds** is a good value. (use 0.18 instead of -0.1 above)

It seems to be **0.145 seconds** if the video came straight from Premiere Pro with H264 encoding.

Note that a video from Android (which has .mp4 extension) is fine with Facebook. The audio is a little bit faster than what I viewed on PC.

**EDIT**

It finally comes a time for me to produce a Twitter video, and it seems to **delay** an audio by 0.15 seconds. So use -0.15 to compensate for that!

**EDIT**

For NicoNico Douga, there’s no delay at all if you use the output from HandBrake. You don’t have to delay anything! Nice!