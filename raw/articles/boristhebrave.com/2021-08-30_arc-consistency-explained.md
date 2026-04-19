---
title: Arc Consistency Explained
url: https://www.boristhebrave.com/2021/08/30/arc-consistency-explained/
author: Boris
published: '2021-08-30'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

I’ve been doing a lot of experiments with WaveFunctionCollapse, which [as we’ve covered before](https://www.boristhebrave.com/2020/04/13/wave-function-collapse-explained/), is essentially a constraint solver turned into a procedural generator.

The underlying solver WaveFunctionCollapse came with is called ** Arc Consistency 3**, or AC-3 for short. But AC-3 is actually one of a whole family of Arc Consistency algorithms. Today, my solver and most others uses AC-4, a more advanced algorithm. Let’s talk a bit about how those both work.

# Preliminaries

I’ve talked about [Constraint Solving](https://www.boristhebrave.com/2020/04/13/wave-function-collapse-explained/) before, but let’s go over the basic idea again. A **Constraint Satisfaction Problem** is where you have a finite set of **variables**. You know the possible range of **values **for each variable, called its **domain**, but you don’t yet know what value each variable should be. The problem contains a series of **constraints**.

Each constraint links together some variables, and asserts about what values are **allowed** in those variables. In my earlier example, I spoke about the `all_different`

constraint, which requires that the value for each variable involved in the constraint takes a different value. The problem, therefore, is to find a choice of value for each variable that is allowed by every constraint in the problem. There are many algorithms to do so.

In this article, we’ll focus on a particular sort of constraint called a **table constraint** (aka an extensional constraint). These constraints have no underlying logic about what values are allowed or not, instead, they are simply defined by a table of tuples (aka relations), where each tuple defines one possible combination of values. For example, if we had variables x, y, and z, and just one table constraint which is on (x,y, z) with tuples (1, 2, 3) and (1, 5, 6), then a solution might be x=1, y=2, z=3 or x=1, y=5, z=6. But x=1, y=2, z=6 would not be solution, as (1, 2, 6) is not a tuple in the table.

Further, most of the time, we’ll consider constraints involving two variables, sometimes called **arcs** or **binary constraints**. Working with more that two variables is an extension called [ Generalized Arc Consistency](https://glossary.informs.org/ver2/mpgwiki/index.php/Generalized_arc_consistency). Most binary algorithms have a more complex generalized variant, but we won’t discuss how those work.

Working with binary constraints is quite nice, as you can visualize the constraint problem as a graph, with one node per variable, and one edge per constraint.

It’s worth noting that any finite constraint can be converted to a table constraint by just listing every possible combination. And any constraint problem can be converted into a binary constraint problem via a [transformation](https://arxiv.org/pdf/1109.5714.pdf). But they are typically not the most efficient ways to solve the problem.

# What is Arc Consistency

Consider an arc, i.e. a constraint between two variables \(x\) and \(y\). For a given value \( a \) in the domain of \(x\), a value \(b\) in the domain of \(y\) is a **support** if \((x,y)\) is allowed by the the constraint, i.e. listed in the constraints table.

If \(a\) doesn’t have a support, then we know it’s impossible for \(x\) to have that value, as it would *have* to to violate the constraint between \(x\) and \(y\). So if we find any value without a support, we can immediately remove it from the variable domain. But if the domain of \(x\) has changed, that may mean that some other values for other variables can now be removed, and so on. A constraint with no values removable on its variables is called **consistent**.

Or explained another way, we look for values that can obviously be removed when considering a single constraint in isolation. If we’ve removed all such values, then everything is consistent. This is useful when trying to write a constraint solver.

Recall that most solvers work by making a guess, propagating some consequences of that guess, and then repeating or backtracking. We can use “make everything arc consistent” as the propagation step – it strikes a nice balance that it can infer many useful consequences, but is quick enough to run to justify tring it. Using a solver in this way is called the **Maintaining Arc Consistency** (MAC) algorithm.

# AC-3

So Arc Consistency algorithms are responsible for making every constraint in a problem consistent. A very simple algorithm for doing so might be as follows:

`AC1 Listing`


- Loop forever:
- For each constraint:
- For each variable of that constraint:
- For each value in the domain of that variable:
- Search for a support of that value on the constraint
- If no support is found:
- remove the value from the domain



- For each value in the domain of that variable:

- For each variable of that constraint:
- If nothing has been removed in this loop, exit

- For each constraint:

In other words, search everything for a value to remove, and keep doing so until there’s nothing left. This approach works, but it is extremely inefficient – there may be many constraints, and many values in each variable.

Let’s try a slightly less terrible approach:

`AC-3-ish Loop Listing`


- Start with a
*worklist*containing all the constraints - While the worklist is non-empty:
- Remove a constraint from the worklist
- For each variable of that constraint:
- For each value in the domain of that variable:
- Search for a support of that value on the constraint
- If no support is found:
- Remove the value from the domain of the variable
- Add any constraints that involve the variable back into the worklist.



- For each value in the domain of that variable:


This is better. Now, we examine each constraint once, and only re-examine a constraint if one of the variables of that constraint has actually changed. This is the essence of **Arc Consistency 3**.

In fact, AC3 is slightly smarter. It considers the direction of the arc, so that (x, y) is a different arc from (y, x). We can use this to avoid double-checking variables we’ve just checked:

`AC-3 Loop Listing`


- Start with a worklist containing two arcs for each constraint.
- While the worklist is non-empty:
- Remove an arc from the worklist, say from \(x\) to \(y\).
- For each value in the domain of \(y\):
- Search for a support of that value on the constraint of the arc
- If no support is found:
- Remove the value from the domain of the variable
- Add arcs from y to any other variables it’s constrainted with (excluding \(x\)).


- If no support is found:

- Search for a support of that value on the constraint of the arc


AC-3 was first described by [Mackworth and Mohr in 1977](https://www.cs.ubc.ca/~mack/Publications/AI77.pdf), and didn’t recieve any significant improvements until a decade later, with AC-4.

Here is an animated version of the process, on a set of 5 variables. Note that in this problem, I’ve also included two unary constraints B != 3 and C != 2. Unary constraints only involve one variable, so are easily dealt with by adjusting the variable domains before the start of the algorithm.

|
Queue:
|
|

# AC-4

AC-4 was developed [in 1986 by Mohr and Henderson](http://cse.unl.edu/~choueiry/Documents/Mohr+Henderson-AIJ1986.pdf). It introduces two keen innovations: be smarter about the loop/worklist used, and use some datastructures to speed up checking the consistency of each constraint.

## AC-4 worklist loop

Let’s focus on that loop over the worklist first. The observation is that AC-3 loses some valuable information – we know which values have been removed from the domain, but only recording what constraints are affected by that change. If we had a precise list of values removed, we could make use of that information when designing the datastructures we will discuss later.

Instead of recording the constraints that need updating, we could record the exact list of values removed.

`AC-4 Loop Listing`


- Start with an empty queue of (variable, value) pairs.
- For each constraint:
- Find all the inconsistent (variable, value) pairs
- Add those pairs to the queue
- Remove those values from the variable domains
- Initialize any datastructures

- While the queue is non-empty:
- Pop a (variable, value) pair from the queue
- For each constraint involving the variable:
- Find newly inconsistent (variable, value) pairs, given the removed pair
- Add those pairs to the queue
- Remove those values from the variable domains



Note that I’ve shortened some of the steps into higher level statements. The lines “initialize datastructure”, “find all inconsistent values” and “find newly inconsistent values” are not fully described. We *could* implement them without out any data structure at all, simply looping over every value and searching for a support, like we did for AC-3. This would still be faster than AC-3 in some cases, as now we only need check individual values that have changed, rather than every value in the domain.

But AC-4 is even smarter. We’re going to record extra information, which will speed up checking for supports.

### AC-4 Datastructure

AC-4 really only persists one piece of information. it needs an array of integers for each variable, with one entry in the array for each value. That integer will track how many supports the value has. Each time a value is removed, we update those counts, and if any count reaches zero, then that means there is no support and implies another value can be removed. We also compile a list of supports for each value, but it doesn’t need to be updated after startup.

Suppose we have 2 variables, x, y and a constraint between them. The domain of x is {1,2} and the domain of y is {3,4,5}. The contraint accepts the following tuples: (1, 3), (1, 4), (2, 4), (1, 6).

Then in terms of supports, we’d say:

x=1 has two supports: (1, 3) and (1, 4). Note that (1,6) is ignored as 6 is not in the domain of y.

x=2 has one support: (2, 4)

y=3 has one support: (1, 3)

y=4 has one support: (1, 4)

y=5 has no supports.

We can visualize that as follows.

I know that’s pretty complicated, so let’s do some simplified code. We won’t worry about having more than two variables and a single constraint. Also, I’m going to use strings, sets and dictionaries for clarity, but in practice everything is done with integers and dense arrays for efficiency.

```
# There are two variables x, y, which initially have some possible values
domain_x = set([1, 2])
domain_y = set([3, 4, 5])
# Table defines the constraint, listing possible combinations of x and y
table = set([
(1, 3),
(1, 4),
(2, 4),
(1, 6),
])
# The constraint storage
support_count_x = {}
support_count_y = {}
# The list of supports at initialization
support_list_x = {}
support_list_y = {}
# Initialize the constraint, reporting any (variable, value)
# pairs that can be rejected
def init_constraint():
# Initialize x
for a in domain_x:
count = 0
for pair in table:
if pair[0] == a and pair[1] in domain_y:
count += 1
support_list_y.setdefault(pair[1], []).append(a)
support_count_x[a] = count
if count == 0: # No support
domain_x.remove(a)
yield ('x', a)
# Initialize y
for b in domain_y:
count = 0
for pair in table:
if pair[0] in domain_x and pair[1] == b:
count += 1
support_list_x.setdefault(pair[0], []).append(b)
support_count_y[b] = count
if count == 0: # No support
domain_y.remove(b)
yield ('y', b)
# Inform the constraint that a value has been removed from a domain,
# Reporting any (variable, value) pairs that can be rejected
def val_remove(variable, value):
if variable == 'x':
for b in support_list_x[value]:
if b in domain_y:
support_count_y[b] -= 1
if support_count_y[b] == 0:
# No more supports left, b can be removed
domain_y.remove(b)
yield ('y', b)
# Now do the same thing for y
...
def ac4_loop():
queue = []
# Initialization
for item in init_constraint():
queue.append(item)
# Main loop
while len(queue) > 0:
(variable, value) = queue.pop(0)
for item in val_remove(variable, value):
queue.append(item)
```


Lets see how this works in practice. Initially, x has domain {1, 2} and y has domain {3, 4, 5}. We then count up for the supports as the initialization step.

We fill in `support_count_x `

with `2`

and `1`

, and fill in `support_count_y `

with `1`

, `1`

and `0`

. Because y=5 has no supports, we immediately know it is not actually possible for y to take this value without violating the constraint, so we can add it to the queue for removal.

When the queue is processed, the removal of 5 from the domain of y would be evaluated, but nothing else happens. One constraint on its own is not very interesting.

But suppose another constraint was also present, and it removes the value of 1 from the domain of x. It would insert `('x', 1)`

onto the queue. Then `val_remove `

would decrement `support_count_y[3]`

from `1`

to `0`

, and `support_count[4]`

from `2`

to `1`

. Thus we’d know that the value of `3`

for variable `y`

can now be removed, as it has no support remaining. Only then would this constraint become arc-consistent.

This approach can beat out AC3 considerably, as we could have huge amounts of values, but only consider the values removed each time through the loop.

But in many other cases, AC4 actually performs poorly. It has a hefty initialization step, and the `support_count`

data is quite bulky and doesn’t work that well with backtracking. While AC4 is the algorithm of choice of WaveFunctionCollapse implementations like mine, it seems state of the art has moved on.

## A note on backtracking

Using Arc Consistency in a solver is called Maintaining Arc Consistency. This means the solver repeatedly makes guesses, uses AC-4 to enforce consistency as a propagation step, and backtracks whenever it determines the problem is impossible.

AC-4 has a very high startup cost – it initializes all the counters to their highest possible values, by incrementing them by one, and compiles lists of supports. So essentially AC-4 has an average case very close to its worst case.

What we really want is to be able to re-use the datastructure from one invocation to the next. This is actually totally feasible: when the solver moves forward, the counters can be kept as is, and we just push more items onto the queue to examine. But when the solver backtracks, we must restore the counters to their previous state.

This can be achieved by either saving a list of all changes, or running AC-4 backwards over a log of value removals. It’s a lot more efficient, but still kinda bad. In later algorithms, we’ll see designs that support much more efficient backtrack operations.

## Summary

AC-3 and AC-4 are only a small piece of the vast constraint solving literature, but they are an influential ones. In the 40 years since their release generalized arc consistency has remained a large focus, and there have been many new algorithms building off of both AC-3 and AC-4. I discuss these in [my next article](https://www.boristhebrave.com/?p=1135).