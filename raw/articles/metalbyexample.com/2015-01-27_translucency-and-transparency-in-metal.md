---
title: Translucency and Transparency in Metal
url: https://metalbyexample.com/translucency-and-transparency/
published: '2015-01-27'
source_blog: Metal by Example
source_site: https://metalbyexample.com
category: graphics
fetched: '2026-04-13'
---

## Introduction

One of the topics we’ve handily avoided so far in our exploration of Metal is rendering of materials that are not opaque. In this post, we’ll explore a couple of related techniques for achieving transparency and translucency: alpha testing and alpha blending.

The sample scene for this post is a desert containing many palm trees and a few pools of water. The leaves of the palm trees consist of a few polygons each, textured with a partially-transparent texture, and the water is rendered as a translucent surface via alpha blending, which we’ll discuss in detail below.

![The sample application from this article demonstrates alpha testing and alpha blending](../../assets/f454747e4c9ee47e.png)


![The sample application from this article demonstrates alpha testing and alpha blending](../../assets/f454747e4c9ee47e.png)


## What is Alpha, Anyway?

Alpha is used to represent the *opacity* (or *coverage*) of a color value. The higher the alpha value, the more opaque the color. When speaking in terms of fragment color, the alpha component indicates how much the scene behind the fragment shows through.

