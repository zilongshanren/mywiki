---
title: Screenshot Saturday 168
url: https://etodd.io/2014/04/26/screenshot-saturday-168/
published: '2014-04-26'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Screenshot Saturday 168

This week was a ton of performance optimizations and graphics upgrades.

Cascading shadow maps! Basically that means all the shadows are much sharper. It was surprisingly easy to implement and barely impacts performance.

Here's a screenshot showing off the new shadows, plus a new character modeling experiment. Just testing things out for now. What do you think?

Turns out, Blender has something called Rigify that can automatically generate an absolutely kick butt IK rig for your character, complete with blend weights for skinning. It's not perfect, especially when there are separate disconnected pieces (eyeballs, for example), but the few problem areas are easy to correct manually. Here's the character animated with the default calculated weights. I haven't touched them at all yet:

That animation is a grand total of three keyframes. I just have to move one IK control, and the rest of the body responds naturally. The rig I have now is entirely FK, meaning to get the animation above I would have had to manually rotate the joints of the legs and arms to get the hands and feet to stay planted. This is one reason the placeholder animations are so terrible. Just having an IK rig means animations will be instantly better.

Again, this is all very experimental but I think it could save a ton of time. Rigging and animation both seem like much easier problems to tackle now. If I continue with this idea I'll definitely post an article about the whole Rigify process, because there is a huge lack of documentation on the subject.

What else is new? Oh, one of my players built this insane structure using the wallrun mechanic... it was slightly exploitable. I went ahead and patched that.

More info about the performance optimizations that happened this week:

My deferred renderer now uses material IDs rather than storing specular properties for every pixel. Now I can cut the G-buffer down to 96 bits spread across three render targets:

**Render Target 1**

Albedo - RGB, 8 bits per channel

Material ID - 8 bit index

**Render Target 2**

Normal X and Y - 8 bits per channel

Motion blur velocity X and Y - 8 bits per channel

**Render Target 3**

Depth - 16 bit float

Normal Z - 16 bit float

Nice things about this setup:

- I can store normals in world space, which is fast, easy, and artifact-free.
- Storing all three dimensions of the normal (as opposed to storing only two and reconstructing the third) is nice because I can encode an extra scalar by multiplying the normal by it. The lighting system can recover that scalar later on by taking the length of the normal. Right now I just use zero-length normals for rain drops, which accept lighting from any direction rather than doing any kind of Lambert shading.
- Lighting and objects with alpha transparency go into 64-bit floating point buffers later on, so we still get full HDR.
- I can come up with a bunch of different material properties that I can bind to material IDs without adding bits to the G-buffer. Right now I only have two: specular exponent and intensity.

That's it for this week! Thanks for reading.