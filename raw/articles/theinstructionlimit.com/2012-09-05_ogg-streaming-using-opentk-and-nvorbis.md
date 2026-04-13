---
title: Ogg streaming using OpenTK and NVorbis
url: https://theinstructionlimit.com/ogg-streaming-using-opentk-and-nvorbis
author: Author Renaud Bédard
published: '2012-09-05'
source_blog: The Instruction Limit
source_site: https://theinstructionlimit.com
category: graphics
fetched: '2026-04-13'
---

##### August 18th, 2015 Update

This article could be an interesting reference for people trying to understand how you can submit your own buffers to do streaming audio with OpenAL, but the actual tools I’m using (NVorbis, OpenTK) are outdated and I can’t recommend them anymore.

If you’re looking for a modern C# way of doing the same thing, look at how [the Song class](https://github.com/flibitijibibo/FNA/blob/master/src/Media/Xiph/Song.cs) is implemented with Ogg Vorbis support in Ethan Lee’s [FNA](https://github.com/flibitijibibo/FNA) library, using [Xiph Vorbisfile](https://www.xiph.org/vorbis/doc/vorbisfile/) and [the DynamicSoundEffect API](https://github.com/flibitijibibo/FNA/blob/master/src/Audio/DynamicSoundEffectInstance.cs), especially if you’re trying to do this in a MonoGame- or XNA-like environment. It’s much faster, the codebase is cut by half, and much less threading pitfalls!

Original article follows…

*Updated September 7th 2012 : New OggStream class with better support for concurrent stream playback.*

I was looking for a suitable replacement for the audio streaming and compression capabilities of [XACT](http://en.wikipedia.org/wiki/Cross-platform_Audio_Creation_Tool) when porting an XNA project to [MonoGame](http://monogame.codeplex.com/), and it doesn’t look like there’s a clear winner yet. MonoGame contributors suggested [NAudio](http://naudio.codeplex.com/), but it looks like work needs to be done to make it portable, and the sample code is a mess. [FMod EX](http://www.fmod.org/) or competing commercial solutions are an easy but costly choice. So I turned to [ OpenAL](http://connect.creativelabs.com/openal/default.aspx) to see if it can be a free and usable solution for streaming compressed audio with some DSP capabilities.

T’was a bit challenging, but not impossible! :)

## Decoding OGGs

