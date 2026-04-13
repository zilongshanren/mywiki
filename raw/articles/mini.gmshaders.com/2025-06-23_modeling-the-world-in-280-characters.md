---
title: Modeling the World in 280 Characters
url: https://mini.gmshaders.com/p/modeling-the-world
author: Xor
published: '2025-06-23'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Modeling the World in 280 Characters

### An exploration of the mindset, methods, and motivations behind crafting tiny, expressive shaders that combine code, art, and constraint

Hi, I’m Xor. As a graphics programmer, my job is essentially to make pixels prettier using math formulas. I work on video effects like lighting, reflections, post-processing, and more for games and animated backgrounds in software.

For fun, I like to unwind by writing compact little shader programs that fit in a “tweet” (280 characters or less). You may have seen some of these posted on X/Twitter. The process of shrinking code while maintaining its functionality is called “code golfing.”

[Here](https://x.com/XorDev/status/1727908092304617661)’s an animated galaxy I wrote in just 197 characters of GLSL code:

This little piece of code runs in real time for every pixel on the screen and generates a unique output color using some fancy math and logic. I build these demos using a tool called [Twigl.app](https://twigl.app/), an online shader editor designed for sharing mini-shaders. It makes exporting videos super easy, and in its “geekiest” mode, it also takes care of the generic header code and shortens built-in variable names.

I even managed to fit a [voxel DDA raytracer](http://x.com/XorDev/status/1505308218863632384) with edge detection into just 190 characters ([update: now 175](https://x.com/XorDev/status/1932874688260194471)):

Today, I’d like to explain why I make these, share my creation process, and show you how you can try it yourself if you’re interested. Let’s start with the “why.”

**Motivation**

Why do I write these? Well, there are several factors. Since I like lists, I’ll go ahead and present them in order of relevance:

**Curiosity and Passion**: Sometimes I get struck by a new idea and just want to play around with it. I like Twigl because it helps lower my expectations and lets me start doodling. There’s less room for overplanning, and it’s super easy to jump in.**Learning and Discovery**: Working within constraints forces me to think through problems differently. By optimizing for code size, I often find ways to simplify or approximate. It doesn’t always lead to more performant code (but often it does) and I’ve learned how to squeeze the most out of every byte. Having very little code makes it easier to experiment with formulas and variations without getting overwhelmed.**Challenge**: Writing tiny code is both challenging and stimulating. It keeps my brain sharp, and I’m constantly developing new skills. It’s basically become a game for me. I’ve accidentally learned a ton of math while trying to solve these technical problems.**Community**: I’ve connected with so many interesting people through this process—artists, designers, math folks, game devs, engineers, tech enthusiasts, and more. Sharing my work has led to some exciting encounters. (More on some notable people later!)

So, in short, it’s fun, thought-provoking, and engaging, and it’s a great way to spark interest in graphics programming. Now, what even is a shader?

**Shader Introduction**

In case you haven’t heard of shaders before, they are programs that run on the GPU (Graphics Processing Unit) instead of the CPU (Central Processing Unit). CPUs excel at complicated or branching operations, which are computed sequentially, one at a time (I’m simplifying here). GPUs are designed to process billions or trillions of predictable operations per second in parallel. This sounds like a lot, but a 4K screen at 60 frames per second outputs nearly 500M pixels per second. Each pixel could have 100s or 1,000s of operations, not to mention anything else the GPU might be used for.

There are several different types of shaders: vertex shaders, fragment shaders, compute shaders, and more, but these tweet shaders are specifically fragment shaders, also known as “pixel shaders,” because they run on every pixel. In essence, fragment shaders take the input fragment coordinates and output a color and opacity (or alpha). Fragment coordinates give you the position of the center of each pixel on screen, so (0.5, 0.5) is the bottom-left (or top-left). One pixel to the right is (1.5, 0.5), and so on to (width – 0.5, height – 0.5). The coordinates variable is called “FC” in Twigl. The output color, “o”, has 4 RGBA components: red, green, blue, and alpha, each ranging from 0.0 to 1.0.

`(1.0, 1.0, 1.0, 1.0)`

is pure white, `(0.0, 0.0, 0.0, 1.0)`

is opaque black, and `(1.0, 0.0, 0.0, 1.0)`

is pure red in the RGBA color format. From here, you can already make simple color gradients:

`o = vec4(0.0, FC.y/100.0, 0.0, 1.0)`

;

Remember, this is run on every pixel, so each pixel will have a unique Fragment Coordinate. That formula makes a simple gradient that starts black at the bottom of the screen (FC.y = 0.0), and the green output value reaches 1.0 when FC.y reaches 100.0.

So you have an output color “o”, the input fragment coordinates “FC”, and four “uniform” inputs which are shared among all pixels: “r” is the shader screen resolution in pixels, “t” is the time in seconds, and also the less commonly used mouse position “m” and the backbuffer texture “b”. And that’s the core of it! From there, it’s a lot of math and logic to control the output colors and generate cool images.

I’m going to skip ahead a bit, but if you’re interested in learning more, try [starting here](https://thebookofshaders.com/)!

# Codrops

This article was written for Codrops. Please read the rest of the [article over there](https://tympanus.net/codrops/2025/06/23/modeling-the-world-in-280-characters/), where I describe my process, code golfing, Q&A, and my story.

Thanks for reading!