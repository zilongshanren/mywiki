---
title: 'C++ Fast Track Part 8: Memory Addresses'
url: https://www.3dgep.com/cpp-fast-track-8-memory-addresses/
author: Robert Grigg
published: '2019-10-30'
source_blog: 3D Game Engine Programming
source_site: https://www.3dgep.com/
category: graphics
fetched: '2026-04-13'
---

One of the harder concepts in C++ is the concept of pointers. Pointers have everything to do with the very nature of the language: C++ gets you pretty close to the hardware you are working with, and one of the most important parts of that hardware is memory. In this tutorial, you will learn to use pointers to refer to memory addresses.


**Previous Part: Debugging**

**Next Part:**

[Colours](https://www.3dgep.com/cpp-fast-track-9-colours/)For this tutorial, you will be using the same template from the [2nd tutorial](https://www.3dgep.com/cpp-fast-track-2-template/):

Your system probably has a few *GiB* (or more commonly but incorrectly denoted *GB*) of memory, which roughly corresponds to a couple billion bytes:

| Symbol | Prefix | Name | Bytes | Size |
|---|---|---|---|---|
| B | byte (B) | \(2^0\) bytes | 1 B | |
| Ki | kibi | kibibyte (KiB) | \(2^{10}\) bytes | 1,024 B |
| Mi | mebi | mebibyte (MiB) | \(2^{20}\) bytes | 1,024 KiB |
| Gi | gibi | gibibyte (GiB) | \(2^{30}\) bytes | 1,024 MiB |
| Ti | tebi | tebibyte (TiB) | \(2^{40}\) bytes | 1,024 GiB |
| Pi | pebi | pebibyte (PiB) | \(2^{50}\) bytes | 1,024 TiB |
| Ei | exbi | exbibyte (EiB) | \(2^{60}\) bytes | 1,024 PiB |

Notice that we use the Ki, Mi, Gi, Ti, etc… symbols for binary units in order to differentiate them from the metric symbols (k, M, G, T, etc…). Computer data is measured in powers of 2 (\(2^b\) – binary) units rather than powers of 10 (\(10^d\) – decimal) units.

Each of the billions of bytes of data is stored in the memory of your computer and can be referred to by its memory *address*. In a 32-bit processor, memory addresses are represented as a 32-bit number. This means that (theoretically) a 32-bit computer can access a maximum of \(2^{32}\) unique memory addresses. Since each memory address refers to a unique byte in memory (since memory is *byte addressable*), that’s 4,294,967,296 bytes, or 4,194,304 KiB, or 4,096 MiB, or 4 GiB.

64-bit processors can access up to \(2^{64}\) unique memory addresses. That’s 18,446,744,073,709,551,616 bytes, or 17,179,869,184 GiB, or 16 EiB. Since most personal computers these days have between 8 – 64 GiB of memory, that’s more data than you’ll probably ever see in a personal computer in your lifetime (maybe…).

Load up a fresh template project. Have a look at the `Surface::Bar`

method in `surface.cpp`

:

|
200
201
202
203
204
205
206
207
208
|
void Surface::Bar( int x1, int y1, int x2, int y2, Pixel c )
{
Pixel* a = x1 + y1 * m_Pitch + m_Buffer;
for ( int y = y1; y <= y2; y++ )
{
for ( int x = 0; x <= (x2 - x1); x++ ) a[x] = c;
a += m_Pitch;
}
}
|

This function draws a bar. At the first line of this function, a *pointer* is created (denoted by the asterisk symbol `*`

). Once line 202 is executed, the *pointer* `a`

will contain the memory address of the first pixel to start drawing the bar. Then the function proceeds with drawing the actual pixels: it loops over the lines that contain the bar (`y1`

to `y2`

), and then over the rows that contain the bar (`x1`

to `x2`

). However, it does not use the `Plot`

function: instead, it writes directly to the memory address that contains the screen pixels.

So, let’s do some experiments. Copy the following `Game::Tick`

method:

|
27
28
29
30
31
|
void Game::Tick( float deltaTime )
{
Pixel* address = screen->GetBuffer();
for ( int i = 0; i < 307200; i++ ) address[i] = i;
}
|

This code gets the memory address of the screen surface in memory, and stores it in a pointer variable (*address*). Then, it uses a single for-loop to fill (most of) the screen.

Now try this code:

|
27
28
29
30
31
|
void Game::Tick( float deltaTime )
{
Pixel* address = screen->GetBuffer() + 100;
for ( int i = 0; i < 255; i++ ) address[i * 800] = i;
}
|

This gets us a blue vertical line.

This demonstrates something important. The lines of your screen may appear separate, but they are not: in memory, your screen is one continuous line in memory, consisting of 800 * 512 pixels. That means that you should look 800 pixels further to get to the next line. Which is exactly what above code does. This also explains why printing text too close to the right edge of your window makes it wrap to the left side: there is no right edge.

Let’s leave the screen pixels for a moment. Copy the following Tick function:

|
27
28
29
30
31
32
33
34
|
void Game::Tick( float deltaTime )
{
int a = 100;
int b = 200;
int* c = &a;
*c = 300;
int w = 0;
}
|

Put a breakpoint (`F9`) on line 31 (`int* c = &a;`

), and run the code. Your program will stop right before it executes line 31.

Now, open a *watch* window (**Debug > Windows > Watch > Watch 1**), and inspect the following values:

| Name | Value | Type |
|---|---|---|
`a` |
`100` |
`int` |
`&a` |
`0x0019fe08 {100}` (this address will be different for you) |
`int *` |

The `&`

symbol, when attached to a variable, gives you the *address of* a variable. So in this case, `a`

is stored somewhere in memory, and now you know what the address of that variable is.

The ampersand (`&`

) is used on line 31 of the code. Here we create a pointer (notice the asterisk `*`

symbol), which points to the address of `a`

. So there is a fundamental difference between variable `a`

and `c`

: `a`

is an *integer* variable, but `c`

is a *pointer* to an *integer*, that is, it contains the *address* of an integer variable.

So why are pointers so important in C++? The reason is: performance. When you plot a pixel at coordinate (`x`

, `y`

), in the end all that matters is that some value at some memory location changes. That’s a simple operation, in principle. But when you only have `x`

and `y`

, you need to calculate that address: it’s on line `y`

, so at least `800 * y`

pixels past the start of the first address of the screen memory. Add `x`

to that to get the correct address. Oh and don’t forget the address of the screen itself. So the formula is: `screen->GetBuffer() + x + y * 800`

. At that point you just have the address, so you still need to plot.

That’s an awful lot of work for a single pixel. If you know the address, all you need to do is put a value right there. Pointers give you low-level control over memory. This gives you fine control over the work that is carried out, and this in turn gives you raw performance (and thus, speedy games).

Here’s your task for today:

- Draw a dotted line (skip every other dot) from (
`0`

,`0`

) to (`400`

,`400`

). Do not use the`Plot`

function, use a pointer variable instead. - Figure out what the distance between dots in memory is to make this code super simple and fast.
- Create an application that does the following:
- Load an
`800x512`

image - Moves a green dot from the top-center (say,
`x = 400`

,`y = 0`

) to the bottom. While doing so, the dot evades obstacles. - When the pixel below the dot is black, it goes down. Otherwise, it goes one pixel to the left if its y is an odd number, or the right if its y is an even number.
- When the pixel reaches the bottom of the screen, it returns to the top.

- Load an

Make sure that the image that you use for step A is suitable for the other steps. Also note that even though we’re moving a single pixel now, but this will become an avalanche soon 🙂

For this assignment, you need to use pointers: it’s also a great way to read screen pixels rather than writing to them.

If you’ve completed the assignment, you should see something similar to the video shown below (the green dot is larger than a single pixel so that it is more visible in the video, but you only need to draw a single green pixel):

Once you have completed this assignment, you may continue with the next part.

Can you post the code for the completed assignment? I would like to study it so I could learn from it, I can’t quite figure it out on my own.

Tibs,

Please join our Discord server: https://discord.com/invite/gsxxaxc

Great explanation of getting started with pointers in C++! For additional practice and understanding, I recommend visiting https://aviatorgamez.in/ – there are plenty of useful resources and exercises on programming language.

okay, so i think i did the first assignment by increasing i by 1602 pixels, since the screen is 800 pixels wide.

void Game::Tick(float deltaTime)

{

Pixel* address = screen->GetBuffer();

for (int i = 0; i ” that could interact with the green ball, can i get some help?