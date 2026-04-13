---
title: Experimenting with fp16 in shaders
url: https://interplayoflight.wordpress.com/2022/12/30/experimenting-with-fp16-in-shaders/
author: Kostas Anagnostou
published: '2022-12-30'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

With recent GPUs and shader models there is good support for 16 bit floating point numbers and operations in shaders. On paper, the main advantages of the a fp16 representation are that it allows packing two 16 numbers into a single 32 bit register, reducing the register allocation for a shader/increasing occupancy, and also allows reduction of ALU instruction count by performing instructions to packed 32 bit registers directly (i.e. affecting the two packed fp16 numbers independently). I spent some time investigating what fp16 looks like at the ISA level (GCN 5) and am sharing some notes I took.

I started with a very simple compute shader implementing some fp16 maths as a test. I compiled it using the 6.2 shading model and the -enable-16bit-types DXC command line argument.

```
cbuffer data
{
float value1;
float value2;
float value3;
float pad;
}
[numthreads(8, 8, 1)]
void main(int2 thread_id : SV_DispatchThreadID)
{
half x = half(thread_id.x) * half(value1);
half y = half(thread_id.y) * half(value2);
half result1 = x * half(value2);
half result2 = y * half(value1);
output1[thread_id] = result1;
output2[thread_id] = result2;
}
```

The produced ISA looks like this

```
s_getpc_b64 s[0:1] // 000000000000: BE801C80
s_mov_b32 s3, s1 // 000000000004: BE830001
s_load_dwordx4 s[12:15], s[2:3], 0x00 // 000000000008: C00A0301 00000000
s_waitcnt lgkmcnt(0) // 000000000010: BF8CC07F
s_buffer_load_dwordx2 s[2:3], s[12:15], 0x00 // 000000000014: C0260086 00000000
s_mov_b32 s0, s4 // 00000000001C: BE800004
s_load_dwordx8 s[12:19], s[0:1], 0x20 // 000000000020: C00E0300 00000020
v_mad_u32_u24 v0, s7, 8, v0 // 000000000028: D1C30000 04011007
s_load_dwordx8 s[20:27], s[0:1], 0x40 // 000000000030: C00E0500 00000040
v_mad_u32_u24 v1, s8, 8, v1 // 000000000038: D1C30001 04051008
v_cvt_f32_i32 v2, v0 // 000000000040: 7E040B00
s_waitcnt lgkmcnt(0) // 000000000044: BF8CC07F
v_cvt_pkrtz_f16_f32 v2, s2, v2 // 000000000048: D2960002 00020402
v_cvt_f32_i32 v3, v1 // 000000000050: 7E060B01
v_mul_f16 v4, v2, v2 dst_sel:WORD_0 dst_unused:UNUSED_PRESERVE src0_sel:WORD_1 src1_sel:WORD_0 // 000000000054: 440804F9 04051402
v_cvt_pkrtz_f16_f32 v3, s3, v3 // 00000000005C: D2960003 00020603
v_mul_f16 v4, v3, v3 dst_sel:WORD_1 dst_unused:UNUSED_PRESERVE src0_sel:WORD_1 src1_sel:WORD_0 // 000000000064: 440806F9 04051503
v_pk_mul_f16 v3, v4, v3 op_sel_hi:[0,0] // 00000000006C: D3900003 00020704
v_pk_mul_f16 v2, v2, v4 op_sel:[0,1] op_sel_hi:[0,1] // 000000000074: D3901002 10020902
v_mov_b32 v4, v3 // 00000000007C: 7E080303
image_store v[3:6], v[0:3], s[12:19] dmask:0xf unorm glc d16 // 000000000080: F0203F00 80030300
v_mov_b32 v3, v2 // 000000000088: 7E060302
image_store v[2:5], v[0:3], s[20:27] dmask:0xf unorm glc d16 // 00000000008C: F0203F00 80050200
```

