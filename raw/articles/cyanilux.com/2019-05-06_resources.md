---
title: Resources
url: https://www.cyanilux.com/resources/
published: '2019-05-06'
source_blog: Cyanilux Shader Tutorials
source_site: https://www.cyanilux.com/
category: graphics
fetched: '2026-04-19'
---

# Resources

The list below links resources mostly related to **Shaders** and **Unity** (various pipelines), including both external & most of my tutorials (the ones with images). Some entries may be for other engines or graph editors but the general idea/method could still be useful, especially if graph/node-based as those tend to have the same nodes just named differently.

- The list is loaded from a
[Github gist](https://gist.github.com/Cyanilux/69e4f228206b1a70c3f8a0ab4f22ef75)(so I don’t have to update the entire site to add entries). If it fails to load for some reason can optionally view that instead. - Entries are grouped under various headings. You can also use the filter below to locate things easier.

## Filter Usage

- The filter below searches for the
**exact string/keyword**(not case sensitive) anywhere in text (including tags at side), so I’d recommend sticking to a single short keyword, like “water” - If you want to use multiple keywords, separate each with
`","`

or`"&"`

(for AND),`"|"`

(for OR), and use`"("`

and`")"`

for grouping.- Example :
`"(BiRP | URP) & HLSL"`

. - AND takes precedence, so
`"a | b & c | d"`

is the same as`"a | (b & c) | d"`


- Example :

If you have suggestions of links to add, please put them in the `#resources`

section of my discord (linked in top right of page)

![](../../assets/aeba32116a601e1e.png)

A post showing how Shader Graph can be used with DrawMeshInstancedProcedural / RenderMeshPrimitives and DrawMeshInstancedIndirect / RenderMeshIndirect to draw grass using GPU Instancing.

(Cyanilux)

![](../../assets/07a6b2da673accd5.png)

![](../../assets/4a9b8575c831d9b0.png)

![](../../assets/c6ca1b2a72fe1818.png)

![](../../assets/efca738c460c861d.png)

Examples for revealing invisible objects (especially decals, such as fingerprints or hidden messages) based on lights, stencils and other masking methods

(Cyanilux)

![](../../assets/956d9974394b2dfb.png)

![](../../assets/c01e6b59a6a28469.png)

![](../../assets/3e47f2538e774ae7.png)

![](../../assets/2ec3026917f2566e.png)

![](../../assets/fe666b746ed81055.png)

![](../../assets/af45cd8ad828c52b.png)

![](../../assets/62a97b0969b10a36.png)

![](../../assets/d7f65c9ef4b1d3a4.png)

![](../../assets/e8ba200e0c2077d8.png)

![](../../assets/4f3131c8b96ca1dd.png)

Soft shaded foliage shader that uses alpha clipping with foliage texture and a small amount of vertex displacement to simulate wind. Applied to a mesh consisting of intersecting quads generated from a particle system

(Cyanilux)

![](../../assets/6164779914aee7ae.png)

![](../../assets/5046e53c91ac6389.png)

![](../../assets/8a6d7ece084ce6bb.png)

A shader which uses a signed distance field stored in the sprite texture's alpha channel to create an outline/glow (and inner-glow) effect, with control over the colour and thickness

(Cyanilux)

![](../../assets/85c4206d4e62efeb.png)

![](../../assets/ddc063ea6e546d99.png)

A shader which uses noise and step functions to discard pixels to create a dissolving effect. Also provides examples for dissolving based on height / Y and using view space position as UVs to avoid seams

(Cyanilux)

![](../../assets/948c4afc74c7b2ff.png)

A shader which produces solid diagonal lines across a quad's surface that moves with the camera position to simulate toon-like glass reflections

(Cyanilux)

![](../../assets/36bef0f8c23e8f60.png)

Examples of fog plane effects produced using the depth texture (scene depth), commonly used to create vertical fog or fake darkness/light for entrances and exits in third person games.

(Cyanilux)

![](../../assets/1d83e3597042e7b0.png)

A shader applied to a flat subdivided plane where vertices are offset vertically based on layered noise, moving at different rates, to create a cloud effect. Also uses scene depth to produce a softer transition with intersecting game objects

(Cyanilux)

![](../../assets/2609c248a85c3db0.png)

![](../../assets/a01a46db2cac3adc.png)

A simple version of a forcefield shader, using fresnel effect for glowing edges and scene depth for intersections with objects in the scene

(Cyanilux)

![](../../assets/e4210eae3dfdfee3.png)

![](../../assets/7283344233b80c52.png)

A water shader that uses the scene color to produce distortion/refractions and reconstructs a position from the scene depth to project caustics on underwater objects

(Cyanilux)

![](../../assets/7c2d33dc23784aed.png)

![](../../assets/2ee2713e57e93f38.png)

A hologram shader based on sine/fraction nodes to produce repeating horizontal lines and fresnel effect, with optional distortion and glitching effects

(Cyanilux)

![](../../assets/38b68ff3837eb83d.png)

![](../../assets/e6b7bb557b544aa8.png)

![](../../assets/d60486abec035bdd.png)

A small post explaining how to convert the UVs of a sprite sheet (or sprites packed in an atlas) into local 0-1 coordinates across each sprite in the shader

(Cyanilux)

![](../../assets/d57c1ed86b5681ee.png)

Goes through examples of Renderer Features and explains how to write Custom Renderer Features and Scriptable Render Passes for Universal RP. Mostly focuses on Unity 2022, but now also provides some snippets for newer versions!

(Cyanilux)

![](../../assets/abb23ea9ed6c0d90.png)

![](../../assets/236f6765ef1886bc.png)

![](../../assets/580c070d0643c8a8.png)

![](../../assets/141a98d800411c6b.png)

An introduction to what a Mesh, Shader and Material is in Unity, how to set Shader Properties from C#, various types of Batching, and a brief look at Forward, Forward+ and Deferred rendering paths

(Cyanilux)

![](../../assets/3dfad1285d245ff1.png)

![](../../assets/a9dd1807cdd1a642.png)

A post explaining how to move vertices in Shader Graph, providing examples such as swaying grass and animated fish and butterflies. Also includes info about recalculating normal vectors.

(Cyanilux)


( No results sorry, Try a different filter!~ )