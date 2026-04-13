---
title: Firefox Beta 15 supports the new Opus audio format – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2012/07/firefox-beta-15-supports-the-new-opus-audio-format/
author: Timothy B Terriberry
published: '2012-07-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox 15 (now in the Beta channel) supports the [Opus audio format](http://en.wikipedia.org/wiki/Opus_%28codec%29), via the [Opus reference implementation](http://www.opus-codec.org/).

## What is it?

Opus is a completely free audio format that was recently approved for publication as a standards-track RFC by the [IETF](http://www.ietf.org/). Opus files can play in Firefox Beta today.

Opus offers these benefits:

**Better compression**than MP3, Ogg, or AAC formats- Good for
**both music and speech** **Dynamically adjustable**bitrate, audio bandwidth, and coding delay- Support for
**both interactive and pre-recorded applications**

## Why Should I care?

First, *Opus is free software*, free for everyone, for any purpose. It’s also an IETF standard. Both the encoder and decoder are free, including the fixed-point implementation (for mobile devices). These aren’t toy demos. They’re the best we could make, *ready for serious use*.

We think Opus is an incredible new format for web audio. We’re working hard to convince other browsers to adopt it, to [break the logjam](http://xkcd.com/927/) over a common <audio> format.

The codec is a collaboration between members of the [IETF Internet Wideband Audio Codec working group](http://tools.ietf.org/wg/codec/), including Mozilla, Microsoft, Xiph.Org, Broadcom, Octasic, and others.

We [designed it](http://opus-codec.org/presentations/) for high-quality, interactive audio (VoIP, teleconference) and will use it in the upcoming [WebRTC standard](http://dev.w3.org/2011/webrtc/editor/webrtc.html). Opus is also *best-in-class* for live streaming and static file playback. In fact, it is the first audio codec to be well-suited for both interactive and non-interactive applications.

Opus is *as good or better* than basically all existing lossy audio codecs, when competing against them in their sweet spots, including:

- General audio codecs (high latency, high quality)
-
- MP3
- AAC (all flavors)
- Vorbis

- Speech codecs (low latency, low quality)
-
- G.729
- AMR-NB
- AMR-WB (G.722.2)
- Speex
- iSAC
- iLBC
- G.722.1 (all variants)
- G.719


And *none* of those codecs have the versatility to support all the use cases that Opus does.

Listening tests show that:

- At 64 kbps,
[Opus](https://people.xiph.org/~greg/opus/ha2011/).*sounds better*than both HE-AAC and Vorbis - A 64 kbps Opus file
.*sounds as good as*a 96 kbps MP3 file

That’s a lot of bandwidth saved. It’s also much more flexible.

Opus can stream:

**narrowband speech**at bitrates as low as 6 kbps**fullband music**at rates of 256 kbps per channel

At the higher of those rates, it is **perceptually lossless**. It also *scales between these two extremes dynamically*, depending on the network bandwidth available.

Opus compresses speech especially well. Those [same test results](https://www.ietf.org/proceedings/80/slides/codec-4.pdf) (slide 19) show that for fullband mono speech, Opus is *almost transparent* at 32 kbps. For *audio books and podcasts*, it’s a real win.

Opus is also great for *short files* (like game sound effects) and *startup latency*, because unlike Vorbis, it doesn’t require several kilobytes of codebooks at the start of each file. This makes *streaming easier*, too, since the server doesn’t have to keep extra data around to send to clients who join mid-stream. Instead, it can send them a tiny, generic header constructed on the fly.

## How do I use it in a web page?

Opus works with the <audio> element just like any other audio format.

For example:

<audio src="ehren-paper_lights-64.opus" controls>

This code in a web page displays an embedded player like this:


(Requires Firefox 15 or later)

## Encoding files

For now, the best way to create Opus files is to use the `opusenc`

tool. You can get source code, along with Mac and Windows binaries, from:

While Firefox 15 is the first browser with native Opus support, playback is coming to **gstreamer**, **libavcodec**, **foobar2000**, and other media players.

## Streaming

Live streaming applications benefit greatly from Opus’s flexibility. You don’t have to decide up front whether you want low bandwidth or high quality, to optimize for voice or music, etc. Streaming servers can *adapt the encoding* as conditions change—*without* breaking the stream to the player.

Pre-encoded files can *stream from a normal web server*. The popular [Icecast streaming media server](http://icecast.org/) can relay a single, live Opus stream, generated on the fly, to thousands of connected listeners. Opus is supported by [the current development version of Icecast](http://www.icecast.org/#release_2.4-beta).

## More Information

To learn more visit [opus-codec.org](http://opus-codec.org/), or join us in #opus on irc.[freenode.net](http://freenode.net).

## About
[
Timothy B. Terriberry ](http://people.xiph.org/~tterribe/)

Timothy B. Terriberry is a long-time volunteer for the Xiph.Org foundation, working on codecs such as Theora, Vorbis, CELT, and Opus. He has been contributing to Mozilla's media support since 2008 and hacking on WebRTC since 2010.

## 35 comments

Henri SivonenJuly 19th, 2012 at 22:33BerndJuly 20th, 2012 at 20:48Giuseppe BilottaJuly 20th, 2012 at 00:05Style ThingJuly 20th, 2012 at 09:41BerndJuly 21st, 2012 at 09:45BerndJuly 21st, 2012 at 10:33BerndJuly 24th, 2012 at 06:30AnonymousJuly 20th, 2012 at 15:49BerndJuly 20th, 2012 at 20:21Jean-Marc ValinJuly 20th, 2012 at 19:16WolfgangJuly 21st, 2012 at 04:33bubbaJuly 21st, 2012 at 14:02Wolfgang KellerJuly 21st, 2012 at 16:15Ralph GilesJuly 25th, 2012 at 13:00PuXJuly 21st, 2012 at 18:07searJuly 22nd, 2012 at 22:43BerndJuly 24th, 2012 at 07:08PuXJuly 26th, 2012 at 16:47panziSeptember 11th, 2012 at 17:59SteveSeptember 12th, 2012 at 18:46OuchNovember 13th, 2012 at 21:52austinJuly 24th, 2012 at 07:01BerndJuly 24th, 2012 at 07:12austinJuly 27th, 2012 at 08:10kiziJuly 26th, 2012 at 15:19Caspy7August 2nd, 2012 at 17:09BerndAugust 13th, 2012 at 08:46Caspy7August 13th, 2012 at 08:58powAugust 26th, 2012 at 19:50pdAugust 2nd, 2012 at 21:33powAugust 26th, 2012 at 19:52sylockSeptember 4th, 2012 at 07:35Ralph GilesSeptember 4th, 2012 at 13:01sylockSeptember 4th, 2012 at 22:31Ralph GilesSeptember 11th, 2012 at 21:51