---
title: Why Raytracing won't simplify AAA real-time rendering.
url: https://c0de517e.blogspot.com/2020/12/why-raytracing-wont-simplify-aaa-real.html
published: '2020-12-27'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

*"The big trick we are getting now is the final unification of lighting and shadowing across all surfaces in a game - games had to do these hacks and tricks for years now where we do different things for characters and different things for environments and different things for lights that move versus static lights, and now we are able to do all of that the same way for everything..."*

Who said this?

Jensen Huang, presenting NVidia's RTX?

Not quite... John Carmack. In 2001, at Tokyo's MacWorld, showing Doom 3 for the first time. It was though on an NVidia hardware, just a bit less powerful than today's 20xx/30xx series. A GeForce 3.

|

[YouTube](https://www.youtube.com/watch?v=80guchXqz14)for a bit of nostalgia.And of course, the unifying technology at that time was stencil shadows - yes, we were at a time before shadowmaps were viable.

Now. I am not a fan of making long-term predictions, in fact, I believe there is a given time horizon after which things are mostly dominated by chaos, and it's just silly to talk about what's going to happen then.

But if we wanted to make predictions, a good starting point is to look at the history, as history tends to repeat. What happened last time that we had significant innovation in rendering hardware?

Did compute shaders lead to simpler rendering engines, or more complex? What happened when we introduced programmable fragment shaders? Simpler, or more complex? What about hardware vertex shaders - a.k.a. hardware transform and lighting...

And so on and so forth, we can go all the way back to the first popular accelerated video card for the consumer market, the 3dfx.

Surely it must have made things simpler, not having to program software rasterizers specifically for each game, for each kind of object, for each CPU even! No more assembly. No more self-modifying code, s-buffers, software clipping, BSPs...

No more crazy tricks to get textures on screen, we suddenly got it all done for us, for free! Z-buffer, anisotropic filtering, perspective correction... Crazy stuff we never could even dream of is now in hardware.

Imagine that - overnight you could have taken the bulk of your 3d engine and deleted it. Did it make engines simpler, or more complex?

Our shaders today, powered by incredible hardware, are much more code, and much more complexity, than the software rasterizers of decades ago!

Are there reasons to believe this time it will be any different?

**Spoiler alert: no.**

At least not in AAA real-time rendering. Complexity has nothing to do with technologies.

Technologies can enable new products, true, but even the existence of new products is always about people first and foremost.

The truth is that our real-time rendering engines could have been dirt-simple ten years ago, there's nothing inherently complex in what we got right now.

Getting from zero to a reasonable, real-time PBR renderer is not hard. The equations are there, just render one light at a time, brute force shadowmaps, loop over all objects and shadows and you can get there. Use MSAA for antialiasing...

Of course, you would need to trade-off performance for such relatively "brute-force" approaches, and some quality... But it's doable, and will look reasonably good.

Even better? Just download Unreal, and hire -zero- rendering engineers. Would you not be able to ship any game your mind can imagine?

The only reason we do not... is in people and products. It's organizational, structural, not technical.

We like our graphics to be cutting edge as graphics and performance still sell games, sell consoles, are talked about.

And it's relatively inexpensive, in the grand scheme of things - rendering engineers are a small fraction of the engineering effort which in turn is not the most expensive part of making AAA games...

In AAA is perfectly ok to have someone work for say, a month, producing new, complicated code paths to save say, one millisecond in our frame time. It's perfectly ok often to spend a month to save a tenth of a millisecond!

Until this equation will be true, we will always sacrifice engineering, and thus, accept bigger and bigger engines, more complex rendering techniques, in order to have larger, more beautiful worlds, rendered faster!

It has nothing to do with hardware nor it has anything to do with the inherent complexity of photorealistic graphics.

We write code because we're not in the business of making disruptive new games, AAA is not where risks are taken, it's where blockbuster productions are made.

It's the nature of what we do, we don't run scrappy experimental teams, but machines with dozens of engineers and hundreds of artists. We're not trying to make the next Fortnite - that would require entirely different attitudes and methodologies.

And so, engineers gonna engineer, if you have a dozen rendering people on a game, its rendering will never be trivial - and once that's a thing that people do in the industry, it's hard not to do it, you have to keep competing on every dimension if you want to be at the top of the game.

**The cyclic nature of innovation.**

Another point of view, useful to make some prediction, comes from the classic works of Clayton Christensen on innovation. These are also mandatory reads if you want to understand the natural flow of innovation, from disruptive inventions to established markets.

One of the phenomena that Christensen observes is that technologies evolve in cycles of commoditization, bringing costs down and scaling, and de-commoditization, leveraging integrated, proprietary stacks to deliver innovation.

In AAA games, rendering has not been commoditized, and the trend does not seem going towards commoditization yet.

Innovation is still the driving force behind real-time graphics, not scale of production, even if we have been saying for years, perhaps decades that we were at the tipping point, in practice we never seemed to reach it.

We are not even, at least in the big titles, close to the point where production efficiency for artists and assets are really the focus.

It's crazy to say, but still today our rendering teams typically dwarf the efforts put into tooling and asset production efficiency.

We live in a world where it's imperative for most AAA titles to produce content at a steady pace. Yet, we don't see this percolating in the technology stack, look at the actual engines (if you have experience of them), look at the talks and presentations at conferences. We are still focusing on features, quality and performance more than anything else.

We do not like to accept tradeoffs on our stacks, we run on tightly integrated technologies because we like the idea of customizing them to the game specifics - i.e. we have not embraced open standards that would allow for components in our production stacks to be shared and exchanged.

I do not think this trend will change, at the top end, for the next decade or so at least, the only time horizon I would even care to make predictions.

I think we will see a focus on efficiency of the artist tooling, this shift in attention is already underway - but engines themselves will only keep growing in complexity - same for rendering overall.

We see just recently, in the movie industry (which is another decent way of "predicting" the future of real-time) that production pipelines are becoming somewhat standardized around common interchange formats.

For the top studios, rendering itself is not, with most big ones running on their own proprietary path-tracing solutions...

**So, is it all pain? And it will always be?**

No, not at all!

We live in a fantastic world full of opportunities for everyone. There is definitely a lot of real-time rendering that has been completely commoditized and abstracted.

People can create incredible graphics without knowing anything at all of how things work underneath, and this is definitely something incredibly new and exciting.

Once upon a time, you had to be John friggin' Carmack (and we went full circle...) to make a 3d engine, create Doom, and be legendary because of it. Your hardcore ability of pushing pixels made entire game genres that were impossible to create without the very best of technical skills.

Today? I believe a FPS templates ships for free with Unity, you can download Unreal with its source code for free, you have Godot... All products that invest in art efficiency and ease of use first and foremost.

Everyone can create any game genre with little complexity, without caring about technology - the complicated stuff is only there for cutting-edge "blockbuster" titles where bespoke engines matter, and only to some better features (e.g. fidelity, performance etc), not to fundamentally enable the game to exist...

And that's already professional stuff - we can do much better!

Three.js is the most popular 3d engine on github - you don't need to know anything about 3d graphics to start creating. We have Roblox, Dreams, Minecraft and Fortnite Creative. We have Notch, for real-time motion graphics...

Computer graphics has never been simpler, and at the same time, at the top end, never been more complex.

**Conclusions**

AAA will stay AAA - and for the foreseeable future it will keep being wonderfully complicated.

Slowly we will invest more in productivity for artists and asset production - as it really matters for games - but it's not a fast process.

It's probably easier for AAA to become relatively irrelevant (compared to the overall market size - that expands faster in other directions than in the established AAA one) - than for it to radically embrace change.

Other products and other markets is where real-time rendering is commoditized and radically different. It -is- already, all these products already exist, and we already have huge market segments that do not need to bother at all with technical details. And the quality and scope of these games grows year after year.

This market was facilitated by the fact that we have 3d hardware acceleration pretty much in any device now - but at the same time new hardware is not going to change any of that.

Raytracing will only -add- complexity at the top end. It might make certain problems simpler, perhaps (note - right now people seem to underestimate how hard is to make good RT-shadows or even worse, RT-reflections, which are truly hard...), but it will also make the overall effort to produce a AAA frame bigger, not smaller - like all technologies before it.

We'll see incredible hybrid techniques, and if we have today dozens of ways of doing shadows and combining signals to solve the rendering equation in real-time, we'll only grow these more complex - and wonderful, in the future.

Raytracing will eventually percolate to the non-AAA eventually too, as all technologies do.

But that won't change complexity or open new products there either because people who are making real-time graphics with higher-level tools already don't have to care about the technology that drives them - technology there will always evolve under the hood, never to be seen by the users...

## 6 comments:

The best take I have seen on graphics trends in the industry that I have seen in awhile!

I agree. In the feature VFX and animation world, the transition from scanline renderers to physically accurate global illumination ray tracers has allowed much more accurate modeling of light behavior and simplified the generation of realistic images but the expectations of the volume and quality of produced content have also increased. Although the nature of progress dictates that we will keep pushing the scale of what can be made, successful content requires that design and technology are in line with each other. Art doesn't get simpler, it evolves and reflects what is possible. Ultimately, it succeeds only when we can relate to it on a human level and that has nothing to do with the tool, even if generally artists are drawn to the potential of new technologies.

I think the point of raytracing is that it unifies under one umbrella all the disparate hacks needed to make different facets of light transport work and it can be an enabling technology. Once the magic grail of realtime path tracing is enabled by having raytracing on hardware the advantages are obvious, in example:

-no need for specialized light types, all emissive geometry can *literally* be a light, and correct soft shadows are just a side effect.

-dynamic/destructible worlds can be lit with correct global illumination: indirect illumination is hard, and probe-based solutions (complemented by ambient occlusion approximations) leave a lot to be desired against even a single bounce correct solution.

-in short, light and materials tend to behave in a more realistic way, which means the way to achieve a vision is much more intuitive for an artist.

-the points above are just about realistic lighting quality but, in more general terms, correctly modeling reflections and refractions could simply open up game design ideas that are currently out of reach.

As pointed out above, on the artistic side less hacks are necessary and artists can focus on producing content instead of spending a good portion of their time figuring out how to realize their ideas or simply working around limitations: I've seen this happen in the offline rendering world when the transition from old reyes renderers (depth/deep map/brickmap preprocessing anyone?) to path tracers led to a higher volume of content, at higher quality, being produced by the same number of artists.

In the end we are moving towards the creation of bigger, more intricate and believable worlds, and if we use what raytracing gives us, we can get there faster and with less pain.

There is no question that RT is the ultimate solution to the rendering equation, I think we have decades of research proving it.



My articles is not against RT nor against progress - it is only dispelling an imho naive idea that RT will make our engines simpler - as most of the complexity has nothing to do with anything related to this or that technology.

Also, we could go into technical reasons why RT stuff is not easy at all, not even "simple" things like pure RT shadows are actually simple (see the recent presentation on RT shadows in COD:CW for example - research.activision.com) - but this would be besides the point.

Absolutely: don't get me wrong, I'm not claiming that raytracing will simplify development. Raytracing is a paradigm shift that will require finding the efficiencies we now have after ~25 years of rasterization, only under a different umbrella that is

conceptually more unified. In the end it's not like development stops just because this new technology allows us to get closer to doing the correct thing: the need to do it more efficiently will always be there, if not only for the fact that the possibilities enabled by it will trigger a demand for more complex content. It's the old adage about the fact that, while Moore's law should have in principle minimized our rendertimes, in practice rendertimes have remained pretty much the same (if not grown longer), just because we throw more stuff (to be calculated with less compromises) to the computer.Exciting times to be part of.

I think we could look outside to other tech trends. Sound, for example. Sound in games was very hardware constrained at first. In the 80's we had chips with basically 3 or 4 oscillators, and the best musicians were also programmers, playing with register to max out all they could from the chip. Fast forward to 90's, we had FM synths that were horrible to program. So much so that most musician were using the default instrument presets. Still, the best musicians would do things like using the sound effect channel to use sampled drums instead of faking them with FM.


Then we got MIDI which sounded better (by default) but had fixed instruments. Then at some point we started streaming real music off CDs!

It sounded much better, but dynamic music (like you'd hear in Monkey Island) was now totally impossible. You would have to wait 5-10 years for it to come back.

In the mean time, some soundcards started offering special hardware accelerated reverbs (EAX) before getting totally obsolete.

Nowadays, nobody cares about dedicated soundcards. Everything is done on the CPU. Even AAA games use third party tools like Fmod or Wwise to add effects, mix the sounds, etc.

Back to rendering. I see a (far, far) future where we'll stop focussing so much on implementation details, and start using the general approach for everything. To follow my previous analogy, my laptop is probably still able to generate a very pure 440hz pulsewave. But no one will play with registers and ports to make that sound, it's much easier to send a 44100khz waveform containing the data of a 440hz pulse. At some point raytracing will get cheap enough that we won't care about details and use it for everything, including 2D GUIs! And the chip makers will actually ditch the rasterizing logic to keep the costs low.

Post a Comment