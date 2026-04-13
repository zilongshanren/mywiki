---
title: Call for a new Post-Processing Pipeline - KGC 2013 talk
url: http://diaryofagraphicsprogrammer.blogspot.com/2013/09/call-for-new-post-processing-pipeline.html
author: Wolfgang Engel
published: '2013-09-30'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

This is the text version of my talk at KGC 2013.


The main motivation for the talk was the idea of looking for fundamental changes that can bring a modern Post-Processing Pipeline to the next level.

Let's look first into the short history of Post-Processing Pipelines, where we are in the moment and where we might be going in the near future.






















Let's look first into the short history of Post-Processing Pipelines, where we are in the moment and where we might be going in the near future.

**History**

Probably one of the first Post-Processing Pipelines appeared in the DirectX SDK around 2004. It was a first attempt to implement HDR rendering. I believe from there on we called a collection of image space effects at the end of the rendering pipeline Post-Processing pipeline.

The idea was to re-use resources like render targets and data with as many image space effects as possible in a Post-Processing Pipeline.

A typical collection of screen-space effects were

- Tone-mapping + HDR rendering: the tone-mapper can be considered a dynamic contrast operator
- Camera effects like Depth of Field with shaped Bokeh, Motion Blur, lens flare etc..
- Full-screen color filters like contrast, saturation, color additions and multiplications etc..

One of the first coverages of a whole collection of effects in a Post-Processing Pipeline running on XBOX 360 / PS3 was done in [Engel2007].

Since then numerous new tone mapping operators were introduced [Day2012], new more advanced Depth of Field algorithms with shaped Bokeh were covered but there was no fundamental change to the concept of the pipeline.

**Call for a new Post-Processing Pipeline**

Let's start with the color space: RGB is not a good color space for a post-processing pipeline. It is well known that luminance variety is more important than color variety, so it makes sense to pick a color space that has luminance in one of the channels. With the 11:11:10 render targets it would be cool to store luminance in one of the 11 bit channels. Having luminance available in the pipeline without having to go through color conversions opens up many new possibilities, from which we will cover a few below.

Global tone mapping operators didn't work out well in practice. We looked at numerous engines in the last four years and a common decision by artists was to limit the luminance values by clamping them. The reasons for this were partially in the fact that the textures didn't provide enough quality to survive a "light adaptation" without blowing out or sometimes most of their resolution was in the low-end greyscale values and there wasn't just enough resolution to mimic light adaptations.

Another reason for this limitation was that the available resolution in the rendering pipeline with the RGB color space was not enough. Another reason for this limitation is the fact that we limited ourselves to Global tone mapping operators, because local tone mapping operators are considered too expensive.

A fixed global gamma adjustment at the end of the pipeline is partially doing "the same thing" as the tone mapping operator. It applies a contrast and might counteract the activities that the tone-mapper already does.

So the combination of a tone-mapping operator and then the commonly used hardware gamma correction, which are both global is odd.

On a lighter note, a new Post-Processing Pipeline can add more stages. In the last couple of years, screen-space ambient occlusion, screen-space skin and screen-space reflections for dynamic objects became popular. Adding those to the Post-Processing Pipeline by trying to re-use existing resources need to be considered in the architecture of the pipeline.

Last, one of the best targets for the new compute capabilities of GPUs is the Post-Processing Pipeline. Saving memory bandwidth by merging "render target blits" and re-factoring blur kernels for thread group shared memory or GSM are considerations not further covered in the following text; but most obvious design decisions.

Let's start by looking at the an old Post-Processing Pipeline design. This is an overview I used in 2007:

*A Post-Processing Pipeline Overview from 2007*



A few notes on this pipeline. The tone mapping operation happens at two places. At the "final" stage for tone-mapping the final result and in the bright-pass filter for tone mapping the values before they can be considered "bright".

The "right" way to apply tone mapping independent of the tone mapping operator you choose is to convert into a color space that exposes luminance, apply the tone mapper to luminance and then convert back to RGB. In other words: you had to convert between RGB and a different color space back and forth twice.

In some pipelines, it was decided that this is a bit much and the tone mapper was applied to the RGB value directly. Tone mapping a RGB value with a luminance contrast operator led to "interesting" results.

Obviously this overview doesn't cover the latest Depth of Field effects with shaped Bokeh and separated near and far field Center of Confusion calculations, nevertheless it shows already a large amount of render-target to render-target blits that can be merged with compute support.

All modern rendering pipelines calculate color values in linear space; meaning every texture that is loaded is converted into linear space by the hardware, then all the color operations are applied like lighting and shadowing, post-processing and then at the end the color values are converted back by applying the gamma curve.

This separate Gamma Control is located at the end of the pipeline, situated after tone mapping and color filters. This is because the GPU hardware can apply a global gamma correction to the image after everything is rendered.

The following paragraphs will cover some of the ideas we had to improve a Post-Processing Pipeline on a fundamental level. We implemented them into our Post-Processing Pipeline PixelPuzzle. Some of the research activities like finally replacing the "global tone mapping concept" with a better way of calculating contrast and color will have to wait for a future column.

**Yxy Color Space**

The first step to change a Post-Processing Pipeline in a fundamental way is to switch it to a different color space. Instead of running it in RGB we decided to use CIE Yxy through the whole pipeline. That means we convert RGB into Yxy at the beginning of the pipeline and convert back to RGB at the end. In-between all operations run on Yxy.

With CIE Yxy, the Y channel holds the luminance value. With a 11:11:10 render target, the Y channel will have 11 bits of resolution.

Instead of converting RGB to Yxy and back each time for the final tone mapping and the bright-pass stage, running the whole pipeline in Yxy means that this conversion might be only done once to Yxy and once or twice back to RGB.

Tone mapping then still happens with the Y channel in the same way it happened before. Confetti's PostFX pipeline offers eight different tone mapping operators and each of them works well in this setup.

Now one side effect of using Yxy is also that you can run the bright-pass filter as a one channel operation, which saves on modern scalar GPUs some cycles.

One other thing that Yxy allows to do is to consider the occlusion term in Screen-Space Ambient Occlusion as a member of the Y channel. So you can mix in this term and use it in interesting ways. Similar ideas apply to any other occlusion term that your pipeline might be able to use.

The choice of using CIE Yxy as the color space of choice was arbitrary. In 2007 I evaluated several different color spaces and we ended up with Yxy at the time. Here is my old table:

*Pick a Color Space Table from 2007*



Compared to CIE Yxy, HSV doesn't allow easily to run a blur filter kernel. The target was to leave the pipeline as unchanged as possible when picking a color space. So with Yxy, all the common Depth of Field algorithms and any other blur kernel runs unchanged in Yxy. HSV conversions also seem to be more expensive compared to RGB -> CIE XYZ -> CIE Yxy and vice versa.

There might be other color spaces similar tailored to the task.

**Dynamic Local Gamma**

As mentioned above, the fact that we apply a tone mapping operator and then later on a global gamma operator appears to be a bit odd. Here is what the hardware is supposed to do when it applies the gamma "correction".

*Gamma Correction*

The main take-away from this curve is that the same curve is applied to every pixel on screen. In other words: this curve shows an emphasis on dark areas independently of the pixel being very bright or very dark.

Whatever curve the tone-mapper will apply, the gamma correction might be counteracting it.

It appears to be a better idea to move the gamma correction closer to the tone mapper, making it part of the tone mapper and at the same time apply gamma locally per pixel.

In fact gamma correction is considered depending on the light adaptation level of the human visual system. The "gamma correction" that is applied by the eye changes the perceived luminance based on the eye's adapatation level [Bartleson 1967] [Kwon 2011].

When the eye is adapted to dark lighting conditions, the exponent for the gamma correction is supposed to increase. If the eye is adapted to bright lighting conditions, the exponent for the gamma correction is supposed to decrease. This is shown in the following image taken from [Bartleson 1967]:

*Changes in Relative Brightness Contrast [Bartleson 1967]*

A local gamma value can vary with the eye's adaptation level. The equation that adjusts the gamma correction following the current adaptation level of the eye can be found in [Kwon 2011].

γv=0.444+0.045 ln(Lan+0.6034)

For this presentation, this equation was taken from the paper by Kwon et all. Depending on the type of game there is an opportunity to build your own local gamma operator.
The input luminance value is generated by the tone mapping operator and then stored in the Y channel of the Yxy color space:

