---
title: 'Static Libraries and Plugins: Global Pain'
url: http://hacksoflife.blogspot.com/2012/12/static-libraries-and-plugins-global-pain.html
author: Benjamin Supnik
published: '2012-12-13'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Years after the X-Plane plugin SDK was ported to operating systems that support Unix .a (archive) static libraries, I have finally come to understand what a mess global symbols can make with incorrect linker settings. The problem is that the incorrect linker settings are almost always the defaults. This blog post will explain what goes wrong with this kind of linker setup and how to fix it. While this stuff might be obvious to those intimately familiar with Linux and Unix-style linking, it's a bit astonishing to anyone coming from the Windows and pre-OS X Mac world, where the assumptions about linkage are very different.


This post may also thoroughly slander Linux, and if I learn why I'm an idiot and the whole problem can be solved in a much better way, hey, that's great. I'd much rather find out that there's a better way and I'm wrong than find out that things really are as broken as they seem.



In other words, if you have five implementations of "void a()" in your dynamic libraries, the first one loaded is used by everyone. It's a global namespace.


Note that if your symbol is not global, it will not be replaced by an earlier variant. So if your symbol isn't global, other people having global symbols can't hose you.


The implications of this are clear: you should be very very careful and very very minimal about what gets exported into the global namespace, because of the risk of symbol collision. I found a bug in an X-Plane plugin because the internal routine sasl_done (in a plugin called sasl) was global and the second instance loaded - sasl_done from libsasl2.dylib had already been loaded by the OS. The results: a random call into a DLL when the plugin thought it was calling itself!


Unfortunately, the default for GCC is to put


There is one exception to this global calling: if you use dlsym to resolve a symbol from a


This post may also thoroughly slander Linux, and if I learn why I'm an idiot and the whole problem can be solved in a much better way, hey, that's great. I'd much rather find out that there's a better way and I'm wrong than find out that things really are as broken as they seem.

#### Globally Symbols and Shared Libraries

Unix-style linkers (e.g. ld on both OS X and Linux) support a*shared global namespace*for symbols exported from shared libraries. Simply put, for any given symbol name, there can be only one 'real' implementation of that symbol, and the first dynamic library (or host app with dynamic linkage, which is basically all host apps these days) to introduce that symbol defines it for*every*dynamic library.In other words, if you have five implementations of "void a()" in your dynamic libraries, the first one loaded is used by everyone. It's a global namespace.

Note that if your symbol is not global, it will not be replaced by an earlier variant. So if your symbol isn't global, other people having global symbols can't hose you.

The implications of this are clear: you should be very very careful and very very minimal about what gets exported into the global namespace, because of the risk of symbol collision. I found a bug in an X-Plane plugin because the internal routine sasl_done (in a plugin called sasl) was global and the second instance loaded - sasl_done from libsasl2.dylib had already been loaded by the OS. The results: a random call into a DLL when the plugin thought it was calling itself!

Unfortunately, the default for GCC is to put

*everything*into the global namespace. As gcc 3.x fades into history, more code is using -fvisibility=hidden and attributes more aggressively, but the defaults make it really easy to do the wrong thing and dump a whole lot of symbols into the flat namespace.There is one exception to this global calling: if you use dlsym to resolve a symbol from a

