---
title: 'Stingray Renderer Walkthrough #7: Data-driven rendering'
url: https://bitsquid.blogspot.com/2017/03/stingray-renderer-walkthrough-7-data.html
author: Tobias
published: '2017-03-09'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

With all the low-level stuff in place it’s time to take a look at how we drive rendering in Stingray, i.e how a final frame comes together. I’ve covered this in various presentations over the years but will try do go through everything again to give a more complete picture of how things fit together.

Stingray features what we call a data-driven rendering pipe, basically what we mean by that is that all shaders, GPU resource creation and manipulation, as well as the entire flow of a rendered frame is defined in data. In our case the data is a set of different *json* files.

These *json*-files are hot-reloadable on all platforms, providing a nice workflow with fast iteration times when experimenting with various rendering techniques. It also makes it easy for a project to optimize the renderer for its specific needs (in terms of platforms, features, etc.) and/or to push it in other directions to better suit the art direction of the project.

There are four different types of *json*-files driving the Stingray renderer:

`.render_config`

- the heart of a rendering pipe.`.render_config_extension`

- extensions to an existing`.render_config`

file.`.shader_source`

- shader source and meta data for compiling statically declared shaders.`.shader_node`

- shader source and meta data used by the graph based shader system.

Today we will be looking at the `render_config`

, both from a user’s perspective as well as how it works on the engine side.

The `render_config`