YYxy=Lγv

γv changes based on the luminance value of the current pixel. That means each pixels luminance value might be gamma corrected with a different exponent. For the equation above, the exponent value is in the range of 0.421 to 0.465.

*Applied Gamma Curve per-pixel based on luminance of pixel*

*•Eye’s adaptation == low - >blue curve*

*•Eye’s adaptation value == high -> green curve*

Lγv

works with any tone mapping operator. L is the luminance value coming from the tone mapping operator.

works with any tone mapping operator. L is the luminance value coming from the tone mapping operator.

With a dynamic local gamma value, the dynamic lighting and shadowing information that is introduced in the pipeline will be considered for the gamma correction. The changes when going from bright areas to dark areas appear more natural. Textures are holding up better the challenges of light adaptation. Overall lights and shadows look better.




**Depth of Field**
As a proof-of-concept of the usage of Yxy color space and the local dynamic gamma correction, this section is showing screen-shots of a modern Depth of Field implementation with separated near and far field calculations and a shaped Bokeh, implemented in compute.


Producing an image through a lens leads to a "spot" that will vary in size depending on the position of the original point in the scene:






Producing an image through a lens leads to a "spot" that will vary in size depending on the position of the original point in the scene:

The Depth of Field is the region, where the CoC is less than the resolution of the human eye (or in our case the resolution of our display medium). The equation on how to calculate the CoC [Potmesil1981] is:

Following the variables in this equation, Confetti demonstrated in a demo at GDC 2011 [Alling2011] the following controls:

- F-stop - ratio of focal length to aperture size
- Focal length – distance from lens to image in focus
- Focus distance – distance to plane in focus

Because the CoC is negative for far field and positive for near field calculations, separate results are commonly generated for the near field and far field of the effect [Sousa13].

Usually the calculation of the CoC is done for each pixel in a down-sampled buffer or texture. Then the near and far field results are generated. Then, first, the far and focus field results are combined and then this result is combined with the near field, based on a near field coverage value. The following screenshots show the result of those steps, with the first screenshot showing the near and far field calculations:







[Alling2011] Michael Alling, "Post-Processing Pipeline", http://www.conffx.com/GDC2011.zip
[Bartleson 1967] C. J. Bartleson and E. J. Breneman, “Brightness function: Effects of adaptation,” J. Opt. Soc. Am., vol. 57, pp. 953-957, 1967.

[Day2012] Mike Day, “An efficient and user-friendly tone mapping operator”,

[Engel2007] Wolfgang Engel, “Post-Processing Pipeline”, GDC 2007

[Kwon 2011] Hyuk-Ju Kwon, Sung-Hak Lee, Seok-Min Chae, Kyu-Ik Sohng, “Tone Mapping Algorithm for Luminance Separated HDR Rendering Based on Visual Brightness Function”, online at

[Potmesil1981] Potmesil M., Chakravarty I. “Synthetic Image Generation with a Lens and Aperture Camera Model”, 1981

[Reinhard] Erik Reinhard, Michael Stark, Peter Shirley, James Ferwerda, "Photographic Tone Reproduction for Digital Images", http://www.cs.utah.edu/~reinhard/cdrom/

[Sousa13] Tiago Sousa, "CryEngine 3 Graphics Gems", SIGGRAPH 2013,



Usually the calculation of the CoC is done for each pixel in a down-sampled buffer or texture. Then the near and far field results are generated. Then, first, the far and focus field results are combined and then this result is combined with the near field, based on a near field coverage value. The following screenshots show the result of those steps, with the first screenshot showing the near and far field calculations:

*Red = max CoC(near field CoC)*

*Green = min CoC(far field CoC)*



Here is a screenshot of the far field result in Yxy:



*Far field result in Yxy*



Here is a screenshot of the near field result in Yxy:

*Near field result in Yxy*



Here is a screenshot of resulting image after it was converted back to RGB:

*Resulting Image in RGB*

**Conclusion**

A modern Post-Processing Pipeline can benefit greatly from being run in a color space that offers a separable luminance channel. This opens up new opportunities for an efficient implementation of many new effects.

With the long-term goal of removing any global tone mapping from the pipeline, a dynamic local gamma control can offer more intelligent gamma control that is per-pixel and offers a stronger contrast of bright and dark areas, considering all the dynamic additions in the pipeline.