On line 5 we read value1 and value2 from the constant buffer. Next follows some code to convert the thread index to float and the interesting work begins on line 13, where the float values (thread.x and value1) are packed to a single register (v2) using the v_cvt_pkrtz_f16_f32 instruction, which can work with both scalar and vector registers as inputs. The first input (source) of the instruction (s2 in this case, containing value1 from the constant buffer) is packed in the low 16 bits (16-31, later referred to as WORD0) and the second input (v2, containing thread_id.x) is packed in the high 16 bits (16-31, later referred to as WORD1) i.e v2 now looks like this

The mul instruction on line 15 is the fp16 version that multiplies 2 fp16 numbers packed in full 32 bit registers, let’s see how this works in greater detail.

v_mul_f16 v4, v2, v2 dst_sel:WORD_0 dst_unused:UNUSED_PRESERVE src0_sel:WORD_1 src1_sel:WORD_0

This instruction says: multiply 2 fp16 numbers, both selected from register v2, writing the output to the lower 16 bits of register v4 leaving the other 16 bits untouched (dst_sel:WORD_0 dst_unused:UNUSED_PRESERVE). From input 0 (src0) use the fp16 packed in the high 16 bits (src0_sel:WORD_1), while from the second input (src1) use the fp16 in the the low 16 bits (src1_sel:WORD_0). This is effectively used to multiply 2 fp16 numbers stored in the same 32 bit register. Lines 16 and 17 implement the same for the value2 and thread_id.y multiplication.

So far we don’t seem to have saved much with fp16 over fp32, we used a single instruction to multiply a pair of fp16 numbers (plus the extra instructions for the conversion). This changes on lines 18 and 19, where the v_pk_mul_f16 instruction is used to simultaneously multiply 2 pairs of fp16s using a single instruction.

v_pk_mul_f16 v3, v4, v3 op_sel_hi:[0,0]

By default that instruction will multiply the low parts of each 32bit registers and store the fp16 result in the low part of the destination register and similarly for the high parts of source and destination registers (i.e the modifiers will be implicitly op_sel:[0,0] op_sel_hi:[1,1] and omitted). This can be overridden by using the op_sel and op_sel_hi modifiers. op_sel will determine which parts (low – 0, or hi – 1) of the inputs will be used for the low part of the destination register and op_sel_hi similarly for the high part of the destination. That particular instruction above will use the default behaviour for the low bits of the destination (i.e. store the multiplication of the low fp16 numbers in the v4 and v3 registers, op_sel:[0,0]), and then perform the same multiplication for the hi 16 bits of the destination (i.e both parts contain the result of value2 * thread.x * value1)

Line 19 does a similar operation for register v2, overriding the default selection to pick the low part of v2 and the high part of v4 to store to both parts of v2 (i.e both parts contain the result of value1 * thread.y * value2).

v_pk_mul_f16 v2, v2, v4 op_sel:[0,1] op_sel_hi:[0,1]

Finally the results are stored to the buffers using 2 image_store instructions. Worth noticing that the instructions use the d16 modifier as the compiler is aware that the input data is in 16 bits.

It is not clear yet what we’ve gained using fp16, let’s compile the same shader without the -enable-16bit-types argument, something that will promote all fp16s data types and operations to fp32

