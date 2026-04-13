---
title: Experimenting with fp16, part 2
url: https://interplayoflight.wordpress.com/2023/01/08/experimenting-with-fp16-part-2/
author: Kostas Anagnostou
published: '2023-01-08'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

In the [previous blog post](https://interplayoflight.wordpress.com/2022/12/30/experimenting-with-fp16-in-shaders/) I discussed how enabling fp16 for a particular shader didn’t seem to make a performance difference and also forced the compiler to allocate a larger number of VGPRs compared to the fp32 version (108 vs 81), which seemed weird as one of the (expected) advantages of fp16 is reduced register allocation. So I spent some more time investigating why this is happening. The shader I am referring to is the ResolveTemporal.hlsl one from the FidelityFX SSSR sample [I recently integrated](https://interplayoflight.wordpress.com/2022/09/28/notes-on-screenspace-reflections-with-fidelityfx-sssr/) to my toy renderer.

I started by running a live shader analysis with RGA for both versions and plotting the results. This showed me how the number of allocated VGPRs evolves over time.

![](../../assets/647a0821204484a6.png)


![](../../assets/647a0821204484a6.png)

The blue graph corresponds to the fp16 version while the orange one to fp32. The horizontal axis corresponds to ISA line number. One thing to notice is the fp16 shader is shorter, at 1249 lines, than the fp32 one at 1405, which is good. The other thing we notice is that up until about line 200 the shaders behave similarly in terms of VGPR allocation but from then on the fp16 shoots up, continuing to allocate VGPRs while the fp32 version is starting to reduce the allocation rate, flattening the curve.

For some context, the shader uses variance and mean radiance estimation in the pixel’s neighbourhood to clip history.

```
FFX_DNSR_Reflections_Moments FFX_DNSR_Reflections_EstimateLocalNeighborhoodInGroup(int2 group_thread_id)
{
FFX_DNSR_Reflections_Moments estimate;
estimate.mean = 0;
estimate.variance = 0;
half accumulated_weight = 0;
for (int j = -FFX_DNSR_REFLECTIONS_LOCAL_NEIGHBORHOOD_RADIUS; j <= FFX_DNSR_REFLECTIONS_LOCAL_NEIGHBORHOOD_RADIUS; ++j)
{
for (int i = -FFX_DNSR_REFLECTIONS_LOCAL_NEIGHBORHOOD_RADIUS; i <= FFX_DNSR_REFLECTIONS_LOCAL_NEIGHBORHOOD_RADIUS; ++i)
{
int2 new_idx = group_thread_id + int2(i, j);
half3 radiance = FFX_DNSR_Reflections_LoadFromGroupSharedMemory(new_idx).radiance;
half weight = FFX_DNSR_Reflections_LocalNeighborhoodKernelWeight(half(i)) * FFX_DNSR_Reflections_LocalNeighborhoodKernelWeight(half(j));
accumulated_weight += weight;
estimate.mean += radiance * weight;
estimate.variance += radiance * radiance * weight;
}
}
estimate.mean /= accumulated_weight;
estimate.variance /= accumulated_weight;
estimate.variance = abs(estimate.variance - estimate.mean * estimate.mean);
return estimate;
}
```

Because there is a lot of reuse of radiance values between neighbouring pixels, the shader stores the radiance in group shared memory to avoid reloading the same samples multiple times. The radiance is packed as half3 in 2 uints (the last 16bits are not used)

```
groupshared uint g_ffx_dnsr_shared_0[16][16];
groupshared uint g_ffx_dnsr_shared_1[16][16];
```

FFX_DNSR_REFLECTIONS_LOCAL_NEIGHBORHOOD_RADIUS is compile-time defined (a value of 4) which allows the compiler to unroll both loops. This also allows the compiler to precalculate and store, in scalar registers for the fp16 case, the weights computed with FFX_DNSR_Reflections_LocalNeighborhoodKernelWeight() as the output only depends on the compile-time known loop index.

So what are the shaders doing around the 200-line number mark? By then, the code has started reading the group shared memory and calculating variance and mean values for radiance. In the the fp32 version, the code seems to happily read the radiance data from the group shared memory, using **ds_read2st64_b32**, and use it to calculate variance and radiance:

```
ds_read2st64_b32 v[59:60], v42 offset1:4 // 000000000520: D8700400 3B00002A
v_madmk_f32 v8, v12, 0x3e162023, v8 // 000000000528: 2E10110C 3E162023
v_madmk_f32 v11, v13, 0x3e162023, v11 // 000000000530: 2E16170D 3E162023
v_madmk_f32 v9, v16, 0x3e162023, v9 // 000000000538: 2E121310 3E162023
v_mul_f32 v12, v24, v24 // 000000000540: 0A183118
v_mul_f32 v13, v41, v41 // 000000000544: 0A1A5329
v_mul_f32 v16, v28, v28 // 000000000548: 0A20391C
v_madmk_f32 v17, v25, 0x3db9ca56, v17 // 00000000054C: 2E222319 3DB9CA56
v_madmk_f32 v23, v26, 0x3db9ca56, v23 // 000000000554: 2E2E2F1A 3DB9CA56
v_cvt_f32_f16 v24, v33 // 00000000055C: 7E301721
v_cvt_f32_f16 v28, v34 // 000000000560: 7E381722
v_madmk_f32 v29, v31, 0x3d4bed87, v29 // 000000000564: 2E3A3B1F 3D4BED87
v_cvt_f32_f16 v33, v0 src0_sel: WORD_1 // 00000000056C: 7E4216F9 00050600
v_add_u32 v34, 0x00000060, v6 // 000000000574: 68440CFF 00000060
ds_read2st64_b32 v[61:62], v36 offset1:4 // 00000000057C: D8700400 3D000024
v_madmk_f32 v8, v12, 0x3e052640, v8 // 000000000584: 2E10110C 3E052640
v_madmk_f32 v11, v13, 0x3e052640, v11 // 00000000058C: 2E16170D 3E052640
v_madmk_f32 v9, v16, 0x3e052640, v9 // 000000000594: 2E121310 3E052640
v_mul_f32 v12, v25, v25 // 00000000059C: 0A183319
v_mul_f32 v13, v35, v35 // 0000000005A0: 0A1A4723
v_mul_f32 v16, v26, v26 // 0000000005A4: 0A20351A
v_madmk_f32 v17, v24, 0x3d4bed87, v17 // 0000000005A8: 2E222318 3D4BED87
v_madmk_f32 v23, v28, 0x3d4bed87, v23 // 0000000005B0: 2E2E2F1C 3D4BED87
v_cvt_f32_f16 v0, v0 // 0000000005B8: 7E001700
v_cvt_f32_f16 v1, v1 // 0000000005BC: 7E021701
v_madmk_f32 v25, v33, 0x3cb0135a, v29 // 0000000005C0: 2E323B21 3CB0135A
v_cvt_f32_f16 v26, v45 src0_sel: WORD_1 // 0000000005C8: 7E3416F9 0005062D
v_add_u32 v29, 0x00000080, v6 // 0000000005D0: 683A0CFF 00000080
image_load v35, v[20:23], s[12:19] unorm // 0000000005D8: F0001100 00032314
ds_read2st64_b32 v[63:64], v32 offset1:4 // 0000000005E0: D8700400 3F000020
v_madmk_f32 v8, v12, 0x3db9ca56, v8 // 0000000005E8: 2E10110C 3DB9CA56
v_madmk_f32 v11, v13, 0x3db9ca56, v11 // 0000000005F0: 2E16170D 3DB9CA56
v_madmk_f32 v9, v16, 0x3db9ca56, v9 // 0000000005F8: 2E121310 3DB9CA56
v_mul_f32 v12, v24, v24 // 000000000600: 0A183118
v_mul_f32 v13, v31, v31 // 000000000604: 0A1A3F1F
v_mul_f32 v16, v28, v28 // 000000000608: 0A20391C
v_madmk_f32 v17, v0, 0x3cb0135a, v17 // 00000000060C: 2E222300 3CB0135A
v_madmk_f32 v23, v1, 0x3cb0135a, v23 // 000000000614: 2E2E2F01 3CB0135A
v_cvt_f32_f16 v24, v45 // 00000000061C: 7E30172D
v_cvt_f32_f16 v28, v46 // 000000000620: 7E38172E
v_madmk_f32 v25, v26, 0x3d4bed87, v25 // 000000000624: 2E32331A 3D4BED87
v_cvt_f32_f16 v31, v49 src0_sel: WORD_1 // 00000000062C: 7E3E16F9 00050631
v_add_u32 v41, 0x00000084, v6 // 000000000634: 68520CFF 00000084
```

It issues 81 ds_read2st64_b32 groupshare read instructions in total which makes sense since we are reading (2*FFX_DNSR_REFLECTIONS_LOCAL_NEIGHBORHOOD_RADIUS + 1)^2 = 81 uint pairs in the double loop above. The groupshared memory read instructions are well spaced and interspersed with a sufficient number of instructions to hide latency. We also notice that the compiler multiplies the weights mentioned above directly using v_madmk_f32 (for example v_madmk_f32 v8, v12, 0x3e052640, v8: the 0x3e052640 is a literal that corresponds to a weight). The fp16 can’t use a similar instruction and stores the literals in scalar registers instead).

