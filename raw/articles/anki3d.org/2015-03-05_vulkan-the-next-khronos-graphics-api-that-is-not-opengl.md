---
title: 'Vulkan: The next Khronos graphics API… that is not OpenGL'
url: https://anki3d.org/vulkan-the-next-khronos-graphics-api-that-is-not-opengl/
author: Panagiotis Christopoulos Charitos
published: '2015-03-05'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

This year’s GDC proved to be quite exciting. New technologies, new ideas and some heavyweight announcements. According to the press one of the most exciting presentations was Khronos’ Vulkan API and the demos running on top of it. That really depicted the momentum, the support and the commitment behind the new API.

This article gathers all the publicly shared information behind the new API and adds some personal thoughts in the mix. The fact that I had the pleasure to follow the development of Vulkan API very closely (I was involved early on in the development of a prototype Vulkan driver for ARM’s GPUs) will give some credibility to my personal views. But that doesn’t mean that my views reflect those of my employer. So, whatever you read in the following lines doesn’t necessary reflect the views of my current employer.


# 1. A Bit of History

Let’s start with a bit of history and two bits of speculation. At some point AMD got selected to power both the major console game systems of the 8th generation (PS4 and XBOX one). Traditionally game consoles feature a very thin and low level graphics API and AMD probably had to prototype and maybe implement solutions that will fit that model. At the same time AMD’s CPUs lag behind Intel’s in performance and energy efficiency and a CPU hungry API would make things even worst for them. A third problem for AMD is that their driver stack often gets criticized for its quality, especially from Linux users. The assumption here is that some of these reasons (and probably some more) contributed in the birth of Mantle API.

Mantle gained some popularity with the help of aggressive marketing and the support of some major game studios. At the same time Khronos members were discussing how the next GL should look like and the ideas varied from low level APIs to something close to the current OpenGL but cleaner. During the summer of 2014 a Khronos member, Apple, unveiled their own API called Metal. That announcement turned some heads and at this point Khronos group understood the seriousness of the situation and the fact that the game industry is leaning towards low level APIs.

During the summer of 2014 Khronos started working harder to sort the ideas out but the process was still messy and there were lots of opinions. AMD intervened and did something unexpected. They “donated” Mantle to Khronos to serve as the starting point for GL-next. Mantle was not just a bunch of ideas, it was an actual implementation with real content and numbers to back it up.

Obviously Mantle is an API designed around a specific group of GPU architectures and that made many companies really nervous. The next months were tense, lots of hard work with everyone trying to shape Mantle according to their architectures and their needs. Many discussions, many meetings and of course prototyping new driver stacks.

# 2. Where OpenGL failed

In order to understand what drove Khronos towards solutions like Vulkan first we need to analyze the state of modern OpenGL. The following paragraphs will give an idea why some developers have negative feelings towards modern OGL and it will also give a glimpse why OGL drivers have lots of bugs.

