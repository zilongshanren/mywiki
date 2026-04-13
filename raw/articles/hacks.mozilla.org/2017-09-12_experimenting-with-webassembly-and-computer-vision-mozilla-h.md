---
title: Experimenting with WebAssembly and Computer Vision – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2017/09/bootcamps-webassembly-and-computer-vision/
author: Dan Callahan
published: '2017-09-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This past summer, four time-crunched engineers with no prior [WebAssembly](https://hacks.mozilla.org/2017/02/a-cartoon-intro-to-webassembly/) experience began experimenting. The result after six weeks of exploration was [WebSight](https://websightjs.com/): a real-time face detection demo based on [OpenCV](http://opencv.org/).

By compiling OpenCV to WebAssembly, the team was able to reuse a well-tested C/C++ library directly in the browser and achieve performance an order of magnitude faster than a similar JavaScript library.

I asked the team members—[Brian Feldman](https://www.linkedin.com/in/brianjfeldman/), [Debra Do](https://www.linkedin.com/in/debra-do/), [Yervant Bastikian](https://www.linkedin.com/in/yervant-bastikian/), and [Mark Romano](https://www.linkedin.com/in/mgromano/)—to write about their experience.

**Note:** The report that follows was written by the team members mentioned above.

WebAssembly (“wasm”) made a splash this year with its [MVP release](http://webassembly.org/roadmap/), and eager to get in on the action, we set out to build an application that made use of this new technology.

We’d seen projects like [WebDSP](https://github.com/shamadee/web-dsp) compile their own C++ video filters to WebAssembly, an area where JavaScript has historically floundered due to the computational demands of some algorithms. This got us interested in pushing the limits of wasm, too. We wanted to use an existing, specialized, and time-tested C++ library, and after much deliberation, we landed on OpenCV, a popular open-source computer vision library.

Computer vision is highly demanding on the CPU, and thus lends itself well to wasm. Building off of some incredible work put forward by the [UC Irvine SysArch](https://github.com/ucisysarch/opencvjs) group and Github user [njor](https://github.com/njor/opencvjs), we were able to update outdated asm.js builds of OpenCV to compile with modern versions of [Emscripten](http://kripken.github.io/emscripten-site/), exposing much of OpenCV’s core functionality in JavaScript callable formats.

Working with these Emscripten builds went much differently than we expected. As Web developers, we’re used to writing code and being able to iterate and test very quickly. Introducing a large C++ library with 10-15 minute build times was a foreign experience, especially when our normal working environments are Webpack, Nodemon, and hot reloading everywhere. Once compiled, we approached the wasm build as a bit of a black box: the module started as an immutable beast of an object, and though we understood it more and more throughout the process, it never became ‘transparent’.

The efforts spent on compiling the wasm file, and then incorporating it into our JavaScript were worthwhile: it outperformed JavaScript with ease, and was significantly quicker than WebAssembly’s predecessor, asm.js.

We compared these formats through the use of a face detection algorithm. The architecture of the functions that drove these algorithms was the same, the only difference was the implementation language for each algorithm. Using web workers, we passed video stream data into the algorithms, which returned with the coordinates of a rectangle that would frame any faces in the image, and calculated an FPS measure. While the range of FPS is dependent on the user’s machine and the browser being used (Firefox takes the cake!), we noted that the FPS of the wasm-powered algorithm was consistently twice as high as the FPS of the asm.js implementation, and twenty times higher than the JS implementation, solidifying the benefits of web assembly.

Building in cutting edge technology can be a pain, but the reward was worth the temporary discomfort. Being able to use native, portable, C/C++ code in the browser, without third-party plugins, is a breakthrough. Our project, [WebSight](https://www.websightjs.com/), successfully demonstrated the use of OpenCV as a WebAssembly module for face and eye detection. We’re really excited about the future of WebAssembly, especially the eventual addition of garbage collection, which will make it easier to efficiently run other high-level languages in the browser.

*You can view the demo’s GitHub repository at github.com/Web-Sight/WebSight.*

## About
[
Dan Callahan ](http://dancallahan.info)

Engineer with Mozilla Developer Relations, former Mozilla Persona developer.

## 5 comments

Samat JainSeptember 12th, 2017 at 20:29Ningxin HuSeptember 13th, 2017 at 08:02mohSeptember 13th, 2017 at 08:33voracitySeptember 23rd, 2017 at 19:56Dan CallahanOctober 2nd, 2017 at 11:39