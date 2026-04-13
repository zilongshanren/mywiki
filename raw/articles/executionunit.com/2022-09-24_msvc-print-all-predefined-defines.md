---
title: 'MSVC Print All Predefined #Defines'
url: https://www.executionunit.com/blog/2022/09/24/msvc-print-all-predefined-defines/
published: '2022-09-24'
source_blog: Blog | Execution Unit
source_site: http://www.executionunit.com/blog/
category: game programming
fetched: '2026-04-13'
---

Sometimes you really need to know what defines your compiler has on by default. I had no idea how
to do this with Visual Studio so I dug in. Here is how to do it.

Open up a VS command prompt, pick the appropriate prompt x86, x64 etc.

![](../../assets/afecd0b4e662bfc2.jpg)


enter the following:

| ```
> echo int main(){} > test.cpp
> cl.exe /PD /Zc:preprocessor test.cpp
```
|

You should see output similar to the following:

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63 | ```
test.cpp
#define _CPPRTTI 1
#define __cpp_ref_qualifiers 200710L
#define __cpp_init_captures 201304L
#define __STDCPP_DEFAULT_NEW_ALIGNMENT__ 8u
#define __cpp_rtti 199711L
#define __cpp_decltype_auto 201304L
#define _MSC_EXTENSIONS 1
#define _MSVC_LANG 201402L
#define __cpp_binary_literals 201304L
#define __cpp_constexpr 201304L
#define _MSC_BUILD 0
#define __cpp_attributes 200809L
#define __cpp_inheriting_constructors 200802L
#define __cpp_generic_lambdas 201304L
#define __cpp_variable_templates 201304L
#define __cpp_nsdmi 200809L
#define _NATIVE_WCHAR_T_DEFINED 1
#define __BOOL_DEFINED 1
#define __cpp_sized_deallocation 201309L
#define __cpp_threadsafe_static_init 200806L
#define _HAS_CHAR16_T_LANGUAGE_SUPPORT 1
#define __cpp_initializer_lists 200806L
#define _IS_ASSIGNABLE_NOCHECK_SUPPORTED 1
#define __cpp_static_assert 200410L
#define __cpp_return_type_deduction 201304L
#define __cpp_enumerator_attributes 201411L
#define __cpp_decltype 200707L
#define _M_IX86_FP 2
#define _CONSTEXPR_CHAR_TRAITS_SUPPORTED 1
#define _MT 1
#define _WCHAR_T_DEFINED 1
#define _MSVC_WARNING_LEVEL 1L
#define __cpp_alias_templates 200704L
#define __cplusplus 199711L
#define __cpp_lambdas 200907L
#define __STDC_HOSTED__ 1
#define __cpp_user_defined_literals 200809L
#define __cpp_rvalue_references 200610L
#define _NATIVE_NULLPTR_SUPPORTED 1
#define __cpp_namespace_attributes 201411L
#define __STDCPP_THREADS__ 1
#define _MSC_FULL_VER 193331629
#define _MSC_VER 1933
#define _MSVC_TRADITIONAL 0
#define __cpp_range_based_for 200907L
#define _MSVC_CONSTEXPR_ATTRIBUTE 1
#define __cpp_raw_strings 200710L
#define _M_IX86 600
#define __cpp_unicode_literals 200710L
#define __cpp_unicode_characters 200704L
#define _MSVC_EXECUTION_CHARACTER_SET 1252
#define _INTEGRAL_MAX_BITS 64
#define __cpp_aggregate_nsdmi 201304L
#define _WIN32 1
#define _CRT_USE_BUILTIN_OFFSETOF 1
#define __cpp_variadic_templates 200704L
#define __cpp_delegating_constructors 200604L
Microsoft (R) Incremental Linker Version 14.33.31629.0
Copyright (C) Microsoft Corporation. All rights reserved.
/out:test.exe
test.obj
```
|

I turned this in to a simple batchfile

Hope this helps.

EOL.

## Comments