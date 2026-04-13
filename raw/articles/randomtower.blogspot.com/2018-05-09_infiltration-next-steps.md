---
title: 'Infiltration: next steps'
url: https://randomtower.blogspot.com/2018/05/infiltration-next-steps.html
author: Pubblicato da Marte
published: '2018-05-09'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

This time I've made a video to show my progress on game so far:You are not dead, you are not living.. yet.

Aeons ago, in a time before mith, your enemies sigil you in a realm far from reality. Weakened and far from your power, your will simply.. disappear.

One echo, from time to time, hit your dreams. Something called humanity is playing with arcane power and forgotten knowledge, part of you.

You simply awaken and take a look into the world. These "humans" will serve you as puppets in your quest to become powerful, again.

**TLTR**: after polishing up ui, my plan is to improve underlying simulation

**0.0.3 release and how to simulate a city**

My hopes is someone is following this sort of "dev diary", but like my previous entries, is not something I'm doing for others, but for myself, in order to clarify project's roadmap and be open as most as possible.

For release 0.0.3 my aim was to create a smaller release (in scope and time) with fewer new features, but important from player perspective. So I've included automatic turn passing with active pause, something like Paradox games like Europa Universalis IV or Stellaris. This feature was requested from a player and after some considerations, I've found reasonable. Prototype does not change too much in term of "feel" and a player can pause at any time. Of course any event will stop time, so player can evaluate events. In the future it's possible to elaborate this pause and let player decide events categories (for example: block turn passing only when there is a rebellion in a city).

I've also added characters portraits (not made by me, found on opengameart.org) for every character classes and I think that feel of the game is now more in line with my vision, so player can simpatize (or hate) a particular character. Sure adding a personalized (or even generated) portrait for every actor in the game for now is out of scope, but is something that can add a lot from player perspective. Imagine for example that player manipulation force an actor to complete a quest, but increase madness a lot. Portrait can display this change with more crazy expression. Something for far future!

Also with a simple introduction for the game (with an icon to reacall at any time) should be more clear what this prototype is about, let me know what do you think about this too! In term of gameplay there is not too much to do, so for now game should be easy after some runs.


Prototype for a prototype

Prototype for a prototype

Meanwhile I'm working on improve city internal simulation. It's a big topic, I know, so in this few words I will explain the main idea and why I choose this approach.

First of all, main idea: infiltration Test is a prototype so goal here is always to do something simple (from my point of view, at first!). Complexity will come with time, so I don't really need to rush on this side for now. Another important goal is to create a world that player can manipulate. For sure a world with some kind of internal simulation is more interesting than a static world, where player on different runs can simply do always the same thing. I've think a lot on this and found a lot of interesting an inspiring examples around, first of all, Dwarf Fortress. On surface DF is a lot about randomness, with many layers of simulation (historical, geological, etc..) that together give us a lot of re playability. DF is just an inspiration for me, but it's also interesting to find that many players found this kind of interactive medium interesting and stimulating.

Let's go back to topic of this article! In present release, npc just react to player actions and context variables, but I want more.. and not too much. Imagine a board game where npc compete for city power and where player can from outside of this "board game", manipulate them. My process was a lot iterative, on following steps:

1) create a small board-game prototype (created with card and paper, a prototype for a prototype!)

2) testing

3) from board game to program

Go deeper on these three steps..

**Board game prototype**

I've played a lot of board game (Risk, Catan, Carcassone, 7 wonders, etc.. ) and I can say I have a precise "feel" of what I want. But how to start create a board game that creates interesting interactions?

My research started from youtube, with some random board games reviews and thoughts on games I've played. For this prototype I don't need a war game or a complex card game, but something simple.

So I started analysing also games I love, like Starcraft (1&2): what kind of resources players manipulate? How these interactions create balance between players?

So i started with a simple consideration: npc need money. Money is a simple concept to track and explain. So every npc start with an amount of money. Using this resource, they can obtain another resource: followers. Followers will be used to attack/defend from other npcs. For me this is really important, because create an auto-balance on which kind of actions npc can do: "can I attack another npc?" or "is better use my followers to do something else" ?

Of course npcs doesn't have these thoughts, but player yes. So if an hypothetical player watches game, can see on top of cold numbers a logic something else, with his imagination. Something powerful and inspired from Hearthstone streaming where during opponent's turn, often host streamer make comments on possible actions, outcomes and so on.