is a [ sjson](http://bitsquid.blogspot.se/2009/10/simplified-json-notation.html) file describing everything from which render settings to expose to the user to the flow of an entire rendered frame. It can be broken down into four parts:

*render settings*,

*resource sets*,

*layer configurations*and

*resource generators*. All of which are fairly simple and minimalistic systems on the engine side.

Render settings is a simple key:value map exposed globally to the entire rendering pipe as well as an interface for the end user to peek and poke at. Here’s an example of how it might look in the `render_config`

file:

```
render_settings = {
sun_shadows = true
sun_shadow_map_size = [ 2048, 2048 ]
sun_shadow_map_filter_quality = "high"
local_lights_shadow_atlas_size = [ 2048, 2048 ]
local_lights_shadow_map_filter_quality = "high"
particles_local_lighting = true
particles_receive_shadows = true
debug_rendering = false
gbuffer_albedo_visualization = false
gbuffer_normal_visualization = false
gbuffer_roughness_visualization = false
gbuffer_specular_visualization = false
gbuffer_metallic_visualization = false
bloom_visualization = false
ssr_visualization = false
}
```


As you will see we have branching logics for most systems in the `render_config`

which allows the renderer to take different paths depending on the state of properties in the `render_settings`

. There is also a block called `render_caps`

which is very similar to the `render_settings`

block except that it is read only and contains knowledge of the capabilities of the hardware (GPU) running the engine.

On the engine side there’s not that much to cover about the `render_settings`

and `render_caps`

, keys are always strings getting murmur hashed to 32 bits and the value can be a `bool`

, `float`

, array of `floats`

or another hashed `string`

.

When booting the renderer we populate the `render_settings`

by first reading them from the `render_config`

file, then looking in the project specific `settings.ini`

file for potential overrides or additions, and last allowing to override certain properties again from the user’s configuration file (if loaded).

The `render_caps`

block usually gets populated when the `RenderDevice`

is booted and we’re in a state where we can enumerate all device capabilities. This makes the keys and values of the `render_caps`

block somewhat of a black box with different contents depending on platform, typically they aren’t that many though.

So that covers the `render_settings`

and `render_caps`

blocks, we will look at how they are actually used for branching in later sections of this post.

There are also a few other miscellaneous blocks in the `render_config`

, most important being:

`shader_pass_flags`

- Array of strings building up a bit flag that can be used to dynamically turn on/off various shader passes.`shader_libraries`

- Array of what`shader_source`

files to load when booting the renderer. The`shader_source`

files are libraries with pre-compiled shader libraries mainly used by the resource generators.

We have the concept of a `RenderResourceSet`

on the engine side, it simply maps a hashed string to a GPU resource. `RenderResourceSets`

can be locally allocated during rendering, creating a form of scoping mechanism. The resources are either allocated by the engine and inserted into a `RenderResourceSet`

or allocated through the `global_resources`

block in a `render_config`

file.

The [ RenderInterface](http://bitsquid.blogspot.se/2017/02/stingray-renderer-walkthrough-6.html) owns a global

`RenderResourceSet`

populated by the `global_resources`

array from the `render_config`

used to boot the renderer.Here’s an example of a `global_resources`

array:

```
global_resources = [
{ type="static_branch" platforms=["ios", "android", "web", "linux"]
pass = [
{ name="output_target" type="render_target" depends_on="back_buffer"
format="R8G8B8A8" }
]
fail = [
{ name="output_target" type="alias" aliased_resource="back_buffer" }
]
}
{ name="depth_stencil_buffer" type="render_target" depends_on="output_target"
w_scale=1 h_scale=1 format="DEPTH_STENCIL" }
{ name="gbuffer0" type="render_target" depends_on="output_target"
w_scale=1 h_scale=1 format="R8G8B8A8" }
{ name="gbuffer1" type="render_target" depends_on="output_target"
w_scale=1 h_scale=1 format="R8G8B8A8" }
{ name="gbuffer2" type="render_target" depends_on="output_target"
w_scale=1 h_scale=1 format="R16G16B16A16F" }
{ type="static_branch" render_settings={ sun_shadows = true }
pass = [
{ name="sun_shadow_map" type="render_target" size_from_render_setting="sun_shadow_map_size"
format="DEPTH_STENCIL" }
]
}
{ name="hdr0" type="render_target" depends_on="output_target" w_scale=1 h_scale=1
format="R16G16B16A16F" }
]
```


So while the above example mainly shows how to create what we call `DependentRenderTargets`

(i.e render targets that inherit its properties from another render target and then allow overriding properties locally), it can also create other buffers of various kinds.

We’ve also introduced the concept of a `static_branch`

, there are two types of branching in the `render_config`

file: `static_branch`

and `dynamic_branch`

. In the `global_resource`

block only static branching is allowed as it only runs once, during set up of the renderer. (*Note:* The branch syntax is far from nice and we nowadays have come up with a much cleaner syntax that we use in the shader system, unfortunately it hasn’t made its way back to the `render_config`

yet.)

So basically what this example boils down to is the creation of a set of render targets. The `output_target`

is a bit special though, on PC and consoles we simply just setup an alias for an already created render target - the back buffer, while on gl based platforms we create a new separate render target. (This is because we render the scene up-side-down on gl-platforms to get consistent UV coordinate systems between all platforms.)

The other special case from the example above is the `sun_shadow_map`

which grabs the resolution from a `render_setting`

called `sun_shadow_map_size`

. This is done because we want to expose the ability to tweak the shadow map resolution to the user.

When rendering a frame we typically pipe the global `RenderResourceSet`

owned by the `RenderInterface`

down to the various rendering systems. Any resource declared in the `RenderResourceSet`

is accessible from the shader system by name. Each rendering system can at any point decide to create its own local version of a `RenderResourceSet`

making it possible to scope shader resource access.

Worth pointing out is that the resources declared in the `global_resource`

block of the `render_config`

used when booting the engine are all allocated in the set up phase of the renderer and not released until the renderer is closed.

A `render_config`

can have multiple `layer_configurations`

. A Layer Configuration is essentially a description of the flow of a rendered frame, it is responsible for triggering rendering sub-systems and scheduling the GPU work for a frame. Here’s a simple example of a deferred rendering pipe:

```
layer_configs = {
simple_deferred = [
{ name="gbuffer" render_targets=["gbuffer0", "gbuffer1", "gbuffer2"]
depth_stencil_target="depth_stencil_buffer" sort="FRONT_BACK" profiling_scope="gbuffer" }
{ resource_generator="lighting" profiling_scope="lighting" }
{ name="emissive" render_targets=["hdr0"]
depth_stencil_target="depth_stencil_buffer" sort="FRONT_BACK" profiling_scope="emissive" }
{ name="skydome" render_targets=["hdr0"]
depth_stencil_target="depth_stencil_buffer" sort="BACK_FRONT" profiling_scope="skydome" }
{ name="hdr_transparent" render_targets=["hdr0"]
depth_stencil_target="depth_stencil_buffer" sort="BACK_FRONT" profiling_scope="hdr_transparent" }
{ resource_generator="post_processing" profiling_scope="post_processing" }
{ name="ldr_transparent" render_targets=["output_target"]
depth_stencil_target="depth_stencil_buffer" sort="BACK_FRONT" profiling_scope="transparent" }
]
}
```


Each line in the `simple_deferred`

array specifies either a named *layer* that the shader system can reference to direct rendering into (i.e a renderable object, like e.g. a mesh, has shaders assigned and the shaders know into which *layer* they want to render - e.g `gbuffer`

), or it can trigger a `resource_generator`

.

The order of execution is top->down and the way the GPU scheduling works is that each line increments a bit in the “Layer System” bit range covered in the post about [sorting](http://bitsquid.blogspot.se/2017/02/stingray-renderer-walkthrough-4-sorting.html).

On the engine side the layer configurations are managed by a system called the `LayerManager`

, owned by the [ RenderInterface](http://bitsquid.blogspot.se/2017/02/stingray-renderer-walkthrough-6.html). It is a tiny system that basically just maps the named

`layer_config`

to an array of “Layers”:```
struct Layer {
uint64_t sort_key;
IdString32 name;
render_sorting::DepthSort depth_sort;
IdString32 render_targets[MAX_RENDER_TARGETS];
IdString32 depth_stencil_target;
IdString32 resource_generator;
uint32_t clear_flags;
#if defined(DEVELOPMENT)
const char *profiling_scope;
#endif
};
```


`sort_key`

- As mentioned above and in the post about how we do[sorting](http://bitsquid.blogspot.se/2017/02/stingray-renderer-walkthrough-4-sorting.html), each layer gets a`sort_key`

assigned from the “Layer System” bit range. By looking up the layer’s`sort_key`

and using that when recording`Commands`

to`RenderContexts`

we get a simple way to reason about overall ordering of a rendered frame.`name`

- the shader system can use this name to look up the layer’s`sort_key`

to group draw calls into layers.`depth_sort`

- describes how to encode the depth range bits of the sort key when recording a`RenderJobPackage`

to a`RenderContext`

.`depth_sort`

is an enum that indicates if sorting should be done front-to-back or back-to-front.`render_targets`

- array of named render target resources to bind for this layer`depth_stencil_target`

- named render target resource to bind for this layer`resource_generator`

-`clear_flags`

- bit flag hinting if color, depth or stencil should be cleared for this layer`profiling_scope`

- used to record markers on the`RenderContext`

that later can be queried for GPU timings and statistics.

When rendering a `World`

(see: [RenderInterface](http://bitsquid.blogspot.se/2017/02/stingray-renderer-walkthrough-6.html)) the user passes a viewport to the `render_world`

function, the viewport knows which `layer_config`

to use. We look up the array of `Layers`

from the `LayerManager`

and record a [ RenderContext](http://bitsquid.blogspot.se/2017/02/stingray-renderer-walkthrough-3-render.html) with state commands for binding and clearing render targets using the

`sort_keys`

from the `Layer`

. We do this dynamically each time the user calls `render_world`

but in theory we could cache the `RenderContext`

between `render_world`

calls.The name `Layer`

is a bit misleading as a layer also can be responsible for making sure that a `ResourceGenerator`

runs, in practice a `Layer`

is either a target for the shader system to render into or it is the execution point for a `ResourceGenerator`

. It can in theory be both but we never use it that way.

The Resource Generators is a minimalistic framework for manipulating GPU resources and triggering various rendering sub-systems. Similar to a layer configuration a resource generator is described as an array of “modifiers”. Modifiers get executed in the order they were declared. Here’s an example:

```
auto_exposure = {
modifiers = [
{ type="dynamic_branch" render_settings={ auto_exposure_enabled=true } profiling_scope="auto_exposure"
pass = [
{ type="fullscreen_pass" shader="quantize_luma" inputs=["hdr0"]
outputs=["quantized_luma"] profiling_scope="quantize_luma" }
{ type="compute_kernel" shader="compute_histogram" thread_count=[40 1 1] inputs=["quantized_luma"]
uavs=["histogram"] profiling_scope="compute_histogram" }
{ type="compute_kernel" shader="adapt_exposure" thread_count=[1 1 1] inputs=["quantized_luma"]
uavs=["current_exposure" "current_exposure_pos" "target_exposure_pos"] profiling_scope="adapt_exposure" }
]
}
]
}
```


First modifier in the above example is a `dynamic_branch`

. In contrast to a `static_branch`

which gets evaluated during loading of the render_config, a `dynamic_branch`

is evaluated each time the resource generator runs making it possible to take different paths through the rendering pipeline based on settings and other game context that might change over time. Dynamic branching is also supported in the `layer_config`

block.

If the branch is taken (i.e if `auto_exposure_enabled`

is true) the modifiers in the `pass`

array will run.

The first modifier is of the type `fullscreen_pass`

and is by far the most commonly used modifier type. It simply renders a single triangle covering the entire viewport using the named `shader`

. Any resource listed in the `inputs`

array is exposed to the shader. Any resource(s) listed in the `outputs`

array are bound as a render target(s).

The second and third modifiers are of the type `compute_kernel`

and will dispatch a compute shader. `inputs`

array is the same as for the `fullscreen_pass`

and `uavs`

lists resources to bind as UAVs.

This is obviously a very basic example, but the idea is the same for more complex resource generators. By chaining a bunch of modifiers together you can create interesting rendering effects entirely in data.

Stingray ships with a toolbox of various modifiers, and the user can also extend it with their own modifiers if needed. Here’s a list of some of the other modifiers we ship with:

`cascaded_shadow_mapping`

- Renders a cascaded shadow map from a directional light.`atlased_shadow_mapping`

- Renders a shadow map atlas from a set of spot and omni lights.`generate_mips`

- Renders a mip chain for a resource by interleaving a resource generator that samples from sub-resource*n-1*while rendering into sub-resource*n*.`clustered_shading`

- Assign a set of light sources to a clustered shading structure (on CPU at the moment).`deferred_shading`

- Renders proxy volumes for a set of light sources with specified shaders (i.e. traditional deferred shading).`stream_capture`

- Reads back the specified resource to CPU (usually multi-buffered to avoid stalls).`fence`

- Synchronization of graphics and compute queues.`copy_resource`

- Copies a resource from one GPU to another.

In Stingray we encourage building all lighting and post processing using resource generators. So far it has proved very successful for us as it gives great per project flexibility. To make sharing of various rendering effects easier we also have a system called [ render_config_extension](http://bitsquid.blogspot.se/2016/08/render-config-extensions.html) that we rolled out last year, which is essentially a plugin system to the

`render_config`

files.I won’t go into much detail how the resource generator system works on the engine side, it’s fairly simple though; There’s a `ResourceGeneratorManager`

that knows about all the generators, each time the user calls `render_world`

we ask the manager to execute all generators referenced in the `layer_config`

using the layers sort key. We don’t restrain modifiers in any way, they can be implemented to do whatever and have full access to the engine. E.g they are free to create their own `ResourceContexts`

, spawn worker threads, etc. When the modifiers for all generators are done executing we are handed all `RenderContexts`

they’ve created and can dispatch them together with the contexts from the regular scene rendering. To get scheduling between modifiers in a resource generators correct we use the 32-bit “user defined” range in the [sort key](http://bitsquid.blogspot.se/2017/02/stingray-renderer-walkthrough-4-sorting.html).

Before we wrap up I’d like to cover some ideas for future improvements.

The Stingray engine has had a data-driven renderer from day one, so it has been around for quite some time by now. And while the `render_config`

has served us good so far there are a few things that we’ve discovered that could use some attention moving forward.

The complexity of the default rendering pipe continues to increase as the demand for new rendering features targeting different industries (games, design visualization, film, etc.) increases. While the data-driven approach we have addresses the feature set scalability needs decently well, there is also an increasing demand to have feature parity across lots of different hardware. This tends to result in lots of branching in `render_config`

making it a bit hard to follow.

In addition to that we also start seeing the need for managing multiple paths through the rendering pipe on the same platform, this is especially true when dealing with stereo rendering. On PC we currently we have 5 different paths through the default rendering pipe:

- Mono - Traditional mono rendering.
- Stereo - Old school stereo rendering, one
`render_world`

call per eye. Almost identical to the mono path but still there are some stereo specific work for assembling the final image that needs to happen. - Instanced Stereo - Using “hardware instancing” to do stereo propagation to left/right eye. Single scene traversal pass, culling using a uber-frustum. A bunch of shader patch up work and some branching in the
`render_config`

. - Nvidia Single Pass Stereo (SPS) - Somewhat similar to instanced stereo but using nvidia specific hardware for doing multicasting to left/right eye.
- Nvidia VRSLI - DX11 path for rendering left/right eye on separate GPUs.

We estimate that the number of paths through the rendering pipe will continue to increase also for mono rendering, we’ve already seen that when we’ve experimented with explicit multi-GPU stuff under DX12. Things quickly becomes hairy when you aren’t running on a known platform. Also, depending on hardware it’s likely that you want to do different scheduling of the rendered frame - i.e its not as simple as saying: here are our 4 different paths we select from based on if the user has 1-4 GPUs in their systems, as that breaks down as soon as you don’t have the exact same GPUs in the system.

In the future I think we might want to move to an even higher level of abstraction of the rendering pipe that makes it easier to reason about different paths through it. Something that decouples the strict flow through the rendering pipe and instead only reasons about various “jobs” that needs to be executed by the GPUs and what their dependencies are. The engine could then dynamically re-schedule the frame load depending on hardware automatically… at least in theory, in practice I think it’s more likely that we would end up with a few different “frame scheduling configurations” and then select one of them based on benchmarking / hardware setup.

As mentioned earlier our system for dealing with GPU resources is very static, resources declared in the `global_resource`

set are allocated as the renderer boots up and not released until the renderer is closed. On last gen consoles we had support for aliasing memory of resources of different types but we removed that when deprecating those platforms. With the rise of DX12/Vulkan and the move to 4K rendering this static resource system is in need of an overhaul. While we can (and do) try to recycle temporary render targets and buffers throughout the a frame it is easy to break some code path without noticing.

We’ve been toying with similar ideas to the “Transient Resource System” described in Yuriy O’Donnell’s excellent GDC2017 presentation: [FrameGraph: Extensible Rendering Architecture in Frostbite](http://www.frostbite.com/2017/03/framegraph-extensible-rendering-architecture-in-frostbite/) but have so far not got around to test it out in practice.

Today our system implicitly deals with binding of input resources to shader stages. We expose pretty much everything to the shader system by name and if a shader stage binds a resource for reading we don’t know about it until we create the [ RenderJobPackage](http://bitsquid.blogspot.se/2017/02/stingray-renderer-walkthrough-3-render.html). This puts us in a somewhat bad situation when it comes to dealing with resource transitions as we end up having to do some rather complicated tracking to inject resource barriers at the right places during the

*dispatch*stage of the

`RenderContexts`

(See: [).](http://bitsquid.blogspot.se/2017/02/stingray-renderer-walkthrough-5.html)

`RenderDevice`

We could instead enforce declaration of all writable GPU resources when they get bound as input to a layer or resource generator. As we already have explicit knowledge of when a GPU resource gets written to by a layer or resource generator, adding the explicit knowledge of when we read from one would complete the circle and we would have all the needed information to setup barriers without complicated tracking.

Last week at GDC 2017 there were a few presentations (and a lot of discussions) around the concepts of having more high-level representations of a rendered frame and what benefits that brings. If you haven’t already I highly encourage you to check out both Yuriy O’Donnell’s presentation [“FrameGraph: Extensible Rendering Architecture in Frostbite”](http://www.frostbite.com/2017/03/framegraph-extensible-rendering-architecture-in-frostbite/) and Aras Pranckevičius’s presentation: [“Scriptable Render Pipeline”](http://aras-p.info/texts/files/2017_GDC_UnityScriptableRenderPipeline.pdf).

In the next post I will briefly cover the feature set of the two `render_configs`

that we ship as template rendering pipes with Stingray.

Thanks a lot for sharing Tobias. When you define a pass that use compute_histogram in Modifiers, is that pass totally data driven? Meaning do you have to write cpp code to set various shader parameters for compute_histogram shader?

ReplyDelete:office.com/setup.com is a self-decision supplier of remote specific help relationship for programming, mechanical get together, and peripherals. We are amazing since we have



ReplyDeleteconfine in things from a wide gathering of outcast affiliations.office.com/setup

On the off chance that you have shown www.norton.com/setup from This security approach has been amassed to all the more likely serve the far reaching pack who are




ReplyDeletestressed over how their 'To a dazzling degree Identifiable Information' (PII) is being used on the web. PII, as tended to in US ask for law and information security, is information that

can be used with no other individual or with other information to see, contact, or locate a specific individual, or to see a man in setting. www.norton.com/setup

This comment has been removed by the author.

ReplyDeleteDownload and install your Norton product. Sign In to Norton. If you do not have a Norton account, click Create account and complete the sign up process. In the Norton Setup window, click Enter a New Product Key. To enroll in Automatic Renewal Service for your Norton subscription, Get Started



ReplyDeletenorton.com/setup

I think this is a useful post and it is exceptionally valuable and learned. along these lines, I might want to thank you for the endeavors you have made recorded as a hard copy this article. In the event that you are searching for antivirus security for your PC and some other advanced gadgets than. Visit@:



ReplyDeleteofficesetupusa.com

office.com/setup

Get started office Setup with Product Key at norton.com/setup



ReplyDelete. Sign in, Enter Product Key and install Office or call us toll-free +1-877-301-0214 Visit Famous Blog norton.com/setup
















ReplyDeleteIn love with this post.thankyou for the information.

Please do find the attached files and download it form our website.

http://www.salaelcachorro.com/get-the-advantages-of-the-greatest-android-functions/

http://www.annonces-rapides.com/android-telephone-software-rising-cellular-working-system/

http://www.marek-knows.com/watch-tv-on-5-inch-i9220-android-four-zero-three-smartphone/

http://www.michaelkors-uk.com/why-are-android-video-games-so-standard-at-present/

http://www.katespade-uk.com/evaluating-the-widows-cell-and-android-develpment-platform/

Loved the article and the others that were mentioned. Thought I would ask you guys to read mine about Mother’s Day. Thanks!

ReplyDeleteMothers Day Images!

Free Mothers Day Images!

refreshing post!!

ReplyDeletewww.office.com/setup

On the off chance that that doesn't fix the issue, attempt these means and endeavor to sign in after every one:


ReplyDeleteClear your program's treats.

Stop and after that restart your program.

Utilize an alternate bolstered internet browser.

Take a stab at signing into an alternate sign-in page, similar to our essential login page or the Yahoo Mail sign-in page.

Visit for more:- yahoo mail sign in problems

Avast internet security phone number


ReplyDeleteMalwarebytes contact number

Outlook Customer Care Phone Number

Yahoo Mail Contact Numberr

Awesome post, I like it very much


ReplyDeleteThanks

bagtheweb | symbaloo | start | wibki

The post is going to help a lot if it will be read carefully, if in case you are unable to fix your brother printer on your own then visit




ReplyDeleteBrother Printer Support Number - 24*7Brother Suppot UK | Toll-free NumberDial Brother printer Toll free Number to reach to our technicians and our experts will assist you about how to set up and install compatible printer drivers. The support center is available 24X7 to provide you best services.

ReplyDeleteBrother printer support | Brother printer support number

find

ReplyDeletego to the website

try this site

look at more info

look what i found

Full Report

websites

Extra resources

get more

If you still have issue while depositing or withdrawing cryptocurrency from Bittrex, even if you fail to create or login to your Bittrex account, just feel free to get in touch with Bittrex Customer Support services for technical assistance with issues related to Bittrex wallet.







ReplyDeletebittrex support numberbittrex support phone number

bittrex support

You can contact Bittrex tech support representatives via phone call or live chat. They are available 24*7 for the convenience of users.

bittrex exchangebittrex customer service

bittrex phone number

wow very nice .

ReplyDeleteDo you want support for bullguard.

Login your account here :- BullGuard Sign In

Thanks you sharing information.






ReplyDeleteTrend Micro not working: If Trend Micro is not working on your system then it might be possible that the software is not installed completely. In that case, uninstall the Trend Micro and then install it again. If it still not working then, make sure that your device does not have existing software. If available then get it uninstalled.

Trend Micro LoginTrend Micro Support Number UKCall at:

Trend Micro helpline Number UKIf you are facing any issues regarding Norton, webroot, Bitdefender, Garmin, Rand McNally dock and Magellan GPS update you will get an instant online solution. For more details visit this link which is given below:


ReplyDeletenorton.com/setup

Bitdefender Central

garmin.com/express

webroot.com/safe

rand mcnally dock

Magellan GPS Update

Online therapy

Applicable to ransomware file recovery , useful content.

ReplyDeleteIf you are looking for good work then we provide the best high-quality essay and other assignments to help online services. Assignment Help Online

ReplyDeleteI am just around The Garden Residences. I discovered The Florence Residences and I in discovering It really supportive and Parc Clematis helped me out a great deal.

ReplyDeleteI would like to introduce stirling residences and help other people, for example, you helped parc esta.

ReplyDeleteThankful to you for such a basic blog. I truly perceive for treasure at tampines data related substance. Much refreshing of for The Hyde.

ReplyDeleteAppreciative to you for View At Kismis site. The spot else may just I get that kind of RV Altitude information written in such a perfect structure at The Avenir showflat.

ReplyDeleteWe are at top to deliver rigorous ,plagiarism free translation.If you are going to choose translation help in Singapore then you must engage your work with us. We deliver you ISO certified translation as your requirements.For more information kindly click the following link

ReplyDeleteTranslation Services SingaporeSingaporeassignmenthelp.com provides cheap essay writing service for students. Our Expert writers write error free work for MBA students in various disciplines to students located outside of Singapore.

ReplyDeleteVery awesome!!! When I seek for this I found this website at the top of all blogs in search engine.Very awesome!!! When I seek for this I found this website at the top of all blogs in search engine. do my assignment for me ireland

ReplyDeletepost.For more information, and click on https://mymcafeecomactivate.com/.


ReplyDeleteNice post! This blog gives the easy tips to install McAFee antivirus program using mcafee.com/activate. This blog provides easy steps to install this security product easily. Thanks for sharing this valuable post.

www.mcafee.com/activate

More than 200 British assignment writers and 24/7 customer support make us #1 assignment writing service in the market. Up to 30% off online assignment full dissertation help. You can find also find many courses here java programming helper.


ReplyDeleteThanks for discuss introduction of Stingray Renderer Walkthrough.I read your excellent post. After reading this post, i really appreciate your effort and my request is to please share us more post in future. Keep it up.The Web Design Dubai Company provides good service of design.


ReplyDelete



ReplyDeleteExcellently written article, if only all bloggers offered the same level of content as you, the internet would be a much better place. Really great post, Thank you for sharing this knowledge.Get best Commercial Cleaning Company Dubai from www.yallacleaning.com

great website! Kopar


ReplyDeletePlayBox HD(Putlocker)






ReplyDeletePlayBox HD is another alternative that works on both iPhones and Androids. It works just like Showbox and has a lot of HD content. PlayBox HD has a simple and clean user interface design and it streams quickly and without buffer over a good WiFi connection.

Crackle

Crackle is a little different from most of the sites and apps here; It is owned by Sony and only features licensed content, so you don't have to worry about a VPN. Everything in Crackle is good quality video and the app allows you to do things like save your favorites and create playlists. Crackle has a clean and simple user interface and can search and rate the shows and movies you want to watch.

This comment has been removed by the author.

ReplyDelete



ReplyDeleteThis is a great blog posting and very useful.SEO Expert Dubai

www.norton.com/setup: Norton setup provides this another option for downloading the complete download setup. Most of the steps are same but with some modifications in the downloading procedures, one can download the setup on another device via norton.com/setup.


ReplyDeleteIncluding various techniques of gambling, both disadvantages and disadvantages. Various techniques that the gambler should know sedgefieldharriers

ReplyDeletemcafee.com/activate - Redeem McAfee for downloading & installing the software and activating its subscription. Visit www.mcafee.com/activate or mcafee activate for more.

ReplyDeletewww.roku.com/link provides the simplest way to stream entertainment to your TV. On your terms. With thousands of available channels to choose from.


ReplyDeleteGlobal Translation Help is leading translation company which offer high quality translation of legal documents at very reasonable price.If you want to get the translation help from us then kindly mail info@globaltranslationhelp.com. Our experts deliver you well precise,an effective legal document translation at very reasonable price.

ReplyDelete

ReplyDeleteroku my account: Sign in to your roku account. A Roku account gives you access to an amazing selection of movies, TV shows, music and more from the Roku Channel Store.

roku.com/link: Watch the latest movies and Tv shows by HBO Max channels with uninterrupted services. Get entertainment by HBO Max on roku with best-in-quality services.

ReplyDelete

ReplyDeleteOfficial Epson printer support and customer service is always free. Download drivers, access FAQs, manuals, warranty, videos, product registration and more.

Mcafee Activate : Reach mcafee.com/activate, Enter 25 digit mcafee product key code, sign in or create mcafee account then download, install and activate it.


ReplyDeleteSwitch on the HP printer and computer · Open web browser and type 123 com setup · Enter HP Printer model number in the space provided.

ReplyDeleteHighly Enlightening Aspects Regarding id verification service


ReplyDeleteRight now id verification service is really popular among persons. There are lots of id verification methods that one can attain on a trusted site known as Trust Swiftly, and a firm can implement the methods to protect their own web business conveniently. In the event you go to this particular TrustSwiftly website, you'll get increasingly more specifics about id verification service.

are you getting problem with microsoft edge then you can uninstall microsoft edge on mac and resinstall it.


ReplyDeleteIs your Malwarebytes giving you sleepless nights these days? Do you find Malwarebytes unable to start with the start of the system? For these and similar other problems, simply dial 1-877-916-7666 and talk to our highly qualified engineer.

ReplyDeleteThrough www.amazon.com/mytv - how you can connect your mobile phone to Amazon Prime. Through amazon.com/mytv, you can watch your favorite TV shows, series movies. You can watch prime videos anywhere on your device. Users need to create an Amazon account if they don’t have an Amazon account and enter the Amazon my TV activation code to watch Amazon prime videos on your device.

ReplyDeleteamazn.com/mytv

www.amazn.com/mytv

Amazon myTV







ReplyDeleteOn the off chance that you're seeing Amazon Prime on your TV, you essentially need to open the application and get your extraordinary

Activate Amazon.com/mytv . It will be given to you when you endeavor to activate an alternate device for review. For instance, getting a Prime Trial notwithstanding contraption Activation code.

Roku.com/link is the page to initiate your streaming device. Allow us to begin the Roku Activation process. From your wireless, open the web browser and paste the URL, Roku.com/link. A brief to give the Roku.com/link enter code will appear on the screen. Enter the Roku Activation code in the code space to finish the Roku device Activation. When activated, clients can add channels to their Roku accounts on their particular devices. Again, if a client finds them signed out of the device, they can utilize URL.roku.com sign in. To sign once again into their accounts.


ReplyDeleteRoku.com/link

Roku Activation code

Hulu is a premium online streaming platform offering some great shows and movies. It comes with a subscription plan, which you can change as per your need.If you need to activate the Hulu, surf to the hulu.com/activate and enter the Hulu activation code Before activating, you need to enter the Hulu account credentials. If you don’t have the existing account, here we are to help you with the Hulu account activation steps




ReplyDeletehulu.com/activate

Hulu activation code

If you are facing any sort of problem with the Epson printer error of your Epson printer, then, you may feel like getting it checked from the Epson experts. But before you call them, you can also try sorting out the problem on your own.


ReplyDeleteepson error code 0xea

Wow! This blog looks exactly like my old one! It’s on a completely different topic but it has pretty much the same page layout and design. Excellent choice of colors!

ReplyDeleteMachine error af





ReplyDeletehulu.com/activate Hulu is a premium online streaming platform offering some great shows and movies. It comes with a subscription plan, which you can change as per your need. You can sign-up and binge watch series without any ads. There are thousands of shows and movies in the streaming library. Further, once the Hulu activate process is completed, you can access to even more content by subscribing to premium networks. If you need to activate the Hulu, surf to the hulu.com/activate and enter the Hulu activation code

hulu.com/activate

Hulu activation code

Nice Blog. Thanks for sharing with us. Such amazing information.







ReplyDeleteHOW TO EARN MONEY BY PURCHASING YOUTUBE SUBSCRIBERS

MyBlogger Club

Guest Posting Site

Best Guest Blogging Site

Guest Blogger

Guest Blogging Site

Dial 1-844-249-4536 which is our popular and trusted Malwarebytes support number. Explain your problem to our engineer and get quick and authentic resolution from him.

ReplyDeletegarmin.com/express



ReplyDeleteSo, if you are also interested in using Prime membership benefits, then you can use this article from the beginning till the end. Once you purchase your subscription, you can use a wide of range features until your subscription expires. The membership benefits also include free delivery of eligible products as well as other exclusive offers. Simply, visit amazon.com/mytv and www.amazon.com/mytv




ReplyDeleteAmazon provides one of the ideal quality of all videos. Additionally, it provides one of the greatest sound quality which other devices do not provide. It is also possible to delight in the stations that you would like to see.

ReplyDeleteamazon.co.uk/mytv

amazon.co.uk/mytv

amazon.co.uk/mytv

amazon.co.uk/mytv sign in

Hello! This is my first visit to your website! Your website provided us useful information to work on. Would like to visit this website again and again.


ReplyDeletetop digital marketing agencies in india

seo india

mobile app developers

google 894

ReplyDeletegoogle 895

google 896

google 897

google 898

google 899

Hands down Livewebtutors is the best proofreading service. I would recommend my friends to use their Dissertation Proofreading Service. This post has taught me a lot about these types of services and what a convenience it brings. I am impressed.

ReplyDeleteHi, I'm Chris Smith A blogger and Review writer From New York. Today I'm going to tell you about one of my favorite websites coupon2deal, where you can get great coupons and deals for free.

ReplyDeleteRosegal Coupon

Light In The Box Coupon

Alamy Promo Code

eBay Coupon



ReplyDeletegeeksscan I appreciate you for this article this is such a wonderful blog Thanks for posting this Read our blog It is related to technology It helps you to solve your issues that you are facing. This is our latest article visit here guest post site

thanks for sharing amazing information. pay to write essay

ReplyDeletewebroot setup


ReplyDeletecan be completed with insertion of 20-digit Webroot keycode. Webroot SecureAnywhere is one of the popular and widely accepted antivirus software in homes and offices.

Download and install or reinstall office.com/setup home and student 2019r



ReplyDeleteuninstall aol its simple go to control panel and then go to installed programes where you get the list of installed software in your pc and there you see aol tech fortress select right click and uninstall that.


ReplyDeletequickbooks support numberFor Smooth Working As Accounting & Finance Software


ReplyDeleteThese are genuinely fantastic ideas in concerning blogging.


ReplyDeleteYou have touched some fastidious points here. Any way keep up writing. 파워볼사이트

I certainly enjoyed reading every bit of your fascinating post. I’ve got you bookmarked to look at new things you post, thanks for sharing. Also checkout departmental cut off mark in tech-u

ReplyDeleteFantastic blog with amazing information, I really like your post, I always like to read quality content having accurate information regarding the subject. Thanks for sharing. Download absu post utme form


ReplyDeleteHello there! Nice article!!! But anyways here’s one of the trusted online baccarat site we can offer you so many promo and event everyday!! Good luck!!!


ReplyDelete토토

바카라사이트

파워볼

카지노사이트

So fantastic goods from you from your blog. I’ve understand your stuff previous to and you’re just too excellent. I enjoyed visiting this blog posts. Thanks for sharing. visit kwasu post utme form closing date

ReplyDelete

ReplyDeleteIts a really interesting and informative article for me. I appreciate your work and skills. Joe Collie Puffer Vest

error code 0xc0000225 windows 7 is the error occur because of the usualy when windows not able to find your system files that is using for booting and boot configuration data you can rebuild bcd to easy recovery of essentials etc. windows 7 code 0xc0000225.


ReplyDeleteTrading Directory is an experienced and reliable Forex Trading company. Here We compare online brokers using transparent 10 point checklists, so you can easily compare the most important factors in one glance.


ReplyDeleteNice Post Please Keep Posting Like This. I am really happy that you guys are writing content like this. Please Keep Posting on Regular Basis. Feel free to visit my website; 토토사이트



ReplyDeleteVery nice blog post. I like this site. Continue the good work! It is exciting to read it and, use it. Thanks for the article. Feel free to visit my website; 바카라사이트



ReplyDeletecanon.com/ijsetup is a website to download Canon printer drivers, you can also visit canonsetup-canon.com/ijsetup website for same.Some factors need to be in mind while choosing an inkjet printer for you. Later, you can easily set up your Canon printer through drivers from canon.com/ijsetup, wireless connection, USB, and a few components. The setup process for every Canon model is almost similar, however the download through http //ij.start.cannon or https //ij.start.cannon and installation process may differ.


ReplyDeleteHello, we have a game to recommend.



ReplyDeleteทางเข้า ufabet

ufabet kick

รูเล็ตสายฟ้า

แทง บอล ผ่าน มือ ถือ

กา บอล1

Thank you for your interest."

system mechanics professional is the best antivirus and real time protection that protect your pc and malware, trojan horse and many kind of latest viruses and give you the best experience of while using your systemmechanic activate.


ReplyDeletesystem mechanics professional is the best antivirus and real time protection that protect your pc and malware, trojan horse and many kind of latest viruses and give you the best experience of while using your systemmechanic activate.


ReplyDeleteDisney Plus is a subscription streaming service that aims to bring the disneyplus.com/begin experience to the whole family. The service features a variety of content from Marvel, Star Wars, Pixar, and Disney movies and TV shows. Disneyplus is a subscription streaming service from Disney, which will include programming from Marvel, Star Wars, Pixar and Disney.


ReplyDeleteGo to Foxnews.com/connect. Follow the steps below to sign in and start watching Fox News Channel and Fox Business Network. Click Watch Live above the video player. Under the video player, it will say "On Air Now". Click on the network you want to watch (Fox News or Fox Business). Select your cable or satellite operator from the list of participating TV service providers (note: this is not necessarily your Internet Service Provider). Below the main provider list, there is a drop-down list with more options. Enter your email address (or username) and password. To login to your account, go to foxnews.com/connect and click the login button in the top right of the screen. The screen will redirect you to the login page. Enter your email address and password.

ReplyDeleteGo to foxnews.com/connect. Follow the steps below to sign in and start watching Fox News Channel and Fox Business Network. Click Watch Live above the video player. Under the video player, it will say "On Air Now". Click on the network you want to watch (Fox News or Fox Business). Select your cable or satellite operator from the list of participating TV service providers (note: this is not necessarily your Internet Service Provider). Below the main provider list, there is a drop-down list with more options. Enter your email address (or username) and password. To login to your account, go to foxnews.com/connect and click the login button in the top right of the screen.

ReplyDeleteOn your screen disneyplus.com/begin the link, you need to go to DisneyPlus.com/Begin and follow the simple steps below: Go to DisneyPlus.com/Begin. Enter the 8-digit code displayed on your TV. Continue press Continue by pressing the Enter key. You can go back to your device of choice and start watching Disney+ How to activate Disney Plus on your device by going to disneyplus.com/begin Make sure it is on Wi-Fi internet, you can follow the steps below below: Connect your device to the internet and open the Disney Plus app. After that, you will be asked if you are already an existing Disney Plus member. If you already have a Disney Plus account, select "Yes". If you don't have an account yet, click "No". Follow the instructions to set up your account. At the end of the page, you will receive a unique code which will be used to turn on your device.

ReplyDeleteDisney+ is a video streaming service.You can access it on multiple devices, including mobile phones,disneyplus.com/start tablets, smart TVs, and set-top boxes. It costs a monthly fee for complete access. First touted back in 2017, Disney sees it as a "big strategic shift" for the company, with its extensive library of content, including Marvel and Star Wars titles.These have generally disappeared from Netflix and other services in order to be exclusive to Disney+.Disney+ offers shows and movies in up to 4K HDR (Dolby Vision) and up to Dolby Atmos audio. It also includes support for four simultaneous streams and the ability to set-up profiles for family members. There are also parental controls to restrict content depending on age - like Netflix and Amazon Prime Video.

ReplyDeleteOn the "Browse" tab of its website and apps, Tubi offers programming from a number of partner studios, like MGM,Tubi.tv/activate Lionsgate, Paramount, and Full Moon Pictures. Some of their most noteworthy inclusions are movies like "The Pursuit of Happyness," "Dinner For Schmucks," "Major League," "Girl Interrupted," and "Kung Fu Panda." There are also TV shows, like "Hell's Kitchen," "Daredevil," "Dance Moms," "The Masked Singer," and "Forensic Files." They even have a separate section of content just for kids.Tubi is available to watch on its website and on iOS and Android devices.

ReplyDeleteDisney Plus is one of the most popular streaming services in the world. You can find a complete list of Disney classics as well as your new favorite Disney films. Disney offers a variety of TV series, movies, and news, as well as sports. Disney plus is a one-stop shop for all of your favorite Disney shows and movies. To watch the Disneyplus.com/begin on your device, you need to activate it or install it on that device. There's plenty of programming from Pixar, Marvel Studios, and the Star Wars world, in addition to Disney is the most popular subscription channels in the world. This service allows you to stream live TV shows, sports, and videos. Disney also will enable you to purchase new movies.

ReplyDeleteThis is great and awesome post for me. I loved to read your blog. it's really-really amazing. thanks for inspired me by your blog. help in writing dissertation

ReplyDeleteLearn how to download and install in-dash map updates and software updates. A computer or laptop, USB flash drive to connect with your computer. You can perform Honda in-dash Software and Map Updates.

ReplyDeleteA conception nice way of blogging, this article writing is also an excitement, if you be acquainted with after that you can write otherwise it is complex to write. very interesting blog! Thanks for sharing. visit lautech freshers school fees this year

ReplyDeleteIt was a very good post indeed. I thoroughly enjoyed reading it in my lunch time. Will surely come and visit this blog more often. Thanks for sharing. I was just browsing through the internet looking for some information and came across your blog. I am impressed by the information that you have on this blog. It shows how well you understand this subject. Bookmarked this page, will come back for more Thanks for the wonderful share. Your article has proved your hard work and experience you have got in this field. Brilliant .i love it reading. What a decent blog you have here. It would be ideal if you refresh it all the more frequently. This points is my advantage. Much obliged to you. 사설토토


ReplyDeleteThis is the best way to share the great article with everyone one.thank you write my assignment

ReplyDeleteinteresting content you have here. check unilorin past question

ReplyDeleteThank you for awesome blog post. We are really grateful for your blog post. Please keep it up. Essay writing services uk

ReplyDeleteThis comment has been removed by the author.

ReplyDeleteIf approved, you Fast 600 Payday Loans must read your loan agreement carefully to make sure you get acquainted with the payday loans guaranteed approval no matter what direct lenders interest rate, term, and other conditions.

ReplyDelete



ReplyDeletePlayground Surfacingis crucial for ensuring the safety of children during playtime. Various materials are used, including rubber mulch, poured-in-place rubber, engineered wood fiber, and artificial turf. Each material offers different benefits in terms of shock absorption, durability, and maintenance requirements. Rubber mulch is popular for its cushioning effect and resistance to weathering, while poured-in-place rubber provides a seamless surface.Engineered wood fiber is cost-effective and offers good shock absorption, and artificial turf provides a natural look with minimal maintenance. Choosing the right surfacing material is essential for creating a safe and enjoyable playground environment.

At GKMIT, we specialize in delivering exceptional front-end solutions designed to enhance your web and mobile applications. As a leading Front End Development Service Company, our team of skilled developers is dedicated to creating user-centric, cutting-edge digital experiences that empower your online presence. We focus on innovation and excellence, offering customizable front-end development services that align with your business needs. Whether you're looking to create a visually stunning website or build a mobile app with seamless navigation, our developers ensure that your digital platforms are both functional and aesthetically appealing. By integrating the latest technologies and industry best practices, GKMIT's front-end solutions provide responsive, high-performance user interfaces that engage your audience and drive results. Our commitment to delivering robust, scalable solutions makes us the trusted partner for businesses looking to stay ahead in today's fast-paced digital landscape.

ReplyDeleteThank you for this incredibly detailed and informative walkthrough of the Stingray renderer! for ISO Certification In Saudi Arabia contact us, Improve Customer Satisfaction Meet customer expectations with certified quality standards.

ReplyDelete"Keep your garage door in top shape with fixngotx garage door maintenance services. Our expert technicians provide thorough inspections, lubrication, and adjustments to ensure smooth operation and prevent costly repairs. With our affordable, reliable, and professional service, you can trust us to extend the life of your garage door and enhance your home’s safety. Contact us today!"

ReplyDeleteQuickBooks Payroll Direct Deposit allows businesses to pay employees quickly and securely by depositing paychecks directly into their bank accounts. It eliminates the need for paper checks and reduces payroll processing time. This feature supports timely, accurate payments and helps streamline payroll management.



ReplyDeleteRead More:

Create QuickBooks Antivirus Exclusion

QuickBooks Antivirus Exclusion

This walkthrough clearly explains how Stingray’s data-driven rendering pipeline works, showing how JSON files define shaders, resources, and frame flow, making the system flexible, hot-reloadable, and adaptable to different project needs.Iso 17025 Certification in Ethiopia


ReplyDeleteThis is amazing! Thank you for sharing - your work is truly inspiring. Your talent shines through in everything you create! Physics can feel challenging with its formulas, diagrams, and problem-solving concepts—but creating a high-quality Physics assignment doesn’t have to be stressful. Physics assignment help can make the entire process easier by offering guidance, clarifying tough concepts, and supporting you with step-by-step solutions. With the right approach, proper planning, and effective support, you can complete your work faster and with greater confidence.

ReplyDelete