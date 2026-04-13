---
title: 'Build systems: CMake'
url: https://anteru.net/blog/2017/build-systems-cmake
published: '2017-06-12'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Welcome to the last build system we’re going to look at in this cycle! As hinted last week, there’s one problem left: How can we find binaries and other dependencies already present in the host environment? This is a tricky question, as we have to solve two problems at the same time: First, we need to be able to find things in a cross-platform manner, which means we need things like “invoke a binary” to query version numbers for instance. Second, we need a rather precise search to ensure that our build system has a good view of the dependency we’re about to integrate. If it’s just a binary, this is usually not a problem, but a C++ library might require special compile definitions, a link library, an include path and more to be set on the *target* project.

Fortunately, I’ve got just the build system for you to demonstrate this – CMake. CMake is in many ways the union of various build systems we’ve seen so far. It’s a build system generator just like [Premake](https://anteru.net/blog/2017/build-systems-premake). It comes with its own scripting language, just like [Bazel](https://anteru.net/blog/2017/build-systems-bazel). It’s called “as-if” it’s a library just like [Scons](https://anteru.net/blog/2017/build-systems-scons). And of top of all of this, it provides two new concepts: Find modules and imported targets.

## Find modules

One of the two big features of CMake are find modules, which allow you to find an existing library or binary with a simple command. Instead of trying to hard-code paths to the Python interpreter, we can just call `find_package(PythonInterp 3.5 REQUIRED)`

and CMake will handle everything. After the command has executed, CMake will populate a few variables so we can consume Python directly. In the case of the module above, `PYTHON_EXECUTABLE`

will point to the Python binary, and we can immediately invoke it in our generator step.

The find modules don’t end with binaries though. You can also search for libraries, and even search for library components. This is super helpful when dealing with large libraries like Boost or Qt, which are very large and require searching up many paths. The search method is just the same, but there are two ways in which the results can be returned. The “old” way is to populate a couple of variables, which are then manually added to your project. The “new” way is to provide an imported target, which handles all of the required settings in a transparent way.

## Imported targets

An imported target in CMake is nothing else than a “normal” target, but assembled manually, instead of being generated as part of the current CMake build. Let me elaborate a bit on this. In CMake, if you add a new target like using for example `add_library`

, it produces a named object you can reference elsewhere – just like we saw it in [Waf](https://anteru.net/blog/2017/build-systems-waf). CMake allows to specify settings on a target which will affect the consumers. For example, you can specify an include directory which is automatically added to everyone linking against this target.

An imported target is now a target which is imported from elsewhere, but internally behaves “as if” it was a normal CMake target. That is, it gets all the goodness of injecting include directories, compile settings and more we mentioned above. There are two ways to get an imported target. The simple one is to let CMake handle this: If your project is set up correctly for installation, CMake can generate a project description which can be imported directly. This is somewhat similar to how [Bazel](https://anteru.net/blog/2017/build-systems-bazel) handles large builds, except that for CMake, you bundle up the project output with the build definition.

The other way to create an imported target is to assemble it by hand, which is what most of the modern find modules do. What happens is that an imported target is created out of thin air, and the various components are then specified manually. If you’re curious about the details, the [add_library](https://cmake.org/cmake/help/latest/command/add_library.html) documentation and the [sample FindModule](https://cmake.org/cmake/help/latest/manual/cmake-developer.7.html#a-sample-find-module) got you covered!

## Sample project

Let’s get started with our sample project then, and the way we generate our lookup table:

```
find_package(PythonInterp 3.5 REQUIRED)
add_custom_command(
OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/lookup_table.cpp
COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/tablegen.py > ${CMAKE_CURRENT_BINARY_DIR}/lookup_table.cpp
DEPENDS tablegen.py)
```


In the first line, we let CMake find the Python interpreter. The next command registers a custom command which will be executed to produce the `lookup_table.cpp`

file. Note that the file needs to be consumed somewhere for this to make sense, otherwise it’s just a leaf in the build graph with no dependency on it. For a custom command, we can specify the dependencies manually, as CMake doesn’t try to run them in a sandbox and log I/O access or anything like that.

Next, we’ll use that generated file in our static library definition:

```
add_library(statlib STATIC
StaticLibrarySource.cpp ${CMAKE_CURRENT_BINARY_DIR}/lookup_table.cpp)
```


We still need to set up the include directories. For this project, we only have one include directory – the current directory – but targets consuming the static library need to use that include directory as well. In CMake, that’s called a `PUBLIC`

include directory:

```
target_include_directories(statlib
PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
```


We’re nearly done, there’s only one bit left, which is specifying the `-fPIC`

flag. Unfortunately, CMake doesn’t handle this automatically, nor does it warn when we try to consume a static library without it enabled. On the upside, CMake provides a *compiler agnostic* way of specifying it:

```
set_property (TARGET statlib PROPERTY POSITION_INDEPENDENT_CODE TRUE)
```


With that, our project is complete. In the dynamic library, we have a case where we need to set a compile definition but only for the library. This is a `PRIVATE`

setting – just as we had `PUBLIC`

above:

```
target_compile_definitions(dynlib
PRIVATE BUILD_DYNAMIC_LIBRARY=1)
```


This way, we can have very fine-grained visibility of the settings, though we can’t restrict project visibility as we could in [Bazel](https://anteru.net/blog/2017/build-systems-bazel). As usual, you can find the whole project in the [sample repository](https://github.com/Anteru/build-systems/tree/master/cmake).

Before we wrap up, some small remarks regarding the various features. The module finding is something which is aimed at Linux environments, which provide all libraries in standard locations. On Windows, the find experience for libraries is such that you typically have to specify the path to the library. It’s not a big problem in practice, as you can specify the various paths on the first invocation of CMake.

Another thing to keep in mind that unlike Premake, which generates portable build files using relative paths to the source, CMake bakes in the full directories. Your build description is yet another build artifact and should be treated as such, so it’s not a tool you can use to generate Visual Studio project files. The developer must have CMake installed, and there’s no easy way to package up CMake into a single executable for instance like there is with Premake.

With this, we’re nearly at the end of the series! For the last blog post, I’d like to gather some information about what build systems *you* use, and to this end, I’ve set up [a survey](https://goo.gl/forms/rkdS77pfKcWNnh2d2). It should only take a minute or so to fill it out. Thanks for your help and see you again next week for the grand finale!