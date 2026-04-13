---
title: 'Notes on #Minimalism in code'
url: http://c0de517e.blogspot.com/2014/08/minimalism.html
published: '2014-08-23'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

A few weeks ago I stumbled upon a nice talk at the public library near where I live, about minimalism, buy a couple of friends, Joshua Fields Millburn and Ryan Nicodemus, who call themselves "the minimalists".

What it's interesting is that I immediately found this notion of parsimony to be directly applicable to programming. I guess, it would apply to most arts, really. I "live tweeted" that "minimalism in life is probably showing the same level of maturity of minimalism in coding" and started sketching some notes for a later post.

On stage I hear "the two most dangerous words in the English language are:

**one day**". This is going to be good, I wonder if these guys -were- programmers.**- Return of Investment**

In real life, clutter comes with a price. Now, that might very well not be a limiting factor, I think that the amount of crap tends to depend on our self-control, while money just dictates how expensive the crap we buy gets, but still there is a price. In the virtual world of code on the other hand clutter has similar negative consequences on people's mental health, but on your finances it might even turn out to be profitable.

*We all laugh at the tales of coders creating "job security" via complexity*, but I don't really think it's something that happens often in a conscious way. No, what I believe is much more common is that worthless complexity is encouraged by the way certain companies and teams work.

Let's make an example, a logging system. Programmer A writes three functions, open, printf, close,

[it works great, it's fast](http://blog.codinghorror.com/futurist-programming-in-1994/), maybe he even shares the knowledge on what he learned writing it. Programmer B creates a logging framework library templated factory whatever pattern piece of crap, badly documented on top of that.
What happens? In a good company, B is fired... but it's not that easy. Because there are maybe two-three people that really know that B's solution doesn't solve anything, many others won't really question it, will just look at this overcomplicated mess and think that must be cool, complexity must exist for a reason. And it's a framework!



So now what could have been done in three lines takes several thousands, and who wants to rewrite several thousand lines? So B's framework begins to spread, it's shared by many projects, and B ends up having a big "sphere of influence" and actually getting a promotion. Stuff for creepypasta, I know.

[Don't do Boost:: at night (nor ever)](http://www.boost.org/doc/libs/1_55_0/libs/geometry/doc/html/geometry/design.html).*In real life things are even more tricky.*Take for example sharing code. Sharing code is expensive (sharing knowledge though is not, always do that) but it can get beneficial of course. Where is the tipping point? "One day" is quite certainly the wrong answer, premature generalization is a worse sin than premature optimization, these days.

There is always a price to pay to generality, even when it's "reasonable". So at every step there is an

[operation research](http://en.wikipedia.org/wiki/Operations_research)problem to solve, over quantities that are fuzzy to say the least.**- Needed complexity**

In their presentation, Joshua and Ryan take some time to point out that they are not doing an exercise in living with the least amount of stuff as possible, they aren't trying to impose some new-age set of rules.


__The point is to bring attention to making "deliberate and meaningful" choices__, which again I saw as being quite relevant to programming.
Simplicity is not about removing all high-level constructs nor it is about being as high-level, and terse, as possible. I'd say it's very hard to encapsulate it in a single metric to optimize, but I like the idea of being conscious of what we do.




Abstractions are useful to "compress" code (at least, they should always be used for that, in practice many times we abstract early and end up with more code, like writing a compressor where the decompressor takes more space than the original file...), but compression is not an end goal (otherwise we would be editing .zip files!), it can reduce complexity "locally" but it "lifts" it into a new, global, concept, that has to be learned, mastered, maintained...



*If we grab a concept, or a construct, do we know really why, or are we just following the latest fad from a blog for cool programmers?*Abstractions are useful to "compress" code (at least, they should always be used for that, in practice many times we abstract early and end up with more code, like writing a compressor where the decompressor takes more space than the original file...), but compression is not an end goal (otherwise we would be editing .zip files!), it can reduce complexity "locally" but it "lifts" it into a new, global, concept, that has to be learned, mastered, maintained...

*Not that we shouldn't be open minded and experimental, try new tools... This is not about writing everything in C, for the rest of our lives. The opposite! We should strive for an understanding of what to use when, be aware, know more.*

It's cool and tempting to have this

[wide arsenal of tools](https://www.pinterest.com/thequiltercook/fun-kitchen-gadgets/), and as in all arts, we are creative and with experience we can find meaningful ways to use quite literally any tool.

But there is a huge difference between being able to expertly choose between a hundred brushes for a painting, having mastered each, and thinking that if we do have and use a hundred brushes we will get a nice painting. We can't be

[masters of too many things](http://www.fastcompany.com/3027379/work-smart/the-psychology-of-limitations-how-and-why-constraints-can-make-you-more-creative)in our lives, we

[have to chose carefully](http://betterphotography.in/perspectives/great-masters/dream-lens-david-alan-harvey/2344/).

*Complexity is not always useless, but surely should be feared more. And it hides everywhere.*

[Do I use a class?](http://c0de517e.blogspot.ca/2012/09/follow-up-why-classes.html)What are the downsides? More stuff in a header, more coupling? What it's getting me, that I can't achieve without. Do I need that template?

[What was a singleton for again](http://c0de517e.blogspot.ca/2008/04/singletons-new-superglue.html), why would it be better than a static? Should I make that operation implicit in the type? Will the less typing needed to use a thing offset the more code needed in the implementation? Will it obscure details that should not be obscured? And so on...

**- Closing remarks**

Even if I said there isn't a single metric to optimize, there are a few things that I like to keep in mind.

One is the amount of code compared to the useful computation the code does. The purpose of all code is algorithmic, we transform data. How much of a given system is dedicated to actually transforming the data? How much is infrastructural? On a similar note, how much heat am I wasting doing things that are not moving the bits I need for the final result I seek?



Again, this isn't about terseness. I can have a hundred lines of assembly that sort an array or one line of python, they lie on opposite ends of terseness versus low-level control line, but in both cases they are doing useful computation.



The second is the amount of code and complexity that I save versus the amount of code and complexity I have to write to get the saving. Is it really good to have something that it's trivial to use "on the surface", but impossible to understand when it comes to the inner workings?



Sometimes the answer is totally a yes, e.g. I don't really care too much about the minute details of how Mathematica interprets my code when I do exploratory programming there. Even if it ends up with me kicking around the code a few times when I don't understand why things don't work. But I might not want that magic to happen in my game code.



Moreover, most of the times we are not even on the

[Pareto front](http://en.wikipedia.org/wiki/Pareto_efficiency), we're not making choices that maximize the utility in one or the other direction. And most of the times, such choices are highly non-linear, where we can just accept a bit more verbosity at the caller-side for a ton less headache on the implementation-side.
Lastly, the minimalists also talk about the "

[packing party](http://www.theminimalists.com/21days/day3/)": pack everything you have, then unpack only the things that you need as you need them, over a few weeks. Throw away the stuff that stays packed. The code equivalent coverage testing: push your game through an extensive profile step, then mark all the lines that were never reached.
Throwing away stuff is more than fine, it's beneficial. Keep the experience and knowledge. And if needed, we always have p4 anyways.



*Somewhat related, and very recommended:*
## 2 comments:

Thank you for the Futurist Programmers link. I like these kind of stirring ideas even if I don't agree with everything they say.

Post a Comment