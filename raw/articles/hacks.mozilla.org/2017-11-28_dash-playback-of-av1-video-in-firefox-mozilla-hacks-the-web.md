---
title: DASH playback of AV1 video in Firefox – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2017/11/dash-playback-of-av1-video/
author: Ralph Giles
published: '2017-11-28'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**Editor’s update:** *At this time, we’ve had to put the AV1 implementation in Firefox behind a Mozilla preference (pref). We are currently working to address an issue that will allow us to turn AV1 back on by default for everyone. In the meantime, you can still try the demo linked in this blog post. You’ll need to open *

`about:config`

in Firefox Nightly and manually switch the setting `media.av1.enabled`

to true.## Bitmovin and Mozilla partner to enable HTML5 AV1 Playback

Bitmovin and Mozilla, both members of the [Alliance for Open Media](http://aomedia.org/license) (AOM), are partnering to bring AV1 playback with HTML5 to Firefox as the first browser to play AV1 MPEG-DASH/HLS streams. While the AV1 bitstream is still being finalized, the industry is gearing for fast adoption of the new codec, which promises to be 25-35% more efficient than VP9 and H.265/HEVC.

The AV1 bitstream is set to be finalized in early 2018. You may ask – “How does playback work on the bitstream that is not yet finalized?”. Indeed, this is a good question as there are still many things in the bitstream that may change during the current state of the development. However, to make playback possible, we just need to ensure that the encoder and decoder use the same version of the bitstream. Bitmovin and Mozilla agreed on a simple, but for the time being useful, codec string, to ensure compatibility between the version of the bitstream in the Bitmovin AV1 encoder and the AV1 decoder in Mozilla Firefox:

"av1.experimental.<git hash>"

A test page has been prepared to demonstrate playback of MPEG-DASH test assets encoded in AV1 by the Bitmovin Encoder and played with the Bitmovin HTML5 Player (7.3.0-b7) in the Firefox Nightly browser.

![playback demo screenshot](../../assets/4d49c24eb1f7a0d6.jpeg)


![playback demo screenshot](../../assets/4d49c24eb1f7a0d6.jpeg)

Visit the demo page at [https://demo.bitmovin.com/public/firefox/av1/](https://demo.bitmovin.com/public/firefox/av1/). You can download [Firefox Nightly here](https://www.mozilla.org/en-US/firefox/channel/desktop/#nightly) to view it.

## Bitmovin AV1 End-to-End

The Bitmovin AV1 encoder is based on the AOM specification and scaled on Bitmovin’s cloud native architecture for faster throughput. Earlier this year, the team wrote about [the world’s first AV1 livestream at broadcast quality](https://bitmovin.com/bitmovin-supports-av1-encoding-vod-live-joins-alliance-open-media/), which was demoed during NAB 2017 and brought the company the [Best of NAB 2017 Award from Streaming Media](https://bitmovin.com/bitmovin-rocks-show-takes-home-best-nab-award/).

The current state of the AV1 encoder is still far away from delivering reasonable encoding times without extensive tuning to the code base: e.g. it takes about 150 seconds on an off-the-shelf desktop computer to encode one second of video. For this reason, Bitmovin’s ability to provide complete ABR test assets (multiple qualities and resolutions) of high quality in reasonable times was extremely useful for testing of the MPEG-DASH/HLS playback of AV1 in Firefox. (HLS playback of AV1 is not officially supported by Apple, but technically possible of course.) The fast encoding throughput can be achieved thanks to Bitmovin’s flexible cloud native architecture, which allows massive horizontal scaling of a single VoD asset to multiple nodes, as depicted in the following figure. An additional benefit of the scalable architecture is that quality doesn’t need to be compromised for speed, as is often the case with a typical encoding setup.

![block diagram of the encoder](../../assets/234aa78d20c746f9.png)


![block diagram of the encoder](../../assets/234aa78d20c746f9.png)

The test assets provided by Bitmovin are segmented WebM outputs that can be used with HLS and MPEG-DASH. For the demo page, we decided to go with MPEG-DASH and encode the assets to the following quality levels:

- 100 kbps, 480×200
- 200 kbps, 640×266
- 500 kbps, 1280×532
- 800 kbps, 1280×532
- 1 Mbps, 1920×800
- 2 Mbps, 1920×800
- 3 Mbps, 1920×800

We used [the royalty-free Opus audio codec](https://hacks.mozilla.org/2017/06/opus-audio-codec-version-1-2-released/) and encoded with 32 kbps, which provides for a reasonable quality audio stream.

## Mozilla Firefox

Firefox has a long history of pioneering open compression technology for audio and video. We added support for the royalty-free [Theora](https://www.theora.org/) video codec [a decade ago](https://bugzilla.mozilla.org/show_bug.cgi?id=422538) in our initial implementation of HTML5 video. [WebM](https://webmproject.org/) support followed [a few years later](https://bugzilla.mozilla.org/show_bug.cgi?id=566245). More recently, we were the first browser to support VP9, Opus, and FLAC in the popular MP4 container.

After the success of the Opus audio codec, our research arm has been investing heavily in a next-generation royalty-free video codec. Mozilla’s [Daala](https://xiph.org/daala/) project has been a test bed for new ideas, approaching video compression in a totally new way. And we’ve been contributing those ideas to the AV1 codec at the [IETF](https://tools.ietf.org/wg/netvc/) and the [Alliance for Open Media](http://aomedia.org/).

AV1 is a new video compression standard, developed by many contributors through the IETF standards process. This kind of collaboration was part of what made Opus so successful, with contributions from several organizations and open engineering discussions producing a design that was better than the sum of its parts.

While Opus was adopted as a mandatory format for the WebRTC wire protocol, we don’t have a similar mandate for a video codec. Both the royalty-free VP8 and the non-free H.264 codecs are considered part of the baseline. Consensus was blocked on the one side by the desire for a freely-implementable spec and on the other for hardware-supported video compression, which VP8 didn’t have at the time.

Major hardware vendors have been involved with AV1 from the start, which we expect will result in accelerated support being available much sooner.

In April, Bitmovin demonstrated the first live stream using the new AV1 compression technology.

In June, Bitmovin and Mozilla worked together to demonstrate the first playback of AV1 video in a web page, using Bitmovin’s adaptive bitrate video technology. The [demo is available](https://demo.bitmovin.com/public/firefox/av1/) now and works with [Firefox Nightly](https://www.mozilla.org/en-US/firefox/channel/desktop/#nightly).

The codec work is open source. If you’re interested in testing this, you can compile an encoder yourself. The format is still under development, so it’s important to match the version you’re testing with the decoder version in Firefox Nightly. We’ve extended the `MediaSource.isTypeSupported`

api to take a git commit as a qualifier. You can test for this, e.g.:

```
var container = 'video/webm';
var codec = 'av1.experimental.e87fb2378f01103d5d6e477a4ef6892dc714e614';
var mimeType = container + '; codecs="' + codec + '"';
var supported = MediaSource.isTypeSupported(mimeType);
```


Then select an alternate resource or display an error if your encoded resource isn’t supported in that particular browser.

Past commit ids we’ve supported are `aadbb0251996`

and `f5bdeac22930`

.The currently-supported commit id, built with default configure options, is available [here](https://github.com/mozilla/gecko-dev/blob/master/media/libaom/README_MOZILLA#L25). Once the bitstream is stable we will drop this convention and you can just test for `codecs=av1`

like any other format.

As an example, running this code inside the current page, we can report:

Since the initial demo, we’ve continued to develop AV1, providing feedback from real-world application testing and periodically updating the version we support to take advantage of ongoing improvements. The compression efficiency continues to improve. We hope to stabilize the new format next year and begin deployment across the internet of this exciting new format for video.

## About Ralph Giles

Ralph has contributed to media technology and royalty-free codecs for most of his career. Currently he helps maintain the video playback module in Firefox and supports new work in the Rust programming language. In his spare time he enjoys books and early music.

## About
[
Martin Smole ](https://www.bitmovin.com)

Martin is responsible for Bitmovin Encoding product strategy, roadmap and development. His team works to enable complex video encoding workflows for global premium media and technology companies like Red Bull Media House and the New York Times. As one of the first employees, Martin led the development of Bitmovin encoding infrastructure, building the world's first commercial massively scalable encoding service, capable of achieving 100x speeds over realtime. Currently, Martin oversees further development of the Bitmovin Encoding solution, including integration of new technologies, like AV1.

## 10 comments

DavidNovember 28th, 2017 at 20:53Ralph GilesNovember 30th, 2017 at 14:45MarcoNovember 29th, 2017 at 03:39Ralph GilesNovember 29th, 2017 at 08:53daveNovember 30th, 2017 at 08:12Ralph GilesNovember 30th, 2017 at 12:51Jim KirkDecember 2nd, 2017 at 16:44Anthony JonesDecember 4th, 2017 at 16:25DDDecember 9th, 2017 at 11:04DDDecember 10th, 2017 at 18:43