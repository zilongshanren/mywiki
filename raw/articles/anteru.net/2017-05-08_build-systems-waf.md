---
title: 'Build systems: Waf'
url: https://anteru.net/blog/2017/build-systems-waf
published: '2017-05-08'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Another week, another build system – this week, we’re going to look at [Waf](https://waf.io). It’s another Python-based build system, and it’s one with a few new concepts, so let’s dive into it right away.

## Overview

The key idea behind Waf is to have the build split up into separate *phases*: Configure, then build. Waf is not the first build system ever with a configure step – that honor probably goes to [automake](https://www.gnu.org/software/automake/) – but it’s the first in this series, and as such, we’ll take the opportunity to investigate what configure is good for.

The idea behind a separate configure step is that there’s a lot of setup code which only needs to be run once to identify the platform. Think of searching for header files and setting build definitions based on this, which usually requires firing up a compiler just to store the result whether it worked or not. Same goes for platform-specific file generation – what’s the name of the operating system, what configuration options did the user specify, and so on.

Instead of running this every time you build, configure runs once, does all the expensive work and persists it, and subsequent build calls don’t even need to execute the configuration steps.

### Project files

Waf project files are plain Python scripts, same as we saw in [SCons](https://anteru.net/blog/2017/build-systems-scons) last week. The key difference is that we need to expose a couple of functions per script which are called by Waf, instead of typing in our commands directly and calling Waf on our own.

We need at least a `configure`

and a `build`

function, and both get a context object passed into them. During `configure`

, we’ll do the usual things like setting up options for the compiler. This is straightforward as the environment exposes the flags directly, and we can manipulate them using Python, which is very well suited for dictionaries and lists.

### Task oriented

Waf’s execution graph is task-based – each task is the atomic unit of work which takes some inputs and transforms them into the outputs. Once the tasks are created, then the scheduler takes over and runs the tasks. Integrating new custom build steps is done through new tasks, as we’ll see below in the sample project. One great feature of the Waf scheduler is that it will automatically extract execution dependencies. If we specify a task which produces files, and we have another task which consumes them, Waf will take care of scheduling them in-order without extra work.

### C++ support

Waf provides C++ support along other languages like D and Fortran, and it’s integrated through language specific tasks. The language integration provides basic build targets, and it has first-class support for C++ specific concepts like include paths. Of all the build systems we’ve looked at so far, Waf is the first one which allows for true modularity of the build files as it exports & imports include directories across targets.

In one file, we can create a new shared library which specifies the `export_includes`

directory, and if we consume that library elsewhere using `use`

, Waf will take care of setting the correct include directory *at the use site*. We can thus move around projects freely, and things will just work – no need to hard-code paths any more.

## Sample project

Let’s start with the static library project, which requires some code generation. As mentioned above, we’ll use a task to generate the lookup table. There’s two things to a task, the definition, and then the invocation. Here’s the definition:

```
class tablegen(Task):
def run(self):
return self.exec_command ('python {} > {}'.format (
self.inputs [0].abspath (),
self.outputs [0].abspath ()
))
```


What we notice right away is that there’s no need for special escape variables, the inputs & outputs are specified as member variables. This also implies the task is *instantiated* for every execution, instead of being reused. This happens very explicitly in the build step:

```
tg = tablegen (env=ctx.env)
tg.set_inputs (ctx.path.find_resource ('tablegen.py'))
tg.set_outputs (ctx.path.find_or_declare ('table.cpp'))
ctx.add_to_group(tg)
```


We specify both the inputs and outputs, which initializes the `self.inputs`

, `self.outputs`

members we saw above. Finally, we add it to the current build group, which is the list of tasks that gets executed for this project. Thanks to the auto-discovery of dependencies, it’s enough to declare the output `table.cpp`

and use that in the subsequent `stlib`

call to get the execution order right.

The rest is very simple:

```
ctx.stlib (
source = 'StaticLibrarySource.cpp table.cpp',
includes = '.',
export_includes = '.',
target = 'statlib',
cxxflags=ctx.env.CXXFLAGS_cxxshlib)
```


This adds a static library, uses the specified include directory and source files, gets a name, and exports include directories as explained above. The last line needs a bit more explanation. The `stlib`

has the usual `-fPIC`

problem for Linux, and unfortunately Waf cannot resolve this automatically. We need to specify the flags manually – the [recommended solution](https://waf.io/blog/2016/09/static-libs-from-shared-objects.html) is to use the `cxxshlib`

flags for a static library. That’s what’s happening here in the last line.

The remainder of the sample project is rather boring – Waf doesn’t require a lot of magic to set up. One of the highlights of Waf is that it builds *out-of-source* by default. All build files, temporaries, and targets get placed into a `build`

folder by default, which is trivial to ignore for source-control systems and avoids polluting the source tree with intermediate files. Even the lookup table we generated above gets built there. There’s only one minor caveat here which is: Waf doesn’t copy shared libraries into the same folder as the binary, nor does it provide an easy build command line which would set up all paths.

As usual, the [sample project is online](https://github.com/Anteru/build-systems/tree/master/waf), and it should work on both Linux and Windows. That’s all for this week, see you again next week!