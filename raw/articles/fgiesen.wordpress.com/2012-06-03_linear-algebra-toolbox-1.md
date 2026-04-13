---
title: (Linear) Algebra Toolbox 1
url: https://fgiesen.wordpress.com/2012/06/03/linear-algebra-toolbox-1/
published: '2012-06-03'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# (Linear) Algebra Toolbox 1

I’m prone to ranting about people making their lives more complicated than necessary with regards to math. Which I’ve been doing quite often lately. So rather than just pointing fingers and shouting “you’re doing it wrong!”, I thought it would be a good idea to write a post about what I consider good practice when dealing with problems in linear algebra and (analytic) geometry. This is basically just a collection of short articles. I have enough material to fill several posts; I’m just gonna write more whenever I feel like it. (Don’t worry, I didn’t abandon my series on Debris, we just had a few gorgeous weekends in a row, and living as I do in the Pacific Northwest sunny weekend days are a limited resource, so I didn’t do a lot of writing lately).

### Get comfortable manipulating matrix expressions

In high school algebra, you learn how to deal with problems such as solving for x using algebraic manipulations. The exact same thing can be done with expressions involving vectors and matrices, albeit with slightly more restrictive rules. It’s worthwhile to get familiar (and comfortable) with this. The most important rules to keep in mind are:


- Vector and matrix addition/subtraction can be handled exactly the same way as their scalar counterparts.
- Since for matrices in general
, multiplying an equation by a matrix must be done consistently – either from the left on both sides, or from the right on both sides.

- As an exception to the above, multiplying a matrix/vector etc. by a scalar is commutative, so the direction doesn’t matter, and the scalar can be moved around in the expression to wherever it is convenient.
- Multiplying any scalar equation by 0 turns it into “0 = 0” which is true but useless. For matrix equations, the equivalent is that the matrices you multiply by must be non-singular, i.e. they must be square and have non-zero determinant.

**Example:** Consider the map . This is an affine transformation, i.e. a linear transformation followed by a translation. Let’s solve this for x:

⇔

⇔

⇔

. The only interesting step here is multiplying from the left by

, the rest is very basic (and shown in more detail than I will use for the rest of this post). Note the result is in the same form as the expression we started with – meaning that the inverse of an affine map (when it exists) is again an affine map, not very surprisingly.


### Matrices depend on the choice of basis

This one is really important.

In linear algebra, the primary objects we deal with are vectors and linear transforms – that is, functions that map vectors to other vectors and are linear. **Neither concept involves coordinates**. Particularly among programmers, there’s this meme that “vector” is basically just fancy math-speak for an array of numbers. **This is wrong**. A vector is a mathematical object, just like the number ten. The number ten can be *represented* in lots of different ways: as text, as “10” in decimal notation, as “1010” in binary notation, as “X” using roman numerals and so forth. These representations are good for different things: decimal and binary have reasonably simple algorithms for addition, subtraction, multiplication and division. Roman numerals are reasonably easy to add and subtract but considerably trickier to multiply, and the textual representation is related to the pronunciation of numbers when we read them out loud, but completely useless to do arithmetic on.

Writing a vector as tuple of numbers is a particular representation that means “one times the first basis vector, plus two times the second basis vector, plus three times the third basis vector”. This representation depends on the choice of basis vectors. Any non-zero vector can end up represented as

, given the right choice of basis. Similarly, a matrix depends on the basis for the source and destination vector spaces, and a given linear transform can have any number of different representations, corresponding to different choices of basis vectors. The important bit here is that even though the numbers can be made almost anything, they’re still describing the same mathematical object, and everything that’s true for this mathematical object will be true no matter which representation we pick.


This means that we have a considerable amount of freedom in choosing a convenient representation. As long as we’re writing code that performs computation, we’ll still drop down to matrices and numbers eventually. But generally, we want to postpone that choice until we absolutely have to – the later we nail it down, the more information we have to make the resulting computation easier. And a lot of stuff can be done without ever choosing an explicit basis or coordinate system at all.

### What’s in a matrix?

