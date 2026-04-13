---
title: Small note on Quaternion distance metrics
url: https://fgiesen.wordpress.com/2013/01/07/small-note-on-quaternion-distance-metrics/
published: '2013-01-07'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Small note on Quaternion distance metrics

There’s multiple ways to measure distances between unit quaternions (a popular rotation representation in 3D). What’s interesting is that the popular choices are essentially all equivalent.

### Polar form

A standard way to build quaternions is using the polar (axis-angle) form

, where n is the (unit length) axis of rotation, θ is the angle, and i, j and k are the imaginary basis vectors.


For a rotation in this form, we know how “far” it goes: it’s just the angle θ. Since the real component of q is just cos(θ/2), we can read off the angle as


where the dot denotes the quaternion dot product.

This measures, in a sense, how far away the quaternion is from the identity element 1. To get a distance between two unit quaternions q and r, we rotate both of them such that one of them becomes the identity element. To do this for our pair q, r, we simply multiply both by r’s inverse from the left, and since r is a unit quaternion its inverse and conjugate are the same:


Note that cosine is a monotonic function over the interval we care about, so in any numerical work, there’s basically never the need to actually calculate that arc cosine: instead of checking, say, whether the angle is less than some maximum error threshold T, we can simple check that the dot product is larger than cos(T/2). If you’re actually taking the arc cosine for anything other than display purposes, you’re likely doing something wrong.

### Dot product

Another way is to use the dot product directly as a distance measure between two quaternions. How does this relate to the angle from the polar form? It’s the same, as we quickly find out when we use the fact that the dot product is invariant under rotations:

and hence also

So again, whether we minimize the angle between q and r (as measured in the polar form) or maximize the dot product between q and r boils down to the same thing. But there’s one final choice left.

### L2 distance

The third convenient metric is just using the norm of the difference between the two quaternions: . The question is, can we relate this somehow to the other two? We can, and as is often the case, it’s easier to work with the square of the norm:


.


In other words, the distance between two unit quaternions again just boils down to the dot product between them – albeit with a scale and bias this time.

### Conclusion

The popular choices of distance metrics between quaternions all boil down to the same thing. The relationships between them are simple enough that it’s easy to convert, say, an exact error bound on the norm between two quaternions into an exact error bound on the angle of the corresponding rotation. Each of these three representations is the most convenient to use in some context; feel free to convert back and forth between them for different solvers; they’re all compatible in the sense that their minima will always agree.

**UPDATE:** As Sam points out in the comments, you need to be careful about the distinction between quaternions and rotations here (I cleared up the language in the article slightly). Each rotation in 3-dimensional real Euclidean space has two representations as a quaternion: the quaternion group double-covers the rotation group. If you want to measure the distances between rotations not quaternions, you need to use slightly modified metrics (see his comment for details).

I’m afraid there’s a serious problem here. Cosine is not monotonic over the interval we care about, because that interval has size 2π, not π.

The « distance » between two rotations cannot be reduced to θ(q,r) = 2acos((q/r)·1) because there would be a discontinuity at 2π: when θ goes beyond π the rotations are actually becoming closer to each other. Luckily this can be fixed using a simple absolute value: θ(q,r) = 2acos(|(q/r)·1|)

Similarly, the L2 metric is not a proper measure of how far apart two rotations are. You can just use 2(1-|q·r|) instead. (By the way, if you only care about monotonicity, you can just drop the 2!)

One last note: some people believe (and some write in books and articles) that enforcing rules such as q.w ≥ 0 when storing or creating quaternions will magically fix the problem. It will not.

Note that, in the polar form, we are taking the cosine of θ/2, not θ directly, and similarly all other forms measure half-angles not angles. I’m a bit careless in using the term “rotation” here though; technically, the metrics defined here are over the quaternions (i.e. spinors), not the rotations they represent (the problem here is that the quaternion group provides a double-cover of SO(3), so each rotation has two representations as quaternions; if q represents a given rotation, so does -q).

Cosine is monotonic over [0,π], which is enough to cover quaternions up to 2π apart (as measured by the angle in the polar form). There is no discontinuity here! The distance is nonzero because

