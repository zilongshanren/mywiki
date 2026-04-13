---
title: Frustum planes from the projection matrix
url: https://fgiesen.wordpress.com/2012/08/31/frustum-planes-from-the-projection-matrix/
published: '2012-08-31'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Frustum planes from the projection matrix

Another quick one. Now this is another old trick, but it’s easy to derive and still not as well-known as it deserves to be, so here goes.

All modern graphics APIs ultimately expect vertex coordinates to end up in one common coordinate system where clipping is done – clip space. That’s the space that vertices passed to the rasterizer are expected in – and hence, the space that Vertex Shaders (or Geometry Shaders, or Domain/Tessellation Evaluation Shaders) transform to. These shaders can do what they want, but the usual setup matches the original fixed-function pipeline and splits vertex transformations into at least two steps: The projection transform and the model-view transform, both of which can be represented as homogeneous 4×4 matrices.

The projection transform is the part that transforms vertices from camera view space to clip space. A view-space input vertex position v is transformed with the projection matrix P and gives us the position of the vertex in clip space:

Here, I’ve split P up into its four row vectors p1T, …, p4T. Now, in clip space, the view frustum has a really simple form, but there’s two slightly different formulations in use. GL uses the symmetric form:




whereas D3D replaces the last row with . Either way, we get 6 distinct inequalities, each of which corresponds to exactly one clip plane:

is the left clip plane,

is the right clip plane, and so forth. Now from the equation above we know that

and

and hence





Or in words, v lies in the non-negative half-space defined by the plane p4T+p1T – we have a view-space plane equation for the left frustum plane! For the right plane, we similarly get

and in general, for the GL-style frustum we find that the six frustum planes in view space are exactly the six planes p4T±piT for i=1, 2, 3 – all you have to do to get the plane equations is to add (or subtract) the right rows of the projection matrix! For a D3D-style frustum, the near plane is different, but it takes the even simpler form

, so it’s simply defined by the third row of the projection matrix.


Deriving frustum planes from your projection matrix in this way has the advantage that it’s nice and general – it works with any projection matrix, and is guaranteed to agree with the clipping / culling done by the GPU, as long as the planes are in fact derived from the projection matrix used for rendering.

And if you need the frustum planes in some other space, say in model space: not too worry! We didn’t use any special properties of P – the derivation works for *any* 4×4 matrix. The planes obtained this way are in whatever space the input matrix transforms to clip space – in the case of P, view space, but it can be anything. To give an example, if you have a model-view matrix M, then PM is the combined matrix that takes us from model-space to clip-space, and extracting the planes from PM instead of P will result in model-space clip planes.

Nice post! Small typo in the equation for the right clip plane, the right-hand side should be (p4-p1)v.

Indeed. Thanks!

Hmmm, that’s kinda like this: http://crazyjoke.free.fr/doc/3D/plane%20extraction.pdf

There was a great paper by Gil Gribb and Klaus Hartmann from 2001 which also detailed this but it doesn’t seem to be available anymore.

The fast extraction paper is available here: http://www8.cs.umu.se/kurser/5DV051/HT12/lab/plane_extraction.pdf

It’s not so obvious (at least it wasn’t for me) how equation

(p4 – p1)v = 0 (and 5 others equations)

is turning into a plane equation. I would add some notes for clarification:

Let (p4 – p1) = K.

K is four dimensional vector:

K = (A, B, C, D)

and

v is any vector in homogeneous coordinates:

v = (x, y, z, 1)

hence

(p4 – p1).v = 0 K.v = 0 (A, B, C, D).(x, y, z, 1) = 0 Ax + By + Cz + D = 0

(where “.” means dot product)

The reason why that was not so obvious to me is that you haven’t mentioned that “w” is

always equal to 1 in homogeneous coordinates.

Anyway, great article! I applied this technique to my little engine. Thank you very much for learning something new :)

Projective geometry / homogeneous coordinates are a fair bit deeper than “just add a 1”. :)

The comments section is not the right place to talk about this (I need to write this one up properly), but each (hyper-)plane in a projective space can be identified uniquely (up to scale) with a linear functional (covector) that is zero on that plane (and only there). This is analogous to how points can be written as vectors, which is again only unique up to scale: (x,y,z,1) and (2x,2y,2z,2) represent the same point. In linear algebra, vectors and covectors are dual; in projective geometry, points and planes are dual; and it turns out that these concept map into each other when writing projective spaces as vector spaces, i.e. points turn into vectors (up to scale) and planes turn into covectors (up to scale). You could also equivalently map points to covectors and planes to vectors, but customarily the former alternative is preferred.

The beauty of all of this is that most algebraic concepts in such spaces have a geometric interpretation, and vice versa. It’s quite powerful.

I’ve heard about dualities in projective geometry (namely about point-line duality

in hyperbolic geometry in lectures “Universal Hyperbolic Geometry” by Prof. Norman J. Wildberger

http://www.youtube.com/course?list=EC6ACFCC19EA82CA71 ). It is very interesting topic, indeed.

Lately I’m very intrigued about covectors (in context of normal vectors). What they really are?

What’s the difference between them and ordinary vectors? How to recognize that particular tuple of numbers is a covector and not a vector? Why they transform differently?

Do you know any good resource (possibly not too bloated with pure mathematical formalism) where can I read more about covectors? (And find answers to my questions).

I just noticed your article on this today. Here’s another version, and it has code at the end, which readers may find of interest: http://gamedevs.org/uploads/fast-extraction-viewing-frustum-planes-from-world-view-projection-matrix.pdf

Oh, and duh, I see someone else found it, too, in an earlier comment here, at a different URL, http://www8.cs.umu.se/kurser/5DV051/HT12/lab/plane_extraction.pdf – well, it’s nice to have two locations, in case one goes away.