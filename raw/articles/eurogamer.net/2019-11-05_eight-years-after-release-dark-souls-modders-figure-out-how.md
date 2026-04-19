---
title: Eight years after release, Dark Souls modders figure out how to make custom
  maps
url: https://www.eurogamer.net/8-years-after-release-dark-souls-modders-figure-out-how-to-make-custom-maps
author: Emma Kent
published: '2019-11-05'
source_blog: Eurogamer.net
source_site: https://www.eurogamer.net/
category: graphics
fetched: '2026-04-19'
---

It might be surprising, but until this point it's been pretty much impossible to import a custom map into the original Dark Souls. According to Souls modders, the closest you could get was importing maps from Demon's Souls - and while modders have worked on custom maps for some time, problems with the specific file format used for collision detection in Dark Souls 1 meant that progress was stalled.

Until now, that is, as several modders have figured out a way to import working custom maps into the game.

[As explained by modder Zullie](https://twitter.com/ZullieTheWitch/status/1191504686723018752), progress began in earnest when modder [Meowmaritus](https://twitter.com/meowmaritus) created a [tool to import models](https://github.com/Meowmaritus/FBX2FLVER), but without collision detection (in layman's terms, the physics required to make things actually solid). The next step was carried out by modder [Horkrux](https://github.com/horkrux), who recently developed a way to create collision maps.

Why was it so hard to get to this point? As [modder Katalash explained on Reddit](https://www.reddit.com/r/Games/comments/drqwt6/modders_meowmaritus_and_horkrux_have_figured_out/f6kxbhy/?utm_source=share&utm_medium=web2x), all Dark Souls games use the proprietary (essentially secret) file format Havok to store collision data, with FromSoftware adding their own customisations on top. "To further complicate matters, the file format and stored data change drastically between game to game," Katalash added. But Horkrux figured out that using an old version of Havok Content Tools (that were released publicly for only a short window of time before Havok stopped distributing them) would allow them to create collision maps in Dark Souls 1, Dark Souls: Prepare to Die Edition and [Dark Souls 2](https://www.eurogamer.net/games/dark-souls-ii).

"Simply put, we were apparently way overthinking it," Zullie told me over Discord.

"We had initially thought we'd have to reverse engineer the collision format that Dark Souls uses in order to be able to generate custom collision, but Horkrux figured out how to do it just by using official Havok tools. It turns out FromSoftware didn't make anything especially fancy, Horkrux just needed to make a template for Havok."

After Meowmaritus and Horkrux figured out the framework, Dropoff undertook the final stage by working to import the Half-Life map Crossfire as proof of concept (something Zullie told me took considerable work to get to a usable state). Check it out in the video below:

[Watch on YouTube](https://www.youtube.com/watch?v=_3bABuMHABw)

While this is a significant breakthrough for the Dark Souls modding community, both Katalash and Zullie believe there's still a long way to go before importing custom maps becomes an easy process.

"The Souls modding community is lacking any sort of formal support, but more than makes up for it in passion," Zullie said. "A few years ago it was a Herculean effort to just put a new model for a weapon into the game. We're continually picking the game apart and then developing the tools to streamline it."

"However, I don't imagine anyone's likely to make an automated process for this while navmeshes remain an obstacle, since the practical applications would be pretty scarce," she added. ([Navigation meshes](https://en.wikipedia.org/wiki/Navigation_mesh) are necessary to help NPCs and enemies pathfind around a map - and like collision data, navmesh data varies wildly between the Souls games.)

"Without them, the best we can essentially make would be strictly PvP focused arenas. With them, we could create entirely new, fully functional levels for the game - player published DLC, for all intents."

It seems like a difficult but promising future for Dark Souls modders - and with Katalash (author of the [Unity-based visual map editor DSTools](https://www.reddit.com/r/darksouls3/comments/awrtei/dstools_a_visual_map_editormodding_toolkit_for/)) and others looking into making tools to create navmesh files, we could see some truly exciting mods in the coming years.