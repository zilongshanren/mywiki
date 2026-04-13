---
title: Game Engine Architecture
url: http://gameenginebook.blogspot.com/2014/09/from-damon-connolly-heya-jason.html
author: Jqgregory
published: '2014-09-17'
source_blog: Game Engine Architecture
source_site: http://gameenginebook.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

**From:**Damon Connolly

Heya Jason. Not sure if you get the time to read through emails often, so I'm just hoping here!

I've recently made the transition from music composition into programming but I'm still new. I have a few issues I'm a bit stuck with and (This will sound totally gay..) You are my hero, Even my mentor who is a pretty high up programmer in another AAA company, recommended your book and said "If you want to be a programmer, You don't do anything, ANYTHING, without first reading this masterpiece".

So my issues:

Everyone says (for example) ints are different sizes on different platforms with different compilers etc etc etc. On one it can be 32 bits on another it can be 64 bits.

Now, in my coding convention i never use "int" or "short int", etc, I always use __int32 or __int16, I even use __int8 if I know the int will always be a small number (i know thats the same as char, and i use char when storing letters, for readability).

What confuses me is, what takes priority? if I'm working on a system in which an int is 64 bits, but i create an int using __int32 does that now force the int size to be 32 bits or does the "32" only go as far as the type name, and despite it being "__int32 myInt", it would actually still be 64 bit or something?

Thank you so much! (not just for reading but just generally being one of the worlds top-most software engineers)

**--------------------------------------**

Hi Damon,












First let me thank you for the kind words! Hearing stories like that make all the hard work of putting together a technical book worthwhile!

Re your question, I think you're confusing the "natural" word size of the CPU with the sizes of individual variables. You can declare and use variables and data objects of any size -- from char/__int8 to __int64 or __m128 (SIMD vectors), and of course you can also declare structs/classes of any size (even GB's in size, although that would be weird). A variable's size is whatever you declared it to be, period.

The natural word size of the CPU is typically defined to be the size of its internal registers, and hence the size it prefers to work with (i.e., can work with most efficiently). But the compiler will generate code such that any sized int will work. e.g., If you try to work with an __int8, but the CPU's natural word size is, say, 32 bits, then the compiler will generate code that loads 32 bits worth of data from memory into a register, and then shifts and masks things off (or uses 8-bit CPU instructions if the CPU supports them) to manipulate those 32 bits AS IF only the 8 bits of your variable are "in play" (i.e. they are shifted down to the least-significant 8 bits, and the upper 24 bits are treated as zeros). But if you load a 32-bit integer on a 32-bit machine, then things are as efficient as possible, because all that shifting and masking and/or using of special 8-bit instructions isn't required.

Now, int and long and char et al are a bit weird because they don't declare universal sizes on all target hardware. Instead they declare pre-defined sizes that

*differ*on different target CPU architectures. So int is*usually*32 bits, but might end up being 64 on some architectures. But that said, once the size has been determined (and it is fixed forever by the designers of your compiler for any given target CPU), then things work exactly as if you had used an explicitly-sized type like __int32. The only thing you need to find out is what that size actually is for your particular combo of compiler+target CPU. Or if you don't care (which is the intent of int et al, after all!), just know that int is typically the most efficient integer type on any CPU, and that it is*at least*32 bits, but might be more.
What I do is simply to use int for almost all local variables (where I don't care about the size and I just want efficiency), and explicitly-sized types for data members within classes and structs (where I often want to control the layout of the object in memory, so I need to know the exact sizes of everything). Basically try to avoid sized types unless your code really cares about the size (and the possible range of values being stored). Another reason to used sized types is if you're potentially dealing with very large values, like e.g. an offset into a file (which could be GB in size) -- so I'd need an unsigned 64-bit int to be sure I cover all reasonably possible file sizes. But 99.9% of your ints are going to be "small" (i.e., <= 0x7fffffff, the largest signed 32-bit value) so who cares, just use int and be efficient.

Make sense? :)

Cheers,

J


P.S. By the way, would it be OK if I included your email and my response on the book's blog (





That would be totally okay! I'll make the blog open up as one of my startup tabs in chrome too :) In fact I'm pretty excited just to get a response from you (I've never idolized in talentless idiots who were famous just for being on TV, I've always idolized in people with inhuman skillsets, so if I met you it would be a "can i have a photo with you and can you sign my book" situation). You also have a really good knack for taking something ridiculously complex and explaining it in a good mix of tech and laymans terms to make it understandable. I have quite a few code books but it's hard to go through any of them due to the fact that every 2 pages theres a massive barely readable code example. I really love that you explain something with metaphors and laymans terms, then put diagrams to show it, and then show succinct code examples. In fact it's so good and so... i dont know how to put it, maybe "optimization-caring" that it's spilling into other areas of my life, My environment art has improved so much, in texel density vs memory usage, using shader tricks to reduce mem usage even more etc etc







P.S. By the way, would it be OK if I included your email and my response on the book's blog (

[http://gameenginebook.](http://gameenginebook.blogspot.com/) blogspot.com/)? Please let me know.**--------------------------------------**

That would be totally okay! I'll make the blog open up as one of my startup tabs in chrome too :) In fact I'm pretty excited just to get a response from you (I've never idolized in talentless idiots who were famous just for being on TV, I've always idolized in people with inhuman skillsets, so if I met you it would be a "can i have a photo with you and can you sign my book" situation). You also have a really good knack for taking something ridiculously complex and explaining it in a good mix of tech and laymans terms to make it understandable. I have quite a few code books but it's hard to go through any of them due to the fact that every 2 pages theres a massive barely readable code example. I really love that you explain something with metaphors and laymans terms, then put diagrams to show it, and then show succinct code examples. In fact it's so good and so... i dont know how to put it, maybe "optimization-caring" that it's spilling into other areas of my life, My environment art has improved so much, in texel density vs memory usage, using shader tricks to reduce mem usage even more etc etc

I don't know if authors/teachers have "target audiences" to "test" their teaching methods, but as someone who is new to programming, but (despite how much people tell me to) cannot overlook the little things I'm not supposed to know about yet like the internal memory padding inside of a struct, controlling the size of everything as much as i can etc, your book REALLY touches on all the little things I've never seen others cover. It's now even getting through to my girlfriend (and trying to get low level stuff through to my girlfriend is like trying to push butter through a sieve)

I just watched your "dogged determination" talk which also boosted my confidence. Hearing how you guys at naughty dog work, really helped boost me back up in knowing that the good guys are still out there somewhere.

Thank you for the answer on the data sizes, that really helped! I'm really excited about the road ahead in programming now!

PS: Sorry about babbling on! I wanted you to know the extent to which your book helps! but please come to the Uk some time so I can buy you a beer and get my book signed!

**--------------------------------------**



Thanks again for all the amazingly kind words! :) I'm flattered and blushing a bit right now. ;) Really glad my work is of help to the game programming community!

I'll give you a ring if I'm in the UK, thanks! (Haven't been yet, would very much like to go someday...)

Cheers,

J

I have played and enjoyed it. Before I play other games Its name is Khu vuon tren may. Now move on to this game.

ReplyDelete