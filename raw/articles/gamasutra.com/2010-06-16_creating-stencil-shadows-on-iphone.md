---
title: Creating Stencil Shadows on iPhone
url: https://www.gamedeveloper.com/art/creating-stencil-shadows-on-iphone
author: Brian Hall
published: '2010-06-16'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# Creating Stencil Shadows on iPhone

Turbine developer Brian Hall delivers a how-to on his technique for displaying high-quality, convincing shadows in 3D environments on the iPhone -- using a technique that the platform is not designed to implement but which is capable of if you know this trick.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

One of the best ways to give the characters in your scene the feeling that they are part of it, and not superimposed upon it, are shadows. They give more depth to the scene and plant your characters firmly upon the ground. When your characters jump, their shadow and the character part, and greater sense of height is felt. In many cases, shadows have become a standard feature of many a 3D engine.

The iPhone, however, and its hardware limitations, present a problem for the typical 3D engine. At a glance, it would seem that the common techniques used to produce shadows are not possible on the iPhone. Limited fragment processing makes shader-based techniques less than ideal, and often requires a costly memory investment. Shadow solutions requiring dynamic textures are also not ideal, as they also require more memory, which is at a premium on the hardware.

Meanwhile, stencil buffer-based shadows are out as well, as the iPhone has no stencil buffer... Aren't they?

Before we delve into how this might be possible on an iPhone, it is important to recall how the Stencil Shadow technique works. At the highest level, the method is straightforward. First, the scene objects are rendered.

Second, the objects to cast shadows have their edges processed, extruded into volumes, and the volumes are rendered into the stencil buffer. Last, a full screen shadow colored quad is rendered over the scene using the stencil buffer as a mask.

There are dozens of approaches to how to extrude the edges of the objects into volumes, and plenty of other sources on how to do just that. For the purposes of this article, let's assume that we know how to generate shadow volumes, and we have extruded the volumes of our geometry so we can get on with the more important parts of the method: rendering the volumes.

While there are concerns about what to do if the camera is inside the shadow volume versus outside the shadow volume, that's deeper issue than needs to be explored right now. The idea is to render the volumes twice. The first time, we render the volumes with back face culling on, z-testing on, and we add one to the stencil. The second time, we render the volumes with front face culling on, z-testing on, and we decrement one from the stencil.

After both passes, what is left in the stencil buffer is zeros where there are no shadows, and greater than zero anywhere else. Basically, anywhere there are back faces and front faces without other geometry in between, there is no shadow. When there is geometry between the back faces and the front faces, the front faces end up getting rendered but not the back faces, thus leaving the stencil buffer with a positive count.

So how is this accomplished on the iPhone which has no stencil buffer? Many years ago, before 3D accelerated hardware was common on desktops, there existed only fixed function pipelines and hardware with limited functionality. Stencil buffers were considered something only needed by high end hardware, however nearly all hardware had a back buffer that had an alpha channel. This alpha channel was used for many things, and in some cases, could even be used as a stencil.

At first blush, the conversion seems simple from the stencil buffer to the alpha buffer. Stencils can add, alpha buffers can add. Stencils can subtract, alpha buffers can subtract. So for a first attempt, all of the stencil operations are swapped out with similar alpha operations.

![](../../assets/b237aa2a0927423b.img)


The first pass of the stencil buildup process. Negates the initial alpha buffer.

On the first pass of rendering the shadow volumes, back face culling is on, z-testing is on, and we use the Add operation with One for a source blend and One as a destination blend.

![](../../assets/a3f131ca7a1db79b.img)


The second pass of the stencil buildup process. Darkens the shadowed areas and forces the unshadowed areas to 1.

On the second pass, front face culling is on, z-testing is on, and we use the Reverse Subtract operation with One as a source blend and One as a destination blend. Unfortunately, this doesn't work right out of the box.

![](../../assets/78d90d010563d9e6.img)


The third pass of the stencil buildup process. Here the complex shadows become more evident: the statue has different values in its shadow areas.

One of the problems is that if we have an alpha of 1 in our destination buffer, and an alpha of 1 for our rendered object, the value in the destination buffer will saturate at 1.

This can happen if a shadow volume is complex and has multiple front faces for the same pixel. A Torus, for instance, has two front facing walls and two back facing walls. The algorithm needs to add up to two before it can subtract in order to render into the buffer properly.

Stencil buffers can have a range of 256 values all the way up into the millions depending on how many bits the stencil buffer has. This allows the stencil to be added to repeatedly before the subtraction phase of the algorithm.

