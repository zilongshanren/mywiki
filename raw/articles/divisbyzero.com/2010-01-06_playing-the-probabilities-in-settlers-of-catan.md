---
title: Playing the probabilities in Settlers of Catan
url: https://divisbyzero.com/2010/01/06/playing-the-probabilities-in-settlers-of-catan/
author: Dave Richeson
published: '2010-01-06'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

One of my favorite board games is [Settlers of Catan](http://en.wikipedia.org/wiki/Settlers_of_Catan). I encourage all of you to check it out. It is a great game because it is a combination of luck and strategy and it is different each time you play. I’ve been on a big Settlers kick lately, because I’ve downloaded a version for my iPod Touch.

This post will probably be interesting only to those people who know the rules to the game (sorry), but I will give a brief explanation of the relavant rules so that anyone can follow the discussion.

A couple of years ago I asked myself the following two questions about Settlers of Catan.

- What are the most valuable intersections? This information is most important to know at the beginning of the game when placing the first two settlements.
- Where should I place the robber to do the most damage?

I just found my notes that I wrote, so I thought I’d share them here. The mathematical analysis is extremely simple, but is kind of fun and maybe a little useful to know.

**The most valuable corners**

At the start of the game the hexagonal game pieces are put in place randomly (as shown in the picture above, which you can click on to enlarge) and the round chips are distributed according the the rules. Each chip has a number 2 through 12 (except 7) on it. The players take turns placing settlements on the corners where three hexagons meet. Once each player has two settlements, play begins.

During each person’s turn a pair of dice are rolled and anyone with a settlement adjacent to a hex with that number on it gets a resource card of that type. If the player has upgraded a settlement to a city and it is adjacent to the hex, he or she gets 2 resource cards. For now I’ll ignore what happens when a 7 is rolled.

Thus it is good to put your settlement next to a 6 or an 8, 5 and 9 are good too, however the hexes with 2’s and 12’s are not worth much. You may put your settlement along the coastline or the desert, but the downside is that it would be adjacent to only 1 or 2 resource hexes.

The round chips not only have numbers, they also have dots on them. The dots give you an easy way to determine which are the valuable hexes. They are assigned as follows:

•: 2, 12

••: 3, 11

•••: 4, 10

••••: 5, 9

•••••: 6, 8

My question is: how do we look at a board and determine the most valuable intersections? By valuable I mean greatest likelihood of yielding a resource card when the dice is rolled. I’m ignoring the other strategies: settling on ports, spreading out your settlements, getting a broad range of resources, etc.

I was surprised to discover that the simple answer is the correct answer: **add up the dots on the adjacent hexes. The intersection with the largest dot-sum is the most valuable.**

The reason this is true is that if a chip has n dots, then the chance of rolling the number on that chip is precisely n/36. For example, there are 3 ways to roll a 10 (4 & 6, 5 & 5, or 6 & 4) and there are 36 possible rolls, thus the chance of rolling a 10 is 3/ 36. Indeed, the 10 chip has 3 dots on it.

Now suppose your settlement is on a 6/4/11 intersection (which corresponds to dots •••••/•••/••, or as I will write from here onward, 5-3-2). Then the chance that this settlement will pay off is .


Before answering the question I must point out that some combinations are impossible. You can’t have two adjacent hexes with the same (dice roll) number on them. You can’t have two adjacent •••••’s (or two adjacent •’s). You cannot have three adjacent hexes with the same number of dots. Thus, here are the most valuable intersections (of course, depending on how the board is set up, not all of these configurations may exist).

Probability 13/36: 5-4-4

Probability 12/36 5-4-3

Probability 11/36: 5-4-2, 5-3-3, 4-4-3

Probability 10/36: 5-4-1, 5-3-2, 4-4-2, 4-3-3

Probability 9/36: 5-3-1, 4-4-1, 4-3-2, 5-4 (on the coast or desert)

One consequence of this analysis is that you should not feel obliged to place every settlement adjacent to a 6 or an 8. There may more valuable corners elsewhere. For example, looking at the intersections in foreground of the picture above, the 8/5/10 and 8/5/4 (5-4-3) corners are the best, the 5/9/10 (4-4-3) is next best, and the 8/4/3 (5-3-2) comes after that.

**The best use of the robber**

The little black guy in the picture above is the robber (or bandit). He temporarily kills any tile upon which he sits (rolling a 7 allows you to move the robber). Obviously, you want to place it on a hex that has none of your settlements or cities and does as much damage to your opponents as possible.

It is important to note that properties (settlements and cities) cannot be placed on adjacent intersections, so you can have at most 3 on each hex.

My question is: where should you put the robber to do maximum damage to the other players? Again, I’m simplifying the analysis. Often you want to harm one player more than another because he or she is about to win—I’ll ignore that.

By the expected damage I mean the expected number of resource cards “lost” when the dice are rolled. For example if there are two settlements and one city on an 8-hex and an 8 is rolled, the other players will not get the 4 resource cards (1+1+2) they would have gotten had the robber not been present. Since the probability of rolling an 8 is 5/36, the expected number of lost resource cards by placing the bandit on the 8 is 4(5/36)=20/36.

It is easy to create a table of expected damages. The values at the top of each column of the table are the number of settlements plus twice the number of cities on the hex (the number of resource cards that would be distributed if that number was rolled). Each entry in the table is the expected damage (in 36ths)—so the larger the number, the greater the damage.

| 1 | 2 | 3 | 4 | 5 | 6 | |
| • | 1 | 2 | 3 | 4 | 5 | 6 |
| •• | 2 | 4 | 6 | 8 | 10 | 12 |
| ••• | 3 | 6 | 9 | 12 | 15 | 18 |
| •••• | 4 | 8 | 12 | 16 | 20 | 24 |
| ••••• | 5 | 10 | 15 | 20 | 25 | 30 |

In short: **to compute the expected damage, add the number of settlements to twice the number of cities, then multiply this by the number of dots on the hex.**

For example, a 6-hex (•••••) with three settlements has a lower expected damage (15/36) than a 9-hex (••••) with 2 settlements and a city (16/36).

[Image by [xingty](http://www.flickr.com/photos/xingty/) ([CC BY-NC-SA 2.0](http://creativecommons.org/licenses/by-nc-sa/2.0/))]

Um, there should be some value for getting the dots on the right resource. Tons of sheep aren’t nearly as useful as tons of bricks and wood.

Very cool. I’m a professional game inventor, and I love to see simple math analysis of games. Also a fan of Settlers of Catan, especially Settlers of the Stone Age.

I was hoping for something a little more sophisticated than “count the dots” — such as calculating the likelihood of drawing certain resources over a round, or showing the chances of drawing the robber in a round (depending on the number of players).

Also, maximizing the # of cards is not always the best strategy. Resource distribution also matters.

Mm. Cheap first pass of the problem.

There’s a second part – protecting yourself against “runs of bad luck” by getting good total number coverage.

It can be a lot more important in Catan to get something on as many dice rolls as possible, than to get more things “on average”.

If you have at least one settlement on every number, you get something every roll that isn’t seven.

This matters, and can matter more than simply maximising your dot count.

The other angle is getting good resource coverage – and for deeper into it, getting good resource coverage of the right type when you actually need it. Brick/Wood early on are crucial, but ore/wheat/sheep become more critical as time goes on.

Then there’s trading to mess it up even further…

The game is a whole lot more complex than your simple dot count analysis above. :-)

Wow, how long did it take you to figure this one out? They pretty much talk about this in the basic rules of the game… just they figured out a way to shorten it.

PROBABILITY

When rolling two dice, the probability of rolling certain numbers is greater than others. Since there are 6 ways to roll a “7” (1+6, 6+1, 2+5, 5+2, 4+3, 3+4) and only 1 way to roll a “12” (6+6) or a “2” (1+1), 7 comes up much more often than 12 or 2. The size of the number on the counters in the game represents this probability; the larger numbers are more likely to be rolled. The probabilities are listed here:

“2” & “12” 3%

“3” & “11” 6%

“4” & “10” 8%

“5” & “9” 11%

“6” & “8” 14%

“7” 17%

What I just put above can be found in the basic rule book for the game.

very cool analysis… thanks!

All of your points are correct, but in my defense, I said the very same things that you did in the body of my post.

1) the mathematical analysis used

elementarytechniques in probability.2) There are almost always other things that we want to consider beyond these probabilistic facts.

