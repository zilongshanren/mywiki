---
title: Porting "Me & My Shadow" to the Web – C++ to JavaScript/Canvas via Emscripten
  – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/04/porting-me-my-shadow-to-the-web-c-to-javascriptcanvas-via-emscripten/
author: Chris Heilmann
published: '2012-04-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Editors note: This is a guest post by [Alon Zakai](http://mozakai.blogspot.co.uk/) of the Mozilla [Emscripten](https://github.com/kripken/emscripten/wiki) team. Thanks Alon!

[Me & My Shadow](http://meandmyshadow.sourceforge.net/) is an open source 2D game, with clever gameplay in which you control not one character but two. I happened to hear about it recently when they released a 0.3 version:

Since I’m looking for games to port to the web, I figured this was a good candidate. It was quite easy to port, here is the result: [Me & My Shadow on the Web](http://syntensity.com/static/mams/mams.html)

You can also get the [source on GitHub](https://github.com/kripken/meandmyshadow.web).

The port was done automatically by compiling the original code to JavaScript using [Emscripten](http://emscripten.org/), an open-source C++ to JavaScript compiler that uses LLVM. Using a compiler like this allows the game to just be compiled, instead of manually rewriting it in JavaScript, so the process can take almost no time.

The compiled game works almost exactly like the desktop version does on the machines and browsers I’ve tested on. Interestingly, performance looks very good. In this case, it’s mainly because most of what the game does is blit images. It uses the cross-platform SDL API, which is a wrapper library for things like opening a window, getting input, loading images, rendering text, etc. (so it is exactly what a game like this needs). Emscripten supports SDL through native canvas calls, so when you compile a game that uses SDL into JavaScript, it will use Emscripten’s SDL implementation. That implementation implements SDL blit operations using drawImage calls and so forth, which browsers generally hardware accelerate these days, so the game runs as fast as it would natively.

For example, if the C++ code has

```
SDL_BlitSurface(sprite, NULL, screen, position)
```

then that means to blit the entire bitmap represented by sprite into the screen, at a specific position. Emscripten’s SDL implementation does some translation of arguments, and then calls

```
ctx.drawImage(src.canvas, sr.x, sr.y, sr.w, sr.h, dr.x, dr.y, sr.w, sr.h);
```

which draws the sprite, contained in `src.canvas`

, into the context representing the screen, at the correct position and size. In other words, the C++ code is translated automatically into code that uses native HTML canvas operations in an efficient manner.

There are some caveats though. The main problem is browser support for necessary features, the main problems I ran into here are typed arrays and the Blob constructor:

- Typed arrays are necessary to run compiled C++ code quickly and with maximum compatibility. Emscripten can compile code without them, but the result is slower and needs manual correction for compatibility. Thankfully, all browsers are getting typed arrays. Firefox, Chrome and Opera already have them, Safari was only missing
`FloatArray64`

until recently I believe, and IE will get them in IE10. - The Blob constructor is necessary because this game uses Emscripten’s new compression option. It takes all the datafiles (150 or so), packs them into a single file, does LZMA on that, and then the game in the browser downloads that, decompresses, and splits it up. This makes the download much smaller (but does mean there is a short pause to decompress). The issue though is that we end up with data for each file in a typed array. It’s easy to use the BlobBuilder for images, but for audio, they need the mimetype set or they fail to decode, and only the Blob constructor supports that. It looks like only Firefox has the Blob constructor so far, I’ve been told on Twitter there might be a workaround for Chrome that I am hoping to hear more about. Not sure about other browsers. But, the game should still work, just without sound effects and music.

Another caveat is that there is some unavoidable amount of manual porting necessary:

JavaScript main loops must be written in an asynchronous way: A callback for each frame. Thankfully, games are usually written in a way that the main loop can easily be refactored into a function that does one iteration, and that was the case here. Then that function that does one main loop iteration is called each frame from JavaScript. However, there are other cases of synchronous code that are more annoying, for example fadeouts that happen when a menu item is picked are done synchronously (draw, SDL_Delay, draw, etc.). This same problem turned up when I ported Doom, I guess it’s a common code pattern. So I just disabled those fadeouts for now; if you do want them in a game you port, you’d need to refactor them to be asynchronous.

Aside from that, everything pretty much just worked. (The sole exception was that this code fell prey to an [LLVM LTO bug](http://llvm.org/bugs/show_bug.cgi?id=12351), but Rafael fixed it.) So in conclusion I would argue that there is no reason not to run games like these on the web: They are easy to port, and they run nice and fast.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 7 comments

azakaiApril 4th, 2012 at 11:05Rasmus WikmanApril 4th, 2012 at 11:59Neil RashbrookApril 5th, 2012 at 05:52azakaiApril 5th, 2012 at 09:57Rudolf O.April 5th, 2012 at 07:44azakaiApril 5th, 2012 at 09:59LozzyApril 8th, 2012 at 04:23