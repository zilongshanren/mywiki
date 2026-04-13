---
title: How to read shader assembly
url: https://interplayoflight.wordpress.com/2021/04/18/how-to-read-shader-assembly/
author: Kostas Anagnostou
published: '2021-04-18'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

When I started graphics programming, shading languages like HLSL and GLSL were not yet popular in game development and shaders were developed straight in assembly. When HLSL was introduced I remember us trying, for fun, to beat the compiler by producing shorter and more compact assembly code by hand, something that wasn’t that hard. Since then shader compiler technology has progressed immensely and nowadays, in most cases, it is pretty hard to produce better assembly code by hand (also the shaders have become so large and complicated that it is not cost effective any more anyway).

Even though no one writes shaders in assembly directly nowadays, it is still useful for a graphics programmer to be able to read and understand the shader assembly (ISA) code produced by the compiler. First, it helps one understand how is the compiler interpreting the high level shader instructions. Some instructions, for eg tan() or integer division don’t map directly to hardware and can expand into many assembly instructions. Second it can help understand how the GPU works, how requests data, performs branches, writes to the output etc. Third, it can help with shader debugging when the actual shader code is not available. And although we don’t typically hand tune shader assembly any more, understanding it can help us make better high-level shader authoring decisions which can lead to higher performance assembly code. Finally, for me personally, it is quite cathartic to sometimes read code without layers of abstraction, with a clear understanding of what it does and as close to the metal as possible.

