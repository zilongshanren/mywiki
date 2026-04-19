---
title: A Data-Oriented, Data-Driven System for Vector Fields - Part 1
url: https://bitsquid.blogspot.com/2012/09/a-data-oriented-data-driven-system-for.html
author: Niklas
published: '2012-09-17'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

A *vector field* is a function that assigns a vector value to each point in 3D space. Vector fields can be used to represent things like *wind* (the vector field specifies the wind velocity at each point in space), water, magnetism, etc.

To me, wind is the most interesting use case. I want a system that can be used for physics (trees, tumble weed, paper cups), particles (leaves, sparks, smoke) and graphics (grass). I also want the system to be capable of handling both global effects (wind blowing through the entire level) and local effects (explosions, air vents, landing helicopters, rising hot air from fires, etc). But I don't want to limit the system to *only* handling wind. I imagine that once the system is in place, it could be put to other interesting uses as well.

There are a number of things that make this an interesting non-trivial design challenge:

Vector fields represent a global shared state. All systems (particles, physics, etc) should react to the same wind. This can create strong couplings between unrelated systems, which we want to avoid.

The system must be fast. We want to be able to make large particle effects that are affected by wind. As a design goal, let's say that it should be able to handle at least 10 000 queries / frame.

As stated above, the system must be flexible enough to handle both global wind and a large variety of different local effects (air vents, fans, etc).


I'll outline the system in a series of articles. Let's start by thinking a bit about how we can represent the vector field in a way that allows for fast queries.

## 1. Use a functional representation

Storing the vector value for every point in 3D space at a decent resolution would require huge amounts of memory. It would also be very expensive to update. If we wanted to change the global wind direction, we would have to loop over all those points and change the value.

So, instead, we will use a functional representation. We will express the field as some closed function *F(p, t)* that gives us the field vector at point *p* in space at the time *t*.

For example, we could express a global wind that oscillates in the x-direction as:

`F(p, t) = Vector3(sin(t), 0, 0)`

The closed function form allows us to evaluate the vector field at any point in space and time.

Note that even with a functional form as the main representation, we can still interact with grid based representations. For example, we can render some section of the *F(p, t)* function to a texture for use on a GPU. Similarly, if we have some grid based wind data that we want to add to the simulation, we could use that as part of the *F(p, t)* expression:

`F(p, t) = Vector3(sin(t), 0, 0) + sample_grid(grid, p)`

## 2. Ignore the time coordinate

The vector field function *F(p, t)* is a function of both space *and* time. The wind varies throughout the level and if we look at any one point, the wind at that point varies over time.

But in practice, we treat the *p* and *t* coordinates very differently. We start at some time *t_0* and then evaluate *F(p, t_0)* for thousands of different *p* values. Then we move on to *t_1* and do the same thing.

We can make use of the fact that *t* remains constant for a large number of evaluations to simplify the function. For example at *t=0.5* the function:

`F(p, t) = sin(p.x) * sin(p.y) * cos(t)`

simplifies to:

`G(p) = sin(p.x) * sin(p.y) * 0.8776`

which is cheaper to evaluate.

Taking this approach a step further, it makes sense to split our system in two parts -- a high level system that knows about time and every frame produces a new *G(p)* for the current time, and a low level system that ignores time completely and just computes *G(p)*. Since the high level system only runs once per frame it can afford to do all kinds of complicated but interesting stuff, like constant folding, optimization, etc.

For the low level system we have reduced the problem to evaluating *G(p)*.

## 3. Express the field as a superposition of individual effects

To make it possible for the field to contain both global effects (world wind) and local effects (air vents, explosions) we express it as a superposition of individual effect functions:

`G(p) = G_1(p) + G_2(p) + ... + G_n(p)`

Here *G_i(p)* represents each individual effect. A base wind could be expressed as just a constant:

`G_0(p) = Vector3(2.1, 1.4, 0)`

A turbulence function could add a random component

`G_1(p) = turbulence(seed, p, 4)`

An explosion effect could create a wind with a speed of 100 m/s outwards from the center of the explosion in a sphere with radius 4.0 meter around the explosion center:

`G_2(p) = sphere(p,c,4) * normalize(p-c) * 100`

Here *sphere(p,c,4)* is a spherical support function that defines the range of the effect. It is *1* if *||p - c|| <= 4.0* and *0* otherwise.

Note again that we have stripped out the time component. At the higher level, this might be an expanding sphere with decreasing wind speeds, but at the low level we only care what it looks like at this instance.

Similar functions can be added for other local effects.

## 4. Use the AABB to cull local fields

If we have a lot of local effects (explosions, etc), evaluating *G(p)* will be pretty expensive.

We can reduce the cost by only evaluating the local effects that are close enough to our particle system to matter.

I.e., instead of evaluating *G(p)* for all particles, we first intersect the AABB of each *G_i(p)*'s support with the AABB of our particle system.

That gives us a simpler function *G'(p)* that we can then evaluate for each particle.

If we wanted to, we could use the wavelength of the field for further simplifications. If the scale at which a field effect changes is much larger than our AABB, we can replace that effect with a Taylor series expansion. Similarly, if an effect oscillates at a scale much smaller than the size of our particles, we can replace it with its average value.

## Next time

Next time I will look at how we can efficiently evaluate arbitrary functions, such as:

`G(p) = Vector3(1,1,0) + turbulence(seed, p, 2) + sphere(p, c, 4)`

for a huge number of particle positions *p*.

