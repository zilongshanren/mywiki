---
title: Free blue noise textures
url: http://momentsingraphics.de/BlueNoise.html
published: '2017-05-16'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# Free blue noise textures

**Update 2016-12-23:** [Morgan McGuire](https://twitter.com/CasualEffects) suggested a use case for blue noise volume textures, so I decided to test this a little. I've uploaded a new version of [the code](http://momentsingraphics.de/Media/BlueNoise/BlueNoiseCode.zip) that fixes a bug for higher-dimensional textures and revised the corresponding paragraph at the end of the The void and cluster method section.

**Update 2017-01-31:** The code is now a separate download with several new features. It is also [available on GitHub](https://github.com/MomentsInGraphics/BlueNoise). A follow-up [blog post on 3D blue noise](http://momentsingraphics.de/3DBlueNoise.html) is online.

Dithering is almost as old as computer graphics but recently it has received quite a lot of attention among game developers. To name two examples out of many, [Mikkel Gjoel](https://twitter.com/pixelmager) spoke about its use in [Inside at GDC 2016](http://www.gdcvault.com/play/1023002/Low-Complexity-High-Fidelity-INSIDE) and [Bart Wronski wrote a blog post series](https://bartwronski.com/2016/10/30/dithering-in-games-mini-series/) about it. This attention is well-deserved.

Whenever you need to round or threshold some real quantity, there is a good chance that dithering provides an inexpensive way to get smoother results. The basic idea is to ensure that the average of pixels in a small region produces a value that resembles the original real quantity more closely. Since the human visual system tends to blur things a little, it essentially computes this average and gets a more accurate impression of the true value. This can look fairly convincing, especially on displays with a high pixel density, as shown in [Figure 1](http://momentsingraphics.de#DitheringExample).

![DitheringExample](../../assets/dd4dc47839300dae.png)


![DitheringExample](../../assets/dd4dc47839300dae.png)

**Figure 1:**Top: A linear greyscale ramp. Bottom: The same greyscale ramp with blue noise dithering. The image only uses two brightness values (black and white) but if you squint your eyes a little it looks much like the original color ramp. Brightness may differ dependent on how close your monitor is to proper sRGB. For an optimal effect, please ensure that your browser does not scale the image (or any of the images below).

We will review some practical applications below but these are not our main objective. If you need more motivation, Mikkel Gjoel does an excellent job explaining [why you want to use dithering](http://www.gdcvault.com/play/1023002/Low-Complexity-High-Fidelity-INSIDE). Instead we take a close look at one particular way to do it that is well-suited for real-time rendering; precomputed blue noise textures.

Blue noise is so useful and inexpensive that everybody should be using it all the time. With this blog post I am hoping to make this easier than ever. The blog post is accompanied by code and a precomputed database of [free blue noise textures](http://momentsingraphics.de/Media/BlueNoise/FreeBlueNoiseTextures.zip).

## Blue noise properties

To get from the continuous greyscale ramp in [Figure 1](http://momentsingraphics.de#DitheringExample) to the dithered version, we take the linear brightness, compare it to a value from a texture with noise and then output black if it is less or equal and white if it is greater. The only difficult part is getting the texture with the noise values because not all sorts of noise are equally well-suited. Robert Ulichney proposed a definition of noise that works particularly well for this purpose and dubbed it blue noise [[Ulichney88]](http://momentsingraphics.de#_Ulichney88). It draws its power from various properties that we review in the following.

If you are not interested in the underlying theoretical considerations, feel free to skip to the A database of blue noise textures section.

### Uniform

Suppose the greyscale ramp at one point has a linear brightness of \(p\in[0,1]\). After dithering the average of pixels in this region (assuming a somewhat uniform brightness) should be as close as possible to \(p\). Put differently, the probability that we output white for this point using a random noise value \(n\in[0,1]\) should be \(p\). We can immediately see what this means for the probability distribution of our noise:
\[ P(n\le p)=p \]
This can only work for all \(p\in[0,1]\) if \(n\) has a uniform distribution on \([0,1]\), i.e. the probability density function is constant one. Getting uniformly distributed (pseudo-)random numbers is easy enough, even in real-time. For example you can use the [Wang hash as proposed by Nathan Reed](http://www.reedbeta.com/blog/quick-and-easy-gpu-random-numbers-in-d3d11/). This way, your random numbers for each pixel will be independent. Such random numbers are called white noise. [Figure 2](http://momentsingraphics.de#WhiteNoiseDithering) demonstrates this approach for dithering a uniform grey image.

![WhiteNoiseDithering](../../assets/2ba0f67d75caf15e.png)


![WhiteNoiseDithering](../../assets/2ba0f67d75caf15e.png)

**Figure 2:**A uniform grey image with linear brightness 0.3 dithered to black and white using white noise.

### Weak low-frequency components

The result in [Figure 2](http://momentsingraphics.de#WhiteNoiseDithering) is not really what we want though. If it were, blurring it would get us close to the original uniform grey image. Instead we get [Figure 3](http://momentsingraphics.de#WhiteNoiseDitheringBlurred). As you can see, there are fairly obvious large-scale structures.

We can use the [Fourier transform](https://en.wikipedia.org/wiki/Fourier_transform) to understand why. If you do not know what that means, do not feel too bad. I won't explain it here but I will provide intuitions for all of the findings. And if you ever have some time for training, learning about signal processing is an excellent way to spend it.

Through the Fourier transform the white noise becomes what you see in [Figure 4](http://momentsingraphics.de#WhiteNoiseFFT). As you can see, it still looks like white noise. Energy is spread out uniformly across all frequency bands. This means that large-scale structures are just as strong as small-scale structures. Blurring diminishes the small-scale structures but leaves us with the large-scale structures which is why [Figure 3](http://momentsingraphics.de#WhiteNoiseDitheringBlurred) still has so much visible structure.

### Isotropic

There is another fast way to compute uniformly distributed textures for dithering: You can generate [Bayer matrices](https://en.wikipedia.org/wiki/Ordered_dithering) such as the one in [Figure 5](http://momentsingraphics.de#BayerMatrix). Doing so just takes a few bitwise logical operations and bit shifts, so it is very easy and fast. The result is an ordered pattern that gives us [Figure 6](http://momentsingraphics.de#BayerDithering) when we use it for dithering. This is still not what we want, because this time the structure is way to obvious. You can clearly see horizontal, vertical and diagonal lines.

The Fourier transform, shown in [Figure 7](http://momentsingraphics.de#BayerFFT), reflects this. There is a single bright spot in the middle, which simply means that our Bayer matrix has a high average value. Values near this spot are fairly small, which means that there is little low-frequency content. However, the energy for the higher frequencies is localized in a small number of frequencies (seen as a few grey dots). Each of them corresponds to a direction where the pattern is strongly periodic. This is why you see all these horizontal, vertical and diagonal lines.

A good noise texture for dithering should spread out its energy evenly in all directions. The Fourier transform should be as radially symmetric around the center as possible. At the same time, we want weak low-frequency components and a uniform distribution. Taking all these demands together gives us blue noise [[Ulichney88]](http://momentsingraphics.de#_Ulichney88).

[Figure 8](http://momentsingraphics.de#BlueNoise470) shows such a noise texture and [Figure 9](http://momentsingraphics.de#BlueNoise470FFT) shows its Fourier transform. As you can see the blue noise texture has less large scale structure than the white noise and indeed the Fourier transform is small near the center. At the same time, it is very isotropic as can be seen from its radial symmetry.

If we dither our grey image with this blue noise, we get the pleasant result in [Figure 10](http://momentsingraphics.de#BlueNoise470Dithering). After blurring it looks almost entirely uniform as shown in [Figure 11](http://momentsingraphics.de#BlueNoise470DitheringBlurred).

### Tileable

Blue noise is extremely well-suited for dithering but unlike white noise or Bayer matrices, we cannot afford to compute it on the fly. We have to precompute it. The question is what resolution we should use? Should we make our blue noise textures as large as the screen resolution? That would impose quite an overhead in terms of memory and bandwidth. Clearly, it would be nicer to work with smaller blue noise textures. Ideally, they would be so small that they fit into L1-cache entirely to reduce the burden in terms of bandwidth.

The obvious way to accomplish this is to make the blue noise textures tileable. Doing so is not too difficult, you just have to wrap around everything at the borders during construction of the texture. And as it turns out, the absence of strong low-frequency content helps a lot in terms of tiling. [Figure 12](http://momentsingraphics.de#BlueNoise64Tiled) shows what tiling of a 64² blue noise texture looks like. If you look very closely, you can probably notice the tiling but it is not too obvious. Fairly small blue noise textures can be enough to do full-screen dithering. For comparison [Figure 13](http://momentsingraphics.de#WhiteNoise64Tiled) shows a tiling of a 64² white noise texture. Here the tiling is very obvious due to the repeating large-scale structures.

## The void and cluster method

Now that we know what blue noise is, it is time to generate it. While this is not an easy problem by any means, it is well-studied and excellent solutions exist. After some literature research I decided to go with Robert Ulichney's void and cluster method [[Ulichney93]](http://momentsingraphics.de#_Ulichney93). The paper does a good job explaining it and it is not too difficult to implement.

The basic idea is to place pixels in increasing order by their brightness. A nice side effect is that each brightness occurs exactly once (e.g., a 16² texture will contain all values from 0 to 255). When a new pixel is placed, a binary mask of already placed pixels is blurred with a tileable Gaussian and the next pixel is placed at the darkest point in this blurred mask. This darkest point is far away from other points, so it is called “largest void.” Through this construction similar values cannot cluster together which avoids large-scale structures. The full algorithm has a few more phases with slight variations of this basic idea. The first phase utilizes randomly placed points and is the only non-deterministic step. For a full discussion, you should read the paper [[Ulichney93]](http://momentsingraphics.de#_Ulichney93).

As far as I can tell, I have implemented this method exactly as described in the paper. The implementation uses Python with the [SciPy stack](http://scipy.org/). The algorithm maps well to such an environment because the most expensive operations are implemented very efficiently in SciPy. Blurring is done through a fast Fourier transform, so the asymptotic run time is \(O(n^2\cdot\log(n))\) where \(n\) is the number of pixels. A 64² blue noise texture will be ready in a little more than a second but you have to wait several days for a 1024² texture. The implementation is well-documented and [available for download](http://momentsingraphics.de/Media/BlueNoise/BlueNoiseCode.zip).

The results are really good. As an example we analyze the 64² blue noise texture in [Figure 14](http://momentsingraphics.de#BlueNoise64Magnified) in more detail. [Figure 12](http://momentsingraphics.de#BlueNoise64Tiled) has already shown how nicely this texture tiles. The Fourier transform in [Figure 15](http://momentsingraphics.de#BlueNoise64FFT) gives an impression of how weak the low-frequency components are.

We can further analyze this by binning frequencies into radial bins and taking the mean as shown in [Figure 16](http://momentsingraphics.de#BlueNoise64RadialSpectrum). This is the typical blue noise spectrum with weak low frequencies. If we bin frequency components dependent on their angle, we get [Figure 17](http://momentsingraphics.de#BlueNoise64AngularSpectrum) which nicely demonstrates just how isotropic the blue noise is.

![BlueNoise64RadialSpectrum](../../assets/c9857f1712e193b7.png)

![BlueNoise64AngularSpectrum](../../assets/78bc77316595c280.png)

Note that the void and cluster method has two parameters besides the output resolution. One is the standard deviation for the Gaussian filter. With larger values you get stronger low-frequency components but better isotropy. Too small values lead to ordered patterns similar to a Bayer matrix. A standard deviation of 1.9 pixels appears to be a good middle ground. The other parameter determines how many points are placed randomly as initial seed. Everything else is deterministic, so if this value is too small you get a deterministic, ordered pattern. Little changes once the value is moderately small.

Another interesting note is that the implementation provided here does not care about the dimension of the output texture. The algorithm trivially generalizes to arbitrary dimensions. In particular, you can generate blue noise volume textures. Just pass a tuple with the resolutions for each of the three dimensions. To generate a volume texture with \(40\cdot 30\cdot 10\) voxels you would write `GetVoidAndClusterBlueNoise((40,30,10),1.9)`

. You can even define an anisotropic Gaussian filter with a different standard deviation for each dimension by writing `GetVoidAndClusterBlueNoise((40,30,10),(1.9,1.7,1.0))`

. Note that this feature has not been tested extensively and was not intended in the original publication [[Ulichney93]](http://momentsingraphics.de#_Ulichney93). Use it at your own risk.

## A database of blue noise textures

Of course, nobody likes to get the code of others running. And you do not have to. I kept my notebook busy for a few days to generate blue noise textures that should cover most needs. This way, you only have to [download the textures](http://momentsingraphics.de/Media/BlueNoise/FreeBlueNoiseTextures.zip), load them into your engine and write a few lines of shader code. I have placed them in the public domain through [CC0-licensing](https://creativecommons.org/publicdomain/zero/1.0/).

All blue noise textures in the database are tileable. Resolutions range from 16² to 1024². There are textures with a single channel of blue noise, two channels, three channels and four channels. Each texture has been stored as common 8-bit RGBA PNG (for easy loading) and as 16-bit PNG with the appropriate number of channels. Only the 512² and 1024² textures are not available in HDR because my code for storing them had an overflow. There are many versions of most textures such that you can use a different one in each frame. Any two textures in the database have been computed with independent random numbers. Only the HDR and LDR versions of the same texture are not independent.

If this choice seems a bit overwhelming, I recommend that you use the 64² 8-bit textures. Just load all 64 of them into a texture array, pick one at random in each frame and apply a random offset in each frame. Concerning the number of channels, you should never use the same channel twice in a single frame. Thus, if you need to dither three real quantities (e.g., a 2D texture coordinate and a brightness), you should use the RGB version of the textures. If you need more than four blue noise values, use multiple textures from the texture array in a single frame.

## Example applications

Now we have all the blue noise we could wish for. It is time to think of ways to use it. Let's begin with the classic.

### Dithering

HDR televisions and monitors are on the rise but the vast majority of customers still sees your content with 8 bits per channel. Whenever you render smooth gradients, large bands will have the exact same color due to this quantization. And on most displays these bands are visible under normal viewing conditions.

As long as people have LDR displays (and possibly beyond that point), dithering is the best way to work around this. Right before the quantization happens, you add blue noise to each pixel. Bands turn into finely stippled gradients that are far less distracting.

As an example I have applied dithering to [prefiltered single scattering with six moments](http://momentsingraphics.de/I3D2016.html). For reasons that are well-explained [elsewhere](http://www.gdcvault.com/play/1023002/Low-Complexity-High-Fidelity-INSIDE) it is best to transition from the uniform noise distribution to a triangular distribution before using the noise for dithering. Also, it is important to do it in the color space in which quantization actually happens. In my case this is sRGB. The whole dithering code is given in [Listing 1](http://momentsingraphics.de#ScatteringDithering). The used sRGB conversion functions are shown in [Listing 2](http://momentsingraphics.de#SRGBConversion).

**Listing 1:**Applies dithering to a linear radiance.

`BlueNoiseTexture`

is supposed to be an array of 64 blue noise textures of resolution 64². `SourceTexelIndex`

is the screen space coordinate of the shaded pixel. `Randomness`

is updated once per frame by setting each bit uniformly at random.```
void ComputeDitheredScatteringColor(
out float4 OutScatteringColor,
float3 ScatteringRadiance,
Texture2DArray<float4> BlueNoiseTexture,
uint2 SourceTexelIndex,uint4 Randomness)
{
// Get some blue noise
float3 BlueNoise=BlueNoiseTexture.Load(uint4((SourceTexelIndex+Randomness.xy)&0x3F,Randomness.w&0x3F,0)).rgb;
// Go from a uniform distribution on [0,1] to a
// symmetric triangular distribution on [-1,1]
// with maximal density at 0
BlueNoise=mad(BlueNoise,2.0f,-1.0f);
BlueNoise=sign(BlueNoise)*(1.0f-sqrt(1.0f-abs(BlueNoise)));
// The dithering has to be done in the same
// space as quantization which is sRGB
OutScatteringColor.rgb=SRGBToLinear(LinearToSRGB(ScatteringRadiance)+BlueNoise/255.0f);
OutScatteringColor.a=1.0f;
}
```


```
/*! Turns a linear RGB color value into sRGB.*/
float3 LinearToSRGB(float3 LinearRGB){
return (LinearRGB<=0.0031308f)?(12.92f*LinearRGB):mad(1.055f,pow(LinearRGB,1.0f/2.4f),-0.055f);
}
/*! Turns an sRGB color value into a linear RGB color
value.*/
float3 SRGBToLinear(float3 SRGB){
return (SRGB<=0.04045f)?(SRGB/12.92f):pow(mad(SRGB,1.0f/1.055f,0.055f/1.055f),2.4f);
}
```


[Figure 18](http://momentsingraphics.de#ScatteringNotDithered) and [Figure 19](http://momentsingraphics.de#ScatteringBlueNoiseDithered) compare single scattering without and with this blue noise dithering, respectively. Dependent on your monitor you may or may not see the difference. In case you do not, I have brightened the images in [Figure 20](http://momentsingraphics.de#ScatteringNotDitheredBrightened) and [Figure 21](http://momentsingraphics.de#ScatteringBlueNoiseDitheredBrightened). As you can see dithering successfully removes the banding and leads to a very smooth end result.

![ScatteringBlueNoiseDithered](../../assets/44b38b692a951234.png)


![ScatteringBlueNoiseDithered](../../assets/44b38b692a951234.png)

**Figure 19:**Participating media with blue noise dithering. The banding has been replaced by less distracting stippled gradients.

### Jittering

A slightly less common application is jittering in ray marching. Ray marching is the simplest way to render participating media (but [not the fastest](http://momentsingraphics.de/I3D2016.html)). You just integrate along each view ray step by step while taking a sample from a shadow map at each step. Jittering means that you add some noise to your starting point along the ray to get a different sampling for each pixel.

[Figure 22](http://momentsingraphics.de#RayMarchingWhiteNoise) shows the result with white noise (i.e. independent random numbers per pixel). As you can see, the end result is very noisy. [Figure 23](http://momentsingraphics.de#RayMarchingBlueNoise) does the same thing using blue noise. The quality improvement is quite astounding. Suddenly, 32 samples seem like they could be enough. This is a huge cost-saving.

![RayMarchingBlueNoise](../../assets/42302e2e26a7e157.png)


![RayMarchingBlueNoise](../../assets/42302e2e26a7e157.png)

**Figure 23:**Ray marching with 32 samples per pixel in a scene with foliage using blue noise for jittering. The result appears far less noisy than

[Figure 22](http://momentsingraphics.de#RayMarchingWhiteNoise)in spite of the identical number of samples. Click

[here for the full image](http://momentsingraphics.de/Media/BlueNoise/RayMarchingBlueNoiseFull.png).

The implementation is not difficult either. You grab a single uniform blue noise value as in [Listing 1](http://momentsingraphics.de#ScatteringDithering) (note that you can use single-channel textures here), multiply it by the delta-vector between ray-sample locations and add that to the location of your first ray sample.

### Bilinear interpolation

As our last application we use blue noise to make [moment soft shadow mapping](http://momentsingraphics.de/I3D2016.html) even faster than it already is. It used to impose a fairly high bandwidth overhead per shaded pixel (2560 bits) because it uses textures with integer entries and therefore hardware bilinear interpolation cannot be utilized. We have to load all the involved texels and do the interpolation manually.

To avoid this cost, we can instead make a pseudo-random choice for one of the four neighboring texels at each point. The probabilities reflect the interpolation weights and the pseudo-randomness comes from a four-channel blue noise texture. This brings the bandwidth overhead down to 1088 bits. The implementation is shown in [Listing 3](http://momentsingraphics.de#DitheredSATQuery). Explaining this code in full would go beyond the scope of this blog post, but the first five lines of the function body are the interesting part. This is where blue noise is added to the texture coordinates before rounding to dither the query.

**Listing 3:**A query to an integer summed-area table using pseudo bilinear interpolation by means of blue noise dithering. The last three parameters are analogous to those in

[Listing 1](http://momentsingraphics.de#ScatteringDithering).

```
void ComputeIntegerRectangleAverage_uint4(
out float4 OutAverageValue,
float2 LeftTop,float2 RightBottom,
Texture2D<uint4> SummedAreaTableTexture,
float4 TextureSize,float2 FixedPrecision,
int2 ViewportPixelIndex,
Texture2DArray<float4> BlueNoiseTexture,
uint4 Randomness)
{
// Sample blue noise
float4 BlueNoise=BlueNoiseTexture.Load(uint4((ViewportPixelIndex+Randomness.yz)&0x3F,Randomness.x&0x3F,0));
// Apply blue noise dithering
int2 iLeftTop=int2(floor(LeftTop*TextureSize.xy+BlueNoise.xy))-1;
int2 iRightBottom=int2(floor(RightBottom*TextureSize.xy+BlueNoise.zw))-1;
// Query a rectangle in the summed-area table
uint4 Sample[2][2]={
{SummedAreaTableTexture.Load(int3(iLeftTop.x,iLeftTop.y,0)),
SummedAreaTableTexture.Load(int3(iLeftTop.x,iRightBottom.y,0))},
{SummedAreaTableTexture.Load(int3(iRightBottom.x,iLeftTop.y,0)),
SummedAreaTableTexture.Load(int3(iRightBottom.x,iRightBottom.y,0))}
};
uint4 Integral=Sample[0][0]+Sample[1][1]-Sample[0][1]-Sample[1][0];
uint2 Size=iRightBottom-iLeftTop;
OutAverageValue=float4(Integral)*FixedPrecision.y/float(Size.x*Size.y);
}
```


[Figure 24](http://momentsingraphics.de#HardShadowNotDithered) shows what the shadow looks like without any interpolation. Obviously, it is blocky. [Figure 25](http://momentsingraphics.de#HardShadowDithered) does the interpolation through blue noise dithering and it immediately looks much better. You can see some noise but when the noise is animated, this becomes even less objectionable and if the ground had some texture, it would be hard to notice.

This gets even better as the shadow becomes softer. Since we are dealing with soft shadows, this happens at greater distance from shadow casters. The contrasts between adjacent pixels become smaller and the noise becomes almost imperceptible, even on the bright white ground plane.

The total frame time for the [full image with dithering](http://momentsingraphics.de/Media/BlueNoise/ShadowDitheredFull.png) at \(3840\cdot 2160\) and with \(4\times\) multi-sample antialiasing is a mere 3.4 ms on a GTX 970. Compared to the 4.8 ms that it takes to render with true bilinear interpolation, this is a major saving.

## Conclusions

Blue noise provides an easy to use but extremely powerful way to spread and amortize pixel shader workload across pixels and across frames (especially if you use temporal antialiasing). Among all sorts of noise that I am aware of, it usually achieves this goal best. Sometimes you may still prefer other noise because you do not want to afford the texture read, but in all other cases you should use blue noise. Given how much work goes into each pixel, the cost is worth it easily.

Through blue noise you can replace artifacts such as banding and lack of interpolation by patterns that are perceived as aesthetic and do not distract as long as you do not have too high contrasts between adjacent pixels. In many cases, this is the least expensive solution to such problems.

The only good reason not to use blue noise used to be that its generation is difficult. With this blog post and the accompanying database, I am ridding you of this excuse. So please use it.

## A note on patents

As far as I can tell, the void and cluster method [[Ulichney93]](http://momentsingraphics.de#_Ulichney93) is covered by [United States Patent 5,535,020](http://patft.uspto.gov/netacgi/nph-Parser?Sect2=PTO1&Sect2=HITOFF&p=1&u=%2Fnetahtml%2Fsearch-bool.html&r=1&f=G&l=50&d=PALL&RefSrch=yes&Query=PN%2F5535020). I am a complete layman when it comes to patent law. However, the way I understand it, this particular patent expired on 9th of July 2013 (issue date plus 17 years) and is now in the public domain.

It is absolutely possible that I have overlooked some extension or that other patents exist but I feel confident enough that relevant patents have expired before December 2016 to publish this blog post. After all, the paper [[Ulichney93]](http://momentsingraphics.de#_Ulichney93) was published in September 1993 and at this point it was prior art. Any patent covering its contents would have to be filed earlier. Such a filing date plus twenty years puts us in September 2013. There are some ways in which a patent term could extend beyond this point, but it seems unlikely that the patent term is still running three years later.

**Disclaimer:** I am not a lawyer and none of the information provided on this blog is legal advice. It is your responsibility to ensure that you are not violating intellectual property rights or other rights by using the material provided in this blog post and in the [accompanying](http://momentsingraphics.de/Media/BlueNoise/FreeBlueNoiseTextures.zip) [downloads](http://momentsingraphics.de/Media/BlueNoise/BlueNoiseCode.zip). Please note the terms of the [Creative Commons public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/) which apply to [the](http://momentsingraphics.de/Media/BlueNoise/FreeBlueNoiseTextures.zip) [downloads](http://momentsingraphics.de/Media/BlueNoise/BlueNoiseCode.zip) provided as part of this blog post.

## References

[ R. A. Ulichney (1988). Dithering with blue noise. Proc. IEEE, 76(1):56-79.
][Official version](https://dx.doi.org/10.1109/5.3288) | [Author's version](http://cv.ulichney.com/papers/1988-blue-noise.pdf)

[ R. A. Ulichney (1993). Void-and-cluster method for dither array generation. Proc. SPIE 1913, Human Vision, Visual Processing, and Digital Display IV.
][Official version](https://dx.doi.org/10.1117/12.152707) | [Author's version](http://cv.ulichney.com/papers/1993-void-cluster.pdf)

## Downloads

## Comments

**Viktor Sehr**

2017-05-16, 11:49

Very interesting article, thanks for taking the time to write it!

**Nikolay**

2017-10-29, 5:23

Probably best article on blue noise to date, thank you for it.

P.S. Do you know that your blue noise textures are now used in Unity3d official post-processing stack for dithering? 🙂

**Christoph**

2017-10-29, 6:27

You are welcome. I did not know about the use in Unity but that is great to hear. Thank you for sharing 🙂 .

**Garrett Stevens**

2018-06-29, 23:00

This is an excellent breakdown, Thank you for taking the time!

**War**

2018-07-12, 10:31

Thanks for the great post.

Wondering why your fft of the bayer matrix looks different than Bart’s one? These two:

**Christoph**

2018-07-13, 0:07

What I am showing is the absolute value of the discrete Fourier transform for a 16×16 signal. That’s a 16×16 signal again.

Bart starts from an 8×8 signal but the DFT has much higher resolution so I’m guessing that he first tiled the Bayer matrix and then took the DFT. This introduces a lot of additional zero entries into the DFT and thus the pixels look more spread out.

**readr**

2018-09-03, 17:58

Looks like the download link for the Python implementation just points to the textures?

**Christoph**

2018-09-03, 21:09

Thanks, I’ve fixed that. The download link at the bottom was correct, but the others were outdated. Originally, the code was part of the archive with the textures.

Comments are closed.