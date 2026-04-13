---
title: 'Build systems: MSBuild'
url: https://anteru.net/blog/2017/build-systems-msbuild
published: '2017-04-24'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Last week we’ve covered Make – an ubiquitous build tool in the Linux world. There’s a variant on Make for Windows as well (`nmake`

), but the real workhorse on Windows is [MSBuild](https://github.com/Microsoft/msbuild). MSBuild is the default build system used by Visual Studio for .NET and C++. Originally a part of the .NET framework, it has grown over time to cover more use cases and is now maintained as an independent project.

## Overview

MSBuild is actually multiple projects in one. At its core, it’s actually Make, but there are many layers and functions which have been added to it to cater for the many different use cases. Before we look at all the extra functionality, I want to show you the core concept of MSBuild, which is the same as for Make or any other build system really: Transforming inputs into outputs.

In MSBuild, the build files are written in XML. A target node defines the inputs and outputs, and contains multiple task nodes which do the transformation. Here’s a simple example:

```
<Target Name="MyTarget" Inputs="file.cpp;file.h" Outputs="library.lib">
<CL Sources="file.cpp"/>
<LIB Sources="file.obj" OutputFile="library.lib">
</Target>
```


The `CL`

and `LIB`

elements are *tasks*. You can think of them as built-in function calls. If you squint a bit, doesn’t this resemble Make a lot? Just as reminder, this is how it would look like in Make:

```
library.lib : file.cpp file.h
cl.exe /c file.cpp
lib.exe /OUT:library.lib file.obj
```


This is the core foundation of both Make and MSBuild. However, where Make only adds some convenience functionality on top, and relies on other tools to generate the build files, MSBuild integrates both this low-level core and many high-level concepts into one framework.

### Logic

Besides variables like Make, MSBuild adds logic on variables through conditions. Conditions can be applied nearly everywhere and allow you to execute targets and tasks only if some condition holds. All tasks and targets can get a `Condition`

attribute. On top of that, more complex constructs can be created including `When`

, `Choose`

and `Otherwise`

elements. This enables complex switch statements and other logic to be evaluated as part of the build process. Typically, this logic will end up populating properties and item lists which are then consumed elsewhere.

MSBuild doesn’t stop on logic embedded in conditional expressions and the XML though. MSBuild is built on .NET and that provides another source of interesting functionality – the ability to call .NET methods. It’s not quite C#, but it allows you do to things like `@(theItem->IndexOf('r'))`

. Or you can initialize a property using `$([System.DateTime]::Now)`

. The way it’s integrated doesn’t allow for large-scale scripting, but to make it easy to call a function here and there.

### Tasks

Thanks to .NET and easy class loading, MSBuild also provides a very wide range of pre-made tasks. Instead of specifying the command line of a tool directly, there’s a task for everything from file copying to C# manifest resource name creation. The tasks are also a good example where MSBuild has grown on a per-client basis, instead of being designed into shape: There’s very specific functionality like a [RequiresFramework35SP1AssemblyTask](https://docs.microsoft.com/en-us/visualstudio/msbuild/requiresframework35sp1assembly-task) which can do things like writing a desktop shortcut – functionality which I would have expected to be provided outside of the core MSBuild distribution.

On the other hand, there’s a large chunk of functionality which I care about that is actually external – the ability to build C++ projects. C++ support into MSBuild was gradually added and unfortunately, it never ended up being a first-class citizen. Even today, the solution file is not a MSBuild file, and there’s special magic to handle it (if you want to see what’s happening, you need to set the environment variable `MSBuildEmitSolution=1`

and then invoke MSBuild on the solution.)

### C++ integration

C++ integration happened through the addition of a slew of new tasks like the [CL Task](https://docs.microsoft.com/en-us/visualstudio/msbuild/cl-task) which is a wrapper around `cl.exe`

. It literally wraps every single parameter you can pass to `CL`

into an attribute. Unlike the C# integration however, the output handling was omitted from the C++ tasks. The `Csc`

task (which calls the C# compiler) provides `TaskParameter`

values which allow you to specify the output easily (you can write the output file name into a property for example). Unfortunately, that’s not the case for the `CL`

task, which requires you to specify the outputs manually.

There’s a lot more to MSBuild than I covered here, but the things mentioned so far are enough to get us started with building our sample project. Without further ado, let’s get ready for some building!

## Sample project build

Let’s walk through the [sample project](https://github.com/Anteru/build-systems/tree/master/msbuild) build file. Unlike all other tools, I didn’t manage to split up the project into multiple self-contained files – everything is in the top-level `build.xml`

.

We’re starting with some setup code:

```
<Import Project="$(VCTargetsPath)\Microsoft.Cpp.Default.props" />
<Import Project="$(VCTargetsPath)\Microsoft.CppCommon.targets" />
```


This tells MSBuild to include C++ tasks, otherwise, there’s no `CL`

task. I also define three item groups so I can reference those files more easily:

```
<ItemGroup>
<StaticLibraryFiles Include="statlib/StaticLibrarySource.cpp;statlib/tablegen.py"/>
<DynamicLibraryFiles Include="dynlib/DynamicLibrarySource.cpp;dynlib/DynamicLibraryHeader.h"/>
<ExecutableFiles Include="executable/ExecutableSource.cpp"/>
</ItemGroup>
```


Now, the individual targets come. The most interesting is the static library, which calls Python.

```
<Target Name="StatLib" Inputs="@(StaticLibraryFiles)" Outputs="statlib.lib">
<Exec Command="python statlib/tablegen.py > table.cpp" Outputs="table.cpp">
<Output TaskParameter="Outputs" ItemName="GeneratedFiles"/>
</Exec>
<CL Sources="statlib/StaticLibrarySource.cpp"/>
<CL Sources="@(GeneratedFiles)"/>
<LIB Sources="StaticLibrarySource.obj;table.obj" OutputFile="statlib.lib"/>
</Target>
```


The static library is a target, it depends on the static library files – I’m referencing the item group here – and then it executes the tasks provided inside in-order. There’s no searching of modules in MSBuild, so I again just hard-coded the call to Python here. I’m also wiring the output of the `Exec`

command into an `ItemName`

which I can then reference below in a `CL`

task – that’s the `@(GeneratedFiles)`

. Finally, I’m calling the linker, specifying all file names manually.

If there’s a dependency between targets, it has to be specified manually inside the `Target`

element. This way, MSBuild can build the whole dependency graph and then execute one target after the other. MSBuild cannot see into individual targets when scheduling, and inside each target everything is executed serially, which is the reason why it can’t just compile all C++ files first, then later link the libraries as they become ready. For in-target parallelism, you have to rely on the task handling this internally, for instance through the `/MP`

option which compiles multiple C++ files in parallel.

In my opinion, MSBuild is a curious piece of software. It’s firmly rooted in the well-designed and highly-consistent world of .NET, which is visible in the “original” parts of the application. At the same time, it was clearly used by many different clients and grew in basically all directions without the guidance of an architect. In the end, we get a large bag of functions and tools to solve the software build problem – but it could be that this is a reflection of the mess that is needed to build any piece of large software.