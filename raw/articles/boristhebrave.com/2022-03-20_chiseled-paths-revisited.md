---
title: Chiseled Paths Revisited
url: https://www.boristhebrave.com/2022/03/20/chiseled-paths-revisited/
author: Boris
published: '2022-03-20'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

Back in 2017, I described a [method of random path generation called Chiseling](https://www.boristhebrave.com/2017/07/15/random-path-algorithm/#). It gives very nice wiggly paths, but I was never satisifed with the performance. I later revisited it, and found a [faster algorithm](https://www.boristhebrave.com/2018/04/28/random-paths-via-chiseling/), but it was a bit complicated to implement.

I’m pleased to say that I think I’ve finally found a way of implementing it that is both **fast** and **simple**.

Recall, the basic idea is that we start off with a grid, and the start and end of the path. We repeatedly remove cells from the grid that do not separate off the start from the end, until there are no more cells to remove. The remaining cells form the path to output.

The trick to speeding this up is to keep a known path from start to end between iterations, called a witness. If you remove any cell that **isn’t** in the witness path, you can be sure that it’ll never separate the start and end, as the witness path is a working route. That means you can skip doing any pathfinding in that case.

Here’s the whole thing spelt out in pseudo code:

- First, initialize an array holding the state of a cell. The state can be Open, Blocked, or Forced.
- Initially, all cells are Open, except the start and end that are Forced.
- Let
`find_path()`

be some pathfinding method (e.g.[Dijkstra’s](https://en.wikipedia.org/wiki/Dijkstra's_algorithm)) that finds a route from the start and end avoiding Blocked cells. It returns null if there is no path. - let
`witness = find_path()`

- while True:
- if there are no Open cells, return
`witness`

- let
`c`

be a random Open cell - Set
`c`

to Blocked - If
`c`

is in`witness`

- Let
`new_path = find_path()`

- if
`new_path`

is null:- Set
`c`

to Forced

- Set
- else
`witness = new_path`



- Let

- if there are no Open cells, return

Every iteration either sets an Open cell to Blocked or Forced (if blocking it would separate start/end), so it will terminate when every Open cell has been set. It’s a lot faster than my previous techniques, as the majority of randomly picked Open cells will not be in the path, so nothing needs to be recomputed. And by the time the witness becomes a significant fraction of all open cells, there are so few cells remaining that `find_path`

is relatively quick.

The full code is on [github](https://github.com/BorisTheBrave/chiseled-random-paths).

Note that the choice of witness doesn’t affect which cells are actually picked, so you can use any pathfinding technique and you’ll get the same distribution of output.

## Animation

## Live Demo

Wiggliness

Animate

[Generate a new path](https://www.boristhebrave.com#)

(all tile graphics are made by

[fictionaldogs of ZFGC](http://zfgc.com/forum/index.php?topic=41500.0))

## Variations

### Performance

It’s handy to keep a set with the list of Open cells in it, and remove a random cell from it each iteration. This is the more efficient than searching through the whole grid looking for open cells.

You can also combine this algorithm with my [previous suggestion](https://www.boristhebrave.com/2018/04/28/random-paths-via-chiseling/) of using an algorithm to find articulation points. When find_path is called, also find articulation points, and set the cells to Forced. This speeds things up slightly as it’s no longer necessary to find articulation points by trial and error.

### Multiple endpoints

As before, you needn’t limit yourself to paths between two points. You can have as many points as you like, as long as `find_path()`

returns a set of cells that links them all. This is easily done by just path finding from a to b, a to c, etc, as there is no need for `find_path()`

to find a *shortest* path. Some pathfinding algorithms can be modified to do find it all in a single call.

### Wiggliness

While chiselled paths makes nice wiggly paths, it doesn’t really have any parameters to control it. The algorithm above can be easily modified in a useful way. Firstly, change `find_path()`

so it picks a *random* *shortest *path, which is usually an easy change for most pathfinding algorithms. Secondly, make the random choice of cell a **weighted** random choice, where picking a cell on the witness path has weight `w`

and a cell off the path has weight 1.

`w`

is then a wiggliness parameter. `w`

=0 is zero wiggliness – the output path will be always be a shortest path. `w`

=1 gives the same wiggliness as the normal algorithm, and w greater than one will actively prefer longer paths.

Nice simple algorithm with good results! Regarding performance, you could speed it up by just terminating early; by watching the animation, it seems like at about 50% completion (i.e. half of the cells are still “open”) the path is usually already either unique, or of good enough quality. Alternatively, you could terminate if the last 5 cells chosen from the witness were “forced”; this usually means the rest of them will be, too.

And if you’re already using Dijkstra, after a certain point you could just block all the cells more than N tiles from the Witness path.