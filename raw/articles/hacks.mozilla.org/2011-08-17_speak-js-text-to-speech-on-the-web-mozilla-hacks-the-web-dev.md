---
title: 'speak.js: Text-to-Speech on the Web – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2011/08/speak-js-text-to-speech-on-the-web/
author: Alon Zakai
published: '2011-08-17'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Text-to-Speech (TTS) can make content more accessible, but there is so far no simple and universal way to do that on the web. One possible approach is shown in ** this demo**, which is powered by

[speak.js](https://github.com/kripken/speak.js), a new 100% pure JavaScript/HTML5 TTS implementation. speak.js is a port of

[eSpeak](http://espeak.sourceforge.net/), an open source speech synthesizer, from C++ to JavaScript using

[Emscripten](http://emscripten.org).

Compiling an existing speech synthesis engine to JavaScript is a good way to avoid writing a complicated project like eSpeak from scratch. Once compiled, the eSpeak code in speak.js doesn’t know it’s running on the web: speak.js uses the [ Emscripten emulated filesystem](https://github.com/kripken/emscripten/wiki/Filesystem-Guide) to ‘fake’ the normal file reading and writing calls that the eSpeak C++ code has (fopen, fread, etc.). This allows the normal eSpeak datafiles to be used (either through an xhr, or by converting them to JSON and bundling them with the script file). The result of running the compiled eSpeak code is that it ‘writes’ a .wav file with the generated audio to the emulated filesystem. speak.js then takes that data, encodes it using base64, and creates a data URL. That URL is then loaded in an HTML5 audio element, letting the browser handle playback. (Note that while that is a very simple way to do things, it isn’t the most efficient. speak.js has not yet focused on speed, but with some additional work it could be much faster, if that turns out to be an issue.)

Why would you want TTS in JavaScript? Well, with speak.js you can bundle a single .js file in your website, and then generating speech is about as simple as writing

speak("hello world")

(see the [speak.js website](https://github.com/kripken/speak.js) for instructions). The generated speech will be exactly the same on all platforms, unlike if your users each did TTS in their own way (using an OS capability, or a separate program). speak.js can also be used to build browser addons in a straightforward way, since it’s pure JavaScript – no need for platform dependent binaries, and the addon will work the same on all OSes.

A few more comments:

- JavaScript is getting more and more capable all the time. The development versions of the top JavaScript engines today can run code compiled from C++ only 3-5X slower than a fast C++ compiler, and getting even better. As a consequence, expanding the capabilities of the web platform can in many cases be done in JavaScript or by compiling to JavaScript, instead of adding new code to the browsers themselves, which inevitably takes longer – especially if you wait for all browsers to implement a particular feature.
- While speak.js uses only standards-based APIs, due to browser limitations it can’t work everywhere yet. It won’t work in IE, Safari or Opera since they don’t support typed arrays, nor in Chrome since it doesn’t support WAV data URLs. So currently speak.js only works properly in Firefox. However, the missing features just mentioned are not huge and hopefully those browser makers will implement them soon. It is also possible to implement workarounds in speak.js for these issues (see next comment).
- Help with improving speak.js is very welcome! One important thing we need is to implement workarounds for the issues that prevent speak.js from running on the browsers it currently can’t run on. Another goal is to build browser addons using speak.js. Please get in touch
[on github](https://github.com/kripken/speak.js)if you want to help out. - eSpeak supports multiple languages so speak.js can too. You do need to include the additional language files though.
[Here](http://syntensity.com/static/espeak_fr.html)is an experimental build where you can switch between English and French support (note that it is an unoptimized build, so it will run slower).

## 14 comments

Muhammad Tarmizi bin KamaruddinAugust 17th, 2011 at 11:45azakaiAugust 17th, 2011 at 11:58PrestaulAugust 17th, 2011 at 12:02azakaiAugust 17th, 2011 at 12:10abralAugust 17th, 2011 at 12:54Eric JungAugust 17th, 2011 at 14:22azakaiAugust 17th, 2011 at 14:48Eric JungAugust 17th, 2011 at 14:51PaulAugust 17th, 2011 at 17:26skierpageAugust 17th, 2011 at 17:35anfemfjsAugust 18th, 2011 at 03:58ChrisSeptember 17th, 2012 at 15:10Gerardo CapielAugust 27th, 2011 at 09:03Gerardo CapielAugust 27th, 2011 at 09:05