---
title: Exploring Rectangle Subdivisions
url: https://www.boristhebrave.com/2025/05/03/exploring-rectangle-subdivisions/
author: Boris
published: '2025-05-03'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

Last week, I saw a talk on [ Vuntra City](https://vuntracity.com/), a procedurally generated city with a fully explorable city. Developer Larissa Davidova explained that she settled on using Recursive Subdivision for the city blocks, as she wanted some level of organicness, while still only having to deal with rectangles. But she didn’t like having indefinitely long roads that cause implausible sightlines.

One way Vuntra City handles this is by subdividing a rectangle into 5 blocks, a pattern I called “whirl” in my [previous article on recursive subdivision](https://www.boristhebrave.com/2021/08/14/recursive-subdivision-variants/). You can see that it has no internal roads that stretch across the entire map.

![](../../assets/46b610a9804045eb.png)

But Larissa’s talk got me thinking. The whirl pattern is interesting because it cannot be made from simple cuts. What other ways of subdividing a rectangle into smaller rectangles 1, are out there?

I define a rectangular subdivision as **reducible** if there is a strict subset of at least two rectangles that has a rectangular boundary. I.e. a subdivision is reducible if you can swap out a subset of rectangles for a single larger rectangle and get a simpler rectangular subdivision.

You can construct all rectangular subdivisions by applying recursive subdivision then at each step picking a random irreducible subdivision. The irreducible ones are also the most visually interesting, as they don’t have any obvious structure that the eye can pick out.

I then wrote a script 2 to enumerate all irreducible rectangular subdivisions on an integer grid. We only care about integer grids as any other subdivision can be made by “sliding” the horizontal and vertical lines around. I also omit any subdivisions that are equivalent to one on a smaller sized grid.

I’ve dumped the full set of irreducible subdivions (up to size 5×5) to a [json file](https://boristhebrave.com/permanent/25/05/solutions_5_5.json), so you can use them for your own generations. Or explore them here:

## Finding a Random Subdivision

These [two](https://math.stackexchange.com/a/4231794) [posts](https://math.stackexchange.com/questions/1116/number-of-ways-to-partition-a-rectangle-into-n-sub-rectangles) give the bones of a random algorithm. Anyone have the time to figure it out and open source it?