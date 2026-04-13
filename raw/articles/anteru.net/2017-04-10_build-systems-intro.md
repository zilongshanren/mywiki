---
title: 'Build systems: Intro'
url: https://anteru.net/blog/2017/build-systems-intro
published: '2017-04-10'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Hi and welcome to a brand-new blog series! Over the coming weeks, I’ll be presenting build systems to you, and today I want to set the stage for this. I’ll be looking at the topic through a C++ lens, as my sample project will be written in C++, but that’s just because I’m a C++ person and that’s what is most interesting for me. That’s just a minor detail though – we’ll cover multiple build systems which support many different languages. Before we look into the project I want to build, let’s take a look first and what we’re going to discuss.

## Build systems

A build system solves a rather simple problem at its core: It transforms
data using rules and takes dependencies into account. You can think of
any build system as a graph traversal engine. Every **node** in that
graph has one or more **inputs**, produces one or more **outputs**, and
the node itself encodes the rules how to transform the inputs into the
desired outputs. That’s it, once everything is laid out in this way,
you just need to find out which **inputs** have changed, and then build
the nodes which (transitively) depend on those inputs.

Unfortunately, that’s a **really** hard problem, as the task of finding
**all** dependencies is a tough one – as the set of dependencies
include the compilers, system SDKs, any library which happens to be in
your project, the specific settings you pass on to your compiler and
**any** file that’s read by one of your transformation steps (and
more!). Spelling out all those dependencies is not realistic, and thus
most build systems will provide some shortcuts to reasonably approximate
it. That’s where the **language** support of a build system comes in
handy, as this allows you to express fewer of those dependencies
manually and just let the build system figure out the details.

The language support part can also extend to dependency management.
Strictly speaking, it’s not part of the core business, but a build
system has a lot of knowledge about the things it builds, and that makes
it convenient to build **more** than just the shared library file you
asked for. For instance, a build system could also deploy all headers
you need to include said shared library, the linker options you need to
link against it, the version, and so on, up to the point that you can
consume it in **another** project just “as if” it was built locally.

## Sample project

With this background, let’s look at the sample project I want to build. It’s a small project consisting of three separate parts:

- A
[static library](https://github.com/Anteru/build-systems/tree/master/base/statlib), which contains a generated source file. That source file is generated from a[Python script](https://github.com/Anteru/build-systems/tree/master/base/statlib/tablegen.py). - A
[dynamic library](https://github.com/Anteru/build-systems/tree/master/base/dynlib)linking against the static library. - An
[executable](https://github.com/Anteru/build-systems/tree/master/base/executable)consuming the dynamic library.

Let’s look at the tricky parts for each of them. The static library has
two interesting requirements to a build system. It needs to find Python
before you can actually generate the source file. If the build system
provides some way to *find* a dependency or binary, that’s a big plus
because it’ll make this part more reliable. The other requirement is a
tricky one – on Linux, a static library which goes into a dynamic
library must be compiled with `-fPIC`

, i.e. as position-independent
code. This can be only discovered by looking at the consumers of the
static library. A C++ aware build system should at least notice this and
warn you.

The dynamic library is straightforward, except that it requires a
preprocessor definition to build. That definition must be set *only* for
the dynamic library, not for the consumer of it.

The executable itself has no extra requirements. It just includes the
dynamic library header and links it. Includes is a good topic though –
there’s one external constraint I’m putting on the build systems which
is that each part must have its own build file, to show how the build
system handles modularity. This also means the build system needs to set
up the include directories, as by default, the individual parts just
`#include`

the headers of their dependencies. That’s it – a small,
but not trivial project, and the “benchmark” I’ll be using going
forward.

You can find the whole setup – without build system files – in my
[build system repository on
github.com/anteru](https://github.com/anteru/build-systems). With every new
blog post, I’ll be adding one new set of build files so you can follow
along. As a small teaser, we’re going to start next week with **Make**!