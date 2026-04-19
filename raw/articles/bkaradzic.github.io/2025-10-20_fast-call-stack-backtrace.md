---
title: Fast Call-Stack Backtrace
url: https://bkaradzic.github.io/posts/fast-call-stack-backtrace/
author: Branimir Karadžić
published: '2025-10-20'
source_blog: Home | Branimir Karadžić's Home Page
source_site: https://bkaradzic.github.io/
category: graphics
fetched: '2026-04-19'
---

**Table of Contents**

## Introduction

When developing a profiler, memory tracker, or logger, you need to programmatically access the call stack to trace how a program reached the location where a method is called. Operating systems offer APIs for call stack tracing, but these are often too slow for practical real-time use. This article will try to demystify all ways of obtaining call-stack traces on different platforms, and I won’t cover resolving debug symbol names here.

## Fast vs Exact

OS APIs provide “exact” call stack tracing, designed to function reliably in all conditions, including for debugger use. For example, on Windows’ API, [ StackWalk64](https://learn.microsoft.com/en-us/windows/win32/api/dbghelp/nf-dbghelp-stackwalk64) is quite heavy-duty and works in all conditions (exceptions, dynamic libraries, etc.), in or out of process.

For fast call-stack tracing, we prioritize speed over exactness, sacrificing some accuracy. This limits the implementation to our own code, compiled with specific compiler options. We don’t want our “fast” function to allocate any memory or do any OS calls, but we are totally fine with it not being able to work from an exception handler call or walk into an externally compiled library.

We will implement two functions: one for “fast” call-stack tracing and one for “exact” tracing when the fast function yields poor results. Both functions avoid memory allocation, writing call-stack addresses to a user-provided C array. The array size, typically 16–32 stack frames, depends on the application. Users can specify frames to skip to hide tracing function internals.

```
1 /// Capture current callstack fast.
2///
3/// @param[in] _skip Skip top N stack frames.
4/// @param[in] _max Maximum frame to capture.
5/// @param[out] _outStack Stack frames array. Must be at least `_max` elements.
6///
7/// @returns Number of stack frames captured.
8///
9uint32_t getCallStackFast(uint32_t _skip, uint32_t _max, uintptr_t* _outStack);
10
11 /// Capture current callstack with slower but more accurate method.
12///
13/// @param[in] _skip Skip top N stack frames.
14/// @param[in] _max Maximum frame to capture.
15/// @param[out] _outStack Stack frames array. Must be at least `_max` elements.
16///
17/// @returns Number of stack frames captured.
18///
19uint32_t getCallStackExact(uint32_t _skip, uint32_t _max, uintptr_t* _outStack);
```


## Stack Frame Layout

The call stack layout organizes memory for function calls, typically including frames with return addresses, parameters, local variables, and saved registers, growing downward from high to low addresses in most systems. Architectures influence this: x86 and x86-64 use downward growth with 16-byte alignment and registers like RSP for stack pointer, while ARM may support bidirectional growth but defaults downward. Operating systems further shape it via ABIs. Linux employs [System V ABI](https://en.wikipedia.org/wiki/X86_calling_conventions#System_V_AMD64_ABI) with red zones for optimization and guard pages for overflow protection, whereas Windows uses its own calling conventions like fastcall, imposes stricter stack size limits, and integrates features like [Structured Exception Handling (SEH)](https://en.wikipedia.org/wiki/Microsoft-specific_exception_handling_mechanisms) and [Address Space Layout Randomization (ASLR)](https://en.wikipedia.org/wiki/Address_space_layout_randomization) for security, affecting frame unwinding and exception handling across platforms.

Generally, ignoring OS and architecture specifics, the call stack follows a standard layout, and it looks something like this:

```
+-------+ <----- high address
| |
~~~
| |
+-------+
| ... | <---- function arguments
+-------+
| RA | <---- return address saved here
+-------+
| RBP | <---- previous stack frame saved (RBP register on x64)
+-------+
| ... | <---- function local variables
+-------+
| | <---- stack pointer register pointing at this location
+-------+
| |
~~~
| |
+-------+ <----- low address
```


The compiler option to prevent stack frame pointer omission in GCC and Clang is `-fno-omit-frame-pointer`

, and in MSVC, it is `/Oy-`

.

## Cross-platform implementation for GCC and Clang

GCC and Clang provide `__builtin_frame_address`

and `__builtin_return_address`

intrinsics for accessing stack frame and return addresses. Using these, we can implement a cross-platform stack walk for any GCC- or Clang-supported platform. The limitation is that these intrinsics require compile-time constant values.

With this knowledge, we can use C macros to create the following “unrolled” implementation:

```
1 BX_NO_INLINE uint32_t getCallStackGccBuiltin(uint32_t _skip, uint32_t _max, uintptr_t* _outStack)
2 {
3#if BX_COMPILER_GCC || BX_COMPILER_CLANG
4 5 BX_PRAGMA_DIAGNOSTIC_IGNORED_CLANG_GCC("-Wframe-address");
6
7 uint32_t num = 0;
8
9#define RETURN_ADDRESS(_x) \
10 if (num < _max) \
11 { \
12 if (0 < _skip) \
13 { \
14 --_skip; \
15 } \
16 else \
17 { \
18 if (NULL == __builtin_frame_address(_x) ) \
19 { \
20 return num; \
21 } \
22 \
23 void* addr = __builtin_return_address(_x); \
24 \
25 if (NULL == addr) \
26 { \
27 return num; \
28 } \
29 \
30 _outStack[num++] = uintptr_t(addr); \
31 } \
32 } \
33 else \
34 { \
35 return num; \
36 }
3738 RETURN_ADDRESS(0);
39 RETURN_ADDRESS(1);
40 RETURN_ADDRESS(2);
41 RETURN_ADDRESS(3);
42 RETURN_ADDRESS(4);
43 RETURN_ADDRESS(5);
44 RETURN_ADDRESS(6);
45 RETURN_ADDRESS(7);
46 RETURN_ADDRESS(8);
47 RETURN_ADDRESS(9);
48
49 RETURN_ADDRESS(10);
50 RETURN_ADDRESS(11);
51 RETURN_ADDRESS(12);
52 RETURN_ADDRESS(13);
53 RETURN_ADDRESS(14);
54 RETURN_ADDRESS(15);
55 RETURN_ADDRESS(16);
56 RETURN_ADDRESS(17);
57 RETURN_ADDRESS(18);
58 RETURN_ADDRESS(19);
59
60 RETURN_ADDRESS(20);
61 RETURN_ADDRESS(21);
62 RETURN_ADDRESS(22);
63 RETURN_ADDRESS(23);
64 RETURN_ADDRESS(24);
65 RETURN_ADDRESS(25);
66 RETURN_ADDRESS(26);
67 RETURN_ADDRESS(27);
68 RETURN_ADDRESS(28);
69 RETURN_ADDRESS(29);
70
71 RETURN_ADDRESS(30);
72 RETURN_ADDRESS(31);
73
74#undef RETURN_ADDRESS
7576 BX_PRAGMA_DIAGNOSTIC_POP();
77
78 return num;
79#else
8081 return 0;
82#endif // BX_COMPILER_GCC || BX_COMPILER_CLANG
83
```


You can see GCC 15.2 output on Godbolt Compiler Explorer of what this code produces [here](https://godbolt.org/#z:OYLghAFBqd5QCxAYwPYBMCmBRdBLAF1QCcAaPECAMzwBtMA7AQwFtMQByARg9KtQYEAysib0QXACx8BBAKoBnTAAUAHpwAMvAFYTStJg1DIApACYAQuYukl9ZATwDKjdAGFUtAK4sGIAGxmpK4AMngMmAByPgBGmMQgAKykAA6oCoRODB7evgFBaRmOAmER0SxxCcl2mA5ZQgRMxAQ5Pn6Btpj2xQwNTQSlUbHxSbaNza15HQrjA%2BFDFSOJAJS2qF7EyOwcJhoAgrsAnOYAzOHI3lgA1CYnbjP4ggB0CLfYu3tXXzdmZwwXXmut3uBHwqBebw%2B3xu%2B2hAH04UwCARiHgYl4CJgEVAGKhwrR5stllcvOECCczHCCFdgJgWmJaH1kABrADiyGQFlJtEcDAgpMEFKpVzhCmZeBSpBJZKF1LhLCYqilAoIKRRVIAVCL1sJGizlh8jiYAOxWfZGjSHFWyq4MHw3E4AESuGluZoO5t%2BWBoESuACVsAAVOR%2ByJwvaOx0BoRCCBw1TE6FJ5Mp1NfEyJNyGy1HPBUK4QO0sB1uEUKhNpytV5MZrPmnM503V5stqu17PHBuHPMFjQlkViiWJ1sj9v1zsTk0WEcz5tjj2TrsAWiXovFKTds5n84tk%2BNzq3h5rmY7u66SiPl53XaNTcv9%2Bvi4nPYgkTkIRCDsdt2dCPRdF5OEqGIVgsSYdB0GITAFAUOMK0TR9d1vad71nRCby7KCCA2BhbR8TdUO%2BdCnxNA9CNbYjd3I7cT3HJDLQANzxdAtXAyCvxFOF/x5cI4SwnDEQgqCYLgg0TmnSiu2o0daIXeju3zV930/H8fyuNjiGHB9ZPk5DpJbSSn344hcKLAjyMM28yP0ytLMtGy5x0jCJzhHUmWZDMLDMyxrAzZ01JVNViCpCANLElDjzrOSb33ByKKcvdrLigyEqOc9MGSlKoqQu9Mqy09MLpHC8JYczkso/ds2iw4A2DUNw0jaNYw0cKCpqoMQzDCMo2wGMIC4Vq6MtWrOoanq%2BrMQbqpG%2BruqaiATim3cZq6xretjSQlq7FaxvmlY3Tana5vWiB/C2icjrWvrjXOo5LvG2MAA5buGjrZqu2NDi26a3tWh7%2Bpag6hvauq/vmrgBqBn7Qd2k6uEmqHlt%2B2G%2Bq4RbEe25HjtRzaMYurGPv6/bxMOgn/q4M68busnwZuqnXph7HYy4Z76ZB0amf6r6MehjnCbMQGSeB%2B75rMSGhd597/rMBGJaRxn%2BfRuXMYV6XceV/HVdF4n3XlvnpcpjXqa1k6zDpo2Gf10XWYt9mpdF7nlclsGTpOQXdZVq3XfFj2Dl%2BLwGG9f0afWqrd2M0z8KNyr9g4VZaE4RJeD8DgtFIVBOCzHzLCuBR1k2DLTh4UgCE0OPVmZJJ/CeRJHsSE5/Fr%2BvG7r6QE44SRk7L9POF4BQQA0Euy9WOBYBgRAUFQFgUjoeJyEoNBp9nhJgC4RIghoHl4n7iAYm7mJwiaABPThi4P5hiCPgB5GJtFqUvuF4Re2EEK%2BGFoE/U94LB0WANwGX7o/UgWAFRGHEF/YBeAoJ1AYtBbumBVC1AxNsYuZIujdwJDEECl8PBYG7iiPALBT68FgcQGI6RMCOkwKA4ABIjDDz4AYYACgABqeBMAAHcr4pEYMQmQggRBiHYFIfh8glBqG7roIIBh6GmGzjYTB/dICrFQGqLIgClxXzMLwVApDURYCURAVYNQ6jOAgK4SYfguDBEDoMcolQ9CFEyAISxjj0jOIYHY4YCRrEmJ6H0CYng2h6D8fUWYXjFg%2BLGP0VxvjwnzHsSMAaawNhbAkPHROXcIEZw4FcVQj1/BLn8JIGkHIrhryeGYAsuBCAkB%2BCcAavAH5aCJKQSukhDhPEOMaQ4hwzCJGNP0lmDTHr6E4J3UgRDEiDxTmnHJfcB5Dy/iPceEAkA6hSBieeEBF4z3oMQSIoFOD5MKcUq4FxDDAALCiAOzJli8EwPgIg%2Bi9D8AEaIcQIi3liJUOoCBUjSAcJAikYhGSOBJ1ILMnRnAr4Yk2dSVA%2BYTlFJKcAMpFSqkQA8EvfZ9TJpNOHqsBAmBwIjCMWMjuvApkzO7vM2wizmnlzaSASQJwniSCkP4E4HLJBcp5aM9uJwslzN7kslpYLtGTIkBoGl2TRWMtaaQjIzhJBAA).

## Simpler platform-specific implementation

We can simplify the code by using `__builtin_frame_address`

once to get the initial stack frame pointer and then chase it. However, assuming the return address location is platform-dependent, making the function platform-specific.

```
1 static const uintptr_t* nextStackFrame(const uintptr_t* _stackFrame)
2 {
3 const uintptr_t* newStackFrame = (const uintptr_t*)*_stackFrame;
4
5 // making sure stack frame addresses are moving in the right direction
6if (newStackFrame <= _stackFrame)
7 {
8 return NULL;
9 }
10
11 // making sure there is no alignment issue
12if (uintptr_t(newStackFrame) & (sizeof(uintptr_t) - 1) )
13 {
14 return NULL;
15 }
16
17 return newStackFrame;
18 }
19
20 BX_NO_INLINE uint32_t getCallStackSystemVAbi(uint32_t _skip, uint32_t _max, uintptr_t* _outStack)
21 {
22 if (BX_ENABLED(BX_PLATFORM_LINUX && BX_CPU_X86 && BX_ARCH_64BIT) )
23 {
24 // get initial stack frame address
25const uintptr_t* stackFrame = (const uintptr_t*)__builtin_frame_address(0);
26
27 uint32_t num = 0;
28
29 while (NULL != stackFrame
30 && num < _max)
31 {
32 // check that return address is valid
33if (uintptr_t(0) == stackFrame[1])
34 {
35 break;
36 }
37
38 if (BX_UNLIKELY(0 < _skip) )
39 {
40 --_skip;
41 }
42 else
43 {
44 // grab return address
45++] = stackFrame[1];
46 }
47
48 // go to next stack frame
49= nextStackFrame(stackFrame);
50 }
51
52 return num;
53 }
54
55 return 0;
56 }
```


On Windows for x86, the code is identical. For MSVC, the implementation differs since `__builtin_frame_address`

-like compiler intrinsics are unavailable. Instead, we obtain the stack frame address by taking the first function argument’s address and subtracting 8 bytes, where the stack frame is stored.

```
1 BX_NO_INLINE uint32_t getCallStackWinAbi(uint32_t _skip, uint32_t _max, uintptr_t* _outStack)
2 {
3 if (BX_ENABLED(BX_PLATFORM_WINDOWS && BX_CPU_X86 && BX_ARCH_32BIT) )
4 {
5 const uintptr_t* stackFrame = (uintptr_t*)&_skip - 2;
6
7 uint32_t num = 0;
8
9 while (NULL != stackFrame
10 && num < _max)
11 {
12 if (uintptr_t(0) == stackFrame[1])
13 {
14 break;
15 }
16
17 if (BX_UNLIKELY(0 < _skip) )
18 {
19 --_skip;
20 }
21 else
22 {
23 _outStack[num++] = stackFrame[1];
24 }
25
26 stackFrame = nextStackFrame(stackFrame);
27 }
28
29 return num;
30 }
31 else if (BX_ENABLED(BX_PLATFORM_WINDOWS && BX_CPU_X86 && BX_ARCH_64BIT) )
32 {
33 return getCallStackWinRtl(_skip + 1, _max, _outStack);
34 }
35
36 return 0;
37 }
```


## Implementation using `_Unwind_Backtrace`


```
1 struct UnwindCallbackData
2 {
3 uint32_t skip;
4 uint32_t max;
5 uint32_t num;
6 uintptr_t* outStack;
7 };
8
9 static _Unwind_Reason_Code unwindCallback(struct _Unwind_Context* _ctx, void* _arg)
10 {
11 UnwindCallbackData& ucd = *(UnwindCallbackData*)_arg;
12
13 if (ucd.num < ucd.max)
14 {
15 if (0 < ucd.skip)
16 {
17 --ucd.skip;
18 return _URC_NO_REASON;
19 }
20
21 _Unwind_Ptr addr = _Unwind_GetIP(_ctx);
22 if (0 == addr)
23 {
24 return _URC_END_OF_STACK;
25 }
26
27 ucd.outStack[ucd.num++] = uintptr_t(addr);
28 return _URC_NO_REASON;
29 }
30
31 return _URC_END_OF_STACK;
32 }
33
34 BX_NO_INLINE uint32_t getCallStackUnwind(uint32_t _skip, uint32_t _max, uintptr_t* _outStack)
35 {
36 UnwindCallbackData ucd =
37 {
38 .skip = _skip + 1,
39 .max = _max,
40 .num = 0,
41 .outStack = _outStack,
42 };
43
44 _Unwind_Backtrace(unwindCallback, &ucd);
45
46 return ucd.num;
47 }
```


## Implementation using `backtrace`


```
1
2 BX_NO_INLINE uint32_t getCallStackExecInfoBacktrace(uint32_t _skip, uint32_t _max, uintptr_t* _outStack)
3 {
4 const uint32_t max = _skip+_max+1;
5 void** tmp = (void**)BX_STACK_ALLOC(sizeof(uintptr_t)*max);
6
7 const uint32_t numFull = backtrace(tmp, max);
8 const uint32_t skip = min(_skip + 1 /* skip self */, numFull);
9 const uint32_t num = numFull - skip;
10
11 memCopy(_outStack, tmp + skip, sizeof(uintptr_t)*num);
12
13 return num;
14 }
```


## Implementation using `RtlCaptureStackBackTrace`


Windows API actually offers the most sane implementation of call-stack backtrace:

```
1NTSYSAPI USHORT RtlCaptureStackBackTrace(
2 [in] ULONG FramesToSkip,
3 [in] ULONG FramesToCapture,
4 [out] PVOID *BackTrace,
5 [out, optional] PULONG BackTraceHash
6);
```


The first few arguments are identical to my function, which is a coincidence. The last argument `BackTraceHash`

helps identify identical call stack traces. I omitted it from my API, as hashing can be done post-processing. For instance, if call stack traces are used for logging and dumped to memory for another process to scrape and analyze, that process can handle the hashing itself.

## Conclusion

Hopefully this article proves useful for developers optimizing their call-stack tracing functions. By implementing both fast and exact functions, developers can choose the right tool for their needs, ensuring efficient and reliable call-stack tracing.

While writing this article, I discovered that C++23 introduced `std::basic_stacktrace`

for call-stack tracing. [Past experience with C++ standards](https://bkaradzic.github.io/posts/orthodoxc++/) suggests it may have issues, such as requiring memory allocation, making it unsuitable for heavy real-time use, and could need 2–3 standard iterations for the C++ committee to refine it.

All code from this article, along with other implementations using OS calls, is available here: [https://github.com/bkaradzic/bx](https://github.com/bkaradzic/bx)

## References

-
Printing a Stack Trace with MinGW


[https://web.archive.org/web/20150706201731/https://www.theorangeduck.com/page/printing-stack-trace-mingw](https://web.archive.org/web/20150706201731/https://www.theorangeduck.com/page/printing-stack-trace-mingw) -
Stack frame layout on x86-64


[https://web.archive.org/web/20150901043512/http://eli.thegreenplace.net/2011/09/06/stack-frame-layout-on-x86-64](https://web.archive.org/web/20150901043512/http://eli.thegreenplace.net/2011/09/06/stack-frame-layout-on-x86-64) -
Programmatic access to the call stack in C++


[https://web.archive.org/web/20150717165002/https://eli.thegreenplace.net/2015/programmatic-access-to-the-call-stack-in-c/](https://web.archive.org/web/20150717165002/https://eli.thegreenplace.net/2015/programmatic-access-to-the-call-stack-in-c/) -
/Oy (Frame-Pointer Omission)


[https://learn.microsoft.com/en-us/cpp/build/reference/oy-frame-pointer-omission?view=msvc-170](https://learn.microsoft.com/en-us/cpp/build/reference/oy-frame-pointer-omission?view=msvc-170) -
3.12 Options That Control Optimization


[https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html) -
-fomit-frame-pointer, -fno-omit-frame-pointer


[https://developer.arm.com/documentation/109443/6-22-2LTS/armclang-Reference/armclang-Command-line-Options/-fomit-frame-pointer---fno-omit-frame-pointer](https://developer.arm.com/documentation/109443/6-22-2LTS/armclang-Reference/armclang-Command-line-Options/-fomit-frame-pointer---fno-omit-frame-pointer) -
C++23

`std::basic_stacktrace`


[https://web.archive.org/web/20250526201211/https://en.cppreference.com/w/cpp/utility/basic_stacktrace.html](https://web.archive.org/web/20250526201211/https://en.cppreference.com/w/cpp/utility/basic_stacktrace.html)