Now I’ve explained what the values in the coordinate representation of a vector mean, but I haven’t yet done the same for the values in a matrix. Time to fix this. Note that with a matrix, there’s generally two vector spaces (and hence two bases) involved, so we have to be careful about which is which. Here’s a simple matrix-vector product expanded out using the usual matrix multiplication rule and then rearranged slightly:

=

=

.


This is straightforward algebra, but it’s key to figuring out what’s matrices actually *mean*. Note that the vectors appearing in that last expression are just the first, second and third columns of our matrix A, respectively. Those are vectors in the “output” vector space, which is 2-dimensional here; there’s also a 3-dimensional “input” vector space that x lives in. Often the two spaces are the same and use the same basis, but that is not a requirement! Anyway, if we plug in (corresponding to the first basis vector in our input vector space), the result will just be the first column of A. Similarly, we’ll get the second and third columns of A if we choose different “test vectors” with the one in a different place.


And this is the connection between matrices and the linear transforms they represent: to form a matrix, just transform the i-th vector of your “input” basis and write the resulting vector represented in your “output” basis into column i. This also means that it’s trivial to write down the matrix for a linear transform if you know what that transform does to your basis vectors. Note that here and elsewhere, if you use row vectors instead of column vectors, you write xA, and the role of rows and columns are reversed.

### Change of basis

Now to give an example for why these distinctions matter, let’s look at a concrete problem: suppose you have a 3D character model authored in a tool that uses a right-handed coordinate system with +x pointing to the right, +y pointing up, and +z pointing out of the screen, and you want to load it in a game that has a left-handed coordinate system with +x pointing right, +y pointing up (same as before) and +z pointing into the screen. Let’s also say that character comes (as character models tend to do) complete with a skeleton and transform hierarchy. Assume for simplicity that the transforms are all linear and represented by 3×3 matrices. In reality they’ll be at least affine and probably be represented either as homogeneous 4×4 matrices or using some combination of 3×3 rotation matrices or unit quaternions, translation vectors and scale factors, but that doesn’t change anything substantial here.

So what do we have to do to convert everything from the modeler’s coordinate system to our coordinate system? It’s just a few sign flips, right? How hard can it be? Turns out, harder than it looks. While it’s easy enough to convert vertex data, matrices present more of a challenge, and randomly flipping signs won’t get you anywhere – and even if you luck out eventually, you still won’t know *why* it works now (you can ask anyone who’s ever tried this).

Instead, let’s approach this systematically. Imagine the model you’re trying to load in 3D space. What we want to do is *leave the model and transforms exactly as they are*, but express them in a different basis (coordinate system). It’s important to get this right. We’re going to be modifying the matrices and coordinates, true, but we’re not actually changing the model itself. Computationally, “express this vector in a different basis that has the z axis pointing in the opposite direction”, “reflect this vector about the z=0 plane” and “flip the sign of the z coordinate” are all equivalent, but they correspond to different conceptual approaches. When you perform a change in basis, it’s clear what has to happen with matrices representing transforms (namely, they have to change transforms to). A reflection is a transform – you might want to apply it to the whole model (at which point it’s best expressed as another matrix you pre-multiply to your transform hierarchy), you might want to reflect part of it, or you might want to just reflect some vertices. All of these actually modify the model (not just your representation of it), and it’s not clear which one is the “right” one. And so forth.

Anyway, enough of philosophy, back to the subject at hand: We have two different bases for the same 3D space: the one used by the modeler (let’s call it basis M) and the one used by your game (basis G). We want to leave the model unchanged and change basis from M to G. The linear transform that leaves everything unchanged is the identity transform I that sends every vector to itself. As mentioned above, every matrix depends on not only the linear transform it represents, but also the basis chosen for the input and output vector space. Let’s make that explicit by adding them as subscripts. We can then write down a matrix that takes a vector expressed in basis M, applies the identity transform (=leaves everything unchanged), then expresses the result in basis G. In our case, the x and y basis vectors in both G and M are the same, while the a vector expressed as in basis M corresponds to

in basis G (and vice versa). Putting it all together, we can write down the

*change-of-basis matrix* to G from M:

.


If we wanted to go the opposite way (to M from G), we would use . Now what can we do with this? Well, first of, we can use it to convert vectors expressed in M to vectors expressed in G:


