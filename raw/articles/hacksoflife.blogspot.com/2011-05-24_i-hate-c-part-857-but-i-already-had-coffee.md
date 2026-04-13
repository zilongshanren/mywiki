---
title: 'I Hate C++ Part 857: But I Already Had Coffee!'
url: http://hacksoflife.blogspot.com/2011/05/i-hate-c-part-857-but-i-already-had.html
author: Benjamin Supnik
published: '2011-05-24'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I suppose what you object to here is more the naming standard used than the expression itself? Definitely agree that Java has better recommended naming standards and I would use such names if I were to use C++ today.

No - the objection is to C's "," operator. In this case, instead of getting the 4-argument is_edge, I get the 2-argument is_edge, and then the return value of is_edge is replaced by the random values of the uninitialized h, vnum.

It's a case of too many forms of syntactic sugar. The result is that nearly anything compiles, no matter how silly.

I suppose what you object to here is more the naming standard used than the expression itself? Definitely agree that Java has better recommended naming standards and I would use such names if I were to use C++ today.

ReplyDeleteNo - the objection is to C's "," operator. In this case, instead of getting the 4-argument is_edge, I get the 2-argument is_edge, and then the return value of is_edge is replaced by the random values of the uninitialized h, vnum.


ReplyDeleteIt's a case of too many forms of syntactic sugar. The result is that nearly anything compiles, no matter how silly.

Ok I see it now :) Wow, hope the compiler issues some kind of warning here at least on pedantic levels.

ReplyDelete