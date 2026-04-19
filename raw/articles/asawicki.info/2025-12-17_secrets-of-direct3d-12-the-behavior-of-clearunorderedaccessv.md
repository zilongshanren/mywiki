---
title: 'Secrets of Direct3D 12: The Behavior of ClearUnorderedAccessViewUint/Float'
url: https://asawicki.info/news_1795_secrets_of_direct3d_12_the_behavior_of_clearunorderedaccessviewuintfloat
published: '2025-12-17'
source_blog: Adam Sawicki Home Page - programming, graphics, games, media, C++, Windows,
  I...
source_site: https://asawicki.info/
category: graphics
fetched: '2026-04-19'
---

Wed

17

Dec 2025

This article is about a quite niche topic - the functions `ClearUnorderedAccessViewUint`

and `ClearUnorderedAccessViewFloat`

of the `ID3D12GraphicsCommandList`

interface. You may be familiar with them if you are a programmer using DirectX 12. Their official documentation - [ClearUnorderedAccessViewUint](https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12graphicscommandlist-clearunorderedaccessviewuint) and [ClearUnorderedAccessViewFloat](https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12graphicscommandlist-clearunorderedaccessviewfloat) - provides some details, but there is much more to say about their behavior. I could not find sufficiently detailed information anywhere on the Internet, so here is my take on this topic.

The two functions discussed here allow “clearing” a buffer, or a subregion of it, by setting every element to a specific numeric value (sometimes also called “splatting” or “broadcasting”). The function `ClearUnorderedAccessViewUint`

accepts a `UINT[4]`

array, while function `ClearUnorderedAccessViewFloat`

accepts a `FLOAT[4]`

array. They are conceptually similar to the functions `ClearRenderTargetView`

and `ClearDepthStencilView`

, which we commonly use for clearing textures. In the realm of CPU code, they can also be compared to the standard function `memset`

.

These functions work with typed buffers. Buffer views can come in three flavors:

`DXGI_FORMAT`

, just like pixels for a texture. For example, using `DXGI_FORMAT_R32G32B32R32_FLOAT`

means each element has four floats (x, y, z, w), 16 bytes in total.`uint`

