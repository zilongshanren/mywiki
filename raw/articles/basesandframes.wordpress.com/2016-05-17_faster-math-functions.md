---
title: Faster Math Functions
url: https://basesandframes.wordpress.com/2016/05/17/faster-math-functions/
author: Robingreen
published: '2016-05-17'
source_blog: Bases and Frames
source_site: https://basesandframes.wordpress.com
category: graphics
fetched: '2026-04-13'
---

I was trying to interpolate a scaling function on an SPU on PS3 and realized, this device has no math library. How do you write `powf()`

without access to `libm`

? The[ IEEE754 standard for floating point numbers](https://standards.ieee.org/findstds/standard/754-2008.html) only covers five fundamental functions – addition, subtraction, multiplication, division and unary negation. It explicitly punts on offering any accuracy or correctness guarantees for transcendental functions leaving accuracy up to the library implementation. It’s amazing that floating point beyond simple expressions ever works.

This began a deep dive into how the transcendental functions are derived and coded. Source code for an implementation of is available through the [Cephes math library](http://www.netlib.org/cephes/) and the source comments have a wealth of [pragmatic experiences embedded](http://www.netlib.org/cephes/singldoc.html#acos) in them:

/* asinf.c * Inverse circular sine * * SYNOPSIS: * * float x, y, asinf(); * * y = asinf( x ); * * DESCRIPTION: * * Returns radian angle between -pi/2 and +pi/2 whose sine is x. * * A polynomial of the form x + x**3 P(x**2) * is used for |x| in the interval [0, 0.5]. If |x| > 0.5 it is * transformed by the identity * * asin(x) = pi/2 - 2 asin( sqrt( (1-x)/2 ) ). *

The code mentions “Cody & Waite” in many places, referring to the book [ Cody, W.J. & W. Waite “Software Manual for the Elementary Functions”, Prentice Hall, 1980, ISBN 0138220646](http://www.amazon.com/Elementary-Functions-Prentice-Hall-computational-mathematics/dp/0138220646/) – a title so out of print that many people work from their own a photocopied version of the title, copies of copies that are handed down between researchers. (To get a feel for what hand typeset technical documents from the 1980’s read like, take a look at

[C.G.van der Laan,](http://oai.cwi.nl/oai/asset/13122/13122A.pdf))

*“Calculation of Special Functions”*, 1986A more recent book [Muller, Jean-Michal, “Elementary Functions: Algorithms and Implementation (2nd Edition)”, Birkhauser, 2005, ISBN-13: 978-0817643720](http://www.amazon.com/Elementary-Functions-Implementation-Jean-Michel-Muller/dp/0817643729/) covers range reduction, minimax polynomials and especially CORDIC implementations in intense detail.

### The Saga of IEEE754

Cody & Waite was written in the days before IEEE754 and had to take into consideration the many accuracy and representation issues of competing hardware architectures around at the time. It was the days of the numerical wild west where anything goes and everyone played fast and loose, and every mainframe and minicomputer maker had their own standards of varying levels of efficiency and accuracy. DEC, IBM, Cray, etc.

The dramatic [story of how IEEE754 was created](http://www.eecs.berkeley.edu/~wkahan/ieee754status/754story.html) is a story of David vs. Goliath. Representatives of the nacient microprocessor industry decided to get together to create one true floating point specification that they could all use to interchange data. The big iron makers were invited but none of them decided microchips were worth bothering with. Intel under Dr John Palmer had ideas for an IC that would be fast, but for patent reasons he couldn’t share with the committee how he was able to implement floating point exceptions as a pipeline bubble, the other manufacturers didn’t believe the standard could be implemented in 40,000 gates and so proposed a different standard without the gradual underflow (a.k.a denormalized floats) method. There was a standoff between Digital Equipment’s VAX- format that had worked well in the minicomputer world for a decade, and the Kahan-Coonen-Stone (K-C-S) proposal from Intel. It came to a head:

“DEC tried to break the impasse by commissioning Univ. of Maryland Prof. G.W. (Pete) Stewart III, a highly respected error-analyst, to assess the value of Gradual Underflow. They must have expected him to corroborate their claim that it was a bad idea. At a p754 meeting in 1981 in Boston Pete delivered his report verbally: on balance, he thought Gradual Underflow was the right thing to do. ( DEC has not yet released his written report so far as I know.) This substantial setback on their home turf discouraged DEC from continuing to fight K-C-S in meetings of p754.”


### Table Based Methods

I included a section on table-based approximation of sine and cosine because for the earliest days of 8-bit machines I always saw people squeeze in 256- or 512-entry sine and cosine tables (back when you had 32KB of memory, you start to care about every byte). This became a non-issue when memories started to expand, but SPU, GPU and embedded processors brought space concerns back to the forefront again. If you analyze the maximal error of an interpolated sin table you can show that a 33-entry table is sufficient to reconstruct a 32-bit floating point sine and cosine at the same time. If only we’d known back in the day.

### Polynomial Approximation

On the web there are a lot of presentations on “advanced” computer math that end up using Taylor series to generate polynomial approximations for famous math functions. You’ve seen them in your Calculus textbook, they’re the definitions for Exp, Tan, Sin that you leaned at school so clearly that must be how they are calculated on computers. Truncate the series, generate a remainder and voila, you’re golden. Wrong.

Reading through the Cephes library, the polynomials you encounter look similar to the polynomials you would generate using a Taylor series, but vastly more accurate. Why the difference, how do they make the magic happen? Tutorials on Function Approximation usually introduce the idea of using [Chebyshev or Pade polynomials](http://wil.byimplication.com/files/chebyshev.pdf) to approximate functions (yes, that paper steals my diagrams from [SH Lighting Gritty Details](https://basesandframes.wordpress.com/2016/05/11/spherical-harmonic-lighting-the-gritty-details/)) which get you closer to the values in Cephes but not quite. The secret sauce that is covered almost nowhere on the web was Minimax polynomials.

The fundamental transcendental functions are mostly written using the same pattern:

- Range Reduction
- Polynomial Approximation
- Reconstruction

Others, like `acosf()`

, are implemented from previous functions using trig identities, so getting accurate versions of short sections of a function is paramount. Once you learn how to use Mathematica or Maple to generate low order polynomials you can produce faster approximations of many functions used in graphics – and that was the goal of the GDC tutorial.

### Tutorial slides and paper from GDC

The big bundle of research was turned into a GDC all-day tutorial with about 5 hours of slides and an accompanying paper. The paper was extended a little and appears as a chapter in [DeLoura M, “Best of Game Programming Gems”, Charles River Media ISBN ](http://www.amazon.com/Best-Game-Programming-Gems-DeLoura/dp/1584505710)

[1584505710](http://www.amazon.com/Best-Game-Programming-Gems-DeLoura/dp/1584505710).

Researching the slides I uncovered an error in the PS2 firmware where an engineer had transcribed and truncated the coefficients for the ESIN and ECOS instruction polynomials introducing a demonstrable shift to the results. Not only can you fix this, but it’s also possible to write a short piece of SPU code that calculated lower accuracy result faster than the ESIN instruction. Not everyday you can beat a hardware instruction with code.

### Errata: BitLog Improved

Looking to update the presentation for it’s asecond showing at GDC, I added some extra sections as an afterthought. One section dealt with looking into whether the power function in specular reflection BRDFs could be separated into several simple powers – it turned out the worked example in the paper was the *only* value that worked as advertised as it lay in a global error minimum. The second addition was a quick hacky logarithm function called *BitLog*.[ Charles Bloom made a post looking into it](http://cbloomrants.blogspot.com/2009/06/06-21-09-fast-exp-log.html), eviscerating my write-up, tracking down the original author Jack Crenshaw and tearing him a new one. He then wrote up an improved version. Yup, couldn’t have been owned more thoroughly.

### Footnote: Printing and reading floating point numbers

The subject of printing and parsing floating point values has a surprisingly convoluted history and is far from a solved problem even today. The seminal paper * “What Computer Scientist Should Know About Floating-Point Arithmetic”* does cover that printing 9 significant digits of a FP number is sufficient to reconstruct the exact binary mantissa of a single-precision float (15 for double-precision), it’s more difficult to prove what is the shortest expression that can correctly reconstruct a float from it’s ASCII value.

The most used algorithm for printing values is * Grisu3* which is fast but bails on a small number of values and has to drop back to the slower, more complete

*algorithm. In 2010 Florian Loitsch presented a paper at the PLDI conference titled*

[Dragon4](http://www.cs.indiana.edu/~dyb/pubs/FP-Printing-PLDI96.pdf)*that proposed a faster method using integer-only internal representation to speed up the process, but it too bails on about 0.6% of all FP values. In 2016, a new algorithm called*

[“Printing Floating Point Numbers Quickly and Accurately With Integers”](http://florian.loitsch.com/publications/dtoa-pldi2010.pdf)*Errol*was proposed in the paper

*that is faster than*

[“Printing Floating Point Numbers: A Faster, Always Correct Method”](http://cseweb.ucsd.edu/~lerner/papers/fp-printing-popl16.pdf)*Dragon4*, only 2.5x slower than

*Grisu3*but has the advantage of being complete.

[Reading FP numbers](http://krashan.ppa.pl/articles/stringtofloat/) is another problem that to do it correctly [requires use of several of the IEEE754 rounding modes](http://www.exploringbinary.com/decimal-to-floating-point-needs-arbitrary-precision/). It’s use of *round-to-half-even* is one of the strongest arguments for correctly supporting the rounding modes in any language. You can test the accuracy of your `scanf`

and `printf`

implementations using [code from Stephen Moshier](http://www.moshier.net/ieetst.zip).


[…] goal was to update the GDC 2002 talk on “Faster Math Functions” as the state of the art in numerical computing has moved on since then. The projects […]