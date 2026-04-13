---
title: Introduction to VIDE
url: http://david.fancyfishgames.com/2012/07/introduction-to-vide.html
author: Legend
published: '2012-07-24'
source_blog: The Legend of GameDev
source_site: http://david.fancyfishgames.com/
category: graphics
fetched: '2026-04-13'
---

Right now, in addition to a few small flash game projects, I'm working on VIDE, which stands for Vectorized Image Deformation Engine. The goal of VIDE is to take images and to deform (bend) them to create animations. The project came about because we were tired having to work around flash's limitations, and there didn't seem to be any animation engine that really suited our needs. Already, we have many games that we plan to use VIDE for. VIDE is being written in Haxe NME, which is a cross-platform language which can compile the code to native PC, Mac or Linux executables, as well as flash swfs to run demos online. It can also compile to mobile devices like iOS, Andriod, and Blackberry. Support for other platforms may come in time, and it wouldn't be that hard for me to add platforms myself as desired (for example, Haxe can compile to C#, which with a little extra code I could make an XNA (XBox) project that runs VIDE).

Right now, I already have the basic functionality for VIDE done. None of the technology behind VIDE is new, in fact a lot of this has been done in 3D games for many years. However, these tools haven't been used a lot in 2D, especially not with deforming images. Below, I will explain how VIDE works.

**Vectorizing an Image**

The first step is to take an image, and break it up into triangles. Each triangle vertex will be assigned a uv coord to map the vertex to the image. This makes it trivial (and very hardware friendly) to simply move the vertex positions and allow the uv interpolation to deform the image. The way I generate triangles from an image is to use marching squares on a threshold of the alpha channel to generate the contour, and then triangulate the contour. As all good programmers know, never reinvent the wheel if you don't have to - and it turns out that there are many free open source libraries that do this. I used Nape, as I had used it before for physics in games and was familiar with it. Nape even has a demo called "BodyFromGraphic" which shows how to use their marching squares implementation on an image:

[http://deltaluca.me.uk/docnew/swf/BodyFromGraphic.html](http://deltaluca.me.uk/docnew/swf/BodyFromGraphic.html). The returned GeomPoly shape then has a triangular decomposition function, so it was almost no work using Nape to get a vectorized version of an image.
![]() |

To render the vectorized image, the next step is to generate uv coordinates which map the vertices into the image. For 3D models, this can be quite difficult, but for our 2D image, all we have to do is take the original position of the vertex as the uv coordinates, as it already maps perfectly on top of the image. For maximal graphics hardware performance, I also generated an index buffer which allowed me to remove all duplicate vertices (which there are many since triangles often share vertices in a connected vector graphic) and just index which unique vertices each triangle used. Now we can use nme's drawTriangles function, which takes the vertices, the index buffer, the uv coords, and an optional culling argument. Since we don't want to cull any triangles (we want to display them all), we can just set the culling to NONE. For those of you who were wondering why VIDE doesn't work in HTML5, that's because the nme drawTriangles function doesn't work in HTML5 at this time. Here is the code to render the vectorized image:



`//begin the bitmap fill to show the image`

`graphics.beginBitmapFill(bitmap,null,false,true); `

`//draw the triangles`

graphics.drawTriangles(vertices, idx, uv, TriangleCulling.NONE);

//end the bitmap fill

`graphics.endFill();`

Setting the BitmapFill's smooth flag to true will make sure that we don't get any artifacts when we deform the image. At this point, we can manually move a vertex position in vertices and see the image deform. Awesome!

![]() |

Programmers make every other major feel so stupid! Just sayin...

ReplyDelete