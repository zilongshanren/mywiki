---
title: Two more reasons why you should be using OpenCL
url: https://anteru.net/blog/2013/two-more-reasons-why-you-should-be-using-opencl
published: '2013-03-30'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Are you planning to add parallel computing to your application, and you wonder what API to use? Here are two good reasons why you should be using [OpenCL](http://www.khronos.org/opencl/) today. If you’re not sure what OpenCL is about, take a look at [a gentle introduction to OpenCL](https://anteru.net/blog/2012/09/19/1940/).

## CPU/GPU portability

OpenCL runs on both AMD and NVIDIA graphics cards. That’s not much different from [DirectCompute](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476331%28v=vs.85%29.aspx), so why bother with OpenCL? The cool thing here is that OpenCL also works on CPUs and on mobile devices. The fact that you can run on CPUs is often overlooked, but there are two good reasons why you really want this:

- CPUs are pretty fast these days, if you properly use the vector units. OpenCL makes this very easy and allows you to have a high-quality CPU fallback, which will guarantee that your application works reasonably for all your customers.
- CPUs typically have much more memory. If you run into a scalability problem where you cannot process the problem on your compute device any more (graphics cards currently have at most 6-8 GiB of memory), it’s trivial to run it on the CPU where memory is really cheap. For the price of a high-end consumer GPU, you can easily buy 64 GiB of ECC RAM.

The last argument is particularly important if you work on data sets which don’t partition very well. For example, if you have a renderer, it is very likely that most scenes will fit on the GPU, but if your customer decides to throw a really complicated mesh at it, you can simply switch to the CPU. Performance will likely suffer, but it will work, and it requires *no additional work* from your side. There’s no other API out there which is that flexible.

## Graphics interop

DirectX has DirectCompute, OpenGL has now compute shaders as well (in revision 4.3.) But only OpenCL allows you to use the *same* compute code with both APIs. For OpenGL, the OpenCL interop is independent of your OpenGL version (you can use OpenGL 4.0 with OpenCL, or OpenGL 3.0 for the matter); the same applies for DirectX.

All that is needed to use OpenCL with both graphics APIs is a minimal interop layer (check the [D3D11 sharing extension](http://www.khronos.org/registry/cl/sdk/1.2/docs/man/xhtml/cl_khr_d3d11_sharing.html) and the [OpenGL sharing extension](http://www.khronos.org/registry/cl/sdk/1.2/docs/man/xhtml/cl_khr_gl_sharing.html).) It basically boils down to two steps: First, mark the buffers & textures you want to share. Second, enqueue acquire and release commands into an OpenCL command queue to synchronise your graphics and compute code. Your OpenCL code stays the same, independent of whether the data is shared with a graphics API or allocated by OpenCL directly. The driver also gets full knowledge of the resource dependencies which allows it to make good scheduling decisions. This makes it possible to efficiently execute the compute kernels on the GPU without synchronising with the host.

Another advantage is that the OpenCL compiler is better optimized for compute code than the compilers for your graphics API. In my experience, the DirectX compiler is notorious for long optimization times once loops are present. This is no surprise, as it has been originally written for short shaders and its heuristics are tuned for graphics code, not long compute kernels. On the other hand, all current OpenCL implementations are based on LLVM, a compiler framework designed to efficiently handle complex compute code like the SPEC benchmark suite.

If you have gotten curious about OpenCL and you want to give it a shot, head over to [my OpenCL tutorial](https://anteru.net/blog/2012/11/03/2009/) which should help to get you started. Have fun coding! If you have questions about OpenCL, feel free to comment or contact me directly.