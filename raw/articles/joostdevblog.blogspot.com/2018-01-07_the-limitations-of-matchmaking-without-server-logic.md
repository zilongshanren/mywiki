---
title: The limitations of matchmaking without server logic
url: http://joostdevblog.blogspot.com/2018/01/the-limitations-of-matchmaking-without.html
author: Joost van Dongen
published: '2018-01-07'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[generic matchmaking systems based on rooms](http://joostdevblog.blogspot.nl/2017/10/working-with-generic-room-based.html). These systems are great for quickly getting things going and are fine for most smallish games. However, if matchmaking is very important for your game and the requirements for matchmaking become more complex, these generic systems turn out to be pretty limiting. Today I'd like to discuss how we tried several approaches to get the best out of such generic systems in our game

[Awesomenauts](http://www.awesomenauts.com/)and how the problems we encountered ultimately led us to develop our own matchmaking servers altogether.

Keep in mind that whether these problems are truly important depends on the game. If your game is a bit more casual, or has fewer players per match, or less focus on online multiplayer, or allows late-join, then the requirements for matchmaking become a lot less stringent. Depending on how demanding the matchmaking for your game is, none of these problems might be enough reason to skip the great convenience of using an existing matchmaking system.

![](../../assets/c3dd6351aea6108e.jpg)

The main problem is that these generic matchmaking systems don't allow serious logic to run on the server. The server keeps a list of gamerooms that the player might join, but the decision which room to actually join is made by the client. With this in mind, let's have a look at some of the client-based matchmaking algorithms we tried in Awesomenauts.

**The 'growing search range' approach**

The standard approach to client-based matchmaking is to have a growing search range. The client starts by asking the server for a list of all the rooms that can be joined and then checks whether any of those rooms are near geographically (to achieve low ping) and are similar in terms of skill. A good starting point might for example be that the other players in the matchroom need to be in the same country/state and differ by at most 500 skillpoints (in a system where 10,000 is the average skill of all players). If several suitable rooms are found, then we join the one closest.

This algorithm is simple enough, but the challenge is what to do when no suitable rooms are found. If you're adamant on always having high quality match-ups, then you might choose to simply wait for more suitable players to appear. However, unless your game has an enormous player count this probably results in really long waiting times for the user, or even in never finding a full match at all.

Therefore we increase the search distance over time. For example, we might double the allowed geographical distance and skill difference every 20 seconds. We keep doing this until we've found a suitable match. If at the biggest search range we still haven't found anyone to play with, then we simply keep waiting and searching.

An important note here is that while searching, the player also has her own room open for others to join. As soon as someone joins your room, you stop searching and just wait until enough players have joined for the match to be started. If you join someone else's room, you close your own room. To avoid problematic edge cases like two players joining each other's rooms simultaneously we add a simple rule: if the other room has only one player in it then we only join it if that room has a lower roomID than our own room. This may seem limiting but in practice doesn't matter much: if I can join your room because you have similar skill, then you can (eventually) join my room as well. It doesn't matter who joins who as long as we end up together.

This is roughly the matchmaking algorithm that Awesomenauts had at launch. What we didn't know back then, is that in many cases the result is little better than just joining a random room. For example, let's say a new player starts searching every 5 seconds. In a game with matches of 20 minutes, this means we have 240 concurrent players, which is pretty nice for a smaller indie game (multiplayer games that are an okay success on Steam are generally in the range of 400 to 2000 concurrent players). In the case of Awesomenauts a full match needs 6 players, which means it would take 30 seconds for a complete group to start searching. For decent matchmaking we don't want to play with just anyone though: we want a good match in terms of ping and skill. Only 1 in 4 players will be even remotely acceptable to play with (in practice probably

[even less](http://joostdevblog.blogspot.nl/2014/11/why-good-matchmaking-requires-enormous.html)), so we need to wait 2 minutes for enough players for a match. However, this won't happen: by the time we've waited that long we will have grown our search radius so far that we will have joined some other match already.

The result is that this algorithm isn't as good at finding a good matchup as one might think initially. We tried playing around with how quickly the search range grows and such, but we couldn't find a way that achieved a big enough improvement.

**League-based matchmaking**

Back then we got a lot of complaints about matchmaking not producing good match-ups, so we concluded that we needed something different. What we came up with was to add a league system to Awesomenauts and limit matchmaking based on that. We added this to the game in September 2012, a few months after launch. The idea is that we divide the leaderboards into 9 leagues, based on player skill. These leagues weren't just intended for matchmaking, but also for the player experience: it's cooler to be in league 2 than to be in place 4735, even though that might actually be the same thing.

![](../../assets/23a7d11e63a11e33.jpg)

The matchmaking rule we combined with these leagues is that players could only join matches in the 3 nearest leagues. So a league 4 player could join matches that are leagues 3, 4 or 5. A league 1 player (the top league) could only join matches in leagues 1, 2 and 3. Having such a hard limit should keep players from experiencing extremely big skill differences with their opponents or teammates.

For this to work you need to know the player's skill pretty well, so an important question is how well the game actually knows each player's skill. This is an important issue in

*any*matchmaking system and is such a big topic that I'm not going to discuss this today. For today's blogpost let's just assume that the game has a somewhat decent idea what a player's actual skill is.

Another important issue is what to do if there are few players online. Having hard limits on who can join who means that in some cases you might not find opponents quickly enough. For this reason we stretched the allowed league range a bit further when few players were playing at that specific moment. The Steam API contains this information so implementing this is simple.

An easy mistake here is to simply split the leaderboards evenly. So for example if there are 90,000 players in the leaderboards, then numbers 80,001 to 90,000 are league 9. However, this doesn't work: some players play much more than others and players who stopped playing are still in the leaderboards. If these would be evenly spread out over the community this wouldn't be a problem, but of course they aren't: top players play much more than bottom players.

Our solution was that we measured how many matches were actually being played each day in each league and adjusted the league sizes based on that. Our implementation was bit clunky so we had to adjust this by hand occasionally, but it worked most of the time. The result is that league 2 is only a few percent of the leaderboards while league 9 is around 55 percent, resulting in equal numbers of matches being played every day in each league.

![](../../assets/afe60b037ad8f9ad.gif)

The league system was a big improvement for the matchmaking in Awesomenauts: not only did it make the matchmaker much better at matching similar players, it also provided a fun extra reward system, since wanting to be in a certain league is a fun challenge.

One specific problem with league based matchmaking is that going up a league makes too big a difference. If you go from the top of league 3 to the bottom of league 2 you suddenly get way better opponents, even though your own skill might have only marginally improved. Also, the skill difference between the top of a league and the bottom of that same league can be really huge, especially in the top leagues. While our matchmaker also looked for the best room to join in terms of exact skill (besides just the league requirements), it wasn't very good at this because of the problems with the growing-search-region algorithm I described earlier in this blogpost. A way to lessen this problem is to have more and smaller leagues, but we felt having dozens of leagues makes league climbing less fun for players.

**The lack of server logic**

While leagues were an improvement, this approach didn't fix the big problem that there's no logic running on the servers. Each client decides for themselves based on incomplete information. This is very limiting to how clever your matchmaking can be. There are lots of situations in which this algorithm will fail to produce optimal match-ups. Here's an example:

![](../../assets/78cb6438877a569e.gif)

As you can see, in this case the algorithms described above fail to find the best possible match-up. Perfect matchmaking is impossible without huge player counts, but the matchmaker should do its best to find the best combinations with what's available.

Below is another example of a type of situation that this algorithm doesn't handle well. This one shows that this particular algorithm is particularly bad at matching premades with other premades: as soon as a single solo player joins, there's no room anymore for another premade that might start searching a little bit later.

![](../../assets/1758d876ec9579bc.gif)

Undoubtedly some super complex distributed algorithm is possible that can always find the optimal match-ups without any logic running on the servers. However, at that point the complexity of the algorithm becomes so high and debugging so difficult that I think running the matchmaking logic on a server instead is a much more viable solution. So we started developing our own matchmaking system (called Galactron) with our own servers. This was added to Awesomenauts in 2016.

In this post I've shown a number of problems we've encountered with generic room-based matchmaking systems and how we tried different approaches to work around those. However, not all of the issues with our early matchmaking approach were caused by the limitations of generic room-based matchmaking. Some issues were caused by how we had actually implemented our side of it. Those make for an interesting read by themselves so my next blogpost will be about the things we could have done better within the confines of generic room-based matchmaking.

## No comments:

## Post a Comment