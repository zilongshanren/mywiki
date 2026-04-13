---
title: 'Towards real-time path tracing: An Efficient Denoising Algorithm for Global
  Illumination'
url: http://raytracey.blogspot.com/2017/07/towards-real-time-path-tracing.html
author: Sam Lapere
published: '2017-07-09'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

July is a great month for rendering enthusiasts: there's of course Siggraph, but the most exciting conference is

[High Performance Graphics](http://www.highperformancegraphics.org/2017/program/), which focuses on (real-time) ray tracing. One of the more interesting sounding papers is titled: "Towards real-time path tracing: An Efficient Denoising Algorithm for Global Illumination" by Mara, McGuire, Bitterli and Jarosz, which was released a couple of days ago. The paper, video and source code can be found atAbstract

We propose a hybrid ray-tracing/rasterization strategy for realtime rendering enabled by a fast new denoising method. We factor global illumination into direct light at rasterized primary surfaces and two indirect lighting terms, each estimated with one pathtraced sample per pixel. Our factorization enables efficient (biased) reconstruction by denoising light without blurring materials. We demonstrate denoising in under 10 ms per 1280×720 frame, compare results against the leading offline denoising methods, and include a supplement with source code, video, and data.

While the premise of the paper sounds incredibly exciting, the results are disappointing. The denoising filter does a great job filtering almost all the noise (apart from some noise which is still visible in reflections), but at the same it kills pretty much all the realism that path tracing is famous for, producing flat and lifeless images. Even the first Crysis from 10 years ago (the first game with SSAO) looks distinctly better. I don't think applying such aggressive filtering algorithms to a path tracer will convince game developers to make the switch to path traced rendering anytime soon. A comparison with ground truth reference images (rendered to 5000 samples or more) is also lacking from some reason.

At the same conference, a

[very similar paper](http://cwyman.org/papers.html)will be presented titled "Spatiotemporal Variance-Guided Filtering: Real-Time Reconstruction for Path-Traced Global Illumination".Abstract

We introduce a reconstruction algorithm that generates a temporally stable sequence of images from one path-per-pixel global illumination. To handle such noisy input, we use temporal accumulation to increase the effective sample count and spatiotemporal luminance variance estimates to drive a hierarchical, image-space wavelet filter. This hierarchy allows us to distinguish between noise and detail at multiple scales using luminance variance.

Physically-based light transport is a longstanding goal for real-time computer graphics. While modern games use limited forms of ray tracing, physically-based Monte Carlo global illumination does not meet their 30 Hz minimal performance requirement. Looking ahead to fully dynamic, real-time path tracing, we expect this to only be feasible using a small number of paths per pixel. As such, image reconstruction using low sample counts is key to bringing path tracing to real-time. When compared to prior interactive reconstruction filters, our work gives approximately 10x more temporally stable results, matched references images 5-47% better (according to SSIM), and runs in just 10 ms (+/- 15%) on modern graphics hardware at 1920x1080 resolution.

It's going to be interesting to see if the method in this paper produces more convincing results that the other paper. Either way HPG has a bunch more interesting papers which are worth keeping an eye on.


UPDATE (16 July): Christoph Schied from Nvidia and KIT, emailed me a link to the paper's preprint and video at


Video screengrab:







UPDATE (16 July): Christoph Schied from Nvidia and KIT, emailed me a link to the paper's preprint and video at

[http://cg.ivd.kit.edu/svgf.php](http://cg.ivd.kit.edu/svgf.php)Thanks Christoph!Video screengrab:

I'm not convinced by the quality of filtered path traced rendering at 1 sample per pixel, but perhaps the improvements in spatiotemporal stability of this noise filter can be quite helpful for filtering animated sequences at higher sample rates.

UPDATE (23 July) There is another denoising paper out from Nvidia: "

*Interactive Reconstruction of Monte Carlo Image Sequences using a Recurrent Denoising Autoencoder*" which uses machine learning to reconstruct the image.Abstract

We describe a machine learning technique for reconstructing image se- quences rendered using Monte Carlo methods. Our primary focus is on reconstruction of global illumination with extremely low sampling budgets at interactive rates. Motivated by recent advances in image restoration with deep convolutional networks, we propose a variant of these networks better suited to the class of noise present in Monte Carlo rendering. We allow for much larger pixel neighborhoods to be taken into account, while also improving execution speed by an order of magnitude. Our primary contri- bution is the addition of recurrent connections to the network in order to drastically improve temporal stability for sequences of sparsely sampled input images. Our method also has the desirable property of automatically modeling relationships based on auxiliary per-pixel input channels, such as depth and normals. We show signi cantly higher quality results compared to existing methods that run at comparable speeds, and furthermore argue a clear path for making our method run at realtime rates in the near future.

## 5 comments:

Did you have a chance to look at Convolutional Neural Network based network such the one Nvidia is proposing ? I think it will be well suited for real time renderer as well.



http://research.nvidia.com/publication/interactive-reconstruction-monte-carlo-image-sequences-using-recurrent-denoising

What they show is pretty amazing, once the model trained it could apply the effect in a few milliseconds

Ray tracing and rasterization is like the tortoise and the hare :-)

The spatiotemporal filter approach looks amazing - like truly amazing and amazingly usable but it has a problem with lag between the GI and the geometry itself which makes it kind of unusable for games... seeing especially shadows to lag behind after objects so much would be painful to endure and gamers would laugh their asses off. The new Nvidia AI filter looks amazing too - no lags but the result is softer than that of the spatiotemporal filter! But costs 50ms on a Pascal Titan which is too much..

I wonder if the noise problem could be solved with IBM's True North chip.




http://www.research.ibm.com/articles/brain-chip.shtml

' These systems can efficiently process high-dimensional, noisy sensory data in real time, while consuming orders of magnitude less power than conventional computer architectures.'

at a few milliwatts....

The Spatiotemporal Variance-Guided Filtering indeed looks amazing, and all the filtering is done in merely 5ms on a Titan X P at 1280x720.




Also this:

"The performance of our technique

is consistent across the sequence and is also largely

independent of scene properties."

That means, that highly detailed scenes should also be possible as far as the path tracing is running well (which is one of the well known strengths of ray/pathtracing)

Also the shadow lagging problem seems to be not that terrible, since it looks like, that it is initially a "bigger" problem, but over time, it is minimized.

It would be interesting to see even faster animations than in the video they made, if the lagging would be more visible.

I'm extremely excited at the implementations of this algorithm, for which I'm sure there will be quite some.

Post a Comment