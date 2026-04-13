---
title: Ray Tracing with the DirectX Ray Tracing API (DXR)
url: http://diaryofagraphicsprogrammer.blogspot.com/2018/04/ray-tracing-with-directx-ray-tracing.html
author: Wolfgang Engel
published: '2018-04-05'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Experimental DXR support was added to


Later on the same page, he says:


So the first question that goes through one's head when looking at DXR is, why do we need now an API for Ray Tracing? The obvious follow-up is, why is that beneficial for game developers?


I could just finish this blog post now and say "there is no benefit for game developers because it restricts the creative process of making games distinguishable and that is obvious" and it will raise the cost of game development because there is one more API to take care off and move on with my day :-) I could say something along the lines of "requesting an API for ray tracing is like selling refrigerators at Antartica" because in this sentence both comparisons have about the same level of complexity.

I could also say something along the lines of "you want to ruin the whole computer graphics experience by letting them learn a ray tracing API first? Do you not have any heart?".


Instead, let's just ask the question why do we need a ray tracing API?


Hardware vendors will say: because we have to map the complexity of ray tracing to our hardware; we need an API. So far we haven't dedicated any silicon to ray tracing (except PowerVR) because rasterized graphics are commercially at this moment more successful. Just in case this time (compared to the 10+ times before) it catches on, we are promising to add ray tracing silicon as long as you let us hide all this for a while behind an API.


OS vendors will say: we want to be at the forefront of development and we want to bind ray tracing to our platform, let's define an API that everyone has to use to bind them also to our platform. If they want to develop for a different platform they will have to rewrite all their code or use a different API that is hopefully less powerful than ours and those two facts might keep them from doing it ...


Then there are game development studios and then graphics programmers. Commonly described as wise and matured, drawing pictures of cats or flowers on paper and screens and living out their creative energies by writing ray tracing code at


Making games distinguishable on a visual level is a common requirement, similar to movies. There is not one ray tracing technique that can take over the role of being generic. There is no way any API could settle on a subset of ray tracing that could be acceptable for a large group of game developers. We *might* all be able to agree on a BVH structure but there is where it ends. Why would any game developer want to black-box ray tracing. This is comparable to say the following: "a game developer only needs one pixel shader for a material like metal, one pixel shader for a material like skin and all the graphics card drivers only need to be optimized for exactly those pixel shaders. That would make life so much easier.". I put this sentence in quotes because this actually happened not long ago and the rationalization was publicly expressed. Game developers were able to prevent this from happening.

As a game developer and graphics programmer, my interest is always in making commercially successful products that are appealing to gamers and distinguishable from their competitors in appearance and gameplay. Deciding about the fate of ray tracing by creating an API that black boxes parts of it is counterproductive to this effort and not in the interest of small or big game developers like EA, Ubisoft, R* and others.


Then there is the cost factor. Supporting another graphics API will be expensive. As usual, the expense is not in the initial implementation but in the maintenance and QA. So in case someone licenses middleware, the cost of maintenance is still there.Treating ray tracing as an additional feature set to the common graphics APIs should be cheaper.


DXR is in the proposal stage at the moment. Microsoft expressed interest in getting feedback from developers and they would like to change it. I would like to encourage people and game development companies to raise their concerns.

On a technical level, I would prefer to extend the existing APIs "enough" and offer more flexibility through additional features like for example a ray tracing feature level, instead of adding a black box for ray tracing. As soon as the special hardware is available it can be exposed through extensions as well.


This will give game developers the creative freedom they need and at the same time offer the opportunity to invest into it easier.




Addendum 1:

One more thought added: in the moment if you want to ship a game on the PC, there is a high chance you will have to go to a hardware vendor to ask for driver updates or performance improvements. If Ray Tracing (RT) gets its own API, we will have to ask for driver updates for RT as well. Obviously, hardware vendors might want something in return for fixing drivers or making sure your RT code runs fast. This is how it works on PC with Graphics APIs.


We work quite often with smaller developers and bigger developers. Bigger developers just go to the hardware vendor and ask for driver updates and dependent on how "important" their game is, they will get them. Smaller developers hardly get noticed in the process. Over the years most of us agreed that the driver / API situation is not good; Now if we add a RT API, we are creating the same ecosystem for a second API on PC ....


On an economic level, this is very much noticeable by publishers and therefore we can explain this to Bethesda, EA, R* and others. If a game launches on a "broken" driver, the sales of that game will be lower. A game publisher can predict the amount of money that a RT API will cost them during the launch of a game. If we add a RT driver/API we have two opportunities to tank sales at the beginning of the lifetime of a game. Most of us saw their game launching with "broken" drivers. Now extend the experience to a second API.


