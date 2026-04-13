---
title: Dependency management 2018
url: https://anteru.net/blog/2018/dependency-management
published: '2018-02-21'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

It’s 2018 and C++ dependency management still remains a hot topic – or an unresolved problem, depending on your point of view. I’m not sure any more it’s actually “generally” fixable in the sense there’s a one-size-fits-all solution, as C++ projects have some unique requirements. For instance, people like setting compiler options for individual packages, they like linking across compiler & language barriers (mostly to C libraries, but there’s also stuff like [ISPC](http://ispc.github.io/)), and all this dependency business needs to get integrated into the build system as well.

Given the C++ world couldn’t agree on a build system yet, or an ABI, I think we’ll be stuck with hand-rolled dependency management for the forseeable future. Is this a bad thing? Yes and no. Yes, because this means everyone has to solve it somehow, but no, as the solutions don’t have to be huge and complex. Which brings me to today’s topic: I’ve redone my dependency handling once more – the third time – and I think I’ve finally arrived at some local optimum. To understand how it can be optimal for my problem case, we need to understand the problem I’m facing first, so let’s start with that.

## C++ framework with dependencies

In my spare time, I’m hacking on a C++ framework since over ten years, and that framework has grown to decent size. Part of the value add from using my framework is the fact that it bundles up a lot of external libraries under one uniform interface. For instance, `libjpeg`

, `libpng`

, `libtiff`

, are all nicely abstracted away so I can just load “any image” and under the hood the right thing happens. For many libraries, I ended up importing them into the source tree and building them as part of the compilation. That is, `libpng`

gets built with the same compiler options as everything else, with the same compiler, which has lots of benefits when it comes to debugging and sanitizers.

At the same time, I got a couple of dependencies which are very rarely updated: Boost, primarily, but also (on Windows) OpenSSL, and ISPC which is a build-time dependency. I’m using [CMake](https://cmake.org/), so I have find modules for all of them, but it’s still a pain to set up a dozen paths, more so as there are a few corner cases. For instance, for Boost & Clang, it’s not enough to just set the directories, but you also need to specify a compiler suffix. Long story short, I compile them only once in a while, and store them on my server. That works, but it has a couple of downsides: What version did I compile against? Is the build compatible or not with the latest compiler? If I want to travel and take my engine with me, do I really need to copy those 10000 files?

Now you might say, well, just commit the binaries to the source repository, and be done with it. That’s a reasonable approach and given I’m using [Mercurial](https://www.mercurial-scm.org/) with [largefiles](https://www.mercurial-scm.org/wiki/LargefilesExtension), that wouldn’t cause huge problems in terms of checkout size. The problem is not the storage, really.

The problem is that by tying your dependencies into your source control, you loose a lot of flexibility and comfort. The first problem you’ll notice is that a version control system is not designed to check out subsets of the repository tree. If I’m on Linux, there’s no use checking out the Windows binaries, so I need partial checkouts or dedicated repositories per OS. This doesn’t scale, as I might need separate dependencies per compiler, per compiler settings, etc.

The second big problem is updating dependencies: Ok, so I have my engine compiled against Boost 1.65, and now Boost 1.66 comes out. How can I switch between those? It’s not so simple if I have to do this in the source tree, especially if I want to try it on separate machines. Do I really want to add this to the repository history just for a test? Especially as it will require a new branch, and if it works, a merge of 10000 files with binaries? Sure, that works, but that’s not what a version control system was designed for.

Finally, there’s also a huge loss in comfort: Version control is optimized for source code, there’s usually no provisioning to have something like a file vault for some files, there’s no user friendly progress reporting when getting very large files, and generally you’re working in a corner case when you throw in tons of binaries into your source tree. Let’s say you want to store your dependencies in [ceph](https://ceph.com/) – where do you even start?

## Solving it externally

There’s no surprise that the solution to this is a customized package management solution. This is quite common in the big projects I saw – and there are various presentations and blog posts about this. I can highly recommend looking at the EA’s [package](https://www.youtube.com/watch?v=NlyDUQS8OcQ) [management](http://ndebug.blogspot.de/2015/01/software-builds-at-ea.html) or other C++ package managers like [Conan](https://conan.io/) or [Spack](https://computation.llnl.gov/projects/spack-hpc-package-manager). All of them try to solve the problem of not having your dependencies directly in the source tree, with various levels of complexity.

For my own needs, I had a couple of goals:

- A simple dependency specification – similar to the
[pip requirements.txt](https://pip.readthedocs.io/en/stable/user_guide/#requirements-files) - The ability to copy the whole repository around. This means it has to be few files (preferably archives) and no database attached.
- The whole thing should integrate directly into CMake, i.e. generate a file I can include into CMake to find all my dependencies.

Turns out, that’s not that hard to roll yourself. The way I structured this is as following:

- A repository provides packages.
- Each package contains releases, which all have a version number.
- Each release contains builds: A particular release, built with a particular compiler.
- A separate package definition repository provides package definitions. These describe packages – more on this below.

This means that for some dependencies, you need to introduce proper version numbers, as OpenSSL for instance is notorious for using letters to denote releases. I’ve opted into semantic versioning, so all dependencies have a three component version number (and in fact OpenSSL is the only dependency which requires some care there.) For each package, the package definition repository stores additional metadata about a package. This includes the package type – whether it’s a tool, a library, but also things like which ABI it’s using.

That would have been nearly enough if not for the problem mentioned at the beginning with Clang – which conditionally needs some extra setting. I’ve solved this by implementing conditions, which are available in two places (for now): One is the CMake build integration description, which tells the package manager what variables need to be set up for CMake. The other place is the dependency definition itself, where I can conditionally create dependencies based on platform, compiler, and so on. A sample package definition can be seen below:

```
<PackageDefinition Name="boost" Type="library" ABI="C++">
<BuildIntegration>
<CMake Key="BOOST_INCLUDEDIR" Value="$(Path)/include"/>
<CMake Key="BOOST_LIBRARYDIR" Value="$(Path)/lib"/>
<CMake Key="Boost_COMPILER" Value="-clang40" If="IsClang4"/>
<Condition Name="IsClang4">
<IsCompiler Name="Clang" Version=">=4,<5" />
</Condition>
</BuildIntegration>
</PackageDefinition>
```


All of the data is stored in a bunch of Xml files – the repository is trivial to hand-edit when a new package comes in, the definition files practically never change, and the builds are just `.xz`

archives. Moving the whole repository around means copying a folder, so that solves the simple to take with you requirement.

The dependency definition is a really simple Xml file:

```
<Dependencies>
<Dependency Name="boost" Version=">=1.65" />
<Dependency Name="ispc" Version="1.9" />
<Dependency Name="openssl" Version="1.1" If="IsWindows" />
<Condition Name="IsWindows">
<IsOperatingSystem Name="Windows"/>
</Condition>
</Dependencies>
```


How big did this thing end up being? Roughly a thousand lines of Python – so it’s a rather small tool, and easy enough to hack on. You might wonder how I’m ok with yet another dependency to get the package manager, but it turns out that’s a much simpler problem to solve. It’s just some python, so I could sub-module this into my main repository, or build an executable with [pyinstaller](http://www.pyinstaller.org/), or just fetch and run it as part of my build script. That’s really a very minor nuisance, as the code is – and always will be – tiny relative to the dependencies themselves.

## Summing it up

If you were hoping for the *one* solution solving all C++ dependency problems, you’ll leave disappointed. Sorry about that! However, if you were always wondering how to roll your own solution, I hope this post brought you some inspiration. It’s really not that much work once you nail down your requirements – and it’s definitely worth doing. Note that I’ve omitted a bunch of problems, like building the dependencies themselves. That something which I envision could be solved long-term through the package definition, but it hasn’t been enough of a problem yet to warrant writing it up. Other than that, I’ve yet to find some case where this breaks down. The next big step for me is integrating this with CMake 3.11’s [FetchContent](https://cmake.org/cmake/help/v3.11/module/FetchContent.html#module:FetchContent) functionality which should enable building everything with a single checkout and just using CMake, without any separate build scripts. But that’s a topic for another blog post, most likely …