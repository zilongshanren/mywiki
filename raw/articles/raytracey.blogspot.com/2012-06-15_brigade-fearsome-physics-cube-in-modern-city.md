---
title: Brigade fearsome physics cube in modern city
url: http://raytracey.blogspot.com/2012/06/brigade-fearsome-physics-cube-in-modern.html
author: Sam Lapere
published: '2012-06-15'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Another real-time rendering test with Brigade, set in the Urban Sprawl scene.

- 800x480 resolution

- 5 spp

- 2x GTX 580

- because there is very little noise, blurring (frame averaging) is turned off

**UPDATE**: A reader of this blog sent me a highly detailed mesh of a procedural mountain landscape (500k traingles), created with World Machine, which rendered extremely fast with Brigade. The image below took less than half a second to render (the lighting isn't great, but that's not the point of this test :)

**UPDATE 2**: some pictures of an upcoming demo (idea by Jeroen van Schijndel):

the refraction index of the window glass is probably too much, should be tweaked

## 64 comments:

This is flat-out



insane. Without mo-blur the scene (IMO) looks much better than with it, and there is virtually no noise! I can only imagine the fidelity with some type of noise filtration and dramatic scene lighting.Also instancing and some quality vegetation will take this to the next level.

Great work, Sam!

It's almost like flying around a photograph (albeit one that is very saturated) :D


I'm floored.

Thanks again :)


Vegetation is indeed something I should look into quite soon. Good tone mapping will also dramatically improve the realism.

Yeah, the colors are still somewhat oversaturated. It's one of the hardest things to get it right.


Flying around a photograph, that's exactly the experience I was after :)

I was actually going to ask about tone-mapping, but thought 3 posts would be excessive!



Would tone mapping be easy to implement given the current engine state?

Tone mapping and bloom would transform these scenes. Even tasteful per-pixel lens flares would add a nice touch.

We're working on implementing a state-of-the-art bloom and tone mapping solution. It's going to take a while before I can post results though.

Do you approximately have the same performance with OpenCL or are your optimizations still very hardware/CUDA specific ? I wonder at how far standardisation of GPU computing has gone with such heavy optimizations.

I can't give you any performance numbers, but it should work fine on OpenCL. The optimizations are the work of Jeroen van Schijndel btw.

I've been checking out this blog for a while now and I've had a few questions pop up if you've got the time to answer them.




By the way I'm no programmer or anything so maybe some questions are a bit off.

First, how come you've been able to make such huge progress in the last few months? At least regarding noise and convergence it seems to be almost night and day compared to the videos from just early this year and from what I understand you've been using the same hardware the whole time. Is it just down to internal improvements in Brigade?

Second, I've heard that ray/path tracers handle increased polycounts much better than standard raster-engines (because they don't have to shade each poly and so on), is this true in the case of brigade too? Compared to other game engines.

And finally, now that it seems like unreal, crytek and square enix are all incorporating some form of ray-tracing into their engines how do you feel Brigade stacks up to them? Of course Brigade is still more advanced in lightning being a pure tracer and all but is "the competition" catching up?

I completely agree with Sean : with no blur and still this low noise level, it is really good ! Not yet perfect, but clearly promising !!! Way to go !

Is there a Linux build of Brigade?

ust a nerd (nice nickname): Brigade has made some huge progress over the last few months and I'm extremely excited about what's coming next. I can't talk about the technical specifics that made this video possible and I'm sure you'll understand this. Basically it comes down to trying out algorithms on the GPU that noone thought would be possible and then optimize the hell out of it.




Brigade is indeed quite insensitive to the complexity of the scene, e.g. the scene in the "It's about time" game contains 1.8 million triangles and runs almost as fast as a scene with just .5 M triangles.

Unreal Engine 4 uses an approximate form of ray tracing, called voxel cone tracing and the octree contains a coarse voxelized representation of the scene, so it can be updated in real-time. The Luminous engine only uses ray tracing for the character's eyes. CryEngine 3 uses screen space raytraced reflections, which works well as an approximation but is not very robust to the viewing angle. Brigade on the other hand traces the whole scene without using any approximations for ray tracing or geometry.

The other engines will of course use more ray tracing with time, but Brigade isn't going to stand still either. The funny thing is that rasterizers are burning more and more compute cycles on complex and elaborate hacks to approximate the look of ray tracing (soft shadows, indirect lighting, screen space reflections, order independent transparency), while that same compute power could be used much more effeciently at doing ray tracing itself.

