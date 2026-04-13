---
title: Snapshot Shaders 2 - Masking Layers
url: https://danielilett.com/snapshot-shaders-2/masking-layers/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

*Snapshot Shaders 2* comes with the ability to mask out every effect in the pack to specific layers based on a highly configurable filter.

You can mask objects based on a local or global mask. Local masks generate a texture for use by one effect only, whereas global masks are available for every effect in a single volume profile. Every effect comes with mask-specific settings, most of which only appear if you have chosen to use a mask.

# Mask Settings

**Mask Mode**- Which type of mask the effect should use. You can choose either*None*,*Global*, or*Local*.**Layer Mask**- Choose which object layers should be detected and drawn to the mask. You can choose any combination of layers, including*Nothing*or*Everything*. Note: you can modify the layer of any object in the top-right of its Inspector window, just above the`Transform`

component.**Rendering Layer Mask**- Similar to the*Layer Mask*, but using Rendering Layers instead. Note: you can modify an object’s Rendering Layer by accessing its`Renderer`

component and finding this parameter near the bottom of its section in the Inspector.**Light Modes**- Choose which kind of objects to include in the mask texture, based on the sort of material being used to render it. You may add several Light Modes to the list. The most common settings you will use are*UniversalForward (Lit)*and*SRPDefaultUnlit (Unlit)*, but you can use the following:*UniversalForward (Lit)*- This tag is used by shaders which support lighting.*UniversalForwardOnly (some custom shaders)*- This tag is used by shaders which need to use Forward rendering, even if the Deferred rendering path is active.*SRPDefaultUnlit (Unlit)*- This tag is used by shader passes that don’t specify any tag. It is commonly used to render objects which don’t need to use lighting.*UniversalGBuffer*- This tag is used by shaders which are compatible with Deferred rendering.*Universal2D*- This tag is used by shaders which use the 2D Renderer.*ShadowCaster*- This tag is used by shaders which support casting shadows.*DepthOnly*- This tag is used by shaders which support rendering depth information into the depth texture.*DepthNormals*- This tag is used by shaders which support rendering normals information into the normal texture.*DepthNormalsOnly*- Similar to UniversalForwardOnly, this pass renders normals information into the normal texture using Forward rendering, even if the Deferred rendering path is active.*Meta*- This tag is used by the lightmap baking pass. Important: it is stripped from shaders when you build the game.

**Render Queue**- Choose whether to include*Opaque*,*Transparent*, or*All*objects in the mask texture.**Draw Skybox To Mask**- Choose whether to include the skybox in the mask texture (unless an opaque object has been drawn in front of it).**Invert Mask**- Should the effect invert the contents of the mask texture (black becomes white, and vice versa)?

# Local Masks

Using a local mask is as easy as choosing *Local* mode in the **Mask Mode** and picking whichever settings you want. This mask will apply only to the effect which sets it.

# Global Masks

Using a global mask requires you to add a volume component called `Global Mask`

to your volume profile using the Add Override button on the profile. The *Render Pass Event* of the `Global Mask`

must be before or the same as any effect that wishes to use it. Then, you need to select *Global* mode in the **Mask Mode** for each effect which needs to use it. This is more efficient than using individual local masks with the same settings, as you only need to generate one mask texture which can be shared between effects, but you may only use one Global Mask on each volume profile.