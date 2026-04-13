---
title: The Role and Difficulty of Skill Based Matchmaking - Game Wisdom
url: https://game-wisdom.com/critical/skill-based-matchmaking
author: Josh Bycer
published: '2024-08-22'
source_blog: Game Wisdom
source_site: https://game-wisdom.com
category: game programming
fetched: '2026-04-13'
---

[Activision’s findings about skill-based matchmaking](https://www.activision.com/cdn/research/CallofDuty_Matchmaking_Series_2.pdf) (SBMM) is an important read about the challenges and misconceptions of creating a competitive and friendly online atmosphere. But it also drives home one of the hardest aspects of these games and how it relates to matchmaking and balancing a game — what does skill mean in a game?


## A Winner is You?

When we talk about singleplayer or linear experiences, it’s far easier to define the skill curve of a game — if the player beats level 1, they can now do level 2. Every reflex-driven game is about constantly testing the player’s mastery and understanding of a game and moving them through the various areas of it.

However, in a match-based or multiplayer game, there is no linear progression, and it makes it far harder to gauge a player’s understanding of how to play. Let’s say I’m playing against a team that everyone has no idea what they’re doing and I walk away with a Kill/Death (or K/D) of 15/2, then I must be some kind of pro gamer, right? But on the very next match, I’m now up against a team that knows how to play and I’m now sitting at 2/15.

Whenever you have someone going up against another live player, the amount of factors affecting a match exponentially becomes more complicated. This goes back to an earlier topic I discussed about monetization elements in games like this — if I’m the best player in the world using the worst weapons in the game, can I reasonably beat someone who is the worst player using the best weapons? And when you add in teams to the mix, the ability to predict skill levels perfectly becomes next to impossible.

## Creating The Core, and Skillful, Experience

Anyone who has played a team-based game knows that hell is truly other people. Being the best or worst player on a team can feel like torture of either carrying the entire team or letting them down respectively. But this also creates a problem with measuring skill when it relates to working with a team, especially if your game features mechanics or elements that aren’t easily quantified. Measuring wins/losses, kills/deaths, hits/not hits, etc., are easily tracked. However, the factors that lead to those results are far harder to gauge.

![skill based matchmaking](../../assets/fb3b96ceb7319e6e.jpg)

DBD continues to struggle with defining their core experience and skill level; making it even harder to learn for new players (source Dead By Daylight)

This is a longstanding problem with the balance and direction of *Dead by Daylight* which has the added difficulty of being asymmetrical. Their matchmaking is based on determining “good play” which again, “good” is often related to “winning.” To win as a killer, you must hook the other team enough times to kill them; to win as a survivor means escaping. Here’s the problem with that, there is far more that is happening in a match for either team that contributes but is not factored to the act of winning.

Let’s say a killer fails to kill the other team, but manages to get the entire team on “death hook” state and holds out for a long time, were they a good or bad killer? For a survivor, let’s say someone is the first one to be killed, but they were constantly juking the killer and taking hits for the entire team, were they a bad player? Both sides are rewarded points based on various factors of smart play, but being able to do this once again is going to be determined by the skill of the killer and the skills of the different survivors.

To add even more confusion, we can bring in the concept of “ELO hell” and having someone be in the wrong matchmaking due to their team. If I’m a really good player and I’m on a team of newcomers who aren’t helping or don’t know how to play, I could end up being completely shut down by the other team, does that mean I’m a horrible player? Or again, be the standout player among a team of lesser-skilled players, does that mean I should be moved up?

Part of understanding what skill means in your game is figuring out how a player/team can win, but also, contribute during a game. Let’s say your game only tracks kills as the sole determination of skill, but if I’m playing a support role like a tank or healer and keep my entire team alive but never score a kill, am I bad player? And to go with that, let’s say I keep healing players who like to jump into death pits and lose all their health and the team loses with a high death ratio, does that make me a bad healer? As a quick tangent, this is also why characters/roles need to be a factor in matchmaking, and why I liked with *Street Fighter 6*, Capcom delineated ranking for a player to each character they play as opposed to an overall rating.

As a brief tangent, ELO scores and matchmaking in 1v1 matches is an easier metric to track compared to team-based games. Given enough time, and the player base and their skill levels will be mostly set thanks to the point disparity at work.

The problem with games that reward “good play”, or “skilled play” is that it leads to success becoming one or two ways of playing.

## Unlocking the Meta

In my other post about competitive design, I mentioned that what is seen as the “best” way of playing these games is often the worst for casual and core audiences. If everyone knows that gun X, perk Y, and character Z, are the best combinations, then why should anyone who wants to move up in the ranking play anything else? This leads to a kind of toxic behavior in these games with players bullying other players if they’re not playing what’s meta at the moment. From MOBAs, to shooters, to even MMOGs, people want to win, as there is no reward for losing a match.

![Overwatch Image](../../assets/586c5c830f62acaf.png)

Team-based games have their own struggles in terms of matchmaking and can lead to even more toxic behavior (source Gamespot)

This often leads to bad sportsmanship and people using rankings as a cudgel against other players: “it’s not my fault we lost, I had the best score on my team.” The problem is that you can play correctly, do everything right, and your team still loses, and the opposite is true. But when you have your entire scope of gameplay being drilled down to 2 to 3 metrics, the game, and other players, don’t care if you were keeping everyone alive, or delaying the other team, if you are the lowest on the scoreboard, then it must have been all your fault. There’s no easy way to try and fix it as you’re going up against human behavior. But this is also why many games now have far stricter and powerful tools for reporting and cataloging bad behavior.

That last point also brings up something important with how multiplayer and skill-based games have transformed over the years.

## The Limits of Skill and Matchmaking

With everything said, this piece is based on one fallacy that needs to be discussed. Everything here is built off designing a competitive/eSport-friendly experience. But as I talked about in a previous piece, that design limits the appeal and longevity of a live-service game. Even if you do find that magic ratio and create a perfectly balanced competitive game, that still doesn’t mean that people will want to play it.

You can give me all the SBMM in the world, that’s not going to get me to enjoy a fighting game, Battle Royale, multiplayer shooter, etc. Multiplayer design has become more and more homogenized over the years with developers chasing both the live service model of making a “daily game” and trying to appeal to the competitive eSports side. Both don’t leave much room for someone looking for a game to enjoy every once in a while, or to play with friends and random people. You must play these games daily or you’re going to fall behind in the meta, your ranking, or any kind of daily play rewards.

![skill based matchmaking](../../assets/4d222b751beb9fe8.png)

Live service has created a push for every multiplayer game to be the only game in town for someone’s free time (source Fortnite)

It feels like forever since we’ve had someone create a unique multiplayer experience that hasn’t been seen before and is a topic of another post I wrote about cooperative multiplayer design. When everything is filtered through the idea of a daily play, team-based/hero shooter, or fighting game, there are only so few ways you can stand out from everyone else in that respect.

*For you reading this — what are your thoughts on SBMM, and can multiplayer design continue to grow in a new direction?*

*If you would like to support what I do and let me do more daily streaming, be sure to check out my **Patreon**. My **Discord is now open** to everyone for chatting about games and game design.*