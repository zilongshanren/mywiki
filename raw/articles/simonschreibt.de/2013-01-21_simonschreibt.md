---
title: Simonschreibt.
url: https://simonschreibt.de/gat/cell-shading/
author: Simon
published: '2013-01-21'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

Making a simple comic look (outlines around objects) is pretty easy. If you know how! Some years ago at the Games Academy, a team was building a comic adventure ([Tummy Trundle](http://www.games-academy.de/games/games-projekte.html)) and investigated how to do a comic look in real time. [Falk](http://www.fa-so.de/) was presenting the solution: grab the 3D model, copy it, invert its normals, add a black material to the copied object and then push the faces outwards along their normals. The result looks like that:

![](../../assets/2b1d75c45d063ab7.gif)


At the end there simply lays one bigger black turtle over the original one. But since the normals of the black turtle are inverted you only see their overlapping parts.

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

[Nicolae Berbece](https://twitter.com/xelubest)just whispered an awesome trick to me: It’s about how to create outlines for a 2D sprite. His idea was to “just” copy the sprite 8 times, colorize and shift them into the 8 directions of the wind:

You might think that up-scaling **one** sprite would be enough. At the first look this seems suitable but you’ll notice several problem areas:

Of course drawing 8 sprites costs more performance but that’s totally fine if you only have small amount of areas where this is necessary. Also you get some great advantages out of this technique!

![](../../assets/f9965add3c1fd470.png)

While a “perfect” outline might look a bit boring (demonstrated via Photoshop-Outline) the little trick creates a really nice silhouette for the hair:

Also it works perfect with soft-alpha (see the smooth transitions at his wrists):

![](../../assets/5c094faa8a976d15.png)


And my favorite (and of course the most important feature): Simple dots morph to small flowers!

![](../../assets/3ad3ccb15dbe8854.png)


I hope you guys like this small trick and thanks to Nicolae for sharing it with us! :,)

![](../../assets/ba0680151067ebbc.png)

Ok, but is it better than just adding sobel edge post processing?

Yes,it’s better than Edge Detect,because it’s has no aliasing,and you can arbitrarily scale them.

Yes but of course the workload for the artist is higher and if you want to change the effect in general you have to re-export all your assets. A post FX is more comfortable in this regard. :D

This is rarely necessary with modern day game engines as they are probably more efficiently processed using vertex shaders rather than doubling the triangle count.

A similar technique is still used with older game engines such as certain maps created for Quake III Arena. Rather than duplicate each polygon, the compiler Q3Map2 offsets each surface and applies a black texture to each backface creating the illusion of inked edges.

Documentation:

http://q3map2.robotrenegade.com/docs/shader_manual/cel-shading.html

Example image:

http://webpages.charter.net/phobos/images/cel_screenshot.jpg

Other similar examples:

http://www.blog.radiator.debacle.us/2010/07/geocomp2-demon-pigs-go-hog-wild-by.html

Thanks for the comments guys :) Obsidian is right, i also don’t believe that this tech is necessary in modern games. But i love this approach because it shows the trick in a good way and hey, maybe some guy has an engine which doesn’t have cool shaders and can do this workaround to achieve an comic look :)

I find the geometric approach can still have qualitative differences from a screen space outline – enough that you’d consider using one over the other. With screen space approaches, you get a uniform pixel line. With a world space geometry shift, the line gets thicker as you get closer to it. You can, of course, do some clever stuff in shaders to blend between. Also, the sobel approach is really super generic, and looks robotic in its implementation, whereas using vertex data starts to give you way more artisanal control over line quality – control width, colour etc. across different sections of a mesh at a vertex or even texel level.

But yes, this can completely be done with a vertex shader, rather than burning it into your model data.

The thing to watch out for with the vertex shader approach is that you always need smooth normals to pull off the effect – if you have a flat shaded normals, the “shell” that you create will have open (non manifold) edges all over the place, meaning that when you move the vertices along the normals, the normals aren’t shared between verts, so they diverge/converge. Basically, your shell becomes a mess.

