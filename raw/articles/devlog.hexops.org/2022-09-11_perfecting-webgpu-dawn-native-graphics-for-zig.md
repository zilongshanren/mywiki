---
title: Perfecting WebGPU/Dawn native graphics for Zig
url: https://devlog.hexops.org/2022/perfecting-webgpu-native/
published: '2022-09-11'
source_blog: Hexops' devlog
source_site: https://devlog.hexops.org/
category: graphics
fetched: '2026-04-19'
---

' devlog

We’ve just finished a complete rewrite of `mach/gpu`

(WebGPU/Dawn bindings for Zig), with 700+ commits, ~7.4k LOC, and 100% API coverage.

WebGPU (not to be confused with WebGL) is a modern graphics API, acting as a unified API to the underlying Vulkan/Metal/DirectX APIs. Despite it’s name, it is also designed for use in native applications via its C API.

Dawn is the C++ implementation of WebGPU by Google, used in Chrome, planned to be shipped to millions of browsers in the not too distant future.

`mach/gpu`

: WebGPU for Zig

6 months ago we [released Mach v0.1](https://devlog.hexops.org/2022/mach-v0.1-zig-graphics-in-60s/) which enabled the creation of native applications using WebGPU graphics in Zig:

![](../../assets/e329616d94fcb225.gif)

It all Just Works™ out of the box in under ~60s - all you need is `zig`

, `git`

, and `curl`

:

```
git clone https://github.com/hexops/mach
cd mach/
zig build run-example-boids
```


(requires Zig v0.10+, see [known issues](https://github.com/hexops/mach/blob/main/doc/known-issues.md).)

We do all the heavy-lifting behind the scenes for you: building Dawn using Zig as a C++ compiler, rewriting build scripts in Zig (so you don’t need ninja/cmake/etc), package up all required dependencies so you don’t need Google’s `depot_tools`

, and more.

Because of this, cross-compilation to every major desktop OS is available at the flip of a switch:

```
$ zig build example-boids -Dtarget=x86_64-windows
$ zig build example-boids -Dtarget=x86_64-linux
$ zig build example-boids -Dtarget=x86_64-macos.12
$ zig build example-boids -Dtarget=aarch64-macos.12
```


But this is old news! We released this 6 months ago-so what’s new since?

## Zig + WebGPU showcase (10+ examples)

The new [Zig WebGPU demo showcase](https://machengine.org/gpu) has 12+ examples you can try on your own machine to begin learning Zig and WebGPU quickly:

## Mach core vs. Mach engine

![](../../assets/e6a8ef47ff3d84ff.png)


Mach has a choose-your-journey development strategy, where you don’t even have to adopt the entire engine to benefit from it. All the WebGPU examples we provide are *Mach core apps*: they rely on Mach for window creation, user input, and setting up the WebGPU API - nothing else. Using *Mach core*, you write your own engine!

Why use this over, say, GLFW and WebGPU on your own? The benefit is that this will work on Desktop, WebAssembly (soon), Mobile (future), and consoles (long term.) You can write Mach core apps in Zig, or other languages via `libmach`

(more on this later.) Think of Mach core as *a competitor to SDL/GLFW.*

In the future we’ll offer *Mach engine* apps, where you buy into our ECS, Unity/Unreal-like editor, and other composable building-blocks that make up the engine at your choosing. But this isn’t ready today.

### Dawn/WebGPU on the Steam Deck

We believe Linux should be a first-class platform, and because of this we’ve found Mach all Just Works™ right out of the box on the Steam Deck (running natively as a Linux Vulkan application, no DirectX or Proton in the mix.):

## A complete rewrite of `mach/gpu`

to be lean & mean

When we wrote the initial WebGPU bindings for Zig 6+ months ago, our primary goal was just to get *something* working to where we could start building out examples: we always knew we’d need to revisit things later, especially as Browser support, the use of native extensions in Dawn (like bindless support in the future, etc.), overhead & other aspects became clear.

We’ve finally done that revisit in a month-long complete rewrite of `mach/gpu`

from the ground up. This brings 700+ commits, zero-overhead bindings, Dawn native extensions, and much more. Here are the highlights.

### Righting our wrongs: runtime interfaces

One goal of `mach/gpu`

is to be able to intercept WebGPU API calls, so that we can provide superior debugging facilities in the future (imagine record-and-replay, step-by-step debugging of WebGPU API calls, etc.)

In the old `mach/gpu`

, we achieved this by wrapping each WebGPU API object that had methods (like textures, render pass encoders, etc.) in a *runtime interface* similar to Zig’s `std.mem.Allocator`

interface:

```
pub const Texture = struct {
/// The type erased pointer to the Texture implementation
/// Equal to c.WGPUTexture for NativeInstance.
ptr: *anyopaque,
vtable: *const VTable,
};
pub const VTable = struct {
destroy: fn (ptr: *anyopaque) void,
// ...
};
pub inline fn destroy(tex: Texture) void {
tex.vtable.destroy(tex.ptr);
}
```


Our thought process was simply to follow any established patterns, learn what didn’t work about it by writing examples, and then revisiting the API later. Even six months ago, though, we knew there were issues with this approach.

**The problem:** In WebGPU, `Descriptor`

data structures are often passed to methods: these fairly large data structures contain a wide range of options and graphics pipeline state to use, and often involve passing a list of WebGPU objects as a field - or nested field - as part of the Descriptor data structure. Because our `Texture`

involves keeping a `ptr`

(the interface implementation) and a `vtable`

pointer (our implementation methods) it meant that a `gpu.Texture`

was two pointers, while a C `WGPUTexture`

was a single pointer - breaking ABI compatibility.

This meant that our `Texture`

could not simply be passed to a C API expecting a `WGPUTexture`

: instead, we needed to pass our `.ptr`

field only. This had viral effects, though: every `Descriptor`

struct which embedded a `Texture`

needed to be copied/rewritten to convert our two-pointer `Texture`

to a single-pointer `WGPUTexture`

. Worse yet, some descriptors hold *dynamic arrays* of such objects, requiring us to *copy an array to a temporary (and worst-case, heap-allocated), buffer* just in order to call the actual WebGPU C API.

Needless to say, this was a cancer we felt we absolutely had to get rid of in the rewrite.

### Comptime interfaces

While we want to get rid of runtime interfaces, maintain C ABI compatability, and be zero-overhead-we’d still like to be able to intercept WebGPU API calls if desired, so that we can provide superior debugging facilities in the future.

Zig’s `std.mem.Allocator`

being a *runtime interface* makes sense because they have different use cases, no existing ABI to remain compatible with, and importantly there are cases where you would want to have **multiple allocator implementations** in the same program for different purposes.

With WebGPU, we have different constraints: it’s very unlikely to want multiple WebGPU implementations per program. We do need to maintain ABI compatibility. So to address this, we introduce a *comptime interface*.

![](../../assets/350aaf1944b567b9.png)

Let’s look at the `Texture.destroy`

method from earlier:

```
pub inline fn destroy(tex: Texture) void {
tex.vtable.destroy(tex.ptr);
}
```


As you can see, this would’ve called the *tex.vtable pointer*, and passed the `tex.ptr`

interface implementation pointer to it. It’s a classical runtime interface implementation. The key point here is that the data type can remain the same, while the *implementation pointer* could be replaced at runtime with a different one. On the other side of this invocation, `tex.vtable.destroy`

would look like this:

```
pub fn destroy(ptr: *anyopaque) void {
c.wgpuTextureDestroy(@ptrCast(c.WGPUTexture, ptr));
}
```


Now let’s look at how the *comptime interface* approach differs:

```
pub const Texture = opaque {
pub inline fn destroy(texture: *Texture) void {
Impl.textureDestroy(texture);
}
// ...
}
```


Firstly, we see that `*gpu.Texture`

is merely an opaque pointer (a C `void*`

if you like), just the same as before. Unlike before, however, there is no vtable pointer: there is only one pointer, it’s passed directly to the implementor via `Impl.textureDestroy`

- and the implementation *cannot be changed at runtime*.

This solves the issue of ABI compatibility (we have only one pointer now), but we still need to let the user of the library - say from their `main.zig`

file - decide which `Impl`

ementation of the interface to use.

Traditionally, one might use generics for this (passing an `Impl`

type parameter to each method for example), but we’d rather not pass that around everywhere: after all, we know it will be decided by one user of the API for the entire program, and requiring a type parameter here would have viral effects to every user of the WebGPU API (every API they expose would need that same type parameter.)

Luckily, in Zig there is a trick: from within our WebGPU API we can import the root file of the program (e.g. `main.zig`

). Zig allows this since it lazily evaluates code, so there’s no dependency loop here. So in our `mach/gpu`

package, we can define:

```
pub const Impl = blk: {
const root = @import("root");
if (!@hasDecl(root, "GPUInterface")) @compileError("expected to find `pub const GPUInterface = T;` in root file");
_ = gpu.Interface(root.GPUInterface); // verify the type
break :blk root.GPUInterface;
};
```


This effectively looks in the user’s `main.zig`

(“root”) file for a declaration like:

```
pub const GPUInterface = gpu.dawn.Interface;
```


Once resolved, our `Impl`

constant is known statically at compile time to be an exact interface implementation of the `gpu.Interface`

: `gpu.dawn.Interface`

in this case, which is just a struct type with functions in it calling the Dawn C API:

```
pub const Interface = struct {
pub inline fn textureDestroy(texture: *gpu.Texture) void {
procs.textureDestroy.?(@ptrCast(c.WGPUTexture, texture));
}
// ...
}
```


The trick here to ensuring that a type actually satisfies the `gpu.Interface`

is that you write a type validator function, which checks if the struct passes to it has the desired methods with matching function signatures:

```
/// Verifies that a gpu.Interface implementation exposes the expected function declarations.
pub fn Interface(comptime T: type) type {
assertDecl(T, "textureDestroy", fn (texture: *gpu.Texture) callconv(.Inline) void);
// ...
return T;
};
```


Best of all, since the interface implementation is completely static and known at comptime, we can enforce every method invocation is `inline`

and we’re not adding any overhead.

### libmach and gpu.Export

![](../../assets/cacbd1c79fc480f1.png)

One recent development is `libmach`

, which will provide at least a C ABI for the creation of *Mach core* applications from other languages (think a bit like SDL, but for WebGPU and it works on Desktop, Mobile, WebAssembly & more in the future.)

One thing we’d like to retain, though, is the ability to have such applications get the same nice WebGPU debugging experience in the future, while still using that language’s existing WebGPU bindings. This means instead of calling Dawn’s `wgpuTextureDestroy`

for example, we’d need to call `libmach`

’s `wgpuTextureDestroy`

.

This is where `gpu.Export`

comes in: it merely takes a `gpu.Interface`

struct with all of the Zig functions that implement the WebGPU API, and exports the WebGPU C ABI for them:

```
/// Exports C ABI function declarations for the given gpu.Interface implementation.
pub fn Export(comptime T: type) type {
_ = Interface(T); // verify implementation is a valid interface
return struct {
// WGPU_EXPORT void wgpuTextureDestroy(WGPUTexture texture);
export fn wgpuTextureDestroy(texture: *gpu.Texture) void {
T.textureDestroy(texture);
}
// ...
};
}
```


From this, you might notice something important: We’ve maintained 100% C ABI compatability in the new `mach/gpu`

rewrite. Every data structure is ABI compatible with Dawn’s `webgpu.h`

header.

### Zig flag sets

One nice property of Zig is it’s `packed struct`

s. For example, in C there is a `WGPUColorWriteMaskFlags`

type which is a `uint32_t`

where the first four bits represent a color write mask for red, green, blue, and alpha respectively. The remaining 28 bits are unused at present.

![](../../assets/9c96380a575be92f.png)

Interacting with `WGPUColorWriteMaskFlags`

in C can be a bit cumbersome: you need to make sure you remember the right bit masking operations to set bits, check if they are set, and so on.

In Zig, we have `packed struct`

in which `bool`

is just one bit - and we have integers of any bit width we desire. We can use this to compose a 32-bit data structure compatible with the C ABI variant, but using nice bools to represent those first four bits:

```
pub const ColorWriteMaskFlags = packed struct {
red: bool = false,
green: bool = false,
blue: bool = false,
alpha: bool = false,
_padding: u28 = 0,
};
```


This is nice because now one can simply check `if (write_mask.red and write_mask.blue)`

for example, or simply pass it as a parameter to a function like `ColorWriteMaskFlags{.red = true, .blue = true}`

.

Read more about how this works: [“Packed structs in Zig make bit/flag sets trivial”](https://devlog.hexops.org/2022/packed-structs-in-zig/)

### Dawn native extensions

One not-so-friendly aspect of `webgpu.h`

(the C API for WebGPU) is that it allows for arbitrary extension of the API via so-called chaining. For example, let’s look at a descriptor struct used as the parameters to create a shader module from its text source code:

```
typedef struct WGPUShaderModuleDescriptor {
WGPUChainedStruct const * nextInChain;
char const * label; // nullable
} WGPUShaderModuleDescriptor;
```


Here you can obviously see there is a `label`

for the shader module - but where does our shader source code go? It’s not clear. And what goes in that `nextInChain`

field? It looks like this:

```
typedef struct WGPUChainedStruct {
struct WGPUChainedStruct const * next;
WGPUSType sType;
} WGPUChainedStruct;
```


Effectively, WebGPU implementations can take arbitrary data structures via this chaining process - as extensions to the WebGPU API for example - so long as the chained struct *begins with these ABI-compatible fields*.

For example-to construct a shader in Zig, you might write:

```
const next_in_chain = c.WGPUShaderModuleWGSLDescriptor{
.chain = c.WGPUChainedStruct{
.next = null, // nothing else to chain
.sType = c.WGPUSType_ShaderModuleWGSLDescriptor, // so it knows what type we chained!
},
.source = my_shader_source_code_text,
};
const shader_module_descriptor = c.WGPUShaderModuleDescriptor{
.nextInChain = @ptrCast(?*const c.WGPUChainedStruct, next_in_chain),
.label = "my shader module",
};
```


That’s pretty nasty! Also take note of how `nextInChain`

needs to be *cast to* the `WGPUChainedStruct`

pointer type, only the `sType`

field identifies it (the C type system can’t.)

More importantly: because `nextInChain`

is an opaque type, you can’t really know what type of pointer is legal at all to give to the API in a `nextInChain`

field. Oof!

Needless to say, we didn’t want to adopt this lack of type safety (and lack of documentation), so we worked with the Dawn developers at Google [to add documentation about what structs are legal where](https://bugs.chromium.org/p/dawn/issues/detail?id=1486&q=reporter%3Ame&can=1), and then in Zig we used this information to replace `next_in_chain`

fields with a union of pointers so it’s type safe (for all known structs) and self-documenting. Our example from before becomes just:

```
const shader_module_descriptor = gpu.ShaderModule.Descriptor{
.next_in_chain = .{
.wgsl_descriptor = &.{.source = my_shader_source_code_text},
},
.label = "my shader module",
};
```


It may not seem much more readable, but all of the type system info is there to protect you and that’s what counts. Of course, we also added a helper to create WGSL shader modules so this ends up being truly clean:

```
device.createShaderModuleWGSL("my shader module", my_shader_source_code_text);
```


### Upstreamed patches to Dawn

Out of the box, Dawn needed a little love to be compiled with Zig as the C/C++ compiled - so we’ve contributed patches upstream for this:

- Resolving some undefined behavior in Dawn caught by Zig using UBSAN by default.
[#87380](https://dawn-review.googlesource.com/c/dawn/+/87380) - Improving constexpr compatibility for a DirectX constant, due to using MinGW DirectX headers.
[#87381](https://dawn-review.googlesource.com/c/dawn/+/87381) - Correcting an invocation of
`_uuidof`

on Windows.[#87309](https://dawn-review.googlesource.com/c/dawn/+/87309) - Adding an option to disable use of (Windows 10+) Windows UI, as we don’t have headers for it.
[#87383](https://dawn-review.googlesource.com/c/dawn/+/87383)

### Obvious improvements

There were many other [obvious improvements](https://github.com/hexops/mach/tree/main/gpu) we won’t enumerate in detail here:

- Achieving 100% API coverage, and coming up with processes/rules/conventions to ensure this all remains up-to-date and correct going forward as Dawn’s
`webgpu.h`

API changes. - Setting the right default values for every field in the entire API, which reduces verbosity of the API substantially.
- Adding slice helpers where the C ABI uses pointers-and-lengths distinctly.
- Adding type-safe helpers to callbacks which would have a
`void*`

userdata pointer in the C API. - Exposing every Dawn native extension, e.g. in anticipation of bindless support in the future.

## Standalone repository

As with all [standalone Mach libraries](https://github.com/hexops/mach/tree/main/libs) that reach a certain level of maturity, `mach/gpu`

is now available in it’s own standalone repository with an example using it with GLFW: [https://github.com/hexops/mach-gpu](https://github.com/hexops/mach-gpu)

## What’s next: browser support, more examples

I’d say we’re well on our way to having a perfect WebGPU/Dawn API for Zig, but we do have a little ways to go. Things coming up include:

- More examples
- Adding browser support: this will be achieved in the near future by direct WebAssembly->JS calls (not via Emscripten.)
- Adding higher-level helpers (always 100% optional, the C ABI is always available and present via
`gpu.Impl.foobar`

methods.)

We’re continuing to work towards [the Mach v0.2 release](https://github.com/hexops/mach/issues/355) otherwise (special thanks for all those contributing to Mach today!)

## Thanks for reading

![](../../assets/7b900b30d22ae132.png)

- Join the
[Mach Discord server](https://discord.gg/XNG3NZgCqp) - Check out the mach/gpu
[example showcase](https://machengine.org/gpu) - Help us
[port/write more WebGPU examples](https://github.com/hexops/mach/issues/230)to Zig - Read up on WebGPU
[compute](https://surma.dev/things/webgpu/)and[rendering](https://alain.xyz/blog/raw-webgpu) [Sponsor development](https://github.com/sponsors/emidoots)if you like what we're doing!