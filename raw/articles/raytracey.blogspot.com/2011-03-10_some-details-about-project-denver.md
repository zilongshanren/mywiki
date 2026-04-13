---
title: Some details about Project Denver
url: http://raytracey.blogspot.com/2011/03/some-details-about-project-denver.html
author: Sam Lapere
published: '2011-03-10'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

-

[http://www.brightsideofnews.com/news/2011/3/9/nvidia-reveals-64-bit-project-denver-cpu-silicon-die.aspx](http://www.brightsideofnews.com/news/2011/3/9/nvidia-reveals-64-bit-project-denver-cpu-silicon-die.aspx)

-

[http://www.brightsideofnews.com/news/2011/3/8/nvidia-project-denver-is-a-64-bit-arm-processor-architecture.aspx](http://www.brightsideofnews.com/news/2011/3/8/nvidia-project-denver-is-a-64-bit-arm-processor-architecture.aspx)

Some interesting bits:

Fermi can apparently run a custom version of Linux:

"Thus, we don't expect Project Denver to appear before late 2012 or early 2013 - in line with Maxwell GPU architecture, which is expected to integrate Project Denver architecture and become the first shipping GPU which could boot an operating system. It would not be the first GPU to boot an operating system, though. According to several PR representatives, the company already managed to boot a special build of Linux using Fermi GPU, but resources for that were abandoned as it proved too much of a hassle."

"In theory, Project Denver cores inside the Maxwell GPU die should enjoy access to 2+TB/s of internal bandwidth and potentially beyond currently possible 320GB/s of external memory bandwidth (using 512-bit interface and high-speed GDDR5 memory). If nVidia delivers this architecture as planned, we might see quite a change in the market - given that neither CPUs from AMD or Intel don't have as high system bandwidth as contemporary graphics cards."

With such extremely fast memory bandwidth between the ARM CPU and the Maxwell GPU (both on the same die), real-time ray tracing of dynamic scenes will benefit greatly because building and rebuilding/refitting of acceleration structures (such as BVHs) is still best handled by the CPU (although there are parallel implementations already, see the

David Luebke (Nvidia graphics researcher and GPU ray tracing expert) said in a


[HLBVH](http://research.nvidia.com/publication/hlbvh-hierarchical-lbvh-construction-real-time-ray-tracing)paper by Pantaleoni and Luebke or the[real-time kd-tree construction](http://graphics.cs.umass.edu/pubs/siggraph09_paper0448.pdf)paper by Rui Wang et al.)David Luebke (Nvidia graphics researcher and GPU ray tracing expert) said in a

[chat session](http://blogs.nvidia.com/2010/09/live-chat-qa-with-bill-dally-and-david-luebke/)preceding the GTC 2010 conference in September:"I think Jacopo Pantaleoni's "HLBVH" paper at High Performance Graphics this year will be looked back on as a watershed for ray tracing of dynamic content. He can sort 1M utterly dynamic triangles into a quality acceleration structure at real-time rates, and we think there's more headroom for improvement. So to answer your question, with techniques like these and continued advances in GPU ray traversal, I would expect heavy ray tracing of dynamic content to be possible in a generation or two."

## No comments:

Post a Comment