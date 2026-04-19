---
title: runevision blog
url: https://blog.runevision.com/2011_12_23_archive.html
published: '2011-12-23'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

So my ant colony bot is doing rather well in the final AI Challenge tournament. It's ranked around [between 4 and 11](http://aichallenge.org/profile.php?user=9661) depending on when you look.

Reading about some of the strategies used by other bots, I'm surprised mine has performed so well, since it's not really that sophisticated. Well, I'm releasing the source code here. This is in the same state as when I submitted it without further cleanup, so not the most tidy code but not a complete mess either.

Note that the bot behaves completely different depending on whether it's compiled as a DEBUG or a RELEASE build. As a debug build it will look for a file called parameters.txt describing parameters to use for various constants in the code and when executed multiple times it will run with those parameters having different values and keep track of statistics of which parameter values work best. More about that later. As a release build the constants are hard-coded in the code and that's what is used in the actual competition.

The bot have these primary functions:

- Combat logic to evaluate each of 5 possible moves (4 directions plus staying) for each ant. Afterwards each ant has a score for each move.
- Path-finding done using "flood-filling" / breadth-first search from the goal locations. Afterwards each ant has an assigned goal and know which direction to move in to get there.
- Goal handling. This basically adds extra points to one or more of the 5 move scores based on the direction obtained from the path-finding.
- Moves resolution. This resolves which ant has the right to move into which position based roughly on "who needs it the most".

### Path-Finding

The first thing I implemented was path-finding. This was originally done using a [flood-fill / breadth-first search](http://en.wikipedia.org/wiki/Flood_fill) from the goal locations. The default path-finding algorithm choice for computer games is A* but it's not useful for being reused by many agents which is why I used the flood-fill instead. It might also be the same or similar to what is called [collaborative diffusion](http://scalablegamedesign.cs.colorado.edu/wiki/Collaborative_Diffusion) - not entirely sure about that; I only heard about that term after I had implemented my solution.

Initially I simply used a queue for the search. I later switched to a [priority queue](http://en.wikipedia.org/wiki/Priority_queue) so I could us various cost functions for the path-finding. For example, by giving positions occupied by my own ants a higher cost, ant behind them will prefer to go around them instead of just being stuck.

I also implemented support for specifying for a goal the maximum number of ants assigned to it, the maximum distance to search out from the goal, and an initial cost (which gives the goal lower overall priority).

The goals I ended up using are:

- Defense positions around my own hills (1 ant each, no cost, max dist 30)
- Enemy hills (a third of all my ants divided by number of known enemy hills, no cost, no max dist)
- Food (1 ant each, cost equal to 4 dist, no max dist)
- Explore (1 ant for each explore position, cost equal to 25 dist, no max dist)
- Enemy ants (20 ants each, cost equal to 42 dist, max dist 13)

The defense positions are positions immediately around my own hills. 12% of my ants are assigned to defense, divided between my hills if more than one.

Any unassigned ants are assigned to enemy hills as well.

*This post is ending up much longer than I thought so I'm splitting it up. Read on in part II about goal handling and moves resolution.*