---
title: Lucky Fluke Post Mortem
url: https://www.boristhebrave.com/2020/07/18/lucky-fluke-post-mortem/
author: Boris
published: '2020-07-18'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

I recently made a game in 48 hours, [Lucky Fluke](https://boristhebrave.itch.io/lucky-fluke). Though technically I’ve done game jams before, [I’ve not done one in a decade](https://www.boristhebrave.com/2011/02/13/meatballs/), and not ever as successfully. So I thought I’d write up what I learnt.

## 1. Unity is really easy

So I’ve developed in C# for a long time, and started playing around in Unity last year, but I’d never made a 2d game with it. I was impressed how easy it was to watch a couple of videos on key concepts, and throw together something that worked pretty much straight away.

We spent about 90 minutes discussing the theme, and then **it took only about 15 minutes to make the basic mechanic that became the core of our game**.

Despite Unity Collab not being especially good, the design of Unity made it easy to work together. I would throw together a prototype with “programmer art” as seen above, and Praeto was easily able to replace it with sprites and animations, and jhicks add audio cues to all the animation, without me constantly fiddling with hooking everything up.

That’s not to say we didn’t run into technical difficulties, such as the hour I spent failing to get jiggle bones working, similarly with full screen support, having to redo some assets to get sprite sort order correct, and several difficulties with FMOD. But in almost all cases, a quick google would find someone with a near identical problem who could explain things.

## 2. Making Jam games is not like making regular games

Obviously, we were aware that the 48 hour format of the hackathon severely limited the scope of the game. It wasn’t too big a challenge for us – Friday evening was spent brainstorming and prototyping, Saturday making the bulk of the game, and Sunday for level design, polish, and uploading. We were more or less finished with a few hours to spare.

But there were other aspects of doing a Jam game that I hadn’t appreciated until afterwards. The jam had over 5000 submissions, so our game was just one in large ocean. There were tons of reviewers, but they **spend a very small amount of time **on each game. That meant a popular entry had to:

- Require very little reading or tutorial
- Get to the hook or twist of the game almost immediately
- Have almost no downtime or filler
- Be easy enough that no real skill investment is required to complete it

Our tutorial was perfectly short and sweet, and the concept immediately graspable. But, I like games with a high skill ceiling, so Lucky Fluke is actually requires some practice to complete. And even worse, I put all the interesting content such as powerups and bosses on the later levels which most people would never see!

This was particularly underscored when the event organizer, Mark Brown, [played our game](https://youtu.be/uUi98Do7dYw?t=6475). With the pressure to get through so many games, and it being at the end of a long session of streaming, it’s not expected that you’ll have much patience for subtlety. **Jam games should be a sledgehammer in the face of ideas and content, gone quickly so the reviewer can rate it and move on.**

One trick I saw in several games was to just have a “Next Level” button, so even the most bored player could flick through the game until they found something interesting. (this button is also a great bodge around uneven level design and bugs).

## 3. Game design is a thing

You’d think this was obvious, but no. Our team consisted of an artist, a programmer and a sound engineer / composer, but no one who has actually sat down and tried to make a game *fun*.

In the end, most of the level design, balance, tuning and other invisible decisions came down to me. I was aware that this stuff was important, but I still didn’t really dedicate enough time to it. That partly lead to the mistake I discussed before of making the game too challenging, and leaving content towards the end, and fairly insipid levels.

But also, the lack of design hurt the fun. I had set out to make a wacky and frenetic shooter, but once I actually played with the game, I couldn’t find a way to amp up the pace and juice without making the game completely unplayable and random. Perhaps someone with more experience would have succeeded.

In the end, we made a game that was more about accuracy than chaos, and we even added a few mechanics to support this, such as the ability to shoot yourself if you spam your gun, and a score system that rewards combos. But many reviewers said it was a missed opportunity.

## Conclusion

The jam was a lot of fun, despite spending the vast majority of my weekend working flat out. I’d highly recommend the experience to any dabbling game devs, **it’s far more fulfulling to make something small, and finish it, than work on your magnum ops for years**. It took me years of hobby programming to finally internalize this.

Though you’ll spend the majority of the jam programming and arting the game, it’s not the most crucial part. Getting a great idea, and exploiting it for maximum effect, are going to be far more important to ultimately winning than the level of polish you bring.