*specific*dynamic library (as returned by dlopen) finds it in that dynamic library, like you would expect. Therefore if you have a plugin with an "official" entry point (like "PluginStart") you can load multiple plugins into the global namespace and find the "right" start function via dlsym. (If a plugin called its own start routine, it might jump into the wrong plugin due to globla namespace issues.#### What Am I Exporting?

On both OS X and Linux you can use "nm" to view your globally exported symbols:

nm my_plugin.dylib | grep "T "

The stuff with a capital T from nm are code symbols in the global namespace. If you make a plugin DLL that has a lot of those, your code may not operate if there are other plugins already loaded.



What this means is: under normal operation, the linker may export dynamic library symbols out of a static library you link against. In other words, if you link against libpng.a, you may end up having your DLL export all of the symbols of libpng! If you aren't the first dynamic library to load, the version of libpng you get may not be the static one you asked for.


This behavior is astonishing at best, but unfortunately it is, again, the default: if the static library didn't specifically set its symbols to hidden, you get "leakage" of static library symbols out of the client shared library. Unfortunately, from my experience this kind of leakage happens all of the time. With X-Plane we statically link libcurl, libfreetype and libpng, and all three have their symbols marked globally by default. These are ./configure based libraries and we don't want to start second-guessing their build decisions. Unfortunately the code tends to be marked up to build the right API in "shared library" mode but not static mode.


You can see this behavior using nm -m on OS X or objdump -t on Linux.







#### Static Libraries: Not So Static

In the Unix world, the .a (static archive) format is basically a collection of .o files with some header info to optimize when the code is linked. .o files retain the hidden/visible attribute information that is used by the linker to export symbols out of a dynamic library.What this means is: under normal operation, the linker may export dynamic library symbols out of a static library you link against. In other words, if you link against libpng.a, you may end up having your DLL export all of the symbols of libpng! If you aren't the first dynamic library to load, the version of libpng you get may not be the static one you asked for.

This behavior is astonishing at best, but unfortunately it is, again, the default: if the static library didn't specifically set its symbols to hidden, you get "leakage" of static library symbols out of the client shared library. Unfortunately, from my experience this kind of leakage happens all of the time. With X-Plane we statically link libcurl, libfreetype and libpng, and all three have their symbols marked globally by default. These are ./configure based libraries and we don't want to start second-guessing their build decisions. Unfortunately the code tends to be marked up to build the right API in "shared library" mode but not static mode.

You can see this behavior using nm -m on OS X or objdump -t on Linux.

#### Working Around Library Leak

Someday we may reach a point where all Unix static libraries keep their symbols "hidden" for dynamic library purposes, but until then there is something a DLL can do to work around this problem: use an explicit list of symbol exports.

Using an explicit list of symbol exports is often considered annoying when an API has a large set of public entry points; usually attributes marking specific functions are preferred. The advantage of an "official list" at link time is that the linker hides

*everything*except that list, and if any static libraries have globally visible symbols, their absence from the master fixes the problem.#### Addendum: What About Namespacing?

Both Linux and OS X have over time developed ways to cope with the flat namespace problem.

On OS X, a dynamic library can be linked with a two-level namespace. The symbol is resolved against both the name of the providing dylib and the symbol itself. The result is that symbols come only from the dylibs where you thought they would come from. If at link time symbol A comes from library X, library X is the only place where it will be provided in the future. (This is the semantics Windows developers are used to.)

On Linux, library APIs can contain version information; as far as I can tell this works by "decorating" symbols with a named library version (e.g. @@GLIBC_2.0). When the ABI is changed, symbols cannot conflict between versions, and in theory this may also protect against cross-talk between libraries since the version symbol has some kind of short universal library identifier. I have found almost no documentation on library versioning; if anyone has a good Linux link I'll add it to this post.

X-Plane's plugin system does not use either of these mechanisms because the plugin system is older than both of them. (Technically on OS X two-level namespaces are older than the plugin system, but the plugin system is older than @loader_path, which is a requirement for strict linking of a dylib in the SDK.) Thus we are stuck with the global namespace and find ourselves trying to force people to keep their symbols to themselves.

http://www.akkadia.org/drepper/dsohowto.pdf

ReplyDeleteBen,






ReplyDeleteon OSX the 'trick' of using --version-script won't work because OSX uses ld.

What I did on OSX to only export the required symbols was this :

On gcc I pass in the option -exported_symbols_list xplanesymbols.symbols

Where xplanesymbols.symbols is a filename with the following contents:

_XPlugin*

this will ensure that only the _XPlugin symbols are exported.

That's what we do too - I'm not sure whether our docs reflect this right now - it's always a battle to keep the wiki updated. My work was also limited to X-Code 3 ... I don't know how much stuff changed for X-Code 4 and 5.

ReplyDelete