---
title: 'Web Games Platform: Newest Developments – Mozilla Hacks - the Web developer
  blog'
url: https://hacks.mozilla.org/2017/03/web-games-platform-newest-developments/
author: Andre Vrignaud
published: '2017-03-01'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In July of 2015 we announced our [Games Technology Roadmap](https://blog.mozilla.org/futurereleases/2015/07/02/mozilla-games-technology-roadmap), and have been working on addressing those pain points as shared by developers.

Games are an important part of the web experience. Mozilla and other browser vendors have been working hard to find alternative paths that developers can migrate to. As we come to the end of plugins ([Firefox 52](https://www.mozilla.org/en-US/firefox/52.0/releasenotes)) and many browsers planning to make Flash click-to-play during 2017-2018, we are working hard to complete the alternatives and insure they are viable. Many new features that will help improve the platform are arriving in the next few versions of Firefox, and we are seeing other browsers on a similar course.

We’ve been working closely with other browsers, tool makers, and game developers to test at scale, and promote universal availability of key technologies across all the major browsers. We have seen success with top Facebook titles such as [Bubble Witch 3 Saga](https://apps.facebook.com/bubblewitch-three) and [Candy Crush Jelly Saga](https://apps.facebook.com/candycrushjelly) from [King](https://king.com), and [Top Eleven](https://apps.facebook.com/topeleven) from [Nordeus](http://www.nordeus.com). There is still work to do to get full potential out of the platform, but today we wanted to provide a status update on what we’ve been working on and what you’ll see shipping in browsers in the near future. Whether you are using compiled code bases and/or JavaScript there’s a little bit here for everybody!

## What We Heard

As we reached out to game developers, publishers, and browser makers we heard a common set of concerns and requests:

- Developers wanted to improve their user experience. They have let us know they would like to see reduced code size, faster compile and load times, reduced memory usage, and improved performance to make it easier for users to engage.
[WebAssembly](https://github.com/webassembly)is a significant leap forward in addressing all of these issues.- We recently
[announced](https://lists.w3.org/Archives/Public/public-webassembly/2017Feb/0002.html)that the four major browsers have reached a consensus on the stable initial version of the standard, enabling all browsers to start shipping WebAssembly. - Mozilla intends to release WebAssembly, the successor to asm.js, in Firefox 52 in March 2017.

- Developers wanted to reach as many users as possible and would like to see more users be able to run
[WebGL](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API)content.- Targeted efforts have improved desktop WebGL success rates on non-Windows XP machines from 80% to 99%. We are also seeing a similar trend across other browsers. In addition, telemetry shows that desktop WebGL availability matches that of Flash on Firefox.
- Developers wanted
[OpenGL ES3](https://en.wikipedia.org/wiki/OpenGL_ES)features in WebGL 2, including new texture formats, and support for floating point texture filtering, rendering to multiple render targets, and MSAA multi-sampling. - WebGL 2 supports OpenGL ES3 features. WebGL 2 was released in Firefox 51 in January 2017, and
[other browsers](https://blog.chromium.org/2016/12/chrome-56-beta-not-secure-warning-web.html)are following suit.

- Developers have asked for greater flexibility in allocating larger amounts of address space on 32-Bit systems to run bigger and more complex applications.
- 32-Bit Out Of Memory (OOM) issues are often caused by a browser process being unable to allocate large blocks of memory due to address space fragmentation.
- Firefox intends to ship a 32-Bit OOM solution in Firefox 53 in April 2017.

We do not have similar challenges in 64-Bit versions of Firefox.

- Developers would like greater information about the hardware Firefox users browse the web on to inform their development decisions.
- We released the 1.0 version of the
[Firefox Hardware Report](https://metrics.mozilla.com/firefox-hardware-report)late last year.

- We released the 1.0 version of the

## Details

### Standardizing and Shipping WebAssembly:

WebAssembly is an emerging standard whose goal is to define a safe, portable, size- and load-time efficient binary compiler target which offers near-native performance — a virtual CPU for the Web. WebAssembly is being developed in a [W3C Community Group](https://www.w3.org/community/webassembly/) (CG) whose [members](https://www.w3.org/community/webassembly/participants) include Mozilla, Microsoft, Google, and Apple.

WebAssembly can be considered the successor to [asm.js](http://asmjs.org), a [Mozilla-pioneered project](https://blog.mozilla.org/futurereleases/2013/05/02/epic-citadel-demo-shows-the-power-of-the-web-as-a-platform-for-gaming) to push the limits of performance within the constraints of the existing JavaScript language. Although, asm.js now offers [impressive performance in all browsers](https://hacks.mozilla.org/2015/03/asm-speedups-everywhere), as a new standard, WebAssembly removes incidental constraints, allowing engines to get ever-closer to native performance (while maintaining the same safety and security model as JavaScript). [Preliminary measurements in Firefox](https://hacks.mozilla.org/2016/10/webassembly-browser-preview/#measurements) show that, on average, WebAssembly brings realistic C/C++ workloads to run within 1.25× native speed, down from 1.38× with asm.js — a 9% improvement! Further speedups are anticipated as work continues on the whole pipeline. Dramatic 8× speedups have been observed for synthetic workloads that utilize new WebAssembly features like 64-bit integer arithmetic.

We recently [announced](https://lists.w3.org/Archives/Public/public-webassembly/2017Feb/0002.html) that the WebAssembly Community Group had reached a consensus on the initial version of the standard. Interoperable implementations have [landed in pre-release Firefox](https://bugzilla.mozilla.org/show_bug.cgi?id=1242803) and Chrome channels, and are under development in [Chakra](https://github.com/Microsoft/ChakraCore/wiki/Roadmap#language-innovation--standards) and [JavaScriptCore](https://bugs.webkit.org/show_bug.cgi?id=159775). Mozilla intends to release WebAssembly, the successor to asm.js, in Firefox 52 in March 2017.

### Improving WebGL Success Rates:

We have been able to identify and address issues that impacted the availability of WebGL on Firefox. In particular, Firefox telemetry shows that we have reduced WebGL availability failures from over 20% in Firefox 47 to less than 8% in Firefox 50 across all machines. And targeted efforts have improved WebGL success rates on non-Windows XP machines from 80% to 99%. This is consistent with the level of improvement we have seen with other browsers.

### Standardizing and Shipping WebGL/WebGL 2:

WebGL 2 is based on the OpenGL ES 3.0 specification, and offers new features, including 3D textures and 2D texture arrays, ESSL 3.0 (an advanced shading language), integer texture formats and vertex attributes, transform feedback, and uniform blocks for more efficient uploads. It also adds primitive restart, framebuffer blitting and invalidation, separable sampler objects, occlusion queries and pixel buffer objects. In addition, some optional WebGL 1 extensions are now part of the guaranteed core of WebGL 2, including multiple render targets, instanced drawing, depth and floating-point textures, and sRGB support. Also notable is support for the new [ETC2 texture format](https://en.wikipedia.org/wiki/Ericsson_Texture_Compression) which provides alpha support on a compressed texture and is supported on both desktop and mobile devices. Finally, improved garbage collection offers a smoother experience overall. WebGL 2 [shipped in Firefox 51](https://hacks.mozilla.org/2017/01/webgl-2-lands-in-firefox/) in January 2017.

### Addressing 32-Bit Out of Memory Issues (OOMs):

A consistent pain point for web developers using compiled code bases and asm.js is hitting out of memory conditions on 32-Bit browsers. By default, on Windows, Firefox is a 32-Bit application. This limits Firefox to being able to use (at most) 4 gigabytes of address space, which tends to become fragmented over time, and prevents a game’s ability to request a large enough allocation to successfully run.

To address this, we have proposed a new [Large-Allocation header.](https://gist.github.com/mystor/5739e222e398efc6c29108be55eb6fe3) This header tells the browser to make a best-effort attempt to load the document in an unfragmented content process, which should greatly decrease the OOM failure rate for top-level browsing contexts, even on bigger allocations. We aim to ensure that if the conditions for a cross-process navigation are met, web apps are able to reliably allocate a gigabyte of contiguous address space. It is our intention to ship this solution in Firefox 53.

An additional opportunity is to encourage users toward using a 64-Bit browser, which allows applications to use huge amounts of physical memory. This means that address space exhaustion (or OOMs) are basically impossible.

Today:

- 72% of our Windows users are running 32-bit Firefox on 64-bit Windows. These users could switch to a 64-bit Firefox.
- 25% are running 32-bit Firefox on 32-bit Windows. These users cannot switch to a 64-bit Firefox.
- 3% are running 64-bit Firefox already.

As nearly three-quarters of Firefox users are running 32-bit Firefox on 64-bit Windows, there is a huge opportunity to improve the ability of those users to run large web apps by accelerating the shift to 64-bit. As such, per our [64-Bit plan of record](https://wiki.mozilla.org/Firefox/Win64#Plan), we are targeting August 2017 (Firefox 55) to change the Firefox installer to default to 64-bit for new installs on 64-bit Windows. Upgrading existing 32-bit Firefox users on 64-bit Windows to 64-bit Firefox will probably happen in October 2017 (Firefox 56).

### Sharing information about the Firefox Hardware Audience:

Suppose you’re developing a sophisticated web game or application. You may have questions about what capabilities web users have access to on their systems, or how you can target the widest possible audience? To help address these questions we [recently released](https://hacks.mozilla.org/2016/12/firefox-hardware-report) the [Firefox Hardware Report](https://metrics.mozilla.com/firefox-hardware-report) to help answer those questions and inform your development decisions.

On the site you’ll find a variety of data points showing what hardware and OSes Firefox web users are using on the web, and trends over time. This includes CPU vendors, cores, and speeds; system memory; GPU vendors, models, and display resolution; Operating System architecture and market share; browser architecture share, and finally, Flash plugin availability.

## In Conclusion

Our focus is now on landing all of the above improvements in the coming months. We wish to extend our gratitude to the game developers, engine providers, and other browsers’ engine teams who have worked so long on this technology. It’s been a massive effort, and we all collectively could not have done it without your help and feedback. Thank you!

## About Andre Vrignaud

Andre Vrignaud is the Head of Platform Strategy for Mozilla’s Mixed Reality Program, where he guides the strategy for Mozilla's efforts to enable an open, sustainable 3D web and ecosystem. With a side of net neutrality and privacy advocacy.

## 5 comments

PinoMarch 2nd, 2017 at 08:44voracityMarch 3rd, 2017 at 06:05Luke WagnerMarch 8th, 2017 at 09:04voracityMarch 10th, 2017 at 05:50diarecMarch 4th, 2017 at 07:53