On the other hand, the fp16 version, seems more keen to read and cache the radiance data in VGPRs instead:

```
ds_read2st64_b32 v[45:46], v46 offset1:4 // 000000000514: D8700400 2D00002E
v_pk_add_f16 v49, v47, v49 op_sel_hi:[1,1] // 00000000051C: D38F0031 1802632F
s_waitcnt lgkmcnt(6) // 000000000524: BF8CC67F
v_pk_mul_f16 v51, v33, s15 op_sel:[1,0] op_sel_hi:[0,0] // 000000000528: D3900833 00001F21
v_add_u32 v52, 0x00000090, v105 // 000000000530: 6868D2FF 00000090
ds_read2st64_b32 v[47:48], v48 offset1:4 // 000000000538: D8700400 2F000030
v_pk_add_f16 v51, v49, v51 op_sel_hi:[1,1] // 000000000540: D38F0033 18026731
s_waitcnt lgkmcnt(6) // 000000000548: BF8CC67F
v_pk_mul_f16 v53, v35, s14 op_sel:[1,0] op_sel_hi:[0,0] // 00000000054C: D3900835 00001D23
v_add_u32 v54, 0x00000094, v105 // 000000000554: 686CD2FF 00000094
ds_read2st64_b32 v[49:50], v50 offset1:4 // 00000000055C: D8700400 31000032
v_pk_add_f16 v53, v51, v53 op_sel_hi:[1,1] // 000000000564: D38F0035 18026B33
s_waitcnt lgkmcnt(6) // 00000000056C: BF8CC67F
v_pk_mul_f16 v55, v37, s13 op_sel:[1,0] op_sel_hi:[0,0] // 000000000570: D3900837 00001B25
v_add_u32 v56, 0x00000098, v105 // 000000000578: 6870D2FF 00000098
ds_read2st64_b32 v[51:52], v52 offset1:4 // 000000000580: D8700400 33000034
v_pk_add_f16 v55, v53, v55 op_sel_hi:[1,1] // 000000000588: D38F0037 18026F35
s_waitcnt lgkmcnt(6) // 000000000590: BF8CC67F
v_pk_mul_f16 v57, v39, s12 op_sel:[1,0] op_sel_hi:[0,0] // 000000000594: D3900839 00001927
v_add_u32 v58, 0x0000009c, v105 // 00000000059C: 6874D2FF 0000009C
ds_read2st64_b32 v[53:54], v54 offset1:4 // 0000000005A4: D8700400 35000036
v_pk_add_f16 v57, v55, v57 op_sel_hi:[1,1] // 0000000005AC: D38F0039 18027337
s_waitcnt lgkmcnt(6) // 0000000005B4: BF8CC67F
v_pk_mul_f16 v59, v41, s6 op_sel:[1,0] op_sel_hi:[0,0] // 0000000005B8: D390083B 00000D29
v_add_u32 v60, 0x000000a0, v105 // 0000000005C0: 6878D2FF 000000A0
ds_read2st64_b32 v[55:56], v56 offset1:4 // 0000000005C8: D8700400 37000038
v_pk_add_f16 v59, v57, v59 op_sel_hi:[1,1] // 0000000005D0: D38F003B 18027739
s_waitcnt lgkmcnt(6) // 0000000005D8: BF8CC67F
v_pk_mul_f16 v61, v43, s7 op_sel:[1,0] op_sel_hi:[0,0] // 0000000005DC: D390083D 00000F2B
v_add_u32 v62, 0x000000c0, v105 // 0000000005E4: 687CD2FF 000000C0
ds_read2st64_b32 v[57:58], v58 offset1:4 // 0000000005EC: D8700400 3900003A
v_pk_add_f16 v61, v59, v61 op_sel_hi:[1,1] // 0000000005F4: D38F003D 18027B3B
s_waitcnt lgkmcnt(6) // 0000000005FC: BF8CC67F
v_pk_mul_f16 v63, v45, s13 op_sel:[1,0] op_sel_hi:[0,0] // 000000000600: D390083F 00001B2D
s_movk_i32 s16, 0x3620 // 000000000608: B0103620
v_add_u32 v64, 0x000000c4, v105 // 00000000060C: 6880D2FF 000000C4
```

