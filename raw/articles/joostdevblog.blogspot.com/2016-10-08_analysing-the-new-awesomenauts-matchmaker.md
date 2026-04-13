---
title: Analysing the new Awesomenauts matchmaker
url: http://joostdevblog.blogspot.com/2016/10/the-first-results-of-new-awesomenauts.html
author: Joost van Dongen
published: '2016-10-08'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](https://www.awesomenauts.com/). This rework is called Galactron. This is a huge operation: especially the matchmaking part is highly complex. We've done a bunch of betas for it so far and last week we let it run live for everyone for 48 hours. After that we turned it off again to analyse the results, read player feedback and fix bugs. Today I'd like to discuss the most interesting results.

I plan to do an overview of how Galactron works in a future blogpost, but today I'm just going to focus on what we've encountered in last week's beta.

### Ragequitters and the removal of latejoin

This is probably the hottest topic in Galactron. Latejoin was probably the most hated feature of the old Awesomenauts so we've removed it altogether. In Galactron players are never put in a match that's already in progress. We've also added a rejoin option so if you're kicked out of a match due to a network error you can get right back into it. Finally, if someone leaves a public match, he can only rejoin that same match and can't get into another. A lot of players like this, but there's also a vocal group who is strongly against the removal of latejoin and the increased punishment for ragequitting.

I think there's no way to make both groups happy: they just want something different out of Awesomenauts. I've seen some people suggest we should make two gamemodes: one where latejoin and ragequit are allowed and one where they aren't. However, this is not an option because our playerbase is not big enough to split it like that. If we had the playercounts of League of Legends we could try things like that, but with our current playercounts we can't afford to split the community. Matchmaking in both versions would be worse if we did.

Instead of talking about opinions, let's have a look at cold hard facts. A common complaint about the removal of latejoin is that if someone leaves a matches and doesn't rejoin, the match remains 3vs2 until the end, whereas in the past the player would be replaced by someone else. This replacement didn't always happen though: in the old matchmaking matches weren't all 3vs3 all the time either. We gather metrics on this, so let's have a look:

![](../../assets/dbe5b020976c173a.gif)

As you can see the percentage of time that matches are 3vs3 is actually

*higher*in Galactron than in the old matchmaking. In other words: while it may feel lame that leavers aren't replaced by latejoiners anymore, the overall result of Galactron is that you're playing 3vs3 more often. So while I can imagine that ragequitters dislike the new punishment they get for leaving, the complaint that matches remain incomplete more because leavers aren't replaced turns out to be unjustified.

### High ping

The other major complaint about Galactron is high ping. While Galactron is supposed to make the average ping lower, players complain that ping is higher. Again, let's look at the metrics to see whether they're right:

![](../../assets/8a63f70d58ee6de2.gif)

Here it turns out that the stats agree with the complaining players: average ping has indeed increased significantly in Galactron.

**This is a big problem that we need to solve.**It's also a big surprise to us: Galactron contains a lot of clever tech to match players better, why isn't that working?

We've been analysing this extensively these past few days and have a bunch of theories, but we don't have the final answer yet. One thing we've noticed is that it seems like Galactron doesn't get enough ping data. While players are waiting for matchmaking the game pings all other waiting players. We expected this would give us ping data on at least 75% of all possible connections, but in practice this turns out to often be around 50%. This means that Galactron doesn't have enough information to make a good matchup. Figuring out why this happens is our highest priority now.

Another possibility is that Galactron may care about skill too much right now. Galactron needs to find the best match-up based on a bunch of criteria around ping and skill. It can't satisfy them all perfectly all the time so it tries to find a balance. We can tweak how important each criterium is and I think we might have made skill too important right now.

A final issue we're looking into is how to handle people with horrible internet. High ping can happen when you're playing against someone on the other side of the globe, but sometimes your opponent just has such a horrible internet connection that he has high ping to everyone, even to people near him. No matter who Galactron matches such players to, the connection will always suck. We haven't decided how to handle that yet. One option is to make such players only play against others with crappy internet and keep them out of the regular matchmaking, but that might give odd results in the leaderboards as they would always be playing against the same people. We'll have to observe this group more once the other issues are fixed.

### Skill matching

This is an aspect where Galactron seems highly successful: matches are very balanced. There are still situations where players of differing skill play against each other, but this is now usually caused by premades in which the players don't have the same skill. We can't split premades so this can't be solved. What we can do however is balance such premades against another similar premade, or against other players with similar skill patterns. Galactron turns out to be able to do so quite often. We also see premades play against other premades much more often now than before.

It would have been nice to compare this to our snowballing stats, but unfortunately those weren't recorded in the Galactron live beta due to an oversight. We normally collect stats about how often one team has much more kills than the other team, and how often the losing team didn't destroy any turrets. It would be interesting to see those stats for Galactron, so it's a pity they weren't recorded during the last beta.

### Waiting times

I've seen some complaints regarding long waiting times in Galactron. Galactron performs a matchmaking round once every 5 minutes. That means that if you start searching for a match just before the round starts you'll get a match really quickly, while if you start searching just after you'll have to wait the full 5 minutes. On average this means a waiting time of 2.5 minutes. That isn't that much longer than before: in the old matchmaking it might take up to 4 minutes before a match stars, and longer if it isn't full yet at that point.

It's easy enough to reduce the waiting time: we can just switch from 5 minutes per matchmaking round to 4 minutes. However, we're not sure we should: a shorter waiting time will also mean lower match quality. There's a balance we need to strike here between speed and quality, and for the moment we think 5 minutes is fine. If we keep seeing a lot of complaints about this we'll reconsider and might change it to 4 minutes at some point. Feel free to share your opinion on this in the comments below.

### Crashes

There have been some reports on crashes in Galactron. We've investigated most of these and so far they seem to be caused by driver issues and by broken Steam downloads. The latter can usually be fixed by running Steam's Verify Integrity Of Steam Cache.

As for the driver issues: my theory is that the crashes that we have data on are caused by alt+tab. Unfortunately our crashdumps don't contain a history that tells us whether alt+tab happened just before, so we can't tell for sure.

If alt+tab crashes than your videocard drivers are problematic. The solution is really simple: run in Borderless Window instead of Full Screen. With Borderless Window the game still covers the entire screen, it's just a different way of asking Windows to do so. Borderless Window is much more stable when it comes to alt+tab, and it's also much faster at it. In general we advice never running Full Screen unless Borderless Window gives you problems. I think we might rename these options to reflect this, since I expect some people might not understand what Borderless Window means.

We're still investigating some of the crash reports. If we encounter any that are caused by Galactron, we'll fix them of course.

### Bugs

Besides the things mentioned above there were also a bunch of random bugs. Most of those we've already fixed by now, or are working on fixing. Some of the most notable ones:

- Global chat didn't work half the time.
- One menu screen around the tutorial didn't accept any button input, making it impossible to progress if you got to this screen (ARGH!).
- Some menu screens didn't support controllers properly; only keyboard+mouse worked there.

So there you have it, the current status of Galactron. If you have any further questions, complaints or suggestions on Galactron then please do post them below in the comments. We hope to do another beta 1.5 weeks from now. Hopefully that one will be good enough that we won't have to turn Galactron off again, but we'll have to see how it goes. Most important is that Galactron needs to be really good before it goes out of beta.

This comment has been removed by the author.

ReplyDeleteIt's not OK above 150 ms

ReplyDeleteYeah, it's a bit of a stretch. The game is still very playable at 180ms ping but it's definitely already annoying at that point.

DeleteI would definitely prefer for the matchmaking time to be shortened.



ReplyDeleteI also think killing latejoins is a terrible idea. Even if quitters weren't replaced every time, they were some of the time. That makes it worth keeping. The new system will just make people hide or feed instead of quitting to end the game fast, or they do quit and you lose because you're stuck with a bot with 0% chance of it being replaced. What's the point of even finishing a match if someone quits?

If I have to wait 5 minutes for every game and lose a good portion of them just because someone quits and isn't replaced, I'm definitely no going to want to play anymore.

Matchmaking time should be shorter than 5 minutes, it takes too much valuable playtime away. I don't see late joins as a bad thing, the game shouldn't be pretty much over because someone quits.

ReplyDeleteThis was really comforting to read and makes me motivated to join in the galatron beta coming up. Keep up the great work.

ReplyDeleteLots of good information, these blogs are great. I have a few ideas on how to shrink that "Incomplete Games" bar if you're interested, might be a bit complex for the average user to understand though.

ReplyDeletePlease do type it here: anything that helps to keep matches fuller is important to making Awesomenauts better. :)