Who would’ve thought, we end up sign-flipping the z coordinate. Written like this, it just seems like a verbose (and inefficient) way to write down what we already know. But note that the subscript notation allows us to see at a glance which basis we’re currently in. More importantly, we can see when we’re trying to chain together transforms that work in different bases. This comes in handy when dealing with trickier objects, such as matrices: note that the transforms stored in the file will both accept and produce vectors expressed in basis M; by our convention, we’d write this as . Now say we want to get the corresponding transform in basis G – well, we could try the same thing that worked for vectors and just multiply the right form of the identity transform from the left:


Oops – see what happened there? That gives us a matrix that produces vectors expressed in basis G, but still expects vectors expressed in basis M as input. To get the true representation of T in basis G, we need to throw in another change of basis at the input end:

So to convert everything to basis G, we need multiply all the vectors with on the left, and multiply all matrices with

from the left and

from the right (the resulting double sign-flip “from both sides” is the bit that’s really hard to stumble upon if you approach the whole issue in “let’s just keep flipping signs until it works” mode). Alternatively, we can leave all the vectors and transforms as they are, happily working in basis M, but then throw in a single

at the top of the transform hierarchy of the model, so that all of it gets transformed into the “game” basis before the rest of the rendering / physics / whatever code gets to see it. Either way works. And not only that, I hope that by now it’s clear

*why* they work.

**Note:** By the way, this convention of explicitly writing down the source and destination coordinate systems *for every single matrix* is good practice in all code that deals with multiple coordinate systems. Names like “world matrix” or “view matrix” only tell half the story. A while back I got into the habit of always writing both coordinate systems explicitly: `world_from_model`

, `view_from_world`

and so forth. It’s a bit more typing, but again, it makes it clear which coordinate system you’re in, what can be safely multiplied by what, and where inverses are necessary. It’s clear what `view_from_world * world_from_model`

gives – namely, `view_from_model`

. More importantly, it’s also clear that `world_from_model * view_from_world`

doesn’t result in anything useful. This stuff prevents bugs – the nasty kind where you keep staring at code for 30 minutes and say to yourself “well, it *looks* right to me”, too.

### Implement your solution, not your derivation