Going back to the fp32 version and focusing on a group memory read instruction on line 199 as an example

`199: ds_read2st64_b32 v[57:58], v52`


It stores the 2 uint packed number in registers v57 and v58. Looking at where those registers are next used, it is on lines

`298: v_cvt_f32_f16 v31, v57`


and

`310: v_cvt_f32_f16 v26, v58`


around 100 lines from when they were read. Once used, those registers are returned to the pool and can be reused. If we do the same for the f16 version

`200: ds_read2st64_b32 v[43:44], v44`


the register v43 is used in this line, quite soon after read

`234: v_pk_mul_f16 v61, v43, s3 op_sel:[1,0] op_sel_hi:[0, 0]`


but v44(containing the second uint and third component of the radiance) is read in line

`509: v_pack_b32_f16 v19, v23, v44`


almost 300 instructions later, being kept alive all that time.

The ds_read2st64_b32 instruction is used in both versions of the shader to read 2 32-bits from the group shared memory which is allocated in 2 uint arrays of 16×16 elements as mentioned above.

groupshared uint g_ffx_dnsr_shared_0[16][16];

groupshared uint g_ffx_dnsr_shared_1[16][16];

It uses offsets to get the appropriate 4 byte value in array, for example

```
ds_read2st64_b32 v[55:56], v56 offset1:4
ds_read2st64_b32 v[85:86], v85 offset0:1 offset1:5
```