Franta: there's no Linux build

Tanks for the thorough response mate.

With that said I can only agree with Sean at the top about using some more organic shapes, maybe a day/night cycle on a hi-poly terrain with some veg and rocks. Looking forward to whatever comes.

lots of trial and error,TheSFReader, thanks!

Just a nerd: a Crysis type environment you mean? Should indeed be interesting to try if I can find such a scene.

is this pure path tracing or combined raytracing with path tracing as you noted in a previous post where you also removed the noise ( Brigade physics test in street scene WIP 2 )

yes, it's not pure path tracing.

It would be really cool to show a dolly zoom effect in some demo.


BTW, this is the best looking real time ray tracing demo I've seen.

Does Brigade support spectral effects?

I don't know if it helps but I've got a little experience in World Machine (procedual terrain generator), which can output terrains in .obj or greyscale heightmap amongst other formats(bare without any props). You can make normals and textures too.


If you think you could use it I could send something like this

imgur.com/XVrus

your way in 128x128 to 4000x4000 polygon resolution and textures and normals in the same size range

Franta: I'm not such a big fan of dolly zoom, but I would like to create a shaky cam effect similar to this one:




http://www.youtube.com/watch?v=CJzJ9WuLH2w

Brigade doesn't support spectral rendering.

Just a nerd: that would be awesome, could you make a procedural terrain in obj which tops at ~300 MB? If that works fine, I can try larger terrains. Can you create a mountain landscape with it as well (something like in the UE4 elemental demo)?

Hi Sam, great performance increase on Brigade!





About a forest/nature scene, why don't you give a try to Blender Island scene by Agus3D?

It's an instanced scene consisting of 19 billion polys but if you are familiar with Blender you could adapt it at your needs.

You could even test your code on an Open 3d package instead of SDKs...

http://blenderartists.org/forum/showthread.php?249664-UPDATED-.bend-19-Billions-of-Polygons-not-a-ridiculous-number-anymore&p=2078966&viewfull=1#post2078966

No problem. 300 MB is about 1800 by 1800 in resolution, which should be plenty for a gameworld.



Because it's procedual (no sculpting unless you want to) It's kinda easy to make something nice (but a bit generic) looking so I should be able to put something up today or tomorow. I guess I'll upload it on Hotfile or something.

What texture/normal map resolution do you want? It's one tex covering the whole terrain in .bmp .png or .tiff

marco: 19 billion polygons are a tad too much for Brigade. You would need something like instancing or on-the-fly geometry generation for that. That's something for the future. But I'll give the island scene a try nonetheless, it looks cool :)


J a n: that would be really cool, a generic landscape is no problem. Could you make a png texture and normal map of 8k x 8k and a lower res version of 2k x 2k or something in that range? Thanks!

Temporarily removed the download links

Hey Sam, are you going to show a "jungle" demo today?



Curios to see!

Cheers

No I was going to try the terrain mesh, but the download links don't work anymore.

That's strange, these links work for me:



http://hotfile.com/dl/160108184/e5386f6/Test.rar.html

http://hotfile.com/dl/160114368/7f56a7a/Testlow.rar.html

If you still can't get them I can try to re-upload

Nice, these links work indeed. Downloading ...

Unfortunately, I wasn't able to load the hi-res nor the low-res terrain in Brigade (low res is 2M triangles, hi-res 7.5M).




But it worked in Octane though. If you want to see it, here's a 5 second render (110 spp) of the 7.5M triangle terrain on one GTX 580 in Octane (1600x512 resolution):

http://i45.tinypic.com/efkm6u.png

Just a nerd: thanks again for the terrain, it's really beautiful and extremely detailed. I'm sure I can make it work in Brigade one day.

If it's just the triangle count that is the problem I can re-build it at any lower resolution(s) if you want to try again.


It's pretty much no work for me now that the actual terrain is already done.

I think it can't render it because I'm using a 32-bit version of Brigade which can handle meshes up to 2M triangles (the 64-bit version can handle meshes as large as your GPU memory can hold).


If you could make a 1 million triangle mesh, i.e. half the size of the low res version, I think it should work for sure.

http://hotfile.com/dl/160286818/55e64d8/Its_Tracetime.rar.html


