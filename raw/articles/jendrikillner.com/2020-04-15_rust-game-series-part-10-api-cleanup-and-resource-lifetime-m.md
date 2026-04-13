---
title: Rust Game Series - Part 10 - API cleanup and resource lifetime management
url: https://www.jendrikillner.com/post/rust-game-part-10/
author: Jendrik Illner
published: '2020-04-15'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

After last week’s post, the code is split into multiple crates, but the game code is still full of direct D3D11 functionality that requires unsafe code.

I would like the game code to be free of unsafe code. Unsafe code is required, but it should be hidden from the game in the abstraction layers.

## Main API components

After a cleanup pass of the API, only a few concepts are left. I am following a very simplified D3D12 design.

- GraphicsDeviceLayer
- Handles d3d11 creation, resources, and swap chain related functionality

- Constant Buffer
- buffer creation and allocator

- Pipeline State Object
- groups vertex/pixel shader. This will later be extended to hold other required state

- Render Pass
- bind render targets and handles color/depth clear

- Command Lists
- contains all rendering related functionality


The implementation of this is relatively straight forward. Most Rust structs are mostly wrapper objects around the native D3D11 objects at this point.

The API example is below:

```
let mut graphics_layer: GraphicsDeviceLayer =
create_device_graphics_layer(main_window.hwnd, args.enable_debug_device).unwrap();
let pso_desc = PipelineStateObjectDesc {
shader_name: "target_data/shaders/screen_space_quad",
};
let screenspace_quad_pso: PipelineStateObject = create_pso(&graphics_layer.device, pso_desc);
begin_render_pass(
&mut graphics_layer.graphics_command_list,
color,
&graphics_layer.backbuffer_rtv,
);
let obj1_alloc = HeapAlloc::new(
ScreenSpaceQuadData {
color,
padding: 0.0,
scale: Float2 { x: 0.5, y: 0.5 },
position: Float2 { x: 0.0, y: 0.0 },
},
&gpu_heap.gpu_data,
&mut gpu_heap.state,
);
bind_pso(
&mut graphics_layer.graphics_command_list,
&screenspace_quad_pso,
);
bind_constant(&mut graphics_layer.graphics_command_list, 0, &obj1_alloc);
draw_vertices(&mut graphics_layer.graphics_command_list, 4);
unmap_gpu_buffer(gpu_heap.gpu_data, &graphics_layer);
execute_command_list(&graphics_layer, &graphics_layer.graphics_command_list);
present_swapchain(&graphics_layer);
```


The more interesting parts from a Rust perspective is the way to handle D3D11 resource management.

## D3D11 memory management

In D3D11, each object is reference counted, and resources are only released once the reference count reaches 0. Each object implements the IUnknown interface that provides the necessary functionality.

D3D11 will internally increment ref counts, but it’s the developers’ responsibility to release these.

In Rust, generally, all resources are released once they reach the end of their lifetime. And I would like to keep these semantics for my API.

This can be achieved through the implementation of the [Drop trait](https://doc.rust-lang.org/std/ops/trait.Drop.html).

### Drop Trait

A [trait object](https://doc.rust-lang.org/1.8.0/book/traits.html) defines the notion of an Interface.
It allows us to express what types of functionality are supported by a type.

This can be used for static dispatching for the use in generics/templates (in C++) or dynamic dispatching.

A struct can implement any number of traits. Some, like the drop trait, are provided by the compiler unless we specify a customized implementation.

And that’s what we are doing for our wrapper types to enable the D3D resources to be released in a way that matches Rust semantics.

The core type of the graphics layer is the GraphicsDeviceLayer struct. The implementation looks like this:

```
pub struct GraphicsDeviceLayer<'a> {
pub immediate_context: *mut ID3D11DeviceContext,
pub swapchain: *mut IDXGISwapChain1,
pub backbuffer_texture: *mut ID3D11Texture2D,
pub backbuffer_rtv: RenderTargetView<'a>,
pub graphics_command_list: GraphicsCommandList<'a>,
pub device: GraphicsDevice<'a>,
}
impl Drop for GraphicsDeviceLayer<'_> {
fn drop(&mut self) {
unsafe {
leak_check_release( self.backbuffer_texture.as_ref().unwrap(), 0, self.device.debug_device);
leak_check_release( self.immediate_context.as_ref().unwrap(), 0, self.device.debug_device);
leak_check_release( self.swapchain.as_ref().unwrap(), 0, self.device.debug_device);
}
}
}
```


You can see that the `impl Drop`

only contains the explicit release logic for the native D3D11 objects stored as part of the object itself.

`leak_check_release`

will assert if the reference count has not reached 0 and print additional information using the D3D11 debug device if available.

All other objects are Rust types, and I implemented the Drop trait for all of them. They are responsible for deleting the objects they contain.

The order in which drop is called might be surprising.

First, the drop function for the root object is called. At the end of the root drop functions, all drop functions of the child items are called. This is done in the order in which they are defined in the struct.

If those objects have children themselves, those will be called before moving on to the next item in the parent struct.

For this class structure it will be in this order:

GraphicsDeviceLayer > RenderTargetView > GraphicsCommandList > (possible child types) > GraphicsDevice

Implementing the drop trait for all wrapper objects enables us to remove all manual Release calls from the game code. The borrow checker and the lifetime specifiers make sure that all objects will be released in the correct order.

Externally owned objects will be released first. For example, Constant Buffer. The lifetime specifier defines that the references are not allowed to outlive the GraphicsDeviceLayer. Therefore the object has to be dropped before dropping the GraphicsDeviceLayer.

## Next Part

With this work completed, we have a foundation to build upon. And it’s time to start implementing a first gameplay prototype. What’s missing for that?

Drawing multiple quads and input handling. I will be looking at these topics next.

The code is available on [GitHub](https://github.com/jendrikillner/RustMatch3/releases/tag/rust-game-part-10)