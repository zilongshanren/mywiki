---
title: The Case for Use.GPU
url: https://acko.net/blog/the-case-for-use-gpu/
author: Steven Wittens
published: '2022-06-14'
source_blog: Hackery, Math & Design — Acko.net
source_site: https://acko.net/
category: graphics
fetched: '2026-04-19'
---

![The Case for Use.GPU](../../assets/e642faf7d3c15bc7.jpg)

# The Case for Use.GPU

## Reinventing rendering one shader at a time

![Cover Image - Burrito](../../assets/e642faf7d3c15bc7.jpg)

The other day I ran into a perfect example of exactly why GPU programming is so foreign and weird. In this post I will explain why, because it's a microcosm of the issues that lead me to build Use.GPU, a WebGPU rendering meta-framework.

What's particularly fun about this post is that I'm pretty sure some seasoned GPU programmers will consider it pure heresy. Not all though. That's how I know it's good.

## A Big Blob of Code

The problem I ran into was pretty standard. I have an image at size WxH, and I need to make a stack of smaller copies, each half the size of the previous (aka MIP maps). This sort of thing is what GPUs were explicitly designed to do, so you'd think it would be straight-forward.

![Downscaling an image by a factor of 2](../../assets/9c68a9becbb29272.jpg)

If this was on a CPU, then likely you would just make a function `downScaleImageBy2`

of type `Image => Image`

. Starting from the initial `Image`

, you apply the function repeatedly, until you end up with just a 1x1 size image:

```
let makeMips = (image: Image, n: number) => {
let images: Image[] = [image];
for (let i = 1; i < n; ++i) {
image = downScaleImageBy2(image);
images.push(image);
}
return images;
}
```


On a GPU, e.g. WebGPU in TypeScript, it's a *lot* more involved. Something big and ugly like this... feel free to scroll past:

```
// Uses:
// - device: GPUDevice
// - format: GPUTextureFormat (BGRA or RGBA)
// - texture: GPUTexture (the original image + initially blank MIPs)
// A vertex and pixel shader for rendering vanilla 2D geometry with a texture
let MIP_SHADER = `
struct VertexOutput {
@builtin(position) position: vec4<f32>,
@location(0) uv: vec2<f32>,
};
@stage(vertex)
fn vertexMain(
@location(0) uv: vec2<f32>,
) -> VertexOutput {
return VertexOutput(
vec4<f32>(uv * 2.0 - 1.0, 0.5, 1.0),
uv,
);
}
@group(0) @binding(0) var mipTexture: texture_2d<f32>;
@group(0) @binding(1) var mipSampler: sampler;
@stage(fragment)
fn fragmentMain(
@location(0) uv: vec2<f32>,
) -> @location(0) vec4<f32> {
return textureSample(mipTexture, mipSampler, uv);
}
`;
// Compile the shader and set up the vertex/fragment entry points
let module = device.createShaderModule(MIP_SHADER);
let vertex = {module, entryPoint: 'vertexMain'};
let fragment = {module, entryPoint: 'fragmentMain'};
// Create a mesh with a rectangle
let mesh = makeMipMesh(size);
// Upload it to the GPU
let vertexBuffer = makeVertexBuffer(device, mesh.vertices);
// Make a texture view for each MIP level
let views = seq(mips).map((mip: number) => makeTextureView(texture, 1, mip));
// Make a texture sampler that will interpolate colors
let sampler = makeSampler(device, {
minFilter: 'linear',
magFilter: 'linear',
});
// Make a render pass descriptor for each MIP level, with the MIP as the drawing buffer
let renderPassDescriptors = seq(mips).map(i => ({
colorAttachments: [makeColorAttachment(views[i], null, [0, 0, 0, 0], 'load')],
} as GPURenderPassDescriptor));
// Set the right color format for the color attachment(s)
let colorStates = [makeColorState(format)];
// Make a rendering pipeline for drawing a strip of triangles
let pipeline = makeRenderPipeline(device, vertex, fragment, colorStates, undefined, 1, {
primitive: {
topology: "triangle-strip",
},
vertex: {buffers: mesh.attributes},
fragment: {},
});
// Make a bind group for each MIP as the texture input
let bindGroups = seq(mips).map((mip: number) => makeTextureBinding(device, pipeline, sampler, views[mip]));
// Create a command encoder
let commandEncoder = device.createCommandEncoder();
// For loop - Mip levels
for (let i = 1; i < mips; ++i) {
// Begin a new render pass
let passEncoder = commandEncoder.beginRenderPass(renderPassDescriptors[i]);
// Bind render pipeline
passEncoder.setPipeline(pipeline);
// Bind previous MIP level
passEncoder.setBindGroup(0, bindGroups[i - 1]);
// Bind geometry
passEncoder.setVertexBuffer(0, vertexBuffer);
// Actually draw 1 MIP level
passEncoder.draw(mesh.count, 1, 0, 0);
// Finish
passEncoder.end();
}
// Send to GPU
device.queue.submit([commandEncoder.finish()]);
```


