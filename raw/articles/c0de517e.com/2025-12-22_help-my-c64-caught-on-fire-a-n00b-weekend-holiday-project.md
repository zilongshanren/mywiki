---
title: Help! My c64 caught on fire!A n00b weekend holiday project.
url: https://c0de517e.com/026_c64fire.htm
author: Angelo Pesce
published: '2025-12-22'
source_blog: 'c0de517e''s weblore: Main Entrance.'
source_site: https://c0de517e.com/
category: graphics
fetched: '2026-04-19'
---

I flew back to Italy for the Christmas holidays, as I usually do. Here I have my childhood c64, on which I learend how to program, and which in the last few years I took to refurbishing.

In general, everytime I'm back to my parent's place I spend some time fixing and sorting out things, and this is one of them.

Now it works like a charm, and of course I also added some

[bells and whistles](https://c64os.com/buyersguide/), mostly stuff that allows me to easily tranfer programs from a PC (a kung-fu cart and a pi1541) - so this year I thought it was time to actually do something with it!

I decided to turn it into a cozy fireplace:

![(click on the image for the full-color version)](../../assets/54ce9a1cda46b88a.png)

(click on the image for the full-color version)
I was quite surprised that it worked, that I managed to complete this project in a few hours over two days, and that it was, most of all, fun!

I expected... more friction, having to work with arcane cross-platform toolchains and the like, but instead I completed almost of all it in a web-based IDE/emulator combo!

Moreover, I am far from being an expert when it comes to c64 coding. Yes, I used to program with one... when I was six or seven! And yes, I do follow its demoscene, and over the years I've read quite a bit about its chips and inner workings, but I've never written any demo effect for it.

In other words... if I managed, you can too! That's what made me want to write this post...

**All you need for Christmas...**
...is a 6502.

Here, I'll give you a crash course on the c64 - the key points of what I knew before starting this.

If you know how modern CPUs work, and how to optimize for them - try to forget all of that. The 64 comes from an era where RAM was faster than compute. Lookup tables are your friend, as it is fully unrolling loops / code generation. We have no caches!

Don't be surprised then to learn that the famous 6502 CPU has only one arithmetic register, the "accumulator". There are also two "index" registers used to offset memory locations, a status register, and a program counter - but you can't do math on any of these, at best, test or increment/decrement.

Moreover, the program counter is the only 16-bit register, all the others are 8-bit.

But who needs registers when you have fast RAM? Memory is your register file: pretty much all 6502 instructions operate between the accumulator and memory locations (or numeric constants, that are still memory, just part of the instruction itself).

To further facilitate this, the 6502 comes with a rich set of addressing modes, most instructions can fetch memory in few different ways: at absolute addresses, at addresses offset with one of the two index registers or even at indirect addresses (addresses contained in memory locations).

There is also a special memory area, called the "zero page", the first 256 bytes of memory (a page is, unsurprisingly, 256 bytes), which has an extra optimization: addressing there takes one cycle less, because the address can be encoded in the instruction in a single byte instead of two.

Have a look at the

[6502 instruction set](https://www.masswerk.at/6502/6502_instruction_set.html), it's very simple! Won't take more than 15 minutes to skim over them all.

**The plan.**
Where things get less simple is to deal with all the c64 custom chips, the SID (sound) and the VIC-II (graphics). That's how demo-scene effects are done! Manipulating these chips in very precise ways to cause them to generate crazy stuff, most of which was never considered possible by the c64 designers back then!

The average c64 demo effect is all about this - generating lookup tables and unrolled assembly to then be able to exactly time internal chip status changes as the video signal is being generated line by line ("racing the beam"). Usually, what is shown on screen is not at all what it seems - i.e. it's not how you would create a similar effect on a PC.

![We won't be porting Second Reality...](../../assets/bd2728a01274a74d.png)

We won't be porting Second Reality...
I know almost nothing of any of this - so my plan was to avoid it all! I wanted to set the VIC-II in some graphic mode that gave me a decently simple, linear framebuffer, and from there on write the code like I would have done on any other computer, hoping that a fire effect is simple enough to compute that the 64 would just be able to cope with it.

Luckily, there is one such mode. The default, vanilla, character mode! Here, we have 40x25 characters on screen, chosen from a set of 256. So, one byte per "pixel", and 1000 pixels in total - great!

![The default "petscii" character set.](../../assets/0893610a57835b11.png)

The default "petscii" character set.
Now, the default character set does not really lean itself to creating a demo effect, but I knew I could create a custom one. My idea was to simply making a dither pattern, and as much as possible work like I had a 8-bit "grayscale" screen.

C64 characters are 8x8, so I could create a dither pattern that has a number of "on" pixels in the character corresponding to its position in the charset: 0 being fully off (background color), 64 being fully on (foreground color), and everything in between being a mix.

Of course though this would give us only 64 values, ideally, I wanted to utilize the whole 8-bit space... On obvious idea is that we could add colors to the mix. For example, having the first 64 values go from black (background) to brown (foreground), then the next 64 have brown as background and red as foreground, then red and yellow, and finally yellow and white.

![My custom charset. Made by hand in C64Studio.](../../assets/54b9414b3cd072f5.png)

My custom charset. Made by hand in C64Studio.
This can't be achieved in the default character mode, unfortunately, as only the foreground color is controllable per-character (via another memory location, still using one byte per character - easy), while the background is shared. Luckily though, there is an

["extended color mode"](https://www.c64-wiki.com/wiki/Extended_color_mode) that fits the bill exactly. In this mode the character set is limited to 64, but the two high bits of each character can be used to control the background color, while the foreground remains in the separate memory location as usual.

**Implementation.**
All development was done in the

[retrogamecoders c64 IDE](https://ide.retrogamecoders.com/), which handly couples the

[cc65 compiler](https://cc65.github.io/) with an emulator.

Writing c64 code in C is generally a terrible idea, and cc65 is not even the "best" compiler out there (is quite old and barely does optimize the generated code -

[llvm-mos](https://llvm-mos.org/wiki/Welcome) might be better), but being able to test in C and then gradually "port" to assembly was crucial for a noob like me. If I were to keep working on this, I'd probably move to

[Kick Assembler](https://theweb.dk/KickAssembler/Main.html#frontpage), which is particularly suited for the kind of code-generation that you want to do in demo-coding.

Anyhow, here are the .c files, step by step, in chronological order. You can just copy and paste them in the retrogamecoders IDE and see how things work, start tinkering if you like! Enjoy!

![](../../assets/ae1b5c08c219d85b.png)

-

[First test of the ECM charset idea.](./026_c64fire/test.c)
-

[Slowest fire-effect ever in pure C.](./026_c64fire/slow.c)
-

[Still in C. Starting to "unroll".](./026_c64fire/fire_0.c)
-

[Starting to port to assembly.](./026_c64fire/fire_1.c)
-

[Ported to assembly, with side-by-side C.](./026_c64fire/fire_2.c)
-

[Assembly only, some more ECM tricks.](./026_c64fire/fire_3.c)
-

["Final" version.](./026_c64fire/fire_4.c)
**Conclusions.**
Something like this could be a good weekend project for anyone.

It might even be a nice idea to make a booklet, like the famous "raytracing in one weekend", maybe using a 386 and a VGA instead of the c64... Could be a fun way to teach graphics and low-level programming.

Perhaps one day...

P.s.

- More experienced c64 devs might have used a

[4x4](https://codebase64.net/doku.php?id=base:4x4_charset_fire_with_lots_of_colors) or

[2x2 mode](https://codebase64.net/doku.php?id=base:nmis_and_distributed_jitter-correction_routines) - unfortunately, these are much trickier to code, requiring to think about triggering badlines, raster timing and jitter, but also... they would result in more resolution, which takes more time for the fire effect itself. Time we don't have. And there is much more overhead to these modes to begin with!

- Maybe next year I'll try the same on an Amiga. Unfortunately, even there is not as easy as it might sound, as famously Amigas do not have "chunky" (linear framebuffer) modes, instead having all their bitmap graphics displayed through planar (one bit per plane) modes. This is a cheap trick that was used to save on memory and scanout complexity, but it makes it incredibly hard to code framebuffer effects, and again, the conversion takes time...