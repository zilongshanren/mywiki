---
title: 'Pairing Functions: Cantor & Szudzik'
url: https://www.vertexfragment.com/ramblings/cantor-szudzik-pairing-functions/
author: Steven Sell
published: '2019-05-14'
source_blog: Vertex Fragment
source_site: https://www.vertexfragment.com/
category: graphics
fetched: '2026-04-13'
---

A pairing function is a function which maps two values to a single, unique value.

$$pair(x, y) = z$$

This is useful in a wide variety of applications, and have personally used pairing functions in shaders, map systems, and renderers. Essentially any time you want to compose a unique identifier from a pair of values. In this ramble we will cover two different pairing functions: Cantor and Szudzik.

Try them out in the demo below:

szudzik(, ) = 0

$$index = {(x + y)(x + y + 1) \over 2} + y$$

This can be easily implemented in any language. An example in JavaScript:

|
|

How Cantor pairing works is that you can imagine traversing a 2D field, where each real number point is given a value based on the order it which it was visited. For the Cantor function, this graph is traversed in a diagonal function is illustrated in the graphic below.

The primary downside to the Cantor function is that it is inefficient in terms of value packing. In a perfectly efficient function we would expect the value of `pair(9, 9)`

to be `99`

. This means that all one hundred possible variations of `([0-9], [0-9])`

would be covered (keeping in mind our values are 0-indexed).

However, `cantor(9, 9) = 200`

. So we use 200 pair values for the first 100 combinations, an efficiency of 50%.

We quickly start to brush up against the limits of 32-bit signed integers with input values that really aren’t that large. For example, `cantor(33000, 33000) = 2,178,066,000`

which would result in an overflow.

Trying to bump up your data type to an unsigned 32-bit integer doesn’t buy you too much more space: `cantor(46500, 46500) = 4,324,593,000`

, another overflow.

Like Cantor, the Szudzik function can be easily implemented anywhere. Another JavaScript example:

|
|

Szudzik can also be visualized as traversing a 2D field, but it covers it in a box-like pattern. This graphics demonstrates the path that Szudzik takes over the field:

The primary benefit of the Szudzik function is that it has more efficient value packing. Comparing against Cantor we see:

```
cantor(9, 9) = 200
szudzik(9, 9) = 99
```


Yes, the Szudzik function has 100% packing efficiency. As such, we can calculate the max input pair to Szudzik to be the square root of the maximum integer value. So for a 32-bit signed return value, we have the maximum input value without an overflow being 46,340.

For a 32-bit unsigned return value the maximum input value for Szudzik is 65,535.

Neither Cantor nor Szudzik pairing functions work natively with negative input values.

However, a simple transformation can be applied so that negative input can be used. It should be noted though that all returned pair values are still positive, as such the packing efficiency for both functions will degrade.

$$b = \left{\begin{array}{ll}
-2y - 1 & : y < 0\

2y & : y \ge 0
\end{array}
\right.$$

In JavaScript:

|
|

In JavaScript:

|
|

Additional space can be saved, giving improved packing efficiency, by transferring half to the negative axis.

$$index = \left{\begin{array}{ll}
c & : (a < 0 \cap b < 0) \cup (a \ge 0 \cap b \ge 0)\

-c - 1 & : (a < 0 \cap b \ge 0) \cup (a \ge 0 \cap b < 0)
\end{array}
\right.$$

In JavaScript:

|
|

The performance between Cantor and Szudzik is virtually identical, with Szudzik having a slight advantage.

| Implementation | Ops/sec | % |
|---|---|---|
| Szudzik | 894,767,289 | 100.00 |
| Cantor | 888,441,837 | 99.29 |
| Szudzik Signed | 885,070,104 | 98.92 |
| Cantor Signed | 884,386,294 | 98.84 |
| Szudzik Signed (Alt) | 863,042,799 | 96.45 |

The full results of the performance comparison [can be found on jsperf](https://jsperf.com/cantor-szudzik-pair-comparison/3).

It should be noted that this article was adapted from an [earlier jsfiddle](https://jsfiddle.net/ssell/5smy3qg6/) of mine.

That fiddle makes note of the following references:

- Szudzik, Matthew.
*An Elegant Pairing Function*.[http://szudzik.com/ElegantPairing.pdf](http://szudzik.com/ElegantPairing.pdf). *Pairing Functions*.[https://en.wikipedia.org/wiki/Pairing_function](https://en.wikipedia.org/wiki/Pairing_function)