The most important thing to notice is that it has a `for`

loop just like the CPU version, near the end. But before, during, and after, there is an enormous amount of set up required.

For people learning GPU programming, this by itself represents a challenge. There's not just jargon, but tons of different concepts (pipelines, buffers, textures, samplers, ...). All are required and must be hooked up correctly to do something that the GPU should treat as a walk in the park.

That's just the initial hurdle, and by far not the worst one.

![Use.GPU Plot](../../assets/2a67d4971142d93e.png)

*Use.GPU Plot aka MathBox 3*

## The Big Lie

You see, no real application would want to have the code above. Because every time this code runs, it would do all the set-up entirely from scratch. If you actually want to do this practically, you would need to rewrite it to add lots of caching. The shader stays the same every time for example, so you want to create it once and then re-use it. The shader also uses relative coordinates 0...1, so you can use the same geometry even if the image is a different size.

Other parts are less obvious. For example, the render `pipeline`

and all the associated `colorState`

depend entirely on the color format: RGBA or BGRA. If you need to handle both, you would need to cache two versions of everything. Do you need to?

The data dependencies are quite subtle. Some parts depend only on the data type (i.e. `format`

), while other parts depend on an actual data value (i.e. the contents of `texture`

)... but usually both are aspects of one and the same object, so it's very difficult to effectively separate them. Some dependencies are transitive: we have to create an array of `views`

to access the different sizes of the `texture`

(image), but then several other things depend on `views`

, such as the `colorAttachments`

(inside `pipeline`

) and the `bindGroups`

.

There is one additional catch. Everything you do with the GPU happens via a `device`

context. It's entirely possible for that context to be dropped by the browser/OS. In that case, it's your responsibility to start anew, recreating every single resource you used. This is btw the API design equivalent of a pure dick move. So whatever caching solution you come up with, it cannot be fire-and-forget: you need to invalidate and refresh too. And we all know how hard that is.

**This is what all GPU rendering code is like. You don't spend most of your time doing the work, you spend most of your time orchestrating for the work to happen.** What's amazing is that it means every GPU API guide is basically a big book of lies, because it glosses over these problems entirely. It's just assumed that you will intuit automatically how it should actually be used, even though it actually takes weeks, months, years of trying. You need to be intimately familiar with the whys in order to understand the how.

One can only conclude that the people making the APIs rarely, if ever, talk to the people using the APIs. Like backend and frontend web developers, the backend side seems blissfully unaware of just how hairy things get when you actually have to let *people* interact with your software instead of just other software. Instead, you get lots of esoteric features and flags that are never used except in the rarest of circumstances.

Few people in the scene really think any of this is a problem. This is just how it is. The art of creating a GPU renderer is to carefully and lovingly choose every aspect of your particular solution, so that you can come up with a workable answer to all of the above. What formats do you handle, and which do you not? Do all meshes have the same attributes or not? Do you try to shoehorn everything through one uber-pipeline/shader, or do you have many? If so, do you create them by hand, or do you use code generation to automate it? Also, where do you keep the caches? And who owns them?

It shouldn't be a surprise that the resulting solutions are highly bespoke. Each has its own opinionated design decisions and quirks. Adopting one means buying into all of its assumptions wholesale. You can only really swap out two renderers if they are designed to render exactly the same kind of thing. Even then, upgrading e.g. from Unreal Engine 4 to 5 is the kind of migration only a consultant can love.

This goes a very long way towards explaining the problem, but it doesn't actually explain the why.

![Use.GPU Picking](../../assets/457f0ba8be0544a4.jpg)

*Use.GPU has first class GPU picking support.*

## Memory vs Compute

There is a very different angle you can approach this from.

