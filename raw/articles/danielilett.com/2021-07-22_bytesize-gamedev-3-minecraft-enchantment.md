---
title: 'Bytesize Gamedev #3 - Minecraft Enchantment'
url: https://danielilett.com/2021-07-22-bytesize-3-minecraft-enchantment/
author: Daniel Ilett
published: '2021-07-22'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

*Minecraft* is still one of the biggest games in the world after about a decade, and one of my favourite visual effects from the game is the shine applied to enchanted gear. In this Bytesize Gamedev, we’ll translate it to Shader Graph.

Bytesize Gamedev is a series of shorter game development tutorials.

Hang out with me and other shader enthusiasts over on [Discord](https://danielilett.com/(https:/discord.gg/tPQEUwPpb3)) and share what you’re working on! And check out this tutorial over on YouTube:

# Minecraft Enchantment

When you enchant items in *Minecraft*, it gains a purple glowing effect on top of whatever magical augmentations you chose. We can simulate the glow using a scrolling texture, and I got the best results by sliding two textures over the model in different directions. Today, we’ll apply the effect to a *Minecraft* pickaxe using Shader Graph - let’s jump into it.

We’ll start with a Sub Graph. Since we’re sampling the texture twice, we can bundle everything to do with the enchantment shine sampling into a Sub Graph so that our main graph is neater. Go to *Create -> Shader -> Sub Graph*, and name it `EnchantmentShine`

. This Sub Graph will output a single `Color`

called `OutColor`

, which you can modify in the `Output Node`

’s settings.

![Your graph can have little a graph, as a treat. Sub Graph Creation.](../../assets/757e2ec20b21af3b.png)

*Your graph can have little a graph, as a treat.*

For the Sub Graph, we’ll add a couple of properties: a `Vector2`

called `Scroll Speed`

and a `Texture 2D`

called `Enchantment Texture`

. You can name them whatever you want, as long as it’s descriptive.

![You can multi-select properties to see them all in Node Settings. Sub Graph Properties.](../../assets/fde9836cac77ccfb.png)

*You can multi-select properties to see them all in Node Settings.*

Then we can sample `Enchantment Texture`

with a `Sample Texture 2D`

node. I multiply the **RGBA** and **Alpha** outputs since we will be using this color additively, then output it to the `Output Node`

.

![These nodes are very enchanting. Sample Enchantment Texture.](../../assets/624582406b8965bf.png)

*These nodes are very enchanting.*

To use the `Scroll Speed`

, I’ll take a `Tiling And Offset`

node and output it to the `Sample Texture 2D`

’s UV input - this is often the easiest way to modify UVs. Since the enchantment shine appears diagonally on objects in *Minecraft*, we’ll stick a `Rotate`

node in here to use as the base UVs for the `Tiling And Offset`

. A **Rotation** of about 15 degrees with a **Center** of (0.5, 0.5) works well. For the **Offset**, I will use `Scroll Speed`

multiplied by `Time`

.

![They see me scrollin'. Sub Graph UVs.](../../assets/4228b45f803be211.png)

*They see me scrollin’.*

Now we’ll handle the main graph, which will be Lit/PBR, depending on your Unity version. Go to *Create -> Shader -> Universal Render Pipeline -> Lit Shader Graph* and name it `Enchantment`

.

![This might be different on older versions - look out for PBR Graph if Lit isn't available. Main Graph Creation.](../../assets/1f7ef2cc30126d69.png)

*This might be different on older versions - look out for PBR Graph if Lit isn’t available.*

The first property here will be `Main Texture`

, and I’ll assign the pickaxe texture by default. Then we’ll add an `Enchantment Texture`

, the same as the Sub Graph, and assign the glow texture by default.

![We won't need Scroll Speed like the Sub Graph, because we'll be assigning values inside the main graph. Main Graph Properties.](../../assets/eda846d6e78327a0.png)

*We won’t need Scroll Speed like the Sub Graph, because we’ll be assigning values inside the main graph.*

We’ll sample the `Main Texture`

, then add two `EnchantmentShine`

nodes - that’s the Sub Graph we made - using the `Enchantment Texture`

. Give them **Scroll Speed** values of (-0.3, 0.6) and (-0.5, 1.3) - you can tweak these if you want. Multiply the second one by 0.25 because we want it to be fainter than the other, then add both together and add the result to the `Main Texture`

sample.

![Using two offsets is usually a good approach for more variation. Main Graph Nodes.](../../assets/37f3cd277cefa2f6.png)

*Using two offsets is usually a good approach for more variation.*

Now we can start outputting things. The result of the final `Add`

node will be used as the **Base Color**. Through experimentation, I found that it’s best to then use the previous `Add`

node for both **Emission** and **Metallic**, which gives the pickaxe a lovely glow.

![You can tweak these if you want - this looked best to me. Main Graph Output.](../../assets/def23c0b364ca64a.png)

*You can tweak these if you want - this looked best to me.*

Thanks for reading *Bytesize Gamedev*, your one-stop shop for shorter game development tips, tricks and tutorials!