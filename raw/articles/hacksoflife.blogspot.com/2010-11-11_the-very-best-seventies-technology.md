---
title: The Very Best Seventies Technology
url: http://hacksoflife.blogspot.com/2010/11/very-best-seventies-technology.html
author: Benjamin Supnik
published: '2010-11-11'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Srsly](http://www.npr.org/blogs/money/2010/10/14/130575234/we-bought-gold).) Lisp is not a computer language; it is a cult that warps the minds of otherwise capable programmers and twists their very notion of what a program is.*

So it is in this context that I began a conscious campaign to reduce the number of parenthesis in my C++. I know, some of you may be saying "

[say what you mean, understand what you say](http://www.aristeia.com/books.html)" and all of that feel-good mumbo jumbo. Heck, my own brother told me not to minimize parens. But I can't have my carefully crafted C++ looking like Lisp. It just won't do.

So slowly I started to pay attention to operator precedence, to see when I didn't actually need all of those "safety" parens. And here's what I found: 95% of the time, the C operator precedence makes the easy and obvious expression the default. I was actually surprised by this, because on the face of it the

[order looks pretty arbitrary](http://www.swansontec.com/sopc.html).

If you squint though, you'll see a few useful groups:

- Unary operators before binary operators.
- Math before comparison.
- Comparison before anything if-like (e.g. && which is more like control flow than an operator).
- Assignment at the bottom.

if( value & mask == flag)doesn't do what you want. You have to write the more annoying:

if((value & mask) == flag)So what went wrong? It turns out there's a

[reason](http://cm.bell-labs.com/cm/cs/who/dmr/chist.html)!

Approximately 5,318 years ago when compilers were made out of yarn and a byte only had five bits, C was being built within the context of B and BCPL. If you thought C was cryptic and obtuse, you should see

[B](http://en.wikipedia.org/wiki/B_%28programming_language%29#Example)and

[BCPL](http://en.wikipedia.org/wiki/BCPL#Examples). B is like C if you removed anything that might tell you what the hell is actually going on, and BCPL looks like you took C, put it in a blender with about 3 or 4 other languages, and played "

[will it blend](http://www.willitblend.com/%27)". (Since BCPL is "no longer in common use", apparently the answer is no. But I guess they couldn't have thought it looked like a C blend at the time, as C hadn't been invented.)

Anyway, in B and BCPL, & and | had a sort of magic property: inside an if statement they used lazy evaluation (like && and || in C/C++) - they wouldn't even bother with the second operand if the first was true or false. So you could write things like this: if(ptr & ptr->value) safely. But you could also write flag = ptr & 1; to extract the low bit.

In a rare moment of preferring sanity over voodoo, Dennis Ritchie chose to split & and | into two operators: | and & would be bit-wise and always evaluate both operators, while && and || would work logically and short-circuit. But since they already had piles of code using & as both, they had to keep the precedence of & the same as in B/BCPL (that is, low precedence like &&) or go back and add parens to all existing code.

So while & could be higher precedence, it's not for historical reasons. But have patience; we've only had to live with this for 38 years. I am sure that in another 40 or 50 years we'll clean things up a bit.

* A program is a huge mess of confusing punctuation. Something clean and elegant like this:

[for(;P("\n"),R=;P("|"))for(e=C;e=P("_"+(*u++/ 8)%2))P("|"+(*u/4)%2);](http://simson.net/ref/ugh.pdf)


Don't forget about 1 << 2 + 3. Basically, all bit ops have the precedence that's usually useless for performing bit ops. Oh well.

ReplyDeleteGood call...although weirdly << is above | so if you are just constructing bit fields you can do


ReplyDelete1 << position | other_flags

But yeah, for things like 1 << bits - 1 it's kind of hosed.