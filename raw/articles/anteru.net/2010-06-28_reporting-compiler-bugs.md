---
title: Reporting compiler bugs
url: https://anteru.net/blog/2010/reporting-compiler-bugs
published: '2010-06-28'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Once in a life-time, you run into a compiler bug … well, that used to be the case, before [HLSL](http://msdn.microsoft.com/en-us/library/bb509561(VS.85).aspx)/[GLSL](http://www.opengl.org/documentation/glsl/)/[OpenCL](http://www.khronos.org/opencl/)/[CUDA](http://nvidia.com/cuda)/C++0x whatever started to crop up and require new front and especially code generation back-ends. More often than not, people just accept that there is a bug somewhere and try to work around it, but you should always remember to report it so it can get fixed quickly. In this post, we’ll take a look how to efficiently report bugs in compilers, as it usually requires quite some work to make an useful bug report.

## Verification

A small note of warning: In languages like OpenCL with little compiler development, it’s quite likely you’ll see one bug or two every few weeks. In this cases, it’s also typically easy to verify that it’s an compiler bug (some plain old C doesn’t compile any more, messages like “internal phase error” etc.)

However, if you’re using C/C++, the chances that it’s a problem on your side and not in the compiler are far above 99.9999%, unless you’re making heavy use of a new feature (for instance, lambda function composition in C++ or something like this.) Typically, the mature compilers are practically bug-free, so please verify that it’s indeed a compiler bug. If you’re a programming newcomer reading this, *always assume it’s your fault* and try to find someone senior before reporting a bug in GCC or so (the [OS functions typically aren’t broken as well](http://www.pragprog.com/the-pragmatic-programmer).)

## Repro case

The first and most important thing of every bug report is the repro case. A good repro case should have:

- The
*absolute minimal amount*of code to trigger the bug. - As few dependencies as possible.
- Contains only a single (!) problem. If there are two bugs triggered by one statement (for instance, pointer dereference triggers one bug, and assignment a second), then don’t group them together.

Make sure that it’s really a compiler bug (ideally, you would try with one, better two other compilers.) In OpenCL, I’ve easily hit a few bugs due to code selection (i.e. back-end.) These bugs just require to rephrase the input code to get fixed, for instance:

```
float a = 3; if (b) a -= 1;
```


would trigger an error, while

```
float a = 3; if (b) a = a - 1;
```


works. These are the easy bugs, and the bulk of bugs is in this category. The expression tree gets somehow so complicated, that some phase of the compiler starts to choke on it. In this case, all you need is typically a tiny code snippet without any dependencies.

It’s getting much more complicated if the problem is bad code generation. Lately, we had a problem in our lab with some multi-threaded, SSE optimised application (written in C++.) At some point, it would simply trash a data structure for no good reason, but only if run in release, and compiled with a particular compiler. That’s basically the worst case; in order to check whether it’s a programming error (some memory being overwritten, for instance), we ported the application to Linux so we could check with the memory debugging tools there (ideally, this would have been [valgrind](http://valgrind.org/), but it choked on the SSE4.1 intrisincs, so we had to use [efence](http://linux.die.net/man/3/efence).) This didn’t highlight anything obviously wrong, so we started to disable optimisations until we found the function which caused the problem.

Now it was “just” some looking at assembly, until we found out that the compiler incorrectly assigned registers. However, this was deep in some large function, so it took us another few hours to cut out enough of the code to get a comparatively small repro case. We also made sure to compile and save the generated code, so we could attach it to the bug report; moreover, we found a workaround. In total, we spend half a week to make sure that it’s a compiler bug! In this case, we ended up with:

- Small repro case: A tiny executable, which, when executed, would create an incorrect result.
- Assembly output of the buggy part as well as manually corrected version.
- A usable workaround.

If all of this is in your repro case, you’re ready to go to the next step, bundling it.

## Bundling

So you have a tiny piece of code which clearly triggers a compiler bug; now how to make sure that the guys on the other side can start fixing it right away? Obviously, you need some kind of project, and for some bugs, you might also need some input to trigger it.

If it’s only a single file using standard headers (i.e. supplied from the compiler’s vendor), it’s typically enough to paste the file. It get’s more interesting once you use custom code. For languages with a pre-processor, your best bet is to run the preprocessor and send the generated file. The resulting file will be really huge, so make sure you add comment markers to your code.

For bugs which require some particular input data to trigger an error, I’ve found two methods to be most useful:

- Embedding all data into the binary itself by processing binary data to a string literal.
- Add a tiny binary blob reader, which reads a file and creates a memory buffer out of it. The blob reader is plain C, so there isn’t a bug hidden in there or complicated code to choke on. It’s plain C, as for instance OpenCL is C-based, so it’s easier to provide a C only file with the report instead of writing one with C++.

Armed with this, you can also add all data that was passed on – this is particularly interesting for things like OpenCL, where a compiler bug might not show up on trivial input (i.e. it won’t crash), but it will crash on real-world data. Make sure you grab the inputs as late as possible in this case (for OpenCL, I simply write out the contents of all buffers right before the function call.)

In case your code consists of several files, you now need to create a project file. In my experience, simple Makefiles work best (you can compile them with [nmake](http://msdn.microsoft.com/en-us/library/dd9y37ha.aspx) on Windows.) With Makefiles, there are no doubts about what is going on, and they cause far less problems than for instance Visual Studio solutions. As I noted above, prefer C to C++ if possible, as it removes yet another possible error source (for instance, you might have exceptions enabled or something like this.) Zip the files together using plain old ZIP, and cross your fingers!

## Closing notes

If you ever run into a compiler or runtime bug, you should really take some time to report it. It’ll make your life easier in the long run (you won’t have to consistently work around), and it’ll help other developers as well. I’m constantly amazed how few people actually report bugs; most of the time, it’s just “I’m getting mad with this XYZ crap” instead of trying to improve the situation for everyone.