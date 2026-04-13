---
title: Synchronous Execution and Filesystem Access in Emscripten – Mozilla Hacks -
  the Web developer blog
url: https://hacks.mozilla.org/2015/02/synchronous-execution-and-filesystem-access-in-emscripten/
author: Alon Zakai
published: '2015-02-24'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[Emscripten](http://emscripten.org/) helps port C and C++ code to run on the Web. When doing such porting, we have to work around limitations of the web platform, one of which is that code must be **asynchronous**: you can’t have long-running code on the Web, it must be split up into events, because other important things – rendering, input, etc. – can’t happen while your code is running. But, it is common to have C and C++ code that **is** synchronous! This post will review how Emscripten helps handle this problem, using a variety of methods. We’ll look at preloading a virtual filesystem as well as a recently-added option to execute your compiled code in a special interpreter. We’ll also get the chance to play some Doom!

First, let’s take a more concrete look at the problem. Consider, for example,

```
FILE *f = fopen("data.txt", "rb");
fread(buffer, 100, 1, f);
fclose(f);
```

This C code opens a file and reads from it synchronously. Now, in the browser we don’t have local filesystem access (content is sandboxed, for security), so when reading a file, we might be issuing a remote request to a server, or loading from IndexedDB – both of which are asynchronous! How, then, does anything get ported at all? Let’s go over three approaches to handling this problem.

**1. Preloading to Emscripten’s virtual filesystem**

The first tool Emscripten has is a **virtual in-memory filesystem**, implemented in JavaScript (credit goes to [inolen](https://github.com/inolen/) for most of the code), which can be pre-populated before the program runs. If you know which files will be accessed, you can preload them (using emcc’s * –preload-file* option), and when the code executes, copies of the files are already in memory, ready for synchronous access.

On small to medium amounts of data, this is a simple and useful technique. The compiled code doesn’t know it’s using a virtual filesystem, everything looks normal and synchronous to it. Things just work. However, with large amounts of data, it can be too expensive to preload it all into memory. You might only need each file for a short time – for example, if you load it into a WebGL shader, and then forget about it on the CPU side – but if it’s all preloaded, you have to hold it all in memory at once. Also, the Emscripten virtual filesystem works hard to be as POSIX-compliant as it can, supporting things like permissions, mmap, etc., which add overhead that might be unnecessary in some applications.

How much of a problem this is depends not just on the amount of data you load, but also the browser and the operating system. For example, on a 32-bit browser you are generally limited to 4GB of virtual address space, and fragmentation can be a problem. For these reasons, 64-bit browsers can sometimes succeed in running applications that need a lot of memory while 32-bit browsers fail (or fail some of the time). To some extent you can try to work around memory fragmentation problems by splitting up your data into separate asset bundles, by running Emscripten’s [file packager](http://kripken.github.io/emscripten-site/docs/porting/files/packaging_files.html?#packaging-using-the-file-packager-tool) separately several times, instead of using *–preload-file* once for everything. Each bundle is a combination of JavaScript that you load on your page, and a binary file with the data of all the files you packaged in that asset bundle, so in this way you get multiple smaller files rather than one big one. You can also run the file packager with *–no-heap-copy*, which will keep the downloaded asset bundle data in separate typed arrays instead of copying them into your program’s memory. However, even at best, these things can only help some of the time with memory fragmentation, in an unpredictable manner.

Preloading all the data is therefore not always a viable solution: With large amounts of data, we might not have enough memory, or fragmentation might be a problem. Also, we might not know ahead of time which files we will need. And in general, even if preloading works for a project, we would still like to avoid it so that we can use as little memory as possible, as things generally run faster that way. That’s why we need the 2 other approaches to handling the problem of synchronous code, which we will discuss now.

**2. Refactor code to be asynchronous**

The second approach is to refactor your code to turn synchronous into asynchronous code. Emscripten provides asynchronous APIs you can use for this purpose, for example, the **fread()** in the example above could be replaced with an asynchronous network download ([emscripten_async_wget, emscripten_async_wget_data](http://kripken.github.io/emscripten-site/docs/api_reference/emscripten.h.html#c.emscripten_async_wget)), or an asynchronous access of locally-cached data in IndexedDB ([emscripten_idb_async_load, emscripten_idb_async_store, etc.](http://kripken.github.io/emscripten-site/docs/api_reference/emscripten.h.html#emscripten-asynchronous-indexeddb-api)).

And if you have synchronous code doing something other than filesystem access, for example rendering, Emscripten provides a generic API to do an asynchronous callback ([emscripten_async_call](http://kripken.github.io/emscripten-site/docs/api_reference/emscripten.h.html#c.emscripten_async_call)). For the common case of a main loop which should be called once per frame from the browser’s event loop, Emscripten has a main loop API ([emscripten_set_main_loop](http://kripken.github.io/emscripten-site/docs/api_reference/emscripten.h.html#c.emscripten_set_main_loop), etc.).

Concretely, an **fread()** would be replaced with something like

```
emscripten_async_wget_data("filename.txt", 0, onLoad, onError);
```

where the first parameter is the filename on the remote server, then an optional void* argument (that will be passed to the callbacks), then callbacks on load and on error. The tricky thing is that the code that should execute right after the fread() would need to be in the onLoad callback – that’s where the refactoring comes in. Sometimes this is easy to do, but it might not be.

Refactoring code to be asynchronous is generally the **optimal** thing to do. It makes your application use the APIs that are available on the Web in the way they are intended to be used. However, it does require changes to your project, and may require that the entire thing be designed in an event-friendly manner, which can be difficult if it wasn’t already structured that way. For these reasons, Emscripten has one more approach that can help you here.

**3. The Emterpreter: Run synchronous code asynchronously, automatically**

The ** Emterpreter** is a fairly new option in Emscripten that was initially developed for

[startup-time reasons](https://blog.mozilla.org/research/2015/02/23/the-emterpreter-run-code-before-it-can-be-parsed/). It compiles your code into a

**binary bytecode**, and ships it with a little

**interpreter**(written in JavaScript, of course), in which the code can be executed. Code running in an interpreter is “manually executed” by us, so we can control it more easily than normal JavaScript, and we can add the capability to pause and resume, which is what we need to turn synchronous code into asynchronous code.

**Emterpreter-Async**, the Emterpreter plus support for running synchronous code asynchronously, was therefore fairly easy to add on top of the existing Emterpreter option.

The idea of an automatic transformation from synchronous to asynchronous code was experimented with by [Lu Wang](https://github.com/coolwanglu) during his internship over the summer of 2014: the [Asyncify](https://github.com/kripken/emscripten/wiki/Asyncify) option. Asyncify rewrites code at the LLVM level to support pausing and resuming execution: you write synchronous code, and the compiler rewrites it to run asynchronously. Returning to the fread() example from before, Asyncify would automatically break up the function around that call, and put the code after the call into a callback function – basically, it does what we suggested you do manually in the “*Refactor code to be asynchronous*” section above. This can work surprisingly well: For example, [Lu ported vim](http://coolwanglu.github.io/vim.js/experimental/vim.html), a large application with a lot of synchronous code in it, to the Web. And it works! However, we hit significant limitations in terms of increased code size because of how Asyncify restructures your code.

The Emterpreter’s async support avoids the code size problem that Asyncify hit because it is an interpreter running bytecode: The bytecode is always the same size (in fact, smaller than asm.js), and we can manipulate control flow on it manually in the interpreter, without instrumenting the code.

Of course, running in an interpreter can be quite slow, and [this one is no exception](https://blog.mozilla.org/research/2015/02/23/the-emterpreter-run-code-before-it-can-be-parsed/) – speed can be significantly slower than usual. Therefore, this is not a mode in which you want to run *most* of your code. But, the Emterpreter gives you the option to decide *which parts* of your codebase are interpreted and which are not, and this is crucial to productive use of this option, as we will now see.

Let’s make this concrete by showing the option in practice on the [Doom](http://en.wikipedia.org/wiki/Doom_%281993_video_game%29) codebase. Here is a ** normal port of Doom** (specifically

[Boon](https://github.com/kripken/boon):, the Doom code with

[Freedoom](http://freedoom.github.io/index.html)open art assets). That link is just Doom compiled with Emscripten,

**not**using synchronous code or the Emterpreter at all, yet. It looks like the game works in that link – do we even need anything else? It turns out that we need synchronous execution in two places in Doom: First, for filesystem access. Since Doom is from 1993, the size of the game is quite small compared to today’s hardware. We can preload all of the data files and things just work (that’s what happens in that link). So far, so good!

The second problem, though, is trickier: For the most part Doom renders a whole frame in each iteration of the main loop (which we can call from the browser’s event loop one at a time), however it also does some visual effects using synchronous code. Those effects are not shown in that first link – Doom fans may have noticed something was missing! :)

Here is ** a build with the Emterpreter-Async option enabled**. This runs the

**entire application**as bytecode in the interpreter, and it’s quite slow, as expected. Ignoring speed for now, you might notice that when you start a game, there is a “

**wipe**” effect right before you begin to play, that wasn’t in the previous build. It looks kind of like a descending wave. Here’s a screenshot:

That effect is ![22297](../../assets/870ea7241db6e32e.png)


[written synchronously](https://github.com/kripken/boon/blob/emterpreter-sync/src/d_main.c#L171)(note the screen update and sleep). The result is that in the initial port of the game, the wipe effect code is executed, but the JavaScript frame doesn’t end yet so no rendering happens. For this reason, we don’t see the wipe in the first build! But we

**do**see it in the second, because we enabled the Emterpreter-Async option, which supports synchronous code.

The second build is *slow*. What can we do? The Emterpreter lets you decide which code runs normally, as full-speed asm.js, and which is interpreted. *We want to run only what we absolutely must run in the interpreter*, and everything else in asm.js, so things are as fast as possible. **For purposes of synchronous code, the code we must interpret is anything that is on the stack during a synchronous operation.** To understand what that means, imagine that the callstack currently looks like this:

```
main() => D_DoomMain() => D_Display() => D_Wipe() => I_uSleep()
```

and the last of those does a call to sleep. Then the Emterpreter turns this synchronous operation into an asynchronous operation by saving where execution is right now in the current method (this is easy using the interpreter’s [program counter](http://en.wikipedia.org/wiki/Program_counter), as well as since all local variables are already stored in a stack on a global typed array), then doing the same for the methods calling it, and while doing so to exit them all (which is also easy, each call to the interpreter is a call to a JavaScript method, which just returns). After that, we can do a setTimeout() for when we want to resume. So far, we have saved what we were doing, stopped, set an asynchronous callback for some time in the future, and we can then return control to the browser’s event loop, so it can render and so forth.

When the asynchronous callback fires sometime later, we reverse the first part of the process: We call into the interpreter for main(), jump to the right position in it, then continue to do so for the rest of the call stack – basically, recreating the call stack exactly as it was before. At this point we can resume execution in the interpreter, and it is as if we never left: **synchronous execution has been turned asynchronous.**

That means that if D_Wipe() does a synchronous operation, it must be interpreted, **and anything that can call it as well**, and so forth, recursively. The good news is that often such code tends to be small and doesn’t need to be fast: it’s typically event-loop handling code, and not code actually doing hard work. Talking abstractly, it’s common to see callstacks like these in games:

```
main() => MainLoop() => RunTasks() => PhysicsTask() => HardWork()
```

and

```
main() => MainLoop() => RunTasks() => IOTask() => LoadFile()
```

Assuming LoadFile() does a synchronous read of a file, it must be interpreted. As we mentioned above, this means everything that can be on the stack together with it must also be interpreted: main(), MainLoop(), RunTasks(), and IOTask() – **but not** any of the physics methods. In other words, if you never have physics and networking on the stack at the **same** time (a network event calling something that ends up calling physics, or a physics event that somehow decides to do a network request all of a sudden), then you can run networking in the interpreter, and physics at full speed. This is the case in Doom, and also other real-world codebases (and even in ones that are tricky, as in [Em-DOSBox](https://github.com/dreamlayers/em-dosbox/) which has recursion in a crucial method,[ sometimes a solution can be found](http://dreamlayers.blogspot.ca/2015/02/fixing-hard-problem-in-em-dosbox-using.html)).

** Here is a build of Doom with that optimization enabled** – it only interprets what we absolutely must interpret. It runs at about the same speed as the original, optimized build

**and**it also has the wipe effect fully working. Also, the wipe effect is nice and smooth, which it wasn’t before: even though the wipe method itself must be interpreted – because it calls sleep() – the rendering code it calls in between sleeping can run at full speed, as that rendering code is never on the stack

*while*sleeping!

To have synchronous code working properly while the project stays at full speed, it is crucial to run exactly the right methods in the interpreter. [Here is a list of the methods we need in Doom](https://github.com/kripken/boon/blob/emterpreter-sync/doit.sh#L11) (in the ‘whitelist’ option there) – only 15 out of 1,425, or ~1%. To help you find a list for your project, the Emterpreter provides both static and dynamic tools, see [the docs](https://github.com/kripken/emscripten/wiki/Emterpreter#deciding-on-which-methods-to-emterpret-for-async) for more details.

**Conclusion**

Emscripten is often used to port code that contains synchronous portions, but long-running synchronous code is not possible on the Web. As described in this article, there are three approaches to handling that situation:

- If the synchronous code just does file access, then
**preloading everything**is a simple solution. - However, if there is a great amount of data, or you don’t know what you’ll need ahead of time, this might not work well. Another option is to
**refactor your code to be asynchronous**. - If that isn’t an option either, perhaps because the refactoring is too extensive, then Emscripten now offers the
**Emterpreter**option to run parts of your codebase in an interpreter which*does*support synchronous execution.

Together, these approaches provide a range of options for handling synchronous code, and in particular the common case of synchronous filesystem access.

## About Alon Zakai

Alon is on the research team at Mozilla, where he works primarily on Emscripten, a compiler from C and C++ to JavaScript. Alon founded the Emscripten project in 2010.

## 2 comments

voracityFebruary 26th, 2015 at 19:29Alon ZakaiFebruary 27th, 2015 at 10:14