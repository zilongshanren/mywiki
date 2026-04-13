---
title: Procedural Rendering on PS2
url: https://basesandframes.wordpress.com/2016/07/25/procedural-rendering-on-ps2/
author: Robingreen
published: '2016-07-25'
source_blog: Bases and Frames
source_site: https://basesandframes.wordpress.com
category: graphics
fetched: '2026-04-13'
---

While working at SCEA R&D I was asked to make a presentation for GDC 2001 showing some of the internals of PS2 and highlighting the new command line tools we had made for compiling VU programs and dumping DMA chains.

I needed something graphically compelling yet simple to generate to show off the power of procedural generation to potentially drawing more per frame than you can fit into PS2’s limited memory, but I am allergic to procedural landscapes or yet another massive particle systems so instead I took inspiration from William Latham’s “Lifeforms”:

![home](../../assets/e32bde8515ccd3c2.jpg)


The Lifeforms were a series of procedurally generated shapes that came out of his work at the IBM UK Research Center. The ideas behind the generation of forms was described in a strange mixture of intense detail and disinterested handwavyness in the 1992 book “[Evolutionary Art and Computers](https://www.amazon.com/Evolutionary-Art-Computers-Stephen-Todd/dp/012437185X)” by mathematician Stephen Todd and William Latham. There was a short video, an exhibition of large scale Cibachrome prints and the book. Latham talks about the history in his TED talk:

My GDC 2001 presentation and accompanying document were in two sections – the first describing how to generate the forms and the second about efficiently implementing them on PS2 using the new tools. It’s a little contrived and not as efficient as it could be, but the point of demo code is to highlight the concepts as clearly as possible. The code to interpolate along a rotation got me looking into how to code exponential and power functions on the VUs, which had no good math libraries for transcendentals. This led directly to the Faster Math Functions presentations the following year.

![lifeforms001](../../assets/1c511c1202141c0b.png)


During the presentation I had to make a disclaimer that, when playing with randomly generated organic shapes, they can very occasionally bring up forms that may appear a little too reproductive for family viewing and that I apologize in advance. It also turns out that when you can generate art 60 times a second instead of the days of laborious rendering using late 1990’s hardware that it took Latham and Todd, it ceases to be art.