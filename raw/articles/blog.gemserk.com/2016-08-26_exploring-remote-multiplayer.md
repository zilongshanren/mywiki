---
title: Exploring Remote Multiplayer
url: https://blog.gemserk.com/2016/08/26/exploring-remote-multiplayer/
published: '2016-08-26'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

Some time ago I’ve started to prototype a multiplayer game, it is some kind of super simplified RTS game for mobile devices where macro decisions are encapsulated into one action through a button.

First versions were prototyped in a multiplayer hot seat fashion by using only one device (a tablet or a phone), that allowed me to quickly iterate between different ideas and find fun as soon as possible. That was a successful approach since the idea of the game proved that it was indeed fun to play with friends, so the next step was to go remote multiplayer with two or more devices.

Since networking is a whole new world for me, I started by reading lots of different articles about making multiplayer games.

The first thing to know is that the common solutions around depend on each kind of game, and knowing that beforehand helps you deciding the best solution for your game, and how your game must be adapted to support it.

In my case, I am developing a really simplified version of a RTS game for mobile, similar to Clash Royale. It is a 1v1 game where each player controls multiple units by giving high level orders like “everyone attack!” or “build new supply depot”.

The common networking approach for this kind of games, where synchronizing the whole world is a bit heavy given there are tons of units, is to do a synchronized simulation where only the main actions are transmitted (to save bandwidth) and each machine/device perform the same simulation. This implies the game should be deterministic in order to avoid desynchronization between players, so given one start state of the game and a list of actions over time, the final state should be always the same.

Making a game deterministic is a really hard problem, but it also has its rewards, like being able to replay the game given the actions of each player over time. This is a great debug tool for developers and at the same time a great freature for players since it is used to see other strategies or to share a great victory with your friends, everything with almost no storage cost.

The idea is to start writing my findings in the remote multiplayer journey to share all the lessons learned.

## References

These are some of the articles I read: