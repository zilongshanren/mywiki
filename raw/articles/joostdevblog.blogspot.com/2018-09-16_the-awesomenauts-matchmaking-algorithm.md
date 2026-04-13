---
title: The Awesomenauts matchmaking algorithm
url: http://joostdevblog.blogspot.com/2018/09/the-awesomenauts-matchmaking-algorithm.html
author: Joost van Dongen
published: '2018-09-16'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](http://www.awesomenauts.com/)we rebuilt our entire matchmaking systems, releasing the new systems in the Galactron update. Today I'd like to discuss how Galactron chooses who you get to play with. While the question is simple enough, the answer turns out to be pretty complex.

![](../../assets/0cc375ffb1705de3.jpg)

Many different factors influence what's a good match. Should players of similar skill play together? Should players from the same region or language player together? Should we take premades into account? Ping? Should we avoid matching players who just played together already? Should we use matchmaking to let griefers play against each other and keep them away from normal folks?

If the answer to all of these questions is 'Yes, let's take that into account!', then you'd better have a

*lot*of players! I've

[previously written](http://joostdevblog.blogspot.com/2014/11/why-good-matchmaking-requires-enormous.html)about how many players you need for that and the short answer is: tens of thousands of simultaneous players, all the time. That's not realistic except for the very biggest hits, so you'll usually need to do with fewer players and make the best out of your matchmaking.

For Awesomenauts we chose to let the matchmaker gather a lot of players and then once every couple of minutes match them all at once. This way the matchmaker has as many players as possible to look for the best possible combinations.

![](../../assets/9b20601187fac731.jpg)

We'd like to match more than 100 people at the same time so that we have plenty of choice. More than that would be even better: our research shows that our algorithm keeps getting better up to as many as 300 people per round, because smaller distant regions (like Australia) don't have enough players for proper matchmaking until that many. However, the more players we wait for, the worse the player experience gets because the waiting times become too long.

### Scoring the quality of a match

Okay, so we have 100+ players that all need to be put in matches, how do we decide what's the best match-up? For example, if we can choose between making a match where the players have equal skill, or one where the ping is low, which do we prefer? And which do we prefer if the difference is more subtle, like we can get slightly more equal skill or slightly better ping? Where do we draw the line? And how do we balance this against wanting to let premades play against each other? Etc. etc.

What we need here is some kind of metric so that we can compare match-ups. Somehow all of those matching criteria need to culminate in one score for the entire group. Using that, the computer can look for the best match-up: the one that gives us the highest score.

To calculate a total score we start by calculating the matchmaking score for each match. We do this be taking a weighted average of a bunch of factors:

**Equally skilled teams**. This is the most obvious factor in matchmaking: both teams should be equally good. Turning this requirement into a number is simple: we take the average skill per team and look at the difference between those. The bigger the difference, the lower our score. Note that this does require some kind of skill system in your game, like ELO or Trueskill. This also means that beginning players are difficult to match, because you don't know their actual skill until they've played a bit.**Equally skilled players**. Even if the two teams are perfectly balanced, the match might not be. For example, if both teams contain two pros and one beginner, then the average skills of the teams are the same, but the match won't be fun. So we use a separate score that ignores teams and simply looks at the skill differences between all players. In a 6 player match there are 15 combinations of players and we simply average all of those. The bigger the difference, the lower the score.**Premades**. Ideally a group of 3 friends who coordinate together should play against a similar group and not against three individual players who don't know each other. Assigning a score to this is simple: if both teams have the same situation, then we have a 100% score. If there's a small difference (like for example a 3 player premade versus a 2 player premade + a solo player) then we get a 60% score. For a big difference (a 3 player premade versus 3 solo players) the score is 0%.**Ping with enemies**. For each player we check the ping with all 3 players in the enemy team. The higher the ping, the lower the score. There are 9 combinations of players this way and we simply average those 9 scores to get the total ping score for this match.**Opponent variation**. This is a subtle one that we added a while after launching Galactron. Since our matchmaker basically looks for players of similar skill with a good connection to each other, it tends to repeatedly put the same players against each other. We expected this to be rare enough that it would be fun when it would happen, but in practice our players encountered the same people too often. To counter this we give a match a lower score if players encountered each other in the previous match as well. If they encountered each other as opponents but are now teammates (or vice-versa) we give that a slightly better score than if they meet each other in the same situation (opponents before, opponents now; or teammates before, teammates now). This gives the matchmaker a slight tendency to swap teams around if despite this rule it ends up making another match with the same players. This rule has a very low weight since we value the other rules more, but still this rule improved the situation significantly and we got much fewer complaints from players about this.**Two possible servers**. Since Awesomenauts is peer-to-peer, each match should have a player who can connect with everyone in the match, so that this player can be the server. Ideally there is also a second player in the match who can connect with everyone. This way if the first server-player drops out of the match, host migration can happen and the match can continue for the remaining players. This rule is only needed for peer-to-peer games: in a game with dedicated servers or relay servers this rule is irrelevant.

![](../../assets/8bf5e721249807f4.gif)

There's one important factor missing here:

*ping with teammates*. Why is this not taken into account? The reason for this is that for every factor we add, the others become a little bit less important. In Awesomenauts a bad connection with your teammates is usually not a big problem because you never need to dodge their bullets. A bad connection with an opponent is much worse, because dodging becomes really difficult if the ping is too high. By ignoring the ping with teammates, we make the ping with opponents a lot more important.

Something to think about when calculating scores is whether we want them to be linear. For example, is a ping improvement from 210ms to 200ms as worthwhile as one from 110ms to 100ms? Both are 10ms improvements, but the latter is relatively twice as big. In Awesomenauts we've indeed tweaked our scoring formulas to better match the perceived difference instead of the absolute difference.

Another consideration is limiting the

*range*of the scores. For example, in Awesomenauts the highest ranked players have a skill of over 20,000, but only 0.3% of all players are above 18,000. In other words: there's a huge difference in skill score in the very top, but this is quite useless to the matchmaker since there are too few players with such a high score to actually take this into account. So before calculating the skill scores we cap them to workable ranges. This way the matchmaker will consider a match-up between two players with skill 18,000 to be as good as one between an 18,000 player and a 20,000 player. Ideally you don't cap anything, but since we have to balance between all the different matchmaking goals capping at some points will make other ranges and aspects more important.

### Combining scores

For each of the above 6 rules we now have a score from 0% (really bad match-up) to 100% (really good), but we need 1 score, not 6. To get this 1 score we take the average of all the scores. We use a weighted average for this so that we can make certain things more important than other things. For example, in a fast-paced game like Awesomenauts, ping should be pretty important. Opponent variation on the other hand is a detail that we don't want to stand in the way of good ping, so that one gets a pretty low weight.

An interesting thing that happens here is that some of these scores react much more extremely than others. Getting a 0% skill score requires having 3 pro players and 3 beginners in a match, which is extremely rare. Getting a 0% premade score however happens much more easily, since all that's required for that is having a three player premade play against three solo players. Some scores reacting more subtly than others is something we need to take into account when choosing the weights: since premades react so strongly, we need to give them a lower weight to keep them from overshadowing scores that respond more smoothly, like skill and ping.

Now that we have a single score for each match, we can calculate the totale score for the 100+ players we're matching. We do so by simply averaging the scores of all the matches. The result is one big megascore.

![](../../assets/3853b9e26431af16.gif)


![](../../assets/3853b9e26431af16.gif)

Since we look at the total score, the algorithm gets certain preferences. If swapping two players increases the score of one match by 5% but decreases the score of the other match by 10%, then it won't do that since in total that makes things worse. This sounds obvious, but in some cases one might want to deviate from this. For example, maybe you might prefer improving a match with a 50% score (which is really bad) to 55% at the cost of decreasing a 90% match to 80% (which is still pretty good). A way to achieve this might be to take the square root of all the match scores before averaging them. That way improving bad matches becomes relatively more important. For Awesomenauts we decided against this, because we think the individual scores already represent well enough how big a match quality improvement really is.

### Finding the match-up with the best score

Now that we have a scoring system that defines what the best match-up is (the one with the highest score) we get to the algorithmic part of the problem: how to actually find that best match-up. With 100+ players the number of combinations we can make is insane so we can't brute-force our way out of this by simply trying all combinations.

I figured this might actually be a graph theory problem so I tried looking for node graph algorithms that could help me, but the problem turned out to be so specific that I didn't find any. Even after consulting a hardcore academic algorithmic expert nothing turned up, so I decided to look for some good guesstimate and just accept that the actual best match-up is probably not findable. The problem might even be NP-complete, but I didn't actually try to prove that. Finding a better algorithm might be a fun thesis topic for a computer science student somewhere.

The approach I ended up at is to first create a somewhat sensible match-up using a simple rule. I tried a couple of rules for this, like for example simply sorting all players by skill and then putting players in matches based on that sorting. So the top six players together get into one match, then the next six, etc. This is easy enough to build and produces the best possible skill scores. Since it ignores all the other scores entirely it performs really badly for ping and premades.

We now have 6 players per match, but we haven't decided who's in the red team and who's in the blue team yet. So the next step is how the six players in each match are divided over the two teams. Here we can brute-force the problem: we simply try every possible combination and select the best one. Here we take into account all 6 scores, so not just skill. The number of combinations is pretty low, especially since the order in which players are in each team doesn't matter. Since we try every combination we know for sure that the players will be split over the teams in the best possible way.

We now have a good starting point. The next step is to look for improvements: we're going to look for swaps of players that will improve the total score. We do this one swap at a time. Here we can again brute-force our way out of this problem: we simply try all swaps and then perform the best one. There are lots of different possible swaps and we also need to recalculate the split over the two teams for each swap, so this uses a lot of processing power. However, modern computers are super fast so with some optimisations we can do a few hundred swaps per second this way.

Especially the first swaps will improve the matches drastically, but we start seeing diminishing returns up to the point where no swaps can be found that are actually an improvement. There might still be some bad matches there, but no single swap will be an improvement overall. In other words: we've reached a local optimum. We almost certainly didn't find the best match-up possible for those 100+ players, but we can't improve this one any further with our current swapping algorithm.

![](../../assets/f21e414e72552a37.gif)

To get out of that local optimum I tried a few things. The first thing I tried is to do a number of forced swaps where the players in the very worst positions are forced into other matches, despite the overall result becoming worse. After a dozen or so forced swaps we start doing normal swaps again. This indeed resulted in a slightly better score, but it did make the algorithm take much longer. Since processing is already taking seconds at this point, performance is very relevant. We don't want players to wait half a minute extra just for this algorithm to finish.

I then tried a different approach: I just leave the first result as it is, and start over again but from a different starting point. I semi-randomly generate a completely new match-up and start doing swaps on that. This will also bring us to a local optimum, but it will be a different one that might actually be better than the previous local optimum.

In practice within 5 seconds we can usually do a couple of retries this way (less if there are more players) and then we simply pick the best one we found. This turns out to produce much better results than trying to force ourselves out of a local optimum, so I threw away that approach and instead we just try a bunch of times. To limit waiting times we simply check how long we've been going so far and do another retry only if we haven't spent too much time yet.

To see how good this could get I tried letting my computer run for a whole night, constantly retrying from different starting points. This produced tens of thousands of different match-ups, all at different local optimums. It turns out that the difference between trying a couple of times and trying tens of thousands of times is actually surprisingly small. This showed us that doing just a couple of retries is already good enough.

![](../../assets/2b02a615d26dcb2c.gif)

### Downsides

So far I've explained how we do matchmaking and why. Now that Galactron has been running for almost two years in this way it's also a good moment to look back: did our approach work out as nicely as hoped? Overall I'm pretty happy with the result, but there is one big choice in here for which I'm not sure whether it's actually the best one: matching everyone at the same time. Doing this gives our matchmaking algorithm the most flexibility to find the best match-ups, but it turns out that players are spread out over the world even more unevenly than I had estimated beforehand, causing problems here.

For example, if we look at a matchmaking round at 20:00 western European time, then the vast majority of those players will be from Europe and the rest of the players will be spread out over the rest of the world. That means that in a matchmaking round of 100 players, there are only a few Australians or South Americans. Those players won't get a good match in terms of ping because there simply aren't enough players in their region in that round.

Solving this requires having even larger numbers of players per round: I think around 300 would be ideal. However, this means either having extremely long waiting times, or having a gigantic playerbase. We'd love to have a playerbase as large as League of Legends, but unfortunately that's not realistic for all but the biggest hit games. The result is that we chose a middle ground: we wait for those 100 players, which can take 5 minutes or even more, and then we just perform matchmaking and accept that the result won't be as good as we'd want for some people. If the number of players is too low then at some point we just perform matchmaking anyway so that waiting times never go beyond a maximum.

While building Galactron we've found very little information on how the big multiplayer games do their matchmaking exactly, but a talk by a designer of Heroes of the Storm (which I unfortunately can't find anymore on YouTube) suggested that at some point in that game, the system was that a match would be started as soon as it could be created with a good enough match quality. In our case this would mean that if there are 6 players who are similar enough in skill and have a good ping with each other, then the match is started immediately. If it takes too long to fill a match, then the requirements are gradually decreased. At some point a player who has waited too long becomes top priority and just gets the 5 most fitting players that the matchmaker can find, even if match quality is lower than desired.

![](../../assets/d3d513881d4d9bf6.jpg)

The benefit of such an approach is flexibility: in areas with lots of players one would get matches much more quickly, while areas with fewer players would get longer waiting times. This kind of flexibility is also nice for pro players: one can make them wait longer so that they only play against others of almost exactly the same skill. Our own algorithm can't diversify like that since players from the whole world are matchmade simultaneously at fixed moments.

In comparison I expect our own method produces slightly better results, because it can juggle with a lot more players at once to find the best match-ups. However, this benefit might not be big enough to weigh up against the benefit of having lower waiting times.

There is one really nice benefit that we get from our fixed matchmaking moments: we can tell the player beforehand exactly how long they'll have to wait for matchmaking to happen. I think waiting is more endurable if you know how much longer you have to wait. Showing how much longer you need to wait is a really nice touch that few other games have.

A direct comparison between the live matchmaking algorithms of Awesomenauts and Heroes of the Storm is unfortunately not possible because Heroes of the Storm has so many more players. Any matchmaking algorithm will do better with more players, so it is to be suspected that regardless of the algorithm, the matchmaking quality in a big game like Heroes of the Storm will be much higher than in Awesomenauts anyway.

### Conclusion

Building a matchmaking system starts with defining what good matchmaking is. No algorithm can produce good match-ups if you don't give the computer rules for what that actually means. In this post I've discussed the rules we use, which are mostly based around skill, ping and premades. Depending on what's important for your game you can add more rules or define them differently.

Just keep in mind that the more rules you have, the less important the other ones become, and every rule you weigh heavier makes the others less important. Restraint and balancing are key here. Also, you probably need a while to finetune the rules further once your matchmaking is live, like we've done with the Galactron matchmaker in Awesomenauts by adding the 'opponent variation' rule later on.

Thanks a lot for this post! Very informative and interesting to read. Thank you so much for posting this, because there is only so few details available out there on the Internet even though it's a very interesting problem, and I believe academics could help a lot on this.



ReplyDeleteReading the algorithmic part made me think a lot about how Genetic Algorithms work - especially the part about swapping people.

It is always interesting to get reminded how problems that look very simple are in fact very complicated to solve

Great post thanks for sharing

ReplyDeleteGreat write-up, thank you!



ReplyDeleteIt seems like you almost reinvented Simulated Annealing. I wonder if the official SA algorithm would perform better. Probably not significantly.

Did you try with other metrics beside the average, like RMS, median, or some percentile? This might give you a bit more control over the extremes (the worst matches), if nothing else.

I did a quick lookup of what Simulated Annealing is. If I understand that approach correctly, I would instead of looking for the optimal swap, try random swaps and accept worse ones as well, as long as they're not too much worse. Each iteration the requirement of how much worse a swap is allowed to be becomes a bit tighter. It's an interesting approach, without trying I can't say whether it would yield better results or not.


DeleteAs for having more control over the extremes: the extremes are mostly caused by players in extreme conditions. Like a premade with players from two continents: no matter how you match those, ping to some players is always going to be horrible. But even in less extreme cases, usually if there is an absolutely horrible match, there is no solution that really solves that without just waiting for more players to have more matching options.

Hello, I am a new player, I read the post and understand pettry well the algorithm to find the best match. I find this way of matchmaking pretty good. But the time of waiting is too long, 5 to 6 minutes of waiting for an average match of 15 minutes it is way too much. This may and will cause people to stop playing the game and keeping new players away from the game... The new generation have no patient and this waiting time for sure will keep them out or get tired of the game pretty quick. If the matchmaking takes maximum 2 minutes to find the best matches this sure will be a big improvement. I really love the game and hope this issue will be reworked to please new and older players, it will be also the best for the game because it will have more players for sure.

ReplyDeleteThank you so much for the post.

ReplyDeleteI've been trying to track the equal player score for several days now. Unfortunately without success. According to the description in the post, you form the differences between all possible player pairings in a game. Afterwards you calculate the average of all differences. The higher the difference, the lower the score.

Unfortunately I can't understand how your algorithm calculates this score. In addition, in the last match from match-up A the average difference is 1979 (playerRatingScore 74%). In the last match from match-up B the average difference is 1832 (playerRatingScore 73%). Even though the difference in matchup A is higher, this matchup gets a better score than matchup B.

What else does this score depend on? I would be so grateful if you could end my sleepless nights.

In practice the calculations for scores are a little bit more complicated than described. I don't remember exactly which extra rules we applied to the Equally Skilled Players score, but here are a few extra rules we've applied wherever we deemed them useful:



Delete-To exaggerate meaningful differences, we sometimes cap them. For example, all pings below 50 are given a perfect score so that improving other ping differences is valued more by the algorithm.

-Similarly we also sometimes cap big differences. For example, we might cap skill differences at 10k, since since a difference of 10k or 12k is equally horrible and we don't care about that difference anymore.

-In some cases we take the power of the scores or differences. Taking a power above 1 results in big differences becoming more important, while taking a power below 1 makes smaller differences a bit more important.

I don't know which of these we actually applied to the Equally Skilled Players score, so I'm afraid you can't exactly simulate our calculations based on this post alone.

(Sorry for the late reply: your post got stuck in the spam filter so I didn't see it before. I hope you didn't have sleepless nights all month... ;) )