This ties in with [one of my older rants](https://fgiesen.wordpress.com/2010/10/21/finish-your-derivations-please/). This is not a general rule you should always follow, but it’s definitely the right thing to do for performance-sensitive code.

In the example above, note how I wrote all transforms involved as matrices. This is the right thing to do in deriving your solution, because it results in expressions that are easy to write down and manipulate. But once you have the solution, it’s time to look at the results and figure out how to implement them efficiently (provided that you’re dealing with performance-sensitive code that is). So if, for some perverse reason, you’re really bottlenecked by the performance of your change-of-basis code, a good first step would be to not do a full matrix-vector multiply – in the case above, you’d just sign-flip the z component of vectors, and similarly work out once on paper what has to happen to the entries of T during the change of basis.

I’ll give more (and more interesting) examples in upcoming posts, but for now, I think this is enough material in a single batch.

I think you are confusing vectors with vector spaces, and confusing matrices in general with their use in transforms in linear algebra in particular. While the math itself is correct, the explanations and rationale are a bit off, as if you just learned a particular application and not the underlying principles. The result could be more confusing rather than helpful. [E.g., if each element of a vector must be multiplied by the corresponding element in a basis vector, what are the elements in a basis vector multipled by?]

A vector is usually defined as an ordered list of numbers (a tuple) that is an element in a set called a vector space — i.e., there are two binary operations (addition and scalar multiplication) that, when applied to any elements of that space, obey 8 fundamental axioms (associativity, commutivity, identity, etc.). In a Real vector space, a vector _is_ just an array of real numbers. Then a basis is a minimal ordered (or indexed) set of vectors that spans the entire space — i.e., any vector in the set can be expressed as a linear combination (a finite sum) of the basis vectors. No circular logic required. Now matrices and linear algebra can be used as linear maps between vector spaces: for things like affine transforms of vectors, changes of bases., etc.

If you have actual issues with the content of these posts, feel free to list specific examples. I will not comment on philosophical issues; if you disagree with the way I am presenting the material, that’s fine; there’s different ways to approach the subject, and if my presentation doesn’t work for you, feel free to stick with a different one.

“[E.g., if each element of a vector must be multiplied by the corresponding element in a basis vector, what are the elements in a basis vector multipled by?]”This touches onto a tricky issue with presentation, namely that using R^n as the canonical example makes it notoriously hard to distinguish between vectors and their representations.

The vectors in R^n are just n-tuples of real numbers. To avoid introducing extra confusion here, I’ll write tuples with commas and vectors without. For posterity, say we have R^2. We have the canonical basis e_1 = (1,0), e_2 = (0,1) – these are both pairs (2-tuples) and members of the vector space R^n. Scalar multiplication and addition in the vector space are defined by applying the respective operations to the tuples, componentwise.

Now, any element of R^2 is both a pair of numbers (because, after all, R^2 is just a set, the cartesian product of R with itself) and a vector (because R^2, with operations defined as sketched above, obeys the vector space axioms). As a pair, some vector v might be (a,b); now what I’m saying is that we can also write this as “a*e_1 + b*e_2” (algebraically, this is trivial). More generally, for any a, b, by closure of the vector space “a*e_1 + b*e_2” is also in R^2, and we write that as the vector “(a b)” with respect to the canonical basis. This happens to agree with (a,b), because the canonical basis is picked to make these two things agree. So in this basis, (2,0) and (2 0) are the same thing.

But I could equally well pick another basis, say v_1=(1,1), v_2 = (1,-1), and then (2,0)=1*v_1 + 1*v_2 would be expressed as (1 1). Again when working directly in R^n this seems pointless; but in practice, a lot of the finite-dimensional spaces that people actually work with are not actually R^n, even though they’re isomorphic to R^n. Euclidean 3-space is a geometrical concept that happens to have the structure of a 3-dimensional real vector space (and is thus isomorphic to R^3); but even though each point in 3-space can be written in cartesian coordinates, unlike “straight” R^n there is no universal agreement on a canonical set of basis vectors. I might decree that i=(1,0,0) and that this point in R^n shall map to the “right” vector in Euclidean space in my isomorphism, but others might choose differently. That’s when keeping the distinct concepts of vectors vs. the tuples representing them (once a basis has been chosen) starts to matter.

Another non-geometric example would be the (n+1)-dimensional vector space of real polynomial of degree <=n. Now the vectors are polynomials, and a typical basis would be the monomial basis – say "x^0, x^1, x^2" for n=2. With this basis, the polynomial "x^2 – 2x + 1" would be written (1 -2 1), and the two forms hopefully look different enough that the distinction is clear.

“A vector is usually defined as an ordered list of numbers (a tuple) that is an element in a set called a vector space”This definition is far, far too specific; a vector space over a field F is simply any set combined with scalar multiplication and addition such that the vector space axioms apply, and any element of the set is then called a vector.

Vectors need not be an ordered list of numbers (see the polynomial example above, where vectors are just polynomials of degree <=n), nor do they even need to be isomorphic to one. The vector space C^inf(R) of smooth functions over R has functions as vectors, and these functions can't be written as an ordered list of numbers. The vector space L^1([0,1]) has vectors that are equivalence classes of Lebesgue-integrable functions over [0,1], and again the elements can't be written that way. Even finite-dimensional spaces can't necessarily been written that way; for example, as my field F I might choose the field of meromorphic functions over a Riemann surface. Then my scalars are functions, not numbers, even if I just look at the vector space F^2.

“In a Real vector space, a vector _is_ just an array of real numbers.”No, this is patently untrue; see the various examples of infinite-dimensional real vector spaces above. Even for finite-dimensional spaces, take the example of the vector space of polynomials of degree <=n. After choosing a basis (say the monomial basis, or the Chebyshev basis), we can write each vector as a n-tuple of real numbers (by expressing the vectors as a linear combination of the basis vectors), and get an isomorphism between the space in question and R^n. Being isomorphic, the two spaces are thus equivalent, but still not identical.

Wish I’d found these posts years ago! I’ve struggled to crack the concepts behind change of coordinate systems for a long time, with insight always seeming to hang just out of reach. Definitely going to be digesting these in more detail with lots of drawings!