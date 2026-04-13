---
title: A Compiler Bug
url: https://thenumb.at/Compiler-Bug/
published: '2021-12-26'
source_blog: Max Slater
source_site: https://thenumb.at/
category: graphics
fetched: '2026-04-13'
---

# A Compiler Bug

While I was working on [Dawn](https://thenumb.at/projects/dawn), I ran into a curious bug in the Visual Studio 2019 C++ compiler. I reported it to the bug tracker, where it was confirmed to be an interference analysis issue. It was eventually fixed nearly a year later in 2020. Today, let’s investigate what the issue really was.

The problem arose upon implementing a Perlin noise type for procedural solid texturing. My type just so happened to include a 4-kilobyte array of pre-initialized random data, and this precise size caused writes to the data to interfere with a preceding struct member. The resulting bug ended up bricking the output of my path tracer—but only with optimizations enabled!

Assuming there was some bug in my code, I was able to narrow down the problem to an unintended write just proceeding the random data array. However, I could not figure what exactly was causing the write. These kind of bugs (particularly those that only show up with optimizations enabled) are typically symptoms of undefined behavior, but there was no undefined behavior here. Hence, I started stripping out pieces of my code until I could minimally reproduce the issue. Eventually, I checked whether my code worked as expected in GCC and Clang, and it did: the issue was a MSVC compiler bug that resulted in broken code-gen.

I was able to capture the issue in the following example:

```
#include <cstdint>
#include <cstdio>
struct data {
uint8_t _data[4095] = {};
};
struct container {
uint8_t type = 1;
data n;
static container make() {
container ret;
printf("Before: %d\n", (int)ret.type);
ret.n = data{};
printf("After: %d\n", (int)ret.type);
return ret;
}
container() {}
container(const container& o) {}
};
void func(container c) {}
void main() {
func(container::make());
}
```


Which resulted in the following output when compiled via `cl bug.cpp -O2`

:

```
Before: 1
After: 0
```


My example seemed weirdly specific. Each of the following changes would correct the output:

- Changing
`_data[4095]`

to`_data[4094]`

or smaller - Removing the container copy constructor
- Removing the call to
`func()`

- Adding an unrelated call to
`container::make()`

before`func()`


With the help of [compiler explorer](https://godbolt.org/z/5a9v99988), we can figure out what the issue was, as well as what changed after the fix. Bisecting the supported compiler versions shows that the assembly output has been quite stable over time, only changing with the jump from version 19.24 to 19.25.

Examining the output (x86, `-O2`

), we will find that the only relevant code is in `main`

—all function calls have all been inlined. Comparing between the two compiler versions reveals near-identical assembly output: the only difference is that the correct version allocates extra stack space, preventing two temporaries from overlapping.

```
$T1 = 32
-- $T2 = 32
++ $T2 = 4128
-- $T3 = 4128
++ $T3 = 8224
main:
; Save registers/allocate stack space
mov [rsp+8], rsi
push rdi
-- mov eax, 8224
++ mov eax, 12320
call __chkstk
sub rsp, rax
; Copy $T3 to $T2
lea rdi, $T2[rsp]
mov ecx, 4096
lea rsi, $T3[rsp]
xor edx, edx
rep movsb
; Create container in $T2 with type = 1
lea rsi, $T2[rsp]
mov r8d, 4095
lea rcx, [rsi+1]
mov [rsi], 1
call memset
; Print $T2->type
movzx edx, [rsi]
lea rcx, OFFSET FLAT:`string'
call printf
; Create temporary data{} in $T1
xor edx, edx
lea rcx, $T1[rsp]
mov r8d, 4095
call memset
; Copy temporary data{} from $T1 to $T2->n
lea rcx, [rsi+1]
mov r8d, 4095
lea rdx, $T1[rsp]
call memcpy
; Print $T2->type
movzx edx, [rsi]
lea rcx, OFFSET FLAT:`string'
call printf
; Deallocate stack space/load registers
-- mov rsi, [rsp+8240]
++ mov rsi, [rsp+12336]
xor eax, eax
-- add rsp, 8224
++ add rsp, 12320
pop rdi
ret 0
```


So, what exactly are these temporaries, and why was the overlap a problem? We can deduce what each temporary means:

`$T1`

: the anonymous`data{}`

created in`container::make`

`$T2`

:`ret`

, created in`container::make`

and passed to`func`

. The same memory is used in both contexts due to[return value optimization and copy elision](https://en.cppreference.com/w/cpp/language/copy_elision)—the copy constructor is never called.`$T3`

: seemingly useless, uninitialized storage that is copied to`$T2`

before it is overwritten. Was this left over from before copy elision but not omitted?

Referring back to the assembly listing, we can see that the broken version assigns `$T1`

and `$T2`

to the same stack location!

| Temporary | Type | Location |
|---|---|---|
| $T1 | data | 32-4127 |
| $T2 | container | 32-4128 |
| $T3 | container | 4128-8224 |

Hence, the code overwrites `$T2->type`

when initializing `data{}`

to zero. But that’s not all: `memcpy`

is used to copy from `$T1`

to `$T2->n`

, which is undefined behavior because the source and destination ranges overlap.

The corrected version allocates separate space for the two temporaries, and everything works as expected.

| Temporary | Type | Location |
|---|---|---|
| $T1 | data | 32-4127 |
| $T2 | container | 4128-8224 |
| $T3 | container | 8224-12320 |

Unfortunately, explaining *what* happened gives us little insight into *why*. Somehow, my code structure gave the compiler the false impression that `ret`

and `data{}`

were not alive at the same time, despite one being copied to the other. Given the context, I would guess the combination of inlining and copy elision caused confusion over stack ownership—but we might never know for sure.