---
title: 'Build systems: FASTbuild'
url: https://anteru.net/blog/2017/build-systems-fastbuild
published: '2017-05-15'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

The last weeks we’ve been steadily increasing the complexity of our build tools – from bare-bones [Make](https://anteru.net/blog/2017/build-systems-make) to [WAF](https://anteru.net/blog/2017/build-systems-waf) which had high-level concepts like include directory export. This week, we’re going back to the roots again with [FASTBuild](http://fastbuild.org/docs/home.html) – you might have seen it [Ubisoft’s presentation at CppCon 2014](https://www.youtube.com/watch?v=qYN6eduU06s).

## Overview

FASTBuild is in many ways similar to Make. It’s a very focused tool for low-level execution, without much fluff on top of it. The main difference between FASTBuild and the other tools we’ve looked at so far is the highly hierarchical configuration setup. In FASTBuild, you build up your configuration step by step, adding all options directly like in Make.

### Project files & syntax

FASTBuild uses a custom language for build files. It’s a very bare-bones languages, providing structured programming through `#if`

similar to a C preprocessor, and various ways to manipulate variables.

The key concepts are inheritance and composition. This allows scaling to large builds by reusing a lot of the configuration without having global state that applies to all projects. Let’s look at how you specify two different target platforms in FASTBuild. Instead of a single option you need to set, you’d specify multiple configurations:

```
.ConfigX86 =
[
.Compiler = "compilers/x86/cl.exe"
.ConfigName = "x86"
]
.ConfigX64 =
[
.Compiler = "compilers/x64/cl.exe"
.ConfigName = "x64"
]
.Configs =
{
.ConfigX86,
.ConfigX64
}
```


This sets up two structures and an array `Configs`

containing them both. Later on, you’d pass around the configuration array to your targets, and just iterate over the array, building a target with each of them manually. This approach allows FASTBuild to generate multiple platforms and configurations at the same time.

### Functions

Functions provide the actual node graph in FASTBuild. For instance, calling the function `Executable`

will register a new executable to be built, which can depend on different libraries. The build graph is built from those dependencies and cannot be expressed directly in the build file language – there’s no way to create a new build node without resorting to C++ and extending the core of FASTBuild.

### … and more

So far, FASTBuild sounds like a very bare-bones replacement of Make, but there are various interesting capabilities built into FASTBuild: Distribution, parallel execution and caching. All of these are related: As FASTBuild knows all dependencies precisely, and has a global understanding of the project, it can automatically distribute the build across multiple cores and even nodes in a network, and it can also cache things which don’t require to be rebuild.

## Sample project

For FASTBuild, we’re going to start with the root build file which contains all the project configuration. As mentioned above, FASTBuild is very explicit about all settings and it requires quite a bit of setup before it can get going. The sample project supports only Windows, and only Visual Studio 2015, but all those settings would be in a separate file for a production build. Building a project on Windows requires a lot of options to be passed to the compiler, I’m picking just the compiler options here as an example:

```
.CompilerOptions = '"%1"' // Input
+ ' /Fo"%2"' // Output
+ ' /Z7' // Debug format (in .obj)
+ ' /c' // Compile only
+ ' /nologo' // No compiler spam
+ ' /W4' // Warning level 4
+ ' /WX' // Warnings as errors
```


Here we can see build-time variable substitutions at work, FASTBuild will replace `%1`

with the name of the input file automatically.

Slightly down below, you’ll notice the first time I’m taking advantage of the structured nature of FASTBuild to specify the `DLLOptions`

. Those are simply the default options, but with minor tweaks:

```
.DLLOptions =
[
.CompilerOptions + ' /DLL /MT'
.LinkerOptions + ' /DLL'
]
```


Later on, we’ll see how this way of setting things comes in handy, but let’s start with the static library. It consists of two nodes – an `Exec`

node which invokes Python to generate the table, and a `Library`

node which requires the table to be generated already. The `Exec`

node is very similar to a basic Make rule:

```
Exec ("tablegen")
{
.ExecExecutable = "C:\Program Files\Python 3.5\python.exe"
.ExecInput = "statlib\tablegen.py"
.ExecOutput = "statlib\table.cpp"
.ExecArguments = "%1"
.ExecUseStdOutAsOutput = true
}
```


The dynamic library is the first one where we’re going to use a structure to pass in parameters. Instead of setting the linker options directly, we just pull in the `DLLOptions`

we defined above using the `Using`

command:

```
DLL("dynlib")
{
Using (.DLLOptions)
.LinkerOutput = "dynlib.dll"
.Libraries = {"statlib" ,"dynlib-obj"}
}
```


We could have written `.LinkerOptions + ' /DLL'`

as well, but then we’d have to duplicate it everywhere in our project where we want to build a shared library. Notice that the dependency to the static library is established directly by name, but we still need to manually set the include path as there’s no communication between targets by default.

Finally, the executable itself has nothing surprising any more, and our sample project is complete (and as usual, available [in the repository](https://github.com/Anteru/build-systems/tree/master/fastbuild) for your viewing pleasure.) I’m a bit on the edge regarding FASTBuild – I like the fact that it’s very focused on building C++ code fast, but I wish it would allow for some more flexibility and extensibility. For instance, it would be interesting to be able to define new functions in the build language. Even if slower than the built-in nodes, this would make it possible to build more complex tasks going beyond the simple property setting & inheritance which is at the core right now.

That’s all for this week, I hope you liked it, and next week we’ll go into the completely opposite direction and look at a very high-level build tool. Stay tuned!