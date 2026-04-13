---
title: Why you should use LLVM's ArrayRef
url: https://anteru.net/blog/2012/why-you-should-use-llvm-s-arrayref
published: '2012-09-19'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

If you are developing for C++, one major source of errors are out-of-bounds accesses when passing around pointers. Even though these pointers come from locations where the buffer size is typically known, errors occur due to the following problem: When you pass around a plain pointer, all information about the size of the buffer is lost at the usage location. That makes it impossible to verify that the buffer has the correct size when writing through it. Luckily, the solution for this is really simple:LLVM’s [ArrayRef](http://llvm.org/docs/ProgrammersManual.html#dss_arrayref).

An array reference is a simple structure which bundles a pointer together with the size of the memory pointed to. The simplest implementation is:

```
template <typename T>
struct ArrayRef
{
T p;
int64 size;
};
```


Keeping the size along with the pointer immediately removes a large class of errors. This brings C++ closer to C# and Java, where all arrays known their bounds, without enforcing the clients to use a particular container class.

As a side bonus, it also decouples the functions from the actual data representation. Instead of forcing clients to pass a standard container, or a pair of iterators, array references handle all those cases transparently. This also works for output buffers by using *mutable* array references which clearly express that this pointer is an output pointer. This removes another possible source of confusion.

Over the last months, I have started to replace raw pointers to buffers in my framework with array references and validation. It didn’t take long before I found the first bunch of bugs where a buffer was too small or too large. It might sound a bit counter-intuitive at first to check if an output buffer is too large, but this turned out to be a useful check. Most of the time, the caller simply overestimates the required memory, so this is a good point to provide an accessor or utility function to get the exact memory and reduce temporary storage requirements. Otherwise, the caller is probably creating a slice from a larger memory buffer, and in that case, it’s usually just as simple to compute the slice size precisely. The only case I found where I only check if the buffer is larger or equal is for compression algorithms.

If you haven’t seen or used array references, it’s time to give them a try and practice safer C++.