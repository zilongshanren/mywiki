---
title: Why good matchmaking requires enormous player counts
url: http://joostdevblog.blogspot.com/2014/11/why-good-matchmaking-requires-enormous.html
author: Joost van Dongen
published: '2014-11-22'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](http://www.awesomenauts.com)often has well over 1,000 people playing the game at the same time, which is very high and successful for an indie game. It certainly sounds like a lot to me, but this is only a fraction of what would be needed to do everything with matchmaking that we would want to do. Today I am going to explain why tens of thousands of concurrent players are needed for truly awesome matchmaking.

Matchmaking has two main goals. The first is to let people play together who will have a good internet connection to each other. We would like to avoid Australians playing together with Europeans because their ping will be very high. High ping decreases the quality of the game experience, especially in a fast and highly competitive game like Awesomenauts. Finding good connections is more complex than simply looking at distance: sometimes you have a worse connection to your neighbour than to someone on the other side of the continent. The internet is just very unpredictable and random when it comes to connection quality.

The second main goal of matchmaking is to let people play together who have similar skill. There is no fun in getting beaten by someone who is way better than you, and n00bstomping gets old really quickly as well.

Now that we know our core goals, let's try to estimate how much 1,000 concurrent players really is. I am going to simplify things and use a lot of assumptions, but I think the ballpark figures are realistic enough to communicate my point.

The first step is to look at how often these players are actually available for matchmaking. An Awesomenauts match takes on average somewhere around 20 minutes, so players are available for matchmaking once every twenty minutes:

| 1,000 / 20 = 50 players per minute |

We don't want to matchmake with people who are too far away, and players are spread all over the globe. Let's say that the average player would have a good enough connection to one third of all players. In reality players are not spread equally, since Awesomenauts is more popular in some countries than in others, and because of time zones. Let's work with that one third though:

| 50 / 3 = 16.7 players per minute |

Next step is skill. Let's say we consider one third of all players to be close enough in skill to make for a fun match:

| 16.7 / 3 = 5.6 players per minute |

AUCH! We are already down from 1,000 concurrent players to only 5.6 suitable players per minute, and this is while looking at only the most basic of assumptions...

For perfect matchmaking I would want to split players further. A common request from Awesomenauts players is to have unranked and ranked multiplayer. If we would add this, the split between these modes would probably not be equal: one mode would likely get more players than the other. Let's assume one third of all players would play one mode, and two thirds would play the other mode. We need to split further from the already small numbers we have because even in unranked matchmaking we still want to match players based on similar skill to create fun matches. This is how few players we would have left in the smallest of the two modes:

| 5.6 / 3 = 1.9 players per minute |

Another common request from the Awesomenauts community is to split pre-mades from solo-queuers. A pre-made is a group of people who form a team by hand in the lobby before the match, while solo-queuers are put together in a team with complete strangers by the matchmaker. Pre-mades potentially have a big advantage because they will likely do much better teamwork. In the ideal case pre-mades would therefore only play against other pre-mades. How many pre-mades there are varies wildly with the skill level of the players (highly skilled players generally play in pre-mades much more). Let's assume that on average one fourth of all players are in a pre-made:

| 1.9 / 4 = 0.46 players per minute |

Since we are talking about perfect matchmaking, let's have another look at our skill-based matchmaking. Above I assumed that one third of all players is a good enough match in skill. In reality the top players are way too much better than the rest to make this ideal. The top 5% of players are an enormous amount better than the top 33% of players. The more precisely we could match based on skill, the better. I think we would need to do at least three times better than we did above for ideal matchmaking:

| 0.46 / 3 = 0.15 players per minute |

I can imagine some more criteria for ideal matchmaking (like supporting more game modes in matchmaking), but I think the point is quite clear already. With 1,000 concurrent players it will take 30 minutes to fill a match! Obviously this is totally unacceptable. Here's a summary of all the criteria I have mentioned so far:

![](../../assets/117bdae8e9a4fa3b.gif)

Let's say it is fine to let players wait for two minutes for a match to fill up, bringing us to 0.3 suitable players during the available time for matchmaking. To bring us to the required 6 we would therefore need 6 / 0.3 = 19 times as many concurrent players for good matchmaking. We started with 1,000, so we need 19,000 concurrent players. Of course there is a big daily fluctuation in the number of players (there are fewer players deep in the night and early in the morning), so to also have good matchmaking at the slow hours we would need three times more players still. Thus we would need 58,000 concurrent players at peak for good matchmaking. That probably equals over 5 million unique players each month. Holy cow that is a lot!

When building a multiplayer game it is important to think about this. Ideal matchmaking requires enormous player counts, and if your matchmaking is built assuming such player counts will be there you might make something that works really badly for more realistic numbers. Therefore the ideal matchmaking system is flexible: it brings perfect matchmaking when there are tons of players but also makes the best of a small player count.

Despite all of this we can still make big improvements to the matchmaking system in Awesomenauts. We are aware of this and are therefore rebuilding the entire matchmaking system from the ground up in a much smarter and much more flexible way than is currently in the game. I am sure this will bring a big improvement, but at the same time it is important to have realistic expectations: no matter how well we build our matchmaking, the player count required for 'perfect' matchmaking is unrealistic for all but the few most successful games in the world.

yay for comments getting absorbed into the void if you try to type something with google acount!


ReplyDeletemmr should give the person playing more freedom. They should have the choice to be able to be matched against higher skilled players, Though it should not disregard the people in his own MMR. Also p2p servers are almost always worse than dedicated ones a eu to us dedicated server you will have a steady 120 ping. where as if it is p2p it will most likely have a steady 300 ping or worse.

I think you have to be a fellow blog maker for you to not be anonymous.

DeleteHopefully Awesomenauts could become as huge as Dota 2 - matchmaking times don't take too long when you have millions of players.

ReplyDeleteOr...you could change matchmaking significantly, to suit the needs of the servers instead of making a matchmaking system 'good enough' for one server and garbage for the others. Refusing to do this results in requiring massive numbers of players or who knows what which we simply don't have.

ReplyDeleteDisclaimer: I frequently play awesomenauts but don't keep up with the community discussions, so I'm guessing this topic has been discussed and/or trolled to death, but I'm legitimately curious. Now the question:



ReplyDeleteWhat were the decisions behind not making the game free to play? I read your post on why free to play inherently can't optimize for the most enjoyable experience, but there are some existing f2p models that (from my point of view) do really well for both players and developers, mainly Dota and League of Legends. (Interestingly, even though Awesomenauts is a paid game, it still can't optimize for the best experience because it has paid skins, as your reply to the Dota comment suggests.)

