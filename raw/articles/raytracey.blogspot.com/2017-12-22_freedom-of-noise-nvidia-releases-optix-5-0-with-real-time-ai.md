---
title: 'Freedom of noise: Nvidia releases OptiX 5.0 with real-time AI denoiser'
url: http://raytracey.blogspot.com/2017/12/freedom-of-noise-nvidia-releases-optix.html
author: Sam Lapere
published: '2017-12-22'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

2018 will be bookmarked as a turning point for Monte Carlo rendering due to the wide availability of fast, high quality denoising algorithms, which can be attributed for a large part to Nvidia Research: Nvidia just released OptiX 5.0 to developers, which contains a new GPU accelerated "AI denoiser" which works as post-processing filter.




In contrast to traditional denoising filters, this new denoiser was trained using machine learning on a database of thousands of rendered image pairs (using both the noisy and noise-free renders of the same scene) providing the denoiser with a "memory": instead of calculating the reconstructed image from scratch (as a regular noise filter would do), it "remembers" the solution from having encountered similar looking noisy input scenes during the machine learning phase and makes a best guess, which is often very close to the converged image but incorrect (although the guesses progressively get better as the image refines and more data is available). By looking up the solution in its memory, the AI denoiser thus bypasses most of the costly calculations needed for reconstructing the image and works pretty much in real-time as a result.


The OptiX 5.0 SDK contains a sample program of a simple path tracer with the denoiser running on top (as a post-process). The results are nothing short of stunning: noise disappears completely, even difficult indirectly lit surfaces like refractive (glass) objects and shadowy areas clear up remarkably fast and the image progressively get closer to the ground truth.

The OptiX 5.0 SDK contains a sample program of a simple path tracer with the denoiser running on top (as a post-process). The results are nothing short of stunning: noise disappears completely, even difficult indirectly lit surfaces like refractive (glass) objects and shadowy areas clear up remarkably fast and the image progressively get closer to the ground truth.

![]() |

The denoiser is based on the Nvidia research paper "

[Interactive Reconstruction of Monte Carlo Image Sequences using a Recurrent Denoising Autoencoder](http://research.nvidia.com/publication/interactive-reconstruction-monte-carlo-image-sequences-using-recurrent-denoising)". The relentless Karoly Zsolnai from

[Two-minute papers](https://www.youtube.com/channel/UCbfYPyITQ-7l4upoX8nvctg)made an excellent video about this paper:

While in general the denoiser does a fantastic job, it's not yet optimised to deal with areas that converge fast, and in some instances overblurs and fails to preserve texture detail as shown in the screen grab below. The blurring of texture detail improves over time with more iterations, but perhaps this initial overblurring can be solved with more training samples for the denoiser:

![]() |

The denoiser is provided free for commercial use (royalty-free), but requires an Nvidia GPU. It works with both CPU and GPU rendering engines and is already implemented in Iray (Nvidia's own GPU renderer), V-Ray (by Chaos Group), Redshift Render and Clarisse (a CPU based renderer for VFX by Isotropix).

Some videos of the denoiser in action in Optix, V-Ray, Redshift and Clarisse:

Optix 5.0:

[youtu.be/l-5NVNgT70U](https://www.youtube.com/watch?v=l-5NVNgT70U)

Iray:

[youtu.be/yPJaWvxnYrg](https://www.youtube.com/watch?v=yPJaWvxnYrg)

This video shows the denoiser in action in Iray and provides a high level explanation of the deep learning algorithm behind the OptiX/Iray denoiser:

V-Ray 4.0:

[youtu.be/nvA4GQAPiTc](http://youtu.be/nvA4GQAPiTc)

Redshift:

[youtu.be/ofcCQdIZAd8](https://www.youtube.com/watch?v=ofcCQdIZAd8)(and

[a post from Redshift's Panos](https://blenderartists.org/forum/showthread.php?395313-Experimental-2-77-Cycles-Denoising-build&p=3267247&viewfull=1#post3267247)explaining the implementation in Redshift)

ClarisseFX:

[youtu.be/elWx5d7c_DI](https://www.youtube.com/watch?v=elWx5d7c_DI)

Other renderers like Cycles and Corona already have their own built-in denoisers, but will probably benefit from the OptiX denoiser as well (especially Corona which was acquired by Chaos Group in September 2017).

The OptiX team has indicated that they are researching an optimised version of this filter for use in interactive to real-time photorealistic rendering, which might find its way into game engines. Real-time noise-free photorealistic rendering is tantalisingly close.

## 2 comments:

Hi there,




I am just in my own deep learning process about this whole new area of research...

I'm curious if you see deep learning on the GPU becoming relevant to game rendering? Are game developers working with nVidia on how to develop ways to use deep learning to render game environments? E.g. could it be trained to preemptively generate virtual realistic looking forests or areas fully of unique, non-repeating detail on the fly and so on?

forgive my naive questions I am very new to all of this but from what I understand, if I'm understanding it correctly, the potential impact of AI is huge.

HI,



There is any ''how to'' install Optix denoiser for Redshift?

thank you.

Post a Comment