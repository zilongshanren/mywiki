---
title: null program
url: https://nullprogram.com/blog/2024/10/03/
published: '2024-10-03'
source_blog: null program
source_site: https://nullprogram.com
category: graphics
fetched: '2026-04-13'
---

nullprogram.com/blog/2024/10/03/

I’m 18 years late, but [Slim Reader/Writer Locks](https://learn.microsoft.com/en-us/windows/win32/sync/slim-reader-writer--srw--locks) have a fantastic
interface: pointer-sized (“slim”), zero-initialized, and non-allocating.
Lacking cleanup, they compose naturally with [arena allocation](/blog/2023/09/27/).
Sounds like a futex? That’s because they’re built on futexes introduced at
the same time. They’re also complemented by [condition variables](https://learn.microsoft.com/en-us/windows/win32/sync/condition-variables)
with the same desirable properties. My only quibble is that slim locks
[could easily have been 32-bit objects](/blog/2022/10/05/), but it hardly matters. This
article, while treating [Win32 as a foreign interface](/blog/2023/05/31/), discusses a
paper-thin C++ wrapper interface around lock and condition variables, in
[my own style](/blog/2024/04/14/).

If you’d like to see/try a complete, working demonstration before diving
into the details: `demo.cpp`

. We’re going to build this from the
ground up, so let’s establish a few primitive integer definitions:

```
using b32 = signed;
using i32 = signed;
using uz = decltype(0uz);
```


Think of `uz`

as like `uintptr_t`

. This implementation will support both
32-bit and 64-bit targets, and we’ll need it as the basis for locks and
condition variables:

```
enum Lock : uz;
enum Cond : uz;
```


Opaque enums provide additional type safety: They have the properties of
an integer, including trivial destruction, but are distinct types which
compilers forbid mixing with other integers. We can’t, say, accidentally
cross condition variable and lock parameters — my main concern. Aside from
zero-initialization, we do not actually care about the values of these
variables, so enumerators are unnecessary. (Caveat: GDB cannot display
opaque enums, which is slightly irritating.)

The documentation doesn’t explicitly mention zero initialization, but the
official `*_INIT`

constants are defined as zero. That locks in zero at the
ABI level, so we can count on it.

All the functions we’ll need are exported by `kernel32.dll`

. Locks have
two variations on lock/unlock: “exclusive” (write) and “shared” (read).
There are also “try” versions, but I won’t be using them.

```
#define W32(r, p) extern "C" __declspec(dllimport) r __stdcall p noexcept
W32(void, AcquireSRWLockExclusive(Lock *));
W32(void, AcquireSRWLockShared(Lock *));
W32(void, ReleaseSRWLockExclusive(Lock *));
W32(void, ReleaseSRWLockShared(Lock *));
```


Declaring Win32 functions in C++ is a mouthful, and everything must be
written in just the right order, but it’s mostly tucked away in a macro.
Usually there’s a stack discipline to these locks, so an RAII scoped guard
is in order:

```
struct Guard {
Lock *l;
Guard(Lock *l) : l{l} { AcquireSRWLockExclusive(l); }
~Guard() { ReleaseSRWLockExclusive(l); }
};
struct RGuard {
Lock *l;
RGuard(Lock *l) : l{l} { AcquireSRWLockShared(l); }
~RGuard() { ReleaseSRWLockShared(l); }
};
```


Dead simple. (What about [rule of three](https://en.cppreference.com/w/cpp/language/rule_of_three)? Instead of working around
this language design flaw, [reach into the distant future](https://quuxplusone.github.io/blog/2023/05/05/deprecated-copy-with-dtor/) where
it’s been fixed: `-Werror=deprecated-copy-dtor`

.) Usage might look like:

```
struct Example {
Lock lock = {};
i32 value;
};
i32 incr(Example *e)
{
Guard g(&e->lock);
return ++e->value;
}
```


Note the `= {}`

to guarantee the lock is always ready for use. It gets
more interesting with condition variables in the mix. That’s three more
functions:

```
W32(b32, SleepConditionVariableSRW(Cond *, Lock *, i32, b32));
W32(void, WakeAllConditionVariable(Cond *));
W32(void, WakeConditionVariable(Cond *));
```


The last parameter on [SleepConditionVariableSRW](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-sleepconditionvariablesrw) indicates if the
lock was acquired shared. Why do locks have distinct acquire and release
functions while condition variables use a flag for the same purpose? Beats
me. I’ll unfold it into two functions, selected by type, with a default
infinite wait:

```
b32 wait(Cond *c, Guard *g, i32 ms = -1)
{
return SleepConditionVariableSRW(c, g->l, ms, 0);
}
b32 wait(Cond *c, RGuard *g, i32 ms = -1)
{
return SleepConditionVariableSRW(c, g->l, ms, 1);
}
```


Usage might look like:

```
for (RGuard g(&lock); remaining;) {
wait(&done, &g);
}
```


The other side is nothing more than a rename (but could also be
[accomplished through linking](/blog/2023/08/27/)):

```
void signal(Cond *c)
{
WakeConditionVariable(c);
}
void broadcast(Cond *c)
{
WakeAllConditionVariable(c);
}
```


And a couple examples of its usage:

```
if (Guard g(&lock); !--remaining) {
signal(&done);
}
// Or:
Guard g(&lock);
ready = true;
broadcast(&init);
while (remaining) {
wait(&done, &g);
}
```


A satisfying, powerful synchronization interface with hardly any code!