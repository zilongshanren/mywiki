---
title: 'Build systems: Bazel'
url: https://anteru.net/blog/2017/build-systems-bazel
published: '2017-05-22'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

As hinted last week, we’re going for some really high-level build system today: [Bazel](https://bazel.build). Bazel is Google’s internal build tool, designed for scale, 100% robust builds, and also fast execution. The motto is “{Fast, Correct} - Choose two”, and today we’re going to find out how Bazel achieves this goal. Besides the features, we’re also covering Bazel as the new concepts it introduced spawned a whole family of build systems like [Please](https://please.build), [Pants](http://www.pantsbuild.org/), as well as [Buck](https://buckbuild.com/).

## Overview

Unlike the systems we saw so far, Bazel wants to guarantee that every build is repeatable. It thus requires very explicit dependencies, and even runs the build in a sandbox to ensure that only the specified files get accessed. This part is hidden from the user and Bazel manages to not require additional work over the other tools we saw so far. Reliable builds are an important puzzle piece for building project at scale. The other major component is composing builds from individual parts, which we’re going to look at next.

One major new concept Bazel introduces to help building at scale is project visibility. Each folder with a `BUILD`

file defines a package – or a project – which can define how it can be consumed. For instance, you can have some shared library which should be visible to anyone, typically a common library. At the same time, so other library might be only really useful inside your small corner of the build tree, and Bazel allows you to limit the visibility to this part from the project itself. From the outside, it’s impossible to link against this project, even though it’s part of the build. This fine-grained visibility makes it easy to compose large builds, because everyone can have his own private utility library and there will be no conflict, nor ambiguity which one to use.

The visibility is expressed through a path syntax: `//path/to/project:rule`

. It’s possible to compose multiple projects into a workspace which introduces another top-level hierarchy changing the path to `@project//path/to/project:rule`

, but that’s already quite advanced use of Bazel – check [the documentation](https://bazel.build/versions/master/docs/external.html#external-packages) if this kind of scaling is interesting for you.

Along with the global view of all projects, Bazel also comes with a very powerful query language to inspect the build. Let’s say for instance I want to know all files our static library creates. This is a query which was impossible to specify for all the build systems we looked at, but in Bazel, it’s really simple:

```
$ bazel query 'kind("generated file", //statlib:*)'
//statlib:table.cpp
```


And voilà, we found out that our `statlib`

project has one rule producing a generated file called `table.cpp`

. The power of the query language doesn’t stop here thought, we can also get the full dependency graph easily:

Bazel comes with it’s own programming language, called Skylark. It looks like Python and you might be tempted to say that it’s the same as in Waf and SCons, but in fact, Skylark is a separate language which just shares the Python syntax for [legacy reasons](https://bazel.build/blog/2017/03/21/design-of-skylark.html). Many moons ago before Google open sourced Bazel, they used the predecessor called Blaze, and that one had a Python interpreter which ran on the build files as a pre-process. Due to this heritage, Python remained part of Bazel, but there’s no Python interpreter any more in modern Bazel.

## Sample project

Time to look at our sample project with Bazel. This time, we have three separate and independent `BUILD`

files. As usual, we’re starting with our static library, and the rule to generate the lookup table:

```
genrule(
name = "gentable",
srcs = ["tablegen.py"],
outs = ["table.cpp"],
cmd = "python3 $< > $@"
)
```


`genrule`

is the most basic level at which you can specify rules for Bazel. Here, we have to specify the inputs and outputs, the command which will be executed, and Bazel will produce a node in its execution graph which consumes `tablegen.py`

and produces `table.cpp`

.

We can use it right away in the next rule in the project:

```
cc_library(
name = "statlib",
srcs = ["StaticLibrarySource.cpp", "table.cpp"],
hdrs = ["StaticLibraryHeader.h"],
visibility = ["//dynlib:__pkg__"],
includes = ["."],
linkstatic = 1
)
```


Here things get interesting. Just like we saw with Waf, we can specify the include directory *for our clients*, which in our case is the current directory. Without this, a library linking to `statlib`

will not see the includes at all. We also specify `linkstatic`

, but lo and behold, Bazel will take care of the `-fPIC`

story for us! We also make the static library visible to our dynamic library through the `visibility`

statement.

The dynamic library project is just what we’d expect:

```
cc_library(
name = "dynlib",
srcs = ["DynamicLibrarySource.cpp"],
hdrs = ["DynamicLibraryHeader.h"],
deps = ["//statlib"],
includes = ["."],
visibility = ["//visibility:public"],
copts = ["-DBUILD_DYNAMIC_LIBRARY=1"]
)
```


We link against the static library using the `deps`

statement, and we make it visible to everyone. As usual, you can inspect the full [build files in the source repository](https://github.com/Anteru/build-systems/tree/master/bazel).

Before we close, there’s one more interesting bit about Bazel – the ability to run your program directly. This is not as trivial as it sounds, as the dynamic library needs to be in the search path for the executable. Bazel takes care of this using the `bazel run`

command:

```
$ bazel run executable
INFO: Found 1 target...
Target //executable:executable up-to-date:
bazel-bin/executable/executable
INFO: Elapsed time: 0.141s, Critical Path: 0.00s
INFO: Running command line: bazel-bin/executable/executable
94
```


That’s quite impressive if you ask me! Bazel is a really interesting project as it tackles the issues of scaling your build system and making it robust at the same time, without sacrificing much on the readability or maintainability side. The query language is very interesting to extract lots of information about your build and allows to express very precise queries, instead of just printing the whole dependency graph and letting you figure out the details. You might think that that’s in for build systems in complexity, but next week, we’re going to look at one of the forks of Bazel which refines the visibility concept even further. Thanks for reading and hope to see you again next week!