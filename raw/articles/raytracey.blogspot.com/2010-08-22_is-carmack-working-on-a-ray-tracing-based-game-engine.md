---
title: Is Carmack working on a ray tracing based game engine?
url: http://raytracey.blogspot.com/2010/08/is-carmack-working-on-ray-tracing-based.html
author: Sam Lapere
published: '2010-08-22'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[http://twitter.com/id_aa_carmack](http://twitter.com/id_aa_carmack)) seem to suggest:

# There has GOT to be a better way to exactly test triangle-in-AABB than what I am currently doing.

# Idea: dynamically rewrite tree structures based on branch history to linearize the access patterns. Not thread safe…

# The valuation strategy behind the Surface Area Heuristic (SAH) used in ray tracing is also adaptable for rasterization engines.

# It is often better to use a global spherical sampling pattern and discard samples behind a plane instead of local hemispheres.

# @Wudan07 equal area but not shape. Got a better non iterative one? Poisson disc for higher quality.

# To uniformly sample a sphere, pick sample points on the enclosing cylinder and project inwards. Archimedes FTW!

# I need to decide if I am going to spend some quality time with CUDA or Android. Supercomputing and cell phones, about equally interesting…

# @castano triangle intersection is 33% of the wall clock time and a trace averages 12 triangle tests, so gather SIMD tests could win some.

# Doing precise triangle tests instead of just bounds tests when building KD trees makes a large difference with our datasets.

# For our datasets, my scalar KD tree trace code turned out faster than the SSE BVH tracer. Denser traces would help SSE.

If Carmack's pioneering work still has the same impact and influence on the game industry as it had in the 90's, ray traced games could become the standard "soon" (which in id terms means about 5-8 years :-).

UPDATE: I wasted a couple of hours and transcribed the part of Carmack's keynote at Quakecon 2010, where he's specifically talking about raytracing (from

[http://www.youtube.com/watch?v=LOdfox80VDU&feature=related](http://www.youtube.com/watch?v=LOdfox80VDU&feature=related)time 3:17 ) English is not my mother tongue so there are some gaps here and there, this part is not about real-time raytracing, but about precomputing the lightmaps and megatextures with raytracing instead of rasterization:

"We were still having precision issues with shadow buffers and all this and that, and finally I just sort of bit the bullet and said “Alright, we’re on the software side, let’s just stop rasterizing, let’s just raytrace everything. I’m gonna do a little bit of rasterizing for where I have to, but just throw lots and lots of rays." And it was really striking from my experience how much better a lot of things got. There are a lot of things that we live with for rasterization as we do in games with making shadows, trying to get shadow buffers working right, finding shadow acné vs Peter Pan effect on here and this balance that never quite get as things move around. Dealing with having to vastly oversize this trying to use environment maps for ambient lighting. And these are the things that people just live and breathe in games, you just accept it, this is the way things are, these are the issues and things will always be like this just getting higher and higher resolution. But it was pretty neat to see a lot of these things just vanish with ray tracing, where the shadows are just, the samples are right. We don’t have to worry about the orientation of some of these things relative to the other things. The radiosity gets done in a much better way and there are far less artifacts. And as we start thinking about things in those terms, we can start thinking about better ways to create all of these different things. So that experience has probably raised in my estimation a little bit the benefit of raytracing in the future of games. Again, there’s no way it’s happening in this coming generation, the current platforms can’t support it. It’s an open question about whether it’s possible in the generation after that, but I would say that it’s almost a foregone conclusion that a lot of things in the generation after that will wind up being raytraced, because it does look like it’s going to be performance reasonable on there and it makes the development process easier, because a lot of problems that you fight with just aren’t there. There’s a lot of things that, yeah, it’s still you could go ahead and render five times or ten times as many pixels, but we’re gonna reach this point where our ten times as many pixels or fragment samples going to give us that much more benefit or would we really like to have all the local shadows done really really right and have better indirect ambient occlusion. Or you can just have the reflections and highlights go where they’re supposed to, instead of just having a crummy environment map that reflects on the shiny surfaces there. So, I can chalk that up as one of those things where I definitely learned some things in the last six months about this and it modified some of my opinions there and the funny coming back around about that is, so I’m going through a couple of stages of optimizing our internal raytracer, this is making things faster and the interesting thing about the processing was, what we found was, it’s still a fair estimate that the gpu’s are going to be five times faster at some task than the cpu’s. But now everybody has 8 core systems and we’re finding that a lot of the stuff running software on this system turned out to be faster than running the gpu version on the same system. And that winds up being because we get killed by Amdahl’s law there where you’re throwing the very latest and greatest gpu and your kernel amount (?) goes ten times faster. The scalability there is still incredibly great, but all of this other stuff that you’re dealing with of virtualizing of textures and managing all of that did not get that much faster, so we found that the 8 core systems were great and now we’re looking at 24 thread systems where you’ve got dual thread six core dual socket systems (?) it’s an incredible amount of computing power and that comes around another important topic where pc scalability is really back now where we have, we went through sort of a ..."


## 3 comments:

Awesome write-up, thanks!


Jerry

Things are closer than we thought.


Today JC posted a tweet:

That went pretty smoothly, I have a real-time OpenCl / OpenGL ray tracing demo now. I can probably get it running with textures tonight.

@ Anonymous: Thanks, I've read it as well. It's pretty exciting when the Godfather of rasterized 3D games suddenly decides to investigate real-time ray tracing for use in games ;-) Carmack still has a significant influence (maybe even the most) on the graphics rendering community, so this bodes very well!

Post a Comment