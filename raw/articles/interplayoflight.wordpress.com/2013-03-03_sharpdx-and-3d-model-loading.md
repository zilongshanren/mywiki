---
title: SharpDX and 3D model loading
url: https://interplayoflight.wordpress.com/2013/03/03/sharpdx-and-3d-model-loading/
author: Kostas Anagnostou
published: '2013-03-03'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

I used to be a great fan of XNA Game Studio as a framework to try new graphics techniques, those that needed a bit more support in the runtime than FX Composer or other shader editors could offer. It hasn’t been updated for quite some time now though, and it is becoming irrelevant in an age of advanced graphics APIs and next gen platforms.

In the past few months I noticed a promising framework, [SharpDX](http://sharpdx.org/), which seems to offer a similar level of abstraction of Direct3D as XNA, ideal for graphics demos, but updated to support D3D11 as well. There is another similar framework, [SlimDX](http://slimdx.org/), but if I understand correctly it is not being as actively developed.

Indeed SharpDX handles and hides Direct3D 11 complexity nicely and, like XNA, allows the programmer to focus on the graphics technique not hindered as much by implementation details (I have had to fight with many pages of D3D samplers, shader views, rasteriser configs etc in other engines just to run a simple shader). I also find it a nice educational tool for learning D3D11, since you still have to use most D3D functionality and go through resource creation and pipeline configuration as normal, albeit at a higher level.

My main issue with SharpDX was its lack of a content pipeline. Although one can apply graphics techniques on procedurally generated spheres and cubes, it is more informative and representative to be able to load and use complex 3d models from files.

I already knew of [Assimp](http://assimp.sourceforge.net/), an open source C++ library that supports a large number of 3d model file formats. I looked around a bit and found a few .NET wrappers for Assimp and I gave [one](http://code.google.com/p/assimp-net/) a go. This particular one talks to the C++ Assimp dll through P/Invoke to load a 3d model and exposes it as a hierarchy of nodes which contains meshes and materials.

The integration was fairly straightforward; all it needed was a conversion step from the Assimp.NET model hierarchy to a representation that can be used by SharpDX (containing vertex and index buffers, vertex declarations and shader views for textures). For my quick test I introduced a Model class which acts as a container of ModelMeshes each of which has all the information needed to render a mesh as well as a single texture. Assimp seems to support more detailed Material definitions but I didn’t go that far in this instance.

The result was pretty good, I managed to load both 3ds and obj files with no problem, with all textures involved (Sponza 3ds file available [here](http://hdri.cgtechniques.com/~sponza/files/)):

I even managed to load the Stanford Dragon obj model that failed to load in FXComposer.

Assimp supports a [wide range of model formats](http://assimp.sourceforge.net/main_features_formats.html), although not fbx which I use a lot. There are [converters](http://usa.autodesk.com/adsk/servlet/pc/item?siteID=123112&id=10775855) one can use though.

SharpDX seems like a capable alternative to the D3D11 C++ engine I’ve been using so far and I will be making the switch for my next demos.

I am sharing the [model loading demo](http://sdrv.ms/VSNIsa) in case anyone is interested; it’s pretty basic but can be used as a template for more elaborate model loaders. The demo includes the Assimp library, .NET wrapper and models needed to run. It also only supports D3D11, it should be easy to convert to D3D9 if needed.

Glad to see that you were able to get Assimp working with SharpDX and thanks for sharing your work! Assimp will be hopefully integrated as part of SharpDX in a future version.

Also, If you are a fan of realtime shader editing, there is a nifty feature in SharpDX to allow shader recompilation on the fly at runtime. Just download latest dev package (2.5) and check the demo CustomEffect on Desktop. If you edit and save the shader (in version Debug), you should be able to see the shader automatically recompiled/reapplied inside the demo.

Not sure also if you have noticed in latest version, the ability to compile font and effects automatically from VisualStudio when building your project, just by selecting the correct Build Action on the property page of the file (ToolkitFxc or ToolkitFont).

Thanks for the feedback!

I am definitely a fan of realtime shader editing and I will try you suggestion.

I quickly built a model in blender, looks like this:

![](../../assets/2d3bd7ad3c3097d1.png)


Exported to Direct X .. did not fix mirror yet .. will use lithium later

Then in my development, which is using sharpdx and assimp, I appended code to read the mesh into vertices:

ASI.Scene model = importer.ImportFile(fileName,

ASI.PostProcessPreset.TargetRealTimeMaximumQuality);

var vertices = new VertexBuffer(device, Utilities.SizeOf() * 2 * model.Meshes[0].VertexCount, Usage.WriteOnly,

VertexFormat.None, Pool.Managed);

Vector4[] VSet = new Vector4[model.Meshes[0].VertexCount * 2];

foreach (ASI.Mesh AMesh in model.Meshes)

{

int i2 = -1;

for(int i1 = 0; i1 < AMesh.VertexCount * 2; i1++)

{

i2++;

VSet[i1] = new Vector4(AMesh.Vertices[i2][0], AMesh.Vertices[i2][1], AMesh.Vertices[i2][2], 1.0f);

i1++;

VSet[i1] = new Vector4(AMesh.Normals[i2][0], AMesh.Normals[i2][1], AMesh.Normals[i2][2], 1.0f);

}

break;

}

vertices.Lock(0, 0, LockFlags.None).WriteRange(VSet);

…

device.DrawPrimitives(PrimitiveType.TriangleList, 0, model.Meshes[0].VertexCount / 3);

…

every second triangle is being displayed .. why?

Thx for reading .. : )

The new version of SharpDX is not compatible with with LoadMesh example

Sorry about that, SharpDX toolkit supports Assimp for quite some time now, so I haven’t used this sample for ages. Thanks for pointing this out.

Did you tried to load different 3ds file into project?

I tried a couple and they seemed to work. To be honest, shortly after i posted this SharpDX toolkit added support for model loading so I haven’t used this library since.

Hey, you said that SharpDX ToolKit added support for model loading. Could you please tell me the name of the method to use? I’ve looked into the SharpDX Documentation, but I haven’t been able to find the right reference.

Use Content.Load(filename), it should do the trick. It can’t handle any model format though, only what Assimp can as far as I know.

Hi, I have a problem with this sample.

When I’m trying to run this code, I’m getting DLLNotFoundException in the AddTextureDiffuse method from ModelMesh class.

Can you help me? I’m new to SharpDX and I would like to learn from this sample, because there are not many SharpDX samples.

Apologies, since SharpDX Toolkit supported this library for loading meshes (ages ago) I haven’t used or maintained this code. It is very old, it is expected that it might not compile with newer versions of SharpDX unfortunately. If you are just are starting to get into SharpDX it might be easier to start with Toolkit which supports the mesh loading functionality you need.

SharpDX Toolkit is pretty similar to XNA Game Studio, which I was learning before trying to learn SharpDX, but this Toolkit is deprecated and not supported, so I think that learning SharpDX is a better idea.

I’ve downloaded this sample from this website and I’m still getting the DLLNotFoundException so maybe this is not a fault of SharpDX version,because this sample uses the same version which you were using here.

Hi! How did you managed to load the Stanford Dragon model? I’m trying to but I’m not succeeding at it. What kind of shader do i have to use?

Is the problem in loading them model and creating the vertex buffers, or rendering it? Back then I used assimp to load the model (obj format). Once you have that loading without problems, then you can rendering it with any shader, using textures or not. I haven’t used Sharp DX in ages though so I don’t know what the state of it is and what support it offers in term of model loading nowadays.

The inputlayout is set to null and you get the following error:

SharpDX.SharpDXException: ‘HRESULT: [0x80070057], Module: [Unknown], ApiCode: [Unknown/Unknown], Message: The parameter is incorrect.