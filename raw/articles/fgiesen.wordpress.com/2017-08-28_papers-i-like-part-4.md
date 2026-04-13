---
title: Papers I like (part 4)
url: https://fgiesen.wordpress.com/2017/08/28/papers-i-like-part-4/
published: '2017-08-28'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Papers I like (part 4)

Continued from [part 3](https://fgiesen.wordpress.com/2017/08/27/papers-i-like-part-3/).

### 16. O’Donoghue et al. – [“Conic Optimization via Operator Splitting and Homogeneous Self-Dual Embedding”](http://stanford.edu/~boyd/papers/scs.html) (2016; numerical math/mathematical optimization)

This is a very neat first-order method to solve cone programs that brings together several key advances in the theory over the past 25 years to produce a conceptually simple (and quite short!) yet powerful solver.

Unfortunately, this puts me in a bit of a pickle here, because I expect most of you don’t know what cone programs are, what “operator splitting” is, or for that matter, what is meant by “homogeneous self-dual embedding” or “first-order method” here.

So I’m going to do the same thing I did in [part 2](https://fgiesen.wordpress.com/2017/08/14/papers-i-like-part-2/) when talking about matrix multiplies and solving linear systems of equations, and back up a whole lot.

We saw linear systems of equations; in matrix form, we were trying to solve


where ,

,

. If A is regular (nonzero determinant), this problem has exactly one solution, and barring potential numerical issues if A is ill-conditioned (just ignore that part if you don’t know what it means), we can solve this with standard methods like LU decomposition with partial pivoting – like the non-pivoted LU we saw in part 2, but now we’re allowed to swap rows to avoid certain problems and increase numerical accuracy (still not gonna go into it here). I hope that after reading part 2, you have at least some idea of how that process goes.


On the next step of the ladder up, we have linear least-squares problems. These naturally occur when we have linear systems with more equations than unknowns (more common), or linear systems with more variable than equations (less common, and I’ll ignore that case in the following), and a few others. These types of problems appear in approximation, or when trying to recover parameters of a linear model from noisy measurements where errors are uncorrelated, have expectation 0 and the same variance (as per the [Gauss-Markov theorem](https://en.wikipedia.org/wiki/Gauss%E2%80%93Markov_theorem)). They also tend to get applied to problems where they’re really not well-suited at all, because linear least-squares is by far the easiest and most widely-known mathematical optimization method. But I’m getting ahead of myself.

Under the original conditions above, we could actually achieve (in exact arithmetic anyway). If we have more equations than variables, we can’t expect to hit an exact solution always; we now have

,

,

,

(at least as many equations as variables), and the best we can hope for is

. We rewrite this into

, because in normed vector spaces, we have good machinery to express that some vector is “close” to zero: we want its norm to be small. That is, we get a problem of the type


for some norm we get to choose. Not surprisingly given the name “least squares”, we choose the 2-norm. I’m going to go over this fairly quickly because least-squares isn’t the point of this post: for a vector x, we have

where

is just a dot product of x with itself written as a matrix product, if you haven’t seen that notation before. We can get rid of the square root by just squaring everything (standard trick) and get:


That’s a quadratic function. Multi-dimensional, but still quadratic. Basic calculus tells us that we can find the extrema of a quadratic function by finding the spot where its derivative is zero. The derivative of the above expression with respect to x is

and setting it to zero brings us to the linear system called the “normal equation”

If you followed along with that, great! If not, don’t worry; the only thing you should remember here is that 2-norm means the function we’re trying to minimize is quadratic, which therefore has a linear derivative, thus we can find the minimum by solving a linear system, which we know how to do. Caveat: the normal equations are not generally the preferred way to solve such problems, because squaring A (the part) greatly amplifies any numerical problems that the matrix might have. Unless you know in advance that

is well-behaved (which you do in several types of problems), you should generally solve such problems with other non-squaring approaches based on say the QR decomposition or SVD, but again, out of scope for this post.


So far, we’ve covered elimination methods for solving linear systems (known to the Chinese back in the 2nd century CE) and linear least-squares; depending on whether you trust Gauss’s assertion that he came up with it before Legendre published it, the latter is either late 18th or early 19th century. The third of the trifecta of fundamental linear numerical algorithms is Linear Programming; this puts us either in the 19th century (if you’re feeling charitable and consider Fourier-Motzkin elimination a viable way to solve them) on in the mid-20th century for the first practical algorithm, the [simplex method](https://en.wikipedia.org/wiki/Simplex_algorithm).

But what *is* a linear program? A canonical-form linear program is a mathematical optimization problem of the form

maximize:

subject to: (componentwise),

(also componentwise)


But as the “canonical-form” name suggests, LPs come in many forms. In general, a linear program:

**must**have a linear objective function. It doesn’t need to be an “interesting” objective function; for example, the sub-class of linear feasibility problems “maximizes” the objective function 0, and it’s really just about finding a point that satisfies the constraints.- can be either minimization or maximization. They’re trivial to turn into each other: to minimize
, just maximize

and vice versa.

**can**have a set of linear equality constraints. These are not strictly necessary and hence absent in the canonical form because you can rewrite a linear equality constraintinto twice the number of inequality constraints

, but basically all solvers naturally support them directly and will prefer you to just pass them in unmodified.

**must**have some linear inequality constraints. Either direction works: to get say, just multiply everything by -1 to yield

. That’s why the canonical form just has one direction.

**may or may not**require x (the variable vector) to be non-negative. The canonical form demands it, but as with the lack of equality constraints, this one’s really not essential. If you’re forced to work with a solver that insists on non-negative x, you can split each variable that can be negative into two variableswith the constraint

. If you have a solver that defaults to unconstrained x and you want non-negative, you just add a bunch of inequality constraints

(i.e. you just append a negated identity matrix at the bottom of your constraint matrix A). Either way, still a linear program.


As you can see, while say a linear system is quite easy to recognize (is it a bunch of equations? Are they all linear in the variables of interest? If so, you’ve got a linear system!), LPs can come in quite different-looking forms that are nevertheless equivalent.

At this point, it would be customary to show a made-up linear problem. A factory can produce two kinds of widgets that have different profit margins and consume some number of machines for some amount of time, how many widgets of each kind of type should we be producing to maximize profit, and so forth. I’m not going to do that (check out a textbook on linear programming if you want to get the spiel). Instead, I’m going to show you an example with a very different flavor to hammer the point home that *LPs are not at all easy to recognize* (or at the very least, that it takes a lot of practice).

Earlier, we went over linear least-squares and saw that the problem reduces to a linear system of equations, because the objective function is quadratic and thus has a linear derivative. Therefore, that trick *only* works for the 2-norm. What if we’d really rather minimize the residuals (that’s the Ax-b) as measured in another norm? Say we want to minimize the largest deviation from 0 in any of the rows; this corresponds to the infinity-norm (or supremum norm), which is defined as . So our new problem is to minimize the maximum error in any of the components:


Turns out that this is a linear program, even if it really doesn’t look like one. Don’t see it? I don’t blame you. Here’s how it goes:

minimize:

subject to: (componentwise).


To make this clear, this is a linear program with our original vector x as its variables, plus an additional auxiliary variable t that we made up. We require that t bound the size of every component of Ax-b; those inequalities are really just saying that if we named the residuals , we’d have

,

and so on. And then as our objective function, we just want the smallest t possible (i.e the smallest upper bound on the absolute value of the residuals), which is how we encode that we’re minimizing our error bound. We don’t constrain x at all; the solver gets to pick x however it wants to make that work. And yeah, I know this feels like a really cheap trick. Get used to it. Mathematical optimization is

*all about* the cheap shots. (Also note that if we had other linear inequality constraints, like say wanting x to be non-negative, we could just throw these in as well. Still a linear program.)

And while we’re on the subject of cheap shots: we have the probably two most important norms in applications, the 2-norm and the infinity-norm; can we get the next important one, the 1-norm as well? Sure we can. Buckle up! The 1-norm of a vector is defined as , i.e. the sum of the absolute values of the components. What happens if we try to minimize

? Yup, we again get a linear program, and this time we need a whole bunch of auxiliary variables and it’s even cheesier than the last one:


minimize:

subject to: ,

,


This combines the auxiliary variables trick from last time with the “split a vector into positive and negative parts” trick we saw when I talked about how to get rid of unwanted constraints. The absolute value of residuals split that way is just the

we see in the objective function. And to top it all off, after introducing 2m auxiliary variables with the two m-element vectors

and

, we discuss them all away by adding the linear equality constraint

that forces them to sum to our residuals.


There are two points I’m trying to make here: first, that a surprising number of problems turns out to be LPs in disguise. And second, that they really don’t need to look like it.

That much for LPs. I still haven’t talked about cone programs or the actual paper, though! But now that I’ve shown how these things crop up, I’m going to reduce the amount of detail a lot.

First: cone programs. What we’ve seen so far are LPs. Cone programs are a generalization, and there’s a whole zoo of them. Cone linear programs are equivalent to regular LPs – effectively just a different canonical form. Then there’s Second-Order Cone Programs (SOCPs) which are a superset of LPs and can also express a whole bunch of other optimization problems including (convex) Quadratic Programming (quadratic objective function, linear inequality constraints) and positive semidefinite quadratically constrained quadratic programming (quadratic objective function and quadratic inequality constraints, all quadratic forms involved positive-semidefinite). This is somewhat surprising at first because SOCPs have a linear objective function and quadratic constraints, but the solution to “I want to express a quadratic objective function using a linear objective function and quadratic constraints” turns out to be yet more cheap shots. (I’ll let you figure out how this one goes yourself, you’ve seen enough by now.)

The next step up from SOCPs is semidefinite programs (SDPs), which can express everything I’ve mentioned so far, and more. And then there’s a couple more cone types that I’m not going to cover here.

What all these cone programs have in common is very similar mathematical foundations (though the neat theory for this is, to my knowledge; relatively recent; we’re in the mid-1990s now!) and very closely related solvers, traditionally [interior point methods](https://en.wikipedia.org/wiki/Interior_point_method) (IPMs).

IPMs work by encoding the constraints using smooth (differentiable) [barrier functions](https://en.wikipedia.org/wiki/Barrier_function). The idea is that such functions increase rapidly near the bounds of the feasible region (i.e. when you’re getting close to constraints being violated), and are relatively small otherwise. Then use [Newton’s method](https://en.wikipedia.org/wiki/Newton%27s_method) to minimize the resulting smooth objective function. And Newton iteration is a “second-order” method, which means that once the iteration gets close to a solution, it will roughly double the number of correct digits in every step. In practice, this means that you perform a bunch of iterations to get close enough to a solution, and once you do, you’ll be converged to within machine precision in another four to six iterations.

And that’s where we finally get to the paper itself: O’Donoghue et al.’s method is not a second-order method; instead, it’s a first-order method that uses a less sophisticated underlying iteration (ADMM) that nevertheless has some practical advantages. It’s not as accurate as second-order methods, but it needs a lot less memory and individual iterations are *much* faster than in second-order methods, so it scales to large problems (millions of variables and constraints) that are currently infeasible to solve via IPMs.

The way it works uses a lot of other techniques that were refined over the past 25 years or so; for example, the titular homogeneous self-dual embedding goes back to the mid-90s and is a general way to encode cone programs into a form where initialization is easy (always a tricky problem with iterative methods), there’s no need to do a separate iteration to find a feasible point first, and boundary cases such as infeasible or unbounded problems are easy to detect.

The end result is a fundamentally *really simple* iteration (equation 17 in the paper) that alternates between solving a linear system – always the same matrix, for what it’s worth – and a projection step. For linear programs, all the latter does is clamp negative values in the iteration variables to zero.

If you’ve made it this far, have at least some understanding of convex optimization and the underlying duality theory, and are interested in the details, definitely check out the paper! If you don’t but want to learn, I recommend checking out Boyd and Vandenberghe’s book [Convex Optimization](https://stanford.edu/~boyd/cvxbook/); there’s also a bunch of (very good!) videos of the course online on YouTube. Another good source if you’re at least somewhat comfortable with numerical linear algebra but don’t want to spend the time on the Convex Optimization course is Paul Khuong’s small tutorial [“So You Want to Write an LP Solver”](https://www.pvk.ca/Blog/2013/12/19/so-you-want-to-write-an-lp-solver/).

And this concludes the parts of this series where I info-dump you to death about numerical math. I won’t cover non-linear optimization or anything related here; maybe some other time. :)

### 17. Braun et al. – [Simple and Efficient Construction of Static Single Assignment Form](http://pp.ipd.kit.edu/uploads/publikationen/braun13cc.pdf) (2013; compilers)

Complete change of pace here; no more math for now, I promise. There will be greek symbols though, because that’s kind of required here. Sorry.

All right, Static Single Assignment form. It’s used in all kinds of compilers these days, but why? Let’s use a small, nonsensical fragment of code in some arbitrary imperative language as demonstration:

x = z + 5; y = 2*x - 1; x = 3; y = y - x;

We have 3 integer variables x, y, and z, and are doing some random computation. The important thing to note here is that we’re assigning to x and y twice, and we can’t just move statements around without changing the meaning of the program. For example, the second assignment to x *has* to go after the first assignment to y.

But computationally, that’s just silly. The second assignment to x doesn’t depend on anything; the only problem is that the *names* x and y refer to different *values* depending on where we are in the problem. For a compiler, it turns out to be much more useful to separate the (somewhat arbitrary, programmer-assigned) names from the values they correspond to. Any dependencies between the actual operations are an intrinsic property of the computation the program is trying to specify. The names, not so much. So instead, we make a pass over the program where we give a variable a new name whenever we’re assigning to it:

x1 = z + 5; y1 = 2*x1 - 1; x2 = 3; y2 = y1 - x2;

And now we can reorder the code if we want to; the only requirement is that a variable must be assigned to before it’s used. So for example, this ordering

x2 = 3; x1 = z + 5; y1 = 2*x1 - 1; y2 = y1 - x2;

has the same meaning – even though we’re now “computing” the second value of x before we compute the first.

This process can be done systematically and straightforwardly for any straight-line block of code without control flow. It’s called “Local Value Numbering” (because we’re numbering values of a variable) and is literally older than digital computers themselves – for example, the idea appears in [Ada Lovelace’s writings](https://www.fourmilab.ch/babbage/sketch.html#NoteD), penned 1842:

Whenever a Variable has only zeros upon it, it is called

0V; the moment a value appears on it (whether that value be placed there arbitrarily, or appears in the natural course of a calculation), it becomes1V. If this value gives place to another value, the Variable becomes2V, and so forth. [..] There are several advantages in having a set of indices of this nature; but these advantages are perhaps hardly of a kind to be immediately perceived, unless by a mind somewhat accustomed to trace the successive steps by means of which the [analytical] engine accomplishes its purposes. We have only space to mention in a general way, that the whole notation of the tables is made more consistent by these indices, for they are able to mark a difference in certain cases, where there would otherwise be an apparent identity confusing in its tendency. In such a case as Vn=Vp+Vn there is more clearness and more consistency with the usual laws of algebraical notation, in being able to writem+1Vn=qVp+mVn.

However, we don’t have SSA yet. That took a bit longer. The problem is what to do with control flow, such as branches and loops. How do we apply value numbering to a program like this?

x = z; y = 0; while (x > 0) { y = y + x; x = x - 1; } x = 2*y;

We can certainly apply local value numbering to each *basic block* of straight-line code, but that doesn’t get us very far in this case. So what do we do? Well, before I do anything else, let me first rewrite that loop slightly to a somewhat less idiomatic but equivalent form that will avoid some trouble with notation in a moment:

x = z; y = 0; loop { if (x <= 0) break; y = y + x; x = x - 1; } x = 2*y;

The problem we have here is that operations such as `y = y + x`

reference different versions of y depending on where we are in the control flow! In the first iteration of the loop, y refers to the initial value set by `y = 0`

; but subsequent iterations reference the y computed by the previous iteration of the loop. We can’t just decide on a single version of any particular variable up-front; it depends on how we got into the current block. However, that’s really *all* it depends on.

So here’s the key trick that gives us SSA: we introduce a construct called φ functions (phi functions) that returns one of its several arguments, depending on where we entered the current block *from*. Which of these values correspond to which way to enter the current block needs to be kept track of; since I’m going with pseudo-code here, I’ll just write it in comments. With φ functions, we can transform the whole example program into SSA form:

x1 = z; y1 = 0; loop { // when entering from outside loop, return first arg // otherwise, return second arg. x2 = φ(x1, x3); y2 = φ(y1, y3); if (x2 <= 0) break; y3 = y2 + x2; x3 = x2 - 1; } x4 = 2*y2;

Note that things get a bit tricky now: the φ functions for x2 and y2 have to reference the values x3 and y3 that are defined later in program order, and the calculation for x4 needs to pick up y2 (and not say y3), because that’s always the most recent definition of y when control flow reaches the computation of x4.

Why do we care about forming SSA? It turns out that this representation is very convenient for all kinds of program analysis, and well-suited to various transforms compilers wish to perform.

In this simple example, it’s not hard to construct the SSA form by hand. But for it to be useful in compilers, we need an algorithm, and it better be efficient – both in the sense that it doesn’t run too long, and in the sense that it shouldn’t increase the size of the program too much. In particular, we’d like to only insert phi functions that are truly necessary, instead of say inserting phis for all visible variables in every single block.

And that’s where this paper comes in. The “standard” SSA construction algorithm is due to Cytron et al., from a 1991 paper; it’s efficient and works fine, and is used in many production compilers, including LLVM. But it needs some fairly complicated machinery to do its job, and is not really suited to incremental construction.

That’s why I like this paper. It uses only elementary techniques, is simple to describe and understand, gives good results, and is suitable for quickly patching up an existing SSA-form program are modifications that would otherwise violate SSA form.

### 18. Lamport, Palais – [“On the Glitch Phenomenon”](http://lamport.azurewebsites.net/pubs/pubs.html#glitch) (1976; hardware/physics)

This link goes to Lamport’s publication page, where he writes a few notes on the paper (and his difficulties in getting it published).

Both the notes and the paper are relatively short and unlike several of the other papers I’ve covered, I don’t have any background information to add; the problem statement here is relatively elementary, it’s just the answer that is surprising.

Lamport later wrote another paper, [Buridan’s principle](http://lamport.azurewebsites.net/pubs/pubs.html#buridan), about other instances of the same problem outside of CS. Like the Glitch paper, he ran into problems getting it published, so again I’m linking to the publications page, which has his notes.

I will quote this part of the notes on “Buridan’s principle”, if you’re not already curious:

My problems in trying to publish this paper and [“On The Glitch Phenomenon”] are part of a long tradition. According to one story I’ve heard (but haven’t verified), someone at G. E. discovered the phenomenon in computer circuits in the early 60s, but was unable to convince his managers that there was a problem. He published a short note about it, for which he was fired. Charles Molnar, one of the pioneers in the study of the problem, reported the following in a lecture given on February 11, 1992, at HP Corporate Engineering in Palo Alto, California:

One reviewer made a marvelous comment in rejecting one of the early papers, saying that if this problem really existed it would be so important that everybody knowledgeable in the field would have to know about it, and “I’m an expert and I don’t know about it, so therefore it must not exist.”


On the topic of SSA form, I would like to plug a paper I love: Click and Cooper, “Combining analyses, combining optimizations”. Cliff Click went on to write C2 (the most famous incarnation of Java HotSpot).

Thanks for this series! The cone program optimization one is in an area I’ve been learning on and off so I can’t wait to read it.