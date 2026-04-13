---
title: Learning DirectX 12
url: https://www.3dgep.com/learning-directx-12-1/
author: Jeremiah
published: '2017-12-14'
source_blog: 3D Game Engine Programming
source_site: https://www.3dgep.com/
category: graphics
fetched: '2026-04-13'
---

This is the first lesson in a series of lessons to teach you how to create a DirectX 12 application from scratch. In this lesson, you will learn how to query for DirectX 12 capable display adapters that are available, create a DirectX 12 device, create a swap-chain, and you will also learn how to present the swap chain back buffer to the screen. In this lesson, you will also create a command queue and a command list and learn how to synchronize the CPU and GPU operations in order to correctly implement N-buffered rendering.


Contents

[1 Introduction](https://www.3dgep.com#Introduction)-
[2 DirectX API](https://www.3dgep.com#DirectX_API) -
[3 DirectX 12 Graphics Pipeline](https://www.3dgep.com#DirectX_12_Graphics_Pipeline) -
[4 GPU Synchronization](https://www.3dgep.com#GPU_Synchronization) -
[5 Dependencies](https://www.3dgep.com#Dependencies) -
[6 DirectX 12 Demo](https://www.3dgep.com#DirectX_12_Demo)[6.1 Preamble](https://www.3dgep.com#Preamble)[6.2 Parse Command-line Arguments](https://www.3dgep.com#Parse_Command-line_Arguments)[6.3 Enable the Direct3D 12 Debug Layer](https://www.3dgep.com#Enable_the_Direct3D_12_Debug_Layer)[6.4 Register the Window Class](https://www.3dgep.com#Register_the_Window_Class)[6.5 Create Window Instance](https://www.3dgep.com#Create_Window_Instance)[6.6 Query DirectX 12 Adapter](https://www.3dgep.com#Query_DirectX_12_Adapter)[6.7 Create the DirectX 12 Device](https://www.3dgep.com#Create_the_DirectX_12_Device)[6.8 Create the Command Queue](https://www.3dgep.com#Create_the_Command_Queue)[6.9 Check for Tearing Support](https://www.3dgep.com#Check_for_Tearing_Support)[6.10 Create the Swap Chain](https://www.3dgep.com#Create_the_Swap_Chain)[6.11 Create a Descriptor Heap](https://www.3dgep.com#Create_a_Descriptor_Heap)[6.12 Create the Render Target Views](https://www.3dgep.com#Create_the_Render_Target_Views)[6.13 Create a Command Allocator](https://www.3dgep.com#Create_a_Command_Allocator)[6.14 Create a Command List](https://www.3dgep.com#Create_a_Command_List)[6.15 Create a Fence](https://www.3dgep.com#Create_a_Fence)[6.16 Create an Event](https://www.3dgep.com#Create_an_Event)[6.17 Signal the Fence](https://www.3dgep.com#Signal_the_Fence)[6.18 Wait for Fence Value](https://www.3dgep.com#Wait_for_Fence_Value)[6.19 Flush the GPU](https://www.3dgep.com#Flush_the_GPU)[6.20 Update](https://www.3dgep.com#Update)-
[6.21 Render](https://www.3dgep.com#Render) [6.22 Resize](https://www.3dgep.com#Resize)[6.23 Fullscreen State](https://www.3dgep.com#Fullscreen_State)[6.24 Window Message Procedure](https://www.3dgep.com#Window_Message_Procedure)[6.25 The Main Entry Point](https://www.3dgep.com#The_Main_Entry_Point)

[7 Conclusion](https://www.3dgep.com#Conclusion)[8 Download the Source](https://www.3dgep.com#Download_the_Source)[9 References](https://www.3dgep.com#References)

DirectX 12 is the successor of the DirectX 11 SDK and represents the largest architectural change to the SDK since the inception of DirectX. The primary reason for this change is the demand from the gaming industry to provide a rendering SDK that gives more power and control to the graphics programmer. Vendor-specific driver implementations were often complex and imposed a CPU performance overhead that the developer had no control over. Much of this overhead could be avoided if you give control back to the developers. One example of the driver overhead that is present in previous versions of the DirectX SDK is resource management. Drivers needed to track the lifetime of every resource that was used by the rendering pipeline. Tracking of resources by the driver is often unnecessary if it can be assumed that the application programmer can perform this task with much less overhead. Providing the developers with the tools to implement their own resource management takes that responsibility away from the driver implementation and often allows for performance improvements if done correctly.

But with great power, comes great responsibility. It is true that this increased complexity makes learning DirectX 12 harder than learning previous versions of the DirectX SDK. As with all things, the first time you encounter something it may seem daunting or too difficult to learn but if you are persistent in your desire to learn this new SDK, the rewards will be well worth it. The previous versions of the DirectX SDK will still work but if you are either looking for a job in the game industry or just trying to update your knowledge and skills in the area of graphics programming, it is required that you learn the DirectX 12 SDK. Most gaming studios will only hire you as a graphics programmer if you have some experience with at least one of the new graphics programming API’s (DirectX 12 or Vulkan).

Don’t worry if you are a total noob when it comes to graphics programming. This lesson is written with no assumptions about your current skill level and assumes you have never written a graphics application before. You should already have some experience programming with C++. In this lesson, you may encounter some C++11 (threading, lambdas, smart pointers) or C++17 features that will not be explained in detail. This lesson is not designed to teach you C++ programming; It is assumed that you already have developed this skill.

DirectX is a collection of **Application Programming Interfaces** (APIs) developed by Microsoft. The various components of the DirectX API provide low-level access to the hardware running on Windows based operating systems [[6]](https://www.3dgep.com#cite-6).

The first version of DirectX was not released at the same time as Windows 95 but shortly after it in September 1995 [[6]](https://www.3dgep.com#cite-6). It was initially released under the name **Windows Game SDK**. **DirectX 2.0** was released in June 1996 and just four months later, the DirectX 3.0 APIs were released [[7]](https://www.3dgep.com#cite-7). Through the period of 1995-1997, the DirectX library went through several version changes to reach version 5. Subsequent major revisions were released on an annual basis until DirectX 9 which was released two years after DirectX 8 [[6]](https://www.3dgep.com#cite-6).

**DirectX 8.0** was released in November 2000 and introduced programmable vertex and pixel shaders giving the graphics programmer full control over the processing of the vertex and shading stages of the rendering pipeline. [Shader Model 1](https://msdn.microsoft.com/en-us/library/windows/desktop/bb509654(v=vs.85).aspx) [[9]](https://www.3dgep.com/cite-9) was the first shader model which introduced vertex and pixel shaders to the programmable pipeline.

**DirectX 9.0** was released in December 2002 and introduced [Shader Model 2.0](https://msdn.microsoft.com/en-us/library/windows/desktop/bb509655(v=vs.85).aspx) [[7]](https://www.3dgep.com#cite-7).

**DirectX 9.0c** was released in August 2004 and introduced [Shader Model 3.0](https://msdn.microsoft.com/en-us/library/windows/desktop/bb509656(v=vs.85).aspx) [[7]](https://www.3dgep.com#cite-7). Shader Model 3.0 extended on Shader Model 2.0 by adding additional functions to the HLSL shader language and increased the instruction count for vertex and pixel shaders allowing for more complex shader programs.

In November 2006, **DirectX 10** was released featuring [Shader Model 4.0](https://msdn.microsoft.com/en-us/library/windows/desktop/bb509657(v=vs.85).aspx) providing backward compatability with Shader Model 3.0 but deprecating Shader Model 1.0 [[10]](https://www.3dgep.com#cite-10). Shader Model 4.0 lifted the shader instruction limits and added the geometry shader profiles to the programmable shader pipeline. The geometry shader allows the graphics programmer to create new geometric primitives from simpler primitives (for example, take a single point as input to the geometry shader and produce a set of triangles).

**DirectX 11** was released in October 2009 and introduced [Shader Model 5.0](https://msdn.microsoft.com/en-us/library/windows/desktop/ff471356(v=vs.85).aspx) [[7]](https://www.3dgep.com#cite-7). Shader Model 5.0 added support for tessellation shaders as well as computer shaders. Tessellation shaders provide the ability to dynamically refine the level of detail of a model by computing the triangle primitives from control points of a Bezier surface (for example, but other tessellation techniques can also be implemented in the tessellation shader). Compute shaders allow the graphics programmer to create general purpose programs that advantage of the massive parallelism of the Graphics Processing Unit (GPU).

On July 29, 2015, together with the launch of Windows 10, Microsoft released version 12 of the DirectX API. **DirectX 12** (and Direct3D 11.3) also introduced [Shader Model 5.1](https://msdn.microsoft.com/en-us/library/windows/desktop/dn933277(v=vs.85).aspx). Shader Model 5.1 did not add any new programmable stages to the shader pipeline but it added support for accessing resources by indexing into descriptor arrays. Texture arrays were already possible prior to Shader Model 5.1 but each texture in the array had to have the same size (width, height) and storage format. Using descriptor arrays allows texture of varying dimensions and storage formats to be accessed from a single shader variable. The only restriction is the variable type (for example Texture1D, Texture2D, or Texture3D).

On April 11, 2017, together with the Windows 10 creators update (version 1703), Shader Model 6.0 was introduced. [Shader Model 6.0](https://msdn.microsoft.com/en-us/library/windows/desktop/mt733232(v=vs.85).aspx) adds additional wave-level intrinsic functions in HLSL. The wave-level intrinsic functions added in [Shader Model 6.0](https://msdn.microsoft.com/en-us/library/windows/desktop/mt733232(v=vs.85).aspx) allow the shader programmer to eliminate barrier constructs when the scope of synchronization is within the width of the SIMD processor (32 lanes on NVidia GPUs and 16 on AMD GPUs or some other set of threads that are known to be atomic relative to each other) [[7]](https://www.3dgep.com#cite-7)[[11]](https://www.3dgep.com#cite-11).

The DirectX SDK is actually a collection of Application Programming Interfaces (API’s). The API that is concerned with hardware accelerated 3D graphics rendering is called Direct3D and is the subject of this article. There are several more API’s which make up the DirectX SDK [[12]](https://www.3dgep.com#cite-12).

**Direct2D** is a hardware-accelerated, immediate-mode, 2D graphics API that provides high-performance and high-quality rendering for 2D geometry, bitmaps, and text. The Direct2D API is designed to interoperate with Direct3D.

**Direct3D** is a 3D graphics API that allows you to create high-performance rendering for 3D geometry. The Direct3D API also allows for the creation of high-performance general-purpose applications that can harness the parallelism of the GPU. Direct3D is the primary subject of this article. When the term DirectX 12 is used, it is often in reference to the Direct3D 12 graphics API.

DirectWrite supports high-quality text rendering, resolution-independent outline fonts, and full Unicode text and layouts.

DirectXMath provides an optimal and portable interface for arithmetic and linear algebra operations on single-precision floating-point vectors (2D, 3D, and 4D) or matrices (3×3 and 4×4).

Provides a signal processing and mixing foundation for games. XAudio2 replaces DirectSound.

Describes how to use the XInput API to interact with the Xbox Controller when it is connected to a Windows computer. XInput replaces DirectInput.

The DirectX 12 graphics pipeline consists of several stages. Some of the stages of the rendering pipeline are **fixed** which means that the stage is only configured through functions of the DirectX 12 API and does not have a “shader program”. Other stages are **programmable** and can be controlled by use of a “shader program”. The following diagram illustrates the various stages of the DirectX 12 graphics pipeline. The arrows indicate the flow of data from each stage of the graphics pipeline as well as from memory resources such as buffers, textures, and constant buffers that are available in high-speed GPU memory.

The image illustrates the various stages of the DirectX 12 rendering pipeline. The blue rectangular blocks represent the fixed-function stages and cannot be modified programmatically. The green rounded-rectangular blocks represent the programmable stages of the graphics pipeline.

The first stage of the graphics pipeline is the **Input-Assembler** (**IA**) stage. The purpose of the input-assembler stage is to read primitive data from user-defined vertex and index buffers and assemble that data into geometric primitives (line lists, triangle strips, or primitives with adjacency data).

The **Vertex Shader** (**VS**) stage is responsible for transforming the vertex data from object-space into clip-space. The vertex shader can also be used for performing (skeletal) animation or computing per-vertex lighting. The vertex shader takes a single vertex as input and outputs the clip-space position of the vertex. The vertex shader is the only shader stage that is absolutely required in order to define a valid pipeline state object [[15]](https://www.3dgep.com#cite-15).

The **Hull Shader** (**HS**) stage is an optional shader stage and is responsible for determining how much an input control patch should be tessellated by the tessellation stage [[14]](https://www.3dgep.com#cite-14).

The **Tessellator Stage** is a fixed-function stage that subdivides a patch primitive into smaller primitives according to the tessellation factors specified by the hull shader stage [[14]](https://www.3dgep.com#cite-14).

The **Domain Shader** (**DS**) stage is an optional shader stage and it computes the final vertex attributes based on the output control points from the hull shader and the interpolation coordinates from the tesselator stage [[14]](https://www.3dgep.com#cite-14). The input to the domain shader is a single output point from the tessellator stage and the output is the computed attributes of the tessellated primitive.

The **Geometry Shader** (**GS**) stage is an optional shader stage that takes a single geometric primitive (a single vertex for a point primitive, three vertices for a triangle primitive, and two vertices for a line primitive) as input and can either discard the primitive, transform the primitive into another primitive type (for example a point to a quad) or generate additional primitives.

The **Stream Output** (**SO**) stage is an optional fixed-function stage that can be used to feed primitive data back into GPU memory. This data can be recirculated back to the rendering pipeline to be processed by another set of shaders. This is useful for spawning or terminating particles in a particle effect. The geometry shader can discard particles that should be terminated or generate new particles if particles should be spawned.

The **Rasterizer Stage** (**RS**) stage is a fixed-function stage which will clip primitives into the view frustum and perform primitive culling if either front-face or back-face culling is enabled. The rasterizer stage will also interpolate the per-vertex attributes across the face of each primitive and pass the interpolated values to the pixel shader.

The **Pixel Shader** (**PS**) stage takes the interpolated per-vertex values from the rasterizer stage and produces one (or more) per-pixel color values. The pixel shader can also optionally output a depth value of the current pixel by mapping a single component 32-bit floating-point value to the

semantic but this is not a requirement of the pixel shader program. The pixel shader is invoked once for each pixel that is covered by a primitive [SV_Depth](https://msdn.microsoft.com/en-us/library/windows/desktop/bb509647(v=vs.85).aspx#System_Value)[[15]](https://www.3dgep.com#cite-15).

The **Output-Merger** (**OM**) stage combines the various types of output data (pixel shader output values, depth values, and stencil information) together with the contents of the currently bound render targets to produce the final pipeline result.

One of the more difficult concepts to understand for beginning DirectX 12 programmers is synchronization. In earlier versions of DirectX and in OpenGL there was no need to be concerned with GPU synchronization in order to get the GPU to render something, it was usually handled by the driver and required little to no intervention from the graphics programmer. In DirectX 12 the graphics programmer must perform explicit GPU synchronization. If GPU synchronization is not handled correctly the programmer will receive errors from the DirectX debug layer that will be difficult to understand and debug.

GPU synchronization is also very important to understand when performing resource management. Resources cannot be freed if they are currently being referenced in a command list that is being executed on a command queue. It is only safe to release those resources after the command queue has finished executing any command list that is referencing those resources.

Before going into too much detail about GPU synchronization, a few terms that may not be familiar are described.

The **Fence** object is used to synchronize commands issued to the **Command Queue**. The fence stores a single value that indicates the last value that was used to **signal** the fence. Although it is possible to use the same fence object with multiple command queues, it is not reliable to ensure the proper synchronization of commands across command queues. Therefore, it is advised to create at least one fence object for each command queue. Multiple command queues can wait on a fence to reach a specific value, but the fence should only be allowed to be signaled from a single command queue. In addition to the fence object, the application must also track a **fence value** that is used to signal the fence. An example of performing CPU-GPU synchronization using fences will be shown in the following sections.

A **Command List** is used to issue copy, compute (dispatch), or draw commands. In DirectX 12 commands issued to the command list are not executed immediately like they are with the DirectX 11 immediate context. All command lists in DirectX 12 are deferred; that is, the commands in a command list are only run on the GPU after they have been executed on a command queue.

The **Command Queue** in DirectX 12 has a very simple interface. For most common cases only the

method and the [ID3D12CommandQueue::ExecuteCommandLists](https://msdn.microsoft.com/en-us/library/windows/desktop/dn788631(v=vs.85).aspx)

method are used. Let’s look at a simple pseudo-code example of using a command queue.[ID3D12CommandQueue::Signal](https://msdn.microsoft.com/en-us/library/windows/desktop/dn899171(v=vs.85).aspx)

|
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
|
method IsFenceComplete( _fenceValue )
return fence->GetCompletedValue() >= _fenceValue
end method
method WaitForFenceValue( _fenceValue )
if ( !IsFenceComplete( _fenceValue )
fence->SetEventOnCompletion( _fenceValue, fenceEvent )
WaitForEvent( fenceEvent )
end if
end method
method Signal
_fenceValue <- AtomicIncrement( fenceValue )
commandQueue->Signal( fence, _fenceValue )
return _fenceValue
end method
method Render( frameID )
_commandList <- PopulateCommandList( frameID )
commandQueue->ExecuteCommandList( _commandList )
_nextFrameID <- Present()
fenceValues[frameID] = Signal()
WaitForFenceValue( fenceValues[_nextFrameID] )
frameID <- _nextFrameID
end method
|

In the pseudo-code listing above, there are four methods defined:

-
`IsFenceComplete`

: Check to see if the fence’s completed value has been reached. -
`WaitForFenceValue`

: Stall the CPU thread until the fence value has been reached. -
`Signal`

: Insert a fence value into the command queue. The fence used to signal the command queue will have it’s completed value set when that value is reached in the command queue. -
`Render`

: Render a frame. Do not move on to the next frame until that frame’s previous fence value has been reached.

The `Render`

method is responsible for rendering the scene. It does this by first populating the command list that contain all of the draw (or compute) commands that are needed to render the scene. The resulting command list is then executed on the command queue using the `ExecuteCommandList`

method. The call to to the `ExecuteCommandList`

method will not block the calling thread. It does not wait for the commands in the command list to be executed on the GPU before it returns to the caller.

The `Signal`

method will append a fence value to the end of the command queue. The fence object that is used to signal the command queue will have it’s completed value set to the value of the signal when processing has reached that point in the command queue. In other words, the completed value for the fence object will be set to the specified fence value only after all of the commands that were executed on the command queue prior to the `Signal`

have finished executing on the GPU. The call to `Signal`

does not block the calling thread but instead just returns the value to wait for before any (writable) GPU resources that are referenced in the command lists can be reused.

The `Present`

method (on line 23) will cause the rendered result to be presented to the screen. The return value from the `Present`

method (in this pseudo-code example) returns the index of the next backbuffer within the swap-chain to render to. When using the

flip model, the [DXGI_SWAP_EFFECT_FLIP_DISCARD](https://msdn.microsoft.com/en-us/library/windows/desktop/bb173077(v=vs.85).aspx)`Present`

method also does not block the main thread. For this reason, the back-buffer resource from the previous frame cannot be reused until the image has been presented to the screen.

To prevent the resource from being overwritten before they are presented to the screen, the CPU thread needs to wait for the fence value of the previous frame to be reached. The `WaitForFenceValue`

method is used to block the CPU thread until the specified fence value has been reached.

It is important to understand that each command queue must track it’s own fence and fence value. DirectX 12 defines three different command queue types:

-
**Copy**: Can be used to issue commands to copy resource data (CPU -> GPU, GPU -> GPU, GPU -> CPU). -
**Compute**: Can do everything a**Copy**queue can do and issue compute (dispatch) commands. -
**Direct**: Can do everything a**Copy**and a**Compute**queue can do and issue draw commands.

Although the DirectX 12 API defines these three different command queue types, it is not necessarily the case that the GPU in your computer actually has three physical work queues. It may also be the case that the GPU may have one dedicated work queue for each one of these types and it may even be the case that it has multiple work queues of each type. As far as I know, there doesn’t seem to be a reliable way of detecting how many queues the GPU has and what types. If you decide to create multiple queues in your own applications, you should allocate one fence object and track one fence value for each allocated command queue. Let’s take a look at a visual example to try to explain how to work with command queues.

In the [image above](https://www.3dgep.com#attachment_8017) several commands are issued on the main thread. In this example, the first frame is denoted `Frame N`. The command lists are executed on the command queue. Immediately after executing the command lists, the queue is signaled with the value `N`. When the command queue reaches that point, the fence will be signaled with the specified value.

Right after the `Signal`

, there is a `WaitForFenceValue`

command which waits for the previous frame (`Frame N-1`) to be finished. Since there were no commands in the command queue in `Frame N-1`, execution continues without stalling the CPU thread.

Then `Frame N+1` is built on the CPU thread and executed on the direct command queue. Before the CPU can continue, the command queue has to finish using the resources from `Frame N`. In this case, the CPU has to wait until signal `N` is reached which indicates that the command queue is finished with those resources.

After the command queue is finished with the resources from `Frame N`, `Frame N+2` can be built and executed on the queue. If the queue is still processing the commands from `Frame N+1`, then the CPU has to wait again for those resources to be available before continuing.

This example demonstrates a typical double-buffered scenario. You might think that using triple-buffering for rendering will reduce the amount of time the CPU has to wait for the GPU to finish its work. This is a naïve solution to the problem. Whenever the CPU is faster at issuing commands than the command queue is at processing those commands, the CPU will have to stall at some point in order to allow the command queue to catch-up to the CPU.

It gets more complicated if you add an additional queue. In this case, you must be careful not to signal the second queue with a fence value that is larger than, but could be completed before, a fence value that was used on another queue using the same fence object. Doing so could result in the fence reaching the fence value from the other queue before the main queue has reached the earlier fence value.

In the [image above](https://www.3dgep.com#attachment_8018) we see that the CPU executes the command list for `Frame N` and signals the `DirectQueue`

with a value of `N`. Meanwhile, the CPU also issues a dispatch command to the `ComputeQueue`

and signals that queue with a value `N+1`. If the `ComputeQueue`

reaches signal `N+1` before the `DirectQueue`

reaches `N` then the fence’s completed value will be set to `N+1`. When the `DirectQueue`

finally reaches the signal with value `N`, it will update the fence’s completed value to `N`. Since `N` is less than `N+1`, the fence’s completed value was decreased but the fence value should never be allowed to decrease!

The moral of the story is to make sure that every command queue tracks its own fence object and fence value and only signals its own fence object. To be safe, the fence value for a queue should never be allowed to decrease. If you are worried that the fence value will eventually overflow and reach 0 again, you must consider that a 64-bit unsigned integer value can have a maximum value of \(2^{64}-1\). If the command queue is signaled 100 times per frame and your game is rendering at an average of 300 FPS (the queue is signaled 30,000 times per second), the game could run for about 19.5 million years before the 64-bit fence value will overflow and wrap to 0.

In order to follow along with this tutorial series, you should ensure that you have the following software installed on your computer.

![](../../assets/27cd466625d90a55.png)

![](../../assets/bcb5e457aa8bcfdf.png)

[Visual Studio Download](https://www.visualstudio.com/downloads/)page and download the latest version of Visual Studio. The

**Community**edition is free for educational or open-source projects.

The DirectX 12 SDK comes included with the Windows 10 SDK which is part of the Visual Studio installation. Just make sure you install the **Game Development with C++** workload as shown in the following image.

![](../../assets/ba1a45015f0ba926.png)

You can download the latest version of CMake from [https://cmake.org/download/](https://cmake.org/download/). Starting from Visual Studio 2017, CMake is integrated into the Visual Studio IDE. For more information on using CMake with Visual Studio, check out my previous article titled [CMake in Visual Studio 2017](https://www.3dgep.com/cmake-visual-studio-2017/).

In the following sections, we will create the DirectX 12 demo application. In this tutorial, the demo will only create a window and clear the screen. Rendering of geometry will be handled in a later tutorial.

The following steps will be shown:

- Register the window class
- Create the window
- Query the GPU adapters
- Create a DirectX 12 device
- Create a command queue
- Create a swap chain
- Create command allocator & command list
- Handle GPU synchronization
- Update & Render
- Handle resizing
- Handle full-screen toggling

The preamble of the source includes the header files that are required to create the demo. Any variables that are used for the demo are also declared in the preamble.

First, the required Windows header files are declared.

|
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
|
#define WIN32_LEAN_AND_MEAN
#include <Windows.h>
#include <shellapi.h> // For CommandLineToArgvW
// The min/max macros conflict with like-named member functions.
// Only use std::min and std::max defined in <algorithm>.
#if defined(min)
#undef min
#endif
#if defined(max)
#undef max
#endif
// In order to define a function called CreateWindow, the Windows macro needs to
// be undefined.
#if defined(CreateWindow)
#undef CreateWindow
#endif
// Windows Runtime Library. Needed for Microsoft::WRL::ComPtr<> template class.
#include <wrl.h>
using namespace Microsoft::WRL;
|

Since this demo uses the Windows library functions, the ubiquitous `Windows.h`

header file is included on line 2. In order to minimize the number of header files that are included in the `Windows.h`

header, the

macro is defined just before the [WIN32_LEAN_AND_MEAN](https://msdn.microsoft.com/en-us/library/windows/desktop/aa383745(v=vs.85).aspx#Faster_Builds_with_Smaller_Header_Files)`Windows.h`

include.

The `shellapi.h`

header file included on line 3 contains the definition for the

function. This function will be used later to parse the command-line arguments passed to the application.[CommandLineToArgvW](https://msdn.microsoft.com/en-us/library/windows/desktop/bb776391(v=vs.85).aspx)

The `min`

and `max`

macros defined in the standard C library header file may conflict with the

and [std::min](http://en.cppreference.com/w/cpp/algorithm/min)

functions defined in the [std::max](http://en.cppreference.com/w/cpp/algorithm/max)

STL header. To avoid any compiler errors, the [algorithm](http://en.cppreference.com/w/cpp/header/algorithm)`min`

and `max`

macros should be undefined and only the

and [std::min](http://en.cppreference.com/w/cpp/algorithm/min)

functions should be used.[std::max](http://en.cppreference.com/w/cpp/algorithm/max)

In the `Windows.h`

header file, a macro called

is defined. Since a function with the same name is defined in this source file, the [CreateWindow](https://msdn.microsoft.com/en-us/library/windows/desktop/ms632679(v=vs.85).aspx)

macro is undefined on line 18. The [CreateWindow](https://msdn.microsoft.com/en-us/library/windows/desktop/ms632679(v=vs.85).aspx)

macro is not needed in this source file since the [CreateWindow](https://msdn.microsoft.com/en-us/library/windows/desktop/ms632679(v=vs.85).aspx)

function is used instead to create the OS window.[CreateWindowExW](https://msdn.microsoft.com/en-us/library/ms632680(v=vs.85).aspx)

The `wrl.h`

header file included on line 22 contains the definition of the

template class. The ComPtr template class provides smart pointer functionality for [ComPtr](https://docs.microsoft.com/en-us/cpp/windows/comptr-class)[COM objects](https://msdn.microsoft.com/en-us/library/windows/desktop/ms694363(v=vs.85).aspx). Please refer to [COM Coding Practices](https://msdn.microsoft.com/en-us/76aca556-b4d6-4e67-a2a3-4439900f0c39) for more information on proper use of COM pointers. Since all DirectX 12 objects are COM objects, the `ComPtr`

template class is used to track the COM object lifetimes.

In the next section, the DirectX 12 specific header files are included.

|
1
2
3
4
5
6
7
8
|
// DirectX 12 specific headers.
#include <d3d12.h>
#include <dxgi1_6.h>
#include <d3dcompiler.h>
#include <DirectXMath.h>
// D3D12 extension library.
#include <d3dx12.h>
|

The Direct3D 12 header file is included on line 26. This header file contains all of the Direct3D 12 objects (Device, CommandQueue, CommandList, etc…).

The [Microsoft DirectX Graphics Infrastructure (DXGI)](https://msdn.microsoft.com/en-us/library/windows/desktop/bb205075(v=vs.85).aspx) is used to manage the low-level tasks such as enumerating GPU adapters, presenting the rendered image to the screen, and handling full-screen transitions, that are not necessarily part of the DirectX rendering API. DXGI 1.6 adds functionality in order to detect HDR displays. HDR rendering will be discussed in another article.

The `d3dcompile.h`

header file contains functions to compile HLSL code at runtime. It is recommended to compile HLSL shaders at compile time (when the application is compiled into an executable) but for demonstration purposes, it might be more convenient to allow runtime compilation of HLSL shaders. Shaders will be introduced in the next lesson.

[D3DCompiler](https://msdn.microsoft.com/en-us/library/windows/desktop/dd607340(v=vs.85).aspx)functions, do not forget to link against the

`d3dcompiler.lib`

library and copy the `D3dcompiler_47.dll`

to the same folder as the binary executable when distributing your project.
A redistributable version of the `D3dcompiler_47.dll`

file can be found in the Windows 10 SDK installation folder at

For more information, refer to the MSDN blog post at: [https://blogs.msdn.microsoft.com/chuckw/2012/05/07/hlsl-fxc-and-d3dcompile/](https://blogs.msdn.microsoft.com/chuckw/2012/05/07/hlsl-fxc-and-d3dcompile/)


The DirectX Math library provides SIMD-friendly C++ types and functions for commonly used for graphics related programming [[16]](https://www.3dgep.com#cite-16). The DirectX Math library will be used in the later tutorials.

The D3D12 extension library (`d3dx12.h`

included on line 32) is not required to work with DirectX 12 but it provides some useful classes that will simplify some of the functions that will be used throughout this tutorial. The `d3dx12.h`

header file is not included as part of the Windows 10 SDK and needs to be downloaded separately from the Microsoft DirectX repository on GitHub ([https://github.com/Microsoft/DirectX-Graphics-Samples/tree/master/Libraries/D3DX12](https://github.com/Microsoft/DirectX-Graphics-Samples/tree/master/Libraries/D3DX12))

A few headers from the Standard Template Library (STL) are also included in the demo.

|
1
2
3
4
|
// STL Headers
#include <algorithm>
#include <cassert>
#include <chrono>
|

The

header contains math related functions such as [algorithm](http://en.cppreference.com/w/cpp/header/algorithm)

and [std::min](http://en.cppreference.com/w/cpp/algorithm/min)

.[std::max](http://en.cppreference.com/w/cpp/algorithm/max)

The

header contains the [cassert](http://en.cppreference.com/w/cpp/header/cassert)

macro.[assert](http://en.cppreference.com/w/cpp/error/assert)

The

header contains time related functions. The [chrono](http://en.cppreference.com/w/cpp/header/chrono)

is used to perfom timing in between calls to the [chrono::high_resolution_clock](http://en.cppreference.com/w/cpp/chrono/high_resolution_clock)`Update`

function.

The only header file that is local to the project is the `Helpers.h`

header file.

|
1
2
|
// Helper functions
#include <Helpers.h>
|

The `Helpers.h`

header file contains functions and classes that provide helper functionality that may be useful in several source files. Currently, the contents of the `Helpers.h`

header file is very simple.

|
1
2
3
4
5
6
7
8
9
10
11
12
13
14
|
#pragma once
#define WIN32_LEAN_AND_MEAN
#include <Windows.h> // For HRESULT
// From DXSampleHelper.h
// Source: https://github.com/Microsoft/DirectX-Graphics-Samples
inline void ThrowIfFailed(HRESULT hr)
{
if (FAILED(hr))
{
throw std::exception();
}
}
|

The `Helpers.h`

header file defines a single function that can be used to check the return value of a DirectX API function. If the function returns an fail code, an exception is thrown. This is useful for debugging the application and simplifies error checking in the main application code.

In the next section, the variables used by the application are defined. Tweak variables and variables that control the application initialization are defined first.

|
1
2
3
4
5
6
7
8
9
10
|
// The number of swap chain back buffers.
const uint8_t g_NumFrames = 3;
// Use WARP adapter
bool g_UseWarp = false;
uint32_t g_ClientWidth = 1280;
uint32_t g_ClientHeight = 720;
// Set to true once the DX12 objects have been initialized.
bool g_IsInitialized = false;
|

The `g_NumFrames`

constant variable defined on line 44 controls the number of back buffer surfaces for the swap chain. This value must not be less than 2 when using the flip presentation model. Details about the swap chain and flip models are discussed in more detail later.

The `g_UseWarp`

variable controls whether to use a software rasterizer ([Windows Advanced Rasterization Platform](https://msdn.microsoft.com/en-us/library/windows/desktop/gg615082(v=vs.85).aspx) – **WARP**) or not. The software rasterizer allows the graphics programmer to access the full set of advanced rendering features that may not be available in the hardware (for example, when running on older GPUs). The **WARP** device can also be used to verify the results of a rendering technique if the quality of the vendor supplied display driver is in question.

The `g_ClientWidth`

and `g_ClientHeight`

variables control the size of the client area when the window is first created.

The `g_IsInitialized`

boolean variable is set to true only after all of the DirectX 12 objects have been created. This variable is used to prevent certain window messages (such as the window resize message) from being handled until after the device and swap chain have been fully created.

In the next section, the Windows and DirectX specific variables are defined.

|
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
|
// Window handle.
HWND g_hWnd;
// Window rectangle (used to toggle fullscreen state).
RECT g_WindowRect;
// DirectX 12 Objects
ComPtr<ID3D12Device2> g_Device;
ComPtr<ID3D12CommandQueue> g_CommandQueue;
ComPtr<IDXGISwapChain4> g_SwapChain;
ComPtr<ID3D12Resource> g_BackBuffers[g_NumFrames];
ComPtr<ID3D12GraphicsCommandList> g_CommandList;
ComPtr<ID3D12CommandAllocator> g_CommandAllocators[g_NumFrames];
ComPtr<ID3D12DescriptorHeap> g_RTVDescriptorHeap;
UINT g_RTVDescriptorSize;
UINT g_CurrentBackBufferIndex;
|

The `g_hWnd`

variable stores a handle to the OS window that will be used to display the rendered image.

When switching to a full-screen window state, the previous size of the window needs to be stored so that when switching back to windowed mode, the window dimensions can be restored correctly. The `g_WindowRect`

variable is used to store the previous window dimensions before going to fullscreen mode.

The DirectX 12 device object is stored in the `g_Device`

variable. The command queue is stored in the `g_CommandQueue`

variable.

The

interface defines the swap chain. The swap chain is responsible for presenting the rendered image to the window. The swap chain will be discussed in more detail later in the tutorial.[IDXGISwapChain4](https://msdn.microsoft.com/en-us/library/windows/desktop/mt732707(v=vs.85).aspx)

The swap chain will be created with a number of back buffer resources. In order to correctly transition the back buffer resources to the correct state, pointers to the back buffer resources will be tracked in the `g_BackBuffers`

array variable. Although the back buffers of the swap chain are actually textures, all buffer and texture resources are referenced using the

interface in DirectX 12.[ID3D12Resource](https://msdn.microsoft.com/en-us/library/windows/desktop/dn788709(v=vs.85).aspx)

GPU commands are first recorded into a

. Generally a single command list is needed to record GPU commands using a single thread. Since this demo uses the main thread to record all GPU commands, only a single command list is defined. The [ID3D12GraphicsCommandList](https://msdn.microsoft.com/en-us/library/windows/desktop/dn903537(v=vs.85).aspx)`g_CommandList`

variable is used to store the pointer to the

.[ID3D12GraphicsCommandList](https://msdn.microsoft.com/en-us/library/windows/desktop/dn903537(v=vs.85).aspx)

The

serves as the backing memory for recording the GPU commands into a command list. Unlike the command list, a command allocator cannot be reused unless all of the commands that have been recorded into the command allocator have finished executing on the GPU. Attempting to reset a command allocator before the command queue has finished executing those commands will result in a [ID3D12CommandAllocator](https://msdn.microsoft.com/en-us/library/windows/desktop/dn770463(v=vs.85).aspx)`COMMAND_ALLOCATOR_SYNC`

error by the debug layer. The `g_CommandAllocators`

array variable is used to store the reference to the command allocators. There must be at least one command allocator per render frame that is “in-flight” (at least one per back buffer of the swap chain).

The back buffer textures of the swap chain are described using a **render target view** (**RTV**). The render target view describes the location of the texture resource in GPU memory, the dimensions (width and height) of the texture, as well as the format of the texture. The RTV is used to clear the back buffers of the render target. In a later tutorial, the RTV will be used to render geometry to the screen.

In previous versions of DirectX, RTVs were created one at a time. Since DirectX 12, RTVs are now stored in **descriptor heaps**. A descriptor heap can be visualized as an array of descriptors (views). A **view** simply describes a resource that resides in GPU memory.

A view in DirectX 12 is also called a descriptor. Similar to a view, a descriptor describes a resource. Since the swap chain contains multiple back buffer textures, one descriptor is needed to describe each back buffer texture. The `g_RTVDescriptorHeap`

variable is used to store the descriptor heap that contains the render target views for the swap chain back buffers.

The size of a descriptor in a descriptor heap is vendor specific (Intel, NVidia, and AMD may store descriptors differently). In order to correctly offset the index into the descriptor heap, the size of a single element in the descriptor heap needs to be queried during initialization. The size of a single RTV descriptor is stored in the `g_RTVDescriptorSize`

variable defined on line 66.

Depending on the flip model of the swap chain, the index of the current back buffer in the swap chain may not be sequential. The `g_CurrentBackBufferIndex`

variable is used to store the index of the current back buffer of the swap chain.

A few variables that are used to perform correct GPU synchronization are defined.

|
1
2
3
4
5
|
// Synchronization objects
ComPtr<ID3D12Fence> g_Fence;
uint64_t g_FenceValue = 0;
uint64_t g_FrameFenceValues[g_NumFrames] = {};
HANDLE g_FenceEvent;
|

The `g_Fence`

variable is used to store the fence object described in section [Fence](https://www.3dgep.com#Fence) above.

The next fence value to signal the command queue next is stored in the `g_FenceValue`

variable.

For each rendered frame that could be “in-flight” on the command queue, the fence value that was used to signal the command queue needs to be tracked to guarantee that any resources that are still being referenced by the command queue are not overwritten. The `g_FrameFenceValues`

array variable is used to keep track of the fence values that were used to signal the command queue for a particular frame.

If the fence object’s completed value has not reached the fence value specified for the frame, then the CPU thread will stall until the fence value is reached. The `g_FenceEvent`

variable is a handle to an OS event object that will be used to receive the notification that the fence has reached a specific value.

A few variables are defined to control the swap chain’s present method.

|
1
2
3
4
5
6
7
|
// By default, enable V-Sync.
// Can be toggled with the V key.
bool g_VSync = true;
bool g_TearingSupported = false;
// By default, use windowed mode.
// Can be toggled with the Alt+Enter or F11
bool g_Fullscreen = false;
|

The `g_VSync`

variable controls whether the swap chain’s present method should wait for the next vertical refresh before presenting the rendered image to the screen. By default, the swap chain’s present method will block until the next vertical refresh of the screen. This will cap the framerate of the application to the refresh rate of the screen. Setting `g_VSync`

variable to `false`

will cause the swap chain to present the rendered image to the screen as fast as possible which will allow the application to render at an unthrottled frame rate but may cause visual artifacts in the form of [screen tearing](https://en.wikipedia.org/wiki/Screen_tearing).

Variable refresh rate displays ([NVidia’s G-Sync](https://developer.nvidia.com/g-sync) and [AMD’s FreeSync](http://www.amd.com/en/technologies/free-sync)) eliminate screen tearing by allowing the graphics application to determine when the vertical refresh should occur.

The `g_Fullscreen`

variable tracks the fullscreen state of the render window.

The source code for the demo has been organized to minimize the number of functions that need to be forward declared. The windows message call back procedure is an exception and requires a forward declaration so that the callback function can be used to register the window class.

|
1
2
|
// Window callback function.
LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);
|

In the next section, the various functions used by the demo application are defined.

The `ParseCommandLineArguments`

function allows a few of the globally defined variables to be overridden by supplying command-line arguments when the application is executed.

|
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
|
void ParseCommandLineArguments()
{
int argc;
wchar_t** argv = ::CommandLineToArgvW(::GetCommandLineW(), &argc);
for (size_t i = 0; i < argc; ++i)
{
if (::wcscmp(argv[i], L"-w") == 0 || ::wcscmp(argv[i], L"--width") == 0)
{
g_ClientWidth = ::wcstol(argv[++i], nullptr, 10);
}
if (::wcscmp(argv[i], L"-h") == 0 || ::wcscmp(argv[i], L"--height") == 0)
{
g_ClientHeight = ::wcstol(argv[++i], nullptr, 10);
}
if (::wcscmp(argv[i], L"-warp") == 0 || ::wcscmp(argv[i], L"--warp") == 0)
{
g_UseWarp = true;
}
}
// Free memory allocated by CommandLineToArgvW
::LocalFree(argv);
}
|

`::`

operator. This notation is used to identify system functions that are defined in global scope. Functions that are defined in the scope of the source file do not use this notation. Using this notation it is easy to differentiate between locally defined functions and system functions. The table below describes the command-line arguments supported by the application.

| Argument | Description |
|---|---|
`-w` , `--width`
|
Specify the width (in pixels) of the render window. |
`-h` , `--height`
|
Specify the height (in pixels) of the render window. |
`-warp` , `--warp`
|
Use the Windows Advanced Rasterization Platform (WARP) for device creation. |

Additional command-line arguments (for example, to specify the application start in fullscreen mode) can be handled by extending this function.

Before doing anything using either the DXGI or the Direct3D API, the debug layer should be enabled in debug builds.

[ID3D12Device](https://msdn.microsoft.com/en-us/library/windows/desktop/dn788650(v=vs.85).aspx)

will cause the runtime to remove the device. |
1
2
3
4
5
6
7
8
9
10
11
|
void EnableDebugLayer()
{
#if defined(_DEBUG)
// Always enable the debug layer before doing anything DX12 related
// so all possible errors generated while creating DX12 objects
// are caught by the debug layer.
ComPtr<ID3D12Debug> debugInterface;
ThrowIfFailed(D3D12GetDebugInterface(IID_PPV_ARGS(&debugInterface)));
debugInterface->EnableDebugLayer();
#endif
}
|

[IID_PPV_ARGS](https://msdn.microsoft.com/en-us/library/ee330727(v=vs.85).aspx)

macro shown here on line 118 is used to retrieve an interface pointer, supplying the IID value of the requested interface automatically based on the type of the interface pointer used.A common syntax in methods that retrieve an interface pointer includes two parameters:

- An [in] parameter, normally of type
`REFIID`

, to specify the IID of the interface to retrieve. - An [out] parameter, normally of type
`void**`

, to receive the interface pointer.

This macro computes the IID based on the type of interface pointer, which prevents coding errors in which the IID and interface pointer type do not match. Windows developers should always use this macro with any method that requires separate IID and interface pointer parameters.


Enabling the debug layer will help in identifying incorrect usage of the DirectX 12 API. The graphics programmer should strive to eliminate any and all errors and warnings that are reported by the debug layer.

Before creating an instance of an OS window, the window class corresponding to that window must be registered. The window class will be automatically unregistered when the application terminates.

|
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
|
void RegisterWindowClass( HINSTANCE hInst, const wchar_t* windowClassName )
{
// Register a window class for creating our render window with.
WNDCLASSEXW windowClass = {};
windowClass.cbSize = sizeof(WNDCLASSEX);
windowClass.style = CS_HREDRAW | CS_VREDRAW;
windowClass.lpfnWndProc = &WndProc;
windowClass.cbClsExtra = 0;
windowClass.cbWndExtra = 0;
windowClass.hInstance = hInst;
windowClass.hIcon = ::LoadIcon(hInst, NULL);
windowClass.hCursor = ::LoadCursor(NULL, IDC_ARROW);
windowClass.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
windowClass.lpszMenuName = NULL;
windowClass.lpszClassName = windowClassName;
windowClass.hIconSm = ::LoadIcon(hInst, NULL);
static ATOM atom = ::RegisterClassExW(&windowClass);
assert(atom > 0);
}
|

The

function takes a pointer to a [RegisterClassEx](https://msdn.microsoft.com/en-us/library/ms633587(v=vs.85).aspx)

structure as its only argument.[WNDCLASSEX](https://msdn.microsoft.com/en-us/library/ms633577(v=vs.85).aspx)

The

structure has the following definition [WNDCLASSEX](https://msdn.microsoft.com/en-us/library/ms633577(v=vs.85).aspx)[[17]](https://www.3dgep.com#cite-17):

|
1
2
3
4
5
6
7
8
9
10
11
12
13
14
|
typedef struct tagWNDCLASSEXW {
UINT cbSize;
UINT style;
WNDPROC lpfnWndProc;
int cbClsExtra;
int cbWndExtra;
HINSTANCE hInstance;
HICON hIcon;
HCURSOR hCursor;
HBRUSH hbrBackground;
LPCWSTR lpszMenuName;
LPCWSTR lpszClassName;
HICON hIconSm;
} WNDCLASSEXW, *PWNDCLASSEXW;
|

Each member has the following definition:

-
`UINT cbSize`

: The size, in bytes, of this structure. Set this member to`sizeof(WNDCLASSEXW)`

. -
`UINT style`

: The class styles. In this case, the

class style specifies that the entire window is redrawn if a movement or size adjustment changes the width of the client area and the[CS_HREDRAW](https://msdn.microsoft.com/en-us/library/ff729176(v=vs.85).aspx)

class style specifies that the entire window is redrawn if a movement or size adjustment changes the height of the client area.[CS_VREDRAW](https://msdn.microsoft.com/en-us/library/ff729176(v=vs.85).aspx) -
`WNDPROC lpfnWndProc`

: A pointer to the windows procedure that will handle window messages for any window created using this window class. In this case we specify the yet undefined`WndProc`

function that was declared earlier. -
`int cbClsExtra`

: The number of extra bytes to allocate following the window-class structure. This parameter is not used here and should be set to 0. -
`int cpWndExtra`

: The number of extra bytes to allocate following the window instance. This parameter is not used here and should be set to 0. -
`HINSTANCE hInstance`

: A handle to the instance that contains the window procedure for the class. This module instance handle is passed to the`WinMain`

function which will be shown later. -
`HICON hIcon`

: A handle to the class icon. This icon will be used to represent a window created with this class in the taskbar and in the top-left corner of the window’s title bar. You can load an icon from a resource file using the

function. If this value is[LoadIcon](https://msdn.microsoft.com/en-us/library/windows/desktop/ms648072(v=vs.85).aspx)`NULL`

(or`nullptr`

) then the default application icon is used. -
`HCURSOR hCursor`

: A handle to the class cursor. This must be a handle to a valid cursor resource. For this demo, we will use the default arrow icon by specifying`LoadCursor( nullptr, IDC_ARROW )`

. -
`HBRUSH hbrBackground`

: A handle to the class background brush. This member can be a handle to the brush to be used for painting the background, or it can be a color value. A color value must be one of the following standard system colors (the value 1 must be added to the chosen color). If a color value is given, you must convert it to one of the following`HBRUSH`

types:`COLOR_ACTIVEBORDER`

`COLOR_ACTIVECAPTION`

`COLOR_APPWORKSPACE`

`COLOR_BACKGROUND`

`COLOR_BTNFACE`

`COLOR_BTNSHADOW`

`COLOR_BTNTEXT`

`COLOR_CAPTIONTEXT`

`COLOR_GRAYTEXT`

`COLOR_HIGHLIGHT`

`COLOR_HIGHLIGHTTEXT`

`COLOR_INACTIVEBORDER`

`COLOR_INACTIVECAPTION`

`COLOR_MENU`

`COLOR_MENUTEXT`

`COLOR_SCROLLBAR`

`COLOR_WINDOW`

`COLOR_WINDOWFRAME`

`COLOR_WINDOWTEXT`


-
`LPCWSTR lpszMenuName`

: Pointer to a null-terminated character string that specifies the resource name of the class menu, as the name appears in the resource file. If this member is`NULL`

, windows belonging to this class have no default menu. -
`LPCWSTR lpszClassName`

: A pointer to a null-terminated const string which is used to uniquely identify this window class. This class name will be used to create the window instance. -
`HICON hIconSm`

: A handle to a small icon that is associated with the window class. If this member is`NULL`

(or`nullptr`

), the system searches the icon resource specified by the`hIcon`

member for an icon of the appropriate size to use as the small icon.

With the window class registered, the OS window instance can be created.

The `CreateWindow`

function is used to create an instance of an OS window.

The window will be created in the center of the primary display device. Care must be taken to prevent the window from being created off-screen. Creating a window larger than the viewable area of the display will cause parts of the window to be offscreen. If the title bar and the window frame are offscreen, then it will not be possible to resize the window to fit in the screen.

|
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
|
HWND CreateWindow(const wchar_t* windowClassName, HINSTANCE hInst,
const wchar_t* windowTitle, uint32_t width, uint32_t height)
{
int screenWidth = ::GetSystemMetrics(SM_CXSCREEN);
int screenHeight = ::GetSystemMetrics(SM_CYSCREEN);
RECT windowRect = { 0, 0, static_cast<LONG>(width), static_cast<LONG>(height) };
::AdjustWindowRect(&windowRect, WS_OVERLAPPEDWINDOW, FALSE);
int windowWidth = windowRect.right - windowRect.left;
int windowHeight = windowRect.bottom - windowRect.top;
// Center the window within the screen. Clamp to 0, 0 for the top-left corner.
int windowX = std::max<int>(0, (screenWidth - windowWidth) / 2);
int windowY = std::max<int>(0, (screenHeight - windowHeight) / 2);
|

The

function retrieves specific system metric information. In this case, the [GetSystemMetrics](https://msdn.microsoft.com/en-us/library/ms724385(v=vs.85).aspx)

and [SM_CXSCREEN](https://msdn.microsoft.com/en-us/library/ms724385(v=vs.85).aspx#SM_CXSCREEN)

system metric are used to retrieve the width and height in pixels of the primary display monitor.[SM_CYSCREEN](https://msdn.microsoft.com/en-us/library/ms724385(v=vs.85).aspx#SM_CYSCREEN)

In order to calculate the required size of the window rectangle, based on the desired client-rectangle size, the

function is used. The [AdjustWindowRect](https://msdn.microsoft.com/en-us/library/ms632665(v=vs.85).aspx)

window style describes a window that can be minimized, and maximized, and has a thick window frame.[WS_OVERLAPPEDWINDOW](https://msdn.microsoft.com/en-us/library/ms632600(v=vs.85).aspx#WS_OVERLAPPEDWINDOW)

On lines 154-155, the dimensions of the adjusted window rectangle are used to compute the width and height of the window that is to be created.

The top-left corner point of the window is computed on lines 158-159 so that the window appears in the center of the screen. The window position should be clamped to \((0,0)\) to prevent the window from being positioned offscreen.

With the window dimensions known, the window instance can be created.

|
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
|
HWND hWnd = ::CreateWindowExW(
NULL,
windowClassName,
windowTitle,
WS_OVERLAPPEDWINDOW,
windowX,
windowY,
windowWidth,
windowHeight,
NULL,
NULL,
hInst,
nullptr
);
assert(hWnd && "Failed to create window");
return hWnd;
}
|

The

function has the following signature [CreateWindowExW](https://msdn.microsoft.com/en-us/library/ms632680(v=vs.85).aspx)[[18]](https://www.3dgep.com#cite-18):

|
1
2
3
4
5
6
7
8
9
10
11
12
13
14
|
HWND WINAPI CreateWindowExW(
_In_ DWORD dwExStyle,
_In_opt_ LPCWSTR lpClassName,
_In_opt_ LPCWSTR lpWindowName,
_In_ DWORD dwStyle,
_In_ int X,
_In_ int Y,
_In_ int nWidth,
_In_ int nHeight,
_In_opt_ HWND hWndParent,
_In_opt_ HMENU hMenu,
_In_opt_ HINSTANCE hInstance,
_In_opt_ LPVOID lpParam
);
|

And each parameter has the following definition:

-
`DWORD dwExStyle`

: The extended window style of the window being created. For a list of possible values,see[Extended Window Styles](https://msdn.microsoft.com/en-us/library/ff700543(v=vs.85).aspx). -
`LPCWSTR lpClassName`

: A null-terminated string or a class atom created by a previous call to the

or[RegisterClass](https://msdn.microsoft.com/en-us/library/ms633586(v=vs.85).aspx)

function. The atom must be in the low-order word of[RegisterClassEx](https://msdn.microsoft.com/en-us/library/ms633587(v=vs.85).aspx)`lpClassName`

; the high-order word must be 0. If`lpClassName`

is a string, it specifies the window class name. The class name can be any name registered with

or[RegisterClass](https://msdn.microsoft.com/en-us/library/ms633586(v=vs.85).aspx)

, provided that the module that registers the class is also the module that creates the window.[RegisterClassEx](https://msdn.microsoft.com/en-us/library/ms633587(v=vs.85).aspx) -
`LPCWSTR lpWindowName`

: The window name. If the window style specifies a title bar, the window title pointed to by`lpWindowName`

is displayed in the title bar. -
`DWORD dwStyle`

: The style of the window being created. This parameter can be a combination of the[window style values](https://msdn.microsoft.com/en-us/library/ms632600(v=vs.85).aspx). -
`int X`

: The initial horizontal position of the window. For an overlapped or pop-up window, the`X`

parameter is the initial x-coordinate of the window’s upper-left corner, in screen coordinates. If`X`

is set to`CW_USEDEFAULT`

, the system selects the default position for the window’s upper-left corner and ignores the`Y`

parameter. -
`int Y`

: The initial vertical position of the window. For an overlapped or pop-up window, the`Y`

parameter is the initial y-coordinate of the window’s upper-left corner, in screen coordinates. If an overlapped window is created with the`WS_VISIBLE`

style bit set and the`X`

parameter is set to`CW_USEDEFAULT`

, then the`Y`

parameter determines how the window is shown. If the`Y`

parameter is`CW_USEDEFAULT`

, then the window manager calls

with the[ShowWindow](https://msdn.microsoft.com/en-us/library/ms633548(v=vs.85).aspx)`SW_SHOW`

flag after the window has been created. If the`Y`

parameter is some other value, then the window manager calls

with that value as the[ShowWindow](https://msdn.microsoft.com/en-us/library/ms633548(v=vs.85).aspx)`nCmdShow`

parameter. -
`int nWidth`

: The width, in device units, of the window. For overlapped windows,`nWidth`

is the window’s width, in screen coordinates, or`CW_USEDEFAULT`

. If`nWidth`

is`CW_USEDEFAULT`

, the system selects a default width and height for the window; the default width extends from the initial x-coordinates to the right edge of the screen; the default height extends from the initial y-coordinate to the top of the icon area. -
`int nHeight`

: The height, in device units, of the window. For overlapped windows,`nHeight`

is the window’s height, in screen coordinates. If the`nWidth`

parameter is set to`CW_USEDEFAULT`

, the system ignores`nHeight`

. -
`HWND hWndParent`

: A handle to the parent or owner window of the window being created. To create a child window or an owned window, supply a valid window handle. This parameter is optional for pop-up windows. -
`HMENU hMenu`

: A handle to a menu, or specifies a child-window identifier, depending on the window style. For an overlapped or pop-up window,`hMenu`

identifies the menu to be used with the window; it can be`NULL`

if the class menu is to be used. -
`HINSTANCE hInstance`

: A handle to the instance of the module to be associated with the window. -
`LPVOID lpParam`

: Pointer to a value to be passed to the window through the

structure ([CREATESTRUCT](https://msdn.microsoft.com/en-us/library/ms632603(v=vs.85).aspx)`lpCreateParams`

member) pointed to by the`lParam`

param of the`WM_CREATE`

message. This message is sent to the created window by this function before it returns.

The window has been created but it has not yet been shown. The window is shown only after the DirectX 12 device and command queue have been created and initialized.

In the next section, the DXGI API is used to query for DirectX 12 capable GPU adapters.

Before creating the DirectX 12 device, a compatible adapter must be present on the user’s computer. The `GetAdapter`

function is used to query for a compatible adapter.

|
1
2
3
4
5
6
7
8
9
|
ComPtr<IDXGIAdapter4> GetAdapter(bool useWarp)
{
ComPtr<IDXGIFactory4> dxgiFactory;
UINT createFactoryFlags = 0;
#if defined(_DEBUG)
createFactoryFlags = DXGI_CREATE_FACTORY_DEBUG;
#endif
ThrowIfFailed(CreateDXGIFactory2(createFactoryFlags, IID_PPV_ARGS(&dxgiFactory)));
|

Before querying for available adapters, a DXGI factory must be created. On line 189, the DXGI factor is created. Enabling the `DXGI_CREATE_FACTORY_DEBUG`

flag during factory creation enables errors to be caught during device creation and while querying for the adapters. The `DXGI_CREATE_FACTORY_DEBUG`

flag should not be used in production builds.

|
1
2
3
4
5
6
7
8
|
ComPtr<IDXGIAdapter1> dxgiAdapter1;
ComPtr<IDXGIAdapter4> dxgiAdapter4;
if (useWarp)
{
ThrowIfFailed(dxgiFactory->EnumWarpAdapter(IID_PPV_ARGS(&dxgiAdapter1)));
ThrowIfFailed(dxgiAdapter1.As(&dxgiAdapter4));
}
|

In the case that a WARP device should be used, the

method can be used to directly create the WARP adapter.[IDXGIFactory4::EnumWarpAdapter](https://msdn.microsoft.com/en-us/library/mt427787(v=vs.85).aspx)

The

method takes a pointer to a [IDXGIFactory4::EnumWarpAdapter](https://msdn.microsoft.com/en-us/library/mt427787(v=vs.85).aspx)

interface but the [IDXGIAdapter1](https://msdn.microsoft.com/en-us/library/ff471329(v=vs.85).aspx)`GetAdapter`

function returns a pointer to a

interface. In order to cast a COM object to the correct type, the [IDXGIAdapter4](https://msdn.microsoft.com/en-us/library/mt825229(v=vs.85).aspx)

method should be used (as shown on line 198). When not using [ComPtr::As](https://docs.microsoft.com/en-us/cpp/windows/comptr-as-method)

, the [ComPtr](https://docs.microsoft.com/en-us/cpp/windows/comptr-class)

method should be used to query for the correct COM object type. For more information, see the reference documentation for [QueryInterface](https://msdn.microsoft.com/library/windows/desktop/ms682521)

.[QueryInterface](https://docs.microsoft.com/en-us/cpp/atl/queryinterface)

|
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
|
else
{
SIZE_T maxDedicatedVideoMemory = 0;
for (UINT i = 0; dxgiFactory->EnumAdapters1(i, &dxgiAdapter1) != DXGI_ERROR_NOT_FOUND; ++i)
{
DXGI_ADAPTER_DESC1 dxgiAdapterDesc1;
dxgiAdapter1->GetDesc1(&dxgiAdapterDesc1);
// Check to see if the adapter can create a D3D12 device without actually
// creating it. The adapter with the largest dedicated video memory
// is favored.
if ((dxgiAdapterDesc1.Flags & DXGI_ADAPTER_FLAG_SOFTWARE) == 0 &&
SUCCEEDED(D3D12CreateDevice(dxgiAdapter1.Get(),
D3D_FEATURE_LEVEL_11_0, __uuidof(ID3D12Device), nullptr)) &&
dxgiAdapterDesc1.DedicatedVideoMemory > maxDedicatedVideoMemory )
{
maxDedicatedVideoMemory = dxgiAdapterDesc1.DedicatedVideoMemory;
ThrowIfFailed(dxgiAdapter1.As(&dxgiAdapter4));
}
}
}
return dxgiAdapter4;
}
|

When not using a WARP adapter, the DXGI Factory is used to query for hardware adapters. The

method is used to enumerate the available GPU adapters in the system. This method returns [IDXGIFactory1::EnumAdapters1](https://msdn.microsoft.com/en-us/library/ff471336(v=vs.85).aspx)

if the adapter index is greater than or equal to the number of available adapters.[DXGI_ERROR_NOT_FOUND](https://msdn.microsoft.com/en-us/library/bb509553(v=vs.85).aspx#DXGI_ERROR_NOT_FOUND)

Since only hardware adapters should be considered, WARP adapters that have the

flag set, should be ignored.[DXGI_ADAPTER_FLAG_SOFTWARE](https://msdn.microsoft.com/en-us/library/ff471327(v=vs.85).aspx)

To verify that the adapter returned from the

method is a compatible DirectX 12 adapter, a (null) device is created using the [IDXGIFactory1::EnumAdapters1](https://msdn.microsoft.com/en-us/library/ff471336(v=vs.85).aspx)

function is used. If this function returns [D3D12CreateDevice](https://msdn.microsoft.com/en-us/library/dn770336(v=vs.85).aspx)

, then the function succeeded and it is a DirectX 12 compatible adapter.[S_OK](https://msdn.microsoft.com/en-us/library/dn706075(v=vs.85).aspx)

Generally speaking, the GPU with the largest amount of dedicated video memory (that is not shared with the CPU) is a good indicator of GPU performance. If there are more DirectX 12 compatible GPU adapters (for example, the integrated Intel GPU) in the system, then the one with the largest amount of dedicated video memory is favored.

On line 216, the GPU adapter is cast to a

interface and retured to the caller.[IDXGIAdapter4](https://msdn.microsoft.com/en-us/library/mt825229(v=vs.85).aspx)

If a valid GPU adapter is found, the actual DirectX 12 device is created.

After querying for a valid DirectX 12 compatible adapter, the DirectX 12 device is created.

The DirectX 12 device is used to create resources (such as textures and buffers, command lists, command queues, fences, heaps, etc…). The DirectX 12 device is not directly used for issuing draw or dispatch commands. The DirectX 12 device can be considered a memory context that tracks allocations in GPU memory. Destroying the DirectX 12 device will cause all of the resources allocated by the device to become invalid. If the device is destroyed before all of the resources that were created by the device, then the debug layer will issue warnings about those objects that are still being referenced.

|
1
2
3
4
|
ComPtr<ID3D12Device2> CreateDevice(ComPtr<IDXGIAdapter4> adapter)
{
ComPtr<ID3D12Device2> d3d12Device2;
ThrowIfFailed(D3D12CreateDevice(adapter.Get(), D3D_FEATURE_LEVEL_11_0, IID_PPV_ARGS(&d3d12Device2)));
|

You have already seen the

function being used in the [D3D12CreateDevice](https://msdn.microsoft.com/en-us/library/dn770336(v=vs.85).aspx)`GetAdapter`

funciton described ealier. In this case, the actual device is created and stored in the `d3d12Device2`

argument.

The

function has the following signature:[D3D12CreateDevice](https://msdn.microsoft.com/en-us/library/dn770336(v=vs.85).aspx)

|
1
2
3
4
5
6
|
HRESULT WINAPI D3D12CreateDevice(
_In_opt_ IUnknown *pAdapter,
D3D_FEATURE_LEVEL MinimumFeatureLevel,
_In_ REFIID riid,
_Out_opt_ void **ppDevice
);
|

And takes the following parameters:

-
`IUnknown *pAdapter`

: A pointer to the video adapter to use when creating a device. Pass`NULL`

(or`nullptr`

) to use the default adapter, which is the first adapter that is enumerated by

.[IDXGIFactory1::EnumAdapters](https://msdn.microsoft.com/en-us/library/bb174538(v=vs.85).aspx) -

: The minimum[D3D_FEATURE_LEVEL](https://msdn.microsoft.com/en-us/library/ff476329(v=vs.85).aspx)MinimumFeatureLevel

required for successful device creation.[D3D_FEATURE_LEVEL](https://msdn.microsoft.com/en-us/library/ff476329(v=vs.85).aspx) -
`REFIID riid`

: The globally unique identifier (`GUID`

) for the device interface. This parameter, and`ppDevice`

, can be addressed with the single macro

.[IID_PPV_ARGS](https://msdn.microsoft.com/en-us/library/ee330727(v=vs.85).aspx) -
`void **ppDevice`

: A pointer to a memory block that receives a pointer to the device.

As was mentioned previously, the graphics programmer should try to fix any and all errors and warnings generated by the debug layer before releasing the DirectX 12 application to the general public. In order to facilitate diagnosing errors and warnings generated by the debug layer, the DirectX 12 device provides access to the

interface. The [ID3D12InfoQueue](https://msdn.microsoft.com/en-us/library/dn950163(v=vs.85).aspx)

interface is used to enable break points based on the severity of the message and the ability to filter certain messages from being generated.[ID3D12InfoQueue](https://msdn.microsoft.com/en-us/library/dn950163(v=vs.85).aspx)

|
1
2
3
4
5
6
7
8
|
// Enable debug messages in debug mode.
#if defined(_DEBUG)
ComPtr<ID3D12InfoQueue> pInfoQueue;
if (SUCCEEDED(d3d12Device2.As(&pInfoQueue)))
{
pInfoQueue->SetBreakOnSeverity(D3D12_MESSAGE_SEVERITY_CORRUPTION, TRUE);
pInfoQueue->SetBreakOnSeverity(D3D12_MESSAGE_SEVERITY_ERROR, TRUE);
pInfoQueue->SetBreakOnSeverity(D3D12_MESSAGE_SEVERITY_WARNING, TRUE);
|

The

interface is queried from the [ID3D12InfoQueue](https://msdn.microsoft.com/en-us/library/dn950163(v=vs.85).aspx)

interface using the [ID3D12Device](https://msdn.microsoft.com/en-us/library/dn788650(v=vs.85).aspx)

method described earlier.[ComPtr::As](https://docs.microsoft.com/en-us/cpp/windows/comptr-as-method)

The

method sets a message severity level to break on (while the application is attached to a debugger) when a message with that severity level passes through the storage filter. The [ID3D12InfoQueue::SetBreakOnSeverity](https://msdn.microsoft.com/en-us/library/dn950197(v=vs.85).aspx)

and the [D3D12_MESSAGE_SEVERITY_ERROR](https://msdn.microsoft.com/en-us/library/dn950147(v=vs.85).aspx#D3D12_MESSAGE_SEVERITY_ERROR)

messages are generated if an error or warning is generated by the debug layer. The [D3D12_MESSAGE_SEVERITY_WARNING](https://msdn.microsoft.com/en-us/library/dn950147(v=vs.85).aspx#D3D12_MESSAGE_SEVERITY_WARNING)

message is generated if a memory corruption occurs.[D3D12_MESSAGE_SEVERITY_CORRUPTION](https://msdn.microsoft.com/en-us/library/dn950147(v=vs.85).aspx#D3D12_MESSAGE_SEVERITY_CORRUPTION)

While all DirectX 12 warnings and errors should be resolved before distributing the application, it may not be practical (or feasible) to address all of the possible warnings that can occur. In such a case, some warning messages can be ignored. A storage queue filter can be specified to ignore certain warning messages that are generated by the debug layer. Messages can be ignored by category, severity, or specific message IDs can be ignored.

|
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
|
// Suppress whole categories of messages
//D3D12_MESSAGE_CATEGORY Categories[] = {};
// Suppress messages based on their severity level
D3D12_MESSAGE_SEVERITY Severities[] =
{
D3D12_MESSAGE_SEVERITY_INFO
};
// Suppress individual messages by their ID
D3D12_MESSAGE_ID DenyIds[] = {
D3D12_MESSAGE_ID_CLEARRENDERTARGETVIEW_MISMATCHINGCLEARVALUE, // I'm really not sure how to avoid this message.
D3D12_MESSAGE_ID_MAP_INVALID_NULLRANGE, // This warning occurs when using capture frame while graphics debugging.
D3D12_MESSAGE_ID_UNMAP_INVALID_NULLRANGE, // This warning occurs when using capture frame while graphics debugging.
};
D3D12_INFO_QUEUE_FILTER NewFilter = {};
//NewFilter.DenyList.NumCategories = _countof(Categories);
//NewFilter.DenyList.pCategoryList = Categories;
NewFilter.DenyList.NumSeverities = _countof(Severities);
NewFilter.DenyList.pSeverityList = Severities;
NewFilter.DenyList.NumIDs = _countof(DenyIds);
NewFilter.DenyList.pIDList = DenyIds;
ThrowIfFailed(pInfoQueue->PushStorageFilter(&NewFilter));
}
#endif
return d3d12Device2;
}
|

No messages are ignored based on their category but the code is left in on line 239 for demonstration purposes.

Since

message severity is for information only, info messages are supressed. [D3D12_MESSAGE_SEVERITY_INFO](https://msdn.microsoft.com/en-us/library/dn950147(v=vs.85).aspx#D3D12_MESSAGE_SEVERITY_INFO)

The following warning messages are suppressed based on their [message ID](https://msdn.microsoft.com/en-us/library/dn950146(v=vs.85).aspx):

-
`CLEARRENDERTARGETVIEW_MISMATCHINGCLEARVALUE`

: This warning occurs when a render target is cleared using a clear color that is not the optimized clear color specified during resource creation. If you want to clear a render target using an arbitrary clear color, you should disable this warning. -
`MAP_INVALID_NULLRANGE`

and`UNMAP_INVALID_NULLRANGE`

: These warnings occur when a frame is captured using the graphics debugger integrated in Visual Studio. Since I think this bug will never be fixed in the debugger, it’s best to just ignore this warning.

On lines 254-260 the info queue filter is defined and the filter is pushed on the info queue using the

method.[ID3D12InfoQueue::PushStorageFilter](https://msdn.microsoft.com/en-us/library/dn950193(v=vs.85).aspx)

On line 266, the DirectX 12 device is returned to the calling function.

Before creating the swap chain, the command queue must be created first.

The `CreateCommandQueue`

function is used to create the command queue for the application.

|
1
2
3
4
5
6
7
8
9
10
11
12
13
14
|
ComPtr<ID3D12CommandQueue> CreateCommandQueue(ComPtr<ID3D12Device2> device, D3D12_COMMAND_LIST_TYPE type )
{
ComPtr<ID3D12CommandQueue> d3d12CommandQueue;
D3D12_COMMAND_QUEUE_DESC desc = {};
desc.Type = type;
desc.Priority = D3D12_COMMAND_QUEUE_PRIORITY_NORMAL;
desc.Flags = D3D12_COMMAND_QUEUE_FLAG_NONE;
desc.NodeMask = 0;
ThrowIfFailed(device->CreateCommandQueue(&desc, IID_PPV_ARGS(&d3d12CommandQueue)));
return d3d12CommandQueue;
}
|

The command queue is created using the

method. This method takes a [ID3D12Device::CreateCommandQueue](https://msdn.microsoft.com/en-us/library/dn788657(v=vs.85).aspx)

structure as the first argument. The [D3D12_COMMAND_QUEUE_DESC](https://msdn.microsoft.com/en-us/library/dn903796(v=vs.85).aspx)

structure has the following definition:[D3D12_COMMAND_QUEUE_DESC](https://msdn.microsoft.com/en-us/library/dn903796(v=vs.85).aspx)

|
1
2
3
4
5
6
|
typedef struct D3D12_COMMAND_QUEUE_DESC {
D3D12_COMMAND_LIST_TYPE Type;
INT Priority;
D3D12_COMMAND_QUEUE_FLAGS Flags;
UINT NodeMask;
} D3D12_COMMAND_QUEUE_DESC;
|

The members of the

structure are:[D3D12_COMMAND_QUEUE_DESC](https://msdn.microsoft.com/en-us/library/dn903796(v=vs.85).aspx)

-

: Specifies the type of command queue to create and can be one of the following types:[D3D12_COMMAND_LIST_TYPE](https://msdn.microsoft.com/en-us/library/dn770348(v=vs.85).aspx)Type-

: The command queue can be used to execute draw, compute, and copy commands. This is the most general type of command queue and will be used in most cases.[D3D12_COMMAND_LIST_TYPE_DIRECT](https://msdn.microsoft.com/en-us/library/dn770348(v=vs.85).aspx#D3D12_COMMAND_LIST_TYPE_DIRECT) -

: The command queue can be used to execute compute and copy commands.[D3D12_COMMAND_LIST_TYPE_COMPUTE](https://msdn.microsoft.com/en-us/library/dn770348(v=vs.85).aspx#D3D12_COMMAND_LIST_TYPE_COMPUTE) -

: Command queue can be used to execute copy commands.[D3D12_COMMAND_LIST_TYPE_COPY](https://msdn.microsoft.com/en-us/library/dn770348(v=vs.85).aspx#D3D12_COMMAND_LIST_TYPE_COPY)

-
-
`INT Priority`

: The priority for the command queue. Can be one of the following values:-

: The command queue has normal priority.[D3D12_COMMAND_QUEUE_PRIORITY_NORMAL](https://msdn.microsoft.com/en-us/library/dn986723(v=vs.85).aspx#D3D12_COMMAND_QUEUE_PRIORITY_NORMAL) -

: The command queue has high priority.[D3D12_COMMAND_QUEUE_PRIORITY_HIGH](https://msdn.microsoft.com/en-us/library/dn986723(v=vs.85).aspx#D3D12_COMMAND_QUEUE_PRIORITY_HIGH) -

: The command queue has global realtime priority.[D3D12_COMMAND_QUEUE_PRIORITY_GLOBAL_REALTIME](https://msdn.microsoft.com/en-us/library/dn986723(v=vs.85).aspx#D3D12_COMMAND_QUEUE_PRIORITY_GLOBAL_REALTIME)

-
-

: Specifies additional flags from the[D3D12_COMMAND_QUEUE_FLAGS](https://msdn.microsoft.com/en-us/library/dn986722(v=vs.85).aspx)Flags

enumeratrion. Currently, the only additional flag is[D3D12_COMMAND_QUEUE_FLAGS](https://msdn.microsoft.com/en-us/library/dn986722(v=vs.85).aspx)

which indicates that the GPU timeout should be disabled for this command queue. Be careful when using this flag. If you encounter errors with GPU timeouts, you should probably address the error instead of using this flag.[D3D12_COMMAND_QUEUE_FLAG_DISABLE_GPU_TIMEOUT](https://msdn.microsoft.com/en-us/library/dn986722(v=vs.85).aspx#D3D12_COMMAND_QUEUE_FLAG_DISABLE_GPU_TIMEOUT) -
`UINT NodeMask`

: For single GPU operation, set this to zero. If there are multiple GPU nodes, set a bit to identify the node (the device’s physical adapter) to which the command queue applies. Each bit in the mask corresponds to a single node. Only 1 bit must be set. For more information refer to[Multi-Adapter](https://msdn.microsoft.com/en-us/library/dn933253(v=vs.85).aspx).

Variable refresh rate displays ([NVidia’s G-Sync](https://developer.nvidia.com/g-sync) and [AMD’s FreeSync](http://www.amd.com/en/technologies/free-sync)) require tearing to be enabled in the DirectX 12 application to function correctly. This feature is also known as “**vsync-off**” [[19]](https://www.3dgep.com#cite-19).

Screen tearing occurs when a moving image is presented to the screen out-of-sync with the vertical refresh rate of the screen. An example of screen tearing can be seen in the image below.

![By Vanessaezekowitz (Own work) [CC BY-SA 3.0 (https://creativecommons.org/licenses/by-sa/3.0)], via Wikimedia Commons](https://upload.wikimedia.org/wikipedia/commons/0/03/Tearing_%28simulated%29.jpg)


![By Vanessaezekowitz (Own work) [CC BY-SA 3.0 (https://creativecommons.org/licenses/by-sa/3.0)], via Wikimedia Commons](https://upload.wikimedia.org/wikipedia/commons/0/03/Tearing_%28simulated%29.jpg)

By Vanessaezekowitz (Own work) [CC BY-SA 3.0 (https://creativecommons.org/licenses/by-sa/3.0)], via Wikimedia Commons

To create an application that supports variable refresh rate displays, the

feature must be supported and the [DXGI_FEATURE_PRESENT_ALLOW_TEARING](https://msdn.microsoft.com/en-us/library/mt722565(v=vs.85).aspx#DXGI_FEATURE_PRESENT_ALLOW_TEARING)

must be specified when creating the swap chain. Additionally, the [DXGI_SWAP_CHAIN_FLAG_ALLOW_TEARING](https://msdn.microsoft.com/en-us/library/bb173076(v=vs.85).aspx#DXGI_SWAP_CHAIN_FLAG_ALLOW_TEARING)

flag must be used when presenting the swap chain with a sync-interval of 0.[DXGI_PRESENT_ALLOW_TEARING](https://msdn.microsoft.com/en-us/library/bb509554(v=vs.85).aspx#DXGI_PRESENT_ALLOW_TEARING)

Support in in the [Windows Display Driver Model](https://en.wikipedia.org/wiki/Windows_Display_Driver_Model) (**WDDM**) for variable refresh rates was added in version [2.1](https://en.wikipedia.org/wiki/Windows_Display_Driver_Model#WDDM_2.1). WDDM 2.1 was added in the Windows 10 Anniversary Update (version 1607) which introduced the DXGI 1.5 API to the Windows 10 SDK. In order to make sure tearing is supported on the user’s computer, it must be queried using the

method.[IDXGIFactory5::CheckFeatureSupport](https://msdn.microsoft.com/en-us/library/mt722567(v=vs.85).aspx)

|
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
|
bool CheckTearingSupport()
{
BOOL allowTearing = FALSE;
// Rather than create the DXGI 1.5 factory interface directly, we create the
// DXGI 1.4 interface and query for the 1.5 interface. This is to enable the
// graphics debugging tools which will not support the 1.5 factory interface
// until a future update.
ComPtr<IDXGIFactory4> factory4;
if (SUCCEEDED(CreateDXGIFactory1(IID_PPV_ARGS(&factory4))))
{
ComPtr<IDXGIFactory5> factory5;
if (SUCCEEDED(factory4.As(&factory5)))
{
if (FAILED(factory5->CheckFeatureSupport(
DXGI_FEATURE_PRESENT_ALLOW_TEARING,
&allowTearing, sizeof(allowTearing))))
{
allowTearing = FALSE;
}
}
}
return allowTearing == TRUE;
}
|

The

method has the following signature:[IDXGIFactory5::CheckFeatureSupport](https://msdn.microsoft.com/en-us/library/mt722567(v=vs.85).aspx)

|
1
2
3
4
5
|
HRESULT CheckFeatureSupport(
DXGI_FEATURE Feature,
[in, out] void *pFeatureSupportData,
UINT FeatureSupportDataSize
);
|

And takes the following parameters:

-

: Specifies one member of[DXGI_FEATURE](https://msdn.microsoft.com/en-us/library/mt722565(v=vs.85).aspx)Feature

to query support for. Currently, the following features can be queried:[DXGI_FEATURE](https://msdn.microsoft.com/en-us/library/mt722565(v=vs.85).aspx)-

: The display supports tearing, a requirement of variable refresh rate displays.[DXGI_FEATURE_PRESENT_ALLOW_TEARING](https://msdn.microsoft.com/en-us/library/mt722565(v=vs.85).aspx#DXGI_FEATURE_PRESENT_ALLOW_TEARING)

-
-
`void *pFeatureSupportData`

: Specifies a pointer to a buffer that will be filled with data that describes the feature support. -
`UINT FeatureSupportDataSize`

: The size, in bytes, of`pFeatureSupportData`

.

The next step in initializing DirectX 12 is to create the swap chain.

The primary purpose of the swap chain is to present the rendered image to the screen. The swap chain stores no less than two buffers that are used to render the scene. The buffer that is currently being rendered to is called the **back buffer** and the buffer that is currently being presented is called the **front buffer**. The back buffer is swapped with the front buffer using the

method. In previous versions of DirectX, the DXGI presentation model used a bit-block transfer ([IDXGISwapChain::Present](https://msdn.microsoft.com/en-us/library/bb174576(v=vs.85).aspx)**bitblt**) model to present the rendered image to the display. When using a bitblt presentation model, the Direct3D runtime copied the contents of the front buffer to a **Desktop Window Manager** (**DWM**) redirection surface. Only after the contents of the front buffer were fully copied to the redirection surface was the image presented to the screen.

Windows 8 and DXGI 1.2 introduced the **flip** presentation model. Using the flip presentation model, the Direct3D runtime passes the front buffer surface directly to the DWM for presentation to the screen. The flip presentation model provides a performance improvement in both space and speed since the redirection surface is no longer required and the front buffer does not need to be copied before it is presented to the screen.

![Swap Chain](../../assets/a164227891ffc3c1.png)


![Swap Chain](../../assets/a164227891ffc3c1.png)

The swap chain stores pointers to a number of buffers in GPU memory. After a present, the pointers are updated to swap through the buffer chain.

The image above provides a visual example of the DXGI flip model [[20]](https://www.3dgep.com#cite-20). DirectX 12 does not support the bitblt presentation model and only supports the flip presentation model. There are two flip effects that can be used when creating the swap chain [[21]](https://www.3dgep.com#cite-21):

-

: Use this flag to specify the flip presentation model and to specify that DXGI persist the contents of the back buffer after you call[DXGI_SWAP_EFFECT_FLIP_SEQUENTIAL](https://msdn.microsoft.com/en-us/library/windows/desktop/bb173077(v=vs.85).aspx#DXGI_SWAP_EFFECT_FLIP_SEQUENTIAL)

. This flag cannot be used with multisampling.[IDXGISwapChain1::Present1](https://msdn.microsoft.com/en-us/library/windows/desktop/hh446797(v=vs.85).aspx) -

: Use this flag to specify the flip presentation model and to specify that DXGI discard the contents of the back buffer after you call[DXGI_SWAP_EFFECT_FLIP_DISCARD](https://msdn.microsoft.com/en-us/library/windows/desktop/bb173077(v=vs.85).aspx#DXGI_SWAP_EFFECT_FLIP_DISCARD)

. This flag cannot be used with multisampling and partial presentation.[IDXGISwapChain1::Present1](https://msdn.microsoft.com/en-us/library/windows/desktop/hh446797(v=vs.85).aspx)

To achieve maximum frame rates while rendering with **vsync-off** [[19]](https://www.3dgep.com#cite-19), the

flip model should be used. The [DXGI_SWAP_EFFECT_FLIP_DISCARD](https://msdn.microsoft.com/en-us/library/windows/desktop/bb173077(v=vs.85).aspx#DXGI_SWAP_EFFECT_FLIP_DISCARD)**discard** means that if the previously presented frame is still in the queue to be presented, then that frame will be discarded and the next frame will be put directly to the front of the presentation queue.

When using the

presentation model, the DXGI runtime will place the presented frame at the end of the presentation queue. Using this presentation model may cause presentation lag when there are no more buffers to utilize as the next back buffer (the [DXGI_SWAP_EFFECT_FLIP_SEQUENTIAL](https://msdn.microsoft.com/en-us/library/windows/desktop/bb173077(v=vs.85).aspx#DXGI_SWAP_EFFECT_FLIP_SEQUENTIAL)

method will likely block the calling thread until a buffer can be made available).[IDXGISwapChain1::Present1](https://msdn.microsoft.com/en-us/library/windows/desktop/hh446797(v=vs.85).aspx)

The `CreateSwapChain`

function is used to create the swap chain.

|
1
2
3
4
5
6
7
8
9
10
11
12
|
ComPtr<IDXGISwapChain4> CreateSwapChain(HWND hWnd,
ComPtr<ID3D12CommandQueue> commandQueue,
uint32_t width, uint32_t height, uint32_t bufferCount )
{
ComPtr<IDXGISwapChain4> dxgiSwapChain4;
ComPtr<IDXGIFactory4> dxgiFactory4;
UINT createFactoryFlags = 0;
#if defined(_DEBUG)
createFactoryFlags = DXGI_CREATE_FACTORY_DEBUG;
#endif
ThrowIfFailed(CreateDXGIFactory2(createFactoryFlags, IID_PPV_ARGS(&dxgiFactory4)));
|

In the first part of the `CreateSwapChain`

function, the DXGI factory is created. This code is similar to the the

function shown earlier and is not described in detail here.[GetAdapter](https://www.3dgep.com#Query_DirectX_12_Adapter)

The

structure is used to describe how the swap chain is created.[DXGI_SWAP_CHAIN_DESC1](https://msdn.microsoft.com/en-us/library/hh404528(v=vs.85).aspx)

|
1
2
3
4
5
6
7
8
9
10
11
12
13
|
DXGI_SWAP_CHAIN_DESC1 swapChainDesc = {};
swapChainDesc.Width = width;
swapChainDesc.Height = height;
swapChainDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;
swapChainDesc.Stereo = FALSE;
swapChainDesc.SampleDesc = { 1, 0 };
swapChainDesc.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;
swapChainDesc.BufferCount = bufferCount;
swapChainDesc.Scaling = DXGI_SCALING_STRETCH;
swapChainDesc.SwapEffect = DXGI_SWAP_EFFECT_FLIP_DISCARD;
swapChainDesc.AlphaMode = DXGI_ALPHA_MODE_UNSPECIFIED;
// It is recommended to always allow tearing if tearing support is available.
swapChainDesc.Flags = CheckTearingSupport() ? DXGI_SWAP_CHAIN_FLAG_ALLOW_TEARING : 0;
|

The

structure has the following definition [DXGI_SWAP_CHAIN_DESC1](https://msdn.microsoft.com/en-us/library/hh404528(v=vs.85).aspx)[[22]](https://www.3dgep.com#cite-22):

|
1
2
3
4
5
6
7
8
9
10
11
12
13
|
typedef struct _DXGI_SWAP_CHAIN_DESC1 {
UINT Width;
UINT Height;
DXGI_FORMAT Format;
BOOL Stereo;
DXGI_SAMPLE_DESC SampleDesc;
DXGI_USAGE BufferUsage;
UINT BufferCount;
DXGI_SCALING Scaling;
DXGI_SWAP_EFFECT SwapEffect;
DXGI_ALPHA_MODE AlphaMode;
UINT Flags;
} DXGI_SWAP_CHAIN_DESC1;
|

And each member has the following definition:

-
`UINT Width`

: A value that describes the resolution width. If you specify a width of 0 when you call the

method to create a swap chain, the runtime obtains the width from the output window and assigns this width value to the swap-chain description. You can subsequently call the[IDXGIFactory2::CreateSwapChainForHwnd](https://msdn.microsoft.com/en-us/library/hh404557(v=vs.85).aspx)

method to retrieve the assigned width value.[IDXGISwapChain1::GetDesc1](https://msdn.microsoft.com/en-us/library/hh404640(v=vs.85).aspx) -
`UINT Height`

: A value that describes the resolution height. If you specify the height as zero when you call the

method to create a swap chain, the runtime obtains the height from the output window and assigns this height value to the swap-chain description. You can subsequently call the[IDXGIFactory2::CreateSwapChainForHwnd](https://msdn.microsoft.com/en-us/library/hh404557(v=vs.85).aspx)

method to retrieve the assigned height value.[IDXGISwapChain1::GetDesc1](https://msdn.microsoft.com/en-us/library/hh404640(v=vs.85).aspx) -

: A[DXGI_FORMAT](https://msdn.microsoft.com/en-us/library/bb173059(v=vs.85).aspx)Format

structure that describes the display format.[DXGI_FORMAT](https://msdn.microsoft.com/en-us/library/bb173059(v=vs.85).aspx) -
`BOOL Stereo`

: Specifies whether the full-screen display mode or the swap-chain back buffer is stereo.`TRUE`

if stereo; otherwise,`FALSE`

. If you specify stereo, you must also specify a flip-model swap chain. -

: A[DXGI_SAMPLE_DESC](https://msdn.microsoft.com/en-us/library/bb173072(v=vs.85).aspx)SampleDesc

structure that describes multi-sampling parameters. This member is valid only with bit-block transfer ([DXGI_SAMPLE_DESC](https://msdn.microsoft.com/en-us/library/bb173072(v=vs.85).aspx)**bitblt**) model swap chains. When using**flip**model swap chain, this member must be specified as`{1, 0}`

. -

: A[DXGI_USAGE](https://msdn.microsoft.com/en-us/library/bb173078(v=vs.85).aspx)BufferUsage

-typed value that describes the surface usage and CPU access options for the back buffer. The back buffer can be used for shader input ([DXGI_USAGE](https://msdn.microsoft.com/en-us/library/bb173078(v=vs.85).aspx)

) or render-target output ([DXGI_USAGE_SHADER_INPUT](https://msdn.microsoft.com/en-us/library/bb173078(v=vs.85).aspx#DXGI_USAGE_SHADER_INPUT)

).[DXGI_USAGE_RENDER_TARGET_OUTPUT](https://msdn.microsoft.com/en-us/library/bb173078(v=vs.85).aspx#DXGI_USAGE_RENDER_TARGET_OUTPUT) -
`UINT BufferCount`

: A value that describes the number of buffers in the swap chain. When you create a full-screen swap chain, you typically include the front buffer in this value. The minimum number of buffers When using the flip presentation model is two. -

: A[DXGI_SCALING](https://msdn.microsoft.com/en-us/library/hh404526(v=vs.85).aspx)Scaling

-typed value that identifies resize behavior if the size of the back buffer is not equal to the target output. This member can be one of the following values:[DXGI_SCALING](https://msdn.microsoft.com/en-us/library/hh404526(v=vs.85).aspx)-

: Directs DXGI to make the back-buffer contents scale to fit the presentation target size. This is the implicit behavior of DXGI when you call the[DXGI_SCALING_STRETCH](https://msdn.microsoft.com/en-us/library/hh404526(v=vs.85).aspx#DXGI_SCALING_STRETCH)

method.[IDXGIFactory::CreateSwapChain](https://msdn.microsoft.com/en-us/library/bb174537(v=vs.85).aspx) -

: Directs DXGI to make the back-buffer contents appear without any scaling when the presentation target size is not equal to the back-buffer size. The top edges of the back buffer and presentation target are aligned together. If the[DXGI_SCALING_NONE](https://msdn.microsoft.com/en-us/library/hh404526(v=vs.85).aspx#DXGI_SCALING_NONE)`WS_EX_LAYOUTRTL`

style is associated with the

handle to the target output window, the right edges of the back buffer and presentation target are aligned together; otherwise, the left edges are aligned together. All target area outside the back buffer is filled with window background color.[HWND](https://msdn.microsoft.com/en-us/library/aa383751(v=vs.85).aspx)

This value specifies that all target areas outside the back buffer of a swap chain are filled with the background color that you specify in a call to

.[IDXGISwapChain1::SetBackgroundColor](https://msdn.microsoft.com/en-us/library/hh446799(v=vs.85).aspx) -

: Directs DXGI to make the back-buffer contents scale to fit the presentation target size, while preserving the aspect ratio of the back-buffer. If the scaled back-buffer does not fill the presentation area, it will be centered with black borders. This constant is supported on Windows Phone 8 and Windows 10. This constant cannot be used with[DXGI_SCALING_ASPECT_RATIO_STRETCH](https://msdn.microsoft.com/en-us/library/hh404526(v=vs.85).aspx#DXGI_SCALING_ASPECT_RATIO_STRETCH)

.[IDXGIFactory2::CreateSwapChainForHwnd](https://msdn.microsoft.com/en-us/library/hh404557(v=vs.85).aspx)

-
-

: A[DXGI_SWAP_EFFECT](https://msdn.microsoft.com/en-us/library/bb173077(v=vs.85).aspx)SwapEffect`DXGI_SWAP_EFFECT`

-typed value that describes the presentation model that is used by the swap chain and options for handling the contents of the presentation buffer after presenting a surface. Valid values for this member are:-

: Use this flag to specify the flip presentation model and to specify that DXGI persist the contents of the back buffer after you call[DXGI_SWAP_EFFECT_FLIP_SEQUENTIAL](https://msdn.microsoft.com/en-us/library/windows/desktop/bb173077(v=vs.85).aspx#DXGI_SWAP_EFFECT_FLIP_SEQUENTIAL)

. This flag cannot be used with multisampling.[IDXGISwapChain1::Present1](https://msdn.microsoft.com/en-us/library/windows/desktop/hh446797(v=vs.85).aspx) -

: Use this flag to specify the flip presentation model and to specify that DXGI discard the contents of the back buffer after you call[DXGI_SWAP_EFFECT_FLIP_DISCARD](https://msdn.microsoft.com/en-us/library/windows/desktop/bb173077(v=vs.85).aspx#DXGI_SWAP_EFFECT_FLIP_DISCARD)

. This flag cannot be used with multisampling and partial presentation.[IDXGISwapChain1::Present1](https://msdn.microsoft.com/en-us/library/windows/desktop/hh446797(v=vs.85).aspx)

-
-

: A[DXGI_ALPHA_MODE](https://msdn.microsoft.com/en-us/library/hh404496(v=vs.85).aspx)AlphaMode

-typed value that identifies the transparency behavior of the swap-chain back buffer. The following values are supported:[DXGI_ALPHA_MODE](https://msdn.microsoft.com/en-us/library/hh404496(v=vs.85).aspx)-

: Indicates that the transparency behavior is not specified.[DXGI_ALPHA_MODE_UNSPECIFIED](https://msdn.microsoft.com/en-us/library/hh404496(v=vs.85).aspx#DXGI_ALPHA_MODE_UNSPECIFIED) -

: Indicates that the transparency behavior is premultiplied. Each color is first scaled by the alpha value. The alpha value itself is the same in both straight and premultiplied alpha. Typically, no color channel value is greater than the alpha channel value. If a color channel value in a premultiplied format is greater than the alpha channel, the standard source-over blending math results in an additive blend.[DXGI_ALPHA_MODE_PREMULTIPLIED](https://msdn.microsoft.com/en-us/library/hh404496(v=vs.85).aspx#DXGI_ALPHA_MODE_PREMULTIPLIED) -

: Indicates that the transparency behavior is not premultiplied. The alpha channel indicates the transparency of the color.[DXGI_ALPHA_MODE_STRAIGHT](https://msdn.microsoft.com/en-us/library/hh404496(v=vs.85).aspx#DXGI_ALPHA_MODE_STRAIGHT) -

: Indicates to ignore the transparency behavior.[DXGI_ALPHA_MODE_IGNORE](https://msdn.microsoft.com/en-us/library/hh404496(v=vs.85).aspx#DXGI_ALPHA_MODE_IGNORE)

-
-
`UINT Flags`

: A combination of

-typed values that are combined by using a bitwise OR operation. The[DXGI_SWAP_CHAIN_FLAG](https://msdn.microsoft.com/en-us/library/bb173076(v=vs.85).aspx)

flag should always be specified if tearing support is available. See[DXGI_SWAP_CHAIN_FLAG_ALLOW_TEARING](https://msdn.microsoft.com/en-us/library/bb173076(v=vs.85).aspx#DXGI_SWAP_CHAIN_FLAG_ALLOW_TEARING)[Check for Tearing Support](https://www.3dgep.com#Check_for_Tearing_Support)for more information on detecting tearing support.

With the swap chain description specified, the swap chain can be created.

|
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
|
ComPtr<IDXGISwapChain1> swapChain1;
ThrowIfFailed(dxgiFactory4->CreateSwapChainForHwnd(
commandQueue.Get(),
hWnd,
&swapChainDesc,
nullptr,
nullptr,
&swapChain1));
// Disable the Alt+Enter fullscreen toggle feature. Switching to fullscreen
// will be handled manually.
ThrowIfFailed(dxgiFactory4->MakeWindowAssociation(hWnd, DXGI_MWA_NO_ALT_ENTER));
ThrowIfFailed(swapChain1.As(&dxgiSwapChain4));
return dxgiSwapChain4;
}
|

The

method is used to create a swap chain that is associated with a OS window handle. This method has the following signature [IDXGIFactory2::CreateSwapChainForHwnd](https://msdn.microsoft.com/en-us/library/hh404557(v=vs.85).aspx)[[23]](https://www.3dgep.com#cite-23):

|
1
2
3
4
5
6
7
8
|
HRESULT CreateSwapChainForHwnd(
[in] IUnknown *pDevice,
[in] HWND hWnd,
[in] const DXGI_SWAP_CHAIN_DESC1 *pDesc,
[in, optional] const DXGI_SWAP_CHAIN_FULLSCREEN_DESC *pFullscreenDesc,
[in, optional] IDXGIOutput *pRestrictToOutput,
[out] IDXGISwapChain1 **ppSwapChain
);
|

And takes the following arguments:

-
`IUnknown *pDevice`

: For Direct3D 12 this is a pointer to a direct command queue (refer to

). This parameter cannot be[ID3D12CommandQueue](https://msdn.microsoft.com/en-us/library/dn788627(v=vs.85).aspx)`NULL`

. -

: The[HWND](https://msdn.microsoft.com/en-us/library/aa383751(v=vs.85).aspx)hWnd

handle that is associated with the swap chain that[HWND](https://msdn.microsoft.com/en-us/library/aa383751(v=vs.85).aspx)

creates. This parameter cannot be[CreateSwapChainForHwnd](https://msdn.microsoft.com/en-us/library/hh404557(v=vs.85).aspx)`NULL`

. -

: A pointer to a[DXGI_SWAP_CHAIN_DESC1](https://msdn.microsoft.com/en-us/library/hh404528(v=vs.85).aspx)*pDesc

structure for the swap-chain description. This parameter cannot be[DXGI_SWAP_CHAIN_DESC1](https://msdn.microsoft.com/en-us/library/hh404528(v=vs.85).aspx)`NULL`

. -

: A pointer to a[DXGI_SWAP_CHAIN_FULLSCREEN_DESC](https://msdn.microsoft.com/en-us/library/hh404531(v=vs.85).aspx)*pFullscreenDesc

structure for the description of a full-screen swap chain. You can optionally set this parameter to create a full-screen swap chain. Set it to[DXGI_SWAP_CHAIN_FULLSCREEN_DESC](https://msdn.microsoft.com/en-us/library/hh404531(v=vs.85).aspx)`NULL`

to create a windowed swap chain. -

: A pointer to the[IDXGIOutput](https://msdn.microsoft.com/en-us/library/bb174546(v=vs.85).aspx)*pRestrictToOutput

interface for the output to restrict content to. You must also pass the[IDXGIOutput](https://msdn.microsoft.com/en-us/library/bb174546(v=vs.85).aspx)

flag in a[DXGI_PRESENT_RESTRICT_TO_OUTPUT](https://msdn.microsoft.com/en-us/library/bb509554(v=vs.85).aspx#DXGI_PRESENT_RESTRICT_TO_OUTPUT)

call to force the content to appear blacked out on any other output. If you want to restrict the content to a different output, you must create a new swap chain. However, you can conditionally restrict content based on the[IDXGISwapChain1::Present1](https://msdn.microsoft.com/en-us/library/hh446797(v=vs.85).aspx)

flag.[DXGI_PRESENT_RESTRICT_TO_OUTPUT](https://msdn.microsoft.com/en-us/library/bb509554(v=vs.85).aspx#DXGI_PRESENT_RESTRICT_TO_OUTPUT)

Set this parameter to`NULL`

if you don’t want to restrict content to an output target. -

: A pointer to a variable that receives a pointer to the[IDXGISwapChain1](https://msdn.microsoft.com/en-us/library/hh404631(v=vs.85).aspx)**ppSwapChain

interface for the swap chain that[IDXGISwapChain1](https://msdn.microsoft.com/en-us/library/hh404631(v=vs.85).aspx)

creates.[CreateSwapChainForHwnd](https://msdn.microsoft.com/en-us/library/hh404557(v=vs.85).aspx)

Switching to a full screen state will be handled manually using a full-screen borderless window. In order to prevent DXGI from switching to a full screen state automatically when pressing the `Alt`+`Enter` key combination on the keyboard, the

method is used specifying the [IDXGIFactory::MakeWindowAssociation](https://msdn.microsoft.com/en-us/library/bb174540(v=vs.85).aspx)`DXGI_MWA_NO_ALT_ENTER`

flag. This effectively prevents DXGI from responding to the `Alt`+`Enter` keyboard sequence.

On line 350, the swap chain is converted to the

interface type using the [IDXGISwapChain4](https://msdn.microsoft.com/en-us/library/mt732707(v=vs.85).aspx)

method and returned to the calling function.[ComPtr::As](https://docs.microsoft.com/en-us/cpp/windows/comptr-as-method)

To render to the swap chain’s back buffers, a **render target view** (**RTV**) needs to be created for each of the swap chain’s back buffers. In the next sections, a descriptor heap is created and the views for each back buffer are recorded into the descriptors of the descriptor heap.

A **descriptor heap** can be considered an array of resource views. As of DirectX 12, before resource views can be created (such as **Render Target Views** (**RTV**), **Shader Resource Views** (**SRV**), **Unordered Access Views** (**UAV**), or **Constant Buffer Views** (**CBV**)), a descriptor heap needs to be created. Certain types of resource views (descriptors) can be created in the same heap. For example, CBV, SRV, and UAV can be stored in the same heap but RTV and Sampler views each require separate descriptor heaps. Descriptor heaps will be discussed in more detail in another lesson which deals with binding textures to the rendering pipeline. For now, a descriptor heap is created to store the render target views for the swap chain buffers.

|
1
2
3
4
5
6
7
8
9
10
11
12
13
|
ComPtr<ID3D12DescriptorHeap> CreateDescriptorHeap(ComPtr<ID3D12Device2> device,
D3D12_DESCRIPTOR_HEAP_TYPE type, uint32_t numDescriptors)
{
ComPtr<ID3D12DescriptorHeap> descriptorHeap;
D3D12_DESCRIPTOR_HEAP_DESC desc = {};
desc.NumDescriptors = numDescriptors;
desc.Type = type;
ThrowIfFailed(device->CreateDescriptorHeap(&desc, IID_PPV_ARGS(&descriptorHeap)));
return descriptorHeap;
}
|

The `CreateDescriptorHeap`

function described above is used to create a descriptor heap of a specific type. The descriptor heap is created based on the

structure which has the following definition [D3D12_DESCRIPTOR_HEAP_DESC](https://msdn.microsoft.com/en-us/library/dn770359(v=vs.85).aspx)[[24]](https://www.3dgep.com#cite-24):

|
1
2
3
4
5
6
|
typedef struct D3D12_DESCRIPTOR_HEAP_DESC {
D3D12_DESCRIPTOR_HEAP_TYPE Type;
UINT NumDescriptors;
D3D12_DESCRIPTOR_HEAP_FLAGS Flags;
UINT NodeMask;
} D3D12_DESCRIPTOR_HEAP_DESC;
|

The members of the

structure are:[D3D12_DESCRIPTOR_HEAP_DESC](https://msdn.microsoft.com/en-us/library/dn770359(v=vs.85).aspx)

-

: A[D3D12_DESCRIPTOR_HEAP_TYPE](https://msdn.microsoft.com/en-us/library/dn859379(v=vs.85).aspx)Type

-typed value that specifies the types of descriptors in the heap. The Type member can have one of the following values:[D3D12_DESCRIPTOR_HEAP_TYPE](https://msdn.microsoft.com/en-us/library/dn859379(v=vs.85).aspx)-

: The descriptor heap for the combination of constant-buffer, shader-resource, and unordered-access views.[D3D12_DESCRIPTOR_HEAP_TYPE_CBV_SRV_UAV](https://msdn.microsoft.com/en-us/library/dn859379(v=vs.85).aspx#D3D12_DESCRIPTOR_HEAP_TYPE_CBV_SRV_UAV) -

: The descriptor heap for the sampler.[D3D12_DESCRIPTOR_HEAP_TYPE_SAMPLER](https://msdn.microsoft.com/en-us/library/dn859379(v=vs.85).aspx#D3D12_DESCRIPTOR_HEAP_TYPE_SAMPLER) -

: The descriptor heap for the render-target view.[D3D12_DESCRIPTOR_HEAP_TYPE_RTV](https://msdn.microsoft.com/en-us/library/dn859379(v=vs.85).aspx#D3D12_DESCRIPTOR_HEAP_TYPE_RTV) -

: The descriptor heap for the depth-stencil view.[D3D12_DESCRIPTOR_HEAP_TYPE_DSV](https://msdn.microsoft.com/en-us/library/dn859379(v=vs.85).aspx#D3D12_DESCRIPTOR_HEAP_TYPE_DSV)

-
-
`UINT NumDescriptors`

: The number of descriptors in the heap. -

: A combination of[D3D12_DESCRIPTOR_HEAP_FLAGS](https://msdn.microsoft.com/en-us/library/dn859378(v=vs.85).aspx)Flags

-typed values that are combined by using a bitwise OR operation. The resulting value specifies options for the heap. Valid flags for the descriptor heap creation are:[D3D12_DESCRIPTOR_HEAP_FLAGS](https://msdn.microsoft.com/en-us/library/dn859378(v=vs.85).aspx)-

: Indicates default usage of a heap.[D3D12_DESCRIPTOR_HEAP_FLAG_NONE](https://msdn.microsoft.com/en-us/library/dn859378(v=vs.85).aspx#D3D12_DESCRIPTOR_HEAP_FLAG_NONE) -

: The flag[D3D12_DESCRIPTOR_HEAP_FLAG_SHADER_VISIBLE](https://msdn.microsoft.com/en-us/library/dn859378(v=vs.85).aspx#D3D12_DESCRIPTOR_HEAP_FLAG_SHADER_VISIBLE)

can optionally be set on a descriptor heap to indicate that it can be bound on a command list for reference by shaders. Descriptor heaps created without this flag allow applications the option to stage descriptors in CPU memory before copying them to a shader visible descriptor heap, as a convenience. But it is also fine for applications to directly create descriptors into shader visible descriptor heaps with no requirement to stage anything on the CPU.[D3D12_DESCRIPTOR_HEAP_FLAG_SHADER_VISIBLE](https://msdn.microsoft.com/en-us/library/dn859378(v=vs.85).aspx#D3D12_DESCRIPTOR_HEAP_FLAG_SHADER_VISIBLE)

This flag only applies to CBV, SRV, UAV and samplers. It does not apply to other descriptor heap types since shaders do not directly reference the other types.

-
-
`UINT NodeMask`

: For single-adapter operation, set this to zero. If there are multiple adapter nodes, set a bit to identify the node (one of the device’s physical adapters) to which the descriptor heap applies. Each bit in the mask corresponds to a single node. Only one bit must be set.

The descriptor heap is created on line 364 using the

method.[ID3D12Device::CreateDescriptorHeap](https://msdn.microsoft.com/en-us/library/dn788662(v=vs.85).aspx)

With the descriptor heap created, the render target views (RTV) for the swap chain’s buffers can be created.

A render target view (RTV) describes a resource that can be attached to a bind slot of the output merger stage (see [Output Merger Stage](https://www.3dgep.com#Output-Merger_Stage)). The render target view describes the resource that receives the final color computed by the pixel shader stage.

More complex usages of render targets will be discussed in the next lesson. For this lesson, the render target will only be cleared to a specific color.

For each back buffer of the swap chain, a single RTV is used to describe the resource.

|
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
|
void UpdateRenderTargetViews(ComPtr<ID3D12Device2> device,
ComPtr<IDXGISwapChain4> swapChain, ComPtr<ID3D12DescriptorHeap> descriptorHeap)
{
auto rtvDescriptorSize = device->GetDescriptorHandleIncrementSize(D3D12_DESCRIPTOR_HEAP_TYPE_RTV);
CD3DX12_CPU_DESCRIPTOR_HANDLE rtvHandle(descriptorHeap->GetCPUDescriptorHandleForHeapStart());
for (int i = 0; i < g_NumFrames; ++i)
{
ComPtr<ID3D12Resource> backBuffer;
ThrowIfFailed(swapChain->GetBuffer(i, IID_PPV_ARGS(&backBuffer)));
device->CreateRenderTargetView(backBuffer.Get(), nullptr, rtvHandle);
g_BackBuffers[i] = backBuffer;
rtvHandle.Offset(rtvDescriptorSize);
}
}
|

The size of a single descriptor in a descriptor heap is vendor specific and is queried on line 372 using the

method. [ID3D12Device::GetDescriptorHandleIncrementSize](https://msdn.microsoft.com/en-us/library/dn899186(v=vs.85).aspx)

In order to iterate the descriptors in a descriptor heap, a handle to the first descriptor in the heap is retrieved on line 374 using the

method. This method returns a [ID3D12DescriptorHeap::GetCPUDescriptorHandleForHeapStart](https://msdn.microsoft.com/en-us/library/dn899174(v=vs.85).aspx)

structure which is a very simple structure that aliases a pointer to a descriptor within a descriptor heap. The [D3D12_CPU_DESCRIPTOR_HANDLE](https://msdn.microsoft.com/en-us/library/dn859369(v=vs.85).aspx)

structure (from the [CD3DX12_CPU_DESCRIPTOR_HANDLE](https://msdn.microsoft.com/en-us/library/mt186565(v=vs.85).aspx)

header file) extends the simple [d3dx12.h](https://msdn.microsoft.com/en-us/library/mt186617(v=vs.85).aspx)

structure providing more functionality to iterate the descriptor heap.[D3D12_CPU_DESCRIPTOR_HANDLE](https://msdn.microsoft.com/en-us/library/dn859369(v=vs.85).aspx)

A pointer to the swap chain’s back buffers is queried on line 379 using the

method.[IDXGISwapChain::GetBuffer](https://msdn.microsoft.com/en-us/library/bb174570(v=vs.85).aspx)

The

method is used to create the RTV. The first parameter to this method is the pointer to the resource that contains the render target texture. The second parameter is a pointer to a [ID3D12Device::CreateRenderTargetView](https://msdn.microsoft.com/en-us/library/dn788668(v=vs.85).aspx)

structure. A [D3D12_RENDER_TARGET_VIEW_DESC](https://msdn.microsoft.com/en-us/library/dn770389(v=vs.85).aspx)`NULL`

description is used to create a default descriptor for the resource. In this case, the resource’s internal description is used to create the RTV. The third parameter to the

method is the handle to the descriptor where the view is placed.[ID3D12Device::CreateRenderTargetView](https://msdn.microsoft.com/en-us/library/dn788668(v=vs.85).aspx)

A pointer to the buffer is also stored in the `g_BackBuffers`

global variable so that the resource can be transitioned to the correct state as will be shown later. Resource transitions will be discussed in more detail later in this lesson.

On line 385, the descriptor handle is incremented to the next handle in the descriptor heap using the `Offset`

method of the

structure.[CD3DX12_CPU_DESCRIPTOR_HANDLE](https://msdn.microsoft.com/en-us/library/mt186565(v=vs.85).aspx)

In the next sections, the command allocator and command list is created. Command allocators and command lists are required to issue rendering commands to the GPU.

A **command allocator** is the backing memory used by a **command list**. A command allocator is created using the

method and must specify the type of command list the allocator will be used with. The command allocator does not provide any functionality and can only be accessed indirectly through a command list. A command allocator can only be used by a single command list at a time but can be reused after the commands that were recorded into the command list have finished executing on the GPU.[ID3D12Device::CreateCommandAllocator](https://msdn.microsoft.com/en-us/library/dn788655(v=vs.85).aspx)

The memory allocated by the command allocator is reclaimed using the

method. A command allocator can only be reset after the commands recorded in the command list have finished executing on the GPU. A GPU fence is used to check if the GPU commands have finished executing on the GPU. Using GPU fences to synchronize GPU commands is shown in the following sections.[ID3D12CommandAllocator::Reset](https://msdn.microsoft.com/en-us/library/dn770464(v=vs.85).aspx)

The `CreateCommandAllocator`

function is used to create the command allocator for the application. In order to achieve maximum frame-rates for the application, one command allocator per “in-flight” command list should be created. The `CreateCommandAllocator`

function shown here only creates a single command allocator but this function will be used later to create multiple allocators for the demo.

|
1
2
3
4
5
6
7
8
|
ComPtr<ID3D12CommandAllocator> CreateCommandAllocator(ComPtr<ID3D12Device2> device,
D3D12_COMMAND_LIST_TYPE type)
{
ComPtr<ID3D12CommandAllocator> commandAllocator;
ThrowIfFailed(device->CreateCommandAllocator(type, IID_PPV_ARGS(&commandAllocator)));
return commandAllocator;
}
|

The

method is used to create the command allocator. This method has the following signature [ID3D12Device::CreateCommandAllocator](https://msdn.microsoft.com/en-us/library/dn788655(v=vs.85).aspx)[[25]](https://www.3dgep.com#cite-25):

|
1
2
3
4
5
|
HRESULT CreateCommandAllocator(
[in] D3D12_COMMAND_LIST_TYPE type,
REFIID riid,
[out] void **ppCommandAllocator
);
|

Where:

-

: A[D3D12_COMMAND_LIST_TYPE](https://msdn.microsoft.com/en-us/library/dn770348(v=vs.85).aspx)type

-typed value that specifies the type of command allocator to create. The type of command allocator can be the type that records either direct command lists or bundles. The command allocator can be one of the following types:[D3D12_COMMAND_LIST_TYPE](https://msdn.microsoft.com/en-us/library/dn770348(v=vs.85).aspx)-

: Specifies a command buffer that the GPU can execute. A direct command list doesn’t inherit any GPU state.[D3D12_COMMAND_LIST_TYPE_DIRECT](https://msdn.microsoft.com/en-us/library/dn770348(v=vs.85).aspx#D3D12_COMMAND_LIST_TYPE_DIRECT) -

: Specifies a command buffer that can be executed only directly via a direct command list. A bundle command list inherits all GPU state (except for the currently set pipeline state object and primitive topology).[D3D12_COMMAND_LIST_TYPE_BUNDLE](https://msdn.microsoft.com/en-us/library/dn770348(v=vs.85).aspx#D3D12_COMMAND_LIST_TYPE_BUNDLE) -

: Specifies a command buffer for computing.[D3D12_COMMAND_LIST_TYPE_COMPUTE](https://msdn.microsoft.com/en-us/library/dn770348(v=vs.85).aspx#D3D12_COMMAND_LIST_TYPE_COMPUTE) -

: Specifies a command buffer for copying.[D3D12_COMMAND_LIST_TYPE_COPY](https://msdn.microsoft.com/en-us/library/dn770348(v=vs.85).aspx#D3D12_COMMAND_LIST_TYPE_COPY)

-
-
`REFIID riid`

: The globally unique identifier (**GUID**) for the command allocator interface (

). The[ID3D12CommandAllocator](https://msdn.microsoft.com/en-us/library/dn770463(v=vs.85).aspx)**REFIID**, or**GUID**, of the interface to the command allocator can be obtained by using the

macro. For example,[__uuidof](https://docs.microsoft.com/en-us/cpp/cpp/uuidof-operator)

will get the[__uuidof](https://docs.microsoft.com/en-us/cpp/cpp/uuidof-operator)([ID3D12CommandAllocator](https://msdn.microsoft.com/en-us/library/dn770463(v=vs.85).aspx))**GUID**of the interface to a command allocator. -
`void **ppCommandAllocator`

: A pointer to a memory block that receives a pointer to the

interface for the command allocator.[ID3D12CommandAllocator](https://msdn.microsoft.com/en-us/library/dn770463(v=vs.85).aspx)

The command list is created next.

A command list is used for recording commands that are executed on the GPU. Unlike previous versions of DirectX, execution of commands recorded into a command list are always deferred. That is, invoking draw or dispatch commands on a command list are not executed until the command list is sent to the command queue.

Unlike the command allocator, the command list can be reused immediately after it has been executed on the command queue. The only restriction is that the command list must be reset first before recording any new commands.

The `CreateCommandList`

function is used to create a command list for the application.

|
1
2
3
4
5
6
7
8
9
10
|
ComPtr<ID3D12GraphicsCommandList> CreateCommandList(ComPtr<ID3D12Device2> device,
ComPtr<ID3D12CommandAllocator> commandAllocator, D3D12_COMMAND_LIST_TYPE type)
{
ComPtr<ID3D12GraphicsCommandList> commandList;
ThrowIfFailed(device->CreateCommandList(0, type, commandAllocator.Get(), nullptr, IID_PPV_ARGS(&commandList)));
ThrowIfFailed(commandList->Close());
return commandList;
}
|

The command list is created on line 402 using the

method. This method has the following signature [ID3D12Device::CreateCommandList](https://msdn.microsoft.com/en-us/library/dn788656(v=vs.85).aspx)[[26]](https://www.3dgep.com#cite-26):

|
1
2
3
4
5
6
7
8
|
HRESULT CreateCommandList(
[in] UINT nodeMask,
[in] D3D12_COMMAND_LIST_TYPE type,
[in] ID3D12CommandAllocator *pCommandAllocator,
[in, optional] ID3D12PipelineState *pInitialState,
REFIID riid,
[out] void **ppCommandList
);
|

Where each parameter has the following definition:

-
`UINT nodeMask`

: For single GPU operation, set this to zero. If there are multiple GPU nodes, set a bit to identify the node (the device’s physical adapter) for which to create the command list. Each bit in the mask corresponds to a single node. Only 1 bit must be set. -

: A[D3D12_COMMAND_LIST_TYPE](https://msdn.microsoft.com/en-us/library/dn770348(v=vs.85).aspx)type

-typed value that specifies the type of command list to create. The command list can be one of the following types:[D3D12_COMMAND_LIST_TYPE](https://msdn.microsoft.com/en-us/library/dn770348(v=vs.85).aspx)-

: Specifies a command buffer that the GPU can execute. A direct command list doesn’t inherit any GPU state.[D3D12_COMMAND_LIST_TYPE_DIRECT](https://msdn.microsoft.com/en-us/library/dn770348(v=vs.85).aspx#D3D12_COMMAND_LIST_TYPE_DIRECT) -

: Specifies a command buffer that can be executed only directly via a direct command list. A bundle command list inherits all GPU state (except for the currently set pipeline state object and primitive topology).[D3D12_COMMAND_LIST_TYPE_BUNDLE](https://msdn.microsoft.com/en-us/library/dn770348(v=vs.85).aspx#D3D12_COMMAND_LIST_TYPE_BUNDLE) -

: Specifies a command buffer for computing.[D3D12_COMMAND_LIST_TYPE_COMPUTE](https://msdn.microsoft.com/en-us/library/dn770348(v=vs.85).aspx#D3D12_COMMAND_LIST_TYPE_COMPUTE) -

: Specifies a command buffer for copying.[D3D12_COMMAND_LIST_TYPE_COPY](https://msdn.microsoft.com/en-us/library/dn770348(v=vs.85).aspx#D3D12_COMMAND_LIST_TYPE_COPY)

-
-

: A pointer to the[ID3D12CommandAllocator](https://msdn.microsoft.com/en-us/library/dn770463(v=vs.85).aspx)*pCommandAllocator

object that the device creates command lists from.[ID3D12CommandAllocator](https://msdn.microsoft.com/en-us/library/dn770463(v=vs.85).aspx) -

: A pointer to the[ID3D12PipelineState](https://msdn.microsoft.com/en-us/library/dn788705(v=vs.85).aspx)*pInitialState

object that contains the initial pipeline state for the command list. This is optional and can be[ID3D12PipelineState](https://msdn.microsoft.com/en-us/library/dn788705(v=vs.85).aspx)`NULL`

. If`NULL`

, the runtime sets a dummy initial pipeline state so that drivers don’t have to deal with undefined state. The overhead for this is low, particularly for a command list, for which the overall cost of recording the command list likely dwarfs the cost of one initial state setting. So there is little cost in not setting the initial pipeline state parameter if it isn’t convenient. Since pipeline state objects are not used in this lesson, the parameter can be`NULL`

. Pipeline state objects will be introduced in the next lessons. -
`REFIID riid`

: The globally unique identifier (**GUID**) for the command list interface. The**REFIID**, or**GUID**, of the interface to the command list can be obtained by using the

macro. For example,[__uuidof](https://docs.microsoft.com/en-us/cpp/cpp/uuidof-operator)

will get the[__uuidof](https://docs.microsoft.com/en-us/cpp/cpp/uuidof-operator)([ID3D12CommandList](https://msdn.microsoft.com/en-us/library/dn770465(v=vs.85).aspx))**GUID**of the interface to a command list. -
`void **ppCommandList`

: A pointer to a memory block that receives a pointer to the

or[ID3D12CommandList](https://msdn.microsoft.com/en-us/library/dn770465(v=vs.85).aspx)

interface for the command list.[ID3D12GraphicsCommandList](https://msdn.microsoft.com/en-us/library/dn903537(v=vs.85).aspx)

Command lists are created in the recording state. For consistency, the first operation that is performed on the command list in the render loop (which will be shown later) is a

. Before the command list can be reset, it must first be closed. The command list is closed on line 404 so that it can be reset before recording commands in the render loop.[ID3D12GraphicsCommandList::Reset](https://msdn.microsoft.com/en-us/library/windows/desktop/dn903895(v=vs.85).aspx)

The next several functions deal with GPU synchronization.

The

is an interface for a GPU / CPU synchronization object. Fences can be used to perform synchronization on either the CPU or the GPU.[ID3D12Fence](https://msdn.microsoft.com/en-us/library/windows/desktop/dn899188(v=vs.85).aspx)

Internally, a fence stores a single 64-bit unsigned integer value. The fence’s initial value is specified when the fence is created. The fence’s internal value is updated on the CPU using the

method and it is updated on the GPU using the [ID3D12Fence::Signal](https://msdn.microsoft.com/en-us/library/windows/desktop/dn899191(v=vs.85).aspx)

method. [ID3D12CommandQueue::Signal](https://msdn.microsoft.com/en-us/library/windows/desktop/dn899171(v=vs.85).aspx)

To wait for a fence to reach a specific value on the CPU, use the

method followed by a call to the [ID3D12Fence::SetEventOnCompletion](https://msdn.microsoft.com/en-us/library/windows/desktop/dn899190(v=vs.85).aspx)

function. To wait for the fence to reach a specific value on the GPU, use the [WaitForSingleObject](https://msdn.microsoft.com/en-us/library/ms687032(v=vs.85).aspx)

method.[ID3D12CommandQueue::Wait](https://msdn.microsoft.com/en-us/library/windows/desktop/dn899173(v=vs.85).aspx)

The following table summarizes the methods to use to synchronize with a fence object.

| CPU | GPU | |
|---|---|---|
Signal |
|
|
Wait |
,
|
|

Pseudo-code for using a fence object was shown previously in the section titled [GPU Synchronization](https://www.3dgep.com#GPU_Synchronization).

As a rule-of-thumb, the fence object should be initialized with a value of zero and the fence value should only be allowed to increase. The fence is considered reached if it is equal to or greater than a specific fence value.

As previously explained when discussing [GPU Synchronization](https://www.3dgep.com#GPU_Synchronization), each thread or GPU queue should have at least one fence object and a corresponding fence value. The same fence object should not be signaled from more than one thread or GPU queue but more than one thread or queue can wait on the same fence to be signaled.

The `CreateFence`

function is used to create a fence object for the application.

|
1
2
3
4
5
6
7
8
|
ComPtr<ID3D12Fence> CreateFence(ComPtr<ID3D12Device2> device)
{
ComPtr<ID3D12Fence> fence;
ThrowIfFailed(device->CreateFence(0, D3D12_FENCE_FLAG_NONE, IID_PPV_ARGS(&fence)));
return fence;
}
|

A

object is created using the [ID3D12Fence](https://msdn.microsoft.com/en-us/library/dn899188(v=vs.85).aspx)

method. This method has the following signature [ID3D12Device::CreateFence](https://msdn.microsoft.com/en-us/library/dn899179(v=vs.85).aspx)[[27]](https://www.3dgep.com#cite-27):

|
1
2
3
4
5
6
|
HRESULT CreateFence(
UINT64 InitialValue,
D3D12_FENCE_FLAGS Flags,
REFIID riid,
[out] void **ppFence
);
|

And takes the following arguments:

-
`UINT64 InitialValue`

: The initial value for the fence. In most normal use-cases, the initial value of the fence should be 0. -

: A combination of[D3D12_FENCE_FLAGS](https://msdn.microsoft.com/en-us/library/dn986729(v=vs.85).aspx)Flags

-typed values that are combined by using a bitwise OR operation. The resulting value specifies options for the fence. Valid fence flags are:[D3D12_FENCE_FLAGS](https://msdn.microsoft.com/en-us/library/dn986729(v=vs.85).aspx)-

: No options are specified.[D3D12_FENCE_FLAG_NONE](https://msdn.microsoft.com/en-us/library/dn986729(v=vs.85).aspx#D3D12_FENCE_FLAG_NONE) -

: The fence is shared.[D3D12_FENCE_FLAG_SHARED](https://msdn.microsoft.com/en-us/library/dn986729(v=vs.85).aspx#D3D12_FENCE_FLAG_SHARED) -

: The fence is shared with another GPU adapter.[D3D12_FENCE_FLAG_SHARED_CROSS_ADAPTER](https://msdn.microsoft.com/en-us/library/dn986729(v=vs.85).aspx#D3D12_FENCE_FLAG_SHARED_CROSS_ADAPTER) -

: The fence is of the non-monitored type. Non-monitored fences should only be used when the adapter doesn’t support monitored fences, or when a fence is shared with an adapter that doesn’t support monitored fences.[D3D12_FENCE_FLAG_NON_MONITORED](https://msdn.microsoft.com/en-us/library/dn986729(v=vs.85).aspx#D3D12_FENCE_FLAG_NON_MONITORED)

-
-
`REFIID riid`

: The globally unique identifier (**GUID**) for the fence interface (

). The[ID3D12Fence](https://msdn.microsoft.com/en-us/library/dn899188(v=vs.85).aspx)**REFIID**, or**GUID**, of the interface to the fence can be obtained by using the

macro. For example,[__uuidof](https://docs.microsoft.com/en-us/cpp/cpp/uuidof-operator)

will get the[__uuidof](https://docs.microsoft.com/en-us/cpp/cpp/uuidof-operator)([ID3D12Fence](https://msdn.microsoft.com/en-us/library/dn899188(v=vs.85).aspx))**GUID**of the interface to a fence. -
`void **ppFence`

: A pointer to a memory block that receives a pointer to the

interface that is used to access the fence.[ID3D12Fence](https://msdn.microsoft.com/en-us/library/dn899188(v=vs.85).aspx)

An OS event handle is used to allow the CPU thread to wait until the fence has been signaled with a particular value. In the next section, the OS event handle is created.

If the fence has not yet been signaled with specific value, the CPU thread will need to block any further processing until the fence has been signaled with that value. An OS event handle is used to block the CPU thread until the fence has been signaled. The `CreateEventHandle`

function described next is used to create the OS event.

|
1
2
3
4
5
6
7
8
9
|
HANDLE CreateEventHandle()
{
HANDLE fenceEvent;
fenceEvent = ::CreateEvent(NULL, FALSE, FALSE, NULL);
assert(fenceEvent && "Failed to create fence event.");
return fenceEvent;
}
|

The OS event handle is created using the

function which has the following signature [CreateEvent](https://msdn.microsoft.com/en-us/library/ms682396(v=vs.85).aspx)[[28]](https://www.3dgep.com#cite-28):

|
1
2
3
4
5
6
|
HANDLE WINAPI CreateEvent(
_In_opt_ LPSECURITY_ATTRIBUTES lpEventAttributes,
_In_ BOOL bManualReset,
_In_ BOOL bInitialState,
_In_opt_ LPCTSTR lpName
);
|

And takes the following arguments:

-

: A pointer to a[LPSECURITY_ATTRIBUTES](https://msdn.microsoft.com/en-us/library/aa379560(v=vs.85).aspx)lpEventAttributes

structure. If this parameter is[SECURITY_ATTRIBUTES](https://msdn.microsoft.com/en-us/library/aa379560(v=vs.85).aspx)`NULL`

, the handle cannot be inherited by child processes. -
`BOOL bManualReset`

: If this parameter is`TRUE`

, the function creates a manual-reset event object, which requires the use of the

function to set the event state to nonsignaled. If this parameter is[ResetEvent](https://msdn.microsoft.com/en-us/library/ms685081(v=vs.85).aspx)`FALSE`

, the function creates an auto-reset event object, and system automatically resets the event state to nonsignaled after a single waiting thread has been released. -
`BOOL bInitialState`

: If this parameter is`TRUE`

, the initial state of the event object is signaled; otherwise, it is non-signaled. -
`LPCTSTR lpName`

: The name of the event object. If`lpName`

is`NULL`

, the event object is created without a name.

The OS event is used to cause the CPU thread to stall using the

function which will be shown later.[WaitForSingleObject](https://msdn.microsoft.com/en-us/library/ms687032(v=vs.85).aspx)

The `Signal`

function is used to signal the fence from the GPU. It should be noted that when using the

method to signal a fence from the GPU, the fence is not signaled immediatly but is only signaled once the GPU command queue has reached that point during execution. Any commands that have been queued before the signal method was invoked must complete execution before the fence will be signaled.[ID3D12CommandQueue::Signal](https://msdn.microsoft.com/en-us/library/windows/desktop/dn899171(v=vs.85).aspx)

|
1
2
3
4
5
6
7
8
|
uint64_t Signal(ComPtr<ID3D12CommandQueue> commandQueue, ComPtr<ID3D12Fence> fence,
uint64_t& fenceValue)
{
uint64_t fenceValueForSignal = ++fenceValue;
ThrowIfFailed(commandQueue->Signal(fence.Get(), fenceValueForSignal));
return fenceValueForSignal;
}
|

The fence is signaled after all of the commands that have been queued on the command queue have finished executing. The `Signal`

function returns the fence value that the CPU thread should wait for before reusing any resources that are “in-flight” for that frame on the GPU.

The fence is signaled on the GPU using the

method. This method has the following signature [ID3D12CommandQueue::Signal](https://msdn.microsoft.com/en-us/library/windows/desktop/dn899171(v=vs.85).aspx)[[29]](https://www.3dgep.com#cite-29):

|
1
2
3
4
|
HRESULT Signal(
ID3D12Fence *pFence,
UINT64 Value
);
|

And takes the following arguments:

-

: A pointer to the[ID3D12Fence](https://msdn.microsoft.com/en-us/library/windows/desktop/dn899188(v=vs.85).aspx)*pFence

object.[ID3D12Fence](https://msdn.microsoft.com/en-us/library/windows/desktop/dn899188(v=vs.85).aspx) -
`UINT64 Value`

: The value to signal the fence with when the GPU queue has finished processing any commands that have been queued prior to the signal.

In the next section, a function to wait until the fence is signaled with a particular value is described.

It is possible that the CPU thread will need to stall to wait for the GPU queue to finish executing commands that write to resources before being reused. For example, before reusing a swap chain’s back buffer resource, any commands that are using that resource as a render target must be complete before that back buffer resource can be reused. Any resources that are never used as a writeable target (for example material textures) do not need to be double buffered and do not require stalling the CPU thread before being reused as read-only resources in a shader. Writable resource such as render targets do need to be synchronized to protect the resource from being modified by multiple queues at the same time.

|
1
2
3
4
5
6
7
8
9
|
void WaitForFenceValue(ComPtr<ID3D12Fence> fence, uint64_t fenceValue, HANDLE fenceEvent,
std::chrono::milliseconds duration = std::chrono::milliseconds::max() )
{
if (fence->GetCompletedValue() < fenceValue)
{
ThrowIfFailed(fence->SetEventOnCompletion(fenceValue, fenceEvent));
::WaitForSingleObject(fenceEvent, static_cast<DWORD>(duration.count()));
}
}
|

The `WaitForFenceValue`

is used to stall the CPU thread if the fence has not yet reached (been signaled with) a specific value. The function will wait for a duration specified by the `duration`

parameter which by default has a duration of about 584 million years. It is advisable to provide the correct fence value to wait on otherwise the end-user will be waiting a long time for the application to continue processing.

The currently completed fence value is queried on line 440. If the fence has not yet reached that value, an event object is registered with the fence and is in turn signaled once the fence has reached the specified value.

It is sometimes useful to wait until all previously executed commands have finished executing before doing something (for example, resizing the swap chain buffers requires any references to the buffers to be released). For this, the `Flush`

function is used to ensure the GPU has finished processing all commands before continuing.

The `Flush`

function is used to ensure that any commands previously executed on the GPU have finished executing before the CPU thread is allowed to continue processing. This is useful for ensuring that any back buffer resources being referenced by a command that is currently “in-flight” on the GPU have finished executing before being resized. It is also strongly advisable to flush the GPU command queue before releasing any resources that might be referenced by a command list that is currently “in-flight” on the command queue (for example, before closing the application).

The `Flush`

function is simply a

followed by a [Signal](https://www.3dgep.com#Signal_the_Fence)

.[WaitForFenceValue](https://www.3dgep.com#Wait_for_Fence_Value)

|
1
2
3
4
5
6
|
void Flush(ComPtr<ID3D12CommandQueue> commandQueue, ComPtr<ID3D12Fence> fence,
uint64_t& fenceValue, HANDLE fenceEvent )
{
uint64_t fenceValueForSignal = Signal(commandQueue, fence, fenceValue);
WaitForFenceValue(fence, fenceValueForSignal, fenceEvent);
}
|

On line 450, the fence is signaled on the GPU. The

function returns the fence value to wait for. The [Signal](https://www.3dgep.com#Signal_the_Fence)

function is used to wait for the fence to be signaled with a specified value. The [WaitForFenceValue](https://www.3dgep.com#Wait_for_Fence_Value)`Flush`

function will block the calling thread until the fence value has been reached. After this function returns, it is safe to release any resources that were referenced by the GPU.

In the next sections, the `Update`

and `Render`

functions are described.

For this lesson, the `Update`

function is extremely simple. Its only purpose is to display the frame-rate each second in the debug output in Visual Studio.

First a few variables are declared and the time between subsequent calls to the `Update`

function is computed using a C++11 high-resolution clock.

|
1
2
3
4
5
6
7
8
9
10
11
|
void Update()
{
static uint64_t frameCounter = 0;
static double elapsedSeconds = 0.0;
static std::chrono::high_resolution_clock clock;
static auto t0 = clock.now();
frameCounter++;
auto t1 = clock.now();
auto deltaTime = t1 - t0;
t0 = t1;
|

The `frameCounter`

variable is used to keep track of the number of times the a frame was rendered to the screen since the last time the frame-rate was printed. The `elapsedSeconds`

variable stores the time in seconds since the last time the frame-rate was printed.

The `clock`

variable is a

which is used to sample time points ([high_resolution_clock](http://en.cppreference.com/w/cpp/chrono/high_resolution_clock)

).[std::chrono::time_point](http://en.cppreference.com/w/cpp/chrono/time_point)

The `t0`

variable is the initial point in time and is initialized to the current time.

Each frame, the `frameCounter`

variable is incremented and the delta time is computed on line 463.

On line 464, `t0`

is updated with the current time point to prepare it for the next frame.

|
1
2
3
4
5
6
7
8
9
10
11
12
|
elapsedSeconds += deltaTime.count() * 1e-9;
if (elapsedSeconds > 1.0)
{
char buffer[500];
auto fps = frameCounter / elapsedSeconds;
sprintf_s(buffer, 500, "FPS: %f\n", fps);
OutputDebugString(buffer);
frameCounter = 0;
elapsedSeconds = 0.0;
}
}
|

The `deltaTime`


variable stores the number of nanoseconds since the previous call to the [time_point](http://en.cppreference.com/w/cpp/chrono/time_point)`Update`

function. In order to convert the `deltaTime`

from nanoseconds into seconds, it is multiplied by \(1\times 10^{-9}\).

The frame-rate is printed to the debug output in Visual Studio only once per second. If the total elapsed time exceeds one second, then the frame-rate (in frames-per-second) is computed on line 470 and on line 472, it is printed to the debug output.

In order to compute the frame-rate for the next second, the `frameCounter`

and `elapsedSeconds`

variables are reset to 0.

Although this is a simple update function, it demonstrates how to create a simple game loop. See [Game Programming Patterns – Game Loop](http://gameprogrammingpatterns.com/game-loop.html) for more information.

In the next section, the `Render`

function is described.

For this simple application, the `Render`

function consists of two main parts:

- Clear the back buffer
- Present the rendered frame

In later lessons, the render loop will become more complicated.

In DirectX 12, it is the responsibility of the graphics programmer to ensure that resources are in the correct state before using them. Resources must be transitioned from one state to another using a **resource barrier** and inserting that resource barrier into the command list. For example, before you can use the swap chain’s back buffer as a render target, it must be transitioned to the

state and before it can be used for presenting the rendered image to the screen, it must be transitioned to the [RENDER_TARGET](https://msdn.microsoft.com/en-us/library/dn986744(v=vs.85).aspx#D3D12_RESOURCE_STATE_RENDER_TARGET)

state.[PRESENT](https://msdn.microsoft.com/en-us/library/dn986744(v=vs.85).aspx#D3D12_RESOURCE_STATE_PRESENT)

There are several types of resource barriers:

-
**Transition**: Transitions a (sub)resource to a particular state before using it. For example, before a texture can be used in a pixel shader, it must be transitioned to the

state.[PIXEL_SHADER_RESOURCE](https://msdn.microsoft.com/en-us/library/dn986744(v=vs.85).aspx#D3D12_RESOURCE_STATE_PIXEL_SHADER_RESOURCE) -
**Aliasing**: Specifies that a resource is used in a placed or reserved heap when that resource is aliased with another resource in the same heap. -
**UAV**: Indicates that all UAV accesses to a particular resource have completed before any future UAV access can begin. This is necessary when the UAV is transitioned for:-
**Read > Write**: Guarantees that all previous read operations on the UAV have completed before being written to in another shader. -
**Write > Read**: Guarantees that all previous write operations on the UAV have completed before being read from in another shader. -
**Write > Write**: Avoids race conditions that could be caused by different shaders in a different draw or dispatch trying to write to the same resource (does not avoid race conditions that could be caused in the same draw or dispatch call). - A UAV barrier is not needed if the resource is being used as a read-only (Read > Read) resource between draw or dispatches.

-

For this lesson, only **transition** resource barriers are used. In a later lesson more complex usages of resource barriers will be shown.

Before any commands can be recorded into the command list, the command allocator and command list needs to be reset to its initial state.

|
1
2
3
4
5
6
7
|
void Render()
{
auto commandAllocator = g_CommandAllocators[g_CurrentBackBufferIndex];
auto backBuffer = g_BackBuffers[g_CurrentBackBufferIndex];
commandAllocator->Reset();
g_CommandList->Reset(commandAllocator.Get(), nullptr);
|

On lines 481-482, pointers to the command allocator and back buffer resource are retrieved according to the current back buffer index.

On lines 484-485 the command allocator and command list are reset. This prepares the command list for recording the next frame.

Usually the first operation that is performed on a render target resource is a clear.

Before the render target can be cleared, it must be transitioned to the

state.[RENDER_TARGET](https://msdn.microsoft.com/en-us/library/dn986744(v=vs.85).aspx#D3D12_RESOURCE_STATE_RENDER_TARGET)

|
1
2
3
4
5
6
7
|
// Clear the render target.
{
CD3DX12_RESOURCE_BARRIER barrier = CD3DX12_RESOURCE_BARRIER::Transition(
backBuffer.Get(),
D3D12_RESOURCE_STATE_PRESENT, D3D12_RESOURCE_STATE_RENDER_TARGET);
g_CommandList->ResourceBarrier(1, &barrier);
|

The

structure is a helper struct that allows for easy initializing of the various resource barriers. In this case the [CD3DX12_RESOURCE_BARRIER](https://msdn.microsoft.com/en-us/library/mt604704(v=vs.85).aspx)

method is used create a transition resource barrier. By default, this will transition all subresources to the same state.[CD3DX12_RESOURCE_BARRIER::Transition](https://msdn.microsoft.com/en-us/library/mt604704(v=vs.85).aspx)

The resource transition must specify both the before and after states of the (sub)resource. This implies that the before state of the resource must be known. The state of the resource cannot be queried from the resource itself which implies that the application developer must track the last know state of the resource. In a single-threaded application, tracking the last known state of the resource is relatively easy task but if the state of the resource needs to be tracked across multiple parallel threads, then it can get complicated. Methods to track the state of resources will be investigated in another lesson. In this lesson, the before and after states of the resource are known so they are hard-coded in the transition barrier structures.

If there is more than a single resource barrier to insert into the command list, it is recommended to store all barriers in a list and execute them all at the same time before an operation that requires the resource to be in a particular state is executed. In this case, there is only one barrier. Since the next operation requires the resource to be in the

state, the resource barrier is inserted directly into the command list on line 493.[RENDER_TARGET](https://msdn.microsoft.com/en-us/library/dn986744(v=vs.85).aspx#D3D12_RESOURCE_STATE_RENDER_TARGET)

Now the back buffer can be cleared.

|
1
2
3
4
5
6
|
FLOAT clearColor[] = { 0.4f, 0.6f, 0.9f, 1.0f };
CD3DX12_CPU_DESCRIPTOR_HANDLE rtv(g_RTVDescriptorHeap->GetCPUDescriptorHandleForHeapStart(),
g_CurrentBackBufferIndex, g_RTVDescriptorSize);
g_CommandList->ClearRenderTargetView(rtv, clearColor, 0, nullptr);
}
|

To clear the back buffer, a CPU descriptor handle to a render target view is stored in the `rtv`

variable. The handle is offset from the beginning of the descriptor heap based on the current back buffer index and the size of the descriptor.

The render target is cleared using the

method which has the following signature [ID3D12GraphicsCommandList::ClearRenderTargetView](https://msdn.microsoft.com/en-us/library/dn903842(v=vs.85).aspx)[[31]](https://www.3dgep.com#cite-31):

|
1
2
3
4
5
6
|
void ClearRenderTargetView(
[in] D3D12_CPU_DESCRIPTOR_HANDLE RenderTargetView,
[in] const FLOAT ColorRGBA[4],
[in] UINT NumRects,
[in] const D3D12_RECT *pRects
);
|

And each parameter:

-

: Specifies a[D3D12_CPU_DESCRIPTOR_HANDLE](https://msdn.microsoft.com/en-us/library/dn859369(v=vs.85).aspx)RenderTargetView

structure that describes the CPU descriptor handle that represents the render target to be cleared.[D3D12_CPU_DESCRIPTOR_HANDLE](https://msdn.microsoft.com/en-us/library/dn859369(v=vs.85).aspx) -
`FLOAT ColorRGBA[4]`

: A 4-component array that represents the color to fill the render target with. -
`UINT NumRects`

: The number of rectangles in the array that the pRects parameter specifies. -

: An array of[D3D12_RECT](https://msdn.microsoft.com/en-us/library/dn879471(v=vs.85).aspx)*pRects

structures for the rectangles in the resource view to clear. If[D3D12_RECT](https://msdn.microsoft.com/en-us/library/dn879471(v=vs.85).aspx)`NULL`

,

clears the entire resource view.[ClearRenderTargetView](https://msdn.microsoft.com/en-us/library/dn903842(v=vs.85).aspx)

After rendering the scene, the current back buffer is presented to the screen.

The last operation performed during rendering is presenting the rendered image to the screen. Before presenting, the back buffer resource must be transitioned to the

state.[PRESENT](https://msdn.microsoft.com/en-us/library/dn986744(v=vs.85).aspx#D3D12_RESOURCE_STATE_PRESENT)

|
1
2
3
4
5
6
|
// Present
{
CD3DX12_RESOURCE_BARRIER barrier = CD3DX12_RESOURCE_BARRIER::Transition(
backBuffer.Get(),
D3D12_RESOURCE_STATE_RENDER_TARGET, D3D12_RESOURCE_STATE_PRESENT);
g_CommandList->ResourceBarrier(1, &barrier);
|

Resource transitions are explained in the previous sections and aren’t repeated here. After transitioning to the correct state, the command list that contains the resource transition barrier must be executed on the command queue.

|
1
2
3
4
5
6
|
ThrowIfFailed(g_CommandList->Close());
ID3D12CommandList* const commandLists[] = {
g_CommandList.Get()
};
g_CommandQueue->ExecuteCommandLists(_countof(commandLists), commandLists);
|

The command list is closed on line 509 using the

method. This method must be called on the command list before being executed on the command queue.[ID3D12GraphicsCommandList::Close](https://docs.microsoft.com/en-us/windows/desktop/api/d3d12/nf-d3d12-id3d12graphicscommandlist-close)

The command list is executed on the command queue using the

method which takes a list of command lists to be executed. [ID3D12CommandQueue::ExecuteCommandLists](https://msdn.microsoft.com/en-us/library/dn788631(v=vs.85).aspx)

|
1
2
3
4
5
|
UINT syncInterval = g_VSync ? 1 : 0;
UINT presentFlags = g_TearingSupported && !g_VSync ? DXGI_PRESENT_ALLOW_TEARING : 0;
ThrowIfFailed(g_SwapChain->Present(syncInterval, presentFlags));
g_FrameFenceValues[g_CurrentBackBufferIndex] = Signal(g_CommandQueue, g_Fence, g_FenceValue);
|

The swap chain’s current back buffer is presented to the screen using the

method. This method has the following signature [IDXGISwapChain::Present](https://msdn.microsoft.com/en-us/library/bb174576(v=vs.85).aspx)[[32]](https://www.3dgep.com#cite-32):

|
1
2
3
4
|
HRESULT Present(
UINT SyncInterval,
UINT Flags
);
|

Where

-
`UINT SyncInterval`

: An integer that specifies how to synchronize presentation of a frame with the vertical blank. Valid values are:-
`0`

: Cancel the remaining time on the previously presented frame and discard this frame if a newer frame is queued. -
`1`

through`4`

: Synchronize presentation for at least \(n\) vertical blanks.

-
-
`UINT Flags`

: An integer value that contains swap-chain presentation options. These options are defined by the

constants.[DXGI_PRESENT](https://msdn.microsoft.com/en-us/library/bb509554(v=vs.85).aspx)

If tearing is supported, it is recommended to always use the

flag when presenting with a sync interval of 0. The requirements for using the [DXGI_PRESENT_ALLOW_TEARING](https://msdn.microsoft.com/en-us/library/bb509554(v=vs.85).aspx#DXGI_PRESENT_ALLOW_TEARING)

flag when presenting are:[DXGI_PRESENT_ALLOW_TEARING](https://msdn.microsoft.com/en-us/library/bb509554(v=vs.85).aspx#DXGI_PRESENT_ALLOW_TEARING)

- The swap chain must be created with the

flag.[DXGI_SWAP_CHAIN_FLAG_ALLOW_TEARING](https://msdn.microsoft.com/en-us/library/bb173076(v=vs.85).aspx) - The sync interval passed into

(or[Present](https://msdn.microsoft.com/en-us/library/bb174576(v=vs.85).aspx)

) must be 0.[Present1](https://msdn.microsoft.com/en-us/library/hh446797(v=vs.85).aspx) - The

flag cannot be used in an application that is currently in full screen exclusive mode (set by calling[DXGI_PRESENT_ALLOW_TEARING](https://msdn.microsoft.com/en-us/library/bb509554(v=vs.85).aspx#DXGI_PRESENT_ALLOW_TEARING)

). It can only be used in windowed mode. To use this flag in full screen Win32 apps, the application should present to a fullscreen borderless window and disable automatic[SetFullscreenState](https://msdn.microsoft.com/en-us/library/bb174579(v=vs.85).aspx)(TRUE)`Alt`+`Enter`fullscreen switching using

.[IDXGIFactory::MakeWindowAssociation](https://msdn.microsoft.com/en-us/library/bb174540(v=vs.85).aspx)

Immediately after presenting the rendered frame to the screen, a signal is inserted into the queue using the

function described earlier. The fence value returned from the [Signal](https://www.3dgep.com#Signal_the_Fence)`Signal`

function is used to stall the CPU thread until any (writeable – such as render targets) resources are finished being used.

After signaling the command queue, the index of the current back buffer is updated.

|
1
2
3
4
5
|
g_CurrentBackBufferIndex = g_SwapChain->GetCurrentBackBufferIndex();
WaitForFenceValue(g_Fence, g_FrameFenceValues[g_CurrentBackBufferIndex], g_FenceEvent);
}
}
|

When using the

flip model, the order of back buffer indicies is not guaranteed to be sequential. The [DXGI_SWAP_EFFECT_FLIP_DISCARD](https://msdn.microsoft.com/en-us/library/windows/desktop/bb173077(v=vs.85).aspx)

method is used to get the index of the swap chain’s current back buffer.[IDXGISwapChain3::GetCurrentBackBufferIndex](https://msdn.microsoft.com/en-us/library/dn903675(v=vs.85).aspx)

Before overwriting the contents of the current back buffer with the content of the next frame, the CPU thread is stalled using the

function described earlier.[WaitForFenceValue](https://www.3dgep.com#Wait_for_Fence_Value)

In the next section window resizing and switching to full-screen mode is described.

A resize event is triggered when the window is created the first time. It is also triggered when switching to full-screen mode or if the user resizes the window by dragging the window border frame while in windowed mode. The `Resize`

function will resize the swap chain buffers if the client area of the window changes.

|
1
2
3
4
5
6
7
8
9
10
11
|
void Resize(uint32_t width, uint32_t height)
{
if (g_ClientWidth != width || g_ClientHeight != height)
{
// Don't allow 0 size swap chain back buffers.
g_ClientWidth = std::max(1u, width );
g_ClientHeight = std::max( 1u, height);
// Flush the GPU queue to make sure the swap chain's back buffers
// are not being referenced by an in-flight command list.
Flush(g_CommandQueue, g_Fence, g_FenceValue, g_FenceEvent);
|

In order to avoid superfluous resizes, the changes to the width and height of the client area are checked for changes. Any references to the swap chain’s back buffers need to be released before resizing the swap chain. Since there may be a command list that is “in-flight” on the GPU which references the swap chain’s back buffers, the GPU needs to be flushed using the

function described earlier.[Flush](https://www.3dgep.com#Flush_the_GPU)

|
1
2
3
4
5
6
7
|
for (int i = 0; i < g_NumFrames; ++i)
{
// Any references to the back buffers must be released
// before the swap chain can be resized.
g_BackBuffers[i].Reset();
g_FrameFenceValues[i] = g_FrameFenceValues[g_CurrentBackBufferIndex];
}
|

After flushing the GPU command queue, the local references to the swap chain’s back buffers are released on line 544. The per-frame fence values are also reset to the fence value of the current back buffer index.

|
1
2
3
4
5
6
7
8
9
10
|
DXGI_SWAP_CHAIN_DESC swapChainDesc = {};
ThrowIfFailed(g_SwapChain->GetDesc(&swapChainDesc));
ThrowIfFailed(g_SwapChain->ResizeBuffers(g_NumFrames, g_ClientWidth, g_ClientHeight,
swapChainDesc.BufferDesc.Format, swapChainDesc.Flags));
g_CurrentBackBufferIndex = g_SwapChain->GetCurrentBackBufferIndex();
UpdateRenderTargetViews(g_Device, g_SwapChain, g_RTVDescriptorHeap);
}
}
|

On line 549 the current swap chain description is queried so that the same color format and swap chain flags are used to recreate the swap chain buffers on line 550.

Since the index of back buffer may not be the same, it is important to update the current back buffer index as known by the application.

After the swap chain buffers have been resized, the descriptors that refer to those buffers needs to be updated. The RTV descriptors are updated on line 555 using the

method described earlier.[UpdateRenderTargetViews](https://www.3dgep.com#Create_the_Render_Target_Views)

In the next section, toggling between fullscreen and windowed state is described.

Since the swap chain’s swap effect is using a flip effect, it is not necessary for the window to obtain exclusive ownership of the screen in order to achieve maximum frame rates. Switching the back buffer to a full screen exclusive mode using the

method can be cumbersome and has the following drawbacks:[IDXGISwapChain::SetFullscreenState](https://msdn.microsoft.com/en-us/library/bb174579(v=vs.85).aspx)

- A

structure is required when creating the swap chain to switch to a full screen state.[DXGI_SWAP_CHAIN_FULLSCREEN_DESC](https://msdn.microsoft.com/en-us/library/hh404531(v=vs.85).aspx) - The resolution and refresh rate must match one of the supported modes of the monitor. Providing incorrect resolution or refresh rate settings may cause the screen to go black for the end user.
- Switching to full screen exclusive mode might cause any other monitors in a multi-monitor setup to turn black.
- The mouse cursor is locked to the full screen display.
- Switching to a full screen state will fail if the GPU that is rendering is is not directly connected to the display device. This is common in multi-GPU configurations (for example laptops with an integrated Intel graphics chip and a dedicated GPU).

To solve these issues with full screen exclusive mode, the window will be maximized using a **full screen borderless window** (**FSBW**) [[33]](https://www.3dgep.com#cite-33).

When using a full screen borderless window the window style is changed so that the window has no decorations (caption, minimize, maximize, close buttons, and frame). The window is then resized to the full screen dimensions of the nearest display. When using a multi-monitor setup, it is possible that the end user wants the game window to be on a different display other than the primary display. To facilitate this functionality, the window should be made full screen on the display that the application window is overlapping with the most. The nearest monitor relative to the application window can be queried using the

function. This function returns a handle to a monitor which can be used to query the monitor info using the [MonitorFromWindow](https://msdn.microsoft.com/en-us/library/dd145064(v=vs.85).aspx)

function.[GetMonitorInfo](https://msdn.microsoft.com/en-us/library/dd144901(v=vs.85).aspx)

The `SetFullscreen`

function is used to switch the window to a full screen borderless window.

|
1
2
3
4
5
6
7
8
9
10
11
|
void SetFullscreen(bool fullscreen)
{
if (g_Fullscreen != fullscreen)
{
g_Fullscreen = fullscreen;
if (g_Fullscreen) // Switching to fullscreen.
{
// Store the current window dimensions so they can be restored
// when switching out of fullscreen state.
::GetWindowRect(g_hWnd, &g_WindowRect);
|

Before switching to a full screen state, the window rectangle is saved using the

function so that the window can be restored when switching back to windowed mode.[GetWindowRect](https://msdn.microsoft.com/en-us/library/ms633519(v=vs.85).aspx)

Next, the window style is changed to a borderless window.

|
1
2
3
4
5
|
// Set the window style to a borderless window so the client area fills
// the entire screen.
UINT windowStyle = WS_OVERLAPPEDWINDOW & ~(WS_CAPTION | WS_SYSMENU | WS_THICKFRAME | WS_MINIMIZEBOX | WS_MAXIMIZEBOX);
::SetWindowLongW(g_hWnd, GWL_STYLE, windowStyle);
|

The

function is used to set the borderless window style.[SetWindowLong](https://msdn.microsoft.com/en-us/library/ms633591(v=vs.85).aspx)

**0**, unsetting every bit specified in the

[WS_OVERLAPPEDWINDOW](https://msdn.microsoft.com/en-us/library/ms632600(v=vs.85).aspx#WS_OVERLAPPEDWINDOW)

constant. This code is explicitly removing all decorators on the window.In the next step, the dimensions of the nearest monitor to the application window is queried.

|
1
2
3
4
5
6
7
|
// Query the name of the nearest display device for the window.
// This is required to set the fullscreen dimensions of the window
// when using a multi-monitor setup.
HMONITOR hMonitor = ::MonitorFromWindow(g_hWnd, MONITOR_DEFAULTTONEAREST);
MONITORINFOEX monitorInfo = {};
monitorInfo.cbSize = sizeof(MONITORINFOEX);
::GetMonitorInfo(hMonitor, &monitorInfo);
|

The

function is used to retrieve a handle to the monitor that is nearest the window for the application.[MonitorFromWindow](https://msdn.microsoft.com/en-us/library/dd145064(v=vs.85).aspx)

The properties for the monitor are queried using the

function. The structure returned from the [GetMonitorInfo](https://msdn.microsoft.com/en-us/library/dd144901(v=vs.85).aspx)

function contains a rectangle structure that describes the full screen rectangle for the monitor.[GetMonitorInfo](https://msdn.microsoft.com/en-us/library/dd144901(v=vs.85).aspx)

|
1
2
3
4
5
6
7
8
9
|
::SetWindowPos(g_hWnd, HWND_TOP,
monitorInfo.rcMonitor.left,
monitorInfo.rcMonitor.top,
monitorInfo.rcMonitor.right - monitorInfo.rcMonitor.left,
monitorInfo.rcMonitor.bottom - monitorInfo.rcMonitor.top,
SWP_FRAMECHANGED | SWP_NOACTIVATE);
::ShowWindow(g_hWnd, SW_MAXIMIZE);
}
|

The

function is used to change the position, size and z-order (make sure it is above all other visible windows) of the window. This function has the following signature [SetWindowPos](https://msdn.microsoft.com/en-us/library/ms633545(v=vs.85).aspx)[[34]](https://www.3dgep.com#cite-34):

|
1
2
3
4
5
6
7
8
9
|
BOOL WINAPI SetWindowPos(
_In_ HWND hWnd,
_In_opt_ HWND hWndInsertAfter,
_In_ int X,
_In_ int Y,
_In_ int cx,
_In_ int cy,
_In_ UINT uFlags
);
|

Where

-
`HWND hWnd`

: A handle to the window. -
`HWND hWndInsertAfter`

: A handle to the window to precede the positioned window in the Z order. This parameter must be a window handle or one of the following values:-

: Places the window at the bottom of the Z order. If the hWnd parameter identifies a topmost window, the window loses its topmost status and is placed at the bottom of all other windows.[HWND_BOTTOM](https://msdn.microsoft.com/en-us/library/ms633545(v=vs.85).aspx#HWND_BOTTOM) -

: Places the window above all non-topmost windows (that is, behind all topmost windows). This flag has no effect if the window is already a non-topmost window.[HWND_NOTOPMOST](https://msdn.microsoft.com/en-us/library/ms633545(v=vs.85).aspx#HWND_NOTOPMOST) -

: Places the window at the top of the Z order.[HWND_TOP](https://msdn.microsoft.com/en-us/library/ms633545(v=vs.85).aspx#HWND_TOP) -

: Places the window above all non-topmost windows. The window maintains its topmost position even when it is deactivated.[HWND_TOPMOST](https://msdn.microsoft.com/en-us/library/ms633545(v=vs.85).aspx#HWND_TOPMOST)

-
-
`int X`

: The new position of the left side of the window, in client coordinates. -
`int Y`

: The new position of the top of the window, in client coordinates. -
`int cx`

: The new width of the window, in pixels. -
`int cy`

: The new height of the window, in pixels. -
`UINT uFlags`

: The window sizing and positioning flags. In this case, the following values are specified.-

: Applies new frame styles set using the[SWP_FRAMECHANGED](https://msdn.microsoft.com/en-us/library/ms633545(v=vs.85).aspx#SWP_FRAMECHANGED)

function. Sends a[SetWindowLong](https://msdn.microsoft.com/en-us/library/ms633591(v=vs.85).aspx)

message to the window, even if the window’s size is not being changed. If this flag is not specified,[WM_NCCALCSIZE](https://msdn.microsoft.com/en-us/library/ms632634(v=vs.85).aspx)

is sent only when the window’s size is being changed.[WM_NCCALCSIZE](https://msdn.microsoft.com/en-us/library/ms632634(v=vs.85).aspx) -

: Does not activate the window. If this flag is not set, the window is activated and moved to the top of either the topmost or non-topmost group (depending on the setting of the[SWP_NOACTIVATE](https://msdn.microsoft.com/en-us/library/ms633545(v=vs.85).aspx#SWP_NOACTIVATE)`hWndInsertAfter`

parameter).

-

The

function is used on line 592 to show the window in a maximized state.[ShowWindow](https://msdn.microsoft.com/en-us/library/ms633548(v=vs.85).aspx)

|
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
|
else
{
// Restore all the window decorators.
::SetWindowLong(g_hWnd, GWL_STYLE, WS_OVERLAPPEDWINDOW);
::SetWindowPos(g_hWnd, HWND_NOTOPMOST,
g_WindowRect.left,
g_WindowRect.top,
g_WindowRect.right - g_WindowRect.left,
g_WindowRect.bottom - g_WindowRect.top,
SWP_FRAMECHANGED | SWP_NOACTIVATE);
::ShowWindow(g_hWnd, SW_NORMAL);
}
}
}
|

If the window is being restored to a windowed state the window style is changed back to the

window style and the size and postion of the window is restored to its windowed size. The [WS_OVERLAPPEDWINDOW](https://msdn.microsoft.com/en-us/library/ms632600(v=vs.85).aspx#WS_OVERLAPPEDWINDOW)

function is used again on line 606 to activate and display the window normally.[ShowWindow](https://msdn.microsoft.com/en-us/library/ms633548(v=vs.85).aspx)

The only thing left to do is to define how the window reacts to window messages (such as key presses and resize events) and to put it all together with the main application glue.

The window message procedure is the `WndProc`

function described next. The window procedure handles any window messages sent to the application. For this simple demo, the following messages are handled:

-

: Repaint a portion of the application’s window contents.[WM_PAINT](https://msdn.microsoft.com/en-us/library/dd145213(v=vs.85).aspx) -

,[WM_SYSKEYDOWN](https://msdn.microsoft.com/en-us/library/ms646286(v=vs.85).aspx)

, and[WM_KEYDOWN](https://msdn.microsoft.com/en-us/library/ms646280(v=vs.85).aspx)

: Sent to the window with keybaord focus when a key is pressed on the keyboard.[WM_SYSCHAR](https://msdn.microsoft.com/en-us/library/ms646357(v=vs.85).aspx) -

: Sent to the window after its size has changed.[WM_SIZE](https://msdn.microsoft.com/en-us/library/ms632646(v=vs.85).aspx)

The

message handler is shown first.[WM_PAINT](https://msdn.microsoft.com/en-us/library/dd145213(v=vs.85).aspx)

|
1
2
3
4
5
6
7
8
9
10
|
LRESULT CALLBACK WndProc(HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam)
{
if ( g_IsInitialized )
{
switch (message)
{
case WM_PAINT:
Update();
Render();
break;
|

In order to prevent the application from handling events before the necessary DirectX 12 objects are created, the `g_IsInitialized`

flag is checked. This flag is set to `true`

in the initialization function after all of the required assets have been loaded. Trying to resize or render the screen before the swap chain, command list and command allocators have been created would be disastrous.

When the

message is sent to the window procedure, the [WM_PAINT](https://msdn.microsoft.com/en-us/library/dd145213(v=vs.85).aspx)

and [Update](https://www.3dgep.com#Update)

functions described earlier are invoked.[Render](https://www.3dgep.com#Render)

This

message handler does not call the [WM_PAINT](https://msdn.microsoft.com/en-us/library/dd145213(v=vs.85).aspx)

and [BeginPaint](https://msdn.microsoft.com/en-us/library/dd183362(v=vs.85).aspx)

as doing so would prevent the [EndPaint](https://msdn.microsoft.com/en-us/library/dd162598(v=vs.85).aspx)

message from being called unless the window is resized, or partially occluded by another window. The [WM_PAINT](https://msdn.microsoft.com/en-us/library/dd145213(v=vs.85).aspx)

message should be sent to the window as often as possible and it will also be invoked while the window is being resized or moved (instead of blocking until the end user releases the mouse button).[WM_PAINT](https://msdn.microsoft.com/en-us/library/dd145213(v=vs.85).aspx)

Next a few keyboard keys are handled.

|
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
|
case WM_SYSKEYDOWN:
case WM_KEYDOWN:
{
bool alt = (::GetAsyncKeyState(VK_MENU) & 0x8000) != 0;
switch (wParam)
{
case 'V':
g_VSync = !g_VSync;
break;
case VK_ESCAPE:
::PostQuitMessage(0);
break;
case VK_RETURN:
if ( alt )
{
case VK_F11:
SetFullscreen(!g_Fullscreen);
}
break;
}
}
break;
// The default window procedure will play a system notification sound
// when pressing the Alt+Enter keyboard combination if this message is
// not handled.
case WM_SYSCHAR:
break;
|

The

message is sent to the window procedure function when the [WM_SYSKEYDOWN](https://msdn.microsoft.com/en-us/library/ms646286(v=vs.85).aspx)`Alt` key is held while pressing another key combination (for example, `Alt`+`Enter`). The

message is sent when any non-system key is pressed (a key is pressed without [WM_KEYDOWN](https://msdn.microsoft.com/en-us/library/ms646280(v=vs.85).aspx)`Alt` being held down).

The demo application handles the following keys:

| Key | Action |
|---|---|
V |
Toggle V-Sync. |
Esc |
Exit the application. |
Alt+Enter, F11
|
Toggle fullscreen mode. |

On line 647 the

message is also being handled but nothing is done with it. The [WM_SYSCHAR](https://msdn.microsoft.com/en-us/library/ms646357(v=vs.85).aspx)

message is posted to the window when a [WM_SYSCHAR](https://msdn.microsoft.com/en-us/library/ms646357(v=vs.85).aspx)

message is translated by the [WM_SYSKEYDOWN](https://msdn.microsoft.com/en-us/library/ms646286(v=vs.85).aspx)

function. If the [TranslateMessage](https://msdn.microsoft.com/en-us/library/ms644955(v=vs.85).aspx)

message is not handled then the default window procedure will handle it and play an annoying system notification sound when pressing [WM_SYSCHAR](https://msdn.microsoft.com/en-us/library/ms646357(v=vs.85).aspx)`Alt`+`Enter` while the window has keyboard focus.

The

message is handled next.[WM_SIZE](https://msdn.microsoft.com/en-us/library/ms632646(v=vs.85).aspx)

|
1
2
3
4
5
6
7
8
9
10
11
|
case WM_SIZE:
{
RECT clientRect = {};
::GetClientRect(g_hWnd, &clientRect);
int width = clientRect.right - clientRect.left;
int height = clientRect.bottom - clientRect.top;
Resize(width, height);
}
break;
|

The client area of the window is queried using the

function. The client rectangle is used to compute the width and height to resize the swap chain buffers.[GetClientRect](https://msdn.microsoft.com/en-us/library/ms633503(v=vs.85).aspx)

If the user clicks the ✖ in the top-right corner of the window, the

message is sent to the window. Not responding to this message could cause the application instance to never quit.[WM_DESTROY](https://msdn.microsoft.com/en-us/library/ms632620(v=vs.85).aspx)

|
1
2
3
4
5
6
7
8
9
10
11
12
13
14
|
case WM_DESTROY:
::PostQuitMessage(0);
break;
default:
return ::DefWindowProcW(hwnd, message, wParam, lParam);
}
}
else
{
return ::DefWindowProcW(hwnd, message, wParam, lParam);
}
return 0;
}
|

Clicking the ✖ in the top-right corner of the window will cause the

message to be sent to the window procedure. Since the application creates only a single window, the [WM_DESTROY](https://msdn.microsoft.com/en-us/library/ms632620(v=vs.85).aspx)

message is sent using the [WM_QUIT](https://msdn.microsoft.com/en-us/library/ms632641(v=vs.85).aspx)

method which will cause the application to terminate. The message loop for the application is shown in the next section.[PostQuitMessage](https://msdn.microsoft.com/en-us/library/ms644945(v=vs.85).aspx)

If another windows message is sent other than one of the messages handled in the window procedure described here or the application is not yet initialized, the message is handled by the default window procedure

.[DefWindowProc](https://msdn.microsoft.com/en-us/library/ms633572(v=vs.85).aspx)

The final function to be described in this lesson is the glue that puts it all together; the main entry point.

The main entry point for Win32 applications is the

function. This function acts as the glue for all of the functions previously shown in this lesson. All of the functions described previously are utilized to create the basis of a functioning DirectX 12 application. The function begins by setting some context for the application and reads the command-line arguments.[wWinMain](https://msdn.microsoft.com/en-us/library/ff381406(v=vs.85).aspx)

|
1
2
3
4
5
6
7
8
9
10
11
|
int CALLBACK wWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, PWSTR lpCmdLine, int nCmdShow)
{
// Windows 10 Creators update adds Per Monitor V2 DPI awareness context.
// Using this awareness context allows the client area of the window
// to achieve 100% scaling while still allowing non-client window content to
// be rendered in a DPI sensitive fashion.
SetThreadDpiAwarenessContext(DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2);
// Window class name. Used for registering / creating the window.
const wchar_t* windowClassName = L"DX12WindowClass";
ParseCommandLineArguments();
|

The

function sets the DPI awareness for the current thread. The [SetThreadDpiAwarenessContext](https://msdn.microsoft.com/en-us/library/mt748629(v=vs.85).aspx)

is an improved per-monitor DPI awarenes mode which provides new DPI-related scaling behaviours on a per top-level window basis [DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2](https://msdn.microsoft.com/library/mt791579(v=vs.85).aspx#DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2)[[35]](https://www.3dgep.com#cite-35). Using this DPI awareness mode, the application is able to achieve 100% pixel scaling for the client area of the window while still allowing for DPI scaling for non-client areas (such as the title bar and menus). This means that the swap chain buffers will be resized to fill the total number of screen pixels (true 4K or 8K resolutions) when resizing the client area of the window instead of scaling the client area based on the DPI scaling settings.

For example, if you have a 4K UHD (3840×2160 or 2160p) monitor and you have configured your DPI scaling to 150% then the default behaviour would be to size the client area to 2560×1440. Specifying the DPI awareness of the application before creating the window fixes this issue while still allowing for DPI scaling on non-client areas (for example the title bar of the window will still be scaled according to the DPI settings).

The window class name used to register and create an instance of the window class for the application is specified on line 684 and the command-line arguments are parsed on line 685 using the

function described earlier.[ParseCommandLineArguments](https://www.3dgep.com#Parse_Command-line_Arguments)

Before doing anything DirectX related, it is highly advisable to enable the debug layer.

|
1 |
EnableDebugLayer();
|

The DirectX debug layer is enabled on line 686 using the

function described previously. Attempting to enable the debug layer after the Direct3D 12 device context has been created will cause the device to be released.[EnableDebugLayer](https://www.3dgep.com#Enable_the_Direct3D_12_Debug_Layer)

|
1
2
3
4
5
6
7
8
|
g_TearingSupported = CheckTearingSupport();
RegisterWindowClass(hInstance, windowClassName);
g_hWnd = CreateWindow(windowClassName, hInstance, L"Learning DirectX 12",
g_ClientWidth, g_ClientHeight);
// Initialize the global window rect variable.
::GetWindowRect(g_hWnd, &g_WindowRect);
|

The tearing support for the application is queried on line 688 using the

function described earlier.[CheckTearingSupport](https://www.3dgep.com#Check_for_Tearing_Support)

On line 690 the window class is registered with the application instance and a window is created on lin 691 using the

function described earlier.[CreateWindow](https://www.3dgep.com#Create_Window_Instance)

On line 695 the window rectangle is queried to prepare the

variable for toggling the full screen state of the window.**g_WindowRect**

Next the DirectX 12 objects are created.

|
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
|
ComPtr<IDXGIAdapter4> dxgiAdapter4 = GetAdapter(g_UseWarp);
g_Device = CreateDevice(dxgiAdapter4);
g_CommandQueue = CreateCommandQueue(g_Device, D3D12_COMMAND_LIST_TYPE_DIRECT);
g_SwapChain = CreateSwapChain(g_hWnd, g_CommandQueue,
g_ClientWidth, g_ClientHeight, g_NumFrames);
g_CurrentBackBufferIndex = g_SwapChain->GetCurrentBackBufferIndex();
g_RTVDescriptorHeap = CreateDescriptorHeap(g_Device, D3D12_DESCRIPTOR_HEAP_TYPE_RTV, g_NumFrames);
g_RTVDescriptorSize = g_Device->GetDescriptorHandleIncrementSize(D3D12_DESCRIPTOR_HEAP_TYPE_RTV);
UpdateRenderTargetViews(g_Device, g_SwapChain, g_RTVDescriptorHeap);
|

On line 697 the

object is created using the [DXGIAdapter](https://msdn.microsoft.com/en-us/library/mt825229(v=vs.85).aspx)

function described earlier. The adapter is passed to the [GetAdapter](https://www.3dgep.com#Query_DirectX_12_Adapter)

function to create the [CreateDevice](https://www.3dgep.com#Create_the_DirectX_12_Device)[ID3D12Device](https://msdn.microsoft.com/en-us/library/mt492652(v=vs.85).aspx) object.

The direct command queue is created on line 701 and the swap chain is created on line 703.

The `g_CurrentBackBufferIndex`

is initialized on line 706. The first back buffer index will very likely be 0 but to be sure it is queried directly from the swap chain instead of making assumptions about the current back buffer index.

On line 708 the RTV descriptor heap is created using the

function described earlier and the RTV descriptor increment size is queried from the device on line 709.[CreateDescriptorHeap](https://www.3dgep.com#Create_a_Descriptor_Heap)

On line 711 the render target views are fill into the descriptor heap using the

function described earlier.[UpdateRenderTargetViews](https://www.3dgep.com#Create_the_Render_Target_Views)

The command list and command allocators are created next.

|
1
2
3
4
5
6
|
for (int i = 0; i < g_NumFrames; ++i)
{
g_CommandAllocators[i] = CreateCommandAllocator(g_Device, D3D12_COMMAND_LIST_TYPE_DIRECT);
}
g_CommandList = CreateCommandList(g_Device,
g_CommandAllocators[g_CurrentBackBufferIndex], D3D12_COMMAND_LIST_TYPE_DIRECT);
|

Since there needs to be at least as many allocators as in-flight render frames, an allocator is created for the each frame (number of swap chain back buffers). However since a single command list is used to record all rendering commands for this simple demo, only a single command list is required. The allocator is created using the

function described earlier and the command list is created using the [CreateCommandAllocator](https://www.3dgep.com#Create_a_Command_Allocator)

function.[CreateCommandList](https://www.3dgep.com#Create_a_Command_List)

The fence and fence event objects are created next.

|
1
2
|
g_Fence = CreateFence(g_Device);
g_FenceEvent = CreateEventHandle();
|

The fence object used to perform GPU synchronization is created on line 720 using the

function and the event handle used to block the CPU until a specific fence value has been reached is created on line 721 using the [CreateFence](https://www.3dgep.com#Create_a_Fence)

function described earlier.[CreateEventHandle](https://www.3dgep.com#Create_an_Event)

Everything needed to run the application is now initialized. It is safe to show the window and enter the application’s message loop.

|
1
2
3
4
5
6
7
8
9
10
11
12
13
|
g_IsInitialized = true;
::ShowWindow(g_hWnd, SW_SHOW);
MSG msg = {};
while (msg.message != WM_QUIT)
{
if (::PeekMessage(&msg, NULL, 0, 0, PM_REMOVE))
{
::TranslateMessage(&msg);
::DispatchMessage(&msg);
}
}
|

After everything is initialized, the `g_IsInitialized`

flag is set to true and on line 725 the window is shown using the

function.[ShowWindow](https://msdn.microsoft.com/en-us/library/ms633548(v=vs.85).aspx)

The message loop on lines 728-735 is a standard message loop for a windows application. Messages are dispatched to the window procedure (the

function described earlier) until the [WndProc](https://www.3dgep.com#Window_Message_Procedure)

message is posted to the message queue using the [WM_QUIT](https://msdn.microsoft.com/en-us/library/ms632641(v=vs.85).aspx)

function (this happens on line 632 of the [PostQuitMessage](https://msdn.microsoft.com/en-us/library/ms644945(v=vs.85).aspx)

function).[WndProc](https://www.3dgep.com#Window_Message_Procedure)

Before the application process can terminate, it is important to flush any pending command lists on the GPU.

|
1
2
3
4
5
6
7
|
// Make sure the command queue has finished all commands before closing.
Flush(g_CommandQueue, g_Fence, g_FenceValue, g_FenceEvent);
::CloseHandle(g_FenceEvent);
return 0;
}
|

The

function is used on line 738 to ensure that any pending command lists have finished executing before exiting the application. It is important to make sure that any resources that may currently be “in-flight” on the GPU have finished processing before they are released. Since all DirectX 12 objects are held by [Flush](https://www.3dgep.com#Flush_the_GPU)

‘s, they will automatically be cleaned up when the application exits but this cleanup should not occur until the GPU is no longer using them.[ComPtr](https://msdn.microsoft.com/en-us/library/br244983.aspx)

On line 740 the handle to the fence event object is released using the

function.[CloseHandle](https://msdn.microsoft.com/en-us/library/ms724211(v=vs.85).aspx)

And finally, the value 0 is returned to indicate that no errors occurred.

If everything is working correctly, you should see a window that is cleared with cornflower blue.

I know it’s not very exciting yet. In the next lesson, we’ll add some geometry to the scene.

In this lesson you learned a little bit about the history of DirectX, the various components of the DirectX API and you learned about the various stages of the rendering pipeline. You also learned how to initialize a DirectX 12 application. You learned how to perform correct synchronization of the GPU command queue that is required to perform double-buffered rendering in DirectX 12. You learned how to register and create and window using the Windows (Win32) API and you also learned how to query for DirectX 12 compatible GPU adapters, create a Direct3D 12 device and how to create a swap chain that is associated with the window. You also learned about descriptor heaps, and how to create a render target view in that heap. Additionally, you learned how to use the command allocators and the command list to clear a render target using a clear color. You also learned how to present the rendered image to the screen taking advantage of variable refresh-rate displays. You also learned how to switch to a full screen state using a full screen borderless window (FSBW) taking into consideration the nearest display relative to the application window. You also learned how to handle a few messages using the windows procedure function and finally the application was put together in the main entry point of the application.

Phew! That was a lot of learning but this is only the tip of the iceberg! In future lessons you will learn how to load vertices and indices into index and vertex buffers, how to write and load shader programs, perform basic lighting equations in a pixel shader, and how to perform HDR rendering! So much more to learn… So stay tuned for the next lessons!

If you enjoyed this lesson (or even if you didn’t) please feel free to leave a comment and let me know how I can improve!

The source code for this lesson is available on GitHub:

[[1] S. Meyers, Effective C++, 2nd ed. Indianapolis, IN: Addison-Wesley, 1998.]

[[2] S. Meyers, Effective Modern C++: 42 Specific Ways to Improve Your Use of C++11 and C++14, 1st ed. O’Reilly Media, 2014.]

[[3] Microsoft, “Learn to Develop with Microsoft Developer Network | MSDN”, Microsoft Developer Network, 2017. [Online]. Available: ][https://msdn.microsoft.com](https://msdn.microsoft.com). [Accessed: 13- Sep- 2017].

[[4] E. Gamma, R. Helm, R. Johnson and J. Vlissides, Design Patterns: Elements of Reusable Object-Oriented Software. Pearson Education, 1994.]

[[5] Boost, “Boost C++ Libraries”, Boost.org, 2017. [Online]. Available: ][http://www.boost.org/](http://www.boost.org/). [Accessed: 14- Sep- 2017].

[[6] Wikipedia, “DirectX”, en.wikipedia.org, 2017. [Online]. Available: ][https://en.wikipedia.org/wiki/DirectX](https://en.wikipedia.org/wiki/DirectX). [Accessed: 31- Oct- 2017].

[[7] Wikipedia, “Direct3D”, en.wikipedia.org, 2017. [Online]. Available: ][https://en.wikipedia.org/wiki/Direct3D](https://en.wikipedia.org/wiki/Direct3D). [Accessed: 31- Oct- 2017].

[[8] C. Eisler, “DirectX Then and Now (Part 1)”, Craig’s Musings, 2006. [Online]. Available: ][http://craig.theeislers.com/2006/02/20/directx-then-and-now-part-1/](http://craig.theeislers.com/2006/02/20/directx-then-and-now-part-1/). [Accessed: 01- Nov- 2017].

[[9] Microsoft, “Shader Model 1 (Windows)”, MSDN, 2017. [Online]. Available: ][https://msdn.microsoft.com/en-us/library/windows/desktop/bb509654(v=vs.85).aspx](https://msdn.microsoft.com/en-us/library/windows/desktop/bb509654(v=vs.85).aspx). [Accessed: 01- Nov- 2017].

[[10] Microsoft, “Shader Model 4 (Windows)”, MSDN, 2017. [Online]. Available: ][https://msdn.microsoft.com/en-us/library/windows/desktop/bb509657(v=vs.85).aspx](https://msdn.microsoft.com/en-us/library/windows/desktop/bb509657(v=vs.85).aspx). [Accessed: 01- Nov- 2017].

[[11] Microsoft, “HLSL Shader Model 6.0 (Windows)”, Msdn.microsoft.com, 2017. [Online]. Available: ][https://msdn.microsoft.com/en-us/library/windows/desktop/mt733232(v=vs.85).aspx](https://msdn.microsoft.com/en-us/library/windows/desktop/mt733232(v=vs.85).aspx). [Accessed: 10- Nov- 2017].

[[12] Microsoft, “DirectX Graphics and Gaming (Windows)”, Msdn.microsoft.com, 2017. [Online]. Available: ][https://msdn.microsoft.com/en-us/library/windows/desktop/ee663274(v=vs.85).aspx](https://msdn.microsoft.com/en-us/library/windows/desktop/ee663274(v=vs.85).aspx). [Accessed: 10- Nov- 2017].

[[13] Microsoft, “Pipelines and Shaders with Direct3D 12 (Windows)”, Msdn.microsoft.com, 2017. [Online]. Available: ][https://msdn.microsoft.com/en-us/library/windows/desktop/dn899200(v=vs.85).aspx](https://msdn.microsoft.com/en-us/library/windows/desktop/dn899200(v=vs.85).aspx). [Accessed: 10- Nov- 2017].

[[14] Microsoft, “Tessellation Stages (Windows)”, Msdn.microsoft.com, 2017. [Online]. Available: ][https://msdn.microsoft.com/en-us/library/windows/desktop/ff476340(v=vs.85).aspx](https://msdn.microsoft.com/en-us/library/windows/desktop/ff476340(v=vs.85).aspx). [Accessed: 10- Nov- 2017].

[[15] Microsoft, “Shader Stages (Windows)”, Msdn.microsoft.com, 2017. [Online]. Available: ][https://msdn.microsoft.com/en-us/library/windows/desktop/bb205146(v=vs.85).aspx](https://msdn.microsoft.com/en-us/library/windows/desktop/bb205146(v=vs.85).aspx). [Accessed: 10- Nov- 2017].

[[16] Microsoft, “DirectXMath (Windows)”, Msdn.microsoft.com, 2017. [Online]. Available: ][https://msdn.microsoft.com/en-us/library/windows/desktop/hh437833(v=vs.85).aspx](https://msdn.microsoft.com/en-us/library/windows/desktop/hh437833(v=vs.85).aspx). [Accessed: 20- Nov- 2017].

[[17] Microsoft, “WNDCLASSEX structure (Windows)”, Msdn.microsoft.com, 2017. [Online]. Available: ][https://msdn.microsoft.com/en-us/library/ms633577(v=vs.85).aspx](https://msdn.microsoft.com/en-us/library/ms633577(v=vs.85).aspx). [Accessed: 22- Nov- 2017].

[[18] Microsoft, “CreateWindowEx function (Windows)”, Msdn.microsoft.com, 2017. [Online]. Available: ][https://msdn.microsoft.com/en-us/library/ms632680(v=vs.85).aspx](https://msdn.microsoft.com/en-us/library/ms632680(v=vs.85).aspx). [Accessed: 24- Nov- 2017].

[[19] Microsoft, “Variable refresh rate displays (Windows)”, Msdn.microsoft.com, 2017. [Online]. Available: ][https://msdn.microsoft.com/en-us/library/windows/desktop/mt742104(v=vs.85).aspx](https://msdn.microsoft.com/en-us/library/windows/desktop/mt742104(v=vs.85).aspx). [Accessed: 24- Nov- 2017].

[[20] Microsoft, “DXGI flip model (Windows)”, Msdn.microsoft.com, 2017. [Online]. Available: ][https://msdn.microsoft.com/en-us/library/windows/desktop/hh706346(v=vs.85).aspx](https://msdn.microsoft.com/en-us/library/windows/desktop/hh706346(v=vs.85).aspx). [Accessed: 27- Nov- 2017].

[[21] Microsoft, “DXGI_SWAP_EFFECT enumeration (Windows)”, Msdn.microsoft.com, 2017. [Online]. Available: ][https://msdn.microsoft.com/en-us/library/windows/desktop/bb173077(v=vs.85).aspx](https://msdn.microsoft.com/en-us/library/windows/desktop/bb173077(v=vs.85).aspx). [Accessed: 27- Nov- 2017].

[[22] Microsoft, “DXGI_SWAP_CHAIN_DESC1 structure (Windows)”, Msdn.microsoft.com, 2017. [Online]. Available: ][https://msdn.microsoft.com/en-us/library/hh404528(v=vs.85).aspx](https://msdn.microsoft.com/en-us/library/hh404528(v=vs.85).aspx). [Accessed: 27- Nov- 2017].

[[23] Microsoft, “IDXGIFactory2::CreateSwapChainForHwnd method (Windows)”, Msdn.microsoft.com, 2017. [Online]. Available: ][https://msdn.microsoft.com/en-us/library/hh404557(v=vs.85).aspx](https://msdn.microsoft.com/en-us/library/hh404557(v=vs.85).aspx). [Accessed: 27- Nov- 2017].

[[24] Microsoft, “D3D12_DESCRIPTOR_HEAP_DESC structure (Windows)”, Msdn.microsoft.com, 2017. [Online]. Available: ][https://msdn.microsoft.com/en-us/library/dn770359(v=vs.85).aspx](https://msdn.microsoft.com/en-us/library/dn770359(v=vs.85).aspx). [Accessed: 28- Nov- 2017].

[[25] Microsoft, “ID3D12Device::CreateCommandAllocator method (Windows)”, Msdn.microsoft.com, 2017. [Online]. Available: ][https://msdn.microsoft.com/en-us/library/dn788655(v=vs.85).aspx](https://msdn.microsoft.com/en-us/library/dn788655(v=vs.85).aspx). [Accessed: 29- Nov- 2017].

[[26] Microsoft, “ID3D12Device::CreateCommandList method (Windows)”, Msdn.microsoft.com, 2017. [Online]. Available: ][https://msdn.microsoft.com/en-us/library/dn788656(v=vs.85).aspx](https://msdn.microsoft.com/en-us/library/dn788656(v=vs.85).aspx). [Accessed: 29- Nov- 2017].

[[27] Microsoft, “ID3D12Device::CreateFence method (Windows)”, Msdn.microsoft.com, 2017. [Online]. Available: https://msdn.microsoft.com/en-us/library/dn899179(v=vs.85).aspx. [Accessed: 30- Nov- 2017].]

[[28] Microsoft, “CreateEvent function (Windows)”, Msdn.microsoft.com, 2017. [Online]. Available: ][https://msdn.microsoft.com/en-us/library/ms682396(v=vs.85).aspx](https://msdn.microsoft.com/en-us/library/ms682396(v=vs.85).aspx). [Accessed: 30- Nov- 2017].

[[29] Microsoft, “ID3D12CommandQueue::Signal method (Windows)”, Msdn.microsoft.com, 2017. [Online]. Available: ][https://msdn.microsoft.com/en-us/library/windows/desktop/dn899171(v=vs.85).aspx](https://msdn.microsoft.com/en-us/library/windows/desktop/dn899171(v=vs.85).aspx). [Accessed: 30- Nov- 2017].

[[30] R. Nystrom, Game programming patterns. [Lieu de publication inconnu]: Genever Benning, 2014.]

[[31] Microsoft, “ID3D12GraphicsCommandList::ClearRenderTargetView method (Windows)”, Msdn.microsoft.com, 2017. [Online]. Available: ][https://msdn.microsoft.com/en-us/library/dn903842(v=vs.85).aspx](https://msdn.microsoft.com/en-us/library/dn903842(v=vs.85).aspx). [Accessed: 08- Dec- 2017].

[[32] Microsoft, “IDXGISwapChain::Present method (Windows)”, Msdn.microsoft.com, 2017. [Online]. Available: ][https://msdn.microsoft.com/en-us/library/bb174576(v=vs.85).aspx](https://msdn.microsoft.com/en-us/library/bb174576(v=vs.85).aspx). [Accessed: 08- Dec- 2017].

[[33] D. Houlton, “Full-screen DirectX* desktop apps using the Flip Presentation Model | Intel® Software”, Software.intel.com, 2017. [Online]. Available: ][https://software.intel.com/en-us/blogs/2013/06/03/full-screen-direct3d-games-using-borderless-windowed-mode](https://software.intel.com/en-us/blogs/2013/06/03/full-screen-direct3d-games-using-borderless-windowed-mode). [Accessed: 11- Dec- 2017].

[[34] Microsoft, “SetWindowPos function (Windows)”, Msdn.microsoft.com, 2017. [Online]. Available: ][https://msdn.microsoft.com/en-us/library/ms633545(v=vs.85).aspx](https://msdn.microsoft.com/en-us/library/ms633545(v=vs.85).aspx). [Accessed: 11- Dec- 2017].

[[35] Microsoft, “DPI_AWARENESS_CONTEXT handle (Windows)”, Msdn.microsoft.com, 2017. [Online]. Available: ][https://msdn.microsoft.com/library/mt791579(v=vs.85).aspx](https://msdn.microsoft.com/library/windows/desktop/mt791579(v=vs.85).aspx). [Accessed: 11- Dec- 2017].

Thank you.

Thank you! I hope to see more DX12 lessons in the near future! 🙂

Mateusz,

Yes, I’m working on Lesson 2 now!

Great lesson!

I am fairly new to C++ programming in general, and was looking for something to get me started with and learn DX12. This lesson is easily the best resource I have found so far.

Thanks, and very much looking forward to part 2!

Thanks Jonathan. I hope to be able to post part 2 this week!

Thanks for such a nice tutorial. Hoping to see your next set of tutorial on HLSL / Shaders soon.

Mukesh,

If you are only interested in the HLSL shaders then you can also check out the DirectX 11 tutorials:

The HLSL shading language in DirectX 12 is identical to DirectX 11. There are a few wave-level intrinsics that are added in Shader Model 6.0 but those wont be introduced until I start talking about compute shaders.

wow, great article

i found DX12 (or vulkan) is more complex….

This is an awesome article. Gave me a much better understanding of the D3D12 basics.

One quick correction… RegisterClassExW returns an ATOM, not an HRESULT. And the return value is 0 if it fails.

Ryan,

Thanks!

I’ve updated the example according to your feedback. Good catch!

I followed the microsoft tutorials and examples at first and got a triangle drawn on the screen, but I still couldn’t understand many of the concepts and api’s. Then I turned to your article and read it head to toe. Now every thing looks so clear to me. Thanks, keep up the good work!

Thanks Geo! I’m glad I could help a few people better understand how to work with DirectX 12.

Thank you! You can use “program_options” for command line https://theboostcpplibraries.com/boost.program_options

Thanks for the tip! I’m aware of the boost offerings but my goal was to use as few 3rd party libraries as possible for these tutorials so that it is as simple as possible. Boost is a great (set of) libraries but it is annoying to keep updating it for each new compiler version.

Why did you create an array of Command Allocators, 1 would suffice?

Newton,

You need at least 1 command allocator for each “in-flight” command list. Since the demo uses triple buffering, then there are a maximum of 3 in-flight command lists, so we need 3 command allocators. Keep in mind the command list can be reused, but the command allocator cannot be reused until it is no longer being used by the command queue.

Hi,

In the Resize() function where you reset the per-frame fence values to the fence value of the current back buffer index, shouldn’t we be doing

g_FrameFenceValues[i] = g_FenceValue

instead?

According to my understanding it doesn’t matter what you set as long as the value being set is less than or equal to g_FenceValue. Since we called Flush just before. We can even set it to 0, can’t we?

Please correct me if I am wrong.

Thanks in advance,

Newton

Newton,

Setting all of the g_FrameFenceValues to g_FrameFenceValues[g_CurrentBackBufferIndex] ensures that the fence value is at least the value that was last signaled on the command queue. It may be safe to set it to 0 (or 1) if there are no commands being executed on the command queue.

This is fantastic. I have been working with DX12 for about 6 months now and this article clarified any doubts I had about the basics. Keep em coming 🙂

Great tutorial!

I think a nice addition would be an explanation of what a Win32 application is and what that looks like in Visual Studio 2017. Since it is now called a Windows Desktop Application (https://docs.microsoft.com/en-us/cpp/ide/visual-cpp-project-types?view=vs-2017). And what the differences are between an empty c++ project and a Windows Desktop Application. Mainly Unicode and preprocessor differences.

That setup really hung me up since I want to do everything inside Visual Studio 2017 for the sake of simplicity since I’m not a build/environment kind of person.

Juan,

Setting up a project in Visual Studio was described in multiple of my previous articles (in previous version of Visual Studio). I’ve since moved towards using CMake for my projects since it is stable build toolchain that doesn’t require me to rewrite the “How to setup a project in Visual Studio” for every tutorial I write. It also allows the reader to choose their preferred build environment (MinGW, or CLion if they so desire — maybe not for DirectX. I haven’t tried these tools with DX) and it should still be possible to follow the rest of the tutorial without the need to manually configure project settings.

I’m sorry to say this, but my suggestion would be to try to use CMake for more projects. After using it for a few projects, I’ve started to prefer using CMake over configuring project settings in Visual Studio. The primary reason this change in opinion is future proofing the tutorials. I don’t have to keep updating the distributed project files for every new version of Visual Studio (I started with Visual Studio 2013 in the first tutorials on the website). Updating CMake with the newer generators is the only thing needed to update the project and solution files.

Also, if you are doing cross-platform development, then learning CMake will save you a tonne of time with

build wrangling.I 100% agree with the suggestion to start using CMake. Manually configuring Visual Studio projects should be a thing of the past. It gets especially cumbersome when your project starts growing and starts requiring more and more external dependencies. CMake can do this and more, neatly and cleanly. Even if you only want to work with Visual Studio, Cmake will still give you benefits.

Instead of undefining min and max, use the NOMINMAX define (preferably globally, like in project settings). This will prevent them from getting defined in the first place.

Good tip! I’ll keep this in mind for the next tutorials.

Hello. My VS for some reason does not allow me to build. It shows errors. Although everything seems to be done correctly, according to the lesson.

Error LNK2019 unresolved external symbol _D3D12CreateDevice@16 referenced in function “class Microsoft::WRL::ComPtr __cdecl CreateDevice(class Microsoft::WRL::ComPtr)” (?CreateDevice@@YA?AV?$ComPtr@UID3D12Device2@@@WRL@Microsoft@@V?$ComPtr@UIDXGIAdapter4@@@23@@Z)

Error LNK2019 unresolved external symbol _D3D12GetDebugInterface@8 referenced in function “void __cdecl EnableDebugLayer(void)” (?EnableDebugLayer@@YAXXZ)

Error LNK2019 unresolved external symbol _CreateDXGIFactory1@8 referenced in function “bool __cdecl CheckTearingSupport(void)” (?CheckTearingSupport@@YA_NXZ)

Error LNK2019 unresolved external symbol _CreateDXGIFactory2@12 referenced in function “class Microsoft::WRL::ComPtr __cdecl CreateSwapChain(struct HWND__ *,class Microsoft::WRL::ComPtr,unsigned int,unsigned int,unsigned int)” (?CreateSwapChain@@YA?AV?$ComPtr@UIDXGISwapChain4@@@WRL@Microsoft@@PAUHWND__@@V?$ComPtr@UID3D12CommandQueue@@@23@III@Z)

Jager,

It seems like you are missing some necessary library files. Did you generate the project files using the GenerateProjectFiles.bat script in the root folder? If not, make sure you do! The CMakeLists.txt file provided with the source files will ensure that the project is linking with the correct libraries.

Also, you must have the Windows 10 SDK installed. This should have been installed when you installed Visual Studio. Make sure you have the latest version of Visual Studio 2017 (or Visual Studio 2019 Preview) before you run the GenerateProjectFiles.bat file to generate the solution and project files.

Thank you for the reply! I already figured out this problem adding d3d12.lib and dxgi.lib libraries to the VS project. 🙂

Hey Jeremiah,

You have a nice tutorial albeit a little too overwhelming for a newbie like me. It’s a little hard to just jump into it when there’s so much to absorb but I feel like there’s a few places where a little more explanation is required because the docs are quite generic and don’t actually offer an insight to the code. Especially places in which the structures and the functions have a normal base version and then 1,2,3,4,.. versions of them too. Like ID3D12Device1,2,etc. I would like to know what’s the difference between them and when to use what. Why not just use the latest everywhere like when actually creating a device create a device with I3D12Device5 instead of 2? Why create 2?

Jako,

DirectX 12 is a bit overwhelming even for experienced programmers. I tried to make it as easy as possible to understand but ended up creating 4 articles (so far), each one about 100 printed pages.

The numbers at the end of the class indicated added functionality to the previous version of the class. The numbers are not necessarily associated with Windows 10 (Operating system) or Window 10 SDK releases (for example, the ID3D12Device1 was relased together with the Windows 10 Anniversary Update, which was the 2nd major Windows 10 update since the original release), they are simply used to indicate added functionality. The DirectX Ray Tracing API (DXR) was added in ID3D12Device5 and ID3D12GraphicsCommandList4. So the numbers are not related to API versions, but simply iterations of that class.

I hope that makes sense?

Yeah,that does. Shouldn’t we be using the latest iterations of the class then? Are we not using them because using them would mean leaving out a selective portion of people?

The tutorials are awesome and I am waiting for part 5,though I haven’t reached that far yet :P.

Thanks. Very helpful tutorial.

I’m having issues with setting up D3Dcompiler_47.lib thingy mentioned in Preamble. How am I supposed to do it with Visual Studio 2019? I have .dll in my project directory but I don’t see .lib file anywhere. Any help appreciated

The

`D3Dcompiler_47.lib`

file is already part of the Windows 10 SDK and should be installed together with Visual Studio if you select the “Game Development with C++” package in the Visual Studio Installer. The lib file is linked at compile time so you don’t need to distribute those files with your executable file.But the

`D3Dcompiler_47.dll`

file is dynamically loaded at runtime (when your executable is run on the end-user’s computer) so only the DLL file needs to be distributed together with your application.I hope that helps.

I concerned with same problem. I fixed this by linking to d3dcompiler.lib not D3Dcompiler_47.lib

Thank you very much for your work with this tutorial, I have already learned a lot. I have received a linker error though and I am not sure why?

It’s the LNK2019 error with D3D12CreateDevice, D3D12GetDebugInterface, CreateDXGIFactory1 and 2

Make sure you are linking against the

`d3d12.lib`

file in your linker settings.If you still have issues with this, then please consider joining the Discord server (https://discord.gg/gsxxaxc) to have any further questions answered.

Yep, I have got it, thank you very much once again!

Will there be any problems if I do this:

while (msg.message != WM_QUIT)

{

if (::PeekMessage(&msg, NULL, 0, 0, PM_REMOVE))

{

::TranslateMessage(&msg);

::DispatchMessage(&msg);

}

Flush(g_CommandQueue, g_Fence, g_FenceValue, g_FenceEvent);

Update();

Render();

}

Not that I am getting any errors or anything, but I will have to go through this article many times to fully understand the synchronization part. Just wanted to know if there is anything wrong in doing this.

Tarun,

Add the

`Flush`

command directly in the message loop will cause the CPU to stall (it will go idle until the GPU is finished executing all the commands from the previous frame). Of course this is not ideal as you probably want to be able to perform the update for the next frame while the GPU is still executing commands.Are you experiencing any issues if you don’t call

`Flush`

here?Thank you, very useful! I got the following error trying to compile with Visual Studio 2019 Community v16.3.2:

.cpp(472,27): error C2664: ‘void OutputDebugStringW(LPCWSTR)’: cannot convert argument 1 from ‘char [500]’ to ‘LPCWSTR’

.cpp(472,21): message : Types pointed to are unrelated; conversion requires reinterpret_cast, C-style cast or function-style cast

\Windows Kits\10\Include\10.0.18362.0\um\debugapi.h(62,1): message : see declaration of ‘OutputDebugStringW’

Jero,

If your project is configured to use the

Unicode Character Set(Project > Properties > Advanced > Character Set) then the`OutputDebugString`

macro will resolve to the`OutputDebugStringW`

function. In this case, any literal strings that you want to use should be wrapped with the`_T`

or`_TEXT`

macro as explained here: https://docs.microsoft.com/en-us/cpp/text/unicode-programming-summary?view=vs-2019.My preference is to set the

Character Setconfiguration property toUse Multi-Byte Character Setand explicitly use`OutputDebugStringA`

function directly instead of relying on the macros. The only exception to this rule is when you need to work with a`_TCHAR`

strings like in the following example:In this case, the

`_com_error`

class is used to convert an`HRESULT`

into a human-readable string but the`_com_error::ErrorMessage`

returns a`TCHAR*`

(which resolves to a`wchar_t*`

when using the Unicode character set and a`char*`

when using a Multi Byte character set).Alternatively, if you want to use the

`OutputDebugStringW`

function directly, then you should always prepend your literals with the`L`

which will convert the string literal to a wide character string:Before using the

`OutpuDebugStringW`

, you should be aware of the caveats as explained here: https://docs.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-outputdebugstringw#remarks.I hope this answers your question!

Instead of writing this manually:

#if defined(min)

#undef min

#endif

#if defined(max)

#undef max

#endif

You could just use this macro that is defined by Windows.h

NOMINMAX

Also instead of this:

using namespace Microsoft::WRL;

I’d recommend a using-declaration instead:

using Microsoft::WRL::ComPtr;

Juan,

Thanks for the tip. I’ve update the github source to include this suggestion.

Why did you make the return value from RegisterClassExW a local global?

static ATOM atom = ::RegisterClassExW(&windowClass);

assert(atom > 0);

Juan,

I can’t think of any reason why the

`ATOM`

is static in this case. Copy-paste error?When creating the adapter where in the documentation does it say that EnumWarpAdapter must take a IDXGIAdapter1?

Also, why not use EnumAdapterByGpuPreference?

According to the documentation, the

`IDXGIFactory4::EnumWarpAdapter`

method actually takes a`IDXGIAdapter`

pointer (actually a pointer to a void pointer) but in the samples I saw, it was using a`IDXGIAdapter1`

pointer. The point here is that the`IDXGIFactory4::EnumWarpAdapter`

method was introduced in DXGI 1.4 but the`IDXGIAdapter4`

that we need wasn’t added until DXGI 1.6. So to safely perform the cast, we need to get a pointer to an earlier type, then cast it to the later type (and ensure it is valid). We can’t ask for the later type directly from the`IDXGIFactory4::EnumWarpAdapter`

method.Because it was added in DXGI 1.6 and I just didn’t know about it at the time of writing the article! The code shown to select the GPU based on the largest amount of dedicated video memory was actually written a few years before writing this article 🙂 But I’ll use that method in the future.

Looking at the

`dxgi1_6.h`

header in the 10.0.1904 Windows 10 SK, it seems that there is a macro which forces use of`EnumAdapterByGpuPreference()`

and removes references to`EnumWarpAdapter()`

and other similar functions labeled in the header as the “C style interface”.Unless you

`#define CINTERFACE`

, you’ll get a link error saying that EnumWarpAdapter is not a member of IDXGIAdapter4.Cameron,

Thanks for the tip. I’ll look into this.

I really appreciate the efforts put up for the tutorial. I dint find much of tutorials/books on directX 12 elsewhere. But I just can’t cope up with the pace after 1st tutorial. Tutorial becomes too hard to understand. I think, there should be small but dedicated tutorial on separate topics before merging all concepts together. For example, a tutorial for only applying texture, a tutorial only for depth and stencil buffer, a tutorial only for index buffer. If I could understand everything separately then merging all into one will be understandable. In current tutorial, I am unable to clarify simple things itself and getting lost into complex inter-linkage of several topics.

DirectX 12 is not for the faint of heart. Even loading textures and generating mipmaps is a laborious task.

If you don’t already have a background in graphics programming, I recommend you follow the DX11 articles here:

Jeremiah, fantastic work out there man. Thank you so much for the tutorials you’ve made. To understand the inner workings behind DX12 is one thing, but to teach about them is a whole another story. Even though I agree that it might be sometimes hard to follow, I wouldn’t blame it on you, since you did your best to explain almost all of the concepts in a concise way and it still took 100 printed pages just to explain how to clear the screen color.

As I see your tutorial series end on the 4th one, and hence I’m not sure what direction should I take once I finish them. Could you hence share what was your way of learning DX12 without your excellent tutorials?

Thank for this detailed DX12 guide,

Having experienced with DX9 was a great help and i was able to process and follow easily.

Any chance of #2 in this series ?

The 2nd tutorial can be found here:

https://www.3dgep.com/learning-directx-12-2/

The DirectX category can be found here:

https://www.3dgep.com/category/graphics-programming/directx/

I’m getting artifacts when I resize the window. And when I try building your code from source I’m also getting the same issue.

I made a stackoverflow about it:

https://stackoverflow.com/questions/63567803/resizing-window-is-causing-artifacts

Any ideas?

Zero,

I can’t find the Stackoverflow question you are referring to.

Consider joining our Discord server for a quicker response:

https://discord.gg/3dgep.com

this is gold

thanks for this great article

a ton of useful info is shared here

much appreciated

When you talk about testing device creation without actually creating the device you say that D3D12CreateDevice returns S_OK when it actually returns S_FALSE according to the documentation

https://docs.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-d3d12createdevice?redirectedfrom=MSDN

(when ppDevice is null)

“To verify that the adapter returned from the IDXGIFactory1::EnumAdapters1 method is a compatible DirectX 12 adapter, a (null) device is created using the D3D12CreateDevice function is used. If this function returns S_OK, then the function succeeded and it is a DirectX 12 compatible adapter.”

Still reading through the tutorial, thanks so much 🙂

An

`HRESULT`

that is a non-negative value (greater than or equal to 0) is considered a success.`S_OK`

has a value of 0 and`S_FALSE`

has a value of 1. Both of these are considered success results and the`SUCCEEDED(S_FALSE)`

macro will evaluate to`true`

. Although it seems unintuitive that`S_FALSE`

is considered a success code, the code is correct.Both your DX11 and DX12 guides are absolutely the best, most thorough, clearest introductions to both APIs, and have helped me immensely. Thank you.

Hi, your lesson helps me a lot, but there seems to be a little mistake.

In the Query DirectX 12 Adapter section, it says that ID3D12CreateDevice function with nullptr as its last argument will return S_OK if the device can be successfully created. But MSDN for this function says: “If ppDevice is NULL and the function succeeds, S_FALSE is returned, rather than S_OK.”

The code you are referring to is just testing if the adapter can be used to create a

`ID3D12Device`

. It’s not actually creating the device.It’s not a mistake


is a valid success code. Any non-negative code is a success code. You may be mistaking this withS_FALSE

which is an error code, butE_FAIL`S_FALSE`

actually indicates success.So if the function returns either

`S_OK`

or`S_FALSE`

, then the function succeeds and that adapter can be used to create a`ID3D12Device`

.The code you are referring to is just testing if the adapter can be used to create a

`ID3D12Device`

.It’s not a mistake


is a valid success code. Any non-negative code is a success code. You may be mistaking this withS_FALSE

which is an error code, butE_FAIL`S_FALSE`

actually indicates success.So if the function returns either

`S_OK`

or`S_FALSE`

, then the function succeeds and that adapter can be used to create a`ID3D12Device`

.The code you are referring to is just testing if the adapter can be used to create a

`ID3D12Device`

. It’s not actually being created.It’s not a mistake


is a valid success code. Any non-negative code is a success code. You may be mistaking this withS_FALSE

which is an error code, butE_FAIL`S_FALSE`

actually indicates success.So if the function returns either

`S_OK`

or`S_FALSE`

, then the function succeeds and that adapter can be used to create a`ID3D12Device`

.The code you are referring to is just testing if the adapter can be used to create a

`ID3D12Device`

. It’s not actually creating the device.It’s not a mistake


is a valid success code. Any non-negative code is a success code. You may be mistaking this withS_FALSE

which is an error code, butE_FAIL`S_FALSE`

actually indicates success.So if the function returns either

`S_OK`

or`S_FALSE`

, then the function succeeds and that adapter can be used to create a`ID3D12Device`

.Thank you for this(Won’t take this knowledge for granted), for some reason whenever I try to use a video tutorial I find it impossible to finish. Always ended up stuck somewhere. But doing this article made me realize something, and that in some cases learning how to initialize a program through reading is better, opposed to trying to copy and keep the pace up with the teacher. By doing the article myself I was able to comment on anything, that seemed complex, also I was forced to go on the web and search for any errors or bugs while trying to initialize, which also helped my learning experience in C++ as a whole.

This is a great resource. Thank you so much for putting it together!

thanks a lot ，this would be the best DirectX lesson i have found

One thing I can’t understand in the Render function.

There is a key difference between the logic of your actual cpp code and that of the pseudo-code when you explained the “Command Queue”:

cpp code: execute -> signal -> present -> waitForFenceValue

pseudo-code: execute -> present -> signal -> waitForFenceValue

The pseudo-code looks correct to me. From my understanding, the cpp code will have a lethal issue: because you did not wait for the “present” to finish before issuing “signal”, doesn’t this mean the render should get messed up?!

Thanks a lot.

The signal occurs in the Present function (https://www.3dgep.com/learning-directx-12-1/#Present) after the swap chain is presented. It’s not different in the CPP code compared to the pseudo-code example.

Hi, and thanks for this tutorial. Still making my way through it.

I come from some Vulkan experience, and I’ve read online (and it seems to me working through this) that factories are analogous to Vulkan instances.

In many Vulkan tutorials and code the instance will just be created once and as a global handle. Here, it seems like we create a factory every time when we need it, such as the CheckTearingSupport() and CreateSwapChain() functions. It’s not as if I expect all these APIs to behave similarly, I am just asking out of curiosity. 🙂 Perhaps this is a design decision of DX-land I am unaware of.

Perhaps it has to do with there being various iterations of IDXGIFactory (1,2,3,4..)? Although it seems to me that using .As() would work?

Thanks a lot!

Very good tutorial, thank you. I appreciate the depth of explanations throughout. The only thing I had to fix myself code-wise is that needs to be included in Helpers.h, though that could be due to project config as well, I’m sure.

It would be helpful for people like me, who are better at C++ than VS, to add a section explaining how to set up the visual studio project, especially since the referenced blog URL no longer works.

1) Change the character set in advanced config properties to multi-byte

2) Add additional dependencies in Linker->Input of d3d12.lib,;dxgi.lib;d3dcompiler.lib

3) Add library directory in VC++ Directories -> Library Directories

4) Add project directory in VC++ Directories -> include Directories

Not sure why steps 2-4 needed to be done manually, but I’ve never had much success with VS.

I guess I got lucky to find this tutorial course as my first one. The best thing for me personally is the fact that you didn’t use any unnecessary classes or another abstractions in this first lesson. It kind of sad that you end up using classes in the second lesson, as I would like the whole course be as abstractions free as possible. Oh whale, I’m probably just gonna “declassify” your code then =)

I want to share with you, people, alternative way to implement the FPS counter in this lesson. Instead of STL ::chrono I recommend using the low level API function QueryPerformanceCounter. This will have much lower overhead comparing to STL and it will also avoid the use of floating point math. Its as simple as this:

LARGE_INTEGER upd_t0, upd_t1;

ui64 upd_frames, nano_secs;

ui64 one_sec_ticks; // How much ticks in one second

void fpsCounterInit()

{

QueryPerformanceFrequency((LARGE_INTEGER *)&one_sec_ticks);

QueryPerformanceCounter(&upd_t0);

}

Call this function in main() before the render() function. This avoids the usage of local static variables, that are super slow in C++.

void update()

{

++upd_frames;

QueryPerformanceCounter(&upd_t1);

ui64 dtime = (ui64)(upd_t1.QuadPart – upd_t0.QuadPart);

upd_t0 = upd_t1;

nano_secs += dtime;

if(nano_secs > one_sec_ticks)

{

p|”FPS: “|upd_frames|N;

upd_frames = 0;

nano_secs = 0;

}

}

Something like this. The “p” is my custom printing class, I print it to the console window. I also read somewhere that it is preferable to use QueryPerformanceCounter in the real game, if you want to keep track of time delta between frames for your physics engine.

Brilliant! Complete, explanatory and illuminating. I couldn’t’ve wished for a clearer tutorial.

This tutorial makes a very common mistake, and that is to assume that a term is understood when no explanation has been given.

Specifically, a person who is completely new to DirectX is not going to know what a command queue is. The term is used repeatedly without any explanation of what it means. This is very confusing for new readers.

I have a question regardeing this pseudocode code:

fenceValues[frameID] = Signal()

WaitForFenceValue( fenceValues[_nextFrameID] )

I wonder why not:

WaitForFenceValue( fenceValues[frameID] )

Suppose we are working on frameID = 0, fenceValues = {0, 0, 0}

After we signal, fenceValue increase to 1, fenceValues = {1, 0, 0}

If we wait for fenceValues[_nextFrameID] where _nextFrameId is 1, then the value is 0 still for fenceValues[1] is still 0 at this point?

Hiring https://contractorfinder.geappliances.com/contractors-calgary-penbrooke-meadows-marlborough-ab was a game-changer for my habitation renovation project. From the introductory consultation to the concluding walkthrough, their professionalism and savvy were evident. The body was communicative, ensuring I was informed at every stage. Their prominence to detail was immaculate, transforming my delusion into reality with precision. Notwithstanding a infrequent unexpected challenges, they adapted swiftly, keeping the project on track. The calibre of toil exceeded my expectations, making the investment worthwhile.

I recently adapted to this locale to decide https://synergy3.com/plumbing/gas-piping/ and roofing contractors, and I couldn’t be happier with the results. The search was straightforward, and I appreciated the complete profiles and guy reviews in the course of each contractor. It made comparing options and reading about other clients’ experiences easy. The contractors I contacted were prompt, knowledgeable, and offered competitive quotes. This site is a unrealistic resource allowing for regarding anyone needing punctilious almshouse restore services. Enthusiastically recommended pro its explicit interface and trait listings!

I recently adapted to this locale to remark https://synergy3.com/plumbing/gas-piping/ and roofing contractors, and I couldn’t be happier with the results. The search was straightforward, and I appreciated the full profiles and customer reviews on the side of each contractor. It made comparing options and reading about other clients’ experiences easy. The contractors I contacted were urge, skilful, and offered competitive quotes. This purlieus is a grotesque resource for anyone needing infallible retreat repair services. Well recommended quest of its user-friendly interface and trait listings!

Late to the game here, but FINALLY a tutorial that really is a tutorial. I’ve lost count of the number of half-assed tutorials that are nothing more than excerpts of code and which explain nothing.