---
title: How to start learning graphics programming?
url: https://interplayoflight.wordpress.com/2018/07/08/how-to-start-learn-graphics-programming/
author: Kostas Anagnostou
published: '2018-07-08'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

About a month ago I opened my Twitter account DMs and invited people to ask me questions about rendering and graphics programming. It had a good response and quite a large number of people sent me their questions.

It caught me by surprise though that the majority of questions was not about particular graphics techniques but about how can one start learning graphics programming. This was not about choosing a graphics course, it was people that knew how to program and wanted to switch to or make a start at graphics.

It appears that with all those graphics APIs, the many freely available game engines, the multitude of graphics frameworks and games that continuously raise the bar in graphics, people feel intimidated and overwhelmed. They don’t know where to start.

It is a bit nebulous, without doubt, but graphics programming can be approached from different angles, at different stages and degrees of difficulty to suit one’s experience and knowledge.

**I am starting from scratch**

The key to learning graphics programming, and any programming for that matter, is in my opinion instant gratification and feedback. You must be able to immediately see the output of your code, with a rapid edit/preview iteration cycle.

When I tried programming for the first time, I could type a few lines like these:

10 CLS 20 PRINT “What is your name?” 30 INPUT A$ 40 PRINT “Hello, nice to meet you ”; A$ 50 END

and a second later the computer was talking to me! This was the magic that captivated me and made me want to learn computer programming.

This is something that is missing these days I think. At my day job, I am lucky if I see the result of my coding within 2-3 minutes after I kick off a build. It is the same with graphics too, too much boilerplate to get a triangle on screen, especially if you are going lower level through a graphics API.

So my advice to people is to start simple and choose something with low friction and instant feedback, like [Shadertoy](https://www.shadertoy.com). For example typing this in the window on the right you get the result straight away on the left:

void mainImage( out vec4 fragColor, in vec2 fragCoord ) { float dist = distance(fragCoord, 0.5 * iResolution.xy); if ( dist < 100.0 ) fragColor = vec4(1.0,1.0,0,1.0); else fragColor = vec4(0,0.5,0.5,1.0); }

Graphics programming can’t get more immediate. Through Shadertoy, one can get a feel of how a pixel shader works, learn about uv coordinates, texturing, things that will take them quite far into graphics programming. You will also pick up the basics of GLSL, a popular shading language. There are many tutorials such as [this](https://gamedevelopment.tutsplus.com/tutorials/a-beginners-guide-to-coding-graphics-shaders--cms-23313) to follow online as well.

You can optionally take it even further and try producing more complex and[ prettier graphics](https://www.shadertoy.com/view/Xds3zN) using raymarching and SDFs. This will provide many opportunities to learn about materials, lighting and shadows which is valuable knowledge moving forwards.

**I have a feel how a painting stuff on screen works.**

Once you can handle pixel shaders confidently, then it is time to move onto a game engine to get a feel of how graphics programming works in a context of a full pipeline and how shaders act on meshes. I would suggest an Editor-based engine like [Unity](https://unity3d.com/) which features a short edit/preview iteration cycle and a large community of developers for support.

In such an environment one can take more control of rendering than Shadertoy, drag and drop 3D models into the scene, create custom vertex and pixel shaders, bind textures, tweak and view the results. Typically, lighting and materials will be handled for you by the engine, but there is nothing stopping you from creating your own.

Again, a game engine will remove a lot of the boilerplate code that is needed to setup the graphics pipeline and will allow you to focus on the crux.

**I can program vertex/pixel shaders, I understand materials and I have a feel of how a graphics engine works.**

This knowledge could make you employable by many game development companies that use game engines like Unity and Unreal. In case you want to take it further though you can use a graphics framework, such as [bgfx](https://github.com/bkaradzic/bgfx), to create your own graphics engine. The advantage of using such a framework is that it hides the low level boilerplate that is required to initiate the graphics device/context, create state objects and resources but it will allow you to manage the resources yourself. You can create your own buffers to pass the vertex/index data to the GPU, set the blending states and rasterisation modes, load, compile and bind the shaders. You can also create your own rendering architecture such as deferred, forward or clustered and implement materials using your BRDF of choice.

In this case getting stuff rendering is a bit more involved than using ShaderToy or Unity but it will provide you with a deeper understanding of how a graphics engine works, without being swamped by a lower level graphics API’s complexity.

**I have a good understanding of how a graphics engine works and I can create a simple one of my own.**

At this point you might want to pick a graphics API up (Direct3D or OpenGL) and take deep plunge into graphics programming. You could try Direct3D12, Vulkan or Metal as well but those APIs have a much steeper learning curve, probably not suitable for someone’s first contact with a graphics API.

Getting meshes rendering on screen, implementing your own rendering passes using a graphics API directly is a quite complicated but ultimately very rewarding experience. You will need to handle graphics devices/contexts, create the resources and compile the shaders yourself and manage the whole graphics pipeline. In this case there is a lot of boilerplate code to wade through before you get anything on screen (although you will learn to hide it eventually under a thin API layer) and it is a steeper learning experience than a graphics framework.

Why would one want to go into graphics programming using a graphics API directly? Like learning to ride a bike without the stabilisers, it is challenging and very rewarding, it is a great learning experience and will give you a deeper understanding of how graphics programming (and GPUs to a large extend) works. Also it is specialised knowledge that is quite sought after by game (engine) development companies.

Choosing the platform and learning how to program graphics techniques is one aspect of graphics programming. The other big aspect is the graphics theory and techniques themselves: learning about lighting and shadowing, materials, rendering architectures, post processing and getting a grasp of how the GPU works internally. Also Maths is a important component of graphics programming. There are many excellent resources to study, the [Real Time Rendering book](http://www.realtimerendering.com/) and the accompanying website is one of my favourite starting points.

To sum it up, getting into graphics programming may seem intimidating but it should not be. It can be approached and untangled gradually, starting simple and building up knowledge as you go. There are many great resources and tools out there, and also a fantastic graphics programmer community that is willing to assist. Enjoy the ride!

[…] How to start learning graphics programming? […]

Thanks for this great introduction. It lowered the bar to start learning. My issue with this (and other game-dev related stuff) is that I want to learn/know it all … so have a hard time starting.

But this intrigues me enough to start working with it, so at least I know the basic concepts and stuff.