two rotations 2π apart actually have distinct quaternions; due to the double-cover, the period is indeed 4π. Because of this period, two quaternions can’t be apart by further than 2π – you can, figuratively speaking, just go the other way round (and indeed our distance metric will slowly decrease, until at 4π we again report a distance of 0). This isnota bug and doesnotneed “fixing”, because sloppy terminology on my part aside, this post is really (as the title states) about distance metrics on quaternions, not rotations. While you can enforce 2π-periodicity like you mention, this is usually not the right thing to do; slathering quaternion-handling code in neighborhooding operations (whether it be enforcing a nonnegative real part or something else) usually causes more problems than it solves; when properly used, quaternions double-covering the rotation group is a feature, not a bug.Sure, if you consider the class of rotations spanning 4π you’re perfectly right in all respects here. I think I just wish it was made clearer to the reader that they must be careful to use the shortcuts if their set of quaternions conver the more naive 3D rotations rather than the doubly covered ones, then.

aside: I’ve always had a pet peeve about the double-coverage thing. p’=qp(1/q), which can be simplified to p’=qpq* with assumption that ||q||=1. The first version all lines thorough the origin (excluded) represent the same orientation. The second version becomes a scaled (by ||q||^2) orientation if you ignore the restriction.

Really interesting article!

And a chance for me to pick your brain :)

What if you want to find the average of n unit quaternions?

If your distance measure for quaternions q anr r is :

1 – dot(q, r)

your average m will have to satisfy:

Argmin Sum(1 – Dot(m,q_i)), for i = 0, n

or

Argmax Sum(Dot(m,q_i)), for i = 0, n

It turns out that m can simply be:

Normalize(Sum(q_i)), for i = 0, n

see here for reference (the paper uses Taylor expansion but the idea is the same): http://www.soest.hawaii.edu/wessel/courses/gg711/pdf/Gramkow_2001_JMIV.pdf

Now, as Sam said, if you want to always get the shortest distance between two quaternions q and r,

you should be using:

1 – Abs(Dot(q, r))

as your distance.

What is the mean rotation m with this distance?

The optimization now is:

Argmax Sum(Abs(Dot(m,q_i))), for i = 0, n

Ideas?

I’m pretty sure you can’t just treat the dot product between quaternions as the distance between them: since q and -q represent the same rotation, q1 . q2 and q1 . (-q2) should give the same distance. However q1 . q2 = -(q1 . (-q2)). Therefore, I believe the solution is to take the absolute value of the dot product.

They do not represent the same rotation in SU(2) which is the actual group the quaternions encode, and the double-cover is in general a feature, not a bug. You do not want to get in the habit of treating q and -q as equivalent in general; shortest-path interpolation in SO(3) is not actually what you want most of the time, and the double-cover fixes it.

You can take the absolute value if you do want to divide out the Z_2 quotient group but this is generally a mistake.

For a practical example of why the double-cover is in practice a feature not a bug (and you should _not_ get in the habing of identifying q with -q and taking whichever gives you the shorter path), consider joints with a limited range of motion that nevertheless spans more than 180 degrees total (even if just a tiny bit).

Typical examples would be the neck joint (for yawing motion), the shoulder and hip joints, and sometimes also wrist joints.

For a quick visualization, you never want interpolation between looking over your shoulder to the right and looking over your shoulder to the left to perform The Exorcist Maneuver :), and by far the easiest way to do that is to use the double-cover to your advantage. It just naturally falls out that yawing your neck 95 degrees to the left of rest pose and yawing it 95 degrees to the right of rest has the all-forward-facing 190-degreee shortest path between them, which is what you want.

Trying to build this out of shortest-path interpolation is an exercise in frustration; for that matter, so is trying to define what exactly shortest-path is even supposed to mean in a N-way weighted combination as you often have in character animation without introducing nasty discontinuities. Again, it works much better to use the double cover to your advantage and make sure all the quaternions you want to interpolate with for a given constrained joint are in the same neighborhood as the rest pose.

Finally, reiterating a point I made in an earlier comment: I specifically say in the post title that this is about distance metrics on _quaternions_, not the rotations in SO(3) they encode. q and -q might encode the same rotation but they are distinct (and distinguishable) quaternions.