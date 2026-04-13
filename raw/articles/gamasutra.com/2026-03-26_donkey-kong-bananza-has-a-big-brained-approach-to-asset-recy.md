---
title: Donkey Kong Bananza has a big-brained approach to asset recycling
url: https://www.gamedeveloper.com/art/donkey-kong-bananza-has-a-big-brained-approach-to-asset-recycling
author: Bryant Francis
published: '2026-03-26'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![](../../assets/e427d8b5c9f968cf.png)


![](../../assets/e427d8b5c9f968cf.png)

**GDC Festival of Gaming (March 9-13, 2026) **

Keep up with the latest news, interviews, talk coverage, and other game dev insights from GDC 2026 right here on Game Developer. __Read More__

# Donkey Kong Bananza has a big-brained approach to asset recycling

Why remake a 3D model when you can just reuse it?

![From left to right, Grumpy Kong, Void Kong, and Poppy Kong, three ape-like enemies, strike a pose. From left to right, Grumpy Kong, Void Kong, and Poppy Kong, three ape-like enemies, strike a pose.](https://eu-images.contentstack.com/v3/assets/blt740a130ae3c5d529/blt333b83aeacfe18bd/69c3fb537f33c4c366613f2a/dpr_1_(7).jpg?width=1280&auto=webp&quality=80&format=jpg&disable=upscale)

## At a Glance

- In a 2026 GDC presentation, programmer Tatsuya Kurihara showed off a pipeline for turning 3D assets into voxelized terrain.
- This process let artists create terrain features in a conventional manner, then implement them in a voxel-based environment.
- It also allowed Nintendo to reuse other in-game assets and not create whole new ones from scratch.

Game developers seem to be cautiously opening up about re-using assets once again. In the last year, developers like former Far Cry and Assassin's Creed director [Alex Hutchison](https://www.pcgamer.com/gaming-industry/asset-reuse-in-videogames-is-essential-and-we-need-to-embrace-it-says-assassins-creed-and-far-cry-director-we-redo-too-much-stuff/), Elden Ring Nightreign director [Junya Ishizaki](https://www.gamesradar.com/games/action-rpg/elden-ring-nightreign-director-says-asset-reuse-is-contentious-but-fromsoft-doesnt-consider-it-a-one-to-one-copy-paste-its-just-an-efficient-way-to-build-these-games/), and IO Interactive CEO [Hakan Abrak](https://80.lv/articles/io-interactive-ceo-reveals-surprising-cost-cuts-behind-hitman-series) have all been vocal about why re-using game assets (be they 3D models, sound effects, or other creations) is important for sustainable game design. This candor is notable because for years, certain groups of players have loudly complained when encountering re-used models—but that backlash has been surpassed by the need to make huge games at a more sustainable pace.

Even Donkey Kong Bananza developer Nintendo seems to be coming out of its shell when it comes to discussing this topic. In a 2026 GDC Festival of Gaming [presentation](https://schedule.gdconf.com/session/constructive-destruction-fusing-voxel-tech-and-3d-action-platforming-in-donkey-kong-bananza/916931) that covered the studio's process of building [destructible voxel environments](https://www.gamedeveloper.com/design/how-voxels-enabled-a-juicy-gameplay-loop-in-donkey-kong-bananza), programmer Tatsuya Kurihara showed off a pipeline created by his team that allowed Bananza's art team to quickly create destructible objects that had been sculpted using 3D animation.

Kurihara's explanation of the pipeline was brief, using the head of Bananza antagonist Void Kong as an example. He explained that models like Void Kong's head could be created in Maya, converted into voxel data in Houdini, and then "voxelized" at runtime in Bananza to create polygons. This wasn't used for Void Kong himself, but rather to create a destructible piece of terrain sculpted in the shape of Void Kong's head, akin to the carvings of four US presidents on Mt. Rushmore (also known by the Sioux Nation—which [maintains its territorial claim](https://www.pbs.org/wgbh/americanexperience/features/rushmore-sioux/) to the mountain—as "[Six Grandmothers](https://en.wikipedia.org/wiki/Mount_Rushmore)").

The creation acts both as a shrine to Void Kong's ego—and as a punching bag for players to channel their frustration out on the pint-sized corporate villain. "The shapes of items and enemies, as well as iconic terrain within levels are all created using this system," Kurihara said.

Looking at the model of Kong and its voxelized in-game counterpart—it raised the question whether Void Kong's character model had been repurposed for this stone effigy.

In a follow-up interview with Kurihara and producer Kenta Motokura, the programmer declined to say if Void Kong's head was an example of asset recycling—but he did confirm Nintendo used the Maya-to-Houdini pipeline to take previously-made 3D assets and reuse them for voxel environments.

## Donkey Kong Bananza's voxelization pipeline was a request from the art team

According to Kurihara, the voxelization process came later in Bananza's development, after the programming team gave the Bananza artists and designers tools to make their own voxel creations. "That leads to a situation where the artists or the level designer will start chugging away, and they'll create this complex voxel design that even I, as the creator, [would say] 'I didn't know you could create something so complicated in this level editor.'"

"It got me thinking—'well, what kind of features can I add to make this process easier?'"

Kurihara said after working with the voxel creation tools, they came back to the engineering team and said "we want to be able to actually 'shave' voxels in this state,' and then we implemented a tool to be able to do that."

Artists then could then either create 3D assets explicitly meant to be voxelized, or take existing 3D assets used for non-voxelized characters or objects and convert them into a destructible form.

![A slide showing how a 3D model can be converted into a voxelized form. A slide showing how a 3D model can be converted into a voxelized form.](../../assets/c7db5479c2b49dc6.png)

Slide via Nintendo, photo by the author

It's not the reuse itself that's notable in this instance, but rather how this method for re-use expands the lifecycle of a 3D model beyond its original conception. Asset recycling is conventionally understood as the process of using assets across multiple games—like how the robotic monsters in Horizon Forbidden West [re-used](https://www.spieltimes.io/news/horizon-forbidden-west-criticized-by-fans-over-recycled-animation/) animations created for Horizon Zero Dawn with almost zero modification.

More expansive modification might be used in a game itself. The Elder Scrolls V: Skyrim for instance, famously created varied bookshelf sizes sometimes just by sticking existing bookshelf models in the floor [to create end tables](https://www.reddit.com/r/GamingDetails/comments/c14h53/in_skyrim_the_tables_are_just_bookshelves_pushed/), reducing the number of assets needed to fill out indoor environments.

Bananza's reuse process expands that idea even further, creating a method that allows objects and characters to be manifested as destructible terrain. Now these objects don't just exist for mere aesthetics, they become part of the core gameplay as well.

And considering these objects were not "meant" to be destroyed, they overlapped with a design principle that emerged as iteration progressed in Bananza's development: that it's more satisfying to destroy objects that don't look like they should be destroyed.

Or as Kurihara stated plainly—drawing laughter from the packed room in San Francisco—"It is more fun to destroy that which is beautiful."

Game Developer and GDC Festival of Gaming are sibling organizations under Informa Festivals.