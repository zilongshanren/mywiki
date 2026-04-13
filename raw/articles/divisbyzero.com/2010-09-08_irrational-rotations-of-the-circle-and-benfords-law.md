---
title: Irrational rotations of the circle and Benford’s law
url: https://divisbyzero.com/2010/09/08/irrational-rotations-of-the-circle-and-benfords-law/
author: Dave Richeson
published: '2010-09-08'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

Take a collection of real-world data such as the lengths of all rivers in the world, the populations of counties in the United States, the net worths of American corporations, or the street addresses of all residents of Detroit. Strip away all the information except the leading digits. What percentage of these digits do you expect to be 1’s? 2’s? 9’s? Surely the answer is the same for all digits: 11% (1/9), right?

It turns out that in many cases, the leading digits are not uniformly distributed, but obey [Benford’s law](http://en.wikipedia.org/wiki/Benford%27s_law): the leading digit occurs with frequency

. [See

[Terence Tao’s post](http://terrytao.wordpress.com/2009/07/03/benfords-law-zipfs-law-and-the-pareto-distribution/) for details on when Benford’s law applies, but roughly speaking the data must be very spread out (e.g., spanning several orders of magnitude), so data sets like zip codes in the US or heights of adult males won’t follow Benford’s law.]

Thus we expect the leading digits to occur with the following frequencies:

Let us look at a concrete example: powers of 2. The first 20 powers of 2 are: 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, and 524288. The leading digit is 1 six times, that’s 30%, it is 2 four times (20%), and 9 zero times (umm,… 0%).

I computed the first 100 and first 500 powers of 2 and found that the leading digits have percentages:

Amazing!

Benford’s law has been used to detect fraud in tax returns and in election results—the numbers that people make up typically do not follow Benford’s law. For more information you may want to [read](http://terrytao.wordpress.com/2009/07/03/benfords-law-zipfs-law-and-the-pareto-distribution/) other [accounts](http://www.nytimes.com/1998/08/04/science/following-benford-s-law-or-looking-out-for-no-1.html) of [Benford’s](http://www.kirix.com/blog/2008/07/22/fun-and-fraud-detection-with-benfords-law/) law [on](http://plus.maths.org/issue9/features/benford/) the [web](http://www.cut-the-knot.org/do_you_know/zipfLaw.shtml).

In this blog post I will give a proof just for the powers of 2. It is a clever proof that uses a theorem about rotations of the circle that [I wrote about last summer](https://divisbyzero.com/2009/06/18/three-cool-facts-about-rotations-of-the-circle/).

For simplicity we’ll consider a circle of circumference 1; equivalently we may think of the circle as with 0 and 1 glued together or as

, the set of real numbers, modulo 1. Let

denote the fractional part of the real number

. Then

all represent the same point on the circle.


Let be any real number. We can think of the sequence

as the orbit of 0 under repeated rotations of the circle by

. We begin with the point 0 on the circle, rotate by

to obtain the point

, rotate by

again to obtain

, etc. In

[my earlier blog post](https://divisbyzero.com/2009/06/18/three-cool-facts-about-rotations-of-the-circle/) I stated the following theorem.

**Theorem.** Suppose is an irrational number.


1. Then is a dense subset of the circle.


2. Moreover, if is an interval in the circle of length

and there are

elements of

in

, then

.


Part 1 of the theorem states that the orbit of the point 0 under an irrational rotation by “fills up” the entire circle; that is, every open interval on the circle, regardless of how small, intersects this set of points. Part 2 says something even stronger. It says that the orbit fills up the circle in a uniform way—asymptotically the amount of time the orbit spends in an interval is equal to the length of the interval (we often say that “the time average equals the space average”).


So what does this have to do with Benford’s law?

The leading digit of is

provided there exists a nonnegative integer

such that


Taking the logarithm (base 10) of the above inequality we obtain

Equivalently,

Notice that for ,

and

are between 0 and 1. Thus we conclude that the leading digit of

is

provided


But is an irrational number. By the second part of our theorem we know that the percentage of the set

that intersects the interval

is precisely the length of the interval

,

, which is what Benford’s law says.


Dave,

In my blog on Benford’s law I point out that, “As you might have guessed, someone else did it earlier; a half century earlier. In 1881 a note to the American Journal of Mathematics by an American astronomer named Simon Newcomb described an unusual observation. He had noticed that the tables of logarithms that were in common use back then by astronomers, always had the pages of the lower numbers more dog-eared than the pages of the higher numbers. He suggested that natural observations tend to start with the number one more often than with an eight or nine. For some reason, the observation went without much comment. ”

For my students, I point out that before they think Newcomb was TOOOO bright, I point out that in 1903 (only months before the Wright Bros. flight at Kittyhawk) he declared boldly, “”Aerial flight is one of that class of problems with which man cannot cope”.

Thanks, Pat. I hadn’t seen your earlier post. I like that story about Newcomb. I’ll have to see if I can find a book of logarithms in our college’s archives so that I can see the page usage for myself. Also thanks for giving me the publication year of his note. I was able to find it in our online holdings in an instant.

There is a misspelling in the last formula.

should be “log(1 + 1/d)”; there is sign mismatch.

Feel free to remove this comment)

Thanks. It is fixed now.

I think it’s useful to imagine a counter. If you have a lot of numbers you’re counting, the dials at the lower end would move quickly; the ones at the higher end (that represent millions, or hundreds of thousands) would move slowly. Those high numbers wouldn’t flip over very often as the smaller numbers kept turning through all the digits. How often do you hear of 900 million anyway. It’s usually 1.2 million or some lower number, especially with $$$. Thanks for the post.