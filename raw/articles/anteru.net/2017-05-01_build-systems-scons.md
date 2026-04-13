---
title: 'Build systems: SCons'
url: https://anteru.net/blog/2017/build-systems-scons
published: '2017-05-01'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

This week we’ll cover [SCons](http://scons.org/), a Python-based build
system. SCons is a full build system, with built-in support for
different programming languages, automated dependency discovery, and
other higher-level utilities. Some of you might have heard of it as it
has been used in [Doom
3](https://github.com/id-Software/DOOM-3/tree/master/neo/sys/scons) for
the Linux builds. That’s at least how I heard about SCons for the first
time ☺ Apparently, at some point, [Frostbite was using
SCons](https://twitter.com/repi/status/285744276506296322) as well.

## Overview

SCons is written in Python – and the build files are actually Python scripts. This is great as there’s no “built-in” scripting, you can just do whatever you want in Python, and you call SCons like any other library.

SCons at its core is similar bare-bones to Make. You have *node objects*
internally which represent the build graph. Usually, those nodes get
generated under-the-hood – for example, you write a SCons file like
this:

```
Program(['main.c'])
```


Here, `main.c`

is an `Object`

(as in a C++ object file, not something
related to object-oriented programming, mind you). The code above is
equivalent to:

```
Program ([Object ('main.c')])
```


This creates one C++ `Program`

node, with one C++ `Object`

as the input.
You can look at the dependency tree using `scons --tree all`

. For the
example above, it would produce something like this:

```
+-.
+-Sconstruct
+-main
| +-main.o
| | +-main.cpp
| | +-/usr/bin/g++
| +-/usr/bin/g++
+-main.cpp
+-main.o
+-main.cpp
+-/usr/bin/g++
```


That’s the full dependency tree. SCons is not timestamp based (at least by default), and the files above will be hashed and checked as dependencies when you ask for a build. When you run the build, you’ll see how SCons processes the tree bottom-up:

```
scons: Building targets ...
g++ -o main.o -c main.cpp
g++ -o main main.o
scons: done building targets.
```


That’s it for the core functionality of SCons. Notice that SCons is aware of all intermediate targets, which means that it can also clean everything by default.

## C++ integration

C++ is yet another target language for SCons, and shares functionality
with C, D and Fortran. All of them have the same targets and a similar
build model. You specify a `Program`

, and based on the list of provided
source files, SCons figures out what compiler to use.

There’s limited support for discovering libraries and functions. It will search the default paths for it, but I haven’t seen a way to register custom search modules. Of course, that’s only a minor limitation, as you can just write the search script in Python, but it’s a bit disappointing that SCons doesn’t come with a set of search scripts.

SCons can optionally generate Visual Studio project files. Optionally,
as there’s no simple “generate project files” from a given SCons node
graph. Instead you build them in a declarative way just like any other
target. What you get from SCons is the actual Xml file generation. This
makes it easier than writing it from scratch, but it requires still some
repetition – for instance, the source files need to be provided to the
target you want to build, and then again to the Visual Studio project.
The Visual Studio project generator doesn’t query them from the target,
this part is left to the user. If you’re interested in the details, the
documentation has some [example
code](http://scons.org/doc/production/HTML/scons-user.html#b-MSVSProject)
which shows a simple project setup.

## Sample project

Let’s see how SCons fares with our sample project. On the good news side, it’s the first system we’re looking at which supports both Linux and Windows with the same build script.

```
import os
# This is needed so we get the python from PATH
env = Environment(ENV = os.environ)
# include path is relative to root directory (indicated as #)
env.Append (CPPPATH='#')
p = os.path.abspath ('./tablegen.py')
```


This is just some basic setup so we can later use the same `python`

executable as we used to invoke SCons. SCons doesn’t inherit the
environment of the surrounding shell by default, so we need to do this
manually. This is for Windows, so we can actually find a Python
interpreter if we have it in the `PATH`

of the calling script.

```
pyexec = 'python' if os.name == 'nt' else 'python'
env.Command ('table.cpp', 'tablegen.py', '{} {} > $TARGET'.format (pyexec, p))
```


Now we’re finally coming to the meat of this build:

```
env.StaticLibrary('statlib', [
# This adds fPIC in a portable way
SharedObject ('StaticLibrarySource.cpp'),
SharedObject ('table.cpp')])
```


Here we’re using the nodes directly, as we’d have to edit the compiler
configuration manually otherwise to add `-fPIC`

. Notice that SCons
doesn’t notice on it’s own that this static library is consumed in a
shared library, so we need to handle this manually. From here on, we can
reference the target `statlib`

in other project files inside the same
build, which simplifies the linking – no hard-coded paths. However, we
can’t export/import include paths directly, so our dynamic library
project will still end up specifying the path for includes manually:

```
SharedLibrary ('dynlib', ['DynamicLibrarySource.cpp'],
LIBS=['statlib'], LIBPATH=['../statlib'],
CPPPATH=['.', '../statlib'], CPPDEFINES = ['BUILD_DYNAMIC_LIBRARY=1'])
```


That’s it for SCons and this week! As always, make sure to look at the
[sample
project](https://github.com/Anteru/build-systems/tree/master/scons)
for a full, working example.

In my opinion, the main advantages of SCons are twofold. First, it lets you freely mix various languages – you can build a combined D and C++ and Java program without breaking a sweat. Second: By virtue of being a Python module, it easily integrates with the typical “glue” code in a build without having to change languages. I currently have a lot of Python code running as part of my build, and having the build system written in Python and using Python for the build files would simplify many things. It also removes the context switch between build system language and utility language. Personally, I’d probably consider it for very heterogenous builds, as SCons makes customization and scripting really simple compared to the other tools we’ve look at so far – and also compared to quite a few tools that are yet to come. Enough teasing for today, see you again next week!