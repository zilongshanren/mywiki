---
title: 'Bytesize Gamedev #2 - Sprite Wobble in Shader Graph'
url: https://danielilett.com/2021-06-18-bytesize-2-sprite-wobble/
author: Daniel Ilett
published: '2021-06-18'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

Some games like [scribbl.io](https://skribbl.io/) have a cute sprite ‘wobble’ effect, with a two-frame animation. In this tutorial, we will implement that same effect in Shader Graph!

Bytesize Gamedev is a series of shorter game development tutorials.

Hang out with me and other shader enthusiasts over on [Discord](https://danielilett.com/(https:/discord.gg/tPQEUwPpb3)) and share what you’re working on!

# Sprite Wobble

Start by creating a new Sprite Unlit graph via *Create -> Shader -> 2D Renderer -> Sprite Unlit Graph (Experimental)* - on newer Unity versions, this is *Create -> Shader -> Universal Render Pipeline -> Sprite Unlit Graph*.

![Gotta start somewhere. New Shader.](../../assets/bcb3ff40653ce9c6.jpg)

*Gotta start somewhere.*

We’ll create four properties: `Main Texture`

, a regular `Texture2D`

; `Flow Map`

, another `Texture2D`

; `Strength`

, a `Vector1`

/`Float`

with a default of `0.005`

; and `Speed`

, another `Vector1`

/`Float`

with a default of `4`

.

![A few basic properties is all we need! Properties.](../../assets/3442789f84b5207c.jpg)

*A few basic properties is all we need!*

Then we need a clock. I’m going to make mine use 4 frames of animation. Take a `Time`

node’s **Time** output, `Multiply`

it by `Speed`

, and then `Modulo`

the result by 4. `Floor`

that, then `Divide`

by 4.

![Better than TikTok. Animation Clock.](../../assets/5980ead56e355832.jpg)

*This clock’s better than TikTok.*

That’s going to become a UV offset. Funnel the clock result into a `Tiling And Offset`

node’s **Offset** pin, with the **UV0** channel in the **UV** input.

![This only works if your flow map is set to repeat! UV Offset.](../../assets/e5a825b29ed24e8b.jpg)

*This only works if your flow map is set to repeat!*

Connect the modified UVs to the **UV** input of a `Normal From Texture`

node, with the `Flow Map`

in its **Texture** slot. This will generate offset vectors for the ‘wobble’. `Multiply`

by `Strength`

.

![You could alternatively use Strength in the Normal From Texture's input. Flow Map.](../../assets/cf7237c2696bfd7e.jpg)

*You could alternatively use Strength in the Normal From Texture’s input.*

Add these offset vectors to a `UV`

node, then use the result in the **UV** field on a `Sample Texture 2D`

node. That node will be sampling the `Main Texture`

. Then we can output its result to the **Color** field on the Master node, and we’re done!

![Ignore the weird preview on Sample Texture 2D - it ignores alpha for some reason. Color Output.](../../assets/eff04c0e21afe31b.jpg)

*Ignore the weird preview on Sample Texture 2D - it ignores alpha for some reason.*

Thanks for reading Bytesize Gamedev, where I bring you short game development tips in an easy to digest format!