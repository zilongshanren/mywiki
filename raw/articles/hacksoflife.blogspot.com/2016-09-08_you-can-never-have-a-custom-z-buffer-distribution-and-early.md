---
title: You Can Never Have a Custom Z Buffer Distribution and Early Z at the Same Time
url: http://hacksoflife.blogspot.com/2016/09/you-can-never-have-custom-z-buffer.html
author: Benjamin Supnik
published: '2016-09-08'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

The distribution of precision in the


In order to get correct perspective rendering via a view frustum, our projection matrix has to put our eye-space Z coordinate into our clip space W coordinate. But we don't get to pick and choose - perspective divide is part of fixed function hardware, and all of X, Y and Z in clip space are divided by the same W. So if we are dividing by our eye-space Z for our screen location, we



You can use this to have a



When are you non-linear? Pretty much any time you do anything to your Z value that can't be described as Ax + By + Cz + D. So for example, for eye-space linear, if we need to multiply by eye-space Z


The problem with not being linear is that the Z buffers written by the





In order for early-Z to be effective, the Z coordinate out of the rasterizer has to be correct - that is, the fragment shader can't modify it. So any scheme that encodes a non-linear depth buffer in fragment shader defeats this.


The really bad news is: you don't just pay once. Now that your Z buffer is encoded with a special encoding, anything that is Z tested (even if it isn't Z-writing) has to calculate Z in the fragment shader as well. So for example, particle systems, clouds, and other fill-rate-intensive effects become more expensive.


In summary: the need to move a custom Z function to the fragment shader is caused by the very thing that gives it better depth distribution, and this defeats early Z. So you can never have early Z and a super depth buffer distribution at the same time.


There is one work-around I have seen that gets around this: use floating point depth and



I wrote this post up after having worked out the math behind custom Z encodings (log Z, floating point eye-space, etc.); I had a todo item to investigate whether we could move X-Plane to a single Z pass and save some overhead.


The answer is, unfortunately, no for now. Losing early Z on our particle and cloud effects is a non-starter; we'd need to use a floating point depth buffer. Unfortunately,


One last note: X-Plane uses a floating point channel of the depth buffer to write floating point depth in eye space. While we split the actual Z buffer and draw in two passes, we build a single unified G-Buffer; our eye-space linear floating point depth has enough range to span both passes, and lets us then shade our G-Buffer in a single pass.


