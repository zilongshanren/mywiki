---
title: Temporal AA and the Quest for the Holy Trail
url: https://www.elopezr.com/temporal-aa-and-the-quest-for-the-holy-trail/
author: Redorav
published: '2022-01-02'
source_blog: The Code Corsair
source_site: http://www.elopezr.com
category: game programming
fetched: '2026-04-13'
---

Long gone are the times where Temporal AA was a novel technique, and slowly more articles appear covering motivations, implementations and solutions. I will throw my programming hat into the ring to walk through it, almost like a tutorial, for the future me and for anyone interested. I am using Matt Pettineo’s [MSAAFilter demo](https://github.com/TheRealMJP/MSAAFilter) to show the different stages. The contents come mostly from the invaluable work of many talented developers, and a little from my own experience. I will introduce a couple of tricks I have come across that I haven’t seen in papers or presentations.

**Sources of aliasing**

The origin of aliasing in CG images varies wildly. Geometric (edge) aliasing, alpha testing, specular highlights, high frequency normals, parallax mapping, low resolution effects (SSAO, SSR), dithering and noise all conspire to destroy our visuals. Some solutions, like hardware MSAA and screen space edge detection techniques, work for a subset of cases but fail in different ways. Temporal techniques attempt to achieve supersampling by distributing the computations across multiple frames, while addressing all forms of aliasing. This stabilizes the image but also creates some challenging artifacts.

**Jitter**

The main principle of TAA is to compute multiple sub-pixel samples across frames, then combine those together into a single final pixel. The simplest scheme generates random samples within the pixel, but there are better ways of producing fixed sequences of samples. Here’s a short overview of [quasi-random sequences](http://extremelearning.com.au/unreasonable-effectiveness-of-quasirandom-sequences/). It is important to select a good sequence to avoid clumping, and a discrete number of samples within the sequence: typically between 4-8 work well. In practice this is more important for a static image than a dynamic one. Below a pixel with 4 samples.

To produce random sub-samples within a pixel we translate the projection matrix by a fraction of a pixel along the frustum plane. The valid range for the jitter offset (relative to the pixel center) is half the inverse of the screen dimension in pixels, so \begin{bmatrix}\dfrac{-1}{2w},\dfrac{1}{2w}\end{bmatrix} and \begin{bmatrix}\dfrac{-1}{2h},\dfrac{1}{2h}\end{bmatrix}. We multiply the offset matrix (just a normal translation matrix) by the projection matrix to get the modified projection, as shown below.


\begin{pmatrix} \dfrac{2n}{w} & 0 & 0 & 0\\ 0 & \dfrac{2n}{h} & 0 & 0\\ 0 & 0 & \dfrac{f}{f-n} & 1\\ 0 & 0 & \dfrac{-f·n}{f-n} & 0\\ \end{pmatrix} · \begin{pmatrix} 1 & 0 & 0 & 0\\ 0 & 1 & 0 & 0\\ 0 & 0 & 1 & 0\\ j_x & j_y & 0 & 1\\ \end{pmatrix}= \begin{pmatrix} \dfrac{2n}{w} & 0 & 0 & 0\\ 0 & \dfrac{2n}{h} & 0 & 0\\ j_x & j_y & \dfrac{f}{f-n} & 1\\ 0 & 0 & \dfrac{-f·n}{f-n} & 0\\ \end{pmatrix}


Once we have a set of samples, we use this matrix to rasterize geometry as normal to produce the image that corresponds to the sample. If it all works well and every frame you get a new jitter, the image should look wobbly like this.

**Resolve**

The next stage in our TAA journey is the resolve pass. We’ll collect the samples and merge them together. Resolve passes can take two forms, either using an accumulation buffer or several past buffers, like [Guerrilla](https://www.guerrilla-games.com/read/decima-engine-advances-in-lighting-and-aa). For this article we’ll stick to the first, as it’s more common and stable. The accumulation buffer stores the result of multiple frames, and gets updated every frame by blending a small percentage (e.g. 10%) of the current, jittered, frame. This should be enough for a static camera. The image still shows some specular aliasing we’ll address later, but it’s stable (it’s an animated webp).

1 2 3 4 | float2 uv = IN.uv; float3 currentColor = CurrentTexture.Sample(uv); float3 previousColor = PreviousTexture.Sample(uv); float3 output = currentColor * 0.1 + previousColor * 0.9; |

So far so good. What happens if we jiggle the camera about a little?

**Ghosting**

The reason we get trails is that we’re sampling the previous frame at the same position as the current frame. The result is a superposition of images that fade away as we accumulate new frames. Since the issue is introduced by moving the camera, let’s tackle that first. Camera motion is relatively simple to fix for opaque objects because we know their world space positions can be reconstructed using the depth buffer and the inverse of the camera projection. For more detail read [here](https://mynameismjp.wordpress.com/2009/03/10/reconstructing-position-from-depth/) and [here](https://mynameismjp.wordpress.com/2010/09/05/position-from-depth-3/), or consult the demo [BackgroundVelocity.hlsl](https://github.com/TheRealMJP/MSAAFilter/blob/master/MSAAFilter/BackgroundVelocity.hlsl). This process is called reprojection, and involves the following steps:

- Read depth from current depth buffer produced by
**current camera C** - Backproject using the inverse of the view-projection matrix, to transform our screen space position into world space
- Use previous view-projection matrix to project onto
**previous camera P**‘s screen space - Transform screen space position to UV and sample the accumulation texture

The devil, as always, is in the details and there are many things to take into account such as the position being outside the previous camera, viewport changes if you have dynamic resolution, etc.

1 2 3 4 5 | float2 reprojectedUV = CameraReproject(uv); float3 currentColor = CurrentTexture.Sample(uv); float3 previousColor = PreviousTexture.Sample(reprojectedUV); float3 output = currentColor * 0.1 + previousColor * 0.9; |

1 2 3 4 5 6 | float2 velocityUV = CurrentVelocityTexture.Sample(uv); float2 reprojectedUV = uv + velocityUV; float3 currentColor = CurrentTexture.Sample(uv); float3 previousColor = PreviousTexture.Sample(reprojectedUV); float3 output = currentColor * 0.1 + previousColor * 0.9; |

![](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7)


![](../../assets/31ea1b2609989e47.webp)

The result is a little blurry but the ghosting has disappeared. Or has it? Let’s try translating the camera now.

**Disocclusion**

As objects move relative to one another, surfaces that weren’t previously visible may come into view; we call that disocclusion. In the image above, moving the camera sideways reveals part of the background that was previously occluded by the model. Note that it looks like it’s the hand that moves, because the background is static. Those two movements are not equivalent, as we’ll see later. The newly revealed surface will correctly reproject itself but encounter invalid information in the accumulation buffer from the model that was previously there. There are multiple ways to address this issue.

#### Color Clamping

Color clamping makes the assumption that colors within the neighborhood of the current sample are valid contributions to the accumulation process. A value sourced from the accumulation buffer that diverges greatly should in theory be discarded. However, rather than throwing the value away and resetting the accumulation process, we adjust it to fit it in the neighborhood and let it through. There are different techniques, but three popular ones are clamp, clip and variance clipping. Shown below in purple is an example of a 3×3 neighborhood. Implementations for different techniques can be found courtesy of [Playdead here](https://github.com/playdeadgames/temporal/blob/4795aa0007d464371abe60b7b28a1cf893a4e349/Assets/Shaders/TemporalReprojection.shader#L212) and their presentation [Temporal Reprojection Antialiasing in INSIDE](https://www.gdcvault.com/play/1022970/Temporal-Reprojection-Anti-Aliasing-in), as well as UE4’s [High Quality Temporal Supersampling](https://de45xmedrsdbp.cloudfront.net/Resources/files/TemporalAA_small-59732822.pdf#page=30).

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 | // Arbitrary out of range numbers float3 minColor = 9999.0, maxColor = -9999.0; // Sample a 3x3 neighborhood to create a box in color space for(int x = -1; x <= 1; ++x) { for(int y = -1; y <= 1; ++y) { float3 color = CurrentTexture.Sample(uv + float2(x, y) / textureSize); // Sample neighbor minColor = min(minColor, color); // Take min and max maxColor = max(maxColor, color); } } // Clamp previous color to min/max bounding box float3 previousColorClamped = clamp(previousColor, minColor, maxColor); // Blend float3 output = currentColor * 0.1 + previousColorClamped * 0.9; |

To more visually represent this algorithm in action I created a little program in Unity that takes a few positions (the value of the position is the color), creates colored spheres (the neighborhood), derives a box from it, takes a history sample and clamps it to that box. It’s easier to see it in 2D. You can appreciate how vastly different colors get approximated to something resembling the original colors.

Any variation of this is a must in a TAA implementation. If the neighborhood has a lot of color variance in it, the bounding box becomes huge and trailing can become apparent again. For that we’ll need extra information. Here’s what clamp looks like.

#### Depth Rejection

The idea behind depth rejection is that we can assume that pixels with very different depth values belong to different surfaces. For this we need to store the previous frame’s depth buffer. This can work well for first person shooters, where the gun and the environment are very far apart. However, it isn’t a universal heuristic, and can go wrong in multiple scenarios, for example foliage or noisy geometry with a lot of depth complexity. For use cases, see:

[Filmic SMAA – Sharp Morphological and Temporal Antialiasing](https://research.activision.com/publications/archives/filmic-smaasharp-morphological-and-temporal-antialiasing)[Dynamic Temporal Antialiasing and Upsampling](https://research.activision.com/publications/2020-03/dynamic-temporal-antialiasing-and-upsampling-in-call-of-duty)

#### Stencil Rejection

Stencil rejection is a bespoke solution that can work well for a limited set of content. The idea is to tag “special” objects with a stencil value that is different to the background. This could be the main character, a car, etc. For this we need to store the previous frame’s stencil buffer. When doing the resolve, we discard any surfaces with different stencil values. Special care needs to be taken to avoid hard edges. For use cases, see:

Update: a similar scheme, mentioned by a [kind reader](https://twitter.com/g_Schellenbaum/status/1477733307152580612?s=20) on Twitter, can be implemented using an ID buffer.

#### Velocity Rejection

Rejecting surfaces based on velocity is in my opinion more robust, as by definition disocclusion arises from the difference in relative motion with respect to the camera between two objects. If two surfaces have very different velocities across two frames then either the acceleration was big or the objects were traveling at different speeds and one suddenly became visible. For this we need to store the previous frame’s velocity buffer. The process is:

- Read current velocity
- Use velocity to determine previous position
- Turn position into UV
- Read previous velocity
- Use velocity similarity metric to determine whether they belong to different surfaces

A discussion on [Twitter](https://twitter.com/BartWronsk/status/1335103698981191680?s=20) mentions two approaches: the dot product of the two velocities and the differences in velocity magnitude. Both have problems.

- Dot product has a discontinuity when either vector is 0 and treats opposing vectors as very different even if their magnitudes are small
- Magnitude difference considers opposing vectors of the same magnitude as identical

The approach I propose is to use the length of the difference between the two vectors, which incidentally is the per-frame acceleration, as the similarity metric. Big accelerations mean disocclusion, and we can create a smooth ramp to take us from no disocclusion to full disocclusion. Here’s a couple of diagrams showing what I mean.

Once we have a similarity metric we can react to it. In this case we are going to lerp towards a slightly blurred version of the screen to avoid having jarring differences between the converged parts and the new ones. An alternative is to modify the convergence factor.

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 | // Assume we store UV offsets float2 currentVelocityUV = CurrentVelocityTexture.Sample(uv); // Read previous velocity float2 previousVelocityUV = PreviousVelocityTexture.Sample(uv + currentVelocityUV); // Compute length between vectors float velocityLength = length(previousVelocityUV - currentVelocityUV); // Adjust value float velocityDisocclusion = saturate((velocityLength - 0.001) * 10.0); // Calculate base accumulated quantity float3 accumulation = currentFrame * 0.1 + previousFrameClamped * 0.9; // Lerp towards a backup value - could be a blurred version derived from the neighborhood float3 output = lerp(accumulation, currentFrameBlurred, velocityDisocclusion); |

#### Alternative Hacks

Another simple way to use velocity is to weigh the contributions based on how fast an object is moving, as they are typically harder to see or are actually affected by e.g. motion blur. Good examples are chase levels or racing games.

**Motion Vectors**

So far we’ve improved a static scene when the camera moves, but what about when objects themselves move? We’ll compare without and with color clamping (left to right respectively).

There’s smearing like before, but now even the inner pixels are affected. Color clamping (right) does its best to fix up the colors but it’s still a jittery mess. Interestingly this can be a common effect in shipped videogames. The image below was captured in a UE4 game, where foliage lacks motion vectors.

This happens because deriving motion only from the camera is not enough, we need to take the object motion into account as well. The typical way to accomplish it is for the vertex shader to compute the position twice, once for the current and once for the previous frame. It passes those to the pixel shader, which computes the difference and outputs that to the velocity texture. For static geometry that doesn’t move or deform, we can keep using only the camera.

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 | // Vertex Shader { // Compute positions in NDC space VS_OUT vsOut; vsOut.previousPosition = ComputePreviousPosition(); vsOut.currentPosition = ComputeCurrentPosition(); } // Pixel Shader { PS_OUT psOut; float2 previousPosition = vsIn.previousPosition.xy / vsIn.previousPosition.w; // Perspective divide float2 currentPosition = vsIn.currentPosition.xy / vsIn.currentPosition.w; // The difference in positions is the velocity float2 velocity = previousPosition - currentPosition; psOut.velocity = velocity * float2(0.5, -0.5) + 0.5; // Put in UV space // Remember to remove the jitters in the space you've uploaded them in (we assume UV space) // We are making it very explicit that there are two jitters here, in practice you can combine them CPU-side psOut.velocity -= currentJitter.xy; psOut.velocity -= previousJitter.xy; } |

Velocity is normally a 2-channel 16-bit floating point texture but it can vary. There are alternatives to computing the position twice, such as keeping a buffer for every vertex with the previous position in. This takes up a lot more memory, 32 bits per vertex in the simplest case, so it would only be recommended if the position computations are very expensive.

**Flicker**

A consequence of adding color clamping is that it may introduce flickering in static images. As a result of aliasing, high intensity subpixels can appear and disappear in alternating frames. The color neighborhood then either clamps or lets them through. Essentially the accumulation process is continuously reset and this appears as flickering. A typical way to fix this is to tonemap the image in an attempt to give less importance to the bright outliers such that the image becomes more stable. There are a few different techniques that I’ve seen.

#### Blend Factor Attenuation

This modifies the blend factor under certain circumstances. UE4 [mentions](https://de45xmedrsdbp.cloudfront.net/Resources/files/TemporalAA_small-59732822.pdf#page=45) they detect when a clamping event is going to happen and reduce the blend factor. This however reintroduces the jitter and has to be done with care.

#### Intensity/Color Weighing

Since the reason for flickering is high variance in consecutive neighborhoods, intensity weighing tries to attenuate pixels whose intensity is high. This stabilizes the image at the cost of specular highlights (they become dimmer, so for something like flickering sand you can boost the intensity or add it after TAA). The demo comes with luminance weighing and I’ve used log weighing in the past, but they are similar. Log weighing converts colors into log space (careful with nans!) before doing any linear operations, which biases towards low intensity values. Here’s a short comparison and pseudocode.

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 | // Store weight in w component float4 AdjustHDRColor(float3 color) { if(InverseLuminance) { float luminance = dot(color, float3(0.299, 0.587, 0.114)); float luminanceWeight = 1.0 / (1.0 + luminance); return float4(floatcolor, 1.0) * luminanceWeight; } else if(Log) { return float4(x > 0.0 ? log(x) : -10.0, 1.0); // Guard against nan } } // Read neighborhood and adjust using weights float3 neighborhoodPixel0 = AdjustHDRColor(ReadNeighborhood) // [...] // Read previous color float4 previousColor = AdjustHDRColor(Reproject(uv)); // Read current color float4 currentColor = AdjustHDRColor(CurrentTexture.Sample(uv)); // Do color clamping float3 previousColorClamped = clamp(previousColor, minColor, maxColor); // Blend float currentWeight = 0.1 * currentColor.a; float previousWeight = 0.9 * previousColor.a; float3 output = (currentColor.rgb * currentWeight + previousColorClamped.rgb * previousWeight); output /= (currentWeight + previousWeight); // Normalize back. Note that this has no effect in the log case if(Log) { output = exp(output); // Undo log transformation } |

**Blurring**

A common criticism of Temporal AA is that it looks blurry. This is an issue that I never understood properly when I first started learning about the topic. We can get a crisp result on a static image, but it will blur in movement due to reconstruction errors. To see why, let’s consider the following reprojection image.

A **current** pixel is reprojected to the **previous **frame where it will most likely not land at a pixel center, instead landing somewhere between 4 samples. There is no exact value that corresponds to our position in the previous frame, so which do we take? This is a reconstruction problem. Taking any one sample produces line-like snapping artifacts. Another option is to bilinearly filter the nearest 4 samples, which is effectively a form of blurring. As there’s an accumulation buffer the error from the reconstruction adds up, causing further blurring. Another option is to take higher-order filtering. Although there are a few, the most popular is the Catmull-Rom filter, computed below as a generalized bicubic when B = 0 and C = 0.5.

This bicubic filter has negative lobes (i.e. introduces a high-pass component) that produces sharper images. Move the slider C to alter the “sharpness”. The standard Catmull-Rom is 16 texture reads that can be optimized to 9 samples by exploiting bilinear filtering. This is used by UE4. Jorge Jiménez further optimized it by discarding the corner samples down to 5 reads for [Call of Duty](https://research.activision.com/publications/archives/filmic-smaasharp-morphological-and-temporal-antialiasing). Here’s a comparison between bilinear and Catmull-Rom when the arm moves towards the camera.

![Before image](../../assets/6c645747f7140658.png)

![After image](../../assets/f59df9f66a3c108a.png)

- One extra possibility to further increase the apparent crispness of the image is to apply a sharpening pass after TAA. Some algorithms like AMD’s FidelityFX already do this during the upscaling pass
- An interesting but perhaps more complicated approach is presented in
[Hybrid Reconstruction Anti Aliasing](https://michaldrobot.files.wordpress.com/2014/08/hraa.pptx). It estimates the error introduced by the reconstruction and tries to compensate for it

**Texture Blurring**

Texture blurring is another of TAA’s criticisms. Textures have already been blurred during the mipmapping process and the runtime is tuned to select the appropriate mipmap that will minimize aliasing while keeping details crisp. The jitter in screen space causes further blur in texture space. As far as I know, there are two ways to combat this directly:

- Introduce a negative mip bias. This will force the GPU to sample more detailed mips. Care needs to be taken to not reintroduce the aliasing we worked so hard to remove, and measure the performance impact of sampling at a higher mip now, but it can bring back detail nicely
- Unjitter the texture UVs. The purpose is to keep the UVs the same as when there’s no screen space jitter. I owe this knowledge to
[Martin Sobek](https://twitter.com/MartinSobek13)who introduced me to this cool (and inexpensive!) trick. In practical terms we express the pixel jitter (increment in screen space) in terms of texture coordinates (increment in UV space) via the derivatives:

\Delta u = \Delta x · \dfrac{\partial u}{\partial x} + \Delta y · \dfrac{\partial u}{\partial y} \Delta v = \Delta x · \dfrac{\partial v}{\partial x} + \Delta y · \dfrac{\partial v}{\partial y}

1 2 3 4 5 | float2 UnjitterTextureUV(float2 uv, float2 currentJitterInPixels) { // Note: We negate the y because UV and screen space run in opposite directions return uv - ddx_fine(uv) * currentJitterInPixels.x + ddy_fine(uv) * currentJitterInPixels.y; } |

**Edges**

When reprojecting the current pixel, we need to realize that the velocity texture, unlike the history color buffer, is aliased. If we’re not careful we could be reintroducing edge aliasing indirectly. To better account for the edges, a typical solution is to dilate the aliased information. We’ll use velocity as an example but you can do this with depth and stencil. There are a couple of ways I know of doing it:

**Depth Dilation**: take the velocity that corresponds to the pixel with the nearest depth in a neighborhood**Magnitude Dilation**: take the velocity with the largest magnitude in a neighborhood

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 | float2 GetVelocity(float uv) { if(DilationMode == None) { return CurrentVelocityTexture.Sample(uv); } else if(DilationMode == ClosestDepth) { float closestDepth = 100.0; float2 closestUVOffset = 0.0; for(int j = -1; j <= 1; ++j) { for(int i = -1; i <= 1; ++i) { float2 uvOffset = float2(i, j) / TextureSize; float neighborDepth = Depth.Sample(uv + uvOffset); if(neighborDepth < closestDepth) { closestUVOffset = uvOffset; closestDepth = neighborDepth; } } } return CurrentVelocityTexture.Sample(uv + closestUVOffset); } else { // Similar to closest depth. Read multiple velocities and compare magnitudes } } |

![Before image](../../assets/42744df4cc2745b7.png)

![After image](../../assets/041fc43a68360d90.png)

**Transparency**

Transparency is a tricky problem to solve, as transparent objects don’t generally render to depth. Low resolution effects such as smoke and dust are typically unaffected by Temporal AA and color clamping does its job without too many issues. However, more general transparency like glass, holograms, etc. can be affected and look poorly if not properly reprojected. There are a couple of solutions to this, and your mileage may vary because it’s content-dependent:

- Write blended motion vectors to the velocity buffer. This is content-dependent but it can work. In fact even writing motion vectors as if they were solid can work if the opacity of the object is sufficiently high
- Introduce a per-pixel accumulation factor: This is what UE4 calls “responsive AA”. Essentially it will trade off ghosting for pixel jitter. Useful for very detailed VFX as shown
[here](https://de45xmedrsdbp.cloudfront.net/Resources/files/TemporalAA_small-59732822.pdf#page=38) - Render transparency after TAA. This is not recommended unless maybe you render them into an offscreen buffer, antialias it with an edge-detection solution such as FXAA or SMAA, and composite back. It can jitter at the edges because it’s compared against a jittered depth buffer

**Camera Cuts**

Camera cuts present challenges when using TAA. A camera cut forces us to invalidate the history buffer, as its contents are no longer representative of the currently rendered frame. We therefore cannot rely on the history to produce a nice antialiased image. There are definitely some ways to address this that I will enumerate here.

- Bias the convergence to accelerate the process. After the camera cut we need to accumulate content as fast as possible
- Use fade outs and fade ins. The TAA will accumulate during the black parts and be converged by the time it fades in
- Apply another form of AA or blur for the first frames, so the convergence isn’t as jarring. This is simpler if you already have the technique available

All in all, they’re all hacks at the end of the day, but it needs addressing. The other thing to keep in mind is that the higher your framerate is, the less this is a problem.

**Epilogue**

I hope you enjoyed this large exposition on TAA. I’m sure I’ve left out many things, but hopefully this is a good place to start. If you have any questions or suggestions let me know, and I hope you learned something today.

**Additional Bibliography**

Most links are located where relevant, but here are a few extras. They are either broad or historically significant.

[A Survey of Temporal Antialiasing Techniques](http://behindthepixels.io/assets/files/TemporalAA.pdf): A must read for a holistic description of TAA techniques[Accelerating Real-Time Shading with Reverse Reprojection Caching](https://gfx.cs.princeton.edu/pubs/Nehab_2007_ARS/NehEtAl07.pdf): As far as I know one of the first documented explanations of this technique[Rendering Techniques in Gears of War 2](https://cdn2.unrealengine.com/Resources/files/GDC09_Smedberg_RenderingTechniques-1415210295.pdf): To my knowledge one of the first applications of a temporal technique, on SSAO

A quality article once again! Thanks!

I don’t see a big difference between Luminance and Log weighing, is one actually cheaper?

Good question. All in all they’re both pretty adequate and serve the purpose. The reason I posted both is I came up with log independently and then learned about luminance.

Log weighing uses trascendental functions (log) which are not full rate but there are fewer, whereas luminance weighing has more fullrate math and divisions (which aren’t fullrate either). You’d have to measure. In my experience a TAA resolve pass should generally be bandwidth bound so you might not notice a difference.

The other thing I would do is test on real world content, for my example it may not make a difference but luminance weighing converges to a constant value when you plot it, whereas log keeps growing slowly. Depending on your content/use case one or the other could be more what you want. Check this to see what I mean https://www.desmos.com/calculator/ysha5ojn5g

There is also this recent research, which uses visibility buffers and material IDs for higher quality rejection decisions:

http://filmicworlds.com/blog/visibility-taa-and-upsampling-with-subsample-history/

Hi Richard,

That is indeed a good article, thanks for posting. There are lots of avenues to pursue further for TAA, especially things like upsampling which many engines do already.

I’m not a big fan of MSAA. I’ve measured around a 10% performance hit on geometry passes, and makes the rendering quite a lot more complicated than it is otherwise. It also to some extent prevents alternative rasterization techniques.

Pingback: Randomly generated stuff

Do you have a demo with the source code?

Hi Denis,

I’ve zipped up what I had here in Dropbox. The code isn’t cleaned up or made to follow the tutorial, but hopefully it’s useful and you can have a play around with it.

https://www.dropbox.com/s/0aicxmw27ew5ytk/TemporalAA.zip?dl=0

Thanks a lot!

Detecting the disocclusion based on velocity and prev velocity should not work for a static camera. Because (if you let’s say moved a sphere in front of the camera) for a disoccluded pixel previously located behind the sphere current velocity is zero and the previous velocity is zero because the current is zero.

Hi Fox,

Thanks for your message. What you say is true for that specific case. In general though, most objects don’t have behave like that unless you’re teleporting them or something specific.

For cases where the velocity-based disocclusion fails, color clamping kicks in and does the job in the same way it used to. Bear in mind these methods aren’t exclusive. You can use any of them together, and they can inform each other as well (i.e. make decisions in one method based on what the other method did)

Pingback: Unheard Engine: 2 months Journey of Vulkan Learning – The Graphic Guy Squall

Think UnjitterTextureUV must have a typo because it takes uv as a float instead of float2. I’ve also not found it to work terribly well in my tests, at least, nowhere near as well as a bias.

Hi ET,

It had a typo indeed, fixed it now. What issues are you seeing? The bias certainly can have a dramatic effect depending on your content.

This article is exceptional, outstanding and amazing! Best TAA article ever.

Really appreciated Vincent, thanks

I really hate TAA tbh, and I hate the fact that games are forcing it to be on to find artifacts lazy developers use.

The ONLY good TAA I’ve ever seen was in Death Stranding here: https://advances.realtimerendering.com/s2017/DecimaSiggraph2017.pdf page 28

No ghosting, smearing or excessive blur.

Hi Kevin, thanks for your comment. As a lazy developer I appreciate that it’s not to everyone’s liking. Unfortunately, the lazy GPUs we get given to work on are very slow and lazy, so we come up with lazy techniques to compensate and try to get nice visuals.

On a serious note, that TAA in particular doesn’t have an accumulation buffer like most TAA implementations. Therefore it is more responsive, at the cost of aliasing and stability. It’s the reason it gets combined with FXAA as well. The Guerrilla guys are very talented and they went with this implementation for that game.

I also dislike ghosting. Some TAA implementations are better than others, just like some implementations of FXAA/SMAA are better. However I also dislike jagged triangles, fizzy foliage and unstable specular. It’s a tradeoff. Like we say in Spain, it doesn’t rain to everyone’s liking. Just grab an umbrella and enjoy the weather.

Thanks for the article! Could you clarify what filtering you’re using to sample the current and history textures? i.e. linear, nearest-neighbor etc.

Additionally, at a blending value of 0.1 I feel that the image quality I get in a static scene is much blurrier than what you have in the 2nd image. Would this indicate some issue with how my jitter is being applied?

Hi Patrick, thank you for the comment!

The history texture is resampled via a bicubic filter as explained in the Blurring section,

“The standard Catmull-Rom is 16 texture reads that can be optimized to 9 samples by exploiting bilinear filtering. This is used by UE4. Jorge Jiménez further optimized it by discarding the corner samples down to 5 reads for Call of Duty. Here’s a comparison between bilinear and Catmull-Rom when the arm moves towards the camera.”

So essentially the canonical way is to sample 16 times around the reprojected position and weigh each sample with the bicubic filter, the other versions are optimizations of top of that. Maybe I could add code to this section, I’ll make a note to do that later.

As for the current pixel, I’ve always taken it as is with no filtering, unless there is disocclusion, in which case I take a blurred sample to hide it a bit. Consider the current pixel as a participant of a much larger set of pixels that you’re filtering. You may consider weighing it according to its distance from the pixel center as is explained in the UE4 presentation

A common problem with jitter blurring is when your jitter produces samples outside of the current pixel. All the jitter needs to do is wobble with a maximum with of 0.5/width and 0.5/height so that it stays within the target pixel. That would be unrelated to the 0.1 factor as that only deals with how fast you want your image to converge. Let me know if anything is unclear.

Great article, thanks!

I was wondering if the “texture double blur” problem can be addressed, instead of by “unjttering” the UVs, simply by disabling the bilinear texture interpolations in the first pass, and letting the TAA do its work.

I understand that bilinear (without TAA) does the job better than TAA (without bilinear), but if TAA is used anyway, the latter might be preferable, maybe?

(Of course, you’d keep MIP-mapping and linear interpolation between MIP-map levels.)

I also understand thay both bilinear interpolations and UV “unjittering” are cheap, but it’s tempting to address a problem by throwing _fewer_ resources at it, rather than more.

(Also, in theory bilinear texel interpolation is not actually the right thing to do anyway — with textures other than diffuse maps, e.g. with normal maps or shininess maps, so it’s a small bonus to get rid of it.)

Ciao Marco,

Thank you for your kind words and comments.

Removing the bilinear filtering is not equivalent to unjittering the UV coordinates. The idea behind unjittering is to preserve the original bilinear filter without adding an additional blurring on top.

That said, there seems to be some traction behind stochastic filtering of textures (https://research.nvidia.com/labs/rtr/publication/pharr2024stochtex/stochtex-slides.pdf) so of course you could do your own filtering by using point filtering and randomly choosing the UV within the mipmap based on derivatives or distance or whatever metric you come up with and let TAA do its thing. That might introduce noise and flickering and perhaps some performance differences as you’ll want to access higher mipmaps in order to capture the detail, but it’s an interesting avenue for sure. It also means more ALU to compute the UV, etc so again it’s not as clear cut. I’ve never tried it, let me know if you come up with interesting results!

Pingback: TAA, Temporal Anti-Aliasing, 템포럴 앤티 앨리어싱 – hongildong

Very nice! I learned a lot from your blog. I’m a Indie game developer from China,writing my blog about TAA,too.Since I don’t have the time to develop my own renderer and implement these algorithms, in order to present this knowledge better, I would like to be able to cite the GIFs from your article in the blogs I post. I will write your name in detail with a link to this blog. Is it possible for me to do so?(This comment uses machine translation)

Hi Loturias,

I’m glad you like the article. As long as you cite it as the original source for the images, feel free to copy them around or use them for yours as much as you like.

Thanks!

Are you ok if the image showing the color-clamping square (https://www.elopezr.com/wp-content/uploads/2021/11/TAA-Color-Neighborhood.png), was used in the updated docs for Babylon.js TAA? (https://doc.babylonjs.com/features/featuresDeepDive/postProcesses/TAARenderingPipeline)

It will be attributed to you and linked back to this article of course.

Hi Jasmine,

Yeah not a problem, many thanks for asking. Feel free to use any of the original images in the post

This is a very good article. I learned a lot, but I still have a question: since TAA essentially reduces aliasing by blending the current frame and historical frames through dithering, it inevitably causes a slight jitter in the image. However, I hardly notice this jitter in some games that use TAA as anti-aliasing. Why is that?

Hi Kallka,

I’m glad you enjoyed it. The reason the jitter is mostly imperceptible is that the contribution of the current pixel is generally quite low, 10% or less, and we fight fireflies aggressively through the use of luminance filters as shown in the article. The other thing that makes this relatively stable is that most pixels in the vicinity are close in color space. In high contrast scenarios the jitter can be quite apparent (alpha testing can be really problematic with TAA). Our eyes mostly do the rest. However that doesn’t mean it doesn’t flicker, you can see in the animated images of the article that it does indeed wobble about when we enlarge the pixels on screen