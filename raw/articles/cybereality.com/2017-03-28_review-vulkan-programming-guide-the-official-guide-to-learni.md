---
title: 'Review: Vulkan Programming Guide: The Official Guide to Learning Vulkan by
  Graham Sellers'
url: https://cybereality.com/review-vulkan-programming-guide-the-official-guide-to-learning-vulkan-by-graham-sellers/
author: Cybereality
published: '2017-03-28'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

![](../../assets/a3a04da7e77c4f2a.jpg)


Although the Vulkan API has been available for about a year now, it was just at the tail end of 2016 that we started to see books published on the topic. For me personally, I prefer learning from books over just reading documentation, and Vulkan Programming Guide is a fine effort. At 480 pages, it is a comfortable length, and manages to hit on a lot of major elements in the API. It is by no means comprehensive, as most of the coverage just shows function or structure prototypes (something you can likely find in the online docs) but there is at least some explanation of what each function does. I found useful the explanation of device limits (such as the maximum frame buffer size, number of bytes in a push constant, etc.) and how to query them, as I have not seen this touched in other texts. Sellers also does a great job of introducing synchronization concepts in one of the later chapters. This is absolutely essential for proper multi-threading, and I have not seen this in other books (at this depth). There is some discussion here and there to performance characteristics. Maybe not enough, but the author does attempt to give guidance on how expensive a particular call could be, or when it might hurt performance. Overall the book was solid. This will be my 3rd Vulkan book, along with a number of tutorials, and I felt there was relevant info gleaned from the text.

Vulkan Programming Guide has 13 chapters, each focusing on a key aspect of the Vulkan API. Inside these chapters are: a high-level overview of Vulkan itself, memory and resources, queues and commands, memory barriers and buffers, presentation, shaders and pipelines, graphics pipelines, drawing, geometry processing, fragment processing, synchronization, queries, and multipass rendering. Not a bad mix of topics. I don’t think anything major was left out, however, some of the coverage could be more fleshed out. While there was great detail on some things. For example, showing SPIR-V disassembly code, other topics were only given a cursory look. In particular, there is very little source code in the book. While the author goes to great lengths to show structure and function prototypes, there isn’t a whole lot of code showing actual usage. While it’s debatable if this is necessary, I would find more code examples to be useful. To be fair, the code that is shown looks good, there just needs to be more it.

All in all, I feel the book is solid and, considering Vulkan is relatively new and there aren’t that many texts available, it’s not a bad choice. One thing to note: I would recommend you start with Learning Vulkan by Parminder Singh. Learning Vulkan is a much more approachable resource, and I found it a little easier to follow. While Vulkan Programming Guide is more in-depth in many cases (in terms of the API spec itself), Learning Vulkan has a lot more C++ sample code, and may be more useful in that respect. In any case, I would buy both books because there are unique advantages in each one. Could Vulkan Programming Guide be improved? Sure. But it’s not a bad book and if you are getting into learning Vulkan today you’ll really need any and every resource you can get your hands on, and this should certainly be on your shelf.