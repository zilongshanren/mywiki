---
title: Entertaining players while waiting for matchmaking
url: http://joostdevblog.blogspot.com/2018/01/entertaining-players-while-waiting-for.html
author: Joost van Dongen
published: '2018-01-28'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](https://www.awesomenauts.com/)with our initial approach to this and how we made waiting a bit less boring later on.

Until the launch of the Galactron update in 2016, this is how it worked in Awesomenauts: when you started searching you got into a matchroom right away. You selected your character, and then you had to wait in the loading screen until the match was full with 6 players. This could take several minutes and there was no interaction possible whatsoever: just a loading screen that says the match isn't full yet. To show progress we did have six tickboxes that showed how many players had joined and whether they had already selected their characters, but that was it.

![](../../assets/56c8603fc8f7a423.jpg)

A static screen with no interaction possible is probably the most boring type of waiting imaginable. Compare this to current Awesomenauts, where you wait in the menus instead of in a loading screen. Still not ideal, but this means that while waiting you can chat with other players, check out the skills and items of all characters and watch replays and live matches. Awesomenauts has a system where it lists the ten most exciting matches happening right now and also automatically selects a match of the day that you can watch. We hardly advertise watching replays while waiting though, so I think many players don't realise that you can watch a live match or replay while waiting for matchmaking.

An important thing to realise when thinking about waiting times is that on PC, players can simply alt+tab and browse the internet while waiting. This isn't possible on console, but there's always that other option: mobile phones. I don't have any statistics on this, but I wouldn't be surprised if a lot of players ignore menus, replays and chat during waiting times and just randomly browse the internet instead.

While I think current Awesomenauts is a huge improvement in terms of diversions while waiting for matchmaking, I don't think it's ideal. Waiting times for a proper match can be rather long (which is

[unavoidable](http://joostdevblog.blogspot.nl/2014/11/why-good-matchmaking-requires-enormous.html)if you don't have a giant playerbase and prefer better match-ups over quicker matchmaking) and clicking through menus isn't the best entertainment in the world. I like the solution that PlayerUnknown's Battlegrounds has: players get thrown into a little area where they can walk and jump around, punch each other, voice chat and generally goof around a bit. It's still clearly a waiting area, but it's so much more fun and interactive than a menu or a replay.

![](../../assets/b2abc00e5a851515.jpg)

Even better is to have some kind of mini-game while waiting. During early development of Awesomenauts we experimented with having a little death match arena where you played until the real match started. It's similar to what PlayerUnknown's Battlegrounds does, but even more game-like since it's real deathmatch. I can't quite remember why we decided not to put this into the game, but I imagine the mean reason was probably a lack of time: we were making a really big game with a small team and needed to cut features in order to finish it before funds ran out.

There might also have been concerns internally that it might be frustrating to be in a deathmatch game and then we thrown out into the main game all of a sudden. Knowing that it can end any moment might potentially make that deathmatch more frustrating than fun. In

[Swords & Soldiers](http://www.swordsandsoldiers.com/)we solved this frustration by letting the player do single player while waiting and storing the state of that single player as soon as an online match started. This way the player could continue the single player session after having finished the online match. However, this approach doesn't work with an online deathmatch. Still, I think having gameplay instead of menus is probably preferable anyway.

![](../../assets/761642091d308038.jpg)

Despite all of this I do think we had some nice touches in the original waiting screen in Awesomenauts. One is that we showed the maximum waiting time left. Waiting for a few minutes is a lot more acceptable if you actually know how long you're going to be waiting than if you don't know whether you need to wait one more minute or ten. If after a few minutes the match was still not full, it would just start with fewer players and add bots to complete the teams. This way the player had a guarantee that when the timer ran out, gameplay would definitely start.

In the new matchmaking system we also want players to know how long they're going to wait, so we still show a number that says how long it takes until the next matchmaking round happens. Only now it's shown in the main menu instead of in the loading screen. This can be frustrating if the time is long (worst case it can be as much as 7 minutes), but at least you know what you're getting into.

In the waiting screen of the old version of Awesomenauts you also heard the theme song of the character you had selected. Every character in Awesomenauts has their own jingle and this adds loads of personality to the game. Since this was basically the only entertainment during this waiting screen we even made these songs longer: jingles for the initial characters were only around 20 seconds, while later on we started aiming for 1:30 minutes to reduce repetition.

In the current system where you don't select a character until the match is full we do miss this great opportunity to let the character jingles shine. Instead you now only hear a short bit of the character jingle after selecting the character. The other way to hear these jingles is in the menus while browsing character stats. Having less focus on these awesome theme songs is a pity.

![]() |

Ideally your multiplayer game has an infinite number of players and you can find equally skilled opponents right away. However, very few games live in this ideal world, so everyone else needs to think cleverly about how their matchmaking works. Just building basic matchmaking and assuming it'll work out isn't going to cut it. If you're interested in reading more on this topic I recommend reading my previous post on

[designing matchmaking for non-gigantic communities](http://joostdevblog.blogspot.nl/2015/09/designing-matchmaking-for-smaller.html)as well.

In the end I think the main reason we ended up with that waiting screen in Awesomenauts for years is that we underestimated how hardcore our community would be. We had designed Awesomenauts as a casual, fun alternative to the other MOBA games. We thought starting with bots right away and adding players as soon as they came online was way more fun than waiting for a full match. Our players disagreed: joining a match that's already in progress is a disadvantage since the bots might have already lost some ground by the time you replace them. Matchmaking issues quickly became the number one complaint about Awesomenauts in our community, so we increased the waiting time before a match actually starts to 2 minutes (or less if the match is already full). This did increase the chance of everyone being there at the start, but we still got complaints about matches not always being full, so we increased the waiting time even further to 4 minutes.

Since we thought we were making a more casual game we hadn't anticipated that our players would prefer long waiting times to be able to play in a more competitive way. We did adjust the system based on this feedback, but the result was waiting in a loading screen. I'm glad we got to improve that situation when Galactron launched later on.

Interesting read as always. I'm just curious about two things. Was there a technical reason why the menu mini-game was removed? That really was a good way to pass the time as it was engaging to some degree. Watching replays and stuff is entertaining, but it's rather passive, you're not actively doing things. The minigame with the ship was a good diversion and even though it was during long queue times I didn't mind as much. Also, a thing I've always wondered, is why can't we use the "Test" feature of the nauts in the same way that we can view replays. I think that's a feature that would be SO useful to try things out and "kill time" while waiting for queue. I never use the test feature because it takes you out of the queue. It's another one of those little utilized features of the game, and if could be used while waiting for the queue you'd be able to practice and experiment with characters.

ReplyDeleteHas the minigame easter egg been removed? I'm not aware of that, I'll ask in the office whether anyone knows what's up with that.


DeleteBeing able to do testmatches (and even full botmatches) during matchmaking is indeed a good idea and one that we've discussed internally. The reason you can't do that at the moment is purely technical: getting into a match brings the game into a different state (even if it's an offline match) and that isn't compatible with doing matchmaking at the same time. Of course this can be fixed, but doing so is surprisingly complex with how our systems work and prone to introduce a lot of bugs. Had we designed the system from the start with this in mind, it would hardly be a problem, but at the moment adding this is unfortunately a lot more work than one might think.

The button for the minigame is still there, but it doesn't do anything except disappear when it's clicked, so I'm assuming the removal was not intentional.

ReplyDeletePutting players in a waiting area before a match starts is not a new concept. Super Smash Brothers Brawl did this with its online by putting the player into a plain arena with a punching bag. Referencing a modern game like PUBG makes it sound like this idea is innovative when it's not. People play games to feel like they're in control because real life can feel very hectic and swallow you up. That's why people getting frustrated when they die and have to wait for a respawn timer before they can do anything. No control = no fun.

ReplyDeleteIndeed, it's not a new thing. PUBG is just an example.

DeleteIt sounds like you regret not implementing something similar. Initially the restriction was funding and time, but after the game released why didn't you revisit that idea?

DeleteAfter release the reason not to build this was still time: there's an infinite number of things we could improve or expand on the game and chose to work on other things than this particular one. For example, we had to implement the Kickstarter stretch goals (modding, spectator mode, replays, new matchmaking, new map, new characters) and many other things.

DeleteThere is still hope, maybe this can be the next addition to nauts? When I'm drawing, I find that the first 80% goes by really fast and I could spend a really long time on the last 20%. So what I'm saying is: a feature like this that's even 80% polished is many times better than nothing. Right?

Delete