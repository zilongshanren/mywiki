---
title: Why I’m excited for Vulkan
url: https://blog.mecheye.net/2015/12/why-im-excited-for-vulkan/
author: Jasper St Pierre
published: '2015-12-10'
source_blog: Clean Rinse
source_site: https://blog.mecheye.net
category: graphics
fetched: '2026-04-13'
---

I’ve stopped posting here because, in some sense, I felt I had to be professional. I have a lot of half-written drafts I never felt were good enough to publish. Since a lot of eyes were on me, I only posted when I felt I had something I was really proud to share. For anyone who has met me in real-life, you know I can talk a lot about a lot of things, and more than anything else, I’m excited to teach and share. I felt stifled by having a platform to say a lot, and only feeling I could say something really complete and polished, even though I have a lot I want to say.

So expect half-written thoughts on things from here on out, a lot more frequently. I’ll still try to keep it technical and interesting to my audience.

# What’s Vulkan

In order to program GPUs, we have a few APIs: **Direct3D** and **OpenGL** are the most popular ones, currently. OpenGL has the advantage of being implemented independently by most vendors, and is generally platform-agnostic. The OpenGL API and specification is managed by the standards organization [Khronos](https://www.khronos.org/). Note that in closed environments, you can find many others. Apple has [Metal](https://developer.apple.com/metal/) for their own set of PVR-based GPUs. In the game console space, Sony had libgcm on the PS3, GNM on the PS4, and Nintendo has the GX API for the Gamecube and Wii, and GX2 for the Wii U. Since it wasn’t expected that GPUs were swappable by consumers like on the PC platform, these APIs were extremely low-level.

OpenGL was originally started back in the mid-80s as a library called Graphics Layer, or “GL”, for SGI’s internal use on their own hardware and systems. They then released it as a product, “IRIS GL”, allowing customers to render graphics on SGI workstations. As a strategic move by SGI, SGI allowed third-parties to implement the API and opened up the specifications, transferring it from “IRIS GL” to “OpenGL”.

In the 30+ years since GL was started, computing has grown a lot, and OpenGL’s model has grown outdated. **Vulkan** is the first attempt at a cross-platform, vendor-neutral low-level graphics API. Low-level APIs are similar to what has been seen in the console space for close to a decade, offering higher levels of performance, but instead of tying itself to a GPU vendor, it allows any vendor to implement it for its own hardware.

# Dishonesty

People have already written a lot about why Vulkan is exciting. It has a lower overhead on the CPU, leading to much improved performance, [especially on CPU-constrained platform like mobile](http://blog.imgtec.com/powervr/vulkan-high-efficiency-on-mobile). Instead of being a global implicit state machine, it’s very explicit, allowing for [better multithreaded performance](http://blog.imgtec.com/powervr/vulkan-scaling-to-multiple-threads).

These are all true, and they’re all good things that people should be excited for. But I’m not going to write about any of these. Instead, I’m going to talk about a more important point which I don’t think has been written about much: the GPU vendor cannot cheat.

You see, there’s been an awkward development in high-level graphics APIs over the last few years. During the early 2000s, the two major GPU vendors, ATI and NVIDIA, effectively had an arms race. They noticed that certain programs and games were behaving “foolishly”.

The code for a game might look like this:


// Clear to black.

glClearColor(0x000000);

glClear();

// Start drawing triangles.

glBegin(GL_TRIANGLES);

glVertex3f(-1, -1, 0);

glVertex3f(-1, 1, 0);

glVertex3f( 1, 1, 0);

// ...

glEnd(GL_TRIANGLES);


(I’m writing in OpenGL, because that’s the API I know, but Direct3D mirrors a very similar API, and has a similar problem)

The vendors noticed that games were clearing the entire screen to black when they really didn’t need to. So they started figuring out whether the game “really” needed to clear the screen, by simply setting a flag that the game wanted a clear, and then not doing it if the triangles painted over it.

Vendors shipped these updated drivers which had better performance. In a perfect world, these tricks would simply improve performance. But competition is a nasty thing, and once one competitor starts playing dirty, you have to follow along to compete.

As another example, the driver vendors noticed that games uploaded textures they didn’t always use. So the drivers started to only upload textures when games actually drew them.

But uploading textures isn’t cheap. When a new texture first appears in a game, it would stall a little bit. And customers got mad at the game developers for having “unoptimized” games, when it was really the vendor’s fault for not implementing the API correctly! Gamers praised the driver vendor for making everything fast, without realizing that performance is a trade-off.

So game developers found another trick: they would draw rectangles with each texture once while the level loaded, to trick the driver into actually uploading the texture. This is the sort of “folklore knowledge” that tends to be passed around from game development company to game development company, that just sort of exists within the industry. This isn’t really documented anywhere, since it’s not a feature of the API, it’s just secret knowledge about how OpenGL really works in practice.

Bigger game developers know all of these, and they tend to have support contracts with the driver vendors who help them solve issues. I’ve heard several examples from game developers where they were told to draw 67 triangles at a time instead of 64 triangles. And that speeds up NVIDIA, but the magic number might be 62 on AMD. Most game engines that I know of, when using “OpenGL in practice”, actually have different paths depending on the OpenGL vendor in use.

I could go on. NVIDIA has broken Chromium because it [patched out the “localtime” function](https://code.google.com/p/chromium/issues/detail?id=16800). The Dolphin project has hit bugs because having an executable named “Dolphin.exe”. We were told by an NVIDIA employee that there was a similar internal testing tool that used the API wrong, and they simply patched it up themselves. A very popular post briefly touched on [“how much game developers get wrong”](http://www.gamedev.net/topic/666419-what-are-your-opinions-on-dx12vulkanmantle/#entry5215019) from an NVIDIA-biased perspective, but having talked to these developers, they’re often told to remove such calls for performance, or because it causes strange behavior because of driver heuristics. It’s common industry knowledge that [most drivers ship with hand-compiled or optimized forms of shaders used in popular games as well](https://fgiesen.wordpress.com/2011/07/01/a-trip-through-the-graphics-pipeline-2011-part-1/).

You might have heard of tricks like “AZDO”, or [“approaching zero driver overhead”](https://www.khronos.org/assets/uploads/developers/library/2014-gdc/Khronos-OpenGL-Efficiency-GDC-Mar14.pdf). Basically, since game developers were asking for a slimmer, simpler OpenGL, NVIDIA added a number of extensions to their driver to support more modern GPU usage. The general consensus across the industry was a resounding sigh.

A major issue in shipping GLSL shaders in games is that since there is no conformance test suite for GLSL, different drivers accept different variants of GLSL. For a simple example, see page 85 [Glyphy slides](http://behdad.org/glyphy_slides.pdf#page=85) for examples of complex shaders in action.

NVIDIA has cemented themselves as the “king of video games” simply by having the most tricks. Since game developers optimize for NVIDIA first, they have an entire empire built around being dishonest. The general impression among most gamers is that Intel and AMD drivers are written by buffoons who don’t know how to program their way out of a paper bag. OpenGL is hard to get right, and NVIDIA has millions of lines of code invested in that. The [Dolphin Project](https://dolphin-emu.org/blog/2013/09/26/dolphin-emulator-and-opengl-drivers-hall-fameshame/) even concludes that NVIDIA’s OpenGL implementation is the only one to really work.

How does one get out of that?

# Honesty

In early 2013, AMD released the [Mantle](http://www.amd.com/en-us/innovations/software-technologies/technologies-gaming/mantle) API, a cross-platform, low-overhead API to program GPUs. They then donated this specification to the Khronos OpenGL committee, and waited. At the same time, AMD worked with Microsoft engineers to design a low-overhead Direct3D 12 API, primarily for the next version of the Xbox, in response to Sony’s success with libgcm.

A year later, the “gl-next” effort was announced and started. The committee, composed of game developers and mobile vendors, quickly hacked through the specification, rounding off the corners. Everyone was excited, but more than anything else, game developers were happy to have a comfortable API that didn’t feel like they were wrestling with the driver. Mobile developers were happy that they had a model that mapped very well to their hardware.

Microsoft got word about gl-next, and quickly followed with Direct3D 12. Another year passed, and the gl-next API was renamed to “Vulkan”.

I have been told through the grape vine that NVIDIA was not very happy with this — they didn’t want to lose the millions they invested in their driver, and their marketing and technical edge, but they couldn’t go against momentum.

Pulling a political coup wasn’t easy — it was tried in the mid-2000s as “OpenGL 3.0”, but since there were less graphics vendors in the day, and since game developers were not allowed as Khronos members, NVIDIA was able to wield enough power to maintain the status quo.

# Accountability

Those of you who have seen the Vulkan API (and there are plenty of details on the open web, even if the specs are currently behind NDA), you know that there isn’t any equivalent to glClear or similar. The designs of Vulkan are that you control a modern GPU from start to finish. You control [all of these steps](https://fgiesen.wordpress.com/2011/07/09/a-trip-through-the-graphics-pipeline-2011-index/), you control what gets scheduled and when.

The games industry has had a term called “dev-to-triangle time” when describing API complexity and difficulty: take an experienced programmer, put him in a room with a brand new SDK he’s never used before, and wait until he gets a single triangle up on the screen. How long does it take?

I’ve always heard the PS2 as having two weeks to a month of dev-to-triangle time, but according to a recent Sony engineer, it was around [3 to 6 months](http://www.engadget.com/2013/06/28/cerny-ps4s-time-to-triangle-to-rival-ps1/) (I think that’s exaggerated, personally). The PS2 made you wrestle with two vector coprocessors, the VU0 and VU1, the Graphics Synthesizer, which ran the equivalent of today’s pixel shaders, along with a dedicated floating-point unit. Getting an engine up on the PS2 required writing code for these four devices, and then writing a process to pass data from one to the other and plug them all together. It’s sort of like you’re writing a driver!

The upside, of course, was that once you put in this required effort, expanding the engine is fairly easy, and you have a fairly good understanding of how everything works and where the boundaries are.

Direct3D and OpenGL, once you wrestle out a few driver issues, consistently has one to two days. The downside, of course, is that complex actions require complex techniques like [draw call batching](https://www.nvidia.com/docs/IO/8228/BatchBatchBatch.pdf) and [using atlases to prevent texture switches](https://en.wikipedia.org/wiki/Texture_atlas), or the more complex AZDO techniques detailed above. Some of these can involve a major restructure of engine code. So the subtleties of high-level APIs are only discovered late in development.

Vulkan chooses to opt for the PS2-like approach: game developers are in charge of building command buffers, submitting them to the GPU, waiting on fences, and swapping the front and back buffers and submitting them to the window system themselves.

This means that the driver layer is fairly thin. An ImgTec engineer mentioned that dev-to-triangle time on Vulkan was likely two weeks to a month.

But what you get in return is all that you got on the PS2, and in particular, you get something that hasn’t been possible on the PC so far: accountability. Since the layer is so thin, there’s no place for the driver vendor to cheat. The graphics performance of games is as much as what the developer puts into it. For once, the people gamers often blame — the game developer — will actually be at fault.

Bravo.

I’d say after I read this article I’ve gotten far more insight into the situation of OpenGL DirectX, Vulkan, and the GPU vendors.

Actually far more than I’d normally have known when reading other articles about Vulkan.

~ James

First of all, I totally agree with everything you said, I just wanted to add something.

On the downside if the application is bugged (e.g. has race conditions between buffers), the driver will have a hard time to fix it. I could even imagine that it works on all current hardware and then fails with future GPUs when the game is already years old and there will be no more patches.

This is not wrong, this is like expecting your Operative System to fix a bug say in VLC. You don’t.

The consumer won’t care why their games don’t run anymore on new hardware.

Any way you cut it, the driver is the wrong place to fix game bugs. If you need to fix a game, then fix /the game/ directly.

Vulkan is hopefully much better specified and will come with conformance tests. It should be easier than ever to debug problems because you don’t have to care about the driver messing behind your back. The “upside” of ‘fixing broken games’ is a mirage, it’s actually the root of many of the problems we’re seeing today in the driver space.

That’s probably where the validation layers come in. If a game runs without error with validation turned on, it should be sufficiently spec-compliant to not have harmful race conditions latent in it.

I really hope this works in all cases, but I’m not sure if it’s even possible to check for all of them.

One very minor detail you can add. When Sony talks about the dev-to-triangle time, they aren’t talking about putting a single triangle on screen – that is trivial. They are talking about how long it would take a developer to use a graphics pipeline with a fairly reasonable degree of efficiency.

Essentially, how long it would take to have an engine where you could actually have something that resembles a playable state without any hitting major bottlenecks that can be avoided.

I hope everyone realizes that Vulkan and D3D12 are 99% the same.

One incredibly huge difference. Vulkan is multilplatform, Direct3D 12 is not. I hope devs don’t support Direct3D 12, in all honesty.

And that’s why Microsoft will do everything they can to make people use DirectX 12. It will force people to use Windows 10.

Except that the latter is proprietary, controlled by one single US company and will only work on Windows10+ and Xbox One.

The former is open, and will work on a multitude of platforms.

The big difference is that Vulkan is hardware and platform “agnostic”!

“Since the layer is so thin, there’s no place for the driver vendor to cheat. The graphics performance of games is as much as what the developer puts into it. For once, the people gamers often blame — the game developer — will actually be at fault.”

Yeah, things aren’t going to work out that way. There is plenty of space to cheat. It remains to be seen how much cheating is normal, though. The key difference is it will be much easier to get great performance without cheating, which isn’t really true now.

Great post. The thing about different behaviour for “Dolphin.exe” reminds me of this one back in the day: http://bazaar.launchpad.net/~compiz-team/compiz/0.9.12/view/head:/plugins/opengl/src/screen.cpp#L47

In general, a great read.

> Pulling a political coup wasn’t easy — it was tried in the mid-2000s as “OpenGL 3.0”, but since there were less graphics vendors in the day, and since game developers were not allowed as Khronos members, NVIDIA was able to wield enough power to maintain the status quo.

This bit is not historically correct. That version of OpenGL that never was is the work of Michael Gold, a then (and now?) NVIDIA employee. NVIDIA employed the spec lead and inventor.

They can still do things behind your back. OpenGL forces them to do that for performance but Vulkan doesn’t stop them. A “well-written” application or engine should not require that help, but what about an averagely written one? What about if a game with suboptimal rendering code happens to have great gameplay, becomes successful and so is important for IHVs to shine on? Everyone is all, “let’s hold hands, do the right thing, and sing tra la la la la,” right now, but if Vulkan becomes important, and big websites are running benchmarks and saying people should be buying GPU A or GPU B based on the scores, NVIDIA especially and AMD too will start throwing driver engineers at the problem of raising their scores. It is a result of basic survival instincts.

I really think that the use of language in this post is unnecessarily loaded. In particular, “optimization” and “cheating” are distinct things, both of which exist.

However, one of them is in fact

desirablewhile the other isn’t. It’s true that the higher level an API is the more it allows the API implementer to optimize, but that’s hardly a bad thing — it means that the game developer doesn’t need to deal with all low-level details of individual hardware. You could easily reformulate “the GPU vendor cannot cheat” as “the GPU vendor cannot optimize”, and it doesn’t sound that great any more.Though I’d argue that neither of them is true – there just may be fewer opportunities to optimize (or “cheat” as you will).

For my view on the subject, read this article: http://www.pcgamer.com/what-directx-12-means-for-gamers-and-developers/

(Yes, it says DX12, but 99% of the actual meat of it is equally applicable to Vulkan)

I agree with some of the previous comments. I don’t see how a new API helps the “cheating” situation at all.

It won’t be long before a major title ships doing something silly/inefficient using Vulcan. Then a ISV will notice and add a specific workaround to its driver. The rest will have to follow suit due to the benchmarking pressure.

I’m no expert on these APIs but I don’t see anything in Vulkan that could expressly prevent these sort of things. The driver can always lie back and say something has been done, when it hasn’t.

The only thing to end this is for all ISVs to cooperate making a pact not to do this. Good luck with that.

Nice article. Yep, it’s fun to see that the PS2 paradigm is about to win eventually. I always said this console had tremendous potential largely underused, without being able to find the words to express it (only supercomputers based on PS2s showed this potential later) . Everyone around me said “it’s too complicated” and I had to bear their “keep it simple” blahblah… Vulkan is a proof that with great power necessarily comes great responsibility (which for a game developer must be interpreted as “you want the real hardware power? now you have it, go to work and show the world what you can do!”).

It feels like an 80’s paradigm return, when there were no drivers, only hardware registers to hack (and hard to find specifications without Internet). We had full power at hand and we pushed the hardware limits like never before and even after that. Then, demo scene became mainly about artistic design instead of technical prowesses. Not that it was a bad thing, but as a hacker, I felt that some magic were lost.

Undoubtly, one of the best things that could happen to the game industry R&D departments was to remove graphic drivers from the equation. Nearly done, can’t wait!