---
title: The Whats and Wherefores of Metal
url: https://metalbyexample.com/whats-and-wherefores/
published: '2014-08-28'
source_blog: Metal by Example
source_site: https://metalbyexample.com
category: graphics
fetched: '2026-04-13'
---

The previous two posts covered many of the nitty-gritty details of Metal, but I wanted to take a step back and put Metal in context. Not only are future posts going to require more work — more math, more figures, more code, deeper examples — I feel it may be necessary to explain the motivation behind this blog. This post is about what I think Metal is and can be, and why I’m so interested in helping others learn about it.


## Abstractions All the Way Down

As a creator of apps or tools, you get to pick where in the abstraction stack you insert yourself. You can use Unreal Engine 4 and get cross-platform support without ever touching code. You can write SpriteKit or SceneKit code and take advantage of a tower of abstraction that lets you talk at the level of scene graphs and materials. You can write OpenGL or OpenGL ES code that requires you to be aware of things like vertex buffers and the GLSL shader language. And, as of iOS 8, you can dispense with most of the abstraction and use Metal.

It’s important to realize that although Metal is low-level, it is still a layer of abstraction. If it were not still abstracting some of the work away from us, there would be no such thing as a command encoder; we’d just write the low-level instructions straight into a buffer and ship them over to the GPU. Similarly, there would be no library or function objects; we’d just write our shaders in machine code and upload them directly. Even then, there would be a driver down below we’d have to talk to, which is…yet another layer of abstraction.

**Metal is unique in that it is the lowest level of abstraction you can access to do graphics programming with on iOS**. That is what gives it such power, and what can make it intimidating to learn.

## Who

I mentioned app and tool developers above, but these are really two different audiences. *Most* developers will choose to use a high-level abstraction to get their work done as quickly as possible. By sacrificing some of the power of low-level frameworks, it is possible to avoid needless details. This tradeoff is perfectly reasonable in many cases.

But plenty of people will choose to use Metal, either because they create the tools and frameworks that other developers use, or because they want to take these devices to their absolute limits. Metal by Example is written for you.

## When

Metal is new, still in flux, and not supported on a lot of devices yet. It’s hard to make a case that it will replace OpenGL ES in the next generation (i.e., the iOS 8 generation) of hardware and software. Instead, as more and more devices with Metal-capable hardware are introduced and make their way into users’ hands, there will come a point where it makes sense to use Metal (or a framework that uses Metal under the hood) for a majority of development, and then exclusively.

In the more immediate future, those third-party tool and framework developers will be eager to add Metal support to their offerings, conditionally running on Metal when it is available.

Therefore, this blog is for early adopters, for now. The curious thing about technology is that it never stops moving, and what seems cutting-edge now will be ubiquitous in just a couple of years.

## Back to the Mac?

Metal is architected to work on a particular breed of hardware that has a close marriage between the CPU and the GPU. Many of its advantages disappear when the abstraction is transferred onto devices with discrete GPUs, like the Mac. That’s the bad news.

The good news is that Metal on the Mac is not an impossibility. In fact, I consider it inevitable. Apple may eventually release ARM-based Macs, which would be a natural fit for Metal, but even before that point, Metal could be implemented in terms of the architecture of current Macs (with interesting implications for performance on devices with only integrated graphics, like the MacBook Air). The real question is when Apple will allocate the resources to make this possible.

## Compute

Although the obvious application of Metal is ultra-performant graphics, it also provides a nice set of APIs for parallel, vectorized computing. This will be of interest to the scientific computing community, with particular applications in medicine and elsewhere. OpenCL has not seen particularly broad adoption, and was never made available on iOS. Metal fills that gap and should prove useful in applications requiring parallel computing.

This blog will focus heavily on graphics, but I would be remiss not to discuss the use of compute kernels to do serious number-crunching. Posts on that topic will be coming sooner rather than later.

## Onward

As always, I want to be clear that this blog is meant to serve the community. Please get in touch (via comments or email) if there are particular topics you’d like me to cover. I hope to make this site the premier source of information on Metal, and the eventual book will be powerfully shaped by the direction of the content here, so throw in your two cents.

I’d like to give a special thanks to the people who are already spreading the word about this site and showing so much support. This is already the most-noticed thing I’ve ever done online, and I hope to do justice to the attention and good faith people are placing with me.

Dr.drawMetal is the harbinger for OpenGL Next.

Metal is designed from learning from OpenCL

Metal is also saying discrete GPU is dead from this point forward.

iOS has support for OpenCL but just for CPU not GPU but the framework is still private.

Make sure you give example of when simd.h is appropriate i.e. running just for compute on the CPU or other scenario.

More visualization of intermediate step for math and such so it is easy to understand what the code is actually doing.

a lot of misconception of Metal since Apple said 10X draw calls. Most people seem to thing games will be 10X faster when that is not the case. It is not going to speed up the GPU. At most you get 40% speed up on games that are around 30 FPS. If your game is already 60 FPS, you will observe negligible speed up.

Hovhannes SafaryanHi,

First of all let me thank you for such a good materials about Metal. It’s really very helpful.

I have a question/suggestion as you told. I’m interested in how can we implement Core Graphics’s all blend modes in Metal ?

Thanks.

Warren MooreGreat question. I actually misstated in my article on blending that Metal does not allow programmable blending, but in fact it is possible to read back from the render buffer in a fragment shader by including a parameter attributed with

`[[color(0)]]`

, with which you can then perform arbitrary blend functions. Core Graphics in particular borrows most of its blend modes from the Porter-Duff model of compositing. Mark Kilgard gave a terrific overview of programmable blending in OpenGL a while ago, which should be applicable to Metal as well.