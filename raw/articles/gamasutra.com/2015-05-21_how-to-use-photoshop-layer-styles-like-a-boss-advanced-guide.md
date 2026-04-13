---
title: How to use Photoshop Layer Styles like a Boss - Advanced guide for game illustrators
url: https://www.gamedeveloper.com/art/how-to-use-photoshop-layer-styles-like-a-boss---advanced-guide-for-game-illustrators
author: Dave Bleja
published: '2015-05-21'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# How to use Photoshop Layer Styles like a Boss - Advanced guide for game illustrators

Photoshop Layer Styles are very powerful and surprisingly versatile, and I use them for almost all of Spryke's graphics. In this guide, I go through various Layer Style tips & tricks, including Pseudo Color Overlays, internal Adjustment Layers and more.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

If you're like many Photoshop users, you might not use Layer Styles much. Or maybe you think that they're only good for cheesy bevel and drop shadow effects. Actually, Layer Styles can be very powerful and surprisingly versatile. In fact, I do almost all of [Spryke](http://www.sprykegame.com/)'s graphics using Layer Styles (applied onto vector shapes).

Note: This guide was first posted on the [Volblog](http://www.volnaiskra.com/volblog/how-to-use-layer-styles-for-efficient-and-versatile-game-illustration-advanced-guide). It is based on Photoshop CC 2014 (the latest version as of writing); minor differences may exist in older or newer versions of Photoshop.

![](../../assets/513542f90f34c33b.img)


## Quick rehash: What are Layer Styles again?

To access Layer Styles, double-click a layer in photoshop. From there, you can tweak various settings to alter the appearance of the layer. Layers that contain Layer Styles have an "fx" icon on them. If you make a Layer Style that you think you'll reuse, you can save it in the "Styles" palette.


![](../../assets/a05ffa999ae10d22.img)


These six identical vector shapes (well, twelve actually, including the little ones in the corners) each have a different Layer Style that greatly affects how it appears.


Below is one of the above layers shown with all of its Layer Style attributes. Not every Layer Style needs to be this complex of course, but by stacking multiple attributes like this, you can achieve a great deal of variety and visual subtlety.

This particular Layer Style is used for lights and other illuminated objects. It has a round inner glow (from Gradient Overlay), intense coloring (Color Overlay and Satin, both using Overlay Blend Mode), noise (Inner Glow), and a somewhat intense reddish glow (Stroke, Outer Glow, Drop Shadow).


![](../../assets/189cd27e8eaeb3bc.img)

![](../../assets/57e81674b169c38d.img)

![](../../assets/cbff8da07912f560.img)


This next Layer Style provides a worn diamond metal plate look. The foundation of the Layer Style is the Pattern Overlay, which provides the diamond plate texture. The colour is first neutralised somewhat (Color Overlay), then intensified (Satin with Overlay Blend Mode). Finally, a subtle degraded appearance is added by a rust-coloured Inner Shadow.

![](../../assets/8c677e665e3ffb71.img)


## What's the benefit of Layer Styles?

There are three main benefits, all of which intertwine:

Non-destructiveness

I'm a firm believer in keeping your workflow as non-destructive as possible. The secret of great design is iteration, and keeping everything editable rather than locked down makes iteration much easier. Thanks to Layer Styles, I can tweak, overhaul, swap or remove the appearance of just about any visual element at any stage.

Quickness

Certain things are just way quicker using Layer Styles than with most other methods. Some examples include: filling with a solid color, creating an outline, adding some noise, creating a glow effect, or filling an effect with a pre-existing texture or image (using Pattern Overlay).

Re-usability

Layer Styles can be copied and pasted from one layer to another, and saved in the Styles palette. This is of particular use to game artists, since we tend to make a large amount of assets, many of which share similar stylistic traits.

When you combine all of these benefits, you get a workflow that is efficient, highly organic, and can grow and evolve with your project. As you work, you can build up a library of Layer Styles that you apply to subsequent assets, tweaking and experimenting when necessary. As your project's aesthetic evolves, you can retrofit earlier assets with updated stylings.


## Are there drawbacks of Layer Styles?

A few. For one, they aren't a silver bullet (but then, with the possible exception of actual silver bullets, what is?). As you'll see below they can do a lot, but they can't do everything. Sometimes you'll still need to use other techniques (painting, photography, filters, etc.) in conjunction with Layer Styles.

They also have a few rigid idiosyncracies. For example, the number, type, and order of attributes are fixed (eg. you can only have one Pattern Overlay, and it always must be below any Color Overlay). And certain behaviours (eg. Stroke combined with translucency) are just plain weird.

But with a little ingenuity these problems can, for the most part, be solved or worked around. More on that later.

Probably the most serious drawback of Layer Styles is performance. If you're using just a handful of Layer Styles then no problem, but if you use hundreds like I do, Photoshop can start to get laggy, no matter how good your computer is (mine's a [beast](http://www.volnapc.com/about.html)) - especially if you're using lots of different blending modes inside them. This isn't really the fault of Layer Styles per se; the performance hit comes from using loads of layers and blending modes in general.

The solution here is to be smart about how you work. Group separate elements in your composition into folders (Layer Groups) and turn them off when necessary. Or, better yet, turn them into Smart Objects. This removes their resource footprint from the current document by displaying a flattened, rasterized version (which you can double-click to access the original editable layers). In the image at the top of this post, every ship and every building is a separate smart object (some of them duplicated).


## Creating a Layer Style library

As your project grows, it's a good idea to start saving your Layer Styles in one place, to make re-use easier. You can use the Styles palette for this (that's exactly what it's for) but I prefer to lay them all out in a separate PSD, as you can see below. This lets me lay them out in more organised way, with labels and compartmentalised groups.

Also, the Styles palette is comprised of squares, while the PSD method allows me to use custom shapes that will better represent the potential of each Layer Style. As you can see below, I use two shapes per Layer Style; together, they show me what a layer style looks like on a large layer, a tiny layer, a round edge, straight edge, corner, and hole.


![](../../assets/6b5fc8ed1fa58f15.img)


The Layer Style library I use for Spryke (click to enlarge)

## Combining Layer Styles

Here you can see a step-by-step process of how I applied layer styles to one of Spryke's elements - a "Weasel" ship. The majority of layers are Vector Shapes (shown initially as wireframe). I add a few small raster elements in the last step.

As you add Layer Styles to differently shaped objects, you may need to tweak them a little. For example, the angle of the red gradient on the wing needed to be rotated when applied to the tail. Similarly, the size of the glow of a large light might need to be taken down a notch when applied to a small one. Thankfully, the non-destructiveness of Layer Styles make this kind of fine-tuning pretty easy.

Also, take note that in some cases, I couldn't achieve everything I wanted in one Layer Style, so I had to duplicate a layer and use more than one set of Layer Styles. This mainly occurred in the context of Pattern Overlays, the only way to import a raster image into Layer Styles. Photoshop only permits one Pattern Overlay per layer style, but I wanted three - a dirty texture, black scratches, and white scratches - so I had to use three identical layers, each with its own Layer Style. (I could have combined all three textures into one pattern, but that would have given me less flexibility.)



![](../../assets/830624aca234e9bd.img)

![](../../assets/e8054ee95df12971.img)



And here's one of Spryke's buildings. Again, practically every element is a Vector Shape with Layer Styles applied to it. (A few more Layer Styles were used than what is shown, but this is the bulk of them).


![](../../assets/d478369dafcdabd8.img)



## Layer Styles for versatility

Because they're so tweakable and non-destructive, Layer Styles are excellent for creating variations of your assets, and even for early experimentation and brainstorming.


![](../../assets/acf1f433c0813e04.img)



![](../../assets/82cc17fa76456894.img)


## Layer Styles as internal Adjustment Layers

So far, I've concentrated on Layer Styles used on their own (ie. setting Fill Opacity to 0% so that none of the original layer contents can be seen). But Layer Styles can also be used as a quick and easy way of adjusting a layer's existing contents, as you would with an Adjustment Layer.

Let's say you want to desaturate a layer. You could do Image>Adjustments>Desaturate (Ctrl-Shift-U), which is very quick but also destructive (you can't change your mind and revert to color later).

You could also use a Hue/Saturation or Black&White adjustment layer. This is non-destructive (and in the case of Black&White, very nuanced), but it's also a little clunky: it creates a separate layer, and by default it'll desaturate all layers underneath it, not just your target layer.

A third option is to use a simple Layer Style: Color Overlay, black (or white, or grey), 100% Opacity, Saturation Blend Mode. This is relatively quick, non-destructive, and has a light footprint in your Layers palette. And of course, you can save the Layer Style so you can copy/paste it to other layers later.

Below are a few examples of possible adjustment types, including desaturation, contrast, colorize, noise, and brightness. Note that in the centremost version, I've used Satin to change the color of the circular metal area without affecting the rest of the creature (more or less).

One of the benefits of this approach is that you can stack multiple effects using Pseudo Color Overlays (see next section) all within just one Layer Style, which helps keep your document compact.


![](../../assets/20717f9567e50e51.img)


Spryke, shown with various adjustments, using Layer Styles


## Pseudo Color Overlays


UPDATE (24 June 2015): Photoshop CC 2015 has introduced the ability to use multiple versions of the same Layer Style attribute within the same Layer Style. So, we can now click a "+" button to get up to 10 Color Overlays at once. This is nice, and alleviates the need for Pseudo Color Overlays somewhat, though not completely.

As of writing, you still can't rearrange the order of Layer Style Attributes. So, for example, if you want a Color Overlay that is applied over the top of an Inner Glow, or before a Gradient Overlay, you'll still need to use the appropriate Pseudo Color Overlays.


In the next section, I'll go through each of the attributes with tips and tricks for each. But first I want to bring attention to what I've dubbed Pseudo Color Overlays.


Color Overlay allows us to apply a colour to the entire layer, which makes it highly useful. Ostensibly, it's the only Layer Style attribute that does so. However, with the correct settings, a number of the other attributes can be made to function in essentially the same way. Here is a list of Pseudo Color Overlays, in order of quickest to most convoluted:


Inner Shadow: 30000px Distance, 0% Choke

Satin: 1px Distance, 250px Size

Inner Glow: 100% Choke, 0px Size, Source: Center

Gradient Overlay: Set up a gradient with identical colour on both ends of spectrum

Pattern Overlay: Create custom pattern that is just a single colour, and use that



Why is this useful? Because it allows you to apply several entire-layer adjustments to a layer in one go. I'll illustrate this with an example.

Let's imagine that we have a shiny blue spaceship that we'd like to make look a bit more aggressive: red, more starkly contrasted, and a little rougher-looking. Also, we want to do this non-destructively.

We'll need to change the ship's color, add texture, and fine tune the brightness/contrast. With the Adjustment Layer method, this would require several new layers. But with Pseudo Color Overlays we can do it all on the original layer, a more compact and more portable solution.

OK, here's our initial blue ship:

![](../../assets/419af688530afb77.img)


First, we use a Pseudo Color Overlay (Gradient Overlay in this case) to change the hue of the entire layer from red to blue:

![](../../assets/6c383411e23abe7d.img)


That's a good start, but it feels too monochrome and maybe a bit too plasticky. Let's add a second color into the mix for nuance, using the 'real' Color Overlay this time.


![](../../assets/576f1e5fff7984f0.img)



That's more interesting, though the addition of cyan tinges has messed up our reds (and whites) a bit. Let's counteract that by applying another reddish colour over the whole layer with another Pseudo Color Overlay (Satin, using the settings listed earlier). We'll use an Overlay Blend Mode again to boost the contrast:


![](../../assets/aebde1fb87ff3f30.img)



OK, the color looks good. Finally, let's add a little bit of noise to the whole thing for a bit of a rougher texture, using Inner Glow:


![](../../assets/20ac7b0ebe197714.img)



OK, there we have it. The method was perhaps a little quick and dirty, but the results are satisfactory. Our ship is redder, rougher, and has a sharper contrast. And, thanks to Pseudo Color Overlays, the whole thing was achieved with just one Layer Style which can easily be disabled, modified, or copied/pasted at any time.


![](../../assets/78d893ab2029f114.img)



## Tips & Tricks for each Layer Style attribute

OK, I'll now provide a few tips, tricks, and potential pitfalls of each Layer Style attribute. I won't explain the basics about each attribute, because you can find those out yourself with a few minutes of experimentation, if you don't know them already.

Bevel & Emboss


Can be useful as a cheap method to create some depth, but proceed with caution. Along with filters such as Filter>Stylize>Find Edges, nothing says "it's my first time using Photoshop!" like heavy-handed use of Bevel & Emboss.

Using Outer Bevel and Smooth, it can be used as a substitute for Drop Shadow

Using Inner Bevel, Chisel Soft, Depth 1000%, Soften 0, Angle 0, Altitude 0, Shadow Mode Normal, it approximates an inside Stroke, but without the translucency bug (see below)

The Texture section allows you to import a monochrome version of any raster image as a highly configurable sort of bump map

The Link with Layer checkbox in the Texture section refers to whether or not the texture will change when you move the layer around the canvas



Stroke

Stay away from blend modes other than Normal 100%, because of the translucency bug (I don't know if this is a bug or a feature, but it's damn annoying so I'm calling it a bug): Applying a Stroke negates all other Layer Style attributes for the affected pixels. For example, if you apply a red Color Overlayand then a blue 6px Inside Stroke, and turn down the stroke's opacity to 50%, instead of seeing a 6px band of purple surrounding the shape, you'll just see a faint blue band, because the red Color Overlay in that 6px band has vanished. See Bevel & Emboss, Inner Shadow and Drop Shadow for workarounds to this problem.

Whenever a stroke looks jaggy or weird, try the other two position settings, as they can sometimes have surprisingly different results.



Inner Shadow

Draggable: while the Inner Shadow section is selected in an open Layer Style dialog, you can drag the canvas to adjust the positioning of the effect

Don't let its name limit you - it can be used for much more than shadows; try it with various Blend Modes

It's one of three effects that includes a Noise slider. This makes it great for quickly adding a bit of texture to an object (try it with Overlay, Screen, or Multiply)

With a 30000px distance and 0% Choke, Inner Shadow becomes a Pseudo Color Overlay (see previous section). Use this in conjunction with Noise to apply noise over the entire layer.

With a 0px Distance and 100% Choke, it effectively becomes an Inside Stroke without the translucency bug. Use it in conjunction with an Outside Stroke if you want a two-coloured border on an object


Inner Glow

Like Inner Shadow and Drop Shadow, it contains a Noise setting

With 100% Choke and Source: Edge, it effectively becomes another Inside Stroke without the translucency bug. Use it in conjunction with an Outside Stroke if you want a two-coloured border on an object, and add a smaller 0 Distance, 100% Choke Inside Stroke for a three-color border

With 100% Choke, Source: Center, and 0px Size, it becomes a Pseudo Color Overlay

Despite Inner Glow appearing above Satin, Satin's effects will be displayed over the top of Inner Glow's. I assume this is a bug.



Satin

Usually only affects a portion of the inside of a layer, so use this to add nuance to an other-wise flat layer.

Draggable: while the Satin section is selected in an open Layer Style dialog, you can drag the canvas to adjust the positioning of the effect

Can sometimes be used to affect only certain elements of an image by carefully adjusting angle, distance, and size, though this potential is constrained by the limited control of the settings.

With 1px Distance, 250px Size, it becomes a Pseudo Color Overlay



Color Overlay

The simplest of the Layer Style attributes

Affects entire layer, which is very useful

Depending on which Blend Mode you use, you can use it for different purposes including, but not limited to: desaturate (Saturation), intensify (Overlay, Color Dodge), tint (Color, Hue), de-tint (Subtract), adjust brightness/contrast (Darken, Multiply, Lighten, Screen, Luminosity)

Can be simulated by Pseudo Color Overlays, which allows several whole-layer effects at once



Gradient Overlay

Useful for helping to simulate lighting or depth

Try using a gradient with a combination of opaque and transparent areas to add a glass-like glare or sheen

Draggable: while the Gradient Overlay section is selected in an open Layer Style dialog, you can drag the canvas to adjust the positioning of the effect

A Gradient Overlay that looks good on one shape will frequently need to be adjusted before it looks good on another shape. Before adjusting the gradient itself, try fiddling with Reverse, Angle, and Scale, as well as dragging the canvas



Pattern Overlay

Basically allows you to import any raster image into your Layer Styles, which adds a whole new dimension of possibilities. As well as actual patterns, this can be used to add texture, photographs, or even text to your Layer Styles.

Consider creating custom patterns specifically for use with Layer Styles (Edit>Define Pattern)

By using a custom pattern that is a single solid color, this becomes a Pseudo Color Overlay. Because of Pattern Overlay's position in the attribute hierarchy, this is also the only Color Overlay (pseudo or otherwise) that lets you use a Gradient Overlay over the top of it.

Draggable: while the Pattern Overlay section is selected in an open Layer Style dialog, you can drag the canvas to adjust the positioning of the effect

Remember to play with the Scale slider, as it can make a powerful contribution to the effect

The Link with Layer checkbox refers to whether or not the texture will change when you move the layer around the canvas



Outer Glow

Don't let the name limit you. With the right blending modes and colors, it can be used to simulate shadows too.

Use it in conjunction with Drop shadow to simulate lighting from two simultaneous sources.

Match the Color, Blend Mode, and Opacity with those of Color Overlay for a seamless continuity between the two effects (great for making fire or lights)

With a 100% Spread, it effectively becomes an Outside Stroke without the translucency bug. Use it in conjunction with an Inside Stroke if you want a two-coloured border on an object.



Drop Shadow

Don't let the name limit you. With the right Blend Mode, it can be used to simulate glows too. Try combining it with Outer Glow for a two-part glow (eg. a large soft blue glow with noise combined with a short, intense white glow without noise)

Draggable: while the Drop Shadow section is selected in an open Layer Style dialog, you can drag the canvas to adjust the positioning of the effect

If the rest of your Layer Style is translucent or transparent, uncheck Layer Knocks Out Drop Shadow to avoid a sharp, unnatural cutoff between the layer shape and the shadow.

With a 0px Distance and 100% Spread, it effectively becomes an Outside Stroke without the translucency bug. Use it in conjunction with an Inside Stroke if you want a two-coloured border on an object.


## General Layer Style Advice

Always feel free to experiment. For the most part, Layer Styles aren't particularly complicated, but they are idiosyncratic, which means that it's easy to understand them, but only after a bit of playing around.

If you want a Layer Style to modify the existing layer contents, set Fill Opacity to 100%

If you want a Layer Style to replace the existing layer contents (except its shape), set Fill Opacity to 0%

You can apply Layer Styles not only to Layers, but to folders (Layer Groups) as well. Layer Styles that are applied to nested Layers and/or Layer Groups will stack.

As with many dialog boxes in Photoshop, holding down Alt changes the Cancel button to Reset, which is useful.

If you add a Mask to a layer with a Layer Style, you'll find that things like Stroke and Outer Glow wrap themselves around the shape of the new Layer Mask rather than just the original layer shape. To stop this behaviour, go to Blending Options: Custom and check Layer Mask Hides Effects or Vector Mask Hides Effects

If you're going to use Layer Styles a lot, you'll probably want to assign custom hotkeys to Copy Layer Style, Paste Layer Style, and Clear Layer Style, as well as one or two individual attributes (eg. Color Overlay)

To avoid cluttering up your Layers palette, click the top-right icon on the Layers palette, select Panel Options and uncheck Expand New Effects (I also set Thumbnail Size to None).


## A final note about Blend Modes

In Photoshop, any pixel that isn't 100% opaque won't have its Blend Mode honoured when flattened or exported. Note that this issue isn't unique to Layer Styles.

Take the following [somewhat ugly...sorry] example:


![](../../assets/8f18c83e03788c25.img)



The shape on the left has a blue Color Overlay and a white Inner Glow and white Outer Glow. Because of the Exclusion and Difference Blend Modes, these glows appear magenta and yellow.

The shape on the right is exactly the same shape, but flattened*. Notice how the Blend Mode of the Inner Glow was honoured, while the Blend Mode of the Outer Glow was not.

The Inner Glow was honoured correctly because it occurred on a 100% opaque portion of the shape, due to the Color Overlay underneath the Inner Glow.

Had the Color Overlay been 50%, the yellowness of the Inner Glow would have persisted, but only partially. Had the Color Overlay not been there at all, the Inner Glow would have suffered the same fate as the Outer Glow. Namely, it would have reverted to Normal, and thus become white.

* in this case, the shape was flattened by being converted into a Smart Object. You'd get the same result with Layer>Flatten Image, Rasterize Layer, or if you saved it as a PNG.

That's it for the guide. I hope it's been useful, and happy creating! For more guides, check out the [Volblog](http://www.volnaiskra.com/volblog).