In this blog post we will discuss shader assembly a bit and provide some pointers on how to read it. This discussion focuses mainly on DirectX and HLSL, similar ideas would apply to other APIs/shading languages. Also in the examples I am using AMD’s shader assembly (ISA) as it is well documented and easy to access with tools like the excellent[ Shader Playground](http://shader-playground.timjones.io/) even if one doesn’t have access to an AMD GPU.

Before we start it is worth mentioning that shader compilation is done in 2 stages: first a tool like fxc or dxc compiles the HLSL code into a GPU agnostic format called Intermediate Language (IL). Then the GPU driver converts the IL into the final shader assembly (ISA) that can be executed on a specific GPU. We will be focusing on ISA, and not on IL, as it is more representative of the code that will actually be executed. In the following example, [an HLSL shader](http://shader-playground.timjones.io/f66cc2731a0f900fe6a58c3c4652ac6b) that multiplies two numbers produces the IL code on the left and the ISA code on the right. The IL code is still relatively high level and hides a lot of the implementation details.

| Intermediate Language | GCN ISA | |
`il_ps_2_55` | `s_mov_b32 m0, s8` |

Let’s consider this [fictional HLSL shader](http://shader-playground.timjones.io/7d8e3e334275e0dfc477154965d10866). Although it doesn’t do anything useful, it uses a lot of the language features one would use in more realistic scenarios, like attribute interpolation, constant buffers, texture reads, Maths operation and branches:

```
struct PSInput
{
float2 uv : TEXCOORD;
};
cbuffer cbData
{
float4 data;
}
Texture2D<float4> tex;
SamplerState samplerLinear;
float4 PSMain(PSInput input) : SV_TARGET
{
float4 result = tex.Sample(samplerLinear, input.uv);
float factor = data.x * data.y;
if( factor > 0 )
return data.z * result;
else
return data.w * result;
}
```

This is the shader assembly it produces, using Radeon GPU Analyser targeting AMD’s GCN GPU architecture:

```
s_mov_b32 m0, s20
s_mov_b64 s[22:23], exec
s_wqm_b64 exec, exec
v_interp_p1_f32 v2, v0, attr0.x
v_interp_p2_f32 v2, v1, attr0.x
v_interp_p1_f32 v3, v0, attr0.y
v_interp_p2_f32 v3, v1, attr0.y
s_and_b64 exec, exec, s[22:23]
image_sample v[0:3], v[2:4], s[4:11], s[12:15] dmask:0xf
s_buffer_load_dwordx4 s[0:3], s[16:19], 0x00
s_waitcnt lgkmcnt(0)
v_mov_b32 v4, s1
v_mul_f32 v4, s0, v4
v_cmp_lt_f32 vcc, 0, v4
s_cbranch_vccz label_0017
s_waitcnt vmcnt(0)
v_mul_f32 v0, s2, v0
v_mul_f32 v1, s2, v1
v_mul_f32 v2, s2, v2
v_mul_f32 v3, s2, v3
s_branch label_001C
label_0017:
s_waitcnt vmcnt(0)
v_mul_f32 v0, s3, v0
v_mul_f32 v1, s3, v1
v_mul_f32 v2, s3, v2
v_mul_f32 v3, s3, v3
label_001C:
s_mov_b64 exec, s[22:23]
v_cvt_pkrtz_f16_f32 v0, v0, v1
v_cvt_pkrtz_f16_f32 v1, v2, v3
exp mrt0, v0, v0, v1, v1 done compr vm
s_endpgm
end
```

At first glance it looks like a mess of cryptic instructions and numbers but let’s try first to colour code corresponding areas between the two shaders to get a rough feel of how HLSL translates to assembly.

```
float4 PSMain(PSInput input) : SV_TARGET
{
float4 result = tex.Sample(samplerLinear, input.uv);
float factor = data.x * data.y;
if( factor > 0 )
return data.z * result;
else
return data.w * result;
}
```


```
s_mov_b32 m0, s20
s_mov_b64 s[22:23], exec
s_wqm_b64 exec, exec
v_interp_p1_f32 v2, v0, attr0.x
v_interp_p2_f32 v2, v1, attr0.x
v_interp_p1_f32 v3, v0, attr0.y
v_interp_p2_f32 v3, v1, attr0.y
s_and_b64 exec, exec, s[22:23]
image_sample v[0:3], v[2:4], s[4:11], s[12:15] dmask:0xf
s_buffer_load_dwordx4 s[0:3], s[16:19], 0x00
s_waitcnt lgkmcnt(0)
v_mov_b32 v4, s1
v_mul_f32 v4, s0, v4
v_cmp_lt_f32 vcc, 0, v4
s_cbranch_vccz label_0017
s_waitcnt vmcnt(0)
v_mul_f32 v0, s2, v0
v_mul_f32 v1, s2, v1
v_mul_f32 v2, s2, v2
v_mul_f32 v3, s2, v3
s_branch label_001C
label_0017:
s_waitcnt vmcnt(0)
v_mul_f32 v0, s3, v0
v_mul_f32 v1, s3, v1
v_mul_f32 v2, s3, v2
v_mul_f32 v3, s3, v3
label_001C:
s_mov_b64 exec, s[22:23]
v_cvt_pkrtz_f16_f32 v0, v0, v1
v_cvt_pkrtz_f16_f32 v1, v2, v3
exp mrt0, v0, v0, v1, v1 done compr vm
s_endpgm
end
```


The uncoloured parts correspond to code the GPU has to execute to setup the main instructions highlighted.

A few things worth discussing before we start digging deeper into the code. First we notice almost all instructions start either with the prefix **v_** or the prefix **s_**, eg **v_mul_f32** and **s_mov_b32**. This gives us some information about the hardware itself: the GCN architecture batches work items (pixels, vertices etc) in batches of 64, called wavefronts, and executes each shader instruction on them in parallel, either operating on data unique to each thread (using the v_ prefix, from vector) or data common to all threads (the s_ prefix from scalar). Worth mentioning that a work item is also often called a “thread”. Multiplying a pixel’s colour by a value is an operation that uses data unique to each thread so the GPU would use a vector instruction. Reading a value from a constant buffer uses data common to all threads so the GPU would use a scalar instruction.

This is a good opportunity to also briefly discuss the type of registers the vector and scalar instructions operate on. The shader code listed above is peppered with vector (vXX) and scalar (sXX) registers, eg v_mul_f32 **v1**, **s3**, **v1**. Registers store data locally that the shader instructions use in operations. A vector register stores one 32 bit quantity per wavefront thread (64 in total) and a scalar register stores one 32 bit quantity common to all threads. I attempted a diagram showcasing a 64 thread wavefront and how a vector and scalar register maps to it to help clarify this.

![](../../assets/29bbd25319809d5e.png)


![](../../assets/29bbd25319809d5e.png)

The mul instruction I mentioned above will multiply the per thread v1 vector register value with the, common to all threads, s3 scalar register value and store the result in the v1 vector register. Sometimes the register indices are presented in brackets for eg s[22:23]. This indicates a register range (scalar registers 22 and 23 in this example) that can be used to store quantities larger than 32 bits.

Finally, it is worth noticing that each instruction indicates the data type is operates on. For example v_mul**_f32** operates on 32 bit floating point numbers, v_mov**_b32** “copies” 32 bit (untyped) quantities between registers, v_cvt_pkrtz**_f16_f32** converts a 32 bit floating point number to a 16 bit one. This is useful to understand the data type and size (16, 32, 64 bits) each instruction uses.

With that information at hand let’s start deciphering the assembly code one chunk at a time.

```
s_mov_b32 m0, s20
s_mov_b64 s[22:23], exec
s_wqm_b64 exec, exec
```

The shader starts with some setup code. Since we will be doing some interpolation later the compiler fills the M0 register (one per wavefront, 32 bits) with the Local Data Store (LDS) offset to the interpolation data (per vertex uv coordinates in this case). Next, it takes a copy of the **exec** register into the scalar registers 22 and 23. The exec (Execute Mask) register stores a 64 bit mask, one bit per wavefront thread, which decides which threads are active and inactive at any moment. Because this register is common to all wavefront threads a scalar (**s_**) instruction is used. Also, this is a good example of combining registers to store values larger then 32 bits. Finally, it executes a **s_wqm_b64** instruction to determine which threads in the wavefront belong to an active pixel quad. Pixel shaders always operate on groups of 2×2 pixels. If a pixel in that quad is active, which means that it covers a triangle, all pixels in the quad will be marked as active. This is done to allow the GPU to determine which quads are active for derivative calculations.

```
v_interp_p1_f32 v2, v0, attr0.x
v_interp_p2_f32 v2, v1, attr0.x
v_interp_p1_f32 v3, v0, attr0.y
v_interp_p2_f32 v3, v1, attr0.y
```

The next snippet **interp**olates the float2 uv coordinates provided by the vertex shader via the local data store (LDS) memory, using the offset stored in M0 register above. We use vector instructions (prefix v_) in this case because each thread (pixel) will have its own uv value. We notice that the interpolation for each uv.x and uv.y component is done in two steps p1 and p2, two instructions per component. During those two steps the GPU reads 3 uv component values, one per vertex, along with the 2 barycentric coordinates and interpolates the final value. This provides us with another piece of knowledge about the GPU hardware, that interpolation is happening in the shader and that there is no dedicated hardware for it. The uv coordinates are now stored in vector registers v2 and v3.

```
s_and_b64 exec, exec, s[22:23]
```

This instruction updates the execution mask for all the wavefront threads. If a thread doesn’t belong to an active pixel quad it gets deactivated.

```
image_sample v[0:3], v[2:4], s[4:11], s[12:15] dmask:0xf
```

This is a texture sample instruction. The _sample postfix implies that this operation can also filter data through a SamplerState object, which is what the HLSL code in the example uses. The first vector register range, v[0:3], indicates the 4 registers that will be used to store the result (v0-v3, 4 floating point values), the v[2:4] range contains the uv coordinates interpolated above (v2 and v3), the scalar register range [4:11] contains the 8 registers used to stored the texture descriptor (which points to the memory address of the texture) and the other scalar range [12:15] contains the 4 registers used to store the descriptor (memory address) of the sampler object used for the filtering of the texture samples (the SamplerState object defined in the HLSL shader). The final dmask (4-bit data mask) operand specifies how many components the texture read should process. A value of 0xf specifies all 4 components. Even though it doesn’t have the v_ prefix, image_sample is a vector instruction.

```
s_buffer_load_dwordx4 s[0:3], s[16:19], 0x00
s_waitcnt lgkmcnt(0)
v_mov_b32 v4, s1
v_mul_f32 v4, s0, v4
```

Next, we need to read the constant data from the constant buffer to multiply the texture colours by. Reading from a constant buffer is a scalar operation common to all wavefront threads, so an **s_buffer_load_dwordx4** is issued. The first scalar range specifies the scalar registers to store the results of the load (s0-s3, 4 fp32 values) and the second range specifies the descriptor of the constant buffer (points to the memory address it is stored). All memory loads have latency, which means that it takes a number of clock cycles (potentially large) from the time a load is issued with the s_buffer_load and when the returned value can be used in the subsequent **v_mov_b32 **instruction, so the shader compiler adds a **s_waitcnt **instruction between the two that will stall if the data are not ready to be used. The **lgkmcnt **argument in a wait instruction signifies that the instruction waits for a constant buffer (or Local/Global data store) read to return. Once the data is here, the shader issues a move instruction to copy the value of s1 to the v4 register and subsequently an v_mul instruction to multiply it with the s0 register (effectively implementing the **float factor = data.x * data.y** HLSL instruction.

This code exposes another bit of info about the hardware, that it doesn’t support direct multiplication of scalar values, it has to first copy one of the two to vector registers. Is this true for all data types? Apparently not, if I change the constant buffer data to be uint4 instead of float4, the shader will issue an integer multiplication instruction **s_mul_i32 **to directly multiply the two scalar values:

```
s_buffer_load_dwordx4 s[0:3], s[16:19], 0x00
s_waitcnt lgkmcnt(0)
s_mul_i32 s0, s1, s0
```


Back to the main shader

```
v_cmp_lt_f32 vcc, 0, v4
s_cbranch_vccz label_0017
```

Now the shader has the result of the multiplication in v4 it can do a **v_cmp_lt_f32** instruction to determine if it is **less than** zero. This instruction sets the Vector Condition Code register (VCC, bit value of 1 means that a thread passed, 0 failed the comparison). Remember that although it is vector comparison (i.e. a different one for each thread), v4 contains the same value for all threads so the result will be same for all threads. If the result of the comparison stored in VCC is zero (**s_cbranch_vccz**), which means that the “less than” comparison failed, the shader will skip the following branch of the code and continue execution from label_0017.

Another bit of insight about the hardware here as well. Although the “comparison” instruction is vector (treats each thread in the wavefront differently), the actual branch instruction is scalar, i.e. the same for all threads. On GCN this is true for all type of branches, they are handled by the Scalar Unit. Also, the branch in this case is all or nothing, either all threads’ factor.x value is less than zero or all larger than zero because the compiler knows that that value originated as a scalar and is the the same for all threads, i.e. there is no divergence. If I changed the comparison value to vary per thread:

```
float4 PSMain(PSInput input) : SV_TARGET
{
float4 result = tex.Sample(samplerLinear, input.uv);
if( result.x > 0 )
return data.z * result;
else
return data.w * result;
}
```


the resulting ISA changes to account for the possible divergence

```
image_sample v[0:3], v[2:4], s[4:11], s[12:15] dmask:0xf
s_mov_b64 s[0:1], exec
s_waitcnt vmcnt(0)
v_cmpx_gt_f32 s[2:3], v0, 0
s_cbranch_execz label_0017
```


Now the shader compiler puts the execution mask into use (which controls which thread is active or not), using the **v_cmpx_gt_f32 **instruction to store the result of the per-thread comparison directly into it. Threads that fail the comparison will be “skipped over”, when the **s_cbranch_execz **instruction (which branches using the execution mask and not the VCC register) is then executed.

Back to the main shader again.

```
s_waitcnt vmcnt(0)
v_mul_f32 v0, s2, v0
v_mul_f32 v1, s2, v1
v_mul_f32 v2, s2, v2
v_mul_f32 v3, s2, v3
s_branch label_001C
```

This is the first branch of the if-statement to multiply the result of the texture read instruction by the constant value (data.z). Similarly to the constant buffer load above, now that texture read results are needed the GPU must ensure that they are here or undefined behaviour will happen. For this, the shader compiler adds another wait instruction, **s_waitcnt**. This time the **vmcnt **operant means that it is waiting for a vector memory return (as opposed to a scalar memory return in the case of the constant buffer read). At the end of the snippet the code will unconditionally jump to label_001C to avoid executing the second branch.

```
label_0017:
s_waitcnt vmcnt(0)
v_mul_f32 v0, s3, v0
v_mul_f32 v1, s3, v1
v_mul_f32 v2, s3, v2
v_mul_f32 v3, s3, v3
```

This is the second branch in the code, to multiply the result from the texture read by the other constant value (data.w). Focusing on the **v_mul_f32 **instruction, it is worth calling out that it can multiply scalars with vectors directly, another bit of info about the underlying hardware. Also worth noticing is that although a float4 multiplication is seemingly one instruction in HLSL and Intermediate Language, it is actually 4 instructions in shader assembly, as dictated by GCN’s design (it has to do with it being a scalar architecture but I don’t want to confuse this with scalar instructions and registers, there is a lot of [material online](https://www.gdcvault.com/play/1019294/Powering-the-Next-Generation-of) that describe how it works for more details).

```
label_001C:
s_mov_b64 exec, s[22:23]
v_cvt_pkrtz_f16_f32 v0, v0, v1
v_cvt_pkrtz_f16_f32 v1, v2, v3
exp mrt0, v0, v0, v1, v1 done compr vm
s_endpgm
```

Shader execution is winding down now, all it remains to be done is write out the results. The snippet starts by restoring the value of the execution mask, stored in the scalars s22 and s23 at the start of the program, to make sure that all required threads will write out the result. The output (a float4 number) is currently stored in vector registers v0-v3. The **v_cvt_pkrtz_f16_f32 **instruction will pack the float32 contents of 2 vector registers (eg v0 and v1) into one float32 vector register. This is done twice, for each of the two pairs (v0, v1 and v2, v3). In the end we have the 2 vector registers v0 and v1 that hold the original float4 output in compressed form, to reduce memory bandwidth. Finally, the **exp **instruction triggers the copy of the output to the bound render target. The **mrt0 **argument means that this instruction targets the first rendertarget in a possible multiple rendertarget configuration (a maximum of 8 rendertargets can be bound as an output to a pixel shader), next follow the vector registers that hold the compressed output values, **done **means that this is the last export in the shader, **compr **means that the data is in compressed form and **vm **flag indicates that the execution mask can used to inform the color buffer which pixels are valid and which have been discarded. With that, the shader stops executing.

I mentioned earlier how reading and understanding shader assembly can help one make better decisions during shader authoring. Although the shader example I provided is trivial and not very useful, it is still difficult to see how it can be improved without having an insider knowledge of what the compiler will do with provided code. Tweaking the shader code slightly to take the **return**; outside the if-statement branches for example we can see in the assembly that the compiler removes the branches entirely, using 4 **v_cndmask_b32** to select the output value based on the result of the comparison instruction **v_cmp_lt_f32**.

```
float4 PSMain(PSInput input) : SV_TARGET
{
float4 result = tex.Sample(samplerLinear, input.uv);
float factor = data.x * data.y;
if( factor > 0 )
result *= data.z;
else
result *= data.w;
return result;
}
```

Shader assembly:

```
s_mov_b32 m0, s20
s_mov_b64 s[22:23], exec
s_wqm_b64 exec, exec
v_interp_p1_f32 v2, v0, attr0.x
v_interp_p1_f32 v3, v0, attr0.y
v_interp_p2_f32 v2, v1, attr0.x
v_interp_p2_f32 v3, v1, attr0.y
s_and_b64 exec, exec, s[22:23]
image_sample v[0:3], v[2:4], s[4:11], s[12:15] dmask:0xf
s_buffer_load_dwordx4 s[0:3], s[16:19], 0x00
s_waitcnt lgkmcnt(0)
v_mov_b32 v4, s1
v_mul_f32 v4, s0, v4
v_cmp_lt_f32 vcc, 0, v4
s_waitcnt vmcnt(0)
v_mul_f32 v4, s2, v0
v_mul_f32 v5, s2, v1
v_mul_f32 v6, s2, v2
v_mul_f32 v7, s2, v3
v_mul_f32 v0, s3, v0
v_mul_f32 v1, s3, v1
v_mul_f32 v2, s3, v2
v_mul_f32 v3, s3, v3
v_cndmask_b32 v0, v0, v4, vcc
v_cndmask_b32 v1, v1, v5, vcc
v_cndmask_b32 v2, v2, v6, vcc
v_cndmask_b32 v3, v3, v7, vcc
s_mov_b64 exec, s[22:23]
v_cvt_pkrtz_f16_f32 v0, v0, v1
v_cvt_pkrtz_f16_f32 v1, v2, v3
exp mrt0, v0, v0, v1, v1 done compr vm
s_endpgm
```

Although in this case it may not make much performance difference because all threads will always follow one branch of the if-statement, and if anything it increases the number of vector registers used which may not be good, this is good knowledge to apply in other scenarios. The bottom line is that one can’t easily tell how HLSL shader changes will affect the final shader assembly without inspecting it.

Most of the information I used in this shader assembly breakdown is documented in [Vega’s ISA reference documentation](https://developer.amd.com/wp-content/resources/Vega_Shader_ISA_28July2017.pdf). There is also a large collection of [low-level GPU guides](http://renderingpipeline.com/graphics-literature/low-level-gpu-documentation/) worth researching if you are interested in learning more, for other GPUs as well, and also Emil Persson’s [excellent](https://www.humus.name/index.php?page=Articles&ID=6) [presentations](https://www.humus.name/index.php?page=Articles&ID=9) on low level shader optimisation.

[…] 💭 How to Read Shader Assembly Blog post by Kostas Anagnostou […]