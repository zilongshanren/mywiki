---
title: Packed structs in Zig make bit/flag sets trivial
url: https://devlog.hexops.org/2022/packed-structs-in-zig/
published: '2022-08-29'
source_blog: Hexops' devlog
source_site: https://devlog.hexops.org/
category: graphics
fetched: '2026-04-19'
---

' devlog

As we’ve been building [Mach engine](https://machengine.org/), we’ve been using a neat little pattern in Zig that enables writing flag sets more nicely in Zig than in other languages.

## What is a flag set?

We’ve been rewriting `mach/gpu`

(WebGPU bindings for Zig) from scratch recently, so let’s take a flag set from the WebGPU C API:

```
typedef uint32_t WGPUFlags;
typedef WGPUFlags WGPUColorWriteMaskFlags;
```


Effectively, `WGPUColorWriteMaskFlags`

here is a 32-bit unsigned integer where you can set specific bits in it to represent whether or not to write certain colors:

```
typedef enum WGPUColorWriteMask {
WGPUColorWriteMask_None = 0x00000000,
WGPUColorWriteMask_Red = 0x00000001,
WGPUColorWriteMask_Green = 0x00000002,
WGPUColorWriteMask_Blue = 0x00000004,
WGPUColorWriteMask_Alpha = 0x00000008,
WGPUColorWriteMask_All = 0x0000000F,
WGPUColorWriteMask_Force32 = 0x7FFFFFFF
} WGPUColorWriteMask;
```


Then to use it you’d use the various bit operations with those masks, e.g.:

```
WGPUColorWriteMaskFlags mask = WGPUColorWriteMask_Red | WGPUColorWriteMask_Green;
mask |= WGPUColorWriteMask_Blue; // set blue bit
```


This all works, people have been doing it for years in C, C++, Java, Rust, and more. In Zig, we can do better.

## Zig packed structs

![](../../assets/7caa9050ff950392.png)

Zig has `packed struct`

s: these let us pack memory tightly, where a `bool`

is actually a single bit (in most other languages, this is not true.) Zig also has arbitrary bit-width integers, like `u28`

, `u1`

and so on.

We can write `WGPUColorWriteMaskFlags`

from earlier in Zig using:

```
pub const ColorWriteMaskFlags = packed struct {
red: bool = false,
green: bool = false,
blue: bool = false,
alpha: bool = false,
_padding: u28 = 0,
};
```


This is still just 32 bits of memory, and so can be passed to the same C APIs that expect a `WGPUColorWriteMaskFlags`

- but interacting with it is much nicer:

```
var mask = ColorWriteMaskFlags{.red = true, .green = true};
mask.blue = true; // set blue bit
```


In C you would need to write code like this:

```
if (mask & WGPUColorWriteMask_Alpha) {
// alpha is set..
}
if (mask & (WGPUColorWriteMask_Alpha|WGPUColorWriteMask_Blue)) {
// alpha and blue are set..
}
if ((mask & WGPUColorWriteMask_Green) == 0) {
// green not set
}
```


In Zig it’s just:

```
if (mask.alpha) {
// alpha is set..
}
if (mask.alpha and mask.blue) {
// alpha is set..
}
if (!mask.green) {
// green not set
}
```


## Comptime validation

Making sure that our `ColorWriteMaskFlags`

ends up being the same size could be a bit tricky: what if we count the number of `bool`

wrong? Or what if we accidently get the padding size wrong? Then it might not be the same size as a `uint32`

anymore.

Luckily, we can verify our expectations at comptime:

```
pub const ColorWriteMaskFlags = packed struct {
red: bool = false,
green: bool = false,
blue: bool = false,
alpha: bool = false,
_padding: u28 = 0,
comptime {
std.debug.assert(@sizeOf(@This()) == @sizeOf(u32));
std.debug.assert(@bitSizeOf(@This()) == @bitSizeOf(u32));
}
}
```


The Zig compiler will take care of running the `comptime`

code block here for us when building, and it will verify that the byte size of `@This()`

(the type we’re inside of, the `ColorWriteMaskFlags`

struct in this case) matches the `@sizeOf(u32)`

.

Similarly we could check the `@bitSizeOf`

both types if we like.

Note that [ @sizeOf](https://ziglang.org/documentation/master/#sizeOf) may include the size of padding for more complex types, while

[returns the number of bits it takes to store](https://ziglang.org/documentation/master/#bitSizeOf)

`@bitSizeOf`

`T`

in memory *if the type were a field in a packed struct/union*. For flag sets like this, it doesn’t matter and either will do. For more complex types, be sure to recall this.

## Explicit backing integers for packed structs

It’s worth noting that in Zig 0.10 (shipping in Nov), the new self-hosted compiler has support for [explicit backing integers for packed structs](https://github.com/ziglang/zig/pull/12379) which will simplify this even further.

Instead of manually adding padding to make up 32 bits, one could simply write `packed struct(u32)`

:

```
pub const ColorWriteMaskFlags = packed struct(u32) {
red: bool = false,
green: bool = false,
blue: bool = false,
alpha: bool = false,
}
```


## Thanks for reading

![](../../assets/74928628287872d1.png)

[Mach engine Discord server](https://discord.gg/XNG3NZgCqp) where we’re building the future of Zig game development.

You can also [sponsor my work](https://github.com/sponsors/emidoots) if you like what I’m doing! :)

## “But C has had bitfields since forever!”

Shortly after posting this article I was inundated with comments proclaiming “But C has had bitfields since forever!”

First, I’d like to say I was not aware of C bitfields at the time of writing - I simply had not ever come across usage of them. Secondly, I’d like to question: if C has bitfields, then why do seemingly all modern C APIs not use? Why do they all expose integer types instead?

And then I found the answer in the TC3 C specification:

![image](../../assets/d300bcb4d9b81bc5.png)

As [this user writes](https://news.ycombinator.com/item?id=32648232):

The in-memory representation of bit fields is implementation-defined. Therefore, if you’re calling into an external API that takes a uint32_t like in the example without an explicit remapping, you may or may not like the results.

In practice, everything you’re likely to come across will be little endian nowadays, and the ABI you’re using will most likely order your struct from top to bottom in memory, so they will look the same most of the time. However, it’s still technically not portable.


My intention behind this article wasn’t to say C is bad; but rather to say that I find Zig’s packed structs quite nice. I actually come from a background mostly in Go - which absolutely does not have bitfields, packed structs, or arbitrary bit-width integers. Having never come across them in C either, my claims against C bitfields today could be summarized as:

- C’s bitfields are more implementation-defined than Zig’s.
- C’s bitfields being so implementation-defined, tend not to be used in modern APIs - so the fact that Zig has come up with a variant which
*is used in practice in most APIs*is very important.

In any case, I am not an expert in C bitfields! I just hate masking to check if bits are set, and the [insane number of ways](https://news.ycombinator.com/item?id=32646998) that exact same logic can be written - both correctly and incorrectly. We deserve nicer syntax to check if a bit field is set out of the box, Zig provides that and I am happier for it.

Please stop messaging me about how C has bitfields :)