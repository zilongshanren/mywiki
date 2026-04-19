---
title: The Benefits of not Writing Zig
url: https://danielchasehooper.com/secret/benefits-of-no-zig/
published: '2025-02-21'
source_blog: Daniel Hooper
source_site: https://danielchasehooper.com/
category: graphics
fetched: '2026-04-19'
---

February 21, 2025・2 minute read

Much has been written about the Zig programming language and people’s experiences writing it. However there are other parts to the Zig project outside of the langauge worth discussing. You can benefit from the zig Project even if you don’t use the languge. Those benefits don’t get enough attention so I wanted to lay them out here.

You may already know that Zig can be used as a C compiler, but Zig has several other tools built in. Here’s the list from `zig help`

:

```
ar Use Zig as a drop-in archiver
cc Use Zig as a drop-in C compiler
c++ Use Zig as a drop-in C++ compiler
dlltool Use Zig as a drop-in dlltool.exe
lib Use Zig as a drop-in lib.exe
ranlib Use Zig as a drop-in ranlib
objcopy Use Zig as a drop-in objcopy
rc Use Zig as a drop-in rc.exe
```


For people avoiding Microsoft tooling (me), this is amazing to have. I think there is room for others, like a macOS `lipo`

drop-in, but I digress.

Honerary mention: Zig has its standard library documentation built-in for offline-viewing. View with `zig std`


Zig has it’s own build system that replaces like make, gradle, etc. Instead of relying on a combination of makefiles and system commands that may or may not be compatible (or installed!) across machines, projects can create a `build.zig`

file to compile. While it’s most commonly used in Zig projects, it is a generic build system that can be used for any process that takes input files and produces output files. I personally find the build API difficult to use in its current state (lack of documentation, needs refinement, poor compiler error messages) - but the actual tooling is nice for consumers of projects with a `build.zig`

file. As somone that found building projects confusin, time consuming, and error prone, I appriciate that projects with a `build.zig`

can be built as easily as

```
git clone <project_url> project
cd project
zig build
```


Cross compilation allows compiling for OSes/chips that are different than the one `zig`

is running on. I work primarily on macOS, and `zig cc`

allows me to create a windows .exe without dealing with Microsoft Visual Studio, or even switching over to a Windows machine! The 40Mb Zig zip totally saves you from tooling differences between platforms.