Here you go. I've estimated the poly count in the file name. I also threw in a closeup of another terrain I had lying around. That one is a bit smoother and shouldn't be hurt as much by lower poly.

Cool! Downloaded, ready for testing.

I only managed to load the most simplified mesh (500k triangles), but it renders very fast. I'll post a screenshot in a minute.

Is there a way to apply the texture and normal because the obj file didn't include texture and normal coordinates?


Thanks again for making these high quality landscapes btw

I'll see if there's a way to do that in World Machine. I thought you could apply them after loading the obj like in (non realtime) software.


Like I said I'm not a programmer :P

no problem :)


maybe I can apply the textures in some 3d modeling software

Looking at the picture you updated the post with I'd definately say 500k is too little for that particular type and scale of terrain.




But at least it's kinda cool to see something I made featured in this blog. I'd definately be able to make something more if you can get it working with the 64-bit or just want a different style. I mostly make these for fun anyways so if I can help out here that's just a bonus

Btw is the reason this renders fast because it is such an open scene and most light just bounce once into the camera or back into the sky?

The lighting is very clean and nice in any case.

I really need to start using 64-bit if I want to run larger meshes.


I think it runs so fast because it's a very open scene, but also because a lot of the BVH nodes in this scene are occluded at anytime. I'll make a short video of it tomorrow if I can make the lighting more attractive.

Mmm the terrain test seems a step back respect the city ones.




Almost every path tracers with 2 580 could run it that good.

I'm waiting for textured version+trees and water.

Regards

Yeah, it was just a quick test to see if Brigade can handle massive terrains.

Hi Sam! About the trees. Can Brigade work with alpha channel of textures?(of leaves for example)

and Is it possible to add instancing in Brigade?

There's no alpha channel nor instancing in Brigade atm.

You can't have tree if you don't support alpha channels...unless you want to model the leaf,which is fine but it would use all the polygon budget.

I realize that. Without alpha support, trees will look fugly, but I'm looking for a way to include a few of them in the city scene anyway, even if that means that every leaf conotains hundreds of triangles.

Sam, are you making a driving game/demo? :) I like that car model who made it?

yeah, a simple driving demo is what I'm going to try next, with some physics and ramps. I don't know who made the car, I got it from Jeroen, a colleague of mine.

By god, if you're going to have a car driving around in your scene it is pretty much mandatory to give it some headlights to show off all the stuff rasterizers can't do!


Preferably even rotating coplights if you can make that work

I'm sorry to interrupt your discussion, but why is alpha channel in textures necessary for a path tracer ? isn't the material's opacity a property of the material and thus handled automatically by the path tracing algorithm ( which would automatically provide the relative effects such subsurface scattering, light propagation through semi transparent materials etc ? ). Am I missing something here ?

@mirror, sometimes you want a part of an object to be transparent, or some gradient. That's what an alpha texture does.

@anonymous if you want it to be transparent then it is a material property ( for path tracing ) not a texture one.


never mind i got it now. it would help for simpler geometry: so you have square leaves ( 2 polygons ) and leaf-like texture, with the non-leaf part of the square being transparent. The other solution would be to fully model a leave, which would lead to a very high polygon count tree.

Sam, is the AO thing you've been showing lately just a mode that can be toggled with actual path tracing?



What I'm think would be a *great* idea is to ship games with the AO mode as the default, but allow PT as an option that's always there.

That way, people can upgrade to path tracing as they get better graphics cards, and also continue to push game developers to greater and greater realism.

That is still to be determined.

Sam,


I'm abit worried since u havent updated ur blog, is everything okay? :)

@Sam, I'm also wondering why the textures in the video look so "wash out" Might it be a gamma issue? The textures probably have a gamma applied to it and Brigade is apply more gamma, so it's getting double gamma.


You could "de-gamma" the textures before using them in Birgade. 1.0 divide by 2.2

another vote for "mouse look"! :D

There will be no more updates for a while

"There will be no more updates for a while"


Why? is it because OTOY won't let you post updates anymore? :O

Not at all.

Hi Sam. No updates? You just ruined my day. But still, keep it up guys. Im watching you :-)

Anonymous: Do not despair!


I'll be back in full force in a jiffy, blogging ad nauseam :)

Extremely awesome thing but you do know that GTX5xx/6xx are crippled in double precision GPGPU? Why don't you go with Radeons/OpenCL?

Post a Comment