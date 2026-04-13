---
title: 'Games that just missed it: Infinite Space edition - Game Wisdom'
url: https://game-wisdom.com/analysis/games-that-just-missed-it-infinite-space-edition
author: Josh Bycer
published: '2011-02-17'
source_blog: Game Wisdom
source_site: https://game-wisdom.com
category: game programming
fetched: '2026-04-13'
---

[Infinite Space](http://en.wikipedia.org/wiki/Infinite_space) for the DS is another unique RPG; like [Avalon Code](http://chronicgamedesigner.blogspot.com/2011/02/games-that-just-missed-it-avalon-code.html) the game has several interesting systems combined with a few design problems. While Infinite Space’s problems are not as damning as Avalon Code it is another lesson of what to watch out for when designing your game.

I’m going to skip the story line for this entry as I’m not exactly sure what is going on and for this talk it is not important. IS is a sci-fi RPG in which you control and customize a fleet of ships. There is a lot to customize in IS which is part of the charm.

Each ship in IS belongs to a ship type such as battleship or carrier. Each type offers several advantages and disadvantages, such as battleships have the most weapon slots but are the slowest to maneuver in combat. You can outfit your ships with different rooms which increase the attributes of the ship. This is similar to Tetris, each room is identified as a geometric shape, and if you fit the room into an empty space on your ship then that room will be installed. Some rooms have to be placed in designated spaces such as the engine in the engine area. Different ships have different layouts which will affect what you can and cannot install.

You will also pick out what weapon systems you want to install, each weapon has a different firing range which determines how close you need to be to the enemy to fire along with several other attributes. If you have a ship that can support fighters you can also assign different fighters to your ship.

The last bit of customization comes from your crew; the main characters you meet in the game can join your crew and be assigned to different posts. Each post will affect something on your ship; some members have special skills that when assigned to the first or second in command station will allow you to use them in combat.

With that said it’s time to talk about combat. As mentioned combat is fleet vs. fleet, a fleet can contain anywhere from one to five ships. I’m going to ignore the special skills and instead focus on the three commands you always have access to in combat: Normal, Dodge and Barrage. On the left side of the screen is a gauge that fills up during combat, the rate is based on the stats of your ships.

As the gauge fills the bar will change color to show what skill you can use, going from green to yellow and finally red. When you use a skill you’ll use up the parts of the gauge, for example using barrage which is red will use up the majority of your gauge.

When you issue a command, you are ordering all the ships in your fleet. You can see on the status window if your ships are within attack range with their weapons. In order to understand the problem with the design you’ll need to know what each command does.

Normal is a basic attack from every ship in your fleet, nothing more nothing less. Dodge puts your fleet in a passive stance; you’ll remain in dodge as long as you do not attack the enemy. If the enemy tries to hit you with either a barrage attack or special, the dodge stance nullifies it. However if the enemy hits you with a normal attack while you are dodging, then their accuracy will be increased, or in other words you’ll be hit by every weapon that is being fired.

The barrage command does three times the damage of one normal command. Most often one barrage command is enough to destroy one ship not counting fights with unique ships which are the boss fights. On paper all this sounds good as a” rock paper scissors” system, but how it was implemented in game is where the trouble is.

Because battles are fleet based, one side having more ships will inherently have the advantage. Almost four out of every five fights you will be outnumbered by the enemy fleet. What makes this troublesome goes back to the barrage command. If the enemy fleet is fully charge you have no choice but to use the dodge stance as getting hit by an enhanced normal attack is nowhere near as damaging as being hit by a barrage.

This removes the element of choice in IS as the biggest choice you’ll make will be either having a 50% chance of surviving vs. a 0% chance. If both fleets are fully charged you have to wait for them to use their barrage first because if you attack, the AI will most often follow up immediately with a barrage and you can’t lose a ship to take out one of theirs since you are outnumbered.

One element of the design which is troubling is that if you lose your flagship in combat, you will automatically lose and get the game over screen. It does not matter how many ships are left in your fleet, this is the only element of the combat system that only the player has to deal with, and the AI does not have this disadvantage.

Another problem is how the system is not really a set of counters. Normal counters dodge, dodge counters barrage, but nothing counters normal. Instead of combat being based on countering the enemy and maneuvering into range, it becomes a slug-fest of who can get their barrage to hit first. Most often luck plays the biggest factor in winning a fight, if you can get the enemy to waste a barrage and follow up with one of your own you’ll have a huge advantage.

As the game goes on the fleet advantage problem will go away, however it will take a while, to give a frame of reference I’m about 18 hours in the game and only have a three ship fleet.

I have two ideas of how to improve combat. The first one is to make barrage a counter to normal attacks, the best way I can think of is hitting a fleet with a barrage attack will reduce their gauge down to green preventing them from following up and at the same time countering a normal attack. This would remove the penalty of attacking first.

Option two would be to leave barrage out of the equation and instead create a fourth option to act as a counter to normal. We could call it “shields” like dodge it is a passive stance however it only blocks normal attacks and must be reapplied after an attack, to prevent it from being too powerful. That way we have some semblance of a “rock, paper, scissors” counter system.

With my ideas I would only try one of them at a time to see it would improve things. Since the AI would also use them we don’t want to continue to give the AI an advantage.

One of the challenges when developing unique systems is how the AI will handle it. In old school RPG design the system is usually basic enough for the AI to understand or the AI is given special skills to compensate. When you have something like IS which is not traditional the designers had to give the AI advantages in the form of outnumbering the player in fights. However by doing that it interferes with the balance and pushes things into the AI’s advantage far too often.

Because of how the attack commands play out combined with being outnumbered, the game stacks the odds against the player which is not good design. This is not the same as making a hard game like Demon’s Souls or Ninja Gaiden Black, in those titles the player is given the tools needed to survive and has to make the most out of them. In IS however it is like being given a knife to fight someone with a sub machine gun.

To further illustrate that point the game has several parts that have you including a NPC ship in your fleet, which just happens to leave right at a boss fight. Meaning that for a boss fight you will fight with one less ship in your fleet which with the systems in place is just kicking the player when they’re down.

As I mentioned at the start, the problems with IS don’t ruin the game or push the game down as far as the issues present in Avalon Code. Eventually once your fleet is maxed out the difficulty of the game smoothes out. Unfortunately you have a long way to go in game before that happens and I don’t know how many gamers would persevere to reach that point.

Josh