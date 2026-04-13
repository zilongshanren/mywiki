---
title: Toon Shaders Pro for URP - Outline (Post Process)
url: https://danielilett.com/toon-shaders-pro/outline-post-process/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

The **Outline** post processing effect is a versatile shader which can use multiple algorithms to draw outlines. From the object-mask style which can draw outlines around specific Unity layers, to depth-normals outlines which use existing post processing textures to draw outlines, you should find an outline style which works for you.

![Outlines](../../assets/dd6f7921aca3a6ab.png)


# Parameters

Note that some of these options are only visible when specific other settings are enabled.

## Rendering Options

**Render Pass Event**- Choose whether to render the outlines before or after URP’s internal post processing effects. That includes effects such as color correction and bloom.**Outline Type**- Choose which outline algorithm to use. There are six choices:**No Outlines**- Don’t render any outlines.**Depth Normal Outlines**- Detect small gradients in the color, depth, and normal vector information across each pixel to find edges.**High Quality Masked Object Outlines**- Render specific object layers to a separate mask texture and find edges in that mask, allowing for varying thickness and a greater level of customization than other algorithms.**Pixel Width Masked Object Outlines**- Use the same object mask as above, but use a cheaper algorithm for pixel-width outlines.**Hull Outlines**- Render each mesh a second time while inverting and inflating the mesh hull.**Debug Outline Mask**- Render only the object mask used for the mask-based effects to the screen. Helpful for finding objects which may have been incorrectly assigned to the wrong layer.


## Outline Options

**Outline Color**- Color applied to the outlines. Some effects may use the transparency value.

## Depth-Normals Options

**Color Sensitivity**- Color gradients greater than this threshold will be detected as edges.**Color Strength**- How strongly a detected color-edge should contribute to the final edge-detection value.**Depth Sensitivity**- Depth gradients greater than this threshold will be detected as edges.**Depth Strength**- How strongly a detected depth-edge should contribute to the final edge-detection value.**Normal Sensitivity**- Normal vector gradients greater than this threshold will be detected as edges.**Normal Strength**- How strongly a detected normal-edge should contribute to the final edge-detection value.**Depth Threshold**- Pixels with a depth higher than this threshold are never detected as edges.

## Object Mask Options

**Object Mask**- Set a layer mask to determine which object layers get rendered into the mask texture.**Mask Ignore Depth**- If enabled, objects get rendered into the mask texture without checking for depth. If rendering many objects, this likely means objects will be rendered out of order. Useful if you render only one object and you want it to be seen through walls.**Mask Drawing Mode**- Choose whether to render outlines along the outer edge of each mesh, along the edge of each triangle, or around the collective area of objects drawn into the mesh. You can also use the borders between different mesh vertex colors.**Light Modes**- Determines which objects get drawn into the mask, based on which shader they are using originally. The tooltip provides useful context for this setting.**Render Queue**- Choose whether to render only opaques, only transparents, or all objects into the mask. However, only opaque objects are properly supported.

## Mask Outline Options

**Masked Outline Thickness**- Set the thickness of the outlines. Larger values get more expensive, so try to keep this as low as possible.**Masked Outline Smoothing**- Decreases the outline contribution of further away pixels for a false smoothing effect.**Outline Draw Sides**- Choose to draw objects ‘inside’ the mask, ‘outside’ it, or on both ‘sides’. Drawing on both sides results in a thicker outline.**Outline Fade Start**- Start to fade out the outlines when the object is this many Unity units from the camera.**Outline Fade End**- When the object is at this distance from the camera, the objects become totally invisible.

## Normals Options

**Use Depth Normals**- When using mask-based outlines, choose whether to layer normal-based edge detection for details ‘inside’ the mask.

## Hull Outline Options

**Outline Thickness**- How far the outlines extend away from the object.**Outline Transparency**- Choose whether to render the outlines with transparency. Since this method uses actual mesh geometry, this has an impact on rendering order.**Outline Lighting**- Should the outlines use simple diffuse lighting based only on the main directional light?**Flip Outline Direction**- When lighting is being used, should the direction of the normal vector be inverted?**Outline Min Lighting**- Set a minimum lighting value to use for the diffuse outline lighting.

# Usage Tips

- Rendering outlines
*before*other post processing effects means that they are subject to those effects. For example, color correction and bloom effects will apply. This may result in a soft, stylized look for your outlines. Otherwise, if you want the outlines to use exactly the color you specify, you should render them*after*. - For the
**Light Mode**setting, Unity restricts the choice of objects to only those objects which use a shader with a light mode in this list. Most lit shaders use*UniversalForward*. Most unlit shaders don’t use a tag, which defaults to*SRPDefautlUnlit*. The toon shader in this pack uses*UniversalForwardOnly*. Shaders which support deferred rendering use*UniversalGBuffer*. - You can use vertex colors to render mask values for some of these effects. I have included a script in
*Demo/Scripts*called**VertexColorRandom**which lets you set random colors on a mesh or its individual triangles – make sure the mesh has*Read/Write*enabled to do this.