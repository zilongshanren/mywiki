---
title: Intervals in modular arithmetic
url: https://fgiesen.wordpress.com/2015/09/24/intervals-in-modular-arithmetic/
published: '2015-09-24'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Intervals in modular arithmetic

I wrote about regular interval overlap checking [before](https://fgiesen.wordpress.com/2011/10/16/checking-for-interval-overlap/). Let’s consider a somewhat trickier case, where our intervals are not defined over the real numbers or regular integers, but are instead subsets of the integers modulo N (for some fixed N). In this post, I’ll just consider the math; but this is something I’ve used in several places, so I expect I’ll be writing about some concrete uses eventually. Throughout this document, I’ll be writing for the set

of integers mod N (feel free to ignore the notation if you’re not familiar with it).


### Intervals mod N, first attempt

The first thing we need to do is agree on what we mean by an interval mod N. Suppose that N=16. In that setting, the meaning of the interval [5,7] is pretty clear: the set {5, 6, 7}. And we can also take something like the integer interval [14,17] representing the set {14, 15, 16, 17} and reduce it mod N to get {14, 15, 0, 1}. But doing this required us to use values outside of {0, …, N-1} to specify the end points. This is often a useful model – I talk about some advantages when doing this for ring buffers in [this old post](https://fgiesen.wordpress.com/2010/12/14/ring-buffers-and-queues/) – but it’s a bit of a cheat; we’d like a way to specify intervals mod N that don’t require us to leave the set of integers mod N to handle the “wraparound” case.

This means that we want to define something like the interval [14,1]. For the regular integers, this would be the empty set; but mod N, it makes more sense to properly wrap around (for example, when you say “the trains don’t run from 11:30pm to 5:30am”, it’s understood that you mean 5:30am the next day, not an empty interval). One way to do this is by handling the wrap-around case separately. **Assuming a, b are reduced mod N**, we could for example define:

This works, but it’s messy, and chopping up our single connected interval mod N into two pieces for the wrap-around case feels like it’s missing something fundamental about arithmetic mod N. We’re thinking in terms of a number line:

But the integers mod N aren’t very “line-like” at all, and they’re commonly (and more appropriately) drawn as a circle (like a clock, with 0 at the top and numbers increasing clockwise, to maximize familiarity—apologies to all mathematicians who expect positive angles to move counter-clockwise).

And in this visualization, there is absolutely nothing special about our interval [14,1]. We happen to pass through 0, but 0 isn’t actually special. It’s just another point on the circle. The reason 0 *becomes* special when we think in terms of regular integers (and hence a number line) is that it’s usually the place where we decide to cut open the circle so we can flatten it into a line. But that has nothing to do with the circle (or the integers mod N); it’s an incidental artifact of the representation we’re picking.

### A different approach

The key problem here is that intervals are normally defined in terms of ordering relationships. For example, real-number intervals are usually defined as sets

.


based on a total order “≤”. But in our circle, we don’t have a useful ordering relation. When you write “4 < 7”, this means that 4 is to the left of 7 on the real number line. If you start at 4 and keep walking right, you’re gonna come by 7 eventually. If you instead were to walk left, the numbers would just keep getting smaller indefinitely.

On our circle mod N, this is not true. If you start at 4 and keep walking in the positive direction (clockwise in our case), you’ll reach 7 after three steps. If you instead walk counterclockwise from 4, you still reach 7 – this time after taking the long way round, in thirteen steps. This is true for any pair of numbers on the circle, which after all represent congruence classes of integers mod N (if you don’t know the terminology, just ignore the rest of this paragraph). It makes sense to say that the integer 4 is less than the integer 7, but the set is not in any useful sense “less” or “greater” than the set

. Viewed in that light, the definition for [a,b] mod N given above is outright weird; the case distinction between “a ≤ b” and “a > b” is testing a condition that doesn’t really make sense in terms of the concepts being expressed.


So ordering relationships are on shaky footing. We can, however, usefully talk about *distances*. For example, “4” and “7” are definitely three steps apart when we take the shortest path, also three steps apart when we’re only allowed to move clockwise, and thirteen steps apart when we’re only allowed to move counterclockwise. In general, we can define distance functions for the “increasing” (clockwise), “decreasing” (counter-clockwise) and shortest-path distances between two points (we won’t actually be using that latter one, I just mention it for completeness):




These distance functions are, technically speaking, mappings from the integers mod N to the natural numbers (hence the explicit use of mod as a binary operation). The distances are regular non-negative integers; while points in the integers mod N can’t be meaningfully compared, distances can. That’s why they’re useful to us. Also note that the “mod N” here is the modulus under Euclidean/floor division – that is, a non-negative value smaller than N.


Most programming languages use truncating division instead, which means the modulus has absolute value less than N but might be negative; you need to consider this when turning any of the equations in here into code!

Given all this, let’s go back to our problem of defining intervals nicely. Well, how do we draw something like the interval [14,1] on our circle? We just move the pen to “14” and start drawing a clockwise arc until we hit the “1”. We can use that exact idea to define intervals: namely, a point x is inside the interval [a,b] if, starting from a and walking in increasing order (clockwise), we hit x before we leave the interval. That leads to our improved definition of a closed interval mod N:


or the equivalent


and the generalizations to half-open intervals are straightforward:



Things are simpler if we always start measuring from the closed (inclusive) end, so that’s what we do. I’ll drop the (mod N) for the rest of the article; we know that’s our setting.

### Point-in-interval tests and symmetry

This definition can be turned into code immediately and leads to fairly elegant point-in-interval tests that don’t break down into multiple cases:

// modN(x) is assumed to calculate Euclidean (=non-negative) x % N. // x in [a,b] (mod N)? static bool point_in_closed_interval(int x, int a, int b) { return modN(x - a) <= modN(b - a); } // x in [a,b) (mod N)? static bool point_in_half_open_interval(int x, int a, int b) { return modN(x - a) < modN(b - a); }

At this point, you should also be noticing something funny about that code (it’s a bit harder to see in the definitions above since the detour through the distance functions obscures the actual computation going on); namely, the fact that we’re subtracting a and then reducing mod N on both sides.

It’s confession time. This whole notion with measuring distances along the circle is not how I derived this; it’s the best way I know to *think* about this problem, but that knowledge came in retrospect. I got here the long way round, with several false starts. The key idea turned out to be thinking about symmetries, which is always worth doing if the problem you’re working on has any; see for example [this](https://fgiesen.wordpress.com/2009/12/15/dxt5-alpha-block-index-determination/) post I wrote 6 years ago!

In this case, the integers mod N are a cyclic group—they wrap around. That’s why it makes sense to draw them as a circle. And that’s why being attached to any particular point being 0 is a bit silly: a circle has continuous rotational symmetry, and our discrete cyclic group has N-fold rotational symmetry. We get the same image if we rotate by an N’th of a full turn. And going back to our setting, since we really only care about distances, we can cyclically rotate our points around any way we want without changing the results.

What these tests really do is exploit this symmetry, “translating” (or more appropriately, rotating) everything by -a. This turns testing x against the interval (or the half-open variants) into testing

against

. Once we move the start point of the interval to 0, we don’t have to worry about wrap-around happening in inconvenient places anymore; comparing the integers directly works fine. Score one for symmetry.


### Interval overlap

This takes care of points. Now for something trickier: how do we test for interval overlap?

The [standard tests for interval overlap](https://fgiesen.wordpress.com/2011/10/16/checking-for-interval-overlap/) are slick, but not really applicable in our situation: the center-extent trick actually generalizes just fine to integers mod N and much more general settings (it works in arbitrary metric spaces provided the sets in question can be expressed as balls in the target metric) but is not ideal in a discrete setting, and the direct tests rely heavily on an order structure we don’t have in our cyclic world.

But what we do have are reasonably simple point-in-interval tests. Can we build an interval overlap test out of them? Well, we can try. Suppose we have two intervals [a,b] and [c,d]. For example, surely, if the “left” endpoint c of [c,d] falls inside [a,b], the two intervals overlap – after all, we know a point that is in both of them! And by symmetry, swapping the roles of the two intervals, if a falls inside [c,d], we again must have overlap.

If you start drawing a few pictures of intervals in various configurations, you’ll soon notice that testing both of these conditions seems to detect all configurations where the intervals actually overlap (and this works with intervals in the real numbers as well as in our discrete setting). The question is, can we *prove* that testing these two points is sufficient, or are we merely lucky? It turns out we didn’t just luck out; here’s a quick proof:

**Lemma**:


or

. In words, the two (non-empty) intervals overlap if and only if at least one of a or c is inside the respective other interval.


Proof: “”

, so if we also have

, then that gives us a point in the intersection of [a,b] and [c,d], which therefore can’t be empty. Likewise with a. Therefore, if either of the two conditions on the right-hand side holds, we indeed have a non-empty intersection.


“” The intersection isn’t empty, so take

. x is in both intervals. Informally, we now “slide” x to the “left” (in negative direction) through the intersection until we hit either of the interval end points a or c. Formally, consider the distances from the interval start points to x

and

. Suppose that d

a ≤ dc. Then we have



In words, a’s distance from c, in positive direction, is no more than x’s; since x already was inside of [c,d], surely a must be too. If instead da > dc, we learn that c is inside [a,b]. In either case, this proves the claim.

This takes care of closed intervals. Note that this proof leans heavily on the intervals in question being non-empty. We can readily adapt it to half-open intervals of the form [a,b), but we do need to make sure to catch either interval being empty first, in which case the intersection of intervals is necessarily empty too. Likewise, you can also easily adapt it to half-open intervals of type (a,b], but in this case you want to be using the “right” end points of intervals for testing, not the left end points.

This may all sound complicated, but the implementation is actually quite short and simple:

// do [a,b] and [c,d] overlap? static bool closed_intervals_overlap(int a, int b, int c, int d) { return modN(c - a) <= modN(b - a) || modN(a - c) <= modN(d - c); } // do [a,b) and [c,d) overlap? static bool half_open_intervals_overlap(int a, int b, int c, int d) { int w0 = modN(b - a); int w1 = modN(d - c); return (w1 != 0 && modN(c - a) < w0) || (w0 != 0 && modN(a - c) < w1); }

And there we go. Interval overlap tests mod N.

### Implementation notes and variations

The most common case in systems programming involves power-of-2 N. In that scenario, `modN`

is readily implemented via bit masking as a single binary AND operation. If N is 232 or 264, 32- or 64-bit unsigned integers can (and should) be used directly, in which case there is no need for explicit masking in the code (although on some 64-bit architectures, unsigned 32-bit arithmetic compiles into 64-bit arithmetic with masking anyway). This is one of the rare cases where unsigned integer overflow works *exactly* the way we need. In this case, you want to be using unsigned integers throughout.

As presented, we’re working with intervals given in terms of two end points, because that’s the most common presentation. But computationally, *all* of the functions in the code shown actually use a single endpoint (on the “closed” end) along with the width of the interval. That’s the `modN(b - a)`

and `modN(d - c)`

terms we keep computing. So if you’re working a lot with intervals mod N, or storing them, you probably want to consider working in that representation directly.

The intervals in this article are intentionally defined with their endpoints coming from , to force us to think about the effects of the cyclical wrap-around in the integers mod N cleanly. Now that we’ve spent some time thinking it through, we can relax that requirement. In particular, when using ring buffers with what I call the “

[virtual stream](https://fgiesen.wordpress.com/2010/12/14/ring-buffers-and-queues/)” model (read/write cursors not reduced mod N), it can make sense to just not reduce the interval lengths mod N at all—that is, turn occurrences of `modN(b - a)`

and `modN(d - c)`

in the code into plain `b - a`

and `d - c`

, respectively, or reduce with respect to a modulus that’s a larger multiple of N. Among other things, this allows us to have half-open intervals covering the entirety of , something the fully reduced variant cannot easily do.


And as a final closing remark, this article comes in at 2500 words to explain less than 20 lines of code doing nothing but straightforward integer arithmetic. That has to be *some* sort of personal record. I’m not sure if that’s good or bad.

Small correction:

> These distance functions are, technically speaking, mappings d : \mathbb{Z}_N \rightarrow \mathbb{N}_0

Should be:

These distance functions are, technically speaking, mappings d : \mathbb{Z}_N \times \mathbb{Z}_N \rightarrow \mathbb{N}_0

Indeed, thanks for the catch! Fixed.

Hello,

I’m currently working on a thesis that involves some modulo intervals. The definition in this article using the distance function works really well for my purpose and I would like to use it. There is no source cited here so I assume it is your own notation? How can I cite you?

Kind regards.

That’s my own notation, yes. I’m sure I’m not the first to describe something like this, but I didn’t conduct a literature search (since it’s all elementary modular arithmetic). As for citation, just as you would cite a website I guess? Might make more sense to link to a snapshot copy on archive.org in case this blog ever migrates elsewhere.