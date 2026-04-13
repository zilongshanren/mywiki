---
title: Stylized Puff Particles
url: https://www.vertexfragment.com/ramblings/stylized-puff-particles/
author: Steven Sell
published: '2023-06-15'
source_blog: Vertex Fragment
source_site: https://www.vertexfragment.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/b30f02456ffd8de1.gif)


With the recent release of *Tears of the Kingdom* I decided to try my hand at the feature that everyone is going crazy about: the puff particles. Those little swirly clouds that appear when a chopped tree crashes to the ground, or when an object is destroyed.

Oh, am I the only one staring at them? Because they are really quite good.

On the surface its a rather simple effect. It appears to be an alpha dissolve particle with a twist/warp distortion. But as we all know, the devil (and style) is in the details.

![](../../assets/b550a471e39c3e42.png)


For myself the shader code is the easy part, especially with such a simple effect. The difficulty lies in the assets supplied to the material which is why I needed a deeper look into the particle. After spending some time examining individual frame captures I soon decided that what was needed was a glimpse at the actual textures being used.

So after loading up my copy of *Breath of the Wild* and donning [the worlds most powerful pair of glasses](https://renderdoc.org/), I was able to peel back the layers and view the actual particle texture sheet.

In addition to the texture sheet, the shader in *Breath of the Wild* and *Tears of the Kingdom* is also being provided the following textures: color palette, vector flow, and a tileable noise. However I will leave those to your imagination and from here on show only textures of my own making.

![](../../assets/91baa1f0dc1748d8.png)


It’s quite colorful isn’t it?

As you may have guessed its a packed texture with each channel conveying different data. From what I can gather, it is split as follows:

`.r`

is the main lighting/shadowing of the particle.`.g`

is rim lighting.`.b`

is depth, which is used in the dissolve effect.`.a`

is the mask.

As we can’t go around using Nintendo owned textures we first need to get assets of our own to use. If you are artistically inclined you can open up your favorite image editing program and paint your own puffs, filling in the channels as needed.

However, I am not. And if you aren’t as well you can use this ShaderToy that I made for this purpose:

*ShaderToy Warning: Open only on a computer with an actual graphics card unless you want your browser to crash.*

It is a fairly simple, if rather unoptimized, [raymarcher](https://iquilezles.org/articles/raymarchingdf/) and works as follows:

Several layers of [metaballs](https://en.wikipedia.org/wiki/Metaballs) are generated and placed in such a way such that they (attempt to) form a generalized cloud/puff shape. The general logic is similar to any standard successive noise algorithm or [Fractal Brownian Motion](https://thebookofshaders.com/13/) where each layer is smaller than the one before it and is placed so that it is on the outer shell of a previous larger metaball.

After layering enough metaballs ontop of each other you eventually get your puff or floret.

With the general shape in place, the shader renders out to our channels as described above:

`.r`

is a simple near vertical directional light with shadowing. It uses a slight[smoothstep](https://registry.khronos.org/OpenGL-Refpages/gl4/html/smoothstep.xhtml)to soften the edges.`.g`

is another directional light that is shining on the far side of the shape, illuminating only the top edges.`.b`

is the linear depth of the surface.`.a`

is a mask where 1.0 = the raymarch hit the shape and 0.0 = the raymarch missed.

We can now adjust the seed values until we get four puffs that we are happy with (this is the tedious part).

![](../../assets/62a656d76ef5a729.png)


With our particle puff texture sheet we just need our own flow texture. You may already have one, or you can simply copy the one above. However if you are not familiar with flow textures here is a quick rundown.

Flow textures are used to distort the UV that is being sampled. They typically map `.r`

to the `x/u`

axis and `.g`

to the `y/v`

axis. Each pixel represents a normalized 2D directional vector on the range `[0, 1]`

that must be expanded to `[-1, 1]`

.

```
float2 packedFlowDir = SAMPLE_TEXTURE(_FlowTexture, sampler_FlowTexture, uv).rg;
float2 flowDir = (packedFlowDir * 2.0f) - 1.0f;
```


Or if you are feeling particularly angry, `flowDir = mad(packedFlowDir, 2.0f, -1.0f)`

.

There are likely many ways to generate such a flow texture, but to do so via a shader the following code can be used:

```
/**
* Rotates the UV clock-wise around the specified pivot point.
*/
float2 RotateUV(float2 uv, float2 pivot, float rotation)
{
float cosA = cos(rotation);
float sinA = sin(rotation);
float2 origin = uv - pivot; // Move the pivot point back to the origin.
= float2(
((cosA * origin.x) - (sinA * origin.y)), // Rotate at origin.
* origin.y) + (sinA * origin.x)));
return (rotated + pivot); // Move back to original position.
/**
* Gives the 2D directional vector that the specified UV is flowing in.
* Essentially this is the direction that the UV is being translated via the RotateUV function.
*
* Returned vector values are on the range [-1, 1].
*/
float2 GetClockwiseFlowVector(float2 uv)
{
float2 uvPast = RotateUV(uv, float2(0.5f, 0.5f), 0.01667f); // The UV the last frame.
return normalize(uv - uvPast);
}
```


A blur can be applied to the result to make it fuzzier, which is what was done for the image at the top of the section. Any area outside of the flow region should be set to the rather horrible
`rgb(127, 127, 0)`

.

![](../../assets/d880e3e8fcead067.gif)


Now that we have our inputs, we can start diving into the actual puff shader.

The effect is what I refer to as an *Alpha Dissolve*. The pixels do not linearly fade away across the whole image at the same time, but instead remain an uniform alpha value until some threshold is met and they dissolve away. Essentially a pixel alpha value is either `0.0`

or `x`

where `x`

can remain constant or itself fade with time.

On top of this, a warp distortion is applied which increases in strength over time. So as the puff fades and dissolves, it is also twisted which makes it become whispier.

The dissolve is relatively simple: if the inverse value in the `.b`

channel is less than the current lifetime of the particle (on the range `[0, 1]`

), then the alpha is set to 0. Otherwise the alpha is set to our uniform value, which may be constant or fade over the lifetime as well.

This means that the higher the `.b`

value is in the source texture (areas that are more white in the image above), the sooner it dissolves away.

Initially I aimed at using input textures that followed the format used in the Zelda games, plus examining the in-game puffs showed that they dissolve from the inside out. So feel free to flip your `.b`

channel values, but for the purpose of this ramble I am staying with the Zelda conventions.

To calculate the dissolve value:

`float dissolve = step(time01 * _DissolveRate, 1.0f - particleDissolve);`


Where,

`time01`

is a[quadratically eased in value](https://easings.net/#easeInQuad)corresponding to the particle lifetime on the range`[0, 1]`

where 0 is the start, and 1 is the end of the lifetime.`_DissolveRate`

is a modifier where higher the value the quick it dissolves. Though this is typically kept at 1.`particleDissolve`

is our sampled texture`.b`

.

The final alpha value is then calculated using our dissolve:

`float alpha = particleMask * _AlphaConstant * dissolve * (1.0f - time01);`


Where,

`particleMask`

is our sampled texture`.a`

.`_AlphaConstant`

is our uniform alpha value, which I tend to set at`0.8`

.

With our particle dissolving away into nothing we can now add the distortion twist which helps to give the illusion of the puff turning into whisps.

The twist itself is simply a modifier to our UV that is used to sample the particle texture sheet. Let’s start by looking at the shader:

```
float2 toCenter = input.uv - float2(0.5f, 0.5f);
float distToCenter = length(toCenter);
float flowModifier = EaseInCubic(saturate(1.0f - distToCenter));
float2 flowUV = RotateUV(input.uv * _FlowTile, float2(0.5f, 0.5f), _Time.y + rand01);
float2 flowDir = SAMPLE_TEXTURE2D(_FlowTexture, sampler_FlowTexture, flowUV).rg * 2.0f - 1.0f;
float flowStrength = _FlowStrength * time01 * flowModifier * flowModifier;
float2 particleUV = WarpUV(input.uv, input.tex1.xy, flowDir, flowStrength);
float4 particle = SAMPLE_TEXTURE2D(_ParticleTexture, sampler_ParticleTexture, particleUV);
```


The first section calculates the `flowModifier`

which is used to have the distortion at full strength at the center of the puff, but taper off as it gets closer to the edge.

Next we rotate the UV that will be used to sample our flow texture, `flowUV`

. This adds an additional internal spin to the puff which already has an external spin from a particle system. The `flowUV`

is then used to sample our previously created flow vector texture.

`flowStrength`

applies our `flowModifier`

and ramps up over time.

The final section simply samples from our texture sheet using the warped UV. The function `WarpUV`

is used as a helper, as we are selecting a subset from the sheet and can be seen in [the full source code](https://www.vertexfragment.com#source-code).

For ease of reference, the individual components of `particle`

can be broken out:

```
float particleLighting = particle.r;
float particleRimLighting = particle.g;
float particleDissolve = particle.b;
float particleMask = particle.a;
```


![](../../assets/3ca708fa760f2a94.png)


The dissolve and twist make up the majority of the shader, aside from standard Unity-specific boilerplate code.

As a final step it needs to be integrated with a particle system. This of course varies by engine but for Unity we need a couple of properties to be fed into the shader:

- The current lifetime, on the range
`[0, 1]`

. - A random value that is constant for the individual particle.

These can be passed through by enabling the `Custom Vertex Streams`

option on the `Renderer`

module of the particle system and adding `Lifetime → AgePercent`

and `Random → StableRandom.x`

. Once enabled these can be retrieved in the vertex shader using a custom input structure:

```
struct ParticleVertInput
{
float4 position : POSITION;
float3 normal : NORMAL;
float4 color : COLOR;
float4 uvData : TEXCOORD0; // (uv.u, uv.v, age percent [0, 1], random value [0, 1])
```


Age percent becomes our `time01`

in the fragment shader, while the random value is used to select from our texture sheet.

```
float age01 = input.uvData.z;
float rand01 = input.uvData.w;
float spriteU = step(rand01, 0.5f) * 0.5f;
float spriteV = step(Hash11(rand01), 0.5f) * 0.5f;
```


`Hash##`

function.
These are a series of the functions that take in a float or vector and return one or more pseudorandom values. They are a fast and effective way of getting a random value in a shader.

The original source for them (though I make use of several modified variants) can be found here: [https://www.shadertoy.com/view/4djSRW](https://www.shadertoy.com/view/4djSRW)

That wraps up our dive into the Alpha Dissolve particle effect as seen in *Breath of the Wild* and *Tears of the Kingdom* (and likely many other games). Though admittedly this isn’t a perfect recreation of the effect as there are two components that I intentionally skipped over:

**Rim Lighting**

I never ended up using the `.g`

channel of our particle textures. Doubtless it is used in the Zelda titles in some way, but even through observation I can’t see it in use. Even went as far as setting up [SPIR-V Cross](https://github.com/KhronosGroup/SPIRV-Cross) to transpile the RenderDoc decompiled shader to GLSL, which worked but quickly got too tired of trying to piece it all together.

It starts off promising enough, and the sampling and unpacking of the flow vector can be easily recognized:

```
vec2 _317 = texture(textureUnitPS0, R5f.xy).xw;
R11f.x = _317.x;
R11f.w = _317.y;
R123f.x = (R11f.w * 2.0) + (-1.0);
R123f.y = (R11f.x * 2.0) + (-1.0);
```


But then it turns into an endless series of variable swaps which are no fun to read through during my limited free time.

```
...
R127f.w = mul_nonIEEE(param_44, param_45);
backupReg0f = R125f.y;
R11f.x = R8f.x + 0.0;
float param_46 = R1f.z;
float param_47 = R125f.x;
R125f.y = mul_nonIEEE(param_46, param_47);
float param_48 = R1f.y;
float param_49 = backupReg0f;
R127f.z = mul_nonIEEE(param_48, param_49);
R123f.w = (PV1fy * intBitsToFloat(1028443341)) + intBitsToFloat(-1119040307);
R123f.w = clamp(R123f.w, 0.0, 1.0);
...
```


**Noise Texture**

At the start we mentioned the Zelda shader was also being provided a tileable noise texture.

Doubtless this is just used to modulate the particle sampling or coloring, which I personally didn’t feel was necessary to achieve an acceptable result.

![](../../assets/fe5eb4e1b796307e.png)

[https://github.com/ssell/AlphaDissolveParticle](https://github.com/ssell/AlphaDissolveParticle)