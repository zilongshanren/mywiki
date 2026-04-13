---
title: Real-time Energy Redistribution Path Tracing in Brigade!
url: http://raytracey.blogspot.com/2010/07/energy-redistribution-path-tracing-in.html
author: Sam Lapere
published: '2010-07-14'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

A lot of posts about Brigade lately, but that's because the pace of development is going at break neck speeds and the intermediate updates are very exciting. Jacco Bikker and Dietger van Antwerpen, the coding brains behind the Brigade path tracer, seem unstoppable. The latest contribution to the Brigade path tracer is the implementation of ERPT or Energy Redistribution Path Tracing. ERPT was presented at Siggraph 2005 and is an unbiased extension of regular path tracing which combines Monte Carlo path tracing and Metropolis Light Transport path mutation to obtain lower frequency noise and converge faster in general. Caustics benefit greatly as well as scenes which are predominantly lit by indirect lighting. The original ERPT paper can be found at


The algorithm seems to be superior than (bidirectional) path tracing and MLT in most cases, while retaining it's unbiased character. And they made it work on the GPU! You could say that algorithm-wise, the addition of ERPT makes Brigade currently more advanced than the other GPU renderers (Octane, Arion, LuxRays, OptiX, V-Ray RT, iray, SHOT, Indigo GPU, ...) which rely on "plain" path tracing.


The following video compares path tracing to ERPT in Brigade at a resolution of 1280x720(!) on a GTX 470:


This image directly compares path tracing on the left with ERPT on the right (the smeary pixel artefacts in the ERPT image are mostly due to the youtube video + JPEG screengrab compression, but I presume that there are also some noise filters applied as described in the ERPT paper):



On a side note, the Sponza scene in the video renders very fast for the given resolution and hardware. When comparing this with


[http://rivit.cs.byu.edu/a3dg/publications/erPathTracing.pdf](http://rivit.cs.byu.edu/a3dg/publications/erPathTracing.pdf)and offers a very in-depth and understandable insight into the technique. A practical implementation of ERPT can be found in the paper "Implementing Energy Redistribution Path Tracing" ([http://www.cs.ubc.ca/~batty/projects/ERPT-report.pdf](http://www.cs.ubc.ca/~batty/projects/ERPT-report.pdf)).The algorithm seems to be superior than (bidirectional) path tracing and MLT in most cases, while retaining it's unbiased character. And they made it work on the GPU! You could say that algorithm-wise, the addition of ERPT makes Brigade currently more advanced than the other GPU renderers (Octane, Arion, LuxRays, OptiX, V-Ray RT, iray, SHOT, Indigo GPU, ...) which rely on "plain" path tracing.

The following video compares path tracing to ERPT in Brigade at a resolution of 1280x720(!) on a GTX 470:

[http://www.youtube.com/watch?v=d9X_PhFIL1o&feature=channel](http://www.youtube.com/watch?v=d9X_PhFIL1o&feature=channel)This image directly compares path tracing on the left with ERPT on the right (the smeary pixel artefacts in the ERPT image are mostly due to the youtube video + JPEG screengrab compression, but I presume that there are also some noise filters applied as described in the ERPT paper):

[ERPT seems to be a little bit darker than regular path tracing in this image, which seems to be a by product of the noise filters according to](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhr6wKzjgzV7WbX4W2NQ-DalPyBa9OdrYr-QHkZLlghEPn9QizMzqayA_v_w2EOlTAypMdVm71p9ueq8_0bMPZ8OQxaqHy5kDKZ7XljbeXIB2GB2LHsGneW6XDz_rdKfldf478i6T5Muho/s1600/brigade_erpt_sponza.jpg)![](../../assets/df6e736b42f7d0ff.jpg)

![](../../assets/df6e736b42f7d0ff.jpg)

[http://pages.cs.wisc.edu/~yu-chi/research/pmc-er/PMCER_files/pmc-er-egsr.pdf](http://pages.cs.wisc.edu/~yu-chi/research/pmc-er/PMCER_files/pmc-er-egsr.pdf).On a side note, the Sponza scene in the video renders very fast for the given resolution and hardware. When comparing this with

## 9 comments:

The new method looks very good but is it fast enough to allow animation?

I don't know. I think we should wait and see. What interests me is if they got rid of the caustic artifacts produced by glass objects, as can be seen in the ERPT implementation paper.

I think that the caustic artifacts in the ERPT implementation paper may come from an error in Equal Deposition Flow procedure. Deposition value is computed from the initial Monte Carlo samples, which is incorrect in my opinion. It should be computed for each mutated sample. Consider the situation in which an initial MC sample has large energy of red color. During path mutation we found a path that also has large energy, but coloured as blue.

Since acceptance probability works on luminance and MC path density it will accept this kind of mutated sample. Practically speaking it leads to spreading red energy over the pixels that should be blue. In effect we can see things like unexpected coloured spots and even blurred textures.

Thanks for this elaborate answer Anonymous. This is very interesting and after re-reading I think I can follow your reasoning. Maybe you could post David Cline or Christopher Batty (authors of ERPT paper and Implementing ERPT paper) and point them to this error.

To be clear, the line





"depVal(r,g,b) = e/lum(e)*e_d/samplesPerPixel"

should be removed from EqualDepositionFlow in the ERPT implementatino paper, and the line

"deposit depVal at y"

should be replaced with the line

"deposit f(y)/lum(f(y))*e_d/samplesPerPixel".

This leads to spread correct amount of total energy, and to distributing single unit of energy in each iteration over correct range of colors.

Yes, I want to point authors to this error and even few more issues. I was thinking about writing a paper containing complete set of clarificatinos, but at this moment I got stuck with my implementation of ERPT. I have troubles with understanding few issues which are not explicitly discussed in the papers. Maybe you can help me a little?

1) What they exactly mean by 'mutations per pixel'. There is something like 'chain length', which varies from 100 to 1000. Another value is 'k', from the original paper, used in estimation of 'e_d'. They call 'k' to be the desired number of mutations per corellated integral. One way to think about 'k' is that 'k' approximates the average number of mutations performed per pixel by ERPT during its whole runtime. In other words, 'k' ~ totalMutationsPerformed / numberOfPixels. But now, consider the parameters of the high quality rendering (192 MC samples and 800 mutations per pixel) in the original paper. Interpretation just described means that there was around 192/800 ~ 4 mutations performed per each MC sample. Since we are making mutation chains of length 100+, a lot of MC samples did not get mutated and energy from these samples did not get redistributed. I am not sure that it is correct behaviour. Maybe it is correct if we do not divide final pixel estimates by the number of MC samples per pixel (algorithm in the original paper does not do this division). However, the Batty's paper indicates this division to be correct. Obviously, the more MC samples are given to ER sampler the final image gets darker and darker, according to this division and fixed number of desired mutations per pixel manually stated by the user. But again, without this division I am not sure that algorithm makes sense.

2) Another issue involves mutation strategies. All the papers I have read about MLT and ERPT, describe mutation strategies, and rules of computing the relative path density to be dependent only on geometrical terms of the probability density function in path space. It seems like the relative path density in the ER sampler is insensitive for the probability of choosing specified scattering mode (i.e. for materials including different types of reflections). If we include this probability to the density change rules then the ratio of transition probabilities T(x|y) and T(y|x) may sometimes get changed significantly leading Markov chains to completely different stationary distribution. All of the papers says nothing about it. Maybe mutation strategies are good just as they are described. Maybe the reader must be bright enough to figure out what to do with materials containing more than one componenet (i.e. diffuse and specular reflections at once).

I hope I have not written to much... and I hope you will reply :)

