---
title: WebAssembly Will Ease Collaboration on Next Generation Video Codecs – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2017/02/webassembly-will-ease-collaboration-on-next-generation-video-codecs/
author: Dan Callahan
published: '2017-02-15'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[Michael Bebenita](https://twitter.com/mbebenita), a Research Engineer at Mozilla, recently posted a [fascinating article](https://medium.com/@mbebenita/av1-bitstream-analyzer-d25f1c27072b) on the development of [AV1](https://en.wikipedia.org/wiki/AOMedia_Video_1), a next-generation video codec. If you’re interested in how new media formats are created, I highly recommend [reading the full article](https://medium.com/@mbebenita/av1-bitstream-analyzer-d25f1c27072b).

What caught my eye is the discussion of porting the AV1 bitstream analyzer to the Web:

The input to the analyzer is usually small (an encoded bitstream), but the output is very large. […]

The ideal solution is to run the analyzer directly in the browserand thus eliminate the need to download analyzer output.

But how do you do this when the codec is written in C? One option is to manually re-implement it in JavaScript and hope you can keep up with changes in the reference implementation. The other better option is to directly re-use the C and *compile it to the Web.* That’s exactly what the AV1 team is doing, with the help of [Emscripten](http://kripken.github.io/emscripten-site/).

Emscripten compiles arbitrary C/C++ into JavaScript, which makes it possible for the AV1 team to automatically compile each revision of their codec to JavaScript and post it to the Web. At which point, comparing two revisions of the codec is as easy as [sharing a link](https://beta.arewecompressedyet.com/analyzer.html?decoder=https://beta.arewecompressedyet.com/runs/av1_ref_off_intra_trellis_15f@2017-02-09T02:25:04.372Z/js/decoder.js&file=https://beta.arewecompressedyet.com/runs/av1_ref_off_intra_trellis_15f@2017-02-09T02:25:04.372Z/objective-1-fast/Netflix_Crosswalk_1920x1080_60fps_8bit_420_60f.y4m-63.ivf).

This workflow is fast enough, but it’s not as fast as it could be. Because JavaScript does not support 64-bit integers, many of AV1’s computations have to undergo costly numeric conversions. Specifically, emulating 64-bit math is estimated to add up to a 20% performance penalty to AV1, and we’ve seen performance penalties of up to 600% in other projects that are directly attributable to this emulation.

That’s where [WebAssembly](http://webassembly.org/) comes in. WebAssembly is a new, low-level format for programs on the Web. It’s an open standard being developed by Mozilla, Microsoft, Google, and Apple, so it will eventually work in all browsers. Crucially, Bebenita explains, “WebAssembly has support for 64 bit math, and once that’s ready [the AV1 Bitstream Analyzer will] be switching over to WebAssembly.”

Fortunately, Emscripten already has experimental support for compiling to WebAssembly, so the AV1 workflow will remain the same: develop a single codebase in C and use Emscripten to compile that to the Web for testing. In this way, WebAssembly will play an integral role in the development of next generation video codecs.

More importantly, this workflow represents a fundamental shift in Web development: **The wall between “native” and the Web is falling,** and developers will be able to seamlessly use the same libraries in both contexts. This marks the end of tedious, manual ports of projects to JavaScript and opens the door to dramatically greater performance on the Web.

## About
[
Dan Callahan ](http://dancallahan.info)

Engineer with Mozilla Developer Relations, former Mozilla Persona developer.

## One comment

ChristieFebruary 15th, 2017 at 21:38