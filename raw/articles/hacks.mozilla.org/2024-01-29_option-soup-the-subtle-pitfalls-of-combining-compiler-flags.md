---
title: 'Option Soup: the subtle pitfalls of combining compiler flags – Mozilla Hacks
  - the Web developer blog'
url: https://hacks.mozilla.org/2024/01/option-soup-the-subtle-pitfalls-of-combining-compiler-flags/
author: Serge Guelton
published: '2024-01-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Firefox development uncovers many cross-platform differences and unique features of its combination of dependencies. Engineers working on Firefox regularly overcome these challenges and while we can’t detail all of them, we think you’ll enjoy hearing about some so here’s a sample of a recent technical investigation.*

During the Firefox 120 beta cycle, [a new crash signature appeared on our radars with significant volume](https://bugzilla.mozilla.org/show_bug.cgi?id=1861365).

At that time, the distribution across operating systems revealed that more than 50% of the crash volume originates from Ubuntu 18.04 LTS users.

The main process crashes in a `CanvasRenderer`

thread, with the following call stack:

0 firefox std::locale::operator= 1 firefox std::ios_base::imbue 2 firefox std::basic_ios<char, std::char_traits<char> >::imbue 3 libxul.so sh::InitializeStream<std::__cxx11::basic_ostringstream<char, std::char_traits<char>, std::allocator<char> > > /build/firefox-ZwAdKm/firefox-120.0~b2+build1/gfx/angle/checkout/src/compiler/translator/Common.h:238 3 libxul.so sh::TCompiler::setResourceString /build/firefox-ZwAdKm/firefox-120.0~b2+build1/gfx/angle/checkout/src/compiler/translator/Compiler.cpp:1294 4 libxul.so sh::TCompiler::Init /build/firefox-ZwAdKm/firefox-120.0~b2+build1/gfx/angle/checkout/src/compiler/translator/Compiler.cpp:407 5 libxul.so sh::ConstructCompiler /build/firefox-ZwAdKm/firefox-120.0~b2+build1/gfx/angle/checkout/src/compiler/translator/ShaderLang.cpp:368 6 libxul.so mozilla::webgl::ShaderValidator::Create /build/firefox-ZwAdKm/firefox-120.0~b2+build1/dom/canvas/WebGLShaderValidator.cpp:215 6 libxul.so mozilla::WebGLContext::CreateShaderValidator const /build/firefox-ZwAdKm/firefox-120.0~b2+build1/dom/canvas/WebGLShaderValidator.cpp:196 7 libxul.so mozilla::WebGLShader::CompileShader /build/firefox-ZwAdKm/firefox-120.0~b2+build1/dom/canvas/WebGLShader.cpp:98

At first glance, we want to blame WebGL. The C++ standard library functions cannot be at fault, right?

But when looking at the WebGL code, the crash occurs in the perfectly valid lines of C++ summarized below:

std::ostringstream stream; stream.imbue(std::locale::classic());

This code should never crash, and yet it does. In fact, taking a closer look at the stack gives a first lead for investigation:

Although we crash into functions that belong to the C++ standard library, these functions appear to live in the firefox binary.

This is an unusual situation that never occurs with official builds of Firefox.

It is however very common for distribution to change the configuration settings and apply downstream patches to an upstream source, no worries about that.

Moreover, there is only a single build of Firefox Beta that is causing this crash.

We know this thanks to a unique identifier associated with any ELF binary.

Here, if we choose any specific version of Firefox 120 Beta (such as 120b9), the crashes all embed the same unique identifier for firefox.

Now, how can we guess what build produces this weird binary?

A useful user comment mentions that they regularly experience this crash since updating to `120.0~b2+build1-0ubuntu0.18.04.1`.

And by looking for this build identifier, we quickly reach [the Firefox Beta PPA](https://launchpad.net/~mozillateam/+archive/ubuntu/firefox-next).

Then indeed, we are able to reproduce the crash by installing it in a Ubuntu 18.04 LTS virtual machine: it occurs when loading any WebGL page!

With the binary now at hand, running `nm -D ./firefox`

confirms the presence of several symbols related to libstdc++ that live in the text section (`T`

marker).

Templated and inline symbols from libstdc++ usually appear as weak (`W`

marker), so there is only one explanation for this situation: firefox has been statically linked with libstdc++, probably through `-static-libstdc++`

.

Fortunately, the build logs are available for all Ubuntu packages.

After some digging, we find [the logs for the 120b9 build](https://launchpadlibrarian.net/697121043/buildlog_ubuntu-bionic-amd64.firefox_120.0~b9+build1-0ubuntu0.18.04.1_BUILDING.txt.gz), which indeed contain references to `-static-libstdc++`

.

But why?

Again, everything is well documented, and thanks to well trained digging skills we reach [a bug report](https://bugs.launchpad.net/ubuntu/+source/firefox/+bug/1856861) that provides interesting insights.

Firefox requires a modern C++ compiler, and hence a modern libstdc++, which is unavailable on old systems like Ubuntu 18.04 LTS.

The build uses `-static-libstdc++`

to close this gap.

This just explains the weird setup though.

What about the crash?

Since we can now reproduce it, we can launch Firefox in a debugger and continue our investigation.

When inspecting the crash site, we seem to crash because `std::locale::classic()`

is not properly initialized.

Let’s take a peek at the implementation.

const locale& locale::classic() { _S_initialize(); return *(const locale*)c_locale; }

`_S_initialize()`

is in charge of making sure that `c_locale`

will be properly initialized before we return a reference to it.

To achieve this, `_S_initialize()`

calls another function, `_S_initialize_once()`

.

void locale::_S_initialize() { #ifdef __GTHREADS if (!__gnu_cxx::__is_single_threaded()) __gthread_once(&_S_once, _S_initialize_once); #endif if (__builtin_expect(!_S_classic, 0)) _S_initialize_once(); }

In `_S_initialize()`

, we first go through a wrapper for `pthread_once()`

: the first thread that reaches this code consumes `_S_once`

and calls `_S_initialize_once()`

, whereas other threads (if any) are stuck waiting for `_S_initialize_once()`

to complete.

This looks rather fail-proof, right?

There is even an extra direct call to `_S_initialize_once()`

if `_S_classic`

is still uninitialized after that.

Now, `_S_initialize_once()`

itself is rather straightforward: it allocates `_S_classic`

and puts it within `c_locale`

.

void locale::_S_initialize_once() throw() { // Need to check this because we could get called once from _S_initialize() // when the program is single-threaded, and then again (via __gthread_once) // when it's multi-threaded. if (_S_classic) return; // 2 references. // One reference for _S_classic, one for _S_global _S_classic = new (&c_locale_impl) _Impl(2); _S_global = _S_classic; new (&c_locale) locale(_S_classic); }

The crash looks as if we never went through `_S_initialize_once()`

, so let’s put a breakpoint there and see what happens.

And just by doing this, we already notice something suspicious.

We do reach `_S_initialize_once()`

, but not within the firefox binary: instead, we only ever reach the version exported by liblgpllibs.so.

In fact, liblgpllibs.so is also statically linked with libstdc++, such that firefox and liblgpllibs.so both embed and export their own `_S_initialize_once()`

function.

By default, *symbol interposition* applies, and `_S_initialize_once()`

should always be called through the procedure linkage table (PLT), so that every module ends up calling the same version of the function.

If symbol interposition were happening here, we would expect that liblgpllibs.so would reach the version of _S_initialize_once() exported by firefox rather than its own, because firefox was loaded first.

So maybe there is no symbol interposition.

This can occur when using `-fno-semantic-interposition`

.

Each version of the standard library would live on its own, independent from the other versions.

But neither the Firefox build system nor the Ubuntu maintainer seem to pass this flag to the compiler.

However, by looking at the disassembly for `_S_initialize()`

and `_S_initialize_once()`

, we can see that the exported global variables (`_S_once`

, `_S_classic`

, `_S_global`

) **are** subject to symbol interposition:

These accesses all go through the global offset table (GOT), so that every module ends up accessing the same version of the variable.

This seems strange given what we said earlier about `_S_initialize_once()`

.

Non-exported global variables (`c_locale`

, `c_locale_impl`

), however, are accessed directly without symbol interposition, as expected.

We now have enough information to explain the crash.

When we reach `_S_initialize()`

in liblgpllibs.so, we actually consume the `_S_once`

that lives in firefox, and initialize the `_S_classic`

and `_S_global`

that live in firefox.

But we initialize them with pointers to well initialized variables `c_locale_impl`

and `c_locale`

that live in liblgpllibs.so!

The variables `c_locale_impl`

and `c_locale`

that live in firefox, however, remain uninitialized.

So if we later reach `_S_initialize()`

in firefox, everything looks as if initialization has happened.

But then we return a reference to the version of `c_locale`

that lives in firefox, and this version has never been initialized.

Boom!

Now the main question is: why do we see interposition occur for `_S_once`

but not for `_S_initialize_once()`

?

If we step back for a minute, there is a fundamental distinction between these symbols: one is a function symbol, the other is a variable symbol.

And indeed, the Firefox build system uses the `-Bsymbolic-function`

flag!

The ld man page describes it as follows:

-Bsymbolic-functions When creating a shared library, bind references to global function symbols to the definition within the shared library, if any. This option is only meaningful on ELF platforms which support shared libraries.

As opposed to:

-Bsymbolic When creating a shared library, bind references to global symbols to the definition within the shared library, if any. Normally, it is possible for a program linked against a shared library to override the definition within the shared library. This option is only meaningful on ELF platforms which support shared libraries.

Nailed it!

The crash occurs because this flag makes us use a weird variant of symbol interposition, where symbol interposition happens for variable symbols like `_S_once`

and `_S_classic`

but not for function symbols like `_S_initialize_once()`

.

This results in a mismatch regarding how we access global variables: exported global variables are unique thanks to interposition, whereas every non-interposed function will access its own version of any non-exported global variable.

With all the knowledge that we have now gathered, it is easy to write a reproducer that does not involve any Firefox code:

/* main.cc */ #include <iostream> extern void pain(); int main() { pain(); std::cout << "[main] " << std::locale::classic().name() <<"\n"; return 0; } /* pain.cc */ #include <iostream> void pain() { std::cout << "[pain] " << std::locale::classic().name() <<"\n"; } # Makefile all: $(CXX) pain.cc -fPIC -shared -o libpain.so -static-libstdc++ -Wl,-Bsymbolic-functions $(CXX) main.cc -fPIC -c -o main.o $(CC) main.o -fPIC -o main /usr/lib/gcc/x86_64-redhat-linux/13/libstdc++.a -L. -Wl,-rpath=. -lpain -Wl,-Bsymbolic-functions ./main clean: $(RM) libpain.so main

Understanding the bug is one step, and solving it is yet another story.

Should it be considered a libstdc++ bug that the code for locales is not compatible with `-static-stdlibc++ -Bsymbolic-functions`

?

It feels like combining these flags is a very nice way to dig our own grave, and [that seems to be the opinion of the libstdc++ maintainers indeed](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=112551).

Overall, perhaps the strangest part of this story is that this combination did not cause any trouble up until now.

Therefore, we suggested to the maintainer of the package to stop using `-static-libstdc++`

.

There are other ways to use a different libstdc++ than available on the system, such as using dynamic linking and setting an `RPATH`

to link with a bundled version.

[Doing that](https://bugzilla.mozilla.org/show_bug.cgi?id=1861365#c11) allowed them to successfully deploy a fixed version of the package.

A few days after that, with the official release of Firefox 120, we noticed a very significant bump in volume for the same crash signature. Not again!

This time the volume was coming exclusively from users of NixOS 23.05, and it was huge!

After we shared the conclusions from our beta investigation with them, the maintainers of NixOS were able to [quickly associate](https://github.com/NixOS/nixpkgs/issues/269571#issuecomment-1825836670) the crash with [an issue that had not yet been backported ](https://github.com/NixOS/nixpkgs/pull/192459)for 23.05 and was causing the compiler to behave like `-static-libstdc++`

.

To avoid such mess in the future, [we added detection for this particular setup in Firefox’s configure](https://phabricator.services.mozilla.com/rMOZILLACENTRAL0930954b46bbc315ffcb92658bde0efc2945b04b).

We are grateful to the people who have helped fix this issue, in particular:

- Rico Tzschichholz (ricotz) who quickly fixed the Ubuntu 18.04 LTS package, and Amin Bandali (bandali) who provided help on the way;
- Martin Weinelt (hexa) and Artturin for their prompt fixes for the NixOS 23.05 package;
- Nicolas B. Pierron (nbp) for helping us get started with NixOS, which allowed us to quickly share useful information with the NixOS package maintainers.