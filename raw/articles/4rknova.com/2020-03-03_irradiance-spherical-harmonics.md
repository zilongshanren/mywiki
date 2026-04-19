---
title: Irradiance, Spherical Harmonics
url: https://www.4rknova.com/blog/2020/03/03/spherical-harmonics
author: Nikolaos Papadopoulos
published: '2020-03-03'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

# Introduction

Spherical Harmonics (SH) are a type of Spherical Radial Basis Function (SRBF) that can be used to encode signals defined on a sphere in a compact way. This makes them an excellent fit for encoding a variety of datasets commonly used in real time graphics. One such dataset is irradiance maps.

Spherical Harmonics are distributed across an infinite series of 0-indexed bands, with each band n adding 2*n+1 coefficients to the set. Higher bands add more granularity by encoding progressively higher frequencies, but also increasing the computational cost of reconstructing the signal.

# Convolution

The process of encoding a spherical signal using Spherical Harmonics is called projection.

In a conventional rendering pipeline, incoming radiance is stored in a cubemap which is then used to generate the respective irradiance map. Incoming radiance is convolved with a cosine lobe oriented about the surface normal. This is a relatively slow process that requires iterating through all pixels, multiple times. Due to run-time constraints for real time applications, irradiance is typically pre-calculated and stored in a separate cubemap. That cubemap is then sampled at runtime to determine the respective irradiance value for a given direction. The downside of this approach is that it has a significant impact on storage and bandwidth requirements.

Alternatively, incoming radiance can be projected to Spherical harmonics, reducing the larger cubemap dataset to 4 or 9 coefficients per color channel. The cosine lobe is also represented in SH [02], simplifying the convolution process which becomes a simple dot product of the two sets of SH coefficients.

Taking advantage of rotational symmetry, a cosine lobe oriented about the Z axis, can also be encoded using Zonal Harmonics, producing a small set of constant coefficients. This representation is rotated and aligned with the normal direction before calculating the dot product of the two coefficient sets.

