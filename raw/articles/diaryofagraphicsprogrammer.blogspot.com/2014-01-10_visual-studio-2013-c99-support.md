---
title: Visual Studio 2013 - C99 support
url: http://diaryofagraphicsprogrammer.blogspot.com/2014/01/visual-studio-2013-c99-support.html
author: Wolfgang Engel
published: '2014-01-10'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I think using C99 in game development could be useful for large teams, especially if they are distributed over several locations.











So I thought I look a little bit closer on the support of C99 in Visual Studio 2013 (we also use VS 2013 with C99 now in my UCSD class).

The new features that are support in VS 2013 are:

**New features in 2013**

- variable decls

- _Bool

- compound literals

- designated initializers

**Already available:**

variadic macros, long long, __pragma, __FUNCTION__, and __restrict

**What is missing:**

- variable-length arrays (VLAs)

- Reserved keywords in C99

C99 has a few reserved keywords that are not recognized by C++:

restrict

_Bool -> this is now implemented ... see above

_Complex

_Imaginary

_Pragma

- restrict keyword

C99 supports the restrict keyword, which allows for certain optimizations involving pointers. For example:

void copy(int *restrict d, const int *restrict s, int n)

{

while (n-- > 0)

*d++ = *s++;

}

C++ does not recognize this keyword.

A simple work-around for code that is meant to be compiled as either C or C++ is to use a macro for the restrict keyword:

#ifdef __cplusplus

#define restrict /* nothing */

#endif

(This feature is likely to be provided as an extension by many C++ compilers. If it is, it is also likely to be allowed as a reference modifier as well as a pointer modifier.)

**Don't know if it is in there:**

- hexadecimal floating-point literals like

float pi = 0x3.243F6A88p+03;

- C99 adds a few header files that are not included as part of the standard C++ library, though:

<complex.h>

<fenv.h>

<inttypes.h>

<stdbool.h>

<stdint.h>

<tgmath.h>




<complex.h>

<fenv.h>

<inttypes.h>

<stdbool.h>

<stdint.h>

<tgmath.h>

**References**

- What was added in June 2013 blog
[http://blogs.msdn.com/b/vcblog/archive/2013/06/27/what-s-new-for-visual-c-developers-in-vs2013-preview.aspx](http://blogs.msdn.com/b/vcblog/archive/2013/06/27/what-s-new-for-visual-c-developers-in-vs2013-preview.aspx) - C99 library support in Visual Studio 2013
[http://blogs.msdn.com/b/vcblog/archive/2013/07/19/c99-library-support-in-visual-studio-2013.aspx](http://blogs.msdn.com/b/vcblog/archive/2013/07/19/c99-library-support-in-visual-studio-2013.aspx) - Incompatibilities between C99 and C++98
[http://david.tribble.com/text/cdiffs.htm](http://david.tribble.com/text/cdiffs.htm)

## 3 comments:

Is this a petition? If so, I'm signing it!


-- Mike Acton, Engine Director, Insmoniac Games

+1 for c99 support


( note that they have their c/c++ __restrict http://msdn.microsoft.com/en-us/library/5ft82fed.aspx own restrict equivalent)

Post a Comment