DeleteThis comment has been removed by the author.

DeleteIt's possibly already been suggested, but my idea is that you bring back Late joins as an optional thing.








DeleteThis solves that rage quitting out of a match means that the team you left will suffer a loss 99% of the time, and that those who hate late joining don't have to bother with it.

Also, the joiner is aware the match he is joining is a late join, and that even in victory the match doesn't count towards ranking. They're doing it purely for experience or fun. (personally I find early game boring, entering a match with 1000+ solar is quite nice)

This opens up that the joiner might accidentally pick a naut that hard counters the enemy team though, which isn't fair towards them. The naut they where building against suddenly isn't the naut there build counters. BKM against a Snare-Build Derpl becomes useless against a DoT-Build Gnaw. RBAY against Rocco becomes useless against Leon. Etc.

My suggestion to fix that would be to give the joiner the naut of the person who left, which solves the issue of a counter-stomp match. The only problem here is the person might be more skilled with that naut than the person who left, or significantly less skilled with that naut than the person who left.

Which is kinda where my solution falls apart, obviously you could check there overall rank rating to get a basic idea of how "Good" they are compared to the quitter, but that isn't exactly precise enough down to the specific naut. A standard froggy main in L2 mostly likely will have a significant drop in skill if they are replacing a slow-tanky naut like Clunk.