If there's already a discussion around this, I'd appreciate a link. If not, I'd be interested to hear some of the factors that kept/keep you from going f2p, which I think could potentially solve a lot of these matchmaking problems. Is it because you don't make enough off skins to make it a viable option? Is it because you're considering having dedicated servers (one can wish...), and more users would make that harder at this point? Or maybe the Dota/League f2p models only work well with a much larger number of characters and skins to unlock or buy?

"Consecutive" doesn't mean what you think it means. I believe the word you're looking for is "concurrent".


ReplyDeleteOtherwise, great read!! :)

Doh! Thanks for pointing that out, I have fixed it in most of the post (cannot fix the image right now but I'll do that later). Funny thing no one mentioned this before even though this post got around 50,000 views.

DeleteSaying something isn't possible is a very bold statement!



ReplyDeleteIt'd be nice to see some actual data backing up these estimates.

If you were to partition those 1000 players into sets of good matches you'd surely find significant size variance owing to the clustering of geographical distribution (peak hours?) and skill distribution. Also average players per minute does not seem a very meaningful measure given its variance throughout the day and the clumping / non-independence of player arrivals.

I only said 'ideal' matchmaking is not possible and I showed the numbers in the post.




DeleteThere is indeed geographical clustering. For most players this makes it better, for a smaller group this makes it much worse. In the ultimate case everyone would be in the same geographical cluster. Then all the numbers in the post above would be 3 times lower.

As for daily fluctuation: our daily peak is currently around 1500 to 2000 simultaneous players. So even when playing in the biggest region at peak hours we would still be far from what I would consider 'ideal' matchmaking.

As for players arriving irregularly: the larger the player base the more regular their arrivals will become. The main source or people arriving at the same moment is a previous match finishing, but for 'ideal' matchmaking this is actually quite bad: I would prefer to matchmake people with different players than with the exact same ones over and over again.

Points taken! Have you considered giving more difficult to matchmake players (e.g. geographically remote) a longer wait in the system?



DeleteBut it depends how you define "ideal" matchmaking. I believe it should ultimately be defined in terms of player experience of the resulting matches. Then skill and geography are ultimately just heuristics to get you there.

Player ratings of the resulting matches are the data to which I referred that are missing from this picture against which performance ought to be measured.

For the new matchmaking we are building we are indeed considering to give more difficult groups a longer waiting time to be able to match them better. This might include premades and people in regions with few players at that time. We have not made the final decision yet on how that is going to work.


DeleteWhat do you mean by "player rating"? Isn't that just a number that represents skill? Or do you mean something else?

I was trying to frame the definition of "ideal matchmaking" something along these lines: consider an oracle machine that somehow always picks in advance the best possible partitioning of the available players into matches that would maximise resulting player enjoyment of the matches.







ReplyDeleteThen you can define your system's performance as relative to this theoretical "ideal matchmaker". Then "ideal matchmaking" is defined in terms of the players you actually have available which seems more useful.

As for what I meant by player rating stats, one way you could aim to measure this performance in the real world would be to collect user submitted ratings of the matches afterwards. For instance you could ask them to give the match scores out of 5 for:

- Overall enjoyment of the match

- How well balanced the match was in terms of skill

- How good or bad the "lag" experience was

- How well-matched the languages were, or other geographic considerations

Then you have some data to work with that hopefully reflects user experience to some extent. Which lets you measure your development progress against these as you try different ideas, and you can at least in principle optimise these different aspects independently.

And for your blog readers you can publish the data answering interesting questions like where is the sweet spot in the tradeoff between minimizing experienced "lag" and minimizing skill difference? Just how long is the average player prepared to wait in a matchmaking queue? :)

