---
title: Porting to Emscripten – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/11/porting-to-emscripten/
author: Turo Lamminen
published: '2014-11-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Emscripten is an open-source compiler that compiles C/C++ source code into the highly optimizable asm.js subset of JavaScript. This enables running programs originally written for desktop environments in a web browser.

Porting your game to Emscripten offers several benefits. Most importantly it enables reaching a far wider potential user base. Emscripten games work on any modern web browser. There is no need for installers or setups – the user just opens a web page. Local storage of game data in browser cache means the game only needs to be re-downloaded after updates. If you implement a cloud based user data storage system users can continue their gameplay seamlessly on any computer with a browser.

More info is available in:

While Emscripten support for portable C/C++ code is very good there are some things that need to be taken into consideration. We will take a look at those in this article.

## Part 1: Preparation

Is porting my game to Emscripten even feasible? If it is, how easy will it be? First consider the following restrictions imposed by Emscripten:

- No closed-source third-party libraries
- No threads

Then, already having some of the following:

- Using SDL2 and OpenGL ES 2.0 for graphics
- Using SDL2 or OpenAL for audio
- Existing multiplatform support

will make the porting task easier. We’ll next look into each of these points more closely.

### First things to check

If you’re using any third-party libraries for which you don’t have the source code you’re pretty much out of luck. You’ll have to rewrite your code not to use them.

Heavy use of threads is also going to be a problem since Emscripten doesn’t currently support them. There are web workers but they’re not the same thing as threads on other platforms since there’s no shared memory. So you’ll have to disable multithreading.

### SDL2