One of the major issues with OGL is its **shading language**. Despite the fact that (for the most part) GLSL itself is OK there are a few quirks that drive people away from it and away from OGL. The first is the fact that, traditionally, all major game engines** write their shaders in HLSL**. For an engine developer, having to support OGL means having to support GLSL as well. That can be achieved by tools that translate HLSL to GLSL or having to write shaders using macros that abstract the functionality of high level languages. People have attempted to do both and/or something in between but the results are far from ideal (see [http://aras-p.info/blog/2014/03/28/cross-platform-shaders-in-2014/](http://aras-p.info/blog/2014/03/28/cross-platform-shaders-in-2014/) for some recent developments on the subject from Aras Pranckevičius). The second problem with GLSL is the **driver bugs**. This particular problem is multi-dimensional and there are many reasons behind it. The fact that every driver is required to implement a full GLSL compiler stack leads to shuttle differences and those differences manifest in compilation failures and bugs. DX solved this problem by having a common compiler outside the driver that translates the high level HLSL to a low level intermediate representation (a.k.a. IR). Then, the driver accepts the IR instead of HLSL. For a driver, an IR is easier to handle and that means less chances of misscompiling and less chances of misunderstanding the spec. Another issue is the **compilation time**. People that have played Linux games that are powered by Unreal 3 often experience long loading times because of this issue. This particular problem is not directly a GLSL problem so I won’t add it here. Another important issue is that OGL applications will have to to expose the **full shader source code**.

The second major problem with OGL (core profile) and something that I find really really annoying is the fact that OGL** doesn’t scale across threads**. Yes, OGL supports multiple shared contexts bound to multiple threads but that functionality cannot be used for multithreaded rendering. The proper multithreading rendering is the ability to build “drawcalls” from multiple threads and append them to a single “queue”. In AnKi I’ve tried to solve this problem by having a single thread serving only OpenGL calls. The problem is that if I ever wanted to balance my rendering across 16 CPU cores that would be almost impossible. For games that require a huge number of drawcalls that particular problem often manifests as 1 CPU core being fully utilized and the rest not.

The third major issue is the **unpredictable performance**. Over the years OGL grew significantly and that growth manifested as conflicting functionality. For example, in OGL 4.4 you practically have 2 ways to create programs (one is the original and the second is ARB_separate_shader_objects), have two ways to create textures (GL 1.1 way and texture storage), have 3+ ways to update buffers from the CPU (read/write functions, map/unmap, ARB_buffer_storage), two ways to handle unifoms (uniforms in a default block and uniform blocks) and I don’t even want to begin counting the ways a texture can be updated. In 4.5 things get even worst by having 2 versions of almost every function, one the classic one and one with ARB_direct_state_access. It’s difficult for someone to distinguish OGL’s fast paths without excessive experimentation or a direct channel to driver developers. Valve was able to optimize the Source engine because they worked really close with nVidia, AMD and Intel. But not everyone has these kind of resources. The real problem boils down to the fact that OGL never had a proper deprecation mechanism. That created a huge API with the developers struggling to comprehend it and to find the the correct way to use it. For those few that really know how to use it, OGL is a charm.

The fourth issue is **the driver bugs**. If you are a Linux desktop user or a Phoronix reader you probably know by now that there is only one decent (enough) implementation out there (the mobile space has other problems that don’t directly revolve around OGL). The rest of the implementations have questionable quality or they are missing important features. With my OGL driver developer hat on I can say for sure that implementing an OGL driver is hard, really hard. Why is it hard? Imagine all the interactions between modern and legacy extensions, then add all the abstractions OGL offers and the cherry on top is the fact that almost none of the OGL objects is mutable. For example you can have a texture of 256×256 size and then resize it to 512×512. This adds lots of driver logic for no real practical reason. Who the hell resizes an already created texture.

The fifth issue is the **performance loss because of various abstractions** that OGL offers. That can be explained using one of the most annoying features of OGL (IMHO), its automatic dependency system. Automatic dependency tracking ensures that read and write operations will appear as they happen in order. For example,

- write to a buffer from the CPU
- draw using that buffer
- at some point that drawcall arrives to the GPU
- while in (3) the app decides to overwrite the buffer’s contents

In the above scenario we have a dependency. The 4th step will have to happen after the 3rd. In practice that requires the driver to track the state of each object. The complexity lies in the fact that every object may have N read dependencies and M write dependencies and the driver will have to resolve and decide what to do next. That is fine but imagine you have a texture for the floor of your level that you loaded once and never touched its contents again. That texture is read-only and since in OGL you cannot mark objects as read-only the driver will have to spend precious CPU cycles tracking that object around. On one hand all those abstractions hide the complexity from the developer, on the other hand they take away the freedom from those developers that know how to do the right thing.

These are some of the issues with modern OGL. The bottom line is that for those developers that know OGL and GLSL spec in and out, know the driver fast paths, write their shaders in GLSL and can fit the rendering into a single CPU core then probably OGL is good enough. If they need something more OGL is not a good choice.

# 3. What Is Vulkan And Why It’s Not OpenGL

Khronos group decided against naming the new API OpenSomething or SomethingGL and this is probably a good decision. Vulkan is not OpenGL, it’s something new that will be developed in parallel with OpenGL. Also, the APIs in question have more differences than similarities and having a common name could be confusing. Vulkan means volcano in some northern languages, a name that closely shows the origins of the API which is Mantle.

So what is Vulkan? The short answer is that Vulkan is a low level API similar to console APIs and Mantle. It’s for PC, mobile and consoles. It’s an API that solves almost all OGL problems I described above and more.

How it looks compared to OGL:

- Vulkan is explicit where OGL has a ton of abstractions.
- Vulkan doesn’t tolerate/handle most errors. On error you will get undefined behaviour or crash or hung.
- Vulkan is thin (also known “close to the metal”), OGL is fat.
- Vulkan exposes the optimal way of doing things, OGL offers many ways of doing the same thing.
- Vulkan drivers are easier to write (at the moment). Valve, IMG and ARM already have prototype drivers.
- Vulkan will drive GPU hardware innovation (explained bellow).
- Vulkan accepts an intermediate representation named SPIR-V, OGL accepts GLSL.
- Vulkan is verbose. Creating a texture in OGL is 2 lines where in Vulkan it can be 50 or more.
- Vulkan may have a steep learning curve. It’s easier to write a “Hello World” app in OGL than Vulkan. But then it gets easier to write in Vulkan.
- If used correctly, Vulkan can push work to the GPU extremely efficiently.
- Even for single threaded applications the CPU usage spend in the driver will go down (depends on the application).
- In Vulkan you can cache part of the state. That will speed up the loading times significantly.
- Vulkan is the only multi-platform API out there. Same as OpenGL.
- Vulkan will be the same for mobile and desktop.
- Vulkan just like OpenGL has mechanisms that will extend it.

The downside of Vulkan hides somewhere between those lines. Writing that close to the metal requires expert knowledge and very careful design. The API will not make any assumptions and it will not try to optimize around bad practices. The term that was chosen for Vulkan is that it is a *ninja API*. It’s somewhat difficult to wield (at first) but in the right hands it can be deadly.

Being a ninja API is not necessarily a bad thing. Consoles also feature ninja APIs and that didn’t stop them from having a plethora of good looking games. Also, people tend to workaround this kind of complexities by creating abstractions. We will probably see some GLU-like libraries that simplify some portions of Vulkan.

In recent years companies like AMD, ARM, nVidia etc spend more resources in software development (drivers, tools) than in hardware. Since software is so damn expensive to produce it becomes quite apparent that the interfaces between software and hardware cannot change often. By interfaces I mean the ways the software communicates with the hardware. That particular problem doesn’t allow radical hardware changes since it’s so expensive to produce software for it. With Vulkan that cost may go down and hopefully that will drive **greater innovation in hardware**.

Another very interesting weapon is the **debug layer.** Vulkan is designed that way so that a debug layer can sit on top of the driver. Its purpose is to validate and error check, its usage is optional and the most important thing is that it’s not part of the driver. Companies (mainly Valve/LunarG) that want a healthy ecosystem around Vulkan bet heavily on the debug layer.

# 4. What will happen to OpenGL?

That is a tough question that doesn’t have an easy answer. OpenGL, most likely, will stay alive for quite some time after the release of Vulkan. There is a huge ecosystem that depends on it. Something that I would love to see is someone implementing an OpenGL core profile using only Vulkan.

# 5. Footnote

Personally I haven’t been that excited in years. Vulkan makes sense as it describes the hardware of this generation. It has the potential to create efficient applications that consume less energy. At the same time drivers will be more robust and with less bugs. Valve, LunarG, Codeplay and others are creating tools that will make things easier for developers and that clearly depicts the momentum of the new API.

The fact that Vulkan looks pretty good from a technical standpoint is not enough to make it successful. We always have to keep in the back of our mind that software companies that control operating systems may try to lock it out. We’ve seen that with Microsoft and Vista and we’ve seen it recently with Google excluding OpenCL in favour of their own crap, Renderscript.

That is all for now.

Great post, thanks for sharing your thoughts and info.

This is indeed the most exciting news I’ve seen in years when it comes to portable graphics code.

(quick remark: you used two different spellings “Vulkan” and “Vulcan” in the article).

(Thanks for the correction! At some point “Vulcan” was also a candidate name.)

This makes me a bit more excited about Vulkan. I’m not sure how much I’ll deal with the low level API’s vs higher level abstractions built upon it, but I’m hoping it sees rapid adoption. Other things that might be interesting in the near future would be something like WebVulkan. Perhaps it’s a bit premature at this point though.