For both elements the address is calculated as base + offset * 64 * 4. As you can see in the offsets specified above, each element will differ by 1024 bytes in address space, which makes sense since each groupshared array is 16*16*4 = 1024 bytes in size.

All of the fp32 version of the shader uses this pattern to read 2 elements in parallel from the two arrays and processing them. This does not hold true for the fp16 version though, after it has issued 41 ds_read2st64_b32 instructions, which as discussed read one element from each 16×16 array in parallel, it switches to using **ds_read2_b32** for the next 40 groupshared memory reads:

```
ds_read2st64_b32 v[85:86], v85 offset0:1 offset1:5 // 0000000007C8: D8700501 55000055
v_pk_add_f16 v87, v87, v88 op_sel_hi:[1,1] // 0000000007D0: D38F0057 1802B157
s_waitcnt lgkmcnt(6) // 0000000007D8: BF8CC67F
v_pk_mul_f16 v88, v73, s17 op_sel:[1,0] op_sel_hi:[0,0] // 0000000007DC: D3900858 00002349
v_pk_add_f16 v89, v87, v88 op_sel_hi:[1,1] // 0000000007E4: D38F0059 1802B157
s_waitcnt lgkmcnt(5) // 0000000007EC: BF8CC57F
v_pk_mul_f16 v90, v75, s14 op_sel:[1,0] op_sel_hi:[0,0] // 0000000007F0: D390085A 00001D4B
ds_read2_b32 v[87:88], v105 offset0:69 offset1:70 // 0000000007F8: D86E4645 57000069
v_pk_add_f16 v89, v89, v90 op_sel_hi:[1,1] // 000000000800: D38F0059 1802B559
s_waitcnt lgkmcnt(5) // 000000000808: BF8CC57F
v_pk_mul_f16 v90, v77, s10 op_sel:[1,0] op_sel_hi:[0,0] // 00000000080C: D390085A 0000154D
v_pk_add_f16 v91, v89, v90 op_sel_hi:[1,1] // 000000000814: D38F005B 1802B559
s_waitcnt lgkmcnt(4) // 00000000081C: BF8CC47F
v_pk_mul_f16 v92, v79, s11 op_sel:[1,0] op_sel_hi:[0,0] // 000000000820: D390085C 0000174F
ds_read2_b32 v[89:90], v105 offset0:71 offset1:72 // 000000000828: D86E4847 59000069
v_pk_add_f16 v91, v91, v92 op_sel_hi:[1,1] // 000000000830: D38F005B 1802B95B
s_waitcnt lgkmcnt(4) // 000000000838: BF8CC47F
v_pk_mul_f16 v92, v81, s15 op_sel:[1,0] op_sel_hi:[0,0] // 00000000083C: D390085C 00001F51
v_pk_add_f16 v93, v91, v92 op_sel_hi:[1,1] // 000000000844: D38F005D 1802B95B
s_waitcnt lgkmcnt(3) // 00000000084C: BF8CC37F
v_pk_mul_f16 v94, v83, s18 op_sel:[1,0] op_sel_hi:[0,0] // 000000000850: D390085E 00002553
ds_read2_b32 v[91:92], v105 offset0:80 offset1:81 // 000000000858: D86E5150 5B000069
v_pk_add_f16 v93, v93, v94 op_sel_hi:[1,1] // 000000000860: D38F005D 1802BD5D
s_waitcnt lgkmcnt(3)
```

