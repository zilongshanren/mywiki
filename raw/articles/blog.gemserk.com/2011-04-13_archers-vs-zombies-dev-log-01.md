---
title: Archers Vs Zombies - Dev Log - 01
url: https://blog.gemserk.com/2011/04/13/archer-vs-zombies-dev-log-01/
published: '2011-04-13'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

I am working on a new game for Android and PC (Windows, Mac and Linux) platforms. The name of the game is not clear yet, for now is Archer Vs Zombies. It is being developed using [Libgdx](https://code.google.com/p/libgdx) (using its box2d port for the physics), [Artemis Entity System Framework](http://slick.javaunlimited.net/viewtopic.php?t=3076) and [Animation4j](https://github.com/gemserk/animation4j). I want to be blogging about the game development progress, maybe some game design decisions and how I am using the libraries, stuff like that.

### Quick Description

An archer has to defend something (could be a castle, a house, people) from enemies (zombies, vampires, etc) which are coming to steal/destroy/kill/eat brains (yeah, they are bad) by throwing arrows to them. There will be waves of enemies and different levels with different landscapes.

Here is a video of the current status of the game, so you can visualize the concept:

note: something happened with the video, it should be finished after second 20.


Here are the features I will concentrate for now:

- There are enemies which comes to kill/steal/destroy.
- Add a movable target as the first enemy prototype.

- The player can control the bow power.
- Add feedback of the current bow power (probably add an arrow in the bow when charging which moves depending on the charge).
- Restrict bow power.


I already have some ideas to add more depth to the game but I want to explain them in further posts.

The game is open source (for now?) with the codename of [archervsworld](https://github.com/gemserk/archervsworld). Also I have a link [here](http://www.gemserk.com/prototipos/archervsworld-release/launch-webstart.jnlp) if you want to test the latest PC stable version, and [here](http://www.gemserk.com/prototipos/archervsworld-release/archervsworld-android.apk) to test the latest Android stable version.

Hope you like it.