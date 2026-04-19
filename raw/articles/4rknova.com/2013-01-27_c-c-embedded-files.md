---
title: C/C++ Embedded Files
url: https://www.4rknova.com/blog/2013/01/27/cpp-embedded-files
author: Nikolaos Papadopoulos
published: '2013-01-27'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

Sometimes it is desirable to embed resource files in c or c++ programs. There are many ways to go about it but in most cases you must convert the files with external tools or scripts.

# Using external tools

For image files, image-magick can be used:

$ imagick input.png output.h

Another common tool that can convert all types of files is xxd.

$ xxd -i input.whatever output.h

While the above methods are perfectly valid, some extra dependencies are added to the build process.

# Using the preprocessor

One interesting way to do this for plain ascii files (eg. shaders) can be found in Bullet's MiniCL example programs and more specifically in lines 31-33 of [MiniCL_VectorAdd.cpp](https://goo.gl/pcRVR)

A preprocessor macro is defined and a string declaration is placed before the file inclusion directive.

```
[...]
#define STRINGIFY(A) #A
char *fsource =
#include "file.ext"
[...]
```


Then the external ascii file is wrapped in the STRINGIFY block.

```
STRINGIFY (
[...]
)
```


Note that the above method still requires that the file is edited to add the macro block but the operation is rundimentary and usually relatively simple to automate.

# Using ASM

Another way is to use an assembly code block that emdeds the data to the .rodata sections of the final binary.

```
#include <stdio.h>
#define STR2(x) #x
#define STR(x) STR2(x)
#define INCBIN(name, file) \
__asm__(".section .rodata\n" \
".global incbin_" STR(name) "_start\n" \
".type incbin_" STR(name) "_start, @object\n" \
".balign 16\n" \
"incbin_" STR(name) "_start:\n" \
".incbin \"" file "\"\n" \
\
".global incbin_" STR(name) "_end\n" \
".type incbin_" STR(name) "_end, @object\n" \
".balign 1\n" \
"incbin_" STR(name) "_end:\n" \
".byte 0\n" \
); \
extern const __attribute__((aligned(16))) void* incbin_ ## name ## _start; \
extern const void* incbin_ ## name ## _end; \
INCBIN(foobar, "binary.bin");
int main()
{
printf("start = %p\n", &incbin_foobar_start);
printf("end = %p\n", &incbin_foobar_end);
printf("size = %zu\n", (char*)&incbin_foobar_end - (char*)&incbin_foobar_start);
printf("first byte = 0x%02x\n", ((unsigned char*)&incbin_foobar_start)[0]);
}
```


This is obviously a platform specific solution that will not work on all platforms.