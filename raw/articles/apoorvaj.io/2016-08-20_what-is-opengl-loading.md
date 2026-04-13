---
title: What is OpenGL loading?
url: https://apoorvaj.io/loading-opengl-without-glew
published: '2016-08-20'
source_blog: apoorvaj.io
source_site: https://apoorvaj.io/
category: graphics
fetched: '2026-04-13'
---

This article is a result of my experiences and experiments with using
OpenGL for [Papaya](https://github.com/ApoorvaJ/Papaya). My
first few weeks learning OpenGL were challenging, because it was very
different than most of the APIs I had interacted with up to that point.
I’m writing this blog post because it would certainly have helped me a
year ago.

*The complete OpenGL loader code described in this post is located
here.*
Note that the code may change in the future, so the link points to the
file as it existed at the time when this post was written. This code was
written to cover Papaya’s usage of OpenGL. You may need to add further
functions/constants manually depending on your program’s usage.

What follows, is hopefully a beginner-friendly explanation.

OpenGL is an API specification. It is *not* a library. This
means that the actual implementation behind the API varies based on your
GPU hardware, your operating system, and your installed graphics
driver.

The OpenGL specification has a lot of different functions defined in it, and the OpenGL specification gets updated periodically. The graphics driver on your machine may not (and probably does not) support all of these functions. The subset of the spec that is supported will depend on your GPU hardware capabilities and the GPU vendor’s support for any given API.

This is the reason that all OpenGL functions aren’t statically
declared in a header file. Furthermore, static linkage to a library is
impossible because target machines for your application will have a
wildly varying set of OpenGL implementations. On Windows machines, the
OpenGL implementation will be in the form a DLL. On 64-bit Windows, the
64-bit dll will be located in
`C:\Windows\system32\opengl32.dll`

(confusing nomenclature
ftw). This DLL is a component of the graphics driver, and is shipped
with it.

To recap, most OpenGL functions are not declared in any standardized header file, and they are not linked statically. This is why OpenGL functions can’t just be called out of the box, and need to be declared and loaded explicitly.

[GLEW](http://glew.sourceforge.net/) (OpenGL Extension
Wrangler) is a cross-platform library that declares and loads OpenGL
functions for you. It also has handy run-time checks to see whether a
given machine supports a given OpenGL profile (a profile is a guarantee
that a given configuration supports a certain set of OpenGL
functions).

GLEW is very handy, especially if you are new to OpenGL. It does most of the heavy-lifting for you, and you remain free to call any valid OpenGL function supported on your system.

Most StackOverflow questions regarding OpenGL loading, advise the
original questioner to simply stop doing custom loading and move to
GLEW. Even the official OpenGL wiki [strongly
advises](https://www.opengl.org/wiki/Load_OpenGL_Functions) you to use an OpenGL loading library.

While automatic loading libraries are handy, they do have some significant disadvantages. I will restrict my critique to GLEW in this particular article, but the same disadvantages generally do apply to other kinds of OpenGL loaders as well.

You can use GLEW in two ways:

Code complexity is a cost too, and is also an axis on which a program should be optimized. This idea has grown on me over time, and I now try to optimize code along its complexity axis, in addition to the performance axis. Code that you will never use in any library is basically dead code, and does increase code complexity needlessly.

Here’s a comparison of build times and the lines of code before and after I removed GLEW from Papaya.

| Metric | GLEW | No GLEW |
|---|---|---|
| Full rebuild time | 6.9 sec | 5.5 sec |
| Lines of code (cloc) | 62820 loc | 25427 loc |

*Build times were measured using the Linux time
command on a laptop with an SSD, and are an average of 5 passes each.
Your milage may vary.*

I ran `cloc`

on just the GLEW folder, and it totaled
37,393 lines of code. That is ridiculously large. To put things into
perspective, the rest of my application - platform code, image
libraries, UI libraries, everything else - totaled 25,427 lines of code.
*Just the GLEW code was larger than the rest of my
application.*

This primarily happens because GLEW has code to handle *all*
OpenGL function APIs, where as I use a very small percentage of
them.

My replacement code for GLEW is only ~180 lines long, and works on Windows and Linux. Mac support isn’t present at the moment, but should be very trivial to add.

Build times have also reduced by over a second.

In this section, I will describe only the interesting excerpts of the
code. *To reiterate, you can view the full source code here.*

This code is based on Fabian Giesen’s [Bink
GL extension loader](https://gist.github.com/rygorous/16796a0c876cf8a5f542caddb55bce8a). I have added platform-specific code, and
packaged it as a single-header file.

#if defined(__linux__)
#include <dlfcn.h>
#define GLDECL // Empty define
#define PAPAYA_GL_LIST_WIN32 // Empty define
#endif // __linux__
#if defined(_WIN32)
#include <windows.h>
#define GLDECL WINAPI
#define GL_ARRAY_BUFFER 0x8892
#define GL_ARRAY_BUFFER_BINDING 0x8894
...
typedef char GLchar;
typedef ptrdiff_t GLintptr;
typedef ptrdiff_t GLsizeiptr;
#define PAPAYA_GL_LIST_WIN32 \
/* ret, name, params */ \
GLE(void, BlendEquation, GLenum mode) \
GLE(void, ActiveTexture, GLenum texture) \
/* end */
#endif // _WIN32


In the platform-specific header, we include the files needed for
getting loading dynamic library binaries - `dlfcn.h`

on POSIX
systems, and `windows.h`

on Windows. We also define the
calling convention prefix `GLDECL`

here, which is primarily
needed for the loader to work correctly on 32-bit Windows.

We include the header file `GL/gl.h`

in this loader, but
this file is usually different on Windows and Linux. The Windows SDK
ships with an older version (OpenGL 1.1) of the file, and hence does not
contain all of the typedefs, constants and function declarations that
are present in the Linux version of the same file. These need to be
added manually to the Windows-specific part of our header. These
constants and functions can be found in the [glext.h file](https://www.opengl.org/registry/api/GL/glext.h).
We can choose to just include that entire file as well, but I have
currently elected not to go that route.

#define PAPAYA_GL_LIST \
/* ret, name, params */ \
GLE(void, AttachShader, GLuint program, GLuint shader) \
GLE(void, BindBuffer, GLenum target, GLuint buffer) \
...
/* end */
#define GLE(ret, name, ...) \
typedef ret GLDECL name##proc(__VA_ARGS__); \
extern name##proc * gl##name;
PAPAYA_GL_LIST
PAPAYA_GL_LIST_WIN32
#undef GLE


This is the bulk of the loader. We declare all the GL functions we
want to use in the PAPAYA_GL_LIST macro. These function prototypes can
be found in the OpenGL registry, or on a website like [docs.gl](http://docs.gl). These are listed in the format
`GLE(return type, function name, params)`

. We don’t include
the “gl” prefix of the function name, purely for cosmetic reasons.

Note the PAPAYA_GL_LIST and GLE() macros. I took this directly from the Bink GL loader, and it is a very nifty pattern for defining macro iterators.

Here, this iterator macro is used to typedef function pointers, and
then to declare extern function pointers. These same function pointers
are later declared in the implementation section of our file. After we
include this header file, we can call OpenGL functions such as
`glAttachShader(...)`

without getting compilation errors.

Finally, the [gl_lite_init()](https://github.com/ApoorvaJ/Papaya/blob/3808e39b0f45d4ca4972621c847586e4060c042a/src/libs/gl_lite.h#L130)
function contains the platform-specific code to load the OpenGL dynamic
library, and then get the function pointers from them. Both - POSIX and
Windows - follow the same basic steps:

`opengl32.dll`

, and
in Linux, it is in the `libGL.so`

(shared object) file. The
library loading function returns an opaque handle.GLEW is handy, but does have its disadvantages. Writing your own GL
loader isn’t rocket science, and will result in faster compilation,
easier builds, and a smaller code base. This isn’t a library as much as
a code snippet, and you will probably need to customize the code to fit
your needs. You can view the full code described in this article [here](https://github.com/ApoorvaJ/Papaya/blob/3808e39b0f45d4ca4972621c847586e4060c042a/src/libs/gl_lite.h).
The file is public domain, so feel free to use it wherever.