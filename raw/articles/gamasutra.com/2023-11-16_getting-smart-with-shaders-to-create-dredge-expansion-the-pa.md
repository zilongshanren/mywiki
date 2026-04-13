---
title: Getting smart with shaders to create Dredge expansion The Pale Reach
url: https://www.gamedeveloper.com/art/getting-smart-with-shaders-to-create-dredge-expansion-the-pale-reach
author: Chris Kerr
published: '2023-11-16'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![A boat approaching a frozen town in Dredge: The Pale Reach A boat approaching a frozen town in Dredge: The Pale Reach](../../assets/c6b57ac319d3f3c6.png)

It's been a pretty good year for New Zealand studio Black Salt Games. The company's debut release, Dredge, launched to critical acclaim and [recently topped 1 million sales](https://www.gamedeveloper.com/business/dredge-smashes-internal-expectations-after-topping-1-million-sales), smashing internal expectations.

Now, the team have expanded the cosmic fishing adventure with the [launch of a new expansion called ](https://store.steampowered.com/app/2561440/DREDGE__The_Pale_Reach/)[The Pale Reach](https://store.steampowered.com/app/2561440/DREDGE__The_Pale_Reach/). The add-on, however, represents a swift change in direction for Black Salt, which initially planned to release a different expansion dubbed The Iron Rig before [temporarily shelving that plan](https://store.steampowered.com/news/app/1562430/view/3735229909370857320) due to production concerns.

During a chat with Game Developer earlier this year, Dredge producer Nadia Thorne and 3D artist Mikey Bastiaens explained The Iron Rig was pushed back to 2024 after it became apparent releasing this year would require more lead time.

"The choice [to delay] was really no choice," says Thorne. "But we had promised players that we would get them something this year, so we asked ourselves 'what can we do in the time we have?' And we knew we could create a new area, because we'd created five."

## Glacial awareness

The Pale Reach adds a brand new ice-themed biome to Dredge that can be experienced at any stage during a playthrough, integrating seamlessly into the base game while expanding gameplay with a new story of "bitter betrayal," additional equipment, and fresh horrors from the deep.

Having already established some solid production pipelines where biomes are concerned, Black Salt felt comfortable building The Pale Reach during a relatively short timeframe. But as is always the case, whether you're making video games or sailing through the salty brine, the tides can turn in an instant.

One of the biggest challenges Black Salt faced this time around was bringing some fidelity to the frozen wastes of The Pale Reach. "It was [tough] getting the materials we used to have that icy feel. It involved playing with transparency through the ice, because on Switch and those sort of platforms transparency is what pretty much tanks performance," says Bastiaens.

"We had to figure out how we could make those assets work for us while not tanking everything."

Bastiaens states that's partly why Black Salt built the expansion using the Switch as a baseline measure of performance. If Nintendo's hybrid handheld could deliver a smooth experience without buckling, it should be a piece of cake for meatier Xbox, PlayStation, and PC hardware.

![A player approached a frozen dock in Dredge: The Pale Reach A player approached a frozen dock in Dredge: The Pale Reach](../../assets/4f1109b6daba947d.jpg)


Overcoming that hurdle also required the team to experiment with a bunch of different shaders, using resources as "sparingly as possible" to deliver sufficiently frosty results.

"We just said 'let's see what happens with this particular shader' because we had to get all the refractions so assets wouldn't have multiple facets on them when you're looking through it. Then we'd just say 'okay, that's too much. Let's change up that shader and do something different with it,'" continues Bastiaens.

"We made multiple different versions of the shaders. One might not have transparency, but another one does. It was just about trying to figure out how we could use things as sparingly as possible and strategically place them [to maximize impact]."

The decision to use a multitude of scene-specific shaders to set the mood in The Pale Reach came after Black Salt had tried to put the same shader on everything—completely sinking performance on the Switch.

"Initially, I was like 'all the ice will have this refraction shader on it' and it made the game pretty much unplayable," says Bastiaens. Delivering performance akin to that of a lurching, barnacle-clad rust bucket wasn't ideal, but it persuaded Bastiaens to create unique shaders and materials based on how folks would engage with them, reserving proper transparency for key moments when it's imperative players can to peer into the ice.

![A horned monster attacking a player's boat in The Pale Reach A horned monster attacking a player's boat in The Pale Reach](../../assets/fccee0aa0c50753b.jpg)


As for how the team streamlined development, Bastiaens explains they were able to essentially refurbish existing objects to create "new" assets that didn't require a huge time-sink.

"For the most part, we were able to reuse existing objects and rocks by pretty much applying new shaders to those things," he says. "There were some instances, where because of how the ice works, we also changed up the geometry to create those 'icy shapes,' but it was just a matter of applying these different materials and different colors to fit the vibe."

Black Salt was also able to use existing shader and material controls to rapidly tweak the "tone" of the ocean in The Pale Reach to create something more "glassy," making the expansion's frozen ice fields feel even more inhospitable.

For more on how Black Salt crafted the wonderfully creepy world of Dredge, you can [read our coverage of Bastiaens GCAP talk](https://www.gamedeveloper.com/production/leveraging-the-unseen-to-turn-players-worst-fears-against-them-in-dredge) where he explains how the studio turned players' worst fears against them. Or [plunge into our extensive interview with the dev team](https://www.gamedeveloper.com/design/trawling-in-the-deep-how-black-salt-games-made-spooky-fishing-rpg-i-dredge-i-) to learn what goes into making an unsettling seascape with hidden depths.

After that, why not [pore over this dev-authored deep dive into ](https://www.gamedeveloper.com/design/deep-dive-the-surprising-depth-of-spatial-inventories-in-dredge)[Dredge's](https://www.gamedeveloper.com/design/deep-dive-the-surprising-depth-of-spatial-inventories-in-dredge)[ spatial inventory system—](https://www.gamedeveloper.com/design/deep-dive-the-surprising-depth-of-spatial-inventories-in-dredge)penned by Black Salt programmer, writer and co-designer Joel Mason.