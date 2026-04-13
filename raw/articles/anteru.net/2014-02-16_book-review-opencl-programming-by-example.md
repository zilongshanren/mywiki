---
title: 'Book review: OpenCL Programming by Example'
url: https://anteru.net/blog/2014/book-review-opencl-programming-by-example
published: '2014-02-16'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

I just finished reading through “[OpenCL Programming by Example](http://www.packtpub.com/opencl-programming-by-example/book?utm_source=socialmedia.com&utm_medium=blog&utm_campaign=OpenCL%20Programming)“, a new book on OpenCL programming. Before we start though, I’m going into full disclosure mode here: I didn’t buy the book, but I got it from [Packt Publishing](http://www.packtpub.com/) for reviewing. All they did is send me the book for free – thanks! Seems it does pay off I write regularly about OpenCL :)

## Packaging

Without further ado, let’s get started. The book is available as PDF, [EPUB](http://en.wikipedia.org/wiki/EPUB), [MOBI](http://en.wikipedia.org/wiki/MOBI) and in the Packt Publishing online reader. I’ve looked at all of them: I the PDF version is the best one, closely followed by the online reader. The ePub is good but has occasional formatting problems (for example, math formulas are rasterized) and the MOBI didn’t format correctly on my Kindle out of the box (the fonts were too small.) You get all versions if you buy it, so you can pick which one works best for you.

## Target audience

This book is aimed at experienced C programmers who haven’t used OpenCL before. I doesn’t hurt to have some parallel programming experience before buying this book, but the authors do a decent job of explaining the programming model.

## The content

I’ve been reading through this book over the last two weeks, and it’s definitely not the kind of book you can just read through in one go. It contains a lot of reference documentation, explaining the OpenCL API functions in similar scope and detail as the [official manual pages](https://www.khronos.org/registry/cl/sdk/1.2/docs/man/xhtml/). There’s also no clear path through the book motivating the individual chapters. Ideally, you pick it up if you are interested on a particular topic, read through the chapter, and go straight to implementation.

Another difficulty that arises is that this book has quite a few spelling mistakes and weird sentence structures. If you expect at least some “reading flow” from your book, you’ll be disappointed. While it makes it hard at times, it’s not too horrible, but during reading, I had the urge to edit and fix a paragraph more than once.

That said, the content itself is solid and obviously written by someone who knows his way around OpenCL. It is written first and foremost for OpenCL 1.2, but it explains the 1.1 APIs that have to be used if your platform doesn’t support 1.2. API wise, the books covers all OpenCL 1.2 core APIs and the OpenGL/OpenCL interop extension. It also mentions [SPIR](https://www.khronos.org/news/press/khronos-releases-spir-1.2-specification-for-portable-encoding-of-opencl-dev), without going into any detail.

The book itself starts with explaining parallel programming architectures, which are probably the weakest chapters in the whole book. It then continues with the OpenCL API, explaining buffers, images, kernels and events. This is a part where I would have swapped the order to be buffers and kernels, then go on with the OpenCL C language, and then continue with images and events. It finishes off with an optimization chapter, image processing algorithms, OpenCL/OpenGL interop and finally a “case-study” chapter. What’s missing are a few performance numbers. Especially when it comes to optimizing code, a result like this makes it 50% faster would be appreciated.

Even though the book is authored by AMD people, they did a fairly good job of keeping everything vendor-neutral. They present different hardware architectures in the book and they don’t focus on AMD specific optimizations. Which is even a bit unfortunate, I would have liked to see one algorithm being picked and explained for instance which optimizations benefit which platform. Just to give the reader an idea, what even why in general, OpenCL is performance portable, some optimizations are still better suited for GPUs and other for CPUs. If you expect some really useful advice on optimizing OpenCL, this book won’t be enough for.

## The code

There’s also example code included. It compiles out-of-the-box on Linux and all samples work fine. On Mac OS X, I didn’t have success building it, and I didn’t try on Windows. There is no sample code for the OpenCL/OpenGL interop chapter. The code uses OpenCL 1.1 functions, so it should work on all platforms.

## The verdict

So let’s sum this up: If you haven’t been using OpenCL yet, and you want a comprehensive introduction which gets you up to speed quickly, this book is for you. It gives you a good idea of the OpenCL API, the programming model and has a few good hands-on examples. You should have some idea of parallel programming though. What you can’t hope for is writing serious OpenCL application right after reading this book, as you’ll need a deeper understanding of the execution model as well as more optimization techniques than this book provides.

That should also make it clear it’s really focused on beginners. If you already know some OpenCL, and hope for some new insights, you can most likely skip this book as it doesn’t contain any advanced OpenCL programming techniques.