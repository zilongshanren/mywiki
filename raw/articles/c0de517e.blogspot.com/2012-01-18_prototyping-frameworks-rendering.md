---
title: Prototyping frameworks (rendering)
url: https://c0de517e.blogspot.com/2012/01/prototyping-frameworks.html
published: '2012-01-18'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

Every now and then, I look around for prototyping frameworks for my rendering work. I always end up with very little but maybe I'm too picky or too lazy. Here are some I've found:

Stuff I actually use:

- FXComposer, both
[2.5](http://developer.nvidia.com/content/fx-composer)and 1.8 (Nvidia does not host it anymore, so you have to google it) as they both crash/have problems in different ways. In particular, 2.5 seems to have problems clearing rendering targets (I use a pass with ztest always to clear), 1.8 crashes in some situations. 1.8 is also nicer for a programmer, but 2.5 is fairly usable. I use SAS and NVidia has some documentation (finally!) about it, to script render passes. In theory both also support proper scripting, but the documentation is thin. A few times when I wanted to look inside FXC 2.5 I used something like ILSpy or .net reflector to delve in the undocumented parts (that's to say, almost everything). - Wolfram's
[Mathematica](http://www.wolfram.com/mathematica/). I wrote a couple of articles on this blog about it, it's great and I love it, I love the language, it's not what you would expect if you're a mathematician but for a programmer is pretty neat (well at least, if you like lisp-ish things, which you should, syntax apart) - Python/IPython (I like the Anaconda distribution) is a good alternative to Mathematica. I still use Mathematica most of the times and I'm not a Python expert, but I've done a few experiments with it.
[SlimDX](http://slimdx.org/)or[SharpDX](http://code.google.com/p/sharpdx/), to tell you the truth I mixed them up a few times, the names are similar. Bottom line, a DX wrapper for C#, I love C#. SharpDevelop if I don't have an updated visual studio which supports the last .net framework.[Processing](http://processing.org/). I wrote an article on the blog about using it with Eclipse for live-coding, it's neat, it's simple, it has a ton of libraries at this point, even to do 3d stuff and shaders but I use it mostly for 2d prototypes.[ShaderToy](https://www.shadertoy.com/). There are a ton of offline programs that offer similar functionality, even on iPad, wherever, it's very popular. But. Having it online is nifty for some quick tests. Unfortunately crashes often on certain browsers/computers (the most common issue is for large shaders to take too long to compile, making WebGL think something's wrong). There are also lots of alternatives ([kickJS editor](http://www.kickjs.org/example/shader_editor/shader_editor.html),[Shdr](http://shdr.bkcore.com/),[GLSL playground](http://glsl.heroku.com/)and[SelfShadow's playground](http://www.selfshadow.com/sandbox/gloss.html)), some more powerful ([WebGl playground](http://webglplayground.net/)which also supports three.js), but ShaderToy is the most popular.- 3D Studio Max. It has an horrible support for shaders (at least it used to, and I suspect not much has changed since) and I never loved it (I love Maya even less though), but I used to know it (six years ago or so) and know maxscript, so I ended up prototyping in Max a few things. It can be handy because you can obviously manipulate meshes all the ways you want and define vertex streams and visually paint attributes on meshes. You can't really control the rendering passes though, so doing non-surface shaders or stuff other than the most basic post-effects is hard. Nowadays I don't use it much if at all.
- Pettineo's framework. Comes with all
[his sample projects](https://mynameismjp.wordpress.com/)and it's a great, simple, well written C++/DX11 framework, very easy to toy with. I have my own fork with some improvements. - Jorge Jimenez
[demo framework](http://www.iryoku.com/smaa/)- as Jorge is a coworker of mine, I have access to his latest version

Seem promising:

[PhyreEngine](http://research.scee.net/files/presentations/gdc2011/2011-GDC-PhyreEngine.pdf), if you have access to the Sony stuff... Might be a bit overkill as it's a fully fledged engine, so the learning curve is not so steep per se but there are tons of examples.- Microsoft/DirectX
[MiniEngine](https://github.com/Microsoft/DirectX-Graphics-Samples/tree/master/MiniEngine). Quite nice! Also NVidia made[Falcor](https://github.com/NVIDIA/Falcor), a "research" framework, but currently it's only OpenGL which is fairly sad (even if understandable as lots of HW extensions come out for OGL first...) [Bart Wronski's C# framework](http://bartwronski.com/2014/04/10/c-net-graphics-framework/). A solid alternative to MJP's, with the added bonus of being C# code.[Karadzic's BGFX](https://github.com/bkaradzic/bgfx)wraps Dx9, 11, 12, OpenGL, GL|ES and Vulkan! It's a bit higher-level than any of these APIs, providing a draw-centric model where draws are sorted on a per-draw key. Neat, even if I don't necessarily care much about being cross-platform while prototyping.[ReedBeta's DX11 framework](https://github.com/Reedbeta/reed-framework).[Threejs](http://threejs.org/).

Some other alternatives:

- Erik-Faye Lund published the sources of his "
[very last engine ever](https://github.com/kusma/vlee)" which is used in a bunch of great[demos](http://pouet.net/prod.php?which=58005)(as in demoscene) I didn't have the time to look into it much yet, but the name sounds great! [Hyeroglyph 3](http://hieroglyph3.codeplex.com/), it's the 3d engine that "ships" with the[Practical Rendering and Computation with DirectX11 book](http://www.amazon.com/Practical-Rendering-Computation-Direct3D-11/dp/1568817207/ref=sr_1_1?s=books&ie=UTF8&qid=1309555438&sr=1-1)(which is nice). It still has a bit more things that I'd like to (more of an engine than a framework) but it's nice.- Matt Fisher
[BaseCode](http://graphics.stanford.edu/~mdfisher/BaseCode.html)could be handy for some kind of experiments. [Cinder](http://libcinder.org/)looks still a bit young, it has many nice things but it lacks some other which I would consider "basics". I feel the same about[openFrameworks](http://www.openframeworks.cc/)and to me Cinder looks nicer. Plus I don't love C++ that much, and Cinder depends on Boost which is a huge turn off :)- Humus
[Framework 3](http://www.humus.name/index.php?page=3D). This is great, it's simpler than a full fledged engine, it's easy to read and it has tons of examples and Humus is notorious for his graphic demos, which all come with sourcecode and were made with his framework! ~~Intel's~~[Nulstein](http://software.intel.com/en-us/articles/vcsource-samples-nulstein/).[VVVV](http://vvvv.org/). It's a node-based graphic thingie. Which would seem like the least suitable thing for rendering prototypes, but it supports shaders, and it supports "code" nodes where you can write C#, so it might be worth a try...[OpenCL Studio](http://www.opencldev.com/), I used to use this for experimentation, but it seems abandoned, sadly.

## 11 comments:

Wow, someone still using FXComposer... guess there never really was anything else like it.



Have you tried using WebGL as a lightweight framework, say under three.js? No MRT, limited capabilities, but a simple quick turnaround -- edit in one window, render in Chrome...

I started doing that when I realized I could use processing.js in mobile Firefox on my Android tablet while commuting on the train (just a little graphics OCD)

That's not a bad idea, I should try. I hate GLSL though, but maybe it got better

I used to use FXComposer all the time on DX9 (up until very recently in fact) just for the convenience of syntax highlight, easy compilation checks and seeing the assembler output.. not for any of the fancy render targets & scripting handling etc. now on DX11 I haven't found a good alternative so I'm back to visual studio. If there was a dx11 fxcomposer id probably use it though.


btw, GLSL is still horrible, pedantic and the compilation is in the driver so its completely vulnerable to vendor-specific screwups. :)

Of course Ati's Rendermonkey (the DLAA source code comes in Rendermonkey format). Needless to say that it is also discontinued.


And Python is great, especially with numpy and scipy (and sometimes the PIL).

Hey Angelo,





I just grab one of my coworkers demo's from his blog

http://mynameismjp.wordpress.com/

and modify it. Usually, I can just take one of his examples and hack together whatever I'm doing pretty quick. His code is really lightweight and doesn't have a lot of framework bs.

-= Dave

anon: I know about Rendermonkey and many people use it effectively. It's not more supported than FXComposer (actually, less), I didn't pick up back in the time when it was cool as it looked way more artist-oriented than FXC 1.8. Nowadays it doesn't make sense to consider it as a tool for the future...

btw, if you do try using Chrome+GLSL (this is for prototyping -- not publication -- so worrying about unsupported browsers may not be important!), note that very recent betas of Chrome now support DDS format (at last!)

KB: publish a tutorial on your blog! :)

maybe I will!



Sad to say I actually had a link on G+ about how I was using WebGL for development on RIFT but removed it because it violated corporate policy against talking about internal processes :/

If you hate GLSL (with you there!), you can also use "cgc -oglsl"

I thought I'd just drop by and ask the author, what's your opinion on Unity as a prototyping framework?

I don't know much about it, but from what I've seen and from how a few friends of mine are using it, it seems great for game prototypes, animation and such, but for rendering I really don't want a game engine or even worse, a game editor. I would just like, as I wrote, some basic functions on top of DX to avoid writing the same boilerplate code over and over, coupled with file watchers and hot-reloading for the various types (textures, shaders etc), and maybe some basic interaction stuff like camera, parameter tweaking etc... A glorified FX composer would do great, or if they opensourced it I'm sure we could poke into it to make it good, removing the limitations of SAS... Or even if they documented decently the scripting/plugin stuff...

Post a Comment