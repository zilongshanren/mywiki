---
title: OpenCL and DirectX/OpenGL interop
url: https://anteru.net/blog/2012/opencl-and-directx-opengl-interop
published: '2012-10-30'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

I’m a big fan of OpenCL, even though it has [a few problems related to graphics](https://anteru.net/blog/2011/12/06/1815/) left. Still, it’s a viable target for graphics related computations, with the promise to have a single implementation of various compute kernels that can be used with both graphics APIs (DirectX and OpenGL.)

OpenCL had built-in interop support for OpenGL since day one with the [ cl_khr_ogl_sharing](http://www.khronos.org/registry/cl/extensions/khr/cl_khr_gl_sharing.txt) extension. The situation on the DirectX side was not that great, though. At the beginning, only NVIDIA provided interoperability support:

[,](http://www.khronos.org/registry/cl/extensions/nv/cl_nv_d3d9_sharing.txt)

`cl_nv_d3d9_sharing`

[,](http://www.khronos.org/registry/cl/extensions/nv/cl_nv_d3d10_sharing.txt)

`cl_nv_d3d10_sharing`

[. All the extensions are highly similar and provide a direct, low-level access to DirectX resources. AMD followed quickly for DirectX10 with](http://www.khronos.org/registry/cl/extensions/nv/cl_nv_d3d11_sharing.txt)

`cl_nv_d3d11_sharing`

[, which is a 1:1 copy of the NVIDIA extension. Unfortunately, there was no equivalent for DirectX11. While in theory it is possible to use the D3D10 extension with DirectX11 with](http://www.khronos.org/registry/cl/extensions/khr/cl_khr_d3d10_sharing.txt)

`cl_khr_d3d10_sharing`

[a lot of voodoo and DirectX10/11 interop](http://msdn.microsoft.com/en-us/library/windows/desktop/ee913554(v=vs.85).aspx), a KHR version of the NVIDIA extension was clearly the way to go.

This took quite some time until OpenCL 1.2, which comes now with [a standard cl_khr_d3d11_sharing](http://www.khronos.org/registry/cl/specs/opencl-1.2-extensions.pdf) extension. The OpenCL version is a slightly expanded version of the NVIDIA extension (for instance, it allows to disable the synchronization guarantees). NVIDIA does not support it though (as it doesn’t support OpenCL 1.2), but AMD just recently implemented it in their driver. I didn’t notice at first, as there was no public announcement and if you search the web for

`cl_khr_d3d11_sharing`

and AMD, you usually wind up with a post of mine where I shake my fist at AMD for not supporting it. However, thanks to [Christophe Riccio](http://www.g-truc.net/)I just discovered that since at least Catalyst 12.10 the driver exposes the DirectX11 KHR sharing extension. That still means two code paths for NVIDIA and AMD, but that’s a small cost to pay for a much wider hardware support. In particular, current AMD hardware has advantages in terms of memory bandwidth (both to local as well as to global memory) which could be highly beneficial for a bunch of use cases I have.

If you’re interested in OpenCL and DirectX11, feel free to try on any hardware now! Just keep in mind that this is not yet a fully debugged and stable system. At least on NVIDIA (haven’t tried AMD’s DirectX11/OpenCL support yet) we’re running into driver synchronization bugs from time to time as well as weird kernel compile errors. Still, you can get some nice stuff working, and I’m looking forward to trying it all out on an AMD card now as well!