---
title: The requirements of good matchmaking
url: http://joostdevblog.blogspot.com/2017/09/the-requirements-of-good-matchmaking.html
author: Joost van Dongen
published: '2017-09-03'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](http://www.awesomenauts.com/), and have iterated live on each of those, so let's have a look at what we've learned so far!

![](../../assets/e04d002807f8eb3d.jpg)

Matchmaking is such a big and complex topic that I'm going to write a series of posts about it. Today I'm going to kick off this topic by looking at the requirements of "ideal" matchmaking. In future posts I'm going to explore the actual matchmaking implementations we've used and their pros and cons. This will start with the standard matchmaking systems that the big platform manufacturers provide (like Valve, Sony, Microsoft and Sony), followed by an analysis of why we switched away from that and how we built our own. I'm also going to dive into some more controversial topics, like the psychological side of matchmaking and how we managed to massively reduce the percentage of people who leave a match before it finishes.

What defines good matchmaking? This depends on the game of course, but usually the matchmaker will try to achieve most of the following things:

- Low waiting times to get into a match.
- Low ping.
- Match players of similar skill.
- Match premades with premades.
- All players in a match start at the same time.

Many additional requirements are possible, such as:

- Match players who speak the same language.
- Punish bad apples by matching them with each other (for example leavers and griefers).
- Don't get matched with the same people too often.
- Gameplay variation: maybe you don't want to be in the same kind of matchup every time.
- Match players who use voice chat with others who also do so.
- Match based on team composition (if one team has a rare team composition then maybe match them with others who also don't have the standard set of tank/healer/harasser/etc).

It's rarely possible to achieve all of these requirements simultaneously. Even if your game is a big success and 100 people or more search for a match

*every minute*, then some requirements might still not be doable with acceptable waiting times. For example, if you want to match Australians only with other Australians, then waiting times deep in the Australian night will be extremely long for all but the biggest games. What works for a game with a playerbase as large as League Of Legends or Call Of Duty doesn't work for most other games.

![](../../assets/7950e1156b7b886c.jpg)

I've previously written a blogpost about

[how many players you need for quality matchmaking](http://joostdevblog.blogspot.nl/2014/11/why-good-matchmaking-requires-enormous.html)and the short summary is that 1000 concurrent players isn't much from a matchmaking perspective. However, it is for most games: especially indie games are considered a hit if they reach 1000 simultaneous players every day. Even if you're convinced your game will be an indie hit you still need to think long and hard about how to make the matchmaking work with that relatively small playerbase. And this isn't limited to indies either: even a big triple-A multiplayer production like Lawbreakers currently has

[only a few hundred](https://steamdb.info/app/350280/graphs/)simultaneous players.

Because it's usually impossible to achieve all matchmaking goals simultaneously, you need to think about how important each of them is. Especially waiting times suffer when you make other requirements more important. The more requirements you can ignore, the better you can do on the other ones. For example, in Awesomenauts we've chosen to ignore ping with teammates: the matchmaker only looks at ping with enemies. This is because you can't hit your teammates anyway, so if there's more lag there then that will be much less of a problem. In an ideal world we would also want a low ping with teammates, but in practice we can achieve better ping with enemies if we ignore ping with teammates, and thus in our case this is a good choice to make.

One important thing to keep in mind when designing a multiplayer game is that adding more gamemodes often means splitting the playerbase and thus increasing waiting times or reducing matchmaking quality. Think long and hard before adding an additional matchmade game mode!

Reducing the matchmaking requirements isn't the only way to reduce waiting times. For example, if you can design your game in a way that allows for drop-in-drop-out, then players will usually be able to get into a match right away. Or if that's not possible, then maybe if rounds are short enough players can spectate a round while waiting for it to finish and then play in the next one. This doesn't reduce the waiting time, but it does make waiting a lot more enjoyable. I've previously written a blogpost that

[explores a bunch of different approaches](
http://joostdevblog.blogspot.nl/2015/09/designing-matchmaking-for-smaller.html)to designing a game so that multiplayer works with a smaller playerbase.

![](../../assets/94d40fa2ab5ade63.jpg)

Since this series of posts is for a large part based on our own experiences, I will mostly talk about matchmaking for MOBAs. In other words: real-time team-based games where skill is extremely important, where matches take relatively long and where the same players should play a match together from start to finish. In a sense MOBAs are amongst the most demanding games in terms of matchmaking requirements.

It's important to realise that other types of games have different requirements. For example, in shooters skill is often mostly ignored. Instead, teams are reshuffled after every round to balance things out. Shooter players usually also expect to get into a match really quickly, while MOBA players are mostly okay with waiting a couple of minutes for a better match-up. Of course this varies from game to game: not all games in the same genre have the same matchmaking requirements.

In the end the most important thing is to take matchmaking seriously. Think about the requirements of your game and don't assume they are the same as for another game. In some cases you might even have to redesign your multiplayer experience to make matchmaking work, maybe by removing some game modes or adding something for players to do while waiting for matchmaking. Matchmaking can't be an afterthought if your multiplayer experience is to thrive!

How have you dealt with the crappy internet these days in form of CGN (Carrier Grade NAT), that is, people who's ISPs in IPv4 space do NAT again on top of the consumer-grade "router" that most people have? Have you implemented ipv6 support?

ReplyDeleteThanks for your post! Can't wait to read more about Awesomenauts matchmaking


ReplyDeletepotty

This reads like you're saying Awesomenauts has good matchmaking.

ReplyDelete