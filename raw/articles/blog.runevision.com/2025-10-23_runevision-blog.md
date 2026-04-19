---
title: runevision blog
url: https://blog.runevision.com/2025/
published: '2025-10-23'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

I've actually been working on a cool erosion technique I'll post about later, but during some downtime, I had an impulse to see if I could make a basic hair shader that doesn't require any specially made meshes or textures. I ended up making *three* hair shaders.

The shapes below are just standard Unity spheres and capsules and only [a simple normal map](https://www.filterforge.com/filters/9157-normal.html) is used; no other textures. The hair strands follow the vertical V direction of the UV map of the mesh.

![](../../assets/829fa84fff4831dd.png)

I also found some characters on the Asset Store and tried changing the hair material to use my shader. Luckily they all already had hair aligned vertically in the UV map (although not 100% for wavy/curly hair, which compromises my shader slightly).

You can see a video here with the shader in action on both basic shapes and characters:

I ended up making these three hair shader implementations:

- Full multisample hair shader
- Specular multisample hair shader
- Approximation hair shader

All three shaders support a diffuse map, a normal map, and properties for color, smoothness, and normal map strength. The diffuse map alpha is used for cutout transparency.

The strategy was to start with Unity's Standard shading model (based on BRDF physically based shading), but modify it to simulate anisotropic shading, that is, to simulate that the surface is made from lots of little parallel cylinders rather than a flat surface.

This approach ensures that the hair shader looks consistent with other materials based on Unity's Standard shader (and other Surface shaders) under a wide variety of lighting conditions and environments.

### 1) Full Multisample Hair Shader

I started out doing brute force anisotropic shading, running the Unity's physically based BRDF shading function up to 50 times and taking a weighted average of the sample colors.

The normals in those samples are spread out in a 180 degree fan of directions centered around the original normal, using the hair strand direction as the axis of rotation. The final color is a weighted average of the samples.

Much of the "magic" of the simulated anisotropic shading comes from the way the samples are weighted in the two multisample shaders (and emulated in the third).

![](../../assets/aa164ca6b415cc5c.png)

The weight of each sample is a product of two functions:

- The cosine of the angle between the original and modified normal. This is because strands of hair occlude other strands of hair when the hair "surface" is seen from the side, and the parts of strands that face outward tend to be less occluded.
- The cosine of the angle between the modified normal and the view direction. This is because the part of the strand that's facing the camera takes up more of the view than parts that are seen at an angle.

Both cosines are clamped to a zero-to-one range before the two are multiplied.

With this weight function to base the weighted average on, the results looked surprisingly good. Of course, running the entire shading up to 50 times is not exactly the fastest approach, performance-wise.

### 2) Specular Multisample Hair Shader

I made a second implementation that reduces computations somewhat by only multi-sampling certain calculations, namely dot products with the normal, and most of the specular term of the lighting. The diffuse term, fresnel, and other calculations are performed only once. The result is nearly indistinguishable from the full multisample hair shader.

There is still a significant amount of calculations being performed up to 50 times though.

### 3) Approximation Hair Shader

Of course, non-brute force approaches to hair shading are possible too, but way harder to make look good. Still, I eventually came up with something fairly decent.

The third implementation does not perform multisampling but instead emulates the same result. The math formulas required for this were devised by means of a combination of partial understanding, intuition, and trial and error, while carefully comparing the results with the full multisample hair shader. As such, it's difficult to explain the details of the logic behind it with any exactness, but you can see the details in the shader source code.

### Closing thoughts

This was just a little experiment I did as a random side project. I haven't looked much at existing research on hair shaders, as I tend to not understand graphics papers very well. My impression is that this has less to do with the subject matter itself, and more to do with the manner in which it's explained.

The one research entry I did look at – [Hair Rendering and Shading by Thorsten Scheuermann](https://web.engr.oregonstate.edu/~mjb/cs557/Projects/Papers/HairRendering.pdf) – only shows the results on a complex multi-layered haircut model; not simple spheres like I used for testing, which makes it impossible to compare results meaningfully.

I'm not planning any further work on the hair shaders, but I've [released them as open source on GitHub](https://github.com/runevision/HairShader). If anyone makes changes or improvements to them – or just use them in a project – I'd love to hear about it.


I don't know if it's because I come from a supremely flat country, or in spite of it, but I love terrain with elevation differences. Seeing cliffs or mountains in the distance fills me with a special kind of calm. The game I'm currently working on, The Big Forest, is full of mountain forests too.

I've just returned from three weeks of vacation in Japan, and I had ample opportunities to admire and study views with layers upon layers of mountains in the distance. And while studying these views, something about the shades of mountains at different distances clicked for me that’s now obvious in retrospect. I'll get back to that.

Note: No photos here have any post-processing applied, apart from what light processing an iPhone 13 mini does out of the box with default settings. I often looked at the photos right after taking them, and they looked pretty faithful to what I could see with my own eyes.

![](../../assets/16607885ee5f03df.img)

![](../../assets/e8c7fb98ee771978.img)

### The blue tint of atmospheric perspective

A beautiful thing about mountains in the far distance is how they appear as colored shapes behind each other in various shades of blue. Sometimes it looks distinctly like a watercolor painting.

![](../../assets/fbb1732c7f02bc64.img)

In an art context, the blue tint that increases with distance is called *aerial perspective* or *atmospheric perspective* ([Wikipedia](https://en.wikipedia.org/wiki/Aerial_perspective)).

I've tried to capture this in The Big Forest too by making things more blue tinted in the distance. In terms of 3D graphics techniques, I implemented it by using the simple fog feature which is built into Unity and most other engines. By setting the fog color to blue, everything fades towards blue in the distance. It can produce a more or less convincing aerial perspective effect. Using fog for this purpose is as old as the fog feature itself. The [original OpenGL documentation](https://www.opengl.org/archives/resources/code/samples/advanced/advanced97/notes/node122.html) mentions that the fog feature using the exponential mode "can be used to represent a number of atmospheric effects", implying it's not only for simulating fog. For our purposes, let's call it the *fog trick*.

![](../../assets/890b0b072dab6727.png)

### Which color does things fade towards?

I long held a misconception that things in the distance (like mountains) get tinted towards whatever color the sky behind them has. In daytime when the sky is blue, the color of mountains approach the same blue color the further away they are. At sunset where the sky is red, the mountains approach that red color too. A hazy day where the sky is white? The mountains fade towards white too.

Of course, the sky is not a single color at a time. Even at its blueest, it's usually more pale at the horizon than straight above.

This raises a dilemma when using the fog trick. Set the fog color too close to the blue sky above, and the distant mountains appear unnatural near the pale horizon. But set the fog color to the pale color of the sky at the horizon, and the result is even worse: Some mountain peaks may then end up looking paler than the sky right behind them, and that looks very bad, since it never happens in reality.

![](../../assets/623acea640ac6ca5.png)

For a long time I wished Unity had a way to fade towards the skybox color (the color of the sky at a given pixel) rather than a single fixed color.

In practice, it's not too difficult to settle on a compromise color which looks mostly fine. It's just still not ideal, for reasons that will become clear later.

### Are more distant mountains more pale?

Now, while I was tweaking the fog color in my game and in general contemplating atmospheric perspective, I could see from certain reference photos I'd found on the Internet that mountains look paler at great distances. Not just paler than their native color – green if covered in trees – but also paler than the deep blue tint they appear with at less extreme distances.

This was counter-intuitive. How could the atmosphere tint things increasingly saturated blue up to a certain distance, but less saturated again beyond that point? Now, the thing is, you never know how random reference photos have been processed, and which filters might have been applied. For a while, I thought it simply came down to tone mapping.

Tone mapping is a technique used in digital photography and computer graphics to map very high contrasts observed in the real world (referred to as high dynamic range) into lower contrasts representable in a regular photograph or image (low dynamic range). For context, the sky can easily be a hundred times brighter than something on the ground that's in shadow. Our eyes are good at perceiving both despite the extreme difference in brightness, but a photograph or conventional digital image cannot represent one thing that's a hundred times brighter than another without losing most detail in one or the other.

If you try to take a picture with both sky and ground, the sky may appear white in the photo even though it looked blue to your eyes. Or if the sky appears as blue in the photo as it did to your eyes, then the ground may appear black. Tone mapping makes it possible to achieve a compromise: The ground can be legible while the sky also appears blue, but it's a paler blue in the photo than it appeared to your eyes. Tone mapping typically turns non-representable brightness into paleness instead.

So I thought: Distant mountains approach the color – and brightness – of the sky, so they may appear increasingly pale in photos simply because they're increasingly bright in reality, and the brightness gets turned into paleness by tone mapping.

However, while observing distant mountains with my own eyes on the Japan trip, it became clear that this theory just doesn't hold up.

### Revised theory

Some of my thinking was partially true. Distant mountains do take on the color of the sky, just in a bit different way than I thought. And tone mapping does sometimes affect the paleness of the sky and distant mountains.

But on this trip I had ample opportunity to study mountains layered at many distances behind each other. I could observe with my own eyes (no tone mapping involved) that they do get paler with distance. (It's not that I've never seen mountains in the distance with my own eyes before, but on previous occasions I guess I didn't think very analytically about the exact shades.) Furthermore I've taken a lot of pictures of it, where (unlike random pictures I find on the Internet) I've verified that the colors and shades look about the same in the pictures as they looked to my eyes in real life.

![](../../assets/53c4ceb3084d113f.png)

So here's what finally clicked for me:

Mountains transition from a deep blue tint in the mid-distance to a paler tint in the far distance for the same reason that the sky is paler near the horizon.

To the best of my current understanding, the complex scientific reason relates to how Rayleigh scattering ([Wikipedia](https://en.wikipedia.org/wiki/Rayleigh_scattering)) and possibly Mie scattering ([Wikipedia](https://en.wikipedia.org/wiki/Mie_scattering)) interact with sunlight and the human visual system, but the end result is this:

As you look through an increasing distance of air (in daytime), the appearance of the air changes from transparent, to blue, to nearly white. (Presumably this goes through a curved trajectory in color space).

- When you look at the sky, there's more air to look through near the horizon than when looking straight up, so the horizon is paler.
- Similarly, there's also more air to look through when looking at a more distant mountain compared to a less distant one, so the more distant one is paler.

A small corollary to this is that the atmospheric tint of a mountain can only ever be less pale than the sky immediately behind it, since you're always looking through a greater distance of air when looking just past the mountain than when looking directly at it.

This can be generalized, so it doesn't only work at daytime, but for sunsets too: Closer mountains are tinted similar to the sky further up, while more distant mountains are tinted similar to the sky nearer the horizon. In practice though, it's hard to find photos showing red-tinted mountains; much more common are blue-tinted mountains flush against the red horizon. Possibly the shadows from the mountains at sunset play a role, or perhaps the distance required for a red tint is so large that mountains are almost never far enough away.

I sort of knew the part about the horizon being paler due to looking through more air, but for some reason hadn't connected it to mountains at different distances. In retrospect it's obvious to me, and I'm sure lots of the readership of this blog were well aware of it, and find it amusing that I only found out about it now. On the other hand, I can also see why it eluded me for a long time:

- It's just not intuitive that a single effect fades things towards one color or another depending on the magnitude.
- It's hard to find good and reliable reference photos, and unclear how to interpret them given the existence of filters and tone mapping.
- The
[Wikipedia page on aerial perspective](https://en.wikipedia.org/wiki/Aerial_perspective)doesn't mention that the color goes from deeper blue to paler blue with distance. You could read the entire page and just come away with the same idea I had, that aerial perspective simply fades towards one color. - If you go deeper and read the Wikipedia pages on
[Rayleigh scattering](https://en.wikipedia.org/wiki/Rayleigh_scattering)and[Mie scattering](https://en.wikipedia.org/wiki/Mie_scattering), they don't mention it either. The one on Rayleigh scattering has a section about "Cause of the blue color of the sky", but it doesn't mention anything about the horizon being paler.

In fact, I've not yet found any resource that is explicit about the fact that the color of increasingly distant mountains go from deeper blue to paler blue. It's even hard to find any references that explain why the sky is paler near the horizon, and the random obscure [Reddit](https://www.reddit.com/r/askscience/comments/34pvyn/why_is_the_sky_lighter_close_to_the_horizon/) and [Stack Exchange](https://earthscience.stackexchange.com/questions/24623/why-does-earths-atmosphere-have-a-whiter-color-near-the-horizon) posts I did find did not agree on whether the paleness of the horizon is due to Rayleigh scattering or to Mie scattering.

I found and tinkered with [this Shadertoy](https://www.shadertoy.com/view/wlBXWK), and if that's anything to go by, the pale horizon comes from Rayleigh scattering, while Mie scattering primarily produces a halo around the sun. I don't know how to add mountains to it though.

All right, that was a lot of text. Here's another nice photo to look at:

![](../../assets/c8ec1cbe16b577d1.img)

I'm still not really certain of much, and you should take my conclusions with a grain of salt. I haven't yet found any definitive validation of my theory that mountains are paler with distance for the same reason the horizon is paler; it's just my best explanation based on my observations so far. I find it somewhat strange that it's so difficult to find good and straightforward information on this topic (at least for people who are not expert graphics programmers or academics), but perhaps some knowledgeable readers of this post can shed additional light on things.

One thing is pretty clear: An accurate rendition of atmospheric perspective (at great distances) cannot be achieved in games and other computer graphics by using the *fog trick*, or other approaches that fade towards a single color. I haven't yet researched alternatives much, but I'm sure there must be a variety of off-the-shelf solutions for Unity and other engines. I've learned that Unreal has a powerful and versatile Sky Atmosphere Component built-in, while Unity's HD render pipeline has a Physically Based Sky feature, which however seems problematic according to various forum threads. If you have experience with any atmospheric scattering solutions, feel free to tell about your experience in the comments below.

It's also worth noting though that the distances at which mountains fade from the deepest blue to paler blue colors can be quite extreme, and may not be relevant at all for a lot of games. Plenty of games have shipped and looked great using the *fog trick*, despite its limitations.

### Light and shadow

Let's finally move on from the subject of paleness, and look at how light and shadow interacts with atmospheric perspective.

Here are two pictures of the same mountains (the big one is the volcano Mount Iwate) from almost the same angle, at two different times. In the first, where the mountain sides facing the camera are in shadow, the mountains appear as flat colors. In the second you can see spots of snow and other details on the volcano, lit by the sun. The color of the atmosphere is also a deeper blue in the second picture, probably due to being closer to midday.

![](../../assets/795e50c08e489d41.img)

![](../../assets/b56509bfa188645d.img)

And here's a picture from Yama-dera (Risshaku-ji temple), where the partial cloud cover lets us see mountains in both sunlight and shadow simultaneously. This makes it very clear that mountain sides at the same distance appear blue when in shadow and green when in light. The blue color of the atmosphere is of course still there in the sunlit parts of the surface, but it's owerpowered by the stronger green light from the sunlit trees.

![](../../assets/d229e9ad5b522cac.img)

That's all the observations on atmospheric perspective I made for now. I would love to hear your thoughts and insights! If you'd like to see more inspiring photos from my Japan trip (for example from a mystical forest stairway), I wrote [another post about that](https://blog.runevision.com/2025/06/photos-from-inspiring-trip-in-japan.html).

### Resources for further study

Here are links to some resources I and others have come across while looking into this topic.

From my perspective, these resources are mostly to get a better understanding of the subject, and the theoretical possibilities. In practice, it's not straightforward to implement one's own atmospheric scattering solution in an existing engine. Even in cases where the math itself is simple enough, the graphics pipeline plumbing required to make the effect apply to all materials (opaque and transparent) is often non-trivial or outright prohibitive for people like me, who aren't expert graphics programmers.

- A simple improvement upon single-color fog is to use different exponents for the red, green, and blue channel. This can be used to have the tint of the atmosphere shift from blue to white with distance. There's example shader code for it in
[this post by Inigo Quilez](https://iquilezles.org/articles/fog/), though unfortunately it lacks images illustrating the effect. The post also covers how to fade towards a different color near the sun, and other effects. - Here's a 2020
[academic paper](https://sebh.github.io/publications/egsr2020.pdf),[video](https://www.youtube.com/watch?v=SW30QX1wxTY)and[code repository](https://github.com/sebh/UnrealEngineSkyAtmosphere)for the atmospheric rendering in Unreal, and here's the[documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/sky-atmosphere-component-in-unreal-engine). - Here's the
[documentation](https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition@17.3/manual/physically-based-sky-volume-override-reference.html)for Unity's Physically Based Sky. - A 2008 paper that gets referenced a lot is
[Precomputed Atmospheric Scattering](https://inria.hal.science/inria-00288758/en)by Bruneton and Neyret, with[code repository here](https://github.com/ebruneton/precomputed_atmospheric_scattering). Unity's solution is based on it, and it's cited and compared in Unreal's paper.


I've just returned from three weeks of vacation in Japan. Besides being great as a vacation – which was the only thing my partner and I planned for, really – it happened to also be inspiring for me as a game developer. I like to make games that take place at least partially in beautiful nature, give a sense of mystery and wonder that invites exploration, and that have environments that incorporate strong verticality. And in all of these respects, Japan delivers in spades.

![](../../assets/b5c6815dc11fdd51.img)


For my game [The Big Forest](https://runevision.com/multimedia/thebigforest/) I want to have creatures that are both procedurally generated and animated, which, as expected, is quite a research challenge.

As mentioned in my [2024 retrospective](https://blog.runevision.com/2025/01/2024-retrospective.html), I spent the last six months of 2024 working on this – three months on procedural model generation and three months on procedural animation. My work on the creatures actually started earlier though. According to my commit history, I started in 2021 after shipping [Eye of the Temple](https://runevision.com/multimedia/eyeofthetemple/) for PCVR, though my work on it prior to 2024 was sporadic.

Though the creatures are still very far from where they need to be, I'll write a bit here about my progress so far.

### The goal

I need lots of forest creatures for the gameplay of *The Big Forest*, some of which will revolve around identifying specific creatures to use for various unique purposes. I [prototyped the gameplay](https://blog.runevision.com/2024/10/procedural-game-progression-dependency.html) using simple sprites for creatures, but the final game requires creatures that are fully 3D and fit well within the game's [forest terrain](https://www.youtube.com/watch?v=VxMwggFQRQM).

![creatures from prototype → replace with 3D procedural creatures → put into procedural terrain](../../assets/59e611f419db45ec.jpg)


![creatures from prototype → replace with 3D procedural creatures → put into procedural terrain](../../assets/59e611f419db45ec.jpg)


Another year went by as an indie game developer and what do I have to show for it?

In [last year's retrospective](https://blog.runevision.com/2024/01/2023-retrospective-and-goals-for-new.html) I wrote that apart from working on my game The Big Forest in general, I had four concrete goals for 2024:

- Present my Fractal Dithering technique
- Release my Layer-Based ProcGen for Infinite Worlds framework as open source
- Wrap up and release The Cluster as a free experimental game
- Make better use of my YouTube channel

I ended up doing only two of those, but it was the two most important ones to me, so I'm feeling all right with that.

### Release of LayerProcGen as open source

I released my [LayerProcGen framework](https://runevision.com/tech/layerprocgen/) as open source in May 2024. LayerProcGen is a framework that can be used to implement layer-based procedural generation that's infinite, deterministic and contextual.

![](../../assets/b482d4f21927bfab.jpg)

I wrote [extensive documentation](https://runevision.github.io/LayerProcGen/) describing not only the specifics of how to use it, but also the overarching ideas and principles it's based on. I also did [a talk at Everything Procedural Conference](https://www.youtube.com/watch?v=4oJGkx0K8UQ) about it, which was well received.