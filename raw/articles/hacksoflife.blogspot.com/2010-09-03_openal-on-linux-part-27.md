---
title: OpenAL on Linux, Part 27
url: http://hacksoflife.blogspot.com/2010/09/openal-on-linux-part-27.html
author: Benjamin Supnik
published: '2010-09-03'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[bug](https://bugs.launchpad.net/bugs/273558)has effected X-Plane 8 and 9; we were able to recut 9 to work around it, but X-Plane 8 is a closed product. Here's the short story:

- A while ago intrepid developers replaced the implementation of libopenal on Linux with a new complete rewrite.
- When they did so, they raised the major version number.

The change in major version breaks the link to X-Plane, and would be appropriate if the library wasn't compatible.

Yesterday someone finally posted a list of dropped ABI symbols in the new OpenAL implementation. They are all extension symbols except for alBufferAppendData. So I can't deny that symbols are dropped and that is an ABI breakage. The question is: should the soname be revised?

Extensions

Most of the symbols missing are _LOKI. For those not familiar with OpenGL extensions (from which the OpenAL extension concept is stolen^H^H^H^H^H^Hborrowed) the idea is this: an app initializes the library, queries some kind of string to see what additional non-core features the library supports, and then resolves function pointers at run-time, using function pointers only once the extension string is present.

Therefore it's really important that the major version of the shared object not change when an extension is removed; the extension is not part of the ABI, applications should not (and cannot) depend on it being present at link-time, and an extension may not function without specialized hardware.

alBufferAppendData

There is one mystery symbol: alBufferAppendData, which is present without a decoration. From what I can tell from the annotated OpenAL 1.0 specification, "append-data" was a proposed streaming scheme that was eventually moved to an extension when it was dropped from the core. It's not in the 1.0 spec and it's not in the 1.1 spec.

So this strikes me as a bug in the implementation of the original library: it exports a symbol that shouldn't be there. Does it make sense to raise the major version of the .so because the symbol has been dropped? I don't think so, but I can see how you could argue it both ways.

The argument for dropping it is this: if the major version is changed, then the old and new OpenAL implementations can live side by side, and all applications are happy. Since alBufferAppendData is not trivial functionality, this would be better than expecting the new implementation to support alBufferAppendData for historic reasons.

But this is not at all what is happening; instead distributions are purging libopenal.so.0 (the old implementation) when they bring in the new one, and then asking applications to recompile themselves.

In other words, because some number of applications may be using a function that is not in any OpenAL specification but is in the old implementation, they have renamed the shared library, forcing everyone to recompile. In other words, they have replaced the convenience of having some games be broken

(In X-Plane we work around this by simply dlopening either libopenal.so.0 or libopenal.so.1, whichever one we can find. Since both implement the core spec symbols, this works fine.)

## No comments:

## Post a Comment