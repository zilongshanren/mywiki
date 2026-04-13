---
title: 'Occlusion and directionality in image based lighting: implementation details'
url: https://interplayoflight.wordpress.com/2021/12/31/occlusion-and-directionality-in-image-based-lighting-implementation-details/
author: Kostas Anagnostou
published: '2021-12-31'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

I got a few follow-up questions on the blog post I published a few days ago on[ occlusion and directionality in image based lighting](https://interplayoflight.wordpress.com/2021/12/28/notes-on-occlusion-and-directionality-in-image-based-lighting/), so I put together a quick follow-up to elaborate on a few points and add some more resources.

To implement the main technique the exploration was based on, Ground Truth ambient occlusion, it is worth starting with the [original paper](https://www.activision.com/cdn/research/Practical_Real_Time_Strategies_for_Accurate_Indirect_Occlusion_NEW%20VERSION_COLOR.pdf) by Jimenez et al. This is best read in conjunction with the [Siggraph 2016 presentation](https://blog.selfshadow.com/publications/s2016-shading-course/#course_content), it will help to understand the paper better. The paper also includes fairly detailed pseudo-code for the GTAO and bent normals implementation, it will help to also use [Intel’s implementation](https://github.com/GameTechDev/XeGTAO) of the technique as a reference, it clarifies some parts of it as well. At the moment the sample does not seem to implement directional GTAO, in which the visibility cone is combined with the cosine and projected to SH.

The first step towards implementing directional GTAO is to convert the original cubemap to a spherical harmonics representation like I discussed in the previous post. An easy way to achieve this is to use the SHMath library in DirectXMath [https://github.com/microsoft/DirectXMath](https://github.com/microsoft/DirectXMath), and more specifically the SHProjectCubeMap() method.

```
HRESULT DirectX::SHProjectCubeMap(
size_t order,
const D3D12_RESOURCE_DESC& desc,
const D3D12_SUBRESOURCE_DATA cubeMap[6],
float *resultR,
float *resultG,
float *resultB
);
```

By setting the order to 3, this will return the 9 float3 SH coefficients used in the exploration. Worth bearing in mind that this method doesn’t support the DXGI_FORMAT_R8G8B8A8_UNORM or DXGI_FORMAT_R8G8B8A8_UNORM_SRGB texture formats out of the box so you will need to add support for it in _LoadScanline() in the large switch statement:

```
case DXGI_FORMAT_R8G8B8A8_UNORM:
case DXGI_FORMAT_R8G8B8A8_UNORM_SRGB:
LOAD_SCANLINE(XMUBYTEN4, XMLoadUByteN4)
```

You also need to make sure that the data are linearised before projected to SH coefficients. Another thing worth bearing in mind is that this method uses the [Condon-Shortley Phase](https://mathworld.wolfram.com/Condon-ShortleyPhase.html) which means that it flips the sign of SH basis for odd m indices (check [Stupid SH tricks](https://www.ppsloan.org/publications/StupidSH36.pdf), Appendix A2 for the polynomial form of the SH basis it actually implements). Whether it flips the sign or not is not that important, what is important is that the SH basis is consistent on both ends, when projecting the cubemap on the CPU and when using the SH coefficients to reconstruct the irradiance in the HLSL shader.

Speaking of which, in the shader we can use the SH coefficients to retrieve the irradiance using the following rough code.

```
float3 GetSHIrradiance(float3 n, float AO, float3 SH[9])
{
// Calculate SH basis, based on PreprocessSHForShader() in https://github.com/GameTechDev/XeGTAO
float SQRT_PI = 1.7724538509f;
float SQRT_5 = 2.2360679775f;
float SQRT_15 = 3.8729833462f;
float SQRT_3 = 1.7320508076f;
float Y[9] = {
1.0f / (2.0f * SQRT_PI), // 0 0
-SQRT_3 / (2.0f * SQRT_PI), // 1 -1
SQRT_3 / (2.0f * SQRT_PI), // 1 0
-SQRT_3 / (2.0f * SQRT_PI), // 1 1
SQRT_15 / (2.0f * SQRT_PI), // 2 -2
-SQRT_15 / (2.0f * SQRT_PI), // 2 -1
SQRT_5 / (4.0f * SQRT_PI), // 2 0
-SQRT_15 / (2.0f * SQRT_PI), // 2 1
SQRT_15 / (4.0f * SQRT_PI) // 2 2
};
// Calculate the zonal harmonics expansion for V(x, ωi)*(n.l)
float t = acos(sqrt(1 - AO));
float a = sin(t);
float b = cos(t);
float A0 = sqrt(4 * PI) * (sqrt(PI) / 2) * a * a;
float A1 = sqrt(4 * PI / 3) * (sqrt(3 * PI) / 3) * (1 - b * b * b);
float A2 = sqrt(4 * PI / 5) * (sqrt(5 * PI) / 16) * a * a * (2 + 6 * b * b);
// Calculate irradiance combining all the above with the normal
float3 irradiance =
SH[0].xyz * A0 * Y[0] +
SH[1].xyz * A1 * Y[1] * n.y +
SH[2].xyz * A1 * Y[2] * n.z +
SH[3].xyz * A1 * Y[3] * n.x +
SH[4].xyz * A2 * Y[4] * (n.y * n.x) +
SH[5].xyz * A2 * Y[5] * (n.y * n.z) +
SH[6].xyz * A2 * Y[6] * (3.0 * n.z * n.z - 1.0) +
SH[7].xyz * A2 * Y[7] * (n.z * n.x) +
SH[8].xyz * A2 * Y[8] * (n.x * n.x - n.y * n.y);
return max( irradiance, 0);
}
```

A quick analysis of the above code: at the beginning we calculate the SH basis constants (array Y[9]), as described in the Stupid SH Tricks document mentioned above, flipping the sign on odd polynomials to make it match the one used in SHProjectCubeMap().

The second part calculates the coefficients for the **V(x,ω i)(n.l)** product like discussed in the

[GTAO paper](https://www.activision.com/cdn/research/Practical_Real_Time_Strategies_for_Accurate_Indirect_Occlusion_NEW%20VERSION_COLOR.pdf). As a first step it retrieves the cone aperture angle from the AO value passed to the function (equation 22). Then it calculates the A0-A2 SH coefficients. Attention must be paid to the fact that the paper lists them as (equation 23)

but to bring them in their final, usable form we need to use equation 17 from the paper

for l = 0, 1, 2 (these are zonal harmonics, they are defined only for m = 0, i.e. they are the same for the whole SH basis row, like discussed in the previous post). This is actually what the shader above calculates for the A0, A1, A2 coefficients.

Finally, all the coefficients are combined with the SH basis to retrieve the irradiance. This needs to be multiplied by the Lambert brdf (**albedo/π**) later to get the final surface colour, but **no AO needs to be multiplied on top**, this is accounted for in the visibility cone projection above. This function should also be called with the bent normal calculated by the GTAO method.

The code is a bit messy and could be optimised a bit, for example the Y[9] constants can be premultiplied into the SH coefficients on the CPU, all that PI Maths can be baked into constants etc, but it is easier to map back to the paper this way.

Wrapping up, it is worth mentioning, like [it has been called out on Twitter](https://twitter.com/KostasAAA/status/1475853832877977606), that the GTAO paper also describes techniques for cheap multibounce AO as well as indirect specular occlusion, which is equally important to directional diffuse AO and worth exploring.

[…] Occlusion and directionality in image based lighting: implementation details […]