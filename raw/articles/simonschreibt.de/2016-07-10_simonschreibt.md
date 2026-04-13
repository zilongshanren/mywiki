---
title: Simonschreibt.
url: https://simonschreibt.de/gat/pintable/
author: Simon
published: '2016-07-10'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

![](../../assets/b772307f30de3ca7.png)


![](../../assets/b772307f30de3ca7.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

“The Joy of VFX” is thought as a happy place where several VFX artists come together and try to mimic awesome effects seen for example in movies. The goal is look at the different approaches and learn of their pros and cons.

The idea comes from [Zoltan](http://www.zoltane.com) and [Attila](https://twitter.com/ATTILAM) and these nice guys proposed to put it on my blog since it’s similar to what I do. We hope you like it. Further “Joys” might be published on a separate blog.

The Pin table

The first effect we try to interpret is the pin table from an X-Men Movie:

[Lee Griggs](http://www.leegriggs.com/335056/3779154/home/xgen-rendered-with-arnold-for-maya) renders were as well a great inspiration:

Since we all used the same basic principle, here’s a short description about the **basic concept** and later every single approach is explained in detail.

![](../../assets/1a17bcad3ed15a25.png)


I didn’t have a good idea where to start so Zoltan stated that the basic idea is to take a cube and make it move via vertex shader. In this example a simple up-down-movement (sine curve) is applied to the vertices (via vertex shader, **not** via object animation):

**whole**cube to move – only the

**top**should be animated. This can be achieved by setting the

**vertex color**of the bottom-vertices to black and the top-vertices to white. The shader multiplies the vertex color with the values for the up-down-movement and since a black color value is zero this nullifies the vertex-movement:

For the example above you can see the vertex color visualized directly on the cube for better understanding.

![](../../assets/a21303ce36bba790.png)

The brighter the pixels, the more it moves the vertices of the cube upwards. The cube has its UVs mapped from top so that the height-map is basically projected onto the cube from above. When we move the texture **along** the cube (UV animation) the vertices start moving:

Vertex color and height-map are visualized as diffuse color so that you can see the relationship between brightness and upward-movement.

But we want to make sure that all vertices of the cube move about the same amount to have a straight “roof”. To achieve this we have to map all the vertices to the **same UV coordinate**. This will make sure that all vertices receive the same height-information:

This looks well, right? Now we can create more of these cubes (I did this in 3Ds Max) and combine them into a single mesh. But without changing the UVs (which are still all on the exact same spot) all of our happy cubes will move in the same manner:

By distributing the UVs like in the example below you achieve that every cube samples a different position of the height-map:

![](../../assets/30f25e3b20be78f4.png)


![](../../assets/a268238e986c52b4.png)


My approach is pretty much the same like what was explained above but I used a different geometry.

![](../../assets/5b971eb75798dcb9.png)

Instead of a cube I used a pyramid where only the central vertex is moved up and down.

This is how my happy spikes look like. I tried to mimic the Liberty Island (like seen in the X-Men Movie).

I stumbled over an interesting problem. Using a 3D software I’m used to that the face-normals get updated when I change the **orientation** of a surface. This is **not** the case when a vertex shader changes something on your mesh! The normals don’t care and you have to manually re-calculate the normals. Here’s an example:

If you don’t update the normals you get incorrect shading like in the example below:

![](../../assets/9b0b24e9aba9fba2.png)


Here’s how it works in Unreal. Pretty simple. :)

![](../../assets/e4aef20c90550c18.png)


But how does it work?! What kind of magic creates a fresh pixel-normal out of nothing?

The secret is: comparison. You take the position of the pixel you want the normal for and look at its **neighbor-pixel** how different their position is in the 3D space. Luckily the graphic card always handles 4 pixels (2×2) at the same time so comparing neighbors is very effective.

Below is a visualization how this works when you create a normal-map out of a height-map (instead of the world-position like in my Unreal-Shader). You use the difference between the neighbor-pixels to create two vectors. Now you can can calculate a new vector which stands 90° on the two others: voilà! We’ve just calculated the pixel-normal!

My solution creates many thin triangles which is kind of a worst-case. You get many ugly edges (if there’s no anti-aliasing) and GPUs don’t like thing triangles which I described here in my [Render Hell Article](https://simonschreibt.de/gat/renderhell-book3/#update2-newproblems).

Now it’s Zoltan’s turn!

![](../../assets/44a961b111390f84.png)


Zoltan’s [current Unreal Engine 4 project](http://www.zoltane.com/pages/unreal/drone-alone/) is a game set in a retro futuristic 80’s house where he puts the pin table in the garden. It is meant to display different things from a fake pond through a chess board to a hedge maze mini-game.

Before we dive into details, this is the final result:

Now let’s talk about how it was made.

![](../../assets/5b971eb75798dcb9.png)

In comparison to the basic approach (explained above) Zoltan wanted to use **6-sided columns** as pins instead of cubes.

He started by creating a plane made up of hexagons in [the Foundry’s Modo](https://www.thefoundry.co.uk/products/modo/). He ended up with ~89K polygons for ~15K hexagons, arranged as a disc. Each hexagon consists of 6 equilateral triangles to keep the structure nice and symmetric after tessellation (more about this will be explained later):

![](../../assets/57ed731aa7a2fa7c.png)


The mesh has **two** UV sets. The first one is planar projected covering the entire mesh but has each hexagon shrunk down into a single point:

![](../../assets/fa7b6b57317d005b.png)


This makes sure that each hexagon gets a single, uniform texture coordinate, producing a nice mosaic effect:

![](../../assets/bd9e595665e16ae2.png)


The 2nd UV set has the hexagons undistorted and on top of each other in the middle of the UV space:

![](../../assets/0e81744a05c2d11c.png)


**Problem**: All hexagons are one mesh and connected to each other so they **can’t** move up and down individually yet. While [Simon’s cubes](https://simonschreibt.de#simonResult) where separated from the beginning Zoltan uses a slightly different way to solve this: With **tessellation**.

![](../../assets/25782725bced9e3b.png)

He tessellates the hexagons to create a gap between the cells. The big advantage is that all the new polygons are created on the fly on the graphic card which reduces storage on the disk and transport-cost from disk to graphic card when my model is loaded.

![](../../assets/c8b15a59bdc3a8b5.png)


**Important**: Note that the tessellation-algorithm is kind of special. It’s more comparable with beveling/chamfering the edges (**left**) instead of just dividing the polygons in its half (**right**).

The original outlines of each cell should not be displaced at all, only the newly created inset supposed to rise. We’ll do this with a mask which is explained below.

Raising the inset means that the columns do not have perfectly vertical sides:

But since they’re pushed a lot the walls are **close enough** to vertical so this trick is not apparent.

![](../../assets/f2523294b353074b.png)

Now we’ve to tell the engine that **only** the **inset areas** are allowed to be moved. Instead of applying vertex color like in the [basic approach](https://simonschreibt.de#basicVertexColor) he creates and uses a gray scale mask for that. This mask will be created by the shader – **not** by hand!

Below is the goal. The mask tells some edges to stay and allows others to move:

First we need a hexagonal gradient as a base:

![](../../assets/439478bd22aa6cec.png)

Looks complicated at first to create something like this in real-time but it’s easier if you make in 3 steps:

(For Unreal users: He used three instances of a material function which produces the following figure from an input UV and a rotation angle):

If you want to know how exactly this works, here’s the Unreal shader network (click to see in full size):

![](../../assets/9e2433fbb4c37729.png)


![](../../assets/9e2433fbb4c37729.png)

Unfortunately the gradient is full of gray values where we want to have more or less a black/white mask. To fix this we can adjust the levels like shown here:

Perfect! This is how our result looks like:

![](../../assets/00c87dcb92a81ea9.png)


And here again the zoomed version where you can see which edges are masked out:

Finally we can push the columns upward properly! But for doing that something or someone has to tell them how much to raise. The basic approach used [hand-made textures](https://simonschreibt.de#basicHeightMap) but here it gets a bit more advanced.

![](../../assets/b2a9850e8df39a6f.png)

We must input some information into the pin table. Therefore this small scene is **hidden** in the level:

![](../../assets/9b73b83731be024a.png)


Zoltan captures this scene from above (like a camera but in Unreal this is called “scene capture 2D”) and store the results into two textures (scene capture target), one for color and one for height. The pin table will use this data later.

These are the captured textures for the maze. To show for example the pond, the “camera” can be moved 1m to the right:

![](../../assets/b0e3bf3b63fde925.png)


**Small hack**: Unreal lacks

**orthogonal**render-to-texture cameras so he had to put the scene capture actors roughly 100m from the target surfaces and set the field of view to 1 degree to decrease the perspective distortion.

Instead of accessing the depth buffer of the captured scene and use this as displacement data for the pin table, he uses the world position of the pixels as height information. In addition the geometries can have gray scale textures applied which are also interpreted which is a huge plus in comparison with a standard depth buffer which doesn’t care about textures at all.

Here you can see the resulting height-information (in this example **not** seen from the top for better visualization):

![](../../assets/44257784902b6c86.png)


![](../../assets/8930f2c0d25c0d4f.png)

Like in my spiky-example, Zoltan had to re-generate the normals for the newly deformed geometry but used a different approach. Here you can see how it would look if you **don’t** do anything:

![](../../assets/a02b66a00410a6d7.png)


He applied new normal vectors pointing into the direction of the faces. For better visualization here you can see the vectors represented with colors:

![](../../assets/52a1cdf79ce91dc2.png)

This was done in similar fashion like we created the hexagonal gray scale mask. Triangle after triangle was taken and hardwired world normals assigned to each of them. [Here](https://data.simonschreibt.de/gat063/z_normals_01_graph.png) you can see how he assigns the values.

For those who wonder about the colors: vector coordinates like for example **[1,0,0]** (XYZ, vector points to the right) can be interpreted as RGB values. If you translate the max. vector value (1) to a max. color value (255) you’ll end up with colors like shown in the picture. For example [255,0,0] (vector pointing right) or [0,255,0] (vector pointing down).

**Note**: If you want a vector pointing to the left or up you have to use negative values like **[-1,0,0]** and since we can’t represent negative colors you’ll end up with black.

The problem is that the new generated normals cover the whole area making it look like a six-sided pyramid:

![](../../assets/2ca47a23720896ac.png)


We need to apply upward facing normals to the “roof” of the column. We can do this by using our hexagonal gradient from before …

![](../../assets/00c87dcb92a81ea9.png)


… but with slightly modified values to make the black areas wider. This masks out the sides of our inset area and makes it possible to assign an upward pointing vector to the top of the column:

The top is colored in blue because a vector of [0,0,1] correlates with [0,0,255].

Like already mentioned you can adjust the values of the mask to make it narrower or wider. If you let it overlap into the top of the column (see the wireframe) …

… then you even get a nicely beveled edge like if you would have baked a normal map for this low-poly column. Here an example with different mask widths:

![](../../assets/f38219b3548de31f.png)


![](../../assets/67e27659b94ddf64.png)


That’s it! We hope you liked this approach as well.

![](../../assets/ec64953771a6f14d.png)



But last but not least: Let’s talk about what didn’t go perfectly well.

![](../../assets/8d4c75a0b9fc22e6.png)

This solution has the downside that pre-calculated normals won’t adapt to actor rotation so if the mesh doesn’t have default orientation then the lighting is broken.

Proper lighting introduces the problem of aliasing: the mesh now has many tall, thin polygons with great differences in illumination which look really bad when the object is some distance away:

Temporal anti-aliasing helps but the mesh still looks very noisy. To work around that Zoltan set the diffuse color of the material to 0.02 and added the color as **emissive**. This decreased the effect of the lighting and limited the possible differences in brightness between the sides of each column. So while the moire effect is still there the temporal anti-aliasing has a much better chance of eliminating the artifacts because the pixels don’t vary that wildly anymore.

He chose this workaround because it also worked both artistically and from a narrative perspective. He made it look like there are colored LEDs in each tube and the light scatters in the translucent plastic. That added detail and some idea how the thing was constructed in the game’s world.

![](../../assets/ec64953771a6f14d.png)


And now let’s look at Attila’s way of the pin table!

![](../../assets/118bd31293242b14.png)


Attila used Unity and a mix of C# and some shaders. But before diving into the details, here is what he got out of his machine (a longer video waits at the end of the article):

Be…auti….ful! Isn’t it? Here’s Another experiment where he played around with creating something with more atmosphere:

But how is all this possible? Let’s have a look:

![](../../assets/b2a9850e8df39a6f.png)

Like Zoltan, Attila uses a camera to capture a **hidden** 3D Scene and uses the captured data as input for his pin table. And since Unity has a camera system which offers **orthogonal** cameras (unlike Unreal) he didn’t have to use a “hacky” solution like Zoltan described [above](https://simonschreibt.de#z_orthogonalHack).

This is the first GIF he created. Notice that the cube-displacement is controlled by the **specularity** of the spheres (and not [yet] the captured height-information):

![](../../assets/637d37b24458b179.gif)

The pin board rig can be thought of as a volume in space that the user can setup and move around. A pair of ortho cameras render the height and color maps of what’s happening inside, according to objects within the volume. This information is used by the pin table shader to displace/colorize a custom mesh. The resolution of that mesh can be specified as well as height-dependent gradients to further color the pins.

The “vfx” letters show off the separation between the height/color info. The gray letters can **only** be seen by the height camera so they contribute to displacement only (brightness = height), the yellow ones are for the color camera. He dragged the 2 objects apart for clarity, but usually they would overlap.

It’s the same for the red bunny, where the red color version and the one with a depth shader on it overlap and look weird in the editor.

The green cube is on a **separate** object layer, not seen by either of the height or color cameras.

Then it even got **interactive**! Here you can see an early version where the mouse cursor defines where cubes are pushed upwards:

A music video as provider for height data? Because he can! (video without music to avoid copyright problems. also it’s shown in 2x speed):

Height & Color Map Generation

To generate the necessary data he used one camera per map. Each camera is set to be in ortho mode and the view is set to cover the whole pin board volume. Attila fell in love with the flexibility of Unity’s camera system. Each camera can be limited to only render objects in specific layers, so objects that meant to only show up in the board can happily coexist with the rest of the scene. It’s also possible to use any post process effects or other tricks on the cameras (see [section “Peakblur Shader”](https://simonschreibt.de#z_peakblur)).

![](../../assets/5b971eb75798dcb9.png)

Really interesting: I used a hand-made mesh, Zoltan modified his hand-made mesh via shader (tessellation) and Attila goes the way of creating the whole mesh **by code**!

At its core each pin is basically a unit size cube, optionally without the bottom face. He stores position data in vertex colors (used as a multiplier for the displacement like explained in the [basic approach](https://simonschreibt.de#basicVertexColor)), and UVs (so each vertex in the board knows where to sample the height/color maps).

**Hacky-Hack**: Because Unity uses 16 bit vertex indexing he can only generates a **chunk** of the whole board as one mesh. Every frame he renders that same chunk many times, with the UVs offset to cover the whole X*Y sized board (resolution is rounded up to the nearest chunk size.)

![](../../assets/b90d8a258a75a4a3.png)

Besides of the procedural mesh generation the C# code takes care of frame by frame updates and has some editor-specific features, like drawing a 3D gizmo representing the volume of the board for easier editing. A scene can contain multiple pin boards, and each can have its own camera setups.

![](../../assets/4217426fa377af9d.png)


![](../../assets/4217426fa377af9d.png)

![](../../assets/b2c00703fad2fb61.png)

PinBoard Shader

He started out creating the shader by hand, but (after Zoltan’s nagging) Attila ended up using ShaderForge for it in Unity, and it worked out fine. Beside the height/color maps the shader also has inputs for gradient textures, blending between them is managed in the C# code.

“PeakBlur” Shader

He wanted to have a custom motion blur-like post process for the height camera that works similarly to VU meters: it peaks fast, but attenuates slowly. So he ended up creating a simple shader for it that uses an accumulation buffer for the blurring. (See at 0:15 in The Showcase video)

Other Shaders

There are a few other shaders that help out: a depth shader for 3d models that are seen by the height camera, and various shaders mostly used for masking and transition effects. (See at the end of The Showcase video for example)

![](../../assets/cfa6116e47b4df37.png)

Attila’s showcase video consists of 3 parts. For each part he created a separate color gradient to set the mood. He flicked between parts using keyboard shortcuts.

- A particle system follows the mouse around and displaces the pins in its wake
- A red Standford bunny appears ominously, and leaves a
**gray**trail behind. The trail is result of the custom peak blur shader he created for the height camera specifically - Some layered noise textures travel along the board creating some interesting patterns for the height camera

![](../../assets/9d0963bcd859fbd3.png)

He also made some [Unity WebGL exports](https://dl.dropboxusercontent.com/u/8889/MeshMashColor/index.html). It shows really nicely what the camera “sees” and writes into textures targets (top left) which then gets translated into height-information (the green/red rings are create by the interactive mouse cursor):

![](../../assets/3f83bed525191b27.png)


That’s all! We really hope you liked the different approaches with all there differences. In any case, please tell us what you think about this small project and if you would like to see more of it.

Have a nice day!

Great article, interesting stuff as usual and it looks sooo good! :D

I’ve been following your blog for a while and you’re doing a great job!

I’m currently a student learning OpenGL and Computer Graphics in general, and the content you post helps me stay motivated whenever I feel a bit overwhelmed.

Oh and I don’t think people would mind if you were to have this series appear on this blog, instead of keeping it as a side project.

Keep up the good work!

Thanks for your nice comment :) Oh yes it’s very easy to feel overwhelmed when it comes to working with computer especially since the internet holds tons of stuff we “should” checkout :D

As always, awesome article and awesome new concept !

Hey Simon! Damn I love this effect!! :D Nice that you are covering this!!

It’s kind of a demoscene-classic as well. Here are 2 examples:

In Frameranger by Fairlight & Co.

Or in 1995 by kewlers: but this time in 3D!

Íñigo Quílez ak iq, also a demoscene guy: Has is a shader “Cubescape” on his webtoy: here as a kind of sound equalizer view.

And here as static “Grid of Capsules“: But you can put in a video-texture into channel0, Britney Spears for instance .. :D

(actually I did something similar but veeeeeery basic for a small strategy game: Future Wars.

Of course here not with arbitrary imagery, just circular. So I had 1 animation curve where the offset was sampled from according to the distance to the center. I think I even combined the cubes meshes that have the same level or have them skinned to only 1 joint.)

Nice examples, dude! Thank you! I love these demos :)

Oh pardon the linkdumping but there is more! :D

Some maybe interesting wip stuff from the Coocoon group from france: Cocoon 3D engine funny test

I guess the according demo is Shattered. Cheers! ëRiC

no worries! its awesome to checkout all these links :D

moar: 3D-Städte aus lokalisierten Einkommens-Daten static tho. But neat premise with the underlying data.

wow, that looks stunning!

I really like seeing the different to the same problem. I like this new “experimental” format as a nice change of pace.

Yeah it’s really nice and I’ve learned a lot from it. :)

Ah and lets not forget

mrdoobhere: voxels_liquidHis kinect project seems interesting in that regard too!

Also some, interesting ones in his threejs sketches

Sorry I forgot to mention that the shadertoy links might be quite heavy! Be careful before pressing them: save any work. These might crash your browser if it’s doing lots of work already and there are many tabs open.

Great stuff. I’ve learned a lot. Thank you Simon, Zoltan and Attila.

I’d love to integrate a similiar effect for the temples in my game i’m working on.

Thx to you guys for explaining this so well.. i really understood the whole theory behind it!

But i still can’t write shaders at all… is there a possibility that you guys show us some code snippets on how you created the basic kawaii cube that is animated via noise map?

I’d love to experiment on something similiar in Unity!

It looks like 4.13 in Unreal Engine now has Orthographic scenecapture2D’s!

no more 1 FOV perspective scenecaptures

Whopp Whoop :) Nice!

I’m working on a similar project, although it’s not designed to be modified in real time. https://www.dropbox.com/s/5ia3y6xytbcutp6/MapHexaEditor6.png

I noticed that no one tried to remove the unnecessary geometry within the structure. did you consider not worth for real time updates or is it just out of the scope of these “small” experiment ?

Also it’s the first time I hear about accumulation buffer, and the few informations in can find talk about low level openGL implémentation. Can you explain how accumulation buffer was done in Unity ?

to be honest, i don’t know what an accumulation buffer is :,( i would imagine that you add color values to them and reduce them automatically over time. What do you mean with unnecessary structure? you mean the “walls” of the pins?

I mean, between two neighbour, one side can’t be seen while the other side can’t be seen bellow it’s neighbour top, if they have the same height, both side can’t be seen.

I made a drawing to explain myself: https://www.dropbox.com/s/mst8ga7wn94fnmu/structure%20explaination.png

For a rectangular shape, removing the unnecessary side can remove as much as 80% of the geometry (for a flat map) and at least 40%. that’s not a small improvement.

For the side that can be seen, making it stop at it’s neighbour height might have benefit to avoid very heavy “overdraw” in the fragment stage, but that’s ususally optimized by the graphic pipeline

That would definitally very cool to do. Not sure how it could be made but yeah, there’s a lot of stuff not necessary.

I’ve just discovered your blog 2 days ago and I’m already a big fan. I really like the intuitive approach you use to understand and reproduce effects you see in games.

Concerning this specific project, I’ve done similar stuff in the past with a different approach, I’ve used geometry shaders to do that. This is typically the kind of stuff working really well with GS, but, unfortunately they are not directly available in Unreal (but they are in Unity/DX11). GS can replace any primitives with other primitives, so I was basically using a point clouds and was replacing every points by a spike/pillar made out of triangles. The advantage is that your are building the geometry directly in the shader and so, you have a total control on the triangles, normals, positions …

You can see this in action in the training arena of Fighter within (a kinect Xbox One Game … yes … I know) on which I worked years ago, there are no ‘real’ geometry here, everything is generated every frames on the fly and the ring was totally dynamic (expanding as fighters move and reacting to in-game action) : https://www.youtube.com/watch?v=uKetR6VO_pY&t=7m30s

I’m not done looking at your blog entries :) … keep up the good work!

Thanks for the kind words! How did you find out about the blog? :)

Nice looking geometry shader! So you did it by code or does Unity have something like visual node networks like Unreal?

slightly related … ;]

https://i.redd.it/izsp0ckw5gdz.jpg

haha, awesome! :D

Are those seperated cubes or one single mesh in atillas version?

And if it is one single mesh, how can you offset one single cube without the direct neighbors but with one UV map?

As far as I remember it’s one mesh containing all the cubes. Every cube has UVs at different positions so that you can control them separately. He generates the mesh but had to split the final mesh into some chunks because of the limitation of Unity when it comes to vertex count. I think per mesh you only can have 65536 vertices.