From that perspective an RT driver is a huge economic factor that is put on the shoulders of the game developers ... you could say whoever wants to add another driver to the PC ecosystem increases the cost of game development on PC substantially ... although it is hard to specify how much.





[The Forge](https://github.com/ConfettiFX/The-Forge)today. Let's think about this for a second by starting with a few quotes from a now famous book, that many people have read in the last couple of days/weeks. The quotes are on the first page of the book "Ray Tracing in One Weekend" by Peter Shirley:I've taught many graphics classes over the years. Often I do them in ray tracing, because you are forced to write all the code but you can still get cool images with no API.

Later on the same page, he says:

When somebody says "ray tracing" it could mean many things.If you read the following pages of this book, you can see that writing a ray tracer might have a low level of complexity. This is why computer graphics students learn ray tracing before they are exposed to the world of Graphics APIs.

So the first question that goes through one's head when looking at DXR is, why do we need now an API for Ray Tracing? The obvious follow-up is, why is that beneficial for game developers?

I could just finish this blog post now and say "there is no benefit for game developers because it restricts the creative process of making games distinguishable and that is obvious" and it will raise the cost of game development because there is one more API to take care off and move on with my day :-) I could say something along the lines of "requesting an API for ray tracing is like selling refrigerators at Antartica" because in this sentence both comparisons have about the same level of complexity.

I could also say something along the lines of "you want to ruin the whole computer graphics experience by letting them learn a ray tracing API first? Do you not have any heart?".

Instead, let's just ask the question why do we need a ray tracing API?

Hardware vendors will say: because we have to map the complexity of ray tracing to our hardware; we need an API. So far we haven't dedicated any silicon to ray tracing (except PowerVR) because rasterized graphics are commercially at this moment more successful. Just in case this time (compared to the 10+ times before) it catches on, we are promising to add ray tracing silicon as long as you let us hide all this for a while behind an API.

OS vendors will say: we want to be at the forefront of development and we want to bind ray tracing to our platform, let's define an API that everyone has to use to bind them also to our platform. If they want to develop for a different platform they will have to rewrite all their code or use a different API that is hopefully less powerful than ours and those two facts might keep them from doing it ...

Then there are game development studios and then graphics programmers. Commonly described as wise and matured, drawing pictures of cats or flowers on paper and screens and living out their creative energies by writing ray tracing code at

