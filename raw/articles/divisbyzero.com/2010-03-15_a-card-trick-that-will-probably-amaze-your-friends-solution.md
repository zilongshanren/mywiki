---
title: A card trick that will probably amaze your friends (solution)
url: https://divisbyzero.com/2010/03/15/a-card-trick-solution/
author: Dave Richeson
published: '2010-03-15'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

Warning! Spoiler alert! This post contains the secret behind [the card trick that I described in my last post](https://divisbyzero.com/2010/03/15/a-card-trick-that-will-probably-amaze-your-friends/). Read that post before reading this one.

First the bad news: this card trick is not fool-proof; it is a probabilistic card trick. The good news is that in my experience, it has a high probability of success. I can’t be more specific than that. If anyone wants to run a [Monte Carlo simulation](http://en.wikipedia.org/wiki/Monte_Carlo_method), I’d be happy to hear how often the trick fails.

The secret to this card trick is that **you play along just like your friend is**, but you use the first upturned card as your key card. She is silently counting and so are you. In the example shown below, her key cards have ovals on them and your key cards have rectangles on them.

As you can see, at first you and she have different key cards, but, **and here’s the essential point**, once you both land on the same card, you will have the same key cards from then onward. Thus, all you have to do is wait until you get near the end of the deck and stop on one of your key cards. If you are lucky, the two of you will be in sync by then and the trick will be a success.

In the example shown above you’re in sync when the seven of diamonds is dealt—the 31st card.

Note: in practice this card trick is quite successful. I played around with [Random.org](http://www.random.org/playing-cards/) for a little while and was unable to find a shuffling that failed. One shuffling didn’t sync up until the second-to-last card though! Quite a few of the shufflings synced in the first or second row. Twice the first card was an ace, so they were in sync right from the beginning.

As I said in my last post, I do not know who to credit for this card trick. If you know, please post it in the comments.

The rules of the original card trick were slightly different than those I presented here. The face cards counted as 10’s. This is fine, but it decreases the probability of success, so I chose to spell the names of the face cards. Also, rather than having the other player draw a card at the start, she or he could mentally pick a card some time during the deal and start counting then. Again, this decreases the chances of success.

[Update: Thanks to John Allen Paulos who [quickly responded on Twitter](http://twitter.com/JohnAllenPaulos/status/10527847994). He said that this trick is called the Kruskal count. He wrote about it in his 1998 book * Once Upon a Number—The Hidden Mathematical Logic of Stories *(he also proposes a biblical hoax that uses this trick). You can also read about the Kruskal count in Ivars Peterson’s December 24, 2001

*MathTrek*article

[Guessing Cards](http://www.maa.org/mathland/mathtrek_12_24_01.html). In his article he points to the article “

[The Kruskal Count](http://arxiv.org/abs/math/0110143),” by Jeffrey C. Lagarias, Eric Rains, Robert J. Vanderbei in which they look at the probabilities of success for various face card values. Finally,

[here’s a nice applet](http://faculty.uml.edu/rmontenegro/research/kruskal_count/kruskal.html)illustrating the Kruskal count (taking face cards to be 5’s).]

Sounds like an application of Markov chains.

Very cool trick, and I love the word play in the title. I’m seeing an 87% success rate in a Monte Carlo simulator. I’m going to try and break it down a little further to see how the success rate grows as you progress through the deck.

Bill, thanks for letting me know about the success rate! That’s pretty good, but not perfect.

However, as @GMichaelGuy said on twitter: “this trick is nice. And when it doesn’t work, you can certainly convince the other person they messed up!”

Dropping the face cards to 1’s would help even more.