The following code sample from [Matt Pettineo](https://twitter.com/mynameismjp?lang=en) implements this process [09].

```
static const float PI = 3.141592654f;
/* Zonal Harmonics coefficients for cosine Lobe */
static const float CosineA0 = Pi;
static const float CosineA1 = (2.0f * Pi) / 3.0f;
static const float CosineA2 = Pi * 0.25f;
struct SH9 { float c[9]; };
struct SH9Color { float3 c[9]; };
// Compute the cosine lobe in SH, oriented about the normal direction
SH9 SHCosineLobe(in float3 dir)
{
SH9 sh;
sh.c[0] = CosineA0 * 0.282095f; /* Band 0 */
sh.c[1] = CosineA1 * 0.488603f * dir.y; /* Band 1 */
sh.c[2] = CosineA1 * 0.488603f * dir.z;
sh.c[3] = CosineA1 * 0.488603f * dir.x;
sh.c[4] = CosineA2 * 1.092548f * dir.x * dir.y; /* Band 2 */
sh.c[5] = CosineA2 * 1.092548f * dir.y * dir.z;
sh.c[6] = CosineA2 * 0.315392f * (3.0f * dir.z * dir.z - 1.0f);
sh.c[7] = CosineA2 * 1.092548f * dir.x * dir.z;
sh.c[8] = CosineA2 * 0.546274f * (dir.x * dir.x - dir.y * dir.y);
return sh;
}
/* Convolution */
float3 SHIrradiance(in float3 normal, in SH9Color radiance)
{
SH9 shCosine = SHCosineLobe(normal);
/* Compute the SH dot product to get irradiance */
float3 irradiance = 0.0f;
for (uint i = 0; i < 9; ++i) {
irradiance += radiance.c[i] * shCosine.c[i];
}
return irradiance;
}
/* Lambertian BRDF */
float3 SHDiffuse(in float3 normal, in SH9Color radiance
, in float3 albedo)
{
return SHIrradiance(normal, radiance) * albedo * (1.0f / PI);
}
```


This code assumes that the initial radiance cubemap is already projected to Spherical Harmonics and the coefficient values are available.

# Cubemap Projection to SH Basis

Computing the convolution at run time using Spherical Harmonics is relatively cheap. However, for embedded devices with limited resources where every single cycle counts, the convolution can be computed offline by using cubemaps and importance sampling. The produced irradiance map can then be projected to Spherical Harmonics. This greatly reduces the number of ALU operations required to reconstruct the signal at run-time.

In either of these methods, the projection of the cubemap to Spherical Harmonics is a relatively simple process.

Each cubemap sample has a color value and a direction. To project the cubemap into SH, the SH basis functions are evaluated in the direction of each texel’s center, and then weighted by the differential solid angle for that texel. The following pseudocode from Peter-Pike Sloan’s “Stupid Spherical Harmonics (SH) Tricks” [03] describes the process.

```
float f[]; // The final SH coefficient values
float s[]; // SH basis
float fWtSum=0; // Sum of weights
Foreach(cube map face)
Foreach(texel)
float fTmp = 1 + u^2+v^2;
float fWt = 4/(sqrt(fTmp)*fTmp);
EvalSHBasis(texel,s);
f += t(texel)*fWt*s; // vector
fWtSum += fWt;
f *= 4*PI/fWtSum; // area of sphere
```


| Symbol | Description |
|---|---|
| u, v | The two coordinates on the given face that are not +/- 1 |
| (ie: on the +X face, it would be y/z, etc.) | |
| t(texel) | The texel color value. |
| EvalSHBasis(texel,s) | Normalizes the input coordinate (on a cube face), and |
| evaluates the SH basis functions in that direction. |

The last normalization would typically not be required, since the normalized sum of the differential solid angles is equal to \(4 * \pi\). Note that the calculation is likely to suffer from varying degrees of error depending on the resolution of the cubemap [03].

A more precise calculation of the per texel solid angle is described in the following code sample. The code snippet is found in AMD’s cubemapgen source code [15] and its mathematical background is explained in detail in a relevant blog post by Rory Driscoll

.

[[07]](https://www.4rknova.com#REF-07)```
static float32 AreaElement( float32 x, float32 y )
{
return atan2(x * y, sqrt(x * x + y * y + 1));
}
float32 TexelCoordSolidAngle(int32 a_FaceIdx, float32 a_U
, float32 a_V, int32 a_Size)
{
// scale up to [-1, 1] range (inclusive)
// offset by 0.5 to point to texel center
float32 U = (2.f * ((float32)a_U + .5f) / (float32)a_Size ) - 1.f;
float32 V = (2.f * ((float32)a_V + .5f) / (float32)a_Size ) - 1.f;
float32 InvResolution = 1.0f / a_Size;
// U and V are the -1..1 texture coordinate on the current face.
// Get projected area for this texel
float32 x0 = U - InvResolution;
float32 y0 = V - InvResolution;
float32 x1 = U + InvResolution;
float32 y1 = V + InvResolution;
float32 SolidAngle = AreaElement(x0, y0)
- AreaElement(x0, y1)
- AreaElement(x1, y0)
+ AreaElement(x1, y1);
return SolidAngle;
}
```


The Spherical Harmonics functions for the first 3 orders are listed below. These formulas assume a normalized direction vector \(d = (x, y, z)\).

| l = 0 | l = 1 | l = 2 | |
|---|---|---|---|
| m = -2 | \(\frac{1}{2}\sqrt{\frac{15}{\pi}}yx\) | ||
| m = -1 | \(\frac{1}{2}\sqrt{\frac{3}{\pi}}y\) | \(\frac{1}{2}\sqrt{\frac{15}{\pi}}yz\) | |
| m = 0 | \(\frac{1}{2} \sqrt{\frac{1}{\pi}}\) | \(\frac{1}{2}\sqrt{\frac{3}{\pi}}z\) | \(\frac{1}{4}\sqrt{\frac{5}{\pi}}(2z^2 - x^2 - y^2)\) |
| m = 1 | \(\frac{1}{2}\sqrt{\frac{3}{\pi}}x\) | \(\frac{1}{2}\sqrt{\frac{15}{\pi}}zx\) | |
| m = 2 | \(\frac{1}{2}\sqrt{\frac{15}{\pi}}(x^2-y^2)\) |

# Samples

The following shadertoy projects implement evaluation of L1 and L2 Spherical harmonics using the preconvolved ‘Grace Cathedral’ irradiance map.

# Issues

When projecting a spherical signal to spherical harmonics, the following issues can be observed.

## Ringing

HDR lighting can cause certain lobes to be very large negative numbers to cancel out the high positive coefficients. There are various techniques to minimize ringing artifacts.

## Detail to Cost ratio

A higher frequency signal will require higher bands to achieve a good approximation, however, this also increases the computational cost of reconstruction.