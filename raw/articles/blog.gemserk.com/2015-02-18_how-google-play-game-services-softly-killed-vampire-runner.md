---
title: How Google Play Game Services softly killed Vampire Runner
url: https://blog.gemserk.com/2015/02/18/how-google-play-game-services-softly-killed-vampire-runner/
published: '2015-02-18'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

We want to talk a bit about how we migrated from our custom [highscores](https://github.com/gemserk/highscores-server) system to use Google Play Game Services (GPGS) Leaderboards for Vampire Runner and the consequences of that change.

Before GPGS was released, we worked on our custom solution for highscores for Vampire Runner. That solution consisted in having scores for multiple time intervals (daily, weekly, monthly and all times scores) and letting guest users play and make scores without the need to log in. You could play the game, make scores and then, if you thought your scores were good, link those scores with your name, really simple and easy, it worked fine.

That custom solution was running on an amazon server and costed about 15 USD/month and since the game was making around that money with the ads, we thought it was acceptable.

A while after GPGS was released, we thought, why maintain and pay money for our own server when we can use GPGS instead? It was very logic, they have some of the features we had on our system and everybody was starting to use it. Also, we trust Google, so we changed Vampire Runner to use GPGS.

However, some time after we changed Vampire Runner, we started to see an important decrease in the number of people playing the game. The problem was something we were aware of but we thought it wouldn’t be so significant. We had a lot of players that didn’t have a Google account or even Google Play (they probably downloaded the game from other store), and they couldn’t log in to compete with other players so the game was less interesting for them since part of our game is based on that, competing to be better than other players.

The truth is the game is not a good game by itself and the main thing that kept our players was being able to compete with others (for a while at least), now that we are forcing them to log in they feel it isn’t worth it so they just go away or they play without logging in, hence without making scores.

### Conclusion

We don’t think Google Play Game Services is the bad guy here but it is not good if you want to capture users from outside Google, same example would apply if we had forced Facebook or Twitter accounts. So if you have a game where you need players to catch other players, consider that. Of course, if you have a great game maybe with only Facebook, Google or Twitter you could keep your game alive but if you consider the three of them, you will get more players. In our case, we had all the world and then we restricted our game to only G+ accounts and that is why we lost players.

That was part of the story of the dying Vampire Runner, hope you like it.