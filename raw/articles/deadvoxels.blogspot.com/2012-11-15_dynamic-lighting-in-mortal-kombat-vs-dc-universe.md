---
title: Dynamic Lighting in Mortal Kombat vs DC Universe
url: http://deadvoxels.blogspot.com/2012/11/dynamic-lighting-in-mortal-kombat-vs-dc.html
author: Jon Greenberg
published: '2012-11-15'
source_blog: Dead Voxels
source_site: http://deadvoxels.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

*MKvsDC*(as the title is colloquially referred to at NetherRealm) was our very first foray into the X360/PS3 generation of hardware. As a result, it featured a lot of experimentation and a lot of exploration to figure out what might and might not work. Unlike our more recent fighters,

*Mortal Kombat (2011)*and

*Injustice: Gods Among Us*(which is still getting completed and looking pretty slick so far), MKvsDC was actually a full-on 3D fighter in the vein of our last-gen (PS2/GameCube/Xbox1) efforts. (Note, once again, everything here has been explained publicly before, just in a bit less detail).

A lot of figuring out how to get things going in MKvsDC was trying to figure out what was doable and at the same time acceptable. The game had to run at 60Hz, but was both being built inside an essentially 30Hz targeted engine and had to look on par with 30Hz efforts. I remember quite early on in development Tim Sweeney and Mark Rein came out to visit Midway Chicago. I remember going for lunch with the Epic crew, myself spending the majority of it speaking with Tim (extremely nice and smart guy) about what I was going to try to do to Unreal Engine 3 to achieve our visual and performance goals. Epic was very up front and honest with us about how UE3 was not designed to be optimal for a game like ours. To paraphrase Sweeney, since this was years ago, "You're going to try to get UE3 to run at 60Hz? That's going to be difficult."

He wasn't wrong. At the time, UE3 was pretty much a multipass oriented engine (I believe it still theoretically is if you're not light baking, using Dominant Lights, or using Lighting Environments, though no one would ship a game that way). Back then there were still a lot of somewhat wishy-washy ideas in the engine like baking PRT maps for dynamic objects, which ended up largely co-opted to build differential normal maps. Lots of interesting experimental ideas in there at the time, but most of those were not terribly practical for us.

So Item #1 on my agenda was figuring out how to light things cheaper, but if possible, also better. Multipass lighting was out - the overhead of multipass was simply too high (reskinning the character per light? I don't think so!). I realize I'm taking this for granted, but I probably shouldn't - consider that one of the obvious calls early on was to bake lighting whereever possible. Clearly this biases towards more static scenes.

Anyhoo, we had really two different problems to solve. The first was how were we going to light the characters. The fighters are the showcase of the game, so they had to look good, of course. The second problem was how were we going to handle the desire for dynamic lighting being cast by the various effects the fighters could throw off. We handled it in the previous gen, so there was a team expectation that it would somehow be available "as clearly we can do even more, now".

So, the first idea was something I had briefly played around with on PS2 - using spherical harmonics to coalesce lights, and then light with the SH's directly. Somewhat trivially obvious now, it was a bit "whackadoo" at the time. The basics of the solution were already rudimentarally there with the inclusion of Lighting Environments (even if the original implementation wasn't entirely perfect at the time). Except instead of extracting a sky-light and a directional as Epic did, we would attempt to just directly sample the SH via the world-space normal.

This worked great, actually. Diffuse results were really nice, and relatively cheap for an arbitrary number of lights (provided we could safely assume these were at infinity). Specularity was another matter. Using the reflection vector to lookup into the solution was both too expensive and of dubious quality. It somewhat worked, but it didn't exactly look great.

So after playing around with some stuff, and wracking my brain a little, I came up with a hack that worked pretty decently given that we were specifically lighting characters with it. In essence, we would take the diffuse lighting result, use that as the local light color, and then multiply that against the power-scaled dot between the normal and eye vector. This was very simple, and not physically correct at all, but surprisingly it worked quite nicely and was extremely cheap to evaluate.

But, then Steve (the art director) and Ed came to me asking if there was anything we could do to make the characters pop a little more. Could we add a rim-lighting effect of some kind? So, again seeking something cheap, I tried a few things, but the easiest and cheapest thing seemed to be taking the same EdotN term and playing with it. The solution I went with was basically something like (going from memory here):

_Clip = 1 -(E dot N);

RimResult = pow(_Clip, Falloff)*(N dot D) * (_Clip > Threshold)

Where *E* is the eye/view vector, *N* the world-space normal, *D* a view-perpendicular vector representing the side we want the rim to show up on, and *Falloff* how sharp we want the highlight to seem. Using those terms provided a nice effect. Some additional screwing around discovered the last part - the thresholding.

This allowed for some truly great stuff. Basically this hard thresholds the falloff of the rim effect. So, this allows for, when falloff is high and threshold is as well, a sharp highlight with a sharp edge to it, which is what Steve wanted. Yet, if you played with it a bit other weirder things were possible, too. If you dropped the falloff so it appeared more gradual and yet hard thresholded early this gave a strange cut-off effect that looked reminiscent of metal/chrome mapping!

To further enhance all of this, for coloring I would take the 0th coefficients from the gathered SH set and multiply the rim value by that, which gave it an environmental coloring that changed as the character moved around. This proved so effective that initially people were asking how I could afford environment mapping in the game. All from a simple hard thresholding hack. In fact, all the metal effects on characters in MKvsDC are simulated by doing this.

Okay, so characters were covered. But environment lighting... yeesh. Once again, multipass wasn't really practical. And I knew I wanted a solution that would scale, and not drag the game into the performance gutter when people started spamming fireballs (or their ilk). What to do....

So it turned out that well, these fireball-type effect lights rarely hung around for very long. They were fast, and moved around a lot. And yet, I knew for character intros, fatalities and victory sequences simply adding them into the per-object SH set wouldn't prove worthwhile, because we'd want local lighting from them. Hmm...

So, I ended up implementing two different approaches - one for characters and a second for environments. For characters, I did the lighting in the vertex shader, hardcoding for 3 active point lights, and outputting the result as a single color interpolator into the pixel shader. This was then simply added in as an ambient factor into the diffuse lighting. As these lights tended to be crazy-over bright, the washing out of per-pixel detail didn't tend to matter anyway.

Environments were more challenging though. As tessellation of the world tended to be less consistent or predictable, the three lights were diffuse-only evaluated either per-pixel or per-vertex (artist selectable). When using per-vertex results, again a single color was passed through, but modulated against the local per-pixel normal's Y component (to fake a quasi ambient occlusion). This worked well enough most of the time, but not always. If you look carefully you can see the detail wash out of some things as they light up.

To keep track of the effect lights themselves, a special subclass of light was added that ignored light flags, and that were managed directly in a 3-deep FIFO so that the designers could spawn lights at will without having to worry about managing them. When dumped out of the end of the FIFO lights wouldn't actually be deleted of course, merely re-purposed and given new values. Extinguished lights were given the color black so they'd stop showing up. Objects and materials had to opt in to accepting dynamic lighting for it to show up, but anything that did was always evaluating all 3 lights whether you could see them or not.

Ironically about 3 months before shipping I accidentally turned off the effect lights showing up on characters and didn't realize until the very last minute when it was pointed out by QA (switched back on at the 11th hour!), which is why you'll find very few screenshots online created by our team with obvious effect lights showing up on the fighters. Oops!

## No comments:

## Post a Comment