the difference being that this instruction calculates the address as base + offset * 4. We notice that now, for the second half of the shader, it doesn’t read elements from the two 16×16 uint arrays but 2 elements from the same array.

It is not clear what causes this weird access pattern. The main goal of the compiler would be to hide memory latency, it could be that it is struggling to pack and perform operations on half3s instead of half4s (which utilise 32bit registers and packed Maths better) to add between memory reads and maybe it resorts to using more VGPRs as intermediate storage while it looks for opportunities to do so. The fact that all the weights are stored in scalar registers, instead of being literals in the operations, like in the fp32 version, probably does not help as well.

A quick test to force the shader to use all data in the groupshared memory, i.e. converting the 2 uints to a half4 and performing operations on half4s instead of half3 types changes the output drastically:

```
ds_read2st64_b32 v[34:35], v13 offset1:4 // 000000000F90: D8700400 2200000D
ds_read2st64_b32 v[13:14], v14 offset1:4 // 000000000F98: D8700400 0D00000E
ds_read2st64_b32 v[36:37], v25 offset1:4 // 000000000FA0: D8700400 24000019
ds_read2st64_b32 v[25:26], v26 offset1:4 // 000000000FA8: D8700400 1900001A
ds_read2st64_b32 v[38:39], v30 offset1:4 // 000000000FB0: D8700400 2600001E
ds_read2st64_b32 v[30:31], v31 offset1:4 // 000000000FB8: D8700400 1E00001F
s_waitcnt lgkmcnt(5) // 000000000FC0: BF8CC57F
s_nop 0x0000 // 000000000FC4: BF800000
v_pk_mul_f16 v40, v34, s17 op_sel:[1,0] op_sel_hi:[0,0] // 000000000FC8: D3900828 00002322
v_pk_mul_f16 v41, v35, s17 op_sel:[1,0] op_sel_hi:[0,0] // 000000000FD0: D3900829 00002323
v_pk_add_f16 v11, v11, v40 op_sel_hi:[1,1] // 000000000FD8: D38F000B 1802510B
v_pk_add_f16 v12, v12, v41 op_sel_hi:[1,1] // 000000000FE0: D38F000C 1802530C
v_pk_mul_f16 v34, v34, v34 op_sel:[1,1] op_sel_hi:[0,0] // 000000000FE8: D3901822 00024522
v_pk_mul_f16 v35, v35, v35 op_sel:[1,1] op_sel_hi:[0,0] // 000000000FF0: D3901823 00024723
v_pk_mul_f16 v34, v34, s17 op_sel_hi:[1,0] // 000000000FF8: D3900022 08002322
v_pk_mul_f16 v35, v35, s17 op_sel_hi:[1,0] // 000000001000: D3900023 08002323
v_pk_add_f16 v0, v0, v34 op_sel_hi:[1,1] // 000000001008: D38F0000 18024500
v_pk_add_f16 v1, v1, v35 op_sel_hi:[1,1] // 000000001010: D38F0001 18024701
s_waitcnt lgkmcnt(4) // 000000001018: BF8CC47F
s_nop 0x0000 // 00000000101C: BF800000
v_pk_mul_f16 v34, v13, s18 op_sel:[1,0] op_sel_hi:[0,0] // 000000001020: D3900822 0000250D
v_pk_mul_f16 v35, v14, s18 op_sel:[1,0] op_sel_hi:[0,0] // 000000001028: D3900823 0000250E
v_pk_add_f16 v11, v11, v34 op_sel_hi:[1,1] // 000000001030: D38F000B 1802450B
v_pk_add_f16 v12, v12, v35 op_sel_hi:[1,1] // 000000001038: D38F000C 1802470C
v_pk_mul_f16 v13, v13, v13 op_sel:[1,1] op_sel_hi:[0,0] // 000000001040: D390180D 00021B0D
v_pk_mul_f16 v14, v14, v14 op_sel:[1,1] op_sel_hi:[0,0] // 000000001048: D390180E 00021D0E
v_pk_mul_f16 v13, v13, s18 op_sel_hi:[1,0] // 000000001050: D390000D 0800250D
v_pk_mul_f16 v14, v14, s18 op_sel_hi:[1,0] // 000000001058: D390000E 0800250E
v_pk_add_f16 v0, v0, v13 op_sel_hi:[1,1] // 000000001060: D38F0000 18021B00
v_pk_add_f16 v1, v1, v14 op_sel_hi:[1,1] // 000000001068: D38F0001 18021D01
```

