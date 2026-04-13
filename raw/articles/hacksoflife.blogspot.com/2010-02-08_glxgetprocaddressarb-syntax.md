---
title: glXGetProcAddressARB Syntax
url: http://hacksoflife.blogspot.com/2010/02/glxgetprocaddressarb-syntax.html
author: Benjamin Supnik
published: '2010-02-08'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

void (*glXGetProcAddressARB(const GLubyte *procName))();Wha? Well, fortunately when you read the spec you'll note that they're just being clever...that's very strange C for

typedef void (*GLfunction)();In other words, unlike all other operating systems, which define the returned type of a proc query as a void *, GLX typedefs it as a pointer to a function taking no arguments and returning nothing.

extern GLfunction glXGetProcAddressARB(const GLubyte *procName);

Why this is useful is beyond me, but if you are like us and call one of wgl, AGL, or GLX, you may have to cast the return of glXGetProcAddressARB to (void *) to make it play nice with the other operating systems.

Well, I can tell you why this is useful, however, I will have to go into greater detail here.




ReplyDeleteSome architectures strictly distinguish between "code" and "data" in memory, e.g. where it is located, how it is laid out, how it is accessed, and so on. A void* pointer is a data pointer, the C standard guarantees that it can be used as a pointer to any data located in memory, regardless of its real type. So it's perfectly save to cast any data to void* and void* to any data. Actually not even an explicit cast is required. You can assign any pointer to a void* variable and you can assign any void* pointer to any other pointer variable without a cast.

Functions are no data, though, they are code. A function pointer is no data pointer, it's a code pointer. The C standard nowhere guarantees that code and data pointers have the same size! Now think of an architecture where code pointers are "bigger" than data pointers, e.g. code 32, data 24 or code 40, data 32 or maybe even code 36, data 27 (9-Bit architecture). Assigning a code pointer to a data pointer on those architectures will cause the code pointer to be truncated and thus possibly corrupted if the higher bits were not all zero. Architectures like this did really exist in the past; though this was long before the breakthrough of the consumer PCs.

By defining the return value of glXGetProcAddressARB as a function pointer, this code becomes "ultra portable" as it will even work correctly on architectures where void* and function pointers have different sizes. Not that this would the case on any platform Linux currently supports, not even on the rather exotic ones. Casting a function pointer to another function pointer is always perfectly save, as both are function pointers.