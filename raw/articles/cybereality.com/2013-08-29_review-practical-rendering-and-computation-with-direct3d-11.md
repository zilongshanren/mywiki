---
title: 'Review: Practical Rendering and Computation with Direct3D 11'
url: https://cybereality.com/review-practical-rendering-and-computation-with-direct3d-11/
author: Cybereality
published: '2013-08-29'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

![Practical Rendering](../../assets/44e45ec9b8c042dd.jpg)


I was thoroughly impressed by Practical Rendering and Computation with Direct3D 11 by Jason Zink. Microsoft’s Direct3D API is certainly not for beginners, and neither is this book. But, at the same time, the author does a great job of explaining the material in a way that is approachable. The book assumes you are already comfortable with C++, and doesn’t hold your hand with the syntax. This is great, since you really should have an understanding of C++ before jumping into 3D graphics programming. It’s also not the kind of book that expects you to type in long pages of example code into your computer. In fact, there are not really any complete examples listed in the book at all. Instead the author chooses to highlight specific API calls and explain how different techniques can be implemented using the GPU.

This is in stark contrast to the last DirectX 11 book I read by Frank Luna. Luna’s text was great, don’t get me wrong. But it was very focused on producing functional demos to showcase certain effects (like shadow mapping or ambient occlusion). Instead Zink chooses to go totally knee-deep into the API itself and, as a reader, I came away much more confident that I understood the material. Just as an example, early on in the book there is a 100 page chapter just on resources. Most other tutorials would briefly show how to create a buffer, and then move on other stuff. Not here. In fact, the next 200 pages of the book is just about how the pipeline works. It’s really great, and rare to find such insight.

Don’t be fooled, there is certainly code in these pages, and there are a few examples. The book covers some topics like deferred rendering, multi-threaded graphics, dynamic tessellation, and physics. What I liked about the examples is that only the bare minimum amount of code was shown. Just enough to understand the key concepts without getting bogged down with boiler-plate code. It also made reading along much nicer, without having to feel like you need to get up every 5 minutes and type something in on a PC. Plus, the source code for the examples, and the author’s engine, are available for free online. So no need to type either way.

One thing I really enjoyed was the discussion on DirectCompute and on compute shaders. There are hardly any books covering DirectCompute, so it’s great to see so much space dedicated to the API. I am very interested in using this in my own engine, though it’s difficult to find information on the topic. Practical Rendering and Computation includes several chapters using compute shaders, for example to do image processing (blur). There was also a good amount of space given for tessellation. So if you are at all interested in these specific topics, it’s pretty much a no-brainer to get this book.

One other thing. Mad props to Jason Zink for being available to the community. You’ll find him on the gamedev.net forums, even helping out newbies with their 3D questions. Much respect.

All-in-all, this was quite an eye-opening read. I mean, after reading the Luna book and doing some online tutorials, I thought I knew about DirectX 11. Well, I knew something. But this book went much further than what I had previously seen on the topic. I would even recommend reading this *before* Frank Luna’s book, as I think that would flow a little better. Get the foundation solid, and then start learning how to code specific effects. Anyway, this book comes highly recommended by me if you are attempting to learn Direct3D.