GPUs are, essentially, massively parallel pure function applicators. You would expect that functional programming would be a huge influence. Except it's the complete opposite: pretty much all the established practices derive from C/C++ land, where the men are men, state is mutable and the pointers are unsafe. To understand why, you need to face the thing that FP is usually pretty bad at: dealing with the performance implications of its supposedly beautiful abstractions.

Let's go back to the CPU model, where we had a function `Image => Image`

. The FP way is to compose it, threading together a chain of `Image → Image → .... → Image`

. This acts as a new function `Image => Image`

. The surrounding code does not have to care, and can't even notice the difference. Yay FP.

![Making an image gray scale, and then increasing the contrast](../../assets/ae901e59f0e8c678.jpg)

But suppose you have a function that makes an image grayscale, and another function that increases the contrast. In that case, their composition `Image => Image`

+ `Image => Image`

makes an extra intermediate image, not just the result, so it uses twice as much memory bandwidth. On a GPU, this is the main bottleneck, not computation. A fused function `Image => Image`

that does both things at the same time is typically twice as efficient.

The usual way we make code composable is to split it up and make it pass bits of data around. As this is exactly what you're not supposed to do on a GPU, it's understandable that the entire field just feels like bizarro land.

It's also trickier in practice. A grayscale or contrast adjustment is a simple 1-to-1 mapping of input pixels to output pixels, so the more you fuse operations, the better. But the memory vs compute trade-off isn't always so obvious. A classic example is a 2D blur filter, which reads NxN input pixels for every output pixel. Here, instead of applying a single 2D blur, you should do a separate 1D Nx1 horizontal blur, save the result, and then do a 1D 1xN vertical blur. This uses less bandwidth in total.

But this has huge consequences. It means that if you wish to chain e.g. Grayscale → Blur → Contrast, then it should ideally be split right in the middle of the two blur passes:

![Grayscale + Blur X → Blur Y + Contrast](../../assets/b2aa8b893c9a20ff.jpg)

*Image → (Grayscale + Horizontal Blur) → Memory → (Vertical Blur + Contrast) → ...*

In other words, you have to slice your code along invisible *internal* boundaries, not along obvious external ones. Plus, this will involve all the same bureaucratic descriptor nonsense you saw above. This means that a piece of code that normally would just call a function `Image => Image`

may end up having to orchestrate several calls instead. It must allocate a place to store all the intermediate results, and must manually wire up the relevant save-to-storage and load-from-storage glue on both sides of every gap. Exactly like the big blob of code above.

When you let C-flavored programmers loose on these constraints, it shouldn't be a surprise that they end up building massively complex, fused machines. They only pass data around when they actually have to, in highly packed and compressed form. It also shouldn't be a surprise that few people beside the original developers really understand all the details of it, or how to best make use of it.

There was and is a massive incentive for all this too, in the form of AAA gaming. Gaming companies have competed fiercely under notoriously harsh working conditions, mostly over marginal improvements in rendering quality. The progress has been steady, creeping ever closer to photorealism, but it comes at the enormous human cost of having to maintain code that pretty much becomes unmaintainable by design as soon as it hits the real world.

This is an important realization that I had a long time ago. That's because composing `Image => Image`

is basically how Winamp's AVS visualizer worked, which allowed for fully user-composed visuals. This was at a time when CPUs were highly compute-constrained. In those days, it made perfect sense to do it this way. But it was also clear to anyone who tried to port this model to GPU that it would be slow and inefficient there. Ever since then, I have been exploring how to do serious fused composition for GPU rendering, while retaining full end-user control over it.

![Use.GPU RTT](../../assets/272f3c8c0a4e14ca.jpg)

*Use.GPU Render-To-Texture, aka Milkdrop / AVS (except in Float16 Linear RGB)*

## Burrito-GPU

Functional programmers aren't dumb, so they have their own solutions for this. It's much easier to fuse things together when you don't try to do it midstream.

For example, monadic IO. In that case, you don't compose functions `Image => Image`

. Rather, you compose a list of all the operations to apply to an image, without actually doing them yet. You just gather them all up, so you can come up with an efficient execution strategy for the whole thing at the end, in one place.

This principle can be applied to shaders, which are pure functions. You know that the composition of function `A => B`

and `B => C`

is of type `A => C`

, which is all you need to know to allow for further composition: you don't need to actually compose them yet. You can also use functions as arguments to other shaders. Instead of a value `T`

, you pass a function `(...) => T`