On the other hand though, that level of fidelity might not be relevant when looking at overall matches that are complete.

And on the other OTHER hand a system like this is likely not worth the effort for like a 5% increase in complete matches.

What you propose is an interesting solution, but the skill difference is indeed a problem. Also, I think a mode in which you get forced into a character in a latejoin will be fun for very few people. Hardly anyone would do that, making the devtime not worth it.


DeleteThere's also another problem: latejoin conflicts with rejoin.


ReplyDeletesad, I play the game since launch, started on the Xbox, and the first time I was discouraged enough to the point of not playing more, for me this update is the end of my matches in Awesomenauts, sad

Why is that? What's wrong with Galactron in your opinion?

DeleteTHANK YOU for eliminating late joins. Contrary to what some have said in these comments, this was a great decision. The last few matches I played were some of the most well-balanced and fun in all my 3000 hours of playtime. Incidentally, there were no quitters.



ReplyDeleteIf someone on your team quits, it means that you got outplayed and now you've gotta step it up to compensate or lose. Its that simple. If that sounds unfair to you, keep in mind that letting some better player come in with an unearned average solar value and turn things around is just as unfair to the winning team, and there's a golden rule to game design - you don't punish players for winning.

Keep up the great work Ronimo!

Higher ping might relate to blocklists. I believe many people just blocked laggy players (at least many people I know),

ReplyDeleteThat's probably a factor, but I'd be surprised if it were significant enough for how big the difference is. There are too many players to make blocking a few dozen that significant, especially since likely no more than a few percent of the total playerbase actually does this. I can imagine that amongst the top players this is done a lot, but on the entire playerbase I really doubt that. That's still a lot of players but it wouldn't have this kind of impact on the stats, I think.

DeleteRather than punish rage quiters or bolster latejoiners, why don't you allow a vote concede?


ReplyDeleteThis would make it so that if most players feel the match is a loss, then they can vote to leave the game. The win would automatically be handed over to the opposing team.

We've discussed this, but the problem is that many ragequitters quit very early in the game. Giving up that early would remove any change of a comeback, which is a wonderful experience when it happens.


DeleteAlso, the challenge with this is that it would produce a lot of frustration if players disagree on whether to give up or not. I know that in many cases when a teammate did a ragequit I felt like we still had a chance. In such a case the discussion within the team would probably get aggressive quickly.

And you think that the frustration that arises from wanting to leave a game where you're getting pummeled, but can't without punishment, is a better alternative?



DeleteMake it so that all three players have to vote to concede. If one doesn't, the game continues. If the other two REALLY want to leave, then they can.

Thank you for eliminating late joins. I 100% support that decision; being thrown in an ongoing losing match was pretty much the least fun you could have in the game. I'd much much rather face the risk of every once in a while having to finish a game with a bot.