Ah, yes, that is indeed a very different definition of "ideal matchmaking". Making the best system possible for a given real situation is a big challenge. We think we can do much better than we are currently doing with Awesomenauts, which is why we are building an entirely new matchmaking system.



DeleteStill, even the theoretical best matchmaking system will give poor results if the playerbase is not big enough.

Various approaches to building a matchmaking system is an interesting topic for a blogpost, I actually plan to write at least two posts about that at some point. The new matchmaking we are building is already our third approach and we have extensively analyses several other, there are lots of interesting things to say about matchmaking algorithms. :)

It is a really interesting topic, and I look forward to the posts!





DeleteI think being at this point in player counts, where those purely statistical approaches huge games use start to break down, actually makes for a more interesting set of problems and potential solutions!

For instance such measurement of player feedback on the matchmaking process itself naturally lends itself to supervised/reinforcement learning. Can machine learning techniques do better at smaller sample sizes?

I wonder if there's been much work done on trying to dynamically model player attributes such as emotions (e.g. happiness/frustration)? You could even augment this with sentiment analysis of the in-game text chat.

For instance if your model predicts the player is likely getting very frustrated, match them with happy team-mates to try and calm them down! Or if they lost 5 matches in a row, deliberately put them in a match they are almost guaranteed to win.

Glad to hear there is plans for better matchmaking. It's frustrating to be rank 1 or 2 and be with players that don't understand how to use their team mates to their own advantage while also the teams advantage. (Eg. a Leon that doesn't pull enemies into yuri's mines and continually 1v3's on other side of map and dies but repeats the same thing like 10 times). And then there is the occasional statement "This is my first time using this character" even though it's rank 1 or 2.

ReplyDeleteThis is why server browsing is important. If you don't have enough players to adequately flood the matchmaker, having access to a server list is better for a myriad of reasons.

ReplyDeleteI love these development explanation posts, and read all of them when they get posted to /r/awesomenauts. But this one is particularly good: a clear and easy-to-understand explanation of a topic that is consistently discussed by players. I revisit and re-read this post from time to time, and refer curious players to it liberally. Thanks for this!

ReplyDeleteGood to hear it's so clear! :)


DeleteI also occasionally get visitor bumps on this post when someone links it in a Smite or DOTA2 discussion. Which is quite hilarious as these games have gigantic userbases, so most of these problems hardly apply to them...

Yeah, I'm by no means experienced with coding (basically just dabbling in HTML and CSS...), but I definitely find your style clear and engaging.


DeleteFunny to hear about those other referrals. I guess the lesson there is that some subset of players will complain about matchmaking even when they have no reason to do so.

I've been playing Awesomenauts with my kids for years now. We basically stopped playing online as a team.



ReplyDeleteWhat I don't understand is: why not introduce handicaps? That way strong player can be matched with weak players, and both still play a challenging match. It probably doesn't even take that much... Maybe just increasing the health based on your handicap would go a long way.

I mean: you clearly do that with bots... Why not with real people?

I can imagine that would be a fun thing for a custom game or local botmatch, but for public online matches I have little doubt that most of the community would utterly hate that. Just imagine how someone would feel if they lost because they got a handicap or because the enemy got a buff...


DeleteAlso, some players smurf so it's impossible for the game to be 100% sure whether someone is a beginner/kid, or whether he is deliberately leaving matches to keep his rating low and not get a handicap. It would be very abusable.

Have you tried or seen anyone change the risk in entering a matchmaking scenario to find an appropriate skill match? For instance, in wagering your points/coins/money, same match has different wagers but players have similar skill.

ReplyDelete