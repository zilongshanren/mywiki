---
title: It's Opus, it rocks and now it's an audio codec standard! – Mozilla Hacks -
  the Web developer blog
url: https://hacks.mozilla.org/2012/09/its-opus-it-rocks-and-now-its-an-audio-codec-standard/
author: Jean-Marc Valin
published: '2012-09-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In a great victory for open standards, the [Internet Engineering Task Force (IETF)](http://www.ietf.org/) has just standardized Opus as [RFC 6716](http://tools.ietf.org/html/rfc6716).

Opus is the first state of the art, free audio codec to be standardized. We think this will help us achieve wider adoption than prior royalty-free codecs like Speex and Vorbis. This spells the beginning of the end for proprietary formats, and we are now working on doing the [same thing for video](https://www.ietf.org/mailman/listinfo/video-codec).

There was both skepticism and outright opposition to this work when it was first proposed in the IETF over 3 years ago. However, the results have shown that we can create a better codec through collaboration, rather than competition between patented technologies. Open standards benefit both open source organizations and proprietary companies, and we have been successful working together to create one. Opus is the result of a collaboration between many organizations, including the IETF, Mozilla, Microsoft (through Skype), Xiph.Org, Octasic, Broadcom, and Google.

## A highly flexible codec

Unlike previous audio codecs, which have typically focused on a narrow set of applications (either voice or music, in a narrow range of bitrates, for either real-time or storage applications), Opus is highly flexible. It can adaptively switch among:

- Bitrates from 6 kb/s to 512 kb/s
- Voice and music
- Mono and stereo
- Narrowband (8 kHz) to Fullband (48 kHz)
- Frame sizes from 2.5 ms to 60 ms

Most importantly, it can adapt seamlessly within these operating points. Doing all of this with proprietary codecs would require at least six different codecs. Opus replaces all of them, with better quality.

![Illustration of the quality of different codecs](../../assets/8150d5e28d9dd7df.png)


The specification is available in [RFC 6716](http://tools.ietf.org/html/rfc6716), which includes the reference implementation. [Up-to-date software releases](http://opus-codec.org/downloads/) are also available.

Some audio standards define a normative encoder, which cannot be improved after it is standardized. Others allow for flexibility in the encoder, but release an intentionally hobbled reference implementation to force you to license their proprietary encoders. For Opus, we chose to allow flexibility for future encoders, but we also made the best one we knew how and released that as the reference implementation, so everyone could use it. We will continue to improve it, and keep releasing those improvements as open source.

## Use cases

Opus is primarily designed for use in interactive applications on the Internet, including voice over IP (VoIP), teleconferencing, in-game chatting, and even live, distributed music performances. The IETF recently decided with [“strong consensus” to adopt Opus as a mandatory-to-implement (MTI) codec](http://www.ietf.org/mail-archive/web/rtcweb/current/msg05267.html) for WebRTC, an upcoming standard for real-time communication on the web. Despite the focus on low latency, Opus also excels at streaming and storage applications, beating existing high-delay codecs like Vorbis and HE-AAC. It’s great for internet radio, adaptive streaming, game sound effects, and [much more](https://hacks.mozilla.org/2012/07/firefox-beta-15-supports-the-new-opus-audio-format/).

Although Opus is just out, it is already supported in many applications, such as [Firefox](http://getfirefox.com), [GStreamer](http://gstreamer.net), [FFMpeg](http://ffmpeg.org), [foobar2000](http://foobar2000.org), [K-Lite Codec Pack](http://codecguide.com/changelogs_full.htm), and [lavfilters](http://code.google.com/p/lavfilters/), with upcoming support in [VLC](http://videolan.org), [rockbox](http://www.rockbox.org/) and [Mumble](http://mumble.info/).

For more information, visit the [Opus website](http://opus-codec.org/).

## About
[
Jean-Marc Valin ](https://jmvalin.ca/)

Jean-Marc Valin has a B.S., M.S., and PhD in Electrical Engineering from the University of Sherbrooke. He is the primary author of the Speex codec and one of the main authors of the Opus codec. His expertise includes speech and audio coding, speech recognition, echo cancellation, and other audio-related topics. He is currently employed by Mozilla to work on next-generation multimedia codecs.

## About
[
Timothy B. Terriberry ](http://people.xiph.org/~tterribe/)

Timothy B. Terriberry is a long-time volunteer for the Xiph.Org foundation, working on codecs such as Theora, Vorbis, CELT, and Opus. He has been contributing to Mozilla's media support since 2008 and hacking on WebRTC since 2010.

## 89 comments

AshleySeptember 11th, 2012 at 11:56Timothy B. TerriberrySeptember 11th, 2012 at 12:02ShmerlSeptember 11th, 2012 at 12:11ShmerlSeptember 11th, 2012 at 12:12Ryan B.September 15th, 2012 at 22:44AnonymousSeptember 11th, 2012 at 12:12Timothy B. TerriberrySeptember 11th, 2012 at 12:21Bruce PerensSeptember 11th, 2012 at 12:30MontySeptember 11th, 2012 at 12:56Bruce PerensSeptember 11th, 2012 at 13:43Timothy B. TerriberrySeptember 11th, 2012 at 13:06Bruce PerensSeptember 11th, 2012 at 13:17spellcheckerSeptember 11th, 2012 at 12:37Robert NymanSeptember 11th, 2012 at 13:36rogerSeptember 11th, 2012 at 12:51Timothy B. TerriberrySeptember 11th, 2012 at 13:20AudySeptember 11th, 2012 at 12:55Timothy B. TerriberrySeptember 11th, 2012 at 13:27starwedSeptember 11th, 2012 at 13:29DuskSeptember 11th, 2012 at 13:40natermerSeptember 11th, 2012 at 14:30Z4ppySeptember 11th, 2012 at 14:53RyanSeptember 15th, 2012 at 19:11ReinoSeptember 11th, 2012 at 13:27AudySeptember 11th, 2012 at 14:39JessicaSeptember 11th, 2012 at 17:05RyanSeptember 15th, 2012 at 19:13gonewestSeptember 11th, 2012 at 16:13Timothy B. TerriberrySeptember 11th, 2012 at 16:52GonewestSeptember 11th, 2012 at 19:12dimitri floresSeptember 11th, 2012 at 17:19Timothy B. TerriberrySeptember 11th, 2012 at 17:28Chun-Kwong WongSeptember 11th, 2012 at 17:33RyanSeptember 15th, 2012 at 19:15JonSeptember 11th, 2012 at 17:37Timothy B. TerriberrySeptember 11th, 2012 at 17:46ferongrSeptember 11th, 2012 at 18:30Jean-Marc ValinSeptember 11th, 2012 at 20:48userSeptember 11th, 2012 at 18:30ShmerlSeptember 11th, 2012 at 18:43Timothy B. TerriberrySeptember 11th, 2012 at 18:47David PiepgrassSeptember 11th, 2012 at 18:37Robert O’CallahanSeptember 11th, 2012 at 19:24Timothy B. TerriberrySeptember 11th, 2012 at 19:39Jean-Marc ValinSeptember 11th, 2012 at 20:44David PiepgrassSeptember 12th, 2012 at 14:23Jean-Marc ValinSeptember 15th, 2012 at 20:21RyanSeptember 15th, 2012 at 19:35Dave HaynieSeptember 12th, 2012 at 05:00MontySeptember 12th, 2012 at 05:11LeonSeptember 13th, 2012 at 07:07David PiepgrassSeptember 13th, 2012 at 08:53Bob HSeptember 13th, 2012 at 09:18David PiepgrassSeptember 13th, 2012 at 10:57RyanSeptember 15th, 2012 at 19:55BerndSeptember 14th, 2012 at 07:43Anthony “Airon” OetzmannSeptember 12th, 2012 at 05:05Anthony “Airon” OetzmannSeptember 12th, 2012 at 05:13Bob HSeptember 12th, 2012 at 05:23Timothy B. TerriberrySeptember 12th, 2012 at 05:31Bob HSeptember 12th, 2012 at 06:39Derrick CoetzeeSeptember 12th, 2012 at 06:03Jean-Marc ValinSeptember 12th, 2012 at 07:17RyanSeptember 15th, 2012 at 20:19Jean-Marc ValinSeptember 15th, 2012 at 20:44dumbSeptember 16th, 2012 at 01:27Jean-Marc ValinSeptember 16th, 2012 at 10:22dumbSeptember 16th, 2012 at 11:32JonadabSeptember 12th, 2012 at 13:39Derrick CoetzeeSeptember 12th, 2012 at 14:26David PiepgrassSeptember 12th, 2012 at 14:46RyanSeptember 15th, 2012 at 20:46rogerSeptember 12th, 2012 at 14:40Timothy B. TerriberrySeptember 13th, 2012 at 04:40BillSeptember 13th, 2012 at 12:49TegSeptember 13th, 2012 at 17:32Jean-Marc ValinSeptember 13th, 2012 at 21:32Omega XSeptember 14th, 2012 at 16:02GonewestSeptember 14th, 2012 at 17:15dumbSeptember 14th, 2012 at 22:52Jean-Marc ValinSeptember 15th, 2012 at 00:16spellcheckerSeptember 15th, 2012 at 10:52Greg MaxwellSeptember 15th, 2012 at 20:07spellcheckerSeptember 18th, 2012 at 20:03Richard M StallmanSeptember 16th, 2012 at 11:50ManuNovember 29th, 2012 at 08:07Derrick CoetzeeNovember 29th, 2012 at 15:12Derrick CoetzeeNovember 29th, 2012 at 15:37MickMarch 12th, 2013 at 04:35