The compiler can now read the data from groupshared memory already packed to 32 bit registers and schedules the reads in such a way so as to hide latency without allocating a large number of VGPRs. You can see above that the registers with the read data (eg v34) are used almost immediately. In this case the fp16 shader allocation drops from 108 to 48 VGPRs but the length of the shader increases by about 150 instructions due to the extra work done on the 4th component. Providing better opportunities for packing definitely helps it seems.

The other thing in the original shader that seems weird is the fact that it splits .xy and .z into 2 uint arrays instead of using a single uint2 array (**Update**: I realised after I wrote this that this is probably done to avoid group shared memory bank conflicts. Even in that case this shows that it is good to profile the code to determine actual impact of any option, and if, for example, the latency of any conflict in this instance can be hidden by improved code generation). Changing the original code to use a single 16×16 uint2 array has again a big impact to the produced ISA:

```
ds_read2_b32 v[20:21], v16 offset1:1 // 0000000005FC: D86E0100 14000010
v_pk_mul_f16 v7, v7, s6 op_sel_hi:[1,0] // 000000000604: D3900007 08000D07
v_pk_add_f16 v1, v1, v7 op_sel_hi:[1,1] // 00000000060C: D38F0001 18020F01
s_waitcnt lgkmcnt(0) // 000000000614: BF8CC07F
v_pk_mul_f16 v7, v20, s0 op_sel:[1,0] op_sel_hi:[0,0] // 000000000618: D3900807 00000114
v_mul_f16 v16, v21, v21 // 000000000620: 44202B15
v_pack_b32_f16 v16, v16, v21 // 000000000624: D2A00010 00022B10
v_pk_mul_f16 v16, v16, s0 op_sel_hi:[1,0] // 00000000062C: D3900010 08000110
v_pk_add_f16 v2, v2, v7 op_sel_hi:[1,1] // 000000000634: D38F0002 18020F02
v_pk_add_f16 v6, v6, v16 op_sel_hi:[1,1] // 00000000063C: D38F0006 18022106
v_pk_mul_f16 v7, v20, v20 op_sel:[1,1] op_sel_hi:[0,0] // 000000000644: D3901807 00022914
ds_read2_b32 v[20:21], v17 offset0:40 offset1:41 // 00000000064C: D86E2928 14000011
v_pk_mul_f16 v7, v7, s0 op_sel_hi:[1,0] // 000000000654: D3900007 08000107
v_pk_add_f16 v1, v1, v7 op_sel_hi:[1,1] // 00000000065C: D38F0001 18020F01
v_pk_mul_f16 v7, v9, s6 op_sel_hi:[1,0] // 000000000664: D3900007 08000D09
v_pk_add_f16 v2, v2, v32 op_sel_hi:[1,1] // 00000000066C: D38F0002 18024102
v_pk_add_f16 v6, v6, v7 op_sel_hi:[1,1] // 000000000674: D38F0006 18020F06
v_pk_mul_f16 v7, v8, v8 op_sel:[1,1] op_sel_hi:[0,0] // 00000000067C: D3901807 00021108
v_pk_mul_f16 v7, v7, s6 op_sel_hi:[1,0] // 000000000684: D3900007 08000D07
v_pk_add_f16 v1, v1, v7 op_sel_hi:[1,1] // 00000000068C: D38F0001 18020F01
s_movk_i32 s10, 0x2f62 // 000000000694: B00A2F62
v_pk_mul_f16 v7, v10, s10 op_sel:[1,0] op_sel_hi:[0,0] // 000000000698: D3900807 0000150A
v_mul_f16 v8, v11, v11 // 0000000006A0: 4410170B
v_pack_b32_f16 v8, v8, v11 // 0000000006A4: D2A00008 00021708
ds_read2_b32 v[22:23], v17 offset0:42 offset1:43 // 0000000006AC: D86E2B2A 16000011
v_pk_mul_f16 v8, v8, s10 op_sel_hi:[1,0] // 0000000006B4: D3900008 08001508
v_pk_add_f16 v2, v2, v7 op_sel_hi:[1,1] // 0000000006BC: D38F0002 18020F02
v_pk_add_f16 v6, v6, v8 op_sel_hi:[1,1] // 0000000006C4: D38F0006 18021106
v_pk_mul_f16 v7, v10, v10 op_sel:[1,1] op_sel_hi:[0,0] // 0000000006CC: D3901807 0002150A
v_pk_mul_f16 v7, v7, s10 op_sel_hi:[1,0] // 0000000006D4: D3900007 08001507
v_pk_add_f16 v1, v1, v7 op_sel_hi:[1,1] // 0000000006DC: D38F0001 18020F01
s_movk_i32 s11, 0x32b9 // 0000000006E4: B00B32B9
v_pk_mul_f16 v7, v12, s11 op_sel:[1,0] op_sel_hi:[0,0] // 0000000006E8: D3900807 0000170C
v_mul_f16 v8, v13, v13 // 0000000006F0: 44101B0D
v_pack_b32_f16 v8, v8, v13
```