(And I don’t know if I’ve ever read the instructions, so they may say these same things there.)

Thanks for reading.

It’s a good mathematical break down, but I think it failed to address the value of resources.

Ore is the most valuable resource in the game (because it’s the most scare and most in demand).

Wheat is the second most valuable (because it’s the most in demand).

So if an intersection has Wheat, Ore, Ore on 4, 9, 10, it may actually be a better spot than a Wool, Wood, Wood, on 5, 6, 8.

Try trading sheep late in the game and you’ll quickly see why it’s the least valuable resource in the game.

Very interesting blog…

Catan is a race to 10 pts and therefore it’s worth considering the shortest resource path from 2 to 10 victory points. Of course, the sequence of resource accumulation, destruction and consumption ultimately determines the victor, but a fundamental understanding of the math behind minimum resource paths is very helpful.

Others should confirm my math, but I believe there are 63 unique combinations of settlements, cities, and development cards that give exactly 10 VPs. Of these, only 11 do not require at least one Victory Point Card; these are a combination of between [1-4] cities, [0,2,4] settlements, and [none, either, both] of the longest road and largest army.

The absolute least cost solution requires 33 resources to build and consists of 3 cities and both the longest road (5) and largest army (3). At a minimum this takes wood, brick, sheep, wheat and ore of {5,5,4,7,12} respectively; or a ratio that is roughly satisfied by placing cities such that each city bordered a tile with dots of {4, 4, 3, 4+2 or 3+3, and 5+5}. In other words, to win quickly (other gameplay elements notwithstanding) players should strive to build on both a 6 and 8 that’s ore, a combination of at least 2 builds of 3,4,5,9,10,11 that are wheat, a 5 or 9 for logs and brick, and a 4 or 10 that’s sheep.

