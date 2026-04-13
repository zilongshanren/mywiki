---
title: Finite differences of polynomials
url: https://divisbyzero.com/2018/02/13/finite-differences-of-polynomials/
author: Dave Richeson
published: '2018-02-13'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

It is interesting watching my kids go through the school math curriculum. Since I’m a math professor, one would think that I would know all of the school-aged math. While that is mostly true, sometimes the teachers and textbooks use unfamiliar terminology for familiar mathematical ideas. (“Oh, ____ is just ___,” I’ve said multiple times.)

My son is now in Algebra 2, and for the first time, he showed me something that I’ve never seen before—the relationship between polynomials and finite differences.

Take any polynomial, such as and any arithmetic sequence, such as 0, 2, 4, 6,… Plug these values into the polynomial. Take the neighboring pairwise differences. So, for instance,

Then take the neighboring pairwise differences of those values, and so on. It turns out that the

*n*th level will consist entirely of the same nonzero value if, and only if, the polynomial has degree *n*. Wow! That’s so cool!

Here’s my worked-out degree-3 example. Notice that after three levels, we yield the constant value 336:

![IMG_0148.JPG](../../assets/f7983ce9ee2ac5b9.jpg)


My son’s textbook (*Algebra 2*, by Larson, Boswell, Kanold, and Stiff) shared this fact but provided no explanation for why it is true (which, as a mathematician, I find very disappointing). So, I had to work it out myself.

![IMG_0147.JPG](../../assets/3f4be70f4f408662.jpg)


It turns out that **more** is true—if the polynomial has degree *n *with leading coefficient *c, *and *a *is the difference between terms in the arithmetic sequence, then the final value is In particular, if

*a*=1 and *c*=1, then the pairwise difference process will terminate with *n*!. Notice that in my example, the final value is

Why is this true?

Here’s a proof by induction on the degree of the polynomial. As the base case, consider a degree-1 polynomial: *p*(*x*)=*cx*+*b*. Then,

so the base case holds.

Now, assume that the result is true for any polynomial of degree *n*-1, for some *n*≥2. We will prove that it is true for a polynomial of degree *n.* Let where c≠0 and “l.o.t.” means “lower order terms.” We see that


Let us call this polynomial *q*(x).

Notice that because the leading coefficient *acn** *is nonzero, *q*(*x*) has degree *n*-1. By our inductive hypothesis, after *n*-1 pairwise differences, the polynomial *q*(*x*) will yield a constant value Thus, for

*p, *the process terminates after *n *steps with the constant value This proves the theorem.


After playing around with this, I googled it, and—no surprise—the mathematics of finite differences has a long history. Also, it is not difficult to see the resemblance of these calculations to the calculation of the derivative (using the definition of the derivative).

This gives a convenient way to extrapolate a sequence. Just calculate the differences until you get a constant (possibly because you’ve reduced the number of terms to 1) and then work your way back up assuming that that row continues to be constant. If your terms actually do come from a polynomial then this method can continue the sequence despite never actually calculating the coefficients of the polynomial.

When I first came to Messiah College in 1973, all Computer Science majors had to take Numerical Analysis. At the time I focused on Newton: Newton’s forward difference formula, Newton’s backward difference formula, Newton’s central difference formula. Later when I wanted to work more history into the curriculum, I had students learn about Babbage’s Difference Engine. Sadly, the course Numerical Analysis has fallen by the wayside. I regret most the chapter on propagation of errors falling by the wayside. Finite differences can help to detect the propagation of one kind of error. A ghost of that chapter shows up in machine architecture when discussing single- versus double-precision floating point numbers. Otherwise, nothing, sadly.