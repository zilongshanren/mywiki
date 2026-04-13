---
title: Open source projects waiting to be implemented
url: https://anteru.net/blog/2012/open-source-projects-waiting-to-be-implemented
published: '2012-07-07'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

There’s a bunch of things out there, which should be implemented as an open-source project for the good of the (developer) community. This is of course a biased, personal list, but if some young developer out there is looking for an interesting project idea, feel free to pick one from the list below:

## Minimal, fast, portable mail client

A portable, minimal, easy-to-extend mail client, which uses a proper database for all storage. [Thunderbird](http://www.mozilla.org/thunderbird/) is a good client, no doubt, but having a simple client written in for instance [Python](http://python.org) + [Qt](http://qt-project.org), with [sqlite](http://sqlite.org) as the backend, should make it faster than Thunderbird, more robust, and easy to synchronise across multiple machines.

Going 100% Qt and C++ might be an option as well, but my gut feeling is that [PyQt](http://www.riverbankcomputing.co.uk/software/pyqt/intro) should be fast enough for the job. Having a database backend for storage is the crucial thing here, to ensure that everything is robust and fast. [mbox](http://en.wikipedia.org/wiki/Mbox) just doesn’t cut the mustard any more when your inbox has several thousand e-mails, especially when it comes to backup.

## Clang-based documentation generator for C++

We have [Clang](http://clang.llvm.org), but we’re mostly still stuck with [Doxygen](http://www.stack.nl/~dimitri/doxygen/) for documenting C++. While Doxygen can be used to generate good documentation, it has lots of shortcomings as it has to guess the meaning of every single statement.

A proper documentation system requires accurate information, and Clang seems like the perfect solution for this. Together with a database backend, this would allow much higher quality documentation and potentially for a docutils-style mixing of code and documentation, where the code is tested while the documentation is built.

The documentation generator should also not contain output-related stuff. I’ve been working on the [robin](https://bitbucket.org/reima/robin) Doxygen to [Sphinx](http://sphinx.pocoo.org) bridge, which generates easy-to-integrate documentation in restructured text from Doxygen XML. Ideally, the next-gen documentation tool will directly produce structured and interlinked documentation fragments, which are easy to convert into whatever representation you need. The focus should be on the data though, and the presentation should be independent (just take a look at the Doxygen XML to see how presentation and content can get intermingled if the data representation is only a second class citizen.)

## Robust meta-shading language for OpenGL/DirectX

[OpenGL](http://opengl.org) and [DirectX](http://en.wikipedia.org/wiki/DirectX) come both with their own shading language, which is not quite identical but extremely comparable otherwise. There is [Cg](http://developer.nvidia.com/cg-toolkit), which is a unified language targeting both OpenGL and DirectX, which unfortunately doesn’t get updated to often and is a “black-box”, and there are some HLSL/GLSL converters like [HLSL2GLSL](https://github.com/aras-p/hlsl2glslfork) or [ANGLE](http://code.google.com/p/angleproject/). So far, there is no open alternative, which unifies GLSL and HLSL into a single front-end and generates GLSL/HLSL at the backend.

Having a meta-shading language and the toolchain in an easy-to-hack format (ideally, some scripting language) would make the whole business much simpler. The key point is that it must be easy to hack, so integrating new features or support for new targets is simple. The output should be simply GLSL/HLSL code, so it can be trivially inspected and further optimized if necessary.

So much for this time, hopefully someone out there finds this list helpful and writes a kick-ass project :)