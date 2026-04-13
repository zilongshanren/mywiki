---
title: Simonschreibt.
url: https://simonschreibt.de/gat/jedi-fallen-order-splishy-splashy/
author: Simon
published: '2023-05-22'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

This article was updated. Jump to [Update 1](https://simonschreibt.de#update1).

What can I say, I like **water textures**. You too? If so, let’s take a look at some water effects in [Jedi: Fallen Order](https://store.steampowered.com/app/1172380/STAR_WARS_Jedi_Fallen_Order/)! If you want, you can jump to specific sections with this index:

One day, I was happily jumping into a puddle and thought to myself: *“I wonder what the textures look like for this effect!”*

[Jedi: Fallen Order](https://store.steampowered.com/app/1172380/STAR_WARS_Jedi_Fallen_Order/)

Interesting: The first jump doesn’t trigger a splash when I land. Only the second (higher) jump does! It looks like there’s a timer and splashes are only allowed to re-trigger after a certain cooldown.

# Splash

Turns out, there are (almost) no textures used! Instead, they use **mesh particles**. Of course, it’s not uncommon to use splashy meshes in modern games, but to be honest, I didn’t expect, that 95% of the splash is mesh based:

[Jedi: Fallen Order](https://store.steampowered.com/app/1172380/STAR_WARS_Jedi_Fallen_Order/)

Indeed, there are some “classic” particles, but those are only used for the small drops. Below, you can see their texture (I assume that each particle gets random UVs assigned to use one of the bubble bobbles):

The majority of the effect is based on **mesh particles** with a nice (refraction) shader. Yes, these meshes contain way more geometry than a standard particle (with only 4 vertices) but there’s no wasted overdraw which is a huge plus.

[Jedi: Fallen Order](https://store.steampowered.com/app/1172380/STAR_WARS_Jedi_Fallen_Order/)

By the way, there is a nice [tutorial out there for creating such splashy meshes](https://vimeo.com/213730714) by [Andreas Glad](https://twitter.com/partikelvfx).

# Impact

Now, I was hooked and wanted to know if other water effects make use of geometries as well. For example, when this friendly AT-AT has a little accident and falls, we can see some nice water splashes.

[Jedi: Fallen Order](https://store.steampowered.com/app/1172380/STAR_WARS_Jedi_Fallen_Order/)

But in this case: **no meshes**!

[Jedi: Fallen Order](https://store.steampowered.com/app/1172380/STAR_WARS_Jedi_Fallen_Order/)

It’s standard particles using a flip book texture (and again nice refraction in the shader):

Since I mentioned **refraction** twice, here is a little example of how this flip book looks with and without refraction:

It’s very interesting, that small effects like the jump gets these complex meshes, while a huge splash like the AT-AT impact “just” gets standard particles. My guess: It’s about scale. Maybe they decided, that meshes for small-scale splashes are OK but creating geometries for huge splashes (with a lot of detail and drops) would require too much geometry?

# Drops

At this point, I couldn’t tell anymore what’s a particle and what’s a mesh. Are the falling drops or the impact splashes meshes or textures?

[Jedi: Fallen Order](https://store.steampowered.com/app/1172380/STAR_WARS_Jedi_Fallen_Order/)

Both are standard particles, where the splash is using the same flip book texture as the AT-AT [impact](https://simonschreibt.de#impact), and the drops are using this one:

# Bubbles

For the bubbles when diving, I was sure it would be geometric spheres distorted via vertex shader!

[Jedi: Fallen Order](https://store.steampowered.com/app/1172380/STAR_WARS_Jedi_Fallen_Order/)

But I was wrong:

[Jedi: Fallen Order](https://store.steampowered.com/app/1172380/STAR_WARS_Jedi_Fallen_Order/)

Here are the two normal maps which are used for the bubbles: One for the bubble itself and another one to distort the bubble for the classic wobbly look:

The bubble texture has enough space left, right, up and down to be distorted without visible seams!

# Waterfalls

There are some nice waterfalls in the game as well, and I **love** to look at geometries and textures from such cascades.

## Waterfall #1 – Classic-Shmassic

Let’s start with this simple, splashy stream of water.

[Jedi: Fallen Order](https://store.steampowered.com/app/1172380/STAR_WARS_Jedi_Fallen_Order/)

To make it short: It’s all particles using the textures we’ve seen before (the flip book from the [impact](https://simonschreibt.de#impact) and the sprite sheet used by the [drops](https://simonschreibt.de#drops)).

[Jedi: Fallen Order](https://store.steampowered.com/app/1172380/STAR_WARS_Jedi_Fallen_Order/)

## Waterfall #2 – Crossed-Shmossed

At first, I thought we see some classic particles falling down like in the example above.

[Jedi: Fallen Order](https://store.steampowered.com/app/1172380/STAR_WARS_Jedi_Fallen_Order/)

But, I was wrong (again). It’s a same mesh and a nice distortion shader runs these textures along it:

[Jedi: Fallen Order](https://store.steampowered.com/app/1172380/STAR_WARS_Jedi_Fallen_Order/)

Note, that it’s a **crossed** plane. This extra geometry makes sure that the cascade also looks nice, even when seen from the **side**.

## Waterfall #3 – Double-Shmouble

The next waterfall looks similar to the one above **but**…

[Jedi: Fallen Order](https://store.steampowered.com/app/1172380/STAR_WARS_Jedi_Fallen_Order/)

…** **it’s not just one mesh but **two** on top of each other:

[Jedi: Fallen Order](https://store.steampowered.com/app/1172380/STAR_WARS_Jedi_Fallen_Order/)

Note, how distorted the meshes look in the video above where the wireframes are revealed, while the mesh looks **not** deformed in the video below. This is because a vertex shader is deforming the vertices to add some nice wavy motion.

[Jedi: Fallen Order](https://store.steampowered.com/app/1172380/STAR_WARS_Jedi_Fallen_Order/)

The shader running on the left mesh uses the textures on the left and the shader running on the right mesh uses the textures on the right.

## Waterfall #4 – Opaque-Shmopaque

These big scale waterfalls are special: A shader mixes several textures and moves them along a static **opaque** geometry:

[Jedi: Fallen Order](https://store.steampowered.com/app/1172380/STAR_WARS_Jedi_Fallen_Order/)

I’m not sure if **all** of these textures are actually used, but that’s what my analyzer showed me:

Now, there’s **another layer** of waterfalls on top! But this time they use a **translucent** material. We know the mesh already from the [Double-Shmouble](https://simonschreibt.de#double):

And if you asked yourself, how the nice water vapor is added to the level: It’s “just” big planes (which add a very nice depth to the image):

That’s it! I hope you’re as fascinated about water effects and their meshes and textures as I am! If you want to know more about the creation of textures for VFX (e.g. water splashes), continue reading here:

Have a very nice day! ♥

Simon

![](../../assets/ba0680151067ebbc.png)

[Death Stranding](https://de.wikipedia.org/wiki/Death_Stranding) was free in the Epic Store and I wanted to look at their waterfalls for some time anyway, what a nice opportunity! Here are they in their full beauty:

[Death Stranding](https://de.wikipedia.org/wiki/Death_Stranding)

The first surprise: Only **one texture** is used! At first, I thought: *“Wait…only a normal map and nothing else?!”* but then I realized, that they put a nice water structure into the Alpha Channel of this texture!

If you need photos with a similar look, check [these amazing photos on textures.com](https://www.textures.com/download/WaterPlain0036/103463)!

The main mask is coming from the mesh itself in form of **vertex colors**. They use the 3 channels for different masks, but I’m not sure what G and B is used for:

I tried to re-create the waterfall material in Unreal. I’m not sure if I got it right, but I think the main thing is to use the vertex color and add the water mask (from the alpha channel) on top. Here is my material, but like I said: It’s just my guess!

Here you can see me trying to get the alpha and albedo right by comparing the unlit versions:

![](../../assets/84b495bc85e91937.png)


![](../../assets/84b495bc85e91937.png)

If you have any idea how to improve the result, or maybe you’ve even some inside-knowledge: Let me know! :)

The Death Stranding waterfall looks great, though your version seems to be missing a secondary layer scrolling over the base waterfall texture to give the illusion of depth, and it also seems to have sharper shading than the DS version.

My guess for the DS waterfall would be that it uses a very simple SSS shader, or maybe diffuse light wrapping, to soften the shading and make it feel more misty. Also looks like they’re scrolling two versions of the same texture, offset both in speed and alignment.

Yes, I need to take a closer look. I was staring at it and sometimes I thought “no…it’s just 1 layer” and then again sometimes it looked like 2 layers. Thanks for the comment!

I’ve checked and in the DrawCall for the waterfall I can only see 1 sampler. So I guess, there is only 1 scrolling layer but it looks very good and fools the eye… here is a RenderDoc screenshot: https://imgur.com/KapdEvB

RenderDoc only shows here that there is a single normal map bound to the shader. It doesn’t say how many times this particular normal map is sampled. So it could be sampling it multiple times.

Hm….I assumed that inSampler0 would tell us, that there’s only one sampler and if the texture is sampled again it would be inSampler1. But I don’t know..need to compare with other captures where the same texture is sampled more than once and see how it looks.

In hlsl，sampler and texture can declare separately. Renderdoc only show the declared sampler or texture in slot. This mean you can declare a single sampler to sample all texture as point filter. And you can read the DXBC code for sample_ or ld_ keyword to knew how many times to sample ,and actually there are 2 sample_ opcode in DXBC code.

Thanks for your comments explaining all that! <3

Thank you for the great post! It’s very helpful!

Btw, you don’t have any struggle to capture DS by RenderDoc?

I’m having trouble in using RenderDoc on DS, RenderDoc seems not launching and not showing any errors…

My graphic card is RTX 2080.

If you have any information about it, It’d be so much help for me!

I’m not sure if I understand what “DS” means, but if you want, write me a mail with more details. :)

Oh, I’m sorry

DS means just Death Stranding

I just can’t launch RenderDoc on Death Stranding, unlike other games I have in my pc

The Key of WaterFall is the BasePass output Normal actually. The WaterFall is main lighted in the GI Pass(a computer shader pass , in the before direction light pass ,the waterfall is almostly balck and only lighted the part under the sun), have no SSS feature but have great SkyLight effect.

Is it possible the other channels are being used as a flow map?

The masks a very smooth and big gradients. If they are used to distort the textures, it would be quite subtle I think…but who knows?

Thank you for your useful post!

Used the same technique on waterfalls for Rise of the Tomb Raider. R and G were used as blends to lerp between the river mat and white water so we wouldn’t have to do the trick we often see where people place rocks or fold down the top of the waterfall to hide the transition. Still had to place rocks on the bottom at times cuz sorting was a pain tho!

Nice, thanks for the info! Did you use only one scrolling texture layer, or did you use two? I’m looking at DS again to see if they are maybe using two, and I missed that yesterday.

Yeah a couple textures and a mask all channel packed with a separate normal

I’ve just checked the drawcall and it looks like here in this case they only use 1 sampler which I interpret as: Only 1 texture layer: https://imgur.com/KapdEvB

By the way: This water sequence in TR is super cool and I was wondering if it’s a flip sim baked into alembic or VAT…maybe you know it? https://youtu.be/1kKhLDx53VE?t=1123