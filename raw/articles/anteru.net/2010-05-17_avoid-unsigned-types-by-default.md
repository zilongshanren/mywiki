---
title: Avoid unsigned types by default
url: https://anteru.net/blog/2010/avoid-unsigned-types-by-default
published: '2010-05-17'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

For some reason or another, unsigned types in C++ are heavily overused. I know that Java doesn’t have them, and many students who learn programming with Java think this is a really serious deficiency which they have to make up by using unsigned types everywhere … however, it turns out, that you will rarely need unsigned types, and in most cases, they do more harm than good.

First of all, there are some cases where you need unsigned types. Pretty much all of these cases can be grouped into two categories:

- Interop: Someone somewhere expects an unsigned value, so you have to convert your stuff at some point. You should try to convert it as late as possible, but with some sanity check. For instance, if you call an API which expects an unsigned size, and you have a signed size in your application, convert only after sanity-checking your signed value!
- I/O: Disk or network I/O often requires the use of unsigned data types, as you typically want to work on the raw bit pattern of the value and not on the actual value. In this case, unsigned types fit and should be used.

Everywhere else, you should really try hard to avoid them. Especially when you design an API, stay away from unsigned types. There’s [a very good article by Scott Meyers](http://www.aristeia.com/Papers/C++ReportColumns/sep95.pdf) on this topic which explains the problems with unsigned types and interfaces. The main problem is that an unsigned type makes error/sanity checking impossible. If you have a function like `memset(void* t, size_t size)`

and a pod like

```
struct pod {
unsigned char flags;
Vector3 coords;
};
```


and you pass on something like `memset(&pod, sizeof (pod) - sizeof (Vector4));`

because you vaguely remembered that pod has a `Vector4`

and a flags field in it, you’re going to clear around 18446744073709551613 bytes worth of data if running on a 64-bit system – with signed types, a quick `assert(size <= 0);`

would have failed with `size == -3`

.

This happens far more often than you would expect. Since I’m trying to use signed types as much as possible, I’ve found lots of lots of places where I can sanity-check values using asserts and pre-condition checks than before. Even for typical use cases like I/O routines (`fwrite`

) or memory stuff (`malloc`

), you can get away with one less bit in practically every case – I don’t remember ever having seen a call which would allocate or write more than 231 elements on a 32-bit machine; let alone 263 elements on a 64-bit machine. So, next time before you start typing unsigned type size, think twice if you’re really ever going to need that extra bit, or whether you are willing to trade it off for error checking.

**Note**: This does not imply that you don’t have to think about valid value ranges. The only help you get from signed types is that overflows are much harder to exploit if you sanitize most values in between. You should however still use things like [SafeInt](http://safeint.codeplex.com/) to make sure your arithmetic stays in range.