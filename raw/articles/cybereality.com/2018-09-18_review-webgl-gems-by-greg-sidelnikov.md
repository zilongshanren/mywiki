---
title: 'Review: WebGL Gems by Greg Sidelnikov'
url: https://cybereality.com/review-webgl-gems-by-greg-sidelnikov/
author: Cybereality
published: '2018-09-18'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

![](../../assets/557c838010d57182.jpg)

I’m a bit conflicted about this book. While there is a lot of good material here, I feel like there were many inconsistencies with the coding style and some errors or confusing explanations that deter from the gems inside. It’s also heavily geared toward complete beginners, making it somewhat of a numbing read for intermediate to advanced programmers. But I still found some reasons to like it, so please read on.

Each chapter or gem covered one focused aspect of WebGL coding. For example: creating a canvas and initializing WebGL, the graphics pipeline and shaders, some basic vector and matrix math, 3d transformations, drawing a triangle, texturing, model loading, mouse + keyboard interactions, a 3d camera, lighting, and collision detection. There is also a short chapter at the end for 2d games, but the bulk of the book is just 3d. So a decent amount of topics here, and some good fundamentals. Much appreciated too that that the author is using straight WebGL API code and not relying on 3rd party libraries.

So what is my issue here? Well, Greg Sidelnikov goes to great lengths to tell the reader that things are easy (and they may or may not be, depending on your skill level) but he could have rather displayed simple samples to illustrate the points. For instance, in the chapter on matrix math he spends about 10 pages of filler trying to sell the idea that matrices are easy, and that he doesn’t want to have long mathematical proofs in the book. However, just saying matrix math is easy doesn’t cut it. I understand the sentiment, but it just wastes time and doesn’t actually make the math easier. Later in the book he does show some examples, but he should have just removed the motivational filler and cut to the chase. I can also understand how this could be beneficial to a complete novice, but I think it does more harm than good, as at some point you actually have to have the knowledge of how things work.

My other issue is that the coding style is very inconsistent. I don’t know if this was just lack of effort or lack of understanding. For example, he shows fragment shader code like this:

gl_FragColor = color * vec4(rgb[0], rgb[1], rgb[2], 1) * texture2D(image, vec2(texture.s, texture.t));

First off, why is the rgb variable indexed like an array and the texture indexed by property? Or why not let GLSL cast these automatically? Or why create a new vec2 for texture, when texture is already a vec2? This makes no sense. The above line could be simplified into the code below, which is much more readable.

gl_FragColor = color * vec4(rgb, 1) * texture2D(image, texture);

This is just one case, but it makes me feel like the author might not have a full understanding of the code and/or copied code from various tutorials and Frankenstein’d it together. There are also less egregious problems, like inconsistent coding style, capitalization, etc. Just little things that make me question the text, like naming the shaders “smooth.vs” and “smooth.frag”. Why not use the common “vert” and “frag” extensions? Or “vs” and “fs”, if he wanted? Having two different naming conventions just looks sloppy. Or when he says an identity matrix consists of all ones, completely false information.

All that said, the book was not completely bad. One thing that was exceptional was the first chapter on 3d, he wrote a simple star-field simulation without WebGL, which was a great introduction to 3d. It’s good to understand the concepts of 3d in a simple software case before jumping into GPU programming, so this was great. Also the fact that he was using straight WebGL and not 3rd party libraries, good for learning the basics. And the WebGL API code itself was explained in a simple manner.

There were some good parts, sure, but finishing the book felt like a chore. I try to finish books that I start, and I’m sometimes surprised, but mostly my first impression is correct. The cover looked amateur, and I could tell it was self-published, but I was willing to give it a chance. While I did learn some things, I’d have to say that overall it was not great. I think especially for intermediate to advanced programmers, there is no reason to read this book. For total beginners, or maybe web developers without OpenGL knowledge, it may be useful but I’d probably still recommend starting elsewhere with a more reputable source. There are some gems here for people willing to dig, but all the little errors and inconsistencies make the final product not hold up.