---
title: Linear Algebra Toolbox 3
url: https://fgiesen.wordpress.com/2012/06/25/linear-algebra-toolbox-3/
published: '2012-06-25'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Linear Algebra Toolbox 3

The last part had a bit of theory and terminology groundwork. This part will be focusing on the computational side instead.

### Slicing up matrices

In the previous parts, I’ve been careful to distinguish between vectors and their representation as coefficients (which depends on a choice of basis), and similarly I’ve tried to keep the distinction between linear transforms and matrices clear. This time, it’s all about matrices and their properties, so I’ll be a bit sloppier in this regard. Unless otherwise noted, assume we’re dealing exclusively with vector spaces (for various n) using their canonical bases. In this setting (all bases fixed in advance), we can uniquely identify linear transforms with their matrices, and that’s what I’ll do. However, I’ll be switching between scalars, vectors and matrices a lot, so to avoid confusion I’ll be a bit more careful about typography: lowercase letters like

denote scalars, lowercase bold-face letters

denote column vectors, row vectors (when treated as vectors) will be written as the transpose of column vectors

, and matrices use upper-case bold-face letters like

. A vector is made of constituent scalars

, and so is a matrix (with two sets of indices)

. Note all these are overlapping to a degree: we can write a 1×1 matrix as a scalar, vector or matrix, and similarly a nx1 (or 1xn) matrix can be written either as vector or matrix. In this context, matrices are the most general kind of object we’re be dealing with, so unless something

*needs* to be a vector or scalar, I’ll write it as a matrix.

