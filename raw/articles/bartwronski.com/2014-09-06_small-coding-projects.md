---
title: Small coding projects
url: https://bartwronski.com/personal-projects/
published: '2014-09-06'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

Some of my personal, spare-time open-source projects:

## Blue Noise Generator

This is my attempt of an implementation of a Siggraph 2016 paper “Blue-noise Dithered Sampling” by Iliyan Georgiev and Marcos Fajardo from Solid Angle. You can find the link to the paper abstract here: [https://www.solidangle.com/research/dither_abstract.pdf](https://www.solidangle.com/research/dither_abstract.pdf)

I wrote about motivation behind it in WIP [mini blog post series](https://bartwronski.com/2016/10/30/dithering-in-games-mini-series/).

## CSharpRenderer

![csharprenderer](../../assets/21b889e90b5b56b4.jpg)


Despite its completely not catchy name (sorry, I was never good with those) this is my personal fav for any rendering related work. Quick and dirty DirectX 11 graphics playground / framework. It allows super-fast iteration times on prototyping some new graphics features. Has hot-loading of shaders, UI, constants, reflection system and scripting and turns DX11 prototyping into something painless and really pleasant. If you are tired of tons of DX11 glue code and long C++ compilation / linking times, ugly syntax and low productivity – check it out! 🙂

I’m slowly adding new features to it and building a good code base for prototyping more sophisticated algorithms.

## Poisson Sampling Generator

![poisson](../../assets/3ea395c83c6b0392.jpg)


Very simple Python code supposed to aid generating various sampling patterns (1D, 2D, 3D, various shapes and options for repetition / rotation) specifically for rendering. It outputs C++ and HLSL code, features generated pattern visualization and a simple GUI.

Note that the link for CSharpRenderer has a small error in the link, a remaining space at the end. BTW very interesting project.

Fixed it – thanks a lot for letting me know! I’m glad that you find it interesting, hope it will be useful in any way. 🙂