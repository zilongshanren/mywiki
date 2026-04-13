---
title: Enhancing DirectX Testing with AMD Smoldr - AMD GPUOpen
url: https://gpuopen.com/learn/enhancing-directx-testing-with-smoldr/
published: '2026-03-17'
source_blog: gpuopen.com
source_site: https://gpuopen.com
category: Graphics Programming Weekly — Jendrik Illner → linked
fetched: '2026-04-13'
---

[ ](https://gpuopen.com/fidelityfx-variable-shading/)


![AMD FidelityFX™ Variable Shading](../../assets/a2e9842e47b14fcd.jpg)

AMD FidelityFX™ Variable Shading

AMD FidelityFX Variable Shading drives Variable Rate Shading into your game.

Writing small graphics applications and running them has historically not been a small feat.
Especially with the emergence of low-level APIs like Microsoft DirectX® 12 and Vulkan™, it takes many lines of code for setup until shader code is running on a GPU.

With Google’s release of [Amber](https://github.com/google/amber), this changed for Vulkan.
Amber made it possible to declare buffers and shaders and run them on the GPU, all in just a few lines of code.
Until now, we were missing an equivalent for DirectX.

Today, we are releasing AMD [Smoldr](https://github.com/GPUOpen-Tools/smoldr), a simple scripting tool to run DirectX 12 shaders on GPUs using a text input file.

Smoldr allows compiling HLSL shaders through DXIL, creating pipelines, resources, views, and then binding and running a compute dispatch. This is all controlled by a text based script file – no C++ development needed.

The project is open-source ([GitHub repository](https://github.com/GPUOpen-Tools/smoldr)), contributions are welcome.
Note that Smoldr is work-in-progress, the script syntax is not fixed and may change in the future.
Being a command-line tool, the focus so far is compute, so compute shaders work well, but all of raytracing is supported too!

One ~~picture~~ script says more than a thousand words, so here is an example on how it looks, adding together the content of two buffers and writing the results into a third:

```
# Create a HLSL source called csshaderSOURCE csshaderByteAddressBuffer inbuf[2] : register(t0); // SRVRWByteAddressBuffer outbuf : register(u0); // UAV
// One workgroup consists of 32 threads[numthreads(32, 1, 1)]void CSMain(uint3 DTid : SV_DispatchThreadID){ // Take 2 numbers from first buffer, one from second, and sum them unsigned int first_idx = DTid.x * 2; float first = inbuf[0].Load<float>(first_idx * 4) + inbuf[0].Load<float>((first_idx + 1) * 4); float sum = first + inbuf[1].Load<float>(DTid.x * 4); outbuf.Store<float>(DTid.x * 4, sum);}END
# Compile the source with dxc into a binary called csobjOBJECT csobj csshader cs_6_4 CSMain
# Allocate buffers in GPU memory for input and outputBUFFER inbuf DATA_TYPE float SIZE 64 SERIES_FROM 0 INC_BY .25BUFFER inbuf2 DATA_TYPE float SIZE 32 SERIES_FROM 10.0 INC_BY .25BUFFER outbuf DATA_TYPE float SIZE 32 FILL 0
# The root signatureROOT default TABLE UAV REGISTER 0 NUMBER 1 SPACE 0 TABLE SRV REGISTER 0 NUMBER 2 SPACE 0END
# Create a compute pipeline called cspipePIPELINE cspipe COMPUTE ATTACH csobj ROOT defaultEND
# Create views that point to the complete buffersVIEW inview inbuf AS SRVVIEW inview2 inbuf2 AS SRVVIEW outview outbuf AS UAV
# Run the pipeline with 1x1x1 workgroups, so 32 threadsDISPATCH cspipe BIND 0 TABLE outview BIND 1 TABLE inviewRUN 1 1 1
# Outbuf should contain the added inbuf + inbuf2 now# Check that the shader worked as expectedEXPECT outbuf float OFFSET 0 EQ 10.25 11.5 12.75 14EXPECT outbuf float OFFSET 64 EQ 30.25 31.5 32.75 34
# Print a buffer's content to the terminalDUMP outbuf float
```


Nothing more than that is needed to run a full-fledged DirectX 12 application:

![Successful Smoldr run](../../assets/7f79962949a2eeb0.png)


Smoldr is built to play around with the DirectX 12 API, with drivers and with hardware. That makes it essential to be as helpful as possible when something unexpected happens. Even for just a typo, Smoldr points out where and what went wrong:

![Smoldr showing an error message](../../assets/5097b5652ef5e37e.png)


Other notable features include support for the Microsoft Agility SDK to try out new, experimental HLSL features.
Graphics tools like the [AMD Radeon™ GPU Profiler](https://gpuopen.com/rgp/) can capture Smoldr scripts by using the `--window`

option, spawning a window and executing the script once every frame.

Compute and raytracing pipelines are working well, so the next big thing to support is mesh shaders. Mesh (and amplification) shaders will allow to easily use modern graphics rendering with Smoldr. Look out for that!

The source code is [ available on GitHub](https://github.com/GPUOpen-Tools/smoldr).

The scripting language syntax can be found [ here](https://github.com/GPUOpen-Tools/smoldr/blob/main/Documentation.md).

Discuss this blog on the [ AMD Developer Community](https://discord.gg/amd-dev).

Sign up to our [ AMD Developer Newsletter](https://www.amd.com/en/forms/sign-up/developer-news.html) for the latest updates.

*DirectX is either a registered trademark or trademark of Microsoft Corporation in the US and/or other countries.*

*Vulkan and the Vulkan logo are registered trademarks of the Khronos Group Inc. Other names are for informational purposes only and may be trademarks of their respective owners.*