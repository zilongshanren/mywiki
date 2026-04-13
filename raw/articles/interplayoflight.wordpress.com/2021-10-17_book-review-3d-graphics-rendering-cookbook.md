---
title: 'Book review: 3D Graphics Rendering Cookbook'
url: https://interplayoflight.wordpress.com/2021/10/17/book-review-3d-graphics-rendering/
author: Kostas Anagnostou
published: '2021-10-17'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

I was recently invited to review the new [3D Graphics Rendering Cookbook](https://www.packtpub.com/product/3d-graphics-rendering-cookbook/9781838986193) book by Sergey Kosarevsky and Viktor Latypov. The main focus of the book is the implementation of a large variety of graphics techniques using both modern OpenGL and Vulkan, an interesting approach that can show the parallels between the two graphics APIs and act as a steppingstone for less experienced programmers towards a better understanding of Vulkan.

The authors use a “cookbook” style in which each chapter is a collection of techniques, ranging from setting up a simple pipeline to render a mesh, to bindless rendering, to using per-pixel lists for order independent transparency. The book covers a good range of modern rendering techniques, it doesn’t delve too much into the theory behind each technique though, providing references for self-study, which many times is necessary to understand the implementation. To get the most out of this book it needs to be used in conjunction to running, studying and experimenting with the source code, which is provided for all chapters.

Graphics programming involves more than loading and displaying a model on screen, and a lot of the programming time is spent on loading/converting assets, setting up UIs, multithreading the application, adding support for profiling. I appreciate the fact the authors devoted quite a bit of time on assembling and discussing a good collection of libraries and frameworks to handle all that and let the reader focus on the graphics techniques.

I also like the “iterative” approach the authors follow in parts of the book, in which the simpler path to achieving the result introduced in an early chapter is revisited later to make more general and widely applicable, instead of overwhelming the reader with a complex implementation early on. This sometimes imposes a linearity in the book, some chapters make sense to be read in a specific order. The authors bring all techniques together towards the end of the book into a larger, more complete sample, that can be used as the basis for the reader to create their own rendering engine.

In general, I would recommend this book to people with some knowledge of graphics theory and techniques, wanting to get hands on with the actual implementation. The OpenGL path is lower friction and has a less steep learning curve and will help people will less experience in graphics programming, gradually transitioning to Vulkan during the second pass if they want to. People with more graphics programming experience can benefit from this book as well, especially those that have started learning Vulkan.

My only criticism of the book would be the image quality, which is pretty low in the copy I received.