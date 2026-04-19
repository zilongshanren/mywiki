---
title: Fast Divergence-Free Noise Generation in Shaders
url: https://atyuwen.github.io/posts/bitangent-noise/
published: '2021-05-17'
source_blog: C++ Minor
source_site: https://atyuwen.github.io/
category: graphics
fetched: '2026-04-19'
---

This article describes a method called “Bitangent Noise” which can generate divergence-free noise efficiently. The [implementation](https://github.com/atyuwen/bitangent_noise/) is a single shader without any other dependencies, and both HLSL and GLSL codes are provided for your convenience. The following image ([video](https://youtu.be/KbdQgGWJ_tA)) shows a particle system that is updated using bitangent noise, and here is a [shadertoy example](https://www.shadertoy.com/view/ftl3zN) shows how to use bitangent noise to make a smoke ball.

Divergence-free noise is an ingenious technique that is extremely suitable for driving particles to move like real fluid motion. The most widely used divergence-free noise generator is called **Curl Noise** 1, I first knew it from smash’s great article

about the making of the

[2](https://atyuwen.github.io#fn:2)[blunderbuss](https://www.youtube.com/watch?v=VCpYH8yDK8g)demo, in which the fluid effect impressed me deeply. Later I also tried to reproduce that effect

[(github project)](https://github.com/atyuwen/efflux), though the result is not as good as smash’s masterpiece.

If you don’t know the curl noise, its core idea is based on this identity: $\nabla \cdot \nabla \times \equiv 0$, i.e. **the divergence of a curl is zero**. So to get a divergence-free vector field, you can firstly generate 3 random scaler fields, then calculate the gradient of each, and finally compute the curl from those gradients, now the result is divergence-free by construction.

While mathematically simple and elegant, curl noise is not very cheap to generate. In practice we usually need 4d noise (3d position + time), which makes things worse, because the higher the dimension, the more expensive to calculate. One day when I was looking over some vector calculus materials and expecting some clues to optimize my noise generator, I occasionally found some identities that are particularly interesting:

$$ \nabla \cdot (A \times B) = B \cdot (\nabla \times A) - A \cdot (\nabla \times B) $$

$$ \nabla \times (\nabla \phi) = 0 $$

From above two equations we have:

$$ \nabla \cdot (\nabla \phi \times \nabla \psi) = 0 $$

That means **the divergence of the cross product of two gradient fields is always zero**. Now we have another method to generate divergence-free noise:

- Generate a random scaler field $\phi$ and calculate its gradient $G$.
- Generate a random scaler field $\psi$ and calculate its gradient $F$.
- return the cross product $G \times F$.

Compare to curl noise which needs 3 gradients, this method is computationally cheaper because it only needs calculating 2 gradients. At first I thought this method was new and named it **Bitangent Noise**, since it’s tangent to both the level surface of field $\phi$ and field $\psi$. But later I found it was already invented by Ivan DeWolf in 2005 3. (I’m wondering why it is so less popular than curl noise.) Since Ivan DeWolf didn’t give it a name, I’ll stick to this punny name “Bi-tangent Noise”.

Okay, now we have bitangent noise to replace curl noise, the remaining task is to implement it efficiently. Since we really don’t want to introduce any external dependencies (e.g. LUT Textures), Ian McEwan & stegu’s pure ALU-based simplex noise [implementation](https://github.com/stegu/webgl-noise/) 4 seems to be a good start. Using simplex noise with analytic derivatives, we can implement bitangent noise straightforwardly like following:

```
float3 BitangentNoise3D(float3 p)
{
float3 dA = SimplexNoise3DGrad(p);
float3 dB = SimplexNoise3DGrad(p + float3(31.416, -47.853, 12.679));
return cross(dA, dB);
}
float3 BitangentNoise4D(float4 p)
{
float3 dA = SimplexNoise4DGrad(p).xyz;
float3 dB = SimplexNoise4DGrad(p + float4(31.416, -47.853, 12.679, 113.408)).xyz;
return cross(dA, dB);
}
```


From above code we can see clearly the cost of bitangent noise is basically twice the cost of simplex noise. For 4d case, there are some trickeries ([e](https://github.com/atyuwen/bitangent_noise/blob/main/Develop/BitangentNoise_ref.hlsl#L233).[g](https://github.com/atyuwen/bitangent_noise/blob/main/Develop/BitangentNoise_ref.hlsl#L239).) to optimize it further, but they all have the drawback of losing some randomness. Can we do it better without sacrificing quality?

Notice that to get 2 gradients, we simply called `SimplexNoiseNDGrad`

twice with different inputs, which prevent sharing of all the intermediate results which are highly dependent on the inputs. What if we just use one `SimplexNoiseNDGrad`

routine and compute 2 gradients simultaneously? And indeed we can do that by providing two different sets of gradients attached to simplex corners. Here comes the last problem: how to pick two random gradients for each simplex corner? Fortunately we have PCGs (Permuted Congruential Generators) [5](https://atyuwen.github.io#fn:5) 6:

```
// Permuted congruential generator (only top 16 bits are well shuffled).
uint2 pcg3d16(uint3 p)
{
uint3 v = p * 1664525u + 1013904223u;
v.x += v.y*v.z; v.y += v.z*v.x; v.z += v.x*v.y;
v.x += v.y*v.z; v.y += v.z*v.x;
return v.xy;
}
uint2 pcg4d16(uint4 p)
{
uint4 v = p * 1664525u + 1013904223u;
v.x += v.y*v.w; v.y += v.z*v.x; v.z += v.x*v.y; v.w += v.y*v.z;
v.x += v.y*v.w; v.y += v.z*v.x;
return v.xy;
}
```


Using PCG we can generate 2 independent random values from the skewed coordinate of each simplex corner, then we can easily pick two random gradients according to these 2 hash values. By feeding those gradients to the standard simplex noise procedure we can generate 2 noise derivatives at one time with very few extra computations, which makes our bitangent noise generator just **a little more expensive** than simplex noise (about 30%, see the performance data below).

These performance data are measured on a Nvidia GTX 1060 card, where each noise function is executed 1280 * 720 * 10 times.

| Noise Function | Cost | Desc |
|---|---|---|
| snoise3d | 1530 μs |
|

**SimplexNoise3D****1153 μs**[optimized 3d simplex noise](https://github.com/atyuwen/bitangent_noise/blob/main/Develop/SimplexNoise.hlsl#L41)[stegu’s 4d simplex nosie](https://github.com/stegu/webgl-noise/blob/master/src/noise4D.glsl)**SimplexNoise4D****1798 μs**[optimized 4d simplex noise](https://github.com/atyuwen/bitangent_noise/blob/main/Develop/SimplexNoise.hlsl#L84)[3d bitangent noise, reference version](https://github.com/atyuwen/bitangent_noise/blob/main/Develop/BitangentNoise_ref.hlsl#L219)**BitangentNoise3D****1534 μs**[optimized 3d bitangent noise](https://github.com/atyuwen/bitangent_noise/blob/main/BitangentNoise.hlsl#L41)[4d bitangent noise, reference version](https://github.com/atyuwen/bitangent_noise/blob/main/Develop/BitangentNoise_ref.hlsl#L227)[4d bitangent noise, low quality](https://github.com/atyuwen/bitangent_noise/blob/main/Develop/BitangentNoise_ref.hlsl#L239)**BitangentNoise4D****2413 μs**[optimized 4d bitangent noise](https://github.com/atyuwen/bitangent_noise/blob/main/BitangentNoise.hlsl#L97)-
Bridson, R., Hourihan, J., Nordenstam, M. 2007. “Curl-Noise for Procedural Fluid Flow”. ACM Trans. Graph. 26, 3, Article 46 (July 2007),

[↩︎](https://atyuwen.github.io#fnref:1) -
Matt “Smash” Swoboda, “A thoroughly modern particle system”.

[https://directtovideo.wordpress.com/2009/10/06/a-thoroughly-modern-particle-system/](https://directtovideo.wordpress.com/2009/10/06/a-thoroughly-modern-particle-system/)[↩︎](https://atyuwen.github.io#fnref:2) -
Ivan DeWolf, “Divergence-Free Noise”.

[https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.93.7627&rep=rep1&type=pdf](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.93.7627&rep=rep1&type=pdf)[↩︎](https://atyuwen.github.io#fnref:3) -
McEwan, Ian, David Sheets, Mark Richardson, and Stefan Gustavson. “Efficient computational noise in GLSL.” Journal of Graphics Tools 16, no. 2 (2012): 85-94.

[↩︎](https://atyuwen.github.io#fnref:4) -
Mark Jarzynski and Marc Olano, “Hash Functions for GPU Rendering”, Journal of Computer Graphics Techniques (JCGT), vol. 9, no. 3, 21-38, 2020

[↩︎](https://atyuwen.github.io#fnref:5) -
Epic Games, UnrealEngine/Random.ush.

[https://github.com/EpicGames/UnrealEngine](https://github.com/EpicGames/UnrealEngine)[↩︎](https://atyuwen.github.io#fnref:6)