In order to resolve this with the alpha buffer, a value of 1/256 can be used for the alpha value of the shadow volume when it is rendered. This allows for additional complexity of geometry to accumulate in the buffer and avoid saturation.

![](../../assets/faec444c122619dd.img)


The fourth pass of the stencil buildup process. The shadow stencil darkens more, and the complex shadows stand out.

However, this also requires more work later when it comes time to apply the shadows, so it is more efficient to use something on the order of 4/256 or 8/256 depending on the complexity of the objects in the scene and the fidelity desired. If too high a value is used for the complexity of the scene, the buffer will saturate resulting in shadowing artifacts.

![](../../assets/fbeebf354d15cd5f.img)


The fifth pass of the stencil buildup process. Here the shadow stencil is nearly 0 everywhere there are shadows.

Once the saturation problem is solved, another problem presents itself. The resulting alpha mask is very light. As a result, when the full screen quad is rendered, the shadow will not be visible. The mask is also not consistently a single value, which will result in shadows of varying darkness when cast by complex objects. The solution is to perform a number of normalization passes on the buffer using a full screen quad.

![](../../assets/ce92f7e2ac12621f.img)


The first pass of the stencil normalization process. Here the shadows are pulled down to 0, and the unshadowed areas become 1 - desired alpha value.

The initial pass is rendered with the quad at an alpha of 1/256 (fewer passes are needed if the alpha of the quad is larger as discussed earlier) with the Subtract blend operation, 1 - Destination Alpha as the source blend and One as the destination blend.

Each subsequent pass is performed with the Reverse Subtract blend operation, 1 - Destination Alpha as the source blend, and Destination Alpha as the destination blend. This builds up the alpha buffer such that we have a clear stencil of 1 where we have no shadows and a small alpha where we want shadows.

Pass | Alpha (unshadowed) | Alpha (shadowed) |
Initial | 0.0000 | 0.0040 |
Pass 1 | 1.0000 | 0.9922 |
Pass 2 | 1.0000 | 0.9767 |
Pass 3 | 1.0000 | 0.9306 |
Pass 4 | 1.0000 | 0.7966 |
Pass 5 | 1.0000 | 0.4312 |

In order to address the issue of the alpha values being inconsistent with complex geometry, one of two different approaches can be applied. The first way is to perform two more passes with a full screen quad with the alpha value of the desired alpha of the shadow stencil. The first pass uses a blend mode of Reverse Subtract, a source blend of One and a destination blend of One. This will take any alpha values less than the desired alpha value, and clamp them to zero. Provided all the alpha values are less than the desired alpha value set, this leaves you with pure zeros in the shadowed areas, and 1 - desired alpha values in the un-shadowed areas.

![](../../assets/dfdc693e7ca01567.img)


The second pass of the stencil normalization process. Here the shadows are set to the desired alpha value, and the unshadowed areas are back to 1.

The second pass adds the desired alpha back to the alpha buffer by using a blend operation of Add, a source blend of One and a destination blend of One. This will give shadowed areas the desired alpha, and un-shadowed areas a value of one. This is effectively a Max operation.

While the iPhone supports the Max operation, I personally have not had success yet getting the operation to work. Theoretically, however, the two above passes could be replaced with a single Max operation that effectively does what the two passes do, with less fill rate.

Now that the alpha stencil is built up, the shadows can be applied. This requires one final pass with a full screen quad colored the desired shadow color with an alpha of 1. The blend operation is Add, the source blend is Zero, and the destination blend is Destination Alpha. Also, the color operation should be Modulate in order to darken the affected areas of the scene.

![](../../assets/898323750f9f49d2.img)


The scene with shadows applied.

Using the alpha buffer for these sorts of tricks is a long standing tradition among those that grew up building the love hate relationship with fixed function pipelines. Mobile platforms for some of us are a blast from the past, where we again get to trick limited hardware to do things we want it to do, in order to obtain stunning visuals. The result: Dynamic Shadows on the iPhone, despite its imposed limitations.

To sum up, we can accomplish stencil quality shadows with a clear pass, up to six stencil building passes, two normalization passes, and an application pass. If fill rate isn't a concern, it's a viable solution to runtime shadows on the iPhone. I've implemented this solution in the Ogre 3D engine version 1.7 and tested it in their Shadows Sample on the iPhone. It will be available in the Ogre 3D distribution at a future date.