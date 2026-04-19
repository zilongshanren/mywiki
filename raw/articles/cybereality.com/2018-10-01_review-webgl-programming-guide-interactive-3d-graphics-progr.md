---
title: 'Review: WebGL Programming Guide: Interactive 3D Graphics Programming with
  WebGL by Kouichi Matsuda and Rodger Lea'
url: https://cybereality.com/review-webgl-programming-guide-interactive-3d-graphics-programming-with-webgl-by-kouichi-matsuda-and-rodger-lea/
author: Cybereality
published: '2018-10-01'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

![](../../assets/b219af9aaa9af9b3.jpg)

WebGL Programming Guide is the first WebGL book that I can fully recommend. The authors stick to straight WebGL code (no libraries like Three.js) and explain everything in full detail. Since they focus more on the API than anything else, most of the samples are simple things like colored triangles or spinning cubes, but that is fine to learn the basics. I liked how sometimes they would show things not to do, and what would happen, which helps with understanding the concepts.

In the book, which is around 500 pages long, Kouichi Matsuda and Rodger Lea cover many important topics including: WebGL initialization, drawing a point, a triangle with transformation, basic animation, color and texture, the GLSL language, cameras, lighting, and a shorter chapter at the end with techniques for fog, shadows, alpha blending, etc. Really a great roster for anyone looking to learn WebGL. Much appreciated are some of the tricks they show, like how to pick 3d objects with the mouse, or how to render off-screen objects to a texture, useful for shadowing or other effects. There is even a chapter detailing how to write an OBJ model importer, perfect for someone not wanting to rely on 3rd party libraries.

I especially liked how detailed the book can become, for example when explaining the differences between right and left-handed coordinate systems. Something that can be confusing to 3d novices but the authors here did a great job. They also use beginner friendly terminology for certain things, like calling depth buffering “hidden surface removal”, which was odd at first until I remembered someone new to 3d may not understand what a depth buffer is without prior knowledge. In the book, many parts of the API are listed out in charts, such as the built-in functions/variables for GLSL, function signatures for the GL context (which explan the errors you may get and return values, etc.). A very competent look at the API.

The book was well written and I did not see any obvious errors (though I did not attempt to run any of the code). Thankfully, they make the code available on the book’s website for anyone wishing to run it themselves and pick it apart. It’s honestly hard to find fault with the text. This is a great look into WebGL and a key point in your journey as a WebGL programmer. Not to be missed.