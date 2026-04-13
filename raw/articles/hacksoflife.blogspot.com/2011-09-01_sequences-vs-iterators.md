---
title: Sequences Vs. Iterators
url: http://hacksoflife.blogspot.com/2011/09/sequences-vs-iterators.html
author: Benjamin Supnik
published: '2011-09-01'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Lately I've been playing with an STL "sequence" concept. That's a terrible name and I'm sure there are other things that are officially "sequences" (probably in Boost or something) and that what I am calling actually have some other name (again, probably in Boost). Anyway, if you know what this stuff should be called, please leave a comment.


EDIT: Arthur pointed me to


Basically: a sequence is a data type that can move forward, return a value, and knows for itself that it is finished - it is the abstraction of a C null-terminated string. Sequences differ from forward iterators in that you don't use a second iterator to find the end - instead you walk the sequence until it ends.


Why would you ever want such a creature? The use case that really works nicely is adaptation. When you want to adapt an iterator (e.g. wrap it with another iterator that skips some elements, etc.) you need to give your current iterator both an underlying "now" iterator and the end; similarly, the end iterator you use for comparison is effectively a place-holder, since the filtered iterator already knows where the end is.


With sequences life is a lot easier: the adapting sequence is done when its underlying sequence is done. Adapting sequences can easily add elements (e.g. adapt a sequence of points to a sequence of mid points) or remove them (e.g. return only sharp corners).


My C++ sequence concept uses three operators:






EDIT: Arthur pointed me to

[this paper](http://www.uop.edu.jo/download/PdfCourses/Cplus/iterators-must-go.pdf); indeed what I am calling sequences are apparently known as "ranges". Having just recoded victor airway support and nav DB access using ranges, I can say that the ability to rapidly concatenate and nest filters using adapter templates is a*huge*productivity win. (See page 44 to have your brain blown off of its hinges. I thought you needed Python for that kind of thing!)Basically: a sequence is a data type that can move forward, return a value, and knows for itself that it is finished - it is the abstraction of a C null-terminated string. Sequences differ from forward iterators in that you don't use a second iterator to find the end - instead you walk the sequence until it ends.

Why would you ever want such a creature? The use case that really works nicely is adaptation. When you want to adapt an iterator (e.g. wrap it with another iterator that skips some elements, etc.) you need to give your current iterator both an underlying "now" iterator and the end; similarly, the end iterator you use for comparison is effectively a place-holder, since the filtered iterator already knows where the end is.

With sequences life is a lot easier: the adapting sequence is done when its underlying sequence is done. Adapting sequences can easily add elements (e.g. adapt a sequence of points to a sequence of mid points) or remove them (e.g. return only sharp corners).

My C++ sequence concept uses three operators:

- Function operator with no arguments to tell if the sequence is still valid - false means it is finished.
- Pre-increment operator advances to the next item.
- Dereference operator returns the current value.

`while(my_seq())`

{

do_stuff_to(*my_seq);

++my_seq;

}


Sounds like you're talking about ranges.




ReplyDeleteAndrei Alexandrescu gives a pretty good introduction on the concept in his presentation "Iterators Must Go".

The first mirror of it I could find was here: http://www.uop.edu.jo/download/PdfCourses/Cplus/iterators-must-go.pdf. He starts talking specifically about ranges around slide 12 of 52.

(Not most Google links to the PDF were to boostcon.com, which was down at the time I was searching.)

This is very similar to Python's notion of an iterator:




ReplyDeleteiterator.next(): Return the next item from the container. If there are no further items, raise the StopIteration exception.

The only difference is that yours is the look-before-you-leap version (which matches up with python vs c's opinions on exceptions, so it's a good change IMO)

http://docs.python.org/library/stdtypes.html#iterator-types