---
title: 'My toy renderer, part 1: Keep it simple'
url: http://momentsingraphics.de/ToyRenderer1KeepItSimple.html
published: '2021-06-25'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# My toy renderer, part 1: Keep it simple

Part 1 of this [series about my toy renderer](http://momentsingraphics.de/ToyRendererOverview.html) covers the most fundamental design decisions. Over the years, I have written many renderers and for a long time their complexity kept growing. This time, I took the opposite route. I wanted to maximize the fraction of code that implements crucial functionality rather than wasting my time on bloaty infrastructure. The code that I wrote (excluding shaders) has 7575 lines at 345 kB. Not exactly a 4k intro but much smaller than any other real-time renderer I have used before. It takes ca. one second to compile and link and startup is also quick.

Upfront, I want to clarify one thing: The design decisions that I advocate here were made for a research renderer developed by a single person. I am not arguing that the same designs should be favored for big commercial projects. However, I would argue that if you develop new techniques for a big commercial product, it may be best to have a small testbed for that, such as the one I am describing here. And some of the ideas, e.g. the way in which I load scenes, may be inspiring for bigger projects.

## Compile times matter

Long compile times are a [huge detriment to productivity](https://xkcd.com/303/). Compiling and linking a big C++ project with lots of dependencies and some template magic can easily take several minutes. I once had a C++ project with only 300 lines of code. Unfortunately, it also had the header-only, template-centric library [Eigen](https://eigen.tuxfamily.org/) as dependency, so compile times immediately rose to half a minute (for a single *.cpp file).

What does that mean for a programming workflow? As you implement a big chunk of new functionality, you are discouraged from testing small bits of it because that requires recompilation. Once you are done, you compile. Maybe at some point in the middle of compilation, an error will be thrown at you. Once that is fixed, you compile again and might get to the point where you encounter run time errors. Maybe you have to compile a debug build to understand those. You squash one trivial bug after the other and eventually things work as they should. If you have compiled and linked ten times during that process and that took one minute on average, you have wasted ten minutes waiting for your compiler.

I firmly believe that this time is always wasted. The time frame is just short enough that it is not wortwhile to switch to another task. People develop different habits of idling, e.g. checking newspages way too frequently. In the worst case, that means that you do not notice when compilation has finished and lose even more time.

Of course, people are aware of this problem and there are many attempts at solutions. Though, all of these make programming more restricted and programs more complex in some way. For example, there is the [PImpl idiom](https://en.cppreference.com/w/cpp/language/pimpl) but that adds boilerplate code, makes code less clear and only shortens compile times for certain types of changes. Modules are another attempt at improving compile times but [gains appear to be moderate](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1441r1.pdf). You can throw hardware at the problem but possibilities for parallelization of compilation and linking are limited, so that cannot get you all that far.

Halving compile times is nice but reducing them to a second is nicer. Just think of some situation where you programmed without having to wait for a compiler. Hot reload of shaders, e.g. on [Shadertoy](https://www.shadertoy.com/), is a nice example. Such an environment encourages experimentation and testing, increases productivity and removes a lot of frustration, especially during debugging. printf debugging is rightfully discouraged in settings with long compile times but can be extremely convenient if compilation and startup are quick. [Python](https://www.python.org/) with the [SciPy stack](https://scipy.org/) is another good example. Of course Python executes more slowly than C++ but most of the time my Python scripts are done running before a similar C++ program would have finished compilation.

Inspired by such experiences, engine developers sometimes try to let you do as much as possible without recompiling. Hot shader reload is a positive example of that. Node graphs, plugin systems or the integration of separate scripting languages are a bit more questionable. They can be quite powerful but the effort to let them interact with all parts of the engine is substantial. Source code is an incredibly powerful and expressive way to accomplish all sorts of tasks. If you invest a lot of effort into a second system for the same purpose, which may also be less convenient to use, you are jumping through hoops because of long compile times.

## Goodbye C++, hello C

I have been using C++ for a long time and for a decade or so, I have been enthusiastic about it. I went deep down into rabbit holes of object-oriented programming, template magic, the STL and boost. I got accustomed to long compile times and boilerplate code. Then three experiences gradually shook my faith into C++: Hot shader reload, [Python](https://www.python.org/) and [Corona](https://github.com/hanatos/corona-13/) (not the one you are thinking of). The first two should be obvious at this point. Making changes to your code and seeing the result a second later is freeing. Besides, Python is so much leaner than C++. As an example, the following code snippets extract the 3 top rows from a 4×4 matrix in [NumPy](https://numpy.org/) and [Eigen](https://eigen.tuxfamily.org/), respectively.

`top = matrix[:3, :]`


`Eigen::Matrix<double, 3, 4> top = matrix.template topRows<3>();`


Then I did some [offline rendering](http://momentsingraphics.de/Siggraph2019.html) and I used the research renderer [Corona](https://github.com/hanatos/corona-13/) developed by my colleague Johannes Schudeiske (the name of the renderer was already awkward before the pandemic, considering that there is a [commercial renderer](https://corona-renderer.com/) with the same name). That is how I came to appreciate the elegance of C. Corona is a moderately big project but it compiles in under two seconds. And the code base has pleasantly little boilerplate code. Where C++ gives you many slightly different takes on the same concept (e.g. `unique_ptr`

, `shared_ptr`

and raw pointers), C gives you one way to go and that one has a conveniently compact notation (such as `float*`

). Chunks of memory are such a universal and natural abstraction that C interfaces can be flexible and long-lived ([stb](https://github.com/nothings/stb) is a good example).

Sticking with the example of matrix math, it is baffling how C code is often more compact and readable than C++ code. A matrix declaration would be `float matrix[4][4];`

. The evergreen [matrix and quaternion FAQ](https://j3d.org/matrix_faq/matrfaq_latest.html) has many great examples of how this kind of code can look in C. Of course, you could take the same approach in C++ but then you are not really using C++. The example from above in C could be simply:

`float* top = matrix;`


Object-oriented programming makes way for structs and global functions. In certain contexts, I have come to prefer this design for a simple reason: When a function interacts with instances of multiple classes, it is often somewhat arbitrary where you put it. It could be a member of any one of the classes or global. If global is the default, no guesswork is required. My structs come with global create and destroy functions. If they are `memset`

to zero, they are “default constructed.” If something goes wrong during initialization, create invokes destroy for cleanup. This approach incurs little boilerplate code. In particular, I won't miss writing setters and getters.

But of course the killer feature of C compared to C++ are short compile times. I do not envy developers of C++ compilers. The C++ standard makes their job difficult and that sometimes results in compromises on efficiency. C is easy to compile and link by design. I can believe that other newer languages such as Rust or D are more pleasant to use than modern C++. However, they seem to perform similarly in terms of compile times.

## Dependencies (or the lack thereof)

Reproducibility is important in research. Others should be able to run my code easily and get the same results. That first part is often hampered by dependencies. In this regard, C and C++ are not that far apart. The best way to ensure that code will be easy to compile, link and run is to restrict dependencies to the bare minimum.

So what is the bare minimum? To use the GPU, I need a graphics API. [Vulkan](https://www.vulkan.org/) is the one that is most widely supported so that is a natural choice. I am not going to write my own extension loader and I also need some operating system fundamentals (e.g. window creation and input/output). [GLFW](https://www.glfw.org/) covers those needs. [Dear ImGui](https://github.com/ocornut/imgui) is incredibly helpful for rapid prototyping. It is not exactly minimalist but as a dependency it behaves itself. You are supposed to just add its source files to your project. It is written in C++, so I need a bit of C/C++ interop here but that is painless. Finally, I use [stb_image_write.h](https://github.com/nothings/stb/blob/master/stb_image_write.h) to write screenshots as PNG, JPG or HDR.

That's all. I ship Dear ImGui, GLFW and stb with my source code releases. GLFW gets compiled as separate project, everything else is part of the project for my renderer. Thus, there are few things that can go wrong with linking. The Vulkan SDK is the only thing that has to be installed separately but that is easy enough and unavoidable, because it is platform specific. I use CMake but it does not do much.

## Wrappers are pointless

My old instinct as I start to use a new graphics API (such as Vulkan) would have been to write wrappers around all functionality that I need. But what does that really accomplish? Well, wrappers:

- Replace familiar interfaces by unfamiliar ones
- The Vulkan specification is relatively well-known among graphics developers. It is certainly more familiar than some private little wrapper that I would put on top of it.
- Remove functionality
- A recurring theme of wrappers is that they try to limit the extensive functionality of graphics APIs to the bits that are frequently used. While that can make certain tasks a bit more convenient, it makes other tasks impossible. In graphics research, you frequently seek out the latest and greatest features (e.g.
[ray queries](https://vulkan.lunarg.com/doc/view/1.2.176.1/linux/1.2-extensions/vkspec.html#VK_KHR_ray_query)in my renderer). Sometimes you need some fairly obscure features. If you rely on wrappers, you first write a wrapper around these obscure features (coming up with your very own unfamiliar interface) and then use them. Using them through the graphics API directly is simply more efficient. - Add bugs
- Like any software, APIs and graphics drivers have bugs. However, this software is widely used, extensively tested and developed by many well-paid professionals. The rate of bugs is reasonably low. Any wrapper will inherit all of these bugs and add some on its own, most likely at a higher rate.
- Protect state
- In stateful APIs such as OpenGL, it has been difficult to ensure that the API is in the right state before each draw call. Wrappers could help with that. But Vulkan goes all in on
[pipeline objects](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#pipelines-graphics)that make the state monolithic. There is no longer a need for such features. - Encapsulate everything in an object-oriented fashion
- I have no use for that. I am happy with the C interfaces of Vulkan and the way I use them (see below).
- Make it possible to exchange one API for another
- It is true that wrappers can make this possible but it is never easy. Usually programs working on top of a wrapper have to be tested carefully against all targeted APIs. I would favor going one level up or down. Either have a consistent scene description that can be rendered by renderers with different APIs or use things like
[MoltenVK](https://github.com/KhronosGroup/MoltenVK)to map a complete graphics API onto a different graphics API.

The bottom line is that I want to use Vulkan directly. Vulkan structs and functions are used in most parts of my renderer. There is no wall delineating API specific code from API independent code. Vulkan is not meant to ever be exchanged for anything else. I would rather rewrite the whole thing.

## Utilities are useful

Of course, writing software with Vulkan from scratch is a lot of work and I would not want to do that every single time. I wrote 1750 lines of code before rendering my first triangles. Wherever possible, my renderer is composed of reusable little chunks. They are not wrappers because they work directly with Vulkan structs and handles but they bundle together some functionality that is frequently used together. If that is what you want, good. If not, just invoke Vulkan functions directly or write another utility.

Here is one example of what that looks like. When you create a couple of buffers, you usually also want to allocate and bind memory for them. Thus, I have structs that maintain an arbitrary number of buffers with a single memory allocation and provide convenient access to some meta data:

```
//! Combines a buffer handle with offset
//! and size
typedef struct buffer_s {
//! The buffer handle
VkBuffer buffer;
//! The offset in the bound memory
//! allocation in bytes
VkDeviceSize offset;
//! The size of this buffer without
//! padding in bytes
VkDeviceSize size;
} buffer_t;
//! A list of buffers that all share a
//! single memory allocation
typedef struct buffers_s {
//! Number of held buffers
uint32_t buffer_count;
//! Array of buffer_count buffers
buffer_t* buffers;
//! The memory allocation that serves
//! all of the buffers
VkDeviceMemory memory;
//! The size in bytes of the whole
//! memory allocation
VkDeviceSize size;
} buffers_t;
/*! Creates one or more buffers according
to the given specifications, performs
a single memory allocation for all of
them and binds it.
\param buffers The output object. Use
destroy_buffers() to free it.
\param device The used device.
\param buffer_infos A specification of
each buffer that is to be created
(buffer_count in total).
\param buffer_count The number of
buffers to create.
\param memory_properties The memory
flags that you want to enforce for
the memory allocation. Combination
of VkMemoryHeapFlagBits.
\return 0 on success.*/
int create_buffers(
buffers_t* buffers,
const device_t* device,
const VkBufferCreateInfo* buffer_infos,
uint32_t buffer_count,
VkMemoryPropertyFlags memory_properties);
/*! Destroys all buffers in the given
object, frees the device memory
allocation, destroys arrays, zeros
handles and zeros the object.*/
void destroy_buffers(
buffers_t* buffers,
const device_t* device);
```


Crucially, `create_buffers()`

expects an array of [ VkBufferCreateInfo](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#VkBufferCreateInfo), not some wrapper imitation of that structure. No matter how exotic the flags are that you want to use for buffer creation, you can use them.

In using this function, a trick that I learned from [Christoph Schied](http://brechpunkt.de/q2vkpt/) comes into play. The [struct initialization in C](https://en.cppreference.com/w/c/language/struct_initialization) lets you treat Vulkan structs like [keyword arguments in Python](https://docs.python.org/3/glossary.html#term-argument). Lately, [C++ also made that possible](https://en.cppreference.com/w/cpp/language/aggregate_initialization). Everything you do not mention, gets zero-initialized and Vulkan is carefully designed so that zero gives reasonable defaults. For example, this code creates the staging buffer for tables of stratified random numbers:

```
VkBufferCreateInfo buffer_info = {
.sType = VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO,
.size = sizeof(uint16_t) * cell_count,
.usage = VK_BUFFER_USAGE_TRANSFER_SRC_BIT
};
buffers_t staging;
if (create_buffers(&staging, device,
&buffer_info, 1,
VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT))
{
printf("Failed to create a %llu byte staging buffer for noise.\n", buffer_info.size);
return 1;
}
```


I would argue that the first two lines are boilerplate but everything else expresses something meaningful about what kind of buffer I need. And that is how it works out most of the time.

This example also illustrates my memory management. The basic strategy is to have one memory allocation per purpose, e.g. one for vertex data, one for textures and one for stratified random numbers. That might not be exemplary but works well in such a small project. My renderer makes a total of 21 memory allocations prior to the first frame, including staging buffers.

I have made positive experiences with reusability of this code. For example, I once wanted a headless application that optimizes some blue noise point sets on the GPU. Although this use case is quite different from what the renderer was written for, it did not take a lot of time and worked flawlessly. One thing that can be slightly annoying to do with my current setup is multi-pass rendering. But that is mostly because I only have three passes at this time so I have not bothered to set up a lot of support code for this kind of thing.

## Dependency “graphs”

In one of my [earlier renderers](http://momentsingraphics.de/HPG2017Demo.html), I was a bit proud of an automated system that kept track of a dependency graph and would automatically figure out the order in which things should get reinitialized if anything changes. It was a fancy object oriented system where everything inherited from some common base classes and method invocations defined dependencies. My new toy renderer has the same feature implemented in two lines of code. I think as far as “keeping it simple” goes, this part is the best example.

I have a `struct application_updates_t`

full of booleans to keep track of what needs to change due to user input. Then there is a function to perform these updates, which gets invoked for application startup and once per frame:

```
/*! Repeats all initialization procedures
that need to be performed to
implement the given update.
\return 0 on success.*/
int update_application(application_t* app,
const application_updates_t* update_in);
```


In this function, I first mark the objects that are directly affected by this update and need to be recreated.

```
VkBool32 swapchain = update.recreate_swapchain;
VkBool32 noise = update.startup | update.regenerate_noise;
VkBool32 ltc_table = update.startup;
VkBool32 scene = update.startup | update.reload_scene;
VkBool32 render_targets = update.startup;
VkBool32 render_pass = update.startup;
VkBool32 constant_buffers = update.startup | update.update_light_count | update.change_shading;
```


But of course, there are also dependencies to account for. Objects referenced other objects during creation so if these other objects get recreated, they also have to be recreated. For example, recreation of the swapchain usually means that the resolution has changed, so render targets also have to be recreated. This is the part that used to be handled by a dependency graph. Now it is handled by a single loop.

```
uint32_t max_dependency_path_length = 16;
for (uint32_t i = 0; i != max_dependency_path_length; ++i) {
render_targets |= swapchain;
render_pass |= swapchain | render_targets;
constant_buffers |= swapchain;
}
```


If you want to be fancy, you can call this a dependency graph. The `|`

operator defines edges and the loop implements [breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search) in a stupid but lean and correct way. The reason why I like this code so much is that almost all of it defines the graph using a compact notation. Only the two lines for the for-loop serve the implementation of the graph traversal. In an object-oriented setting, you could overload the `|`

operator to get the same syntax. But then nobody would know what that code does without looking up the definition of the operator. Applying an `or`

to booleans is self-explanatory.

Once all the dependencies have been propagated, the objects that need to be destroyed get destroyed in reverse order:

```
vkDeviceWaitIdle(app->device.device);
if (constant_buffers) destroy_constant_buffers(&app->constant_buffers, &app->device);
if (render_pass) destroy_render_pass(&app->render_pass, &app->device);
if (render_targets) destroy_render_targets(&app->render_targets, &app->device);
if (scene) destroy_scene(&app->scene, &app->device);
if (ltc_table) destroy_ltc_table(&app->ltc_table, &app->device);
if (noise) destroy_noise_table(&app->noise_table, &app->device);
```


Then, if necessary, the swapchain gets resized without recreating the underlying window. Finally, all other objects get recreated. It is guaranteed that all the objects they depend on have been recreated first. This step exploits [short-circuit evaluation](https://en.wikipedia.org/wiki/Short-circuit_evaluation) for compact code that aborts at the first error.

```
if (
(noise && load_noise_table(&app->noise_table, &app->device, get_default_noise_resolution(app->render_settings.noise_type), app->render_settings.noise_type))
|| (ltc_table && load_ltc_table(&app->ltc_table, &app->device, "data/ggx_ltc_fit", 51))
|| (scene && load_scene(&app->scene, &app->device, app->scene_specification.file_path, app->scene_specification.texture_path, VK_TRUE))
|| (render_targets && create_render_targets(&app->render_targets, &app->device, &app->swapchain))
|| (render_pass && create_render_pass(&app->render_pass, &app->device, &app->swapchain, &app->render_targets))
|| (constant_buffers && create_constant_buffers(&app->constant_buffers, &app->device, &app->swapchain, &app->scene_specification, &app->render_settings))
)
return 1;
```


The function `update_application()`

is the only place in my code-base where all these create and destroy functions get invoked. There is very little redundancy in this code, every line says something important about the inner workings of the program. The code above is abridged a bit for this blog post, there are a few more objects requiring initialization. Though, all the ideas are present.

## Embracing the GLSL preprocessor

Another common source of complexity in real-time renderers is handling the many different shaders. Like any research prototype, my toy renderer has to implement many variants of many techniques for comparisons. In the past, I created a graph-based system where every function invocation was a vertex and every input an edge. Then the shader got plugged together automatically. The result was a mixture of hand-written shader code with nothing but functions for tiny building blocks and moderately readable auto-generated shader code. [Appendix D of my JCGT paper on moment shadow maps](http://jcgt.org/published/0006/01/03/) is a testament to that. Later I used [Falcor](https://github.com/NVIDIAGameWorks/Falcor), which embraces the customized shader language [Slang](https://github.com/shader-slang/slang) to alleviate the problem.

These solutions have something in common with wrappers: They replace a familiar system (GLSL shaders) by something unfamiliar. That is a problem, because my shader code functions as a reference implementation. Others should learn from it and be able to adapt it to their needs. The more obfuscated the code is, the less likely it is that the demonstrated techniques get used by others. I prefer plain old GLSL that every somewhat senior graphics developer can read and understand.

Thus, my renderer uses the GLSL preprocessor extensively, especially in the form of `#if`

. Any selection of a rendering technique corresponds to a bunch of preprocessor defines. They are toggled by the C-code that compiles the shaders at run time by invoking [glslangValidator](https://github.com/KhronosGroup/glslang/). Some functions are implemented by long chains of `#if`

and `#elif`

directives to implement the same functionality with many different techniques. While that can be slightly cumbersome to read, the same could be said of all other solutions I've encountered thus far. It also means that shaders get recompiled whenever a setting changes. There are so few of them that recompilation is fast and there is no point in caching all possible variants.

## Conclusions

Before using this new toy renderer, I have been using the C++ renderer [Falcor](https://github.com/nvidiagameworks/falcor) and prior to that various versions of [my own thing](http://momentsingraphics.de/HPG2017Demo.html). I do not miss either of those and feel more productive now. The short compile times really make a difference and when new features get added to Vulkan, they are available to me instantly. Falcor gets lots of things right but compile and load times are quite bad. It is also a bit annoying that ca. 4 GB of disk space go away whenever I compile a Falcor application.

In the next part of this series, our main concern are fast load times.