Of course, the game almost never allows such a build scenario.

Interestingly, the greatest 10 VP solution requires at least 42 resources and consists of 4 settlements, 3 cities but neither the longest road nor the largest army. To build this requires a supply of {10,10,5,8,9} resources, roughly akin to settlement/city placement such that wood, brick, wheat and ore are well balanced and sheep is half as likely as the others.

One final point…all winning scenarios require diverse and balanced resource accumulation. Whenever possible, go for balance rather than dots because trading is (usually) a very costly activity and it is extremely hard to recover from 4:1 (or even 2:1) exchange rates.

I’d be happy to post additional comments about the math I’ve derived or answer specific questions if there is interest.

We had a big debate on whether dividing up the development cards into two piles and all players picking randomly from two piles (vs one pile like the rules say) will change the outcome of the game? And how much difference it would make, if any? What do you think about this?

No difference between two piles of cards and one pile of cards, assuming the pile of cards is properly shuffled. To take it to an extreme, spread all the cards out so there is only one card per pile. Randomly choose one of those cards, is the same as picking the top card from a properly shuffled pile.

The fly in the ointment is “properly shuffled”. :-) 7 reasonably good (not *too* good, perfect shuffling defeats the randomness!) riffle shuffles to get proper random ordering.

If players always pick from the same pile (e.g. the one nearest them), then it doesn’t matter at all, provided you follow the same exhaustion rules as for one pile (i.e., if you exhaust one of the two piles, you split the remaining cards so you have two piles again without re-using the discard piles).

I just stumbled upon this, and it’s nice to see other people taking a crack at analyzing this game. I recently finished a project where I mathematically analyzed Catan, and am still playing with some of the consequences that I found. Overall, this game is a mathematician’s and economist’s delight!