```
s_getpc_b64 s[0:1] // 000000000000: BE801C80
s_mov_b32 s3, s1 // 000000000004: BE830001
s_load_dwordx4 s[12:15], s[2:3], 0x00 // 000000000008: C00A0301 00000000
s_waitcnt lgkmcnt(0) // 000000000010: BF8CC07F
s_buffer_load_dwordx2 s[2:3], s[12:15], 0x00 // 000000000014: C0260086 00000000
s_mov_b32 s0, s4 // 00000000001C: BE800004
s_load_dwordx8 s[12:19], s[0:1], 0x20 // 000000000020: C00E0300 00000020
s_load_dwordx8 s[20:27], s[0:1], 0x40 // 000000000028: C00E0500 00000040
v_mad_u32_u24 v0, s7, 8, v0 // 000000000030: D1C30000 04011007
v_mad_u32_u24 v1, s8, 8, v1 // 000000000038: D1C30001 04051008
v_cvt_f32_i32 v2, v0 // 000000000040: 7E040B00
s_waitcnt lgkmcnt(0) // 000000000044: BF8CC07F
v_mul_f32 v2, s2, v2 // 000000000048: 0A040402
v_cvt_f32_i32 v3, v1 // 00000000004C: 7E060B01
v_mul_f32 v3, s3, v3 // 000000000050: 0A060603
v_mul_f32 v2, s3, v2 // 000000000054: 0A040403
v_mul_f32 v6, s2, v3 // 000000000058: 0A0C0602
v_mov_b32 v3, v2 // 00000000005C: 7E060302
v_mov_b32 v4, v2 // 000000000060: 7E080302
v_mov_b32 v5, v2 // 000000000064: 7E0A0302
image_store v[2:5], v[0:3], s[12:19] dmask:0xf unorm glc // 000000000068: F0203F00 00030200
v_mov_b32 v7, v6 // 000000000070: 7E0E0306
v_mov_b32 v8, v6 // 000000000074: 7E100306
v_mov_b32 v9, v6 // 000000000078: 7E120306
image_store v[6:9], v[0:3], s[20:27] dmask:0xf unorm glc // 00000000007C: F0203F00 00050600
```