ds_read2st64_b32 instructions are now replaced by ds_read2_b32 memory reads to read the radiance data components consecutively and the shader adds enough ALU instruction in between memory reads to hide the latency, reducing the need to allocate a large number of VGPRs. The allocation in this case is 37 VGPRs compared to the original 108 (for the fp16 version) and the shader is about the same length.

One final consideration, would using a half3 instead of a uint2 packed array help?

```
ds_read_u16_d16 v17, v13 // 0000000009E0: D8B40000 1100000D
ds_read_u16_d16 v20, v13 offset:4 // 0000000009E8: D8B40004 1400000D
ds_read_u16_d16_hi v20, v13 offset:2 // 0000000009F0: D8B60002 1400000D
ds_read_u16_d16_hi v17, v14 // 0000000009F8: D8B60000 1100000E
ds_read_u16_d16 v13, v14 offset:4 // 000000000A00: D8B40004 0D00000E
ds_read_u16_d16_hi v13, v14 offset:2 // 000000000A08: D8B60002 0D00000E
ds_read_u16 v14, v15 // 000000000A10: D8780000 0E00000F
s_waitcnt lgkmcnt(3) // 000000000A18: BF8CC37F
s_nop 0x0000 // 000000000A1C: BF800000
v_mul_f16 v21, v17, v17 // 000000000A20: 442A2311
v_pack_b32_f16 v21, v21, v17 // 000000000A24: D2A00015 00022315
v_pk_mul_f16 v21, v21, s12 op_sel_hi:[1,0] // 000000000A2C: D3900015 08001915
v_pk_mul_f16 v26, v20, s12 op_sel_hi:[1,0] // 000000000A34: D390001A 08001914
v_pk_add_f16 v1, v1, v21 op_sel_hi:[1,1] // 000000000A3C: D38F0001 18022B01
v_pk_add_f16 v0, v0, v26 op_sel_hi:[1,1] // 000000000A44: D38F0000 18023500
v_pk_mul_f16 v20, v20, v20 op_sel_hi:[1,1] // 000000000A4C: D3900014 18022914
v_pk_mul_f16 v20, v20, s12 op_sel_hi:[1,0] // 000000000A54: D3900014 08001914
v_pk_add_f16 v6, v6, v20 op_sel_hi:[1,1] // 000000000A5C: D38F0006 18022906
v_mul_f16 v20, v17, v17 dst_sel:WORD_0 dst_unused:UNUSED_PRESERVE src0_sel:WORD_1 src1_sel:WORD_1 // 000000000A64: 442822F9 05051411
v_pack_b32_f16 v17, v20, v17 op_sel:[0,1,0] // 000000000A6C: D2A01011 00022314
v_pk_mul_f16 v17, v17, s11 op_sel_hi:[1,0] // 000000000A74: D3900011 08001711
s_waitcnt lgkmcnt(1) // 000000000A7C: BF8CC17F
v_pk_mul_f16 v20, v13, s11 op_sel_hi:[1,0] // 000000000A80: D3900014 0800170D
v_pk_add_f16 v1, v1, v17 op_sel_hi:[1,1] // 000000000A88: D38F0001 18022301
v_pk_add_f16 v0, v0, v20 op_sel_hi:[1,1] // 000000000A90: D38F0000 18022900
v_pk_mul_f16 v13, v13, v13 op_sel_hi:[1,1] // 000000000A98: D390000D 18021B0D
v_pk_mul_f16 v13, v13, s11 op_sel_hi:[1,0] // 000000000AA0: D390000D 0800170D
v_pk_add_f16 v6, v6, v13 op_sel_hi:[1,1] // 000000000AA8: D38F0006 18021B06
s_waitcnt lgkmcnt(0) // 000000000AB0: BF8CC07F
v_mul_f16 v13, v14, v14 // 000000000AB4: 441A1D0E
v_pack_b32_f16 v13, v13, v14 // 000000000AB8: D2A0000D 00021D0D
v_pk_mul_f16 v13, v13, s10 op_sel_hi:[1,0] // 000000000AC0: D390000D 0800150D
v_pk_add_f16 v1, v1, v13 op_sel_hi:[1,1] // 000000000AC8: D38F0001 18021B01
v_add3_u32 v13, v3, v2, 24 // 000000000AD0: D1FF000D 02620503
v_lshl_add_u32 v13, v13, 1, v13 // 000000000AD8: D1FD000D 0435030D
v_lshlrev_b32 v13, 1, v13 // 000000000AE0: 241A1A81
v_add3_u32 v14, v3, v2, 32 // 000000000AE4: D1FF000E 02820503
v_lshl_add_u32 v14, v14, 1, v14 // 000000000AEC: D1FD000E 0439030E
v_lshlrev_b32 v14, 1, v14
```

