---
title: Introduction to DirectX 11
url: https://www.3dgep.com/introduction-to-directx-11/
author: Jeremiah
published: '2014-03-21'
source_blog: 3D Game Engine Programming
source_site: https://www.3dgep.com/
category: graphics
fetched: '2026-04-13'
---

In this article, I will introduce the reader to DirectX 11. We will create a simple demo application that can be used to create more complex DirectX examples and demos. After reading this article, you should be able to create a DirectX application and render geometry using a simple vertex shader and pixel shader.


Contents

[1 Introduction](https://www.3dgep.com#Introduction)-
[2 DirectX 11 Components](https://www.3dgep.com#DirectX_11_Components) -
[3 DirectX 11 Pipeline](https://www.3dgep.com#DirectX_11_Pipeline) -
[4 DirectX Demo](https://www.3dgep.com#DirectX_Demo) -
[5 Shaders](https://www.3dgep.com#Shaders) -
[6 DirectX Demo Cont…](https://www.3dgep.com#DirectX_Demo_Conthellip) [7 Download the Demo](https://www.3dgep.com#Download_the_Demo)[8 References](https://www.3dgep.com#References)

**DirectX** is a collection of application programming interfaces (API). The components of the DirectX API provides low-level access to the hardware running on a Windows based Operating System [[1]](https://www.3dgep.com#DirectX).

Prior to the release of Windows 95, application programmers had direct access to low-level hardware devices such as video, mouse, and keyboards. In Windows 95, access to these low-level hardware devices was restricted [[2]](https://www.3dgep.com#Windows_95). The developers at Microsoft realized that in order to facilitate access to these low-level devices, APIs needed to be developed to provide an abstract way to access these low-level hardware devices [[1]](https://www.3dgep.com#DirectX).

The first version of DirectX was released in September 1995 shortly after the release of Windows 95 under the name **Windows Game SDK** [[1]](https://www.3dgep.com#DirectX). Through the period of 1995-1997, the DirectX library went through several version changes to reach version 5. Subsequent major revisions saw a release on an annual schedule until DirectX 9 which wasn’t introduced until two years after DirectX 8 [[1]](https://www.3dgep.com#DirectX).

Prior to **DirectX 8.0**, the graphics programmer was restricted to a fixed-function rendering pipeline. This meant that the implementation of the rendering algorithms were fixed in the graphics hardware. DirectX 8 introduced the first versions of a programmable shading language with [Shader Model 1](http://msdn.microsoft.com/en-us/library/windows/desktop/bb509654(v=vs.85).aspx) [[4]]. Shader Model 1 featured a single shader profile for creating a very simple vertex shader and did not provide a shader profile for pixel shading.

**DirectX 9.0** was released in December 2002 [[1]](https://www.3dgep.com#DirectX) and introduced [Shader Model 2.0](http://msdn.microsoft.com/en-us/library/windows/desktop/bb509655(v=vs.85).aspx). Shader Model 2.0 introduced a new vertex shader profile as well as a pixel shader profile. Pixel shaders provided the ability to create per-pixel lighting.

**DirectX 9.0c** was released in August 2004 [[1]](https://www.3dgep.com#DirectX) together with the introduction of [Shader Model 3.0](http://msdn.microsoft.com/en-us/library/windows/desktop/bb509656(v=vs.85).aspx). Shader Model 3.0 extended the existing vertex shader and pixel shader profiles increasing the number of instructions and allowing for more complex shaders.

In November 2006, **DirectX 10** was released [[1]](https://www.3dgep.com#DirectX) which introduced [Shader Model 4.0](http://msdn.microsoft.com/en-us/library/windows/desktop/bb509657(v=vs.85).aspx). Shader Model 4.0 extended the functionality of the vertex shader and the pixel shader as well as introduced a new shader profile called the geometry shader. Shader Model 4.0 also introduced the Effect Framework which allowed the graphics programmer to create effect files (.fx) that combined vertex, pixel, and geometry shaders in a single file. Support for the effect files was subsequently dropped in later versions of the Direct3D API.

**DirectX 11** was released in October 2009 [[1]](https://www.3dgep.com#DirectX) together with [Shader Model 5.0](http://msdn.microsoft.com/en-us/library/windows/desktop/ff471356(v=vs.85).aspx). Shader Model 5.0 extended the vertex, pixel, and geometry shaders of Shader Model 4.0 as well as introduce tessellation and compute shader profiles. Tessellation shaders provide the functionality to progressively refine the detail of a mesh at run-time while the compute shaders provide a general-purpose compute language that is executed on the GPU instead of the CPU.

On March 20, 2014, Microsoft will announce the release of **DirectX 12** [[5]](https://www.3dgep.com#DirectX12) which will no doubt require me to rewrite this entire article.

The table below shows the various releases of DirectX and the corresponding shader model and shader profiles [[1]](https://www.3dgep.com#DirectX)[[2]](https://www.3dgep.com#Direct3D)[[4]](https://www.3dgep.com#ShaderModels).

| DirectX | Release Date | Shader Model | Shader Profile(s) |
|---|---|---|---|
| DirectX 8.0 | November 12, 2000 | Shader Model 1.0 | vs_1_1 |
| DirectX 9.0 | November 19, 2002 | Shader Model 2.0 | vs_2_0, vs_2_x, ps_2_0, ps_2_x |
| DirectX 9.0c | August 4, 2004 | Shader Model 3.0 | vs_3_0, ps_3_0 |
| DirectX 10.0 | November 30, 2006 | Shader Model 4.0 | vs_4_0, ps_4_0, gs_4_0 |
| DirectX 10.1 | February 4, 2008 | Shader Model 4.1 | vs_4_1, ps_4_1, gs_4_1 |
| DirectX 11.0 | October 22, 2009 | Shader Model 5.0 | vs_5_0, ps_5_0, gs_5_0, ds_5_0, hs_5_0, cs_5_0 |

As previously mentioned, the DirectX SDK is actually a collection of programming API’s. The DirectX API that deals with hardware accelerated 3D graphics is the Direc3D API (and the subject of this article) however there are several more API’s which make up the DirectX SDK.

**Direct2D** is a hardware accelerated 2D graphics API which provides high-performance and high-quality rendering for 2D geometry, bitmaps, and text [[6]](https://www.3dgep.com#Direct2D).

**Direct3D** is a hardware accelerated 3D graphics API [[7]](https://www.3dgep.com#Direct3D_2). This API is the subject of this article.

**DirectWrite** API provides support for high-quality sub-pixel text rendering that can use **Direct2D**, **GDI** or application-specific rendering technology [[8]](https://www.3dgep.com#DirectWrite).

The **DirectXMath** API provides SIMD-friendly C++ types and functions for common linear algebra and graphics math operations common to DirectX applications [[9]](https://www.3dgep.com#DirectXMath). We will be using this math library for some simple math operations in the application code.

**XAudio2** is a low-level audio API that provides signal processing and mixing foundation for developing high performance audio engines for games [[10]](https://www.3dgep.com#XAudio2).

XInput Game Controller API enables applications to receive input from the Xbox 360 Controller for Windows [[11]](https://www.3dgep.com/XInput).

The purpose of the Microsoft DirectX Graphics Infrastructure (**DXGI**) is to manage low-level tasks that can be independent of the DirectX graphics runtime. You may want to work with DXGI directly if your application needs to enumerate devices or control how data is presented to an output [[12]](https://www.3dgep.com#DXGI). In this article, we will be using DXGI to enumerate the display devices in order to determine the optimal refresh rate of the screen.

The DirectX 11 Graphics pipeline consists of several stages. The following diagram illustrates the different stages of the DirectX 11 rendering pipeline. The arrow indicates the flow of data from each stage as well as the flow of data from memory resources such as buffers, textures, and constant buffers that are available on the GPU.

The image illustrates the 10 stages of the DirectX 11 rendering pipeline. The rectangular blocks are fixed-function stages and cannot be modified programmatically. The rounded-rectangular blocks indicate programmable stages of the pipeline.

The first stage of the DirectX graphics pipeline is the **Input-Assembler** (**IA**) stage. In this stage, the geometry is specified and the layout of the data which is expected by the vertex shader is configured [[13]](https://www.3dgep.com#DirectX_Pipeline).

The **Vertex Shader** (**VS**) stage is usually responsible for transforming the vertex position from object space into clip space but it can also be used for performing skinning of skeletal animated meshes or per-vertex lighting [[13]](https://www.3dgep.com#DirectX_Pipeline). The input to the vertex shader is a single vertex and the minimum output from the vertex shader is a single vertex position in clip-space (the transformation to clip-space can also be performed by the tessellation stage or the geometry shader if either is active).

The **Hull Shader** (**HS**) stage is an optional shader stage and is responsible for determining how much an input control patch should be tessellated by the tessellation stage [[14]](https://www.3dgep.com#Tessellation).

The **Tessellator Stage** is a fixed-function stage that subdivides a patch primitive into smaller primitives according to the tessellation factors specified by the hull shader stage [[14]](https://www.3dgep.com#Tessellation).

The **Domain Shader** (**DS**) stage is an optional shader stage and it computes the final vertex attributes based on the output control points from the hull shader and the interpolation coordinates from the tesselator stage [[14]](https://www.3dgep.com#Tessellation). The input to the domain shader is a single output point from the tessellator stage and the output is the computed attributes of the tessellated primitive.

The **Geometry Shader** (**GS**) stage is an optional shader stage that takes a single geometric primitive (a single vertex for a point primitive, three vertices for a triangle primitive, and two vertices for a line primitive) as input and can either discard the primitive, transform the primitive into another primitive type (for example a point to a quad) or generate additional primitives [[13]](https://www.3dgep.com#DirectX_Pipeline).

The **Stream Output** (**SO**) stage is an optional fixed-function stage that can be used to feed primitive data back into GPU memory. This data can be recirculated back to the rendering pipeline to be processed by another set of shaders [[13]](https://www.3dgep.com#DirectX_Pipeline). This is useful for spawning or terminating particles in a particle effect. The geometry shader can discard particles that should be terminated or generate new particles if particles should be spawned.

The **Rasterizer Stage** (**RS**) stage is a fixed-function stage which will clip primitives into the view frustum and perform primitive culling if either front-face or back-face culling is enabled [[13]](https://www.3dgep.com#DirectX_Pipeline). The rasterizer stage will also interpolate the per-vertex attributes across the face of each primitive and pass the interpolated values to the pixel shader.

The **Pixel Shader** (**PS**) stage takes the interpolated per-vertex values from the rasterizer stage and produces one (or more) per-pixel color values [[13]](https://www.3dgep.com#DirectX_Pipeline). The pixel shader can also optionally output a depth value of the current pixel by mapping a single component 32-bit floating-point value to the **SV_Depth** semantic but this is not a requirement of the pixel shader program. The pixel shader is invoked once for each pixel that is covered by a primitive [[15]](https://www.3dgep.com#Shader_Stages).

The **Output-Merger** (**OM**) stage combines the various types of output data (pixel shader output values, depth values, and stencil information) together with the contents of the currently bound render targets to produce the final pipeline result [[13]](https://www.3dgep.com#DirectX_Pipeline).

Now that we have a little bit of background information regarding the different stages of DirectX 11 let’s try to put it together to create a simple DirectX application that is capable of rendering 3D geometry using a minimal vertex shader and pixel shader.

In this tutorial I will be using **Visual Studio 2012** to create a template project that can be used to create subsequent DirectX 11 demos in the future. Starting with Visual Studio 2012 and the [Windows 8 SDK](http://msdn.microsoft.com/en-us/windows/desktop/hh852363.aspx) the DirecX SDK is now part of the Windows SDK so you do not need to download and install the DirectX SDK seperatly. See [Where is the DirectX SDK?](http://msdn.microsoft.com/en-us/library/windows/desktop/ee663275(v=vs.85).aspx) for more information.

Visual Studio 2012 also has the ability to compile your HLSL shader code as part of the regular compilation step and you can then load the precompiled shader code directly instead of compiling the shader code at runtime. This enables your application to load faster especially if you have many shaders. In this article I will show how you can setup your project to make use of shader compilation but I will also show you how you can load and compile your shader at runtime.

In this demo, I will not be using any 3rd party dependencies. All included headers and libraries are part of the Windows 8 SDK that comes with Visual Studio 2012 however you should make sure that you have applied the latest updates to Visual Studio 2012 so that you are working with the newest version of the Windows 8 SDK.

The first step to creating our DirectX demo is to setup an empty Win32 project in Visual Studio. First, let’s startup Visual Studio.

Select **File > New Project** from the main menu to bring up the **New Project** dialog box.

In the **New Project** dialog box, select the **Visual C++ > Empty Project** template. Choose a **Name**, **Location** and optionally a **Solution name** (or accept the default) for your new project and press the **OK** button to create the new project.

Before we continue configuring the project, let’s create a single CPP source file.

Select **Project > Add New Item…** from the main menu.

Select the **Visual C++ > C++ File (.cpp)** template and specify the name **main.cpp** and a location for the new source file. I prefer to put my C++ source files in subdirectory with the name **src** relative to the project folder. Press the OK button to create the file and add it to the project.

We need at least one CPP source file in the project in order to configure the project correctly. With the main.cpp file added to the project, we can now configure the project settings.

Open the project properties dialog by selecting **Project > Properties** from the main menu.

In the **Configuration** drop-down box, select **All Configurations**.

Select **Configuration Properties > General** and change the **Output Directory** to **bin\**.

In the **Debug** configuration only, change the **Target Name** to **$(ProjectName)d**. With this configuration, both the debug and the release builds will go to the same folder. To ensure we don’t replace release builds with debug builds and visa-versa, we will append the letter “d” to the end of the debug builds.

Select **Configuration Properties > Debugging** and change the Working Directory to **$(OutDir)** for both the **Debug** and **Release** configurations. Doing this will ensure that the current working directory will be correctly set to the location of our executable file so that we can express paths in the application relative to the executable (instead of relative to the project folder which usually is a major cause of confusion for beginning programmers).

If you want to place your public include folders in a separate directory then we need to tell the C++ compiler where our include files are located. In the **C/C++ > General** options add the name of the public include folder to the **Additional Include Directories** options. In my case, I have a separate folder called **inc** relative to my project folder where I will keep the header files for the project.

You will notice that we do not need to specify the location of the DirectX headers and libraries when using Visual Studio 2012. These paths are automatically included when we create a new project in Visual Studio 2012.

Although not absolutely necessary, I find using precompiled headers useful as it reduces the overall compile time of the project. For this small project, it may not be necessary to use precompiled headers but for large projects it is definitely useful to know how to setup precompiled headers.

For more information on creating and using precompiled header files for your Visual Studio project, please refer to [Creating Precompiled Header Files](http://msdn.microsoft.com/en-us/library/szfdksca.aspx) in the MSDN documentation.

Create a new header file in your project with the name **DirectXTemplatePCH.h** or something similar. The **PCH** postfix indicates that this file will be used to generate the precompiled header file.

Create a new C++ file in your project with the name **DirectXTemplatePCH.cpp**. This file will be used to create the precompiled header.

The content of the **DirectXTemplatePCH.cpp** file should contain only a single include statement and nothing else! If you have other include directives in this file or any C++ code then you are doing it wrong.

|
1 |
#include <DirectXTemplatePCH.h> |

Now that we’ve added the initial files that will be used for precompiled headers, let’s configure our project to create and use the precompiled headers.

Select **Project > Properties** from the main menu.

Make sure that **All Configurations** is selected in the **Configuration** drop-down box.

Select **Configuration Properties > C/C++ > Precompiled Headers** and set the **Precompiled Header** option to **Use (/Yu)**.

Set the **Precompiled Header File** option to the name of the header file you created in the previous step. In my case the name of the precompiled header file is **DirectXTemlatePCH.h**.

Apply the settings and without closing the project properties dialog box, select the **DirectXTemplatePCH.cpp** source file in the **Solution Explorer**.

For the **DirectXTemplatePCH.cpp** source file only, change the **Precompiled Header** option to **Create (/Yc)** and the other options should be the same as we specified at the project level.

With these settings configured, let’s start writing some code!

The global header file will contain all of the external (non changing) include files. You should not include project specific header files in the global header file because they are changing often. If the contents of the global header file change often then we can no longer take advantage of precompiled headers.

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
// System includes
#include <windows.h>
// DirectX includes
#include <d3d11.h>
#include <d3dcompiler.h>
#include <DirectXMath.h>
#include <DirectXColors.h>
// STL includes
#include <iostream>
#include <string>
|

Since we are creating a Windows application, we first include the ubiquitous Windows header file. This header file contains all of the definitions for creating a Windows based application.

The next set of headers includes the Direct3D API. The **d3dcompiler** header file is required for loading and compiling HLSL shaders. The **DirectXMath** header file includes math primitives like vectors, matrices and quaternions as well as the functions to operate on those primitives. The **DirectXColors** header defines a set of commonly used colors.

|
1
2
3
4
5
|
// Link library dependencies
#pragma comment(lib, "d3d11.lib")
#pragma comment(lib, "dxgi.lib")
#pragma comment(lib, "d3dcompiler.lib")
#pragma comment(lib, "winmm.lib")
|

This set of statements will cause the library dependencies to be automatically linked in the linker stage. You can also specify these libraries in the **Additional Dependencies** property in the **Linker** options if you want but putting them here simplifies the project configuration settings. Also if you were creating a library project, this file could be included in the global header file of another project to perform automatic linking of the required library dependencies.

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
// Safely release a COM object.
template<typename T>
inline void SafeRelease( T& ptr )
{
if ( ptr != NULL )
{
ptr->Release();
ptr = NULL;
}
}
|

The **SafeRelease** function can be used to safely release a COM object and set the COM pointer to NULL. This function allows us to safely release a COM object even if it has already been released before. Since we will be releasing COM objects a lot in this application, this function will also allow us to create neater code.

Before we get into the application code, we first need to define some global variables that will be used throughout the demo.

We first need to include the global header file that we created in the previous step.

|
1
2
|
#include <DirectXTemplatePCH.h>
using namespace DirectX;
|

On line 2 I include the **DirectX** namespace into the global namespace. All of the functions and types defined in the **DirectXMath** API are wrapped in the DirectX namespace. I got really tired of typing out the DirectX namespace every time I wanted to use a vector or a matrix so instead I just import the namespace.

The first set of globals define some properties for the application window.

|
1
2
3
4
5
6
7
|
const LONG g_WindowWidth = 1280;
const LONG g_WindowHeight = 720;
LPCSTR g_WindowClassName = "DirectXWindowClass";
LPCSTR g_WindowName = "DirectX Template";
HWND g_WindowHandle = 0;
const BOOL g_EnableVSync = TRUE;
|

The size of the window is defined by the **g_WindowWidth**, and **g_WindowHeight** variables. The actual window that we will create will be slightly larger than this because these variables actually define the size of the renderable area (or client area) of the window. The actual window size including the window frame will be computed before the actual window is created.

Before we can create a window instance, we need to create a window class. The window class should be unique for our application so we need to define a unique name for the class as well. The unique window class name is defined using the **g_WindowClassName** global variable.

The **g_WindowName** variable holds the name of the window that will be created from the window class. The window name will also be displayed in the top of the window frame.

The **g_WindowHandle** is used to identify the instance of the window that will be created.

A regular LCD or LED computer monitor has a vertical refresh rate of 60 Hz. That means that the image displayed on the screen is presented 60 times per second. When rendering your 3D application, you can choose to let your application display the image at the same rate as the screen’s refresh rate. The advantage of synchronizing your applications display rate with the refresh rate of the screen is that it eliminates any visible artifacts known as [screen tearing](https://en.wikipedia.org/wiki/Screen_tearing). If you want to render your scene as fast as possible, you can set the **g_EnableVSync** variable to **FALSE** and then your application will not wait for the vertical refresh of the screen to present the scene on the screen.

These are all of the variables that we need to define for the application window. The next set of variables will be DirectX specific.

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
// Direct3D device and swap chain.
ID3D11Device* g_d3dDevice = nullptr;
ID3D11DeviceContext* g_d3dDeviceContext = nullptr;
IDXGISwapChain* g_d3dSwapChain = nullptr;
// Render target view for the back buffer of the swap chain.
ID3D11RenderTargetView* g_d3dRenderTargetView = nullptr;
// Depth/stencil view for use as a depth buffer.
ID3D11DepthStencilView* g_d3dDepthStencilView = nullptr;
// A texture to associate to the depth stencil view.
ID3D11Texture2D* g_d3dDepthStencilBuffer = nullptr;
// Define the functionality of the depth/stencil stages.
ID3D11DepthStencilState* g_d3dDepthStencilState = nullptr;
// Define the functionality of the rasterizer stage.
ID3D11RasterizerState* g_d3dRasterizerState = nullptr;
D3D11_VIEWPORT g_Viewport = {0};
|

The **g_d3dDevice**, **g_d3dDeviceContext**, and **g_d3dSwapChain** are the absolute minimum variables required for the most basic DirectX 11 application. A **ID3D11Device** instance is used for allocating GPU resources such as buffers, textures, shaders, and state objects (to name a few). The **ID3D11DeviceContext** is used to configure the rendering pipeline and draw geometry. The **IDXGISwapChain** stores the buffers that are used for rendering data. This interface is also used to determine how the buffers are swapped when the rendered image should be presented to the screen.

The **g_d3dRenderTargetView** and the **g_d3dDepthStencilView** variables are used to define the subresource view of the area of a buffer to which we will draw to. A resource view defines an area of a buffer that can be used for rendering. In this case we need two views, the **g_d3dRenderTargetView** will refer to a subresource of a color buffer while the **g_d3dDepthStencilView** will refer to a subresource of a depth/stencil buffer.

The **IDXGISwapChain** instance has only a single color buffer that will be used to store the final color that is to be presented on the screen. In order to store depth information, we must create a separate depth buffer. The **g_d3dDepthStencilBuffer** will be used to refer to a 2D texture object that will be used to store the depth values so that objects close to the camera do not get overdrawn by objects that are farther away from the camera regardless of their drawing order.

We also need to define a few state variables for configuring the rasterizer and output-merger stages. The **g_d3dDepthStencilState** will be used to store the depth and stencil states used by the output-merger stage and the **g_d3dRasterizerState** variable will be used to store rasterizer state used by the rasterizer stage.

The **g_Viewport** variable defines the size of the viewport rectangle. The viewport rectangle is also used by the rasterizer stage to determine the renderable area on screen. You can use multiple viewports to implement split-screen multiplayer games.

The next set of variables that will be declared are specific to this demo and not generic for DirectX initialization.

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
// Vertex buffer data
ID3D11InputLayout* g_d3dInputLayout = nullptr;
ID3D11Buffer* g_d3dVertexBuffer = nullptr;
ID3D11Buffer* g_d3dIndexBuffer = nullptr;
// Shader data
ID3D11VertexShader* g_d3dVertexShader = nullptr;
ID3D11PixelShader* g_d3dPixelShader = nullptr;
|

The **g_d3dInputLayout** variable will be used to describe the order and type of data that is expected by the vertex shader.

The **g_d3dVertexBuffer** and **g_d3dIndexBuffer** variables will be used to store the vertex data and the index list that defines the geometry which will be rendered. The vertex buffer stores the data for each unique vertex in the geometry. In this demo, each vertex will store it’s position in 3D space and the color of the vertex. The index buffer stores a list of indices into the vertex buffer. The order of the indices in the index buffer determines the order that vertices in the vertex buffer are sent to the GPU for rendering.

For this simple demo, we will have two shaders, a vertex shader and a pixel shader. The **g_d3dVertexShader** variable will hold a reference to the vertex shader object and the **g_d3dPixelShader** will store a reference to the pixel shader.

Next we’ll declare set of buffers that will be used to update the constant variables that are declared in the vertex shader.

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
// Shader resources
enum ConstantBuffer
{
CB_Application,
CB_Frame,
CB_Object,
NumConstantBuffers
};
ID3D11Buffer* g_d3dConstantBuffers[NumConstantBuffers];
|

Here we declare three constant buffers. Constant buffers are used to store shader variables that remain constant during current draw call. An example of a constant shader variable is the camera’s projection matrix. Since the projection matrix will be the same for every vertex of the object, this variable does not need to be passed to the shader using vertex data. Instead, we declare a constant buffer that stores the projection matrix of the camera and this shader variable only needs to be updated when the camera’s projection matrix is modified (which is to say, not often).

-
**Application**: The application level constant buffer stores variables that rarely change. The contents of this constant buffer are being updated once during application startup and perhaps are not updated again. An example of an application level shader variable is the camera’s projection matrix. Usually the projection matrix is initialized once when the render window is created and only needs to be updated if the dimensions of the render window are changed (for example, if the window is resized). -
**Frame**: The frame level constant buffer stores variables that change each frame. An example of a frame level shader variable would be the camera’s view matrix which changes whenever the camera moves. This variable only needs to be updated once at the beginning of the render function and generally stays the same for all objects rendered that frame. -
**Object**: The object level constant buffer stores variables that are different for every object being rendered. An example of an object level shader variable is the object’s world matrix. Since each object in the scene will probably have a different world matrix this shader variable needs to be updated for every separate draw call.

This separation of shader variables is arbitrary and you can choose whatever method you would like to separate your constant buffers in your own shaders. Generally you should split up constant buffers in your shader based on the frequency the variables need to be updated.

The next set of variables define the variables that will be updated by the application and used to populate the variables in the constant buffers of the shader.

|
1
2
3
4
|
// Demo parameters
XMMATRIX g_WorldMatrix;
XMMATRIX g_ViewMatrix;
XMMATRIX g_ProjectionMatrix;
|

We will only draw a single object on the screen in this demo. For this reason, we only need to keep track of a single world matrix which will transform the object’s vertices into world space. The **g_WorldMatrix** is a 4×4 matrix which will be used to store the world matrix of the cube in our scene.

The **g_ViewMatrix** only needs to be updated once per frame and is used to store the camera’s view matrix that will transform the object’s vertices from world space into view space.

The **g_ProjectionMatrix** is updated once at the beginning of the application and is used to store the projection matrix of the camera. The projection matrix will transform the object’s vertices from view space into clip space (which is required by the rasterizer).

Next, we’ll define the geometry for the single object that will be rendered in our scene.

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
// Vertex data for a colored cube.
struct VertexPosColor
{
XMFLOAT3 Position;
XMFLOAT3 Color;
};
VertexPosColor g_Vertices[8] =
{
{ XMFLOAT3( -1.0f, -1.0f, -1.0f ), XMFLOAT3( 0.0f, 0.0f, 0.0f ) }, // 0
{ XMFLOAT3( -1.0f, 1.0f, -1.0f ), XMFLOAT3( 0.0f, 1.0f, 0.0f ) }, // 1
{ XMFLOAT3( 1.0f, 1.0f, -1.0f ), XMFLOAT3( 1.0f, 1.0f, 0.0f ) }, // 2
{ XMFLOAT3( 1.0f, -1.0f, -1.0f ), XMFLOAT3( 1.0f, 0.0f, 0.0f ) }, // 3
{ XMFLOAT3( -1.0f, -1.0f, 1.0f ), XMFLOAT3( 0.0f, 0.0f, 1.0f ) }, // 4
{ XMFLOAT3( -1.0f, 1.0f, 1.0f ), XMFLOAT3( 0.0f, 1.0f, 1.0f ) }, // 5
{ XMFLOAT3( 1.0f, 1.0f, 1.0f ), XMFLOAT3( 1.0f, 1.0f, 1.0f ) }, // 6
{ XMFLOAT3( 1.0f, -1.0f, 1.0f ), XMFLOAT3( 1.0f, 0.0f, 1.0f ) } // 7
};
WORD g_Indicies[36] =
{
0, 1, 2, 0, 2, 3,
4, 6, 5, 4, 7, 6,
4, 5, 1, 4, 1, 0,
3, 2, 6, 3, 6, 7,
1, 5, 6, 1, 6, 2,
4, 0, 3, 4, 3, 7
};
|

The **VertexPosColor** struct defines the properties of a single vertex. In this case the **Position** member variable will be used to store the position of the vertex in 3D space and the **Color** member variable will be used to store the red, green, and blue components of the vertex’s color.

The cube geometry that we will render consists of 8 unique vertices (one for each corner of the cube). We cannot simply send the cube geometry directly to the rendering pipeline as-is because the rendering pipeline only knows about points, lines, and triangles (not cubes, spheres, or any other complex shape). In order to create a set of triangles we need to define an index list which determines the order the vertices are sent to the GPU for rendering. In this case, each face of the cube consists of two triangles, an upper and a lower triangle. The first face of the triangle consists of six vertices: { {0, 1, 2}, {0, 2, 3} }. You will notice that in order to create the face, we will duplicate vertex 0, and 2.

When creating the index buffer for our geometry, we must also take the winding order of the vertices into consideration. The winding order of front-facing triangles is determined by the rasterizer state and we can specify that the winding order should be either clock-wise or counter-clockwise. This choice is arbitrary but it will have an impact on the order of the indices in the index buffer. For this demo, we will consider front-facing triangles to be in a clock-wise winding order. The diagram below shows the winding order for the first face of the cube.

The lower triangle of the face consists of vertices { 0, 1, 2 } and the upper triangle of the face consists of vertices { 0, 2, 3 }. The gray dashed line represents the triangle subdivision of the face.

The last part of the preamble is the function declarations.

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
// Forward declarations.
LRESULT CALLBACK WndProc (HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam);
template< class ShaderClass >
ShaderClass* LoadShader( const std::wstring& fileName, const std::string& entryPoint, const std::string& profile );
bool LoadContent();
void UnloadContent();
void Update( float deltaTime );
void Render();
void Cleanup();
|

The **WndProc** function is the function that will handle any mouse, keyboard, and window events that are sent to our application window.

The **LoadShader** template function will be used to load and compile a shader at runtime. It’s templated on the type of shader that is being loaded.

The **LoadContent**, and **UnloadContent** functions will load the demo specific resources such as the vertex buffer and index buffer GPU resources for our cube geometry.

The **Update** function will be used to update any logic required by our demo.

The **Render** function will render the scene.

The **Cleanup** function is used to release any DirectX specific resources like the device, device context, and swap chain.

The first thing our application will do is initialize and create the window. We will create a function called **InitApplication** for this purpose. First we’ll register a window class and then we’ll create a window using that window class.

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
/**
* Initialize the application window.
*/
int InitApplication( HINSTANCE hInstance, int cmdShow )
{
WNDCLASSEX wndClass = {0};
wndClass.cbSize = sizeof( WNDCLASSEX );
wndClass.style = CS_HREDRAW | CS_VREDRAW;
wndClass.lpfnWndProc = &WndProc;
wndClass.hInstance = hInstance;
wndClass.hCursor = LoadCursor( nullptr, IDC_ARROW );
wndClass.hbrBackground = (HBRUSH)(COLOR_WINDOW+1);
wndClass.lpszMenuName = nullptr;
wndClass.lpszClassName = g_WindowClassName;
if ( !RegisterClassEx(&wndClass) )
{
return -1;
}
|

The window class defines a set of attributes which define a window template. Each window your application creates must have a window class registered which is required to create the window.

The **WNDCLASSEX** structure has the following definition [[16]](https://www.3dgep.com#WNDCLASSEX):

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
typedef struct tagWNDCLASSEX {
UINT cbSize;
UINT style;
WNDPROC lpfnWndProc;
int cbClsExtra;
int cbWndExtra;
HINSTANCE hInstance;
HICON hIcon;
HCURSOR hCursor;
HBRUSH hbrBackground;
LPCTSTR lpszMenuName;
LPCTSTR lpszClassName;
HICON hIconSm;
} WNDCLASSEX, *PWNDCLASSEX;
|

And the members have the following definition:

-
**UINT cbSize**: The size, in bytes, of this structure. Set this member to sizeof(WNDCLASSEX). -
**UINT style**: The class style. In this case we use the**CS_HREDRAW**class style which causes the entire window to redraw if a movement or size adjustment changes the width of the client area and the**CS_VREDRAW**class style which causes the entire window to redraw if a movement or a size adjustment changes the height of the client area. -
**WNDPROC lpfnWndProc**: A pointer to the windows procedure that will handle window events for any windows created using this class. In this case we specify the yet undefined**WndProc**function which was declared earlier. -
**int cbClsExtra**: The number of extra bytes to allocate following the window-class structure. This parameter is not used here and should be set to 0. -
**int cpWndExtra**: The number of extra bytes to allocate following the window instance. This parameter is not used here and should be set to 0. -
**HINSTANCE hInstance**: A handle to the instance of the module that owns this window class. This module instance handle is passed to the**WinMain**function which will be shown later. -
**HICON hIcon**: A handle to the class icon. This icon will be used to represent a window created with this class in the task bar and in the top-left corner of the window’s title bar. You can load an icon from a resource file using the[LoadIcon](http://msdn.microsoft.com/en-us/library/windows/desktop/ms648072(v=vs.85).aspx)function. If this value is**NULL**(or**nullptr**) then the default application icon is used. -
**HCURSOR hCursor**: A handle to the class cursor. This must be a handle to a valid cursor resource. For this demo, we will use the default arrow icon by specifying**LoadCursor( nullptr, IDC_ARROW )**. -
**HBRUSH hbrBackground**: A handle to the class background brush. This member can be a handle to the brush to be used for painting the background, or it can be a color value. A color value must be one of the following standard system colors (the value 1 must be added to the chosen color). If a color value is given, you must convert it to one of the following**HBRUSH**types:**COLOR_ACTIVEBORDER****COLOR_ACTIVECAPTION****COLOR_APPWORKSPACE****COLOR_BACKGROUND****COLOR_BTNFACE****COLOR_BTNSHADOW****COLOR_BTNTEXT****COLOR_CAPTIONTEXT****COLOR_GRAYTEXT****COLOR_HIGHLIGHT****COLOR_HIGHLIGHTTEXT****COLOR_INACTIVEBORDER****COLOR_INACTIVECAPTION****COLOR_MENU****COLOR_MENUTEXT****COLOR_SCROLLBAR****COLOR_WINDOW****COLOR_WINDOWFRAME****COLOR_WINDOWTEXT**

-
**LPCTSTR lpszMenuName**: Pointer to a null-terminated character string that specifies the resource name of the class menu, as the name appears in the resource file. If this member is NULL, windows belonging to this class have no default menu. -
**LPCTSTR lpszClassName**: A pointer to a null-terminated const string which is used to uniquely identify this window class. This class name will be used to create the window instance. -
**HICON hIconSm**: A handle to a small icon that is associated with the window class. If this member is**NULL**(or nullptr), the system searches the icon resource specified by the**hIcon**member for an icon of the appropriate size to use as the small icon.

With the window class structure initialized, the window class is registered on line 114 using the [RegisterClassEx](http://msdn.microsoft.com/en-us/library/windows/desktop/ms633587(v=vs.85).aspx) function.

With the window class registered, we can create a window instance using this class.

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
RECT windowRect = { 0, 0, g_WindowWidth, g_WindowHeight };
AdjustWindowRect( &windowRect, WS_OVERLAPPEDWINDOW, FALSE );
g_WindowHandle = CreateWindowA( g_WindowClassName, g_WindowName,
WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT,
windowRect.right - windowRect.left,
windowRect.bottom - windowRect.top,
nullptr, nullptr, hInstance, nullptr );
if ( !g_WindowHandle )
{
return -1;
}
ShowWindow( g_WindowHandle, cmdShow );
UpdateWindow( g_WindowHandle );
return 0;
}
|

We want to create a window with a client area of **g_WindowWidth** by **g_WindowHeight** but if we create a window with those dimensions, the client are will be slightly smaller. In order to get a window with a client area the size we want, we can use the [AdjustWindowRect](http://msdn.microsoft.com/en-us/library/windows/desktop/ms632665(v=vs.85).aspx) function to adjust the inital window rectangle to account for the window style.

The window instance is created using the **CreateWindow** function. This function has the following signature [[18]](https://www.3dgep.com#CreateWindow):

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
HWND WINAPI CreateWindow(
_In_opt_ LPCTSTR lpClassName,
_In_opt_ LPCTSTR lpWindowName,
_In_ DWORD dwStyle,
_In_ int x,
_In_ int y,
_In_ int nWidth,
_In_ int nHeight,
_In_opt_ HWND hWndParent,
_In_opt_ HMENU hMenu,
_In_opt_ HINSTANCE hInstance,
_In_opt_ LPVOID lpParam
);
|

**_In_**,

**_Out_**,

**_Outptr_**,

**_Inout_**etc. macros are part of Microsoft’s Source-code Annotation Language (SAL)

[[17]](https://www.3dgep.com#SAL)and primarily used to describe how a function uses its prameters. Any annotation which includes

**_opt_**indicates that the parameter is optional and can be

**NULL**.

And the properties to this function have the following definition:

-
**LPCTSTR lpClassName**: The name of the window class to use as a template to create the window instance. The class name must match one of the classes that were previously registered using**RegisterClass**or**RegisterClassEx**and associated to the**hInstance**module. -
**LPCTSTR lpWindowName**: The name of the window instance. When creating a window with a title bar, the window name will be displayed in the title bar. -
**DWORD dwStyle**: The style of the window being created. This parameter can be a combination of any of the[window styles](http://msdn.microsoft.com/en-us/library/windows/desktop/ms632600(v=vs.85).aspx). -
**int x**: The initial horizontal position of the window. For an overlapped or pop-up window, the x parameter is the initial x-coordinate of the window’s upper-left corner, in screen coordinates. If this parameter is set to**CW_USEDEFAULT**, the system selects the default position for the window’s upper-left corner and ignores the y parameter. -
**int y**: The initial vertical position of the window. For an overlapped or pop-up window, the y parameter is the initial y-coordinate of the window’s upper-left corner, in screen coordinates. If an overlapped window is created with the**WS_VISIBLE**style bit set and the x parameter is set to**CW_USEDEFAULT**, then the y parameter determines how the window is shown. If the y parameter is**CW_USEDEFAULT**, then the window manager calls[ShowWindow](http://msdn.microsoft.com/en-us/library/windows/desktop/ms633548(v=vs.85).aspx)with the**SW_SHOW**flag after the window has been created. If the y parameter is some other value, then the window manager calls**ShowWindow**with that value as the**nCmdShow**parameter. -
**int nWidth**: The width, in device units, of the window. For overlapped windows, nWidth is either the window’s width, in screen coordinates, or**CW_USEDEFAULT**. If**nWidth**is**CW_USEDEFAULT**, the system selects a default width and height for the window; the default width extends from the initial x-coordinate to the right edge of the screen, and the default height extends from the initial y-coordinate to the top of the icon area.**CW_USEDEFAULT**is valid only for overlapped windows. In this case, we set the initial window width to the total width of the adjusted window rectangle. -
**int nHeight**: The height, in device units, of the window. For overlapped windows,**nHeight**is the window’s height, in screen coordinates. If**nWidth**is set to**CW_USEDEFAULT**, the system ignores**nHeight**. In this case, we set the initial window height to the total height of the adjusted window rectangle. -
**HWND hWndParent**: A handle to the parent window. Since we are creating a top-level window, this parameter can be**NULL**(or nullptr). -
**HMENU hMenu**: A handle to a window or NULL to use the menu that was specified in the window class template. If both the window class and this parameter are**NULL**, no menu will be created for this window. -
**HINSTANCE hInstance**: A handle to the instance of the module to be associated with the window. -
**LPVOID lpParam**: A pointer to a value to be passed to the window through the[CREATESTRUCT](http://msdn.microsoft.com/en-us/library/windows/desktop/ms632603(v=vs.85).aspx)structure (**lpCreateParams**member) pointed to by the lParam param of the[WM_CREATE](http://msdn.microsoft.com/en-us/library/windows/desktop/ms632619(v=vs.85).aspx)message. This message is sent to the created window by this function before it returns.

If the window creation succeeded, the window is shown with the [ShowWindow](http://msdn.microsoft.com/en-us/library/windows/desktop/ms633548(v=vs.85).aspx) function and the [UpdateWindow](http://msdn.microsoft.com/en-us/library/windows/desktop/dd145167(v=vs.85).aspx) function is called to force the client area of the window to be painted.

Before we continue, let’s take a look at what a minimum windows procedure function must contain.

The windows procedure function is the function that is assigned to the [WNDCLASSEX](http://msdn.microsoft.com/en-us/library/windows/desktop/ms633577(v=vs.85).aspx) structure’s **lpfnWndProc** member variable when we registered the window class. All windows created with with the same class will have the same window procedure function.

The purpose of the windows procedure callback function to to process messages sent to the window.

The windows procedure callback function has the following signature [[52]](https://www.3dgep.com#WindowProc):

|
1
2
3
4
5
6
|
LRESULT CALLBACK WindowProc(
_In_ HWND hwnd,
_In_ UINT uMsg,
_In_ WPARAM wParam,
_In_ LPARAM lParam
);
|

Where:

-
**HWND hwnd**: A handle to the window for which the event is intended. -
**UINT uMsg**: The event message. For lists of the system-provided messages, see[System-Defined Messages](http://msdn.microsoft.com/en-us/library/windows/desktop/ms644927(v=vs.85).aspx#system_defined). -
**WPARAM wParam**: Additional message information. The contents of this parameter depend on the value of the**uMsg**parameter. -
**LPARAM lParam**: Additional message information. The contents of this parameter depend on the value of the**uMsg**parameter.

The return value is the result of the message processing and depends on the message sent [[52]](https://www.3dgep.com#WindowProc).

For this demo, we will implement a minimum message handling function that only responds to the [WM_PAINT](http://msdn.microsoft.com/en-us/library/windows/desktop/dd145213(v=vs.85).aspx) and [WM_DESTROY](http://msdn.microsoft.com/en-us/library/windows/desktop/ms632620(v=vs.85).aspx) windows messages. All other messages will be handled by the [DefWindowProc](http://msdn.microsoft.com/en-us/library/windows/desktop/ms633572(v=vs.85).aspx) function.

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
LRESULT CALLBACK WndProc (HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam)
{
PAINTSTRUCT paintStruct;
HDC hDC;
switch ( message )
{
case WM_PAINT:
{
hDC = BeginPaint( hwnd, &paintStruct );
EndPaint( hwnd, &paintStruct );
}
break;
case WM_DESTROY:
{
PostQuitMessage( 0 );
}
break;
default:
return DefWindowProc( hwnd, message, wParam, lParam );
}
return 0;
}
|

At a minimum, the window procedure must respond to the [WM_PAINT](http://msdn.microsoft.com/en-us/library/windows/desktop/dd145213(v=vs.85).aspx) window message. We don’t actually do any rendering with this message except erase the window’s background contents using the window class’s background brush (**hbrBackground** variable of the [WNDCLASSEX](http://msdn.microsoft.com/en-us/library/windows/desktop/ms633577(v=vs.85).aspx) structure).

In order to close the window, we will also respond to the [WM_DESTROY](http://msdn.microsoft.com/en-us/library/windows/desktop/ms632620(v=vs.85).aspx) window message which simply calls the [PostQuitMessage](http://msdn.microsoft.com/en-us/library/windows/desktop/ms644945(v=vs.85).aspx) function which will be handled in **Run** function which we will define in the next section.

Before we can display the window, we need to create our main game loop. To execute the main game loop, we will create a **Run** function which will continue to execute until the user decides to quit (by pressing the big red cross on the top-right side of the window).

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
31
32
33
34
35
|
/**
* The main application loop.
*/
int Run()
{
MSG msg = {0};
static DWORD previousTime = timeGetTime();
static const float targetFramerate = 30.0f;
static const float maxTimeStep = 1.0f / targetFramerate;
while ( msg.message != WM_QUIT )
{
if ( PeekMessage( &msg, 0, 0, 0, PM_REMOVE ) )
{
TranslateMessage( &msg );
DispatchMessage( &msg );
}
else
{
DWORD currentTime = timeGetTime();
float deltaTime = ( currentTime - previousTime ) / 1000.0f;
previousTime = currentTime;
// Cap the delta time to the max time step (useful if your
// debugging and you don't want the deltaTime value to explode.
deltaTime = std::min<float>(deltaTime, maxTimeStep);
// Update( deltaTime );
// Render();
}
}
return static_cast<int>(msg.wParam);
}
|

The **Run** function will continue to execute indefinitely until the [WM_QUIT](http://msdn.microsoft.com/en-us/library/windows/desktop/ms632641(v=vs.85).aspx) window message is posted to the window’s message queue.

The [PeekMessage](http://msdn.microsoft.com/en-us/library/windows/desktop/ms644943(v=vs.85).aspx) function will retrieve the next message from the message queue. The **PM_REMOVE** indicates that the retrieved message should be removed from the window’s message queue. The [PeekMessage](http://msdn.microsoft.com/en-us/library/windows/desktop/ms644943(v=vs.85).aspx) function will return **FALSE** if there are no messages to process.

The [TranslateMessage](http://msdn.microsoft.com/en-us/library/windows/desktop/ms644955(v=vs.85).aspx) function will translate virtual-key messages into character messages [[53]](https://www.3dgep.com#TranslateMessage) and the [DispatchMessage](http://msdn.microsoft.com/en-us/library/windows/desktop/ms644934(v=vs.85).aspx) function will dispatch the message to the appropriate window’s procedure function [[54]](https://www.3dgep.com#DispatchMessage).

If there is no message to process, then we will call **Update** and **Render** which will update the game logic and render our scene. These functions are commented out now because they have not been defined yet.

When the game loop exits, the [MSG](http://msdn.microsoft.com/en-us/library/windows/desktop/ms644958(v=vs.85).aspx) structure’s **wParam** member will contain the return code which was specified as the only parameter to the [PostQuitMessage](http://msdn.microsoft.com/en-us/library/windows/desktop/ms644945(v=vs.85).aspx) in the **WndProc** function shown earlier.

Before we can execute our application, we must define the main entry point.

The main entry point for our application is the **wWinMain** function. In this function we will initialize the window and start the main game loop. When the game loop exits, the return code from **Run** method will be returned to the process that invoked our application.

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
|
int WINAPI wWinMain( HINSTANCE hInstance, HINSTANCE prevInstance, LPWSTR cmdLine, int cmdShow )
{
UNREFERENCED_PARAMETER( prevInstance );
UNREFERENCED_PARAMETER( cmdLine );
// Check for DirectX Math library support.
if ( !XMVerifyCPUSupport() )
{
MessageBox( nullptr, TEXT("Failed to verify DirectX Math library support."), TEXT("Error"), MB_OK );
return -1;
}
if( InitApplication(hInstance, cmdShow) != 0 )
{
MessageBox( nullptr, TEXT("Failed to create applicaiton window."), TEXT("Error"), MB_OK );
return -1;
}
int returnCode = Run();
return returnCode;
}
|

On line 747, the [XMVerifyCPUSupport](http://msdn.microsoft.com/en-us/library/microsoft.directx_sdk.utilities.xmverifycpusupport(v=vs.85).aspx) function will return **true** if the **DirectXMath** library is supported on the current platform.

The **InitApplication** function will create the main window and show it on screen.

The **Run** function will kick-off the main game loop and only returns control back to the main function when the user closes the main window.

If we run our application now, we should see an empty game window that looks similar to the image below.

It’s not very interesting to look at so let’s initialize a Direct3D 11.

In this function we will initialize the Direct3D 11 device, context and swap chain required for rendering graphics.

The process of initializing a Direct3D rendering device consists of several steps:

- Create the device and swap chain,
- Create a render target view of the swap chain’s back buffer,
- Create a texture for the depth-stencil buffer,
- Create a depth-stencil view from the depth-stencil buffer,
- Create a depth-stencil state object that defines the behaviour of the output merger stage,
- Create a rasterizer state object that defines the behaviour of the rasterizer stage.

To create the device and swap chain, we must first setup the swap chain description. The swap chain description defines the size and number of render buffers that will be used by the swap chain. It also associates the window to the swap chain which determines where the final image will be presented. The swap chain description also defines the quality of anti-aliasing (if any) that should be applied and how the back buffer is flipped during presentation.

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
/**
* Initialize the DirectX device and swap chain.
*/
int InitDirectX( HINSTANCE hInstance, BOOL vSync )
{
// A window handle must have been created already.
assert( g_WindowHandle != 0 );
RECT clientRect;
GetClientRect( g_WindowHandle, &clientRect );
// Compute the exact client dimensions. This will be used
// to initialize the render targets for our swap chain.
unsigned int clientWidth = clientRect.right - clientRect.left;
unsigned int clientHeight = clientRect.bottom - clientRect.top;
DXGI_SWAP_CHAIN_DESC swapChainDesc;
ZeroMemory( &swapChainDesc, sizeof(DXGI_SWAP_CHAIN_DESC) );
swapChainDesc.BufferCount = 1;
swapChainDesc.BufferDesc.Width = clientWidth;
swapChainDesc.BufferDesc.Height = clientHeight;
swapChainDesc.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;
swapChainDesc.BufferDesc.RefreshRate = QueryRefreshRate( clientWidth, clientHeight, vSync );
swapChainDesc.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;
swapChainDesc.OutputWindow = g_WindowHandle;
swapChainDesc.SampleDesc.Count = 1;
swapChainDesc.SampleDesc.Quality = 0;
swapChainDesc.SwapEffect = DXGI_SWAP_EFFECT_DISCARD;
swapChainDesc.Windowed = TRUE;
|

The **DXGI_SWAP_CHAIN_DESC** has the following definition [[19]](https://www.3dgep.com#DXGI_SWAP_CHAIN_DESC):

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
typedef struct DXGI_SWAP_CHAIN_DESC {
DXGI_MODE_DESC BufferDesc;
DXGI_SAMPLE_DESC SampleDesc;
DXGI_USAGE BufferUsage;
UINT BufferCount;
HWND OutputWindow;
BOOL Windowed;
DXGI_SWAP_EFFECT SwapEffect;
UINT Flags;
} DXGI_SWAP_CHAIN_DESC;
|

The members of the **DXGI_SWAP_CHAIN_DESC** struct are defined as:

-
**DXGI_MODE_DESC BufferDesc**: This parameter is a type[DXGI_MODE_DESC](http://msdn.microsoft.com/en-us/library/windows/desktop/bb173064(v=vs.85).aspx)and has the following members:-
**UINT Width**: A value that describes the resolution width. If you specify the width as zero when you call the[IDXGIFactory::CreateSwapChain](http://msdn.microsoft.com/en-us/library/windows/desktop/bb174537(v=vs.85).aspx)method to create a swap chain, the runtime obtains the width from the output window and assigns this width value to the swap-chain description. -
**UINT Height**: A value describing the resolution height. If you specify the height as zero when you call the[IDXGIFactory::CreateSwapChain](http://msdn.microsoft.com/en-us/library/windows/desktop/bb174537(v=vs.85).aspx)method to create a swap chain, the runtime obtains the height from the output window and assigns this height value to the swap-chain description. -
**DXGI_RATIONAL RefreshRate**: A[DXGI_RATIONAL](http://msdn.microsoft.com/en-us/library/windows/desktop/bb173069(v=vs.85).aspx)structure describing the refresh rate in hertz. We can use 0/1 to specify an unbounded refresh rate. This is useful if we don’t intend to synchronize the presentation of the scene with the refresh rate of the screen. If the window contents are to be displayed full-screen, then this should be the ideal refresh rate at the specified display resolution. If it is a windowed application, then it should be the refresh rate of the desktop. -
**DXGI_FORMAT Format**: The pixel format of the display. For a list of possible display formats see[DXGI_FORMAT](http://msdn.microsoft.com/en-us/library/windows/desktop/bb173059(v=vs.85).aspx). In this case we specify**DXGI_FORMAT_R8G8B8A8_UNORM**which creates a 4-component 32-bit unsigned normalized integer format that supports 8 bits per channel including alpha[[20]](https://www.3dgep.com#DXGI_FORMAT). -
**DXGI_MODE_SCANLINE_ORDER ScanlineOrdering**: Describes the scan-line drawing mode and can be one of the following values[[21]](https://www.3dgep.com#DXGI_MODE_SCANLINE_ORDER%20):-
**DXGI_MODE_SCANLINE_ORDER_UNSPECIFIED**(Default): The scanline order is unspecified. -
**DXGI_MODE_SCANLINE_ORDER_PROGRESSIVE**: The image is created from the first scanline to the last without skipping any. -
**DXGI_MODE_SCANLINE_ORDER_UPPER_FIELD_FIRST**: The image is created beginning with the upper field. -
**DXGI_MODE_SCANLINE_ORDER_LOWER_FIELD_FIRST**: The image is created beginning with the lower field.

-
-
**DXGI_MODE_SCALING Scaling**: This parameter describes the scaling mode and can be one of the following values[[22]](https://www.3dgep.com#DXGI_MODE_SCALING):-
**DXGI_MODE_SCALING_UNSPECIFIED**(Default): Unspecified scaling. -
**DXGI_MODE_SCALING_CENTERED**: Specifies no scaling. The image is centered on the display. This flag is typically used for a fixed-dot-pitch display (such as an LED display). -
**DXGI_MODE_SCALING_STRETCHED**: Specifies stretched scaling.

-

-
-
**DXGI_SAMPLE_DESC SampleDesc**: A**DXGI_SAMPLE_DESC**structure that describes multi-sampling parameters. The**DXGI_SAMPLE_DESC**structure has the following members[[23]](https://www.3dgep.com#DXGI_SAMPLE_DESC):-
**UINT Count**: The number of multisamples per pixel. -
**UINT Quality**: The image quality level. The higher the quality, the lower the performance. The valid range is between zero and one less than the level returned by[ID3D11Device::CheckMultisampleQualityLevels](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476499(v=vs.85).aspx). The default sampler mode, with no anti-aliasing, has a count of 1 and a quality level of 0.

-
-
**DXGI_USAGE BufferUsage**: A member of the**DXGI_USAGE**enumerated type that describes the surface usage and CPU access options for the back buffer. This parameter can be one of the following values[[24]](https://www.3dgep.com#DXGI_USAGE):-
**DXGI_USAGE_BACK_BUFFER**: The surface or resource is used as a back buffer. You don’t need to pass**DXGI_USAGE_BACK_BUFFER**when you create a swap chain. -
**DXGI_USAGE_READ_ONLY**: Use the surface or resource for reading only. -
**DXGI_USAGE_RENDER_TARGET_OUTPUT**: Use the surface or resource as an output render target. -
**DXGI_USAGE_SHADER_INPUT**: Use the surface or resource as an input to a shader. -
**DXGI_USAGE_SHARED**: Share the surface or resource. -
**DXGI_USAGE_UNORDERED_ACCESS**: Use the surface or resource for unordered access.

-
-
**UINT BufferCount**: A value that describes the number of buffers in the swap chain. -
**HWND OutputWindow**: An**HWND**handle to the output window. This member must not be**NULL**. -
**BOOL Windowed**: A Boolean value that specifies whether the output is in windowed mode. -
**DXGI_SWAP_EFFECT SwapEffect**: A member of the[DXGI_SWAP_EFFECT](http://msdn.microsoft.com/en-us/library/windows/desktop/bb173077(v=vs.85).aspx)enumerated type that describes options for handling the contents of the presentation buffer after presenting a surface. This parameter can have one of the following values[[25]](https://www.3dgep.com#DXGI_SWAP_EFFECT):-
**DXGI_SWAP_EFFECT_DISCARD**(Default): Use this flag to specify the bit-block transfer (bitblt) model and to specify that DXGI discard the contents of the back buffer after you call[IDXGISwapChain::Present](http://msdn.microsoft.com/en-us/library/windows/desktop/bb174576(v=vs.85).aspx). Use this flag to enable the display driver to select the most efficient presentation technique for the swap chain. -
**DXGI_SWAP_EFFECT_SEQUENTIAL**: Use this flag to specify the bitblt model and to specify that DXGI persist the contents of the back buffer after you call[IDXGISwapChain::Present](http://msdn.microsoft.com/en-us/library/windows/desktop/bb174576(v=vs.85).aspx). Use this option to present the contents of the swap chain in order, from the first buffer (buffer 0) to the last buffer. This flag cannot be used with multisampling.

-
-
**UINT Flags**: A member of the[DXGI_SWAP_CHAIN_FLAG](http://msdn.microsoft.com/en-us/library/windows/desktop/bb173076(v=vs.85).aspx)enumerated type that describes options for swap-chain behavior.

The **QueryRefreshRate** function is used to query the ideal refresh rate given the specified screen dimensions. If the **vSync** flag is **FALSE** then this function simply returns 0/1 which indicates that the screen should be refreshed as quickly as possible without waiting for a vertical sync. You can see the implementation of the **QueryRefreshRate** function by downloading the demo available at the end of this article.

With the swap chain description initialized, we can create both the swap chain object and the Direct3D 11 device at the same time.

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
UINT createDeviceFlags = 0;
#if _DEBUG
createDeviceFlags = D3D11_CREATE_DEVICE_DEBUG;
#endif
// These are the feature levels that we will accept.
D3D_FEATURE_LEVEL featureLevels[] =
{
D3D_FEATURE_LEVEL_11_1,
D3D_FEATURE_LEVEL_11_0,
D3D_FEATURE_LEVEL_10_1,
D3D_FEATURE_LEVEL_10_0,
D3D_FEATURE_LEVEL_9_3,
D3D_FEATURE_LEVEL_9_2,
D3D_FEATURE_LEVEL_9_1
};
// This will be the feature level that
// is used to create our device and swap chain.
D3D_FEATURE_LEVEL featureLevel;
HRESULT hr = D3D11CreateDeviceAndSwapChain( nullptr, D3D_DRIVER_TYPE_HARDWARE,
nullptr, createDeviceFlags, featureLevels, _countof(featureLevels),
D3D11_SDK_VERSION, &swapChainDesc, &g_d3dSwapChain, &g_d3dDevice, &featureLevel,
&g_d3dDeviceContext );
|

The **createDeviceFlags** is a bitfield that defines a set of special parameters that are used to create the device [[26]](https://www.3dgep.com#D3D11_CREATE_DEVICE_FLAG). In this case we specify the **D3D11_CREATE_DEVICE_DEBUG** flag to create a device that supports the [debug layer](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476881(v=vs.85).aspx#Debug). The debug layer provides additional checks for correctness and consistency and provides more robust feedback if we do something wrong. Adding this layer does incur some overhead so it is not recommended for production releases.

During device creation, we can specify which feature level we will support. The **featureLevels** array lists the various feature levels in order from the most desirable to least desirable. The device will be created with the highest feature level that is supported by the end-user’s hardware. To support the widest range of hardware, we will allow the feature level to fall back to 9_1 which provides support for devices as of DirectX 9. For a full list of feature levels and what they each support, see [Direct3D feature levels](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476876(v=vs.85).aspx). The **featureLevel** parameter defined on line 280 will contain the actual feature level that the Direct3D device was created with. We can also query the supported feature level of the device at a later time by using the [ID3D11Device::GetFeatureLevel](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476528(v=vs.85).aspx) method or use the [ID3D11Device::CheckFeatureSupport](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476497(v=vs.85).aspx) method to check for a specific feature.

On line 282 we use the [D3D11CreateDeviceAndSwapChain](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476083(v=vs.85).aspx) function to create the Direct3D device, context, and swap chain.

The [D3D11CreateDeviceAndSwapChain](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476083(v=vs.85).aspx) function has the following signature [[27]](https://www.3dgep.com#D3D11CreateDeviceAndSwapChain):

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
HRESULT D3D11CreateDeviceAndSwapChain(
_In_ IDXGIAdapter *pAdapter,
_In_ D3D_DRIVER_TYPE DriverType,
_In_ HMODULE Software,
_In_ UINT Flags,
_In_ const D3D_FEATURE_LEVEL *pFeatureLevels,
_In_ UINT FeatureLevels,
_In_ UINT SDKVersion,
_In_ const DXGI_SWAP_CHAIN_DESC *pSwapChainDesc,
_Out_ IDXGISwapChain **ppSwapChain,
_Out_ ID3D11Device **ppDevice,
_Out_ D3D_FEATURE_LEVEL *pFeatureLevel,
_Out_ ID3D11DeviceContext **ppImmediateContext
);
|

Which has the following properties:

-
**IDXGIAdapter *pAdapter**: A pointer to the video adapter to use when creating a device. Pass**NULL**(or**nullptr**) to use the default adapter, which is the first adapter enumerated by the[IDXGIFactory::EnumAdapters](http://msdn.microsoft.com/en-us/library/windows/desktop/bb174538(v=vs.85).aspx)method. -
**D3D_DRIVER_TYPE DriverType**: The Direct3D driver which implements the device. It must be one of the following values[[28]](https://www.3dgep.com#D3D_DRIVER_TYPE):-
**D3D_DRIVER_TYPE_UNKNOWN**: Unknown driver type. I’m not sure why or when you would ever use this value. -
**D3D_DRIVER_TYPE_HARDWARE**: A hardware driver, which implements Direct3D features in hardware. This is the primary driver that you should use in your Direct3D applications because it provides the best performance. -
**D3D_DRIVER_TYPE_REFERENCE**: A reference driver, which is a software implementation that supports every Direct3D feature. A reference driver is designed for accuracy rather than speed and as a result is slow but accurate. The rasterizer portion of the driver does make use of special CPU instructions whenever it can, but it is not intended for retail applications; use it only for feature testing, demonstration of functionality, debugging, or verifying bugs in other drivers. -
**D3D_DRIVER_TYPE_NULL**: A NULL driver, which is a reference driver without render capability. This driver is commonly used for debugging non-rendering API calls, it is not appropriate for retail applications. -
**D3D_DRIVER_TYPE_SOFTWARE**: A software driver, which is a driver implemented completely in software. The software implementation is not intended for a high-performance application due to its very slow performance. -
**D3D_DRIVER_TYPE_WARP**: A WARP driver, which is a high-performance software rasterizer. The rasterizer supports feature levels 9_1 through level 10_1 with a high performance software implementation. For information about limitations creating a WARP device on certain feature levels, see[Limitations Creating WARP and Reference Devices](http://msdn.microsoft.com/en-us/library/windows/desktop/ff728764(v=vs.85).aspx).

-
-
**HMODULE Software**: A handle to a DLL that implements a software rasterizer. The value should be non-**NULL**when**D3D_DRIVER_TYPE**is**D3D_DRIVER_TYPE_SOFTWARE**and**NULL**otherwise. -
**UINT Flags**: The runtime layers to enable (see[D3D11_CREATE_DEVICE_FLAG](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476107(v=vs.85).aspx)); values can be bitwise OR’d together. -
**const D3D_FEATURE_LEVEL *pFeatureLevels**: A pointer to an array of[D3D_FEATURE_LEVEL](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476329(v=vs.85).aspx)s, which determine the order of feature levels to attempt to create. -
**UINT FeatureLevels**: The number of elements in the**pFeatureLevels**array. -
**UINT SDKVersion**: The SDK version. Since we are using the DirectX 11 SDK, this value must always be**D3D11_SDK_VERSION**. -
**const DXGI_SWAP_CHAIN_DESC *pSwapChainDesc**: A pointer to a swap chain description which was created earlier. -
**IDXGISwapChain **ppSwapChain**: Returns the address of a pointer to the[IDXGISwapChain](http://msdn.microsoft.com/en-us/library/windows/desktop/bb174569(v=vs.85).aspx)object that represents the swap chain used for rendering. -
**ID3D11Device **ppDevice**: Returns the address of a pointer to an[ID3D11Device](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476379(v=vs.85).aspx)object that represents the device created. -
**D3D_FEATURE_LEVEL *pFeatureLevel**: Returns a pointer to a[D3D_FEATURE_LEVEL](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476329(v=vs.85).aspx), which represents the first element in an array of feature levels supported by the device. -
**ID3D11DeviceContext **ppImmediateContext**: Returns the address of a pointer to an[ID3D11DeviceContext](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476385(v=vs.85).aspx)object that represents the device context.

If we execute the [D3D11CreateDeviceAndSwapChain](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476083(v=vs.85).aspx) function on a computer with a video card driver that does not implement the Windows Display Driver Model version 1.2 ([WDDM 1.2](http://msdn.microsoft.com/en-us/library/windows/hardware/jj583805(v=vs.85).aspx)) or higher and we speicfy **D3D_FEATURE_LEVEL_11_1** in the feature levels array then this function will fail. The initial version of Windows 7 provided WDDM 1.1 which provides support for the **D3D_FEATURE_LEVEL_11_0** feature level and earlier but if we specify **D3D_FEATURE_LEVEL_11_1** then the **D3D11CreateDeviceAndSwapChain** function will fail. In fact, if you do not have the latest version of the Windows SDK, the **D3D_FEATURE_LEVEL_11_1** enumeration value may not even be defined and you won’t be able to compile this code. If this is the case for you, make sure you update Visual Studio 2012 to the latest version using the Windows Update utility. In the case this function does fail, we simply try again, but this time we remove the **D3D_FEATURE_LEVEL_11_1** value from the **featureLevels** array.

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
if ( hr == E_INVALIDARG )
{
hr = D3D11CreateDeviceAndSwapChain( nullptr, D3D_DRIVER_TYPE_HARDWARE,
nullptr, createDeviceFlags, &featureLevels[1], _countof(featureLevels) - 1,
D3D11_SDK_VERSION, &swapChainDesc, &g_d3dSwapChain, &g_d3dDevice, &featureLevel,
&g_d3dDeviceContext );
}
if ( FAILED(hr) )
{
return -1;
}
|

The **D3D11CreateDeviceAndSwapChain** function is invoked again, this time without the **D3D_FEATURE_LEVEL_11_1** enumeration value.

On line 295, we check again if it still failed. If this is the case then it is likely that there is no compatible hardware for any of the feature levels we are requesting. In that case you might want to try one of the other driver types such as **D3D_DRIVER_TYPE_WARP** but please consider [Limitations Creating WARP and Reference Devices](http://msdn.microsoft.com/en-us/library/windows/desktop/ff728764(v=vs.85).aspx) before trying this. I’ll leave this up to the reader to implement if they so desire.

If our program gets this far, then we have a valid **D3D11Device**, **D3D11DeviceContext**, and **DXGISwapChain** and we can continue to initialize the swap chain to prepare it for rendering graphics into.

The first step is to create a render target view from the swap chain’s back buffer.

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
// Next initialize the back buffer of the swap chain and associate it to a
// render target view.
ID3D11Texture2D* backBuffer;
hr = g_d3dSwapChain->GetBuffer( 0, __uuidof(ID3D11Texture2D), (LPVOID*)&backBuffer );
if ( FAILED( hr ) )
{
return -1;
}
hr = g_d3dDevice->CreateRenderTargetView( backBuffer, nullptr, &g_d3dRenderTargetView );
if ( FAILED( hr ) )
{
return -1;
}
SafeRelease( backBuffer );
|

On line 305, we use the swap chain’s **GetBuffer** method to retrieve a pointer to the swap chain’s single back buffer. The swap chain’s back buffer is automatically created based on the content of the **DXGI_SWAP_CHAIN_DESC** variable that we passed to the **D3D11CreateDeviceAndSwapChain** function so we do not need to manually create a texture for this purpose. However we do need to associate the backbuffer to a render target view in order to render to the swap chain’s back buffer.

A render target view is used by the Output Merger (OM) stage to draw the final colors emitted by the pixel shader. A render target view allows you to specify an area of a resource which is suitable for rendering to. For example, you can create a larger resource and specify that a smaller region of that larger resource be used as the render target for the output merger stage by creating a render target view of the smaller sub resource.

On line 311 the render target view is created from the entire **backBuffer** resource by using the **ID3D11Device::CreateRenderTargetView** method.

The **ID3D11Device::CreateRenderTargetView** has the following signature [[29]](https://www.3dgep.com#CreateRenderTargetView):

|
1
2
3
4
5
|
HRESULT CreateRenderTargetView(
[in] ID3D11Resource *pResource,
[in] const D3D11_RENDER_TARGET_VIEW_DESC *pDesc,
[out] ID3D11RenderTargetView **ppRTView
);
|

Where:

-
**ID3D11Resource *pResource**: Pointer to a[ID3D11Resource](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476584(v=vs.85).aspx)that represents a render target. This resource must have been created with the[D3D11_BIND_RENDER_TARGET](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476085(v=vs.85).aspx)flag. -
**const D3D11_RENDER_TARGET_VIEW_DESC *pDesc**: Pointer to a[D3D11_RENDER_TARGET_VIEW_DESC](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476201(v=vs.85).aspx)that represents a render-target view description. Set this parameter to**NULL**to create a view that accesses all of the subresources in mipmap level 0. -
**ID3D11RenderTargetView **ppRTView**: Address of a pointer to an[ID3D11RenderTargetView](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476582(v=vs.85).aspx). Set this parameter to**NULL**to validate the other input parameters (the method will return**S_FALSE**if the other input parameters pass validation).

In this case, because we want to create a render target view from the entire back buffer resource, we can pass **NULL** (or **nullptr**) for the 2nd parameter to this method.

After creating the render target view, we can release the reference to the back buffer texture. On line 317, the reference to the backBuffer COM object is released.

Although the swap chain is automatically created with a color buffer, we cannot start rendering 3D graphics until we have created a depth buffer and a depth stencil view to refer to that depth buffer. The depth buffer is necessary when drawing 3D graphics so that objects that are drawn far away from the viewer do not appear to be drawn on top of objects that appear close to the viewer regardless of the order in which they are rendered.

Let’s first create a 2D texture that will be used as a depth (and stencil) buffer.

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
|
// Create the depth buffer for use with the depth/stencil view.
D3D11_TEXTURE2D_DESC depthStencilBufferDesc;
ZeroMemory( &depthStencilBufferDesc, sizeof(D3D11_TEXTURE2D_DESC) );
depthStencilBufferDesc.ArraySize = 1;
depthStencilBufferDesc.BindFlags = D3D11_BIND_DEPTH_STENCIL;
depthStencilBufferDesc.CPUAccessFlags = 0; // No CPU access required.
depthStencilBufferDesc.Format = DXGI_FORMAT_D24_UNORM_S8_UINT;
depthStencilBufferDesc.Width = clientWidth;
depthStencilBufferDesc.Height = clientHeight;
depthStencilBufferDesc.MipLevels = 1;
depthStencilBufferDesc.SampleDesc.Count = 1;
depthStencilBufferDesc.SampleDesc.Quality = 0;
depthStencilBufferDesc.Usage = D3D11_USAGE_DEFAULT;
hr = g_d3dDevice->CreateTexture2D( &depthStencilBufferDesc, nullptr, &g_d3dDepthStencilBuffer );
if ( FAILED(hr) )
{
return -1;
}
|

To create the texture, we must first define a **D3D11_TEXTURE2D_DESC** variable that will be used to describe the texture we want to create.

The **D3D11_TEXTURE2D_DESC** structure has the following members [[30]](https://www.3dgep.com#D3D11_TEXTURE2D_DESC):

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
typedef struct D3D11_TEXTURE2D_DESC {
UINT Width;
UINT Height;
UINT MipLevels;
UINT ArraySize;
DXGI_FORMAT Format;
DXGI_SAMPLE_DESC SampleDesc;
D3D11_USAGE Usage;
UINT BindFlags;
UINT CPUAccessFlags;
UINT MiscFlags;
} D3D11_TEXTURE2D_DESC;
|

Where:

-
**UINT Width**: Texture width (in texels). This should be the same width as the swap chain’s back buffer. -
**UINT Height**: Texture height (in texels). This should be the same height as the swap chain’s back buffer. -
**UINT MipLevels**: The maximum number of mipmap levels in the texture. See the remarks in[D3D11_TEX1D_SRV](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476231(v=vs.85).aspx). Use 1 for a multisampled texture; or 0 to generate a full set of subtextures. -
**UINT ArraySize**: Number of textures in the texture array. For single textures, use 1. -
**DXGI_FORMAT Format**: The texture format. For this texture, we use**DXGI_FORMAT_D24_UNORM_S8_UINT**which is a 32-bit z-buffer format that supports 24 bits for depth and 8 bits for stencil. (See[DXGI_FORMAT](http://msdn.microsoft.com/en-us/library/windows/desktop/bb173059(v=vs.85).aspx)). -
**DXGI_SAMPLE_DESC SampleDesc**: Structure that specifies multisampling parameters for the texture. See[DXGI_SAMPLE_DESC](http://msdn.microsoft.com/en-us/library/windows/desktop/bb173072(v=vs.85).aspx). The value of the**SampleDesc**member should match the**SampleDesc**member of the[DXGI_SWAP_CHAIN_DESC](http://msdn.microsoft.com/en-us/library/windows/desktop/bb173075(v=vs.85).aspx)structure which was created earlier. -
**D3D11_USAGE Usage**: Value that identifies how the texture is to be read from and written to. It can be one of the following values[[31]](https://www.3dgep.com#D3D11_USAGE):-
**D3D11_USAGE_DEFAULT**(Default): A resource that requires read and write access by the GPU. This is likely to be the most common usage choice. -
**D3D11_USAGE_IMMUTABLE**: A resource that can only be read by the GPU. It cannot be written by the GPU, and cannot be accessed at all by the CPU. This type of resource must be initialized when it is created, since it cannot be changed after creation. -
**D3D11_USAGE_DYNAMIC**: A resource that is accessible by both the GPU (read only) and the CPU (write only). A dynamic resource is a good choice for a resource that will be updated by the CPU at least once per frame. To update a dynamic resource, use a**Map**method. -
**D3D11_USAGE_STAGING**: A resource that supports data transfer (copy) from the GPU to the CPU.

-
-
**UINT BindFlags**: Identifies how to bind a resource to the pipeline (see[D3D11_BIND_FLAG](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476085(v=vs.85).aspx)). In this case, we specify**D3D11_BIND_DEPTH_STENCIL**which indicates that this buffer is to be used as a depth-stencil target for the output-merger stage. -
**UINT CPUAccessFlags**: Specifies the types of CPU access allowed for a resource (see[D3D11_CPU_ACCESS_FLAG](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476106(v=vs.85).aspx)). This value can be**0**in which case no CPU access is required for the resource. -
**UINT MiscFlags**: Identifies additional options for resources (see[D3D11_RESOURCE_MISC_FLAG](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476203(v=vs.85).aspx)).

With the **D3D11_TEXTURE2D_DESC** variable configured, we can create the texture resource with the **ID3D11Device::CreateTexture2D** method. This method has the following signature [[32]](https://www.3dgep.com#CreateTexture2D):

|
1
2
3
4
5
|
HRESULT CreateTexture2D(
[in] const D3D11_TEXTURE2D_DESC *pDesc,
[in] const D3D11_SUBRESOURCE_DATA *pInitialData,
[out] ID3D11Texture2D **ppTexture2D
);
|

Where:

-
**const D3D11_TEXTURE2D_DESC *pDesc**: A pointer to a[D3D11_TEXTURE2D_DESC](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476253(v=vs.85).aspx)structure that describes a 2D texture resource. -
**const D3D11_SUBRESOURCE_DATA *pInitialData**: A pointer to an array of[D3D11_SUBRESOURCE_DATA](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476220(v=vs.85).aspx)structures that describe subresources for the 2D texture resource. If the resource is multisampled,**pInitialData**must be**NULL**because multisampled resources cannot be initialized with data when they are created. If the resource is created using the**D3D11_USAGE_IMMUTABLE**usage flag, then**pInitialData**must be valid and cannot be**NULL**. -
**ID3D11Texture2D **ppTexture2D**: A pointer to a buffer that receives a pointer to a ID3D11Texture2D interface for the created texture.

After we have created the depth/stencil buffer resource, we must create a **ID3D11DepthStencilView** before we can use this depth buffer for rendering. To do this, we will use the **ID3D11Device::CreateDepthStencilView** method.

|
1
2
3
4
5
|
hr = g_d3dDevice->CreateDepthStencilView( g_d3dDepthStencilBuffer, nullptr, &g_d3dDepthStencilView );
if ( FAILED(hr) )
{
return -1;
}
|

The **ID3D11Device::CreateDepthStencilView** method has the following signature [[33]](https://www.3dgep.com#CreateDepthStencilView):

|
1
2
3
4
5
|
HRESULT CreateDepthStencilView(
[in] ID3D11Resource *pResource,
[in] const D3D11_DEPTH_STENCIL_VIEW_DESC *pDesc,
[out] ID3D11DepthStencilView **ppDepthStencilView
);
|

Where:

-
**ID3D11Resource *pResource**: Pointer to the resource that will serve as the depth-stencil surface. This resource must have been created with the**D3D11_BIND_DEPTH_STENCIL**flag. -
**const D3D11_DEPTH_STENCIL_VIEW_DESC *pDesc**: Pointer to a depth-stencil-view description (see[D3D11_DEPTH_STENCIL_VIEW_DESC](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476112(v=vs.85).aspx)). Set this parameter to**NULL**to create a view that accesses mipmap level 0 of the entire resource (using the format the resource was created with). -
**ID3D11DepthStencilView **ppDepthStencilView**: Address of a pointer to an[ID3D11DepthStencilView](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476377(v=vs.85).aspx).

Similar to the color buffer of the swap chain, we want to create a depth-stencil-view of the entire resource. In this case, we can simply supply **NULL** (or **nullptr**) for the 2nd parameter to the **CreateDepthStencilView** method.

At this point we have initialized the render buffers that are used by our DirectX application. Next we need to create a depth/stencil state object which controls how depth-stencil testing is performed by the output-merger stage and a rasterizer state object which controls how the rasterizer stage behaves.

First let’s create the **ID3D11DepthStencilState** object. To do this, we first create a **D3D11_DEPTH_STENCIL_DESC** variable that describes the **ID3D11DepthStencilState** object.

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
// Setup depth/stencil state.
D3D11_DEPTH_STENCIL_DESC depthStencilStateDesc;
ZeroMemory( &depthStencilStateDesc, sizeof(D3D11_DEPTH_STENCIL_DESC) );
depthStencilStateDesc.DepthEnable = TRUE;
depthStencilStateDesc.DepthWriteMask = D3D11_DEPTH_WRITE_MASK_ALL;
depthStencilStateDesc.DepthFunc = D3D11_COMPARISON_LESS;
depthStencilStateDesc.StencilEnable = FALSE;
hr = g_d3dDevice->CreateDepthStencilState( &depthStencilStateDesc, &g_d3dDepthStencilState );
|

The **D3D11_DEPTH_STENCIL_DESC** is a structure with the following members [[34]](https://www.3dgep.com#D3D11_DEPTH_STENCIL_DESC):

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
typedef struct D3D11_DEPTH_STENCIL_DESC {
BOOL DepthEnable;
D3D11_DEPTH_WRITE_MASK DepthWriteMask;
D3D11_COMPARISON_FUNC DepthFunc;
BOOL StencilEnable;
UINT8 StencilReadMask;
UINT8 StencilWriteMask;
D3D11_DEPTH_STENCILOP_DESC FrontFace;
D3D11_DEPTH_STENCILOP_DESC BackFace;
} D3D11_DEPTH_STENCIL_DESC;
|

Where:

-
**BOOL DepthEnable**: Set to**TRUE**to enable depth testing, or set to**FALSE**to disable depth testing. -
**D3D11_DEPTH_WRITE_MASK DepthWriteMask**: Identify a portion of the depth-stencil buffer that can be modified by depth data. This variable can be one of the following values[[35]](https://www.3dgep.com#D3D11_DEPTH_WRITE_MASK):-
**D3D11_DEPTH_WRITE_MASK_ZERO**: Turn off writes to the depth-stencil buffer. -
**D3D11_DEPTH_WRITE_MASK_ALL**: Turn on writes to the depth-stencil buffer.

-
-
**D3D11_COMPARISON_FUNC DepthFunc**: A function that compares depth data against existing depth data. The function options are listed in[D3D11_COMPARISON_FUNC](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476101(v=vs.85).aspx). -
**BOOL StencilEnable**: Set to**TRUE**to enable stencil testing, or set to**FALSE**to disable stencil testing. -
**UINT8 StencilReadMask**: Identify a portion of the depth-stencil buffer for reading stencil data. -
**UINT8 StencilWriteMask**: Identify a portion of the depth-stencil buffer for writing stencil data. -
**D3D11_DEPTH_STENCILOP_DESC FrontFace**: Identify how to use the results of the depth test and the stencil test for pixels whose surface normal is facing towards the camera (see[D3D11_DEPTH_STENCILOP_DESC](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476109(v=vs.85).aspx)). -
**D3D11_DEPTH_STENCILOP_DESC BackFace**: Identify how to use the results of the depth test and the stencil test for pixels whose surface normal is facing away from the camera (see[D3D11_DEPTH_STENCILOP_DESC](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476109(v=vs.85).aspx)).

In this case, we enable depth testing and set the depth function to **D3D11_COMPARISON_LESS** which says that if the source data is less than the destination data (that is, the source data is closer to the eye), then the depth comparison passes.

If we wanted to render a transparent effect (such as a particle effect) but the transparent objects are not depth sorted, we would need to enable the depth test function so that the transparent object are still occluded by opaque object but disable depth writes by setting the **DepthWriteMask** member variable to **D3D11_DEPTH_WRITE_MASK_ZERO** so that the transparent objects do not occlude any other transparent objects.

Since we are not using the stencil testing for this demo, we simply set the **StencilEnable** flag to **FALSE** and forego setting any of the other stencil related variables.

With the **D3D11_DEPTH_STENCIL_DESC** structure setup, we can create the **ID3D11DepthStencilState** object using the **ID3D11Device::CreateDepthStencilState** method.

The **ID3D11Device::CreateDepthStencilState** method has the following signature [[36]](https://www.3dgep.com#CreateDepthStencilState):

|
1
2
3
4
|
HRESULT CreateDepthStencilState(
[in] const D3D11_DEPTH_STENCIL_DESC *pDepthStencilDesc,
[out] ID3D11DepthStencilState **ppDepthStencilState
);
|

Where:

-
**const D3D11_DEPTH_STENCIL_DESC *pDepthStencilDesc**: Pointer to a depth-stencil state description (see[D3D11_DEPTH_STENCIL_DESC](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476110(v=vs.85).aspx)). -
**ID3D11DepthStencilState **ppDepthStencilState**: Address of a pointer to the depth-stencil state object created (see[ID3D11DepthStencilState](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476375(v=vs.85).aspx)).

The final step in initializing the application for 3D rendering is setting up the rasterizer state object. Similar to the depth-stencil state object, we need to define a **D3D11_RASTERIZER_DESC** structure that defines how the rasterizer state object behaves.

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
// Setup rasterizer state.
D3D11_RASTERIZER_DESC rasterizerDesc;
ZeroMemory( &rasterizerDesc, sizeof(D3D11_RASTERIZER_DESC) );
rasterizerDesc.AntialiasedLineEnable = FALSE;
rasterizerDesc.CullMode = D3D11_CULL_BACK;
rasterizerDesc.DepthBias = 0;
rasterizerDesc.DepthBiasClamp = 0.0f;
rasterizerDesc.DepthClipEnable = TRUE;
rasterizerDesc.FillMode = D3D11_FILL_SOLID;
rasterizerDesc.FrontCounterClockwise = FALSE;
rasterizerDesc.MultisampleEnable = FALSE;
rasterizerDesc.ScissorEnable = FALSE;
rasterizerDesc.SlopeScaledDepthBias = 0.0f;
// Create the rasterizer state object.
hr = g_d3dDevice->CreateRasterizerState( &rasterizerDesc, &g_d3dRasterizerState );
if ( FAILED(hr) )
{
return -1;
}
|

The **D3D11_RASTERIZER_DESC** structure has the following members [[37]](https://www.3dgep.com#D3D11_RASTERIZER_DESC):

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
typedef struct D3D11_RASTERIZER_DESC {
D3D11_FILL_MODE FillMode;
D3D11_CULL_MODE CullMode;
BOOL FrontCounterClockwise;
INT DepthBias;
FLOAT DepthBiasClamp;
FLOAT SlopeScaledDepthBias;
BOOL DepthClipEnable;
BOOL ScissorEnable;
BOOL MultisampleEnable;
BOOL AntialiasedLineEnable;
} D3D11_RASTERIZER_DESC;
|

Where:

-
**D3D11_FILL_MODE FillMode**: Determines the fill mode to use when rendering and can be one of the following values[[38]](https://www.3dgep.com#D3D11_FILL_MODE):-
**D3D11_FILL_WIREFRAME**: Draw lines connecting the vertices. -
**D3D11_FILL_SOLID**: Fill the triangles formed by the vertices.

-
-
**D3D11_CULL_MODE CullMode**: Indicates triangles facing the specified direction are not drawn. This variable can have one of the following values[[39]](https://www.3dgep.com#D3D11_CULL_MODE):-
**D3D11_CULL_NONE**: Always draw all triangles. -
**D3D11_CULL_FRONT**: Do not draw triangles that are front-facing. -
**D3D11_CULL_BACK**: Do not draw triangles that are back-facing.

-
-
**BOOL FrontCounterClockwise**: Determines if a triangle is front- or back-facing. If this parameter is**TRUE**, a triangle will be considered front-facing if its vertices are counter-clockwise on the render target and considered back-facing if they are clockwise. If this parameter is**FALSE**, the opposite is true. -
**INT DepthBias**: Depth value added to a given pixel. For info about depth bias, see[Depth Bias](http://msdn.microsoft.com/en-us/library/windows/desktop/cc308048(v=vs.85).aspx). -
**FLOAT DepthBiasClamp**: Maximum depth bias of a pixel. For info about depth bias, see[Depth Bias](http://msdn.microsoft.com/en-us/library/windows/desktop/cc308048(v=vs.85).aspx). -
**FLOAT SlopeScaledDepthBias**: Scalar on a given pixel’s slope. For info about depth bias, see[Depth Bias](http://msdn.microsoft.com/en-us/library/windows/desktop/cc308048(v=vs.85).aspx). -
**BOOL DepthClipEnable**: Enable clipping based on distance.

The hardware always performs x and y clipping of rasterized coordinates. When**DepthClipEnable**is set to the default–**TRUE**, the hardware also clips the z value. When you set**DepthClipEnable**to**FALSE**, the hardware skips the z clipping. -
**BOOL ScissorEnable**: Enable scissor-rectangle culling. All pixels outside an active scissor rectangle are culled. Scissor rectangles can be specified using the[ID3D11DeviceContext::RSSetScissorRects](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476478(v=vs.85).aspx)method. -
**BOOL MultisampleEnable**: Specifies whether to use the quadrilateral or alpha line anti-aliasing algorithm on multisample antialiasing (MSAA) render targets. Set to**TRUE**to use the quadrilateral line anti-aliasing algorithm and to**FALSE**to use the alpha line anti-aliasing algorithm. -
**BOOL AntialiasedLineEnable**: Specifies whether to enable line antialiasing; only applies if doing line drawing and**MultisampleEnable**is**FALSE**.

With the **D3D11_RASTERIZER_DESC** structure filled in, we can create the **ID3D11RasterizerState** object using the **ID3D11Device::CreateRasterizerState** method.

The **ID3D11Device::CreateRasterizerState** method has the following signature [[40]](https://www.3dgep.com#CreateRasterizerState):

|
1
2
3
4
|
HRESULT CreateRasterizerState(
[in] const D3D11_RASTERIZER_DESC *pRasterizerDesc,
[out] ID3D11RasterizerState **ppRasterizerState
);
|

Where:

-
**const D3D11_RASTERIZER_DESC *pRasterizerDesc**: Pointer to a rasterizer state description. -
**ID3D11RasterizerState **ppRasterizerState**: Address of a pointer to the rasterizer state object created (see[ID3D11RasterizerState](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476580(v=vs.85).aspx)).

Although not strictly considered part of the Direct3D initialization phase, setting up a viewport definition is a necessary component of initializing the rasterizer stage. The viewport defines the area in screen space where our final render will go. For this application, we will be rendering to the entire client area of the application window but we could also define two viewports if we wanted to implement split screen multiplayer or a picture-in-picture effect.

To configure the viewport, we need to know the width and height of the client area. We have already computed the width and height of the client rectangle on lines 243-244 of the **InitDirectX** function and we used the client area to determine the size of the swap chain’s back buffer and the depth-stencil buffer. We will set the viewport to the same dimensions.

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
// Initialize the viewport to occupy the entire client area.
g_Viewport.Width = static_cast<float>(clientWidth);
g_Viewport.Height = static_cast<float>(clientHeight);
g_Viewport.TopLeftX = 0.0f;
g_Viewport.TopLeftY = 0.0f;
g_Viewport.MinDepth = 0.0f;
g_Viewport.MaxDepth = 1.0f;
return 0;
}
|

The **g_Viewport** global variable is of type **D3D11_VIEWPORT**. This structure has the following members [[41]](https://www.3dgep.com#D3D11_VIEWPORT):

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
typedef struct D3D11_VIEWPORT {
FLOAT TopLeftX;
FLOAT TopLeftY;
FLOAT Width;
FLOAT Height;
FLOAT MinDepth;
FLOAT MaxDepth;
} D3D11_VIEWPORT;
|

Where:

-
**FLOAT TopLeftX**: X position of the left hand side of the viewport. -
**FLOAT TopLeftY**: Y position of the top of the viewport. -
**FLOAT Width**: Width of the viewport. -
**FLOAT Height**: Height of the viewport. -
**FLOAT MinDepth**: Minimum depth of the viewport. Ranges between 0 and 1. -
**FLOAT MaxDepth**: Maximum depth of the viewport. Ranges between 0 and 1.

Now that we have initialized Direct3D, let’s update the **wWinMain** to include this change.

At this point we can update the main function to include the function to initialize Direct3D.

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
|
;" title="main.cpp"]
int WINAPI wWinMain( HINSTANCE hInstance, HINSTANCE prevInstance, LPWSTR cmdLine, int cmdShow )
{
UNREFERENCED_PARAMETER( prevInstance );
UNREFERENCED_PARAMETER( cmdLine );
// Check for DirectX Math library support.
if ( !XMVerifyCPUSupport() )
{
MessageBox( nullptr, TEXT("Failed to verify DirectX Math library support."), TEXT("Error"), MB_OK );
return -1;
}
if( InitApplication(hInstance, cmdShow) != 0 )
{
MessageBox( nullptr, TEXT("Failed to create applicaiton window."), TEXT("Error"), MB_OK );
return -1;
}
if ( InitDirectX(hInstance, g_EnableVSync) != 0 )
{
MessageBox( nullptr, TEXT("Failed to create DirectX device and swap chain."), TEXT("Error"), MB_OK );
return -1;
}
int returnCode = Run();
return returnCode;
}
|

If we run the application again, we will still only see a blank window because we still haven’t rendered anything onto the screen.

Up until now, we have only seen the generic initialization code that is required for a minimum Direct3D application. Next we will look at the initialization code that is specific for this particular demo. Before we do that, I would like to diverge to the subject of shaders. First we will create a simple vertex shader and pixel shader that we can use to render our geometry.

Up until DirectX 9, the Direct3D API featured a fixed-function pipeline. Using the fixed-function pipeline the graphics programmer was not required to write shaders. As of DirectX 10, the fixed-function pipeline has been deprecated and replaced by a programmable shader pipeline. The minimum required shaders for a DirectX 10 or newer application are a vertex shader and a pixel shader. The vertex shader is responsible for transforming the incoming vertex position into clip-space as required by the rasterizer stage and the pixel shader is responsible for computing the final pixel color from the interpolated vertex attributes.

The shader language for DirectX is called High Level Shading Language (**HLSL**). HLSL is a C-like (and C++-like as of shader model 5.0) programming language that has support for variables, structs (and interfaces and classes as of shader model 5.0), functions, and various flow control constructs such as if, for, while, do, and switch.

HLSL has another kind of language syntax which is not used in C or C++ programming called **semantics**. A semantic is a name which is associated to a shader input or output variable. Semantics are required on all variables that are passed between shader stages. In the generic case, the value of the semantic is arbitrary. The only requirement is that there is a matching semantic associated to an output variable in the source shader stage with an input variable in the destination shader stage. For example, the vertex shader might declare an output variable called **out_color** of type **float4** which is associated to the **COLOR** semantic and the pixel shader declares an input variable called **in_color** of type **float4** which is also associated to the **COLOR** semantic. This will cause the value of the **out_color** variable declared in the vertex shader to be connected to the value of the **in_color** variable in the pixel shader.

We will also use semantics to bind the geometry coming from the application to the input assembler and vertex shader stages in the following sections.

Besides these generic semantics, HLSL also defines a set of System-Value semantics [[42]](https://www.3dgep.com#SystemValueSemantics) which you can associate to input and output variables that have a special meaning to the rendering pipeline. All system-value semantics begin with a **SV_** prefix such as **SV_Position**. As an example, the **SV_Position** system-value semantic is used to associate a float4 output variable from the vertex shader with the homogeneous clip-space position required by the rasterizer.

For more information on HLSL syntax, please refer to the MSDN documentation on [HLSL Language Syntax](http://msdn.microsoft.com/en-us/library/windows/desktop/bb509615(v=vs.85).aspx).

Since the vertex shader stage comes first in the rendering pipeline, let’s take a look at the vertex shader first.

The vertex shader consumes vertex attributes from the Input Assembler stage and transforms the vertex position into homogeneous clip-space for the rasterizer stage. The vertex shader can also manipulate other vertex attributes (for example shift and scale texture coordinates) but this is optional in a vertex shader.

The input to the vertex shader is the object-space vertex position and any other vertex attributes that are passed by the application. At a minimum, We need to transform the object-space vertex position into homogeneous clip-space for use by the rasterizer. To perform this transformation, we will multiply the object-space vertex position by the model-view-projection matrix. The model-view-projection matrix is a combination of the geometry’s world matrix, the camera’s view matrix, and the camera’s projection matrix. We will need to pass these matrices to the vertex shader to perform the transformation. We will use constant buffers to store the matrices based on the frequency at which they are updated. Let’s see how we do this.

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
cbuffer PerApplication : register( b0 )
{
matrix projectionMatrix;
}
cbuffer PerFrame : register( b1 )
{
matrix viewMatrix;
}
cbuffer PerObject : register( b2 )
{
matrix worldMatrix;
}
|

First we declare three constant buffers using the **cbuffer** type. Each constant buffer is assigned to constant buffer registers by supplying the **b** register type. Explicitly assigning the constant buffer registers in this way is optional as the shader compiler will do this anyways if we don’t explicitly assign the registers but doing this provides more control over the placement of the buffers.

You will notice that we split the 3 matrices according to how frequently the matrix is updated. The projection matrix is usually updated when the application is started (in this demo anyways) and the view matrix is updated once per frame and the world matrix is updated for each separate object that will be rendered using this shader. By separating the variables in this way, we can reduce the amount of data that must be sent over the GPU bus. Of course this is an example showing the use of constant buffers. In your own shaders, you may want to compute the combined model-view-projection matrix in the application and only update a single uniform matrix variable in the shader.

Next we need to define a set of variables that will be passed from the application to the vertex shader. For this purpose, we will define a structure that will contain all of the input attributes for the vertex.

|
1
2
3
4
5
|
struct AppData
{
float3 position : POSITION;
float3 color: COLOR;
};
|

The **AppData** struct is used to encapsulate all of the vertex attributes that are sent from the application (the code to map vertex attributes from the application to varying shader variables will be shown later). These are the varying input variables to the vertex shader.

Here we also see the first use of semantics. The **position** variable has the **POSITION** semantic and the color variable has the **COLOR** semantic. We will use these semantics to connect the application variables to the shader variables.

Similar to the input variables, we will define a struct which encapsulates the output variables. These variables are sent from the vertex shader to the pixel shader.

|
1
2
3
4
5
|
struct VertexShaderOutput
{
float4 color : COLOR;
float4 position : SV_POSITION;
};
|

The **VertexShaderOutput** defines the variables that will be output from the vertex shader. At a minimum, the vertex shader must output a **float4** variable bound to the **SV_Position** system-value semantic as this is required by the rasterizer stage.

The **color** variable is bound to the **COLOR** semantic. The pixel shader will also need a matching **float4** input variable which is bound to the **COLOR** semantic to allow this variable to pass from the vertex shader stage to the pixel shader stage. In order for the color variable in the vertex shader to be correctly bound to the matching variable in the pixel shader, not only does the semantics need to match but the register they are bound to must also match. For this reason, I placed the **color** variable before the **position** variable in the **VertexShaderOutput** structure. This way, the first register will be assigned to the **color** variable in both the vertex shader and the pixel shader (as we will see briefly).

Now let’s see the entry point function of the vertex shader.

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
VertexShaderOutput SimpleVertexShader( AppData IN )
{
VertexShaderOutput OUT;
matrix mvp = mul( projectionMatrix, mul( viewMatrix, worldMatrix ) );
OUT.position = mul( mvp, float4( IN.position, 1.0f ) );
OUT.color = float4( IN.color, 1.0f );
return OUT;
}
|

The **SimpleVertexShader** function is the entry point for the vertex shader program. It takes an **AppData** struct variable as input and returns a **VertexShaderOutput** struct as output.

On line 32, the combined model-view-projection matrix is computed by multiplying the projection, view, and world matrix together. You will notice that we are post-multiplying the world matrix by the view matrix and the model-view matrix by the projection matrix. If you have done some programming with DirectX in the past, you may have used row-major matrix order in which case you would have swapped the order of multiplications. Since DirectX 10, the default order for matrices in HLSL is column-major so we will stick to this convention in this demo and future DirectX demos.

Using column-major matrices means that we have to post-multiply the vertex position by the model-view-projection matrix to correctly transform the vertex position from object-space to homogeneous clip-space.

On line 34 the vertex color is simply passed as-is to pixel shader.

Next we will create a pixel shader that will be used to determine the final pixel color of our geometry.

The pixel shader for this demo is even simpler than the vertex shader. In this case we simply output the color value passed from the vertex shader to the currently bound render target by returning a value that is bound to the **SV_Target** system value semantic.

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
struct PixelShaderInput
{
float4 color : COLOR;
};
float4 SimplePixelShader( PixelShaderInput IN ) : SV_TARGET
{
return IN.color;
}
|

The **PixelShaderInput** struct defines the input variables that we expect to be passed from the vertex shader stage. In this case, we only need the color value from the vertex shader which was bound to the **COLOR** semantic. We don’t need the **position** variable which was bound to the **SV_Position** system-value semantic because that variable was only required by the rasterizer stage.

Now that we have defined the shaders we need to use them in our application. Before we can use them we must compile these shaders into a format that the GPU can understand. We can chose to precompile the shaders in the application’s compilation phase or we can load the HLSL shaders at runtime and compile them “on-the-fly”.

If we compile the shaders with the compilation phase of our application then we can distribute our shaders with the application in a pre-compiled format and we can load the shaders faster because they don’t require compilation during the loading of the application.

If we decide to compile the shaders at runtime then we may get noticeably slower load times if we have a lot of shaders to compile but we have more control over how the shader is loaded based on runtime logic.

As of Visual Studio 2012, files with the **hlsl** extension that are added to your project will be compiled by the **FXC.exe** HLSL shader compiler during the compilation phase of your project. The shader code can be compiled either into a byte array that you can include directly in your source code or you can compile to a compiled shader file which you can load at runtime.

Add the **SimpleVertexShader.hlsl** file and the **SimplePixelShader.hlsl** file to your project.

Right-click the **SimpleVertexShader.hlsl** file in the solution explorer and select Properties from the pop-up menu that appears.

For both Debug and Release builds, select the **HLSL Compiler > General** options and set the **Entrypoint Name** property to **SimpleVertexShader** to match the name of the entry point function defined in the shader.

Set the **Shader Type** to **Vertex Shader (/vs)** and set the **Shader Model** to the shader model you want to support.

Select the **HLSL Compiler > Output Files** node.

The **Header Variable Name** property determines the name of the global variable that is declared in the header file which is used to refer to the compiled byte array of your shader.

The **Header File Name** determines the location of the header file where the compiled shader byte array will be written to. The location of this property is relative to the folder where your project file is located.

The **Object File Name** determines the location of the the file that contains the compiled shader object file is written to.

Follow these steps for the pixel shader as well.

You do not need to specify both the **Header File Name** and the **Object File Name** because you will usually only use one or the other. In the next section I will show how you can use either of these options to load the precompiled shader object in the application.

The other way to compile your shaders is to compile them at runtime. Using this method requires the d3dcompiler runtime to be distributed with your application and if you are building a DirectX application for the Windows App store then you should not use this method. This method should only be used to test and debug your shaders or if you do not intend to distribute your DirectX application on the Windows App store and you don’t mind the extra load time of compiling your shaders at runtime.

To load the shader at runtime, we will define a template function called **LoadShader** to load a shader from a file path. Since the loading of the shader object is similar regardless of the type of the shader except for a few lines of code, the LoadShader function will be templated on the type of shader object we are loading.

We will probably also want to take the feature level of the end-users graphics hardware into consideration when loading our shaders. If the end-users computer only supports feature level 10_0 we should not try to compile our shaders using Shader Model 5.0. The **GetLatestProfile** template function will return the latest shader profile based on the feature level of the end-users computer.

First let’s declare the **GetLatestProfile** template function.

|
1
2
3
|
// Get the latest profile for the specified shader type.
template< class ShaderClass >
std::string GetLatestProfile();
|

Next we will specialize this function based on the vertex shader type.

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
31
32
33
34
35
36
37
38
39
40
41
|
template<>
std::string GetLatestProfile<ID3D11VertexShader>()
{
assert( g_d3dDevice );
// Query the current feature level:
D3D_FEATURE_LEVEL featureLevel = g_d3dDevice->GetFeatureLevel();
switch( featureLevel )
{
case D3D_FEATURE_LEVEL_11_1:
case D3D_FEATURE_LEVEL_11_0:
{
return "vs_5_0";
}
break;
case D3D_FEATURE_LEVEL_10_1:
{
return "vs_4_1";
}
break;
case D3D_FEATURE_LEVEL_10_0:
{
return "vs_4_0";
}
break;
case D3D_FEATURE_LEVEL_9_3:
{
return "vs_4_0_level_9_3";
}
break;
case D3D_FEATURE_LEVEL_9_2:
case D3D_FEATURE_LEVEL_9_1:
{
return "vs_4_0_level_9_1";
}
break;
} // switch( featureLevel )
return "";
}
|

This version of the template function returns the latest vertex shader profile that can be used to compile the vertex shader given the specific feature level supported by the end-user’s hardware.

And we will also provide a specialization for the pixel shader type.

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
31
32
33
34
35
36
37
38
39
|
template<>
std::string GetLatestProfile<ID3D11PixelShader>()
{
assert( g_d3dDevice );
// Query the current feature level:
D3D_FEATURE_LEVEL featureLevel = g_d3dDevice->GetFeatureLevel();
switch( featureLevel )
{
case D3D_FEATURE_LEVEL_11_1:
case D3D_FEATURE_LEVEL_11_0:
{
return "ps_5_0";
}
break;
case D3D_FEATURE_LEVEL_10_1:
{
return "ps_4_1";
}
break;
case D3D_FEATURE_LEVEL_10_0:
{
return "ps_4_0";
}
break;
case D3D_FEATURE_LEVEL_9_3:
{
return "ps_4_0_level_9_3";
}
break;
case D3D_FEATURE_LEVEL_9_2:
case D3D_FEATURE_LEVEL_9_1:
{
return "ps_4_0_level_9_1";
}
break;
}
return "";
}
|

This version of the function returns the latest pixel shader profile that can be used to compile the pixel shader.

Feel free to implement template specializations for the geometry shader, hull shader and domain shader types. Keep in mind that geometry shaders are only supported as of feature level 10_0 and hull and domain shaders are only supported as of feature level 11_0 [[43]](https://www.3dgep.com#FeatureLevels).

Another function that should be specialized based on the shader type is a function that will create a shader object based on the shader type. This is the only part of the **LoadShader** function that is different depending on what kind of shader is being loaded.

First we will define a template function that will create the shader object.

|
1
2
|
template< class ShaderClass >
ShaderClass* CreateShader( ID3DBlob* pShaderBlob, ID3D11ClassLinkage* pClassLinkage );
|

The **CreateShader** template function takes a binary object and the class linkage object and creates the appropriate shader object.

First let’s specialize this template function on the [ID3D11VertexShader](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476641(v=vs.85).aspx) type.

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
template<>
ID3D11VertexShader* CreateShader<ID3D11VertexShader>( ID3DBlob* pShaderBlob, ID3D11ClassLinkage* pClassLinkage )
{
assert( g_d3dDevice );
assert( pShaderBlob );
ID3D11VertexShader* pVertexShader = nullptr;
g_d3dDevice->CreateVertexShader( pShaderBlob->GetBufferPointer(), pShaderBlob->GetBufferSize(), pClassLinkage, &pVertexShader );
return pVertexShader;
}
|

This function uses the [ID3D11Device::CreateVertexShader](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476524(v=vs.85).aspx) method to create the vertex shader object.

Next, we’ll specialize on the [ID3D11PixelShader](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476576(v=vs.85).aspx) shader type.

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
template<>
ID3D11PixelShader* CreateShader<ID3D11PixelShader>( ID3DBlob* pShaderBlob, ID3D11ClassLinkage* pClassLinkage )
{
assert( g_d3dDevice );
assert( pShaderBlob );
ID3D11PixelShader* pPixelShader = nullptr;
g_d3dDevice->CreatePixelShader( pShaderBlob->GetBufferPointer(), pShaderBlob->GetBufferSize(), pClassLinkage, &pPixelShader );
return pPixelShader;
}
|

Clearly this version of the template function is not much different than that of the vertex shader type except in the method that is used to create the shader object but we needed to do this to simplify the functionality of the **LoadShader** function which I will show next.

The **LoadShader** template function takes the file path to a HLSL shader file, the entry point function in that file, and a compatible profile to compile the shader to and returns the initialized shader object.

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
template< class ShaderClass >
ShaderClass* LoadShader( const std::wstring& fileName, const std::string& entryPoint, const std::string& _profile )
{
ID3DBlob* pShaderBlob = nullptr;
ID3DBlob* pErrorBlob = nullptr;
ShaderClass* pShader = nullptr;
std::string profile = _profile;
if ( profile == "latest" )
{
profile = GetLatestProfile<ShaderClass>();
}
|

The **LoadShader** function accepts the profile to use to compile the shader but we can also use the special value **“latest”** profile value which specifies that the latest profile for the current feature level should be used.

The next step is to compile the HLSL shader into a Binary Large Object (BLOB) using the [D3DCompileFromFile](http://msdn.microsoft.com/en-us/library/windows/desktop/hh446872(v=vs.85).aspx) function.

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
|
UINT flags = D3DCOMPILE_ENABLE_STRICTNESS;
#if _DEBUG
flags |= D3DCOMPILE_DEBUG;
#endif
HRESULT hr = D3DCompileFromFile( fileName.c_str(), nullptr,
D3D_COMPILE_STANDARD_FILE_INCLUDE, entryPoint.c_str(), profile.c_str(),
flags, 0, &pShaderBlob, &pErrorBlob );
if ( FAILED( hr ) )
{
if ( pErrorBlob )
{
std::string errorMessage = (char*)pErrorBlob->GetBufferPointer();
OutputDebugStringA( errorMessage.c_str() );
SafeRelease(pShaderBlob);
SafeRelease(pErrorBlob);
}
return false;
}
|

The **D3DCompileFromFile** function has the following signature [[44]](https://www.3dgep.com#D3DCompileFromFile):

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
HRESULT WINAPI D3DCompileFromFile(
in LPCWSTR pFileName,
in_opt const D3D_SHADER_MACRO *pDefines,
in_opt ID3DInclude *pInclude,
in LPCSTR pEntrypoint,
in LPCSTR pTarget,
in UINT Flags1,
in UINT Flags2,
out ID3DBlob **ppCode,
out_opt ID3DBlob **ppErrorMsgs
);
|

Where:

-
**LPCWSTR pFileName**: A pointer to a constant null-terminated string that contains the name of the file that contains the shader code. -
**const D3D_SHADER_MACRO *pDefines**: An optional array of[D3D_SHADER_MACRO](http://msdn.microsoft.com/en-us/library/windows/desktop/ff728732(v=vs.85).aspx)structures that define shader macros. Each macro definition contains a name and a NULL-terminated definition. If not used, set to**NULL**. -
**ID3DInclude *pInclude**: An optional pointer to an[ID3DInclude](http://msdn.microsoft.com/en-us/library/windows/desktop/ff728746(v=vs.85).aspx)interface that the compiler uses to handle include files. If you set this parameter to**NULL**and the shader contains a**#include**directive, a compile error occurs. You can pass the**D3D_COMPILE_STANDARD_FILE_INCLUDE**macro, which is a pointer to a default include handler. This default include handler includes files that are relative to the current directory. -
**LPCSTR pEntrypoint**: A pointer to a constant null-terminated string that contains the name of the shader entry point function where shader execution begins. -
**LPCSTR pTarget**: A pointer to a constant null-terminated string that specifies the shader target or set of shader features to compile against. The shader target can be a shader model (for example, shader model 2, shader model 3, shader model 4, or shader model 5 and later). The target can also be an effect type (for example, fx_4_1). For info about the targets that various profiles support, see[Specifying Compiler Targets](http://msdn.microsoft.com/en-us/library/windows/desktop/jj215820(v=vs.85).aspx). -
**UINT Flags1**: A combination of shader[compile options](http://msdn.microsoft.com/en-us/library/windows/desktop/gg615083(v=vs.85).aspx)that are combined by using a bitwise OR operation. The resulting value specifies how the compiler compiles the HLSL code. -
**UINT Flags2**: A combination of[effect compile options](http://msdn.microsoft.com/en-us/library/windows/desktop/gg615084(v=vs.85).aspx)that are combined by using a bitwise OR operation. The resulting value specifies how the compiler compiles the effect. When you compile a shader and not an effect file,**D3DCompileFromFile**ignores**Flags2**and should be set to 0. -
**ID3DBlob **ppCode**: A pointer to a variable that receives a pointer to the[ID3DBlob](http://msdn.microsoft.com/en-us/library/windows/desktop/ff728743(v=vs.85).aspx)interface that you can use to access the compiled code. -
**ID3DBlob **ppErrorMsgs**: An optional pointer to a variable that receives a pointer to the[ID3DBlob](http://msdn.microsoft.com/en-us/library/windows/desktop/ff728743(v=vs.85).aspx)interface that you can use to access compiler error messages, or**NULL**if there are no errors.

If the shader compilation fails, (which is likely to happen if our shader contains a syntax error) [D3DCompileFromFile](http://msdn.microsoft.com/en-us/library/windows/desktop/hh446872(v=vs.85).aspx) returns a [Direct3D 11 error code](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476174(v=vs.85).aspx) and we can use the error blob to determine the error that occured. The [OutputDebugString](http://msdn.microsoft.com/en-us/library/windows/desktop/aa363362(v=vs.85).aspx) function can be used to send the error message directly to the Visual Studio debug log.

At this point we only have the shader blob but we still need to create a shader object from the binary blob object. We can use the **CreateShader** template function we defined earlier.

|
1
2
3
4
5
6
7
|
pShader = CreateShader<ShaderClass>( pShaderBlob, nullptr );
SafeRelease( pShaderBlob );
SafeRelease( pErrorBlob );
return pShader;
}
|

The compiled shader object is now ready for use by the rendering pipeline.

Now that we have seen two simple HLSL shaders and we have compiled and loaded the shaders into shader objects let’s put them to good use in our application.

The **LoadContent** function will be used to load demo specific content. The content that should be loaded in this function would be shaders that are specific to the demo, geometry that will be rendered in the scene, and textures or any other resources that are specific to this particular demo.

In the **LoadContent** function, we’ll create two buffers. The first buffer will contain the vertex data that defines the geometry that will be rendered on the screen. The second buffer will contain the index data that defines the order to send the vertex data to the GPU for rendering.

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
bool LoadContent()
{
assert( g_d3dDevice );
// Create an initialize the vertex buffer.
D3D11_BUFFER_DESC vertexBufferDesc;
ZeroMemory( &vertexBufferDesc, sizeof(D3D11_BUFFER_DESC) );
vertexBufferDesc.BindFlags = D3D11_BIND_VERTEX_BUFFER;
vertexBufferDesc.ByteWidth = sizeof( VertexPosColor ) * _countof(g_Vertices);
vertexBufferDesc.CPUAccessFlags = 0;
vertexBufferDesc.Usage = D3D11_USAGE_DEFAULT;
D3D11_SUBRESOURCE_DATA resourceData;
ZeroMemory( &resourceData, sizeof(D3D11_SUBRESOURCE_DATA) );
resourceData.pSysMem = g_Vertices;
HRESULT hr = g_d3dDevice->CreateBuffer( &vertexBufferDesc, &resourceData, &g_d3dVertexBuffer );
if ( FAILED(hr) )
{
return false;
}
|

To create a buffer we need two things; a [D3D11_BUFFER_DESC](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476092(v=vs.85).aspx) structure that describes the buffer we are creating and a [D3D11_SUBRESOURCE_DATA](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476220(v=vs.85).aspx) structure that defines the data to initialize the buffer with.

The [D3D11_BUFFER_DESC](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476092(v=vs.85).aspx) structure has the following definition [[45]](https://www.3dgep.com#D3D11_BUFFER_DESC):

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
typedef struct D3D11_BUFFER_DESC {
UINT ByteWidth;
D3D11_USAGE Usage;
UINT BindFlags;
UINT CPUAccessFlags;
UINT MiscFlags;
UINT StructureByteStride;
} D3D11_BUFFER_DESC;
|

Where:

-
**UINT ByteWidth**: The size of the buffer in bytes. -
**D3D11_USAGE Usage**: Identify how the buffer is expected to be read from and written to. Frequency of update is a key factor. The most common value is typically**D3D11_USAGE_DEFAULT**; see[D3D11_USAGE](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476259(v=vs.85).aspx)for all possible values. -
**UINT BindFlags**: Identify how the buffer will be bound to the pipeline (see[D3D11_BIND_FLAG](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476085(v=vs.85).aspx)). Since this is a vertex buffer we specify the**D3D11_BIND_VERTEX_BUFFER**which allows this buffer to be bound as a vertex buffer to the input-assembler stage. -
**UINT CPUAccessFlags**: CPU access flags (see[D3D11_CPU_ACCESS_FLAG](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476106(v=vs.85).aspx)) or 0 if no CPU access is necessary. -
**UINT MiscFlags**: Miscellaneous flags (see[D3D11_RESOURCE_MISC_FLAG](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476203(v=vs.85).aspx)) or 0 if unused. -
**UINT StructureByteStride**: The size of each element in the buffer structure (in bytes) when the buffer represents a structured buffer. For more info about structured buffers, see[Structured Buffer](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476335(v=vs.85).aspx#Structured_Buffer).

The [D3D11_SUBRESOURCE_DATA](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476220(v=vs.85).aspx) structure is used to specify the data that is used to initialize a buffer when it is created.

The [D3D11_SUBRESOURCE_DATA](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476220(v=vs.85).aspx) structure has the following definition [[46]](https://www.3dgep.com#D3D11_SUBRESOURCE_DATA):

|
1
2
3
4
5
|
typedef struct D3D11_SUBRESOURCE_DATA {
const void *pSysMem;
UINT SysMemPitch;
UINT SysMemSlicePitch;
} D3D11_SUBRESOURCE_DATA;
|

Where:

-
**const void *pSysMem**: A pointer to the data to initialize the buffer with. -
**UINT SysMemPitch**: The distance (in bytes) from the beginning of one line of a texture to the next line. System-memory pitch is used only for 2D and 3D texture data as it is has no meaning for the other resource types. -
**UINT SysMemSlicePitch**: The distance (in bytes) from the beginning of one depth level to the next. System-memory-slice pitch is only used for 3D texture data as it has no meaning for the other resource types.

On line 406, we set the **pSysMem** member of the **resourceData** variable to the **g_Vertices** array which was defined in the main preamble.

The [ID3D11Device::CreateBuffer](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476501(v=vs.85).aspx) method is used to create the vertex buffer which can be bound to the input-assembler stage to render the cube geometry.

The [ID3D11Device::CreateBuffer](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476501(v=vs.85).aspx) method has the following signature [[47]](https://www.3dgep.com#CreateBuffer):

|
1
2
3
4
5
|
HRESULT CreateBuffer(
[in] const D3D11_BUFFER_DESC *pDesc,
[in, optional] const D3D11_SUBRESOURCE_DATA *pInitialData,
[out, optional] ID3D11Buffer **ppBuffer
);
|

Where:

-
**const D3D11_BUFFER_DESC *pDesc**: A pointer to a[D3D11_BUFFER_DESC](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476092(v=vs.85).aspx)structure that describes the buffer. -
**const D3D11_SUBRESOURCE_DATA *pInitialData**: A pointer to a[D3D11_SUBRESOURCE_DATA](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476220(v=vs.85).aspx)structure that describes the initialization data; use**NULL**to allocate space only (with the exception that it cannot be**NULL**if the usage flag is**D3D11_USAGE_IMMUTABLE**). -
**ID3D11Buffer **ppBuffer**: Address of a pointer to the[ID3D11Buffer](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476351(v=vs.85).aspx)interface for the buffer object created.

Next, we’ll create an index buffer using a similar method.

Similar to the vertex buffer, we’ll use the [ID3D11Device::CreateBuffer](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476501(v=vs.85).aspx) method to create and initialize the index buffer. The only difference between the vertex buffer and the index buffer is the bind flags of the index buffer will be [D3D11_BIND_INDEX_BUFFER](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476085(v=vs.85).aspx) and the data that is used to initialize the buffer.

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
// Create and initialize the index buffer.
D3D11_BUFFER_DESC indexBufferDesc;
ZeroMemory( &indexBufferDesc, sizeof(D3D11_BUFFER_DESC) );
indexBufferDesc.BindFlags = D3D11_BIND_INDEX_BUFFER;
indexBufferDesc.ByteWidth = sizeof(WORD) * _countof(g_Indicies);
indexBufferDesc.CPUAccessFlags = 0;
indexBufferDesc.Usage = D3D11_USAGE_DEFAULT;
resourceData.pSysMem = g_Indicies;
hr = g_d3dDevice->CreateBuffer( & indexBufferDesc, &resourceData, &g_d3dIndexBuffer );
if ( FAILED(hr) )
{
return false;
}
|

Now we need to define the three constant buffers that will be used to store the constant uniform variables used in the vertex shader.

Creating the constant buffers is very similar to creating the vertex and index buffers expect will will only initialize the size of the constant buffers but not the contents of the constant buffers. The contents of these constant buffers will be initialized later.

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
// Create the constant buffers for the variables defined in the vertex shader.
D3D11_BUFFER_DESC constantBufferDesc;
ZeroMemory( &constantBufferDesc, sizeof(D3D11_BUFFER_DESC) );
constantBufferDesc.BindFlags = D3D11_BIND_CONSTANT_BUFFER;
constantBufferDesc.ByteWidth = sizeof( XMMATRIX );
constantBufferDesc.CPUAccessFlags = 0;
constantBufferDesc.Usage = D3D11_USAGE_DEFAULT;
hr = g_d3dDevice->CreateBuffer( &constantBufferDesc, nullptr, &g_d3dConstantBuffers[CB_Application] );
if ( FAILED(hr) )
{
return false;
}
hr = g_d3dDevice->CreateBuffer( &constantBufferDesc, nullptr, &g_d3dConstantBuffers[CB_Frame] );
if ( FAILED(hr) )
{
return false;
}
hr = g_d3dDevice->CreateBuffer( &constantBufferDesc, nullptr, &g_d3dConstantBuffers[CB_Object] );
if ( FAILED(hr) )
{
return false;
}
|

In this case, we specify **D3D11_BIND_CONSTANT_BUFFER** for the bind flags of the constant buffers and we use **nullptr** for the **D3D11_SUBRESOURCE_DATA** parameter to just allocate memory for the buffer but not initialize that memory.

Since we will need to update the contents of the constant buffer in the application, you may be tempted to set the buffer’s **Usage** property to **D3D11_USAGE_DYNAMIC** and the **CPUAccessFlags** to **D3D11_CPU_ACCESS_WRITE**. You must resist this temptation! Later we will update the contents of this buffer using the [ID3D11DeviceContext::UpdateSubresource](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476486(v=vs.85).aspx) method and this method expects constant buffers to be initialized with **D3D11_USAGE_DEFAULT** usage flag and buffers that are created with the **D3D11_USAGE_DEFAULT** flag must have their **CPUAccessFlags** set to 0.

Each of these three constant buffers only contains a single 4×4 matrix but a constant buffer may contain any number of matrices, vectors, or scalars. The only requirement is that the constant buffer is created the same size as the constant buffer defined in the shader in which it is used.

Now let’s load some shaders.

As mentioned in the [Compiling Shaders](https://www.3dgep.com#Compiling_Shaders) section, there are several ways to load the shader at runtime.

- Load and compile the shader at runtime.
- Load a precompiled shader object.
- Create a shader from a byte array.

We can use the [LoadShader](https://www.3dgep.com#Load_a_Shader) template function described earlier to load and compile the HLSL shaders at runtime.

|
1
2
3
|
// Load the shaders
g_d3dVertexShader = LoadShader<ID3D11VertexShader>( L"../data/shaders/SimpleVertexShader.hlsl", "SimpleVertexShader", "latest" );
g_d3dPixelShader = LoadShader<ID3D11PixelShader>( L"../data/shaders/SimplePixelShader.hlsl", "SimplePixelShader", "latest" );
|

If we want to load a precompiled shader object, we can use the [D3DReadFileToBlob](http://msdn.microsoft.com/en-us/library/windows/desktop/hh446877(v=vs.85).aspx) function to load the precompiled shader directly to a [ID3DBlob](http://msdn.microsoft.com/en-us/library/windows/desktop/ff728743(v=vs.85).aspx) interface.

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
// Load the compiled vertex shader.
ID3DBlob* vertexShaderBlob;
#if _DEBUG
LPCWSTR compiledVertexShaderObject = L"SimpleVertexShader_d.cso";
#else
LPCWSTR compiledVertexShaderObject = L"SimpleVertexShader.cso";
#endif
hr = D3DReadFileToBlob( compiledVertexShaderObject, &vertexShaderBlob );
if ( FAILED(hr) )
{
return false;
}
hr = g_d3dDevice->CreateVertexShader( vertexShaderBlob->GetBufferPointer(), vertexShaderBlob->GetBufferSize(), nullptr, &g_d3dVertexShader );
if ( FAILED( hr ) )
{
return false;
}
|

How to create the compiled shader object (.cso) was explained in the [Precompiled Shaders](https://www.3dgep.com#Precompiled_Shaders) section of this article.

And the final method which is probably the easiest and most portable way to load a precompiled shader is to load the shader from a byte array. The FXC.exe compiler can write the definition of the byte array to a header file which can be included in the application and use the byte array to create the shader. Suppose we configured the shader compiler to output the byte array for the vertex shader into a global variable named **g_SimpleVertexShader** and the byte array for the pixel shader into a global variable named **g_SimplePixelShader** then we could load the shaders in this way:

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
hr = g_d3dDevice->CreateVertexShader( g_SimpleVertexShader, sizeof(g_SimpleVertexShader), nullptr, &g_d3dVertexShader );
if ( FAILED( hr ) )
{
return false;
}
hr = g_d3dDevice->CreatePixelShader( g_SimplePixelShader, sizeof(g_SimplePixelShader), nullptr, &g_d3dPixelShader );
if ( FAILED( hr ) )
{
return false;
}
|

Now that we have seen multiple methods for loading a shader, we need to define an [ID3D11InputLayout](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476575(v=vs.85).aspx) interface object which maps the vertex buffer elements to the varying vertex attributes in the vertex shader.

The [ID3D11InputLayout](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476575(v=vs.85).aspx) interface is used to define how the vertex data attached to the input-assembler stage is layed out in memory. An instance of the [ID3D11InputLayout](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476575(v=vs.85).aspx) interface object is created using the [ID3D11Device::CreateInputLayout](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476512(v=vs.85).aspx) method. This method has the following signature [[48]](https://www.3dgep.com#CreateInputLayout):

|
1
2
3
4
5
6
7
|
HRESULT CreateInputLayout(
[in] const D3D11_INPUT_ELEMENT_DESC *pInputElementDescs,
[in] UINT NumElements,
[in] const void *pShaderBytecodeWithInputSignature,
[in] SIZE_T BytecodeLength,
[out] ID3D11InputLayout **ppInputLayout
);
|

Where:

-
**const D3D11_INPUT_ELEMENT_DESC *pInputElementDescs**: An array of the input-assembler stage input data types; each type is described by an element description (see[D3D11_INPUT_ELEMENT_DESC](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476180(v=vs.85).aspx)). This structure will be described in the next section. -
**UINT NumElements**: The number of input elements in the**pInputElementDescs**array. -
**const void *pShaderBytecodeWithInputSignature**: A pointer to the compiled shader. The compiled shader code contains a input signature which is validated against the array of elements. -
**SIZE_T BytecodeLength**: The size in bytes of the**pShaderBytecodeWithInputSignature**array. -
**ID3D11InputLayout **ppInputLayout**: A pointer to the input-layout object created (see[ID3D11InputLayout](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476575(v=vs.85).aspx)).

The input-layout is created from an array of [D3D11_INPUT_ELEMENT_DESC](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476180(v=vs.85).aspx) structures. Each element in the array describes a single element of the vertex buffer that is bound to the input-assembler stage.

The **D3D11_INPUT_ELEMENT_DESC** structure has the following definition [[49]](https://www.3dgep.com#D3D11_INPUT_ELEMENT_DESC):

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
typedef struct D3D11_INPUT_ELEMENT_DESC {
LPCSTR SemanticName;
UINT SemanticIndex;
DXGI_FORMAT Format;
UINT InputSlot;
UINT AlignedByteOffset;
D3D11_INPUT_CLASSIFICATION InputSlotClass;
UINT InstanceDataStepRate;
} D3D11_INPUT_ELEMENT_DESC;
|

Where:

-
**LPCSTR SemanticName**: The HLSL semantic associated with this element in a shader input-signature. -
**UINT SemanticIndex**: The semantic index for the element. A semantic index modifies a semantic, with an integer index number. A semantic index is only needed in a case where there is more than one element with the same semantic. -
**DXGI_FORMAT Format**: The data type of the element data. See[DXGI_FORMAT](http://msdn.microsoft.com/en-us/library/windows/desktop/bb173059(v=vs.85).aspx). For example, if the element describes a 4-component floating point vector, the**Format**flag would be set to**DXGI_FORMAT_R32G32B32A32_FLOAT**. -
**UINT InputSlot**: If using a single vertex buffer with interleaved vertex attributes then the input slot should always be 0. If using several packed vertex buffers where each vertex buffer contains the vertex data for a single vertex attribute, then the input slot is the index of the vertex buffer that is attached to the input assembler stage. -
**UINT AlignedByteOffset**: Offset (in bytes) between each element. Use**D3D11_APPEND_ALIGNED_ELEMENT**for convenience to define the current element directly after the previous one, including any packing if necessary. -
**D3D11_INPUT_CLASSIFICATION InputSlotClass**: Identifies the input data class for a single input slot. This member can have one of the following values[[50]](https://www.3dgep.com#D3D11_INPUT_CLASSIFICATION):-
**D3D11_INPUT_PER_VERTEX_DATA**: Input data is per-vertex data. -
**D3D11_INPUT_PER_INSTANCE_DATA**: Input data is per-instance data.

-
-
**UINT InstanceDataStepRate**: The number of instances to draw using the same per-instance data before advancing in the buffer by one element. This value must be 0 for an element that contains per-vertex data (the slot class is set to**D3D11_INPUT_PER_VERTEX_DATA**).

Armed with this information, we can define the **D3D11_INPUT_ELEMENT_DESC** array that defines the layout of our vertex data and create the [ID3D11InputLayout](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476575(v=vs.85).aspx) object.

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
// Create the input layout for the vertex shader.
D3D11_INPUT_ELEMENT_DESC vertexLayoutDesc[] =
{
{ "POSITION", 0, DXGI_FORMAT_R32G32B32_FLOAT, 0, offsetof(VertexPosColor,Position), D3D11_INPUT_PER_VERTEX_DATA, 0 },
{ "COLOR", 0, DXGI_FORMAT_R32G32B32_FLOAT, 0, offsetof(VertexPosColor,Color), D3D11_INPUT_PER_VERTEX_DATA, 0 }
};
hr = g_d3dDevice->CreateInputLayout( vertexLayoutDesc, _countof(vertexLayoutDesc), vertexShaderBlob->GetBufferPointer(), vertexShaderBlob->GetBufferSize(), &g_d3dInputLayout );
if ( FAILED(hr) )
{
return false;
}
SafeRelease( vertexShaderBlob );
|

The vertex buffer for our cube geometry contains two attributes; the vertex position and the vertex color. Both the vertex position and the vertex color are passed to the vertex shader as a 3-component 32-bit floating-point vector. Since both attributes are stored interleaved in a single vertex buffer (instead of storing each attribute packed in separate vertex buffers) they both use the first (0) input slot. Since both of these attributes describe per-vertex (as apposed to per-instance) attributes, they use the **D3D11_INPUT_PER_VERTEX_DATA** input classification.

On line 489, the input layout object is created using the layout description.

With the input layout object created, we no longer need the shader blob so on line 495, the shader blob is released.

The pixel shader is loaded in a similar way to the vertex shader but there is no need to define the input layout for the pixel shader. The pixel shader is loaded from a precompiled shader object.

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
// Load the compiled pixel shader.
ID3DBlob* pixelShaderBlob;
#if _DEBUG
LPCWSTR compiledPixelShaderObject = L"SimplePixelShader_d.cso";
#else
LPCWSTR compiledPixelShaderObject = L"SimplePixelShader.cso";
#endif
hr = D3DReadFileToBlob( compiledPixelShaderObject, &pixelShaderBlob );
if ( FAILED(hr) )
{
return false;
}
hr = g_d3dDevice->CreatePixelShader( pixelShaderBlob->GetBufferPointer(), pixelShaderBlob->GetBufferSize(), nullptr, &g_d3dPixelShader );
if ( FAILED( hr ) )
{
return false;
}
SafeRelease( pixelShaderBlob );
|

This code snippet is very similar to the vertex shader loading so it will not be explained in detail.

One final thing we can do in the **LoadContent** method for this demo is setup the projection matrix and update the constant buffer that stores the value of the projection matrix in the shader.

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
// Setup the projection matrix.
RECT clientRect;
GetClientRect( g_WindowHandle, &clientRect );
// Compute the exact client dimensions.
// This is required for a correct projection matrix.
float clientWidth = static_cast<float>( clientRect.right - clientRect.left );
float clientHeight = static_cast<float>( clientRect.bottom - clientRect.top );
g_ProjectionMatrix = XMMatrixPerspectiveFovLH( XMConvertToRadians(45.0f), clientWidth/clientHeight, 0.1f, 100.0f );
g_d3dDeviceContext->UpdateSubresource( g_d3dConstantBuffers[CB_Appliation], 0, nullptr, &g_ProjectionMatrix, 0, 0 );
return true;
}
|

On line 528, the projection matrix is computed from the [XMMatrixPerspectiveFovLH](http://msdn.microsoft.com/en-us/library/microsoft.directx_sdk.matrix.xmmatrixperspectivefovlh(v=vs.85).aspx) function and on line 530 the contents of the projection matrix are copied into the per-appliction constant buffer using the [ID3D11DeviceContext::UpdateSubresource](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476486(v=vs.85).aspx) method.

The [ID3D11DeviceContext::UpdateSubresource](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476486(v=vs.85).aspx) method has the following signature [[51]](https://www.3dgep.com#UpdateSubresource):

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
void UpdateSubresource(
[in] ID3D11Resource *pDstResource,
[in] UINT DstSubresource,
[in] const D3D11_BOX *pDstBox,
[in] const void *pSrcData,
[in] UINT SrcRowPitch,
[in] UINT SrcDepthPitch
);
|

Where:

-
**ID3D11Resource *pDstResource**: A pointer to the destination resource (see[ID3D11Resource](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476584(v=vs.85).aspx)). -
**UINT DstSubresource**: A zero-based index, that identifies the destination subresource. See[D3D11CalcSubresource](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476081(v=vs.85).aspx)for more details. -
**const D3D11_BOX *pDstBox**: A pointer to a box that defines the portion of the destination subresource to copy the resource data into. Coordinates are in bytes for buffers and in texels for textures. If NULL, the data is written to the destination subresource with no offset. The dimensions of the source must fit the destination (see[D3D11_BOX](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476089(v=vs.85).aspx)). -
**const void *pSrcData**: A pointer to the source data in memory. -
**UINT SrcRowPitch**: The size of one row of the source data. -
**UINT SrcDepthPitch**: The size of one depth slice of source data.

For a shader-constant buffer; set **pDstBox** to **NULL**. It is not possible to use this method to partially update a shader-constant buffer [[51]](https://www.3dgep.com#UpdateSubresource).

Now that we have loaded the content that will be used by our demo, let’s implement the update and render functions so that we can see something interesting on the screen.

First we’ll implement the update function. This function doesn’t do much except setup the camera’s view matrix and create a rotation matrix for our cube.

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
void Update( float deltaTime )
{
XMVECTOR eyePosition = XMVectorSet( 0, 0, -10, 1 );
XMVECTOR focusPoint = XMVectorSet( 0, 0, 0, 1 );
XMVECTOR upDirection = XMVectorSet( 0, 1, 0, 0 );
g_ViewMatrix = XMMatrixLookAtLH( eyePosition, focusPoint, upDirection );
g_d3dDeviceContext->UpdateSubresource( g_d3dConstantBuffers[CB_Frame], 0, nullptr, &g_ViewMatrix, 0, 0 );
static float angle = 0.0f;
angle += 90.0f * deltaTime;
XMVECTOR rotationAxis = XMVectorSet( 0, 1, 1, 0 );
g_WorldMatrix = XMMatrixRotationAxis( rotationAxis, XMConvertToRadians(angle) );
g_d3dDeviceContext->UpdateSubresource( g_d3dConstantBuffers[CB_Object], 0, nullptr, &g_WorldMatrix, 0, 0 );
}
|

On lines 807-810 we setup the view matrix by placing the camera 10 units back looking towards the origin.

On line 810, the constant buffer which is used to store the view matrix is updated using the same method used to update the projection matrix.

On line 814-818 we create a rotation matrix that is used to rotate the cube and on line 819 the constant buffer that stores the object’s world matrix is updated using the same method that was used to update the view matrix and the projection matrix.

Before we can render we will define two helper functions. The first will clear the render target, and the depth and stencil buffers and the second will be used to present the contents of the swap chain’s back buffer to the screen.

Before we can start rendering a new frame, we must clear the old contents of the back buffer and the depth/stencil buffers.

|
1
2
3
4
5
6
|
// Clear the color and depth buffers.
void Clear( const FLOAT clearColor[4], FLOAT clearDepth, UINT8 clearStencil )
{
g_d3dDeviceContext->ClearRenderTargetView( g_d3dRenderTargetView, clearColor );
g_d3dDeviceContext->ClearDepthStencilView( g_d3dDepthStencilView, D3D11_CLEAR_DEPTH|D3D11_CLEAR_STENCIL, clearDepth, clearStencil );
}
|

The [ID3D11DeviceContext::ClearRenderTargetView](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476388(v=vs.85).aspx) method is used to clear the back buffer to a particlular color and the [ID3D11DeviceContext::ClearDepthStencilView](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476387(v=vs.85).aspx) method is used to clear the depth and stencil buffer to a particular depth value and stencil value.

The back buffer of the swap chain and the depth/stencil buffer must be accessed using their views.

After everything has finished rendering, we must tell the swap chain to present the contents of the back buffer to the screen. For this we will create a **Present** helper function.

The **Present** function is called at the end of the drawing code and finalizes the frame.

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
void Present( bool vSync )
{
if ( vSync )
{
g_d3dSwapChain->Present( 1, 0 );
}
else
{
g_d3dSwapChain->Present( 0, 0 );
}
}
|

The [IDXGISwapChain::Present](http://msdn.microsoft.com/en-us/library/windows/desktop/bb174576(v=vs.85).aspx) method is used to flip the back buffer to the front for display in the application window. The [IDXGISwapChain::Present](http://msdn.microsoft.com/en-us/library/windows/desktop/bb174576(v=vs.85).aspx) method takes two parameters [[55]](https://www.3dgep.com#Present):

-
**UINT SyncInterval**: An integer that specifies how to synchronize presentation of a frame with the vertical blank. For the bit-block transfer (bitblt) model ([DXGI_SWAP_EFFECT_DISCARD](http://msdn.microsoft.com/en-us/library/windows/desktop/bb173077(v=vs.85).aspx#DXGI_SWAP_EFFECT_DISCARD)or[DXGI_SWAP_EFFECT_SEQUENTIAL](http://msdn.microsoft.com/en-us/library/windows/desktop/bb173077(v=vs.85).aspx#DXGI_SWAP_EFFECT_SEQUENTIAL)), values are:-
**0**: The presentation occurs immediately, there is no synchronization. -
**1,2,3,4**: Synchronize presentation after the**nth**vertical blank.

For the flip model (

[DXGI_SWAP_EFFECT_FLIP_SEQUENTIAL](http://msdn.microsoft.com/en-us/library/windows/desktop/bb173077(v=vs.85).aspx#DXGI_SWAP_EFFECT_FLIP_SEQUENTIAL)), values are:-
**0**: Cancel the remaining time on the previously presented frame and discard this frame if a newer frame is queued. -
**n > 0**: Synchronize presentation for at least**n**vertical blanks.

-
-
**UINT Flags**: An integer value that contains swap-chain presentation options. These options are defined by the[DXGI_PRESENT](http://msdn.microsoft.com/en-us/library/windows/desktop/bb509554(v=vs.85).aspx)constants.

If vertical-sync is enabled, then the presentation of the back buffer will wait until the next vertical blank for the screen. If the vertical sync is not enabled, then the contents of the back buffer will be displayed immediately without synchronization.

And finally everything is in place for rendering the geometry to the screen.

In the render function, we’ll first clear the back buffer and the depth/stencil buffers. Then we’ll initialize each stage of the rendering pipeline and finally we’ll draw the geometry.

The first step of our render function (after checking our preconditions) is to clear the screen.

|
1
2
3
4
5
6
|
void Render()
{
assert( g_d3dDevice );
assert( g_d3dDeviceContext );
Clear( Colors::CornflowerBlue, 1.0f, 0 );
|

On line 846, we call the **Clear** function to clear the contents of the back buffer and depth/stencil buffer.

The first stage of the rendering pipeline is the input assembler (**IA**).

|
1
2
3
4
5
6
7
|
const UINT vertexStride = sizeof(VertexPosColor);
const UINT offset = 0;
g_d3dDeviceContext->IASetVertexBuffers( 0, 1, &g_d3dVertexBuffer, &vertexStride, &offset );
g_d3dDeviceContext->IASetInputLayout( g_d3dInputLayout );
g_d3dDeviceContext->IASetIndexBuffer( g_d3dIndexBuffer, DXGI_FORMAT_R16_UINT, 0 );
g_d3dDeviceContext->IASetPrimitiveTopology( D3D11_PRIMITIVE_TOPOLOGY_TRIANGLELIST );
|

On line 851-854 we setup the various properties of the input assembler stage. On line 851, we bind the vertex buffer to to input assembler stage using the [ID3D11DeviceContext::IASetVertexBuffers](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476456(v=vs.85).aspx) method. This method takes the following arguments [[56]](https://www.3dgep.com#IASetVertexBuffers):

-
**UINT StartSlot**: The first input slot for binding. The first vertex buffer is explicitly bound to the start slot; this causes each additional vertex buffer in the array to be implicitly bound to each subsequent input slot. The maximum of 16 or 32 input slots (ranges from 0 to**D3D11_IA_VERTEX_INPUT_RESOURCE_SLOT_COUNT**– 1) are available; the[maximum number of input slots depends on the feature level](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476876(v=vs.85).aspx). -
**UINT NumBuffers**: The number of vertex buffers in the array. The number of buffers (plus the starting slot) can’t exceed the total number of IA-stage input slots (ranges from 0 to**D3D11_IA_VERTEX_INPUT_RESOURCE_SLOT_COUNT**–**StartSlot**). -
**ID3D11Buffer *const *ppVertexBuffers**: A pointer to an array of vertex buffers (see[ID3D11Buffer](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476351(v=vs.85).aspx)). The vertex buffers must have been created with the[D3D11_BIND_VERTEX_BUFFER](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476085(v=vs.85).aspx)flag. -
**const UINT *pStrides**: Pointer to an array of stride values; one stride value for each buffer in the vertex-buffer array. Each stride is the size (in bytes) of the elements that are to be used from that vertex buffer. -
**const UINT *pOffsets**: Pointer to an array of offset values; one offset value for each buffer in the vertex-buffer array. Each offset is the number of bytes between the first element of a vertex buffer and the first element that will be used.

Since we only have a single vertex buffer, the **StartSlot** is always 0 and the **NumBuffers** is 1. The **StartSlot** argument should match the **InputSlot** of the [D3D11_INPUT_ELEMENT_DESC](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476180(v=vs.85).aspx) elements that were configured in the **LoadContent** function.

On line 852 the input layout is specified for the input assembler stage using the [ID3D11DeviceContext::IASetInputLayout](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476454(v=vs.85).aspx) method. The input layout object used must match the input signature of the vertex shader which is bound to the vertex shader stage while rendering.

On line 853 the index buffer is bound to the input assembler stage using the [ID3D11DeviceContext::IASetIndexBuffer](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476453(v=vs.85).aspx) method. This method takes the following arguments [[57]](https://www.3dgep.com#IASetIndexBuffer):

-
**ID3D11Buffer *pIndexBuffer**: A pointer to an[ID3D11Buffer](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476351(v=vs.85).aspx)object, that contains indices. The index buffer must have been created with the[D3D11_BIND_INDEX_BUFFER](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476085(v=vs.85).aspx)flag. -
**DXGI_FORMAT Format**: A[DXGI_FORMAT](http://msdn.microsoft.com/en-us/library/windows/desktop/bb173059(v=vs.85).aspx)that specifies the format of the data in the index buffer. The only formats allowed for index buffer data are 16-bit (**DXGI_FORMAT_R16_UINT**) and 32-bit (**DXGI_FORMAT_R32_UINT**) integers. -
**UINT Offset**: Offset (in bytes) from the start of the index buffer to the first index to use.

And on line 854 the type of primitive that will be used for rendering is specified using the [ID3D11DeviceContext::IASetPrimitiveTopology](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476455(v=vs.85).aspx) method. In this case we specify the **D3D11_PRIMITIVE_TOPOLOGY_TRIANGLELIST** primitive type which indicates to the input assembler stage that we are rending with a list of discontinuous triangles.

The next stage of the rendering pipeline is the vertex shader stage (**VS**). For the vertex shader stage we only have to specify the vertex shader which will be used to transform the object space vertices to homogeneous clip space and bind any constant buffers that are used by the vertex shader stage.

|
1
2
|
g_d3dDeviceContext->VSSetShader( g_d3dVertexShader, nullptr, 0 );
g_d3dDeviceContext->VSSetConstantBuffers(0, 3, g_d3dConstantBuffers );
|

The vertex shader is bound to the vertex shader stage using the [ID3D11DeviceContext::VSSetShader](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476493(v=vs.85).aspx) method. This method takes the following arguments [[58]](https://www.3dgep.com#VSSetShader):

-
**ID3D11VertexShader *pVertexShader**: Pointer to a vertex shader (see[ID3D11VertexShader](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476641(v=vs.85).aspx)). Passing in**NULL**disables the shader for this pipeline stage. -
**ID3D11ClassInstance *const *ppClassInstances**: A pointer to an array of class-instance interfaces (see[ID3D11ClassInstance](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476353(v=vs.85).aspx)). Each interface used by a shader must have a corresponding class instance or the shader will get disabled. Set**ppClassInstances**to**NULL**if the shader does not use any interfaces. -
**UINT NumClassInstances**: The number of class-instance interfaces in the**ppClassInstances**array.

On line 857 the constant buffers used by the vertex shader are bound to the vertex shader stage using the [ID3D11DeviceContext::VSSetConstantBuffers](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476491(v=vs.85).aspx) method. This method takes the following arguments:

-
**UINT StartSlot**: Index into the device’s zero-based array to begin setting constant buffers to (ranges from 0 to**D3D11_COMMONSHADER_CONSTANT_BUFFER_API_SLOT_COUNT**– 1). -
**UINT NumBuffers**: Number of buffers to set (ranges from 0 to**D3D11_COMMONSHADER_CONSTANT_BUFFER_API_SLOT_COUNT**– StartSlot). -
**ID3D11Buffer *const *ppConstantBuffers**: Array of constant buffers (see[ID3D11Buffer](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476351(v=vs.85).aspx)) being given to the device.

After the vertex shader stage but before the pixel shader stage comes the rasterizer stage. The rasterizer stage is responsible for interpolating the various vertex attributes output from the vertex shader and invoking the pixel shader program for each screen pixel which is affected by the rendered geometry.

|
1
2
|
g_d3dDeviceContext->RSSetState( g_d3dRasterizerState );
g_d3dDeviceContext->RSSetViewports( 1, &g_Viewport );
|

On line 859 the rasterizer stage is initialized using the [ID3D11DeviceContext::RSSetState](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476479(v=vs.85).aspx) method. This method takes a pointer to a [ID3D11RasterizerState](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476580(v=vs.85).aspx) object which we created in the **InitDirectX** function.

The rasterizer stage also needs to know about any viewports that are used to map the clip space coordinates into screen space. All viewports are bound to the rasterizer stage using the [ID3D11DeviceContext::RSSetViewports](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476480(v=vs.85).aspx) method. This takes the following arguments [[59]](https://www.3dgep.com#RSSetViewports):

-
**UINT NumViewports**: Number of viewports to bind. -
**const D3D11_VIEWPORT *pViewports**: An array of D3D11_VIEWPORT structures to bind to the device.

All viewports must be set atomically as one operation. Any viewports not defined by the call are disabled.

Which viewport to use is determined by the **SV_ViewportArrayIndex** semantic output by a geometry shader; if a geometry shader does not specify the semantic, Direct3D will use the first viewport in the array [[59]](https://www.3dgep.com#RSSetViewports).

Next we’ll setup the pixel shader stage. For this stage, we only have to bind the pixel shader program to the pixel shader stage.

|
1 |
g_d3dDeviceContext->PSSetShader( g_d3dPixelShader, nullptr, 0 );
|

The pixel shader is bound to the pixel shader stage using the [ID3D11DeviceContext::PSSetShader](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476472(v=vs.85).aspx) method. This method is similar to the method to set the vertex shader so I won’t detail the arguments here.

The output merger stage (as it’s name suggests) merges the output from the pixel shader onto the color and depth buffers.

|
1
2
|
g_d3dDeviceContext->OMSetRenderTargets( 1, &g_d3dRenderTargetView, g_d3dDepthStencilView );
g_d3dDeviceContext->OMSetDepthStencilState( g_d3dDepthStencilState, 1 );
|

The back buffer and depth/stencil buffer are bound to the output merger stage using the [ID3D11DeviceContext::OMSetRenderTargets](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476464(v=vs.85).aspx) method. This method takes the following arguments [[60]](https://www.3dgep.com#OMSetRenderTargets):

-
**UINT NumViews**: Number of render targets to bind (ranges between 0 and**D3D11_SIMULTANEOUS_RENDER_TARGET_COUNT**). If this parameter is nonzero, the number of entries in the array to which**ppRenderTargetViews**points must equal the number in this parameter. -
**ID3D11RenderTargetView *const *ppRenderTargetViews**: Pointer to an array of[ID3D11RenderTargetView](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476582(v=vs.85).aspx)that represent the render targets to bind to the device. If this parameter is**NULL**and NumViews is 0, no render targets are bound. -
**ID3D11DepthStencilView *pDepthStencilView**: Pointer to a[ID3D11DepthStencilView](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476377(v=vs.85).aspx)that represents the depth-stencil view to bind to the device. If this parameter is**NULL**, the depth-stencil view is not bound.

You can render to multiple render targets by mapping multiple output values to the **SV_Target[n]** (where **n** is between 0 and **D3D11_SIMULTANEOUS_RENDER_TARGET_COUNT**) semantic in the pixel shader. Currently, the maximum number of render target views that can be mapped to the output merger stage is eight (8).

On line 865, the [ID3D11DeviceContext::OMSetDepthStencilState](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476463(v=vs.85).aspx) method is used to map the [ID3D11DepthStencilState](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476375(v=vs.85).aspx) object that was created in the **InitDirectX** function. Setting the first argument of this method to **NULL** will use the default state listed in [D3D11_DEPTH_STENCIL_DESC](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476110(v=vs.85).aspx) [[61]](https://www.3dgep.com#OMSetDepthStencilState).

Now that we have initialized the various stages of the rendering pipeline, we can render the cube geometry to the screen.

|
1 |
g_d3dDeviceContext->DrawIndexed( _countof(g_Indicies), 0, 0 );
|

The [ID3D11DeviceContext::DrawIndexed](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476409(v=vs.85).aspx) method is used to draw indexed primitives without instancing. The [ID3D11DeviceContext::DrawIndexed](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476409(v=vs.85).aspx) method takes the following arguments [[62]](https://www.3dgep.com#DrawIndexed):

-
**UINT IndexCount**: Number of indices in the currently bound index buffer to draw. -
**UINT StartIndexLocation**: The location of the first index read by the GPU from the index buffer. -
**INT BaseVertexLocation**: A value added to each index before reading a vertex from the vertex buffer.

The final step in the render function is to present the swap chain’s back buffer to the screen.

|
1
2
|
Present( g_EnableVSync );
}
|

Because we are such tidy programmers, we should not forget to tidy up the resource before our application quits.

The **UnloadContent** function is used for releasing the resources that were allocated in the **LoadContent** method.

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
void UnloadContent()
{
SafeRelease(g_d3dConstantBuffers[CB_Appliation]);
SafeRelease(g_d3dConstantBuffers[CB_Frame]);
SafeRelease(g_d3dConstantBuffers[CB_Object]);
SafeRelease(g_d3dIndexBuffer);
SafeRelease(g_d3dVertexBuffer);
SafeRelease(g_d3dInputLayout);
SafeRelease(g_d3dVertexShader);
SafeRelease(g_d3dPixelShader);
}
|

Since all of the resources we allocated are all COM objects, we can use the **SafeRelease** method to release the reference count of the COM objects. If the COM object’s reference count reaches 0, it will be automatically deleted by the system.

We should also not forget to cleanup the references to the resources allocated in the **InitDirectX** function.

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
void Cleanup()
{
SafeRelease( g_d3dDepthStencilView );
SafeRelease( g_d3dRenderTargetView );
SafeRelease( g_d3dDepthStencilBuffer );
SafeRelease( g_d3dDepthStencilState );
SafeRelease( g_d3dRasterizerState );
SafeRelease( g_d3dSwapChain );
SafeRelease( g_d3dDeviceContext );
SafeRelease( g_d3dDevice );
}
|

Now that we have defined all of the necessary functions let’s complete the main function.

At this point we should update the **Run** to call the **Update** and **Render** functions.

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
31
32
33
34
35
36
|
" title="main.cpp"]
/**
* The main application loop.
*/
int Run()
{
MSG msg = {0};
static DWORD previousTime = timeGetTime();
static const float targetFramerate = 30.0f;
static const float maxTimeStep = 1.0f / targetFramerate;
while ( msg.message != WM_QUIT )
{
if ( PeekMessage( &msg, 0, 0, 0, PM_REMOVE ) )
{
TranslateMessage( &msg );
DispatchMessage( &msg );
}
else
{
DWORD currentTime = timeGetTime();
float deltaTime = ( currentTime - previousTime ) / 1000.0f;
previousTime = currentTime;
// Cap the delta time to the max time step (useful if your
// debugging and you don't want the deltaTime value to explode.
deltaTime = std::min<float>(deltaTime, maxTimeStep);
Update( deltaTime );
Render();
}
}
return static_cast<int>(msg.wParam);
}
|

This function is identical to the **Run** function shown in the section titled [The Run Method](https://www.3dgep.com#The_Run_Method) except now we can compile the application with the **Update** and **Render** functions uncommented.

And the final version of the main function which also loads the demo content and performs cleanup after the main window is closed.

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
31
32
33
34
35
36
37
38
|
;" title="main.cpp"]
int WINAPI wWinMain( HINSTANCE hInstance, HINSTANCE prevInstance, LPWSTR cmdLine, int cmdShow )
{
UNREFERENCED_PARAMETER( prevInstance );
UNREFERENCED_PARAMETER( cmdLine );
// Check for DirectX Math library support.
if ( !XMVerifyCPUSupport() )
{
MessageBox( nullptr, TEXT("Failed to verify DirectX Math library support."), TEXT("Error"), MB_OK );
return -1;
}
if( InitApplication(hInstance, cmdShow) != 0 )
{
MessageBox( nullptr, TEXT("Failed to create applicaiton window."), TEXT("Error"), MB_OK );
return -1;
}
if ( InitDirectX(hInstance, g_EnableVSync) != 0 )
{
MessageBox( nullptr, TEXT("Failed to create DirectX device and swap chain."), TEXT("Error"), MB_OK );
return -1;
}
if ( !LoadContent() )
{
MessageBox( nullptr, TEXT("Failed to load content."), TEXT("Error"), MB_OK );
return -1;
}
int returnCode = Run();
UnloadContent();
Cleanup();
return returnCode;
}
|

Now if we run the application again, we should see a rotating cube on a cornflower-blue background.

You can download the source code including the project files for this demo here:

[[1] Wikipedia. (2014). Directx. [online] Retrieved from: ][http://en.wikipedia.org/wiki/DirectX](https://en.wikipedia.org/wiki/DirectX) [Accessed: 10 Mar 2014].

[[2] Wikipedia. (2014). Direct3d. [online] Retrieved from: ][http://en.wikipedia.org/wiki/Direct3D](https://en.wikipedia.org/wiki/Direct3D) [Accessed: 10 Mar 2014].

[[3] Wikipedia. (2014). Windows 95. [online] Retrieved from: ][http://en.wikipedia.org/wiki/Windows_95](https://en.wikipedia.org/wiki/Windows_95) [Accessed: 10 Mar 2014].

[[4] Msdn.microsoft.com. (2014). Shader models vs shader profiles (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/bb509626(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/bb509626(v=vs.85).aspx) [Accessed: 11 Mar 2014].

[[5] IGN. (2014). Gdc: microsoft to debut DirectX 12 on march 20 – ign. [online] Retrieved from: ][http://www.ign.com/articles/2014/03/06/gdc-microsoft-to-debut-directx-12](http://www.ign.com/articles/2014/03/06/gdc-microsoft-to-debut-directx-12) [Accessed: 11 Mar 2014].

[[6] Msdn.microsoft.com. (2014). Direct2D (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/dd370990(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/dd370990(v=vs.85).aspx) [Accessed: 11 Mar 2014].

[[7] Msdn.microsoft.com. (2014). Direct3D (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/hh309466(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/hh309466(v=vs.85).aspx) [Accessed: 11 Mar 2014].

[[8] Msdn.microsoft.com. (2014). DirectWrite (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/dd368038(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/dd368038(v=vs.85).aspx) [Accessed: 11 Mar 2014].

[[9] Msdn.microsoft.com. (2014). DirectXMath (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/hh437833(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/hh437833(v=vs.85).aspx) [Accessed: 11 Mar 2014].

[[10] Msdn.microsoft.com. (2014). Xaudio2 APIs (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/hh405049(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/hh405049(v=vs.85).aspx) [Accessed: 11 Mar 2014].

[[11] Msdn.microsoft.com. (2014). XInput game controller APIs (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/hh405053(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/hh405053(v=vs.85).aspx) [Accessed: 11 Mar 2014].

[[12] Msdn.microsoft.com. (2014). DXGI overview (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/bb205075(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/bb205075(v=vs.85).aspx) [Accessed: 11 Mar 2014].

[[13] Msdn.microsoft.com. (2014). Graphics pipeline (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476882(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476882(v=vs.85).aspx) [Accessed: 11 Mar 2014].

[[14] Msdn.microsoft.com. (2014). Tessellation overview (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476340(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476340(v=vs.85).aspx) [Accessed: 11 Mar 2014].

[[15] Msdn.microsoft.com. (2014). Shader stages (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/bb205146(v=vs.85).aspx#Pixel_Shader_Stage](http://msdn.microsoft.com/en-us/library/windows/desktop/bb205146(v=vs.85).aspx#Pixel_Shader_Stage) [Accessed: 11 Mar 2014].

[[16] Msdn.microsoft.com. (2014). Wndclassex structure (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ms633577(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ms633577(v=vs.85).aspx) [Accessed: 14 Mar 2014].

[[17] Msdn.microsoft.com. (2014). Annotating function parameters and return values. [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/hh916382.aspx](http://msdn.microsoft.com/en-us/library/hh916382.aspx) [Accessed: 14 Mar 2014].

[[18] Msdn.microsoft.com. (2014). Createwindow function (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ms632679(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ms632679(v=vs.85).aspx) [Accessed: 14 Mar 2014].

[[19] Msdn.microsoft.com. (2014). Dxgi_swap_chain_desc structure (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/bb173075(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/bb173075(v=vs.85).aspx) [Accessed: 14 Mar 2014].

[[20] Msdn.microsoft.com. (2014). Dxgi_format enumeration (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/bb173059(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/bb173059(v=vs.85).aspx) [Accessed: 14 Mar 2014].

[[21] Msdn.microsoft.com. (2014). Dxgi_mode_scanline_order enumeration (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/bb173067(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/bb173067(v=vs.85).aspx) [Accessed: 14 Mar 2014].

[[22] Msdn.microsoft.com. (2014). Dxgi_mode_scaling enumeration (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/bb173066(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/bb173066(v=vs.85).aspx) [Accessed: 14 Mar 2014].

[[23] Msdn.microsoft.com. (2014). Dxgi_sample_desc structure (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/bb173072(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/bb173072(v=vs.85).aspx) [Accessed: 14 Mar 2014].

[[24] Msdn.microsoft.com. (2014). Dxgi_usage (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/bb173078(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/bb173078(v=vs.85).aspx) [Accessed: 14 Mar 2014].

[[25] Msdn.microsoft.com. (2014). Dxgi_swap_effect enumeration (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/bb173077(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/bb173077(v=vs.85).aspx) [Accessed: 14 Mar 2014].

[[26] Msdn.microsoft.com. (2014). D3d11_create_device_flag enumeration (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476107(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476107(v=vs.85).aspx) [Accessed: 17 Mar 2014].

[[27] Msdn.microsoft.com. (2014). D3d11createdeviceandswapchain function (windows). [online] Retrieved from: http://msdn.microsoft.com/en-us/library/windows/desktop/ff476083(v=vs.85).aspx [Accessed: 17 Mar 2014].]

[[28] Msdn.microsoft.com. (2014). D3d_driver_type enumeration (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476328(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476328(v=vs.85).aspx) [Accessed: 17 Mar 2014].

[[29] Msdn.microsoft.com. (2014). Id3d11device::createrendertargetview method (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476517(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476517(v=vs.85).aspx) [Accessed: 17 Mar 2014].

[[30] Msdn.microsoft.com. (2014). D3d11_texture2d_desc structure (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476253(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476253(v=vs.85).aspx) [Accessed: 17 Mar 2014].

[[31] Msdn.microsoft.com. (2014). D3d11_usage enumeration (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476259(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476259(v=vs.85).aspx) [Accessed: 17 Mar 2014].

[[32] Msdn.microsoft.com. (2014). Id3d11device::createtexture2d method (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476521(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476521(v=vs.85).aspx) [Accessed: 17 Mar 2014].

[[33] Msdn.microsoft.com. (2014). Id3d11device::createdepthstencilview method (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476507(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476507(v=vs.85).aspx) [Accessed: 17 Mar 2014].

[[34] Msdn.microsoft.com. (2014). D3d11_depth_stencil_desc structure (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476110(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476110(v=vs.85).aspx) [Accessed: 17 Mar 2014].

[[35] Msdn.microsoft.com. (2014). D3d11_depth_write_mask enumeration (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476113(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476113(v=vs.85).aspx) [Accessed: 17 Mar 2014].

[[36] Msdn.microsoft.com. (2014). Id3d11device::createdepthstencilstate method (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476506(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476506(v=vs.85).aspx) [Accessed: 17 Mar 2014].

[[37] Msdn.microsoft.com. (2014). D3d11_rasterizer_desc structure (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476198(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476198(v=vs.85).aspx) [Accessed: 17 Mar 2014].

[[38] Msdn.microsoft.com. (2014). D3d11_fill_mode enumeration (windows). [online] Retrieved from:][ http://msdn.microsoft.com/en-us/library/windows/desktop/ff476131(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476131(v=vs.85).aspx) [Accessed: 17 Mar 2014].

[[39] Msdn.microsoft.com. (2014). D3d11_cull_mode enumeration (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476108(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476108(v=vs.85).aspx) [Accessed: 17 Mar 2014].

[[40] Msdn.microsoft.com. (2014). Id3d11device::createrasterizerstate method (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476516(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476516(v=vs.85).aspx) [Accessed: 17 Mar 2014].

[[41] Msdn.microsoft.com. (2014). D3d11_viewport structure (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476260(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476260(v=vs.85).aspx) [Accessed: 17 Mar 2014].

[[42] Msdn.microsoft.com. (2014). Semantics (windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/bb509647(v=vs.85).aspx#System_Value](http://msdn.microsoft.com/en-us/library/windows/desktop/bb509647(v=vs.85).aspx#System_Value) [Accessed: 18 Mar 2014].

[[43] Msdn.microsoft.com. (2014). Direct3D feature levels (Windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476876(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476876(v=vs.85).aspx) [Accessed: 18 Mar 2014].

[[44] Msdn.microsoft.com. (2014). D3DCompileFromFile function (Windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/hh446872(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/hh446872(v=vs.85).aspx) [Accessed: 19 Mar 2014].

[[45] Msdn.microsoft.com. (2014). D3D11_BUFFER_DESC structure (Windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476092(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476092(v=vs.85).aspx) [Accessed: 19 Mar 2014].

[[46] Msdn.microsoft.com. (2014). D3D11_SUBRESOURCE_DATA structure (Windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476220(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476220(v=vs.85).aspx) [Accessed: 19 Mar 2014].

[[47] Msdn.microsoft.com. (2014). ID3D11Device::CreateBuffer method (Windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476501(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476501(v=vs.85).aspx) [Accessed: 19 Mar 2014].

[[48] Msdn.microsoft.com. (2014). ID3D11Device::CreateInputLayout method (Windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476512(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476512(v=vs.85).aspx) [Accessed: 19 Mar 2014].

[[49] Msdn.microsoft.com. (2014). D3D11_INPUT_ELEMENT_DESC structure (Windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476180(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476180(v=vs.85).aspx) [Accessed: 19 Mar 2014].

[[50] Msdn.microsoft.com. (2014). D3D11_INPUT_CLASSIFICATION enumeration (Windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476179(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476179(v=vs.85).aspx) [Accessed: 19 Mar 2014].

[[51] Msdn.microsoft.com. (2014). ID3D11DeviceContext::UpdateSubresource method (Windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476486(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476486(v=vs.85).aspx) [Accessed: 20 Mar 2014].

[[52] Msdn.microsoft.com. (2014). WindowProc callback function (Windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ms633573(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ms633573(v=vs.85).aspx) [Accessed: 20 Mar 2014].

[[53] Msdn.microsoft.com. (2014). TranslateMessage function (Windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ms644955(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ms644955(v=vs.85).aspx) [Accessed: 20 Mar 2014].

[[54] Msdn.microsoft.com. (2014). DispatchMessage function (Windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ms644934(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ms644934(v=vs.85).aspx) [Accessed: 20 Mar 2014].

[[55] Msdn.microsoft.com. (2014). IDXGISwapChain::Present method (Windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/bb174576(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/bb174576(v=vs.85).aspx) [Accessed: 21 Mar 2014].

[[56] Msdn.microsoft.com. (2014). ID3D11DeviceContext::IASetVertexBuffers method (Windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476456(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476456(v=vs.85).aspx) [Accessed: 21 Mar 2014].

[[57] Msdn.microsoft.com. (2014). ID3D11DeviceContext::IASetIndexBuffer method (Windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476453(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476453(v=vs.85).aspx) [Accessed: 21 Mar 2014].

[[58] Msdn.microsoft.com. (2014). ID3D11DeviceContext::VSSetShader method (Windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476493(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476493(v=vs.85).aspx) [Accessed: 21 Mar 2014].

[[59] Msdn.microsoft.com. (2014). ID3D11DeviceContext::RSSetViewports method (Windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476480(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476480(v=vs.85).aspx) [Accessed: 21 Mar 2014].

[[60] Msdn.microsoft.com. (2014). ID3D11DeviceContext::OMSetRenderTargets method (Windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476464(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476464(v=vs.85).aspx) [Accessed: 21 Mar 2014].

[[61] Msdn.microsoft.com. (2014). ID3D11DeviceContext::OMSetDepthStencilState method (Windows). [online] Retrieved from: ][http://msdn.microsoft.com/en-us/library/windows/desktop/ff476463(v=vs.85).aspx](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476463(v=vs.85).aspx) [Accessed: 21 Mar 2014].

[http://msdn.microsoft.com/en-us/library/windows/desktop/ff476409(v=vs.85).aspx] [Accessed: 21 Mar 2014].

[[63] Sherrod, A. & Jones, W. (2012). Beginning directx 11 game programming. Boston, MA: Course Technology.]

Damn, you really put some effort into thing, gj.

Wow. One of the best tutorials I’ve ever seen on subject. Please, don’t stop. Great job!

This is just great. Thank you so much. Using C# and various frameworks (XNA, libGDX), also Unity engine. I decided to take a look at Direct3D API. If you have some tips to share on terrain rendering please add it to your todo (if your time allows).

But this intro only is worth a lot. Thank you once again.

Awesome tutorial! Been looking all over the web for something like this – its fantastic! Thanks for taking the time to write it and document out all the details, its very easy to follow and very well written! This is what every C++ game programming book *should* start with! Kudos!!

Thanks for this awesome tutorial!

Thought you’d like to know, I’m a University student and we’re in the process of moving from Dx9 to Dx11 and we’ve all been pointer here to get started.

Again, many thanks for such an in-depth tutorial on the subject. 🙂

If you follow this tutorial and are a beginer like me, you may hane some issues, here’s the ones I got. Include , and go to (VS) Tools->Options->Debugging->Symbols, then check “Microsoft Symbol Servers”. You may also have some issues with precompiling headers, for the sake of following the tutorial completely I disabled it. Great tutorial ! Thanks a lot !

I meant include alogrithm header.

Nick,

Yes, the <algorithm> header was not required when I initially wrote this article using Visual Studio 2012 (I suppose it was included by another header with VS2012). When switching to Visual Studio 2013, the <algorithm> header needed to be explicitly included for the std::min and std::max functions.

I am still learning but I live this tutorial. Instead of using VS2012 I use VS2013 Community.

In order for me to get the code working I needed to include the library “#include <algorithm>”. Without I was not able to use ‘std::min’

Best DirectX 11 introduction!! Thanks a lot!

Hi, thanks for a great tutorial!

Have you got any example at loading a shader directly from .hlsl source ?

I am stuck with using the LoadShader function because then the CreateInputLayout function requires a shader blob. How do I get it ??

Additionnaly is there a way to compile a shader from a string input like OpenGL does ?

Thanks.

Julien,

The example to compile a shader from a file at runtime is explained here:

http://www.3dgep.com/introduction-to-directx-11/#Runtime_Compiled_Shader

http://www.3dgep.com/introduction-to-directx-11/#Load_and_Compile_at_Runtime

And to build the input layout from the shader blob:

http://www.3dgep.com/introduction-to-directx-11/#Input_Layout

To load a shader from a string you use the

D3DCompilefunction:https://msdn.microsoft.com/en-us/library/dd607324(v=vs.85).aspx

What I don’t understand is : at the point of calling the g_d3dDevice->CreateInputLayout function, we don’t have a shader blob available (if using the LoadShader func.) because the shader blob is created inside the LoadShader func. and gone at the time a call is made to g_d3dDevice->CreateInputLayout.

I can’t just do this right : hr = g_d3dDevice->CreateInputLayout(vertexLayoutDesc, _countof(vertexLayoutDesc), &g_d3dVertexShader, sizeof(g_d3dVertexShader), &g_d3dInputLayout); ???

Julien,

In this tutorial I simply wanted to show you how you could load and compile a shader at runtime. If you look at the LoadContent function, you will see that I’m not actually using LoadShader function (it’s commented out). You are correct about the CreateInputLayout function. It needs the shader blob (not the Shader object that you get back from ID3D11Device::CreateVertexShader).

The problem is that the LoadShader function would need to know about the layout of the input attributes but it can’t know that without reflecting the shader object. This is possible, but I didn’t do that in this tutorial because I wanted to keep it simple.

For a detailed method to generate the input layout automatically using shader reflection, see this clip I made on pastebin:

http://pastebin.com/YvW9Zhs3

Keep in mind, there are some drawbacks to using this method to automatically build the input layout. The biggest drawback being that the reflection library can’t tell if something is a per-vertex attribute or a per-instance attribute.

Another drawback is that the reflection library can’t know your buffer layout. I just send each attribute in a separate buffer so each buffer will have a unique input slot.

I hope this helps.

Excellent tutorial! But link to source code doesn’t work.

Soslan,

Thanks for pointing this out. I’ve updated the link. It should work now.

Sorce code does’t comply with Article.

Soslan,

Sorry about that! I had 2 files with the same name and I accidentally linked the wrong one. The link has now been fixed (really this time).

Hi JvO,

your tutorial is really very helpful , but –

the ‘updated’ link seems to point to a wrong file, please check again.

Thanks

Kurt

Oops! You are right! That was the link to my DX9 template project 🙁

I’ve updated the link (again) and now with the correct link.

Your tutorial has led my group from zero DX11 experience to a working demo and understanding of the different parts of the pipeline and device initialization.

Thank you.

We found a few mispelling and inconsistencies:

– line 40 ConstanBuffer should be ConstantBuffer

– line 42 CB_Appliation should be CB_Application

I also liked the project boilerplate setup with include files and output files. Thanks.

Michele,

Thanks for pointing out the typos! I’m glad this tutorial was useful for you and your group!

My first successful steps with DX11 came with your tutorial.

Thank you very much!

Thanks!!! This is the first out of the box demo that I found that complies and runs with no issues on Visual Studio 2017!

Gnollrunner,

I just updated the demo a few weeks ago to fix a few issues that broke it under VS2017! Glad to hear it is also working for you!

Very helpful, thank you very much for your efforts!

For some reason the cube does not render for me unless I have MSI Afterburners OSD (On Screen Display) enabled. It will render if the OSD is enabled and then disabled but when the program loads up, if the OSD isn’t initially enabled, it will not render the cube.

To make things even stranger, if Afterburner isn’t even running (not even in the background) the cube still won’t render.

Here are a few images of the issue: https://imgur.com/a/1Bnf0aX

I have no idea how or why this is happening or how to stop it. Does anybody know how to fix this issue or even what might be causing this?

Mike,

Up until now, nobody has reported this issue.

Did you try to compile the project in Debug mode? Do you get any warnings or errors in the Visual Studio debug output?

Thank you very much Sir !!

Cool intro.

I believe that the creation of an additional ID3D11Texture2D* backBuffer is superfluous.

You already have the global g_d3dDepthStencilBuffer so you can use that.

Just saying in case there’s something I’m missing.

Thank you for sharing knowledge. You shall be rewarded!

Yokattan,

The swap chain buffers are used to store the red, green, blue (RGB) color components that will be presented on screen. Since the swap chain does not have a depth buffer, a separate depth buffer must be created. The color buffer from the swap chain and the depth buffer that is created separately, are used together to make up the

render targetthat is bound to the output merger stage.So the

`backBuffer`

is used to refer to the back buffer of the swap chain (but only to use it to create a render target view in`g_d3dRenderTargetView`

which is later used to bind to the output merger stage) and the`g_d3dDepthStencilBuffer`

is used to store the depth/stencil buffer and later used to create the depth stencil view in`g_d3dDepthStencilView`

which is in turn used to bind to the output merger.So they are not the same thing, you need both a color buffer (from the swap chain) and a depth/stencil buffer in order to correctly render 3D objects.

Regarding my previous comment.. I had a hard time understanding why you name it backBuffer.

You’re creating a view out of the primary swapChain’s buffer (it contains only one; we could call it g_d3dRenderTargetBuffer to stay true to our naming conventions), why call it backBuffer?

Instead call it tempBuffer. I’m not sure exactly why Windows names it like so and simply release the resource afterwards. Bad design here would be my guess.

If you can elaborate please

Yokattan,

The

`backBuffer`

variable is used to store a pointer to the back buffer of the swap chain. Since it is only used to create the render target view, it can be calledtempBufferbut don’t be deceived: There is no buffer being created here, we’re just getting a reference to the swap chain’s back buffer so that the render target view can be created (on line 311).Getting a reference to the swap chain’s back buffer will increment its reference count (see https://docs.microsoft.com/en-us/windows/win32/com/the-component-object-model for information about COM objects) and it is therefore required to release the reference after the render target view is created. This does not cause the underlying resource to be released since it is still owned by the swap chain.

I hope this helps.

Just to clarify something. The swap chain initially contains only one buffer right, so we simply use backBuffer to refer to it temporarily just to create the renderTargetView. Later we will create another buffer the depthStencilBuffer (and an associated view from it) and bind it to the swap chain.

Is this true? I believe I understand now. Thank you very much.

A very thorough and helpful article it is, even in 2019!

But I think it can be shortened by leaving method signatures as external links to MSDN and picking the typical or special ones out of the regulars.

Still, thanks for the efforts you’ve put into it. <3

Snull,

Thanks for your feedback. The method signatures and the explanation of every parameter may indeed be overkill. However, one of the things I loath about MSDN documentation is how scattered the information is. In this article, I wanted to have all the information in a single place. It’s not only a tutorial, but it’s also a reference!

I appreciate the inlined MSDN documentation, this is just the style I prefer. All that is needed is placed in one logical sequence and detailed to really understand whats going on. I also looked a lot at the refered documentation to better grasp the concepts.

Thank, you very much! It is still the best start tutorial I have found in 2024! If only now I could figure out why I see nothing but a blue window 🙂

Feel free to join our Discord server to ask any questions you might still have: https://discord.gg/gsxxaxc

Thank you so much for this detailed guide!

I know this article is a bit old but is the template download link working? Google Drive says it has a virus in it, but I am sure it is a false positive.

I’ll look into moving the source code to GitHub.

I’ve moved the source to GitHub:

https://github.com/jpvanoosten/LearningDirectX11/tree/v1.0.0

Thanks a lot!

Is it necessary to set:

g_d3dDeviceContext->RSSetState

g_d3dDeviceContext->RSSetViewports

every frame even though they do not change?

Also how does the buffer in the swap chain that the render target view points to update to point to the next buffer in the swap chain after Present() is called?

It may not be necessary to call

`g_d3dDeviceContext->RSSetState`

and`g_d3dDeviceContext->RSSetViewports`

if they don’t change, but you should call`g_d3dDeviceContext->RSSetViewports`

if the screen size changes.The question about the swap chain is a good question. In this tutorial/demo, the swap chain only has a single buffer. According to the documentation (DXGI_SWAP_EFFECT enumeration), the user only has read/write access to the buffer at index 0. I suppose the render target only knows about the buffer at index 0 and whenever you call

`Present`

on swap chain, it sets the next buffer to index 0. So you don’t need to create a render target for the other back buffers…This is different in DX12 where you need a render target for each back buffer texture and you use IDXGISwapChain3::GetCurrentBackBufferIndex to query the current render target to use for rendering. But this is not required for DX11.

I have an issue when visual studio runs the .exe file.

In Render() function, VS sets a breakpoint with the following warning message:

“Exception thrown at 0x7B7DF586 (d3d11_3SDKLayers.dll) in DirectX11Template.exe: 0xC0000005: Access violation while reading location 0x0000008C.

Unhandled exception at 0x7B7DF586 (d3d11_3SDKLayers.dll) in DirectX11Template.exe: 0xC0000005: Access violation reading location 0x0000008C.”

The main window appears with no error, but crushes when compiler catch the render() function.

I’m using visual studio 2015 commnunity, setted up the project as a Win32.

Thank you!

I’m not certain, but this could be related to the fact that the textures couldn’t be loaded due to the working directory not being set correctly. I’ve committed the

.userfiles (they were previously ignored by the .gitignore file) which might fix the issue when running the demo in Visual Studio.A few things to note:

TextureAndLightingproject is set as the project to run when you start debugging in Visual StudioDebugging\Working Directoryproperty is set to$(OutDir)and not$(ProjectDir)in the project properties.bin\folder and the textures are in thedata\Texturesfolder.When debugging in Visual Studio, the value of the $(ProjectDir) variable is used to set the working directory. The application is looking in

..\datafor the textures, but if you are not running in the correct working directory, then it won’t be able to find the textures.I hope this helps.