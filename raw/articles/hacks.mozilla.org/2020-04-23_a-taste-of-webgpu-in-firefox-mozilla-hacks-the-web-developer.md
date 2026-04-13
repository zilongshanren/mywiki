---
title: A Taste of WebGPU in Firefox – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2020/04/experimental-webgpu-in-firefox/
author: Dzmitry Malyshau
published: '2020-04-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

WebGPU is an emerging API that provides access to the graphics and computing capabilities of hardware on the web. It’s designed from the ground up within the W3C [GPU for the Web](https://www.w3.org/community/gpu/) group by all major browser vendors, as well as Intel and a few others, guided by the following principles:


We are excited to bring WebGPU support to Firefox because it will allow richer and more complex graphics applications to run portably in the Web. It will also make the web platform more accessible to teams who mostly target modern native platforms today, thanks to the use of modern concepts and first-class [WASM](https://webassembly.org/) (WebAssembly) support.

## API concepts

WebGPU aims to work on top of modern graphics APIs: [Vulkan](https://www.khronos.org/vulkan/), [D3D12](https://docs.microsoft.com/en-us/windows/win32/direct3d12/directx-12-programming-guide), and [Metal](https://developer.apple.com/metal/). The constructs exposed to the users reflect the basic primitives of these low-level APIs. Let’s walk through the main constructs of WebGPU and explain them in the context of [WebGL](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API) – the only baseline we have today on the Web.

### Separation of concerns

The first important difference between WebGPU and WebGL is that WebGPU separates resource management, work preparation, and submission to the GPU ([graphics processing unit](https://en.wikipedia.org/wiki/Graphics_processing_unit)). In WebGL, a single context object is responsible for everything, and it contains a lot of associated state. In contrast, WebGPU separates these into multiple different contexts:

`GPUDevice`

creates resources, such as textures and buffers.`GPUCommandEncoder`

allows encoding individual commands, including render and compute passes.- Once done, it turns into
`GPUCommandBuffer`

object, which can be submitted to a`GPUQueue`

for execution on the GPU. - We can present the result of rendering to the HTML canvas. Or multiple canvases. Or no canvas at all – using a purely computational workflow.

Overall, this separation will allow for complex applications on the web to stream data in one or more [workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers) and create any associated GPU resources for it on the fly. Meanwhile, the same application could be recording work on multiple workers, and eventually submit it all together to `GPUQueue`

. This matches multi-threading scenarios of native graphics-intensive applications and allows for high utilization of multi-core processors.

### Pipeline state

The second important change is how WebGPU encapsulates pipeline state.

In WebGL, the user would create a [shader](https://developer.mozilla.org/en-US/docs/Web/API/WebGLShader) program at program initialization. Later when the user attempts to use this shader program, the driver takes into consideration all the other states currently set, and may need to internally recompile the shader program. If the driver does recompile the shader program, this could introduce CPU stalls.

In contrast, WebGPU has the concept of a pipeline state object (namely, `GPURenderPipeline`

and `GPUComputePipeline`

). A pipeline state object is a combination of various states that the user creates in advance on the device – just like in native APIs. The user provides all this state upfront, which allows the browsers and hardware drivers to avoid extra work (such as shader recompilation) when it’s used later in GPU operations.

From the developer perspective, it’s easier to manage these coarse state objects as well. They don’t have to think as much about which of the fine-grained states to change, and which ones to preserve.

The pipeline state includes:

- Shaders
- Layouts of vertex buffers and attributes
- Layouts of bind groups
- Blending, depth, and stencil states
- Formats of the output render targets

### Binding model

A third difference between WebGPU and WebGL is the binding model. The WebGPU binding model is largely inspired by Vulkan (as an intersection of capabilities of the target native APIs) and allows resources to be grouped together into a `GPUBindGroup`

object. Then we bind `GPUBindGroup`

s during command recording in order to use the resources within shaders.

By creating these bind groups upfront, the graphics driver can perform any necessary preparations in advance. This allows the browser to change resource bindings much faster between draw calls.

Most importantly, the user has to describe the layout of resource bindings ahead of time, baking it into a `GPUBindGroupLayout`

object. Both pipeline states and concrete bind groups know about the bind group layout as well. This knowledge serves as a contract between the shader and the API. It allows the browser or the driver to lay out resources in a way that allows faster binding.

### Complementary talks

There are public talks by the active members of the standards group, which may help better understanding of what the API is, how it evolved, and how we expect it to be used. Dzmitry Malyshau from Mozilla talked about the Rust aspect of implementing WebGPU for native platforms at [Fosdem 2020](https://fosdem.org/2020/schedule/event/rust_webgpu/). Earlier, Corentin Wallez from Google gave an overview of WebGPU API at [DevFest Toulouse 2019](https://www.youtube.com/watch?v=_UFkuYZrXV0). Last but not the least, the [Google I/O 2019](https://www.youtube.com/watch?v=K2JzIUIHIhc) presentation was full of shiny demos and code samples.

## Firefox story

### Tech stack

In Firefox, we are working on a complete ground-up implementation of the WebGPU specification. The core logic is provided by the [wgpu-core](https://github.com/gfx-rs/wgpu) project that is written by the Rust community with Mozilla’s help. It’s based on the [gfx-rs](https://github.com/gfx-rs/gfx/) project which is able to translate Vulkan-like GPU workloads to D3D12, D3D11, Metal, and even OpenGL (to some degree).

We are also working on the [shader infrastructure](https://github.com/gfx-rs/naga) that would allow us to work with WebGPU Shading Language, validate it against the API expectations, and convert it to the backend shading language that is expected by the driver.

The latest and greatest of our work can be seen in [Nightly](https://blog.nightly.mozilla.org/) with the “`dom.webgpu.enabled = true`

” preference set, which also requires “`gfx.webrender.all = true`

”. It should work on Windows 7 and Linux with Vulkan drivers, Windows 10, macOS, and even on qualified Android devices. Be prepared for a bumpy ride because everything is still a work in progress!

### Examples

At the time of writing, Firefox Nightly can run all of the Google [SPIR-V-based](https://austineng.github.io/webgpu-samples/) WebGPU samples with an exception of “animometer” (which relies on `GPURenderBundle`

that we haven’t yet implemented). Here is Nightly rendering the “fractal cube” on Linux/Vulkan:

We can also execute computational workloads. For example, here is Nightly rendering the “boids” example on Windows 10/Vulkan:

The Rust community has also been working on targeting the WebGPU directly in [wgpu-rs](https://github.com/gfx-rs/wgpu-rs) (which provides a Rust API and uses the same [wgpu](https://github.com/gfx-rs/wgpu) project for implementing it). This exciting work opens the doors for us to have many existing applications in the Rust ecosystem running in the browser. The first batch of these applications is `wgpu-rs`

[own examples](https://wgpu.rs). Here is Nightly rendering the “shadow” example on macOS/Metal:

### Future work

There are many things missing in Firefox Nightly to make this WebGPU implementation truly usable. It’s still early days, and we just got the first examples working.

#### Error handling

One major area that is missing is the **error model**. WebGPU errors work on the concept of “contagious internal nullability” (also called “maybe monad”): at some point, an object that’s incorrectly used may become “Invalid”. The actual error will be returning back to the content side asynchronously. If any other object becomes dependent on it (for example, a texture as a part of a bind group object), that parent object also becomes “Invalid” – so that state is contagious. Implementing this error model will allow developers to iterate on code without crashing the GPU process (which is typically a safe Rust panic), or causing any other side effects.

#### Accelerated presentation

Another important bit to implement is hardware support for presentation. Currently, to display the rendered image to an HTML canvas, the image is first rendered on the GPU. It is then read back to a CPU-side buffer, which we provided to WebRender as an “external image”. WebRender uploads the image contents to the GPU again and finally displays it on the HTML canvas. This round-trip is unnecessary in general. Instead, we want to use the platform-specific mechanisms of surface sharing between the WebGPU backend APIs and WebRender. We’ll need to approach each platform independently to implement this, while keeping the current path as fall-back.

#### API coverage

Finally, there are bits of the specification we have not implemented yet. This will be a constant process of catching up as the spec evolves, until it eventually stabilizes. One of the missing pieces is support for `GPURenderBundle`

objects. Each bundle contains a small sequence of rendering commands that it can use and reuse multiple times in recording of passes. It’s currently the only mechanism of re-using the commands in the API. It will be important for the more complex kinds of content on the Web, such as open-world games.

## State of the spec

The WebGPU [specification](https://gpuweb.github.io/gpuweb/) is developed [on GitHub](https://github.com/gpuweb/gpuweb) in the form of [Bikeshed](https://github.com/tabatkins/bikeshed) documents (separate for the main WebGPU spec and the WebGPU shading language). It’s open for participation!

The group has mostly resolved the major architecture issues of the API. Recently we agreed on the WebGPU Shading Language direction based on the [Tint prototype](https://docs.google.com/presentation/d/1qHhFq0GJtY_59rNjpiHU--JW4bW4Ji3zWei-gM6cabs). We still need to solve a lot of design riddles before we make it available to end users to write shaders in.

One of the unresolved issues is the API for data transfers between CPU and GPU. Working with memory directly is where the web platform differs greatly from native platforms. We’ve discussed a dozen different proposals but [have not yet found](https://github.com/gpuweb/gpuweb/issues/697#issuecomment-613050478) a design solution that fulfills our principles.

Overall, the spec is still heavily a work in progress. It’s available for early hackers but not recommended for any use in production yet. We are hoping to get a minimum-viable-product version of the spec and implementations by the end of 2020. The current state of implementations can be checked on [webgpu.io](http://webgpu.io).

## About
[
Dzmitry Malyshau ](https://kvark.github.io)

Dzmitry is an elder rustacean, who worked in AAA game development. He joined Mozilla in 2016 to help kicking WebRender integration into Gecko, and designing the new WebGPU API in collaboration with all browser vendors.

## 12 comments

JackieApril 23rd, 2020 at 10:49JCApril 24th, 2020 at 01:31Dzmitry MalyshauApril 24th, 2020 at 08:34WhyNotHugoApril 24th, 2020 at 05:31Dzmitry MalyshauApril 24th, 2020 at 08:46TexnapbMay 20th, 2020 at 14:56Dzmitry MalyshauMay 20th, 2020 at 17:33JackieApril 26th, 2020 at 11:02Dzmitry MalyshauApril 27th, 2020 at 07:39Butch ShivelyApril 30th, 2020 at 14:27maikalalMay 1st, 2020 at 00:01Alex G RiceMay 14th, 2020 at 15:26