[ShaderToy](https://www.shadertoy.com/). ShaderToy is a showcase of the possibilities of ray tracing and all the opportunities it might have in games. It shows the wide range of approaches with their respective pros and cons and what creative people can really achieve if you offer them the freedom to do it.Making games distinguishable on a visual level is a common requirement, similar to movies. There is not one ray tracing technique that can take over the role of being generic. There is no way any API could settle on a subset of ray tracing that could be acceptable for a large group of game developers. We *might* all be able to agree on a BVH structure but there is where it ends. Why would any game developer want to black-box ray tracing. This is comparable to say the following: "a game developer only needs one pixel shader for a material like metal, one pixel shader for a material like skin and all the graphics card drivers only need to be optimized for exactly those pixel shaders. That would make life so much easier.". I put this sentence in quotes because this actually happened not long ago and the rationalization was publicly expressed. Game developers were able to prevent this from happening.

As a game developer and graphics programmer, my interest is always in making commercially successful products that are appealing to gamers and distinguishable from their competitors in appearance and gameplay. Deciding about the fate of ray tracing by creating an API that black boxes parts of it is counterproductive to this effort and not in the interest of small or big game developers like EA, Ubisoft, R* and others.

Then there is the cost factor. Supporting another graphics API will be expensive. As usual, the expense is not in the initial implementation but in the maintenance and QA. So in case someone licenses middleware, the cost of maintenance is still there.Treating ray tracing as an additional feature set to the common graphics APIs should be cheaper.

DXR is in the proposal stage at the moment. Microsoft expressed interest in getting feedback from developers and they would like to change it. I would like to encourage people and game development companies to raise their concerns.

On a technical level, I would prefer to extend the existing APIs "enough" and offer more flexibility through additional features like for example a ray tracing feature level, instead of adding a black box for ray tracing. As soon as the special hardware is available it can be exposed through extensions as well.

This will give game developers the creative freedom they need and at the same time offer the opportunity to invest into it easier.

Addendum 1:

One more thought added: in the moment if you want to ship a game on the PC, there is a high chance you will have to go to a hardware vendor to ask for driver updates or performance improvements. If Ray Tracing (RT) gets its own API, we will have to ask for driver updates for RT as well. Obviously, hardware vendors might want something in return for fixing drivers or making sure your RT code runs fast. This is how it works on PC with Graphics APIs.

We work quite often with smaller developers and bigger developers. Bigger developers just go to the hardware vendor and ask for driver updates and dependent on how "important" their game is, they will get them. Smaller developers hardly get noticed in the process. Over the years most of us agreed that the driver / API situation is not good; Now if we add a RT API, we are creating the same ecosystem for a second API on PC ....

On an economic level, this is very much noticeable by publishers and therefore we can explain this to Bethesda, EA, R* and others. If a game launches on a "broken" driver, the sales of that game will be lower. A game publisher can predict the amount of money that a RT API will cost them during the launch of a game. If we add a RT driver/API we have two opportunities to tank sales at the beginning of the lifetime of a game. Most of us saw their game launching with "broken" drivers. Now extend the experience to a second API.

From that perspective an RT driver is a huge economic factor that is put on the shoulders of the game developers ... you could say whoever wants to add another driver to the PC ecosystem increases the cost of game development on PC substantially ... although it is hard to specify how much.

## 5 comments:

Thanks for your opinion! When I read it I thought: Wow, I could‘t formulate my concerns any better! With all the hype around ray tracing we really don‘t need a black box API that hides the acceleration structures from the user. I wrote a path tracer in Cuda (for medical visualization) and what I really missed was a real cross-platform Compute API on the level of Cuda (bindless texture objects, device pointers in structs, ...), not a ray tracing API.

Those are all reasonable concerns. The opaqueness of the acceleration structures is a little worrying. Hopefully more details will come with time.




That said, we all work with a black box with regard to rasterization and the shader pipeline on modern GPUs, and I don't see that as a negative. Sure there are some problems, but they've abstracted away a lot of details that we don't need to worry about anymore, and I see that as a net benefit. I feel that DXR can possibly get us to that point, that's assuming that the accelerated structures and traversal is something we all agree on.

The question I have is, why do we need new hardware for this? What specifically needs to be accelerated that couldn't already be done with existing compute hardware.

Ideally this ray tracing framework would have been implemented entirely as compute libraries that we could opt in to, and if your application doesn't want to use any ray tracing, then those compute resources could be used for other tasks. Then again, maybe I'm just wanting someone to do my work for me.

Great post Wolfgang. I think I'm broadly in agreement. Personally I'd much rather see the hardware blocks that accelerate Ray Tracing exposed from DirectX and other similar APIs, and then have some wrapper APIs on top that you can opt into that help you manage the complexity (If you want that!).



On the hardware side I think there are two main things that would help. One is some hardware to accelerate the BVH/Triangle intersection. The other is something to help manage the large unsorted "bag" of shader threads that Ray Tracing tends to produce. In my head I see this is some sort of hardware sorter, so your intersection hardware spits out "any hit" requests to invoke shaders, that then get buffered up somewhere in hardware, and periodically spat out as an ordered list, ready to be easily dispatched by the hardware. Same thing happens again when you invoke the closest hit shader.

This sort of hardware block to allow fast coalescing of micro thread dispatches is not just useful for tracing rays though, it's something that comes up a lot in GPGPU, and so having something there that was open and designed for helping to flexibly manage micro dispatches would be a big win all around. Ideally you want to be able to dispatch multiple threads with this if you so desire, not just a single thread "per ray". Also it would be nice if this was something that didn't have to feed straight into a dispatch if you didn't want it to. Seeing as RT suffers from so many issues to do with divergence once you're not dealing with primary or shadow rays, it would be good if the application had some hope of trying to do further processing/sorting/black magic on it's secondary rays to try to reduce this. Then you might be able to even start using LDS and cross lane fun to accelerate thing (if its not hidden from you by the API..).

Yeah, these are all fair points I didn't think about before, but agree on. I think the best solution would be exposing the hardware for low-level developers, but having the more blackboxy options for lazy people like me, who would really like to have a standard and tested fast BVH acceleration structure with all the necessary shader/ray sorting, fast rebuilding and such.

What are your thoughts about Apple's approach to ray tracing in the form of a Metal Performance Shader?




https://developer.apple.com/documentation/metalperformanceshaders/metal_for_accelerating_ray_tracing

Post a Comment