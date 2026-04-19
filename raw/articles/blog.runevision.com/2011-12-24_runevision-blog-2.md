---
title: runevision blog
url: https://blog.runevision.com/2011/12/
published: '2011-12-24'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

What do you know, it looks like I got 4th place in the AI Challenge!

I began writing an explanation of my bot and you can read [Part I here](http://blog.runevision.com/2011/12/ai-challenge-my-bot-explained-part-i.html) as well as downloading the source code. Right now is holiday time with the family; I'll write up the remainder afterwards. :)


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


The final tournament has begun. Here's some interesting battles [my bot](http://aichallenge.org/profile.php?user=9661) has been in that I've captured on video.

My 5th game where my bot annihilates 8 opponents in an epic battle!

My 6th game where my opponent just won't die (or my massive army is not quite aggressive enough). Also: Dancing!


For the past - hmm, almost 2 months now - I've taken a break from my other hobbies and let myself become distracted by Google's [AI Challenge](http://aichallenge.org) - an Artificial Intelligence (AI) programming contest.

Not for much longer though since the final submission deadline is in 10 hours at the time of writing.

When I [wrote about it a months ago](http://blog.runevision.com/2011/11/ant-colony-google-ai-challenge.html) I'd only been at it for a few weeks but [my bot](http://aichallenge.org/profile.php?user=9661) was already ranked 39th in the world out of 10000+.

Since then I've made a lot of improvements - but so have the other contestants, so the overall level has continuously risen.

Whenever a new version of a bot is uploaded to the content servers, the skill and rank is completely reset, so the bot will have to fight its way all the way back up from the bottom. That can take a few days to a week depending on how high a ranking it can get before it's stabilized.

I last uploaded a bot four days ago. It has gotten up to rank 22 in the world; my highest ranking yet. It's also the top ranked bot in Denmark by a large margin and the 3rd ranked bot written in C#.

When working on improving the bot, it's usually hard to know if some new idea will actually improve the bot or just make it worse without having tested it first. I usually test by running a game with the new version against the old version. However, most changes only make a small difference that will only slightly increase the bot's chances of winning, so it has to be in many games before it's clear if it's better or not. Did it win 4 out of 6 games? Might just be a coincidence due to random luck.

You can see it quickly becomes tiresome to test these things manually. That's why I programmed a simple framework to automatically run many games in a row between the various version of the bot and gather statistics on which versions win the most times. I've often let this run overnight so I have statistics from hundreds of games the next day.

Sometimes, however - sometimes an idea turns out to be a significant improvement. By significant I mean that the new version consistently beat the previous version - as in 10 out of 10 times. Those times when I've managed to make such an improvement have been the most satisfying moments of this competition.

The most interesting improvements have all been related to how the ants handle combat. The way [battle resolution](http://aichallenge.org/specification.php#Battle-Resolution) works in the game follows simple rules but has complex consequences and my understanding of it has increased in stages.

The combat is basically about ants being in majority winning over ants that are in minority. If one red ant is within combat range of one white ant, they both die. But if one red ant is within combat range of two white ants, only the red ant die and both of the white ants survive.

Initially I thought combat was a matter of being cautious. Only move into combat range if you have more ants you can move within range than the opponent has. But it's not that simple. There's various potential outcomes to consider and also an element of gamble. I might write some more about it after the competition has ended if not somebody higher ranking does it first. Not that I'm an expert by any count - I feel like I've only scratched the surface.

Anyway, since I uploaded that last bot four days ago I've made several significant improvements in the combat skillz of my bot, meaning that the newest version I have here totally and consistently kicks the ass of that version I uploaded four days ago. Now I've just uploaded this new version. It will probably be the last unless I get some last-minute epiphany which is not likely by now.

We'll see how it performs in the final tournament.