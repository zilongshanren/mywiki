---
title: C#/.NET graphics framework
url: https://bartwronski.com/2014/04/10/c-net-graphics-framework/
published: '2014-04-10'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

In my [previous post about bokeh](https://bartwronski.com/2014/04/07/bokeh-depth-of-field-going-insane-part-1/) I promised that I will write a bit more about my simple C# graphics framework I use at home for prototyping various DX11 graphics effects.

You can download its early version with demonstration of bokeh effect [here](https://dl.dropboxusercontent.com/u/50951404/bokeh_dof01.7z).

So, the first question I should probably answer is…

## Why yet another framework?

Well, there are really not many. 🙂 In the old days of DirectX 9, lots of coders seemed to be using [ATI (now AMD) RenderMonkey](http://developer.amd.com/tools-and-sdks/archive/legacy-cpu-gpu-tools/rendermonkey-toolsuite/) . It is no longer supported, doesn’t have modern DirectX APIs support. I really doubt that with advanced DX10+ style API it would be possible to create something similar with full featureset – UAVs in all shader stages, tesselation, geometry and compute shaders.

Also today most of newly developed algorithms got much more complex.

Lots of coders seem to be using [Shadertoy](https://www.shadertoy.com/) to showcase some effects or quite similar, quite an awesome example would be [implementation of Brian Karis area lights by ben](https://www.shadertoy.com/view/ldfGWs). Unfortunately such frameworks work well for fully procedural, usually raymarched rendering with a single pass – while you can demonstrate amazing visual effects (demoscene style), this is totally unlike regular rendering pipelines and is often useless for prototyping shippable rendering techniques. Also because of basing everything on raymarching, code becomes hard to follow and understand, with tons of magic numbers, hacks and functions to achieve even simple functionalities…

There are two frameworks I would consider using myself and that caught my attention:

[“Sample Framework” by Matt Pettineo](http://mynameismjp.wordpress.com/2013/09/16/sample-framework-updates/). It seems it wraps very well lots of common steps needed to set up simple DirectX 11 app and Matt adds new features from time to time. In the samples I tried it works pretty well and the code and structure are quite easy to follow. If you like coding in C++ this would be something I would look into first, however I wanted to have something done more in “scripting” style and that would be faster to use. (more about it later).[bgfx by Branimir Karadžić](https://github.com/bkaradzic/bgfx). I didn’t use it myself, cannot really tell more about it, but it has benefit of being multiplatform and multi API, so it should make it easy to abstract lots of stuff – this way algorithms should be easier to present in a platform agnostic way. But it is more of an API abstraction library, not a prototyping playground / framework.

A year or two ago I started to write my own simple tool, so I didn’t look very carefully into them, but I really recommend you to do so, both of them are for sure more mature and written better way than my simple tech.

Let’s get to my list of requirements and must-have when developing and prototyping stuff:

- Possibility of doing multi pass rendering.
- Mesh and texture loading.
- Support for real GPU profiling – FPS counter or single timing counter are not enough! (btw. paper authors, please stop using FPS as a performance metric…)
- DX11 features, but wrapped – DX11 is not very clean API, you need to write tens of lines of code to create a simple render target and all of “interesting” views like RTV, UAV and SRV.
- Data drivenness and “scripting-like” style of creating new algorithms.
- Shader and possibly code reloading and hot swapping (zero iteration times).
- Simple to create UI and data driven UI creation.

## Why C# / . NET

I’m not a very big fan of C++ and its object-oriented style of coding. I believe that for some tasks (not performance critical) scripting or data driven languages are much better, while other things are expressed much better in functional or data oriented style. C++ can be a “dirty” language, doesn’t have a very good standard library and templated extensions like boost (that you need for as simple tasks as regular expressions) are a nightmare to read. To make your program usable, you need to add tons of external library requirements. It gets quite hard to have them compile properly between multiple machines, configurations or library versions.

Obviosuly, C++ is here to stay, especially in games, I work with it every day and can enjoy it as well. But on the other hand I believe that it is very beneficial if a programmer works in different languages with different working philosophies – this way he can learn “thinking” about problems and algorithms, not the language specific solutions. So I love also Mathematica, multi-paradigm Python, but also C#/.NET.

As I said, I wanted to be able to code new algorithms in a “scripting” style, not really thinking about objects, but more about algorithms themselves – so I decided to use .NET and C#.

It has many benefits:

- .NET has lots of ways of expressing solutions to a problem. You even can write in more dynamic/scripting style, Emit or dynamic objects are extremely powerful tools.
- It has amazingly fast compilation times and quite decent edit&continue support.
- Its performance is not that bad if you don’t write with it code that is executed thousands of times per frame.
- .NET on windows is an excellent environment / library and has everything I need.
- It should run on almost every developers Windows, with Visual Studio Express (free!) and if you limit used libraries (I use
[SlimDX](http://slimdx.org/)) compilation / dependency resolving shouldn’t be a problem. - It is very easy to write complex functional-style solutions to problems with LINQ (yes, probably all game developers would look disgusted at me right now 🙂 ).
- It is trivial to code UI, windows etc.

So, here I present my C# / .NET framework!


## Simplicity of adding new passes

As I mentioned, my main reason to create this framework was making sure that it is trivial to add new passes, especially with various render targets, textures and potentially compute. Here is an example of adding simple pass together with binding some resources, render target and later rendering a typical post-process fullscreen pass:


using (new GpuProfilePoint(context, "Downsample")) { context.PixelShader.SetShaderResource(m_MainRenderTarget.m_RenderTargets[0].m_ShaderResourceView, 0); context.PixelShader.SetShaderResource(m_MainRenderTarget.m_DepthStencil.m_ShaderResourceView, 1); m_DownscaledColorCoC.Bind(context); PostEffectHelper.RenderFullscreenTriangle(context, "DownsampleColorCoC"); }

We also get a wrapped GPU profiler for given section. 🙂

To create interesting resources (render target texture with all potentially interesting resource views) one would type once simply just:

m_DownscaledColorCoC = RenderTargetSet.CreateRenderTargetSet(device, m_ResolutionX / 2, m_ResolutionY / 2, Format.R16G16B16A16_Float, 1, false);

Ok, but how do we handle the shaders?

## Data driven shaders

I wanted to avoid tedious manual compilation of shaders, creation of shader objects and determining their type. Adding a new shader should be done in just one place, shader file – so I went with data driven approach.

Part of the code called ShaderManager parses all the fx files in the executable directory with multiple regular expressions and looks for shader definitions, sizes of compute shader dispatch groups etc. and stores all the data.

So all shaders are defined in hlsl with some annotations in comments, they are automatically found and compiled. It supports also shader reloading and on shader compilation error presents a message box with error message and you can close it after fixing all of the shader compilation errors. (multiple retries possible)

This way shaders are automatically found, referenced in code by name.

// PixelShader: DownsampleColorCoC, entry: DownsampleColorCoC // VertexShader: VertexFullScreenDofGrid, entry: VShader // PixelShader: BokehSprite, entry: BokehSprite // PixelShader: ResolveBokeh, entry: ResolveBokeh // PixelShader: ResolveBokehDebug, entry: ResolveBokeh, defines: DEBUG_BOKEH

## Data driven constant buffers

I also support data driven constant buffers and manual reflection system – I never really trusted DirectX effects framework / OpenGL reflection.

I use dynamic objects from .NET to access all constant buffer member variables just like regular C# member variables – both for read and write. It is definitely not the most efficient way to do it, forget about even hundreds of drawcalls with different constant buffers – but on the other hand, it was never main goal of my simple framework – but real speed of prototyping.

Example of (messy) mixed read and write constant buffer code – none of “member” variables are defined anywhere in code:

mcb.zNear = m_ViewportCamera.m_NearZ; mcb.zFar = m_ViewportCamera.m_FarZ; mcb.screenSize = new Vector4((float)m_ResolutionX, (float)m_ResolutionY, 1.0f / (float)m_ResolutionX, 1.0f / (float)m_ResolutionY); mcb.screenSizeHalfRes = new Vector4((float)m_ResolutionX / 2.0f, (float)m_ResolutionY / 2.0f, 2.0f / (float)m_ResolutionX, 2.0f / (float)m_ResolutionY); m_DebugBokeh = mcb.debugBokeh > 0.5f;

Nice and useful part of parsing constant buffers with regular expressions is that I can directly specify which variables are supposed to be user driven. This way my UI is also created procedurally.

float ambientBrightness; // Param, Default: 1.0, Range:0.0-2.0, Gamma float lightBrightness; // Param, Default: 4.0, Range:0.0-4.0, Gamma float focusPlane; // Param, Default: 2.0, Range:0.0-10.0, Linear float dofCoCScale; // Param, Default: 6.0, Range:0.0-32.0, Linear float debugBokeh; // Param, Default: 0.0, Range:0.0-1.0, Linear

As you see it supports different curve responses of sliders. Currently is not very nice looking due to my low UI skills and laziness (“it kind of works, so why bother”) – but I promise to improve it a lot in the near future, both on the code side and usability.

## Profilers

Final feature I wanted to talk about and something that was very important for me when developing my framework was possibility to use extensively multiple GPU profilers.

You can place lots of them with hierarchy and profiling system will resolve them (DX11 disjoint queries are not obvious to implement), I also created very crude UI that presents it in a separate window.

## Future and licence

Finally, some words about the future of this framework and licence to use it.

This is 100% open source without any real licence name or restrictions, so use it however you want on your own responsibility. If you use it and publish something based on it and respect the graphics programming community and development, please share your sources as well and mention where and who you got original code from – but you don’t have to.

I know that it is in very rough form, lots of unfinished code, but every week it gets better (every time I use it and find something annoying or not easy enough, I fix it 🙂 ) and I can promise to release updates from time to time.

Lots of stuff is not very efficient – but it doesn’t really matter, I will improve it only if I need to. On the other hand, I aim to improve code quality and readability constantly.

My nearest plans are to fix obj loader, add mesh and shader binary caching, better structure buffer object handling (like append/consume buffers), provide more supported types in constant buffers and fix the UI. Further future is adding more reflection for texture and UAV resources, font drawing and GPU buffer-based on-screen debugging.


Nice! I had the same problem few years ago and I decided to write my own program (it was not technically a framework) in C++. I’m actually working on the second version right now, but it’s based on the engine I use at work so not exactly available to public. Just wanted to let you know that we really need framework like yours so keep up the good work! 🙂

PS: RenderMonkey was awesome!

Thanks for sharing! I’m just wondering why not using github or something similar for code sharing? )

Thanks! I will definitely submit it to the github 🙂

First, I want to clean it up a bit more and add some functionalities – if I continue working on it with my current tempo, I think it should happen around late May.

I had to install the SlimDX Runtime (slimdx.org/download.php), or else it would go into an infinite loop trying to load shaders (ShaderBytecode.CompileFromFile throwing System.Runtime.InteropServices.SEHException causing “done” to never be true in CompileShader::CompileShader).

Figured it was worth mentioning in case anyone else have the same problem. 🙂

Thanks for your comment! The problem is that provided DLL is for specific .NET and windows version (64bit), on other OS doesn’t work – typical problem of .NET assemblies interoperability…

I will maybe try switching in some further future to SharpDX, which supports “anycpu” configuration in one dll – and won’t be dependent on a specific dll for every different configuration.

Pingback: C#/.NET graphics framework on GitHub + updates | Bart Wronski

I keep getting the same error in ShaderManger.cs in visual studio at line 129. Here is the error:An unhandled exception of type ‘System.ArgumentException’ occurred in System.dll

Additional information: The directory name C:\Users\Cian\Documents\Visual Studio 2013\Projects\CSharpRenderer-master\shaders is invalid.

There seems nothing is wrong with that line, the folder “shaders” is there, any idea on whats happening?

I’ve never had it on any machine, but on what function call do you get this exception – my guess would be at getting contents of directory right? Then it could be problem of permissions of .NET / executable, but it should be a different type of exception… You could also try to add backslash in code, but I have no idea if it’s it. According to: http://msdn.microsoft.com/en-us/library/wz42302f(v=vs.110).aspx you can also try GetInvalidPathChars on this string.

Yep its when assigning the shaders folder directory to the string path;

w.Path = Directory.GetCurrentDirectory() + “\\shaders”

Ok I got it working. What I did was move all the files from the project folder to my visual studio project folder. Bit strange but it works…

Pingback: Major C#/.NET graphics framework update + volumetric fog code! | Bart Wronski

Awesome work! Thank you for sharing! FYI I’m working on a cache file asset loader that loads up models from a proprietary format from a old game. Just something fun to do, I plan to use your loading to display the geometry.

Thanks again!

Thank you very much for your kind comment! 🙂 I’m very happy you found it useful. If you think that what you’re doing could be useful for others, please think about sharing – thanks! 🙂