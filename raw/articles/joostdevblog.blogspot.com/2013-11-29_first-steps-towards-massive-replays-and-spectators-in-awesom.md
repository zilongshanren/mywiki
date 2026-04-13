---
title: First steps towards massive replays and spectators in Awesomenauts
url: http://joostdevblog.blogspot.com/2013/11/first-steps-towards-massive-replays-and.html
author: Joost van Dongen
published: '2013-11-29'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](http://www.awesomenauts.com). It might not be immediately obvious, but this is actually an incredibly complex problem to solve. We have the very first bits working now, so here is a video in which I show and explain what we have so far:

Our first target with replays is to get them working offline, so you store replays of your own matches on your own harddisk and you can email those files to your friends by hand. Storing and browsing replays through online servers comes after that and is still a long way away. We hope that the offline replays can go in beta before Christmas, but right now it seems like that might still be too early for how complex this all is.

So why are replays so difficult to build? There are a ton of reasons for this. One is that players need to be able to do live spectating. In high-level tournament matches, we currently sometimes get near to 1000 simultaneous viewers for a single match. This is on Twitch, so the bandwidth is handled by Twitch, but for our spectator mode we will need to make that possible ourselves. Handling that kind of user numbers and internet traffic is by itself already a big challenge.

Another problem is that players need to somehow get their replays to a server, live while playing. By itself this is not very difficult, but to keep this from disrupting normal online play, we need to do this in an extremely small amount of bandwidth. We are targeting to stream out a replay from one player to the server in only 1 to 2 kilobyte per second. The total size of a 20 minute match will then be around 2mb. Streaming all data in so few bits is an interesting challenge, but I think it is quite achievable.

Another problem is version management. We release lots of patches for Awesomenauts, and most patches change significant things in our gameplay logic. That means that if we rely on that gameplay logic for playing back replays, then stored replays will often not be playable anymore once we release a patch. A solution for this would be to add version management to the gameplay code, but that would add a kind a code complexity that we definitely don't want there. And I haven't even mentioned how sensitive to bugs that would be... Another solution would be to store legacy versions of the game to play older replays, but that would produce very high loading times when switching between reviews, and would mean loads of downloading to get all those older game versions.

Our solution for this version problem is to store only graphical data in the replay. This way if gameplay logic changes, it doesn't matter for stored replays, since those don't use the gameplay logic anyway. The demo shown above already works like this. However, this does mean that we cannot use any of the current gameplay code or network packages for the replays. We need to rebuild it all from the ground up in a different way. That is why the demo above still lacks animations and bullets and pickups and such: they have not been rebuilt for replays yet.

Another issue in the replays implementation is server bandwidth and loading times. If players view lots of replays, this will cost us a lot of bandwidth and thus a lot of money. Also, if players need to download the entire replay before they can watch it, then waiting times might be long. We even want players to be able to immediately skip to specific moments in the replay without downloading everything in between. With this in mind, the replay system again becomes a lot more complex.

There are several other challenges in implementing replays and spectator mode, but these are the most important. The video shown actually solves the basics of several of those already: there is quite a bit of interesting code architecture behind it. This is also why it took so long before we got anything to show at all: storing and playing character positions is by itself not all that difficult, but doing it in a way that will work with the above issues makes it a lot more time-consuming to implement. I expect I will be able to do a great talk or series of blogposts on this once the whole replays system has been built...

As a conclusion to this blogpost, I would like to say that this is a mightily interesting and fun challenge! We at the

[Ronimo](http://www.ronimo-games.com)coding team are greatly enjoying this task: coding puzzles are the best puzzles!

Hey! Nice job!

ReplyDeleteI suggest you checking spectator mode of Starcraft 2 - It's really nice, because one can see there whole game played again, but... They also planned on implementing(idk if they implemented it) co-replays - which was an option of watching replay together, and ability to take control over some player at any given moment of game - so, if Awesomenauts clan had couch and lost match, couch could have said "Look, you could have done something like this". Of course it's not as spectacular as in SC, and means implementing good AI, but it's a nice little fact that you may be interested in.

Anyway, good job!

Looks nice so far! Are you willing to share more technical details? Like what approach are you using (like incremental with key frames or samples with interpolation)? and are you packing values together in single variables to save space (and how)?

ReplyDeleteAlso: The 10kb per 10s you have at the moment is without bullets?

I'll be writing about it more later on, but to give some more details: we bitcrunch all our data, so a float that doesn't need a lot of precision might go into 9 bits or something like that. For example, a 2D position is stored in 26 bits (13 bits for X and 13 bits for Y). The 10kb currently is without bullets and animations, so LOTS of data is missing. However, it is also with way more position keyframes than needed, so I expect the total will stay beneath 20kb per 10s.

DeleteNice nice! I'll be looking forward to more updates :)

DeleteNeed more Joost video's. NEED!

ReplyDeleteI'll try some more video stuff in the future, curious to see people's reactions. :)

ReplyDeleteNice read!



ReplyDelete2MB for the replay of a 20m match sounds really low. I'm guessing lag frames and such will be stored from a host perspective?...

When you guys finish the replay system will it be available from the ronitech engine or will it be specially designed for awesomenauts?

We don't know yet whether every player will store his own part of the replay (less lag issues, less bandwidth per player, more complexity in piecing the parts together).


DeleteMost of the replays system will only be relevant for Awesomenauts, since most of the logic and optimisations are game-specific.