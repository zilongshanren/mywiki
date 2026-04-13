---
title: Debugging DirectX9 is so stressful!
url: http://c0de517e.blogspot.com/2011/03/debugging-directx9-is-so-stressful.html
published: '2011-03-26'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I've been working on console games for the past five years, so I don't know much about the PC tech these days. Now I'm on a console/pc title and I just had to debug the PC build.

Oh. My. God.

I got so stressed I actually almost got sick that night. And then yes, it turned out to be a really small bug that I could totally have debugged easier without hooking these tools anyway.

Pix for Windows is a joke, but still it's the best tool I tried... It's a bit better on DX10/11 (faster refresh)

[NVidia perfHud](http://developer.nvidia.com/nvidia-perfhud)is rather useless (even if I hear it's better than Pix for profiling, which I believe as Pix currently is unable to do any profiling at all) and the Intel GPA thing did not seem to really work at all (it took 20 minutes just to load the capture and it gave me some weird results, even if it looks better than Pix, it's promising I guess) -

**Update**:

[newer versions of GPA](http://software.intel.com/en-us/articles/vcsource-tools-intel-gpa/)seem to work fine, and actually it's now my preferred DX9 tool!

[ApiTrace](https://github.com/apitrace/apitrace#readme)is a new tool which might be good... I had a look at one of the early versions which did not work for DX9, now it seems to have added support for all APIs...

ATI has a Gpu PerfStudio thing which is decent, but it

[deprecated DX9](http://developer.amd.com/archive/gpu/perfstudio/pages/default.aspx), the

[current version](http://developer.amd.com/tools/PerfStudio/Pages/default.aspx)is for DX10/11 only.

I really fucking hope that the new Nvidia Parallel NSight (a.k.a. Nexus) and ATI Gpu PerfStudio 2 are great, I could not try them as they're dx10/11 only and I'm currently on dx9. Overall it really shows how much the industry is committed to PC these days...

## 10 comments:

Hey, at least you can use the d3d debug runtime and get meaningful error codes from D3D, and D3D is stable, and well documented. There are much worse API's to work with.








Here's how graphics programming on the different platforms is for me, in order from best to worst:

Xbox 360 - D3D has extensive error handling, PIX is amazing, and the docs / whitepapers are thorough. The GPU is powerful and has easily understandable performance characteristics, and you only have to target one hardware config. It doesn't get any better than this.

D3D9 - decent error handling and feedback, all the graphics debugging and profiling tools generally suck but may be useful if you get really desperate, docs are decent. As with all PC development, compatibility and performance scaling are a bitch.

PC OpenGL - god awful error handling, no error feedback, practially no graphics tools, terrible sparse documentation, but at least your PC is probably not going to BSOD when you cause an error. As with all PC development, compatibility and performance scaling are a bitch.

PS3 - simple errors often hang the GPU in a generic way with no human understandable information, other errors result in undefined behavior which only repro's rarely, tools are archaic and extremely buggy, documentation is terrible and then translated into English, GPU is gimped so you have to try to make up for it with SPU programming instead of spending the time on important things.

So on my scale, you are complaining about having to use the second best platform =)

I didn't check the quality of OpenGL debugging tools but I know that there are a few. But PS3 has (surprisingly) way, way, way, way, way. WAYWAYWAYWAYWAY. WAY, better tools than Dx9.






Actually since last year PS3 gcmhud does not hang horribly anymore, and it became almost my favorite dev platform for graphics as you can debug/analyze in realtime.

But even the horrible gpad is gold compared to win pix.

Ps3 is not well documented, right.

But at least it's just one GPU, and after a while you learn it and you wrap all the things that need to be wrapped in your own abstractions.

PC DirectX is well documented but the various GPUs are not, at all. Plus you get to deal with various driver problems. So in the end PC is more obscure, by a big margin.

@Daniel OGL has glDebugger. In a PC land it's the only tool which just works and doesn't crash too often. I also would never place a console below PC.


@DEADC0DE before DX10 it was a bit better. Now it looks like no one cares about DX9 tools.

I use Pix and GPAD all the time so I'm curious what your complaint with Pix is?





You can see all device state from depth stencil, to raster, samplers, textures, etc.

You can see pre-vertex mesh, post vertex shader mesh and what the mesh looks like in the viewport.

You can debug shaders with or without source code.

What more do you need?

Anonym: I'm talking about pix for windows, not pix for xbox.



Pix for windows hangs when trying to debug pixels, does not update the framebuffers at each drawcalls properly, does not have decent performance measures, does an horrible job of organizing drawcalls...

Even the interface is all bugged, some windows do not refresh/resize properly (at least pix64 on win7)

I had the same thoughts going to pix for win from pix 360. Once I found out that I could right click the device on the draw call and hit view device I was a little more at ease, but it is still ridiculous that you have to type in your buffer declaration when two clicks away is the same information. If you didn't see the view devices stuff check it out, it eluded me for the first couple times I used it.

Anon: yes I saw it. Still it sucks, I mean, the actual windows do not refresh right on win7, it feels like it's totally an old, abandoned tool.


But by far the most annoying thing is that it does not display each drawcall properly, that makes everything really a guesswork.

@Daniel you can copy & paste a PS3 GPU crash dump into GPAD and it'll decode it for you. I also like the conditional profiling in GPAD.


PIX for windows also doesn't support the INTZ texture formats, so I have to disable shadows to use it. :(

I am talking about Windows PIX not 360.






Everything I said

* check all device state

* see pre vertex, post vertex mesh, and viewport mesh

* debug pixels (see pixel history)

* debug vertices

* view textures

* view samplers

etc.

Is all available in windows version of Pix.

So I repeat my question, what else do you need?

Also, I have no problem with it rendering correctly so perhaps you have a configuration problem.

Feature wise, PIX for windows would be quite OK (but definitely not as great as XBox360 version). Problem is, that those features VERY often does not work at all or work incorrectly. This is especially true for pixel shaders debugging, which is in my opinion one of the most useful feature (in case it works correctly). Sometimes, pixel shader debugger does not start but displays 'Out of video memory' message, sometimes it is unable to display values of registers\variables correctly etc. It sucks.

Post a Comment