, which a shader calls in a pre-determined place. The result is a tree of shader code, starting from some `main()`

, which can be linked into a single program.

To enable this, I defined some custom `@attributes`

in WGSL which my shader linker understands:

```
@optional @link fn getTexture(uv: vec2<f32>) -> vec4<f32> { return vec4<f32>(1.0, 1.0, 1.0, 1.0); };
@export fn getTextureFragment(color: vec4<f32>, uv: vec2<f32>) -> vec4<f32> {
return color * getTexture(uv);
}
```


The function `getTextureFragment`

will apply a texture to an existing `color`

, using `uv`

as the texture coordinates. The function `getTexture`

is virtual: it can be linked to another function, which actually fetches the texture color. But the texture could be entirely procedural, and it's also entirely optional: by default it will return a constant white color, i.e. a no-op.

It's important here that the functions act as real closures rather than just strings, with the associated data included. The goal is to not just to compose the shader code, but to compose all the orchestration code too. When I bind an actual texture to `getTexture`

, the code will contain a texture binding, like so:

```
@group(...) @binding(...) var mipTexture: texture_2d<f32>;
@group(...) @binding(...) var mipSampler: sampler;
fn getTexture(uv: vec2<f32>) -> vec4<f32> {
return textureSample(mipTexture, mipSampler, uv);
}
```


When I go to draw anything that contains this piece of shader code, the texture should travel along, so it can have its bindings auto-generated, along with any other bindings in the shader.

That way, when our blur filter from earlier is assigned an input, that just means linking it to a function `getTexture`

. That input could be a simple image, or it could be another filter being fused with. Similarly, the output of the blur filter can be piped directly to the screen, or it could be passed on to be fused with other shader code.

What's really neat is that once you have something like this, you can start taking over some of the work the GPU driver itself is doing today. Drivers already massage your shaders, because much of what used to be fixed-function hardware is now implemented on general purpose GPU cores. If you keep doing it the old way, you remain dependent on whatever a GPU maker decides should be convenient. If you have a monad-ish shader pipeline instead, you can do this yourself. You can add support for a new packed data type by polyfilling in the appropriate encoder/decoder code yourself automatically.

This is basically the story of how web developers managed to force browsers to evolve, even though they were monolithic and highly resistant to change. So I think it's a very neat trick to deploy on GPU makers.

There is of course an elephant in this particular room. If you know GPUs, the implication here is that every call you make can have its own unique shader... and that these shaders can even change arbitrarily at run-time for the same object. Compiling and linking code is not exactly fast... so how can this be made performant?

There are a few ingredients necessary to make this work.

The easy one is, as much as possible, pre-parse your shaders. I use a webpack plug-in for this, so that I can include symbols directly from `.wgsl`

in TypeScript:

```
import { getFaceVertex } from '@use-gpu/wgsl/instance/vertex/face.wgsl';
```


A less obvious one is that if you do shader composition using source code, it's actually far less work than trying to compose byte code, because it comes down to controlled string concatenation and replacement. If guided by a proper grammar and parse tree, this is entirely sound, but can be performed using a single linear scan through a highly condensed and flattened version of the syntax tree.

This also makes perfect sense to me: byte code is "back end", it's designed for optimal consumption by a run-time made by compiler engineers. Source code is "front end", it's designed to be produced and typed by humans, who argue over convenience and clarity first and foremost. It's no surprise which format is more bureaucratic and which allows for free-form composition.

The final trick I deployed is a system of structural hashing. As we saw before, sometimes code depends on a value, sometimes it only depends on a value's type. A structural hash is a hash that only considers the types, not the values. This means if you draw the same *kind* of object twice, but with different parameters, they will still have the same structural hash. So you know they can use the exact same shader and pipeline, just with different values bound to it.

In other words, structural hashing of shaders allows you to do automatically what most GPU programmers orchestrate entirely by hand, except it works for any combination of shaders produced at run-time.

The best part is that you don't need to produce the final shader in order to know its hash: you can hash along the way as you build the monadic data structure. Even before you actually start linking it, you can know if you already have the result. This also means you can gather all the produced shaders from a program by running it, and then bake them to a more optimized form for production. It's a shame WebGPU has no non-text option for loading shaders then...

## Use the GPU

If you're still following along, there is really only one unanswered question: where do you cache?

Going back to our original big blob of code, we observed that each part had unique data and type dependencies, which were difficult to reason about. Given rare enough circumstances, pretty much all of them could change in unpredictable ways. Covering all bases seems both impractical and insurmountable.

