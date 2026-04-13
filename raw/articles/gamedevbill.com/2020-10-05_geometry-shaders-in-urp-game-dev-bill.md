---
title: Geometry Shaders in URP - Game Dev Bill
url: https://gamedevbill.com/geometry-shaders-in-urp/
author: Bill
published: '2020-10-05'
source_blog: Game Dev Bill
source_site: https://gamedevbill.com/
category: game programming
fetched: '2026-04-13'
---

![](../../assets/63d91eca96b3c0e7.png)

Geometry shaders are shader functions you can run after your vertex shader, and before the fragment shader. Today I’ll go over how to set one up in the Universal Render Pipeline, or URP. As a bonus, I’ll also be covering a trick for creating code shaders in URP that bypasses a lot of the effort and understanding generally required.

I used Unity 2020.1 and Shader Graph 8.2.

This article is paired with [this YouTube video](https://youtu.be/beSRCSRS6mI). Either should stand on their own, but they are best together.

*This article may contain affiliate links, mistakes, or bad puns. Please read the *[disclaimer](https://gamedevbill.com/disclaimer/) for more information.

[disclaimer](https://gamedevbill.com/disclaimer/)for more information.

*Every triangle has three cornersEvery triangle has three sidesNo more, no less, you don’t have to guessWhen it’s three, you can seeIts a magic number*

– Schoolhouse Rocks

Back when most of my shader work was in the built-in renderer, I wrote [an article on how to set geometry shaders up in that pipeline](https://gamedevbill.com/unity-vertex-shader-and-geometry-shader-tutorial/). Now that I’ve largely moved to URP, I once again needed some geometry shader magic, and found it surprisingly hard to set up. URP seems to eschew code based shaders, and the current shader graph (8.2 as of this writing) doesn’t support geometry shaders.

So I’ve worked out the simplest solution I could for creating geometry shaders in URP, and want to share it with you today.

If you find this useful, subscribing to [my YouTube channel](https://www.youtube.com/c/gamedevbill), or getting one of my [recommended ](https://assetstore.unity.com/packages/3d/vegetation/the-illustrated-nature-153939?aid=1011l3QFn)[assets](https://assetstore.unity.com/packages/tools/terrain/gaia-2-terrain-scene-generator-42618?aid=1011l3QFn) is always appreciated.

## What is a geometry shader?

A geometry shader is a shader that runs on, well, geometry. More specifically, it’s run on every triangle. So for a quad, your vertex shader would be run 4 times, and a geometry shader would be run twice. It’s worth noting that in the quad example, the shared vertices are considered unique at this stage. So you technically have six vertices by the time the geometry shader is executing.

To borrow a graphic from [the Vulkan tutorial site](https://vulkan-tutorial.com/Drawing_a_triangle/Graphics_pipeline_basics/Introduction):

![](../../assets/ed7aa77623147308.png)


![](../../assets/ed7aa77623147308.png)

## Code from shader graph trick

Since shader graph doesn’t support geometry shaders, we need a code shader. Cyan has a really good [write up covering how to make these](https://cyangamedev.wordpress.com/2020/06/05/urp-shader-code/), but it requires a lot of technical understanding. I’ll show you a shortcut.

Instead of actually creating a code based shader from scratch, we’re going to let Unity generate it for us.

First, make a PBR shader graph. From just this starting point, you can create a code shader, but I’m going to do a few steps first to make it more successful.

Create a Position node in the graph, and copy it. With one copy, set the mode to “Object” and feed this into the Vertex Position of the master node. Then, with the other copy, set the mode to “World” and feed this into Alpha.

![basic shader graph needed to generate code](../../assets/20407859987b89df.png)


![basic shader graph needed to generate code](../../assets/20407859987b89df.png)

After that, right click on the master node, and select Show Generated Code. This will generate a shader file in your <ProjectDirectory>/Temp/ folder. The name of the file will include the name of the shader graph, as well as a lot of generated characters. Copy that generated shader file into Assets, and you can now use it. I’d suggest renaming it from the generated name to something simpler.

Magic!

## Sample shader

This graph provides the proper baseline if you want to continue purely in code. It’s not quite sufficient for this article, however, because I want to work through a tangible example. So I’m going to modify my graph so that it turns a cube into a sphere.

In a scene create a cube, and then use ProBuilder to “Subdivide Object” four times. This gives us a cube where each side is actually 16×16 quads.

Back in the original shader graph, take the output of the Object-Space position, and Add (-0.5, -0.5, 0.5) to it. Then feed that into a normalize, and then into an Add with (0.5, 0.5, -0.5). Essentially this takes each vertex along the surface of the cube, and moves it so that all are the same distance (one unit) from the center of the object.

![shader graph to turn a cube into a sphere](../../assets/cd93887e6126398e.png)


![shader graph to turn a cube into a sphere](../../assets/cd93887e6126398e.png)

Looking at the result of this graph in the editor, it has created a sphere, but with square-ish coloring. The reason is that our normals are still based on the old cube shape. We’re going to fix those normals in a geometry shader today. Once again, use “Show Generated Code” to get the generated file, and copy it into Assets to work with.

For a way to fix them directly in the shader graph (with a better looking result) [see my earlier article on the subject](https://gamedevbill.com/shader-graph-normal-calculation/).

![Sphere shape with cube normals](../../assets/bd95afc2bb01d087.png)

## Anatomy of the generated shader

There is a ton of code in this generated shader, most of which I’ll ignore, but let’s walk through some key items. To follow along, open up your copy of the shader in any text editor (I recommend Rider).

### Shader Name

The first line of the file is the name, and it’s always “PBR Master”. Change this to something more useful (likely the file name). After doing that, it’s a good time to jump back into Unity, right click on the shader file and select Create->Material. This will make a Material using this shader.

### Passes

Within the meat of the file there are five Pass sections. The most important two being “Universal Forward” and “ShadowCaster”. There’s not too much to say about the Passes other than to comment that we’ll be creating our geometry shader outside this scope, and having all five reference it. If you make a really advanced geometry shader you may not want that, but for most purposes it’s fine.

### #pragma vertex vert

Inside each pass, there is a pair of pragma lines that define the name of the vertex and fragment methods the shader will execute. You don’t actually have access to those, and they aren’t super important, but this is the spot where we tell the shader about our geometry shader (more on this later).

### VertexDescriptionFunction

The `VertexDescriptionFunction `

is essentially the vertex function. It’s at least the part of the vertex function you get access to. I won’t be modifying it today, but in case you want to code up some vert magic, here’s where you’d do it.

Gaining access to this method is why I added the first Position node in that basic shader graph. If your graph has any node feeding into a vertex input of the master node, this method will show up in the generated file. If you didn’t feed anything into the vertex inputs of the master node, you wouldn’t have this method.

### SurfaceDescriptionFunction

Similar to the previous, `SurfaceDescriptionFunction `

as you may guess is your bit of fragment shader. Here again, I’m not going to do much other than remove the placeholder logic I’d had in the graph. If you recall I had the world-space position fed into the alpha output. I don’t actually want that there, but put it in for reasons explained in the `PackedVaryings `

section below

To clear this out, simply set the `Alpha `

to 1 in each `SurfaceDescriptionFunction `

(in all the passes that have one).

surface.Alpha = 1;//(IN.WorldSpacePosition).x;

### PackedVaryings

Next up are four blocks of code: `Varyings, PackedVaryings, PackVaryings`

, and `UnpackVaryings`

.

This is where the magic happens. `PackedVaryings `

are key to our hijacking of data between the vertex and fragment stages. Without this we wouldn’t be able to use this code to make our geometry shader in URP.

The `PackedVaryings `

is what puts the data from the vertex shader into graphics card registers (things like `TEXCOORD0`

), and what lets the fragment shader pull the data out. The layout of `PackedVaryings `

is where we look to grab the data in our geometry shader.

What exactly ends up in the `PackedVaryings `

is dependent on what the shader graph needs. That’s why I put the second position node in my shader graph above. By taking world space position and feeding it into the alpha, I’ll ensure that it’s needed in the fragment shader. This puts it in the `PackedVaryings`

.

It’s important to explicitly feed what you need into `Alpha `

or `AlphaClipThreshold`

. The other fragment inputs, such as `Color`

, are not used in the “ShadowCaster” Pass. If the “Universal Forward” pass needs something the “ShadowCaster” does not, then those two passes will have different varyings. That makes it hard for us to write one geometry method shared between the two.

### Lining up the registers

It requires looking at the varyings holistically to work out how to grab the data. For example, in the `PackVaryings `

method you can see that `positionWS `

is fed into `interp00`

. Then in `PackedVaryings `

you can see that `interp00 `

is stored in `TEXCOORD0`

; (I know it’s easy to mix up `PackVaryings `

and `PackedVaryings`

!)

## Adding Geometry

Now on to how to add a geometry shader.

### #pragma declaration

First, in all five passes, add a line between the vertex and fragment pragmas to declare usage of a geometry function.

#pragma vertex vert #pragma geometry geom #pragma fragment frag

### GeomData struct

Now we’ll start setting the geometry code up. At the very top of the file, right after subshader, add an `HSLSINCLUDE `

block. This allows us to crate one geometry method that all passes will use.

Inside that code block, create a struct called GeomData.

HLSLINCLUDE struct GeomData { float4 positionCS : SV_POSITION; float3 positionWS : TEXCOORD0; float3 normalWS : TEXCOORD1; float4 tangentWS : TEXCOORD2; float3 viewDirectionWS : TEXCOORD3; float2 lightmapUV : TEXCOORD4; float3 sh : TEXCOORD5; float4 fogFactorAndVertexLight : TEXCOORD6; float4 shadowCoord : TEXCOORD7; };

This struct, and the variables in it can be named whatever you want. The key is that they are tied to registers. Here I’ve used the multiple varyings to figure out which data is fed into which registers, and named my variables accordingly.

It’s important, if you are reading from the registers, to make sure that you either write a custom geometry function for each pass, or make sure that those registers are used the same ways in all Passes.

### Geometry Function

Lastly we’ll add a geometry method. This method takes in three vertices worth of GeomData as input and passes an array of them back out. At a minimum, you’d want to pass three back out, but you can pass more.

Here is a do-nothing geometry shader, to show you what the minimum code looks like.

[maxvertexcount(3)] void geom(triangle GeomData input[3], inout TriangleStream<GeomData> triStream) { GeomData vert0 = input[0]; GeomData vert1 = input[1]; GeomData vert2 = input[2]; triStream.Append(vert0); triStream.Append(vert1); triStream.Append(vert2); triStream.RestartStrip(); }

I’ll go through section by section.

`[maxvertexcount(3)]`

– This declares to the compiler that the method will return no more than 3 vertices. If your geometry shader is generating additional geometry, up this number.

`void geom( ... input[3], ... triStream)`

– The method declaration takes 3 vertices in, and returns however many it wishes (up to the declared max) in the `triStream`

. The method name here is important. This name, `geom `

in my case, must match the name used in the `#pragma geometry geom`

from anearlier step.

`GeomData vertN = input[N]`

– This copies the data on the incoming vertices to local variables.

`triStream.Append(vertN)`

– This adds each vertex to the output stream.

`triStream.RestartStrip()`

– This method needs to be called after every set of three vertices. It informs the system that you have just finished defining a triangle.

### Fixing Normals

Now to add the logic that actually fixes our normals. A normal can be calculated form two edges of a triangle using a cross product. The two edges can be determined by subtracting corner positions.

Note that in the code below I am using `positionWS `

not `positionCS`

. The clip space (CS) position is needed as a final output to render properly, but doesn’t suit our math well. In general clip space coordinates are harder to work with, and in the specific case of normals, we need our normal output in world space.

... GeomData vert2 = input[2]; float3 normal = normalize(cross( normalize(vert0.positionWS.xyz - vert1.positionWS.xyz), normalize(vert0.positionWS.xyz - vert2.positionWS.xyz) ));

With that normal calculated, feed it into the `normalWS `

fields of each vertex.

vert0.normalWS = normal; vert1.normalWS = normal; vert2.normalWS = normal; triStream.Append(vert0); ...

![normals fixed by geometry shader](../../assets/95918431984fac37.png)

This corrects our normals on each triangle in the shape. Unfortunately it doesn’t give us smooth edges, but this isn’t a lesson in fixing normals. This is a lesson in geometry shaders, that used fixing normals as a convenient example.

## Advanced Geometry Shaders in URP

This is obviously just scratching the surface of what can be done with geometry shaders. My intent today was just to show you how to create on in URP. I plan to cover more uses for them in future tutorials.

If you have something specific you’d like to see in a geometry shader tutorial (or any tutorial for that matter), comment on the [YouTube video to let me know](https://youtu.be/beSRCSRS6mI)**. **

Web [hosting provided by BlueHost](https://www.bluehost.com/track/gamedevbill/AboutMe).

*Do something. Make progress. Have fun.*