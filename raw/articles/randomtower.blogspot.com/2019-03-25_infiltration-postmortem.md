---
title: Infiltration postmortem
url: https://randomtower.blogspot.com/2019/03/infiltration-postmortem_25.html
author: Pubblicato da Marte
published: '2019-03-25'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

## Infiltration postmortem

With release 1.0 Infiltration is done, at least as prototype. My vision in the beginning was the following

*a turn based single player asymmetric game where player take control of an agent and manipulate actors and organizations to obtain victory*

And this prototype wasn't able to prove this vision and my idea for this postmortem is to analyze why.

I think that postmortem, something people do for ludum dare, or 7DRL (and even at work!) are quite useful if you want to understand what you have done, why and win/lose for your project. So let's start!

### Beginning

Work from beginning to end without a clear plan is not easy. Not even for an hobby like videogame development. I know it before and I know it better right now!

What have worked in the beginning, like every new project, was the vision: for Infiltration I wanted to build something unique, inspired from That Which Sleeps, but on my take. I can say that from first build my vision was to follow my path, be inspired but not strictly follow anyone. I'm proud of this and instead to do, like in the past or in the future, something that someone else have done, I have create Infiltration.

Goal here was to learn, learn from mistakes, learn from players and of course learn from me.

[Many times in the past I have build clones of other people games](https://randomtower.blogspot.com/2019/02/ten-years-later.html). This time is not like the other time, just because That Which Sleeps never come out.

I think a good start was to put out first build quickly. If I look back, game is not so different from now:

Key elements are all here:

• a static map of a continent with provinces and few notables cities

• an advancement for turns, because is a turn based game

• log of actions

Seems a little bit, but inside there was core code too:

• select an actor from a list, corrupt it

• send actor to search for hidden secrets

• clue mechanics

• madness and crazy actions for actors

I don't want to analyze every build, is not so important, but focus on the start. I have a goal, stated on a written vision and my first step was already a misstep. Why you ask?

Because I focus a lot on simulation side,

[like said in bay12 forum](http://www.bay12forums.com/smf/index.php?topic=169949.0). Few players are interested on simulation at this level, for my thoughts because of the following points:

1. simulations without interactions are not interesting

2. simulations without an overall story that gives context to actors and player actions are not engaging

3. simulations without possible forecast by player are not playable

I think that these three key points are interesting for me (and maybe someone else too!) so analyze it in deep.

### Simulations without interactions are not interesting

I have build a simulation where actors runs a card game. Every actors has at start same amount of resources (money, arcane power, influence, followers) that can use to do following actions:

• move to another city

• do a quest from a list of city's specific list

• gather followers

• improve basic amount of money every turn

• improve number of followers every turn

• acquire access to a district

• attack a district if owned from another player

If you have played a little bit with Infiltration and see these list you can see why there is a lot of movement between cities, why actors do what they do and what is the meaning of districts. For player, because Infiltration is an asymmetric game, this is not so important. Key point here is to get access with a corrupted agent into the district where hidden knowledge is.

But as you can understand all the time spent on this side wasn't well invested by me. What I wanted was a world with actors that interact between themself and in the end what they do is to move around a lot on start, then slow down and defend/attack they property in a city. An actor in a city cannot win, so if player help or try to stop a particular actor (or corrupt anyone!) is not so important.

This was a mistake. A simulation without a meaningful interaction by player is not interesting, at least for me.

What I have done instead could be explained in design actor interactions in a way that player, with his action can interfer, really boost an actor on his fight to the power in a city (or in all the realm!). Of course a similar boost by the player after a while could be noted and investigation starts: player is not directly invested by the outcome, but instead his puppet.

As you can see this there is an emergent story from few little rules and another think I have learned from this experience is players can fill the gaps between part of the stories and get actual meaning by this.

So let's move to next point...

### Simulations without an overall story that gives context to actors and player actions are not engaging

Infiltration is a prototype, so build an actual story for it was right decision. But I have created bit of stories anyway. Cities has descriptions:

Theros is capital of a Kingdom and the centre of administrative power in the kingdom, Theros is home to the King's throne and the endless debating of his councillors.

Anrios, The City of Winter, Anrios is the seat of the Guild of Warriors and the quality of its mines are famous across the continent.

And same goes for guilds, actors and monsters.

This effort is useful, if directed wisely. Again player actions are in a much larger context (and this is fine!): he learn from the start that he is a trapped god and he must uncover hidden knowledge in order to fully awake. Overall story is fine, but how this story is developed?

I have done nothing on this side: story here is to unlock five findings and you have done.

What I have done instead is to plan a story, even minimal, with some key points and decision for player. Decisions that affect how he can play early, medium and late stage of the game. And example is, in order to get a hidden knowledge, to sacrifice his followers. This is an huge decision: do you want more power now, or wait for later to do this sacrifice? This sort of decision can unlock a new power for player, to sacrifice a follower to power up another one. Evilness, right?

But I don't want to focus here only on quick decision: I want something that unlock new part of the game, something that player can fully understand only if he play more than one run. A sort of meta-game where players can unlock new factions, actors types and even part of the map that instead are not available.

I believe a right approach is something like Arkam Horror or Heretic Operative or even Xcom: in these games there is an overall story that player unlock doing some actions in order. What I want from this kind of games is a direction that player can follow (not must!) to unlock what scenario's creator have designed.

But again is hard or even impossible to understand possible choices if player cannot forecast his action's outcomes...

### Simulations without possible forecast by player are not playable

One of my points with Infiltration is to build a simulation where player is asymmetric to other actors. This is not like chess, where every player can see same board, have all same pieces.

Asymmetric games for me are so interesting because I can interact with a world, but cannot do same things other actors can do. As player I cannot go into that dungeon to find an hidden secret!

What player must do is to corrupt an actor and send it to the dungeon: but you cannot know what he will found or even if he will come back!

This concept, as far I can tell, I well explored in Spire of Sorcery a game I'm waiting to play, like you can understand. I'm not so interested in micro-management (inventory? Ah-ehm.. boring!), but this a postmortem!

Right on track! What I want to focus as reasoning here is where player can forecast on outcome of his actions (30% will be very bad for my agent, 60% will be okay, 10% will be great) better game can be in my opinion.

A key point here, that I've found online recently is that action input should not be random, but output yes. I want to elaborate this more, to understand properly. If player can decide to do an action (input, like send an agent to do a particular quest) he will be in control of possible outcomes (output, that quest is easy, or hard). If instead player is forced to follow a random action (input like throw a dice) he will not be in control of outcome (output, rolled 1, failure).

Difference is subtle, but for me is importand. This is why games that have an high degree of randomness after a while are not so interesting on my eyes.

My failure with Infiltration is to realize this after a while, introducing challenges without a proper explanation on what are outcomes. Right now in Infiltration you do a challenge (physical, social, intelligence) for every action you force an actor to do. This is fine, but for example explore a cave with a monster, what are possible outcomes? You don't know, because as player you don't know nothing of this monster. So, throw a dice, ehm... not cool for me!

### Pros

Simply because this a retrospective, I have also to focus on right decisions in Infiltration making.

A good decision was to start simple, be simple, not to focus on complicate frameworks, libraries, ux/ui, . It's a prototype anyway, so in most cases will be trashed, so why bother to learn something new?

If you are able to clarify your goal, you right tool in your head to navigate on every little decision (and make a videogame, even for hobby, is full of little decisions!).

Another important, really important step was to focus a little bit more on marketing. I know that is an hobby, but spread a word more on twitter, on my blog, on bay12 forum, was right decision from the start.

You don't know how many people can help you, in many ways (with a translation, with a good word, with a critique!), so be open, it's an hobby, you don't have to be feared!

## Conclusions

I say thanks to anyone have supported me, inspired and say something (on good or bad). I think Infiltration was a good experiment and prototype that have helped to become more consciuous of what I want from this kind of game:

• interact more and in meaningful way with the simulation

• be sure that player actions fit in an overall story, with branches and big decisions

• present to the player possible outcomes for every actions, so it's possible to do meaningful decision

I think that three points above are a big step on right decisions, for next game on this side!

Hope someone will find this postmortem interesting, just drop a line for a discussion on this side, see you soon!

## No comments:

## Post a Comment