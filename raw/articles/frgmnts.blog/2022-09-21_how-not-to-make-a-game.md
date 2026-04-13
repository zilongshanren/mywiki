---
title: How Not to Make a Game
url: https://frgmnts.blog/f/how-not-to-make-a-game.html
author: Mario Kaiser
published: '2022-09-21'
source_blog: 'FRGMNTS: Bite Size Fiction'
source_site: https://frgmnts.blog
category: game programming
fetched: '2026-04-13'
---

# How Not to Make a Game

This is a post-mortem and a collection of lessons learned while making my first indie game, Coregrounds, which we had published on Steam in April 2018 and shut down by the end of 2018.

Before we get to it, a bit of history: While I had dabbled in game development before, Coregrounds was my first real game project. And I wanted to get it right; when I started in 2013, I took my sweet time, saved up some money and worked on the concept for a little over a year. Then I developed a proof-of-concept version within half a year and published that on the game's website. The result looked like this:

After playtesting this version with friends and family and realizing that the game actually worked, I went full-on, founded a company, continued to improve the graphics and gameplay and had a much nicer beta version after another six months or so:

After completing this version, I went head-on into marketing the game, didn't know much about what I was doing and ended up spending a lot of time without much to show for it.

I also went to many events in Berlin like Talk & Play, showed Coregrounds at AMaze and Quo Vadis and eagerly collected feedback from players, the bottom line for me being then: there's still so much to improve. Money was running out though, so I ran a [Kickstarter (opens new window)](https://www.kickstarter.com/projects/1143574579/coregrounds-tower-defense-for-the-esports-generati), which failed to reach the funding goal.

But I still loved the fuck out of this game. I didn't want to stop. I recruited a developer from the game's community who would develop the game server while I'd focus on the client and everything else. I hired an artist to level up the game's art. I took on a part time job and we worked painfully hard for almost two years on the version we ended up releasing on Steam in April 2018, which looked like this:

The new version's launch on [Steam (opens new window)](https://store.steampowered.com/app/649770/Coregrounds/) was far from successful: we had somewhat rushed the launch and had completely avoidable technical and gameplay issues which made most of the initial traffic spike from Steam bounce right off the game.

Over the rest of 2018 we struggled to improve the game further, marketing it and building the critical mass of players a PVP game needs to work. We didn't succeed, noticed that the mobile versions we had planned for the game would have needed another massive overhaul due to performance issues and thus decided to call it quits, shut down the servers and [open source the game's code (opens new window)](https://github.com/ehmprah/coregrounds).

## Lesson #1

Listen to advice

If you're starting to make a game, you're probably reading lots of articles, lists, tutorials and whatnot. You're talking to other, more experienced people. You're surrounded by good advice, that's the easy part. The difficult part is actually heeding that advice. Especially as a game development rook, you might not wanna hear certain things. Both articles and people told me making a complex multiplayer game might turn out to be too much work for a single person, which I didn't want to hear, which brings us right to the next lesson learned.

## Lesson #2

Know your limits

With Coregrounds I made the game I wanted to play myself; I didn't spend nearly enough time thinking about wether this was the game I could make in a reasonable time. A MOBA-style multiplayer game is so complex and thus incredibly much work which I just didn't think of beforehand and thoroughly failed to see right up to the end. Even when we were two programmers, we were in way over our heads and spend way too much time programming, which is but a part of making a game.

## Lesson #3

Don't do everything yourself

When starting out as a programmer, I used frameworks a lot. Over time I was annoyed by all the overhead and when making Coregrounds, I opted for a different approach and wanted to make as much as I could myself. This was a very good decision for myself and a very bad decision for Coregrounds. Had I opted for a canvas framework like PixiJS for example we wouldn't have had the performance issues that kept us from releasing the mobile versions of the game. Long story short: don't do everything yourself or you'll make developing a complex game even more worse.

## Lesson #4

Marketing is a bitch

I started out thinking it's enough to make a cool game. If only the game is good enough, people would come naturally, it would surely take off at some point I thought. Well, no. Apart from the fact that the game was not good enough in that way, there are tons of games that are and still lead a fairly unnoticed existence somewhere in the void. A game is nothing without people playing it, people only play it when you market it, and marketing a game is really fucking difficult, especially if don't have any budget for it.

## Lesson #5

Don't love your game (too much)

Coregrounds was not only a business venture. It was the game I wanted to make with a hobbyist's heart. I was in love with this game right from the start, which kept me from seeing its faults and immanent problems. I thought all we needed was more work, more programming, better graphics, more finetuning. I did not want to see that the product "indie tower defense moba mashup niche game made by mostly one person" was problematic to begin with.

## Lesson #6

Community can be a blessing and a curse

Especially in retrospect I have a very biased relatenship with the Coregrounds community. Pretty much right from the beginning, Coregrounds attracted a few dozen die-hard fans. People love something you've created and not only dump hundreds of hours into playing it, but also theorycraft, recruit more players and are just so damn passionate about your game that you end up really convinced you're onto something here. It just feels good to have people care about something you make, so you want to keep on making it, even if that might not make sense.

## Lesson #7

It's all about learning

While Coregrounds itself was a failure, I had years of fun making it. I have developed and shipped a multiplayer game and probably would not have gotten my current job without that experience. I have learned a ton of things, not just about programming. I wouldn't do it again, but I am glad to have done it.

## Where to next?

Coregrounds was my first real game project, but most definitely not my last. In fact, a second game is currently in the works. It's not going to be a multiplayer game. I'm not going to develop it in full time, draining my savings. This time, I'm making it with the hobbyist's heart, no strings attached. If you're interested in that, follow me on [Twitter (opens new window)](https://twitter.com/ehmprah) or subscribe to my [newletter](https://frgmnts.blog/newsletter.html).