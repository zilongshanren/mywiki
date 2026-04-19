---
title: 'Secrets of Direct3D 12: Resource Alignment'
url: https://asawicki.info/news_1726_secrets_of_direct3d_12_resource_alignment
published: '2020-04-19'
source_blog: Adam Sawicki Home Page - programming, graphics, games, media, C++, Windows,
  I...
source_site: https://asawicki.info/
category: graphics
fetched: '2026-04-19'
---

Sun

19

Apr 2020

In the new graphics APIs - Direct3D 12 and Vulkan - creation of resources (textures and buffers) is a multi-step process. You need to allocate some memory and place your resource in it. In D3D12 there is a convenient function `ID3D12Device::CreateCommittedResource`

that lets you do it in one go, allocating the resource with its own, implicit memory heap, but it's recommended to allocate bigger memory blocks and place multiple resources in them using `ID3D12Device::CreatePlacedResource`

.

When placing a resource in the memory, you need to know and respect its required size and alignment. Size is basically the number of bytes that the resource needs. Alignment is a power-of-two number which the offset of the beginning of the resource must be multiply of (`offset % alignment == 0`

). I'm thinking about writing a separate article for beginners explaining the concept of memory alignment, but that's a separate topic...

![Direct3D 12 resource alignment](../../assets/7600495df3770a83.png)


Back to graphics, in Vulkan you first need to create your resource (e.g. `vkCreateBuffer`

) and then pass it to the function (e.g. `vkGetBufferMemoryRequirements`

) that will return required size of alignment of this resource (`VkMemoryRequirements::size`

, `alignment`

). In DirectX 12 it looks similar at first glance or even simpler, as it's enough to have a structure `D3D12_RESOURCE_DESC`

describing the resource you will create to call `ID3D12Device::GetResourceAllocationInfo`

and get `D3D12_RESOURCE_ALLOCATION_INFO`

- a similar structure with `SizeInBytes`

and `Alignment`

. I've described it briefly in my article [Differences in memory management between Direct3D 12 and Vulkan](https://asawicki.info/articles/memory_management_vulkan_direct3d_12.php5).

But if you dig deeper, there is more to it. While using the mentioned function is enough to make your program working correctly, applying some additional knowledge may let you save some memory, so read on if you want to make your GPU memory allocator better. First interesting information is that alignments in D3D12, unlike in Vulkan, are really fixed constants, independent of a particular GPU or graphics driver that the user may have installed.

`D3D12_DEFAULT_RESOURCE_PLACEMENT_ALIGNMENT`

.`D3D12_DEFAULT_MSAA_RESOURCE_PLACEMENT_ALIGNMENT`

.So, we have these constants and we also have a function to query for actual alignment. To make things even more complicated, structure `D3D12_RESOURCE_DESC`

contains `Alignment`

member, so you have one alignment on the input, another one on the output! Fortunately, `GetResourceAllocationInfo`

function allows to set `D3D12_RESOURCE_DESC::Alignment`

to 0, which causes default alignment for the resource to be returned.

Now, let me introduce the concept of "small textures". It turns out that some textures can be aligned 4 KB and some MSAA textures can be aligned to 64 KB. They call this "small" alignment (as opposed to "default" alignment) and there are also constants for it:

`D3D12_SMALL_RESOURCE_PLACEMENT_ALIGNMENT`

.`D3D12_SMALL_MSAA_RESOURCE_PLACEMENT_ALIGNMENT`

.| Default | Small | |
|---|---|---|
| Buffer | 64 KB | |
| Texture | 64 KB | 4 KB |
| MSAA texture | 4 MB | 64 KB |

Using this smaller alignment allows to save some GPU memory that would otherwise be unused as padding between resources. Unfortunately, it's unavailable for buffers and available only for small textures, with a very convoluted definition of "small". The rules are hidden in the description of [Alignment member of D3D12_RESOURCE_DESC structure](https://docs.microsoft.com/en-us/windows/win32/api/d3d12/ns-d3d12-d3d12_resource_desc#alignment):

