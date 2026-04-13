---
title: Designing matchmaking for non-gigantic communities
url: http://joostdevblog.blogspot.com/2015/09/designing-matchmaking-for-smaller.html
author: Joost van Dongen
published: '2015-09-06'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[recently explained](http://joostdevblog.blogspot.nl/2015/08/why-adding-multiplayer-makes-game.html). The vast majority of online multiplayer games ever made isn't playable any more because of this. Partially this is because not all games can be a success, but there is a much more important reason: often the matchmaking is poorly designed for a smaller playerbase. With clever choices multiplayer can flourish even with a tiny community.

For an average indie game that is doing okay but isn't a big hit it is pretty decent to have 40 simultaneous players a few weeks after launch. Our own game

[Awesomenauts](http://www.awesomenauts.com)did really well so our daily peak is usually above 1000 players, but expecting such numbers is unrealistic for most games.

Let's consider a four player multiplayer game that has three game modes. We press the quickmatch button and the game starts looking for opponents. If a match takes on average 30 minutes and there are 40 simultaneous players then a player starts looking for a match once every 45 seconds. Since there are three game modes your mode will have one player searching once every 135 seconds. Waiting for a complete match of four players then takes almost 7 minutes.

Seven minutes! Few players are willing to look at a "Searching" screen for that long, so most will just quit and play something else. If a player concludes your game is dead he probably won't try again later and is lost forever. Whatever playerbase you had will quickly disappear. So many multiplayer games die because there aren't enough players for a good experience.

However, with clever design choices this fate can be averted. 40 simultaneous players would have been plenty for a good experience if matchmaking had been designed in a different way.

![](../../assets/9e7d2d1fb2a7b255.jpg)

**Reduce game modes**

Game modes split the community. If half of your players wants to play Domination while the other half wants to play Deathmatch, then they all have only half as many opponents to play with. In the example above removing two game modes would have reduced the waiting time to 2:15 minutes, which might already have done the trick. Even the gigantonormous League of Legends has removed less popular game modes because there weren't enough players for a good experience.

For exactly this reason Awesomenauts has only one core game mode. There is a custom game option where users can set up all kinds of weird game modes, but these aren't part of the core matchmaking and thus only playable through friend invites. This way there are extra options for players who want them, but there is only one core mode and it has plenty of players to matchmake with. (For a more detailed analysis of player spread, check my blogpost on

[why good matchmaking requires enormous player counts](http://joostdevblog.blogspot.nl/2014/11/why-good-matchmaking-requires-enormous.html).)

If you really want to have more game modes, you can also choose to force players to play whatever is available. Maybe players can select a preferred game mode and the matchmaker looks at all the preferences and tries to find the best match-up. If there aren't enough players in your favourite game mode, then you just play a different game mode. The downside of this approach is that players would probably complain a lot that they aren't put in their favourite game mode. Not having an option at all might in some cases feel better than having an option that you can't actually play...

**Allow solo play while waiting**

The above approach tries to reduce the waiting times. An alternative is to make waiting more fun so that players are willing to wait longer. In our 2010 game

[Swords & Soldiers](http://www.swordsandsoldiers.com)we allow players to play

*all*single player content while waiting for an opponent. If you start the matchmaker a little icon appears in a corner of the screen and you can just play some skirmish against the computer until another human becomes available to play with. This works wonders: players are willing to wait much longer, increasing the chance they actually find an opponent.

This can be improved further by having content that is fun to play repeatedly. A story campaign isn't so much fun to play every time while waiting, but a highscore mode is. In Swords & Soldiers I usually played the endless Survival mode while waiting. Of course it sucks to be thrown out of your highscore run because an opponent is found, so our solution was to auto-save the solo match when starting a multiplayer match. You can continue your single player challenge after the multiplayer has ended.

A while ago a colleague of mine tried playing Swords & Soldiers online. Even though the Steam version of the game is almost five years old now and there are only a few people playing, he got three different opponents in just an hour. There were never more than four people playing Swords & Soldiers simultaneously that evening, so he got a surprisingly good multiplayer experience with such a microscopic community. Amazing!

![](../../assets/8a3876660974a385.jpg)

**Playing against bots**

For Awesomenauts we chose a different approach. Here we let the match start even if there aren't enough players for a full 3vs3 match. The missing spots are filled with bots until more players are found. The result is that even if there are very few players online, you never have to wait long and can always start playing.

Initially Awesomenauts just started a match right away regardless of how many players were found, removing waiting times altogether. The big downside of this is that it doesn't work well with a competitive mentality: it feels unfair if bots already lost a tower before you even joined. For this reason we later added waiting time, but with a countdown timer that shows the maximum waiting time left. Since Awesomenauts has plenty of players most of the time the match will be full well before the timer runs out, so you rarely start with bots.

This drop-in aspect of the game is a constant source of complaints from our userbase, but players often don't realise that without it, Awesomenauts might not have survived its first months. It took nearly half a year before our playerbase reached a constant good amount on PC and even with those smaller numbers there were never long loading times.

![](../../assets/013b9e3cc88deea6.jpg)

**Adding more players**

So far I have focussed on making the most out of a your existing players. Another important approach is to maximise the numbers of players. This can be done in various ways. Many multiplayer games are free-to-play, increasing the size of the playerbase (although there are also plenty of free-to-play games that don't actually manage to gather a significant playerbase).

The developers of

[Verdun](http://www.verdungame.com/)chose a hybrid approach: at some point their game had a free browser version and a paid Steam version and they all played together online. The free players didn't bring in a lot of money directly, but they made the game more fun for the Steam players, increasing sales there.

Even when not going free-to-play it is a good idea to not make a game too expensive. The average indie game seems to have recently gone up in price, but I would heavily advice against pricing a multiplayer-only game above $15: this will decrease the size of the playerbase. Selling more copies is more important for the long term income of a multiplayer game than the short term income of a higher price. Awesomenauts is $10 and we often drop its price heavily during sales, by as much as 90%. This boosts the playerbase enormously, more than making up for the low price.

**Extreme measures**

If you want to make a multiplayer game playable with below 10 simultaneous online players you might have to resort to extreme measures to keep something going. Several devs told me they promoted a specific moment, like one specific evening every week, as multiplayer evening. This way everyone comes online at the same moment, creating a somewhat lively community once per week. One dev even went as far as taking the multiplayer functionality offline altogether during weekdays, only allowing multiplayer during weekends.

![](../../assets/fd4c9b1037e8afae.jpg)

I can imagine other, more subtle ways to get players online at the some moment. Like allowing players to send a challenge to other players who are near them in the leaderboards. The game then sets up a time for them to play against each other, giving them a good reason to come online at one particular time. Asynchronous multiplayer is also a good way to do this, but this only works with certain types of games. For highscore based games asynchronous multiplayer can be an excellent way of boosting the competition within the community.

![](../../assets/920eba768b15f717.jpg)

![](../../assets/dd408a15230af855.jpg)

There are many other ways to make the most out of a small community. For example, things like clever lobbies, a rematch option and showing the expected waiting time per game mode. Key is to consider matchmaking a real part of game design, something to brainstorm about and come up with creative solutions. If you just make something then you might end up killing your community much quicker than needed. If you aren't Blizzard or Riot then thinking about how to make the most out of a smaller online community is crucial to the success of your multiplayer game.

Awesome post. This type of content is literally gold for up and coming devs. I hope others will utilize these ideas more in the future.

ReplyDeleteVery good... I use almost all these techniques in my game Rawar :) It's working more or less... thanks!



ReplyDeletehttp://rawardevlog.blogspot.nl

Daan

What about showing the players stats about who's online and whether they're in a game or not? How about graphs that show the last week in players online per hour, so players can use that find common times to play?


ReplyDeleteAre there any reasons against those, or are they unmentioned because you didn't think of them?

They are unmentioned because there are a million possible ways to tackle this and I had to stop writing at some point. :)




DeleteI think showing player numbers might not be a good idea if the game has few players. With 10 players online you might be able to find a good match, but seeing such a low number might turn people off. Of course, with large playerbases it can be great marketing. :)

An alternative is to show the health of various game modes. If you allow the player to choose which mode to play and tell him whether he'll have a good chance of finding opponents for each game mode this might be a flexible solution.

By the way, I know one particular game that shows how many people are online and simply lies about it. The game has been dead for years but claims thousands of people are online. You don't actually find any opponents, it just shows that high number.

Even if you are Blizzard, your game can die. Though it has several reasons, it is clear that Overwatch is dying nowadays.




ReplyDeleteSolo play is a used method that sometimes called skirmish. Combining it by using bots for empty places can be considered too. Long-lasting online games should also have a great community. Toxicity is a problem of online games, keeping its level as low as possible is a serious job.

I also created a blog post about toxicity: https://gamegraduate.com/the-problem-of-multiplayer-games-toxicity/

I consider toxicity is the basic problem of multiplayer games. Games overcoming it most, are one step ahead.