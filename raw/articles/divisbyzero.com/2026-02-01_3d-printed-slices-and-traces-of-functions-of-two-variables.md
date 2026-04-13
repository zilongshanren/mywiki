---
title: 3D-Printed Slices and Traces of Functions of Two Variables
url: https://divisbyzero.com/2026/02/01/3d-printed-slices-and-traces-of-functions-of-two-variables/
author: Dave Richeson
published: '2026-02-01'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

I have been using [OpenSCAD](https://openscad.org) to generate mathematical objects for 3D printing. Many months ago, I tried using ChatGPT as a coding assistant for OpenSCAD. It was pretty terrible. There was a lot of hallucinating regarding what code OpenSCAD would accept. Recently, I thought I’d try again. It is much better now!

I’m teaching Multivariable Calculus this semester. In that class, we look at surfaces and graphs of functions of two variables. We talk about things like traces and level curves for these objects. I decided I wanted to try 3D printing them.

My approach was to use VS Code for typing the OpenSCAD code. I didn’t know if this would work, but it worked very well. I had the file open in OpenSCAD; when I made an edit in VS Code, it automatically updated in OpenSCAD. Perfect. Then, I used GitHub Copilot in the sidebar as a coding assistant. It was hugely helpful.

Below are some examples of the objects I created. All the OpenSCAD code is available on my [GitHub page](https://github.com/divisbyzero/MV-Calc-Slices-OpenSCAD). The code can generate

- The complete solid
- Traces for x=constant, y=constant, and z=constant with supporting structures so they stay together.
- One slice at a time, with slots in them, and a stand with slots in them, so they can be assembled and disassembled.

There are a variety of parameters you can tinker with to get the design exactly the way you want it. These objects printed very well, with the exception of the z=constant traces. Because the traces are horizontal, I had to turn the object 90°. But the slicer still had to add substantial support to get the object to print. They did print, but the edges where the supports were attached were a little ragged.

![](../../assets/6fcedc82cdabe564.jpeg)


![](../../assets/6fcedc82cdabe564.jpeg)

![](../../assets/1d623e072aad9038.jpeg)


![](../../assets/1d623e072aad9038.jpeg)

![](../../assets/400b00f20959f442.jpeg)


![](../../assets/400b00f20959f442.jpeg)

These are beautiful, Dave!Sent from my iPad