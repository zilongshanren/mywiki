---
title: Simonschreibt.
url: https://simonschreibt.de/gat/battlefield-bad-company-2-smoke-column/
author: Simon
published: '2013-02-11'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

BF BC 2 had awesome environments and sometimes contained huge smoke columns in the background. Smoke in far distance moves very slow, so it should be totally OK if you wouldn’t animate it. But when you stand still, you can see some movement in the BF BC 2 smoke!

As far as i see, they use a non animated smoke column as base which contains an alpha mask for the borders. OK that’s clear. And then they have a scrolling smoke texture on top which only contains “bright” smoke. This bright smoke seems to be only visible where (a) the base smoke has its alpha and more interesting (b) where the base smoke is bright itself. For me it seems, that the scrolling texture uses the diffuse color of the base smoke as transparency map, because you can’t (or barely can) see the “bright” moving smoke where the base is dark.

Did anyone understand what i mean? :)

I really like this approach because it gives some detail without being too complex. I mean you could try to do this with an particle system but then you never would know what you get exactly as result. Also you would have to pre-calculate the particles because you want the smoke column to be there at game start – not 10 minutes later when the particles slowly moved to their positions.

I think you have it right. It looks like it also has an additive quality. There is the alpha channel which defines the shape of the column, a ‘background’ diffuse which gives volume to the column and then the moving bit added or multiplied or lerped in somehow.

I would love to see the textures they used but it’s not possible to get them. An alternative would be, that the dev artist from Dice writes a comment. That would be awesome :)

Great blog! I’m ploughing through all old posts.

This effect is unlike most discussed here because it doesn’t stand up to close scrutiny, working only in the player’s periphery. I blame the static background part.

It occurs that the shader complexity would be similar if, instead of a static low-frequency brightness + alpha background with a high-frequency brightness detail texture scrolling over it, there was a single scrolling texture defining silhouette alpha + all brightness, with a secondary texture giving distance-related alpha falloff to the smoke. This way it’d look more like a single coherent smoke column.

At first glance it would restrict the scrolling to 45 degrees, but it’s close to that in this BFBC2 effect. I *think* I’ve seen similar techniques, though I couldn’t tell you where.

Thanks for your comment! :)

Yeah a silhouette texture would be another possibility. But instead of a fade-texture i would vote for a shader where you can use vertex colors to make the fading. Hm…reminds me that i have to play the game again someday :)