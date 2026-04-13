---
title: 'Build systems: Buck'
url: https://anteru.net/blog/2017/build-systems-buck
published: '2017-05-29'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Last week we looked at [Bazel](https://anteru.net/blog/2017/build-systems-bazel), and today we’re going to look at one of the build systems in the Bazel family: Buck. Buck is Facebook’s variant of Bazel, so most of what was written last week still applies. The interesting bit we’re going highlight today is how Buck handles include directories. Before we start though, let’s understand first why this is something worth writing about!

## The include mess

What’s wrong with `#include`

files? Well, what isn’t – especially when it comes to building bigger projects. The main issue is collision of include file names. Assume you have two libraries `A`

and `B`

both with an `utility.h`

, and which you want to consume from a single project. As we’ve seen before in Bazel and Waf, some build systems allow to transitively forward include directories, which is great as nothing is ambiguous. But in the setup just described, you’ll have a collision between the two `utility.h`

files, and if you don’t have full control over the layout of your project, you can’t actually resolve it! The only way to disambiguate is to find a parent directory from which the `utility.h`

files have a unique path.

Interestingly, this is something which C++ modules are supposed to fix eventually, but in the meantime, the solution space is rather sparse. In my own framework, I decided to use what I call [canonical include files](https://anteru.net/blog/2012/canonical-include-files-for-frameworks-libraries). Qt, another huge C++ library, uses a similar approach. In both cases, an indirection layer is used to solve the problem, but the indirection layer is created manually.

## Buck & includes

Buck provides tooling to solve the problem once and for all. Just like in Bazel, we define the public `#include`

files, but what Buck does now it automatically copies them into a new directory, and then forces this as the include directory – with the project name attached to it. What we included previously using `#include "StaticLibraryHeader.h"`

now becomes `#include "statlib/StaticLibraryHeader.h"`

. When building a project, you’ll notice that in the `buck-out/gen/statlib`

folder, there’s a new folder named `statlib#default,private-headers`

and this contains all headers we marked as export from the static library.

The only difference compared to Bazel – where we specified an `includes`

directive which contained the current directory – is that we need to specify them manually:

```
cxx_library(
name = "statlib",
srcs = ["StaticLibrarySource.cpp", ":gentable"],
headers = ["StaticLibraryHeader.h"],
visibility = ["//dynlib:dynlib"],
exported_headers = ["StaticLibraryHeader.h"],
link_style = "static_pic"
)
```


As long as your library names don’t collide, this seems like a very nice solution to this age-old C++ problem. Going forward, it should allow a clean transition to modules, which will cause other build tools quite some headache as they introduce yet another build target and dependency per C++ library.

Otherwise, Buck behaves very similar to Bazel, with some changes to the command names, but nothing earth-shattering. See for yourself in the [sample repository](https://github.com/Anteru/build-systems/tree/master/buck)! Thanks for reading and see you again next week!