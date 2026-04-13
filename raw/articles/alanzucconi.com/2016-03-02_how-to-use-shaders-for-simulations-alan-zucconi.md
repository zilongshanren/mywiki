---
title: How to Use Shaders for Simulations - Alan Zucconi
url: https://www.alanzucconi.com/2016/03/02/shaders-for-simulations/
author: Alan Zucconi
published: '2016-03-02'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This series of tutorials will teach you how use shaders for simulations; in particular how to use them to simulate fluids. This first post will focus on how to continuously process a texture using a shader. This technique is at the heart of most simulations and will be used in this series to implement shaders that simulate smoke and liquids.

![texture6](../../assets/3f63f45da503c812.gif)

[Introduction](https://www.alanzucconi.com#introduction)- Part 1.
[The Code](https://www.alanzucconi.com#part1) - Part 2.
[The Shader](https://www.alanzucconi.com#part2) [Conclusion & download](https://www.alanzucconi.com#conclusion)

A previous post ([Screen Shaders & Image Effects](https://www.alanzucconi.com/2015/07/08/screen-shaders-and-postprocessing-effects-in-unity3d/)) explained how shaders can affect not only objects, but also cameras. Similarly, we will use a shader to process a texture. As far as the GPU is concerned, we’re only manipulating pixels – regardless whether they come from a camera or a 3D model. If you’re familiar with Unity, you might know how the pipeline for post processing works:

![texture1](../../assets/049ba41e716bd25a.png)

The technique shown in this post is substantially different, because the edited texture is fed again to the shader, allowing to be processed continuously:

![texture2](../../assets/5a462e47263fe15f.png)

In the context of traditional materials, this doesn’t really make sense. There are situations, however, in which we want to repeat a certain process. Simulating how smoke diffuse, for instance, requires a constant computation. For this toy example we will create a shader that simply inverts the colours of a texture.

Since this new pipeline is not standard, we will need a script (`ApplyShader`

) that triggers it. To process a texture with a shader, Unity offers the function [Graphics.Blit](http://docs.unity3d.com/ScriptReference/Graphics.Blit.html):

Graphics.Blit(sourceTexture, destinationTexture, material);

The shader needs to be wrapped into a material and the two textures have to be different. If we want to update the original texture, we need to use an additional buffer texture:

public Material material; // Wraps the shader public RenderTexture texture; private RenderTexture buffer; public void UpdateTexture() { Graphics.Blit(texture, buffer, material); Graphics.Blit(buffer, texture); }

The original `texture`

is processed into `buffer`

, which is then copied again into `texture`

. We also need to start the loop somewhere, so is necessary to initialise the with an image for the first iteration:

public Texture initialTexture; void Start () { Graphics.Blit(initialTexture, texture); buffer = new RenderTexture(texture.width, texture.height, texture.depth, texture.format); }

The buffer is allocated with the same properties of the original render texture.

#### Updating periodically

The last step is now to invoke the `UpdateTexture`

function periodically.

private float lastUpdateTime = 0; public float updateInterval = 0.1f; // Seconds public void Update () { if (Time.time > lastUpdateTime + updateInterval) { UpdateTexture(); lastUpdateTime = Time.time; } }

### ⭐ Recommended Unity Assets

All the code written so far requires a shader in order to process pixels. Post processing requires a [vertex and fragment shader](https://www.alanzucconi.com/2015/07/01/vertex-and-fragment-shaders-in-unity3d/) in order to work. For this specific example, we will create one that simply inverts the colour of the image it receives.

float4 frag(v2f_img i) : COLOR { float4 c = tex2D(_MainTex, i.uv); return 1 - c; }

![texture4](../../assets/1ce0bb8216dc03e1.gif)

For the invert shader to work as a post processing effect, is necessary to set the following properties:

ZTest Always Cull Off ZWrite Off Fog { Mode off }

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

To make `ApplyShader`

works, you will need to provide it with the following:

**Initial Texture**: A texture to initialise the process;**Texture**: A render texture, which will be continuously fed to the shader;**Material**: A material that wraps the shader you want to use for the computation;**Update Interval**: how often (in seconds) this scripts will be called.

There is another important part that you must not skip: if you want your rendered texture to be displayed in the game, you need another material to render it, like in the picture below:

![textire3](../../assets/135ec9e0e5db427f.png)

There are many interesting applications of this technique. The next tutorials in this series will explore how the `ApplyShader`

script can be used to simulate water and smoke that are both realistic and interactive. There are other interesting applications, especially when it comes to computations that are highly parallalisable. A future tutorial will explain how to efficiently simulate Conway’s [Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) within a shader.

![texture5](../../assets/78228051d606a65d.gif)

If you want to use shaders to perform computation, you might be better off using [Compute Shaders](http://docs.unity3d.com/Manual/ComputeShaders.html) instead. Unfortunately they are not supported on all platforms, and there’s a general lack of resources on them. Using “traditional” shaders to simulate smoke and water is a little bit of a stretch, but requires little new knowledge and runs on everything that support shaders.

You can download the Unity package for this tutorial [here](https://www.patreon.com/posts/13678657/).

**The next part of this tutorial ( How to Simulate Smoke with Shaders) will focus on how this technique can be used to simulate the diffusion component of particles (such as the ones that compose smoke) into a fluid (like air).**

#### Other resources

- Part 1.
**How to Use Shaders for Simulations** - Part 2.
[How to Simulate Smoke with Shaders](https://www.alanzucconi.com/2016/03/09/simulate-smoke-with-shaders/) - Part 3.
[How to Simulate Cellular Automata with Shaders](https://www.alanzucconi.com/?p=4643)

## Leave a Reply Cancel reply