Before even touching Emscripten there are things you can do in your normal development environment. First of all you should use SDL2. SDL is a library which takes care of platform-specific things like creating windows and handling input. An incomplete port of SDL 1.3 ships with Emscripten and there’s [a port of full SDL2](https://github.com/Daft-Freak/SDL-emscripten) in the works. It will be merged to upstream soon.

*Space combat in FTL.*

### OpenGL ES 2.0

Second thing is to use OpenGL ES 2.0. If your game is using the SDL2 render interface this has already been done for you. If you use Direct3D you’ll first have to create an OpenGL version of your game. This is why multiplatform support from the beginning is such a good idea.

Once you have a desktop OpenGL version you then need to create an OpenGL ES version. ES is a subset of full OpenGL where some features are not available and there are some additional restrictions. At least the NVidia driver and probably also AMD support creating ES contexts on desktop. This has the advantage that you can use your existing environment and debugging tools.

You should avoid the deprecated OpenGL fixed-function pipeline if possible. While Emscripten has some support for this it might not work very well.

There are certain problems you can run into at this stage. First one is lack of extension support. Shaders might also need rewriting for Emscripten. If you are using NVidia add #version line to trigger stricter shader validation.

GLSL ES requires precision qualifiers for floating-point and integer variables. NVidia accepts these on desktop but most other GL implementations not, so you might end up with two different sets of shaders.

OpenGL entry point names are different between GL ES and desktop. GL ES does not require a loader such as GLEW but you still might have to check GL extensions manually if you are using any. Also note that OpenGL ES on desktop is more lenient than WebGL. For example WebGL is more strict about glTexImage parameters and glTexParameter sampling modes.

Multiple render targets might not be supported on GL ES. If you are using a stencil buffer you must also have a depth buffer. You must use vertex buffer objects, not user-mode arrays. Also you cannot mix index and vertex buffers into the same buffer object.

For audio you should use SDL2 or OpenAL. One potential issue is that the Emscripten OpenAL implementation might require more and larger sound buffers than desktop to avoid choppy sounds.

### Multiplatform support

It’s good if your project has multiplatform support, especially for mobile platforms (Android, iOS). There are two reasons for this. First, WebGL is essentially OpenGL ES instead of desktop OpenGL so most of your OpenGL work is already done. Second, since mobile platforms use ARM architecture most of the processor-specific problems have already been fixed. Particularly important is memory alignment since Emscripten doesn’t support unaligned loads from memory.

After you have your OpenGL sorted out (or even concurrently with it if you have multiple people) you should port your game to Linux and/or OS X. Again there are several reasons. First one is that Emscripten is based on LLVM and Clang. If your code was written and tested with MSVC it probably contains non standard constructs which MSVC will accept but other compilers won’t. Also different optimizer might expose bugs which will be much easier to debug on desktop than on a browser.

*FTL Emscripten version main menu. Notice the missing “Quit” button. The UI is similar to that of the iPad version.*

A good overview of porting a Windows game to Linux is provided in [Ryan Gordon’s Steam Dev Days talk](https://www.youtube.com/watch?v=Sd8ie5R4CVE).

If you are using Windows you could also compile with MinGW.

### Useful debugging tools

#### UBSan

The second reason for porting to Linux is to gain access to several useful tools. First among these is undefined behavior sanitizer (UBSan). It’s a Clang compiler feature which adds runtime checks to catch C/C++ undefined behavior in your code. Most useful of these is the unaligned load check. C/C++ standard specifies that when accessing a pointer it must be properly aligned. Unfortunately x86-based processors will perform unaligned loads so most existing code has not been checked for this. ARM-based processors will usually crash your program when this happens. This is why a mobile port is good. On Emscripten an unaligned load will not crash but instead silently give you incorrect results.

UBSan is also available in GCC starting with 4.9 but unfortunately the unaligned load sanitizer is only included in the upcoming 5.0 release.

#### AddressSanitizer

Second useful tool in Clang (and GCC) is AddressSanitizer. This is a runtime checker which validates your memory accesses. Reading or writing outside allocated buffers can lead to crashes on any platform but the problem is somewhat worse on Emscripten. Native binaries have a large address space which contains lots of empty space. Invalid read, especially one that is only slightly off, might hit a valid address and so not crash immediately or at all. On Emscripten the address space is much “denser” so any invalid access is likely to hit something critical or even be outside the allocated address space entirely. This will trigger an unspectacular crash and might be very hard to debug.

#### Valgrind

The third tool is Valgrind. It is a runtime tool which runs uninstrumented binaries and checks them for various properties. For our purposes the most useful are memcheck and massif. Memcheck is a memory validator like AddressSanitizer but it catches a slightly different set of problems. It can also be used to pinpoint memory leaks. Massif is a memory profiler which can answer the question “why am I using so much memory?” This is useful since Emscripten is also a much more memory-constrained platform than desktop or even mobile and has no built in tools for memory profiling.

Valgrind also has some other checkers like DRD and Helgrind which check for multithreading issues but since Emscripten doesn’t support threads we won’t discuss them here. They are very useful though so if you do multithreading on desktop you really should be using them.

Valgrind is not available on Windows and probably will never be. That alone should be a reason to port your games to other platforms.

### Third-party libraries

Most games use a number of third-party libraries. Hopefully you’ve already gotten rid of any closed-source ones. But even open-source ones are usually shipped as already-compiled libraries. Most of these are not readily available on Emscripten so you will have to compile them yourself. Also the Emscripten object format is based on LLVM bytecode which is not guaranteed to be stable. Any precompiled libraries might no longer work in future versions of Emscripten.

While Emscripten has some support for dynamic linking it is not complete or well supported and should be avoided.

The best way around these issues is to build your libraries as part of your standard build process and statically link them. While bundling up your libraries to archives and including those in link step works you might run into unexpected problems. Also changing your compiler options becomes easier if all sources are part of your build system.

Once all that is done you should actually try to compile with Emscripten. If you’re using MS Visual Studio 2010 there’s an integration module which you can try. If you’re using cmake Emscripten ships with a wrapper (emcmake) which should automatically configure your build.

If you’re using some other build system it’s up to you to set it up. Generally `CC=emcc`

and `CXX=em++`

should do the trick. You might also have to remove platform-specific options like SSE and such.

## Part 2: Emscripten itself

So now it links but when you load it up in your browser it just hangs and after a while the browser will tell you the script has hung and kill it.

What went wrong?

On desktop games have an event loop which will poll input, simulate state and draw the scene and run until terminated. On a browser there is instead a callback which does these things and is called by the browser. So to get your game to work you have to refactor your loop to a callback. In Emscripten this is set with the function [emscripten_set_main_loop](http://kripken.github.io/emscripten-site/docs/api_reference/emscripten.h.html#c.emscripten_set_main_loop). Fortunately in most cases this is pretty simple. The easiest way is to refactor the body of your loop to a helper function and then in your desktop version call it in a loop and in the browser set it as your callback. Or if you’re using C++11 you can use a lambda and store that in `std::function`

. Then you can add a small wrapper which calls that.

Problems appear if you have multiple separate loops, for example loading screens. In that case you need to either refactor them into a single loop or call them one after another, setting a new one and canceling the previous one with `emscripten_cancel_main_loop`

. Both of these are pretty complex and depend heavily on your code.

So, now the game runs but you get a bunch of error messages that your assets can’t be found. The next step is to add your assets to the package. The simple way is to preload them. Adding the switch `--preload-file <filename>`

to link flags will cause Emscripten to add the specified files to a .data file which will then be preloaded before main is called. These files can then be accessed with standard C/C++ IO calls. Emscripten will take care of the necessary magic.

However this approach becomes problematic when you have lots of assets. The whole package needs to be loaded before the program starts which can lead to excessive loading times. To fix this you can stream in some assets like music or video.

If you already have async loading in your desktop code you can reuse that. Emscripten has the function `emscripten_async_wget_data`

for loading data asynchronously. One difference to keep in mind is that Emscripten async calls only know asset size after loading has completed whereas desktop generally knows if after the file has been opened. For optimal results you should refactor your code to something like “load this file, then here’s an operation to do after you have it”. C++11 lambdas can be useful here. In any case you really should have matching code on the desktop version because debugging is so much easier there.

You should add a call at the end of your main loop which handles async loads. You should not load too much stuff asynchronously as it can be slow, especially if you’re loading multiple small files.

So now it runs for a while but crashes with a message about exceeded memory limit. Since Emscripten emulates memory with JavaScript arrays the size of those arrays is crucial. By default they are pretty small and can’t grow. You can enable growing them by linking with `-s ALLOW_MEMORY_GROWTH=1`

but this is slow and might disable asm.js optimizations. It’s mostly useful in the debugging phase. For final release you should find out a memory limit that works and use `-s TOTAL_MEMORY=<number>`

.

As described above, Emscripten doesn’t have a memory profiler. Use Valgrind massif tool on Linux to find out where the memory is spent.

If your game is still crashing you can try using JavaScript debugger and source maps but they don’t necessarily work very well. This is why sanitizers are important. `printf`

or other logging is a good way to debug too. Also `-s SAFE_HEAP=1`

in link stage can find some memory bugs.

Osmos test version on Emscripten test html page.

### Saves and preferences

Saving stuff is not as simple as on desktop. The first thing you should do is find all the places where you’re saving or loading user-generated data. All of it should be in one place or go through one wrapper. If it doesn’t you should refactor it on desktop before continuing.

The simplest thing is to set up a local storage. Emscripten already has the necessary code to do it and emulate standard C-like filesystem interface so you don’t have to change anything.

You should add something like this to either the `preRun`

in html or first thing in your main:

```
FS.createFolder('/', 'user_data', true, true)
FS.mount(IDBFS, {}, '/user_data');
FS.syncfs(true, function(err) {
if(err) console.log('ERROR!', err);
console.log('finished syncing..');
}
```

Then after you’ve written a file you need to tell the browser to sync it. Add a new method which contains something like this:

```
static void userdata_sync()
{
EM_ASM(
FS.syncfs(function(error) {
if (error) {
console.log("Error while syncing", error);
}
});
);
}
```

and call it after closing the file.

While this works it has the problem that the files are stored locally. For desktop games this is not a problem since users understand that saves are stored on their computer. For web-based games the users expect their saves to be there on all computers. For the Mozilla Bundle, Humble Bundle built a `CLOUDFS`

library which works just like Emscripten’s `IDBFS`

and has a pluggable backend. You need to build your own using emscripten `GET`

and `POST`

APIs.

Osmos demo at the Humble Mozilla Bundle page.

### Making it fast

So now your game runs but not very fast. How to make it faster?

On Firefox the first thing to check is that asm.js is enabled. Open web console and look for message “Successfully compiled asm.js”. If it’s not there the error message should tell you what’s going wrong.

The next thing to check is your optimization level. Emscripten requires proper `-O`

option both when compiling and linking. It’s easy to forget `-O`

from link stage since desktop doesn’t usually require it. Test the different optimization levels and read the Emscripten documentation about other build flags. In particular `OUTLINING_LIMIT`

and `PRECISE_F32`

might affect code speed.

You can also enable link-time optimization by adding `--llvm-lto <n>`

option. But beware that this has known bugs which might cause incorrect code generation and will only be fixed when Emscripten is upgraded to a newer LLVM sometime in the future. You might also run into bugs in the normal optimizer since Emscripten is still somewhat work-in-progress. So test your code carefully and if you run into any bugs report them to Emscripten developers.

One strange feature of Emscripten is that any preloaded resources will be parsed by the browser. We usually don’t want this since we’re not using the browser to display them. Disable this by adding the following code as `--pre-js`

:

```
var Module;
if (!Module) Module = (typeof Module !== 'undefined' ? Module : null) || {};
// Disable image and audio decoding
Module.noImageDecoding = true;
Module.noAudioDecoding = true;
```

Next thing: don’t guess where the time is being spent, profile! Compile your code with `--profiling`

option (both compile and link stage) so the compiler will emit named symbols. Then use the browser’s built-in JavaScript profiler to see which parts are slow. Beware that some versions of Firefox can’t profile asm.js code so you will either have to upgrade your browser or temporarily disable asm.js by manually removing `use asm`

-statement from the generated JavaScript. You should also profile with both Firefox and Chrome since they have different performance characteristics and their profilers work slightly differently. In particular Firefox might not account for slow OpenGL functions.

Things like `glGetError`

and `glCheckFramebuffer`

which are slow on desktop can be catastrophic in a browser. Also calling `glBufferData`

or `glBufferSubData`

too many times can be very slow. You should refactor your code to avoid them or do as much with one call as possible.

Another thing to note is that scripting languages used by your game can be very slow. There’s really no easy way around this one. If your language provides profiling facilities you can use those to try to speed it up. The other option is to replace your scripts with native code which will get compiled to asm.js.

If you’re doing physics simulation or something else that can take advantage of `SSE`

optimizations you should be aware that currently asm.js doesn’t support it but it should be coming sometime soon.

To save some space on the final build you should also go through your code and third party libraries and disable all features you don’t actually use. In particular libraries like SDL2 and freetype contain lots of stuff which most programs don’t use. Check the libraries’ documentation on how to disable unused features. Emscripten doesn’t currently have a way to find out which parts of code are the largest but if you have a Linux build (again, you should) you can use

```
nm -S --size-sort game.bin
```

to see this. Just be aware that what’s large on Emscripten and what’s large on native might not be the same thing. In general they should agree pretty well.

Sweeping autumn leaves in Dustforce.

## In conclusion

To sum up, porting an existing game to Emscripten consists of removing any closed-source third party libraries and threading, using SDL2 for window management and input, OpenGL ES for graphics, and OpenAL or SDL2 for audio. You should also first port your game to other platforms, such as OS X and mobile, but at least for Linux. This makes finding potential issues easier and gives access to several useful debugging tools. The Emscripten port itself minimally requires changes to main loop, asset file handling, and user data storage. Also you need to pay special attention to optimizing your code to run in a browser.

## About
[
Turo Lamminen ](http://www.alternativegames.net/)

Programmer at Alternative Games game porting company with special focus on the Linux environment.

## About
[
Tuomas Närväinen ](http://www.alternativegames.net)

Works as a programmer at Alternative Games porting company with primary responsibility of the OS X and Windows platforms.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 2 comments

nemoNovember 4th, 2014 at 10:31Alon ZakaiNovember 4th, 2014 at 12:48