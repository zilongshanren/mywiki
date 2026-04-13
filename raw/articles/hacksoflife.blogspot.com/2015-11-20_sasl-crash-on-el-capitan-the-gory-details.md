---
title: SASL Crash on El Capitan - the Gory Details
url: http://hacksoflife.blogspot.com/2015/11/sasl-crash-on-el-capitan-gory-details.html
author: Benjamin Supnik
published: '2015-11-20'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I'm trying to not clog up the X-Plane developer blog with tons of technical C++ details. There are a small number of developers who actually want to know those details, so I'm going to post them here. This post explains why












[SASL](http://www.1-sim.com/)was crashing on plugin-unload on El Capitan (but not older operating systems).
Both SASL and Apple's OpenAL implementation are open source, so despite this being a bug that was totally

*not*in the X-Plane code base, I was able to look at everyone involved and debug it myself. I am not particularly happy about having to do that, but the symptoms of the bug were:- Upgrade to El Capitan for free - why not, new things are shiny.
- Run X-Plane - seems okay!
- Run SASL plane - seems okay!
- Switch from SASL plane to plane that ships with X-Plane. Oh noes - my sim crashed! Report a bug to Laminar Research.

So I got involved because users thought this was our bug, even though it wasn't.

Hrm - new crash in Apple's framework in a new OS. Blame Apple! Except, no other OpenAL code is crashing.

### Apple's Bug

It turns out there is a bug in Apple's OpenAL. It's one that has been in there for a long time, but only shows up in El Capitan, and frankly doesn't matter in any real way. On OS X, if you call alcDestroyContext on a context that has (1) playing sounds and (2) is the only context for its device and (2) isn't using effects on those sounds then you get an uncaught exception on El Capitan.

The actual bug is subtle - the tear-down order of the underlying audio units that power Apple's OpenAL implementation isn't quite right in this case, resulting in AudioUnits returning an error code in a destructor. The code throws this and catches it in the underlying alcDestroyContext call.

From what I can tell, there was a

*tool chain*change in El Capitan that causes this to terminate an app. I am not an expert, but I think that throwing an exception out of a destructor is undefined behavior, and now Clang is putting its foot down. When I compiled OpenAL from source, my built version simply caught the exception and returned it from alcDestroyContext.
For what it's worth, I don't consider this a severe bug or engineering failure by Apple. The OpenAL specification is a total disaster, and I don't blame anyone who misses a corner case (assuming deleting a playing context even is legal - with a spec like that, who knows). And no app in its right mind would just go kill the context without stopping audio first. Which brings us to SASL's bug.

### SASL's Bug

SASL had a bug too. SASL uses a stack based C++ class to change the OpenAL audio context from X-Plane's context to its own to do audio work and then turn it back when done. This is a classic RAII way to manage state.

ContextChanger changer(sound->context);

Except the clean-up code in SASL had this:

ContextChanger(sound->context);

That is, of course, totally legal C++, and totally not useful. I look forward to the day when creating a temporary object in its own expression with a non-trivial destructor is a warning, because I've done this in my own code too.

Without a working context changer, SASL's cleanup code would attempt to clean up all of

*X-Plane's*audio objects (not cool man, not cool!) and then kill its own context. Of course, its own context was still playing since no cleanup had happened.
To put it bluntly, this bug makes me pretty mad, and here's why:

- This code has literally never worked right. Not once, not since day one.
- The fact that this code was not working right was
*easily*detectable just by checking the OpenAL error code. When SASL goes to delete sources in the wrong context, in most cases the source names are wrong and OpenAL returns an error code. During development and in debug mode, SASL should be checking the OpenAL error code, at least when it finishes its own work before returning control to X-Plane.

ContextChanger(ALCcontext *context) {oldContext = alcGetCurrentContext();alcMakeContextCurrent(context);alGetError();};

If you don't speak OpenAL, basically that's SASL

*clearing*the error code before beginning audio work, with no check of what is in there. This is*not*how to do error checking.### The Fix Is In

The good news is that the newest version of SASL (2.4 as of this writing) fixes the context changer bug, and also in some cases checks the OpenAL error code after issuing OpenAL commands. The error checking is not as complete as I'd like to see, and still will silence the error sometimes, but it's a step in the right direction.

Are there any teachable moments here? I think there are a few:

- If an API provides return codes* for the purpose of determining program correctness (E.g. OpenAL returning "invalid source") it is absolutely to leverage those return codes to do debug assertion checking.
- It is not good enough to run the code and observe expected behavior at the user level - you need to verify that the code is actually doing what you expect, or you don't know. (A very wise senior engineer once told that to me 21 (!) years ago when I was just an intern at Avid Technology...it's taken me about that long to deeply understand this in my gut.)
- Any time the behavior of code isn't going to be directly user observable (which includes pretty much all resource cleanup code), you need to design the system for debug-ability, e.g. create test cases, attach the debugger, put logging in place, put assertions in place. Proving a program is correct and debugging it is a design requirement just like functionality.

* I don't want to use the term error codes for these returns because I think it is important to distinguish between mistakes in program correctness (you, the programmer, screwed up) and expected failures of hardware (e.g. a disk read error). Having a return enumeration from a function is a coding idiom that can be used for

*either*of these cases. In the case of OpenAL and OpenGL, the returned code detects both programmer mistakes and underlying "errors", e.g. exhaustion of memory.
Hi Ben! Interesting read. Just a quick note about the throwing destructor:

ReplyDeleteThe rules changed slightly recently. In c++98, throwing out of a destructor was perfectly fine during normal execution. However, if a destructor was called due to stack unwinding after an exception was thrown, it would call std::terminate. C++11 introduced the noexcept mechanism as a replacement for the now deprecated throw() specifications. Throwing out of a method marked noexcept results in std::terminate being called as well. And guess what, destructors are now marked noexcept implicitly, resulting in the behavior you observed.

Thanks Stefan - that makes perfect sense. Having examined the stack, it definitely looked like the run-time or compiler had simply decided to abort(). And it's consistent with what I saw: when I compiled the Yosemite OpenAL code (I had to seriously hack the existing x-code project to get it to compile) under C++98, the throw was successfully caught at the outer level of OpenAL.

DeleteA couple days ago, I heard about this and looked at the ancient google code SASL for a couple minutes - the same thing popped out to me. That's a hard bug to eyeball if you're not looking for it!

ReplyDelete