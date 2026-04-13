---
title: OpenCL 2.0 Review
url: https://anteru.net/blog/2013/opencl-2-0-review
published: '2013-07-23'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

This is going to be a review in the spirit of G-Truc's excellent [OpenGL reviews](http://www.g-truc.net/project-0032.html#menu). Without further ado, let's dive into the details of the new OpenCL specification. We'll take the three parts one-by-one, starting with the platform and runtime.
Platform & Runtime
==================
The platform has several new features:
* Extended image support
* Shared memory
* Pipes
* Android Driver
Let's get started with the **image support**. Image support in OpenCL used to be very basic at best, with lots of limitations like for instance not being able to read and write from the same image. This has been mostly addressed with OpenCL 2.0, which adds `read_write`

as a modifier for images, provides mip-mapped images as well as images with more than one sample per pixel, and most importantly, 3D image reads and writes. Additionally, sRGB support has been added. Still missing are writes to multi-sampled images, and mip-mapped images are only an optional feature. Interestingly, mip-mapped reads are supported for 3D textures as well, where they are really useful and hard (read: slow) to emulate otherwise.
OpenCL 2.0 also adds sharing of depth images and multi-sampled textures with OpenGL, similar to the OpenCL 1.2 extension. Unfortunately, the Direct3D11 sharing has not been updated accordingly. This is weird, as all that is required is to update the list of supported DXGI formats to add the depth formats and copy & paste the text from the OpenGL extension.
**Shared virtual memory** is an interesting feature which will most likely require new hardware. What it adds is a single address space which is shared between the host and device. Basically, you allocate a block of memory which can be read and written by both the host and the device. There are two possible implementations:
* Coarse-grained sharing: Requires you to use map and unmap the buffer for updates. Not really that interesting, all that you gain in this mode is that the pointer values are the same (if you store pointers inside the buffer, it will work on both the host and device.) This can be likely implemented on current hardware by adjusting all pointer accesses into a shared memory region on the device.
* Fine-grained sharing: No need for mapping/unmapping, things just work. With atomics, it's even possible to update parts of the data while a kernel is updating other parts. This is actually real shared memory.
I expect the fine-grained sharing to appear on integrated GPUs first (AMD APUs, Intels HD graphics.) Discrete GPUs will eventually follow, AMD should be able to do it already, while NVIDIA will follow with Maxwell. This is one of the great new features of OpenCL 2.0 and will dramatically simplify tasks which require complicated data structures (trees, etc.) For instance, I have to flatten trees to use node-relative indices right now to use them on the GPU, which can be skipped when using the shared memory features.
Next up are **pipes** which are incredibly exciting as well, as you can use them to transfer data between multiple kernel invocations. Together with the ability to enqueue kernels from the device, this is going to be awesome. It will allow real data-flow programming and load-balancing on the GPU, removing one of the biggest bottlenecks in the current model. For instance, we can now write kernels which expand data, and run the consumer kernels concurrently on the same device instead of having to run the expansion kernel first (with low utilization, but high bandwidth usage) and then run the computation kernel next (which has to fetch all data back from memory again.) This is only really useful with kernel creation on the device, but combined, the possibilities are infinite. A very nice addition!
Finally, there will be a way to load OpenCL implementations on Android systems. For anyone who used Renderscript, this is godsend :)
Language
========
On the language side, there are three major changes:
* "Generic" address space
* C11 atomics
* The awesome kernel creation and the corresponding language feature, blocks
The **generic address space** removes the need to overload functions based on address space. I have several functions which take either a local or a global pointer, which currently have to be written twice (or you use ugly macros.) With the generic address space, those functions can be written once and will work with arguments from any address space. A nice and helpful addition.
**C11 atomics** extend the current atomics and are very interesting if used in conjunction with the shared memory feature. This will allow a much tighter integration. Overall, this feature mostly extends and completes the atomic support and brings it to feature parity with C11/C++11.
**Work-group functions** add parallel primitives across a single work group. This might not sound like a big deal, but it actually is. For example, let's assume I need the min/max depth of a 2D image tile. Using work-group functions, this is easily expressed using a work-group wide reduce. The advantage here is that the hardware vendors can provide highly optimized implementations. Additionally, you get access to any/all broadcast functions, which can be used to optimize kernel execution (if for example all work-items take the same path, it might be beneficial to load data into local memory instead of fetching, things like that.)
Finally, **blocks and device kernel creation**. Blocks are simply C lambda functions, which should be familiar to users of Apple's Grand Central Dispatch. The syntax is exactly the same and pretty similar to C++ lambdas (except that you cannot capture variables.) The important part here is that they can be used to create new kernels and schedule them from within a kernel! With OpenCL 2.0, kernels can dispatch new kernels without having to go through the host. This will open completely new possibilities, where an algorithm can adapt to the work without having to go back and forth between the host. What is even more interesting that with the help of atomics, shared memory and pipes, we can now create producer-consumer queues on the device and control it from the host without ever having to do an OpenCL call after starting the kernel.
Extensions & SPIR
=================
On the extensions side, it looks quite similar to OpenCL 1.2, with most of the interesting extensions not being available on a lot of hardware. Hopefully this will improve with OpenCL 2.0, but I don't see ubiquitous support for OpenGL multi-sampled texture sharing coming to AMD and NVIDIA soon.
**SPIR** has been updated, as far as I can tell, it has been mostly cleaned up. I'm not sure why this is still not part of the core OpenCL specification, but it is the right way forward and I can't wait for implementations to support it. If done correctly, SPIR will allow you to compile all your kernels using the compiler of your choice and just ship the SPIR code instead of having to hope that the compiler on your client's machine works correctly.
Summary
=======
Overall, OpenCL 2.0 looks like a viable long-term programming target. It resolves several nasty limitations (image support, generic address space) and provides forward-looking features (shared memory, device kernel creation). What's still missing for me is proper Direct3D11 interop (all formats, read & write) and the support for the static C++ language subset that AMD is bringing forward. While not critical, it would make programming quite a bit simpler if I wouldn't have to write a stack for integers, one for floats, etc.
OpenCL 2.0 is however much more than I would have expected, given that the development seemed pretty slow over the last year. Now, I can't wait to get my hands on the first OpenCL 2.0 compliant runtime.
If I missed something, please tell me in the comments, and I'll update this blog post. This is my first OpenCL review, so if you have suggestions, please go ahead so I can make those reviews more useful in the future. Thanks!
**Update**: 2014-09-13, added work-group wide functions.