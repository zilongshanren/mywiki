---
title: Simonschreibt.
url: https://simonschreibt.de/gat/deus-ex-alpha-terrain/
author: Simon
published: '2023-05-28'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

Three years ago, while playing [Deus Ex: Mankind Divided](https://store.steampowered.com/app/337000/Deus_Ex_Mankind_Divided/), I noticed a nice little trick and [tweeted](https://twitter.com/simonschreibt/status/1344375160904810498?t=_zZwTW4fxDbHV_ULw8Arjg&s=09) about it – today is the day when I finally release it as an article. Do you guess, what’s this about?

Correct answer: The terrain blends nicely with the stone! Let me explain it in more detail: Usually when objects and terrain intersect with each-other, one can see a harsh intersection. In Deus Ex on the other hand, there’s a nice smooth transition between terrain and object:

Now, blending objects with the terrain is **not** a spectacular new idea. A list:

- I myself described a fun technique for trees in Torchlight
[[Link]](http://simonschreibt.de/gat/world-of-torch-siege-blended-trunks/) - There is an amazing technique to blend the colors and even normals of the terrain with the mesh (known from Battlefront 2)
[[Link]](https://orikmcfly.artstation.com/projects/9zRna) [TigSource Thread about Terrain Blending in Zelda: BotW & Farcry 5](https://forums.tigsource.com/index.php?topic=67068.0)[[Link]](https://forums.tigsource.com/index.php?topic=67068.0)- Terrain blending with Unreal Realtime Virtual Texturing (RVT)
[[Link]](https://www.youtube.com/watch?v=0-xXIMjlmqE) - There is this fun experiment to use Pixel Depth Offset & Dithering to blend terrain and object
[[Link]](https://www.youtube.com/watch?v=tyLSH5zF-rI)

What I like about the Deus Ex approach: it’s a simple hack (and you know me, I LOVE tricks like that!).

Let’s look at some examples, and maybe you can guess already what’s happening here:

[Deus Ex: Mankind Divided](https://store.steampowered.com/agecheck/app/337000/)

The terrain uses a **translucent material**!

As such, it can make use of a simple [depth fade](https://www.youtube.com/watch?v=2BxrGjPcirk) (the closer a pixel is to an opaque surface, the more transparent it gets) it can now blend smoothly with the (opaque) objects.

Instead of doing a simple depth fade, [EmilMeiton describes an improved method](https://forums.tigsource.com/index.php?topic=67068.msg1401676#msg1401676): *“using the depth buffer “raw” to blend my objects works, but the result is heavily dependent on the angle of the camera to the ground. […] I realized we could simply reverse this effect by calculating the tangent of the angle between the terrain normal and the view direction (camera vector) and use this to divide the earlier used distance (between terrain and object beneath). It’s not perfect but it’s way better than the result before,”*

Allow me to say a few words why seeing a translucent material surprised me:

**Overdraw**. We always hear: Be careful with overdraw! Avoid huge particles!! It kills your performance!!!!111 So, seeing a terrain (which fills at least half the screen most of the time) using a translucent material seemed counterintuitive to me.

**Sorting**. Translucent objects usually have sorting issues. In the video below, you can see those in the form of polygons being visible**through**other polygons in front:

Note: Unreal just added [Order Independent Translucency,](https://youtu.be/o3CemUinXbw?t=849) and this might be a game changer!

The reason why all of this was a surprise to me was, that usually terrain rendering works like shown below.

[GTA V Graphics Study by Adrian Courrèges](https://www.adriancourreges.com/blog/2015/11/02/gta-v-graphics-study/)

As you can see, the terrain is opaque and drawn **very early**. This makes sense because now you don’t need to render anything which is hidden behind the already rendered pixels. Adrian send me another [example of Metal Gear Solid V](https://www.adriancourreges.com/blog/2017/12/15/mgs-v-graphics-study/?s=09#depth-pre-pass) where they render the terrain first to avoid rendering anything behind it – this advantage would be lost in the case of Deus Ex where the terrain is rendered last.

When I saw the Deus Ex approach the first time, I asked on Twitter and Ben Golus answered and explained a bit [here](https://twitter.com/bgolus/status/1344378238483632128?t=k0c3UnhksAS5c79RCUQntw&s=09) and [here](https://twitter.com/bgolus/status/1344385739098734595?t=Ii_N0YZCrmwsvDe5DOkW_w&s=09) (just in case you want more details).

Let’s now take a look at the mentioned problems (overdraw & sorting):

# Overdraw

Here’s my guess why overdraw is **not** a huge problem in this case:

It’s only **one** layer. Usually when artists get warned about overdraw, it’s to avoid that too many translucent layers overlap each other so that 1 pixel is touched 50x during rendering because 50 particles cover its area.

It helps, that the terrain is very **flat** so that we never see it overlapping itself (something like my sorting-example from above, where the hills overlap each other, never occurs in Deus Ex):

[Deus Ex: Mankind Divided](https://store.steampowered.com/agecheck/app/337000/)

# Sorting Issues

Just one sentence above I wrote, that the sorting in Deus Ex should not be a problem because of the flatness of the terrain. Still, I’d like to show you the rendering process in Deus Ex and show an example how potential sorting issues could be solved (e.g. if the terrain has overlapping hills).

Like usually in real-time rendering, all opaque objects come first. Usually the terrain is part of that (see GTA V example above), but not so much in Deus Ex! There are some patches of orange sand, but those will be occluded soon:

Now, the terrain is drawn on top. It has a translucent material which allows for the smooth blend with the opaque geometry. Note that it also gets rendered into the depth buffer! **This is special!** Usually this is **not** the case for translucent objects ([more details here](https://research.ncl.ac.uk/game/mastersdegree/graphicsforgames/transparencyanddepth/Tutorial%204%20-%20Transparency%20and%20Depth.pdf)) but here it’s OK because we know, that nothing needs to be rendered behind the terrain pixels.

The next steps would be shadows, lighting, other translucent elements like particles and of course the UI. But those things are not interesting for us right now.

I’d like to emphasize how important it is, that the (translucent) terrain gets written into the depth buffer because it serves two purposes:

1. **Avoiding sorting issues**. By comparing newly drawn pixels to the already existing depth information, we can discard those pixels, which are behind already rendered ones:

I made a [tutorial how to set up the example above to avoid sorting issues](https://youtu.be/1YJP55GYFoo).

As mentioned before: My example is very mountainous, but the terrain in Deus Ex is quite **flat!** So in theory, in this specific case, rendering the (translucent) terrain into the depth buffer would not have been necessary since there are no sorting issues to be expected. **But** we can use the depth information for something else:

2. **Depth Fade for particles**. In the example below, you can see, typical sorting issues (left), a “fix” by forcing the particle to be drawn on top (center) and the nicest way of having the particle “reacting” to the terrain by doing a nice depth fade (right):

Again: Doing such a depth fade is very normal when we’re talking about a particle being close to an **opaque** object because they always render into the depth buffer while **translucent **object like our terrain usually do not!

And here you can see it in action in the game. The dust effect has a soft transition with the terrain:

[Deus Ex: Mankind Divided](https://store.steampowered.com/agecheck/app/337000/)

# By the way…

Zelda: BotW uses a similar technique, and here is a [thread where flogelz re-creates the terrain blending](https://forum.unity.com/threads/solved-zelda-botw-terrain-intersection-blending.756209/). They don’t use a translucent material for the terrain but blend everything in the GBuffer, but the render order is the same: First everything else, then the terrain.

# Summary

Deus Ex uses a nice hack to blend terrain and objects. Three things are special about its terrain rendering:

- The terrain renders
**after**all opaque objects - The terrain uses a
**translucent**material - The terrain renders into the depth buffer (usually only opaque objects do)

These things are done to:

- Avoid sorting issues
- Blend terrain softly with objects
- Blend other translucent elements like particles softly with the (translucent) terrain

Resulting problems could be:

- Potentially waste of rendering opaque objects because they’re completely occluded by the terrain (not the case in Deus Ex)
- When looking closely, the hack is quite visible since it depends on the angle between of camera and terrain


I hope you liked the article and feel free to leave a comment!

Simon ♥

Interesting approach. I don’t like the artifacts it produces and hence for a first/third person game this is not ideal. But I can see the benefits in Top-Down games where the camera is further away and the view angle is rather below 45° towards the surface normals. This should produce more constant results and less parallax artifacts.