---
title: The Next Generation of Web Gaming – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2017/07/the-next-generation-of-web-gaming/
author: Andre Vrignaud
published: '2017-07-20'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Over the last few years, Mozilla has worked closely with other browsers and the industry to [advance the state of games on the Web](https://hacks.mozilla.org/2017/03/web-games-platform-newest-developments/). Together, we have enabled developers to deploy native code on the web, first via asm.js, and then with its successor [WebAssembly](http://webassembly.org). Now available in Firefox and Chrome, and also soon in [Edge](https://blogs.windows.com/msedgedev/2017/04/20/improved-javascript-performance-webassembly-shared-memory/#oqgire84ExxVPttp.97) and [WebKit](https://webkit.org/blog/7691/webassembly/), WebAssembly enables near-native performance of code in the browser, which is great for game development, and has also shown benefits for WebVR applications. WebAssembly code is able to deliver more predictable performance due to JIT compilation and garbage collection being avoided. Its wide support across all major browser engines opens up paths to near-native speed, making it possible to build high-performing plugin-free games on the web.

*“In 2017 Kongregate saw a shift away from Flash with nearly 60% of new titles using HTML5,*” said Emily Greer, co-founder and CEO of Kongregate.

*“Developers were able to take advantage of improvements in HTML5 technologies and tools while consumers were able to enjoy games without the need for 3rd-party plugins. As HTML5 continues to evolve it will enable developers to create even more advanced games that will benefit the millions of gamers on Kongregate.com and the greater, still thriving, web gaming industry.”*

Kongregate’s data shows that on average, about 55% of uploaded games are HTML5 games.

And we can also see that these are high-quality games, with over 60% of HTML5 titles receiving a “great” score (better than a 4.0 out of 5 rating).

In spite of this positive trend, opportunities for improvement exist. The web is an ever-evolving platform, and developers are always looking for better performance. One major request we have often heard is for multithreading support on the web. [SharedArrayBuffer](https://hacks.mozilla.org/2017/06/a-crash-course-in-memory-management/) is a required building block for multithreading, which enables concurrently sharing memory between multiple web workers. The [specification](https://tc39.github.io/ecma262/#sec-sharedarraybuffer-objects) is finished, and Firefox [intends to ship](https://groups.google.com/forum/#!topic/mozilla.dev.platform/Fjh9z7Er3aA) SharedArrayBuffer support in Firefox 55.

Another common request is for [SIMD](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SIMD) support. SIMD is short for Single Instruction, Multiple Data. It’s a way for a CPU to parallelize math instructions, offering significant performance improvements for math-heavy requirements such 3D rendering and physics.

The [WebAssembly Community Group](http://webassembly.org) is now focused on enabling hardware parallelism with SIMD and multithreading as the next major evolutionary steps for WebAssembly. Building on the momentum of shipping the first version of WebAssembly and continued collaboration, both of these new features should be stable and ready to ship in Firefox in early 2018.

Much work has gone into optimizing runtime performance over the last few years, and with that we learned many lessons. We have collected many of these learnings in a practical blog post about [porting games from native to web](https://hacks.mozilla.org/2017/07/webassembly-for-native-games-on-the-web), and look forward to your input on other areas for improvement. As multithreading support lands in 2018, expect to see opportunities to further invest in improving memory usage.

We again wish to extend our gratitude to the game developers, publishers, engine providers, and other browsers’ engine teams who have collaborated with us over the years. We could not have done it without your help — thank you!

## About Andre Vrignaud

Andre Vrignaud is the Head of Platform Strategy for Mozilla’s Mixed Reality Program, where he guides the strategy for Mozilla's efforts to enable an open, sustainable 3D web and ecosystem. With a side of net neutrality and privacy advocacy.

## 3 comments

Andrew WooldridgeJuly 20th, 2017 at 11:59Andre VrignaudJuly 20th, 2017 at 16:06WebGL userJuly 29th, 2017 at 08:20