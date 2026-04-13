---
title: Creating crisper special effects with trails
url: http://joostdevblog.blogspot.com/2016/09/creating-crisper-special-effects-with.html
author: Joost van Dongen
published: '2016-09-11'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](http://www.awesomenauts.com)were either animated by hand or made using particles. This seemed to give enough possibilities, until we played the gorgeous

[Ori and the Blind Forest](https://www.youtube.com/watch?v=VrbGwU5Zx4M), which has very crisp special effects. We analysed how they achieved this and one of the conclusions was that for many things that we would make with particles, they used trails. Trails are quite an obvious concept, but for some reason it had never seemed like a big problem that they weren't an option in our tools. So about a year ago I added trails to our engine.

![](../../assets/fb7d418e559fcc3f.jpg)

How to implement trails seems quite obvious: it's just a series of triangle segments, what's interesting about that? However, when I started implementing trails it turned out there are quite a lot of different approaches imaginable. I went with one that's extremely flexible, but also sometimes slightly difficult to control for certain effects. Today I'd like to share how I built our trails tool and what the pros and cons are. But before I get to that, let's start with a video that shows the tools for our trails and what our artists have made with those.

The core idea of my implementation is that a trail is like a series of connected particles, called

*segments*. Each segment has it's own position and velocity, and the trail is formed by creating polygons in between the segments. This is a fun approach: it makes things like gravity, waviness and wind really easy, since you can just apply those effects to each segment separately and then connect them. It also means that the trail automatically stretches when you move quickly, just like a trail should.

![](../../assets/09e98e8d3524e46a.gif)

An interesting aspect is what to do when standing still. In the case of normal particles you would just keep creating them regardless of your own speed, but with a trail that isn't a good idea: connecting segments that are nearly on the same position results in jumpy segment orientations. My solution to this is to have a minimum distance between segments and only emit another segment if you've moved enough. Doing this naively does have a weird side-effect: you get small holes in between the starting point of the trail and the newest created segment. To avoid this I move the newest segment along with the position of the emitter until a new segment is made.

![](../../assets/43833d0fa86afcd1.gif)

If no care is taken something similar would also happen at the end, where the tip of the trail just suddenly disappears when its segment times out. Here the solution is to smoothly move the timed out final segment towards the penultimate segment before removing it.

To avoid creating too many segments, the artist sets how many segments he needs. Since I already have this minimum distance between segments I figured this would also be a good way to limit the number of segments. However, I now bumped into another oddity: if you move really quickly you will create a new segment every frame. That means that the number of segments depends on the framerate. Our artists have fast computers and usually have vsync disabled so they often run the game at 200fps or more. They need to go out of their way to see what Awesomenauts looks like on 30fps or even 20fps. To avoid situations where artists unknowingly create effects that only look smooth and good on very high framerates, I've limited the maximum number of segments per second to 60. If on older netbooks the framerate drops below that you will still get less smooth trails, but the difference between 20fps and 60fps is much more acceptable than between 20fps and 200fps.

A fun option you get from treating segments as particles is that you can do more than just leave them. A normal trail only exists when you move, it's literally a trail. But why not shoot segments away, like you often do with particles? With some creativity this can be abused to create effects like flames (shooting segments upwards) or flags (shooting segments horizontally) and get a very dynamic look for them. I also added an option for gravity/wind to change the speed of a segment over time.

One of the most fun things when making tools is when artists (ab)use them to make things you didn't expect. Especially

[Ronimo](http://www.ronimo-games.com)artist Ralph is really good at this. He considers it his personal crusade to use every feature of our editors for something. The weirder the feature, the more Ralph considers it a challenge to use it for something pretty. So when making trails my goal was to feed the Ralph by making trails super flexible. For this reason I added four different ways of mapping textures to the trail, and two textures can be combined on a single trail:

![](../../assets/b82d933e382193cd.jpg)

![](../../assets/2f71838b9b81e5e9.jpg)

When I showed the trails to our artists they immediately wondered whether they could make things like a hair or a cape with it. Doing so with a normal trail would result in a very elastic look: trails become longer and shorter depending on how fast you move, which is usually not desired when making something like a braid or cloth. To fix this problem I added a feature that gives the trail a maximum and minimum length, shortening or stretching it when needed. This turned out not to work too well. The minimum length gave really odd results, especially when the character is standing still, so I removed that feature altogether. The maximum length does work, but in practice it doesn't produce convincing hair or cloth movement, so our artists usually go back to hand-animating those. I think to make good hair or cloth you need a very different approach: those require a real physics simulation, instead of simply emitting segments like I do now.

On top of all of the things discussed so far we got a lot of additional flexibility for free: years ago I made the tools of the Ronitech (our internal engine) in such a way that almost anything is animatable, so our artists can change most of the settings of trails over time. This allows for a lot of fun additional possibilities, like varying the thickness of a trail over time, or making the colour pulsate.

My implementation of trails does have one main downside: textures aren't very stable. The constantly varying length of the first and last segments makes textures flicker a bit, even though I compensate to get the correct texture coordinates. Framedrops can also leave longer holes in between segments, which is not immediately a problem but again it makes textures slightly less stable. I think if I were to ever make another version of trails I would decouple the polygons from the segments, and just create the polygons at equal distances over the path laid out by the segments.

All in all I'm really happy with how our trails system turned out. The approach of treating a trail as connected particles makes some things slightly unpredictable, but it does give a lot of flexibility. I expect our artists will come up with some more unexpected uses of trails in the future.

In the next two weeks I will discuss two more specific aspects of trails: the smoothing algorithm I created to make angular movement produce very smooth and curvy trails, and how to solve the texture distortion that occurs when skewing a quad with a texture on it. Till then!

Glad to see a new article here again!




ReplyDeleteQuite an interesting read. Never used trails myself in any context but now I feel a bit inspired.

So if I understand correctly, the segments are still acting like regular particles in the sense that they are not physically attached to each other like in a cloth-simulation? One thing that came to mind as a potential effect was a rotating spiral, although would probably not maintain its shape very well if the emitter is moving quickly. Wonder if one could use trails for creating less "traily" stuff. I guess procedural trees would be a good one. Segments could act as emitters themselves and create branches or leaves. Could get quite surreal if the tree or branches are constantly iterated like any other effect.

Looking forward to the next part!

Yeah, my implementation means the parts of a trail are not physically connected, they just get a mesh between them to make them look connected. This is necessary since one expects a trail to be longer when you move faster, so fixing the length or angle of a trail segment is kind of the opposite of a trail.


DeleteOur artists have tried using trails for things like hair, fire and even plants. In general my implementation of trails doesn't give a 'stable' enough look for most of those. It works really well with things like gradients and smoky stuff, but less well with tangible stuff.

Rarely do I see offten how Coding and Art play hand in hand and the artist side in me is kicking me of not learning code. thank you for being as big as a inspration to me as any other artist I see.

ReplyDelete:)


DeleteMost artists become really unhappy when they need to learn code (I know because I was once a programming teacher at an art school, poor students...), but I enjoy looking at art from a coding standpoint. :)

Your game design engine seems to have become quite extensive already. Have you thought of releasing it as a game making/designing tool? I know that I personally would love to use something like this.

ReplyDeleteWe've thought about it, but the amount of work involved in turning it into something that's generally useful is enormous still. The engine is currently too intertwined with the Awesomenauts code and lots of basic functionality is missing because we didn't need it. Going from an in-house engine to an engine that others can use is a lot of work.


DeleteWe are releasing some of the tools for Awesomenauts modding though. :) The AI editor is already included with the game and the level editor is coming soon as well.

Oh that awesome to hear! I love awesomenauts and am looking forward to having the abilty to play around with it more

Delete