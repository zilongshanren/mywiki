---
title: 'Calculating the mean and variance with one pass :: nklein software'
url: http://nklein.com/2011/02/calculating-the-mean-and-variance-with-one-pass/
author: Pat
published: '2011-02-15'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

A friend showed me this about 15 years ago. I use it every time I need to calculate the variance of some data set. I always forget the exact details and have to derive it again. But, it’s easy enough to derive that it’s never a problem.

I had to derive it again on Friday and thought, I should make sure more people get this tool into their utility belts

.

First, a quick refresher on what we’re talking about here. The mean of a data set

is defined to be

. The variance

is defined to be

.


A naÃ¯ve approach to calculating the variance then goes something like this:

(flet ((square (x) (* x x)))

(let* ((n (length data))

(sum (reduce #'+ data :initial-value 0))

(mu (/ sum n))

(vv (reduce #'(lambda (accum xi)

(+ accum (square (- xi mu))))

data :initial-value 0)))

(values mu (/ vv n)))))

This code runs through the data list once to count the items, once to calculate the mean, and once to calculate the variance. It is easy to see how we could count the items at the same time we are summing them. It is not as obvious how we can calculate the sum of squared terms involving the mean until we’ve calculated the mean.

If we expand the squared term and pull the constant outside of the summations it ends up in, we find that:



When we recognize that and

, we get:



This leads to the following code:

(flet ((square (x) (* x x)))

(destructuring-bind (n xs x2s)

(reduce #'(lambda (accum xi)

(list (1+ (first accum))

(+ (second accum) xi)

(+ (third accum) (square xi))))

data :initial-value '(0 0 0))

(let ((mu (/ xs n)))

(values mu (- (/ x2s n) (square mu)))))))

The code is not as simple, but you gain a great deal of flexibility. You can easily convert the above concept to continuously track the mean and variance as you iterate through an input stream. You do not have to keep data around to iterate through later. You can deal with things one sample at a time.

The same concept extends to higher-order moments, too.

Happy counting.

**Edit:** As many have pointed out, this isn’t the most numerically stable way to do this calculation. For my part, I was doing it with Lisp integers, so I’ve got all of the stability I could ever want. 🙂 But, yes…. if you are intending to use these numbers for big-time decision making, you probably want to look up a really stable algorithm.

See this page for a more accurate algorithm.

For certain data sets this may not be the best approach.

See [1] for some alternatives.

[1] http://en.wikipedia.org/wiki/Algorithms_for_calculating_variance

This looks like a standard single pass algorithm, which can have some numerical problems, arising from catastrophic cancellation in the final subtraction at the end. For example, this algorithm can sometimes result in negative variances. (The two-pass algorithm is also unstable for some data sets too.) You can fix things somewhat by using Kahan compensation.

Have you looked at the wikipedia page This is a one-pass Welford algorithm that is numerically stable. I have compared this algorithm to kahan-compensated two-pass computations for large data sets and the differences are very small. If you analyse the Welford algorithm, the computations tend to reduce round-off errors (by dividing subtractions by the data count, a number greater than one).

I recommend reading the whole page and the Chan and Terriberry references, which extend the one-pass method to higher moments, also in a numerically stable way.

I have a python implementation of the Chan-Terriberry-Welford system which works quite nicely over data sets with up to 1.2 million samples. I also have an implementation of the Welford one-pass algorithm for weighted data. In the weighted case, the variance computations do not automatically reduce round-off errors, as you can’t be sure that the divisor of the subtractions, (the running sum of weights) is greater than one , so you have to build it with Kahan compensation. I’m happy to supply the code to anyone who is interested.

oh darn I got the link wrong.

The wikipedia page I meant to refer to is: Algorithms_for_calculating_variance#On-line_algorithm

sorry about that!

AFAIR, second method is less numerically stable. It doesn’t mean it is useless, but it may behave poorly in some situations. 🙂