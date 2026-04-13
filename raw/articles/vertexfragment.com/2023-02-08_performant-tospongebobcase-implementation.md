---
title: Performant tOsPoNgEbObCaSe Implementation
url: https://www.vertexfragment.com/ramblings/spongebob-case/
author: Steven Sell
published: '2023-02-08'
source_blog: Vertex Fragment
source_site: https://www.vertexfragment.com/
category: graphics
fetched: '2026-04-13'
---

All programmers have their perferred string format, and they tend to choose one of the following “mainstream” styles:

`camelCase`

`PascalCase`

`snake_case`

`kebab-case`


Today I present what is sure to be your new favorite: `sPoNgEbObCaSe`

. It is quite simple, each word starts lower-case and then each subsequent letter alternates between upper- and lower-case.

“I really like the look of sPoNgEbObCaSe, but my language (C#) doesn’t provide any built-in utilities for converting a string to it!”


Well, you are in luck! Two performant implementations are detailed below.

What started off as joke puzzle between coworkers to implement a string converter for this novelty case quickly (d)evolved into a rather serious endeavour to see who could produce the fastest implementation of a `tOsPoNgEbObCaSe()`

extension method.

The method was to follow the design of the existing `string.ToLower()`

and `string.ToUpper()`

methods: take in an arbitrary string and return a copy of that string in the desired format.

My first attempt at an implementation was fairly fast and works with any string (ASCII or unicode) and runs in *O(n)* time.

```
public static string tOsPoNgEbObcAsE(this string str)
{
char[] sPoNgEbObCaSe = str.ToLower().ToCharArray();
bool lower = true;
for (int i = 0; i < sPoNgEbObCaSe.Length; ++i)
{
if ((sPoNgEbObCaSe[i] >= 97) && (sPoNgEbObCaSe[i] <= 122))
{
if (!lower)
{
sPoNgEbObCaSe[i] = (char)(sPoNgEbObCaSe[i] - 32);
}
lower = !lower;
}
else
{
lower = true;
}
}
return new string(sPoNgEbObCaSe);
}
```


It lower-cases the entire string and then iterates over each character. If it is a alphabet character (a-z) it conditionally changes it to an upper-case alphabet character (A-Z). The condition being a `lower`

flag that when false indicates the character should not be lower-case.

The flag toggles for every alphabet character (a-z and A-Z) and resets when encountering any other character.

The resulting method is fairly fast, taking **an average of 0.0002 milliseconds per string** in my test setup (500,000 strings, with an average string length of 61 characters).

And then I was challenged to make a branchless implementation, which of course would be even faster.

This was done by essentially “baking” the different logic branch paths into static arrays. One array for the character conversion between cases, and another array for the `lower`

flag flipping.

It should be noted that the method presented below, `tOsPoNgEbObcAsEfAsT`

, is faster but supports only up to ASCII 128. So please keep that in mind before integrating it with your production systems.

```
private static readonly int[] ToLower = new int[128] { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127 };
private static readonly int[] ToUpper = new int[128] { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 123, 124, 125, 126, 127 };
private static readonly int[] Flip = new int[128] { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0 };
private static readonly int[][] ToLowerUpper = new int[][] { ToLower, ToUpper };
public static unsafe string tOsPoNgEbObcAsEfAsT(this string str)
{
int lower = 0;
int length = str.Length;
char[] sPoNgEbObCaSe = new char[length];
fixed (char* p = str)
{
for (int i = 0; i < length; ++i)
{
sPoNgEbObCaSe[i] = (char)ToLowerUpper[lower][(int)p[i]];
lower = Flip[p[i]] * (1 - lower);
}
}
return new string(sPoNgEbObCaSe);
}
```


Aside from the array baking mentioned earlier, this implementation also makes use of `unsafe`

code which allows for direct pointer manipulation in C#. This is used to avoid the string copy done at the start of the first implementation.

Running against the same test conditions as the other method, the fast version **averaged 0.00012 milliseconds per string**, nearly twice as fast!

There you have it, two implementations of sPoNgEbObCaSe formatters, things you didn’t know you needed.

Feel free to take up the challenge for yourself and try to make your own even faster implementation.