In essence, you DO want a copy of whatever you’re using but without doing the “move along normals” step (let the vertex shader do this trivial step). This does mean you’re kinda doubling up data, but that data can then be interpreted in fun different ways by the shader (use vertex color luminescence for line width, alpha for vertex transparency, or build the UVs like a flow map so that you can “Grow in” your silhouettes).

You mention some really good points here. Especially that you have thicker near lines and thinner far lines is great from an composition standpoint. That the data will exist twice is true…but as far as i understood it’s not too bad because there’s no heavy material needed for the outline and i think render polygons isn’t the big problem for the hardware. Correct me if i’m wrong :D Oh nice point with the shading – that’s something i didn’t think about.

Thanks for the comment!

Having experimented with this in the past, there is a neat trick to get around the ‘non-manifold’ problem; bake the ‘smooth’ normals into the vertex colours and then push out along those instead (with the alpha channel controlling push distance for thick/thin edges). Obviously this means you can’t use the vertex colours for anything else though.

There’s no need to ‘invert the normals’ either; just render with front-face culling instead and you’ll get the same result for one less operation.

The one unavoidable downside is in inside edges; this technique handles outlines fairly well but internal details are likely to be skipped over or just plain look bad.

What do you think about the “edging” in Borderlands 2? I think they did a really good job. Looks great, maybe i’ll do a small article about this later. If you don’t mind, i could send you some questions ;) ’cause i can’t explain myself how Borderlands did it.

It was! It definitely wasn’t this method though; there’s a number of ways of doing it (used in most 3d modellers too for edge selection etc; see also the ‘sketch’ rendering modes in Sketchup for example) especially if you have direct access to the graphics pipeline – for example, with an in-house engine rather than Unity / UDK.

There’s a paper named “Stylized Rendering Techniques For Scalable Real-Time 3D Animation” by Lake A. et al you can find around the interwebs that discusses most of the cell-shading / edge detection techniques around – there’s a copy of it here at the moment.

Key points involve building an edgelist of… well, edges, in a given mesh, finding silhouette and ‘crease’ edges and then drawing them; it’s kind of beyond what vertex and fragment shaders can traditionally do and into an involved custom/modified GPU rendering pipeline.

Non-Photorealistic Computer Graphics by Strothotte T. and Schlechtweg S. also cover it pretty in-depth.

Biggest limitation to ‘proper’ line rendering techniques is that they typically require additional mesh information (namely, on the mesh’s edges) that gets traditionally stripped out of most game mesh formats in the name of optimization, making implementing it on Unity or the UDK a major challenge without access to the source code.

I saw two intereting things in Borderlands 2 regarding the outlining.

1. The Outlines fade out. With that there are no hard cuts where lines “meet” e.g. with the ground: http://data.simonschreibt.de/share/outline_fading.jpg

2. The outlining seem to tone the whole polygon. If you look close, you’ll notice that the side-polygon (which stands in a very narrow angle to the camera) get’s black: http://www.youtube.com/watch?v=PgEPSJ3aSc4

-Sorry for the long delay!

From the looks of that, they’re probably using a Sobel Edge Detection filter on the scene normals. I er… forgot about that method (oops).

Deferred Rendering, which is pretty common these days, involves rendering all the normals in the view out to a texture. Run the Edge Detection filter on that and the depth texture and you find the sharp changes in normals, ie outlines or creases.

For a comparison on edge detection on the render result vs scene normals, compare these two: http://docs.unity3d.com/Documentation/Components/script-EdgeDetectEffect.html vs edge detection on scene normals

Thank you very much for the hints & links! Unity gets more powerful with every day :)

Guilty Gear Xrd is probaby relevant here.

Here’s a link to a technical video explaining how they achieved their amazing cell shaded look:

http://youtu.be/yhGjCzxJV3E

Thank you for the link! I already know the talk and it’s AMAZING! I love it! <3