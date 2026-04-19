---
title: 'Crap: WASMtoy.A failed experiment.'
url: https://c0de517e.com/004_wasmtoy.htm
author: Angelo Pesce
published: '2023-09-14'
source_blog: 'c0de517e''s weblore: Main Entrance.'
source_site: https://c0de517e.com/
category: graphics
fetched: '2026-04-19'
---

A while ago, for no good reason at all, I decided to learn javascript. Enticed by this newfangled idea called "the web", and the promise of "write once, run anywhere, for real this time" - I embarked on a (short) journey, of course mostly focusing on Computer Graphics.

Tragically, if you want to learn (or teach) real-time rendering today, the javascript/webgl ecosystem (I strongly reccomend

[picoGL.js](https://tsherif.github.io/picogl.js/)) is among the better choices.

Nobody should start with Vulkan or DirectX 12 (even 11 is questionable), Metal requires a mac, classic OpenGL is dead and "modern" OpenGL is both dead and an horrible, design by commitee mess (don't worry, Vulkan's gonna get there too).

Maybe one day I'll write something about "Javascript for C++ rendering engineers who can't web good", but as always, I'm digressing... Suffice to say, along the road I became also interested in WASM - and that path crossed another interest of mine, in building universal virtual machines for "permacomputing" communities (see:

[https://github.com/paladin-t/fantasy](https://github.com/paladin-t/fantasy)).

I wanted to see if WASM, or a WASM subset, could make for a viable universal language for a small virtual computer, and thus I created "WASMtoy" - a

[ShaderToy](https://www.shadertoy.com/) inspired editor that allows you to write "raw" webassembly, gives you a small block of memory with a defined memory mapping to a framebuffer, and executes every frame a WASM function to draw on screen.

I never intended to create an actual website with a database ala ShaderToy proper, but I thought perhaps it would be cute to do something like this for code golfing and have a twitter bot that listens to tweets with binaries encoded within them, and replies with the resulting image after evaluating a few frames - ala

[BBC micro bot](https://www.bbcmicrobot.com/).

That's why you'll see in the WASMtoy page buttons to encode/decode base2048.

On paper all of this sounds lovely (to me), and on paper WASM looks great as well - it has both registers (local and global) and a stack to make expression evaluation (chaining instructions) easy. The instruction set itself looks very reasonable, and I could get most things up and running in a day!

In fact, at the beginning the only major obstacles were my zero knowledge of web anything, the fact that most libraries insist in distibuting only node.js packages (while I don't want packages at all, I want to just include all the code I need in the static page), and other general javascript warts (really? if I mispell a variable, and access something that does not exist, there is no... error at all? never? WTF?).

Unfortunately, in the end it was a failure on all accounts. The main issue is that WASM is clearly made for compiler writers, not to be used directly. Register access is terrible, with explicit get/set that move from registers to the stack.

The stack seems like something that would be amazing for code golfing (one of the main virtues of Forth, and of stack machines since, is that it's very compact), but alas, WASM lacks stack modification opcodes like "dup" and "rot" - which are fundamental if you want to save space and your sanity. No "dup" means to reuse a value you have to save it to a register, which again entail these annoying explicit get/set opcodes.

So... my loss is your... something. I don't know. Have fun!

[WASMtoy](004_wasmtoy/main.html)