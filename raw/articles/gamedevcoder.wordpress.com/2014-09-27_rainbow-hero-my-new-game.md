---
title: Rainbow Hero – my new game
url: https://gamedevcoder.wordpress.com/2014/09/27/rainbow-hero-my-new-indie-game/
published: '2014-09-27'
source_blog: Gamedev Coder Diary
source_site: https://gamedevcoder.wordpress.com
category: game programming
fetched: '2026-04-13'
---

After some very long and slow, mostly after hours, development I have finally released my new puzzle game – [Rainbow Hero](http://www.pixelelephant.com/rainbowhero):


The game is an old-school type of game as far as mechanics with some painterly stylized graphics and a fairy tale style audio.

One of my primary gameplay inspirations for Rainbow Hero was [Stone Age](http://www.myabandonware.com/game/stone-age-1iq) – a game released for PC DOS in 1992. I remember when I played it with my father on my old good Intel 486. Years later, I played it again with my wife. Both times it was a lot of fun. Clever, often seemingly impossible, puzzles and lots of cool ideas.

Another inspiration was Lasermania – game released in 1990 for Amiga. I liked the general idea of reflecting lasers but I considered the game prohibitive as far as difficulty level. Even though I am a patient kind of gamer and I love solving puzzles, I got stuck on some of the very first levels and didn’t want to continue.

There’s a couple more inspirations including general [pushover](http://en.wikipedia.org/wiki/Sokoban) mechanic as well as some totally original ones. I’ve always loved playing puzzle games and I guess with Rainbow Hero it is my attempt at gathering together some of the most interesting puzzles that could be applied to grid based levels and putting them together into a game.

One of the cool things that I am particularly happy with is time rewind feature that simply lets you go back in time – either when you get stuck or just want to try different approach. This isn’t anything new – games such as Braid use this a lot (and not just for purely time rewind) – but it makes the game a lot more player friendly.

In fact, it was pretty straightforward to do code wise. All I had to do was to store game state for each frame. Then, with ‘rewind’ button pressed, the game gets continually restored from past states. A little bit of work went into optimizing memory usage, so that the game state is small enough I can safely store hours of gameplay.

If you’re into serious puzzle solving Rainbow Hero might be the game for you. It is already [available on Steam](http://store.steampowered.com/app/343570) and directly via [game website](http://www.pixelelephant.com/rainbowhero). And if you happen to play the game I’d love to hear what you have to say about it.

this game is cool. thanks for sharing, mate.