---
title: Rust Game Series - Part 6 - Drawing a procedural quad
url: https://www.jendrikillner.com/post/rust-game-part-6/
author: Jendrik Illner
published: '2019-12-11'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

With a working swap chain, nothing will stop us from rendering a quad.

We will be looking at the following topics:

- generating vertex data in a shader
- compile shaders
- load shaders
- record draw commands
- executing command lists

## procedural quad shaders

What is a procedural quad? This means we don’t use any data from vertex buffers, but instead, the system provided SV_VertexID is used to generate the vertex positions inside of the vertex shader itself.

This makes drawing a quad easier since no buffer needs to created, filled from the CPU, and bound to the pipeline. The vertex shader is below:

```
VertexToPixelShader VS_main(uint vertex_id: SV_VertexID)
{
VertexToPixelShader output;
switch (vertex_id) {
case 0: output.position_clip = float4(-1, 1, 0, 1); break; // top-left
case 1: output.position_clip = float4( 1, 1, 0, 1); break; // top-right
case 2: output.position_clip = float4(-1, -1, 0, 1); break; // bottom-left
case 3: output.position_clip = float4( 1, -1, 0, 1); break; // bottom-right
}
output.position_clip.xy *= 0.5f; // change the size of the quad a bit
return output;
}
```


## compile shader

Given a shader, we need to compile it; for now, a batch file is all that is required. Shaders are compiled using the Microsoft FXC compiler, which gets distributed in the Windows SDK.

```
:: compile VS shader
..\build_environment\microsoft\fxc\fxc.exe /T vs_4_0 src_data\shaders\screen_space_quad.hlsl /EVS_main /Fo target_data\shaders\screen_space_quad.vsb
..\build_environment\microsoft\fxc\fxc.exe /T ps_4_0 src_data\shaders\screen_space_quad.hlsl /EPS_main /Fo target_data\shaders\screen_space_quad.psb
```


### shader loading

Loading and creation shaders are straightforward from Rust. The std filesystem provides the functionality to load binary files into memory. With the data loaded into memory, a pointer and length are passed to CreateVertexShader/CreatePixelShader, and the shaders are ready to use afterward

```
// load a shader
let vertex_shader_memory = std::fs::read("target_data/shaders/screen_space_quad.vsb").unwrap();
let pixel_shader_memory = std::fs::read("target_data/shaders/screen_space_quad.psb").unwrap();
let error: HRESULT = d3d11_device.CreateVertexShader(
vertex_shader_memory.as_ptr() as *const winapi::ctypes::c_void,
vertex_shader_memory.len(),
std::ptr::null_mut(),
&mut vertex_shader as *mut *mut ID3D11VertexShader,
);
let error: HRESULT = d3d11_device.CreatePixelShader(
pixel_shader_memory.as_ptr() as *const winapi::ctypes::c_void,
pixel_shader_memory.len(),
std::ptr::null_mut(),
&mut pixel_shader as *mut *mut ID3D11PixelShader,
);
```


## record draw commands

Normally most D3D11 code would now directly execute its work on the immediate context. I prefer to use DeferredContext instead.

A deferred context allows commands to be recorded into a command list that can later be executed using the immediate context. I prefer this way because it makes more logical sense to me.

GPU execution from the immediate context is under the control of the driver, and there are no guarantees when work might be executed. With an explicit command list execution steps, it’s apparent when CPU work is being done to record commands compared to when the GPU is allowed to execute those commands.

To be able to record a command list, a deferred context needs to be created.

```
let mut command_context: *mut ID3D11DeviceContext = std::ptr::null_mut();
let error = graphics_device.CreateDeferredContext(0, &mut command_context);
```


Given this context, we can now set up the state for our quad. The code is very compact, all the work is done in the vertex shader without requiring any buffers or shader resource bindings.

```
// set viewport for the output render target
command_context.RSSetViewports(1, &viewport);
// bind backbuffer as render target
let rtvs: [*mut winapi::um::d3d11::ID3D11RenderTargetView; 1] = [graphics_layer.backbuffer_rtv];
command_context.OMSetRenderTargets( 1, rtvs.as_ptr(), std::ptr::null_mut() );
// bind the shaders
command_context.VSSetShader(vertex_shader, std::ptr::null_mut(), 0);
command_context.PSSetShader(pixel_shader, std::ptr::null_mut(), 0);
// we are drawing 4 vertices using a triangle strip topology
command_context.IASetPrimitiveTopology(D3D11_PRIMITIVE_TOPOLOGY_TRIANGLESTRIP);
command_context.Draw(4, 0);
```


This recorded all the commands. And are now waiting to be executed by the GPU. For this, we need access to the recorded command list and execute it using the immediate context.

```
let mut command_list: *mut ID3D11CommandList = std::ptr::null_mut();
command_context.FinishCommandList(0, &mut command_list);
immediate_context.ExecuteCommandList(command_list, 1);
```


Given all this, and a pixel shader that writes a yellow color. We get to see this:

![Yellow quad on a blue background Yellow quad on blue background](../../assets/968452ec547d9a94.png)


Next, I am going to dive deeper into Rust and use lifetimes to write a custom allocator for safe, constant buffer management.

The code is available on [GitHub](https://github.com/jendrikillner/RustMatch3/releases/tag/rust-game-part-6)