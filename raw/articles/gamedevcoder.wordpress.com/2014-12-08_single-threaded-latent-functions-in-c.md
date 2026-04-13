---
title: (Single-Threaded) Latent Functions in C++
url: https://gamedevcoder.wordpress.com/2014/12/08/single-threaded-latent-functions-in-c/
published: '2014-12-08'
source_blog: Gamedev Coder Diary
source_site: https://gamedevcoder.wordpress.com
category: game programming
fetched: '2026-04-13'
---

I’ve been recently considering conversion of one object oriented [Unreal Script](http://en.wikipedia.org/wiki/UnrealScript) like language code into C++ to improve its run-time performance. And while most of the features of the language seemed easy to transform from one to another there was one that wasn’t trivial to do: latent functions.

Now, just to make sure: by latent functions here I mean functions that might take a long time to finish and this is not because they’re heavy functions but because they might need to wait for something. The best example of such function is Sleep().

My goal was to support execution of multiple such functions on a single thread without having to block i.e. whenever the function needs to wait for something it should get paused and it should be possible to resume it later at any time. Pseudo-code sample:

int MyFunction( float a ) { [...] // Some code Sleep( 1 second ); // Wait 1 second [...] // Some code Sleep( 2 seconds ); // Wait 2 seconds [...] // Some code } [...] call.Call( MyFunction, 10.0f ); // Call MyFunction with a == 10.0f while ( !call.IsDone() ) // While not finished { call.Advance(); // Keep resuming [...] // Other code } result = call.GetResult(); // Done! Now get the result

What I ended up with is a very small library that makes implementing latent functions in C++ a bit easier to write (and read!). My implementation is based on an idea described in [Coroutines in C](http://www.chiark.greenend.org.uk/~sgtatham/coroutines.html) but goes beyond what’s presented there in that it:

- allows for arbitrarily nested latent function calls
- doesn’t require programmer to access parameters or local variables via context struct (makes the code look a lot more like ‘normal’ code)
- fully supports canceling latent call without memory leaks; this is achieved by storing individual parameters and local variables along with their destructor functions

But the main trick stays the same and is the fact that individual ‘case’ blocks can be placed anywhere inside of the ‘switch’ block which allows us to jump pretty much anywhere in the function body – almost like goto instruction. In particular, using this language feature, we can jump to where we left off previously and resume code execution.

The only major limitation of this implementation, and one I’d love to be able to solve but I’m afraid there’s no solution for it in pure C++, is that one can’t place latent function calls returning non-void value inside of an expression, e.g. inside an ‘if’ condition. This is because it’s impossible to use switch-case (or goto) to jump to inside of an expression.

Check out [LatentLib](https://github.com/macieks/LatentLib) on github and let me know what you think. But please keep in mind that it hasn’t been implemented with high performance in mind (separate dynamic memory allocation per variable and stack frame) but more so to present the general concept.

Why not just use setjmp/longjmp style coroutines?

Or, if you’re really interested in staying within the language, maybe http://gabriel.kerneis.info/software/cpc/ has some relevant ideas?

What’s the advantage of setjmp/longjmp based approach? Wouldn’t it result in potential memory leaks in the case of coroutine getting canceled? (need to destroy function parameters and local vars in that case). Do you know if there are any successful portable implementations of setjmp/longjmp based approach?

And regarding CPC, I have to say I really like the general idea. It’s a lot more complex approach but it has the potential to solve all the problems with implementations like mine.

One other alternative is to implement continuations in C, which is basically what you’ve done, but you can make the usage a little nicer.

What exactly do you suggest when you say continuations in C?