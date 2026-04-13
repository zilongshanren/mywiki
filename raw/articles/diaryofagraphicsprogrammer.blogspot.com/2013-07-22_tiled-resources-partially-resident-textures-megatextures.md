---
title: Tiled Resources / Partially Resident Textures / MegaTextures
url: http://diaryofagraphicsprogrammer.blogspot.com/2013/07/tiled-resources-partially-resident.html
author: Wolfgang Engel
published: '2013-07-22'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

One of the new features of DirectX 11.2 and now OpenGL 4.4 is

- no dependent texture read necessary

- hardware filtering works including anisotropic filtering

AMD offers an

Let's step one step back and see what challenge a Megatexture is supposed to solve. In Open World games, we solve the challenge of having a high detail in textures with two techniques:

- on-going

- procedural generation of "large" textures: generating a large terrain texture is best done by generating it on the fly. That means stitching a "large" texture together out of smaller textures with one "control texture" that then also requires a dependent texture read.

The advantage of procedural texture generation is that it doesn't require a lot of "streaming" memory bandwidth, while one large texture or also many small textures eat into the amount of available "streaming" memory bandwidth.

Now with a MegaTexture there is the ability to store much more details in the large texture but it comes with the streaming cost. If you have an implementation that doesn't generate the terrain texture procedurally on the fly and you have to stream the terrain data, than the streaming cost might be similar to your current solution, so the MegaTexture might be a win here.

The biggest drawback of Partially Resident Textures / MegaTextures seems to be forgotten in the articles that I have seen so far: someone has to generate them. There might need to be an artists who fills a very large texture with a high amount of detail pixel-by-pixel. To relieve the workload, a technique that is called "Stamping" is used. As the name implies a kind of "stamp" is applied at several places onto the texture. Stamping also means giving up the opportunity to create unique pixels everywhere. In other words the main advantage of a MegaTexture, offering a huge amount of detail, is counteracted by stamping.

In practice this might lead to a situation where your MegaTexture doesn't hold much detail because artists would have to work a long time to add detail and this would be too expensive. Instead the level of detail that is applied to the texture is reduced to an economically feasible amount.

The overall scenario changes, when data exists that -for example- is generated from satellite images of the earth with high resolution. In that case a MegaTexture solution will offer the best possible quality with less art effort and you can build a workflow that directly gets the pre-generated data and brings it into your preferred format and layout.

For many game teams, the usage of MegaTextures will be too expensive. They can't afford the art time to generate the texture in case they can't rely on existing data.








[Tiled Resources](http://msdn.microsoft.com/en-us/library/windows/apps/bg182880.aspx#four). Tiled Resources allow to manage one large texture in "hardware" tiles and implement a megatexture approach. The advantage of using the hardware for this compared to the[software solution](http://silverspaceship.com/src/svt/)that was used before are:- no dependent texture read necessary

- hardware filtering works including anisotropic filtering

AMD offers an

[OpenGL extension](http://www.opengl.org/registry/specs/AMD/sparse_texture.txt)for this as well and it is available on all newer AMD GPUs. NVIDIA has shown it running on the build conference on[DirectX 11.2](http://blogs.nvidia.com/blog/2013/06/26/higher-fidelity-graphics-with-less-memory-at-microsoft-build/). So there is a high chance that it is available on a large part of the console and PC market soon.Let's step one step back and see what challenge a Megatexture is supposed to solve. In Open World games, we solve the challenge of having a high detail in textures with two techniques:

- on-going

[texture streaming](http://gamedeveloper.com/view/feature/130186/streaming_for_next_generation_games.php): on a console you keep streaming from physical media all the time. This requires careful preparation of the layout of the physical media and a multi-core/multi-threaded texture streaming pipeline with -for example- priority queues.- procedural generation of "large" textures: generating a large terrain texture is best done by generating it on the fly. That means stitching a "large" texture together out of smaller textures with one "control texture" that then also requires a dependent texture read.

The advantage of procedural texture generation is that it doesn't require a lot of "streaming" memory bandwidth, while one large texture or also many small textures eat into the amount of available "streaming" memory bandwidth.

Now with a MegaTexture there is the ability to store much more details in the large texture but it comes with the streaming cost. If you have an implementation that doesn't generate the terrain texture procedurally on the fly and you have to stream the terrain data, than the streaming cost might be similar to your current solution, so the MegaTexture might be a win here.

The biggest drawback of Partially Resident Textures / MegaTextures seems to be forgotten in the articles that I have seen so far: someone has to generate them. There might need to be an artists who fills a very large texture with a high amount of detail pixel-by-pixel. To relieve the workload, a technique that is called "Stamping" is used. As the name implies a kind of "stamp" is applied at several places onto the texture. Stamping also means giving up the opportunity to create unique pixels everywhere. In other words the main advantage of a MegaTexture, offering a huge amount of detail, is counteracted by stamping.

In practice this might lead to a situation where your MegaTexture doesn't hold much detail because artists would have to work a long time to add detail and this would be too expensive. Instead the level of detail that is applied to the texture is reduced to an economically feasible amount.

The overall scenario changes, when data exists that -for example- is generated from satellite images of the earth with high resolution. In that case a MegaTexture solution will offer the best possible quality with less art effort and you can build a workflow that directly gets the pre-generated data and brings it into your preferred format and layout.

For many game teams, the usage of MegaTextures will be too expensive. They can't afford the art time to generate the texture in case they can't rely on existing data.

## 4 comments:

There is a great video about id Tech 5 showing off their level editor : https://www.youtube.com/watch?v=b4ieFw2s7Fw&feature=player_detailpage#t=140s

I think as you say the main challenge with mega textures is the authoring part, most current level editors or 3D packages won't be suited for mega texturing as far as I know.

Yes. I love the fact that this is now supported in hardware. This is especially cool for flight simulators that can just grab satellite data and go with it.

I am looking forward on caching shadow maps this way.

Great article!

Do you know what is the difference between the tier1 and tier2 tiled resources implementation in D3D?

Being an artist I'm not sure if stamping is that big an issue, one can overlay various stamps at multiple levels of transparency and use blending tricks to break the illusion of repeating detail. Also if you have huge library of stamping material, which once the pipeline is in place will grow over time there'll be plenty of resource material to work with.



You do have a point about the pixel by pixel painting thing, but I think that's a trend that's been going on for quite a while now. It seems to me a 512²px texture is about the level where you can do crispy pixel level detail before things start becoming uneconomical. It's certainly a thing of diminishing returns, when you know you're gonna tile a lot you can spend a lot of time making a really nice and modular 128²px texture. Every time you double your dimensions you quadruple your work load. This is the stuff you see going on in the late nineties, but it sorta got phased out as texture budgets rose and became more of a hybrid photosourcing and baking + retouching thing in general. If you go higher you can adopt a more painterly style, but it's clear the pixel art stage where you can work really close 'to the metal' is something only mobile and indie games pursue these days. It's a bit better with the sculpting apps vs painting in 2D, but you can clearly see artists still repeat a lot of detail simply as a part of the working process because it's just too much work otherwise. Stamping isn't a bad thing as long as you can paint over to add little peculiar details afterwards that trick the viewer into thinking it's really all painted uniquely. When I was playing Rage I certainly started looking for repeating detail a few times, I never found much, though they stamped almost everything.

And yeah, this virtualized memory thing is totally awesome! Can't wait to see what people do with it, seems incredibly useful for shadow maps. It seems you can't have really good looking self shadowing without using ridiculous SM sizes (not accounting for pesky acne, sadly). So I'm hoping we'll see more of that :)

Post a Comment