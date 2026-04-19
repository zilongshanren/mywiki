---
title: Notes on atmospheric perspective and distant mountains
url: https://blog.runevision.com/2025/06/notes-on-atmospheric-perspective-and.html
published: '2025-06-29'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

## Notes on atmospheric perspective and distant mountains

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

## 3 comments:

Very cool writeup and use of reference images!

In path traced scenes we get these effects quite naturally by using a Mie scattered volume (dust, fog) near the earth and Rayleigh scattering in the upper atmosphere. The Rayleigh scattering tints the sky and the Mie scattering in-scatters the sky and sun into the lightpath from the mountains to the eye. At the same time the Mie scattered particles absorb the reflected green light from the forest. This makes distant mointants appear more sky-colorish and faded. This should also be pretty close to what happenes in reality if I am not mistaken.

I was also just in Japan, admiring the nature in both the rural and urban areas, and finding inspiration for my games. I really enjoyed reading your thought processes and admire your overall approach, which seems to include teaching what you’ve learned for everyone’s benefit.





The subtlety of light scattering in 3D rendering is a new frontier for me. Light scattering at distances seems easy to get passable with “fog tricks,” as you put it, but difficult to get just right in the way one might want to when building a game that aims to emulate the natural world with high fidelity.

Game engine light scattering seems necessarily smoke and mirrors— alternative being to simulate the refraction of light through air particles, which doesn’t seem computationally feasible, particularly at great distances.

Light scattering based on the composition of the atmosphere, could be used in a more diegetic manner, where changing the composition of the atmosphere is sufficient to achieve the desired effect.

I would think game engine fog is trying to do this, I doubt they are rending particles (dust, as the previous comment suggests) in 3D space to it. I’ll have to read up some more to find out, but could be an interesting follow up in this blog :)

Your mountains in game are different LODs anyway, why not just have the actual LODs generate with different colors/tone maps based on distance? kind of like American West watercolor artists simulating the orange, blue, purple transitions of mountains as the cascade towards horizon at sunset? Think Mesa Verde, Bryce Canyon.


It is also interesting to look at how Horizon Zero Dawn Complete Edition accomplishes this as well (the remastered version handles it differently with global illumination.)

Post a Comment