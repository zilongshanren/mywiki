---
title: Basis Projection
url: http://hacksoflife.blogspot.com/2010/11/basis-projection.html
author: Benjamin Supnik
published: '2010-11-29'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[previous post](http://hacksoflife.blogspot.com/2010/11/change-of-basis-revisited.html)I described a transform matrix as a sort of kit of "premade parts" that each vertex's components call out. Thus a vertex of (1, 0.5, 0) means "use 1 measure of the X basis from the matrix, 0.5 measures of the Y basis, and skip the Z basis, we don't want any of that." You can almost see a matrix as a form of encoding or compression, where we decode using the "premade parts" that are basis vectors. (I must admit, this is not a very good form of compression, as we don't save any memory.)

So if our model's vertices are encoded (into "model space") and a model positioning matrix decodes our model into world space (so we can show our model in lots of places in the world), how do we encode that model? If we have one house in world space, how do we encode it into its own model space?

One way to do so would be "basis projection". We could take the dot product of each vector in our model* with each basis vector, and that ratio of correlation would tell us how much of the encoding vector we want. What would a matrix for this encoding look like?

`[x][Xx Xy Xz]`

[y][Yx Yy Yz]

[z][Zx Zy Zz]


where we are encoding into the vector X, Y, and Z, described in the world coordinates.So we have put our basis vectors for our model into the rows of the matrix to encode, while last time we put them into the columns to decode.

Wait - this isn't surprising. The encode and decode matrices are inverses and the inverse of an orthogonal matrix is its transpose.

Putting this together, we can say that our orthogonal matrix has the old basis in the new coordinate system in its columns at the same time as it has the new basis in the old coordinate system in its rows. We can view our matrix through either the lens of decoding (via columns - each column is a "premade part") or encoding (via rows - how closely do we fit that "premade part").

Why bring this up? The previous post was meant to serve two purposes:

- To justify some particularly sparse implementations of camera operations. (E.g. how did we get the code down to so few operations, why is this legal?)
- To try to illustrate the connection between the symbols and geometric meaning of matrices and vectors.

* As in the previous article, we can think of our model as a series of vectors from the origin to the vertices in our mesh.

## No comments:

## Post a Comment