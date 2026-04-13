---
title: 'Getting started with OpenCL, Part #1'
url: https://anteru.net/blog/2012/getting-started-with-opencl-part-1
published: '2012-11-03'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Welcome to a short series on how to get started with OpenCL. I assume that you are a developer, you know what OpenCL is and you want to get up to speed quickly. We’ll be building a small example application with OpenCL which will eventually be able to apply a blur filter on an image. You can find the [complete source code in my Git repository](https://github.com/anteru/opencltutorial). In this part, we’ll prepare everything so we can actually use OpenCL. You should fetch [the corresponding code](https://github.com/Anteru/opencltutorial/tree/6354f82a4201fa7cadf1362ff8a248a39e142a39) to follow along easily. The second part covers how to run a simple kernel, and the third part does a slightly more complicated example where an image is processed.

First of all, a quick overview of how OpenCL actually works. OpenCL comes as a runtime environment and has to be installed on your target machine, no matter if you are using Windows or Linux. For Mac OS X, OpenCL is already part of the system, so there is nothing to install there. The runtime installs two things: First, a dispatch library and then the actual runtime containing the implementation. The dispatch library is necessary as there is typically more than one runtime present on a machine. For instance, there might be the AMD CPU runtime and an NVIDIA GPU runtime installed at the same time. The dispatcher makes sure that they don’t overwrite each other.

To get started, you need to be able to link against this dispatch library, called `OpenCL.dlld`

on Windows. Every OpenCL SDK comes with an `OpenCL.libd`

which allows exactly for that. The most important OpenCL SDKs right now are:

- The
[Intel SDK](http://software.intel.com/en-us/vcsource/tools/opencl-sdk), which works on newer Intel CPUs and integrated graphics units from Intel. It comes with OpenCL 1.2 support. - The
[AMD APP SDK](http://developer.amd.com/tools/hc/AMDAPPSDK/downloads/Pages/default.aspx), which works on any CPU (both AMD and Intel) and on AMD GPUs. It supports OpenCL 1.2 as well. - The
[NVIDIA GPU SDK](https://developer.nvidia.com/gpu-computing-sdk), which works on NVIDIA GPUs only and supports only OpenCL 1.1.

No matter which one you choose, you have to make sure that the `OpenCL.libd`

is found by your linker and that the headers are in your include path. For the example project, I’ll be using CMake, so we need a FindOpenCL.cmake which does the search. Feel free to grab [the one from the repository](https://github.com/Anteru/opencltutorial/blob/682cea05d2f9d21340987a8de3f42c2c5fa84fd6/cmake/FindOpenCL.cmake). If you are not familiar with CMake, then take a look at [the CMake tutorial first](http://www.cmake.org/cmake/help/cmake_tutorial.html).

Assuming that OpenCL got found correctly, you can now include the OpenCL header it in your source code. The exact path depends on whether you are using Mac OS X or not:

```
#ifdef __APPLE__
#include "OpenCL/opencl.h"
#else
#include "CL/cl.h"
#endif
```


That’s all, OpenCL is completely contained in a single header. The API is written in C, and while there is a C++ wrapper, we’ll be using the C API only for this example. Don’t worry, it’s not too hard or overly verbose. Before we get started with actual code, grab a [copy of the specification](http://www.khronos.org/registry/cl/specs/opencl-1.1.pdf). It contains a reference of all functions, error codes, and structures; making it very handy. In particular, the error codes for each function are well explained and make it easy to understand why a particular call fails.

Remember the dispatch library mentioned above which allows choosing between different implementations? This is exactly how we’ll start. An implementation is called a *platform* in OpenCL; each platform can contain multiple *devices*. A device is where the code actually gets executed in the end; notice that each device in the same platform can support different features. For instance, if you have the AMD runtime installed and an AMD CPU and GPU, both will appear under the AMD platform but the GPU might support a different OpenCL version and extensions than the CPU. For this example, we’ll use only core OpenCL 1.1 features, which are available virtually everywhere, but keep this in mind for the future.

We begin by querying what platforms are available:

```
cl_uint platformIdCount = 0;
clGetPlatformIDs (0, nullptr, &platformIdCount);
std::vector<cl_platform_id> platformIds (platformIdCount);
clGetPlatformIDs (platformIdCount, platformIds.data (), nullptr);
```


All OpenCL APIs follow the same scheme; in this case, we call the function first with an empty output to obtain the number of numbers. After that, we can fetch the platforms in a correctly sized buffer.

We don’t care in particular about which platform we’re going to use, so we continue directly by querying the devices for the first platform we’ve found. Notice how strikingly similar the code is:

```
cl_uint deviceIdCount = 0;
clGetDeviceIDs (platformIds [0], CL_DEVICE_TYPE_ALL, 0, nullptr,
&deviceIdCount);
std::vector<cl_device_id> deviceIds (deviceIdCount);
clGetDeviceIDs (platformIds [0], CL_DEVICE_TYPE_ALL, deviceIdCount,
deviceIds.data (), nullptr);
```


Now we have found a device, which means we can finally run some computation on it? Not so fast, to actually use it, two more things are needed. A context, which manages resources on a set of devices, and a command queue which executes the commands. This is separated so you can create all resources up-front using only the context, and then create multiple queues on the same device to submit work from multiple threads.

Creating a context is straightforward:

```
const cl_context_properties contextProperties [] =
{
CL_CONTEXT_PLATFORM,
reinterpret_cast<cl_context_properties> (platformIds [0]),
0, 0
};
cl_context context = clCreateContext (
contextProperties, deviceIdCount,
deviceIds.data (), nullptr,
nullptr, &error);
```


From here on, we’ll also check for errors. Every function that can fail in OpenCL returns an error code, either via an output parameter (if the function creates an object) or directly as the return value. We will check that this error value is set to `CL_SUCCESS`

, which indicates that the call worked and exit the application otherwise.

Remember that resources like the context have to be cleaned up later on, by using the appropriate release method. Every resource is reference counted, after the creation, it starts with one reference. The reference count can be increased using the `clRetain*d`

methods and decreased using `clRelease*d`

. There’s no need to release the platform or the devices, but everything else must be cleaned up.

At this point, we have a context ready, now we need a queue as well, which is equally easy to create. If you followed along so far, you have done everything necessary to set up OpenCL and now you’re ready to get some work done; we’ll take a look at how to actually run code in the second part of this introduction.