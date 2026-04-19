---
title: 'Review: Learning Vulkan by Parminder Singh'
url: https://cybereality.com/review-learning-vulkan-by-parminder-singh/
author: Cybereality
published: '2017-03-02'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

![](../../assets/569542a921b7cfda.jpg)


Learning Vulkan by Parminder Singh is an excellent foray into the Vulkan graphics API and quite a competent book. The text is a reasonable 466 pages, and packs a lot in there. Singh covers all the basics of using Vulkan and goes into great detail at each step of the way. Not only is there actual C++ code shown (a lot of it), but he explains each API call and what objects to pass it, a breakdown of each object structure and what it does, what’s valid (or invalid) for data you can put in, and so forth. I have not read the official Vulkan Programming Guide yet (that’s coming next) so I’m not able to compare them here. However, this book is an absolute treasure trove of information, and presented with clear context, not just a copy and paste of API docs.

While the book is not particularly long, the author does manage to cover a good amount of ground. Of the topics included are: getting started with the LunarG SDK, initializing the API, debugging, command buffers and memory management, allocating image resources and the swapchain, buffers, render passes, framebuffers, working with SPIR-V shaders, pipelines and pipeline state management, descriptors and push constants, and finally drawing a textured polygon. I’m still getting acquainted with Vulkan myself, but this does seem to touch on all the fundamental topics to get started with the API. It really seems like Parminder Singh knows what he is talking about and feel I learned a lot finishing this text.

One thing to keep in mind, this is not really a book about graphics programming techniques, but rather a survey of the API. Meaning, unlike Frank Luna’s DirectX books, you won’t have any cool demos to showcase at the end. Through the whole book you’re basically just working with the initialization of the Vulkan API, though you do end up with a colored triangle and finally a textured cube. This is honestly fine, and just what is needed at this point in the life of Vulkan. Flashy demos are cool, sure, but once you have the fundamentals down, it shouldn’t be hard to apply that knowledge, or port techniques from other APIs.

I will note, however, that I wish there was more discussion into the performance cost or characteristics of parts of the Vulkan API. For example, sometimes there are multiple ways to perform an action (like with uniform buffers or push constants getting data into a shader) and there wasn’t much explanation as to when to do one thing over the other. This is not a huge concern, as there are lots of articles online covering these types of things and it seems the book is there to get you familiar with the concepts and data structures to allow you to do your own research later. Certainly, I still have a lot of questions but I can’t imagine a more thorough book as an introduction to this relatively new API.

Some familiarity with older graphics APIs will probably help, but I don’t think it’s absolutely needed. In my opinion, if you are wanting to learn graphics programming today, you might as well just jump into Vulkan (or DirectX12, if you prefer) as the industry will quickly adopt these new, lower-level APIs and you will be setting yourself up for the future. Do understand, though, that Vulkan is extremely verbose and needs something like 1,000 lines of code just to get a triangle on the screen. So stark beginners may be put off by that complexity. And you should definitely have good working knowledge of C++ before getting into this. With that in mind, however, I think that Learning Vulkan by Parminder Singh is a great place to start to delve into this exciting new world of Vulkan. Well worth reading.