An excellent [paper by Andrew Glassner](http://www.imaginary-institute.com/resources/TechNote10/TechNote10.html) details the complementarity of opacity and coverage to a much greater extent than I can write about it here.

## Alpha Testing

The first technique we’ll use to render partially-transparent surfaces is *alpha testing*.

Alpha testing allows us to determine whether a fragment should contribute to the renderbuffer, by comparing its opacity against a threshold (called the *reference value*). Alpha testing is used to make surfaces *selectively* transparent.

One common application of alpha testing is the rendering of foliage, where relatively few polygons can be used to describe the shape of leaves, and the alpha channel of the leaf texture can be used to determine which pixels are drawn which are not.

![Alpha testing allows us to draw partially-transparent palm fronds](../../assets/164f820326701995.png)


![Alpha testing allows us to draw partially-transparent palm fronds](../../assets/164f820326701995.png)

## Alpha Testing in Metal

Alpha testing in Metal is implemented in the fragment function. The shader file contains a global reference value (0.5 in the sample app), against which our alpha values will be compared. The fragment function samples the diffuse texture of the palm tree, which has an alpha value of 0 for the texels that should be transparent. The sampled color is then used to decide whether the fragment should be visible, described in the sections that follow.

### The ‘discard_fragment’ function

In order to indicate to Metal that we don’t want to provide a color for a fragment, we cannot simply set the returned alpha value to 0. If we did, the fragment depth would still be written into the depth buffer, causing any geometry behind the “transparent” point to be obscured.

Instead, we need to call a special function that avoids specifying a color value for the fragment entirely: `discard_fragment`

. Calling this function prevents Metal from writing the computed depth and color values of the fragment into the renderbuffer, which allows the scene behind the fragment to show through.

### The Texture Alpha Channel

To perform the per-fragment alpha test, we need a specially-constructed texture that contains suitable coverage information in its alpha channel. The figure below shows the palm leaf texture used in the sample app.

![The texture used to draw the palm fronds in the sample app.](../../assets/d7791baf2a735db6.png)


![The texture used to draw the palm fronds in the sample app.](../../assets/d7791baf2a735db6.png)

### Performing the Alpha Test

The implementation of alpha testing in the fragment shader is very straightforward. Bringing together the techniques we just discussed, we test the sampled alpha value against the threshold, and discard any fragments that fail the alpha test:

float4 textureColor = texture.sample(texSampler, vert.texCoords); if (textureColor.a < kAlphaTestReferenceValue) discard_fragment();

### A Note on Performance (Optional)

Using `discard_fragment`

has performance implications. In particular, it prevents the hardware from performing an optimization called *early depth test* (sometimes called *early-z*).

Oftentimes, the hardware can determine whether a fragment will contribute to the renderbuffer before calling the fragment function, since fragment depth is computed in the rasterizer. This means that it can avoid shading blocks of fragments that are known to be obscured by other geometry.

On the other hand, if a fragment is going to be shaded with a function that contains conditional `discard_fragment`

calls, this optimization cannot be applied, and the hardware must invoke the shader for every potentially-visible fragment.

In the sample code for this post, we have separate fragment functions for geometry that is rendered with the alpha test and without. The alpha testing function should only be used on geometry that actually needs it, as overuse of `discard_fragment`

can have a strongly negative performance impact.

A full explanation of early depth-testing is well beyond the scope of this post, but you can read [Fabien Giesen’s fantastic blog post on the subject](https://fgiesen.wordpress.com/2011/07/08/a-trip-through-the-graphics-pipeline-2011-part-7/) for all of the details.

## Alpha Blending

Another useful technique for implementing transparency is *alpha blending*.

Alpha blending is achieved by interpolating between the color already in the renderbuffer (the destination) and the fragment currently being shaded (the source). The exact formula used depends on the desired effect, but in this article we will use the following equation:

![Rendered by QuickLaTeX.com c_f = \alpha_s \times c_s + (1 - \alpha_s) \times c_d](../../assets/51d209bb15801fd8.png)


where ![Rendered by QuickLaTeX.com c_s](../../assets/af66e6db50fad9e1.png)

![Rendered by QuickLaTeX.com c_d](../../assets/da108c4658529686.png)

![Rendered by QuickLaTeX.com \alpha_s](../../assets/a10cfe97a1a66125.png)

![Rendered by QuickLaTeX.com c_f](../../assets/4ccdf9f96f722896.png)


Expressed in words: we multiply the source color’s opacity by the source color’s RGB components, producing the contribution of the fragment to the final color. This is added to the additive inverse of the opacity multiplied by the color already in the renderbuffer. This “blends” the two colors to create the new color that is written to the renderbuffer.

## Alpha Blending in Metal

In the sample project for this article, we use alpha blending to make the surface of the water translucent. This effect is computationally cheap, and it can be enhanced by with partial reflection and an animation that slides the texture over the water surface or physically displaces it.

### Enabling Blending in the Pipeline State

There are at least two ways of achieving blending in Metal: fixed-function and programmable. We will discuss fixed-function blending in this section. Fixed-function blending consists of setting properties on the color attachment descriptor of the render pipeline descriptor. These properties determine how the color returned by the fragment function is combined with the pixel’s existing color to produce the final color.

To make the next several steps more concise, we save a reference to the color attachment:

MTLRenderPipelineColorAttachmentDescriptor *renderbufferAttachment = pipelineDescriptor.colorAttachments[0];

To enable blending, set `blendingEnabled`

to `YES`

:

renderbufferAttachment.blendingEnabled = YES;

Next, we select the operation that is used to combine the weighted color and alpha components. Here, we choose `Add`

:

renderbufferAttachment.rgbBlendOperation = MTLBlendOperationAdd; renderbufferAttachment.alphaBlendOperation = MTLBlendOperationAdd;

Now we need to specify the weighting factors for the source color and alpha. We select the `SourceAlpha`

factor, to match with the formula given above.

renderbufferAttachment.sourceRGBBlendFactor = MTLBlendFactorSourceAlpha; renderbufferAttachment.sourceAlphaBlendFactor = MTLBlendFactorSourceAlpha;

Finally, we choose the weighting factors for the destination color and alpha. These are the additive inverse of the factors for the source color, `OneMinusSourceAlpha`

:

renderbufferAttachment.destinationRGBBlendFactor = MTLBlendFactorOneMinusSourceAlpha; renderbufferAttachment.destinationAlphaBlendFactor = MTLBlendFactorOneMinusSourceAlpha;

### The Alpha Blending Fragment Shader

The fragment shader is responsible for returning a suitable alpha value for blending. This value is then used as the “source” alpha value in the blending equation configured on the rendering pipeline state.

In the sample code, we multiply the sampled diffuse texture color with the current vertex color to get a source color for the fragment. Since the texture is opaque, the vertex color’s alpha component becomes the opacity of the water. Passing this value as the alpha of the fragment color’s return value produces alpha blending according to how the color attachment was previously configured.

![Alpha blending allows the sandy desert show through the clear water surface](../../assets/4c957b9903f21c5b.png)


![Alpha blending allows the sandy desert show through the clear water surface](../../assets/4c957b9903f21c5b.png)

### Order-Dependent Blending versus Order-Independent Blending

When rendering translucent surfaces, order matters. In order for alpha blending to produce a correct image, translucent objects should be rendered after all opaque objects. Additionally, they should be drawn from back to front (in decreasing order from the camera). Since order is dependent on the view position and orientation, objects need to be re-sorted every time their relative order changes, often whenever the camera moves.

We avoid this problem entirely in the sample app by having only a single, convex, translucent surface in the scene: the water. Other applications won’t have it so easy.

There has been much research in the last several years on ways to avoid this expensive sorting step. One technique uses a so-called *A-buffer* to maintain a pair of color and depth values for the fragments that contribute to each pixel. These fragments are then sorted and blended in a second pass.

More recently, research has placed an emphasis on the mathematics of alpha compositing itself, in an attempt to derive an *order-independent transparency* solution. Refer to [McGuire and Bavoil’s recent paper](http://jcgt.org/published/0002/02/09/) for the full details on this technique.

## Conclusion

In this article, we have seen two ways of rendering non-opaque materials: alpha testing and alpha blending. These two techniques can be used side-by-side to add extra realism to your virtual scenes.

GaryBlending is programmable, in the same fashion of gl_LastFragData for OpenGL es for iOS, the fragment shader can take in the destination colour of the currently attached render target, its an input to the fragment shader with the [[ color[0]] attribute. See page 55 of the metal shading language guide.

Jessy CatterwaulI just got confirmation from Apple (http://apple.co/1SjjaMn) that this is actually what the compiler is using, instead of actual blending hardware. I wonder if they added “blending” to the API because they knew that they were going to bring Metal to non-embedded GPUs this year. My current prediction is that we’ll see Metal only on integrated GPUs, next month, and that Tuesday’s refresh represents the last discrete GPUs ever, in an Apple notebook.

JessyThe < is rendering as < That really confused me until I downloaded the sample code and realized that it was a text rendering problem.

Warren MooreThanks for catching that! I think it’s a bug in the interaction between WordPress Jetpack and SyntaxHighlighter. I re-applied my patch after upgrading SyntaxHighlighter and it seems to be rendering correctly again. Look okay from your side?

JessyYes, it’s fixed! However, my comment renders the same < twice, which makes me look insane. Oh well.

Warren MooreI have changed history to make you appear less insane 😉

JakeHello! I’m a big fan of your articles and have been finding them very useful in getting started working on a sketching/drawing engine, but I’ve hit a roadblock. In my pipelineState, I’m matching all of your settings of rgb/alhpa blend operations and factors (Add, SourceAlpha, and OneMinusSourceAlpha), but my quads are always rendered with black behind its smooth alphas.

Here you can see my brush textures are being rendered with black backgrounds, making them seem much darker than they should.

http://imgur.com/a/48F1T

I was wondering if you ran into this problem before (something similar happens when erasing some of your water texture with a smooth eraser in photoshop and setting its mesh opacity to 1, which I included in that album). I’m running out of leads and am starting to get desperate.

If it matters, I’m writing my code in Swift and would by happy to show it if needed.

Warren MooreHappy to take a look at the code (wm@warrenmoore.net). Most particularly, I’m curious how you’re computing the color you return from your fragment shader.

Warren MooreSince you’re loading your textures with CoreGraphics, you’re getting premultiplied alpha (i.e., the color channels are already multiplied by their respective alpha values). The consequence of using premultiplied alpha with the SourceAlpha, OneMinusSourceAlpha blend factors is that the source alpha value is redundantly multiplied, causing areas with a < 1.0 to become unnaturally dark. If instead you use the One, OneMinusSourceAlpha blend factors, you get a much more pleasing result. Incidentally, this is the main reason I used an opaque texture and translucent vertex colors when demonstrating blending in the article.

JakeThanks so much for the tips! It really means a lot.

Instead of dealing with Core Graphics premultiplying my alphas, I decided that I should just use an alpha mask since I don’t even need texture colors. This results in everything working correctly with SourceAlpha, OneMinusSourceAlpha!

http://i.imgur.com/5IwjP8S.png

Shader code:



fragment half4 alpha_mask_fragment(VertexOut interpolated [[stage_in]],

texture2d texture [[texture(0)]],

sampler sampler2D [[sampler(0)]]) {

float4 sampled = texture.sample(sampler2D, interpolated.texCoord);

return half4(interpolated.color.r,


interpolated.color.g,

interpolated.color.b,

interpolated.color.a * sampled.r);

}

Thanks again!

Warren MooreOutstanding! Happy to help.

JessyDo you you can use half4(interpolated.color.rgb, interpolated.color.a * sampled.r)? As long as you “fill up” the vector, you can use swizzles instead of scalars.

JakeNeat tip! Thanks for the heads up. I’m still pretty new to programming shaders.

Eric MillerHi, I’m enjoying your book and site and it is really helping me with metal. I have a question on the design decisions. In the InstancedDrawing example you use separate buffers for the shared, terrain and cow uniforms. In this example all are placed in a single buffer you use offsets to the various uniforms. Why did you choose one style over the other? What criteria do you use to determine how the data is structured? Are there and specific advantages or disadvantages? Thanks for the work you’ve done.

Eric

Warren MooreI’m not sure I was consistent on this, so I’d rather discuss the principles rather than the particular choices I made when writing these articles originally.

The chief advantage to using separate buffers is that you can separate concerns, for example by having objects store their own uniform buffers, rather than store their offsets into some shared buffer to which every object is coupled. Taken to the extreme, though, this means you make a lot of small allocations, which is wasteful.

The chief advantage of using a single buffer is that you might get better locality of reference if objects are drawn in the same order their varying properties are laid out in the buffer. In this case, you make one large, page-aligned allocation instead of allocating a lot of small buffers separately. Given the choice, this is the option I always choose these days. (Allocating page-aligned allows you to avoid an extra copy when creating the buffer, if you use the

`NoCopy`

variant of`-newBuffer...`

).One thing that I didn’t really harp on enough in either of these articles is avoiding writing into memory from the CPU when it is being used by the GPU. For consistent results using a single global buffer, it really is quite important to segment your buffers into chunks and write into one chunk while the GPU is consuming the previous frame’s chunk. This is even more important when using Metal on OS X, where managed buffers have separate backing stores in CPU and GPU memory, requiring explicit synchronization.

JessyThanks, Warren. Do you have a good resource on page alignment? It’s not something I’ve come across yet.

Warren MooreWithout writing a full treatise on virtual memory, it works roughly like this. Every process on a system “sees” an address space that covers (almost) all of the physical memory of the system. At any given time, though, it probably only needs to have a fraction of this memory full (“resident”). The OS and the CPU work together to cycle chunks of data into and out of memory, translating between the addresses seen by the process and the addresses corresponding to the bits in physical RAM. Because of the overhead in mapping from the virtual space to the physical space, the virtual memory address space is broken up into “pages” (which are usually 4kB or 16kB in size), the smallest unit of virtual memory that can be made resident or evicted from residency. iOS is different from OS X in the sense that iOS doesn’t write evicted pages to disk, so they can never be recovered (this is why you take low memory warnings seriously on iOS, and why it has no recourse but force-quit apps that consume a lot of memory when not in the foreground)(note that there are higher-level systems than virtual memory that *do* store some app state to disk when apps become inactive, but that’s a separate discussion).

Sitting between virtual memory and your application,

`malloc`

incorporates extra bookkeeping to efficiently make allocations that are smaller than one page (these are usually aligned to 16 bytes, which is way more granular than iOS’s page size of 16kB). When you’re making larger allocations, though, you can jump straight to allocating entire pages for yourself (with`posix_memalign`

or`vm_allocate`

). These functions do “page-aligned” allocations, meaning that the address you get back is a multiple of the virtual page size (`getpagesize()`

) These page-aligned allocations are the only ones that Metal can safely use to back a buffer without doing its own copy. That’s what I was referring to in the above comment.YanThere are at least two ways of achieving blending in Metal: fixed-function and programmable….

What’s the second way?

Thanks

Warren MooreProgrammable blending entails reading the current color from the frame buffer and combining it with the color of the fragment currently being processed. In Metal on iOS, the existing color can be obtained by adding a parameter attributed with

`[[color(0)]]`

to your fragment function, or adding a member with this attribute to the`[[stage_in]]`

structure received by your fragment function. The deferred lighting sample from Apple uses this technique extensively to perform additive blending.David HIs programmable blending place more stress or overhead on the GPU than fixed-function? Should we try to use fixed function if at all possible?

Warren MooreYou should use fixed-function blending when possible because there’s no need to write or maintain code that reimplements the existing blend operations. You’d have to be doing something rather exotic to require programmable blending. On platforms that support framebuffer fetch (iOS and Apple Silicon), even fixed-function blending is implemented in terms of programmable blending as a shader post-amble, but that’s an implementation detail.