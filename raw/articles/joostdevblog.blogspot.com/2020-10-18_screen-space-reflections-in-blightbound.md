---
title: Screen Space Reflections in Blightbound
url: http://joostdevblog.blogspot.com/2020/10/screen-space-reflections-in-blightbound.html
author: Joost van Dongen
published: '2020-10-18'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Blightbound](https://www.blightbound.com/)(currently in

[Early Access on Steam](https://store.steampowered.com/app/1263070/Blightbound/)) is that we want to combine 2D character animation with high quality 3D rendering. Things like lighting, normal maps,

[depth of field blur](http://joostdevblog.blogspot.com/2010/09/depth-of-field-blur-in-proun.html), soft particles, fog and real-time shadows are used to make it all gel together and feel different from standard 2D graphics. One such effect I implemented into our engine is SSR: Screen Space Reflections. Today I’d like to explain what SSR is and what fun details I encountered while implementing it into our engine.



*A compilation of places with reflections in rain puddles in Blightbound.*

So we need something else. The most commonly used techniques for implementing reflections in games are cubemaps, planar reflections and Screen Space Reflections (SSR). We mostly wanted to use reflections for puddles and such, so it’s important to us that characters standing in those puddles are actually reflected in real-time. That means that static cubemaps aren’t an option. A pity, since static cubemaps are by far the cheapest way of doing reflections. The alternative is dynamic reflections through cubemaps or planar reflections, using render-textures. These techniques are great, but require rendering large portions of the scene again to render-textures. I guessed that the additional rendercalls and fillrate would cost too much performance in our case. I decided to go for Screen Space Reflections (SSR) instead.

The basic idea behind SSR is that since you’re already rendering the scene normally, you might as well try to find what’s being reflected by looking it up in the image you already have.

![](../../assets/5992cd3767faeef7.jpg)

SSR has one huge drawback though: it can only reflect things that are on-screen. So you can’t use a mirror to look around a corner. Nor can you reflect the sky while looking down at the ground. When you don't focus on the reflections this is rarely a problem, but once you look for it you can see some really weird artefacts in reflections due to this. For example, have a look at the reflections of the trees in


![](../../assets/4e24adff96574b2a.jpg)



[this video](https://youtu.be/SE6R3ZGlxHc?t=258)of Far Cry 5.![](../../assets/4e24adff96574b2a.jpg)


So we’re looking up our reflections in the image of the scene we already have, but how do we even do that? The idea is that we cast a ray into the world, and then look up points along the ray in the texture. For this we need not just the image, but also the depth buffer. By checking the depth buffer, we can look whether the point on our ray is in front of the scene, or behind it. If one point on the ray is in front of whatever is in the image and the next is behind it, then apparently this is where the ray crossed the scene, so we use the colour at that spot. It’s a bit difficult to explain this in words, so have a look at this scheme instead:



![](../../assets/8f1b0205431354d6.jpg)

Since SSR can cast rays in any direction, it’s very well suited for reflections on curved surfaces and accurately handles normal maps. We basically get those features for free without any extra effort.


*A demo*

*in the Blightbound engine*

*of SSR, with a scrolling normal map for waves.*



At its core SSR is a pretty simple technique. However, it’s also full of weird limitations. The challange of implementing SSR comes from working around those. Also, there are some pretty cool ways to extend the possibilities of SSR, so let’s have a look at all the added SSR trickery I implemented for Blightbound.

First off there’s the issue of transparent objects. Since the world of Blightbound is covered in a corrupting mist (the “blight”), our artists put lots of foggy layers and particles into the world to suggest local fog. For the reflections to have the right colours it’s pretty important that these fog layers are included in the reflections. But there are also fog layers in front of the puddles, so we can't render the reflections last either.

The solution I chose is simple: reflections use the

*previous*frame instead of the*current*frame. This way we always look up what's being reflected in a complete image, including all transparent objects. The downside of this is of course that our reflection isn't completely correct anymore: the camera might have moved since the previous frame, and characters might be in a different pose. However, in practice the difference is so small that this isn't actually noticeable while playing the game.![](../../assets/eef4fd2ce0eac43e.jpg)

Transparent objects pose another problem for SSR: they're not in the depth buffer so we can't locate them correctly. Since Blightbound has a lot of 2D animation, lots of objects are partially transparent. However, many objects can use alpha test. For example, the pixels of a character's texture are either fully transparent of not transparent at all. By rendering such objects with alpha test, they can write to the depth buffer without problems.

This doesn't solve the problem for objects with true transparency, like smoke, fog and many other special effects. This is something that I don't think can be reasonably solved with SSR, and indeed we haven't in Blightbound. If you look closely, you can see that some objects aren't reflected at all because of this. However, in most cases this isn't noticeable because if there's an opaque object closely behind it, then we'll see the special effects through that. While quite nonsensical, in practice this works so well that it seems as if most explosions are actually reflected correctly.

![](../../assets/7f73bdc6a7e65150.gif)

*Transparent objects like this fire aren't in the depth buffer and thus can't be found for reflections. However, if another object is close behind, like the character on the left, then the transparent object is reflected through that. The result is that it seems as if many special effects are properly reflected.*

Having perfectly sharp reflections looks artificial and fake on many surfaces. Reflections in the real world are often blurry, even more so the further the reflected object is from the surface. To get reflections that accurately blur with distance I've applied a simple trick: the rays get a slight random offset applied to their direction. This way objects close remain sharp and objects get blurrier with distance. Artists can tweak the amount of blur per object.

However, this approach produces noise, since we only cast one ray per pixel. We could do more, but that would be really heavy on performance. Instead, to reduce the noise a bit, when far enough away I also sample from a low-resolution blurry version of the scene render-texture. This is a bit redundant but helps reduce the noise. Finally, by default in Blightbound we do supersampling anti-aliasing (SSAA) on the screen as a whole. This results in more than one ray being shot per screen-pixel. Only on older GPUs that can't handle SSAA is this turned off.

![](../../assets/563bdadb786f0f2f.jpg)

Another issue is precision. For really precise reflections, we would need to take a

*lot*of samples along the ray. For performance reasons that's not doable though, so instead we make small jumps. This however produces a weird type of jaggy artefacts. This can be improved upon in many different ways. For example, if we would render the reflections at a lower resolution, we would be able to take a lot more samples per ray at the same performance cost. However, with how I implemented SSR into our rendering pipeline that would have been quite cumbersome, so I went for a different approach which works well for our specific situation:

- More samples close to the ray's origin, so that close reflections are more precise.
- Once the intersection has been found, I take a few more samples around it through binary search, to find the exact reflection point more precisely. (The image below is without binary search.)
- The reflection fades into the fog with distance. This way the ray never needs to go further than a few meters. This fits the world of Blightbound, which is basically always foggy.

The result of these combined is that we get pretty precise reflections. This costs us 37 samples along a distance of at most 3.2 meters (so we never reflect anything that's further away than that from the reflecting surface).

Any remaining imperfects become entirely unnoticeable since blur and normal maps are often used in Blightbound, masking any artefacts even further.

![](../../assets/cd73b06ea85fe621.jpg)

A challenge when implementing SSR is what to do with a ray that passes behind an object. Since our basic hit-check is simply whether the previous sample was in front of an object and the next one is behind an object, a ray that should pass behind an object is instead detected as hitting that object. That's unintended and the result is that objects are smeared out beyond their edges, producing pretty ugly and weird artefacts. To solve this we ignore a hit if the ray dives too far behind an object in one step. This reduces the smearing considerably, but the ray might not hit anything else after, resulting in a ray that doesn't find an object to reflect. In Blightbound we can solve this quite elegantly by simply using the level's fog colour for such failed rays.

![](../../assets/4601887ff712d2f8.gif)

*By default, SSR produces these kinds of vertical smears. Assuming objects have a limited thickness reduces this problem greatly, but adds other artefacts, like holes in reflections of tilted objects.*

This brings us to an important issue in any SSR implementation: what to do with rays that don't hit anything? A ray might fly off the screen without having found an object, or it might even fly towards the camera. Since we can only reflect what we see, SSR can't reflect the backs of objects and definitely can't reflect anything

*behind*the camera. A common solution is to have a static reflection cubemap as a fallback. This cubemap needs to be generated for each area so that the reflection makes sense somewhat, even if it isn't very precise. However, since the world of Blightbound is so foggy I didn't need to implement anything like that and can just fall back to the fog colour of the area, as set by an artist.The final topic I would like to discuss regarding SSR is graphics quality settings. On PC users expect to be able to tweak graphics quality and since SSR eats quite a lot of performance, it makes sense to offer an option to turn it off. However, what to do with the reflecting objects when there's no SSR? I think the most elegant solution is to switch to static cubemaps when SSR is turned off. Static cubemaps cost very little performance and you at least get some kind of reflection, even if not an accurate and dynamic one.

However, due to a lack of time that's not what I did in Blightbound. It turned out that just leaving out the reflections altogether looks quite okay in all the spots where we use reflections. The puddles simply become dark and that's it.

![](../../assets/94e43f3499b7e5be.jpg)

For reference,

[here's the shader code of my SSR implementation](http://www.proun-game.com/Oogst3D/BLOG/SSR%20-%20Ronitech%20shader%20code.txt). This code can't be copied into an engine directly, since it's dependent on the right render-textures and matrices and such from the engine. However, for reference when implementing your own version of SSR I expect this might be useful.SSR is a fun technique to implement. The basics are pretty easy, and real-time reflections are a very cool effect to see. As I've shown in this post, the real trick in SSR is how to work around all the weird limitations inherent in this technique. I'm really happy with how slick the reflections ended up looking in Blightbound and I really enjoyed implementing SSR into our engine.

Great post -- thanks!



ReplyDeleteI hadn't thought much about reflections since the era of the original Unreal game (e.g. https://www.youtube.com/watch?v=26I-Pw-yPJ4), which I think implemented them (expensively) by just rendering flipped geometry a second time with partial opacity.

I assume that when using SSR while looking down at a 3D object at a steep angle, the incorrect perspective of the reflection (i.e. showing the top of the object rather than the bottom) can be noticeable. But having 2D characters probably mostly avoids this, right? :-)

SSR has correct perspective on reflections. It uses the depth buffer to figure out perspective. However, you are right that it has artefacts at steep angles or when trying to reflect something that's not visible to the camera (like the back of an object). Exactly how these artefacts look depends on the implementation: do we reflect the front of the object instead, or nothing at all, or use a static fallback cubemap?




DeleteIn Blightbound in such cases we reflect a flat fog colour, as can be seen in this image from the blogpost:

https://1.bp.blogspot.com/-p8mOBV0MQi4/X4xqctSv6cI/AAAAAAAAH44/WWq3mSGx37kIoyGTCesFhBoSm5kWaQyKQCLcBGAsYHQ/s16000/SSR%2B-%2BScreenshot.jpg

The horizontal barrel behind the woman's left foot partially disappears in the reflection, with some smears of where SSR did figure it out. At that spot the barrel indeed has a very steep angle with the camera.

Ah, got it. I was focusing on how the reflection can't e.g. show the underside of an object that's being viewed from above (since the underside wouldn't be rendered normally). But yeah, it makes sense that the perspective of the visible parts of the object will be correct in the reflection since you're raycasting into the depth buffer -- the top of an object will never appear in the reflection since the rays won't hit it (assuming that the barrels are 3D objects and not billboards).


DeleteThe part of me that hasn't done any graphics stuff since the introduction of GPUs and shaders is still amazed that it's feasible to cast a ray through every pixel for every frame!