---
title: Linear Algebra Toolbox 2
url: https://fgiesen.wordpress.com/2012/06/15/linear-algebra-toolbox-2/
published: '2012-06-15'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Linear Algebra Toolbox 2

In the [previous part](https://fgiesen.wordpress.com/2012/06/03/linear-algebra-toolbox-1/) I covered a bunch of basics. Now let’s continue with stuff that’s a bit more fun. Small disclaimer: In this series, I’ll be mostly talking about finite-dimensional, real vector spaces, and even more specifically for some n. So assume that’s the setting unless explicitly stated otherwise; I don’t want to bog the text down with too many technicalities.


### (Almost) every product can be written as a matrix product

In general, most of the functions we call “products” share some common properties: they’re examples of “bilinear maps”, that is vector-valued functions of two vector-valued arguments which are linear in both of them. The latter means that if you hold either of the two arguments constant, the function behaves like a linear function of the other argument. Now we know that any linear function can be written as a matrix product

for some matrix M, provided we’re willing to choose a basis.


Okay, now take one such product-like operation between vector spaces, let’s call it . What the above sentence means is that for any

, there is a corresponding matrix

such that

(and also a

such that

, but let’s ignore that for a minute). Furthermore, since a product is linear in

*both* arguments, itself (respectively

) is a linear function of a (respectively b) too.


This is all fairly abstract. Let’s give an example: the standard dot product. The dot product of two vectors a and b is the number . This should be well known. Now let’s say we want to find the matrix

for some a. First, we have to figure out the correct dimensions. For fixed a,

is a scalar-valued function of two vectors; so the matrix that represents “a-dot” maps a 3-vector to a scalar (1-vector); in other words, it’s a 1×3 matrix. In fact, as you can verify easily, the matrix representing “a-dot” is just “a” written as a row vector – or written as a matrix expression,

. For the full dot product expression, we thus get

=

(because the dot product is symmetric, we can swap the positions of the two arguments). This works for any dimension of the vectors involved, provided they match of course. More importantly, it works the other way round too – a 1-row matrix represents a scalar-valued linear function (more concisely called a “linear functional”), and in case of the finite-dimensional spaces we’re dealing with, all such functions can be written as a dot product with a fixed vector.


The same technique works for any given bilinear map. Especially if you already know a form that works on coordinate vectors, in which case you can instantly write down the matrix (same as in part 1, just check what happens to your basis vectors). To give a second example, take the cross product in three dimensions. The corresponding matrix looks like this:


.


The is standard notation for this construction. Note that in this case, because the cross product is vector-valued, we have a full 3×3 matrix – and not just any matrix: it’s a skew-symmetric matrix, i.e.

. I might come back to those later.


So what we have now is a systematic way to write any “product-like” function of a and b as a matrix product (with a matrix depending on one of the two arguments). This might seem like a needless complication, but there’s a purpose to it: being able to write everything in a common notation (namely, as a matrix expression) has two advantages: first, it allows us to manipulate fairly complex expressions using uniform rules (namely, the rules for matrix multiplication), and second, it allows us to go the other way – take a complicated-looked matrix expression and break it down into components that have obvious geometric meaning. And that turns out to be a fairly powerful tool.

### Projections and reflections

Let’s take a simple example: assume you have a unit vector , and a second, arbitrary vector

. Then, as you hopefully know, the dot product

is a scalar representing the length of the projection of x onto v. Take that scalar and multiply it by v again, and you get a vector that represents the component of x that is parallel to v:


.


See what happened there? Since it’s all just matrix multiplication, which is associative (we can place parentheses however we want), we can instantly get the matrix that represents parallel projection onto v. Similarly, we can get the matrix for the corresponding orthogonal component:


.


All it takes is the standard algebra trick of multiplying by 1 (or in this case, an identity matrix); after that, we just use linearity of matrix multiplication. You’re probably more used to exploiting it when working with vectors (stuff like ), but it works in both directions and with arbitrary matrices:

and

– matrix multiplication is another bilinear map.


Anyway, with the two examples above, we get a third one for free: We’ve just separated into two components,

. If we keep the orthogonal part but flip the parallel component, we get a reflection about the plane through the origin with normal

. This is just

, which is again linear in x, and we can get the matrix

for the whole by subtracting the two other matrices:


.


None of this is particularly fancy (and most of it you should know already), so why am I going through this? Two reasons. First off, it’s worth knowing, since all three special types of matrices tend to show up in a lot of different places. And second, they give good examples for transforms that are constructed by adding something to (or subtracting from) the identity map; these tend to show up in all kinds of places. In the general case, it’s hard to mentally visualize what the sum (or difference) of two transforms does, but orthogonal complements and reflections come with a nice geometric interpretation.

I’ll end this part here. See you next time!

“we get a reflection about the plane through the origin with normal v”

I think you made a mistake: you reflect with normal (Ov)x.

With normal v, you should write x(parallel) – x(orthogonal).

Ops, no I’m wrong, sorry.

I confused the symmetrical vector with the reflected one. Sorry…

I would like to see a paper on Absorbing Markov Chains and one on Linear Programming they both require Matrix Inversion.