---
title: A different way of generating high-res screenshots
url: http://c0de517e.blogspot.com/2011/04/different-way-of-generating-high-res.html
published: '2011-04-06'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Having a hi-res screenshot tool in a game, even if you don't ship a "photo mode" to the user, is very common for marketing purposes (posters and so on). Now what I see commonly done for such things is to have a tiling renderer, that's to say, render the same scene multiple times, each time writing out a portion of the final screenshot. That's done because GPUs have limits in terms of rendering sizes and often the memory needed to store intermediate buffers is simply not there (especially if you're shipping on consoles).

The tiling strategy often results in being a pain for two reasons: first, you have to scale all pixel-based effects in order not to shrink in the final screenshot*, second, tiles create non symmetric frustums that are tricky to handle, as assuming a symmetric frustum ends up allowing simpler equations in a few places (i.e. in shaders that go from the z-buffer to view space and back).

So here it is a recipe for a different screenshot tool. 1... 2... 3...

Instead of generating N tiles, shift your viewport (yes, as in the viewport matrix) of a fraction of a pixel N times (in a grid fashion). Then instead of collating the tiles next to each other, take each generated image and interleave the samples, like this:

Four two-by two images. Image one has no shift, image two is shifted by half a pixel on the x, image 3 is shifted by half a pixel on the y, image 4 is shifted by half a pixel on x and y

11 22

11 22

33 44

33 44High-res result:

1212

1212

3434

3434

**Done!**

...

Ok... not quite! I lied. Did you spot the error? A hint... pixel footprint...

Each image will cover one quarter of the scene in the final image, but the GPU does not really know. It will still generate all derivatives as if it was not a high-resolution image, thus all the mipmaps will be wrong in the final image (too blurry). The solution there is to mipbias all your samplers (it should be easy, in your material system probably there is only a point where the textures of a given material are bound), or even more easily just set the maximum mip level to be zero, as usually very high res screenshots will hit the top mip anyways.

**Done!**

Erhm... I lied again! Sort-of. This method does indeed work, but it's still not correct. We're shifting the view, it means that our images do not share the same view center, so we're not using a pinhole camera anymore (or well, we made that pinhole non infinitesimal). In pratice this is not a big deal, even if it can still screw some math (in a couple of SSAO implementations I've worked with, I had to disable the shift when generating the AO map). Of course, to be correct, we should rotate the camera...

Or should we? Ok enough toying. Rotating the camera is better but still not 100% right, as now we're also slightly rotating the near and far planes for each image. Again, it's not something noticeable, but in the end to be entirely correct we should maintain the near and far straight, and that will lead again to non-symmetric frustums (even if only a tiny bit).

Of course, once you have any method to generate high res screenshots, it's easy to do many more cool tricks, like accumulating images to simulate DOF and motion blur and antialiasing, rendering soft shadows and so on.

*Note: * you'll still need to have such functionality if you're shipping a PC title that can do different resolutions. And it's quite a pain, because if you just express all your screenspace effects in relative units instead of pixels you get the right "size" of the effect, but you will also have less dense samples, and thus not really scale the quality with the resolution. Many effects will actually look worse (aliasing artifacts, i.e. in a bloom we can get shimmering), others do rely on accessing neighboring pixels (think about fast Gaussian filters that leverage the bilinear interpolation between samples)*.

## 7 comments:

Your view frustum doesn't have to be symmetric. Keep the eye point the same, and shear (don't rotate) the planes in x and y.


Also, I thought this was pretty well known...like how 3dfx used to do full-screen supersampling.

Autodidactic: did you hit "comment" too fast, while reading every other line of the post?



"tiles create non symmetric frustums that are tricky to handle, as assuming a symmetric frustum ends up allowing simpler equations in a few places"

Where did I write that you can't have non-symmetric frustums? I wrote that they are trickier to handle! But wasn't that obvious ALSO by the fact that I said that the tiling method is the most common?

So this is the same as Rabin's "Poster Quality Screenshots" article in Game Programming Gems 4 ;)


When I tried to use it, I ran into some issues that it does not really scale to more than something like 2x2 larger shots. The diagonal edges do not turn into proper lines, but into some weird semi-staircase pattern. I attributed that to the GPU rasterizer still snapping to pixels, but maybe I just did something wrong.

NeARAZ: I guess, I didn't read much of the GPGems, I mostly skim these books :) I saw two different implementations of it and I didn't notice that problem in either.

NeARAZ: I've used this to generate huge shots (we're talking posters that take up an entire wall at 300 dpi), so it definitely scales up.


The main issues we ran into were artifacts with DoF and bloom, as pointed out in the article, but they were manageable.

Sorry, looks like I missed the key paragaph! That's what I get for reading/posting on my phone.

Any clues how one would calculate how far to move the camera to achieve this?

Post a Comment