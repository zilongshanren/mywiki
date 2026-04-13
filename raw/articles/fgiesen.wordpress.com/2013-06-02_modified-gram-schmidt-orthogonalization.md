---
title: Modified Gram-Schmidt orthogonalization
url: https://fgiesen.wordpress.com/2013/06/02/modified-gram-schmidt-orthogonalization/
published: '2013-06-02'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Modified Gram-Schmidt orthogonalization

Sometimes, you need to turn a linearly independent set of vectors into an orthonormal basis – or, equivalently, take a matrix that is “close” to orthogonal (for example, an orthogonal matrix that has been updated multiple times and might have started to drift due to round-off error) and make it properly orthogonal again.

The standard way to solve this problem is called [Gram-Schmidt orthogonalization](http://en.wikipedia.org/wiki/Gram%E2%80%93Schmidt_process). The idea is pretty simple. Say we have a list of (linearly independent) input vectors **v**1, …, **v**n. For the first vector in our output orthogonal basis, we just normalize the first input vector:

For the second vector **u**2 to be orthogonal to the first, we need to remove the component of **v**2 parallel to **u**1, which is a simple [projection](https://fgiesen.wordpress.com/2012/06/15/linear-algebra-toolbox-2/):

We now have two orthonormal vectors; for the third vector, we now need to remove the components that are parallel to either of them:

and so forth. You get the idea. This is the “classical” Gram-Schmidt process, or “CGS”. It’s simple and easy to derive, and works just fine in exact arithmetic. However, when performed using floating-point arithmetic, it is numerically unstable – badly so. Let me give an example: consider the matrix

where ε is any value small enough so that (1 + ε2) rounds to 1 in the given floating-point type. I’m using single-precision IEEE floating point and ε=10-4 for this example. Let’s run this through the classic Gram-Schmidt process:

static void classic_gram_schmidt(Mat33f &out, const Mat33f &in) { out.col[0] = normalize(in.col[0]); out.col[1] = normalize(in.col[1] - dot(in.col[1], out.col[0])*out.col[0]); out.col[2] = normalize(in.col[2] - dot(in.col[2], out.col[0])*out.col[0] - dot(in.col[2], out.col[1])*out.col[1]); }

which produces this result (rounded to 4 decimal digits):

Ouch. The first column not being “perfectly” normalized is expected – after all, we explicitly chose ε so that (1 + ε2) rounded to 1 – but the third column is not at all orthogonal to the second column; in fact, there’s a perfect 45 degree angle between the two. For an orthogonalization algorithm, that’s a pretty serious failure.

It turns out that there’s a really simple fix though: “modified” Gram-Schmidt. Instead of computing all the dot products from the original vectors, perform the projections one by one, using the result of the previous projection as the input to the next. In exact arithmetic, this is equivalent, but using floating-point arithmetic, this version:

static void modified_gram_schmidt(Mat33f &out, const Mat33f &in) { out.col[0] = normalize(in.col[0]); out.col[1] = normalize(in.col[1] - dot(in.col[1], out.col[0])*out.col[0]); out.col[2] = in.col[2] - dot(in.col[2], out.col[0])*out.col[0]; // note the second dot product is computed from the partial // result out.col[2], not the input vector in.col[2]! out.col[2] -= dot(out.col[2], out.col[1])*out.col[1]; out.col[2] = normalize(out.col[2]); }

produces (again rounded to 4 decimal digits):

Much better. Now, by itself, better results on a single matrix don’t tell us anything, but it turns out that the MGS algorithm comes with a bounded error guarantee: The orthogonalized matrix **Q** satisfies the inequality

where c1 and c2 are constants, u is the machine precision (the “epsilon” for the given floating point type), and κ = κ(**A**) is the [condition number](http://en.wikipedia.org/wiki/Condition_number) of the input matrix. And in fact, orthogonalizing a matrix using MGS is numerically equivalent to performing a [Householder QR decomposition](http://en.wikipedia.org/wiki/QR_decomposition) (a known stable algorithm) on the matrix A augmented with a few extra zero rows at the top – which also means that, in addition to the above error bound on the orthogonality of Q, MGS is also backwards stable with a nice error bound. (Both claims are proven [here](http://epubs.siam.org/doi/abs/10.1137/0613015?journalCode=sjmael)).

Long story short: this is a nice example of a numerical algorithm where two approaches identical in exact arithmetic yield dramatically different results when computed using floating-point. And it comes with an action item: if you have code that orthogonalizes a matrix (or orthonormalizes a tuple of basis vectors) using a Gram-Schmidt-like method, you should check whether it corresponds to the classical or modified GS algorithm. The modified algorithm has roughly the same cost (albeit with a different dependency structure that is slightly less amenable to vectorization) and is numerically much superior. Even for something as small as 3×3 matrices, as the example above shows. And if you want to play around with it, feel free to check out the [code](https://gist.github.com/rygorous/5695154) I used for the numerical experiments.

**UPDATE**: And before I get angry comments: in 3D, the cheapest way to compute the third basis vector is to not look at the third source vector at all, and instead simply use the cross product of the first two (assuming they’re normalized). This is cheaper, stable, and guarantees that the result will be a right-handed orthonormal basis. It does not, however, generalize to higher dimensions, so knowing about MGS is still useful.