(When we run our two depth passes, we change

[default Z buffer configuration](https://www.sjbaker.org/steve/omniv/love_your_z_buffer.html)is not ideal. Precision is distributed via a 1 / x curve. This means more precision close to the camera, and less precision far away from it (which is good) but the curve goes asymptotic near the front, so it uses up*too much*precision. If you've had to try to tune your near clip plane, you know that bringing that near clip plane in just a little bit makes things much worse in the distance.In order to get correct perspective rendering via a view frustum, our projection matrix has to put our eye-space Z coordinate into our clip space W coordinate. But we don't get to pick and choose - perspective divide is part of fixed function hardware, and all of X, Y and Z in clip space are divided by the same W. So if we are dividing by our eye-space Z for our screen location, we

*have*to do so for depth as well. This is what distributes our depth precision.#### We Have Shaders - We Can Do Better

Now that we have shaders, we have the power to mess with this scheme. Let's say we want our Z buffer to contain an eye-space linear distribution. No problem! At the end of our vertex shader, we just load whatever Z we want, then multiply by our clip-space W to pre-nullify the perspective divide. Perfect!You can use this to have a

[logarithmic Z buffer](http://www.gamasutra.com/blogs/BranoKemen/20090812/85207/Logarithmic_Depth_Buffer.php), or you can use an eye-space Z buffer in floating point and in both cases you get really great distribution of depth precision. You can have a really, really close near clip plane and still have a huge depth range.#### The Problem With Not Being Linear

All of these custom Z distributions have one thing in common: the clip space Z values distributed across a triangle are*non-linear*. That is, if we find a point half-way along the edge of a triangle, the Z value that our formula produces will not be the same as the Z value the*hardware interpolator*produces based on the two triangle corners.When are you non-linear? Pretty much any time you do anything to your Z value that can't be described as Ax + By + Cz + D. So for example, for eye-space linear, if we need to multiply by eye-space Z

*again*, we're not linear.The problem with not being linear is that the Z buffers written by the

*middle*of a triangle may be very different from where it would have been if the triangle was tessellated. If you have a large-ish terrain triangle with a small decal like a rock on top of it, the middle of the large triangle might interpolate to be too close (or too far), causing Z errors. If you have a mesh with layers that requires hidden surface removal and it isn't extremely uniform in vertex density, again, interior interpolation error can lead to Z artifacts. Any polygon that intersects the clip planes is also going to go somewhat haywire, as the clipping changes Z mid-triangle*while the camera moves*.#### Let's Try The Fragment Shader

The above problems are almost certainly a show-stopper for any engine that shows artist-made 3-d meshes. The solution is to move the custom Z calculation to the fragment shader, so it can be done per pixel. This works great from a correctness standpoint - every pixel results in the right Z according to your encoding, but it has a nasty side effect: you lose early-Z.[Early Z](https://www.opengl.org/wiki/Early_Fragment_Test)is an optimization where your GPU runs the depth-stencil test*before*the fragment shader, instead of after. This is a huge win for any scene with significant hidden surfaces; fragment shading costs for hidden surfaces are completely removed, because the hardware doesn't even dispatch the fragments for shading. Without Early Z, your fragment shader runs, fetching textures, burning bandwidth, consuming ALU, and then throws the result out at the very end when it turns out that, oh noes, you've been drawing a secret base that's behind a closed door.In order for early-Z to be effective, the Z coordinate out of the rasterizer has to be correct - that is, the fragment shader can't modify it. So any scheme that encodes a non-linear depth buffer in fragment shader defeats this.

The really bad news is: you don't just pay once. Now that your Z buffer is encoded with a special encoding, anything that is Z tested (even if it isn't Z-writing) has to calculate Z in the fragment shader as well. So for example, particle systems, clouds, and other fill-rate-intensive effects become more expensive.

In summary: the need to move a custom Z function to the fragment shader is caused by the very thing that gives it better depth distribution, and this defeats early Z. So you can never have early Z and a super depth buffer distribution at the same time.

There is one work-around I have seen that gets around this: use floating point depth and

[reverse the near and far encoding values](https://developer.nvidia.com/content/depth-precision-visualized); since floating point has more precision at 0.0, you are using the higher precision of float where we need it (where 1/Z is imprecise).#### Split Depth for Now

X-Plane, like many games, uses two separate Z environments to cope with a very close view (inside the cockpit, where millimeters matter) and the world (where you can be millions of meters from the horizon). This isn't ideal - the cost of separating the Z passes isn't zero.I wrote this post up after having worked out the math behind custom Z encodings (log Z, floating point eye-space, etc.); I had a todo item to investigate whether we could move X-Plane to a single Z pass and save some overhead.

The answer is, unfortunately, no for now. Losing early Z on our particle and cloud effects is a non-starter; we'd need to use a floating point depth buffer. Unfortunately,

[ARB_clip_control](https://www.opengl.org/registry/specs/ARB/clip_control.txt)isn't wide-spread enough for us to count on. We'd also eat bandwidth in moving from a D24_S8 integer depth buffer to a D32F_S8 depth buffer (which pads out to 64 bits per depth sample.One last note: X-Plane uses a floating point channel of the depth buffer to write floating point depth in eye space. While we split the actual Z buffer and draw in two passes, we build a single unified G-Buffer; our eye-space linear floating point depth has enough range to span both passes, and lets us then shade our G-Buffer in a single pass.

(When we run our two depth passes, we change

*only*the near and far clip planes and nothing else; this means we can reuse our shadow maps and share our G-Buffer. This takes most of the cost out of our two passes.)
> We'd also eat bandwidth in moving from a D24_S8 integer depth buffer to a D32F_S8 depth buffer (which pads out to 64 bits per depth sample.





ReplyDeleteNot really. It's common to have separate depth and stencil buffers in HW; it may even be the case for D24S8 so it's possible that you're just wasting 1 byte/pixel of bandwidth by not using D32FS8.

E.g. http://amd-dev.wpengine.netdna-cdn.com/wordpress/media/2013/10/SI_3D_registers.pdf lists Z_24 format as deprecated. See also http://developer.amd.com/wordpress/media/2013/05/GCNPerformanceTweets.pdf:

GCN Performance Tip 1: Issues with Z-Fighting? Use D32_FLOAT_S8X24_UINT

format with no performance or memory impact compared to D24S8.

Notes: Depth and stencil are stored separately on GCN architectures. The

D32_FLOAT_S8X24_UINT is therefore not a 64-bit format like it could appear to be.

There is no performance or memory footprint penalty from using a 32-bit depth buffer

compared to using a 24-bit one.

Not sure what it's like on NVidia hardware, but I'd be very surprised if D32FS8 was a 64-bit format. Plus in general bandwidth is hard to estimate for depth targets since depth compression usually works pretty well.

Ah look at that - combined depth stencil isn't so combined anymore. :-)

DeleteWhat about layout(early_fragment_tests) in;?


ReplyDeletehttps://www.opengl.org/registry/specs/ARB/shader_image_load_store.txt

If you know what you are doing (tm), you can force early Z.

The problem is that the early Z will be against the pre-fragment shader output, because the fragment shader hasn't run. This kind of thing is useful for "conservative" depth, where you say "I'm going to touch Z, but not in a way that could make an early-Z-eliminated fragment visible."


DeleteBut since we don't know the mesh ordering between a low and high tessellated surface, error in the intermediate vertex-shader Z vs interpolation is going to err in both directions, making artifacts even if the Z test is re-run a second time. The only correct thing is to have early Z off.

Precision proportional to 1/z is very reasonable. You can move an object to be twice as far away and scale it to be twice as large, and end up with the same amount of depth buffer across the object. Perfect!





ReplyDeleteWhat's really going on is that precision is proportional to the derivative of the transformation. So if your depth values are 1-1/z, your precision is d/dz (1-1/z) = 1/z^2. Ouch!

A reversed floating-point depth buffer gives d/dz log(1/z) = -1/z. Perfect indeed.

OpenGL is very helpful with its normalized depth in [-1, 1], followed by a transformation to some range in [0, 1]. A depth buffer value of 0 corresponds to a normalized depth of -1: to attain it, you need catastrophic cancellation. A normalized depth of 0 corresponds to a depth buffer value of 1/2 (either that or you have a smaller depth range, which doesn't help): also catastrophic cancellation.

To prevent that you need NV_depth_buffer_float which allows an extended depth range (and give up far clipping at infinity, which is an advantage in some applications if anything) or clip control, neither of which is supported on OS X. Yay. I like OS X and my MacBook Pro but I hate how Apple is always years behind on OpenGL. When they finally released an OS X version supporting OpenGL 4.1 it was already over three years old, 4.4 being the current version at the time. None of the extensions enabling proper floating-point depth are supported. In Windows even the Iris Pro 5200 supports 4.3, and the GeForce 750M supports 4.5.

Speaking of depth range, you can render multiple passes in multiple depth ranges. That allows for some redistribution while keeping everything in the same depth buffer. You don't even need a floating-point buffer. It might not be perfectly seamless, however. Results and strategies probably depend on the particular renderer. I'll have to think about this sometime.

ReplyDeleteAh...interesting. So instead of:



Delete- Draw the far stuff over the whole Z range with far near/far clip

- Nuke Z

- Draw near stuff over the whole Z range with close near/far clip

We would instead:

- Set Z range for 0.5 to 1

- Draw far stuff in far clip config

- Set Z range to 0 to 0.5

- Draw near stuff in near clip config

I don't know how much better this is though.

- We still have a "hard wall" between the two Z environments. This means a strict ordering of what we draw, determining which elements go in which buckets, and any time the objects don't fit the partitioning scheme, we have artifacts.

(You can see these artifacts now if you walk out of the 3-d cockpit and look at a jetway...it's an awkward configuration where we can't do strict partitioning of scenery and airplane objects into separate Z buckets, and the results would make MC Escher smile. :-)

Other than saving a Z clear, what's the win here compared to clearing Z between passes?

My main brain fart was on creating some kind of consistency by having no overlap between depth ranges. Everything would be drawn in all applicable passes (hopefully without drawing too many things twice). An advantage of depth range as opposed to another clear (which would also work) is that everything is in the one depth buffer. You could drop it from the G-buffer. You wouldn't strictly have to render the passes in order if you have a use for that.





ReplyDeleteI just fear there will be glitches in the transition. OpenGL has clip z in the inclusive [-w, w], in theory anyway. The theoretical primitive sitting right on the transition plane would be drawn twice even if you got rasterization to be consistent. Then again, my GeForce 750M actually seems to use [-w, w). And is the depth range then going to map to the depth buffer precisely where we want it? I'm getting the impression my GPU is better suited than the actual spec, which honestly isn't a very comforting thought.

How are you going to match geometry exactly? Pass exactly the same clip xyw in both passes to begin with. Clip z is where things can and probably will mess up. Use split modelview/projection transformations for it. The projection transformations on z should be set up such that the transition z lands exactly on 1 in one pass and exactly on -1 in the other. Consider both transformations in each pass and quantize such that clipping could theoretically be correct on both sides, requiring a particular choice of transition plane and nullifying precision gains. A geometry shader can't help; a single primitive could be made more precise, at the cost of alignment with adjacent primitives. Then hope the clipping implementation is downright perfect because it probably isn't made to support this kind of abusive invariance.

Note that there are or have traditionally been different clipping implementations. NVIDIA has reportedly been clipless for years, meaning the rasterizer could handle it all directly without requiring traditional clipping with new vertices (say many sources; when I asked one they said they heard it directly from an employee). I'm not sure if that's still the case. It wouldn't make sense given current D3D rasterization rules. Anyway, if there's a difference in this department, it may or may not make a difference for this trick.

Yeah, not so great when you work it out. It looks doable with glitches on the transition plane. It would be so nice, though.