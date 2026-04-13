---
title: Handling Shadows in Mortal Kombat (2011)
url: http://deadvoxels.blogspot.com/2012/11/so-i-havent-posted-anything-in.html
author: Jon Greenberg
published: '2012-11-04'
source_blog: Dead Voxels
source_site: http://deadvoxels.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I figured I'd talk a little about how shadows were dealt with in Mortal Kombat (aka MK9). The key thing to keep in mind is that in MK9 the performance envelope that could be dedicated to shadows was extremely limited. And yet, there were some conflicting goals of having complex looking shadow/light interaction. For example, our Goro's Lair background features a number of flickering candles casting shadows on walls, along with the typical grounding shadow one expects.

So, what did we do? We cheat. A lot. But everyone who can cheat in game graphics *should* cheat, or imho, you're doing it wrong. Rendering for games is all about cheating (or to be better about wording - being clever). It's all about being plausible, not correct.

The key to keeping lighting under control in Mortal Kombat is rethinking light management. Unlike a lot of games, Mortal Kombat has the distinct advantage of a very (mostly) controlled camera and view. There are hard limits to where are shadow casters can go, what our lights do and therefore where shadows might appear. Thus, unlike probably every other engine ever made, we do NOT compute caster/receiver interaction at runtime. Instead, we require artists to explicitly define these relationships. This means that in any given environment we always know where shadows might show up, we know which lights cast shadows, we know which objects are doing the casting.

So, I'm not a total jerk in how this exposed to the artists. They don't have to directly tie the shadow casting light to the surface. Instead they mark up surfaces for their ability to receive shadows and what kind of shadows the surface can receive. Surfaces can receive the ground shadow, a spotlight shadow, or both. You want two spotlights to shadow-overlap? Sorry, not supported. Redesign your lighting. This might sound bad, but it ends up with shadows not being "locally concentrated" and spread across the level. More on this shortly...

As everything receiving shadows in MK9 is at least partially prelit, shadows always down-modulate. All shadows cast by a single light source are presumed to collate into a single shadow-map, and all "maps" actually occupy a single shadow texture. So we can practically handle four shadows simultaneously being constructed - the overhead of building the maps starts to get crazy. And at a certain point we're risking quality to the point where it's likely not worth it. As we only have a few characters on-screen casting shadows, at a certain point its just not worth the trouble, either.

So, in a level like Goro's Lair in MK9 we can have a number of flickering candle shadows on the walls, giving it a really dramatic spooky look, especially when combined with the nice wet-wall shader work by the environment team. We can handle this cost by knowing explicitly that only a max of four shadows ever update, and that the local pixel shader for any given wall section only has to handle a given specific spot shadow projection. This allows the artists to properly balance the level's performance costs and ensure they stay within budget (which for shadow construction is absurdly low).

For texture projection (aka gobos in our engine's terminology) the same logic applies. You can get either subtractive gobos (say, the leaves in Living Forest) or additive ones (the stained glass in Temple) in a level, but not both. You can have multiple gobos in a level, but only one can hit a particular object at a time. Objects explicitly markup that they can receive the gobos, and then even pick how complex the light interaction is expected to be to keep shader cost under control (does the additive gobo contribute to the lighting equation as a directional light or merely as ambient lighting).

The gobos themselves can't be animated - they're not Light Functions in Epic-speak. Light Functions are largely unworkable, as they're too open-ended cost wise - the extra pass per-pixel is too expensive (MK demands each pixel is touched only once to the point of no Z-prepass). And hey, they're generally *extremely* rare to see in UE3 titles, even by Epic, for good reason. But, we can fake some complex looking effects by allowing artists to animate the gobo location, or switch between active gobos. Flying these gobo casters around is how we animate the dragon-chase sequence found in RoofTop-Day, which ended up being quite clever.

But that's the point really. The difference between building a game and building an engine is figuring out clever uses of tech, not trying to solve open-ended problems. The key is always to make it look like you're doing a whole lot more than you actually are. If you're going to spend the rendering time on an effect, make sure its an obvious and dramatic one.

## No comments:

## Post a Comment