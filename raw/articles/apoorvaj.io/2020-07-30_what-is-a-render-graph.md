---
title: What is a render graph?
url: https://apoorvaj.io/render-graphs-1
published: '2020-07-30'
source_blog: apoorvaj.io
source_site: https://apoorvaj.io/
category: graphics
fetched: '2026-04-13'
---

This article is my attempt to document my experimental render graph
project, called [graphene](https://github.com/ApoorvaJ/graphene). Graphene is
still in flux, and I do not have a crystal clear roadmap ahead of me,
only loose goals. It is scary to publish something when I don’t have the
full picture yet. However, documentation is best written fresh, so I
will write what comes to mind now, and edit later if required. I might
write more articles later if I have more to talk about. Here’s what I
have so far:

You can think of the process of rendering as a bipartite graph. This
means that there are two sets of *things*, and an element of one
set can only be connected to an element of the
other. Build
systems can also be thought of as bipartite graphs, as explained in [ The
Success and Failure of Ninja](http://neugierig.org/software/blog/2020/05/ninja.html) by Evan Martin.

![](../../assets/ac683ee3638d16c8.png)


In the case of rendering, the two sets are
*resources* and
*passes*.
*Passes* represent execution of shaders, with a given pipeline
state. *Pipeline state* is things like blend modes, depth
testing, viewport, etc. Passes consume and produce *resources*,
which are buffers or images.

This is basically a render graph.

I think it’s interesting to develop an API around this abstraction.
I’m far from the first person looking at this
problem,
*FrameGraph: Extensible Rendering Architecture in Frostbite [ Video,
Slides]*
by Yuriy O’Donnell.

Now let’s have a look at some specifics:

There is a fundamental tension between graphics developers, and newer GPU APIs like Vulkan, Metal or DirectX 12:

The APIs want to front-load everything. Every aspect of pipeline state—which images to render to, which buffers to consume, whether the depth test is enabled, whether blending is enabled, which shaders to execute—all should be declared up-front. At run-time, you can avoid expensive validation checks, and dispatch to the GPU as fast as possible.

Graphics developers (although I can’t speak for everyone) want to specify logic in the render loop. That way, they can toggle effects individually for gameplay or debug visualization.

Thus, loosely speaking, APIs want to be retained mode, but graphics developers want to be immediate mode. Render graphs are a good way to resolve this tension.

There are three steps to working with a render graph:

The Unreal Engine 4 graph API looks roughly like this:

// Declaration
FRDGBuilder graph(cmd_buf);
graph.add_pass(
...
// Dispatch
[pass_0_params, shader_0](cmd_buf) {
... // Draw calls or compute dispatches
}
);
// Declaration
graph.add_pass(
...
// Dispatch
[pass_1_params, shader_1](cmd_buf) {
... // Draw calls or compute dispatches
}
);
// Invocation
graph.execute(); </div>


Here, the dispatches are lambdas. When the user calls
`graph.execute()`

, each pass begins, its lambda is called,
and then it ends.

Lambdas tend to play fast and loose with lifetimes. In C++ you basically assume that the captured state is valid and accessible in the lambda. Rust is much stricter, and this style of API gets too hairy.

Instead, I’ve found that this tends to work a lot better:

// Declaration
let pass_0 = graph.add_pass(...);
let pass_1 = graph.add_pass(...);
graph.build();
// Invocation
pass_0.begin();
// Dispatch
... // Draw calls or compute dispatches
// Invocation
pass_0.end();
pass_1.begin();
// Dispatch
... // Draw calls or compute dispatches
// Invocation
pass_1.end();


There are no lambdas here. Code runs in the same order that it’s written in, and lifetimes become very straightforward.

Let’s look at the anatomy of a frame in this API:

![](../../assets/ee143875e2986bcc.png)


`begin_frame()`

clears a command buffer and appends a
begin command to it.`graph.build()`

is called, we hash the array of
passes and check if we already have a cached graph with the same hash.
If we don’t, then we construct a new one. Graph construction is
expensive, but only happens on application init, on window resize, on
shader hot-reload, or if the rendering logic is changed.`pass.begin()`

and `pass.end()`

append render
pass instructions and pipeline state changes to the command buffer.
Pipeline barriers also may get inserted here.`end_frame()`

ends the command buffer and sends
it to the GPU to be executed.That’s basically it.

*Side-note:* I had an idea of using Rust’s async/await
features to build a render graph. Since that feature also internally
builds a directed graph, there is some semantic overlap. I asked around,
and found out that there already was a working implementation of this
idea! [ rendertoy](https://github.com/h3r2tic/rtoy-samples/blob/2a3a640a214d07c6e431e2214f0a22d51f552cdb/src/bin/stochastic-lighting/main.rs#L24)
by Tomasz Stachowiak. After going through the code, I decided
that the complexity of async/await wasn’t worth it for me, for this
project.

My API is not without its demerits, though: Each pass has to be
declared once, and then invoked once. This is a little extra
boilerplate. Probably most painfully, it *requires* that the
passes be declared and invoked in the same order, but does nothing to
enforce this at compile-time. If you have any thoughts, please get in
touch.

Going forward I want to implement the following features. I might have something to say about them later: