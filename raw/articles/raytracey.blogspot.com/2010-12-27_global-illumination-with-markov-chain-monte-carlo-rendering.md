---
title: Global illumination with Markov Chain Monte Carlo rendering in Nvidia Optix
  2.1 + Metropolis Light Transport with participating media on GPUs
url: http://raytracey.blogspot.com/2010/12/markov-chain-monte-carlo-in-optix-21.html
author: Sam Lapere
published: '2010-12-27'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Optix 2.1 was released a few days ago and includes a Markov Chain Monte Carlo (MCMC) sample, which only works on Fermi cards (New sample: MCMC - Markov Chain Monte Carlo method rendering. A global illumination solution that requires an SM 2.0 class device (e.g. Fermi) or higher).


MCMC rendering methods, such as MLT (Metropolis light transport) and ERPT (energy redistribution path tracing) are partially sequential because each path of a Markov chain depends on the previous path and is therefor more difficult to parallellize for GPUs than standard Monte Carlo algorithms. This is an image of the new MCMC sampler included in the new Optix SDK, which can be downloaded from


MCMC rendering methods, such as MLT (Metropolis light transport) and ERPT (energy redistribution path tracing) are partially sequential because each path of a Markov chain depends on the previous path and is therefor more difficult to parallellize for GPUs than standard Monte Carlo algorithms. This is an image of the new MCMC sampler included in the new Optix SDK, which can be downloaded from

[http://developer.nvidia.com/object/optix-download.html](http://developer.nvidia.com/object/optix-download.html).![](../../assets/5f8f6cbfc9c0d094.png)


![](../../assets/5f8f6cbfc9c0d094.png)

There is also an update on the Kelemen-style Metropolis Light Transport GPU renderer from Dietger van Antwerpen. He has released this new video showing Metropolis light transport with participating media running on the GPU:


[http://www.youtube.com/watch?v=3Xo0qVT3nxg](http://www.youtube.com/watch?v=3Xo0qVT3nxg)![](../../assets/6108c167eca0eb3c.jpg)


![](../../assets/6108c167eca0eb3c.jpg)

This scene is straight from the original Metropolis light transport paper from Veach and Guibas (


## 2 comments:

Its a really wonderful Blog. With regards to effectiveness, LED grow light triumph yet again. Plants are actually only capable of using 10% of the powerfully bright light that HID bulbs radiate.

Man, those plants are really power-inefficient creatures, they could learn a lesson or two from ARM I suppose. Thanks for the nice spam Samual!

Post a Comment