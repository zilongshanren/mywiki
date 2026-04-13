---
title: Random thoughts after moving from GLSL to HLSL
url: https://anki3d.org/random-thoughts-after-moving-from-glsl-to-hlsl/
author: Panagiotis Christopoulos Charitos
published: '2023-01-09'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

AnKi always had its shaders written in GLSL because it started as an OpenGL engine. Recently I decided to start rewriting them from GLSL to HLSL with one of the main motivations being that GLSL, as a language, has stopped evolving and it’s missing modern features. Sure, there are new extensions added to GLSL all the time but those extensions expose new Vulkan functionality, they don’t add new syntax to the language. So let’s dive into some random thoughts around HLSL that are tailored to Vulkan and SPIR-V.

## Things HLSL does well compared to GLSL

The language is **evolving**. HLSL had recently gained support for templates, bitfields and these are just a few examples. Microsoft recently opened up the language “spec” so that everyone can request new features: [https://github.com/microsoft/hlsl-specs](https://github.com/microsoft/hlsl-specs)

The inclusion of **templates** solves quite a few problems, especially in cases where the same function can be made a template and work with all kinds of floating point types (float, float16_t and even min16float).

HLSL supports **enums **which is very handy especially when sharing code between HLSL and C++. HLSL even supports strongly typed enums which is pretty neat since AnKi only uses strongly typed enums in C++.

**ByteAddressBuffer** is pretty useful since you can load any user defined data structure with it. GLSL has something even cooler though and that’s **Buffer Device Address** which is almost like pointers. I won’t go into details on how BDA works but the GLSL syntax is just weird. Since we are focusing on languages I’ll give this point to HLSL even if ByteAddressBuffer is less flexible than BDA.

Another plus for HLSL is how it handles **relaxed precision** 32bit floats. HLSL has the min16float family of types that map to relaxed precision 32bit floats in SPIR-V. In GLSL the syntax for relaxed precision is verbose and falls flat in cases where a preprocessor define is used to switch relaxed precision on and off. Example of what I mean in GLSL:

```
#define USE_RELAXED 0
#if USE_RELAXED
#define min16float3 mediump vec3
#else
#define min16float3 vec3
#endif
int i = 10;
min16float3 f = min16float3(i); // ERROR. This will become f = mediump vec3(i) which is not a thing
min16float3 f = vec3(i); // Works but its syntax is bad
```

Another good thing about HLSL is that it seems to be less verbose. When converting shaders from GLSL to HLSL I realized that I was removing more lines that adding. Also check this:

```
// GLSL
layout(binding = 0) uniform b
{
Uniforms uniforms;
};
// HLSL
[[vk::binding(0)]] ConstantBuffer<Uniforms> uniforms;
```

## Now let’s move to the things HLSL needs improvement (in general, and for Vulkan specifically).

The biggest issue with HLSL is the **quality of DirectX compiler’s (aka DXC) SPIR-V** backend. SPIR-V in DXC was originally introduced by Google because of Stadia and maintained primarily by them. Unfortunately Google never had the capacity to solve all the issues and things are worst now that Google doesn’t have the same stakes in it (Stadia is dead). I found 2 issues in DXC’s SPIR-V backend and created bug reports but my issues are still there unresolved. One of them even has a patch with a fix. Unfortunately it’s difficult to beat glslang when it comes to quality. glslang is being extensively tested in Vulkan’s conformance testing suite where DXC just has a few unit tests and Google has some shaders from games ported to Stadia.

There are 2 ways to compile shaders with the DXC. You either invoke the executable dxc.exe or you link with the DXC library. The 2nd is the more performant option but that would mean that AnKi would have to ship with the whole DXC source code and also build it. DXC is a fork of clang so that’s simply a non starter. At the same time Microsoft is moving HLSL to mainline clang which would be an even bigger roadblock when it comes to interfacing with a library. Compiling shaders using dxc.exe should be fine right? After all this is how you compile your C++ source code. But then you have Windows with its awful overhead when invoking executables. Compiling shaders on Linux is orders of magnitude faster than Windows. Anyway, the point is that **DXC is not really embeddable** unlike glslang.

The 3rd issue with HLSL (and D3D in general) is the **packing rules** of members of structures. There are different rules for constant buffers and different for everything else. And Vulkan slightly differs from D3D as well. See the mess for yourselves here [https://github.com/microsoft/DirectXShaderCompiler/blob/main/docs/SPIR-V.rst#memory-layout-rules](https://github.com/microsoft/DirectXShaderCompiler/blob/main/docs/SPIR-V.rst#memory-layout-rules). So good luck sharing types between HLSL and C++. HLSL should adopt Vulkan’s **scalar block layout** (VK_EXT_scalar_block_layout) and call it a day. With scalar block layout the packing rules are equal to C/C++’s. Problem solved.

Another issue with DXC’s SPIR-V backend is that it **can’t handle both relaxed precision and explicit 16bit floating point** types. If someone enables 16bit arithmetic in DXC (-enable-16bit-types) all min16float types will transform from relaxed 32bit to explicit 16bit. glslang can support all types at the same time without any issues.

~~A minor issue that irritates me is the way HLSL ~~ **initializes vector types**. In GLSL you can write a=vec3(0) and initialize all components of the vector to zero. In HLSL you need to write the verbose a=float3(0, 0, 0) or the weird (float3)0. GLSL wins here.**UPDATE**: As János Turánszki pointed out on Twitter in HLSL you can write a=0 which is serviceable.

Another minor thing that came up is **code formatting**. AnKi uses clang-format to format both C++ and GLSL source files. clang-format works quite well (by accident) with GLSL but not for HLSL. HLSL has some weird syntax that clang-format misinterprets. But with a little bit of help from python I managed to solve these problems and sutisfy my pedantic nature.

Another minor issue is the **inconsistency of attributes**. In one hand you have single bracket attributes like [unroll] and [numthreads()] and in the other [[vk::binding()]]. Also the various semantics should have been attributes.

## In conclusion

Today, HLSL is a more usable language compared to GLSL. Where HLSL mostly fails (for AnKi) is in the SPIR-V backend of DXC. Khronos should probably invest more in its maintenance.

Perhaps a strange argument for the lines omitted when converting from GLSL to HLSL? At least, I can write like this:

// GLSL

layout(binding = 0) uniform b { Uniforms uniforms; };

which I find easier to read than this:

// HLSL

[[vk::binding(0)]] ConstantBuffer uniforms;

Because HLSL has more verbosity with angle brackets, double square brackets, and PascalCase words. Lower-case only is a lot easier to write, and I find them easier to read too – but maybe that’s just me? 🙂

I just learned that my comment is auto-formatted :D. What I meant is for the GLSL code that I can also write that in 1 line.