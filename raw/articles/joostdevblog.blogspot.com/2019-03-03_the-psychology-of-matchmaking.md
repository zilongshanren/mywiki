---
title: The psychology of matchmaking
url: http://joostdevblog.blogspot.com/2019/03/the-psychology-of-matchmaking.html
author: Joost van Dongen
published: '2019-03-03'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](http://www.awesomenauts.com/)matchmaking. However, the psychology of matchmaking is a very important topic when designing a matchmaking system, so today I'm going to discuss it anyway. For science! :)

While we were designing the Galactron matchmaking systems I did quite a lot of research into how the biggest multiplayer games approach their matchmaking. The devs themselves often don't say all that much about it, but there's plenty of comments and analysis by the players of those games. The one thing they all have in common, is that whatever game you look for, you'll always find tons of complaints from users claiming the matchmaking for that particular game sucks.

![](../../assets/e60b87269f7dee9d.jpg)

My impression is that no matter how big the budget and how clever the programmers, a significant part of the community will always think they did a bad job regarding matchmaking. Partially this might be because many games indeed have bad or mediocre matchmaking, but there's also a psychological factor: I think even a theoretical 'perfect' implementation will meet a lot of negativity from the community. Today I'd like to explore some of the causes for that.

The first and most obvious reason is that matchmaking is often a scapegoat. Lost of match? Must be because of the crappy matchmaking. My teammates suck? Must be the crappy matchmaking. Got disconnected? Definitely not a problem in my own internet connection, must be the crappy matchmaking. Undoubtedly in many cases the matchmaking is indeed part of the problem, but these issues will exist even with 'perfect' matchmaking. Sometimes you're just not playing well. Sometimes a teammate has a bad day and plays much worse than they normally do. Sometimes your own internet connection dropped out. No matchmaker can solve these issues.

There's a strong psychological factor at play here: for many people their human nature is to look for causes outside themselves. I think this is a coping mechanism: if you're not to blame, then you don't have to feel bad about yourself either.

Of course there is such a thing as better or worse matchmaking. That players use matchmaking as a scapegoat shouldn't be used as an excuse to not try to make better matchmaking. But it sure makes it difficult to asses the quality of your matchmaking systems. Whether your matchmaker is doing well or not, there will practically always be a lot of complaints. The more players you have, the more complaints.

For this reason it's critical to collect a lot of metrics about how your matchmaking is objectively doing. We gather overall metrics, like average ping and match duration and such, but we also store information about individual matches. This way when a player complains we can look up their match and check what happened exactly. This allows us to analyse whether specific complaints are caused by problems in the matchmaker, are something that the matchmaker can't fix (like a beginner and a pro being in a premade together) or whether the user is using matchmaking as a scapegoat for something else.

![](../../assets/ce8bcdb4778e1120.jpg)

Another problem for matchmaking is that player's don't have a single, predictable skill level. The matchmaker matches a player based on their average skill, but how well they actually play varies from match to match. One match they might do really well, and then the next they might do badly. For example, maybe the player gets overconfident and makes bad decisions in the next match because of that. Or maybe the player is just out of luck and misses a couple of shots by a hair that they would normally hit. Or maybe the player got home drunk from a party and decided to play a match in the middle of the night, playing far below their normal skill level. These are things that a matchmaker can't predict. This will often make it seem like the matchmaker didn't match players of similar skill. Sometimes this might result in a teammate who would normally be as good as you but happens to play like a bag of potatoes during this one match in which they're in your team.

While this problem is not truly solvable by matchmaking, there are some things developers can do to improve on it. For example, in Heroes Of The Storm you select your hero before you go into matchmaking. This allows the matchmaker to take into account that you might be better at some heroes than at others. If it detects that you're playing a hero that you haven't played in a long while, then maybe it should matchmake you below your skill level. I have no idea whether Heroes Of The Storm actually does this, but it's certainly a possibility. This would allow detecting some of the cases in which a player is normally really good, but is currently trying something new that they haven't practised yet.

![](../../assets/71809d9e394202b3.jpg)

However, this particular trick comes at a heavy cost, which is why we decided not to put it into Awesomenauts: if players select their hero before matchmaking happens then matchmaking is severely limited in who can play with whom, which damages other matchmaking criteria. (I've previously discussed this in my blogpost about

[why you need huge player numbers for good matchmaking](http://joostdevblog.blogspot.com/2014/11/why-good-matchmaking-requires-enormous.html).)

A very different kind of psychological aspect is that players are often bad at estimating their own skill level. The following example of this is something that I have no doubt will be recognised by many people who play multiplayer games. A while ago I played a match in which a teammate was constantly complaining about how badly I was playing and how I was causing us to lose the match. However, looking at the scoreboard I could see that he was constantly dying and was by far doing worst of all players in the match. Apparently that player didn't realise that he was much less good at the game than he thought he was.

There's more to this than anecdotal evidence however. The developers of League of Legends have described that on average, players rate their own skill 150 points higher than their real MatchMaking Rating. (That part of

[the post](https://support.riotgames.com/hc/en-us/articles/201752954-Matchmaking-Guide)has been removed in the meanwhile, but you can still find it

[here on Wayback Machine](https://web.archive.org/web/20161111092742/https://support.riotgames.com/hc/en-us/articles/201752954-Matchmaking-Guide#q5).) As they also mention there, psychology actually has a term for this: it's called the

[Dunning-Kruger effect](https://en.wikipedia.org/wiki/Dunning%E2%80%93Kruger_effect). A League of Legends player analysed a poll about this

[here](https://boards.euw.leagueoflegends.com/en/c/player-behaviour-en/3JcpguAs-the-dunning-kruger-effect-in-lol-and-some-correlations)and gives an excellent explanation of how it works:

"According to the Dunning-Kruger-Effect people overestimate themselves more the more unskilled they are. This isn’t caused by arrogance or stupidity, but by the fact that the ability to judge a certain skill and actually being good at that skill require the same knowledge. For example if I have never heard of wave management in LoL I am unable to notice that I lack this skill, because how would I notice something if I don’t even know it exists? I would also not notice this skill in other people, which is why I would overestimate my own skill if I compared myself to others. This it what causes the Dunning-Kruger-Effect." - Humpelstilzche |

As some readers suggested, all of these psychological factors invite an interesting thought: would it help to give players more control? After all, if you have no control you blame the system, while if you do have more choice, you also have yourself to blame and maybe accept the results more. Giving players choice over matchmaking is in many ways old-fashioned and reminds me of the early days of online multiplayer, where you selected your match yourself from a lobby browser. The common view these days seems to be that players expect a smooth and automated experience. They don't want to be bothered and just want to click PLAY and get a fun match. Or at least, most devs seem to assume that that's what players want.

For Awesomenauts I've actually been curious for a while what would happen if we removed the automated matchmaking and instead relied entirely on opening and selecting lobbies. The modding scene would surely thrive a lot more that way, but how would it affect player experience and player counts? It would be a risky change and also too big a change to just try though so I doubt we'll ever get to know the answer to that question. Also, I'm not sure whether our current lobby browser provides a smooth enough experience for making it that important.

I do think it's interesting to explore this further though. I wonder what would be the result if matchmaking were from the beginning designed around being a combination of automation, communication and player control.

Before ending this blogpost I should mention one more psychological aspect of matchmaking: the developer's side. As a developer it can be really frustrating to get negative comments on something you've spent a lot of time on. Understanding why can help in coping with this frustration. Just like matchmaking can be a scapegoat for players after losing a match, the psychology of matchmaking can be a scapegoat for developers after getting negative feedback from players.

None of the psychological factors discussed in this post are an excuse to just claim that the matchmaking in a game is good despite players complaining. However, for a developer it's really important to realise that these factors do exist. Understanding the psychology of matchmaking allows you to build better matchmaking and helps to interpret player comments. I have no doubt that I've only scratched the surface of this topic, so I'm quite curious: what other psychological aspects influence how matchmaking is experienced by players?

I think a big part of the problem is that you want to rank players for two different purposes: one, you want to have an estimate of players' skill that you can use in matchmaking and two, you want a competitive leaderboard.





ReplyDeleteI think it's best to separate these two: the leaderboard needs to be "fair" in certain ways the raw matchmaking skill estimate doesn't. For instance, in most games you are punished on the leaderboard for quitting ahead of time, but if this affects matchmaking then the sore loser will get easy matches as a reward - is this desirable?

Another thing is that you for fairness reasons want to reward players for playing. If you're the top player, you shouldn't be able to keep that position on the leaderboard forever by not playing! But the matchmaking might still want to assume you've kept most of your old skills if you start playing again.

If you split matchmaking and leaderboard ranking, and keep the former hidden from players (or viewable only in a very reduced form, e.g. three levels, no ranking), you are free to experiment, and use every machine learning trick in the book to get a good estimate for the true skill level, without worrying that the metric will be gamed.

You can for instance incorporate character choice. It's true you can't do it before matchmaking, but you can do it afterwards. You will want to reduce the skill level penalty for losing with an unfamiliar naut, or simply getting a horrible match up character wise.

Yeah I agree that leaderboards and MMR (MatchMaking Rating) shouldn't be the same thing like they are in Awesomenauts. For this reason in Swords & Soldiers 2 we chose to have the MMR under the hood and separate from the leaderboards.




DeleteHowever, it's a thorny subject any way you implement it. In games where MMR and leaderboards are separated you can find lots of complaints from players who say they are matched with players who aren't near them in the leaderboards. Which is kind of the point of separating MMR and leaderboards...

Reworking that for Awesomenauts was too much work though. We have a basic prototype of a new leaderboard that's separate from MMR, but the work involved in really making that cool, fun and rewarding proved too much to be feasible so long after launch.

I don't think any of that contradicts my point in the blogpost, by the way. Even with 'perfect' matchmaking and leaderboards the psychological factors mentioned here would still generate a lot of complaints.

What are the stats you gather on the objective quality of matchmaking? Difference between player levels? Ping? Those little graphs are very intriguing!

ReplyDeleteThe screen I posted shows the result of matchmaking rounds over time. There's a matchmaking around every couple of minutes and each round a lot of players get matched simultaneously. The graph shows for each round the quality of the best, worst and average match that was created. If you click a round, you get details on every match that was created in that round: ping, whether players played together during the previous match, premades and MatchMaking Rating of each player.



DeleteThe grid in the screenshot shows ping between every player and every other player (which is important because Awesomenauts is peer-to-peer). Red means bad ping, green means good ping.

There's more but that's not in the screenshot and I'm too lazy to write a complete book about it here. ;)

I know it's not as easy for games that aren't 1v1, but I really like the way match making is done in sites like lichess.org








ReplyDeleteThe players have a lot more freedom to play against who they want. Also the elo is shown.

If a player rated 1100 and a player rated 2400 want to play together in a rated game, they can.

When you look for a game to play, you can use their quick pairing to let the match making algorithm do it's thing. You can also create your custom games where you determine the elo range, time controls, etc. And their match making algorithm will find people that fit into your criteria.

They have systems in place to detect hackers or cheaters that abuse the system. If they are detected, the elo is refunded to those that lost against them.

That to me, gives a lot of transparency to their match making. It's very very hard to want to blame their system for a loss. Also a good player on a new account gets placed really fast where he belongs because he can decide to play against better players right away, he doesn't need to destroy low elo games.

One other point, I don't know if it's due to the nature of chess, but lower rated players will often challenge higher rated players and play hundreds of consecutive games even though they lose almost all of them. It just goes to show that the imbalance isn't as bad when you have the control to choose the game. Players can view that as a learning experience and they don't need to be pushed into a casual game where everyone feels like they are wasting their time.

Anyway, I'm sort of rambling, but hopefully this gives you ideas.

Giving players more control is an interesting thought. In many ways it's old-fashioned: in the early days of online gaming most games worked like that, while today very few do. Players kind of expect a smooth and automated experience. They don't want to be bothered and just want to click PLAY and get a good experience. Or at least, most devs seem to assume that that's what players want.


DeleteFor Awesomenauts I've actually been curious for a while what would happen if we removed the automated matchmaking and instead relied entirely on opening and selecting lobbies. The modding scene would surely thrive a lot more that way, but how would that affect player experience and player counts? It's too big a change to just try though so I doubt we'll ever know the answer to that question.

I've actually added a bit to my blogpost based on your and Don Reba's suggestions. Thanks for sharing your thoughts! :)

DeleteOr even better: Have both. I am most fond of the idea of having quick-play button but also a server/lobby-list underneath it. For awesomenauts it could have been custom games where there is a checkbox Ranked/unranked where custom game rules are blocked off. This so it qualifies to get ranks on leaderboards and rewards at the end of the game.



DeleteIf you press quickplay custom you get thrown in whatever lobby unranked, with quickplay ranked you get thrown in any lobby with ppl of your rank. You can also get to the list but are restricted to how far your rating differences from the average or individuals. For parties the entering rating can be based on the party average.

I think players that are looking for indie titles maybe want more control than very casual players in triple A titles. I can't prove it though but still interesting thought that it's based on the audience of your title. Games like Team fortress 2 are also still kicking eventhough it had a very ugly ui serverlist for a very long time.

I'm glad I could provide some feedback. I'd suggest that you create an account on lichess.org and play a couple games to get a feel for the way their system works. (Or watch people play bullet chess on Twitch.)




DeleteYou'll notice that lichess has different rating system for different time controls. From the front page, you have access to quick pairing. Even without making an account. The experience is very smooth.

They have automated tournaments in many time controls and even for custom chess rules: https://lichess.org/tournament

The match making algorithm on tournaments is really amazing, you should check it out. It's completely different than what you have considered in this post. The matches are rated. (Probably hard to adapt for non 1v1 games, but maybe it gives you ideas.)

Have you given much thought to finding a more social engineering approach to addressing player complaints? It's easy for players to scapegoat the matchmaking system because they view it as a black box they have no control over. But they might be much less inclined to do so if they were somehow involved in the process and saw the result as their responsibility. This might even call for the algorithm to be simplified and be made less "perfect".

ReplyDeleteJean-David Moisan had a somewhat similar though above, I've replied there to both your post and his.

DeleteI've actually added a bit to my blogpost based on your and Jean-David Moisan's suggestions. Thanks for sharing your thoughts! :)

DeleteI think the nauts matchmaking does what it has to do. What I see on a daily basis is that only the really inexperienced or new players tend to (still) blame the matchmaking. This is partly because they wrongly judge players skill levels based on a single game performance.






ReplyDeleteWhat I miss in this blog is emphasizing on blind character selection. It does say a little on different performances based on human error and character experience, but not so much is said on matchup.

In nauts you have no idea of telling what characters you will be facing and sometimes teaming with. I believe players that don't have the knowledge or skill have from this dunner-kruger-effect and mistake matchup with overall player skill on single game performance -> conclusion = poor matchmaking. This isn't so surprising as only a handful of players understand the complexity of balance. Nauts is a game that is heavily influenced by hardcounters.

You also won't know how well your teamplay is. Sometimes the weakest nauts in damage numbers can be the greatest assets to the team (scoop/yoolip/LUX). Sometimes the best counters are also the least versatile. The pickrate is heavily influenced by winrate. The pub meta revolves around picks that have the least chance of being countered. For the inexperienced eye the choices don't matter and can wrongly judge player skill.

Sometimes people just believe the opponent is infinitely better than them while they are the same rank, or think a teammate is incredibly bad by counting his death stats, eventhough he's just trying setting things up to make a difference. Judging the matchmaking for this is an easy escape and scapegoat option. Perhaps what I described is something to talk about for future blogposts?

I agree that character selection is certainly a big factor here: if you happen to have the right team for what your opponents play, you can win a match even if the opponents are more skilled.



DeleteSome big MOBAs approach this by having a draft system before a match in high league play. We've considered this as well, but we think it's too hardcore for the majority of players, and it turned out to be too much work to make just for high league players. It would definitely have been a nice and interesting feature though.

Some games also solve this by allowing you to switch class mid-match so you can counter your opponents. I think Overwatch is an example of this? We considered this for Awesomenauts, but this approach doesn't fit a MOBA well since it kind of invalidates the whole point of levelling your hero during a match and making important choices. A choice is less interesting if you can revert it at any point.

'The state of overwatch' is a video by the professional player Seagull where he explains the psychology of matchups. It's a very interesting video and shows that even a big game like overwatch runs into a lot of similar problems. I highly recommend watching this and look for similarities.






ReplyDeleteOne of the subjects he mentions is the switching between hero's during the match. It can cause a lot of problems and disturb the flow of the game, instead of playing the game people are arguing whether to switch or not. This freedom can make the player experience better but also worse. The problem is very apparent in a SoloQ environment where the tactics of assembling a full team composition is not available to you, while premades have a huge advantage of finetuning the composition. Premades can adapt on the matchup as a group which makes it very hard to lose.

One of main questions Seagull tries to answer is: "Can there still be a fun environment for players that don't play in parties"? Well first of all, in my experience these games always get more serious over time no matter what. People that keep playing will get better and better and the meta becomes less rough around the edges. It doesn't necessarily mean that people that win are always really skillfull and talented, because being more knowledgeable can get you very far. The gap between new and old players knowledge and experience continues to grow over the years. I think no matter how you change the game, it will overall always go from innocent to more unforgiving to hardcore for elite players. The SoloQ environment becomes a lot harder as a result of this.

I think that Seagull is mainly dissapointed in what the meta has become and I can relate to this with nauts. In a way determining skill in a multiclass game is also a downfall. In the original post it's mentioned that players perform worse or better with certain characters that they haven't practised with. I agree, however people are also worse or better with certain characters depending on how the relation between the skill curve and effectiveness of character is designed. This isn't necessarily wrong but it does raise the question if the matchmaking can even determine the right rank for players.

I think it's frustrating to lose versus players that are clearly worse than you and have to put minimal effort in to win, just as always losing against better players while you put all your effort into it. The story from both sides are really discouraging and I don't think there really is a single good answer. For example, the 'noobtube' in call of duty was one of the most hated weapons, but it also gave worse players a chance and therfore brought the game to a wider audience. Another example is the pyromaniac from team fortress 2 who will most likely win in small rooms by walking at you. Again, players that don't really understand the complexity of the game can't judge the difficulty of playing a matchup. This may lead to praise or criticising players or blame towards the matchmaking.

A way to solve this is to emphasize on different rewards. The big objective is to win the game, while a smaller objective is to win a round. An even smaller objective is to get a kill. I think in general less skilled players should never take a whole game or even a round, but it's wrong if a pro player never dies. Just like the examples of other games it's better if these strategies sometimes work but aren't so reliable. In nauts however we've seen many approaches where the least depth or hard characters are also strong and reliable. It makes it even harder for the player to deal with matchmaking cause the game has so many hardcounters that can't be dealt with at any point in the match.

You make a lot of good points. Many of these things have endlessly been discussed internally at Ronimo. For example, Ayla received a big rework because she was easy to be strong with while at the same time being difficult to counter. Such reworks are really difficult though: we wanted to keep the core of the character the same since that's what makes her her. This limits how much she could change. Also, we knew that whatever change we did, there would always be a vocal group of players who would hate it because they enjoyed playing her as she was.



DeleteThe issue that a game becomes more hardcore over time is a very challenging topic. It makes the game less appealing to beginners, but at the same time makes it more interesting for hardcore players to spend hundreds or even thousands of hours on it.

A particular challenge there is indeed whether there should be mechanics to give beginners their occasional success, like you mention with the Pyro in Team Fortress 2. Originally Awesomenauts had crits with pure random, and those occasionally gave you several crits in a row, giving you a very small chance at doing enormous damage. That's great for beginners because it lands them an occasional kill against a better player. However, hardcore players tend to dislike luck, so at some point we changed that into crits that were better spaced out, and eventially even removed crits altogether. While a lot of players rejoiced at those changes, I'm still not sure whether that really was a good choice. It made the game better for competitive play, but maybe also worse for more casual players.

After rereading this I still want to make a few points. The core audience get more needy, people have spend hundreds of hours into a game and start to know the game inside out. A small singular audience grows out to many groups of different opinions. In some way balancing and insight on game direction is a form of content they will get hyped for. Eventhough players can be rude in a sense it's just the fanatical feeling of "perfecting" what is already there they grew to love.











DeleteA lot of games aren't old fashioned anymore. They aren't DRM-free and are handled by large companies. The lack of freedom with it can be bothering. I don't quite understand why more options it can't run alongside quick-play/click and play style.

I think the key here is to have options that can be found whenever the player is ready for them. Maybe everyone starts out using the quick-play button, but as time continues some of the players notice some of the game environments don't match their wishes so they put search the right server manually. Without such option the player will always be forced to play in the same game environment.

In nauts there is the choice of selecting your own character. Each has their own skill floor and skill ceiling and that's fine. A character like Yoolip is straight-forward but also more limited, while a character like Ted Mcpain is complex and has more options. You can expect someone will go from one character to the next in his in game journey because ppl get more knowledgable, practised and hardcore.

However in nauts, players can't really escape the main matchmaker and blind character selection. So then the question becomes how can you achieve true occasional success assuming the matchmaker finds good games? I think it's a balance between skill versus %power/reliability.

Of course this raises the question what would happen if skill A was easier, more reliable and stronger than skill B. Well, This would make skill B completely obsolete. Of course awesomenauts had a good run of patching these things out, but it's pretty clear that in seperate matchups this can still exist to the point you will never win a one-on-one. The occassional success goes from "kill level" to "match point level". And for hardcore lobbies this can drive players insane.

I think the psychological difference is that dying from a pyromaniac is a single death and you can instantly move on, however in nauts people that know the bad matchups have to sit down demotivated for a whole lengthy game. This frustration can lead to all kinds of scapegoating.

I do think that winning occasional full matches can be okay. What I'm trying to say is that luck is fine as long as it's not predictable before the outcome. I really believe players don't want to know the outcome of luck beforehand and because of poor knowledge sometimes scapegoat the wrong aspects of a game. In Call of duty Deathmatch noobs were able to take games from pro's cause it's heavily reliant on first-sight first-kill and bumping into as many players as possible. Pro's still had better chance of survival and getting kills somewhat faster, but it's not impossible for a noob to get surrounded by a lot of people to take the lead.

So in conclusion I think in general people don't like luck in awesomenauts because of the lack of control beforehand that leads to predictable outcomes. And that the game doesn't bring optional stuff outside ranked mode (that has a stable enough audience) that really changes the game experience what makes the player feel somewhat in control(serverlists/gamemodes/drafts).

Influence on the game as an individual or small group sharing your opinion is hard, at the same time it's hard to streamline the game for players after all these years by the devs. It's a singular hub, changes apply to everyone. If your main gets nerfed your entire game experience might be nerfed alongside of it.

I think your point is that there should be more modes, control and options? The problem with giving players more choice, is that it splits the multiplayer community. That's fine in gigantic games, but in a smaller online multiplayer game having a lot of modes and options will quickly result in a bunch of them being empty or, even worse, all of them being too small to really sustain themselves. That's why Awesomenauts has one main matchmaker and deliberately calls custom games an extra: to keep the matchmaker going despite not having millions of active players.

DeleteI'm a little sad that one factor of match-making was completely left out of this post: Getting a match going at all. It's all fine and dandy to have a well thought-out algorithm for putting together a match when there's a huge player pool. However a lot of games i played online (most recent in memory: war thunder, ff14 dungeon queues/pvp) suffer not from "bad matchups", but from taking forever to put them together.



ReplyDeleteThey all show extremely rudimentary, and often completely worthless information, for example the "this many players are waiting" in war thunder and "estimated matchup time" in ff14. However none of them show simple tools such as graphs that show the history of players having queued, and matches achieved, to help players work out at which days in the week or times of the day it'd be easier to actually get playing.

Which is doubly confusing to me, as players being able to actually get into games would end up pulling friends into it when they have a higher chance of actually making it happen, as opposed to everyone just trying, failing, and giving up forever.

The reason I didn't mention that topic here is that it's kind of out of the scope of what I wanted to talk about. However, I totally agree that getting a match at all is a very important issue! I've actually written several blogposts about this a while ago:



Deletehttps://joostdevblog.blogspot.com/2014/11/why-good-matchmaking-requires-enormous.html

https://joostdevblog.blogspot.com/2015/09/designing-matchmaking-for-smaller.html

Oh yeah, i remember reading those back in the day. They were interesting and full of insights. I'm still surprised why literally no gaming company i've ever seen doesn't attack the "small multiplayer base" by making the UI more useful and informative for humans.

Delete