It turns out this is 100% wrong. Covering all bases in every possible way is not only practical, it's eminently doable.

Consider some code that calls some kind of constructor:

```
let foo = makeFoo(bar);
```


If you set aside all concerns and simply wish for a caching pony, then likely it sounds something like this: "When this line of code runs, and `bar`

has been used before, it should return the same `foo`

as before."

The problem with this wish is that this line of code has zero context to make such a decision. For example, if you only remember the last `bar`

, then simply calling `makeFoo(bar1)`

`makeFoo(bar2)`

will cause the cache to be trashed every time. You cannot simply pick an arbitrary N of values to keep: if you pick a large N, you hold on to lots of irrelevant data just in case, but if you pick a small N, your caches can become worse than useless.

In a traditional heap/stack based program, there simply isn't any obvious place to store such a cache, or to track how many pieces of code are using it. Values on the stack only exist as long as the function is running: as soon as it returns, the stack space is freed. Hence people come up with various `ResourceManager`

s and `HandlePool`

s instead to track that data in.

The problem is really that you have no way of identifying or distinguishing one particular `makeFoo`

call from another. The only thing that identifies it, is its place in the call stack. So really, what you are wishing for is a stack that isn't ephemeral but permanent. That if this line of code is run in the exact same *run-time context* as before, that it could somehow restore the previous state on the stack, and pick up where it left off. But this would also have to apply to the function that this line of code sits in, and the one above that, and so on.

Storing a copy of every single stack frame after a function is done seems like an insane, impractical idea, certainly for interactive programs, because the program can go on indefinitely. But there is in fact a way to make it work: you have to make sure your application has a completely finite execution trace. Even if it's interactive. That means you have to structure your application as a fully rewindable, one-way data flow. It's essentially an Immediate Mode UI, except with memoization everywhere, so it can selectively re-run only parts of itself to adapt to changes.

For this, I use two ingredients:

- React-like hooks, which gives you permanent stack frames with battle-hardened API and tooling

- a Map-Reduce system on top, which allows for data and control flow to be returned back to parents, after children are done

What hooks let you do is to turn constructors like `makeFoo`

into:

```
let foo = useFoo(bar, [...dependencies]);
```


The `use`

prefix signifies memoization in a permanent stack frame, and this is conditional on `...dependencies`

not changing (using pointer equality). So you explicitly declare the dependencies everywhere. This seems like it would be tedious, but I find actually helps you reason about your program. And given that you pretty much stop writing code that isn't a constructor, you actually have plenty of time for this.

The map-reduce system is a bit trickier to explain. One way to think of it is like an async/await:

```
async () => {
// ...
let foo = await fetch(...);
// ...
}
```


Imagine for example if `fetch()`

didn't just do an HTTP request, but actually subscribed and kept streaming in updated results. In that case, it would need to act like a promise that can resolve multiple times, without being re-fetched. The program would need to re-run the part after the `await`

, without re-running the code before it.

Neither promises nor generators can do this, so I implement it similar to how promises were first implemented, with the equivalent of a `.then(...)`

:

```
() => {
// ...
return gather(..., (foo) => {
//...
});
}
```


When you isolate the second half inside a plain old function, the run-time can call it as much as it likes, with any prior state captured as part of the normal JS closure mechanism. Obviously it would be neater if there was syntactic sugar for this, but it most certainly isn't terrible. Here, `gather`

functions like the resumable equivalent of a `Promise.all`

.

What it means is that you can actually write GPU code like the API guides pretend you can: simply by creating all the necessary resources as you need them, top to bottom, with no explicit work to juggle the caches, other than listing dependencies. Instead of bulky OO classes wrapping every single noun and verb, you write plain old functions, which mainly construct things.

In JS there is the added benefit of having a garbage collector to do the destructing, but crucially, this is not a hard requirement. React-like hooks make it easy to wrap imperative, non-reactive code, while still guaranteeing clean up is always run correctly: you can pass along the code to destroy an object or handle in the same place you construct it.

It really works. It has made me over 10x more productive in doing anything GPU-related, and I've done this in C++ and Rust before. It makes me excited to go try some new wild vertex/fragment shader combo, instead of dreading all the tedium in setting it up and not missing a spot. What's more, all the extra performance hacks and optimizations that I would have to add by hand, it can auto-insert, without me ever thinking about it. WGSL doesn't support 8-bit storage buffers and only has 32-bit? Well, my version does. I can pass a `Uint8Array`