Followers can be used from npc also to complete quests. A quest is generated by world on start of simulation, like a deck of cards to complete, to get more resources. Don't forget quests, because this is the entry point for Infiltration player (you): quests can be created by player and will have side effects that npcs cannot evaluate on start and give player more power for later stages. I will go back on this for sure, don't panic!

So a quest is a mechanics to tell a story. Many games has this mechanics, that provide a lot of useful side effects:

- balance: a quest has one or more pre-requisite, so it's easy to provide some entry-level quest (like "Kill all bandits in the forest", require 5 followers)

- tell a story: a quest with a minimum of description (together with a common lore) can create a meta-story that again player can improve with his imagination, "filling gaps" between quests. For example from previous quest, when you read bandits and know that you are in a fantasy settings, you have can have a lot of examples in mind. Cheap trick? Maybe, but it's fun for me to think about these tricks!

- outcomes: solve a quest can give npc rewards in terms of money, follower or another resource: influence (see more later)

- easy to implement: create a quest is really simple, because with some templates (quest cost 1, obtain reward 1, quest cost 4, obtain reward 4) can be created quickly and balanced again quickly. This comes from Magic the gathering, where a creature that has attack 5 and defence 5, usually cost 5, so 5+5=5, more or less (I know that is no more true from a long time!)

So for this prototype I've created a "deck" or "list" of available quests. Every turn, npc can evaluate if a quest if solvable (prerequisites are met) and do it.

With reward in terms of influence points, npc unlock another core "action": compete for district.

I've said before a little about district, but think about them like a "poi" in a city. Castle, Cathedral, market, port, underground. These "point of interests" are main goal for npc, that fight using followers one against other to conquer them.

There is some randomness here, because of a dice roll involved, but is not so important right now.

So far the "loop" for a npc:

1) every turn, get money

2) acquire more followers if possible

3) solve a quest if possible and get influence points

4) using influence point acquire a district of fight using followers

**Test board game prototype**

After a first prototype on paper I realized that order must be inverse, because I need that every npc made at max one action for turn, so the correct loop is:

1) using influence point acquire a district of fight using followers

2) solve a quest if possible and get influence points

3) acquire more followers if possible

4) every turn, get money

But an npc can win the game? For now yes and no. It depends on how good dice rolls are and there is not too much "tactic" or "strategic thinking" involved. This is good! From an human point of view this is boring, but from an actor (programmed by me) it's fine.

Think about it: you don't need an AI to create some movement in a city, you need only a little bit of randomness (not too much) and some basic rules and actions. Interaction between these elements is the key!

So after two plays of this game, I've found a lot difficult to follow every npc stats (money/followers/influence), quests (done/todo), etc..

So I quickly iterate in a computer prototype (separate from infiltration test). I would stress a point here: create a prototype on paper and go AFTER to programming side of things is a huge plus for me. Many mistakes are easily spotted on paper and computer programs can create a lot of simulations quickly, more and more quickly that is impressive! I've runs of 500 turns with npcs that still compete for victory.. so I'm on right way to create what I need for infiltration test.


From board game to program

From board game to program

This little journey is almost on it's end.

What I miss? An example is content: with program it's possible to create (not procedurally create, just create) quickly a lot of quests, npcs and different kind of districts to work on simulation, again a good point!

But in order to optimize my time, I've made a command line game, not something with a gui. It's a choice dictated by a simple consideration: I'm the only one that will see this prototype in the prototype. You as player will see all this integrated to infiltration and without all debug informations floating around.

All was nice until I notice that something was missing.. the player!

I've mention before player can create quests solvable by npcs, but how to track advancement for player!

So I've introduced a new resource: arcane power. This resource comes only from quests made on districts (I think you can follow the pattern here, right?) and gives npc opportunity to obtain special power/objects and .. uncover world secrets.

So we are on the end of the circle here. When a forgotten secret is uncovered, player unlock new power (create more quests? force manipulation on npcs?

**Conclusion**

So my plan for 0.0.4 will be to integrate my other prototype simulation into infiltration, so you will see outcome of these simulation in game.

I'm excited to see final result and your feedbacks on that, because even if limited, these interactions between npcs will create a more dynamic world, a crucial point of a game like this one.

Next step on this will be to integrate player actions and quest creation mechanics into this loop, but will be a dedicated post about that!

Thanks for reading and as always any feedback is appreciated!

## No comments:

## Post a Comment