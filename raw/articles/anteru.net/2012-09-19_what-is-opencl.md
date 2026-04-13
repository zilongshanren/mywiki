---
title: What is OpenCL?
url: https://anteru.net/blog/2012/what-is-opencl
published: '2012-09-19'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

*This is a short, basic introduction to OpenCL targeted at customers who are curious to understand how software works and for developers who are not yet familiar with massively parallel programming.*

As a consumer, you might wonder why your new mobile phone comes with a quad-core processor and what applications can take advantage of it. Similarly, if you have a notebook, you probably have multiple cores right now, yet some applications like a text processor don’t run faster while others like image processing do benefit a lot. How comes? As a developer, you might have come to the point where you try to rewrite parts of your application to benefit from multi-threading, and you wonder why this is so complicated using the OS interfaces?

Due to NVIDIA’s excellent marketing, you’ve probably already heard about [CUDA](http://www.nvidia.com/cuda). On notebooks, there’s often a greenish “CUDA enabled” sticker. But what does it actually mean? And how does CUDA fit into the big picture?

The core problem in the hardware space right now is power usage; battery life in mobile devices is very important, just as efficiency in desktop or notebook PCs. What happened is that it’s no longer possible to run a single program faster – on the other hand, multi-core CPUs can run multiple programs at the same time. Each of them might run just as fast as it did a few years ago, but by running more of them, the overall throughput increases. That’s the reason we’re seeing more and more cores even in mobile phones. Graphics cards are also a type of processor with lots and lots of processing cores.

The big question with all these cores is how to make efficient use of them. What CUDA brought to the table was a programming model, inspired by the graphics APIs, which we now consider the best approach for highly parallel programs. This programming model brings strong constraints – for instance, communication between elements is limited, memory accesses are more complicated, but it allows certain problems to be efficiently solved. For instance, a lot of image processing tasks like blurring or adjusting colours maps very well to this programming model. However, if an application is designed for CUDA, it also means that it is limited to NVIDIA’s GPUs. This may be fine, but sometimes you don’t have a GPU, sometimes the memory on the GPU is not enough, and sometimes AMD’s GPUs might be just faster at a given problem.

Enter [OpenCL](http://www.khronos.org/opencl/): OpenCL is a standardized formulation of the parallel programming model, with similar constraints as CUDA, but with a much wider hardware support. From mobile phones over graphics cards to CPUs, OpenCL provides an unified interface for software developers. For you as a customer, this means you have to care less about the particular device at hand. Your image processing suite will work just fine on your smartphone, on your notebook, and if you move it to you desktop PC, you will get better performance, but in every case, the software will use the hardware *efficiently*. With CUDA, what might happen is that on your notebook without an NVIDIA card, a tool will only use one CPU core and burn a lot of power. With OpenCL, chances are that it will all CPU cores and the integrated graphics chip as well. This will result in better performance and lower energy use.

For you as a customer, OpenCL is yet another technique which makes your software run faster and improves battery life/power efficiency. It also makes it easier for you to compare and choose hardware which works best for your problem, as you get more choice. Finally, OpenCL is also heading to the web: In the future, we can expect image processing tools which are running completely in the browser. These tools are highly likely to take advantage of OpenCL.

For you as a developer, OpenCL provides an API to target a lot of massively parallel hardware platforms with the same code. This means less duplication, easier development and easier deployment. If you haven’t given it a try yet, you should at least take a look now. Parallel programming is here to stay, and OpenCL provides the most gentle introduction to it.