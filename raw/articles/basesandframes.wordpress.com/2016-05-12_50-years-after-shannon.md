---
title: 50+ Years after Shannon
url: https://basesandframes.wordpress.com/2016/05/12/50-years-after-shannon/
author: Robingreen
published: '2016-05-12'
source_blog: Bases and Frames
source_site: https://basesandframes.wordpress.com
category: graphics
fetched: '2026-04-13'
---

Inspired by Michael Unser’s IEEE paper * Sampling – 50 Years After Shannon* I set out to explain the ideas and innovation to the gamedev audience. The resulting presentation ended up a bit too math heavy for my liking and needs more worked examples, but it’s a good motivation to learn more about bi-orthogonality of bases.

If you learned the mathematical basis for Shannon Sampling Theory in college, the latest theory of Generalized Sampling replaces a few of the blocks in the classic Shannon diagram to guarantee perfect reconstruction for finite signals if you have control over both the analysis and synthesis functions.

In the real world you usually don’t have the ability to fine tune reconstruction (e.g. the point-spread function in a TV image or the acoustics of a cellphone speaker) so a less severe goal called *Consistent Reconstruction* can be used where the goal is to optimize one of either the sampling or reconstruction filters so that feeding the output signal back through the system leads to the same result. To do this we add a filter into the Shannon diagram that we can optimize to give this property and this gives us close to perfect reconstruction for any sampled signal in real world usage; for example the 100Hz temporal upsampling in your digital TV works using this theory.

Hughes Hoppe and Diego Nahib also took a look into generalized sampling and specifically some uses in computer graphics, available as Microsoft Research Technical Report MSR-TR-2011-16 * Generalized Sampling in Computer Graphics*.