ReplyDeleteKeep up the awesome work!

Hi, potterman here.




ReplyDeleteHow exactly do you measure the pings in the matchup section ? I mean, do you measure all the possible 150*149 (assuming 150 players) pings, or just a subset of them ?

Also, how do you handle the skill vs ping problem ? Do you first take a look at (say) all the "good ping" matches, and then if the skill difference is too high in the skill-best "good ping" matchup, you take a look at the "OK ping", and so on until you find a good match ? Or do you use something more complex ?

This is a really interesting subject actually

The idea is indeed that all players ping all other players, so that we have ping data on all 150x149/2 possible connections. In practice some will not be done in time, so we expected to have ping data on around 80% of those. However, in practice we often only have around 50% it seems.


DeleteSkill vs ping: our approach is that we can calculate a score for each match based on both skill and ping. The matchmaker then looks for the matchup that has the highest average score for all the matchups it creates. The core of this is the calculation of this score: ping and skill each have a weight that is used to combine them.

I think you should be able to predict pings with far less data. You only need the proper statistical model, or simply throw some deep learning at it. Under the (too idealistic) assumption that ping is solely determined through distance on earth's surface, you require only three pings from known locations to exactly determine the unknown location. Now maybe two dimensions aren't enough. You have an individual noise term, and latency is determined by network structure. But I think some ten to twenty pings for each player should be enough to predict all mutual pings for an arbitrary number of players with good accuracy.

DeleteIn theory you are right, but in practice the internet is a lot more unpredictable than you seem to realise. With a LOT of time and research it might be possible to come up with something useful here, but it's incredibly hard. For example, sometimes two random players just can't connect to each other. They can both connect to everyone except to each other. Coming up with a model that would correctly predict this kind of thing would be incredibly hard.

DeleteI love the idea of putting people with horrible internet into their own pool. And this isn't me talking from just the good internet side of things. I made a bad choice to get cheaper internet from a relative, and because he gave me a good deal and would lose money if I left too soon, I felt obligated to stay the whole year with the internet. I tried playing Awesomenauts a couple times and felt like I just ruined the game for everyone, and that made me feel bad (except for the people who flamed me, I didn't feel bad for them :)). So I literally had to stop playing Awesomenauts for about a year, which sucked.


ReplyDeleteSo from a standpoint of someone who cares about the game and doesn't want it ruined for others, I would have appreciated the opportunity to still play, even if it's with other people with horrible internet. And as far as the people who don't care if they ruin it for others or abuse it on purpose... well I don't think we need to worry about them.

I appreciate the 'ARGH' about the tutorial screen bug.

ReplyDeleteAlso grateful that you guys fixed it in most recent beta test!

I played Awesomenauts for 1600+ hours, first 1000 in USA, next 300 in Asia, 300 rest is my bloated queue times waiting to be matched in Asia. One day at weekend, in-between 6 hours trying to get a match, I only get full matched 3-4 times, its ridiculous. When I get matched with players from Asia/Australia I got 80 ms ping with them. Everyone around the globe uses Fiber Optics, who uses better? dafuq with salty lag rants from some of EU/USA players, 200 ping if not jitter-ish still plays smoothly, if not maybe they should start blaming their potato PC. My latest rank during my first 1000 hours (pre-galactron 2?) is at top 300 (Between League 1 and 2) with 1100-ish matches in that season, after 1 year vacuum and f2p, I start playing again hoping to get better Matchmaking and my rank is now 1200 L2. I could only imagine the hurdles for newer players in 2017, with such long queue, misleading bot matches (they gonna think game is dead since apparently players with "high ping" get matched with bots very often), salty lag rants, 3-4 Nauts unlocked (imagine getting stomped against 200ms L2 - L3 veterans with all nauts unlocked).


ReplyDeleteTLDR: During F2P launch Ronimo should have segregated the servers to Regions (EU, Asia, USA) then allow players to have an option to get matched inside their region only, or inside+outside. This solves one crucial problem in short run (Newer players from their respective regions will be matched inside their region with good pings and not getting matched with bots) Look at that playerbase shrinking to the original after spike. In long run playerbase retained = more players.

Just time is too much, rest all things seems fine and the best thing is skills matching.

ReplyDelete