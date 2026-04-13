---
title: Finish your derivations, please
url: https://fgiesen.wordpress.com/2010/10/21/finish-your-derivations-please/
published: '2010-10-21'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Finish your derivations, please

Every time you ship a product with half-assed math in it, God kills a fluffy kitten by feeding it to an ill-tempered panda bear (don’t ask me why – I think it’s bizarre and oddly specific, but I have no say in the matter). There’s tons of ways to make your math way more complicated (and expensive) than it needs to be, but most of the time it’s the same few common mistakes repeated ad nauseam. Here’s a small checklist of things to look out for that will make your life easier and your code better:

**Symmetries**. If your problem has some obvious symmetry, you can usually exploit it in the solution. If it has radial symmetry around some point, move that point to the origin. If there’s some coordinate system where the constraints (or the problem statement) get a lot simpler, try solving the problem in that coordinate system. This isn’t guaranteed to win you anything, but if you haven’t checked, you should – if symmetry leads to a solution, the solutions are usually very nice, clean and efficient.**Geometry**. If your problem is geometrical, draw a picture first, even if you know how to solve it algebraically. Approaches that use the geometry of the problem can often make use of symmetries that aren’t obvious when you write it in equations. More importantly, in geometric derivations, most of the quantities you compute actually have geometrical meaning (points, distances, ratios of lengths, etc). Very useful when debugging to get a quick sanity check. In contrast, intermediate values in the middle of algebraic manipulations rarely have any meaning within the context of the problem – you have to treat the solver essentially as a black box.**Angles**. Avoid them. They’re rarely what you actually want, they tend to introduce a lot of trigonometric functions into the code, you suddenly need to worry about parametrization artifacts (e.g. dealing with wraparound), and code using angles is generally harder to read/understand/debug than equivalent code using vectors (and slower, too).**Absolute Angles**. Particularly, never never*ever*use angles relative to some arbitrary absolute coordinate system. They*will*wrap around to negative at some point, and suddenly something breaks somewhere and nobody knows why. And if you’re about to introduce some arbitrary coordinate system just to determine some angles, stop and think very hard if that’s really a good idea. (If, upon reflection, you’re still undecided,[this website](http://www.nooooooooooooooo.com/)has your answer).**Did I mention angles?**There’s one particular case of angle-mania that really pisses me off: Using inverse trigonometric functions immediately followed by sin / cos. atan2 / sin / cos: World’s most expensive 2D vector normalize. Using acos on the result of a dot product just to get the corresponding sin/tan? Time to brush up your[trigonometric identities](http://en.wikipedia.org/wiki/List_of_trigonometric_identities#Inverse_trigonometric_functions). A particularly bad offender can be found[here](http://wiki.gamedev.net/index.php/D3DBook:(Lighting)_Oren-Nayar)– the relevant section from the simplified shader is this:float alpha = max( acos( dot( v, n ) ), acos( dot( l, n ) ) ); float beta = min( acos( dot( v, n ) ), acos( dot( l, n ) ) ); C = sin(alpha) * tan(beta);

Ouch! If you use some trig identities and the fact that acos is monotonically decreasing over its domain, this reduces to:

float vdotn = dot(v, n); float ldotn = dot(l, n); C = sqrt((1.0 - vdotn*vdotn) * (1.0 - ldotn*ldotn)) / max(vdotn, ldotn);

..and suddenly there’s no need to use a lookup texture anymore (and by the way, this has way higher accuracy too). Come on, people! You don’t need to derive it by hand (although that’s not hard either), you don’t need to buy some formula collection, it’s all on Wikipedia – spend the two minutes and look it up!

**Elementary linear algebra**. If you build some matrix by concatenating several transforms and it’s a performance bottleneck, don’t get all SIMD on it, do the obvious thing first: do the matrix multiply symbolically and generate the result directly instead of doing the matrix multiplies every time. (But state clearly in comments which transforms you multiplied together in what order to get your result or suffer the righteous wrath of the next person to touch that code). Don’t invert matrices that you know are orthogonal, just use the transpose! Don’t use 4×4 matrices everywhere when all your transforms (except for the projection matrix) are affine. It’s not rocket science.**Unnecessary numerical differentiation**. Numerical differentiation is numerically unstable, and notoriously difficult to get robust. It’s also often completely unnecessary. If you’re dealing with analytically defined functions, compute the derivative directly – no robustness issues, and it’s usually faster too (…but remember the chain rule if you warp your parameter on the way in).

Short version: Don’t just stick with the first implementation that works (usually barely). Once you have a solution, at least spend 5 minutes looking over it and check if you missed any obvious simplifications. If you won’t do it by yourself, think of the kittens!

Amen! Particularly about avoiding trig.

Nice post!

> Don’t invert matrices that you know are orthogonal, just use the transpose!

I believe the basis vectors should have unit length too for inverse==transpose, so really the transpose should only be used if the matrices are orthonormal.

> World’s most expensive 2D vector normalize.

No, *this* is the World’s most expensive 2D vector normalize :)

void vec2dNormalize(vec2d& outNormal, const vec2d &inNormal)

{

while (1)

{

outNormal.x = frand(-1.0f, 1.0f);

outNormal.y = frand(-1.0f, 1.0f);

// yeah I said it. no epsilon thresholds

bUnitLen = (outNormal.x*outNormal.x + outNormal.y*outNormal.y) == 1.0f;

bParallel = (-outNormal.y*inNormal.x + outNormal.x*inNormal.y) == 0.0f;

if (bUnitLen && bParallel)

return;

}

}

Possibly so expensive it’ll never finish. Sadly, I’ve actually seen someone sort lists like this too. Randomly permuting the list, and then testing whether it’s sorted until they get a sorted list :(

“I believe the basis vectors should have unit length too for inverse==transpose, so really the transpose should only be used if the matrices are orthonormal.”

The terminology is a bit unfortunate there. Matrices are called orthogonal if and only if the corresponding basis vectors are orthonormal (the usual definition is that Q^T Q = Q Q^T I). There’s no special name for matrices with orthogonal but non-normalized basis vectors.

Finally someone who gets it. Orthonormal is orthogonal but orthogonal is not always orthonormal. And neither implies invertibility. Whole books have been written on the subject, and I’m a novice. So mathematicians are welcome to pile on.

If an orthogonal matrix has full column rank r, all of its r columns are orthogonal to each other, but all of its rows may not be orthogonal to each other. Nothing specific can be said about the magnitude of any row or column in such a matrix except that the magnitude of every column must be greater than zero, and the magnitude of at least r rows must be greater than zero. If an orthogonal matrix has full row rank r, all of its r rows are orthogonal to each other, but all of its columns may not be orthogonal to each other. Nothing specific can be said about the magnitude of any row or column in such a matrix except that the magnitude of every row must be greater than zero, and the magnitude of at least r columns must be greater than zero. If an orthogonal matrix has full row and column rank r, it is square, nonsingular, and invertible. Furthermore its columns are orthogonal to each other and its rows are orthogonal to each other. But the inverse of an invertible orthogonal matrix may not be equal to the transpose of that matrix. And nothing specific can be said about the magnitude of any row or column in such a matrix except that the magnitude of every row must be greater than zero, and the magnitude of every column must be greater than zero.

If an orthonormal matrix has full column rank r, all of its r columns are orthogonal to each other, but all of its rows may not be orthogonal to each other. Nothing specific can be said about the magnitude of any row or column in such a matrix except that the magnitude of every column is unity, and the magnitude of at least r rows must be greater than zero. If an orthonormal matrix has full row rank r, all of its r rows are orthogonal to each other, but all of its columns may not be orthogonal to each other. Nothing specific can be said about the magnitude of any row or column in such a matrix except that the magnitude of every row must be unity, and the magnitude of at least r columns must be greater than zero. If an orthonormal matrix has full row and column rank r, it is square, nonsingular, and invertible. Furthermore its columns are orthogonal to each other and its rows are orthogonal to each other. And the inverse of an invertible orthonormal matrix is equal to the transpose of that matrix. And the magnitude of each row and column in such a matrix is unity.

Note carefully what I said. No orthogonal or orthonormal matrix is invertible unless it has full row and column rank. However, simple pseudo inverses do exist for all orthogonal and orthonormal matrices. Thus if Q represents an orthonormal matrix, then Q^T Q = Q Q^T = I if and only if Q has full row and column rank. Suppose Q represents an orthonormal matrix with full column rank but not full row rank, then Q^T Q = I but Q Q^T does not. Why? Because Q Q^T is obviously singular and I is not. Likewise if Q represents an orthonormal matrix with full row rank but not full column rank, then Q Q^T = I but Q^T Q does not. Again why? Because Q^T Q is obviously singular and I is not. What are the pseudo inverses in these cases? And what are the pseudo inverses when Q is only orthogonal?

A system of vectors can be orthogonal or orthonormal. In particular, there are orthonormal bases (ONBs).

But in the matrix case, “orthonormal” matrices aren’t a thing (in common mathematical usage anyway). An orthogonal (complex generalization: unitary – replace transpose with Hermitian transpose) matrix is defined as a matrix A such the A^T A = I (the transpose is the inverse). This implies that both the rows and column vectors form orthonormal systems and the matrix has full rank (otherwise it couldn’t have an inverse).

Numerics checklist:

– Special cases are ugly but necessary in most numerical code. Be suspicious of too beautiful code that looks like a one-to-one translation from a paper or textbook. Most likely it is full of pitfalls.

– As a rule, prefer self-correcting iterative methods over direct methods. Even a venerable direct method like Gaussian elimination needs iterative refinement for numerical robustness in the face of ill-conditioned problems. This also applies to simple closed forms like the cubic formula. The chief virtue of self-correction is that it makes intermediate round-off error almost a non-issue. But you must still think carefully about your stopping condition (error vs residual conditioning, circle of uncertainty in calculating error and residual deltas, etc).

I hate to look unsmart, but I’m working on this:

Ouch! If you use some trig identities and the fact that acos is monotonically decreasing over its domain, this reduces to:

Think you could expand that a little?

Arc cosine is monotonically decreasing: see the diagram here (blue curve). Note how the curve strictly goes down as you go further to the right. This is what “monotonically decreasing” means, visually.

In formulas, this means that if x acos(y): x is further to the left, so its arc cosine value is higher, because the arc cosine is steadily decreasing as you go to the right!

Hence

`alpha = max( acos( dot( v, n ) ), acos( dot( l, n ) ) )`

is the same as`alpha = acos( min( dot( v, n ), dot( l, n ) )`

– max turns into min because smaller values of x imply larger values of acos(x). Similar for beta.Now, the only thing we do with alpha is compute its sine. By the Pythagorean theorem,

`sin(x)^2 + cos(x)^2 = 1`

. So`sin(alpha) ^ 2 + cos(alpha) ^ 2 = 1`

, which in turn means that`sin(alpha)^2 = 1 - cos(alpha)^2`

, so`sin(alpha) = +- sqrt(1 - cos(alpha)^2)`

. (Positive sign turns out to be correct in this case). So we never need to compute the acos for alpha in the first place: we already have cos_alpha, which is just`cos_alpha = min( dot( v, n ), dot( l, n ) )`

.`tan(beta)`

is similar:`tan(beta) = sin(beta) / cos(beta) = sqrt(1 - cos_beta^2) / cos_beta`

. So`C = sin_alpha * tan_beta`

=`sqrt(1 - cos_alpha^2) * sqrt(1 - cos_beta^2) / cos_beta`

=`sqrt((1 - cos_alpha^2) * (1 - cos_beta^2)) / cos_beta`

.Now note that the square root term contains the same expressions for both cos_alpha and cos_beta and just multiplies them together – so it doesn’t matter which of them is the min of the two dot products and which is the max; we calculate the same value for both dot products and multiply them together. Introducing some more names:

`vdotn = dot( v, n )`

`ldotn = dot( l, n )`

`cos_alpha = min( vdotn, ldotn )`

`cos_beta = max( vdotn, ldotn )`

so

C =

`sqrt((1 - cos_alpha^2) * (1 - cos_beta^2)) / cos_beta`

=`sqrt( ( 1 - vdotn^2 ) * ( 1 - vdotl^2 ) ) / max( vdotn, ldotn )`

.Thank you so much for taking the time to spell this out for me! I get it, yet at the same time I know it’s just convoluted enough that I wouldn’t arrive at the solution. After reading your blog and Emil Persson’s “Low Level Thinking” presentation at GDC’13, it made me look at some of the shader code we have here which is ripe for optimization.

The fact that this is a pet peeve of yours and his, means that you both see this as obviously important and fairly trivial to do.

My thinking is instead that the both of you had lots of practice optimizing code using trig identities and many other methods, that are not even a consideration when teaching programming.

Your combined works imply is that there is a strong need for practice optimization problems, at the algorithmic level and low level for professionals.

In the long term, University course work ought to involve lots of these sorts of optimizations, particularly involving dot products and trig identities.

I’ll keep plugging away at my code optimizations (I know I will get rid of that atan somehow), but thanks so much for showing me how a pro does it.