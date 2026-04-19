---
title: '16BPP.net: Blog / C8: My new CHIP-8 Emulator'
url: https://16bpp.net/blog/post/c8-my-new-chip-8-emulator
published: '2014-07-19'
source_blog: '16BPP.net: Blog / Page 1'
source_site: https://16bpp.net/
category: graphics
fetched: '2026-04-19'
---

During my spring break (sometime in March), I decided to revisit my ![Blitz by David Winter](../../assets/bf41ab9d12298d71.png)


[old CHIP-8 emulator](http://16bpp.net/blog/post/status-update-2)that I made in the beginning of the school year.

I consider both to be separate projects. There are quite a few differences between the new one and the older one.


**Done in C++ instead of C**

C is a lot of fun and this could have been done without the help of classes, but I felt using an object orient approach to this made a bit more sense and made components of the CHIP-8 machine a bit more reusable.


**Uses the newer SDL2 library**

This is not too much of an advancement, except that the emulator is a bit more future proof. I've been looking for an excuse to learn the differences between the newer and older SDL libraries and I think this gave a pretty good foundation. So far I really like the changes that have been made to the API.


**Much better modularized and cleaned up**

The older emulator was essentially a one source file behemoth. In this one, I looked at the CHIP-8 machine as a hole and split it up into smaller parts that would be interconnected. For instance, there are separate Display, CPU, Stack, Memory and Buzzer objects. One of the original ideas was to have a version that ran on SDL2 and another on Qt (but I decided not to do a Qt version), so I tried to make sure that most of these objects were not dependent upon a specific platform. Certain components, like the Buzzer, are. Most of the platform specific code is supposed to be put into the main program loop or separate source files


There are also variations of CHIP-8 out there and these objects are able to accommodate “non-standard,” CHIP-8 systems in case you wanted an emulator for their ROMs. It also wouldn't be as hard to add in Super CHIP-8 support, but I'm not doing that for a while.


**B**![Brix by Andreas Gustafsson](../../assets/283be15961f04937.png)

**etter interpretation of CHIP-8 and more ROMS working**

While I don't have all of the ROMs complete working order I have much more than I did with the last emulator. I grabbed a copy [Frédéric Devernay's SVision-8 emulator](http://devernay.free.fr/hacks/chip8/) and used it as a reference since I don't have a real piece of CHIP-8 hardware with me. With the last emulator I just read the CHIP-8 manuals and online resources on how the op-codes are interpreted. For a few of them, there is some non-consensus for what they do. This of course was quite frustrating. I would say now though that I have a good 80-90% of ROMS working perfectly versus the older one that was more around 60-70%.


**More features**

Nothing too significant other than the addition of saves states. They seem a little complex at first, but they were actually quite easy to implement. Essentially it's either dump/load all of the registers, stack, and memory into/from a file. My emulator supports one thousand save states (though you could change the number if you wanted), but I doubt anyone will use that many for a measly CHIP-8 program.

I also added in step-by-step execution. This was mainly done for my purposes of debugging, but the code is still in there in case someone wants to run through a ROM step-by-step. They would need to edit a boolean value in the source to turn it on.


**Final Thoughts**

With all that, I'm fairly happy with how it turned out. The only things that frustate me are the ROMs that still don't work. I haven't touched most of the source code since, just the README file to document it a bit better. If you want to checkout the source, [the repo is right here](https://github.com/define-private-public/c8).