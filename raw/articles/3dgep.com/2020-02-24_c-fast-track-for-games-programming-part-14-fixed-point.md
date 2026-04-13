---
title: 'C++ Fast Track for Games Programming Part 14: Fixed Point'
url: https://www.3dgep.com/cpp-fast-track-14-fixed-point/
author: Robert Grigg
published: '2020-02-24'
source_blog: 3D Game Engine Programming
source_site: https://www.3dgep.com/
category: graphics
fetched: '2026-04-13'
---

In part [Part 9](https://www.3dgep.com/cpp-fast-track-9-colours/) you worked with colours and were introduced to the noble art of bitmagic. Here’s a quick refresher: multiplying an integer value by a power of 2 can be done by shifting its (binary) bits to the left.

Division is similar, except this time you shift to the right. So for example, \(6a\) is equivalent to \(2^2a+2a\) which is equivalent to `(a<<2)+(a<<1)`

using bit-shifting operations. Being aware of the number of bits in a variable is especially important if more than one number is stored in the bits of a 32-bit integer. This is is the case for 32-bit colours: Each of the red, green, and blue components each use 8-bits with the alpha component completing the 32-bits to represent a single pixel.


**Previous Part: Data Structures**

**Next Part:**

[File I/O](https://www.3dgep.com/cpp-fast-track-15-fileio/)For this tutorial, we’ll be using the same template from the [2nd tutorial](https://www.3dgep.com/cpp-fast-track-2-template/):

To introduce some new concepts, I will start with a brief snippet that slowly zooms in on an image:

|
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
|
#include "game.h"
#include "surface.h"
#include "template.h"
namespace Tmpl8
{
void Game::Init() {}
void Game::Shutdown() {}
Surface* img = new Surface("assets/aagun.tga");
float dx = 2.0f;
void Game::Tick(float deltaTime)
{
Pixel* dst = screen->GetBuffer();
Pixel* src = img->GetBuffer();
int srcWidth = img->GetWidth();
int srcHeight = img->GetHeight();
for (int x = 0; x < ScreenWidth; x++)
for (int y = 0; y < ScreenHeight; y++)
{
int readxpos = (int)(dx * x) % srcWidth;
int readypox = (int)(dx * y) % srcHeight;
Pixel sample = src[readxpos + readypox * srcWidth];
dst[x + y * ScreenWidth] = sample;
}
dx *= 0.999f;
}
};
|

The code works like this: First, we copy pixels from `img`

to `screen`

(by accessing the pixels in the Surface, via the `Surface::GetBuffer`

method).

Variable `dx`

is set to `2`

, so when `x`

is `10`

, `dx * x`

is `20`

: we read pixel `20`

from the original image. For the next frame however, `dx`

is no longer `2.0`

: it slowly gets smaller. After a few frames, dx is much smaller than `2`

, and so we read far less pixels from `img`

, but we still plot the same amount of pixels. This causes the stretching effect.

Some other remarks about this code:

- If you do not add
`f`

to`2.0`

on line 12, you will get a warning. This is because C++ assumes that`2.0`

(without a postfix) is a double precision (64-bit) floating-point number, and you are storing it in a single precision (32-bit) float variable. The compiler warns you in this case because the cast from a 64-bit value to a 32-bit value will cause a loss of precision. Don’t worry about it, just postfix the`f`

after constant literals that should be treated as single precision floating-point values to prevent the warning. - Pointers are used as arrays in this code (
`src`

and`dst`

). This works, because an array*is*a pointer in C++. And the other way round:`Pixel* screen`

is an array, and therefore you can access the tenth pixel as`screen[10]`

.

There’s something else going on in this code, something that is not immediately obvious. And that’s the bit that I want to talk about.

Have a look at this line again:

|
22 |
int readxpos = (int)(dx * x);
|

We need an integer to read from the image pixel array. But, `dx * x`

does not result in an integer. Actually, `x`

is an integer, but as soon as you multiply an `int`

(integer) by a `float`

, the result is a `float`

too. Or, to be precise: the integer is converted to a floating-point value, and *then* the multiplication is done. So, there are actually two conversions occuring on that line:

|
22 |
int readxpos = (int)(dx * (float)x);
|

Is that a problem? Yes it is. Conversions take time, and even if it’s not a lot of time, in this case it can easily be prevented.

Before you proceed, get yourself a larger image. I got this one from the internet:

When you try the larger image in the application, you’ll see that the speed went down (quite) a bit. Getting rid of the conversions will improve that.

So how do you get rid of conversions, if you need integers for the array, and a float to store `0.999f`

? The answer is: *fixed point math*. The concept is pretty simple. Suppose you *forget* the dot in `0.999f`

. Instead, you write: `999`

, and you remember that this number is a thousand times too large. Next, you do all your calculations as usual. So: `readxpos = dx * x`

. Once you’re done calculating, you get the correct answer by dividing by `1000`

. What you just did is exchanging an int-to-float conversion and a float-to-int conversion for a division. This in itself is not a big improvement (if at all), but it does become a big improvement when you realize that `1000`

is just an arbitrary factor. For a computer, a power of `2`

is much better: `1024`

would do just fine.

There’s just one thing you need to be aware of. When you multiply two numbers that are both `1000`

times too large, the result is `1000000`

times too large. You can see how this is countered in the modified code snippet:

|
11
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
24
25
26
28
|
Surface* img = new Surface("assets/aagun.tga");
void Game::Tick(float deltaTime)
{
Pixel* dst = screen->GetBuffer();
Pixel* src = img->GetBuffer();
int srcWidth = img->GetWidth();
int srcHeight = img->GetHeight();
for (int x = 0; x < ScreenWidth; x++)
for (int y = 0; y < ScreenHeight; y++)
{
int readxpos = ((dx * x) >> 10) % srcWidth;
Pixel sample = src[readxpos + readypos * srcWidth];
dst[x + y * ScreenWidth] = sample;
}
}
|

In other words: when you multiply two numbers that are both 1024 times too large, the result is (1024 * 1024) too large. You can fix this by dividing by 1024. In the code above, this is done by shifting 10 bits to the right.

The code is now a lot faster. We now have a *bitshift* instead of the two conversions. Apparently, this is a lot faster in C++.

In the above example, we got roughly three digits of decimal precision by multiplying our floats by *1024*. This means that there is a now a limit to precision: the smallest number in an integer is still 1, which represents 1/1024 in our fixed point notation. What if we want things to be more precise?

We can scale by a bigger power of 2. We used 1024, which is \(2^{10}\); let’s go for \(2^{16}\) instead, which is 65,536. If you try this in the fixed point code, you will notice that things break… Why?

Well: there is this line that says `dx = (dx * 1023) >> 10`

. What kind of numbers are we processing here? Variable `dx`

starts at `2 * 1024 = 2048`

; this fits in 12 bits (almost 11, but 2047 is the largest number that still fits in 11 bits). Then we have 1023, which takes 10 bits. Multiply them together, and we get results that requires 21 bits. No problem. But what happens if `dx`

takes 17 bits, and 1023 becomes 65535, which takes 16 bits? The result (before shifting back by 16) takes 33 bits, and that doesn’t fit in an integer! Things do work however if we use \(2^{15}\) instead, which is 32,768.

With fixed point arithmetic you will need to carefully balance the range of your numbers, and their *precision*.

Your tasks for today:

Modify the code so that it can zoom out, instead of just zooming in. Use a modulo (`%`

) to make sure the source image gets repeated if it’s too small. Once the modulos are in, you’ll notice that your code gets quite a bit slower again. This is because modulo is performing a division (which is slow). If you make your source image size a power of `2`

, you can get rid of the modulo: `% 256`

can be calculated more rapidly using `& 255`

, and likewise `% 512`

can be calculated using `& 511`

. But that’s *bit* magic again🤓.

Modify the code so that the zooming image appears to bounce against your screen.

Add rotation to the zooming image. Keep using fixed point arithmetic in the inner loop.

**Previous Part: Data Structures**

**Next Part:**

For the basic portion of the assignment, is the instruction to add a modulo of image size already done in the example on lines 22 and 23?

The modulo is already handled in the example shown. The zooming, bouncing and rotating are not handled.