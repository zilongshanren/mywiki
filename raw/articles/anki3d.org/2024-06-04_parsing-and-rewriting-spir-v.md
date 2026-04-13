---
title: Parsing and rewriting SPIR-V
url: https://anki3d.org/parsing-and-rewriting-spir-v/
author: Panagiotis Christopoulos Charitos
published: '2024-06-04'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

[SPIR-V](https://www.khronos.org/spir/) is a binary language that describes the GPU shader code for the Vulkan and OpenCL APIs. For most graphics programmers SPIR-V is a completely opaque binary blob that they don’t have to touch or know much about. Someone can use their preferred compiler to translate GLSL or HLSL to SPIR-V, can use [SPIRV-Tools](https://github.com/KhronosGroup/SPIRV-Tools) to optimize or assemble/disassemble, can use [SPIRV-Cross](https://github.com/KhronosGroup/SPIRV-Cross) or [SPIRV-Reflect](https://github.com/KhronosGroup/SPIRV-Reflect) to perform shader reflection and finally they can use [SPIRV-Cross](https://github.com/KhronosGroup/SPIRV-Cross) to cross compile SPIR-V to some high level language. There is enough tooling out there to not have to worry about the internals. SPIR-V is very well defined and quite simple to understand and manipulating it without the use of 3rd part tools is not something to feel intimidated by and this is the point I’m trying to make with this post.

Why parse and/or rewrite SPIR-V? For AnKi I’ve stumbled into a couple of cases where there was no existing tooling that could do what I wanted. The first case is quite simple. I wanted to find if the fragment shader was discarding. This was quite simple, just search if the shader contains spv::OpKill. The 2nd usecase is more elaborate. Due to various reasons AnKi’s shaders were rewritten to support HLSL and HLSL’s binding model (using the [register](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-variable-register) keyword). Since there is not direct mapping of HLSL’s binding model to Vulkan/SPIR-V we had to get a little creative. Without going into many details, DXC is remapping HLSL registers to some logical Vulkan bindings using -fvk-b-shift and co (register -> spv::DecorationBinding). These logical bindings are used to identify the register when performing shader reflection (spv::DecorationBinding -> register). After DXC completes the translation the output SPIR-V contains logical bindings that need to be replaced. So after reflection AnKi rewrites the bindings. And this is the 2nd case where AnKi had to parse SPIR-V but also rewrite it.

This page describes how parsing SPIR-V works: [https://github.com/KhronosGroup/SPIRV-Guide/blob/main/chapters/parsing_instructions.md](https://github.com/KhronosGroup/SPIRV-Guide/blob/main/chapters/parsing_instructions.md)

SPIR-V binary starts with a header that is 20 bytes. After that the instructions follow. Each instruction starts with a 32bit opcode and a variable number of 32bit arguments. The opcode encodes the opcode itself and the number of arguments. Iterating all the instructions is pretty simple. Finding if the SPIR-V binary contains spv::OpKill can be done like this:

```
bool hasOpKill(uint32_t* pCode, uint32_t codeSize)
{
uint32_t offset = 5; // first 5 words of module are the headers
while(offset < codeSize)
{
uint32_t instruction = pCode[offset];
uint32_t length = instruction >> 16;
uint32_t opcode = instruction & 0x0ffffu;
offset += length;
if(opcode == spv::OpKill)
{
return true;
}
}
return false;
}
```

Similar story if someone would want to rewrite the bindings for example:

```
void rewriteBindings(uint32_t* pCode, uint32_t codeSize)
{
uint32_t offset = 5; // first 5 words of module are the headers
while(offset < codeSize)
{
uint32_t instruction = pCode[offset];
uint32_t length = instruction >> 16;
uint32_t opcode = instruction & 0x0ffffu;
// Encoding: OpDecorate || id || DecorationBinding || <literal>
if(opcode == spv::OpDecorate && pCode[offset + 2] == spv::DecorationBinding)
{
pCode[offset + 3] = someValue; // 3rd argument is the binding. Re-write it
}
offset += length;
}
}
```

Pretty simple.