`UNKNOWN`

layout.`RENDER_TARGET`

or `DEPTH_STENCIL`

.Could `GetResourceAllocationInfo`

calculate all this automatically and just return optimal alignment for a resource, like Vulkan function does? Possibly, but this is not what happens. You have to ask for it explicitly. When you pass `D3D12_RESOURCE_DESC::Alignment`

= 0 on the input, you always get the default (larger) alignment on the output. Only when you set `D3D12_RESOURCE_DESC::Alignment`

to the small alignment value, this function returns the same value if the small alignment has been "granted".

There are two ways to use it in practice. First one is to calculate the eligibility of a texture to use small alignment on your own and pass it to the function only when you know the texture fulfills the conditions. Second is to try the small alignment always. When it's not granted, `GetResourceAllocationInfo`

returns some values other than expected (in my test it's `Alignment`

= 64 KB and `SizeInBytes`

= 0xFFFFFFFFFFFFFFFF). Then you should call it again with the default alignment. That's the method that Microsoft shows in their ["Small Resources Sample"](https://github.com/microsoft/DirectX-Graphics-Samples/tree/master/Samples/Desktop/D3D12SmallResources). It looks good, but a problem with it is that calling this function with an alignment that is not accepted generates D3D12 Debug Layer error #721 *CREATERESOURCE_INVALIDALIGNMENT*. Or at least it used to, because on one of my machines the error no longer occurs. Maybe Microsoft fixed it in some recent update of Windows or Visual Studio / Windows SDK?

Here comes the last quirk of this whole D3D12 resource alignment topic: Alignment is applied to offset used in `CreatePlacedResource`

, which we understand as relative to the beginning of an `ID3D12Heap`

, but the heap itself has an alignment too! `D3D12_HEAP_DESC`

structure has `Alignment`

member. There is no equivalent of this in Vulkan. Documentation of [D3D12_HEAP_DESC structure](https://docs.microsoft.com/en-us/windows/win32/api/d3d12/ns-d3d12-d3d12_heap_desc) says it must be 64 KB or 4 MB. Whenever you predict you might create an MSAA textures in a heap, you must choose 4 MB. Otherwise, you can use 64 KB.

Thank you, Microsoft, for making this so complicated! ;) This article wouldn't be complete without the advertisement of open source library: [D3D12 Memory Allocator](https://github.com/GPUOpen-LibrariesAndSDKs/D3D12MemoryAllocator) (and similar [Vulkan Memory Allocator](https://github.com/GPUOpen-LibrariesAndSDKs/VulkanMemoryAllocator/)), which automatically handles all this complexity. It also implements both ways of using small alignment, selectable using a preprocessor macro.

**Update 2025-02-02:** With the new version DirectX 12 Agility SDK 1.716.0-preview, Microsoft introduced "tight alignment" feature that removes the 64 KB alignment requirement for buffers. For more information, see my new blog post [DirectX 12 Agility SDK 1.716.0-preview Explained](https://asawicki.info/news_1783_directx_12_agility_sdk_17160-preview_explained) and Microsoft blog post introducing this feature: [Agility SDK 1.716.0-preview: Tight Alignment of Resources](https://devblogs.microsoft.com/directx/agility-sdk-1-716-0-preview-tight-alignment/)

[Comments](https://asawicki.info/news_1726_secrets_of_direct3d_12_resource_alignment#disqus_thread) |
[#microsoft](https://asawicki.info/news?x=tag&tag=microsoft) [#rendering](https://asawicki.info/news?x=tag&tag=rendering) [#directx](https://asawicki.info/news?x=tag&tag=directx)
[Share](http://www.addtoany.com/share_save?linkurl=https%3A%2F%2Fasawicki.info%2F%2Fnews_1726_secrets_of_direct3d_12_resource_alignment&linkname=Secrets+of+Direct3D+12%3A+Resource+Alignment)