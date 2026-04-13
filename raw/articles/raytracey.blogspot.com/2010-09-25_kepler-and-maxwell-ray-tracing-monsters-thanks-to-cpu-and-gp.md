---
title: 'Kepler and Maxwell: ray tracing monsters thanks to CPU and GPU cores on the
  same chip?'
url: http://raytracey.blogspot.com/2010/09/kepler-and-maxwell-ray-tracing-monsters.html
author: Sam Lapere
published: '2010-09-25'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

At GTC 2010, Nvidia announced their future GPUs named Kepler and Maxwell. One of the more interesting quotes:

"Between now and Maxwell, we will introduce virtual memory, pre-emption, enhance the ability of the GPU to autonomously process, so that it's non-blocking of the CPU, not waiting for the CPU, relies less on the transfer overheads that we see today. These will take GPU computing to the next level, along with a very large speed up in performance," said Jen-Hsun Huang.


Pre-emption was already revealed in a slide from a presentation by Tony Tomasi at Nvision08 (


"Between now and Maxwell, we will introduce virtual memory, pre-emption, enhance the ability of the GPU to autonomously process, so that it's non-blocking of the CPU, not waiting for the CPU, relies less on the transfer overheads that we see today. These will take GPU computing to the next level, along with a very large speed up in performance," said Jen-Hsun Huang.

Pre-emption was already revealed in a slide from a presentation by Tony Tomasi at Nvision08 (

[http://www.pcper.com/article.php?aid=611](http://www.pcper.com/article.php?aid=611)), depicting a timeline showing pre-emption, full support for function pointers, C++, etc. :![](http://www.pcper.com/images/reviews/611/gpu01.jpg)


![](http://www.pcper.com/images/reviews/611/gpu01.jpg)

The part about "the ability of the GPU to autonomously process, so that it's non-blocking of the CPU, not waiting for the CPU, relies less on the transfer overheads that we see today" is very interesting and suggests the incorporation of CPU cores on the GPU, as shown in a slide from an Nvidia presentation at SC09 (

[http://www.nvidia.com/content/GTC/documents/SC09_Dally.pdf):](http://www.nvidia.com/content/GTC/documents/SC09_Dally.pdf%29:)

![](../../assets/26e6093d72b852ec.jpg)


We all know that Intel and AMD are looking at merging CPU cores and GPUs on the same die.

In my mind, the future is for hybrid computing, where different kind of processors working together and find their own kind of tasks to work on. Currently, multi-core CPU and many-core GPU are working together, tasks are distributed by software schedulers. Data parallel tasks are assigned to GPUs and task-parallel jobs are assigned to GPUs. However, communication between these two kinds of processors is the performance bottleneck. I hope NVIDIA can provide a solution on their desktop GPU product line too.Bill Dally:That's exactly right. The future is heterogeneous computing in which we use CPUs (which are optimized for single-thread performance) for the latency sensitive portions of jobs, and GPUs (which are optimized for throughput per unit energy and cost) for the parallel portions of jobs. The GPUs can handle both the data parallel and the task parallel portions of jobs better than CPUs because they are more efficient. The CPUs are only needed for the latency sensitive portions of jobs - the serial portions and critical sections.

Do you believe a time will come when GPU and CPU are on the same chip or "board" it seems the logical next step to avoid the huge PCI-E latency and have a better GPU-CPU interactivity ? i know there is ongoing research in this area already ...but what is your personal opinion on the possibility and benefits of this ?"Bill Dally:Our Tegra processors already combine CPUs and a GPU on a single chip. For interactivity what's important is not the integration but rather having a shared memory space and low latency synchronization between the two types of cores.

I don't see convergence between latency-optimized cores and throughput optimized cores. The techniques used to optimize for latency and throughput are very different and in conflict. We will ultimately have a single chip with many (thousands) of throughput cores and a few latency-optimized cores so we can handle both types of code.

From the above slide, Nvidia expects to have 16 CPU cores on the GPU by 2017, deducing from that you would get:

- 2017: GPU with 16 CPU cores

- 2015: GPU with 8 CPU cores

- 2013: Maxwell with 4 CPU cores

- 2011: Kepler with 2 CPU cores

My bet is that Kepler will at least have one and probably two (ARM based) CPU cores and Maxwell will probably have 4 CPU cores on the GPU. The inclusion of true CPU cores on the GPU will make the CPU-GPU bandwidth problem of today obsolete and will enable smarter ray tracing algorithms like Metropolis light transport and bidirectional path tracing on the GPU. Biased rendering methods such as photon mapping and irradiance caching will be easier to implement. It will also give a tremendous performance boost to the (re)building of acceleration structures and to ray tracing of dynamic geometry, which will no longer depend on the slow PCIe bus. Apart from ray tracing, most other general computation tasks will also benefit greatly. I think this CPU/GPU combo chip will be Nvidia's answer to AMD's oft-delayed Fusion and Intel's Sandy Bridge.

## 6 comments:

Nice find, i was speculating that Nvidia would have to go that direction, because if consoles are going that way so will the PC market seeing how consoles are the driving software devopment and SOC for consoles is a no brainer.



This brings to mind what intel said when they droped larrabee, "fusion is the future."

I was wondering with 3D stacking could you use L3 cache to bridge two separate dies like a 22nm CPU and 20nm GPU to create a single chip? After all AMD used to have a separate chip for SIMD and the they still use separate shedulars in their cores today.

I don't know anything about chip design, but I think the GPU and CPU cores in future Nvidia chips will be on the same die.

great blog by the way.

Thanks!

Hi! I really like you blog, I find very usefull and important info here, I don´t find any email to write to you, I wish you could publish one, I bet you will recieve many congratulations.



Good work, keep comming all the good stuff.

Thanks!

>>- 2011: Kepler with 2 CPU cores

It's 2013 and that never happened :p

Post a Comment