at a time.I plan to write a more comprehensive article about buffers in DX12 and their types. For now, I recommend the excellent article [Let’s Close the Buffer Zoo by Joshua Barczak](http://www.joshbarczak.com/blog/?p=1260) for more information. In my article below, we will use only typed buffers.

The functions `ClearUnorderedAccessViewUint`

and `ClearUnorderedAccessViewFloat`

have a quite inconvenient interface, requiring us to provide two UAV descriptors for the buffer we are about to clear: a GPU handle in a shader-visible descriptor heap and a CPU handle in a non-shader-visible descriptor heap. This means we need to have both kinds of descriptor heaps, we need to write the descriptor for our buffer twice, and we need three different descriptor handles - the third one being a CPU handle to the shader-visible heap, which we use to actually create the descriptor using `CreateUnorderedAccessView`

function. The code may look like this:

// Created with desc.Type = D3D12_DESCRIPTOR_HEAP_TYPE_CBV_SRV_UAV, // desc.Flags = D3D12_DESCRIPTOR_HEAP_FLAG_SHADER_VISIBLE. ID3D12DescriptorHeap* shaderVisibleDescHeap = ... // Created with desc.Type = D3D12_DESCRIPTOR_HEAP_TYPE_CBV_SRV_UAV, // desc.Flags = D3D12_DESCRIPTOR_HEAP_FLAG_NONE. ID3D12DescriptorHeap* nonShaderVisibleDescHeap = ... UINT handleIncrementSize = device->GetDescriptorHandleIncrementSize( D3D12_DESCRIPTOR_HEAP_TYPE_CBV_SRV_UAV) UINT descIndexInVisibleHeap = ... // Descriptor index in the heap. UINT descIndexInNonVisibleHeap = ... // Descriptor index in the heap. D3D12_GPU_DESCRIPTOR_HANDLE shaderVisibleGpuDescHandle = shaderVisibleDescHeap->GetGPUDescriptorHandleForHeapStart(); shaderVisibleGpuDescHandle.ptr += descIndexInVisibleHeap * handleIncrementSize; D3D12_CPU_DESCRIPTOR_HANDLE shaderVisibleCpuDescHandle = shaderVisibleDescHeap->GetCPUDescriptorHandleForHeapStart(); shaderVisibleCpuDescHandle.ptr += descIndexInVisibleHeap * handleIncrementSize; D3D12_CPU_DESCRIPTOR_HANDLE nonShaderVisibleCpuDescHandle = nonShaderVisibleDescHeap->GetCPUDescriptorHandleForHeapStart(); nonShaderVisibleCpuDescHandle.ptr += descIndexInNonVisibleHeap * handleIncrementSize; D3D12_UNORDERED_ACCESS_VIEW_DESC uavDesc = {}; uavDesc.ViewDimension = D3D12_UAV_DIMENSION_BUFFER; uavDesc.Format = DXGI_FORMAT_R32G32B32R32_FLOAT; // My buffer element format. uavDesc.Buffer.FirstElement = 0; uavDesc.Buffer.NumElements = 1024; // My buffer element count. ID3D12Resource* buf = ... // My buffer resource. device->CreateUnorderedAccessView(buf, NULL, &uavDesc, shaderVisibleCpuDescHandle); device->CreateUnorderedAccessView(buf, NULL, &uavDesc, nonShaderVisibleCpuDescHandle); UINT values[4] = {1, 2, 3, 4}; // Values to clear. commandList->ClearUnorderedAccessViewUint( shaderVisibleGpuDescHandle, // ViewGPUHandleInCurrentHeap nonShaderVisibleCpuDescHandle, // ViewCPUHandle buf // pResource values, // Values 0, // NumRects NULL); // pRects

Why did Microsoft make it so complicated? We may find the answer in the [official function documentation](https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12graphicscommandlist-clearunorderedaccessviewuint) mentioned above, which says: *"This is to allow drivers that implement the clear as a fixed-function hardware operation (rather than as a dispatch) to efficiently read from the descriptor, as shader-visible heaps may be created in WRITE_COMBINE memory."* I suspect this was needed mostly for older, DX11-class GPUs with more fixed-function hardware, while modern GPUs can read from and write to video memory more freely.

We must also remember to set the shader-visible descriptor heap as the current one using `ID3D12GraphicsCommandList::SetDescriptorHeaps`

before performing the clear. Interestingly, on my RTX 4090 it works even without this step, but this is still incorrect and may not work on a different GPU. The D3D Debug Layer emits an error in this case.
Note this is different from texture clears performed using `ClearRenderTargetView`

and `ClearDepthStencilView`

, where we use Render-Target View (RTV) and Depth-Stencil View (DSV) descriptors, which can never be shader-visible, so they cannot be used in `SetDescriptorHeaps`

. For more information, see my older article: ["Secrets of Direct3D 12: Do RTV and DSV descriptors make any sense?"](https://asawicki.info/news_1772_secrets_of_direct3d_12_do_rtv_and_dsv_descriptors_make_any_sense).

The functions `ClearUnorderedAccessViewUint`

and `ClearUnorderedAccessViewFloat`

require the buffer to be in the `D3D12_RESOURCE_STATE_UNORDERED_ACCESS`

state, just like when writing to it from a compute shader. If the buffer was in a different state before, we need to issue a transition barrier (`D3D12_RESOURCE_BARRIER_TYPE_TRANSITION`

). If we use the buffer as a UAV before or after the clear, the state doesn't change, but we need to issue an UAV barrier (`D3D12_RESOURCE_BARRIER_TYPE_UAV`

) to make the commands wait for each other. Otherwise, a race condition could occur, as the commands could run in parallel.

These restrictions make buffer clearing with these functions similar to using compute shaders, and different from `ClearRenderTargetView`

and `ClearDepthStencilView`

, which are used for clearing textures, or from copy operations (`CopyResource`

, `CopyBufferRegion`

), which do not require barriers around them. For a more in-depth investigation of this distinction, see my older article: ["Secrets of Direct3D 12: Copies to the Same Buffer"](https://asawicki.info/news_1722_secrets_of_direct3d_12_copies_to_the_same_buffer).

Here comes the main part that inspired me to write this article. I asked myself how are the `UINT[4]`

values passed to the `ClearUnorderedAccessViewUint`

function converted to the values of elements in the buffer, depending on the element format. I could not find any mention of this on the Internet, so I did some experiments. Below, I summarize my findings. Unfortunately, the behavior is inconsistent between GPU vendors! I tested on Nvidia (GeForce RTX 4090, driver 591.44), AMD (Radeon RX 9060 XT, driver 25.11.1), and Intel (Arc B580, driver 32.0.101.8250) - all on Windows 25H2 (OS Build 26200.7462) with DirectX Agility SDK 1.618.3 Retail.

`DXGI_FORMAT_R32G32B32A32_UINT`

, the values are written as-is, because the format matches exactly the values accepted by the function, so for example `{1, 2, 3, 4}`

gets written as `0x00000001, 0x00000002, 0x00000003, 0x00000004, 0x00000001, 0x00000002, 0x00000003, 0x00000004, ...`

`DXGI_FORMAT_R32G32_UINT`

, from `{1, 2, 3, 4}`

, the buffer will be filled with `0x00000001, 0x00000002, 0x00000001, 0x00000002, ...`

- only the first 2 components are used.`DXGI_FORMAT_R16G16B16A16_UINT`

:
`0x20003`

gets written as `0xFFFF`

.`0x0003`

.`UNORM`

formats:
`UINT`

formats. For example, values `{0, 2, 255, 0xFFFFFFFFu}`

written to a buffer with `DXGI_FORMAT_R8G8B8A8_UNORM`

become `{0x00, 0x02, 0xFF, 0xFF}`

, despite they logically represent `{0, 2.0/255.0, 1.0, 1.0}`

. The normalization logic isn't working here. Note this is different from the Float version of the function described in the next section. However, it makes sense, because otherwise the only useful values in this function would be 0 and 1.`0x20003`

becomes `0x03`

.`DXGI_FORMAT_R16G16B16A16_SINT`

, and we use only the lowest 16 bits of the value, like `0xFFF0u`

to write value -16:
`0x7FFF`

.`DXGI_FORMAT_R16G16B16A16_SINT`

, but this time specify `0xFFFFFFF0`

(which is the 32-bit representation of -16):
`DXGI_FORMAT_R32G32B32A32_FLOAT`

, the values are bit-casted to float, e.g. value `0x3F800000u`

becomes 1.0.To summarize, the `ClearUnorderedAccessViewUint`

function may be useful when we want to set a specific bit pattern to the elements of a buffer in `UINT`

format, but for other formats or out-of-range values the behavior is unreliable and we cannot be sure it won't change in the future.

Here is a similar summary of the behavior of function `ClearUnorderedAccessViewFloat`

, which takes 4 floats as the value, for different formats of buffer elements:

`DXGI_FORMAT_R32G32B32A32_FLOAT`

, the values are written as-is, because the format matches exactly the values accepted by the function.`{1.0f, 2.0f, 3.0f, 4.0f}`

, but the format has only 2 components, like `DXGI_FORMAT_R32G32_FLOAT`

, only `{1.0f, 2.0f}`

is written repeatedly.`{1.0f, -1.0f, 0.5f, 2.0f}`

in `DXGI_FORMAT_R16G16B16A16_FLOAT`

become `0x3C00, 0xBC00, 0x3800, 0x4000`

.`{0.0f, 123.0f, -1.0f, -10.5f}`

written to a buffer with `DXGI_FORMAT_R32G32B32A32_SINT`

becomes `{0, 123, -1, -10}`

.`{0, 0x42f60000, 0xbf800000, 0xc1200000}`

, which are floating-point values specified on input, just directly bit-casted.`-100.0`

becomes `0xFFFFFF9C`

.`0xC2C80000`

.`{0.0f, 1.0f, 123.0f, 1000.f}`

written to a buffer with `DXGI_FORMAT_R8G8B8A8_UINT`

becomes `{0, 1, 123, 255}`

.`{0x00, 0xFF, 0xFF, 0xFF}`

.`UNORM`

or `SNORM`

, values are converted and clamped, respecting its logical representation with normalization. For example, with `DXGI_FORMAT_R8G8B8A8_UNORM`

, values `0.0...1.0`

are mapped to `0...255`

and values above `1.0`

become `255`

. Note this is different from the Uint version of the function described above. The Float version is better to work with such formats.To summarize, the `ClearUnorderedAccessViewFloat`

function is useful when we want to set a specific numeric value, correctly converted to the specific format, especially when it's `FLOAT, UNORM, SNORM`

. For consistent behavior across GPUs, we should avoid using it with `UINT, SINT`

formats.

If we want to limit the range of elements to clear, we have 2 equivalent ways of doing so:

1. Set the limit when filling the descriptor:

D3D12_UNORDERED_ACCESS_VIEW_DESC uavDesc = {}; uavDesc.ViewDimension = D3D12_UAV_DIMENSION_BUFFER; uavDesc.Format = ... uavDesc.Buffer.FirstElement = firstElementIndex; // !!! uavDesc.Buffer.NumElements = elementCount; // !!! device->CreateUnorderedAccessView(...

2. Set the limit as a "rectangle" to clear:

D3D12_RECT rect = { firstElementIndex, // left 0, // top firstElementIndex + elementCount, // right 1}; // bottom commandList->ClearUnorderedAccessViewUint( shaderVisibleGpuDescHandle, // ViewGPUHandleInCurrentHeap shaderInvisibleCpuDescHandle, // ViewCPUHandle buf // pResource values, // Values 1, // NumRects !!! &rect); // pRects !!!

Note that in both cases, the boundaries are expressed in entire elements, not bytes.

The behavior I presented above is based on my experiments, as it is not described precisely in the official documentation of [ClearUnorderedAccessViewUint](https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12graphicscommandlist-clearunorderedaccessviewuint) and [ClearUnorderedAccessViewFloat](https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12graphicscommandlist-clearunorderedaccessviewfloat) functions in DX12. The state of DX12 documentation in general is somewhat messy, as I described in my recent post ["All Sources of DirectX 12 Documentation"](https://asawicki.info/news_1794_all_sources_of_directx_12_documentation). Normally, when something is not defined in DX12 documentation, we might resort to the older DX11 documentation. In this case, however, that would be misleading, because DX12 behaves differently from DX11:

`DXGI_FORMAT_R32_UINT`

, so `{1, 2, 3, 4}`

is written as `0x00000001, 0x00000001, ...`

.`DXGI_FORMAT`

enum (shared by DX11 and DX12). There are no 3-byte formats at all, and 8-bit floating-point numbers were not supported by GPUs until recently (as I described in my article `100.0, -100.0`

to a buffer in a normalized format like `DXGI_FORMAT_R16G16_SNORM`

issues no error and clamps the value to the minimum/maximum representing `+1.0 / -1.0`

, becoming `0x7FFF, 0x8001`

in our case.