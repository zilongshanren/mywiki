---
title: 'Book: 3D Engine Design for Virtual Globes'
url: https://outerra.blogspot.com/2011/07/book-3d-engine-design-for-virtual.html
author: Outerra
published: '2011-07-03'
source_blog: Outerra
source_site: https://outerra.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[3D Engine Design for Virtual Globes](http://www.virtualglobebook.com/)is a

[book](http://www.amazon.com/3D-Engine-Design-Virtual-Globes/dp/1568817118?ie=UTF8&tag=virtua06a-20&link_code=btl&camp=213689&creative=392969)by Patrick Cozzi and Kevin Ring describing the essential techniques and algorithms used for the design of planetary scale 3D engines. It's interesting to note that even though virtual globes gained the popularity a long time ago with software like Google Earth or NASA World Wind, there wasn't any book dealing with this topic until now.

![](../../assets/4de75646a487afd7.png)


![](../../assets/4de75646a487afd7.png)

As the topic of the book is relevant also for planetary engines like Outerra, I would like to do a short review here.

I have been initially contacted by Patrick to review the chapter about the depth precision, and later he also asked for a permission to include some images from Outerra there. You can check out the sample chapters, for example the

[Level of Detail](http://www.virtualglobebook.com/3DEngineDesignForVirtualGlobesSection121.pdf).

Behind the simple title you'll find almost surprisingly in-depth analysis of techniques essential for the design of virtual globe and planetary-scale 3D engines. After the intro, the book starts with the fundamentals: the basic math apparatus, and the basic building blocks of a modern, hardware friendly 3D renderer. The fundamentals conclude with a chapter about globe rendering, on the ways of tesselating the globe in order to be able to feed it to the renderer, together with appropriate globe texturing and lighting.

Part II of the book guides you to the area that you cannot afford to neglect if you don't want to hit the wall further along in your design - precision. Regardless of what spatial units you are using, it's the range of detail expressible in floating point values supported by 3D hardware that is limiting you. If you want to achieve both global view on a planet from space, and a ground-level view on it's surface, without handling the precision you'll get jitter as you zoom in and it soon becomes unusable. The book introduces several approaches used to solve these vertex precision issues, each possibly suited for different areas.

Another precision issue that affects the rendering of large areas is the precision of depth buffer. Because of an old non-ideal hardware design that reuses values from perspective division also for the depth values it writes, depth buffer issues show up even in games with larger outdoor levels. In planetary engines that also want a human scale detail this problem grows beyond the bounds. The chapter on depth buffer precision compares several algorithms that more or less solve this problem, including the algorithm we use in Outerra -

[logarithmic depth buffer](http://outerra.blogspot.com/2009/08/logarithmic-z-buffer.html). Who knows, maybe one day we'll get a direct hardware support for it, as per

[Thatcher Ulrich's suggestion](http://tulrich.com/geekstuff/log_depth_buffer.txt), and it becomes a thing of the past.

Third part of the book concerns with the rendering of vector data in virtual globes, used to render things like country boundaries or rivers, or polygon overlays to highlight areas of interest. It also deals with the rendering of billboards (marks) on terrain, and rendering of text labels on virtual globes.

The last chapter in this part,

*Exploiting Parallelism in Resource Preparation*, deals with an important issue popping up in virtual globes: utilizing parallelism in the management of content and resources. Being able to load data on the background, not interfering with the main rendering is one of the crucial requirements here.

The last part of the book talks about the rendering of massive terrains in hardware friendly manner: about the representation of terrain, preprocessing, level of detail. Two major rendering approaches have their dedicated chapters in the book: geometry clipmapping and chunked LOD, together with a comparison. Of course, the book also comes with a comprehensive list of external resources in each chapter.

We've received many questions from several people that wanted to know how we started programming our engine and what problems we have encountered, or how did we solve this or that. Many of them I can now direct to this book, which really covers the essential stuff one needs to know here.

## No comments:

Post a Comment