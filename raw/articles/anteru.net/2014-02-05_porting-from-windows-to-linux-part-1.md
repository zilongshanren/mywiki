---
title: Porting from Windows to Linux, part 1
url: https://anteru.net/blog/2014/porting-from-windows-to-linux-part-1
published: '2014-02-05'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Hi and welcome to a blog series about how to port graphics applications from Windows to Linux. The series will have three parts: Today, in the first part, we’ll be looking at prerequisites for porting. These are things you can do any time to facilitate porting later on, while still working on Windows exclusively. In the second part, the actual porting work will be done, and in the last part, I’ll talk a bit about the finishing touches, rough edges, and how to keep everything working. All of this is based on my experience with porting my research framework; which is a medium-sized project (~ 180 kLoC) that supports Linux, Windows and Mac OS X.

However, before we start, let’s assess the state of the project before the porting begins. For this series, I assume you have a Visual Studio based solution written in C++, with Direct3D being used for graphics. Your primary development environment is Visual Studio, and you haven’t developed for Linux before. You’re now at the point where you want to add Linux support to your application while keeping Windows intact – so we’re not talking about a rushed conversion from Windows to Linux, but of a new port of your application which will be maintained and supported alongside the Windows version.

## Prerequisites

Let’s start by sorting out the obvious stuff: Your need a *source control solution* which will work on Linux. If your project is stored in [TFS](http://en.wikipedia.org/wiki/Team_Foundation_Server), now is the time to export everything to your favourite portable source control. If you are not sure what to choose, take [Mercurial](http://mercurial.selenic.com/), which comes with a [nice UI](http://tortoisehg.bitbucket.org/) for all platforms.

Next, check all your *dependencies*. If you rely on [WIC](http://en.wikipedia.org/wiki/Windows_Imaging_Component) for image loading, you’ll have to find a portable solution first. In my experience, it’s usually easier to have the same code running on Windows and Linux later on than having a dedicated path for each OS. In my project, I wrapped the low-level libraries like [libpng](http://www.libpng.org/pub/png/libpng.html) or [libjpg](http://www.ijg.org/) directly instead of using a larger image library.

Now is also the time to *write tests*. You’ll need to be able to quickly verify that everything is working again. If you haven’t written any automated tests yet, this is the moment to start. You’ll mostly need functional tests, for instance, for disk I/O, so focus on those first. I say mostly functional tests, as unit tests tend to be OS agnostic. In my framework, unit tests cover low-level OS facilities like threads and memory allocators, while everything else, including graphics, is covered by functional tests.

For testing, I can highly recommend [Google Test](http://code.google.com/p/googletest/). It’s not designed for functional tests right away, but it’s very easy to write a wrapper around a Google Test enabled project for functional testing. My wrapper is written in Python and sets up a new folder for each functional test, executes each test in a new process and gathers all results.

Finally, if you have any *build tools*, make sure that those are portable now. I used to write them in C# when it was really new, but since a few years, I use only [Python](https://python.org) for build tools. Python code tends to be easy to maintain and it requires no build process whatsoever, making it ideally suited for build system infrastructure. Which brings us to the most important issue, the build system.

## Build system

If you are using Visual Studio (or [MSBuild](http://en.wikipedia.org/wiki/MSBuild) from the command line), stop right now and start porting it to a *portable build system*. While in theory, MSBuild is portable to Linux using [xbuild](http://www.mono-project.com/Microsoft.Build), in practice, you’ll still want to have a build system which is developed on all three platforms and used for large code bases. I have tried a bunch of them and finally settled with [CMake](http://www.cmake.org). It uses an arcane scripting language, but it works, and it works reliably on Windows, Linux, and Mac OS X.

Porting from Visual Studio to CMake might seem like a huge effort at first, but it’ll make the transition to Linux much easier later on. The good thing about CMake is that it works perfectly on Windows and it produces Visual Studio project files, so your existing Windows developer experience remains the same. The only difference is that adding new source files now requires you to edit a text file instead of using the IDE directly, but that’s about it.

While writing your CMake files, here’s a few things you should double-check:

- Are your path names case-sensitive? Windows doesn’t care, but on Linux, your include directory won’t be found if you mess up paths.
- Are you setting compiler flags directly? Check if CMake already sets them for you before adding a huge list of compiler flags manually.
- Are your dependencies correctly set up? With Visual Studio, it’s possible to not define all dependencies correctly and still get a correct build; while other build tools will choke on it. Use the graph output of CMake to visualize the dependencies and double check both the build order, and the individual project dependencies.

With CMake, you should also take advantage of the [“Find”](http://cmake.org/cmake/help/v2.8.12/cmake.html#section_StandardCMakeModules) mechanism for dependencies. On Linux, nearly all dependencies are available as system libraries, serviced by the package manager, so it definitely makes sense to link against the system version of a dependency if it is recent enough.

The end result of this step should be exactly the same binaries as before, but using CMake as the build system instead of storing the solutions directly in source control. Once this is done, we can start looking at the code.

## Clean code

Did you ever `#include`

system headers like `<windows.h>`

in your code? Use system types like `DWORD`

? Now is the time to clean up and to isolate these things. You want to achieve two goals here:

- Remove system includes from headers as much as possible.
- Remove any Visual C++ specific code.

System headers should be only included in source files, if possible. If not, you should *isolate* the classes/functions and provide generic wrappers around them. For instance, if you have a class for handling files, you can either use the [PIMPL](http://c2.com/cgi/wiki?PimplIdiom) idiom or just derive a Windows-specific class from it. The second solution is usually simpler if your file class is already derived from somewhere (a generic stream interface, for instance.) Even if not, we’re wrapping an extremely slow operating system function here (file reads will typically hit the disk), so the cost of a virtual function call won’t matter in practice.

To get rid of Visual C++ specific code, *turn on all warnings *and treat them as errors. There are a bunch of bogus warnings you can disable ([I’ve blogged about them previously](https://anteru.net/blog/2007/01/10/136/)), but everything else should get fixed now. In particular, you don’t want any Visual C++ specific extensions enabled in headers. The reason why you want all warnings to be fixed is that on Linux, you’ll be getting hundreds of compile errors and warnings at first, and the less these are swamped by issues that are also present on Windows, the better.

While cleaning up, you should pay special attention to *integer sizes*. Windows uses 32-bit `long`

s in 64-bit mode, Linux defaults to 64-bit `long`

s. To avoid any confusion, I simply use 64-bit integers when it comes to memory sizes.

The better you clean up your code, the less work you’ll have to spend later during porting. The goal here should be to get everything to build on Windows, with platform specific files identified and isolated.

So much for today! Next week, we’ll look at how to get rid of Direct3D and how to start bringing up the code base on Linux. Stay tuned!