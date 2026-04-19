---
title: When in doubt, break it down
url: https://claire-blackshaw.com/blog/2010/11/when-in-doubt-break-it-down/
author: Claire Blackshaw
published: '2010-11-14'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

![When in doubt, break it down](../../assets/4318849526b2bf6d.jpg)

I can point to countless notebooks some of which date back to some of my first programming experiments in my pre-teen years. One problem which I've never felt happy about are *TILES*.

Now I've always had a bit of a love affair with tiles but also an obsession with clean logic. Sadly tiles require some dirty link ups when working in an animated 2d or 3d world not built out of tiles but instead pixels or some floating point algebra.

Not to mention the issue of *WALLS!!!* Does tile A or B own the wall, or does it exist in wall space. Do you split the wall down the middle? In the case of wall space does the tile extend underneath it?

These all have quick and dirty answers but I don't like working like that. Sadly I've never been called on professionally to look at the tile problem. If I ever had I'm sure the sanity of deadlines and my team would have made the problem almost trivial filled with arbitrary choices.

So yeah the game I've been working on was stuck in limbo for a month while I fought with data formats, and variety of ways of representing the data. Not to mention a bunch of stupid graphic glitches.

## Solution

Bless Sophie and her balance of manic development with apathy. After a coffee and my ranting about the tiles I realised how stupid it was and in one day rewrote it from scratch. In a horrible hacky memory inefficient way. Though my stubborn self and experience found the hacky method worked and then was easily smoothed out. I honestly couldn't tell you if it is the best solution but it is a solution!

For those curious I went with the concept of wall space which overlaps with tiles and belongs to no tile. So it has additionally memory overlap but no convoluted calculations involving bitmasks, or bit shifting.

So hopefully I can move on from here and just place objects in the world and then get some guys running around the room X-Com style.