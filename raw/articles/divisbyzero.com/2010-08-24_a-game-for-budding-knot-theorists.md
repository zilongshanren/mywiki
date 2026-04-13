---
title: A game for budding knot theorists
url: https://divisbyzero.com/2010/08/24/a-game-for-budding-knot-theorists/
author: Dave Richeson
published: '2010-08-24'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

Thanks to [Sam Shah](http://samjshah.com/) for introducing me to this fascinating online game: [Entanglement](http://gopherwoodstudios.com/entanglement/?n=1).

The rules are simple. You are given hexagonal tiles, one at a time, each adorned with six short segments of rope. Use them to construct the longest possible knot (measured in segments) before running into a wall. Entanglement is fun and addicting!![Screen shot 2010-08-24 at 9.43.36 AM](../../assets/8ee999fd291864c8.png)


How high can you go? A quick analysis shows that the highest possible score is 169. How do we come up with that value?![Screen shot 2010-08-24 at 9.07.54 PM](../../assets/4058de7a31ce7659.png)


Each tile has six segments on it—two ends on each side of the hex. There are spaces for 36 hexagons. Thus a full board will have 6*36=216 strands. However, some of these strands will end at a wall. To be precise, there are 48 boundary sides. One of those boundaries is the starting wall (and the ending wall of a “perfect game”). So a perfect game must contain at least 47 unused strands (such as the strand shown above that starts and ends at the central hex). Thus it is impossible to get a score higher than 216-47=169.

Sure, that is a theoretical upper bound. Is it attainable? It turns out that it is! A player named “atomic” got a perfect 169 and [there is a screenshot to prove it](http://blog.gopherwoodstudios.com/2010/06/perfect-score-in-entanglement.html).

Now the only question is, [what knot is that](http://www.math.toronto.edu/~drorbn/KAtlas/Knots/)?

Update: Thank you to commenter “Evan” for pointing out a very similar board game, [Tantrix](http://en.wikipedia.org/wiki/Tantrix), which came out in the late ’80’s. Also, I want to mention [KnoTiles](http://members.cox.net/knotcompendium/KnoTiles.html) which was given to me by my friend [Gene Chase](http://home.messiah.edu/~chase/chase.htm)—also very fun.

Well I can answer the last one: it’s no knot at all. It might be a tangle, though.

Of course you’re right (but I was thinking of them being connected at the center to become a knot).

Looks like a knock-off of Tantrix: http://en.wikipedia.org/wiki/Tantrix

I’ve got the Tantrix Game Pack, which allows for up to four players. It’s quite fun to play with the tiles.

Thanks, Evan. I don’t think I’ve ever seen Tantrix.

which looks like a knock off of http://www.gamepuzzles.com/edgmtch3.htm#KO

which is an older game.

I would say it’s some 13 crossings knot. But there’s hella of them :)

I agree that it seems to have 13 non-trivial crossings. I guess it’s also a composite knot made of three trefoil knots and a few crossings.

The original hexagonal path game was Kaliko, created by Charles Titus and Craige Schensted. In the 1970s, this game was sold by Hallmark under the name, “Psyche-Paths,” in die-cut cardboard. Future Classics, the inventors’ company, recovered the rights to the game and produced Kaliko in clear acrylic until 1987. Since 1991 the game has been licensed to and produced exclusively by Kadon Enterprises, Inc. The acrylic version of Kaliko was replaced by lasercut wood in 2001. Tantrix is a knock-off of Kaliko, with minor changes such as using four colors where each tile has 3 colors. See the Kadon set here: http://www.gamepuzzles.com/edgmtch3.htm#KO — up to four players can play it as a game, and there are countless amazing puzzle designs.