This has also been posted to [The Bitsquid blog](http://bitsquid.blogspot.com).

Hi Niklas,

ReplyDeleteI don't know much about water or air flows but... Can wind blow perturbations realistically be expressed "as a superposition of individual effect functions" ? It seems more complicated than that to be realistic imo.

That being said, I think your system still provide a efficient way to simulate forces in a simple way. Thanks for this article =)

Another technique is to use procedural noise functions to define the flow field influence at an arbitrary sample location. If you rotate the gradient vectors of Perlin Noise, or Simplex noise, that's relatively cheap. Another way is to use an analytically derived integral of the noise itself -- commonly used in flow noise.




ReplyDeleteI added all of these noise functions to an OpenCL demo I wrote a while back. Perhaps these will be useful:

https://developer.apple.com/library/mac/#samplecode/OpenCL_Procedural_Grass_and_Terrain_Example/Listings/grass_kernels_cl.html#//apple_ref/doc/uid/DTS40008186-grass_kernels_cl-DontLinkElementID_13

-- dg

@Lythom This is not intended to be a full physical water or air simulation (i.e. solving the Navier-Stokes equations, collision, etc). Such simulations are really expensive... and not something you can expect to run over an entire level.



ReplyDeleteRather, you should see this as "animated" wind & water.

(Though if you really wanted to, you could run a physical simulation in some small part of the level, and plug the result of that in, as one of the effects in G(p).)

@Derek Yes, the turbulence() function that I hint at in the code examples is intended to be a Perlin-noise function (the third argument is the number of octaves).


ReplyDeleteThe idea of this is to combine noise with other effects, such as scripted wind, and gameplay events, such as explosions.

Niklas -- you missed my point. Most noise functions, including multi-octave turbulence returns a scalar value. The ones I offered provide vector values based on the derivate of the noise.

ReplyDeleteAh, sorry, a bit too quick on the keyboard.


ReplyDeleteNot having thought about this much, my idea was just to use a separate noise function for each component (different seeds). Does using the gradient instead lead to "nicer noise" or is it just a performance improvement?

Using the analytical gradient of the noise provides coherent patterns (with each component matching the underlying scalar field), and it means you can directly combine the directional vector with the scalar value (eg, for velocity and intensity or relief mapping).



ReplyDeleteUsing separate noise functions will generate uncorrelated vectors -- useful for semi-random behaviour and domain distortion -- just another technique.

Both of these can be very useful.

This comment has been removed by the author.

ReplyDeleteThis comment has been removed by the author.

ReplyDeleteHi Niklas,




ReplyDeleteThere has been publications on using noise fields to compute divergence-free velocity fields, I suppose that's what Derek was talking about:

http://www.cs.cornell.edu/~tedkim/WTURB/wavelet_turbulence.pdf

they use wavelet noise, but really, the technique they describe can be applied to anything. (it is a bit expensive to compute on the CPU though, as it requires sampling the scalar noise six times, but produces nice results)

Hi Niklas,


ReplyDeleteInteresting read, have you considered caching the results of the calculation? perhaps by defining some kind of uniform grid to provide calculations from and then performing the calculation if it is requested, then caching N most recent calculations?

If considering a larger simulation area, I imagine it could help with particle systems that are localised into smaller subsets of the overall grid.

On the other hand, it could add lookup time in the cache.

Have you attempted it?

I haven't done that, but I've considered it. Especially for things like getting wind to interact with GPU-generated grass and similar things.

ReplyDeleteThat's such a nice information to share. Yellowstone Coat

ReplyDeleteThank you, I have recently been searching for information about this topic for ages and

ReplyDeleteyours is the best I have discovered so far.

Leather jacket

Fantastic goods from you, man. I've understand your stuff previous to and you're just too fantastic.

ReplyDeleteI actually like what you've acquired here.

Best Cargo Services Dubai to Pakistan

Glass Works Dubai

Both independent .net web designer and in-house specialists are presented to how .Net innovation can change how tech arrangements are made for organizations. Significant language for coding with .Net is C#. Regardless of whether we discuss a parttime net designer, a lesser net engineer independent, or a senior full-stack in-house expert run a mastery with C# because of it being object-situated, which exhibits prevalent usefulness, yet additionally upgrades progressed efficiency, by offering fast improvement arrangements. Different dialects are normal for use C++, F#, VB.Net>> .net developer part time

ReplyDeleteHello! Regardless of the size of your team, sooner or later you may need to hire new developers and grow your team. And at such a moment, I recommend that you take advantage of the software development staff expansion model. Our company will help you with this and go through this process with you! >> extension team


ReplyDeleteAt the present time, it is simply necessary to have an angular js developer in your company, but there are not always resources to support this developer! You can choose with us both one developer and a whole development department who will work remotely, which has a very positive effect on the cost of maintaining these specialists!

ReplyDeleteAre you a business owner or recruiter facing the challenge of finding real talent for a DevOps developer position? Then I can recommend you the following site cisco devops automation engineers, which will help you select the required number of real professionals in your field, according to any of your criteria and terms, and as a bonus for a very nice price.

ReplyDeleteHello to all entrepreneurs. What I know for sure is that not everyone is able to immediately understand why creating projects based on build operate transfer contract sample is so popular. And the answer is simple - because this way the project will definitely be successful and high-quality, which will help to improve the business and accelerate success.

ReplyDeleteThis comment has been removed by the author.

ReplyDeleteThis comment has been removed by the author.

ReplyDeleteThis article effectively outlines the numerous benefits of custom software development for businesses. The points are well-explained and easy to understand for readers. It highlights how tailored solutions can streamline processes, increase efficiency, and ultimately lead to a competitive advantage. A great read for those considering investing in custom software.

ReplyDeleteYour blog posts are always so informative and well-researched. I look forward to reading more in the future!

ReplyDelete