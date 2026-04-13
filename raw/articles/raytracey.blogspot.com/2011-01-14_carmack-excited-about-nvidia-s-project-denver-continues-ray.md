---
title: Carmack excited about Nvidia's Project Denver, continues ray tracing research
url: http://raytracey.blogspot.com/2011/01/carmack-excited-about-nvidias-denver.html
author: Sam Lapere
published: '2011-01-14'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Nvidia's recently announced move into CPU territory with Project Denver has been very well received by the general public. Game developers (who have known about this project for over a year) like John Carmack have also expressed interest. Most people are tired of the current x86 duopoly held by AMD and Intel, and for them this archaic 30+ years old legacy technology cannot die fast enough. Carmack is especially happy about Nvidia's choice for ARM because he is already familiar with coding for the ARM CPUs in mobile devices like Apple's iPhone and Google's Android.


From

[his twitter acount](http://twitter.com/ID_AA_Carmack):

"I have quite a bit of confidence that Nvidia will be able to make a good ARM core. Probably fun for their engineers."

"Goal for today: parallel implementation of my TraceWorld Kd tree builder"

"10mtri model got 2.5x faster on 1 thread, 19x faster on 24 (hyper)threads."

"Amdahl’s law is biting pretty hard at the start, with only being able to fan out one additional thread per node processed."

As can be seen from his twitter entries, he also restarted his research on ray tracing. One specific thing to note is that he's talking about Amdahl's law. I first saw this law in a Siggraph 2008 presentation by Jon Olick on parallelism, and it is something that will be hampering traditional rasterization more than raycasting/raytracing. From wikipedia (Amdahl's law):


"The speedup of a program using multiple processors in parallel computing is limited by the time needed for the sequential fraction of the program. For example, if 95% of the program can be parallelized, then the theoretical maximum speedup using parallel computing would be 20 times faster, no matter how many processors are used. "

And a few thoughts related to Amdahl's law from Carmack's talk at QuakeCon 2010 in August (see


[http://raytracey.blogspot.com/2010/08/is-carmack-working-on-ray-tracing-based.html](http://raytracey.blogspot.com/2010/08/is-carmack-working-on-ray-tracing-based.html)), implying that current GPUs, no matter how powerful, can only speed up the code to a certain extent and that scalability on multi-core CPUs is better (because contrary to the GPU, multi-core CPUs can speed up the serial code parts as well):"so I’m going through a couple of stages of optimizing our internal raytracer, (TreeWorld used for precomputing the lightmaps and megatextures, not for real-time purposes) this is making things faster and the interesting thing about the processing was, what we found was, it’s still a fair estimate that the GPUs are going to be five times faster at some task than the CPUs. But now everybody has 8 core systems and we’re finding that a lot of the stuff running software on this system turned out to be faster than running the GPU version on the same system. And that winds up being because we get killed by Amdahl’s law there where you’re throwing the very latest and greatest GPU and your kernel amount (?) goes ten times faster. The scalability there is still incredibly great, but all of this other stuff that you’re dealing with of virtualizing of textures and managing all of that did not get that much faster. So we found that the 8 core systems were great and now we’re looking at 24 thread systems where you’ve got dual thread six core dual socket systems. It’s an incredible amount of computing power and that comes around another important topic where PC scalability is really back now "

Nvidia's project Denver is very important in this respect and will bring the theoretical maximum speedup (limited by Amdahl's law) much closer to reality, because CPU cores and GPU cores are located on the same chip and are not depending on any bandwidth restrictions. The ARM CPU cores will take care of the latency sensitive sequential parts of the code, while the CUDA cores will happily blast through the parallel code. For ray tracing in particular, this means that the ARM CPU cores will be able to dynamically build acceleration structures and speed up tree traversal for highly irregular workloads with random access, and that the plentiful CUDA cores will do ray-triangle intersection and BRDF shading at amazing speeds. This will make the Denver chip a fully programmable ray tracing platform which greatly accelerates all stages of the ray tracing pipeline. In short, a wet dream for ray tracing enthusiasts like myself :D! Based on the power-efficient ARM architecture, I think that Denver-derived chips will also be the platform of choice for cloud gaming services, for which heat and power inefficiency from the currently used x86 CPUs are creating a huge problem.


## No comments:

Post a Comment