Out of the box, OpenAL doesn’t support being fed MP3 or OGG sources. There are [extensions](http://connect.creativelabs.com/openal/OpenAL%20Wiki/Extensions.aspx) for those, but [according to one implementation](http://kcat.strangesoft.net/openal.html), they’re deprecated. So you need to handle decoding yourself and feed the PCM bitstream to OpenAL.

It sure would be nice to have a purely managed implementation of [libVorbis](http://xiph.org/vorbis/), but it doesn’t exist, so there’s a dozen homemade decoders floating around open source code hubs in various states of workability. I was pointed to [ NVorbis](http://nvorbis.codeplex.com/) by TheGrandHero

[on the TIGSource forums](http://forums.tigsource.com/index.php?topic=28301.msg788593#msg788593), and I haven’t found a better alternative yet.

[CsVorbis](https://github.com/mono/csvorbis)is another, but it doesn’t support streaming, all the decoding is done up-front, which defeats the purpose.

[OggSharp](http://oggsharp.codeplex.com/)is just a fork of CsVorbis with XNA helpers, so nope. TheGrandHero also mentioned trying out

[DragonOgg](http://sourceforge.net/projects/dragonogg/)but having

[problems](http://forums.tigsource.com/index.php?topic=28301.msg788475#msg788475)with it.

NVorbis worked like a charm for me, but it’s pretty early and doesn’t support some features like seeking around the stream, so looping or restarting playback requires creating a new whole new reader/decoder. I also took some time to optimize the memory usage in [my fork of the project](https://github.com/renaudbedard/nvorbis).

*07/09/2012 Update : Andrew Ward, the author of NVorbis, resolved the memory allocation problems that the version I forked off had, so I pulled the new changes out instead.*

## Streaming

Once you have some decoded data, you have to make OpenAL stream it. This is sort of tricky but [well](http://devmaster.net/posts/openal-lesson-8-oggvorbis-streaming-using-the-source-queue)–[documented](http://benbritten.com/2010/05/04/streaming-in-openal/).

The basic idea is the following :

- Generate one OpenAL
**source**for your sound file, like XACT cues - Generate 2 or more OpenAL
**buffers** - Fill at least one of those with the first samples of the sound and enqueue it/them to the source
- Start playback of the source; it’ll play all the buffers associated with it, in order
**In a background thread**:- Query the source to know whether buffers have already been processed
- If so, dequeue those buffers, refill them with fresh data and re-enqueue them

In practice, since it involves threads, it’s a bit more obtuse than the pseudo-code, but OpenAL makes it relatively painless. The trick is to read enough data and often enough to avoid buffer underruns.

Then, if you want to loop the sound, it’s not as easy as setting the source’s “Looping” parameter to true, because the buffers never contain the full sound file. Instead of no longer feeding the buffers when you hit the end of the Ogg stream, you just start back at the beginning and feed continuously, which has the nice side-effect of being 100% gapless.

## Filters and effects

Finally, I wanted to have one fancy effect that XACT provided : low-pass filtering. This is used extensively in FEZ as a gameplay mechanic, so I could hardly live without it in MonoGame ports.

Thankfully, [OpenAL Effect Extensions](http://connect.creativelabs.com/developer/Wiki/Introduction%20to%20EFX.aspx) (EFX) provide cross-platform effects including filters, at least in theory. In reality, this depends on whether the driver implementation supports them, and even the Creative reference Windows implementation doesn’t on my system.

I was able to find a software implementation that does though, [OpenAL Soft](http://kcat.strangesoft.net/openal.html), and it’s cross-platform, so that bodes well.

To override the installed implementation, just supply the software DLL in the application’s directory and voilà. Had no problems with it up to now, performance or otherwise.

Plus, it comes with a console application that outputs which EFX and other extensions are supported in this implementation. This is handy to detect whether the right DLL’s been used, and helped me figured out that the Creative implementation didn’t support any filter. Here’s what it should say :

## Sample class

The result of all of this is a OggStream class that is in my fork of NVorbis on GitHub, which you can find here :

[OggStream.cs (initial, simpler version)](https://github.com/renaudbedard/nvorbis/blob/9a14370d649869ab86fdaf905ca232905583e4aa/OggStream/OggStream.cs)**OggStream.cs**(version 2.0 with better concurrent stream playback support)

*Update :* Version 2.0 comes with [a sample console application](https://github.com/renaudbedard/nvorbis/blob/54a922615010f52330e6b4bad7c481ff4e27c778/OggStream/Program.cs) which allows you to test and visualize how different streams get buffered and when buffer underruns occur in a nice concise format. I’m really quite happy about it, give it a shot! Here’s how it looks :

![New visualization program](../../assets/543be63a30aabe69.png)


Legend of the symbols that this app blurts out :

`(*`

means synchronous buffering (`Prepare()`

) has started, and`)`

means it ended.`.`

means that one buffer has been refilled with fresh samples`|`

means that there are no more samples to consume from the sound file`!`

means that playback stopped because of a buffer underrun and had to be restarted`{`

and`}`

represent calls to`Start()`

and`Stop()`

`[`

and`]`

represent calls to`Pause()`

and`Resume()`

`L`

,`F`

or`f`

and`V`

or`v`

in prefix means respectively that the stream is looping, fading the low-pass filter in/out or fading volume in/out

My code has only been tested on .NET on Windows, but I don’t see why it wouldn’t work in Mono either.

Like all the unlicensed content on this blog, it’s public domain, but attribution is appreciated.

Thanks for your code, really was very interesting and it was very useful too.

Why Ogg Vorbis , when we now have Ogg Opus ?

Well for one thing, I had no idea it existed! It seems pretty new.

Also, it could take a while until we get a purely managed decoder like NVorbis. I hope it happens, though.

I owe you a beer! Now get back to Montreal!

Hey! The NVorbis guy just made an update that fixed the memory consumption problem, just wanted to let you know :) (https://nvorbis.codeplex.com/discussions/437551)