The compiler shader is a bit longer for one, due to the extra mov instructions. It issues 4 multiplication instructions as does the fp16 version, so no gain here. In terms of register allocation, the fp32 version has 10 VGPRs and 30 SGPRs while the fp16 version has 5 VGPRs and 30 SGPRs, so there is the potential to improve [occupancy](https://interplayoflight.wordpress.com/2020/11/11/what-is-shader-occupancy-and-why-do-we-care-about-it/) here.

One other thing worth investigating is what would happen in the constant buffer data were in fp16 to begin with

```
cbuffer data
{
half value1;
half value2;
float value3;
float2 pad;
}
```

The resulting ISA will then be

```
s_getpc_b64 s[0:1] // 000000000000: BE801C80
s_mov_b32 s5, s1 // 000000000004: BE850001
s_load_dwordx8 s[12:19], s[4:5], 0x20 // 000000000008: C00E0302 00000020
s_load_dwordx8 s[20:27], s[4:5], 0x40 // 000000000010: C00E0502 00000040
s_mov_b32 s0, s2 // 000000000018: BE800002
s_load_dwordx4 s[0:3], s[0:1], 0x00 // 00000000001C: C00A0000 00000000
s_waitcnt lgkmcnt(0) // 000000000024: BF8CC07F
s_buffer_load_dword s0, s[0:3], 0x00 // 000000000028: C0220000 00000000
v_mad_u32_u24 v0, s7, 8, v0 // 000000000030: D1C30000 04011007
v_mad_u32_u24 v1, s8, 8, v1 // 000000000038: D1C30001 04051008
v_cvt_f32_i32 v2, v0 // 000000000040: 7E040B00
v_cvt_pkrtz_f16_f32 v2, 0, v2 // 000000000044: D2960002 00020480
s_waitcnt lgkmcnt(0) // 00000000004C: BF8CC07F
v_mul_f16 v2, s0, v2 dst_sel:WORD_0 dst_unused:UNUSED_PRESERVE src0_sel:WORD_0 src1_sel:WORD_1 // 000000000050: 440404F9 05841400
v_cvt_f32_i32 v3, v1 // 000000000058: 7E060B01
v_cvt_pkrtz_f16_f32 v3, 0, v3 // 00000000005C: D2960003 00020680
v_mul_f16 v2, s0, v3 dst_sel:WORD_1 dst_unused:UNUSED_PRESERVE src0_sel:WORD_1 src1_sel:WORD_1 // 000000000064: 440406F9 05851500
v_pk_mul_f16 v3, v2, s0 op_sel:[0,1] op_sel_hi:[0,1] // 00000000006C: D3901003 10000102
v_mov_b32 v4, v3 // 000000000074: 7E080303
image_store v[3:6], v[0:3], s[12:19] dmask:0xf unorm glc d16 // 000000000078: F0203F00 80030300
v_pk_mul_f16 v2, s0, v2 op_sel:[0,1] op_sel_hi:[0,1] // 000000000080: D3901002 10020400
v_mov_b32 v3, v2 // 000000000088: 7E060302
image_store v[2:5], v[0:3], s[20:27] dmask:0xf unorm glc d16 // 00000000008C: F0203F00 80050200
```

One interesting thing that happens is that on line 8, the constant buffer load instruction loads both value1 and value2 already packed in s0 and the logic of the operand selection during v_pk_mul_f16 changes a bit to reflect that but otherwise the code is pretty similar.

What will happen if we throw a float operation into the mix?

```
cbuffer data
{
half value1;
half value2;
float value3;
float2 pad;
}
[numthreads(8, 8, 1)]
void main(int2 thread_id : SV_DispatchThreadID)
{
half x = half(thread_id.x) * half(value1);
half y = half(thread_id.y) * half(value2);
x *= value3; // multiply the fp16 x by the fp32 value3
half result1 = x * half(value2);
half result2 = y * half(value1);
output1[thread_id] = result1;
output2[thread_id] = result2;
}
```

The resulting ISA now looks like

```
s_getpc_b64 s[0:1] // 000000000000: BE801C80
s_mov_b32 s5, s1 // 000000000004: BE850001
s_load_dwordx8 s[12:19], s[4:5], 0x20 // 000000000008: C00E0302 00000020
s_load_dwordx8 s[20:27], s[4:5], 0x40 // 000000000010: C00E0502 00000040
s_mov_b32 s0, s2 // 000000000018: BE800002
s_load_dwordx4 s[0:3], s[0:1], 0x00 // 00000000001C: C00A0000 00000000
s_waitcnt lgkmcnt(0) // 000000000024: BF8CC07F
s_buffer_load_dwordx2 s[0:1], s[0:3], 0x00 // 000000000028: C0260000 00000000
v_mad_u32_u24 v0, s7, 8, v0 // 000000000030: D1C30000 04011007
v_mad_u32_u24 v1, s8, 8, v1 // 000000000038: D1C30001 04051008
v_cvt_f32_i32 v2, v0 // 000000000040: 7E040B00
v_cvt_pkrtz_f16_f32 v2, 0, v2 // 000000000044: D2960002 00020480
s_waitcnt lgkmcnt(0) // 00000000004C: BF8CC07F
v_mul_f16 v2, s0, v2 dst_sel:WORD_0 dst_unused:UNUSED_PRESERVE src0_sel:WORD_0 src1_sel:WORD_1 // 000000000050: 440404F9 05841400
v_cvt_f32_i32 v3, v1 // 000000000058: 7E060B01
v_cvt_pkrtz_f16_f32 v3, 0, v3 // 00000000005C: D2960003 00020680
v_mul_f16 v2, s0, v3 dst_sel:WORD_1 dst_unused:UNUSED_PRESERVE src0_sel:WORD_1 src1_sel:WORD_1 // 000000000064: 440406F9 05851500
v_cvt_f32_f16 v3, v2 // 00000000006C: 7E061702
v_mul_f32 v3, s1, v3 // 000000000070: 0A060601
v_cvt_pkrtz_f16_f32 v3, 0, v3 // 000000000074: D2960003 00020680
v_pk_mul_f16 v3, s0, v3 op_sel:[1,1] op_sel_hi:[1,1] // 00000000007C: D3901803 18020600
v_mov_b32 v4, v3 // 000000000084: 7E080303
image_store v[3:6], v[0:3], s[12:19] dmask:0xf unorm glc d16 // 000000000088: F0203F00 80030300
v_pk_mul_f16 v2, s0, v2 op_sel:[0,1] op_sel_hi:[0,1] // 000000000090: D3901002 10020400
v_mov_b32 v3, v2 // 000000000098: 7E060302
image_store v[2:5], v[0:3], s[20:27] dmask:0xf unorm glc d16 // 00000000009C: F0203F00 80050200
```

Things are going well until line 18 in which the compiler has to promote the fp16 result to fp32 to perform the float multiplication

v_cvt_f32_f16 v3, v2

and then convert to fp16 again on line 20. In this simple shader mixing a float operation just increases the number of instructions but it is likely that it could increase the register allocation in more complex ones so it would be good to be avoided.

This was useful to tell us how fp16 works under the hood and showed some potential but this simple shader isn’t enough to reveal any real benefits. For that I will try an actual shader from the [FidelityFX SSSR sample](https://interplayoflight.wordpress.com/2022/09/28/notes-on-screenspace-reflections-with-fidelityfx-sssr/), which uses fp16 extensively. I realise that I keep going back to the SSSR sample quite frequently for my investigations since I integrated it to my toy renderer. I quite like that sample, it implements a lot of modern techniques and it saves me the trouble of implementing them for some quick investigations.

So compiling the ResolveTemporal.hlsl shader using the same as above DXC configuration I get a VGPR allocation of 110 and an SGPR allocation of 37. Compiling the shader without support for fp16 I get a VGPR allocation of 83 and a SGPR allocation of 49, so the fp32 version has the advantage here (SGPR allocation rarely becomes the bottleneck).

I won’t list the shader ISA here as it is 1200+ lines but on first inspection it seems to contain a healthy dose of vk_pk instructions like the following

```
v_pk_add_f16 v18, v18, v24 op_sel_hi:[1,1] // 000000000D7C: D38F0012 18023112
v_pk_mul_f16 v24, v26, s12 op_sel_hi:[1,0] // 000000000D84: D3900018 0800191A
v_pk_mul_f16 v26, v31, v31 op_sel:[1,1] op_sel_hi:[0,0] // 000000000D8C: D390181A 00023F1F
v_pk_add_f16 v16, v16, v17 op_sel_hi:[1,1] // 000000000D94: D38F0010 18022310
v_pk_mul_f16 v17, v19, s3 op_sel_hi:[1,0]
```

but it also seems to contain a few promotions from fp16 to fp32, which like discussed are not ideal.

```
v_cvt_f32_f16 v5, v2 src0_sel: WORD_1 // 000000001F00: 7E0A16F9 00050602
v_cvt_f32_f16 v11, v44 // 000000001F08: 7E16172C
v_cvt_f32_f16 v2, v2 // 000000001F0C: 7E041702
v_cvt_f32_f16 v12, v8 // 000000001F10: 7E181708
v_cvt_f32_f16 v13, v22 // 000000001F14: 7E1A1716
v_cvt_f32_f16 v16, v20 // 000000001F18: 7E201714
```

There must be some float operations mixed in somewhere, a quick investigation reveals that FFX_DNSR_Reflections_ClipAABB() mixes fp32 and fp16 operations:

```
half3 FFX_DNSR_Reflections_ClipAABB(half3 aabb_min, half3 aabb_max, half3 prev_sample) {
// Main idea behind clipping - it prevents clustering when neighbor color space
// is distant from history sample
// Here we find intersection between color vector and aabb color box
// Note: only clips towards aabb center
float3 aabb_center = 0.5 * (aabb_max + aabb_min);
float3 extent_clip = 0.5 * (aabb_max - aabb_min) + 0.001;
// Find color vector
float3 color_vector = prev_sample - aabb_center;
// Transform into clip space
float3 color_vector_clip = color_vector / extent_clip;
// Find max absolute component
color_vector_clip = abs(color_vector_clip);
half max_abs_unit = max(max(color_vector_clip.x, color_vector_clip.y), color_vector_clip.z);
if (max_abs_unit > 1.0) {
return aabb_center + color_vector / max_abs_unit; // clip towards color vector
} else {
return prev_sample; // point is inside aabb
}
}
```

There is one here:

```
half FFX_DNSR_Reflections_Luminance(half3 color) { return max(dot(color, float3(0.299, 0.587, 0.114)), 0.001); }
```

And a fun one here (in FFX_DNSR_Reflections_ResolveTemporal())

```
// Blend with average for small sample count
new_signal.xyz = lerp(new_signal.xyz, avg_radiance, 1.0 / max(num_samples + 1.0f, 1.0));
```

If you can’t see the issue in the last one at first, adding the “f” after the literal 1.0 will force promotion of all operands to float.

Mixing fp16/fp32 operation issues may be quite tricky to locate, especially when you retrofit support for fp16 to a large codebase. Quick tip, always inspect the DXC warnings, they may tell you when floats are demoted to fp16s:

```
ffx_denoiser_reflections_common.h:53:59: warning: conversion from larger type 'float' to smaller type 'half', possible loss of data [-Wconversion]
half FFX_DNSR_Reflections_Luminance(half3 color) { return max(dot(color, float3(0.299, 0.587, 0.114)), 0.001); }
```


Fixing those issues drops VGPR allocation only by one to 109 and the SGPR allocation by 3 to 34.

There are also some promotions to float that I couldn’t fix

```
v_cvt_f32_f16 v1, v0 // 000000002120: 7E021700
v_cvt_f32_f16 v5, v3 src0_sel: WORD_1 // 000000002124: 7E0A16F9 00050603
s_movk_i32 s0, 0x0204 // 00000000212C: B0000204
v_mul_f16 v4, v4, v2 dst_sel:WORD_0 dst_unused:UNUSED_PRESERVE src0_sel:WORD_1 src1_sel:WORD_1 // 000000002130: 440804F9 05051404
v_cvt_f32_f16 v6, v3 // 000000002138: 7E0C1703
v_cmp_class_f32 s[2:3], v1, s0 // 00000000213C: D0100002 00000101
v_cmp_class_f32 s[6:7], v5, s0 // 000000002144: D0100006 00000105
v_cmp_class_f32 s[8:9], v1, 3 // 00000000214C: D0100008 00010701
v_cmp_class_f32 s[12:13], v5, 3 // 000000002154: D010000C 00010705
```

The v_cmp_class_f32 instructions refer to this part of FFX_DNSR_Reflections_ResolveTemporal:

```
if (any(isinf(new_signal)) || any(isnan(new_signal)) || any(isinf(new_variance)) || any(isnan(new_variance)))
{
new_signal = 0.0;
new_variance = 0.0;
}
```

Although GCN 5.0 supports a 16 bit version of v_cmp_class_f32 the compiler doesn’t use it for some reason (all inputs are fp16).

Would VGPR allocation change if we targeted RDNA instead of GCN? Without fp16 support the compiler allocates 87 VGPRs and 48 SGPRs while with fp16 support it allocates 106 VGPRs and 44 SGPRs, so the fp32 version still has the advantage.

In the end, all it matters is actual performance impact. On my integrated AMD GPU (GCN5) the temporal resolve SSSR pass costs the same for both fp16 and fp32 while on the NVidia RTX 3080 mobile GPU the fp32 version is actually 23% faster, so for that particular shader, fp16 is not really a gain.

It appears that, as with many techniques and features, the actual gain will vary depending on the application and as always it needs profiling to determine if it will improve a rendering pass.