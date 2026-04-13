---
title: Orthographic Depth
url: https://cyangamedev.wordpress.com/2020/03/05/orthographic-depth/
author: Cyan
published: '2020-03-05'
source_blog: Cyan
source_site: https://cyangamedev.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Note : Info in this post still applies but may be a little outdated as the Scene Color node has been updated in newer versions of Shader Graph. Please also see : [https://www.cyanilux.com/tutorials/depth/#orthographic-scene-depth](https://www.cyanilux.com/tutorials/depth/#orthographic-scene-depth)

Hey! I use the **depth texture/buffer** (**Scene Depth** node) in quite a few of my shader breakdowns, but the graphs given only work with a camera with a **Perspective** projection, meaning objects further away from the camera are smaller on the screen, which gives a 3D effect.

A camera can also have an **Orthographic** projection, where regardless of how far away objects are from the camera, the size on the screen remains the same. This is more useful for 2D games (e.g. sidescrollers, top-down or isometric-style games).

![](../../assets/f0fff0bc97323994.png)

The scene is showing a cube structure with a hole in the middle. Each side of the cube has a width of 1 unit and length (and height) of 5 units.

For a while I’ve had a [small twitter thread](https://twitter.com/Cyanilux/status/1169932943869059073) about using the depth buffer for an Orthographic camera projection, but wanted to turn it into a proper blog post as well as make the graphs support different platforms (Direct3D-like and OpenGL-like, as listed in the [Platform Differences](https://docs.unity3d.com/Manual/SL-PlatformDifferences.html) docs page).

##### Perspective

In a **Perspective** camera projection, sampling the depth texture (**Scene Depth** set to **Raw** mode) returns a value from **0 to 1** which encodes the depth from the **near **to **far** camera clipping planes (or vice versa if the platform uses a **reversed** **depth** buffer – which can help with precision). The value is also **non-linear** though – which means a value of **0.5** won’t be halfway between the two clipping planes, (again this is to help with precision).

For most effects, we want to convert this value into a linear01 or linear-eye value, which is done using the **Linear01Depth** & **LinearEyeDepth** functions (or **Scene Depth** set to **Linear01** or **Eye** modes). I believe these functions/modes handle platform differences (the reversed depth buffer) for us, so their outputs should be the same across any platform.

If you want more information on the Perspective Depth Buffer, see the depth part of the [Scene Color & Depth nodes](https://cyangamedev.wordpress.com/2019/06/01/scene-color-depth-nodes/) post, It’ll break down the different modes on the node a little bit more, and show the code for the Linear01Depth and LinearEyeDepth functions.

##### Orthographic

However, in a **Orthographic** projection, sampling the depth texture (**Scene Depth** set to **Raw** mode) **already returns a linear 0 to 1 value**. We don’t want to convert it so **must use the Raw mode**!

However, as mentioned before, the depth buffer could also be **reversed** depending on the target platform so we need to take that into account before using the value. This is done by using the **Z Buffer Sign** output from the **Camera** node (aka _ProjectionParams.x), which returns **-1** if the depth is reversed, and **1** if it is not. We can compare this in a **Branch** and if reversed, we want to use the **One Minus** node on the depth output like so :

![](../../assets/342f5895b2529cd2.png)

This output is now between **0** and **1**, reaching from the **near** to the **far** clip planes, regardless of the target platform.

For most effects we also likely need to **Lerp** it with the **near** and **far** clip planes to have the depth in terms of **View space units** (This should be similar to the result given by the LinearEyeDepth / Eye mode output for a Perspective projection. The Viewspace is also called camera/eye space, which is basically just a rotated/offset version of world space so the camera is at the origin looking down the negative z axis. The unit scale is the same as the units you use to position GameObjects in the inspector).

In various shader breakdowns I’ve used the “*Depth Difference*” and “*Reconstructing World Position from Depth*” techniques – both shown in the [Fog Plane Shader Breakdown](https://cyangamedev.wordpress.com/2019/12/05/fog-plane-shader-breakdown/). Below I’ve listed the **Orthographic** equivalent of these techniques, again taking into account any platform differences so they will work on both Direct3D-like and OpenGL-like platforms. Note that depending on the platform (e.g. mobile) you may get precision issues if the far clipping plane is too far away (which may cause visible banding in the depth result).

### Depth Difference

![](../../assets/df10c5c9009ca31d.png)

This technique uses the **difference in the two depth values** (in view/eye space) to obtain a gradient where objects in the scene intersect with the object with the shader (in this case a plane/surface).

In perspective we use the raw Screen Position **alpha**(/w) component, which is produced by the projection matrix. It’s used for converting to normalised device coordinates (NDC), where between a vertex and fragment shader it divides the clip space coordinate by this alpha (/w) component (known as the *perspective divide*), but it also happens to be the viewspace depth to the fragment. However in an orthographic projection, this value is just **1**, which means the clip space is already normalised. In this case we need to use the **B/Z** value to obtain the depth (between **-1** and **1**, or **1** and **0** depending on platform). (I’ve summarised this quite a bit based on knowledge I’ve picked up. If you want to read up more on the different coordinate spaces [this article](http://www.codinglabs.net/article_world_view_projection_matrix.aspx) is quite informative).

The graph below shows how this would work with an **Orthographic** projection, taking into account platform differences (like the reversed depth buffer and some clip space differences).

Note that the **Master** node is also set to **Transparent** so it doesn’t write it’s own depth to the depth buffer.

The **Custom Function** node uses a String type with the Body as follows :

Out = float2(

UNITY_NEAR_CLIP_VALUE,

UNITY_RAW_FAR_CLIP_VALUE

);

The name of the function isn’t important, but I have it set to *GetClipValues*. There are no Inputs, but one Output (**Out**, set to **Vector2**). The purpose of this function is to obtain the near and clip plane “**values” **(not like the **Camera** node outputs which are the actual clip plane *distances* though). We use these values to remap the clip space z/depth range into a **0** to **1** range.

For Direct3D-like platforms (Direct3D, Metal and consoles) this is :

NEAR = **1**, FAR = **0**

For OpenGL-like platforms (OpenGL and OpenGL ES2/3) this is :

NEAR = **-1**, FAR = **1**

### Reconstructing World Position from Depth

![](../../assets/5d4ede84724af9bb.png)

Being able to obtain a world space position from the Scene Depth is quite useful, (though obtaining it for an orthographic projection is more complicated than it’s perspective counterpart). I’ve used something similar for a perspective projection in the [Water Shader Breakdown](https://cyangamedev.wordpress.com/2019/06/10/water-shader-breakdown/) for the caustics effect, as well as in the fog one that I also mentioned before.

The graph below shows how this would work with an **Orthographic** projection, taking into account platform differences (the reversed depth buffer).

Note that the **Master** node is also set to **Transparent** so it doesn’t write it’s own depth to the depth buffer.