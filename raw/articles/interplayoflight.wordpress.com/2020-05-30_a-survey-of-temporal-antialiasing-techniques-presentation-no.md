---
title: 'A Survey of Temporal Antialiasing Techniques: presentation notes'
url: https://interplayoflight.wordpress.com/2020/05/30/a-survey-of-temporal-antialiasing-techniques-presentation-notes/
author: Kostas Anagnostou
published: '2020-05-30'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

At Eurographics 2020 virtual conference, Lei Yang did a presentation of the[ Survey of Temporal Antialiasing Techniques](http://behindthepixels.io/assets/files/TemporalAA.pdf) report which included a good overview of TAA and temporal upsampling, its issues and future research.

I have taken some notes while watching it and I am sharing them here in case anyone finds them useful.

**Introduction**

- TAA is the defacto antialiasing technique
- suitable for deferred renderers, replacing MSAA which is expensive with such architectures
- it is like supersampling: multiple samples per pixel but spreading the samples across time instead of all in one frame
- Only current frame sample can be trusted. Others may be occluded/dis-occluded/different lighting etc.
- Recursive process: the output of the previous frame (history buffer) feeds into the current frame
- history buffer sample is re-projected into the current frame to compensate for scene motion
- renderer supplies per pixel motion vectors
- reprojected samples are validated/rectified using samples from the current frame.
- accumulate new samples into history buffer

- a subpixel jitter offset is applied to projection matrix
- needs a low discrepancy sequence (Halton)
- We usually store a single colour in the history buffer to save space
- We use an exponential filter to combine new sample into history buffer (1-a) * history_colour + a * new_colour
- corresponds to a weighted sum of samples with smaller weights assigned to older samples
- We typically use a small alpha value to get even weights over previous samples
- a fixed alpha can reduce quality of antialiasing though, adaptive alpha (eg progressively decreasing from the harmonic series) can improve this.

- Reprojection takes care of moving objects/camera
- bilinear or bicubic filtering can be used to reconstruct the pixel colours
- reprojected history colour can be wrong (occlusion, dissocclusion, lighting changes, wrong motion vectors)
- We need to rejected or rectify it
- Validation can be done comparing depth, normal, object/prim ID, colour
- If invalid we can reject of fade out history colour setting alpha close to 1.
- Rectification makes history colour more consistent with new colour samples
- Compare it with pixels in 3×3 neighbourhood in the new colour buffer and use clipping or clamping against the neighbourhood colour AABB.
- Variance clipping (fit AABB around mean and variance of the neighbourhood) avoids outlier colours

- TAA is used for upsampling as well
- Use a history buffer resolution higher than the rendered image resolution
- has advantage over spatial upsampling techniques (more information)
- Bins temporal samples to a higher resolution grid

- Scaling-aware sample accumulation
- Step 1: Upscale current frame samples to higher resolution with spatial interpolation. Produces blurry image.
- Step 2: Blur the image with history buffer (already at higher resolution). We need adaptive blending based on sample location. Can use blurring kernel instead of binary decision.

- Checkerboard rendering is a form of temporal upsampling. Fixed 1:2 upsampling rate, uses MSAA or target independent rasterisation — more complicated to implement.

**Challenges**

- Bluriness. Two main reasons:
- History resampling due to reprojection. Quality improves with more expensive filters
- History clipping/clamping. Can incorrectly removed detailed features in history [introducing flickering]. More pronounced with temporal upsampling.
- Sharpening is often used to reduce bluriness

- Ghosting
- incorrect history clamping
- often visible on disocclusion of highly detailed (contrast) background. A high contrast bg causes the clamping AABB to bloat and becomes ineffective in removing invalid history

- Temporal instability and Moire
- Occurs when frequency of a feature and the sampling frequency are correlated
- Jittered position cause alternate values and flickering
- History clamping exposes the flickering result

- Undersampling artifacts
- Newly disoccluded regions with not enough samples in the history buffer
- Appears overly sharp/aliased or contain unstable noise
- Can be improved with spatial AA techniques

- Inflexible history rectifiction techniques prevent us from getting higher quality images.

**Future research**

- Use machine learning to replace heuristics (DLSS 2.0)
- Can produce more detailed results

Paper covers more TAA related topics (HDR and colour space, performance, variable rate shading, temporal denoising)

**Questions from audience**

- What colour spaces can we use for rectification?
- Any would do, some people use in Ycocg or YUV that produce tighter AABBs
- Still not ideal, colour clamping can be problematic in areas of high contrast (large AABBs), leaking colours from previous frames.

- How do HDR colour spaces affect TAA?
- we want to do TAA after HDR resolve
- postprocessing happens in HDR and sometimes need TAA beforehand
- workaround is to do fake (reversible) tonemap, do TAA and then reverse it before any further postprocessing with antialiased result. Can reduce effectiveness of TAA sometimes.

- Will DLSS replace TAA?
- today it can be a replacement for TAA + it offers upsampling

- Can maintaining a history of the AABBs can maybe help solve the flickering problem?
- potentially but will also increase the amount of data that need reprojecting every frame.

- Any new info about DLSS 2.0 – no plans for further publications