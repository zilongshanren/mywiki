---
title: Unity 101 - From zero to shaders in no time
url: http://c0de517e.blogspot.com/2016/07/unity-101-rendering.html
published: '2016-07-02'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

*Disclaimer:*



*I'm actually no Unity expert, as I started to look into it more seriously*

[for a course I taught](http://c0de517e.blogspot.ca/2016/06/learning-by-teaching.html), but I have to say, it looks like it could be right now one of the best solutions for a prototyping testbed.


*This post is not meant as a rendering (engineering) tutorial, it's written for people who know rendering, and want to play with Unity, e.g. to prototype effects and techniques.*



**Introduction:**

I really liked Nvidia's FXComposer for testing out ideas, and I still do, but unfortunately that product has been deprecated for years.

Since then I started playing with

[MJP's framework](https://mynameismjp.wordpress.com/)by adding functionality that I needed (and later he added himself), and there are a couple of[other really good frameworks out there by skilled programmers](http://c0de517e.blogspot.ca/2012/01/prototyping-frameworks.html), but among the full-fledged engines, Unity seems to be the best choice right now for quick prototyping.
The main reason I like Unity is its simplicity. I can't even begin to get around Unreal or CryEngine, and I don't really care about spending time learning them. Unity on the other hand is simple enough that you can just open it and start poking around, which is really its strength. People often obsess too much on details of technology. Optimization and refinement are relatively easy, it's the experimental phase which we need to do quickly!

**Unity basics:**

There are really only three main concepts you need to know:

**1) A project is made of assets**(textures, meshes...). You just drag and drop files into the project window, and they get copied to a folder with a bit of metadata describing how to process them. All assets are hot-reloaded. Scripts (C# or JavaScript code) are assets as well!

**2) Unity employs a scene-graph system**(you can also directly

[emit draws](https://docs.unity3d.com/ScriptReference/Graphics.DrawMesh.html), but for now we'll ignore that). You can drag meshes into the scene hierarchy and they will appear in the game and the editor view, and create lights, cameras and various primitives.

The difference between the two is that the game is seen through a game camera, the editor can freely roam, and when you are in game view you can change object properties (if you're paused), but these changes don't persist (aren't serialized in the scene), while when you are in the editor changes are persistent.





**3) Unity uses a component system for everything**. A C# script just defines a class (with the same name as the script file) which inherits from "MonoBehaviour" and can implement certain callbacks.

All the public class members are automatically exposed in the component UI as editable properties (and C# annotations can be used to customize that) and serialized/deserialized with the scene.





A component can be attached to any scene object (a camera, a mesh, a light...) and can access/modify its properties, and perform actions at given times (before rendering, after, before update, on scene load, on component enable, when drawing debug objects and so on and so forth...)




Components can really freely change anything in the scene, as there is a way of finding objects by name, type and so on, and can also create new objects and so on. The performance characteristics of doing some operations is sometimes...

Components can really freely change anything in the scene, as there is a way of finding objects by name, type and so on, and can also create new objects and so on. The performance characteristics of doing some operations is sometimes...

[surprising](https://snowhydra.wordpress.com/2015/06/01/unity-performance-testing-getcomponent-fields-tags/), and in real games you might need to cache/[pool](https://docs.unity3d.com/Manual/MobileOptimizationPracticalScriptingOptimizations.html)certain things, but for prototyping it's irrelevant.**Shaders & Rendering:**

From the rendering side things are similarly simple. Perhaps the most complex aspect for someone unfamiliar with it, is the shader system.


As most engines, Unity has a shader system that allows for automatic generation of shader permutations (e.g. the forward renderer needs as permutation per light type and shadow) and it also needs to handle different platforms (it can cross-compile HLSL to GLSL).

As most engines, Unity has a shader system that allows for automatic generation of shader permutations (e.g. the forward renderer needs as permutation per light type and shadow) and it also needs to handle different platforms (it can cross-compile HLSL to GLSL).

It achieves that with a small DSL for shader description "

Unity has also other ways of making shaders

[ShaderLab](https://docs.unity3d.com/Manual/SL-Reference.html)", and the shader code is actually embedded into it.Unity has also other ways of making shaders

[without touching HLSL](https://docs.unity3d.com/Manual/ShaderTut1.html), and a "surface shader" system that allows to avoid writing VS ans PS, but these are not really that interesting for a rendering engineer, so I won't cover them :)
ShaderLab has functionality to set render state and declare shader parameters, with the latter automatically reflected in the Material UI, when a material binds to a given shader. I won't go into a detailed description of this system, because once you see a ShaderLab shader things should be pretty obvious, but I'll provide some examples at the end.

For geometry materials, the procedure is quite simple: you'll need ShaderLab shader (.shader) asset, a material asset that is bound to it, and then you can just assign it to a mesh (drag and drop) and everything should work.


Unity supports three rendering systems (as of now): VertexLit (which is really a forward renderer without multipass and up to eight lights per object - some parts of the Unity docs say this is deprecated, but it seems it's going to live at least as a shader type), Forward (multipass, one light at a time - this rendering mode actually coexists with VertexLit) and Deferred (as in "shading", there is also a legacy system that does "deferred lighting" but that's actually deprecated).

The shader has to declare for which system it's coded and the way Unity passes the lighting information to the shader changes based on that.

Unity supports three rendering systems (as of now): VertexLit (which is really a forward renderer without multipass and up to eight lights per object - some parts of the Unity docs say this is deprecated, but it seems it's going to live at least as a shader type), Forward (multipass, one light at a time - this rendering mode actually coexists with VertexLit) and Deferred (as in "shading", there is also a legacy system that does "deferred lighting" but that's actually deprecated).

The shader has to declare for which system it's coded and the way Unity passes the lighting information to the shader changes based on that.

For post-effects materials you'll need both

The rendering API exposed by Unity is really minimal, but it's super easy to create rendertargets and draw fullscreen quads. Unity automatically chains post-effects if there are multiple components overriding OnRenderImage, and callback provides a source and destination rendertarget, so the chain is completely transparent to the scripts.

[a shader and a component](http://www.alanzucconi.com/2015/07/08/screen-shaders-and-postprocessing-effects-in-unity3d/). The component will be a C# script that gets attached to the camera and triggers rendering in the OnRenderImage callback. In the script one can create programmatically a material, binding it to the shader and settings its parameters, so there's no need to have a separate material asset.The rendering API exposed by Unity is really minimal, but it's super easy to create rendertargets and draw fullscreen quads. Unity automatically chains post-effects if there are multiple components overriding OnRenderImage, and callback provides a source and destination rendertarget, so the chain is completely transparent to the scripts.

Fore more advanced effects, there is support for drawing and creating meshes (including their vertex attributes), drawing immediate geometry (lines and so on, usually for debugging) and even doing "procedural draws" (draws with no mesh data attached, vertices are assumed to be pulled from a buffer) and dispatching compute shaders.


It's also possible to access the g-buffer when using the deferred renderer and sample shadowmaps manually, but there is no provision for changing the way either are created, and no real access to any of the underlying graphics API (unless you write C++ plugins).


Last but not least, on PC Unity integrates with

It's also possible to access the g-buffer when using the deferred renderer and sample shadowmaps manually, but there is no provision for changing the way either are created, and no real access to any of the underlying graphics API (unless you write C++ plugins).

Last but not least, on PC Unity integrates with

[RenderDoc](https://github.com/baldurk/renderdoc)and Visual Studio for easy debugging, which is really a nice perk.**All this is best explained with code**, so, if you care to try,

**-->**

## No comments:

Post a Comment