The memory read pattern is closer to when we read and did Maths on all components of the radiance (.w included), using ds_read_u16_d16 to read 16bits of data to store to the low word (bits 15-0) of the register or ds_read_u16_d16_hi to store to the high word of the destination register (bits 31-16) directly, without the need for packing instructions. This access pattern allows for the lowest VGPR allocation (28) as well and good register reuse, increasing the line count to 1611. Interesting to note that the number of accesses to the group shared memory now went up to 232, compared to the 81 in the other cases. Also this is the only modification that drops that original cost of the fp16 version of the shader by 25%, on an AMD integrated GPU (GCN5). And since we all like graphs showcasing improvements, this is the one from the top of the page with the VGPR allocation after the last change.

![](../../assets/ded100668a65476b.png)


![](../../assets/ded100668a65476b.png)

It appears that fp16 can provide opportunities to reduce VGPR allocation, and the success of this can depend on the complexity of the data type and memory access. It is although worth noting the reduced VGPR allocation, which leads to increased occupancy, is not the only way to hide memory latency, the compiler may be able to do that during code generation [by moving code around](https://interplayoflight.wordpress.com/2020/11/11/what-is-shader-occupancy-and-why-do-we-care-about-it/) if it has enough suitable instructions available to do so, like discussed above.

Sadly I doubt there are reusable best practices to be extracted from this. It all seems rather likely to change unpredictably between GPUs and compiler versions… the smarter a compiler gets, the less predictable it tends to become.

That’s why I liked the approach taken by Halide; a more direct specification of the optimizations you expected the compiler to perform, albeit within a limited algorithmic domain.