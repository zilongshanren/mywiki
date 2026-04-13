---
title: Cycle detection algorithms are handy to know
url: https://fgiesen.wordpress.com/2010/10/08/cycle-detection-algorithms-are-handy-to-know/
published: '2010-10-08'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Cycle detection algorithms are handy to know

What the title says :). Just thought it was worth mentioning since I talked a bit about singly-linked lists in the [“Data structures and invariants”](https://fgiesen.wordpress.com/2010/09/27/data-structures-and-invariants/) post, and cycles are the primary way that a singly-linked list can “go wrong” on you without containing invalid pointers: notably, you can get this if you try to insert some item `x`

to a list when that list already contains `x`

. (If you insert the “new” `x`

before or at the position of the `x`

that’s already in the list, you will get a cycle. If you insert it later, you will inadvertently remove all items between the old and new position).

When debugging this, it’s useful to have some cycle-detection code. You can add some fields to the list for debugging (not quite as trivial as it sounds, since clearing a “visited” flag involves traversing the list that might have a cycle – you need to make sure all fields are in a known “visited” state *before* you start looking for cycles if you do it this way), but a nicer solution that doesn’t require extra memory is to use a cycle detection algorithm. There are two main choices – Floyd’s “tortoise and hare” algorithm and Brent’s algorithm – and both are worth knowing about. They’re also explained well on [Wikipedia](http://en.wikipedia.org/wiki/Cycle_detection), so read up if you’ve never encountered them before.

One interesting thing about Brent’s algorithm is that it’s an instance of iterative deepening. The classic application of iterative deepening is in minimax search. The idea is to reduce your space usage at the expense of retreading your steps anew with every successive round of deepening. But as long as the step growth rate is exponential then you end up within the optimal number of steps by a constant factor, in spite of the retreading.

Here’s a related puzzle. You’re a paratrooper who lands on a railway track that extends indefinitely in both directions. You know your buddy landed somewhere else on the track, but you don’t know exactly where or in which direction. What is the optimal search pattern?

Now that’s a name I haven’t seen in quite some while. :) Hiya Per!

Nice variation on the problem. You can find your buddy with the total distance walked within a constant factor of the distance by walking some distance d in an arbitrary direction. If you don’t find your buddy, you return to your starting point and walk c*d units in the opposite direction (for any c > 1). Keep on switching directions and multiplying distance by c every time until you find your buddy.

That got me thinking though. Assume both you and your buddy land at the same time and pick the same initial direction, distance and c (say you’ve both been drilled to follow a prescribed procedure). You’ll never meet each other (assuming the railway track is infinite, as they so often are!). Is there a strategy that’s still within a constant factor of the optimum, yet guarantees success if both persons follow it?