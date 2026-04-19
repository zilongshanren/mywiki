---
title: '16BPP.net: Blog / Random Art in Nim'
url: https://16bpp.net/blog/post/random-art-in-nim
published: '2017-01-09'
source_blog: '16BPP.net: Blog / Page 1'
source_site: https://16bpp.net/
category: graphics
fetched: '2026-04-19'
---

Edit (Jan 30th, 2017): I written an article on how Random Art works. [You can read it here.](https://16bpp.net/page/how-random-art-works)

Have you ever heard of [Random Art](http://random-art.org/) before? If you don't know what it is, the short and skinny is that it's a program that will generate some really stunning images using a randomly generated math equation. That's what the image above was made with. The original program was written by [Andrej Bauer](http://andrej.com/). The Random Art website uses an OCaml program that been compiled to JavaScript. Unfortunately the source for that is not publicly posted (which is a shame because it makes some of the best pictures), but [a simple Python implement is available](http://math.andrej.com/2010/04/21/random-art-in-python/). Going off from that, I decided it port it over to Nim and add support for rending with OpenGL (and make a few other changes I see fit).

Well... actually I ported that to C++ (& Qt) first about a year ago, then I did another port over to C# four months later. The C# one was a little more interesting because it was a distributed rendering system leveraging cloud services and RabbitMQ; I ended up using it on a film I was working on. Pretty cool. Those... I don't really feel comfortable sharing the source to right now. But I'll give you a Nim implementation instead. : P

You can find the application [over here on GitLab](https://gitlab.com/define-private-public/random-art-Nim) ([or GitHub](https://github.com/define-private-public/random-art-Nim) if you prefer it). To compile the thing, your going to need GLFW installed as well. It can run into two modes: CPU bounding rendering and GPU (via OpenGL). There is a lot more info the in the [Readme](https://gitlab.com/define-private-public/random-art-Nim/blob/master/README.md), but here is the usage message:


Usage: ./random_art [input] [options..] input : a path to an equation file, or provide `stdin` to read input from standard input Options: -r, --renderer : cpu | opengl render on the CPU or with a GPU (using OpenGL) -s, --size : <width>x<height> the dimension of the render, must be a positive int -b, --bounds : <xMin>,<xMax>,<yMin>,<yMax> the bounds to use to render, must be a float -o, --output : <filename>.png the file to save the render as, must end with .png


If you run the application without providing an equation, it will think up one for you. Writing your own equations has this [Scheme-like](https://en.wikipedia.org/wiki/Scheme_(programming_language)) syntax. It's pretty easy to understand, but also to parse. The equation below makes the image to the right.


(mul (var y) (mod (sum (var x) (var y) ) (const 1 0.7 -0.1 0.95) ) )


I plan on working on this some more down the road. You can already see some of my changes showing up (e.g. an alpha value). I'll keep you guys posted. Once again, [the code is available here](https://gitlab.com/define-private-public/random-art-Nim) ([GitHub mirror](https://github.com/define-private-public/random-art-Nim)).