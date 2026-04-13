---
title: Execution Unit
url: https://www.executionunit.com/index5.html
published: '2014-03-21'
source_blog: Blog | Execution Unit
source_site: http://www.executionunit.com/blog/
category: game programming
fetched: '2026-04-13'
---

I’m currently writing an editor for our next game. We’ve used many tool in the past ([Blender](http://www.blender.org), [Tiled](http://www.mapeditor.org) & [Mappy](http://tilemap.co.uk/mappy.php)) to make games but we thought it was really time to invest in our own code base. This was heavily influenced by the great experience we had using [Unity3D …](https://unity3d.com)

I evaluated [Unity3D](http://unity3d.com) for a few months before deciding NOT to use it. It’s a really, really great tool and it was a tough decision. Ultimately I felt like there was more resitance to steady progress using Unity3D over extending/upgrading my own code. Here is a rough guide …

*If you want to cut to the chase you can download the code here*.

**This isn’t a very well written blog post, it’s more of a dump of my thoughts as I tested out LuaBridge and didn’t get to trying out OOLua**.

Once again I am starting …

After working with Qt5.x for a few months and really starting to enjoy the flexibility of `qmake`

and `QtCreator`

I decided to try using [CMake](http://www.cmake.oth) to build `XCode`

and `MSVC`

proejcts.

After turning on `C++11`

a few weeks ago I found that `QtCreator`

debugging became more difficult as …

When you load a vertex and fragment shader in OpenGL you need to pass in data such as the current viewport transform, camera transform and lighting data. You do this via `Uniform`

variables.

Each of these Uniforms is addressed via a location which in true OpenGL style is a `GLuint …`


I’ve been playing with building an App using [qmake](http://qt-project.org/doc/qt-5/qmake-manual.html) as the build system. I started with a simple QT App built using the wizard in QTCreator and tweaking it.

I ran in to the problem that I needed to copy the [SFML](http://www.sfml-dev.org) [frameworks](http://en.wikipedia.org/wiki/Software_framework) in to the App Bundle. The …

## Why pack textures/images?

If you’re making a game then it’s more efficient to tell the hardware:

1 2 3 4 |
|

than to

1 2 3 … |

I’ve been looking for a new home server for a few months. Recently (the last six years) have been running EPIA [Mini-itx](http://en.wikipedia.org/wiki/Mini-ITX) motherboards in [Cubid](http://www.mini-itx.com/reviews/2688R/) cases. They are basically silent and powerful enough to run a small fileserver and webserver.

My EPIA boards were starting to show their age …

Many years ago I bought a [Current Cost](http://www.currentcost.com) meter. Infact it was so long ago now that they have called my version [The Classic](http://www.currentcost.com/product-theclassic.html). I wanted to see how much electrical energy all my servers, home computers and gadgets were using.

The Current Cost package contains two main parts, a …

In order to build the assets for my games I have a series of python scripts that know how to take files TexturePacker, Tiled, and Blender and build them for use within the engine. My main platform is OS X and it has good terminal support and more importantly I …