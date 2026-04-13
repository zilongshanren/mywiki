---
title: Raytraced global illumination denoising
url: https://interplayoflight.wordpress.com/2022/03/26/raytraced-global-illumination-denoising/
author: Kostas Anagnostou
published: '2022-03-26'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Recently, I’ve been playing Metro: Exodus on Series X a second time, after the enhanced edition was released, just to study the new raytraced GI the developers added to the game (by the way, the game is great and worth playing anyway). What makes this a bigger achievement is that the game runs at 60fps as well. The developers, smartly, use a layered approach in calculating the GI in the game, starting with screen space raymarching the g-buffer for collisions and then resorting to tracing rays at 0.25 rays per pixel (aka raytracing at half the rendering resolution) when none is found. They also use [DDGI ](https://morgan3d.github.io/articles/2019-04-01-ddgi/)to calculate second bounce, to light the hitpoints with indirect lighting as well, and all these working together give an overall great lighting result. While all this is very interesting, it is their approach to denoising that piqued my interest and I set about to explore it a bit more in my toy renderer. This technique is described in [this presentation](https://developer.download.nvidia.com/video/gputechconf/gtc/2019/presentation/s9985-exploring-ray-traced-future-in-metro-exodus.pdf) and expanded in [this one](https://developer.download.nvidia.com/video/gputechconf/gtc/2020/presentations/s22699-fast-denoising-with-self-stabilizing-recurrent-blurs.pdf), where from I will be borrowing some images as well.

At the moment games typically raytrace with 1 ray per pixel maximum, and this results to a very noisy image.

![](../../assets/40d7e0a8821f1ccc.png)


![](../../assets/40d7e0a8821f1ccc.png)

Developers need to resort to quite involved denoising methods to suppress that noise, fill-in the missing data and achieve good final quality.

Animating the noise used to produce the rays and temporally accumulate, one can increase the amount of information in the image.

![](../../assets/8ddb0d9f61980789.png)


![](../../assets/8ddb0d9f61980789.png)

You can generate the rays animating the blue noise as described [here](https://blog.demofox.org/2017/10/31/animating-noise-for-integration-over-time/) or by binding a different blue noise texture every frame (I have found the latter to produce better results)

```
GenerateTangentFrame(normal, tangent, bitangent);
rand = blueNoiseBuffer[screenPos.xy & (NOISE_TEX_SIZE - 1)].xy;
float3 rayDirection = SampleHemisphere(rand.xy);
rayDirection = rayDirection.x * tangent + rayDirection.y * bitangent + rayDirection.z * normal;
```

The output of the temporal accumulation pass can then be spatially blurred to remove the remaining noise. The blurring is done in world space to better preserve thin objects and to avoid contribution from surfaces that are too far away from the zone of interest (image from the above presentation).

For the blurring kernel we can use offsets from a Poisson distribution.

This is common denoising setup, described in the following diagram from the presentation:

The temporal accumulation does not see the result of the blurring pass and this can lead to an increased number of blurring passes (of kernel samples) to adequately remove the noise from the image. The authors of the Metro: Exodus’ denoising tech suggested using the output of the blurring pass as the history buffer for the temporal accumulation pass, to reduce the number of samples required for the blurring kernel.

The authors called this technique a “recurrent blur”. Using this approach and animating (rotating) the blur kernel:

```
float rand = blueNoiseBuffer[screenPos.xy & (NOISE_TEX_SIZE - 1)].x;
theta = rand.x * 2.0f * PI;
float cosTheta = cos(theta);
float sinTheta = sin(theta);
for (int i = 0; i < NoofTaps; i++)
{
float2 tapPos = taps[i];
tapPos.x = tapPos.x * cosTheta - tapPos.y * sinTheta;
tapPos.y = tapPos.x * sinTheta + tapPos.y * cosTheta;
//do texture sampling
}
```

we can remove most of the noise in a single blurring pass. On top of this, to avoid overblurring, the authors suggest modifying the blur kernel radius based on how long ago the pixel history was rejected (for example because of a disocclusion) and they adjust it as such:

```
float N = min(FramesSinceHistoryReset, 32);
float blurScale = 1.0 / (1.0 + N);
float radius = GIBlurRadius * blurScale;
```

This has the effect of a large radius (and stronger blurring) with newly rejected pixels which gradually reduces as number of sample accumulated in the history buffer for a specific pixel increases.

Applying all this using a kernel of 8 Poisson distributed taps, rotated every frame, of 2m radius suppresses the noise quite well:

![](../../assets/240016aadb0154cd.png)


![](../../assets/240016aadb0154cd.png)

The only problem is that the filter kernel is not geometry aware so it blurs across surface that it should not. To address that, the authors suggest taking the normal of each sample into account and compare it with the central pixel’s one, to modify the sample weight:

```
float3 normalSample = NormalsBuffer.SampleLevel(SamplerLinear, newUV, 0).xyz;
float normalW = saturate(dot(normal, normalSample));
normalW = pow(normalW, NormalWeightStrength);
w *= normalW;
```

Actually they suggest not raising the normal’s dot product to a power but for the above scene at least I found it necessary to improve bleeding across different surfaces.

![](../../assets/53450bc13199db48.png)


![](../../assets/53450bc13199db48.png)

This works well with surfaces with different orientations but not when they are “parallel” like the walls in this case:

To address this, the authors use the distance of the sample from the plane tangent to the central pixel to modify the sample weight.

This handles these cases well

![](../../assets/6b75c1581d8e7e5d.png)


![](../../assets/6b75c1581d8e7e5d.png)

One final addition I made was to use ambient occlusion to modify the blur radius. This helps overblurring the occlusion and maintains a better contrast. Since this is an indoor scene and a full AO term would overdarken the scene (and affect blurring disproportionately), I instead calculated ambient obscurance clamping the ray hit distance to 0.5m: AO = saturate(hitDistance/0.5);

![](../../assets/26740ed0ecadb9d9.png)


![](../../assets/26740ed0ecadb9d9.png)

I used this term to directly scale the blur radius.

![](../../assets/ce48f975962b4493.png)


![](../../assets/ce48f975962b4493.png)

While Metro: Exodus’ denoising technique is not the most “state of the art” any more (other techniques like [ReSTIR](https://research.nvidia.com/publication/2021-06_ReSTIR-GI%3A-Path) have since emerged, although the recurrent blur is still the basis of techniques like [ReBLUR](https://www.springerprofessional.de/en/reblur-a-hierarchical-recurrent-denoiser/19538328)), I appreciate how it used existing denoising tools like temporal accumulation and geometric aware blurring in a smart way to achieve good results and high framerates.