Best regards.

To be clear, the line



"depVal(r,g,b) = e/lum(e)*e_d/samplesPerPixel"

should be removed from EqualDepositionFlow in the ERPT implementatino paper, and the line

"deposit depVal at y"

should be replaced with the line

"deposit f(y)/lum(f(y))*e_d/samplesPerPixel".

This leads to spread correct amount of total energy, and to distributing single unit of energy in each iteration over correct range of colors.

Yes, I want to point authors to this error and even few more issues. I was thinking about writing a paper containing complete set of clarificatinos, but at this moment I got stuck with my implementation of ERPT. I have troubles with understanding few issues which are not explicitly discussed in the papers. Maybe you can help me a little?

[to be continued]

1) What they exactly mean by 'mutations per pixel'. There is something like 'chain length', which varies from 100 to 1000. Another value is 'k', from the original paper, used in estimation of 'e_d'. They call 'k' to be the desired number of mutations per corellated integral. One way to think about 'k' is that 'k' approximates the average number of mutations performed per pixel by ERPT during its whole runtime. In other words, 'k' ~ totalMutationsPerformed / numberOfPixels. But now, consider the parameters of the high quality rendering (192 MC samples and 800 mutations per pixel) in the original paper. Interpretation just described means that there was around 192/800 ~ 4 mutations performed per each MC sample. Since we are making mutation chains of length 100+, a lot of MC samples did not get mutated and energy from these samples did not get redistributed. I am not sure that it is correct behaviour. Maybe it is correct if we do not divide final pixel estimates by the number of MC samples per pixel (algorithm in the original paper does not do this division). However, the Batty's paper indicates this division to be correct. Obviously, the more MC samples are given to ER sampler the final image gets darker and darker, according to this division and fixed number of desired mutations per pixel manually stated by the user. But again, without this division I am not sure that algorithm makes sense.

2) Another issue involves mutation strategies. All the papers I have read about MLT and ERPT, describe mutation strategies, and rules of computing the relative path density to be dependent only on geometrical terms of the probability density function in path space. It seems like the relative path density in the ER sampler is insensitive for the probability of choosing specified scattering mode (i.e. for materials including different types of reflections). If we include this probability to the density change rules then the ratio of transition probabilities T(x|y) and T(y|x) may sometimes get changed significantly leading Markov chains to completely different stationary distribution. All of the papers says nothing about it. Maybe mutation strategies are good just as they are described. Maybe the reader must be bright enough to figure out what to do with materials containing more than one componenet (i.e. diffuse and specular reflections at once).


I hope I have not written to much... and I hope you will reply :)

Best regards.

Hi once again anonymous. I wish I could help, but I am not a programmer, and I don't know the mathematical concepts behind erpt and mlt, though I understand the theory behind it relatively well. The blog post about ERPT on GPUs is about the work of Dietger van Antwerpen (not me to be clear). He is currently a student at the Technische Universiteit Delft, the Netherlands. Maybe he can help you with the implementation aspects of ERPT. I think the best way to contact him is through replying on one of his youtube video's (Youtube username is Dietger86) or PM via the www.ompf.org forum (username is Dietger), you will first have to register on that forum of course. I hope this could be of help. Cheers

Post a Comment