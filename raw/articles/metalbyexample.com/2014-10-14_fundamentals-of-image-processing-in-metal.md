---
title: Fundamentals of Image Processing in Metal
url: https://metalbyexample.com/fundamentals-of-image-processing/
published: '2014-10-14'
source_blog: Metal by Example
source_site: https://metalbyexample.com
category: graphics
fetched: '2026-04-13'
---

In this post, we will start exploring the world of image processing with the Metal shading language. We will create a framework capable of representing chains of image filters, then write a pair of image filters that will allow us to adjust the saturation and blur of an image. The end result will be an interactive app that allows you to control the image filter parameters in real-time.

This post is designed to be read after its companion article, [Introduction to Compute Programming](http://metalbyexample.com/introduction-to-compute/).

![The sample application UI, allowing filter adjustment in real-time.](../../assets/8164584bdc381d2f.png)


![The sample application UI, allowing filter adjustment in real-time.](../../assets/8164584bdc381d2f.png)

You can [download the sample project here](http://metalbyexample.com/wp-content/uploads/ImageProcessing.zip).


## A Look Ahead

To motivate this post a little further, here is a snippet from the sample project. It illustrates how to succinctly create and chain together the desaturation and blur filters controlled by the UI above.

context = [MBEContext newContext]; imageProvider = [MBEMainBundleTextureProvider textureProviderWithImageNamed:@"mandrill" context:context]; desaturateFilter = [MBESaturationAdjustmentFilter filterWithSaturationFactor:0.75 context:context]; desaturateFilter.provider = imageProvider; blurFilter = [MBEGaussianBlur2DFilter filterWithRadius:0.0 context:context]; blurFilter.provider = desaturateFilter; imageView.image = [UIImage imageWithMTLTexture:blurFilter.texture];

## A Framework for Image Processing

Before we talk about how to implement particular kinds of image filters, it will help to have a flexible framework for executing compute shaders. Each filter will the have the ability to configure its compute pipeline with its input and output textures and execute its kernel function.

### Texture Providers and Consumers

Since we will be operating on images in the form of textures, we need an abstract way to refer to objects that produce and consume textures. Filters, for example, consume *and* produce textures, and we will also need a class for generating textures from images in the application bundle.

We abstract the idea of texture production with a protocol named `MBETextureProvider`

:

@protocol MBETextureProvider <NSObject> @property (nonatomic, readonly) id<MTLTexture> texture; @end

This simple interface gives us a way to (synchronously) request a texture from a texture provider. It might cause an image filter to perform its filtering procedure, or load an image from disk. The important point is that we know we can retrieve a texture from any object that conforms to `MBETextureProvider`

.

On the other hand, the `MBETextureConsumer`

protocol allows us to tell an object which texture provider it should consume textures from:

@protocol MBETextureConsumer <NSObject> @property (nonatomic, strong) id<MBETextureProvider> provider; @end

When a texture consumer wants to operate on a texture, it requests the texture from its provider and operates on it.

### An Image Filter Base Class

Abstractly, an image filter transforms one texture into another by performing an arbitrary operation on it. Our `MBEImageFilter`

class does much of the work necessary to invoke a compute shader to produce one texture from another.

The image filter base class conforms to the texture provider and texture consumer protocols just discussed. This allows us to chain filters together to perform multiple operations in sequence. Because of the synchronous nature of the command queue managed by the image context, it is guaranteed that each filter completes its work before its successor is allowed to execute.

Here is the relevant portion of the `MBEImageFilter`

class’ interface:

@interface MBEImageFilter : NSObject <MBETextureProvider, MBETextureConsumer> @property (nonatomic, strong) MBEContext *context; @property (nonatomic, strong) id<MTLComputePipelineState> pipeline; @property (nonatomic, strong) id<MTLTexture> internalTexture; @property (nonatomic, assign, getter=isDirty) BOOL dirty; - (instancetype)initWithFunctionName:(NSString *)functionName context:(MBEContext *)context; - (void)configureArgumentTableWithCommandEncoder:(id<MTLComputeCommandEncoder>)commandEncoder;

The filter must be instantiated with a function name and a context. These are used to create a compute pipeline state, which is then stored in the `pipeline`

property.

The image filter maintains an internal texture that it uses as the output texture of its kernel function. This is so it can store the result of its computation and provide it to other filters. It can also be drawn to the screen or converted to an image.

Image filters may have any number of parameters that affect how they carry out their computation. When one of them changes, the internal texture is invalidated and the kernel function must be re-executed. The `dirty`

flag allows filter subclasses to indicate when this is necessary. A filter will only be executed when its `dirty`

flag is set to `YES`

, which is done inside custom property setters.

The image filter base class contains an `-applyFilter`

method that is invoked when it is asked to provide its output texture and it is currently dirty. This method creates a command buffer and command encoder, and dispatches its kernel function as discussed in the previous sections.

Now that we have the necessary machinery in place, let’s talk about a couple of example filters that will put it to use.

## Building a Saturation Adjustment Filter

The first filter we will build is a saturation adjustment filter. The filter will have a configurable saturation factor that determines how much the filter should desaturate the input image. This factor can range from 0 to 1. When the saturation factor is 0, the output image will be a grayscale version of the input. For values between 0 and 1, the filter will produce an image in which the colors are more or less muted, by interpolating between the grayscale image and the input image.

![A sequence of images showing how increasing the saturation factor of the filter from 0 to 1 increases image saturation](../../assets/ae4469fed6fc8487.png)


![A sequence of images showing how increasing the saturation factor of the filter from 0 to 1 increases image saturation](../../assets/ae4469fed6fc8487.png)

### Calculating Brightness from RGB

Every RGB color value has a corresponding brightness value, which we will represent by the symbol ![Rendered by QuickLaTeX.com Y'](../../assets/bfde26e278b48824.png)


![Rendered by QuickLaTeX.com Y' = 0.299 R + 0.587 G + 0.114 B](../../assets/5543bd385075d5a9.png)


Note that the factors in the formula sum to 1. Their values are based on human perception of the intensity of different primary colors of light: the human eye is most sensitive to green light, followed by red light, and finally blue light. (These values are published as part of [ITU-R Recommendation BT.601-7](http://www.itu.int/rec/R-REC-BT.601-7-201103-I/en), section 2.5.1, if you care to read all the details.)

Replacing each color in an image with a gray pixel of its corresponding brightness results in a completely desaturated image that has the same perceptual brightness as the original image. This will be the task of our desaturation kernel function, which is presented below.

### The Shader

To support passing the saturation factor to our kernel function, we create a single-membered struct called `AdjustSaturationUniforms`

:

struct AdjustSaturationUniforms { float saturationFactor; };

The kernel function itself takes an input texture, an output texture, a reference to the uniform struct, and a 2D vector of integers with an attribute we haven’t seen before: `thread_position_in_grid`

.

Recall from the previous article that we dispatch a two-dimensional set of threadgroups whose size is calculated from the dimensions of the source texture. The `thread_position_in_grid`

attribute tells Metal to generate a coordinate vector that tells us where we are in the 2D grid that spans the entire dispatched set of work items, i.e. our current coordinates in the source texture.

We specify the intended access pattern for each texture parameter: `access::read`

for the input texture, and `access::write`

for the output texture. This restricts the set of functions we can call on these parameters.

kernel void adjust_saturation(texture2d<float, access::read> inTexture [[texture(0)]], texture2d<float, access::write> outTexture [[texture(1)]], constant AdjustSaturationUniforms &uniforms [[buffer(0)]], uint2 gid [[thread_position_in_grid]]) { float4 inColor = inTexture.read(gid); float value = dot(inColor.rgb, float3(0.299, 0.587, 0.114)); float4 grayColor(value, value, value, 1.0); float4 outColor = mix(grayColor, inColor, uniforms.saturationFactor); outTexture.write(outColor, gid); }

We read the source texel’s color and calculate its brightness value based on the formula presented earlier. The `dot`

function allows us to do this more succinctly than doing the three multiplications and two additions separately. We then generate a new color by duplicating the brightness into the RGB components, which makes a shade of gray.

To calculate the partially-desaturated output color, we use a function from the Metal standard library: `mix`

, which takes two colors and a factor between 0 and 1. If the factor is 0, the first color is returned, and if it is 1, the second color is returned. In between, it blends them together using linear interpolation.

Finally, we write the resulting desaturated color into the output texture.

### The Saturation Adjustment Class

In order to drive the saturation adjustment kernel, we need to extend the image filter base class. This subclass is named `MBESaturationAdjustmentFilter`

:

@interface MBESaturationAdjustmentFilter : MBEImageFilter @property (nonatomic, assign) float saturationFactor; + (instancetype)filterWithSaturationFactor:(float)saturation context:(MBEContext *)context; @end

Setting the `saturationFactor`

property causes the filter to set its `dirty`

property, which causes the desaturated image to be re-computed lazily when its `texture`

property is requested.

The subclass’ implementation of `-configureArgumentTableWithCommandEncoder:`

consists of boilerplate to copy the saturation factor into a Metal buffer. It is not shown here.

With that, we have a complete filter class and kernel function for performing image desaturation.

## Blur

The next type of image filter we will look at is the blur filter.

Blurring an image involves mixing the color of each texel with the colors of adjacent texels. Mathematically, a blur filter is a weighted average of a neighborhood of texels (it is a kind of *convolution*). The size of the neighborhood is called the *radius* of the filter. A small radius will average fewer texels together and produce a less blurry image.

### Box Blur

The simplest kind of blur is a *box blur*. The box blur gives equal weight to all the nearby texels, computing their average. Box blurs are easy to compute, but can produce ugly artifacts, since they give undue weight to noise.

Suppose we choose a box blur of radius 1. Then each texel in the output image will be the average of the input texel and its 8 nearest neighbors. Each of the 9 colors is given an equal weight of 1/9.

![A box blur filter averages the neighborhood around each texel.](../../assets/af859d3f9412c5f4.png)


![A box blur filter averages the neighborhood around each texel.](../../assets/af859d3f9412c5f4.png)

Box blurs are easy, but they don’t produce very satisfying results. Instead, we will use a somewhat more sophisticated blur filter, the Gaussian blur.

### Gaussian Blur

In contrast to the box blur, the Gaussian blur gives unequal weights to the neighboring texels, giving more weight to the texels that are closer, and less weight to those that are farther away. In fact, the weights are computed according to a 2D *normal distribution* about the current texel:

![Rendered by QuickLaTeX.com G_\sigma(x, y) = \frac{1}{\sqrt{2 \pi \sigma^2}} e^{-\frac{x^2 + y^2}{2 \sigma^2}}](../../assets/5fcb25afc4649398.png)


where ![Rendered by QuickLaTeX.com x](../../assets/3b22ee0c7f9feba0.png)

![Rendered by QuickLaTeX.com y](../../assets/c451373bde3e19db.png)

![Rendered by QuickLaTeX.com \sigma](../../assets/664aa5542220b23e.png)


![The Gaussian blur filter. Increasing the filter radius creates a smoother image](../../assets/2c352ab3e425b7a4.png)


![The Gaussian blur filter. Increasing the filter radius creates a smoother image](../../assets/2c352ab3e425b7a4.png)

### The Blur Shader

Computing the blur weights for a Gaussian filter can be expensive, especially for a filter with a large radius. Because of this, we will precompute the table of weights and provide it to the Gaussian blur kernel function as a texture. This texture has a pixel format of `MTLPixelFormatR32Float`

, which is a single channel 32-bit floating-point format. Each texel holds a weight between 0 and 1, and all of the weights sum up to 1.

Inside the kernel function, we iterate over the neighborhood of the current texel, reading each texel and its corresponding weight from the look-up table. We then add the weighted color to an accumulated value. Once we have finished adding up all the weighted color values, we write the final color to the output texture.

kernel void gaussian_blur_2d(texture2d<float, access::read> inTexture [[texture(0)]], texture2d<float, access::write> outTexture [[texture(1)]], texture2d<float, access::read> weights [[texture(2)]], uint2 gid [[thread_position_in_grid]]) { int size = weights.get_width(); int radius = size / 2; float4 accumColor(0, 0, 0, 0); for (int j = 0; j < size; ++j) { for (int i = 0; i < size; ++i) { uint2 kernelIndex(i, j); uint2 textureIndex(gid.x + (i - radius), gid.y + (j - radius)); float4 color = inTexture.read(textureIndex).rgba; float4 weight = weights.read(kernelIndex).rrrr; accumColor += weight * color; } } outTexture.write(float4(accumColor.rgb, 1), gid); }

### The Filter Class

The blur filter class, `MBEGaussianBlur2DFilter`

derives from the image filter base class. Its implementation of `-configureArgumentTableWithCommandEncoder:`

lazily generates the blur weights and sets the look-up table texture on the command encoder as the third parameter (argument table index 2).

- (void)configureArgumentTableWithCommandEncoder:(id<MTLComputeCommandEncoder>)commandEncoder { if (!self.blurWeightTexture) { [self generateBlurWeightTexture]; } [commandEncoder setTexture:self.blurWeightTexture atIndex:2]; }

The `-generateBlurWeightTexture`

method uses the 2D standard distribution formula above to calculate a weight matrix of the appropriate size and copy the values into a Metal texture.

This completes our implementation of the Gaussian blur filter class and shader. Now we just need to revisit how we chain filters together and get the final image to the screen.

## Chaining Image Filters

Now we can revisit the code from the beginning of the post with a new appreciation for how it actually works.

context = [MBEContext newContext]; imageProvider = [MBEMainBundleTextureProvider textureProviderWithImageNamed:@"mandrill" context:context]; desaturateFilter = [MBESaturationAdjustmentFilter filterWithSaturationFactor:0.75 context:context]; desaturateFilter.provider = self.imageProvider; blurFilter = [MBEGaussianBlur2DFilter filterWithRadius:0.0 context:context]; blurFilter.provider = desaturateFilter; imageView.image = [UIImage imageWithMTLTexture:blurFilter.texture];

The main bundle image provider is a utility for loading images into Metal textures and acts as the beginning of the chain. It is set as the texture provider for the desaturate filter, which in turn is set as the texture provider of the blur filter.

Requesting the blur filter’s texture is actually what sets the image filtering process into motion. This causes the blur filter to request the desaturation filter’s texture, which in turn causes the desaturation kernel to be dispatched synchronously. Once it is complete, the blur filter takes the desaturated texture as input and dispatches its own kernel function.

Finally, the blur filter returns its texture, which can then be displayed to the screen.

## Displaying a Filtered Texture

In order to display the filtered texture without copying it back to the CPU, we can draw a quadrilateral with Metal, and use the filtered texture as a texture map. Depending on the desired behavior (maintain the aspect ratio while filling the view, maintain the aspect ratio while ensuring the entire image remains visible, stretch the result to fill the screen disregarding aspect ratio, etc.), we need to compute a different set of vertices or a different set of texture coordinates. The sample code shows how to account for these various cases and may make for interesting reading (consult the `MBEImageView`

class).

## Driving Image Processing Asynchronously

Above, I mentioned that the filters dispatch their kernel functions *synchronously*. Since image processing is computationally intensive, we need a way to do the work on a background thread in order to keep the user interface responsive.

Committing a command buffer to a command queue is inherently thread-safe, but controlling other aspects of concurrency are the responsibility of the programmer.

Fortunately, Grand Central Dispatch makes our work easy. Since we will only be invoking image filters in response to user actions on the main thread, we can use a pair of `dispatch_async`

calls to throw our image processing work onto a background thread, asynchronously updating the UI on the main thread when all of the filters are done processing.

We will use a crude mutex in the form of an `atomic`

64-bit integer property on the view controller that increments every time a UI update is requested. If another user event has not occurred by the time the block executes on the background queue, the image filters are allowed to execute, and the UI is refreshed.

- (void)updateImage { ++self.jobIndex; uint64_t currentJobIndex = self.jobIndex; // Grab these values while we're still on the main thread, since we could // conceivably get incomplete values by reading them in the background. float blurRadius = self.blurRadiusSlider.value; float saturation = self.saturationSlider.value; dispatch_async(self.renderingQueue, ^{ if (currentJobIndex != self.jobIndex) return; self.blurFilter.radius = blurRadius; self.desaturateFilter.saturationFactor = saturation; id<MTLTexture> texture = self.blurFilter.texture; dispatch_async(dispatch_get_main_queue(), ^{ self.imageView.texture = texture; }); }); }

## Conclusion

In this post we introduced the basics of parallel computation with Metal and saw a couple of examples of image filters that can run efficiently on the GPU. Future posts will explore other GPGPU ideas. As always, if you have topic suggestions, feel free to leave them in the comments below.

kobyCan this be applied to your previous work? Like the spinning teapot that’s rendered and then has a filter applied to it? Or would it be better to do blur in pixel shader in one pass?

warrenmYou certainly could apply an image filter to a rendered frame; that’s what post-processing effects are. After all, nothing says you have to render directly into a CAMetalDrawable’s texture. You could instead render to an offscreen framebuffer, pass its texture through an image filter, then draw the resulting texture into the drawable’s texture using a full-screen quad.

kobyAre CIFilters too slow for Metal? How can we use all those great filters in Metal? Or do we have to implement them ourselves?

kobyHrm…I added the saturation filter to see if it could be run in realtime. My frame rate dropped from 60 to 12.

Moving the saturation code into the pixel shader maintained 60 fps.

VerletHi Warren. Thank you very much for this very great series of posts. Great examples and very well written!

Just one question: The code for the gaussian_blur_2d kernel starts out by using a variable called “blurKernel”. Where does that come from? Was it supposed to be “weights”?

warrenmYeah, that was totally supposed to be `weights`. Great catch! Fixed above.

SebastianHuHow would I implement histogram creation with Metal?

The basic idea is to feed a bin as device buffer into the kernel with 256 integers for each workgroup, find the index into that buffer by workgroup index and pixel value and increment the bin at that position. In the end for each workgroup the bins are added. But how can I get the workgroup index in the kernel? WWDC session 605 was handling this but obviously the compute API has undergone major changes.

warrenmThe documentation doesn’t make this clear, but the [[threadgroup_position_in_grid]] attribute indicates the position of the currently executing threadgroup as a set of indices between 0 and the threadgroup size in a particular dimension. It’s not exactly analogous to the former work_group_id attribute, but you can calculate that value by combining the threadgroup_position_in_grid value and the threadgroups_per_grid values. I can explain further if needed.

SebastianHuThank you, Warren. That makes sense to me. Indeed, the documentation might need some love. Also the synchronization features and threadgroup memory stuff is just mentioned, not more.

SebastianHuHmm, further explanation would be awesome. Doesn’t seem to work.

Jim WrenholtAll the kernel examples I’m seeing write to a texture created with MTLPixelFormat.BGRA8Unorm.

If I try to create an outputTexture with a different format I keep getting an error “Non-writable texture format”. Is .BGRA8Unorm the only writable format?

Can a kernel function output float values?

Warren MooreAccording to this thread in the developer forums, Metal cannot write to 32-bit float or integer textures, but 16-bit formats should work (as well as various Unorm formats). You can return a float or half value from a compute kernel, which Metal will pack into the appropriate format for the target (e.g., when writing to BGRA8Unorm, a `float4` value will be swizzled and scaled so that its components fall between 0 and 255).

Shannon PotterWhy do you draw the texture back into a graphics context to display inside a UIImage? Doesn’t that just cause unnecessary overhead going from the GPU to the CPU?

Why can’t you just display the texture using Metal, modify it according to your filter kernels, then redisplay the new texture?

I’m kind of a newbie to low-level graphics, but I thought it was possible to do these sorts of tasks (i.e., image processing) “live” by keeping everything living on the GPU to avoid expensive copies back and forth between the CPU and GPU.

iColoramaI’m with Shannon Potter above..why to convert to UIImage?? Please could you rewrite it for the ones learning Metal..

Warren MooreYeah, I agree that’s a huge inefficiency. I’m going to revisit this article and its companion article in the next few weeks. Thanks for bringing my attention back to this.

iColoramaThanks so much! Very much appreciated!

Warren MooreOkay, apparently “a few weeks” means “76 weeks,” but I’ve just updated the article and sample code to draw the filtered texture without taking a round-trip through the CPU. Better late than never?

icoloramaMany, many thanks!!!! Of course it is better than never)) I will take a look at it!

Uli KustererErr… I think you have a weird bug in there. You’re doing ++self.jobIndex. That can’t work, .jobIndex calls the accessor method, minimal change would be ++self->_jobIndex; But prolly better to do self.jobIndex = self.jobIndex +1; Or did they add code to the ++ operator to be aware of accessors?

Uli KustererScratch that, the only correct way seems to be self.jobIndex = self.jobIndex +1; ++self.foo increments self by one (that is 8 bytes if you’re 64 bit), then tries to call an accessor on that invalid pointer.

Uli KustererIgnore that last one. Had the precedence table upside down. Still, unless I missed them adding that to clang, ++ doesn’t work with properties.

Warren MooreIn the Objective-C 2.0 era, Clang evolved some pretty good heuristics around how to handle this case. It actually does the right thing, emitting two calls to

`objc_msgSend`

with an increment in between, as you can see from the disassembly.`adrp x8, #0x100012000`

add x8, x8, #0x268 ; @selector(jobIndex)

stur x0, [x29, #0xfffffff8]

stur x1, [x29, #0xfffffff0]

ldur x0, [x29, #0xfffffff8]

ldr x1, [x8]

mov x8, x0

str x0, [sp, #0x30]

mov x0, x8

bl imp___stubs__objc_msgSend

adrp x8, #0x100012000

add x8, x8, #0x270 ; @selector(setJobIndex:)

add x2, x0, #0x1

ldr x1, [x8]

ldr x8, [sp, #0x30]

mov x0, x8

bl imp___stubs__objc_msgSend

I agree it’s not the clearest way to write that expression, and I’d probably use direct ivar access if I were writing it again. Did something go wrong at runtime that caused you to observe this, or did you just notice it in passing?

WaresoftWhat if you wanted to apply the saturation effect to only the bottom half of the image . How would you modify your texture to do something like this?

Warren MooreThe easiest way to do this would be to check the y value of the thread position in the grid, passing through the pixel value if it’s less than half, and modifying it otherwise.

WaresoftThat makes sense. Is there an alternate method that can be used? Instead of modifying the shader program, can you only apply the saturation filter to portions of the image?

Warren MooreYou could pass a sequence of floats representing a bounding rect (left, top, right, bottom) in a buffer (perhaps using

`setBytes:length:atIndex:`

, since it’s such a small amount of data) and use that as the “region of interest” in the shader.ColinWhy there is a black line at the top of the result texture？

As shown below.（Left：the result texture Right：the original texture）

![2017052397592PastedGraphic.png](http://7xkc7a.com1.z0.glb.clouddn.com/2017052397592PastedGraphic.png)

Warren MooreI suspect what’s happening is that the kernel is reading outside the bounds of the image, which is technically undefined behavior. Most GPUs will return solid black in this case, which will then get convolved with the edge pixels. To avoid this, you can use a sampler to repeat the texture outside its normalized bounds, or crop the result to get rid of the pixels on the edge.

David HoerlYou need this additional statement in ApplyFilter now:

textureDescriptor.usage = (MTLTextureUsageShaderRead | MTLTextureUsageShaderWrite);

Warren MooreRight; this code was written before the introduction of usage modes in Metal, and the fact that iOS 9 introduced this property with a default value of

`MTLTextureUsageShaderRead`

broke code that assumed textures to be writeable by default.Slipp Douglas ThompsonPro Tip: Three runs of a box blur can produce results with low artifacts nearly indistinguishable from a gaussian blur, but much more efficiently (the math is simpler). It depends on your pipeline setup, of course, since it’s dependent on being able to read values back out from the previous pass quickly.

This trick is fairly common in computer vision implementations, where even-distribution blurs are needed (such as for finding edges), and GPU performance is at an absolute premium.

Philip GThanks, that was a very helpful guide!

While adapting some of the code, I ran into trouble on the bottom+right edges with images whose sizes which weren’t divisible by 8.

Changing

`MTLSize threadgroups = MTLSizeMake(`

[inputTexture width] / threadgroupCounts.width,

[inputTexture height] / threadgroupCounts.height,

1);

to

`MTLSize thread_groups = MTLSizeMake(`

(input_texture.width + thread_group_counts.width - 1) / thread_group_counts.width,

(input_texture.height + thread_group_counts.height - 1) / thread_group_counts.height,

1);

in MBEImageFilter.m fixed the problem.

Warren MooreRounding up in this way does ensure that you process every pixel, but be mindful that it can also cause out-of-bounds accesses if you don’t guard against them when reading and writing. Nowadays, most Metal devices support non-uniform threadgroups, which can be dispatched with the

`[MTLComputeCommandEncoder dispatchThreads:threadsPerThreadgroup:]`

method. This obviates the need for bounds checking, because you can use a grid size that exactly matches the dimensions of your images.Philip GMany thanks for your reply. I prefer bounds-checking anyway; I don’t think the cost of four comparisons (albeit nested) is too much. For instance, with the Gaussian blur as-is you get a black border to the image. By testing textureIndex and supplying a more neutral (or pre-calculated average) colour when out-of-bounds this can be eliminated. 🙂

WasimQuestion about asynchronous processing. Looking at CommandBuffer::computeCommandEncoder(MTL::DispatchType::DispatchTypeConcurrent) can one use that along side render command encoder and not have to block rendering, without having to create another thread?

Warren MooreNo,

`MTLDispatchTypeConcurrent`

simply informs Metal that the commands encoded by the command encoder should be run concurrently if possible, and that you take responsibility for the synchronization of any resources that are not tracked (for example, resources allocated from an`MTLHeap`

that have a hazard-tracking mode of “untracked.”If you want to interleave render and compute commands in a single encoder, you should investigate tile shading with tile render pipelines, a feature available since A11 and on all Apple Silicon systems.