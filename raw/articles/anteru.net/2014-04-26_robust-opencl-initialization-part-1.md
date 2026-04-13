---
title: 'Robust OpenCL initialization, part #1'
url: https://anteru.net/blog/2014/robust-opencl-initialization-part-1
published: '2014-04-26'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Initializing and using OpenCL is a bit tricky, in particular on Windows and Linux, which don’t come with OpenCL installed out of the box. Unlike OpenGL, which is always present, you cannot simply link against OpenCL and hope your application to even start, as it may not be present on the target machine at all. If you plan to ship an application which uses OpenCL, you’ll need a robust way to detect if OpenCL is present and usable.

## OpenCL initialization problems & solutions

As mentioned above, the first problem we have to solve is to find out whether OpenCL is present at all. The problem is that when you develop an OpenCL application, you typically work with a stub library. This stub library is the ICD, or [Installable Client Driver](http://www.khronos.org/registry/cl/extensions/khr/cl_khr_icd.txt), a small library responsible for dispatching the function calls to the OpenCL implementations. When your application starts up, the ICD searches for installed OpenCL platforms and loads them on your behalf. That’s the theory at least. In practice, you’ll run into two separate problems with the ICD: It may not be present at all, and if it is present, it may have the wrong version.

First one is easy, if you run on a fresh installation of Windows for example, there is no ICD at all, so your application will fail loading it and most likely crash right away. The second problem is similar, your application will start loading, but crash due to a missing import.

Fortunately, there is a good solution for the ICD problem. Instead of relying on some ICD, you can ship the [Khronos ICD](http://www.khronos.org/news/permalink/opencl-installable-client-driver-icd-loader) with your application (the license specifically allows to redistribute the binary without restriction.) It’s a tiny library, built with [CMake](http://cmake.org/), which provides the complete OpenCL 1.2 ICD loader. By using this, you can at least guarantee that the ICD will be present on the target machine.

That brings us to the second problem, and that is to determine if the OpenCL implementation works. Even if the ICD is present, various stuff may still fail. The driver configuration can be broken, the driver may not be installed properly, or initializing OpenCL will simply crash. While these issues are less common, you’ll still want to guard against them.

There’s only one really good solution I can think of, which is also used by Adobe, as far as I know. What you do is you start a “test” process which tries to initialize an OpenCL context, and you check the return value of this process. If it exits normally and returns success, you consider OpenCL to be available and then you load your own compute library which is linked directly against OpenCL. If the process fails, you fall back to another implementation.

## Conclusion

For the most robust OpenCL initialization, you’ll want to use both solutions outlined above:

**Ship your own ICD**: This guarantees that you have a working ICD, and that this ICD has the version you expect.**Run a check process**to test the waters: This will safeguard you against incomplete driver installations and other problems.

It’s also a good idea to check the driver version reported by the OpenCL platform. If you know that some bug got fixed in a particular driver version, I would recommend to have a simple whitelist of vendors and driver versions and just use your fallback path if you find a known bad driver version.

In practice, you’ll always find an ICD, as AMD, Intel and NVIDIA all ship OpenCL with their drivers. The most common problem you’ll encounter is an outdated ICD (NVIDIA ships with OpenCL 1.1 only, and that includes their ICD) or a broken driver.

In case you have any questions, feel free to comment or send me a mail.

**Update**: For Optimus & other hybrid graphics initialization woes, make sure to check out [part #2](https://anteru.net/blog/2014/04/28/2377/).