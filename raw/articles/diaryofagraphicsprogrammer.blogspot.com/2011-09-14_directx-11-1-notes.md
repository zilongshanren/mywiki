---
title: DirectX 11.1 Notes
url: http://diaryofagraphicsprogrammer.blogspot.com/2011/09/directx-111-notes.html
author: Wolfgang Engel
published: '2011-09-14'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I plan to update this blog in the next couple of days with more information as soon as it becomes available.


The upgrade from DirectX 11 to DirectX 11.1 is targeting the following areas:


1. Use UAV's at every Pipeline stage

2. Use logical operations in a render target

3. Shader tracing: looks like a new way to measure shader performance


The functions (ID3D11Device::CheckFeatureSupport / ID3D11Device::CheckFormatSupport) that check for supported features and formats were extended as well. D3D11_FEATURE_DATA_ARCHITECTURE_INFO seems to be for tiled-based rendering hardware commonly used in mobile GPUs and D3D11_FEATURE_DATA_SHADER_MIN_PRECISION_SUPPORT too. DXGI_FORMAT was extended to support video formats that now can be processed with shaders by using resource views (SRV/RTV/UAV). There is a new D3D_FEATURE_LEVEL_11_1 defined (i.e. a minor revision of the hardware feature set), but I don’t (yet) have a good link to give you to summarize the required features. Of course, there’s no public drivers or hardware out yet that exposes FL 11.1 anyhow. As before, DirectX 11.1 (the API) works with a range of Feature Levels (the hardware). WARP on Windows 8 supports FL 11.0 (and 10.1 as before) and includes support for the DXGI 1.2 16bpp formats (565, 5551, 4444). The Windows 8 Developer Preview SDK includes the latest HLSL compiler FXC tool and D3DCompiler.DLL, the Debug Layers DLL, and the REF device DLL for DirectX 11.1 on Windows 8. The MSDN documentation now includes details on SM 4.x and SM 5.0 shader assembly (for deciphering the compiler’s disassembly output) plus details on BC6H/BC7 compression formats <


The upgrade from DirectX 11 to DirectX 11.1 is targeting the following areas:

- Enabling Metro-style applications (there’s some additional access control for this which impacted almost every API in the OS so there’s no Direct3D 9 in Metro-style, but Direct3D 11.x is fully supported)
- Technical computing (optional extended double-precision instructions (division, etc.) and optional Sum of Absolute Differences instruction; enabling hardware access via Direct3D from session 0; HLSL compiler improvements)
- Low-power device optimizations (reduced shader precision hints for HLSL/driver, Tiled Graphics Rendering optimizations, 4 bit-per-pixel DXGI formats 565, 5551, 4444)
- Various graphics stack unification efforts (Direct3D 11 Video, Direct3D interop improvements for Direct2D & Media Foundation, etc.)

- Windows on ARM

[MSDN website](http://msdn.microsoft.com/en-us/library/hh404562%28v=VS.85%29.aspx#support_a_larger_number_of_uavs). For me the most remarkable things on this page are:1. Use UAV's at every Pipeline stage

2. Use logical operations in a render target

3. Shader tracing: looks like a new way to measure shader performance

The functions (ID3D11Device::CheckFeatureSupport / ID3D11Device::CheckFormatSupport) that check for supported features and formats were extended as well. D3D11_FEATURE_DATA_ARCHITECTURE_INFO seems to be for tiled-based rendering hardware commonly used in mobile GPUs and D3D11_FEATURE_DATA_SHADER_MIN_PRECISION_SUPPORT too. DXGI_FORMAT was extended to support video formats that now can be processed with shaders by using resource views (SRV/RTV/UAV). There is a new D3D_FEATURE_LEVEL_11_1 defined (i.e. a minor revision of the hardware feature set), but I don’t (yet) have a good link to give you to summarize the required features. Of course, there’s no public drivers or hardware out yet that exposes FL 11.1 anyhow. As before, DirectX 11.1 (the API) works with a range of Feature Levels (the hardware). WARP on Windows 8 supports FL 11.0 (and 10.1 as before) and includes support for the DXGI 1.2 16bpp formats (565, 5551, 4444). The Windows 8 Developer Preview SDK includes the latest HLSL compiler FXC tool and D3DCompiler.DLL, the Debug Layers DLL, and the REF device DLL for DirectX 11.1 on Windows 8. The MSDN documentation now includes details on SM 4.x and SM 5.0 shader assembly (for deciphering the compiler’s disassembly output) plus details on BC6H/BC7 compression formats <

[http://msdn.microsoft.com/en-us/library/bb943998(v=VS.85).aspx](http://msdn.microsoft.com/en-us/library/bb943998(v=VS.85).aspx)> <[http://msdn.microsoft.com/en-us/library/hh447232(v=VS.85).aspx](http://msdn.microsoft.com/en-us/library/hh447232(v=VS.85).aspx)> <[http://msdn.microsoft.com/en-us/library/hh308955(v=VS.85).aspx](http://msdn.microsoft.com/en-us/library/hh308955(v=VS.85).aspx)> What is different from DirectX 11 on PC- D3DX9, D3DX10, D3DX11 are not supported for Metro-style applications.
- The Texconv sample includes the "DirectXTex" library which has all the texture processing functionality, WIC-based IO, DDS codec, BC software compression/decompression, etc. as shared source that was in D3DX11.
- D3DCSX_44.DLL is in the Windows SDK for redist with applications, and I believe is supported in Metro style applications.
- D3DCompiler_44.DLL is available for REDIST with Desktop applications and for development, but is not supported for REDIST in Metro-style applications. We've long recommended not doing run-time compliation, and Metro style enforces this at deployment time.
- XINPUT1_4.DLL and XAUDIO2_8.DLL are included in the OS and are fully supported for Metro style applications.

## No comments:

Post a Comment