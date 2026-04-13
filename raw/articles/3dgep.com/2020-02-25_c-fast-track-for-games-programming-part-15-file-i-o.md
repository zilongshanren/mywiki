---
title: 'C++ Fast Track for Games Programming Part 15: File I/O'
url: https://www.3dgep.com/cpp-fast-track-15-fileio/
author: Robert Grigg
published: '2020-02-25'
source_blog: 3D Game Engine Programming
source_site: https://www.3dgep.com/
category: graphics
fetched: '2026-04-13'
---

Before we continue with typical game related topics, you need to know a few more general techniques that will help you when you write your games. One of these techniques is *file I/O*. *File I/O* stands for *Input/Output*. You are of course already performing file I/O operations, for example when you load an image. However, this is handled by some image library ([FreeImage](http://freeimage.sourceforge.net/)). Sometimes, you simply want to store your own data.


**Previous Part: Fixed Point**

**Next Part:**

[Physics](https://www.3dgep.com/cpp-fast-track-16-physics/)For this tutorial, we’ll be using the same template from the [2nd tutorial](https://www.3dgep.com/cpp-fast-track-2-template/):

The very first article of this series made you write a *Hello World* application. This was also the last application that you had to print anything to a text window. There’s a reason for this: there are too many books already that make you write text-based applications, and this simply has little to do with game development.

There are however a few areas where

comes in handy. One of these areas is debugging (see [printf](http://www.cplusplus.com/reference/cstdio/printf/)[Part 7: Debugging](https://www.3dgep.com/cpp-fast-track-7-debugging/)).

Try this piece of code:

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
|
#include "game.h"
#include "surface.h"
#include "template.h"
#include <cstdio> //printf
namespace Tmpl8
{
float x = 200.0f, y = 0.0f, vx = 0.1f, vy = 0.0f;
void Game::Init() { }
void Game::Shutdown() { }
static Sprite rotatingGun(new Surface("assets/aagun.tga"), 36);
static int frame = 0;
void Game::Tick(float deltaTime)
{
screen->Clear(0);
screen->Box(x, y, x + 5, y + 5, 0xffffff);
if ((vy += 0.02f, y += vy) > ScreenHeight) vy = -vy;
if ((x += vx < 0) || (x >= ScreenWidth)) vx = -vx;
}
};
|

This is probably the shortest (but also most horribly-written) bouncing cube code possible (send your code if you can think of something worse!). On top of that, it doesn’t work: The bouncing cube leaves the screen at the right side. Let’s do some debugging!

Add the following line to your `Game::Tick`

method:

|
19 |
printf("X - position: % f\nY - position: % f\n", x, y);
|

The output of the

command is directed to the console window that is behind your game window. Left-click with your mouse inside the console window (to select some text) to pause the running application, this will block the main thread and let you examine the contents of the console window. Right-click to continue running the application.[printf](http://www.cplusplus.com/reference/cstdio/printf/)

The

function used in the previous section has a number of [printf](http://www.cplusplus.com/reference/cstdio/printf/)*interesting codes* in it. There’s the `%f`

: which is replaced by the contents of variable `x`

. Then, there is the `\n`

character: this sequence emits a *new line*, so printing continues on the next line.

The

command is pretty useful, especially if you know how to use it. Find out about the details of the [printf](http://www.cplusplus.com/reference/cstdio/printf/)

function here: [printf](http://www.cplusplus.com/reference/cstdio/printf/)[printf – C++ Reference](http://www.cplusplus.com/reference/cstdio/printf/). After reading about the

function, you will learn that you can replace [printf](http://www.cplusplus.com/reference/cstdio/printf/)`%f`

by `%i`

to print an integer. You can also write `%.2f`

to print a float with `2`

decimals.

Sadly, all this formatting goodness is not something we can use with the `Surface::Print`

function, which just expects a plain string to print. We can however *print* to a string to bypass this issue:

|
16
17
18
19
20
22
23
24
25
|
void Game::Tick(float deltaTime)
{
screen->Clear(0);
char text[128];
sprintf(text, "X - position: % f\nY - position: % f\n", x, y);
screen->Box(x, y, x + 5, y + 5, 0xffffff);
if ((vy += 0.02f, y += vy) > ScreenHeight) vy = -vy;
if ((x += vx > 0) || (x >= ScreenWidth)) vx = -vx;
}
|

This time, we get all the benefits of

, and use this to print the current position of the box to the game window.[printf](http://www.cplusplus.com/reference/cstdio/printf/)

Once you know how to get text to the screen using the

function and to a string using [printf](http://www.cplusplus.com/reference/cstdio/printf/)

function, moving on to files is easy. Try the following:[sprintf](http://www.cplusplus.com/reference/cstdio/sprintf/)

|
16
17
18
19
20
22
23
24
25
|
void Game::Tick(float deltaTime)
{
screen->Clear(0);
FILE* f = fopen( "positions.txt", "a" );
fprintf( f, "X-position: %f\nY-position: %f\n", x, y );
screen->Box(x, y, x + 5, y + 5, 0xffffff);
if ((vy += 0.02f, y += vy) > ScreenHeight) vy = -vy;
if ((x += vx < 0) || (x >= ScreenWidth)) vx = -vx;
}
|

This time, the position of the cube will be written to a file. Note how

was replaced by [printf](http://www.cplusplus.com/reference/cstdio/printf/)

. The first parameter of [fprintf](http://www.cplusplus.com/reference/cstdio/fprintf/)

is a [fprintf](http://www.cplusplus.com/reference/cstdio/fprintf/)

, which you first need to open. In this case, the file is opened for [FILE](http://www.cplusplus.com/reference/cstdio/FILE/)*appending* (`"a"`

). You can also open a file for *writing* (`"w"`

– this will clear the file first) or *reading* (`"r"`

). You can also open the file for *binary* reading and writing, using `"rb"`

and `"wb"`

respectively.

Before we continue, you need to make a file for testing purposes. Using notepad, create a file named `settings.txt`

and place it in the directory where you unzipped **TheTemplate.zip** file. Put the following info in it:

|
1 |
xpos = 100
|

Now, in your `Game::Init`

function, add the following code:

|
9
10
11
12
13
14
|
void Game::Init()
{
FILE* f = fopen("settings.txt", "r");
fscanf(f, "xpos = %f", &x);
fclose(f);
}
|

When you run the application, you will see that the cube starts bouncing at `x = 100`

now, and you can change the start position using a configuration file, without recompiling your code. This is a very useful feature for games!

The data that we have written to and read from a file so far has been *text-only*. The advantage of this is that the resulting files are *human-readable*; the disadvantage is that the files get somewhat large. A float variable, for instance, needs `4`

bytes in memory, but in a file, `3.14159265358979`

requires 16 bytes.

If you don’t need to be able to read the file yourself, you can use binary file i/o. This lets you write the contents of any variable, or even better, the contents of any area in memory, directly to a file. Here are some examples:

|
9
10
11
12
13
15
|
void Game::Init()
{
FILE* f = fopen("bindat.bin", "wb");
fwrite(&x, 4, 1, f);
fwrite(&y, 4, 1, f);
}
|

This code will create a file for binary writing. Then, it writes two blocks of 4 bytes (the size of a float). The first line (line 12) writes the value of `x`

to the file, and the second line (line 13) writes the value of `y`

to the file.

Note that you need to know how large a variable is to be able to store it to a file. When in doubt, use the

operator:[sizeof](https://en.cppreference.com/w/cpp/language/sizeof)

|
12 |
fwrite( &x, sizeof(x), 1, f );
|

Compared to just writing `4`

this will not make your code slower, it’s just more typing.

Reading the data from such a file is very similar:

|
11
12
13
14
|
FILE* f = fopen( "bindat.bin", "rb" );
fread( &x, 4, 1, f );
fread( &y, 4, 1, f );
fclose( f );
|

This time, the file is opened for binary reading, and

is used instead of [fread](http://www.cplusplus.com/reference/cstdio/fread/)

.[fwrite](http://www.cplusplus.com/reference/cstdio/fwrite/)

Create a function that saves the contents of the screen to a `.tga`

image file that can be loaded into your favourite image editing application.

A `.tga`

file consists of a *header* and the actual image data. For the image data, you can simply save lines of pixels. For the header, you need the following data:

|
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
|
struct TGAHeader
{
unsigned char ID, colmapt; // set both to 0
unsigned char type; // set to 2
unsigned char colmap[5]; // set all elements to 0
unsigned short xorigin, yorigin;// set to 0
unsigned short width, height; // put image size here
unsigned char bpp; // set to 32
unsigned char idesc; // set to 0
};
|

You can now create a variable of type `TGAHeader`

:

|
16 |
TGAHeader header;
|

The size of the header is (and absolutely must be) precisely 18 bytes. You can verify this again using `sizeof(TGAHeader)`

.

Finally, you can set individual fields of this header:

|
17 |
header.ID = 0;
|

- Find one of your previous assignments and add a
`Game::ScreenShot`

method to it. - Add code to your application that saves a screenshot whenever you press a specific key on the keyboard.

Use

to produce file names like [sprintf](http://www.cplusplus.com/reference/cstdio/sprintf/)`screenshot001.tga`

where each new screenshot increments the last three digits of the filename.

**Previous Part: Fixed Point**

**Next Part:**