as a `vec<u8>`

and not think about it.

The big blob of code in this post is all real, with only some details omitted for pedagogical clarity. I wrote it the other day as a test: I wanted to see if writing vanilla WebGPU was maybe still worth it for this case, instead of leveraging the compositional abstractions that I built. The answer was a resounding no: right away I ran into the problem that I had no place to cache things, and the solution would be to come up with yet another ad-hoc variant of the exact same thing the run-time already does.

Once again, I reach the same conclusion: the secret to cache invalidation is no mystery. A cache is impossible to clear correctly when a cache does not track its dependencies. When it does, it becomes trivial. And the best place to cache small things is in a permanent stack frame, associated with a particular run-time call site. You can still have bigger, more application-wide caches layered around that... but the keys you use to access global caches should generally come from local ones, which know best.

All you have to do is completely change the way you think about your code, and then you can make all the pretty pictures you want. I know it sounds facetious but it's true, and the code works. Now it's just waiting for WebGPU to become accessible without developer flags.

Veterans of GPU programming will likely scoff at a single-threaded run-time in a dynamic language, which I can somewhat understand. My excuse is very straightforward: I'm not crazy enough to try and build this multi-threaded from day 1, in a static language where every single I has to be dotted, and every T has to be crossed. Given that the run-time behaves like an async incremental data flow, there are few shady shortcuts I can take anyway... but the ability to leverage the `any`

type means I can yolo in the few places I really want to. A native version could probably improve on this, but whether you can shoehorn it into e.g. Rust's type and ownership system is another matter entirely. I leave that to other people who have the appetite for it.

The idea of a "bespoke shader for every draw call" also doesn't prevent you from aggregating them into batches. That's how Use.GPU's 2D layout system works: it takes all the emitted shapes, and groups them into unique layers, so that shapes with the same kind of properties (i.e. archetype) are all batched together into one big buffer... but only if the z-layering allows for it. Similar to the shader system itself, the UI system assumes every component *could* be a special snowflake, even if it usually isn't. The result is something that works like dear-imgui, without its obvious limitations, while still performing spectacularly frame-to-frame.

![Use.GPU Layout](../../assets/b40c001fb4a28299.png)

*Use.GPU Layout - aka HTML/CSS*

For an encore, it's not just *a* box model, but *the* box model, meaning it replicates a sizable subset of HTML/CSS with pixel-perfect precision *and* perfectly smooth scaling. It just has a far more sensible and memorable naming scheme, and it excludes a bunch of things nobody needs. Seeing as I have over 20 years of experience making web things, I dare say you can trust I have made some sensible decisions here. Certainly more sensible than W3C on a good day, amirite?

* * *

Use.GPU is not "finished" yet, because there are still a few more things I wish to make composable; this is why only the shader compiler is currently [on NPM](https://www.npmjs.com/package/@use-gpu/shader). However, given that Use.GPU is a fully "user space" framework, where all the "native" functionality sits on an equal level with custom code, this is a matter of degree. The "kernel" has been ready for half a year.

One such missing feature is derived render passes, which are needed to make order-independent transparency pleasant to use, or to enable deferred lighting. I have consistently waited to build abstractions until I have a solid set of use cases for it, and a clear idea of how to do it right. Not doing so is how we got into this mess into the first place: with ill-conceived extensions, which often needlessly complicate the base case, and which nobody has really verified if it's actually what devs need.

In this, I can throw shade at both GPU land *and* Web land. Certain Web APIs like WebAudio are laughably inadequate, never tested on anything more than toys, and seemingly developed without studying what existing precedents do. This is a pitfall I have hopefully avoided. I am well aware of how a typical 3D renderer is structured, and I am well read on the state of the art. I just think it's horribly inaccessible, needlessly obtuse, and in high need of reinventing.

**Edit**: There is now more documentation at [usegpu.live](https://usegpu.live).

The code is [on Gitlab](http://gitlab.com/unconed/use.gpu). If you want to play around with it, or just shoot holes in it, please, be my guest. It comes with a dozen or so demo examples. It also has a sweet, fully reactive inspector tool, shown in the video above at ~1:30, so you don't even need to dig into the code to watch it work.

There will of course be bugs, but at least they will be novel ones... and so far, a lot fewer than usual.