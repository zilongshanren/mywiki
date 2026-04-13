---
title: Writing Web Audio API code that works in every browser – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2013/08/writing-web-audio-api-code-that-works-in-every-browser/
author: Soledad Penadés
published: '2013-08-20'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

You probably have already read [the announcement](https://hacks.mozilla.org/2013/07/web-audio-api-comes-to-firefox/) on the Web Audio API coming to Firefox, and are totally excited and ready to make your *until-now-WebKit-only* sites work with Firefox, which uses the unprefixed version of [the spec](https://dvcs.w3.org/hg/audio/raw-file/tip/webaudio/specification.html).

Unfortunately, Chrome, Safari and Opera still use the `webkitAudioContext`

prefixed name. Furthermore, as a result of the spec being still in flux, some browsers use deprecated properties and method names that are not present in standards-compliant browsers: Safari uses the old method names, Firefox uses the new ones, and Chrome and Opera use both. In addition, not all features of Web Audio are already implemented in Firefox *yet*.

*What do we do!?*

We don’t want to maintain two or more separate code bases, and feature detection code is cumbersome! Plus we want to write code that reliably works in the future, or at least, works with a minimum amount of changes. Is there a way to satisfy all these constraints at the same time? *Probably!*

## Writing for today (and tomorrow)

First, get a copy of [AudioContext-MonkeyPatch](https://github.com/cwilso/AudioContext-MonkeyPatch/) by Chris Wilson. This little library will “normalise” the interfaces for you and make it look as if your code is running in a standards compliant browser, by aliasing prefixed names to the unprefixed versions. And it won’t do anything if the unprefixed versions are already present.

Once you include it in your page, you can write in “modern Web Audio API” style, and do things such as:

```
var audioContext = new AudioContext();
```

everywhere, including Chrome/ium, Opera, Safari, and —of course!— Firefox.

Also, if new methods such as `start`

are not detected in some nodes, the library will also alias them to their old names. Thus, `start`

is mapped to `noteOn`

, `stop`

to `noteOff`

, and so on.

If you’re porting moderately “old” code (say, a year old) it’s possible that it uses some methods that `AudioContext-MonkeyPatch`

doesn’t alias, because it helps you to write code in the *new* style. For example, the way to create instances of `GainNode`

used to be

```
var gain = audioContext.createGainNode();
```

but nowadays it is just

```
var gain = audioContext.createGain();
```

Since the old method names are not present in Firefox, existing code may crash with something like `createGainNode is not a function`

, and you now know why.

There’s [a section](https://dvcs.w3.org/hg/audio/raw-file/tip/webaudio/specification.html#OldNames) in the spec that lists the old names and their updated equivalences; be sure to check it out and change your code accordingly. You can also check [this article](https://developer.mozilla.org/en-US/docs/Web_Audio_API/Porting_webkitAudioContext_code_to_standards_based_AudioContext) on porting which covers more cases and has many code samples.

## Things that are not ready yet

Second, ensure that your project doesn’t use node types that are not implemented yet in Firefox: [MediaStreamAudioSourceNode](https://dvcs.w3.org/hg/audio/raw-file/tip/webaudio/specification.html#MediaStreamAudioSourceNode), [MediaElementAudioSourceNode](https://dvcs.w3.org/hg/audio/raw-file/tip/webaudio/specification.html#MediaElementAudioSourceNode) and [OscillatorNode](https://dvcs.w3.org/hg/audio/raw-file/tip/webaudio/specification.html#OscillatorNode).

If it’s using, for example, `OscillatorNode`

, you will have to wait until it is supported, or maybe, if you’re really eager, hack in some replacement using [ScriptProcessorNode](https://dvcs.w3.org/hg/audio/raw-file/tip/webaudio/specification.html#ScriptProcessorNode-section), which allows you to write a node with callbacks that get called periodically, so that your JavaScript code generates or processes audio.

The node parameters you use must also be supported in Firefox too. If they aren’t, you might be able to change them into something “acceptable” for the time being, and count on the talented audio developers to implement those very soon.

For example, up until a couple of days ago [PannerNode](https://dvcs.w3.org/hg/audio/raw-file/tip/webaudio/specification.html#PannerNode-section) did not support the default HRTF panning model yet, and attempting to use a `PannerNode`

with that configuration simply resulted in silence or a mono output coming out from that node, depending on the build you used.

Today the support is already present in [Nightly](http://nightly.mozilla.org/), but not quite yet in [Aurora](http://www.mozilla.org/en-US/firefox/aurora/). In the meantime, you can explicitly specify `'equalpower'`

instead:

```
var panner = new audioContext.PannerNode();
panner.panningModel = 'equalpower';
```

## Keep track

The best way to know what’s going on in the Web Audio API land is to subscribe to the [mailing list](http://lists.w3.org/Archives/Public/public-audio/). Be aware that there might be a bit of high level tech discussions from time to time, and you might not understand it all, but you will learn a lot even if only by skimming through it.

You might also want to subscribe to [the umbrella bug](https://bugzilla.mozilla.org/show_bug.cgi?id=779297) that tracks the Web Audio API implementation in Firefox, so that you get alerts when associated bugs get updated or resolved.

Finally, there’s also a [list of projects](https://github.com/WebAudio/demo-list) built with the Web Audio API, specifying which ones use the standard `AudioContext`

and which browsers do they work on. If you’re a person that learns by example, it might be interesting to have a look at their source and see how they have resolved the compatibility issues.

## About
[
Soledad Penadés ](https://soledadpenades.com)

Sole works at the Developer Tools team at Mozilla, helping people make amazing things on the Web, preferably real time. Find her on #devtools at irc.mozilla.org

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 2 comments

Mark BoasAugust 21st, 2013 at 03:32Soledad PenadésAugust 21st, 2013 at 03:38