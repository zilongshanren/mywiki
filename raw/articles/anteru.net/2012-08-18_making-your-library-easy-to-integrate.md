---
title: Making your library easy to integrate
url: https://anteru.net/blog/2012/making-your-library-easy-to-integrate
published: '2012-08-18'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Let’s assume you have been writing a small-to-medium library which solves some specific problem, and now you would like to publish it as open-source so other people can integrate it. Think of stuff like a new compression algorithm, some image processing, mesh loading, you name it. How can you make sure that your library gets reused by many people, and patches come flowing back?

## Use a proper license

License the code as [BSD](http://opensource.org/licenses/BSD-2-Clause), [MIT](http://opensource.org/licenses/MIT)/[Boost](http://opensource.org/licenses/BSL-1.0), or place it in [public domain](http://unlicense.org/). Any other license is an unnecessary hurdle to adoption. Putting your code under a license which requires a lawyer to be properly understood means many people in companies won’t even take a look at it (they might not be even allowed to look at your code!)

BSD is probably the best choice, it’s widely accepted and allows people to track back the code to you. If in doubt, I would use the BSD. Just make sure you don’t use a copyleft license like [GPL](http://opensource.org/licenses/GPL-3.0). While there are certainly areas where the GPL makes sense, small, reusable libraries are not that area – putting your stuff under GPL means basically any company developer will ignore you. Not the best way to get many people to use your code!

## Use a sane version control

It should go without saying that you use a version control system, but if you put a library online, make sure that patching and branching is easy. That basically means you need to use [Mercurial](http://mercurial.selenic.com/) or [git](http://git-scm.com/), as all other version systems are either to unpopular or make branching and patching extremely hard – [Subversion](http://subversion.apache.org/) is such a system, so keep away from it.

Ideally, you want to put it only somewhere together with at least a short description and, if possible, an issue tracker. [Bitbucket](https://bitbucket.org/), [github](https://github.com/), [gitorious](http://gitorious.org/), [Google Code](http://code.google.com) are all popular choices with few differences in functionality between them.

## The build system

I assume that your library is in C or C++, if it is in a scripting language like Python, just skip this paragraph. If you use C/C++, make sure that building your library is simple even without a build system in place. Ideally, just provide an “amalgamation” file like [SQLite](http://www.sqlite.org/) does, if that is not possible, at least make sure that throwing all your source files into a single project results in a working binary.

Some projects split themselves into multiple libraries, with heavy-duty dependencies, and use extremely complex build-scripting to get built. An example for this is the [Alembic](http://code.google.com/p/alembic/) library, which requires the [ILM](http://www.openexr.com/) libraries and the [HDF5](http://www.hdfgroup.org/HDF5/) library. The easiest way to build such a library is not to use the provided build files, but just slapping everything together into one project and be done with it (all of the ILM files can be easily compiled into a single static library, same for all of Alembic, and you’re done.)

If your library is indeed more complex, as you are doing compile-time configuration/generation of files, provide a version with all generated files. If someone just wants to build your library, that will be the easiest solution. If that isn’t possible, then your library is probably to large or complicated, and not easy to reuse anyway. Consider releasing sub-parts of your library in this case.

There’s nothing wrong with providing a bunch of makefiles as well, but don’t assume people will be using them. If you provide makefiles, it should consider to also provide source files for [CMake](http://www.cmake.org) as well, which is a pretty standard system to get project files generated for a wide range of IDEs.

## The code

Your code should be reasonably portable and clean (see also this [great blog post on how to clean bad code](http://www.altdevblogaday.com/2012/08/18/cleaning-bad-code/)). In general, it should have few dependencies, and compile without warnings at the highest warning level. Assume that the users will always compile at the highest level and fix them. Ideally, you should also run some static analysis over the code to make sure you don’t have obvious null-pointer dereferences and other stuff. Make sure that you don’t include dead code in your library, that function that was useful five revisions back should live in the repository history, and nowhere else. This reduces the amount of code that a user has to port, if he decides to use your code on a new platform.

Portability is also very important. Try to make sure that your code works fine on the major compilers (MSVC for Windows, GCC for Linux, Clang for Mac OS X). The easiest thing to do is probably to stick with simple C (C89) or simple C++ without fancy meta-programming. If you have dependencies, make them few, and try to use the most common libraries. Boost is usually overkill, but if you really need threads, it still the next-best choice instead of writing your own wrappers.

One important part is I/O. If your library does some I/O, make sure the user can provide his own I/O routines. Often enough, I want to load some data from memory, or from a socket, or some other non-standard source. [RPly](http://w3.impa.br/~diego/software/rply/) is for instance a very nice library for reading PLY files, unfortunately, it assume your file is readable by `fopen`

. A good example of how to do it is the [libpng](http://www.libpng.org/pub/png/libpng.html), which makes it trivial to hook in your own input/output routines.

## The patch handling

And here’s the most important part. Assuming your have a nice, easy-to-integrate library, you can expect that a few users will come back to you with patches. Make sure that submitting patches is easy, for instance, by providing a contact address in every source file or by adding some prominent link to the mailing list to your project description. If someone submits a patch, give timely feedback; it’s ok to reject patches but explain why.

It’s also nice if there is some simple set of tests which can be used to verify the correctness of the code, but the most important thing is to get usable patches. Once accepted, try to actually commit and push the patch out quickly as well. This makes it easier for people who keep their own private fork.

What’s also nice is to have some kind of road-map so everyone can understand if you are planning big changes to your library or whether the code is in maintenance-only mode. If you are in maintenance-only – which you should try to be, after all, your library is small and solves a particular problem – users will be more willing to perform deeper integration on their side.