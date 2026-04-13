---
title: Watercolour Shader Experiments
url: https://cyangamedev.wordpress.com/2020/10/06/watercolour-shader-experiments/
author: Cyan
published: '2020-10-06'
source_blog: Cyan
source_site: https://cyangamedev.wordpress.com
category: game programming
fetched: '2026-04-13'
---

![](../../assets/ba06c78b754c2192.png)

[Twitter thread here](https://twitter.com/Cyanilux/status/1312011823697342464).

## Intro

Hey! I’ve been experimenting with “**Watercolour**” shader effects as part of a tech art/shader challenge over on [Harry Alisavakis’ discord](https://twitter.com/HarryAlisavakis/status/1191692720030584832).

The final result contained **3** shaders with a watercolour look, as listed below. There is also a skybox shader which wasn’t made as part of the challenge but felt like it fit the scene quite well. You can find that in [this twitter thread](https://twitter.com/Cyanilux/status/1310989532746178560).

: Objects/Meshes in the scene have a shader which uses a noise texture with the**Object Shader****Triplanar**node. This samples the texture**3**times, “projecting” it onto objects from each axis. This is more expensive but prevents the noise having obvious seams that could be produced with regular model uvs. The shader also samples the main light’s shadowmap to apply a watercolour shadow effect (which looks best with smooth shadows enabled).: There’s an image effect shader over the entire screen which uses a**Image Effect / Blit Shader**[Blit Renderer Feature](https://github.com/Cyanilux/URP_BlitRenderFeature)to apply it. This shader is responsible for the outlines effect, slight distortion and the noisy white vignette to give the effect of the watercolour paint fading out at the edges of the screen.: A few watercolour paint splodges have also been placed around the scene using a shader that reconstructs the world position from the**Decal Shader****Scene Depth**, and transforms it into object space to project textures/noise onto other meshes – essentially what a decal is, but probably not the best way to achieve decals. If this was used in an actual game it would also project on the player as it walks through. Also be aware that the camera cannot go into the decal mesh or the effect disappears.

I’ve also shared the project files on [Github](https://github.com/Cyanilux/URP_WatercolourShaders), though I suggest reading this post and recreating the shaders for yourself, as it will help you learn more! As always, these were written for the **Universal Render Pipeline **(URP). Similar concepts may work in HDRP but probably not without edits (and a different way to blit to the screen, as the renderer feature is a URP specific thing as far as I’m aware).

## Object Shader

##### Watercolour Shadows

First up is the shader applied to **objects/meshes** in the scene. I’m using an **Unlit Master** node as I want to handle some **custom lighting/shading** rather than relying on PBR.

In order to handle this we need a custom function to obtain information about the main light, and sample it’s shadowmap. For the **Unlit Master** we need to add some additioanl keywords to make sampling shadows work (or edit the custom function further). Luckily I already have set up a **sub-graph** to handle this – you can find more info on the [Shader Graph Custom Lighting](https://cyangamedev.wordpress.com/2020/09/22/custom-lighting/) post.

![](../../assets/fc68a1e4ed872948.png)

The subgraph here takes a World **Position** in for sampling the shadow, rather than specifying the node in the graph itself. This allows us to offset that position a bit, e.g. using some noise so the shadows aren’t perfectly straight. However a problem arises when offsetting the shadow position, as we can offset into the mesh, which creates shadows where we don’t actually want them. As a way to combat this, I’m controlling the strength/direction of the offset by using the light’s rotation. I played around with a couple methods for this but found the following to produce the best results.

In order to obtain the light’s rotation, I’m using a C# script on our **Main Directional Light**. This constructs a rotation matrix and passes it into shaders using a global matrix property, like so :

```
using UnityEngine;
[ExecuteAlways]
public class SetMainLightMatrix : MonoBehaviour {
private int property = Shader.PropertyToID("_WorldToMainLightMatrix");
void Update() {
// Create Rotation Matrix from transform.
// Basically transform.localToWorldMatrix, but only rotation.
Matrix4x4 matrix = Matrix4x4.Rotate(transform.rotation);
// Set Global Matrix shader property
Shader.SetGlobalMatrix(property, matrix);
}
}
```

From here, we can obtain this in shader graph by creating a **Matrix4x4 property** in the blackboard, and changing it’s reference to match the one in the script (**_WorldToMainLightMatrix**). We’ll **Multiply** this with a **Vector3** node, and **Subtract** it from the **Position** node set to **World** space, in order to offset that position. The order of multiplication is important here, as it is matrix multiplication!

For now we’ll just set this **Vector3** node to something like **(0, 0, 1)**, which results in pushing the shadow position in the same direction as the light itself. You can compare this to no offset **(0, 0, 0)** to help see the difference. Of course, instead of **1**, we want to use noise.

I’m using two **Simple Noise** nodes in this setup, with different scales so there is more detail to the edges. Also using UVs based on the **World** **Position** (for seamless tiling across the **XZ** plane, see the [Worldspace UVs](https://cyangamedev.wordpress.com/2020/01/28/worldspace-uvs-triplanar-mapping/) post for more info).

![](../../assets/ee5081f2ce09745a.png)

This goes into the **Z** axis of our **Vector3** node that handles offsetting the shadow position. For added effect, we’ll apply this to the **X** axis too. (We could also apply it to the **Y** axis, but this will produce some problems with the flat ground plane and shallow light angles, try it out if you want though). Ideally we should also center the **X** offset, by subtracting a value, in this case around **0.2**. This value depends on the range of the noise so many vary if it’s replaced with a noise texture instead (or if the other values are adjusted).

![](../../assets/69d11ae238f0f1e8.png)

Now that the shadow is noisy, we’ll take the **Shadow Attenuation** output from our **Main Light subgraph**, and use the following setup to get those darker edges on the shadow. This replicates how watercolour paint tends to gather on edges (when a wet brush is used on dry paper at least).

![](../../assets/03e220f59c79d1f6.png)

The **One Minus** inverts the soft shadows so they are white (**1**), rather than black (**0**), and then we reduce that down to grey (**0.5**) as we don’t want the shadows that bright, and use it in the **Lerp** node’s **B** input. We set **A** as **1**, and use **T** as a **Step** on the **Shadow Atten** with a value close to, but not equal to **1**.(e.g. **0.95**). The step basically provides us a harsh transition of white (**1**) where there are shadows. This is used to select a value of **B** where there are shadows, and **A** where there is not, producing :

![](../../assets/a219c19b051c2082.png)

##### Custom Lighting

Next with this shader is introducing the custom shading. For this, we’ll apply a soft diffuse shading effect by taking a **Dot Product** of the **Normal Vector** and **Light Direction**. We **Saturate** the result (aka clamp the value between **0** and **1**) , to remove negative values and **Add** a value of **0.7**, to brighten up the darker side. We then need to **Saturate** again as we don’t want values to be larger than **1**.

![](../../assets/3294379b5f62accc.png)

##### Noise

I’d now like to apply some more noise so it’s not as plain. To achieve a nice effect without seams, I’m using a noise texture in the **Triplanar** node. This samples the texture **3** times and projects it on each axis, blending based on the normals. We take the noise output, **Add** **0.8** and **Saturate** and **Multiply** this with our **Diffuse Shading** result, as well as the **Watercolour Shadows** result.

To help with a more watercolour-like effect, I’m also going to take the **Triplanar** noise result, **Multiply** by a **strength property**, **Subtract** a value (e.g. **0.3**) and use an **Absolute** node. This has the effect of producing dark edges in the noise, which I feel gives a sort of “patchy” watercolour look. (At least it looks better than just applying the regular noise more). This is again multiplied along with the shading x noise x shadows.

![](../../assets/24dbb52171e1fc22.png)

I also have a **Fresnel Effect** multiplied in too, but it’s so subtle that it might as well not be there, and it’s only used for the round objects anyway to make the edges facing away from the camera slightly darker.

More importantly, to apply some colour, I’m using a **Lerp** with the **T** as the result of multiplying all these effects together. **A** is set to the “shadow”/darker colour, while **B** is set to the main colour, but also added with the multiplied result to brighten it up a bit. This could be left out depending on the result wanted though.

![](../../assets/e908127268cbe828.png)

## Image Effect / Blit Shader

For the image effect shader, we need a **Texture2D property** with the reference “**_MainTex**”, as the **Blit** used to apply the shader to the screen will send the source texture into this property, which in this case will be the view of the camera.

![](../../assets/b72b5d6e48b86a04.png)

To handle the blit, I’m using my [Blit Renderer Feature](https://github.com/Cyanilux/URP_BlitRenderFeature), which is added to the **Forward Renderer** used by the Main Camera / URP Asset. The settings are as follows :

![](../../assets/52985cbf7f03f2a8.png)

##### Distortion

We sample the **_MainTex** using a **Sample Texture 2D** node. In order to handle distortion we need to offset the UVs so will put a **Tiling And Offset** node into the **UV** input. I’m using the **Simple Noise** node with a large scale (around **200**). **Subtract** **0.5** in order to center it. **Multiply** by **0.01** so it is not as strong (as offsetting with a value of **0.5** would be half of the entire screen’s size, which is way to strong!), then put it into the **Offset** input.

![](../../assets/5fbbbaaaad35e998.png)

##### Edge Detection / Outlines

To handle the edge detection, I’m using the [Roberts Cross](https://en.wikipedia.org/wiki/Roberts_cross) technique, which involves sampling the **Scene Depth** four times, with an offset in each diagonal direction. We then take the difference of the two opposite depth samples, raise them to a **Power** of 2, **Add** and **Square Root** them. We can then increase the strength through a **Multiply** node with a large value like **100**.

![](../../assets/21855d22b4b30c66.png)

##### White Vignette

For adding white edges to the screen, I’m multiplying our **Distortion** output by **20** to increase the strength a bit again, then putting it into the **Offset** input on another **Tiling And Offset** node. We can then take the **Distance** between that and a **Vector2** of **(0.5, 0.5)** which is the center of the UVs/screen. I’m then remapping this with a **Smoothstep** before adding it with our texture result.

![](../../assets/85046d354480c0a8.png)

After adding we need to **Saturate** the result to remove values above **1**. Then to combine the **Edge Detection**, the output of this goes into the **A** input of a **Lerp** node. **B** is set to a black **Color** node (which is the outline colour, could be converted to a **Color property** instead). The **T** value is the edge detection result, multiplied by **15** to increase the strength further.

![](../../assets/02a24efbbd82cae5.png)

## Watercolour Splodge Decal Shader

I have a few splodges of watercolour paint around the scene, mostly green ones to act as moss. For these I did a similar effect to the shadows, where the edges are more visible than the inner parts. There might be better methods to produce decal effects as it isn’t something I’ve looked into that much, but still might as well share how I handled it.

They are drawn to cubes in the scene, and use the scene depth to project it onto surfaces. The camera cannot go through the cube though, or the effect disappears.

##### Reconstruct World Position from Depth

First up, I reconstruct the world position from the **Scene Depth**. This is something I’ve explained before in other posts (like my [Water Shader Breakdown](https://cyangamedev.wordpress.com/2019/06/10/water-shader-breakdown/) for projecting the caustics, and in the [Fog Shader Breakdown](https://cyangamedev.wordpress.com/2019/12/05/fog-plane-shader-breakdown/)), but in short :

We can use the **Screen Position** node set to **Raw** and take the **W** component to obtain the **view space depth** to the fragment position, or “**fragment depth**” for short. We can then obtain a vector in world space going from that fragment to the camera (**View Direction**), and **Divide** it by this fragment depth. In a way, normalising it, but based on depth rather than it’s true magnitude/distance. (Depth is the distance perpendicular to the camera plane). We can then **Multiply** by the **Scene Depth** to scale the vector and after subtracting it from the **Camera** **Position**, it obtains the world space position we wanted.

(Note, the **View Direction** node is not normalised in URP which is good as that’s what we need. In HDRP it is normalised however, so you’d need to replace it with something else (basically Camera Position – Absolute World Position). I think the Position node set to World space would also work, due to it being camera relative anyway, might need negating though).

![](../../assets/8fef6e8b575d886d.png)

##### offset with noise

After we’ve reconstructed the world position from the depth, we **Transform** it into **Object** space as we want the decal to project based on the object’s transform. We can then sample some noise using this position as UVs. I’m using the setup below for this. Since the position is a **Vector3** but UVs are **Vector2**, this only takes the **RG/XY** components, which acts like projecting the texture through the **Z** axis. Also because it’s in object space we can also rotate the GameObject to change the projection. Usually it’s best to align the **Z** axis with the surface that the decal should be projected onto.

Rather than having the noise scale with the decal, I wanted the noise to stay at a consistent scale in the world which is where multiplying by the **Scale** output from the **Object** node comes in useful. It’s a little hacky here, since I’m only taking the **X** axis into account and ignoring the **Y** – but I quite liked being able to stretch the decal a bit too.

![](../../assets/467f7c1444585d9b.png)

##### Handle Splodge alpha & Colour

After multiplying the noise by **0.5**, this is used to offset/distort our **Projected Decal Position**. We can then take the **Length** to obtain a distance field (**0** at the projected decal position’s origin, and increasing in any direction – But not perfect circles/spheres, since it’s distorted by the noise. We can **Subtract** a value to shift the value to one of those distorted circles. A fairly common way to achieve a nice anti-aliased shape out of a distance field is to use the **DDXY** node (aka **fwidth**) on it, then divide the distance field by the result. This can be used to mask the alpha so we ensure nothing outside of our paint splodge is rendered.

The rest of the graph makes sure that the alpha of the colour is taken into account, and edges are slightly more opaque and darker in colour than the center. Also mixed some of the noise from earlier into the colour for a bit more variation.

This graph is also set to **Transparent** Surface mode, on the small cog on the **Master** node.

![](../../assets/dae3a8b376868371.png)

Thanks for reading! If you have any troubles recreating anything here, you can find the shadergraph files and the scene I put together on [github](https://github.com/Cyanilux/URP_WatercolourShaders).

If you have any comments, questions or suggestions please drop me a tweet [@Cyanilux](https://twitter.com/Cyanilux), and if you enjoyed reading **please consider sharing a link with others**!