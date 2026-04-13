---
title: How we solved the infamous sliding bug
url: http://joostdevblog.blogspot.com/2014/04/the-infamous-sliding-bug.html
author: Joost van Dongen
published: '2014-04-05'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](http://www.awesomenauts.com), one that had been in the game for very long: the infamous "sliding bug". This bug is a great example of the complexities of spreading game simulation over several computers in a peer-to-peer multiplayer game like Awesomenauts. The solution we finally managed to come up with is also a good example of how very incorrect workarounds can actually be a really good solution to a complex problem. This is often the case in game development: it hardly ever matters whether something is actually correct. What matters is that the gameplay feels good and that the result is convincing to the player. Smoke and mirrors often work much better in games than 'realism' and 'correctness'.

Whenever the sliding bug happened, two characters became locked to each other and started sliding through the level really quickly. With higher lag, they usually kept sliding until they hit a wall. I have recorded a couple of mild examples of this bug, where the sliding stops quite quickly but still clearly happens.

*Note the weird way in which the collision between Froggy and the worms happens.*

To understand why this bug happened, I first need to explain some basics of our network structure. Awesomenauts is a purely peer-to-peer game. This means that the simulation of the game is spread out over all the players in the game: every computer is responsible for calculating part of the gameplay. Particularly, each player manages his own character. The result is that character control is super fast: your computer can execute button presses immediately and there is no lag involved in your own controls, since there is no server which has final say over your own character. Of course, lag is still an issue in interactions with other characters that are managed on other computers.

Spreading out the simulation like this is simple enough, until you starting looking at collisions. How to handle when two characters bump into each other? Luckily Awesomenauts does not feature real physics, which would have made this even more complex. Our solution is simply that each character solves

*only*his own collisions. So if two players bump into each other, they solve only their own collision (in other words: they move back a bit to make sure they don't collide anymore). They don't interfere with the other character's position at all. This works pretty well and is very easy to build, but it does become difficult to control the exact feel of pushing a character, since lag is part of that equation.

![](../../assets/74d9442eb5a8c8b8.jpg)

This works because normally both players will try to resolve their collision in the opposite direction: the character to the right will move to the right and the character to the left will move to the left, thus moving them away from each other.

Which brings us back to the sliding bug. This bug happens when the computers disagree on who is standing to the right and who is standing to the left. If both computers think their player is standing to the right, then they will both try to resolve the collision by moving to the right. However, since they both move in the same direction the collision is not actually solved, so they keep sliding together until they hit a wall.

![](../../assets/8e98528ad108e561.jpg)

It is clear how this would cause sliding, but why would the computers disagree on who is standing to the right? This requires both lag and a relatively rare combination of timing and positioning. This is a difficult one to explain, so I'll first explain it in words and then in a scheme. I hope the combination makes it clear what is happening.

Let's look at the situation when two players are both moving to the right. Lonestar is in front and Froggy is behind. Froggy is moving faster, so Froggy is catching up with Lonestar. Now Froggy jumps and lands on top of Lonestar. Because of lag, the jumping Froggy sees a version of Lonestar that is slightly in the past. Since Lonestar is moving to the right, his past version is still a bit more to the left. The resulting positioning is such that Froggy thinks he is further to the right than Lonestar, so Froggy starts resolving his own collision to the right. Lonestar on the other hand sees a past version of Froggy (again because of lag) and thinks he himself is to the right. The lag makes both Froggy and Lonestar think they are on the right side.

![](../../assets/e14909900b802dfd.jpg)

We originally thought this would be a very rare bug, but in practice it turns out that it happened often enough that most Awesomenauts players encountered it occasionally. In fact, there was one top player who was able to aim Froggy's Dash so well that he could trigger this bug almost every time. He used it to attach his opponents to him to do maximum damage with the Tornado after the Dash. Impressive skills! Gameplay mechanics that are so difficult to time are cool because they raise the skill ceiling in a game, but it was a bug so we did want to squash it.

Since we thought it was rare and since we couldn't think of an obvious solution, we first ignored the bug for quite a while, until a couple of months ago I managed to finally come up with an elegant solution. Or at least, so I thought...

The solution I came up with was to turn off collision handling for one of the players whenever the sliding bug occurs. This way they stop sliding together, and the character who still handles collisions will resolve the collision for both of them by moving himself a bit further than he normally would. The collision is only turned off between these two characters and only for a short amount of time.

This requires knowing when the bug is happening, which is not obvious because the bug is happening on two different computers over the internet. To detect occurrences of the bug we added a new network message that is sent whenever two players collide. The player with the lowest objectID sends a message to indicate which side he believes he is on. This is a very simple message, simply saying "

*I am Froggy, I am colliding with Lonestar and I think I am to his right*". Lonestar receives this message and if it turns out to be inconsistent with what he thinks is happening, then Lonestar turns off his own collision handling and lets Froggy resolve the collision on his own.

![](../../assets/2e0e37545b569597.jpg)

This is simple enough to build and indeed solves the basic version of the sliding bug, but it turned out to feel pretty broken. There are two reasons for this. The first is that in the above situation, if often happens that a character starts resolving his collision in one direction, and then in the other direction. This felt very glitchy, as the character moved in one direction for a bunch of frames and then suddenly moves in the other direction.

The second and bigger problem is that our collision resolving is done at a relatively low speed. We do this deliberately, because this way when you jump on top of a character, it feels like you slide off of him, instead of instantly being pushed aside. This is a gameplay choice that makes the controls feel good. However, this means that collision resolving is not faster than normal walking, so it is possible for Lonestar to keep walking in the same direction as in which Froggy is resolving the collision. This way the collision is never resolved and Froggy keeps sliding without having control. This may sound like a rare situation, but in practice player behaviour turned out to cause this quite often, making this solution not good enough.

![](../../assets/12386ed039bbe7aa.jpg)

Seeing that this didn't work, I came up with a new solution, which is even simpler: whenever the sliding bug happens,

*both*characters turn off their collision, and it is not turned on again until they don't collide any more. In other words: we don't resolve the collision at all!

This sounds really broken, but it turns out that this works wonders in the game: players rarely stand still when that close to an enemy, so they pretty much instantly jump or walk away anyway. In theory they could keep standing in the same spot and notice that the collision is not resolved, but this hardly every happens. Moreover, even if it does happen, it is not that much of a problem: teammates can also stand in the same spot, so two enemies standing in the same spot does not look all that broken.

![](../../assets/a8e8156f2f634b09.jpg)

This solution has been live on Steam for over a month now and as far as we know, it is working really well.

As you might have noticed, this has been a pretty long and complex blogpost. The sliding bug is just one tiny part of network programming, so I hope this makes it clear how complex multiplayer programming really is. There are hundreds upon hundreds of topics at least as difficult as this one that all need to be solved to make a fast-paced action MOBA like Awesomenauts. Also, this solution is a very nice example of something that seems really wrong and way too simple from a programming standpoint, but turns out to work excellently when actually playing the game.

That's a great work around, Joost, I love it :D, This bug has always bothered me a bit (although sometimes I exploited it to quickly escape from dangerous situations in Ribbit's jungle), and this isn't the only game to have it. I remember that once I was playing NFSW (also peer-to-peer) with my brother (team escape) and he got trapped between a bunch of cops, and as I was behind him I tried to crash on his back so he's sent out of the situation. And I did, I hit him right on the back but he didn't move at all, and on his screen, I missed him, went by his side, crashed with a cop right in front of him and I was there parked in front of him. And then we suddenly began going backwards, in my screen he was going backwards pushing me and on his I was going backwards pushing him, so we began flying in the opposite direction of the race and through all the cops behind at an impossible speed (while in reverse). Although it's very rare, I'm very glad that you could solve it :D

ReplyDeleteAwesome! Thanks for the insight. I always wondered why that bug happened.

ReplyDeleteWow, it's funny how not acting to it fixes it!

ReplyDeleteYour first solution would also be more problematic in case of 3 or more characters interacting in collision.



ReplyDeleteFurthermore, for some situations like collision and other situations that require authorization it might be useful to use a super peer. For instance the client with the lowest IP or objectID. And so, not have the other characters do any kind of collision solving between characters at all. So your game is still p2p but has a 'server' for some authoritative situations.

The solution you use now is prettier though, i like it.

Why not have the collision be resolved by an arbitrator: a third player. Presumably, location information is transmitted to other players as well, so if Froggy and Lonestar collide, then the other players will see that collision and Lonestar's and Froggy's positions from a neutral perspective. The other clients then send instructions to Lonestar and Froggy based on their perspective of the situation; one might send, " Froggy moves left and Lonestar moves right."


ReplyDeleteHow you decide who the ultimate arbitrator is might take a little more thought. You could have all other clients send a solution and the most common solution is the one you apply. You could also have the other clients also send their measured latency to Lonestar and Froggy and the solution that is most evenly distanced between Lonestar and Froggy gets chosen under the assumption that their perspective is the most neutral. You might also do something where one client is assigned as an arbitrator for each pair of players based on some criteria and they just keep an eye out for any collisions between those two players and then they alone send down the resolution instructions.

That doesn't work when there are only two players in a match, so that would mean having two different ways of handling collision depending on how many players are in the match...

DeleteWait... so the chosen solution was... don't have collision between players?


ReplyDeleteWhat was the design reason in the beginning to have collision between players?

No, only in this very particular rare situation. In all other situations collision is still there.

DeleteBut again, what happens when you turn collision completely off all the time? I didn't play the game yet but if I can go into an enemy in one situation, isn't it better that I can go into them all the time?

DeleteWe tried various collision rules early in development and not colliding at all felt really bad. There are also a lot of tactics in Awesomenauts with body blocking, so there is a lot of gameplay in collisions.


DeleteKeep in mind that the sliding bug fix only turns off collision in an extremely rare situation. In practical gameplay all collisions work fine.

but in the other hand , your final solution makes the game that

ReplyDeleteplayer can't use their "body" to stop emeny's moving

so , is there any more prefect solution？

It only does so in a very specific rare situation, and only if you land on top of someone. If you land on top of someone, then the bodyblock has already failed anyway, so it does not really matter for that.

DeleteI have never played a MOBA that suffers this bad from latency. Is it due to Awesomenauts being a platformer with direct imput?



ReplyDeleteAfter 200 hrs me and my friends are at the point of leaving the game. Why does the host experience lag? The displayed latency ingame is not even close to the real latency. 200ms on a player that is able to kill you with an effective latency of 1 or 2 seconds.

Sorry for being kind of offtopic. ;)

I will check your blog for some more articles about the actual netcode of awesomenauts to really understand why the current state is this bad.

Apart from these issues, great game! :)