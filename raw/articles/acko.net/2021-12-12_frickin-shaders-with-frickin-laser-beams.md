---
title: Frickin' Shaders With Frickin' Laser Beams
url: https://acko.net/blog/frickin-shaders-with-frickin-laser-beams/
author: Steven Wittens
published: '2021-12-12'
source_blog: Hackery, Math & Design — Acko.net
source_site: https://acko.net/
category: graphics
fetched: '2026-04-19'
---

![Frickin' Shaders With Frickin' Laser Beams](../../assets/888327efaa3479f7.jpg)

# Frickin' Shaders With Frickin' Laser Beams

![Cover Image](../../assets/888327efaa3479f7.jpg)

## Hassle free GLSL

I've been working on a new [library to compose GLSL shaders](https://www.npmjs.com/package/@use-gpu/shader). This is part of a side project to come up with a [composable and incremental way](https://gitlab.com/unconed/use.gpu) of driving WebGPU and GPUs in general.

```
#pragma import { getColor } from 'path/to/color'
void main() {
gl_FragColor = getColor();
}
```


The problem seems banal: linking together code in a pretty simple language. In theory this is a textbook computer science problem: parse the code, link the symbols, synthesize new program, done. But in practice it's very different. Explaining why feels itself like an undertaking.

From the inside, GPU programming can seem perfectly sensible. But from the outside, it's impenetrable and ridiculously arcane. It's so bad I [made fun of it](https://acko.net/blog/hello-world-on-the-gpu/).

This might seem odd, given the existence of tools like ShaderToy: clearly GPUs are programmable, and there are several shader languages to choose from. Why is this not enough?

Well in fact, being able to render text on a GPU is still enough of a feat that someone has [literally made a career out of it](http://sluglibrary.com). There's a data point.

Another data point is that for almost every major engine out there, adopting it is virtually indistinguishable from forking it. That is to say, if you wish to make all but the most minor changes, you are either stuck at one version, or you have to continuously port your changes to keep up. There is very little shared cross-engine abstraction, even as the underlying native APIs remain stable over years.

When these points are raised, the usual responses are highly technical. GPUs aren't stack machines for instance, so there is no real recursion. This limits what you can do. There are also legacy reasons for certain features. Sometimes, performance and parallelism demands that some things cannot be exposed to software. But I think that's missing the forest for the trees. There's something else going on entirely. Much easier to fix.

## Just Out of Reach

Let's take a trivial shader:

```
vec4 getColor(vec2 xy) {
return vec4(xy, 0.0, 1.0);
}
void main() {
vec2 xy = gl_FragIndex * vec2(0.001, 0.001);
gl_FragColor = getColor(xy);
}
```


This produces an XY color gradient.

In shaders, the `main`

function doesn't return anything. The input and output are implicit, via global `gl_…`

registers.

Conceptually a shader is just a function that runs for every item in a list (i.e. vertex or pixel), like so:

```
// On the GPU
for (let i = 0; i < n; ++i) {
// Run shader for every (i) and store result
result[i] = shader(i);
}
```


But the `for`

loop is not in the shader, it's in the hardware, just out of reach. This shouldn't be a problem because it's such simple code: that's the entire idea of a shader, that it's a parallel `map()`

.

If you want to pass data into a shader, the specific method depends on the access pattern. If the value is constant for the entire loop, it's a *uniform*. If the value is mapped 1-to-1 to list elements, it's an *attribute*.

In GLSL:

```
// Constant
layout (set = 0, binding = 0) uniform UniformType {
vec4 color;
float size;
} UniformName;
```


```
// 1-to-1
layout(location = 0) in vec4 color;
layout(location = 1) in float size;
```


Uniforms and attributes have different syntax, and each has its own position system that requires assigning numeric indices. The syntax for attributes is also how you pass data between two connected shader stages.

But all this really comes down to is whether you're passing `color`

or `colors[i]`

to the `shader`

in the implicit `for`

loop:

```
for (let i = 0; i < n; ++i) {
// Run shader for every (i) and store result (uniforms)
result[i] = shader(i, color, size);
}
```


```
for (let i = 0; i < n; ++i) {
// Run shader for every (i) and store result (attributes)
result[i] = shader(i, colors[i], sizes[i]);
}
```


If you want the shader to be able to access all `colors`

and `sizes`

at once, then this can be done via a `buffer`

:

```
layout (std430, set = 0, binding = 0) readonly buffer ColorBufferType {
vec4 colors[];
} ColorBuffer;
layout (std430, set = 0, binding = 1) readonly buffer SizeBufferType {
vec4 sizes[];
} SizeBuffer;
```


You can only have one variable length array per buffer, so here it has to be two buffers and two bindings. Unlike the single uniform block earlier. Otherwise you have to hardcode a `MAX_NUMBER_OF_ELEMENTS`

of some kind.

Attributes and uniforms actually have subtly different type systems for the values, differing just enough to be annoying. The choice of uniform, attribute or buffer also requires 100% different code on the CPU side, both to set it all up, and to use it for a particular call. Their buffers are of a different type, you use them with a different method, and there are different constraints on size and alignment.

Only, it gets worse. Like CPU registers, bindings are a precious commodity on a GPU. But unlike CPU registers, typical tools do not help you whatsover in managing or hiding this. You will be numbering your bind groups all by yourself. Even more, if you have both a vertex and fragment shader, which is extremely normal, then you must produce a single list of bindings for both, across the two different programs.

And even then the above is all an oversimplification.

It's actually pretty crazy. If you want to make a shader of some type `(A, B, C, D) => E`

, then you need to handroll a unique, bespoke definition for each particular A, B, C and D, factoring in a neighboring function that might run. This is based mainly on the access pattern for the underlying data: constant, element-wise or random, which forcibly determines all sorts of other unrelated things.

No other programming environment I know of makes it this difficult to call a plain old function: you have to manually triage and pre-approve the arguments on both the inside and outside, ahead of time. We normally just automate this on both ends, either compile or run-time.

It helps to understand why bindings exist. The idea is that most programs will simply set up a fixed set of calls ahead of time that they need to make, sharing much of their data. If you group them by kind, that means you can execute them in batches without needing to rebind most of the arguments. This is supposed to be highly efficient.

Though in practice, shader permutations do in fact reach high counts, and the original assumption is actually pretty flawed. Even a modicum of ability to modularize the complexity would work wonders here.

The shader from before could just be written to end in a pure function which is exported:

```
// ...
#pragma export
vec4 main(vec2 xy) {
return getColor(xy * vec2(0.001, 0.001));
}
```


Using plain old functions and return values is not only simpler, but also lets you compose this module. This `main`

can be called from somewhere else. It can be used by a new function `vec2 => vec4`

that you could substitute for it.

The crucial insight is that the rigid bureaucracy of shader bindings is just a very complicated *calling convention* for a function. It overcomplicates even the most basic programs, and throws composability out with the bathwater. The fact that there is a special set of globals for input/output, with a special way to specify 1-to-1 attributes, was a design mistake in the shader language.

It's not actually necessary to group the contents of a shader with the rules about how to apply that shader. You don't want to write shader code that strictly limits how it can be called. You want anyone to be able to call it any way they might possibly like.

So let's fix it.

## Reinvent The Wheel

There is a perfectly fine solution for this already.

If you have a function, i.e. a shader, and some data, i.e. arguments, and you want to represent both together in a program... then you make a *closure*. This is just the same function with some of its variables bound to storage.

For each of the bindings above (uniform, attribute, buffer), we can define a function `getColor`

that accesses it:

```
vec4 getColor(int index) {
// uniform - constant
return UniformName.color;
}
```


```
vec4 getColor(int index) {
// attribute - 1 to 1
return color;
}
```


```
vec4 getColor(int index) {
// buffer - random access
return ColorBuffer.color[index];
}
```


Any other shader can define this as a function prototype without a body, e.g.:

```
vec4 getColor(int index);
```


You can then link both together. This is super easy when functions just have inputs and outputs. The syntax is trivial.

If it seems like I am stating the obvious here, I can tell you, I've seen a lot of shader code in the wild and virtually nobody takes this route.

The API of such a linker could be:

```
link : (module: string, links: Record<string, string>) => string
```


Given some main shader code, and some named snippets of code, link them together into new code. This generates exactly the right shader to access exactly the right data, without much fuss.

But this isn't a *closure*, because this still just makes a code string. It doesn't actually include the data itself.

To do that, we need some kind of type `T`

that represents shader modules at run-time. Then you can define a `bind`

operation that accepts and returns the module type `T`

:

```
bind : (module: T, links: Record<string, T>) => T
```


This lets you e.g. express something like:

```
let dataSource: T = makeSource(buffer);
let boundShader: T = bind(shader, {getColor: dataSource});
```


Here `buffer`

is a GPU buffer, and `dataSource`

is a *virtual* shader module, created ad-hoc and bound to that buffer. This can be made to work for any type of data source. When the bound shader is linked, it can produce the final manifest of all bindings inside, which can be used to set up and make the call.

That's a lot of handwaving, but believe me, the actual details are incredibly dull. Point is this:

**If you get this to work end-to-end, you effectively get shader closures as first-class values in your program.** You also end up with the calling convention that shaders probably should have had: the 1-to-1 and 1-to-N nature of data is expressed seamlessly through the normal types of the language you're in: is it an array or not? is it a buffer? Okay, thanks.

In practice you can also deal with array-of-struct to struct-of-arrays transformations of source data, or apply mathbox-like number emitters. Either way, somebody fills a source buffer, and tells a shader closure to read from it. That's it. That's the trick.

Shader closures can even represent things like materials too. Either as getters for properties, or as bound filters that directly work on values. It's just code + data, which can be run on a GPU.

When you combine this with a .glsl module system, and a loader that lets you [import .glsl symbols directly](https://www.npmjs.com/package/@use-gpu/glsl-loader) into your CPU code, the effect is quite magical. Suddenly the gap between CPU and GPU feels like a tiny crack instead of the canyon it actually is. The problem was always just getting at your own data, which was not actually supposed to be your job. It was supposed to tag along.

Here is for example how I actually bind position, color, size, mask and texture to a simple quad shader, to turn it into an anti-aliased SDF point renderer:

```
import { getQuadVertex } from '@use-gpu/glsl/instance/vertex/quad.glsl';
import { getMaskedFragment } from '@use-gpu/glsl/mask/masked.glsl';
const vertexBindings = makeShaderBindings(VERTEX_BINDINGS, [
props.positions ?? props.position ?? props.getPosition,
props.colors ?? props.color ?? props.getColor,
props.sizes ?? props.size ?? props.getSize,
]);
const fragmentBindings = makeShaderBindings(FRAGMENT_BINDINGS, [
(mode !== RenderPassMode.Debug) ? props.getMask : null,
props.getTexture,
]);
const getVertex = bindBundle(
getQuadVertex,
bindingsToLinks(vertexBindings)
);
const getFragment = bindBundle(
getMaskedFragment,
bindingsToLinks(fragmentBindings)
);
```


`getVertex`

and `getFragment`

are two new shader closures that I can then link to a general purpose `main()`

stub.

I do not need to care one iota about the difference between passing a buffer, a constant, or a whole 'nother chunk of shader, for any of my attributes. The props only have different names so it can typecheck. The API just composes, and will even fill in default values for nulls, just like it should.

## GP(GP(GP(GPU)))

What's neat is that you can make access patterns themselves a first-class value, which you can compose.

Consider the shader:

```
T getValue(int index);
int getIndex(int index);
T getIndexedValue(int i) {
int index = getIndex(i);
return getValue(index);
}
```


This represents using an index buffer to read from a value buffer. This is something normally done by the hardware's vertex pipeline. But you can just express it as a shader module.

When you bind it to two data sources `getValue`

and `getIndex`

, you get a closure `int => T`

that works as a new data source.

You can use similar patterns to construct virtual geometry generators, which start from one `vertexIndex`

and produce complex output. No vertex buffers needed. This also lets you do recursive tricks, like using a line shader to make a wireframe of the geometry produced by your line shader. All with vanilla GLSL.

By composing higher-order shader functions, it actually becomes trivial to emulate all sorts of native GPU behavior yourself, without much boilerplate at all. Giving shaders a dead-end main function was simply a mistake. Everything done to work around that since has made it worse. `void main()`

is just where currently one decent type system ends and an awful one begins, nothing more.

In fact, it is tempting to just put all your data into a few giant buffers, and use pointers into that. This already exists and is called "bindless rendering". But this doesn't remove all the boilerplate, it just simplifies it. Now instead of an assortment of native bindings, you mainly use them to pass around ints to buffers or images, and layer your own structs on top somehow.

This is a textbook case of the inner platform effect: when faced with an incomplete or limited API, eventually you will build a copy of it on top, which is more capable. This means the official API is so unproductive that adopting it actually has a negative effect. It would probably be a good idea to redesign it.

In my case, I want to construct and call any shader I want at run-time. Arbitrary composition is the entire point. This implies that when I want to go make a GPU call, I need to generate and link a new program, based on the specific types and access patterns of values being passed in. These may come from other shader closures, generated by remote parts of my app. I need to make sure that any subsequent draws that use that shader have the correct bindings ready to go, with all associated data loaded. Which may itself change. I would like all this to be declarative and reactive.

If you're a graphics dev, this is likely a horrible proposition. Each engine is its own unique snowflake, but they tend to have one thing in common: the only reason that the CPU side and the GPU side are in agreement is because someone explicitly spent lots of time making it so.

This is why getting past drawing a black screen is a rite of passage for GPU devs. It means you finally matched up all the places you needed to repeat yourself in your code, *and* kept it all working long enough to fix all the other bugs.

The idea of changing a bunch of those places simultaneously, especially at run-time, without missing a spot, is not enticing to most I bet. This is also why many games still require you to go back to the main screen to change certain settings. Only a clean restart is safe.

So let's work with that. If only a clean restart is safe, then the program should always behave exactly as if it had been restarted from scratch. As far as I know, nobody has been crazy enough to try and do all their graphics that way. But you can.

One way of doing that is with a [memoized effect system](https://acko.net/blog/climbing-mt-effect/). Mine is [somewhere halfway between](https://gitlab.com/unconed/use.gpu/-/blob/master/packages/app/src/app.ts#L78) discount [ZIO](https://zio.dev/) and discount [React](https://www.facebook.com/react/). The "effect" part ensures *predictable* execution, while the "memo" part ensures no *redundant* re-execution. It takes a while to figure out how to organize a basic WebGPU/Vulkan-like pipeline this way, but you basically just stare at the data dependencies for a very long time and keep untangling. It's just plain old code.

The main result is that changes are tracked only as granularly as needed. It becomes easy to ensure that even when a shader needs to be recompiled, you are still only recompiling 1 shader. You are not throwing away all other associated resources, state or caches, and the app does not need to do much work to integrate the new shader into subsequent calls immediately. That is, if you switch a binding to another of the same type, you can keep using the same shader.

The key thing is that I don't intend to make thousands of draw calls this way either. I just want to make a couple dozen of exactly the draw calls I need, preferably today, not next week. It's a radically different use case from what game engines need, which is what the current industry APIs are really mostly tailored for.

The best part is that the memoization is in no way limited to shaders. In fact, in this architecture, it always knows when it doesn't need to re-render, when nothing could have changed. Code doesn't actually run if that's the case. This is illustrated above by only having the points move around if the camera changes. For interactive graphics outside of games, this is actually a killer feature, yet it's something that's usually solved entirely ad-hoc.

One unanticipated side-effect is that when you add an inspector tool to a memoized effect system, you also get an inspector for every piece of significant state in your entire app.

On the spectrum of retained vs immediate mode, this perfectly hits that React-like sweet spot where it feels like immediate mode 90% of the time, even if it is retaining a lot behind the scenes. I highly recommend it, and it's not even finished yet.

* * *

A while ago I said something about "React VR except with Lisp instead of tears when you look inside". This is starting to feel a lot like that.

In [the code](https://gitlab.com/unconed/use.gpu/-/blob/master/packages/components/src/geometry/virtual.ts#L44), it looks absolutely nothing like any OO-style library I've seen for doing the same, which is a very good sign. It looks *sort of* similar, except it's as if you removed all code except the constructors from every class, and somehow, everything still keeps on working. It contains a fraction of the bookkeeping, and instead has a bunch of dependencies attached to hooks. There is not a single `isDirty`

flag anywhere, and it's all driven by plain old functions, either Typescript or GLSL.

The effect system allows the run-time to do all the necessary orchestration, while leaving the specifics up to "user space". This does involve version counters on the inside, but only as part of automated change detection. The difference with a dirty flag might seem like splitting hairs, but consider this: you can write a linter for a hook missing a dependency, but you can't write a linter for code missing a dirty flag somewhere. I know which one I want.

Right now this is still just a mediocre rendering demo. But from another perspective, this is a pretty insane simplification. In a handful of reactive components, you can get a proof-of-concept for something like Deck.GL or MapBox, in a fraction of the code it takes those frameworks. Without a bulky library in between that shields you from the actual goodies.