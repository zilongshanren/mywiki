---
title: Furstenberg’s topological proof of the infinitude of primes
url: https://divisbyzero.com/2010/09/08/furstenbergs-topological-proof-of-the-infinitude-of-primes/
author: Dave Richeson
published: '2010-09-08'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

I just returned from a 10-day trip to India. It was my first visit there. I gave a talk at the [ICM Satellite Conference: Various Aspects of Dynamical Systems](http://www.math-msubaroda.in/ds2010.html). The conference was hosted by the [Department of Mathematics](http://www.math-msubaroda.in/) at the [M. S. University, Baroda](http://www.msubaroda.ac.in/), which is in [Vadodara](http://en.wikipedia.org/wiki/Vadodara) (formerly Baroda) in the Indian state of Gujarat. Unfortunately, I wasn’t able to go early to attend the [ICM](http://www.icm2010.org.in/) (International Congress of Mathematicians) in Hyderabad.

![](../../assets/5f84536ad626f639.jpg)


My talk was on [some joint work](http://www.ams.org/journals/proc/2010-138-12/S0002-9939-2010-10434-3/home.html) with my friend and long-time collaborator, [Jim Wiseman](http://ecademy.agnesscott.edu/~jwiseman/). There were a lot of good speakers at the conference (including Jim, who spoke about the research on which we’re currently working). The most well-known mathematician at the conference was [Hillel Furstenberg](http://en.wikipedia.org/wiki/Hillel_Furstenberg). He treated us to an hour-long talk, a presentation of some open problems, and the valedictory address at the end of the conference. I also had the pleasure of eating one dinner with him and his wife.

So I thought I’d take a moment to share one of Furstenberg’s coolest (and shortest) proofs. He published a one-paragraph note in the May 1955 issue of the *American Mathematical Monthly*, entitled “On the Infinitude of Primes.” It is a topological proof that there are infinitely many primes. (Note: apologies to my readers who have not take a course in point-set topology.)

**Theorem.** There are infinitely many primes.

Suppose, for the sake of contradiction, that there are finitely many primes.

We create a topology for the integers () by defining a

[basis](http://en.wikipedia.org/wiki/Base_(topology)), . The basis consists of all

[arithmetic progressions](http://en.wikipedia.org/wiki/Arithmetic_progression). For example, the following sets are elements of :


,


, and


.


How do we know that is a basis? We must check two things. First, it must cover

, which it does. Second, if

and

are in

and

, then there must be an element

such that

. Indeed, suppose

and

are the differences between successive terms in the sequences

and

, respectively. Let

be the least common multiple of

and

. Then

is the required basis element.


Thus generates a unique topology on

. (Furstenberg points out that this topology happens to be

[normal](http://en.wikipedia.org/wiki/Normal_space) and hence [metrizable](http://en.wikipedia.org/wiki/Metrizable_space).)

Observe that every arithmetic progression is a closed set: the complement of each arithmetic progression is an open set since it is the union of (finitely many) arithmetic progressions, each having the same difference. For example,

.


For each prime , let

and let

. We assumed that there are finitely many primes, so

is the union of finitely many closed sets. Thus

is closed and its complement

is open.


However, , which is clearly not open (every open set is either empty or infinite). This is a contradiction. So there are infinitely many primes.


[Update: here’s a [reworked version of Furstenberg’s proof ](http://www.idmercer.com/monthly355-356-mercer.pdf)that avoids all topological language.]

Yes, it is a very cute proof. I think there is something similar in the first chapter of Martin Aigner’s Proofs from the Book.

Hi,

Just curious, but I don’t quite follow the proof – when I suppose I have the finite list of just ‘2’, I get as A the even numbers, and the complement the odd which if I follow is open and so I get no contradiction.

Similarly I can’t see how to get that the complement is {-1,1} without implicitly assuming an infinite number of primes – am I missing something (probably, only have 2nd year topology..)

Like the blog, keep up the good work!

Cheers,

Charlie

Charlie,

The first observation is that the complement of A is open—that by itself is not a contradiction. The “hidden assumption” (which I thought about stating explicitly when I wrote the post, but didn’t) is that every integer other than 1 and -1 is divisible by some prime. That’s why the complement of A is {-1,1}. That 2-element set is not open, and this is gives the contradiction.