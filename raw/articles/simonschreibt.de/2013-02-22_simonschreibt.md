---
title: Simonschreibt.
url: https://simonschreibt.de/gat/airborn-trees/
author: Simon
published: '2013-02-22'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

I like trees. Of course there are many ways of creating them (e.g. explained in this wiki article from polycount) but the tree of Airborn got my special attention because when I saw it the first time, I thought:

Another thing I like about trees: you have to care about the leafs, because normally the shading would make their unlit faces pretty dark. So you need some kind of “translucency”. I asked Neox and the answer is: They modified the normals. This means they used the inner “bubble” object as a base and “projected” the normal orientation of it to the leaf “cloud”. So you don’t get too dark/bright faces in the wrong place, but a very nice and soft shadow gradient all over the leafs.

Warby told me another very pleasant advantage about this technique: You avoid too many transparent planes being rendered over each other. The big blob mesh in the middle culls most of them, so you only need to care about the stuff of the front/sides.

Update 1

Megan Varde was so inspired that she made these cool trees. <3 <3 <3

Update 2

Dave mentioned another great example for trees using a similar tech:

Update 3

Emory has created a TUTORIAL about how to adjust the Normals in Blender, to achieve similar results like the Airborn tree. Should this tutorial-link be dead or offline in the future for some reason, I stored it as a picture on my server.

There is a massive amount of programming magic presented in the fresh talk “Rendering Tiny Glades With Entirely Too Much Ray Marching” by Tomasz Stachowiak, but the trees stuck out to me. Instead of having an artist place little cross-plane-meshes all around a blob-mesh, here are the faces themselves are turned into camera facing billboards!

The tree crown consists of a quadrangulated mesh, where each quad face is unwrapped individually to 0-1 in uv space. The shader remaps the uv to -1 to 1 and is then multiplied with the view matrix to transform the uvs into view space, and are then used as a vertex offset in the vertex shader, which makes each face look towards the camera.

Oh, and thank you very much Belzecue for mentioning, that Pontus actually made a full tutorial about that process! Click below!

the images don’t seam to load on this post for me, I have tried at a number of different locations with different ISPs. Could you please check to see if the images are actually accessible and if they are not fix that. Thanks

Usually this is done via Vertex Shader. Those shaders can push around vertices and move them for example with a simple sine-curve. By using vertex color, you can mask out the lower parts of the foilage to make it fix/not moving on the ground.

Hi! Any advise on how to place all the bases of 3planes into the spheres faces, just manually or there is a better way? It seems to be incredibly obvious to everyone but I can’t find any info on how to do this in Maya

By continuing to use the site, you agree to the use of cookies. more information

The cookie settings on this website are set to "allow cookies" to give you the best browsing experience possible. If you continue to use this website without changing your cookie settings or you click "Accept" below then you are consenting to this.

the images don’t seam to load on this post for me, I have tried at a number of different locations with different ISPs. Could you please check to see if the images are actually accessible and if they are not fix that. Thanks

Hm..here it’s working fine. If you want, send me an email, i’ll send you the images directly then.

Freaking brilliant with that lighting solution…

That’s right! So logic … but i never would have thought making it like that by my own.

Hey ! I adore your blog, some of those awesome tricks have recently save my ass ))

Hello Simon, any clue on how to animate the foliage for a game engine, like Unity?

Usually this is done via Vertex Shader. Those shaders can push around vertices and move them for example with a simple sine-curve. By using vertex color, you can mask out the lower parts of the foilage to make it fix/not moving on the ground.

You can google for “animate foilage” or something like that. I found this for example very quickly: https://www.youtube.com/watch?v=AYZcqOcP0B4

Hi! Any advise on how to place all the bases of 3planes into the spheres faces, just manually or there is a better way? It seems to be incredibly obvious to everyone but I can’t find any info on how to do this in Maya

Except from scripting this idea comes into my mind: https://www.youtube.com/watch?v=Pn4oZ0oUL9A

But maybe there are other procedural approaches as well…

Due to recent events with ArtStation, the last update [update 4] now goes nowhere as Roman has flushed out his artstation page.

but I managed to relocate it elsewhere

https://80.lv/articles/creating-stylized-leaves-in-maya/

As well as a copy of it he has up on gumroad

https://rdurand.gumroad.com/l/BoFGo

Thank you so much! I’ve updated the links!

Thank you for maintaining this page. It’s incredibly informative!