Any future development in the area of Post-Processing Pipelines can be focused on a more intelligent luminance and color harmonization.

**References**

[Alling2011] Michael Alling, "Post-Processing Pipeline", http://www.conffx.com/GDC2011.zip

[Day2012] Mike Day, “An efficient and user-friendly tone mapping operator”,

[http://www.insomniacgames.com/mike-day-an-efficient-and-user-friendly-tone-mapping-operator/](http://www.insomniacgames.com/mike-day-an-efficient-and-user-friendly-tone-mapping-operator/)

[Engel2007] Wolfgang Engel, “Post-Processing Pipeline”, GDC 2007

[http](http://www.coretechniques.info/index_2007.html)

[://](http://www.coretechniques.info/index_2007.html)

[www.coretechniques.info/index_2007.html](http://www.coretechniques.info/index_2007.html)

[Kwon 2011] Hyuk-Ju Kwon, Sung-Hak Lee, Seok-Min Chae, Kyu-Ik Sohng, “Tone Mapping Algorithm for Luminance Separated HDR Rendering Based on Visual Brightness Function”, online at

[http://world-comp.org/p2012/IPC3874.pdf](http://world-comp.org/p2012/IPC3874.pdf)

[Potmesil1981] Potmesil M., Chakravarty I. “Synthetic Image Generation with a Lens and Aperture Camera Model”, 1981

[Reinhard] Erik Reinhard, Michael Stark, Peter Shirley, James Ferwerda, "Photographic Tone Reproduction for Digital Images", http://www.cs.utah.edu/~reinhard/cdrom/

[Sousa13] Tiago Sousa, "CryEngine 3 Graphics Gems", SIGGRAPH 2013,

[http://www.crytek.com/cryengine/presentations/cryengine-3-graphic-gems](http://www.crytek.com/cryengine/presentations/cryengine-3-graphic-gems)

## 9 comments:

You can even render the scene directly in a luminance-color format, as in The Compact YCoCg Frame Buffer. They also use chroma subsampling to reduce framebuffer bandwidth. The reconstruction filter for this could also be integrated into the compute shader postprocess.


I'm still using global tone mapping because I've yet to come across a local one that looks good. All the ones I've seen have problems with halos and other such unnatural artifacts. In practice I found Jim Hejl's tone curve (slide 140 here), together with exposure and contrast adjustment prior to tone mapping, to be quite adequate for games.

Why no mention ycocg ?





From gpu pro 4 "practical framebuffer compression" ;)

( or The Compact YCoCg Frame Buffer http://www.pmavridis.com/research/fbcompression/ )

Nathan: yes. You can do that. There are numerous articles in the last few GPU Pros who cover that.




Rendering your geometry in RGB and then converting it in screen-space should be faster. You don't pay any overdraw cost then.

Local tone mapping operator: I think tone mapping is in general not such a great solution. In seom game teams there is a "manual" way to color harmonization. The lead artist prepares a color table and the team sticks to this color table for a certain level.

You want to mimic this in your postFX ...

Tuan: yes I really like this article it is great.

My concern is that if you covert into a different color space while rendering an object, you might pay the overdraw cost for the color conversion. This is why I render in RGB and covert to a different color space in screen-space.

Converting to YCoCg is only a handful of ALU ops, though. It's quite possible it will add no cost at all to a shader due to texture latency hiding, etc. I'd be surprised if it's a cost worth worrying about.


If feeling ambitious, one could do the whole renderer and art pipeline in YCoCg - pre-processing all color textures, light colors, etc. into it. :) No extra runtime cost then! Except for the final conversion to RGB at the end.

Nathan: YCoCg sounds great! This would be awesome. If you try, let me know how it is going :-)

Very cool stuff :-)

The idea of having per-pixel tone mapping is interesting, but AFAIK the final tone mapping done at the end of rendering is used to counteract the non-linear behavior of photons on our monitors, so I am not convinced that we should do the per-pixel tone mapping there.

Converting to YCoCg is only a handful of ALU ops, though. It's quite possible it will add no cost at all to a shared due to texture latency hiding, etc. I'd be surprised if it's a cost worth worrying about.

Post a Comment