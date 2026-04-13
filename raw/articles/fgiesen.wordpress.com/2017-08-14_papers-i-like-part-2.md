---
title: Papers I like (part 2)
url: https://fgiesen.wordpress.com/2017/08/14/papers-i-like-part-2/
published: '2017-08-14'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Papers I like (part 2)

Continued from [part 1](https://fgiesen.wordpress.com/2017/08/12/papers-i-like-part-1/).

Once I was about a thousand words into describing background for GEMM, it became pretty clear that it made more sense to group the numerical math papers into one post, so here goes the (out-of-order) numerical linear algebra special issue.

### 11. Goto, van de Geijn-[“Anatomy of high-performance matrix multiplication”](http://www.cs.utexas.edu/~flame/pubs/GotoTOMS_revision.pdf) (2008; numerical Linear Algebra / HPC)

You might wonder: why do we care about matrix multiplication in particular so much? Who is it who’s doing these giant matrix multiplies? If you’re a customer of a linear algebra library, it’s not unlikely that you’re never calling GEMM (GEneral Matrix Multiply, the customary name for matrix multiply kernels, thanks to FORTRAN 77’s 6-character limit for function names) at all. So what gives?

Well, if you’re calling into a linear algebra library, odds are you want to solve a linear system of equations (which usually turns into a pivoted LU decomposition plus a solve step), a linear least-squares problem (depending on the problem and your accuracy requirements, this might turn either into a Cholesky decomposition or a QR decomposition, again followed by a solve step), or you want something fancier like the SVD (yet another matrix decomposition, and you probably still eventually want to solve a linear system – but you’re using the SVD because it’s noisy or ill-conditioned and you want to munge around with the singular values a bit).

What’s with all the focus on “decompositions”? Are numerical analysts secretly the world’s most pocket-protected goth band? No: a matrix decomposition (or factorization) expresses a more general matrix as the product of several special matrices that have some desirable structure. For example, the LU decomposition turns our general matrix into a product

where

is a

[unit lower triangular](https://en.wikipedia.org/wiki/Triangular_matrix) matrix and is upper triangular (note: I’ll be ignoring pivoting in this post for simplicity). The LU decomposition is the industrial-strength counterpart of the Gaussian Elimination process you might have learned in school, but with some side benefits: you can decompose the matrix once and then reuse the factorization multiple times if you’re solving the same system many times with different right-hand sides (this is common in applications), and it also happens to be really nice to have the whole process in a form that can be manipulated algebraically, which we’ll be using in a moment.


But why does this decomposition help? Well, suppose we have a toy system with 3 equations and 3 unknowns, which can be written as a matrix equation where

is a 3×3 matrix of coefficients and

and

are 3-element column vectors. If we have a LU decomposition for A, this turns into


How does this help? Well, we can’t solve the full thing yet, but we now have two fairly simply matrices. For now, let’s focus on the left matrix and treat as an unknown:


Well, this one’s easy: the first row just states that . The second row states that

, and we know everything but

, so we can rearrange this to

. With this, the final row

poses no problems either, yielding

. So

just falls out, given

we can compute

, and given both we can compute

. This is called “forward substitution”. Note that we’re just computing

here. However, we’re never forming the inverse of L explicitly! This is important.

*In numerical LA, when you see an inverse, that means you’re supposed to use the corresponding “solve” routine*. Actually computing the inverse matrix is generally both inefficient and inaccurate and to be avoided whenever possible.

Anyway, now that we have , we can write out the

we defined it as, and use that to solve for the

we actually wanted:


This time, we’re going backwards: ,

, and

. You will not be surprised to learn that this is called “backwards substitution”. Again, we’re just calculating

, which does not actually use a matrix inversion when U is triangular.


And that’s how you solve a linear system given a LU decomposition. In [BLAS](https://en.wikipedia.org/wiki/Basic_Linear_Algebra_Subprograms)-ese, solving a triangular system using forwards or backwards substitution for one right-hand side is called a TRSV (TRiangular Solve for a single Vector) – that single routine handles both types. It’s what’s called a level-2 BLAS operation. Level-1 operations are between two vectors, level-2 operations work on a matrix and a vector, and level-3 operations work on two matrices. More about “levels” in a bit.

That’s all dandy, but what does any of this have to do with GEMM? Hang on, we’re getting close. Let’s first generalize slightly: what if we want to solve multiple systems with the same A all at once? Say we want to solve two systems

at once (using superscripts to denote the separate vectors, since I’m already using subscripts to denote components of a vector or matrix). It turns out that you can just write this as a single matrix equation

where we just group the column vectors for x into one matrix X, and the column vectors for b into another matrix B. Again we can solve this for a LU-decomposed A by forward and back substitution (remember, still not actually forming inverses!)

note that we already know one direct way to do this type of equation: loop over the columns of X (and B) and solve them one by one, as above. This kind of operation is called a TRSM: TRianguler Solve for Multiple right-hand sides, or TRiangular Solve for Matrix, our first level-3 BLAS operation.

Just to get used to the idea of dealing with multiple right-hand sides at once, let’s write down the full matrix equation form for a 6 equations, 6 unknowns unit lower triangular system with two separate right-hand sides explicitly:

As before, the first row tells us that ; the second row mutliplied out gives

, and so forth, which we solve the exact same way as before, only now we’re always multiplying (and summing) short row vectors instead of single scalars.


But 6×6 is still really small as far as real-world systems of equations go and this is already getting really unwieldy. It’s time to chop the matrix into pieces! (You can always do that, and then work on blocks instead of scalars. This is really important to know.) Let’s just draw some lines and then cut up the matrices involved into parts:

turns into the matrix equation

where and

are unit lower triangular, and

is just a general matrix. If we just multiply the matrix product out by blocks (again, the blocks behave like they’re scalars in a larger matrix, but you need to make sure the matrix product sizes match and be careful about order of multiplication because matrix multiplication doesn’t commute) we get two matrix equations:


The first of these is just a smaller TRSM with a 2×2 system, and in the second we can bring the term to the right-hand side, yielding


On the right-hand side, we have a matrix multiply of values we already know (we computed with the smaller TRSM, and everything else is given). Compute the result of that, and we have another TRSM, this time with a 4×4 system.


The matrix multiply here is one instance of a GEneral Matrix Multiply (GEMM). The corresponding BLAS function computes , where the left arrow denotes assignment, A, B, and C are matrices, and α and β are scalar values. In this particular case, we would have

,

,

,

and

.


So we cut the matrix into two parts, did a bit of algebra, and saw that our TRSM with a 6×6 L can be turned into a 2×2 TRSM, a GEMM of a 4×2 by a 2×2 matrix, and finally a 4×4 TRSM. Note the function of the matrix multiply: once we’ve computed two unknowns, we need to subtract out their contributions from every single equation that follows. That’s what the GEMM does. It’s the first matrix multiply we’ve seen, but does it matter?

Well, the next thing to realize is that we can do the splitting trick again for the 4×4 TRSM, turning *it* into 2 even smaller TRSM, plus another GEMM. But now that we’ve establishes the idea of using blocks, let’s skip to a somewhat more serious problem size, so it becomes clear why this is interesting.

Let’s say our A is 1000×1000 (so 1000 equations in 1000 unknowns); its LU factors are the same size. This time, let’s say we’re doing 20 right-hand sides at once, and working in blocks of 30×30. We have the same equation as before:

but this time is 30×30 unit lower triangular,

is 970×30,

is 970×970 unit lower triangular,

and

are 30×20, and

and

are 970×20. Again we do the same 3 steps:


(TRSM, 30×30 matrix times 30×20 RHS)

(GEMM, 970×30 times 30×30)

(TRSM, 970×970 times 970×30)


Now the computational cost of both a m×n-by-n×p TRSM and a m×n-by-n×p GEMM (the middle dimensions always have to match) are both roughly 2×m×n×p floating-point operations (flops, not to be confused with all-uppercase FLOPS, which conventionally denote flops/s, because nomenclature is stupid sometimes). Which means the first step above (the medium TRSM) has on the order of 1800 flops, while the second step (the GEMM) takes 873000 flops. In short, of these two steps, step 1 is basically a rounding error in terms of execution time.

And note that we’re splitting a large × TRSM into a medium × medium TRSM, a large × small GEMM, and a final large × large (but smaller than the original) TRSM. And we can keep doing the same splitting process to that remaining large TRSM, until it becomes small as well. In short, this process allows us to turn a large TRSM into a sequence of medium-size TRSM (always the same size), alternating with large-size GEMMs (which keep getting smaller as we proceed down). And what happens if you look at the matrix as a whole is that we end up doing a small amount of actual TRSM work near the diagonal, while the rest of the matrix gets carpet-bombed with GEMMs.

In short, even though what we wanted to do was solve a pre-factored linear systems for a bunch of different right-hand sides, what the computer actually ended up spending its time computing was mostly matrix multiplies. The GEMM calls are coming from *inside the solver*! (Cue scary music.)

Alright. At this point you might say, “fair enough, that may indeed be what happens if you use this TRSM thing that for all we know you just made up, but I for one am *not* ever asking the computer to solve the same equation with 50 different right-hand sides in a batch, so how does this apply to me?” Okay then, let’s have a look at how LU factorizations (which so far I’ve assumed we just have lying around) are actually computed, shall we? (And again, note I’m ignoring pivoting here, for simplicity.)

What we want to do is factor our matrix A into a unit lower triangular and an upper triangular factor:

So, how do we do that? Just keep staring at that equation for a minute longer, see if it flinches first! It doesn’t? Bugger. Okay, plan B: apply our new favorite trick, splitting a matrix into blocks, to play for time until we get a brilliant idea:

Our top-left block needs to be square (same number of rows as columns), else this isn’t right, but it can be any size. This makes

square as well, and the other blocks are rectangular. The zeros are there because we want L and U to be lower and upper triangular respectively, and their entire top-right respectively bottom-left blocks

*better* be all zero. Furthermore, and

are also unit lower triangular (like the bigger L we carved them out of), and likewise

and

are upper triangular. About the remaining

and

, we can’t say much.


Still drawing blanks on the ideas front. But let’s just keep going for now: if we multiply out that matrix equation, we get

Wait a second. That first line is a smaller LU decomposition, which we’re trying to figure out how to compute. But suppose we knew for now, and we had something that gave us and

. Then that second line is really just

. That’s a TRSM, we just went over that. And the third line is

, which is also a TRSM (of a shape we haven’t seen before, but it works the same way). Once we have

and

, our hand is forced with regards to these two matrices; for the factorization to multiply to the correct result A, we

*need* them to be the things I just wrote down. And if we know these two matrices, we can attack that last equation by moving their product to the left-hand side:

Hey look, we do a big GEMM and then resume with computing a LU decomposition of the remainder – we’ve seen that kind of structure before! Great. This is how to do a block LU decomposition: compute a LU decomposition of the top-left block, two TRSMs, one GEMM to update the bottom-right part, then keep decomposing that. And this time the TRSMs are on medium × medium × large problems, while the GEMM is on large × medium × large, so again the bulk of the computation is going to be spent in the GEMM part.

But we still don’t know how to compute the LU decomposition of that top-left block. No worries: if in doubt, go for a cheap shot. We don’t know how to do this for an arbitrary block. But what if we make our partition really silly? For is a 1×1 element “matrix” levels of silly? (That is, we’re just splitting off one row and one column at the top left.)


Then is a no-brainer; all three of these matrices are 1×1, and we require

to be “unit” (ones on the diagonal), which for a 1×1 matrix just means that

. Therefore

. Ta-daa! We “solved” a 1×1 LU decomposition. But that’s all we really need. Because once we have that one value

determined, we can crank through our other 3 formulas, which give us

(the rest of the top row of U),

(the rest of the left column of L), and updates the rest of the matrix to eliminate the one variable we just computed. To compute a LU decomposition of a block, we simply keep peeling off 1×1 sub-blocks until we run out of matrix to decompose.


This description covers both “regular” and block LU decompositions (in fact we just do blocks and then get the regular decomposition as a special case when we do 1×1 blocks, at which point the problem becomes trivial), and not a single index or elementary row operation was harmed in the preceding text.

Note that this time, we turned LU decomposition (i.e. Gaussian elimination) into mostly-GEMMs-and-some-block-TRSMs, and we already saw earlier that block TRSMs turn into mostly-GEMMs-and-some-small-TRSMs. Therefore, the entire process of factoring a linear system and then solving it turns into… mostly GEMMs.

And *that’s* why everyone cares about GEMMs so much. (And also, you may now see why even if *you* don’t use TRSMs, math libraries still include them, because the solvers your app code calls want to call them internally!)

This pattern is not just specific to Gaussian Elimination-type algorithms, either. Block Householder for QR decompositions? Heavy on GEMMs. Hessenberg reduction for Eigenvalue problems? Basically Householder, which is mostly GEMMs. Computation of the Singular Value Decomposition (either for solvers or to get PCAs)? Generally starts with Golub-Kahan Bidiagonalization or one of its relatives, which is a somewhat fancier version of the QR decomposition algorithm, and yup, lots of GEMMs again. Then the actual singular value computation is iterative on that bidiagonal matrix, but that part tends to take less time than the non-iterative parts surrounding it, because the iteration is only iterating on a matrix reduced to 2 diagonals, whereas everything else works with the whole matrix.

In fact, what we’ve seen so far is a pattern of various matrix operations turning into smaller versions of themselves, plus maybe some other matrix operations, plus a GEMM. Guess what happens with a GEMM itself? If your guess was “GEMMs all the way down”, you’re right. It’s like a weed. (And turning GEMMs into smaller GEMMs is, in fact, quite important – but that’s in the paper, so I won’t talk about it here.)

This concludes our brief foray into dense numerical LA and why HPC people are so obsessed about GEMM performance. Note that dense problems are basically the easy case, at least from a high-level point of view; many of the things that are really interesting are huge (millions of equations and variables) but sparse and with exploitable structure, and these take a lot more care from the user, as well as more sophisticated algorithms. (That will nevertheless usually end up calling into a dense LA library for their bulk computations.)

Now that I’ve hopefully satisfyingly answered *why* GEMM, let’s talk a bit about the actual paper. The presentation I gave you of splitting up a matrix into blocks wasn’t just for notational convenience; that’s how these algorithms tend to work internally. The reason is that large matrices are, well, large. There’s an inherent 2D structure to these algorithms and completely looping over one axis of a giant matrix tends to thrash the cache, which in turn means there are suddenly lots of main memory accesses, and at that point you lose, because current computers can do way more computation per unit of time than they can do memory-to-cache transfers. If you truly want to do high-performance computation, then you *have* to worry about memory access patterns. (In fact, that’s most of what you do.)

That is something I pushed on the stack earlier in this post: different BLAS levels. This is an old chestnut, but it’s worth repeating: level-1 BLAS operations are vector-vector; something like say a big dot product (DOT in BLAS). Doing a dot product between two N-element vectors is on the order of 2N flops, and 2N memory operations (memops) to load the elements of the two vectors. 1:1 flops to memops – no good! Level-2 BLAS operations are matrix-vector; take say M×N matrix by M-element vector multiplication (GEMV, GEneral Matrix times Vector). Does 2MN flops, M×(N+2) memops (load all matrix elements once, load each vector element once, store each vector element once); closer to 2:1 flops to memops, which is an improvement, but still bad if you have the SIMD units to compute 32 single-precision flops per cycle and core and the main memory bandwidth to load half a float per cycle and core (the size of this gap is similar for CPUs and GPUs, for what it’s worth). It just means that your performance drops off a cliff once you’re working on data larger than your cache size.

Level-3 BLAS operations like GEMM, however, have 2MNP flops to MN+NP+MP necessary memops (load each matrix element once, store the result). That means the flops to memops ratio can in principle get arbitrarily large if only the matrices are big enough. Which in turn means that high-performance GEMMs are all about making sure that they do, in fact, reuse matrix elements extensively once they’re in the cache, and making sure that all the different cache levels are happy.

The way this works is interesting and worth studying, and *that’s* why that paper was on my list. Whew.

### 31. Bientinesi, van de Geijn-[“Formal Correctness and Stability of Dense Linear Algebra Algorithms”](http://www.cs.utexas.edu/users/flame/pubs/IMACS05.pdf) (2005; numerical LA)

According to my headings, all of the above was about the matrix multiplication paper. Well, what can I say? I was lying.

That whole business with deriving our LU decomposition by partitioning our matrix into blocks, writing down equations for the individual block elements, and then winging our way towards a solution? That’s, essentially, this paper. Except the real paper is a lot more rigorous and consequently with a lot less “winging it”.

Partitioning matrices into blocks for fun and profit is a numerical linear algebra mainstay. I saw it done for a few algorithms at university. The work of this group at UT Austin (especially the stuff following from this paper) is what made me realize just how general and systematic it can be when it’s done right.

For a large class of dense LA algorithms, this procedure is well-specified enough to derive a working algorithm automatically from a problem description, complete with correctness and numerical stability analysis, within seconds; no inspiration required. It’s an algorithm-derivation algorithm. For a very limited (and fairly rigidly structured) problem domain, but still!

This is really cool and I like it a lot.

Good stuff. FYI, part 1 was in category “Papers” but part 2 is in category “Uncategorized”.