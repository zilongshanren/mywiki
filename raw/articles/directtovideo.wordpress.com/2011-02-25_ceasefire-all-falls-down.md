---
title: ceasefire (all falls down).
url: https://directtovideo.wordpress.com/2011/02/25/ceasefire-all-falls-down/
published: '2011-02-25'
source_blog: direct to video
source_site: https://directtovideo.wordpress.com
category: graphics
fetched: '2026-04-13'
---

**Ceasefire (All falls down..)** by **CNCD vs Fairlight** – 2nd place, Assembly 2010 combined demo competition.

[Capped.tv](http://capped.tv/cncd_fairlight-ceasefire_all_falls_down) [Youtube](http://www.youtube.com/watch?v=vQ2iQQvofCE&feature=related) [Pouet](http://www.pouet.net/prod.php?which=55558) [Download executable binary](ftp://ftp.scene.org/pub/parties/2010/assembly10/demo/ceasefire_all_fall_down_by_cncd_vs_fairlight.zip)

(This is late. Really really late. Sorry. I’ve been busy! Honest.)

It’s become traditional for us to do something for [Assembly](http://www.assembly.org) (in Helsinki, Finland, 5-8 aug 2010). This year we wanted to do a demo that continued from Agenda with the particle theme, but took things further – we felt like we barely scratched the surface of what was possible. And we actually started quite early, almost three months before. The core plan and direction was laid down and we organised the soundtrack. We wanted to try and really plan something out and make something big.

![ceasefire](../../assets/62087d6f2e9a660d.jpg)


*100% particles*

Unfortunately when man makes plans.. well, it completely didn’t work out. The soundtrack didn’t come out as we hoped, the demo plot was far too bound to the soundtrack and the visuals were far too bound to the plot – we were at the mercy of it. Every scene was required, every part needed for it to make sense. We realised the whole thing wasn’t going to happen. So we started again. We hunted around for possible tracks and in the end [Hunz](http://hunz.com.au/) came to the rescue – he let us use his beautiful track “All Falls Down” and also remixed it for us to fit the direction on a very short timescale.

So about that direction – well, the original plan for the demo was this sort of time-shifted end-of-the-world meet your maker theme where a city gets destroyed by some sort of holocaust, but then a phoenix rises from its ashes. It was going to be great! Trust me. Well, happily the new soundtrack – with strong vocals leading the way – actually did support this theme, but we were able to do something more loose than we had originally planned – disaster-related scenes, but less of a central plot to be reliant on.

Naturally the engine had matured a bit since Agenda, and we now benefitted from overall better performance, as well as a number of new features and effects; in particular lines / hair, displacement mapping of particles and collisions with distance fields. There were also a few effects I made specifically for the demo: fire using fluid solvers, raytraced spheres and a tidal wave thing. I’ll go through some of those in turn.

**Hair**

A natural step when you’ve got a particle system is to try linking the particles together with lines so you get something like hair, and that’s how this started out. Then you’ve got two immediate issues to overcome: how to get the right particles linked together so it isn’t a jumbled mess; and how to make them move in a way that appears connected. Fortunately if you solve the latter you’re a long way to fixing the former.

Firstly, we assume that particles next to each other in the texture are part of the same line, up until some line length is reached. For simplicity’s sake all the lines contain the same number of particles, and that number is a power of two so a number of lines fit neatly into the particle texture. Lines are arranged solely in the X direction of the particle texture and can’t spread onto multiple rows: i.e. the maximum line length allowed is the width of the particle texture. With this arrangement you’ve got a pretty easy way of finding the particles that make up one line, of finding the next and previous particles in the line and so on. For example, in a 1024×1024 particle texture and a line length of 256, I have 4 lines per row – 4096 lines in total.

Connected movement is achieved by using a spring solver. Particles attempt to maintain a certain distance from their connected neighbours in a line by pushing and pulling towards them; several iterations of that are performed per update. So it’s simply a case of looking at the next and previous particles in the line and moving the particle towards or away from its neighbours as appropriate. End points can be anchored if we want.

Ah, but why do the previous and next particles actually make sense as line neighbours in the first place? Can’t they be anywhere in space? No, because I have a special emitter that emits particles in a suitable way – i.e. as lines in the first place. This can be done using a random direction, or using normals from a mesh, or to fill a mesh, or along contours of a distance field. If they start off in a good shape, and there’s a spring solver on them to keep them in a good shape, they stay in a good shape. Easy.

For rendering we have a couple of options: line primitives or camera-facing quad strips. Quads have the advantage of having actual thickness, but they’re slower to render and have to be at least a minimum thickness or they get culled by the hardware. We tessellate at render time using catmull rom splines so lines can be smoother – that’s just done in the vertex shader. We use opacity shadow maps just like the particles use – so the lines are self shadowed nicely.

The shading had quite a lot of faking involved too, actually. I used a blend between a few colours; a dark tone which is used as an “occluded” colour near the root, and a lighter “unoccluded” tone; then a couple of tones to randomly pick between for each strand of hair.

![hair](../../assets/9d04aea2bb225310.jpg)


**Unreleased material alert!* The hair effect when used on a horse, a while ago*

Naturally as with all these particle things, the issue isn’t about numbers, it’s about control – and that was the trick: emitting to fill a mesh (a match stick in this case), getting all blown about and then reforming into that mesh again. It turned out the curl noise affector worked great on lines because it has spatial continuity – it made it look like hair underwater, which is exactly what we wanted.

**Fire**

I spent some time looking into how to do a good fire effect with the help of some Siggraph papers. Fire is quite hard to do properly – you have to capture the large-scale and small-scale movements. The really good way to do fire is to use a massive 3D fluid solver which is big enough to capture the small-scale details – but that’s completely prohibitive in terms of memory and performance. So there’s an approximation. The basic theory is, you use a small number of screen-aligned 2D slices each running their own separate 2D fluid solver; and you blend the input velocity and density across the slices so they all have pretty similar source data, which means they all move in a way that makes sense across the slices. Then you add some procedural fluid flow (read: curl noise) on top to add detail.

The way I started was to follow the paper and use particles for inputs. You render them as particles extruded into quads to capture the motion, rendering both density & temperature and velocity into the slices as MRTs; then you apply 2D fluid solvers to the slices, apply some procedural motions and render the slices view aligned with some shader to generate colour from temperature. Well, it turned out to be a total bitch. It appeared the paper left out a few critical details, and it didn’t work out quite the way I hoped. The biggest problem was one of scale – getting a fire that would work for a big volume of it – like the heads of some tikis – was very different to one that worked for a small one like the burning head of a match. Also we couldnt get quite as many slices as we wanted because it was just too heavy with large, high resolution fluid simulations, even in 2D. The particles also didn’t give a clean and smooth enough result, even when extruded into quads.

In the end we ditched particles as inputs totally and used meshes instead. Well, GBuffers anyway. I rendered the meshes to GBuffers and blended those into the fire buffers, weighted by depth from slice and generating velocities using perlin noise and the screen space normals. This gave a much cleaner result which was more controllable and a massive amount faster. Still a total bitch to get the scales working well for different fires, though.


*Evolution of the fire effect*

![evolution of fire](../../assets/ab35df66cd79cebb.jpg)



![evolution of fire](../../assets/19ba6e8f21012c68.jpg)



![evolution of fire](../../assets/27da2b602593d246.jpg)


*See, it got better*


And then there was the rendering. You would think it’d be easy to map a floating point temperature value into good looking colours, but it wasn’t. I also had to blend them across the slices and with other scene elements, and there just didn’t seem to be a mode that made it look good. It took an age of tweaking and I never was satisfied with it.

In the end we got.. something. I wasn’t totally happy with the effect but it did add something to the demo that wasn’t particles. It looked pretty good when applied to that fucking phoenix at the end though.

**Raytraced spheres**

Problem: render a reasonably large number (lets say 100s) of moving spheres that can overlap in screen space, and are all refractive, with a reasonable degree of accuracy. Solution? Lets see.. they need to refract the background which is easily achieved through render to texture; that alone could be achieved with a simple rasterisation-based approach. But they also need to refract each other given that they could overlap a lot – and that overlapping makes rasterisation inappropriate, and a raytracing solution would be better. Oh, and we also need it to not eat too much frame time given that it’s a small part of a much larger scene, so that – combined with the large number of spheres – prohibits a simple brute force approach of checking the ray against each sphere per pixel and then again for the refractions.

![Spheres, during development](../../assets/91d6ac1b1bab3a3b.jpg)


*Raytraced spheres turned into particles, early in development. This effect was a right pain*

What I needed was a way of reducing the problem down to a smaller set of spheres per pixel which are likely to affect the ray at that pixel. One way would be to build a 3D spatial database for the spheres and use that to trace more efficiently, but that isn’t all that pixel shader friendly – or easy to update per frame. So I cut a few corners and went for a 2D approach. The idea was, at a low resolution I worked out which spheres overlapped each pixel and stored those spheres in render targets; then at a high resolution I only consider the spheres in those render targets to trace through, rather than all of them. In order to cope with refractions I had to be a bit generous on the overlap test, but it worked well. The low resolution classification step was a long shader that looped through the large number of spheres – sorted front to back and roughly pre-classified on CPU to only check those vaguely near the pixel – and gathered the first 4 that overlapped, writing them to MRTs. The high resolution tracing shader loaded the 4 spheres from the render targets and checked them for ray intersections, then traced the ray through for refractions, finally getting an exit direction to look up the back buffer. 4 spheres was usually enough overlap to get believeable refractions – and hey, we were going to turn it all into particles anyway, so there was room for error.. wait, what was that about overkill?

I’ve used this approach before to render large numbers of metaballs (1000s) too; the problem is that with a lot of balls you start to need a lot of overlapped spheres per pixel, and you simply can’t cache enough, so it breaks down. To do 1000s of metaballs you need a different approach, but that’s something for another post..

**Particle fun**

One of the main scenes in the demo involves a street of buildings which gets blown up, building at a time, into particle explosions. That got.. pretty heavy. Each building was built of 1m particles, so we ended up pushing 10m particles per frame through the render. Ow. That was just not going to fly as regular particles where we maxed out any reasonable GPU at 2m – and blew all kinds of memory limits with more than that – so we had to do some things to cut it down.

![blow that shit up](../../assets/3840a9755318077b.jpg)


*New PC shadebob record*

The first idea was “static particles”. The idea was, don’t do all the simulation and sorting the particles go through; just use the position and colour textures that were pregenerated for emission from a mesh, and pass them straight to the particle renderer. The particles could be pre-sorted in that texture for a rough camera direction so it looked alright. This obviously slices the amount of work done per frame a lot. The particles would be static though, but we could use displacement mapping effects (see later) to add some movement. We could also fake them fading in and out for lifetime cycles.

This trick bought us a lot of the time back; we could actually render the scene with this and get some sort of sensible framerate. But we didn’t want a static scene, we wanted to explode the buildings. So I devised a scheme of smoke and mirrors, whereby a building is static particles until it explodes, and then switches seamlessly to a proper particle system. Buut, you cant very well keep them all as particle systems after explode because it wastes loads of VRAM, which we’re already pushing too hard; so I wait until the explosion gets almost static and then switch them to an imposter by rendering them to a texture.

**Displacement Mapping**

Displacement mapping was used to add a per-frame offset to particle positions. This is done at render time only; well, not actually in the vertex shader, but as a pre-pass just before the render which processes the position buffer. It’s means it’s a temporary operation – it doesn’t have to persist to the next frame so it’s not part of the simulation, so the results don’t get stored and eat memory. So it works on static particles like on the street scene, which is ideal because we needed to add some movement there.

I added a bunch of operators – audio-based FFT modifiers, perlin noise movement modifiers, and things using images. We used it for some pulsing audio effects and a few other bits and pieces. Simple but oh, so effective.

**Depth of field**

Jani came up with this and it worked out a total treat. The idea is that we had so many particles that we could achieve a depth of field look just by randomising the positions a bit at render time (in vertex shader), where the randomness is controlled by the distance from focus. It took a fair few goes for him to explain it to me in a way that I understood, but once we got there I added it and it totally worked – it looked great. We could use it for focus pulls, “blurring out” shots and so on.

![ceasefire](../../assets/effd70766379e6a4.jpg)


*Particle randomisation for depth of field*

**Distance fields**

The subject of collisions with particles against meshes had come up before. Like that of real particle fluids – i.e. SPH – or rigid bodies or meshing, it usually get met with “in realtime? fuck off” or “yea.. I bet in 5 years we’ll be doing that” or “I’ll get to it when I’m done adding the radiosity solver” or some other smartass coder vs artist remark. Like what we used to say about shadows in the 90s. Of course, those arguments always end up evaporating because it actually gets done in the end when someone comes up with a practical, simple, workable way of doing it. And so it is here. All the hype about distance fields made me get around to writing a proper mesh to signed distance field conversion routine for some effect or other, and I realised it would make perfect sense to use for particle collisions. With meshes.

It’s a pretty simple routine; get the particle position in the space of the distance field, see if it’s inside, work back to find the 0 contour and the field normal at the hit point and then do something. Like move the particle and set some bounce velocity. So I did it and we used it with the tidal wave scenes, and it was great! Particles colliding with logos, with 3d scenes, and so on.

Well, it *would* have been great if the routine had worked. It didn’t; the mesh to distance field conversion was broken, so parts of the field were all wrong and it produced all kind of funny results. We managed to fudge the effect enough to get through the demo but it wasn’t until months later that I realised the mistakes and made something that really worked properly. In the demo it works in a few places but it’s not quite what it should have been.. so you get a few splashes off the logo and some collisions with what basically ended up as boxes in the subway scene.

The good news is I fixed it since, and it’s brilliant. So many applications for it; although the real challenge is in getting an accurate signed distance field of an arbitrary complex mesh efficiently in the first place, and that was what took so long to solve. It probably deserves a whole article on it’s own so let’s leave it there.

**Water **

I don’t know how this came about, but someone – might have been me actually – had the idea of using an ocean water effect and making the particles follow it. That water routine is so old. I’ve had it working since about 2003 and never actually used it in a demo, although it was planned for a couple and didn’t make it. It’s the implementation of Tessendorf’s FFT-based ocean water simulation, and it gives you a nice realistic ocean water heightfield which people usually use for meshes. I remember at the time I wrote it it worked fast on something like 32×32 or 64×64 grids on a PC CPU (due to the inverse 2D FFT you need to do), which wasn’t all that good looking. Since then Caspar did one on the PS3 running on SPU which ran at 256×256 if I remember right; fortunately PC CPUs caught up and now I can run it at a decent resolution pretty comfortably. If you want to know how the ocean routines work, google Tessendorf FFT ocean water and you’ll no doubt be presented with a load of material.

![water](../../assets/4c790d976922b68d.jpg)


*Original version of the water effect*

![ceasefire](../../assets/34704dfacf6c70b5.jpg)


*The water in the subway scene, later*

That was the first step; but then we started messing with it. We had a subway scene where we wanted to fill it with water and make it look like a wave was crashing through it. In an ideal (fantasy) world that would be done with proper fluid dynamics; I thought it’d be better (i.e. achieveable) if we faked it by taking the ocean effect and applying some magical space modifier to it to warp it into the shape of a wave. Simple.. a wave curl is a bit like some warped bell curve shifted and curled around by a twist / vortex equation. Right? Except somehow I was attempting to do this really late at night not all that long before the deadline, and I just couldn’t get it for ages and ages. GCSE maths is hard.

![ceasefire](../../assets/270a29f2db31ed6a.jpg)


*The subway scene*

**Post Processing**

I have to quickly mention the post processing effects – well, *effect* – that we used to make the screen all break up and look like a broken video recording. A lot of people moaned about it, some liked it. Personally I love it**. **It’s a combination of a load of different small things which go together to make something cool. We mix between a load of distortions using sinewaves and noise – some on scanlines, some on blocks; stretching, offseting and flipping the screen; and then this frame-holding effect where we keep a history of a few frames and randomly hold them or jump between them for a little while. There’s something really satisfying about taking a scene you’ve spent ages lovingly crafting, and then messing it up on purpose.


So there it is – we tried to make plans, it didn’t work out, and we made something much quicker instead. I’m really glad I got to work with Hunz, and I’m happy with some of the routines that were put together pretty fast. Demo compos, like war, can be the source of great innovation and technical advancement – if things have to get done, they get done. Yep, demo compos are a lot like war actually. Except you can watch them with a few beers in the grandstand of a hockey arena, not on CNN.

I happened to do a seminar at Assembly which is [here](http://vimeo.com/14458079) – if you want to watch 50 minutes of me discussing how we made our recent demos and at the same time being a cocky little shit. Go on, you know you want to.

*Coming soon: all the new things we’ve been doing between when the content of this blog post was actually fresh and relevant, and now..*

Really nice write up! Looking forward to more like it, both write ups and amazing demos

Comment by Joakim Dahl — February 25, 2011 @ 3:27 pm

Thanks! I aim to be able to play with all this things in… about 10 years 😉

Comment by Mr.doob — February 26, 2011 @ 2:44 am

>although the real challenge is in getting an accurate signed distance field of an arbitrary complex mesh efficiently in the first place

I would LOVE to hear about that, I’ve tried to tackle that problem in the past and was not really happy with the results.

The part with the buildings exploding into particles was really awesome. However I found the demo overall very painful to watch due to the tearing effect and constant stuttering. I actually had to watch the end again on youtube to make sure it wasn’t my machine dying.

I really appreciate you sharing about all the techniques you developed, including where they fell apart. Huge respect!

Comment by talden — February 26, 2011 @ 4:06 am

Great write up and great production!

Comment by Sam Izzo — February 26, 2011 @ 5:13 am

[…] you love reading about process then you should stop and look at this page. Smaash has done a wonderful job about the challenges in coding a demo like […]

Pingback by hunz » Blog Archive » Best Soundtrack Nominee — February 26, 2011 @ 5:29 am

The fire simulation was from the paper “Directable, high-resolution simulation of fire on the GPU” wasn’t it? I’m pretty disappointed if it was as incomplete as you mention, it looked quite interesting…

Comment by G — February 26, 2011 @ 5:41 pm

thats it. wasn’t that it was incomplete, more that the implementation requires a lot of tweaking. 🙂

Comment by directtovideo — February 26, 2011 @ 5:43 pm