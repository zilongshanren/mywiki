---
title: The hidden cost of shader instructions
url: https://interplayoflight.wordpress.com/2025/01/19/the-hidden-cost-of-shader-instructions/
author: Kostas Anagnostou
published: '2025-01-19'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

I posted a few days ago a screenshot of the long shader ISA code produced by the RGA compiler for a single atan2() instruction. The post got quite a large engagement and it felt like a lot of people were surprised by the fact, so I decided to write a post to discuss the “hidden” cost of shader instructions a bit more.

For the following I am referring to GCN/RDNA architectures and most ISA was produced using [https://godbolt.org/](https://godbolt.org/). To aid the discussion I have, quite unscientifically, assigned the cause of the “hidden” the cost of shader instructions broadly 3 to categories:

- No hardware support for the instruction
- Hardware implementation of the instruction
- Instruction has a dependency on a resource

Let’s start with the first category, an instruction doesn’t have a hardware (native) implementation and needs to be implemented using a, sometimes large, number of native instructions. This is very common cause of “hidden” cost and can take people by surprise. Inverse trigonometric functions (acos, asin, atan, atan2) don’t have a native implementation, this is for eg the RDNA ISA code produced for a single atan2:

```
v_cmp_gt_f32 s[0:1], v2, 0 // 00000000001C: D4040000 00010102
s_mov_b64 s[2:3], exec // 000000000024: BE82047E
v_cmpx_eq_f32 exec, v0, 0 // 000000000028: D412007E 00010100
v_mov_b32 v0, lit(0x3fc90fda) // 000000000030: 7E0002FF 3FC90FDA
v_cndmask_b32 v0, lit(0xbfc90fda), v0, s[0:1] // 000000000038: D5010000 000200FF BFC90FDA
s_andn2_b64 exec, s[2:3], exec // 000000000044: 8AFE7E02
s_cbranch_execz label_0308 // 000000000048: BF8800AF
v_cmp_gt_f32 s[4:5], v0, 0 // 00000000004C: D4040004 00010100
s_mov_b64 s[6:7], exec // 000000000054: BE86047E
v_cmpx_eq_f32 exec, v2, 0 // 000000000058: D412007E 00010102
v_cndmask_b32 v0, lit(0x40490fda), 0, s[4:5] // 000000000060: D5010000 001100FF 40490FDA
s_andn2_b64 exec, s[6:7], exec // 00000000006C: 8AFE7E06
s_cbranch_execz label_0308 // 000000000070: BF8800A5
s_mov_b64 s[8:9], exec // 000000000074: BE88047E
v_cmpx_gt_f32 exec, abs(v0), abs(v2) // 000000000078: D414037E 00020500
v_div_scale_f32 v1, vcc, v0, v0, v2 // 000000000080: D56D6A01 040A0100
s_cbranch_execz label_01A4 // 000000000088: BF880046
v_div_scale_f32 v3, vcc, v2, v0, v2 // 00000000008C: D56D6A03 040A0102
s_denorm_mode 0x000f // 000000000094: BFA5000F
v_rcp_f32 v6, v1 // 000000000098: 7E0C5501
v_fma_f32 v5, -v1, v6, 1.0 // 00000000009C: D54B0005 23CA0D01
v_fmac_f32 v6, v5, v6 // 0000000000A4: 560C0D05
v_mul_f32 v4, v3, v6 // 0000000000A8: 10080D03
v_fma_f32 v5, -v1, v4, v3 // 0000000000AC: D54B0005 240E0901
v_fmac_f32 v4, v5, v6 // 0000000000B4: 56080D05
v_fma_f32 v3, -v1, v4, v3 // 0000000000B8: D54B0003 240E0901
s_denorm_mode 0x000c // 0000000000C0: BFA5000C
v_div_fmas_f32 v1, v3, v6, v4 // 0000000000C4: D56F0001 04120D03
v_mov_b32 v4, lit(0xbc8bf91a) // 0000000000CC: 7E0802FF BC8BF91A
v_div_fixup_f32 v0, v1, v0, v2 // 0000000000D4: D55F0000 040A0101
v_cmp_eq_f32 s[10:11], abs(v0), 0 // 0000000000DC: D402010A 00010100
v_rcp_f32 v1, abs(v0) // 0000000000E4: D5AA0101 00000100
v_and_b32 v2, lit(0x7fffffff), v0 // 0000000000EC: 360400FF 7FFFFFFF
v_cmp_gt_f32 vcc, abs(v0), 1.0 // 0000000000F4: D404016A 0001E500
v_and_b32 v0, lit(0x80000000), v0 // 0000000000FC: 360000FF 80000000
v_cndmask_b32 v1, v1, 0, s[10:11] // 000000000104: D5010001 00290101
v_cndmask_b32 v3, v2, v1, vcc // 00000000010C: 02060302
v_mul_legacy_f32 v1, v3, v3 // 000000000110: 0E020703
v_fmac_legacy_f32 v4, lit(0x3b47bf1d), v1 // 000000000114: 0C0802FF 3B47BF1D
v_fma_legacy_f32 v4, v4, v1, lit(0x3d3751b7) // 00000000011C: D5400004 03FE0304 3D3751B7
v_fma_legacy_f32 v4, v4, v1, lit(0xbd9e0bf8) // 000000000128: D5400004 03FE0304 BD9E0BF8
v_fma_legacy_f32 v4, v4, v1, lit(0x3ddc5c26) // 000000000134: D5400004 03FE0304 3DDC5C26
v_fma_legacy_f32 v4, v4, v1, lit(0xbe11cde3) // 000000000140: D5400004 03FE0304 BE11CDE3
v_fma_legacy_f32 v4, v4, v1, lit(0x3e4cc636) // 00000000014C: D5400004 03FE0304 3E4CC636
v_fma_legacy_f32 v4, v4, v1, lit(0xbeaaaaa3) // 000000000158: D5400004 03FE0304 BEAAAAA3
v_fma_legacy_f32 v2, v4, v1, 1.0 // 000000000164: D5400002 03CA0304
v_mul_legacy_f32 v4, v3, v2 // 00000000016C: 0E080503
v_fma_legacy_f32 v1, -v3, v2, lit(0x3fc90fdb) // 000000000170: D5400001 23FE0503 3FC90FDB
v_cndmask_b32 v1, v4, v1, vcc // 00000000017C: 02020304
v_xor_b32 v0, v0, v1 // 000000000180: 3A000300
v_mov_b32 v1, lit(0x40490fda) // 000000000184: 7E0202FF 40490FDA
v_cndmask_b32 v1, lit(0xc0490fda), v1, s[0:1] // 00000000018C: D5010001 000202FF C0490FDA
v_add_f32 v1, v0, v1 // 000000000198: 06020300
v_cndmask_b32 v0, v1, v0, s[4:5] // 00000000019C: D5010000 00120101
label_01A4:
s_andn2_b64 exec, s[8:9], exec // 0000000001A4: 8AFE7E08
s_cbranch_execz label_0308 // 0000000001A8: BF880057
s_mov_b64 s[10:11], exec // 0000000001AC: BE8A047E
v_cmpx_eq_f32 exec, abs(v0), abs(v2) // 0000000001B0: D412037E 00020500
v_mov_b32 v0, lit(0x3f490fda) // 0000000001B8: 7E0002FF 3F490FDA
v_mov_b32 v1, lit(0xbf490fda) // 0000000001C0: 7E0202FF BF490FDA
v_cndmask_b32 v0, lit(0x4016cbe4), v0, s[4:5] // 0000000001C8: D5010000 001200FF 4016CBE4
v_cndmask_b32 v1, lit(0xc016cbe4), v1, s[4:5] // 0000000001D4: D5010001 001202FF C016CBE4
v_cndmask_b32 v0, v1, v0, s[0:1] // 0000000001E0: D5010000 00020101
s_andn2_b64 exec, s[10:11], exec // 0000000001E8: 8AFE7E0A
v_div_scale_f32 v1, vcc, v2, v2, v0 // 0000000001EC: D56D6A01 04020502
s_cbranch_execz label_0308 // 0000000001F4: BF880044
v_div_scale_f32 v3, vcc, v0, v2, v0 // 0000000001F8: D56D6A03 04020500
s_denorm_mode 0x000f // 000000000200: BFA5000F
v_rcp_f32 v6, v1 // 000000000204: 7E0C5501
v_fma_f32 v5, -v1, v6, 1.0 // 000000000208: D54B0005 23CA0D01
v_fmac_f32 v6, v5, v6 // 000000000210: 560C0D05
v_mul_f32 v4, v3, v6 // 000000000214: 10080D03
v_fma_f32 v5, -v1, v4, v3 // 000000000218: D54B0005 240E0901
v_fmac_f32 v4, v5, v6 // 000000000220: 56080D05
v_fma_f32 v3, -v1, v4, v3 // 000000000224: D54B0003 240E0901
s_denorm_mode 0x000c // 00000000022C: BFA5000C
v_div_fmas_f32 v1, v3, v6, v4 // 000000000230: D56F0001 04120D03
v_mov_b32 v4, lit(0xbc8bf91a) // 000000000238: 7E0802FF BC8BF91A
v_div_fixup_f32 v0, v1, v2, v0 // 000000000240: D55F0000 04020501
v_cmp_eq_f32 s[4:5], abs(v0), 0 // 000000000248: D4020104 00010100
v_rcp_f32 v1, abs(v0) // 000000000250: D5AA0101 00000100
v_and_b32 v2, lit(0x7fffffff), v0 // 000000000258: 360400FF 7FFFFFFF
v_cmp_gt_f32 vcc, abs(v0), 1.0 // 000000000260: D404016A 0001E500
v_and_b32 v0, lit(0x80000000), v0 // 000000000268: 360000FF 80000000
v_cndmask_b32 v1, v1, 0, s[4:5] // 000000000270: D5010001 00110101
v_cndmask_b32 v3, v2, v1, vcc // 000000000278: 02060302
v_mul_legacy_f32 v1, v3, v3 // 00000000027C: 0E020703
v_fmac_legacy_f32 v4, lit(0x3b47bf1d), v1 // 000000000280: 0C0802FF 3B47BF1D
v_fma_legacy_f32 v4, v4, v1, lit(0x3d3751b7) // 000000000288: D5400004 03FE0304 3D3751B7
v_fma_legacy_f32 v4, v4, v1, lit(0xbd9e0bf8) // 000000000294: D5400004 03FE0304 BD9E0BF8
v_fma_legacy_f32 v4, v4, v1, lit(0x3ddc5c26) // 0000000002A0: D5400004 03FE0304 3DDC5C26
v_fma_legacy_f32 v4, v4, v1, lit(0xbe11cde3) // 0000000002AC: D5400004 03FE0304 BE11CDE3
v_fma_legacy_f32 v4, v4, v1, lit(0x3e4cc636) // 0000000002B8: D5400004 03FE0304 3E4CC636
v_fma_legacy_f32 v4, v4, v1, lit(0xbeaaaaa3) // 0000000002C4: D5400004 03FE0304 BEAAAAA3
v_fma_legacy_f32 v2, v4, v1, 1.0 // 0000000002D0: D5400002 03CA0304
v_mul_legacy_f32 v4, v3, v2 // 0000000002D8: 0E080503
v_fma_legacy_f32 v1, -v3, v2, lit(0x3fc90fdb) // 0000000002DC: D5400001 23FE0503 3FC90FDB
v_cndmask_b32 v1, v4, v1, vcc // 0000000002E8: 02020304
v_xor_b32 v0, v0, v1 // 0000000002EC: 3A000300
v_sub_f32 v1, lit(0x3fc90fda), v0 // 0000000002F0: 080200FF 3FC90FDA
v_sub_f32 v0, lit(0xbfc90fda), v0 // 0000000002F8: 080000FF BFC90FDA
v_cndmask_b32 v0, v0, v1, s[0:1] // 000000000300: D5010000 00020300
label_0308:
s_mov_b64 exec, s[2:3] // 000000000308: BEFE0402
v_cvt_pkrtz_f16_f32 v2, v0, 0 // 00000000030C: D52F0002 00010100
v_mov_b32 v3, 0 // 000000000314: 7E060280
exp mrt0, v2, v2, v3, v3 done compr vm // 000000000318: F8001C0F 00000302
s_endpgm // 000000000320: BF810000
```

Admittedly this is one of the most extremes examples, not all inverse trigonometric functions expand to so many instructions. It is not only inverse trigonometric instructions that are expanded into many native ones, tan() has no native implementation as well, it is calculated using cos and sin instructions, which have:

```
v_mul_f32 v0, 0.15915494, v0 // 000000000014: 100000F8
v_cos_f32 v1, v0 // 000000000018: 7E026D00
v_sin_f32 v0, v0 // 00000000001C: 7E006B00
v_rcp_f32 v1, v1 // 000000000020: 7E025501
v_mul_legacy_f32 v0, v0, v1 // 000000000024: 0E000300
```

More widely used instructions that don’t have native implementation are normalize() and length(), for eg this is normalize():

```
v_mul_legacy_f32 v1, v2, v2 // 000000000024: 0E020502
v_fmac_f32 v1, v3, v3 // 000000000028: 56020703
v_fmac_f32 v1, v0, v0 // 00000000002C: 56020100
v_rsq_f32 v1, v1 // 000000000030: 7E025D01
v_mul_legacy_f32 v2, v2, v1 // 000000000034: 0E040302
v_mul_legacy_f32 v3, v3, v1 // 000000000038: 0E060303
v_mul_legacy_f32 v0, v0, v1 // 00000000003C: 0E000300
```

Integer division using vector registers is another area of large instruction expansion. As there are no native vector instructions to implement this, a single x/y division with integer operands would produce around 35 instructions on RDNA ISA. Integer division with scalar registers is even worse, producing a mix of around 42 scalar and vector instructions (I will spare you from pasting unending streams of instructions here, you can experiment with [godbold.org](https://godbolt.org/) if you’d like to see it in action).

Cubemap sampling is another instruction that is, perhaps unexpectedly, expanded to multiple ones as the compiler is attempting to calculate the face to use:

```
// cubemap.Sample(samplerLinear, direction.xyz);
v_cubema_f32 v1, v2, v3, v0 // 000000000034: D5470001 04020702
s_load_dwordx8 s[4:11], s[0:1], null // 00000000003C: F40C0100 FA000000
s_load_dwordx4 s[0:3], s[0:1], 0x000020 // 000000000044: F4080000 FA000020
v_cubetc_f32 v4, v2, v3, v0 // 00000000004C: D5460004 04020702
v_rcp_f32 v1, abs(v1) // 000000000054: D5AA0101 00000101
v_cubesc_f32 v5, v2, v3, v0 // 00000000005C: D5450005 04020702
v_cubeid_f32 v0, v2, v3, v0 // 000000000064: D5440000 04020702
v_fmaak_f32 v2, v4, v1, lit(0x3fc00000) // 00000000006C: 5A040304 3FC00000
v_fmaak_f32 v1, v5, v1, lit(0x3fc00000) // 000000000074: 5A020305 3FC00000
s_and_b64 exec, exec, s[12:13] // 00000000007C: 87FE0C7E
s_waitcnt lgkmcnt(0) // 000000000080: BF8CC07F
image_sample v[0:2], [v1,v2,v0], s[4:11], s[0:3] dmask:0x7 dim:SQ_RSRC_IMG_CUBE // 000000000084: F080071A 00010001 00000002
```

Another example of an HLSL operation that can have a large impact on number of instructions produced is register (VGPR) array indexing. Say that you try to access a register using a uniform (same for all threads) index:

```
// float data[4] = {....} // store some values in a VGPR array
// float result = data[index]; // index is the same for all threads
v_mov_b32 v4, 0 // 00000000004C: 7E080280
s_cmp_lt_u32 s0, 4 // 000000000054: BF0A8400 <---- Protect against array overflow
s_cbranch_scc0 label_0064 // 000000000058: BF840002
s_mov_b32 m0, s0 // 00000000005C: BEFC0300
v_movrels_b32 v4, v5 // 000000000060: 7E088705
```

The compiler will add an out of bounds check and if the index is within range, it will access the register in the array using the index as a relative offset (v_movrels_b32 v4, v5).

In cases where the index is different for every thread (thread variant) though, the compiler can’t use it as a relative offset and resorts to comparing the index value to all possible values in the range:

```
// float data[4] = {....} // store some values in a VGPR array
// float result = data[index]; // index is thread variant
v_mov_b32 v4, 0 // 000000000034: 7E080280
v_cmp_eq_i32 vcc, 0, v5 // 000000000038: 7D040A80
v_cndmask_b32 v0, v4, v6, vcc // 00000000003C: 02000D04
v_cmp_eq_i32 vcc, 1, v5 // 000000000040: 7D040A81
v_cndmask_b32 v1, v0, v7, vcc // 000000000044: 02020F00
v_cmp_eq_i32 vcc, 2, v5 // 000000000048: 7D040A82
v_cndmask_b32 v1, v1, v8, vcc // 00000000004C: 02021101
v_cmp_eq_i32 vcc, 3, v5 // 000000000050: 7D040A83
v_cndmask_b32 v1, v1, v9, vcc // 000000000054: 02021301
```

The larger the register array, the more values it will need to compare and the longer the produced code will be.

Let’s now consider the second category, the extra cost that comes from the specific hardware implementation of an instruction or a hardware restriction that might impact the cost of an operation.

Even for native instructions (instructions that have a hardware implementation), not all instructions have the same cost. Transcendental instructions (cos, sin, exp, log, rsq, sqrt) have native implementations in many architectures but for example on AMD GPUs are 4 times the cost of a floating point multiplication or addition. Also on AMD, an integer multiplication is 4 times the cost as well. To illustrate this, this is the latency of some native instructions I extracted from the ISA breakdown of a shader compiled with RGA in [Shader Playground](https://shader-playground.timjones.io/):

```
s_mov_b32 m0, s2 Scalar ALU 4
v_rcp_f32 v2, v2 Vector ALU 16
v_mul_f32 v2, v2, v3 Vector ALU 4
v_mul_lo_u32 v3, v3, v4 Vector ALU 16
v_cvt_f32_i32 v3, v3 Vector ALU 4
v_cos_f32 v0, v0 Vector ALU 16
v_mac_f32 v3, v2, v0 Vector ALU 4
v_mov_b32 v0, 0 Vector ALU 4
```

A floating point multiply has a latency of 4 clock cycles, while cos, rcp and integer multiplication (v_mul_lo_u32) all have a latency of 16 clock cycles on a GCN GPU. Latency is the number of clock cycles from instruction issue to instruction finish on all wave threads.

There are other cases where what code the compiler ends up producing does not exactly match the expected behaviour due to some hardware limitation. For example when performing floating point maths with scalar registers, since GCN/RDNA architecture does not support it, the compiler won’t increase the amount of instructions but it will convert all of them to vector operations:

```
// float3x3 m; // both m and v are stored in scalar registers
// float3 v;
// float3 result = mul(v,m)
v_mul_f32 v0, s0, s8 // 000000000060: D5080000 00001000
v_mul_f32 v1, s0, s10 // 000000000068: D5080001 00001400
v_mul_f32 v2, s0, s12 // 000000000070: D5080002 00001800
v_fma_f32 v0, s9, s1, v0 // 000000000078: D54B0000 04000209
v_fma_f32 v1, s11, s1, v1 // 000000000080: D54B0001 0404020B
v_fma_f32 v2, s13, s1, v2 // 000000000088: D54B0002 0408020D
v_fma_f32 v0, s3, s2, v0 // 000000000094: D54B0000 04000403
v_fma_f32 v1, s14, s2, v1 // 00000000009C: D54B0001 0404040E
```

This could impact vector register (VGPR) allocation and maybe shader occupancy.

The final source of hidden cost I’d like to briefly discuss, more for awareness, involves instructions that need access to some resource, like texture read instructions, group shared memory instructions etc. This type of cost is frequently less predictable compared to the ones discussed so far, for example a cos() will always be quarter-rate compared to a multiplication when targeting a specific architecture. The cost of a texture read depends a lot on whether the memory is in the cache (a few cycles) or if it has to reach out to RAM (hundreds of cycles). Furthermore, the impact of that memory latency is variable, depending on whether the compiler can hide it with instruction reordering, or the Compute Units have enough waves in flight to swap and avoid stalling the GPU ([more here](https://interplayoflight.wordpress.com/2020/11/11/what-is-shader-occupancy-and-why-do-we-care-about-it/)).

Memory reads can also have hidden costs depending on what we read and how we request the read. For example, on GCN, reading a single channel texture using a point sampler [will be more expensive than without](https://gpuopen.com/wp-content/uploads/2017/03/GDC2017-Advanced-Shader-Programming-On-GCN.pdf) (the following assumes requested data is in the cache):

```
float result = tex.Sample(pointSampler, uv); // 16 clocks, assuming cache hit
float result = tex[coord]; // 4 clocks, assuming cache hit
```

A response similar to the one discussed above with VGPR indexing can happen when using arrays of textures (resources in general). In cases the index is not the same for all threads, the compiler will add extra code to batch resource access by index, a process called a “waterfall loop” (on GCN/RDNA GPUs at least)

```
// StructuredBuffer<float> inputBuffer[];
// float result = inputBuffer[NonUniformResourceIndex(index)][j]; // index is thread variant
v_lshlrev_b32 v1, 2, v1
v_lshlrev_b32 v0, 5, v0
s_mov_b32 s0, s2
s_mov_b64 s[2:3], exec
s_mov_b64 s[4:5], exec
label_0009:
v_readfirstlane_b32 s6, v0 // <-- get index from first active thread
v_cmpx_eq_u32 exec, s6, v0 //<-- only activate threads that use the same index
s_load_dwordx4 s[8:11], s[0:1], s6
s_waitcnt lgkmcnt(0)
buffer_load_dword v0, v1, s[8:11], 0 offen
s_andn2_b64 s[4:5], s[4:5], exec
s_mov_b64 exec, s[4:5]
s_cbranch_execnz label_0009 <-- loop back and process another batch
```

Another “hidden” cost may come from groupshared memory (LDS) access pattern. For example on RDNA but also NVidia GPUs [LDS is divided in 32 banks](https://gpuopen.com/learn/rdna-performance-guide/) and the optimal access pattern is for each thread to access a different bank:

```
float groupshared data[128]; // memory is divided into 32 banks, accessed as index % 32
[numthreads(8, 8, 1)]
void main( uint2 GTid : SV_GroupThreadID )
{
float result = data[GTid.y*32 + GTid.x] // each thread accesses a different bank, no conflict
}
```

Divergence from this access pattern can introduce conflicts and increased instruction latency, in the following extreme case where consecutive threads attempt to access the same memory bank:

```
float groupshared data[128]; // memory is divided into 32 banks, accessed as index % 32
[numthreads(8, 8, 1)]
void main( uint2 GTid : SV_GroupThreadID )
{
float result = data[GTid.x*32 + GTid.y] // consecutive threads access the same bank, conflicts
}
```

This will serialise access and can increase the instruction latency by 32 times.

The above were just a few of examples of how the compiler can interpret the high level instructions in unexpected ways but also of added cost due to specific hardware implementation of an instruction.

The question is what can we do in such cases? At least in the case of inverse trigonometric functions there are plenty of approximations that we can [consider](https://seblagarde.wordpress.com/2014/12/01/inverse-trigonometric-functions-gpu-optimization-for-amd-gcn-architecture/), but also look for opportunities to [avoid them](https://iquilezles.org/articles/noacos/) altogether. In the end though, the actual impact of the “hidden costs” will depend on your circumstances, the cost of doing stuff and the bottlenecks on your targeted GPU, how a potential increase in VGPR allocation affects occupancy, whether the increased number of instructions puts pressure on the instruction cache, whether the shader is memory latency bound and has room for more ALU, whether you are running a complementary async compute task in parallel to soak up an unused resource.

Regardless of whether you need to do anything about it though or not, it is always worth to be aware of the “hidden costs”, inspect what your compiler produces for your target platform if you can (the actual ISA not intermediate code like DXIL) and profile, never assume what the impact will be.