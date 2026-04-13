---
title: Retro CRT Shader Breakdown
url: https://cyangamedev.wordpress.com/2020/09/10/retro-crt-shader-breakdown/
author: Cyan
published: '2020-09-10'
source_blog: Cyan
source_site: https://cyangamedev.wordpress.com
category: game programming
fetched: '2026-04-13'
---

## Intro

Recently I made this shader that attempts to replicate an old **CRT (cathode-ray tube) monitor**, with a few additional distortion/static effects. It was made as part of a tech art/shader challenge over on [Harry Alisavakis’ discord](https://twitter.com/HarryAlisavakis/status/1191692720030584832), with the theme as “**Retro**”.

I’ve also shared the shader and example setup [here on github](https://github.com/Cyanilux/URP_RetroCRTShader).

As explained in the readme on the github, the example also includes a multi-camera setup to render the scene to a low-resolution render texture, to achieve a pixelated look. It could likely be applied to a regular mesh renderer too though, e.g. if you wanted to use it for a TV monitor (and it could still use a second camera render texture or MovieTexture/VideoPlayer to have an animated image too).

In this breakdown we won’t be going over that additional camera setup, and will be applying the shader/blit directly to the main camera’s forward renderer rather than having the low-resolution / pixelated effect. If you are interested in that, you can look at the example given in the above github link. Note that the gif in the above tweet also includes some additional [post processing](https://cyangamedev.wordpress.com/2020/06/22/urp-post-processing/) using URP’s integrated volume system (**Vignette, Film Grain, Chromatic Aberration**).

The breakdown will also mostly go over each effect separately. I’ve tried to mention how they connect up, but if you are unsure you can find the full graph image [here](https://github.com/Cyanilux/URP_RetroCRTShader/blob/master/retro_graph.png).

## Breakdown

##### Blit Setup

To begin we’ll create a new **Unlit Graph** quickly, and a **material** using it. Before we open it up in shadergraph though, we’ll apply it to the screen using a **Blit Render Feature** – like the one found on the [Post Processing in URP](https://cyangamedev.wordpress.com/2020/06/22/urp-post-processing/) post, or my custom one found [here on github](https://github.com/Cyanilux/URP_BlitRenderFeature).

With the scripts in our project assets, we can add the feature to the **Forward Renderer** asset, using our material we just created. We will likely want the blit to occur in the “*Before Rendering Post Processing*” event and only use pass index **0**, but other settings can be left at their defaults.

![](../../assets/4e436abd2e580599.png)

When adding this feature, the screen should go grey as the shader doesn’t output any other colours yet. We’ll now open the graph and create a **Texture2D** with the reference as “**_MainTex**”. This will be important in order to obtain the source texture from the blit feature – which in this case is the colour texture from what the camera has rendered.

![](../../assets/6130ed025c1f3267.png)

We’ll sample that texture with the **Sample Texture 2D** node. We can then connect it to the **Master** node **Color** input in order to see our scene again. That’s not too exciting, but we can now add additional effects and adjust how the texture is sampled to create various distortions.

While we are here, you can also create all the other properties that will be required if you want to :

- Main Texture (
**Texture2D**, reference should be “_MainTex”) - CRT Warp Strength (
**Vector1**, default**1, 1**) - Scanline Height (
**Vector1**, default**10**) - Scanline Strength (
**Vector1**, default**0.5**) - Distortion Strength (
**Vector1**, default**1**) - Static Strength (
**Vector1**, default**0.1**) - RGB Stripe Resolution (
**Vector1**, default**30**for sake of previews, but for material probably want**384**(**128*3**) or something) - Image Brightness (
**Vector1**,**2**)

##### Quick Note about Keywords

For many of the effects included in the final shader, I used [keywords](https://docs.unity3d.com/Packages/com.unity.shadergraph@8.2/manual/Keywords.html) to allow each effect to be toggled on or off. This causes the shader to be compiled into **multiple variants** where the calculations can be avoided when the keyword is off.

This can improve the performance of the shader as you don’t need to do necessary calculations when those effects are off. However with each keyword added it **doubles** the amount of shader variants – which will increase build time (and objects which use separate variants won’t be batched together with the SRP Batcher! For the blit this is less of a problem though, as it’s a single effect and isn’t applied to a mesh renderer to allow that batching to even occur).

I’m using the “**shader feature**” definition for the keywords, which means **unused variants will be stripped from the build**. This is useful to keep the build file sizes down, but if the keywords are adjusted at runtime (e.g. with material.EnableKeyword or DisableKeyword) the required shader might not be included and just show as magenta. If you use the “**multi compile**” definition instead, they will **always be included in the build**, so more useful when adjusting keywords at runtime.

Of course, If you don’t care about being able to enable or disable effects, you can ignore the keywords entirely and just include the effects you want. If you see any keyword nodes (ones with the “**On**” and “**Off**” inputs) you can just ignore it and use whatever the **On** input would be.

##### CRT Warping

First up is replicating the **warping** that some cathode-ray tube monitors had. The **Spherize** node handles this quite well. We simply need to set the **Center** to (**0.5, 0.5**) so it is in the center of the uvs.

In order to control the strength from outside of the shader, I’ve used a **Vector2 property**. The output of this **Spherize** will basically be used for any nodes that use the **UV** input, such as the **Sample Texture 2D**, in order to apply that warping effect.

We also want to apply some black edges to parts outside of the screen. This will hide some of the clamping/stretching that occurs outside of the texture’s bounds but also add to the CRT effect. To achieve this we can use the **Rounded Rectangle** node, with the UVs as our warped result from the **Spherize**. This will be multiplied with our **Texture Sample 2D** output to remove colour from those black parts (since multiplying by **0** results in **0**/black).

![](../../assets/1e2ac3aad2c64b13.png)

##### Scanlines

For the scanlines, we’re using a **Fraction** node which removes the integer part of the value (e.g. **5.5** becomes **0.5**). With a gradient input (like the **Y** coordinate across the screen, obtained from the G output of the **Split** of our warped UVs), it produces a repeating **0-1** pattern. It can be adjusted by first multiplying the **Y** coordinate with a value. Here I’m also taking the **Screen** **Height** into account but you might want to leave that out depending on the result you want.

To make the lines softer, we can **Subtract** **0.5** and use the **Absolute** node. I’ve then included a few nodes to adjust the strength of the effect and **Saturate** clamps it to keep the values between **0** and **1**. This can then be multiplied with our final colour before putting it into the **Unlit Master** node.

![](../../assets/7f0fa5c80ee09c26.png)

**RGB Stripes (phosphors / subpixel)**

With any monitors, a single pixel is made up of various coloured stripes (sometimes dots/other patterns but I’m just doing stripes here), usually **red**, **green** and **blue **(sometimes **BGR** rather than **RGB** though).

In order to produce this effect, I’ve taken the **X** coordinate of the warped UVs (aka **R** output from **Split**). This can be multiplied with a **Vector1 property** to control the resolution (which in this case actually means “*how many coloured stripes*”, so should probably be a multiple of **3**, or you could multiply by **3** separately as well).

We can use the **Modulo** node to convert the position into a repeating **0-3** pattern (similar to what the **Fraction** node did earlier). With this we can use a few **Step** nodes and some math to produce 3 different stripes, which is put into a **XYZ** inputs (aka **RGB**) of a **Vector3** node.

![](../../assets/b0935560e970e6f7.png)

We can **Multiply** this with our main **Texture Sample 2D** to apply the effect. But a side-effect of that is the image looks darker than it was before. To help with this, we can **Add** a brightness value before multiplying.

(I’ve also included the keyword node here, it’s input is the output from the previous image. The output of this image goes to the multiply with the texture sample).

![](../../assets/a7317f7371e95c4b.png)

##### Distortion

Moving back to the UVs for a bit, we can offset them (aka **Add**/**Subtract**, or via the **Tiling And Offset** node if you prefer) using some noise to produce a **distortion effect**. I’m using the **Simple Noise** node for this which produces **2D** noise, but I want to offset each row of the screen by the same amount so really only need **1D**.

I’ve set the input as a **Vector1** based on the **Y** axis from our warped UVs offset by **Time**, meaning all **X** positions produce the same result. Maybe this isn’t the most performant solution but didn’t really want to have to handle noise calculations myself. (Using a scrolling noise texture would be another method).

We also need to **Subtract** **0.5** from our noise result, so that we offset equally in each left/right direction, rather than only to the right. We’ll also be adding some additional effects in the next sections, so for now just create two **Add** nodes, leaving the other inputs with **0**.

Since the UVs of the entire screen are **0-1** and our noise is now in the **-0.5** to **0.5** range, we also need to multiply by some very small values such as **0.1** and a **Vector1** “*Distortion Strength*” **property**, otherwise we would be offsetting a maximum of half of the entire screen’s width which is very much too strong!

To make sure this distortion only occurs in the **X** axis, we put it into the **X** input on a **Vector2** node and **Add** it to our warped UVs from the CRT warping. This result can then be used as the UV input of the **Sample Texture 2D** node instead.

##### Static

In order to add a **static effect**, I’m using the warped UVs and offsetting them by **Time**, then using a **Random Range** node. This generates some pure random noise. (You may also want to use a **Fraction** node on the time to prevent the lines in the noise, produced by precision issues).

![](../../assets/0445cb12017375cd.png)

In order to connect this, we’ll **Multiply** it by a **Vector1** “*Static Strength*” **property** then **Add** it to the **Sample Texture 2D** **RGBA** result (before the multiplies for applying other effects).

I’m also multiplying the **Random Range** output by **0.2** and putting it into one of the **Add** nodes from the **Distortion** section to add a bit of noisy static to that distortion too.

##### Scrolling Static

The final effect to discuss is an additional scrolling static effect, which also affects the distortion further. To achieve this we **Split** the warped UVs again and **Multiply** the **Y/G** axis with **1.5**. We then **Add** **Time** and put it into a **Fraction** node to obtain a repeating **0-1** pattern that moves downwards. I’ve then put this into a **Power** node with a value of **5**, which means the gradient is much less linear than before – which will look better with the distortion.

I’ve multiplied this by **5** and put it into the other **Add** node from the **Distortion** section.

We’ll also take the **Power** node output and **Multiply** it with the **Random Range** from the **Static** section. This applies that static effect to the scrolling pattern, and this could be added with the other static effect as is, but I wanted it to control the colour a bit more. To handle this, I used the **Colorspace Conversion** node which is converting a **Vector3** node from **HSV** (hue, saturation, value/brightness) into **RGB** colour space.

The **X** input into the **Vector3** will be the **hue** for the effect, which I’ve controlled using the **Simple Noise** output from the **Distortion** section. It seems to mostly produce some cyan/green colours, but the noise produces a bit of variation for a “glitchy” effect. The **Y/saturation** will be a constant value of **0.8**, and the **Z/value/brightness** will be controlled by the scrolling static pattern we just made.

The result of the **Colorspace Conversion** can then be added with the other static effect before adding it to the **Sample Texture 2D** **RGBA** result.

![](../../assets/57c8d18adcdca532.png)

Thanks for reading! If you need help figuring out any of the connections you can find a [full image of the graph here](https://github.com/Cyanilux/URP_RetroCRTShader/blob/master/retro_graph.png)!

If you have any comments, questions or suggestions please drop me a tweet [@Cyanilux](https://twitter.com/Cyanilux), and if you enjoyed reading **please consider sharing a link with others**!