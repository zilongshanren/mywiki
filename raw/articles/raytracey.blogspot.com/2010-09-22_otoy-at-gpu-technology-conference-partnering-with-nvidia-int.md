---
title: OTOY at GPU Technology Conference, partnering with Nvidia, Intel and AMD
url: http://raytracey.blogspot.com/2010/09/otoy-at-gpu-technology-conference.html
author: Sam Lapere
published: '2010-09-22'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[a session about emerging companies](https://nvidia.confreg.com/gputechconference/schedule/by-session/4c4602a5165562e54d000068). Apparently there's no exclusive deal any longer between OTOY and AMD

[according to this article at Venturebeat.](http://venturebeat.com/2010/09/22/otoy-scores-important-deals-for-its-server-gaming-technology/)

OTOY will also make use of CUDA in the future which is great news!!! Hopefully this will speed up adoption of the technology by a factor of 10 to 50x ;-)

UPDATE: here's the full PR release:

OTOY to Present Enterprise Cloud Platform at NVIDIA GPU Technology Conference

OTOY will unveil its Enterprise Cloud platform at the GPU Technology Conference this week. The platform is designed to enable developers to leverage NVIDIA CUDA, PhysX and Optix technologies through the cloud.

Santa Clara, CA (PRWEB) September 23, 2010

OTOY announced that it will unveil its Enterprise Cloud platform at the GPU Technology Conference this week. The platform is designed to enable developers to leverage NVIDIA CUDA, PhysX and Optix technologies through the cloud. OTOY's proprietary ORBX GPU codec will enable high performance 3D applications to render on a web server and instantly stream to any thin client.OTOY is participating in the GTC “Emerging Companies Summit,” a two-day event for developers, entrepreneurs, venture capitalists, industry analysts and other professionals.

OTOY Enterprise Cloud platform


The OTOY Enterprise Cloud platform sandboxes an application or virtual machine image without degrading or limiting GPU performance. CUDA-powered applications, such as Adobe's Creative Suite 5, will be able to take full advantage of GPU acceleration while streaming from a virtual OTOY session.OTOY bringing GPGPU to the browser


In addition to supporting CUDA through its server platform, OTOY's 4k web plug-in adds CUDA and OpenCL compliant scripting across all major web browsers, including Internet Explorer, Mozilla FireFox, Google Chrome, Apple Safari and Opera. GPU web applets that cannot run locally are executed and rendered using OTOY server side rendering. This ensures that GPU web applets can be viewed on any client, including HTML 4 browsers.Next generation rendering tools coming to developers


OTOY enables server hosted game engines to render LightStage assets and leverage distributed GPU ray-tracing or path-tracing in the cloud. The OTOY Enterprise Cloud platform can host complete game engine SDKs, making game deployment to Facebook or other web portals simple and instantaneous.OTOY will add native support for CryEngine content in 2011, starting with Avatar Reality's Blue Mars. Blue Mars is the first virtual world built using the Crytek engine. It is currently in beta testing on the OTOY platform.

About OTOY


OTOY is a leading developer of innovative software solutions for GPU and CPU hardware, as well as a provider of convergence technologies for the video game and film industries. OTOY works with a wide range of movie studios, game developers, hardware vendors and technology companies.[http://www.prweb.com/releases/2010/09/prweb4551884.htm]

## 6 comments:

I don't understand, does this mean an end to the deal of using otoy with the amd fusion render cloud?

Good question! FRC was supposed to launch in summer 2009, was then postponed to Q2 2010 (which ended a month ago) after the deal with Super Micro, so who knows? Maybe we will see a voxel ray traced Ruby demo using the CUDA version of OTOY at Kepler's launch! ;-) *fingers crossed*

Many thanks for your reply


I am not so sure about this Ruby voxel demo. Look back when Jules Urbach first showed us New York city in that scene with ruby that looked completely real. The one where people thought it was a video of New York city and couldn't believe it was 100% ray traced running in real time off 1x 2GB ATI radeon GPU using voxels. AMD had talked about releasing the demo for consumers who have an ATI card. This was ever released. Maybe because 100% real time ray tracing with the graphics we were seeing are just not possible. I mean look at Nvidia's attempts. They just can't even create a demo that is even close to those graphics which were shown a few years ago right to this day. Probably because the AMD demo just may not of been real. I really don't know, what do you think?

That's a very good remark and something I have been wondering about myself a lot(believe me).




Nvidia's ray tracing and path tracing demo's (like Design Garage that came with Fermi) are calculating the GI solution in real-time, i.e. nothing is precomputed, and GPUs are still not powerful enough to render noiseless path traced GI in real-time.

The GI in the Ruby demo was precomputed (see this article at TechCrunch: http://techcrunch.com/2008/08/20/the-truth-behind-liveplaces-photo-realistic-3d-world-and-otoys-rendering-engine/ there is a bunch of other info about the demo as well), so this explains why it could be rendered at such quality in real-time. The raytracing is only used for determining which voxel should be displayed at a given pixel (raycasting) and for some of the reflections in the windows.

The reason why the demo was not released to the public is unclear to me. I've talked to Jules myself last year and I remember it had something to do with the code running into trouble with AMD CAL (AMD's own GPGPU API before OpenCL was introduced), which doesn't surprise me if you read the harsh criticism of Vlado (from Chaos Group) and Dade (from LuxRender) on the lamentable state of AMD's OpenCL implementation: it's "buggy, crashes all the time and refuses to compile" In short, it's a OpenCLusterfuck :-)

Haaah! OTOY is now using CUDA!

Normal, considering the crappy state of ATI's OpenCL implementation.

Yeah exactly. ATI is screwing up big time in GPU computing, that's why they never talk about it and put all emphasis on games.

Post a Comment