All that said, let’s take another look at matrices. As I explained before (in [part 1](https://fgiesen.wordpress.com/2012/06/03/linear-algebra-toolbox-1/)), the columns of a matrix contain the images of the basis vectors. Let’s give those vectors names:

.


This is just taking the n column vectors making up A and giving them distinct names. This is useful when you look at a matrix product:

.


You can prove this algebraically by expanding out the matrix product and doing a bunch of index manipulation, but I’d advise against it: don’t expand out into scalars unless you have exhausted every other avenue of attack – it’s tedious and extremely error-prone. You can also prove this by exploiting the correspondence between linear transforms and matrices. This is elegant, very short and makes for a nice exercise, so I won’t spoil it. But there’s another way to prove it algebraically, without expanding it out into scalars, that’s more in line with the spirit of this series: getting comfortable with manipulating matrix expressions.

The key is writing the as the result of a matrix expression. Now, as explained before, the i-th column of a matrix contains the image of the i-th basis vector. Since we’re using the canonical basis, our basis vectors are simply




…


and it’s easy to verify that (this one you’ll have to expand out if you want to prove it purely algebraically, but since the product is just with ones and zeros, it’s really easy to check). So multiplying

from the right by one of the

gives us the i-th column of a, and conversely, if we have all n column vectors, we can piece together the full matrix by gluing them together in the right order. So let’s look at our matrix product again: we wan’t the i-th column of the matrix product

, so we look at


exactly as claimed. As always, there’s a corresponding construction using row vectors. Using the *dual basis* of linear functionals (note no transpose this time!)



…


we can disassemble a matrix into its rows:

and since , we can write matrix products in terms of what happens to the row vectors too (though this time, we’re expanding in terms of the row vectors of the first not second factor):


.


### Gluing it back together

Above, the trick was to write the “slicing” step as a matrix product with one of the basis vectors – and so forth. We’ll soon need to deal with the gluing step too, so let’s work out how to write that as a matrix expression too so we can manipulate it easily.


Let’s say we have a m×2 matrix A that we’ve split into two column vectors ,

. What’s the matrix expression that puts A back together from those columns again? So far we’ve expressed that as a concatenation; but to be able to manipulate it nicely, we want it to be a linear expression (same as everything else we’re dealing with). So it’s gotta be a sum: one term for

and one for

. Well, the sum is supposed to be

, which is a m×2 matrix, so the summands all have to be m×2 matrices too. The

are column vectors (m×1 matrices), so for the result to be a m×2 matrix, we have to multiply from the right with a 1×2 matrix. From there, it’s fairly easy to see that the expression that re-assembles

from its column vectors is simply:


.


Note that the terms have the form column vector × row vector – this is the general form of the vector outer product (or dyadic product) that we first saw in the

[previous part](https://fgiesen.wordpress.com/2012/06/15/linear-algebra-toolbox-2/). If A has more than two columns, this generalizes in the obvious way.

So what happens if we disassemble a matrix only to re-assemble it again? Really, this should be a complete no-op. Let’s check:

For the last step, note that the summands are matrices that are all-zero, except for a single one in row i, column i. Adding all these together produces a matrix that’s zero everywhere except on the diagonal, where it’s all ones – in short, the n×n identity matrix. So yes, disassembling and re-assembling a matrix is indeed a no-op. Who would’ve guessed.


Again, the same thing can be done for the rows; instead of multiplying by from the right, you end up multiplying by

from the left, but same difference. So that covers slicing a matrix into its constituent vectors (of either the row or column kind) and putting it back together. Things get a bit more interesting (and a lot more useful) when we allow more general submatrices.


### Block matrices

In our first example above, we sliced A into n separate column vectors. But what if we just slice it into just two parts, a left “half” and a right “half” (the sizes need not be the same), both of which are general matrices? Let’s try:

For the same reasons as with column vectors, multiplying a second matrix B from the left just ends up acting on the halves separately:

and the same also works with right multiplication on vertically stacked matrices. Easy, but not very interesting yet – we’re effectively just keeping some columns (rows) glued together through the whole process. It gets more interesting when you start slicing in the horizontal and vertical directions simultaneously, though:

Note that for the stuff I’m describing here to work, the “cuts” between blocks need to be uniform across the whole matrix – that is, all matrices in a block column need to have the same width, and all matrices in a block row need to have the same height. So in our case, let’s say is a p×q matrix. Then

must be a p×(n-q) matrix (the heights have to agree and

is n columns wide),

is (m-p)×q, and

is (m-p)×(n-q).


Adding block matrices is totally straightforward – it’s all element-wise anyway. Multiplying block matrices is more interesting. For regular matrix multiplication , we require that B has as many columns as A has rows; for block matrix multiplication, we’ll also require that B has as many block columns as A has block rows, and that all of the individual block sizes are compatible as well. Given all that, how does block matrix multiplication work? Originally I meant to give a proof here, but frankly it’s all notation and not very enlightening, so let’s skip straight to the punchline:


Block matrix multiplication works just like regular matrix multiplication: you compute the “dot product” between rows of B and columns of A. This is all independent of the sizes too – I show it here with a matrix of 1×2 blocks and a matrix of 2×2 blocks because that’s the smallest interesting example, but you can have arbitrarily many blocks involved.

So what does this mean? Two things: First, most big matrices that occur in practice have a natural block structure, and the above property means that for most matrix operations, we can treat the blocks as if they were scalars in a much smaller matrix. Even if you don’t deal with big matrices, working at block granularity is often a lot more convenient. Second, it means that big matrix products can be naturally expressed in terms of several smaller ones. Even when dealing with big matrices, you can just chop them up into smaller blocks that nicely fit in your cache, or your main memory if the matrices are truly huge.

All that said, the main advantage of block matrices as I see it are just that they add a nice, in-between level of granularity: dealing with the individual scalars making up a matrix is unwieldy and error-prone, but sometimes (particularly when you’re interested in some structure within the matrix) operating on the whole matrix at once is too coarse-grained.

### Example: affine transforms in homogeneous coordinates

To show what I mean, let’s end with a familiar example, at least for graphics/game programmers: matrices representing affine transforms when using homogeneous coordinates. The matrices in question look like this:

where is an arbitrary square matrix and

is a translation vector (note the 0 in the bottom row is printed in bold and means a 0 row vector, not a scalar 0!). So how does the product of two such matrices look? Well, this has obvious block structure, so we can use a block matrix product without breaking A up any further:


Note this works in any dimension – I just required that A was square, I never specified what the actual size was. This is a fairly simple example, but it’s a common case and handy to know.

And that should be enough for this post. Next time, I plan to first review some basic identities (and their block matrix analogues) then start talking about matrix decompositions. Until then!