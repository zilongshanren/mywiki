---
title: Rust Game Series - Part 7 - Rust lifetimes and GPU Constant Allocator | Jendrik
  Illner
url: https://www.jendrikillner.com/post/rust-game-part-7/
author: Jendrik Illner
published: '2020-03-11'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

In this part, I will be talking about how to write a custom memory allocator using Rust and D3D11. The concepts are applicable for general-purpose memory allocations but designed for the requirements of constant buffer management.

I am going to try to explain Rust lifetimes in the process and show how it can help to eliminate some classes of bugs.

# Constant Buffer Overview

There are different ways to approach constant buffer management, I will implement it as follows:

- Allocate one large constant buffer for each frame
- Define a linear bump allocator that uses this buffer as backing storage
- Use
[PSSetConstantBuffers1](https://docs.microsoft.com/en-us/windows/win32/api/d3d11_1/nf-d3d11_1-id3d11devicecontext1-pssetconstantbuffers1)to record the offset into this buffer for each draw call

# Extend the screen space quad

Before we can start looking at the memory management, we need to update the shader so that constant data is used. The updated shader below allows the size, position, and final quad-color to be read from the constant buffer.

```
cbuffer ScreenSpaceQuadData : register(b0)
{
float3 color;
float2 scale;
float2 position;
};
VertexToPixelShader VS_main(uint vertex_id: SV_VertexID)
{
VertexToPixelShader output;
switch (vertex_id) {
case 0: output.position_clip = float4(-1, 1, 0, 1); break; // top-left
case 1: output.position_clip = float4( 1, 1, 0, 1); break; // top-right
case 2: output.position_clip = float4(-1, -1, 0, 1); break; // bottom-left
case 3: output.position_clip = float4( 1, -1, 0, 1); break; // bottom-right
}
output.position_clip.xy *= scale;
output.position_clip.xy += position;
return output;
}
float3 PS_main(VertexToPixelShader input) : SV_TARGET
{
return color;
}
```


To interface with this structure from Rust, we need to define a few helper classes.

```
#[repr(C)]
struct Float3 {
x: f32,
y: f32,
z: f32,
}
#[repr(C)]
struct Float2 {
x: f32,
y: f32,
}
#[repr(C)]
struct ScreenSpaceQuadData {
color: Float3,
padding: f32,
scale: Float2,
position: Float2,
}
```


The one thing to call out is `repr(C)`

.

This instructs the compiler to follow the C alignment rules. The Rust and C alignment rules are very similar, but the significant difference is that the Rust compiler is free to reorder fields. At the time of writing, the compiler doesn’t seem to be doing that, however.

One problem is that HLSL doesn’t follow the C alignment rules and instead packs on float4 boundaries.

That’s why you see a `padding: f32`

inside of the ScreenSpaceQuadData definition.
This is required because following the C alignment rules, `scale`

would directly follow `color`

.
To follow the HLSL rules, we need one padding float to fill the float4.

The following two float2 types are packed into a single float4, so no padding is required for those variables.

With this, we have a Rust layout that matches the HLSL constant buffer layout. Time to look at the API result of the constant buffer system, and then I will present the thoughts and reasons behind the design.

```
let frame_constant_buffer = create_constant_buffer(
graphics_device_layer.native.device,
1024 * 8, // size of the buffer
),
let mut gpu_heap = LinearAllocator {
gpu_data: map_gpu_buffer(buff, graphics_device_layer.native.context),
state: LinearAllocatorState { used_bytes: 0 },
};
let obj1_alloc: HeapAlloc<ScreenSpaceQuadData> = HeapAlloc::new(
ScreenSpaceQuadData { color, padding: 0.0,
scale: Float2 { x: 1.0, y: 1.0 },
position: Float2 { x: 0.0, y: 0.0 },
},
&gpu_heap.gpu_data,
&mut gpu_heap.state,
);
let first_constant: u32 = obj1_alloc.first_constant_offset;
let num_constants: u32 = obj1_alloc.num_constants;
command_context1.as_ref().unwrap().PSSetConstantBuffers1(
0, // which slot to bind to
1, // the number of buffers to bind
&frame_data.frame_constant_buffer.native_buffer, // the buffer to bind
&first_constant, // the first constant offset
&num_constants, // number of constants to bind
);
command_context.as_ref().unwrap().Draw(4, 0);
unmap_gpu_buffer(gpu_heap.gpu_data, graphics_device_layer.native.context);
```


# Implementation

The underlying memory is provided from a constant buffer. This buffer is located in GPU accessible memory and needs to be mapped so that the CPU can access it.

The function interface looks like this:

```
fn map_gpu_buffer<'a>(
buffer: &'a mut ID3D11Buffer,
context: &ID3D11DeviceContext,
) -> MappedGpuData<'a>
```


The one thing that will immediately stick out is the use `<'a>`

and `'a`

on the types.

These are lifetime annotations. Every reference in Rust has a lifetime, but in many situations, [lifetime-elision](https://doc.rust-lang.org/1.9.0/book/lifetimes.html#lifetime-elision) makes it possible to omit the annotations. But there are many situations in which the lifetime is unclear and needs to be provided explicitly.

An Important point to stress, the borrow checker only looks at the function definition for lifetime tracking. It doesn’t inspect the code inside a function.

In this case, the lifetime annotations can be read as follows:

The function accepts a reference to an ID3D11Buffer. This buffer object has lifetime `'a`

.
The function returns a MappedGpuData, which has the same lifetime annotation `'a`

.
This means that MappedGpuData internally contains a reference to data based on ID3D11Buffer.

Therefore this requires the return value to have the same or shorter lifetime then the buffer it was derived from.

The struct needs explicit lifetime annotations to make this visible to the compiler.

```
pub struct MappedGpuData<'a> {
data: &'a [u8], // reference to slice of cpu accessible gpu memory
buffer: &'a mut ID3D11Buffer, // reference to the d3d11 buffer the data comes from
}
```


Now we have the building blocks required for the implementation of `map_gpu_buffer`


```
fn map_gpu_buffer<'a>(
buffer: &'a mut ID3D11Buffer,
context: &ID3D11DeviceContext,
) -> MappedGpuData<'a> {
let mut mapped_resource = D3D11_MAPPED_SUBRESOURCE {
pData: std::ptr::null_mut(),
RowPitch: 0,
DepthPitch: 0,
};
// map the buffer
let result: HRESULT = unsafe {
context.Map(
buffer as *mut ID3D11Buffer as *mut winapi::um::d3d11::ID3D11Resource,
0, D3D11_MAP_WRITE_NO_OVERWRITE, 0,
&mut mapped_resource,
)
};
MappedGpuData {
data: unsafe {
std::slice::from_raw_parts_mut(
mapped_resource.pData as *mut u8,
mapped_resource.RowPitch as usize,
)
},
buffer,
}
}
```


Most of these are just D3D11 function calls, but the construction of the MappedGpuData requires a bit of description.
The structure contains a slice to CPU accessible GPU memory. D3D11 provides us with a pointer and a size, we can combine this information using the unsafe `from_raw_parts_mut`

to build a slice which can be used as a “normal” rust slice afterward.

The mutability of the borrow is forwarded to the returned type. This is independent of how the struct is defined. Since the buffer is a mutable borrow also the returned MappedGpuData will be a mutable borrow. This means we cannot map the same buffer twice unless we release the returned borrow.

Unmapping the buffer is quite straightforward. No lifetime annotations are required as MappedGpuData is passed in by moving ownership. This means after `unmap_gpu_buffer`

returns, the `mapped_data`

will not be valid anymore and cannot be accessed.

```
fn unmap_gpu_buffer(mapped_data: MappedGpuData, context: &ID3D11DeviceContext) {
unsafe {
context.Unmap(
mapped_data.buffer as *mut ID3D11Buffer as *mut winapi::um::d3d11::ID3D11Resource,
0,
);
}
}
```


With this functionality in place, we are now able to map and unmap GPU constant memory.

Time to implement an allocator that uses this memory buffer as backing storage.

```
pub struct LinearAllocatorState {
used_bytes: usize,
}
pub struct LinearAllocator<'a> {
gpu_data: MappedGpuData<'a>,
state: LinearAllocatorState,
}
```


The allocator is a simple linear allocator called LinearAllocator. Here the state is split into two separate structs to separate mutable and immutable state.

Why this split? It’s related to the forwarding of borrow mutability. Let us look at how it’s used:

```
let obj1_alloc: HeapAlloc<ScreenSpaceQuadData> = HeapAlloc::new(
ScreenSpaceQuadData { color, padding: 0.0,
scale: Float2 { x: 1.0, y: 1.0 },
position: Float2 { x: 0.0, y: 0.0 },
},
&gpu_heap.gpu_data,
&mut gpu_heap.state,
);
```


The implementation of this look as follows:

```
pub struct HeapAlloc<'a, T> {
ptr: &'a mut T,
first_constant_offset: u32,
num_constants: u32,
}
impl<'a, T> HeapAlloc<'a, T> {
pub fn new(
x: T,
gpu_data: &'a MappedGpuData,
state: &mut LinearAllocatorState,
) -> HeapAlloc<'a, T>
```


HeapAlloc is following the design of [Box](https://doc.rust-lang.org/std/boxed/struct.Box.html) but adjusted for the requirements of D3D11 constant buffer binding.
It contains a mutable borrow of generic Type T with an explicit lifetime annotation.

The HeapAlloc::new function has an explicit lifetime annotation too, and the return type lifetime matches the lifetime of the MappedGpuData passed into the function.

As I mentioned earlier, the borrow type is forwarded to the reference. Since we want multiple allocations to be done into the same buffer, we cannot use a mutable reference. Otherwise, a second allocation would also return a mutable reference. But only a single mutable borrow is allowed to be active at the same time.

We still need to modify the state of the LinearAllocator to increment the allocation offset. Therefore we split the state from the buffer and pass the LinearAllocatorState as mutable borrow.

The full implementation is below:

```
impl<'a, T> HeapAlloc<'a, T> {
pub fn new(
x: T,
gpu_data: &'a MappedGpuData,
state: &mut LinearAllocatorState,
) -> HeapAlloc<'a, T> {
let allocation_size: usize = round_up_to_multiple(std::mem::size_of::<T>(), 256);
let data_slice = gpu_data.data;
let start_offset_in_bytes = state.used_bytes;
let data_ptr =
data_slice[state.used_bytes..(state.used_bytes + allocation_size)].as_ptr() as *mut T;
state.used_bytes += allocation_size;
unsafe {
// write data into target destination
std::ptr::write(data_ptr, x);
HeapAlloc {
ptr: data_ptr.as_mut().unwrap(),
first_constant_offset: (start_offset_in_bytes / 16) as u32,
num_constants: (allocation_size / 16) as u32,
}
}
}
}
```


The core of the alloc construction is based on slices. The allocator uses the base slice for data and sub-divides this slice into smaller sub-slices. This operation internally performs range checks to validate that constant allocations don’t overflow the source buffer and will cause a Panic if an overflow would be happening.

With all these pieces in place, we have a working allocator system for constants.

If you would like to use a HeapAlloc

```
impl<T> std::ops::Deref for HeapAlloc<'_, T> {
type Target = T;
fn deref(&self) -> &T {
self.ptr
}
}
impl<T> std::ops::DerefMut for HeapAlloc<'_, T> {
fn deref_mut(&mut self) -> &mut T {
self.ptr
}
}
```


A few D3D11behaviour worth mentioning related to PSSetConstantBuffers1:

First of all, this doesn’t work on Windows 7 and requires extended interface access ([ID3D11DeviceContext1](https://docs.microsoft.com/en-us/windows/win32/api/d3d11_1/nn-d3d11_1-id3d11devicecontext1))

To get to the extented interface query it afer creating the base interface:

```
command_context.as_ref().unwrap().QueryInterface(
&ID3D11DeviceContext1::uuidof(),
&mut command_context1 as *mut *mut ID3D11DeviceContext1
as *mut *mut winapi::ctypes::c_void,
);
```


Additionally, Cargo.toml will need to be adjusted to list d3d11_1

```
winapi = { version = "0.3", features = ["winuser", "d3d11", "d3d11_1", "winerror", "dxgi1_2"] }
```


There is also a bug when this feature is not supported by the driver, as described in [MSDN - Calling PSSetConstantBuffers1 with command list emulation](https://docs.microsoft.com/en-us/windows/win32/api/d3d11_1/nf-d3d11_1-id3d11devicecontext1-pssetconstantbuffers1#calling-pssetconstantbuffers1-with-command-list-emulation) but a workaround is provided.

TLDR when runtime emulation doesn’t always update the offsets, need to first unbind constant buffers explicitly :(

The full implementation is on GitHub, and the previously constant color quad is now animated with a cyclic color change between Red and Black.

![Quad changing color on a blue background Quad changing color on blue background](../../assets/2d61f317b517ec4b.gif)


Please let me know if I got something wrong or explained it in an unclear way.

Before continuing with the game, I am going to provide an overview of how I am using Rust with Visual Studio on Windows in the next post.

The code is available on [GitHub](https://github.com/jendrikillner/RustMatch3/releases/tag/rust-game-part-7)