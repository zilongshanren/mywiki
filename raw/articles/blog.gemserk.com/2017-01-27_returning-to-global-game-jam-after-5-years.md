---
title: Returning to Global Game Jam after 5 years
url: https://blog.gemserk.com/2017/01/27/returning-to-global-game-jam-after-5-years/
published: '2017-01-27'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

After [five years](https://blog.gemserk.com/2012/01/30/our-participation-in-global-game-jam-2012-uruguay/) of Global Game Jam vacations, we joined this year’s the last weekend.

It was a really enjoyable time and we had a lot of fun. In this blog post I would love to share my experience as some kind of postmortem article with animated gifs, because you know, animated gifs rules.

The Theme of this jam was “Waves” and together with my team we did a 1v1 fighting game where players have to attack each other by sending waves through the floor tiles to hit the adversary.

Here is a video of our creation:

My team was composed by:

[Franco Zucchi](https://twitter.com/pencilwing)- Art[Manuel González](https://mazzuri.tumblr.com/)- Art- Joaquin Bello - Code
- Rodrigo Arigón - Code and multiple stuff
[Leandro Mesquita](https://twitter.com/leanmesquita)- Game Design[Ariel Coppes](https://twitter.com/arielsan)(me) - Code- Ignacio Fernandez - Audio, he wasn’t part of the team but he helped us.

Here are links to download the game and to its source code:

[Global Game Jam](http://globalgamejam.org/2017/games/ripple-rivals)[Source code](https://github.com/acoppes/rippleppl), if you are really thrilled on how we manage to do such a great game.

# Postmortem

Developing a game in two days is a crazy experience and so much can happen, it is a incredible survival test where you try not to kill each other (joking) while making the best game ever (which doesn’t happen, of course). Here is my point of view of what went right and what could have been better.

## What went right

From the beginning we knew we wanted to complete the jam with something done, and with that we mean nothing incomplete goes inside the game. That helped us to keep a small and achievable scope for the time we had.

When brainstorming the game we had luck in some way and reached a solid idea twenty minutes before sharing a pitch to the rest of the jammers, after being discussing by a couple of hours. The good part was not only we were happy with it but it also was related with the theme (we wanted to do a beat’em up but we couldn’t figure out how to link it with it).

Deciding to use familiar tools like Github, Unity and Adobe Animate and doing something we all had experience in some way helped us a lot to avoid unnecessary complications. I have to mention too that half of the team works together at Ironhide so we know each other well.

Our first prototypes, both visual and mechanical, were completed soon enough to validate we were right about the game and they also were a great guide during development. Here are two gifs about each one.

![alt text](../../assets/b7472091ac0bb68e.gif)


![alt text](../../assets/6709090b5bb87b4a.gif)


Our artists did a great job with the visual style direction which was really aligned with the setting and background story we thought while brainstorming. If you are interested [here](https://github.com/acoppes/rippleppl/wiki/Story) is the story behind the game.

![alt text](../../assets/282c2dd22f8aabca.gif)


Using the physics engine sometimes seems like exaggerating a bit, mainly with small games but the truth is, when used right, it could help to achieve unexpected mechanics that add value to the game while simplifying things. In our case we used to detect not only when a wave hits a player but also to detect when to animate the tiles and it was not only a good decision but also really fun.

![alt text](../../assets/761a1397e529355c.gif)


Using good practices like prototyping small stuff in separated Unity scenes, like we did with the tile animations, allowed us to quickly iterate a lot on how things should behave so they become solid before integrating with the rest of the game.

Knowing when to say no to new stuff, to keep focus on small, achievable things, even though, from time to time, we spent some time to think new and crazy ideas.

Having fun was a key pillar to develop the game in time while keeping the good mood during the jam.

## What could have been better

We left the sound effects to the end and couldn’t iterate enough so we aren’t so happy with the results. However, it was our fault, the dude that did the sounds was great and helped us because a lot (if you are reading, Thank you!). In the future, a better approach would be to quickly test with sounds like voice made or similar downloaded effects from other games, to give him better references to work with.

Not giving room to learn and integrate things like visual effects and particles which would have improved the game experience a lot. Next time we should spend some time to research what we wanted to do and how it could be done before discarding it, I am sure some lighting effects could have improved a lot the visual experience.

We weren’t fast enough to adapt part of the art we were doing to what the game mechanics were leading us, that translates to doing art we couldn’t implement or it is not appreciated enough because it doesn’t happen a lot during the game. If we reacted faster to that we could have dedicated more time in other things we wanted to do.

Too many programmers for a small game didn’t help us when dividing tasks in order to do more in less time. In some way this forced us to work together in one machine and it wasn’t bad at all. It is not easy to know how many programmers we needed before making the team nor adapting the game to the number of programmers. In the end I felt it was better to keep a small scope instead of trying to do more because a programmer is idle. In our case our third programmer helped with game design, testing and interacting with the sounds guy.

Since the art precedes the code, it should be completed with time before integrating it and since we couldn’t anticipate the assets we almost can’t put them in the game. In fact we couldn’t integrate some. The lesson is, test the pipeline and know art deadline is like two hours before the game jam’s end in order to give time to programmers.

Using Google Drive not in the best way complicated things when sharing assets from artists to developers to integrate in the game since we had to upload and download manually. A better option would have been using Dropbox since it automatically syncs. Another would have been forcing artists to integrate them in the game themselves using Unity and Git to share it, but I didn’t want them to hate me so quick so they avoided this growth opportunity.

The game wasn’t easy to balance since it needed 2 players in order to test and improve it. Our game designer tried the game each time a new player came to see what we were doing but that were isolated cases. I believe were affected a bit by the target resolution of the first visual prototype in terms of game space which left us only with the wave speed factor but if we changed to too slow the experience was affected.

We didn’t start brainstorming fast enough, it was a bit risky and we almost didn’t find a game in time. For the next time, we should start as soon as possible.

Some of the ideas we say no because of the scope were really fun and in some way we may have lose some opportunities there.

Drinking too much beer on Saturday could have reduced our capacity but since we can’t prove it we will not stop drinking beer during Global Game Jams.

## Conclusion

Participating on the Global Game Jam was great but you have to have free weekends to do it, for some of us it is not that simple to make time to join the event but I’m really sure it worth it.

I hope to have time for the next one and see our potential unleashed again. Until then, thanks my team for making a good game with me in only one weekend.

Cheers.