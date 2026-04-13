---
title: 'OpenCL path tracing tutorial 1: Firing up OpenCL'
url: http://raytracey.blogspot.com/2016/11/opencl-path-tracing-tutorial-1-firing.html
author: Sam Lapere
published: '2016-11-01'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

This is the first tutorial in a new series of GPU path tracing tutorials which will focus on OpenCL based rendering. The first few tutorials will cover the very basics of getting started
with OpenCL and OpenCL based ray tracing and path tracing of simple
scenes. Follow-up tutorials will use a cut-down version of

[AMD's RadeonRays framework](http://developer.amd.com/tools-and-sdks/graphics-development/radeonpro/radeonrays-technology-developers/)(the framework formerly known as FireRays), to start from as a basis to add new features in a modular manner. The goal is to incrementally work up to include all the features of RadeonRays, a full-featured GPU path tracer. The[Radeon Rays source](https://github.com/GPUOpen-LibrariesAndSDKs/RadeonRays_SDK)also forms the basis of AMD's Radeon ProRender Technology (which will also be integrated as a native GPU renderer in an[upcoming version of Maxon's Cinema4D](https://www.maxon.net/en/news/maxon-blog/article/the-future-of-rendering/)). In the end, developers that are new to rendering should be able to code up their own GPU renderer and integrate it into their application.**Why OpenCL?**

The major benefit of OpenCL is its platform independence, meaning that the same code can run on CPUs and GPUs made by AMD, Nvidia and Intel (in theory at least, in practice there are quite a few implementation differences between the various platforms). The tutorials in this series should thus run on any PC, regardless of GPU vendor (moreover a GPU is not even required to run the program).

Another advantage of OpenCL is that it can use all the available CPU and GPUs in a system simultaneously to accelerate parallel workloads (such as rendering or physics simulations).

In order to achieve this flexibility, some boiler plate code is required which selects an OpenCL platform (e.g. AMD or Nvidia) and one or more OpenCL devices (CPUs or GPUs). In addition, the OpenCL source must be compiled at runtime (unless the platform and device are known in advance), which adds some initialisation time when the program is first run.

**OpenCL execution model quick overview**

This is a superquick overview OpenCL execution model, just enough to get started (there are plenty of more exhaustive sources on OpenCL available on the web).

In order to run an OpenCL program, the following structures are required (and are provided by the OpenCL API):

**Platform**: which vendor (AMD/Nvidia/Intel)**Device**: CPU, GPU, APU or integrated GPU**Context**: the runtime interface between the host (CPU) and device (GPU or CPU) which manages all the OpenCL resources (programs, kernels, command queue, buffers). It receives and distributes kernels and transfers data.**Program**: the entire OpenCL program (one or more kernels and device functions)**Kernel**: the starting point into the OpenCL program, analogous to the main() function in a CPU program. Kernels are called from the host (CPU). They represent the basic units of executable code that run on an OpenCL device and are preceded by the keyword "__kernel"**Command queue**: the command queue allows kernel execution commands to be sent to the device (execution can be in-order or out-of-order)**Memory objects**: buffers and images

These structures are summarised in the diagram below (slide from AMD's

[Introduction to OpenCL programming](http://amd-dev.wpengine.netdna-cdn.com/wordpress/media/2013/01/Introduction_to_OpenCL_Programming-201005.pdf)):
![]() |

**OpenCL memory model quick overview**

The full details of the memory model are beyond the scope of this first tutorial, but we'll cover the basics here to get some understanding on how a kernel is executed on the device.

There are four levels of memory on an OpenCL device, forming a memory hierarchy (from large and slow to tiny and fast memory):

**Global memory (similar to RAM)**: the largest but also slowest form of memory, can be read and written to by all work items (threads) and all work groups on the device and can also be read/written by the host (CPU).**Constant memory**: a small chunk of global memory on the device, can be read by all work items on the device (but not written to) and can be read/written by the host. Constant memory is slightly faster than global memory.**Local memory (similar to cache memory on the CPU)**: memory shared among work items in the same work group (work items executing together on the same compute unit are grouped into work groups). Local memory allows work items belonging to the same work group to share results. Local memory is much faster than global memory (up to 100x).**Private memory (similar to registers on the CPU)**: the fastest type of memory. Each work item (thread) has a tiny amount of private memory to store intermediate results that can only be used by that work item

**First OpenCL program**

With the obligatory theory out of the way, it's time to dive into the code. To get used to the OpenCL syntax, this first program will be very simple (nothing earth shattering yet): the code will just add the corresponding elements of two floating number arrays together in parallel (all at once).


In a nutshell, what happens is the following:


In a nutshell, what happens is the following:

- Initialise the OpenCL computing environment: create a platform, device, context, command queue, program and kernel and set up the kernel arguments
- Create two floating point number arrays on the host side and copy them to the OpenCL device
- Make OpenCL perform the computation in parallel (by determining global and local worksizes and launching the kernel)
- Copy the results of the computation from the device to the host
- Print the results to the console

The code contains plenty of comments to clarify the new syntax:

This code is also available at




[https://github.com/straaljager/OpenCL-path-tracing-tutorial-1-Getting-started](https://github.com/straaljager/OpenCL-path-tracing-tutorial-1-Getting-started)**Compiling instructions**(for Visual Studio on Windows)

To compile this code, it's recommended to download and install the

**(this works for systems with GPUs or CPUs from AMD, Nvidia and Intel, even if your system doesn't have an AMD CPU or GPU installed) since Nvidia's OpenCL implementation is no longer up-to-date.**[AMD App SDK](http://developer.amd.com/tools-and-sdks/opencl-zone/amd-accelerated-parallel-processing-app-sdk/)- Start an empty Console project in Visual Studio (any recent version should work, including Express and Community) and set to
**Release**mode - Add the SDK include path to the "
**Additional Include Directories**" (e.g. "C:\Program Files (x86)\AMD APP SDK\2.9-1\include") - In Linker > Input, add "
**opencl.lib**" to "**Additional Dependencies**" and add the OpenCL lib path to "**Additional Library Directories**" (e.g. "C:\Program Files (x86)\AMD APP SDK\2.9-1\lib\x86") - Add the
**main.cpp**file (or create a new file and paste the code) and build the project

**Download binaries**

The executable (Windows only) for this tutorial is available at



It runs on CPUs and/or GPUs from AMD, Nvidia and Intel.

[https://github.com/straaljager/OpenCL-path-tracing-tutorial-1-Getting-started/releases/tag/v1.0](https://github.com/straaljager/OpenCL-path-tracing-tutorial-1-Getting-started/releases/tag/v1.0)It runs on CPUs and/or GPUs from AMD, Nvidia and Intel.

**Useful References**

- "

**A gentle introduction to OpenCL**":

[http://www.drdobbs.com/parallel/a-gentle-introduction-to-opencl/231002854](http://www.drdobbs.com/parallel/a-gentle-introduction-to-opencl/231002854)

- "

**Simple start with OpenCL**":

[http://simpleopencl.blogspot.co.nz/2013/06/tutorial-simple-start-with-opencl-and-c.html](http://simpleopencl.blogspot.co.nz/2013/06/tutorial-simple-start-with-opencl-and-c.html)

- Anteru's blogpost,

**Getting started with OpenCL**(uses old OpenCL API)

[https://anteru.net/blog/2012/11/03/2009/index.html](https://anteru.net/blog/2012/11/03/2009/index.html)

-

**AMD introduction to OpenCL programming**:

[http://amd-dev.wpengine.netdna-cdn.com/wordpress/media/2013/01/Introduction_to_OpenCL_Programming-201005.pdf](http://amd-dev.wpengine.netdna-cdn.com/wordpress/media/2013/01/Introduction_to_OpenCL_Programming-201005.pdf)

**Up next**

In the next tutorial we'll start rendering an image with OpenCL.

## 4 comments:

Thanks for the tutorial Sam, I have always been interested in learning OpenCL and will try and follow along with your tutorials :)

I had a problem using debugging on Visual Studio, which had nothing at all to do with the code in the tutorial.





The problem was that I was using intel integrated graphics, but installed a AMD graphics card later on, so both drivers were present and one graphics card was not installed. When I went to debug (clicking the green arrow in VS), it would crash on the first OpenCL call with an "access violation" error. However if I ran the program without debugging, it ran fine.

Looking at the call stack during the crash, it showed the crash in the Intel graphics driver. I tried various things, in the end I just uninstalled the Intel graphics driver, HOWEVER, in Windows this does not completely remove the driver. First, uninstall the graphics driver normally. Then we need to remove the driver from device manager. If you are running

Windows 7 or lower, you must add an environment variable to show hidden devices - follow these instructions: https://msdn.microsoft.com/en-us/windows/hardware/drivers/install/viewing-hidden-devicesAfter this, open device manager, and click in the toolbar "view -> show view hidden devices". Then expand the "Display Adapters" screen, right click the intel graphics (should be greyed out), then click uninstall.

I'm still not sure why the crash only occurs if you enable debugging in Visual Studio, but the program runs fine without debugging. Maybe when debugging is enabled it catches more errors, and running normally it ignores the access violation error.

I think for OpenCL 2.0, a preprocessor definition need to be added: CL_USE_DEPRECATED_OPENCL_2_0_APIS. Because the OpenCL C++ wrapper as I can find from AMD website: http://developer.amd.com/tools-and-sdks/opencl-zone/, is using 2.0 deprecated function.

Im in love with the way you explained everything.. <3

Thank you for putting this tutorial up you have no idea how desperate i was for something like this..

Post a Comment