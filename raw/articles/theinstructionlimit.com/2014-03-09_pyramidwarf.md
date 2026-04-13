---
title: Pyramidwarf
url: https://theinstructionlimit.com/pyramidwarf
author: Author Renaud Bédard
published: '2014-03-09'
source_blog: The Instruction Limit
source_site: https://theinstructionlimit.com
category: graphics
fetched: '2026-04-13'
---

**Pyramidwarf** is a game I made in collaboration with [Samuel Boucher](https://twitter.com/MonsieurEureka) (alias Monsieur Eurêka) with music by Stefan Boucher at the Global Game Jam 2014 in the TAG Lab of the Concordia University, in Montréal. The version you can download here is a tweaked, split-screen version of the “party build” you can find [on the GGJ website](http://globalgamejam.org/2014/games/pyramidwarf).

**Windows** : [pyramidwarf-final-1.01-windows.zip](http://theinstructionlimit.com/collegiennes/pyramidwarf-final-1.01-windows.zip) [12 Mb]

**Mac** : [pyramidwarf-final-1.01-mac.zip](http://theinstructionlimit.com/collegiennes/pyramidwarf-final-1.01-mac.zip) [12 Mb]

This was my first experience with Samuel in a jam, he’s a kickass vector artist currently working with Ko-Op on [GNOG](http://www.gnoggame.com/), which you should totally check out.

(the game was demoed at the [Montréal Joue Arcade 11](http://tag.hexagram.ca/events/arcade-11-tag-open-house/), too!)

We worked with Unity, as is the usual for me in game jams, and the initial idea was to make a stacking game where you’d either race the other player with a really unstable stack of little guys, or throw parts of your pyramid to the other player’s to break it up. And of course, this being a game jam, we didn’t do half of the stuff we planned for, and ended up with a super janky physics-based stacking game that happens to be silly enough to be fun!

On my side, it was my first time really exploiting Unity physics in a game. I’d done some basic rigid-body stuff and used character controllers ([Volkenessen](http://theinstructionlimit.com/volkenssen-global-game-jam-2012) was physics based as well), but never hinges or physics-based multi-body animation. One of the fun/interesting parts to do under pressure was the walk animation using torque and impulses : the leg pushes itself up, angles up, the body gets a magical shove and the legs readjust themselves to stay upright. It’s definitely not physically correct, but it looks like a bunch of cardboard puppets and that’s exactly what we were going for!

To build the pyramid, dwarves need to go *up* somehow, and the way we solved that is just… teleportation. These little guys have magic on their side, and they can teleport to the first free spot of the pyramid to keep stacking up. This caused rigidbody overlapping problems that I sorta resolved by just testing a whole lot if something’s there before teleporting, and denying the move otherwise.

The “final 1.01” build I posted here is not bug-free, but it’s shippable, so here goes. I might come back to it and fix rendering issues, and maybe implement dwarf-throwing, because it still sounds so great in my head.

Enjoy!

c joli! les anims de fond sont fluides! Elles sont faites avec l’éditeur d’anim unity ou avec une extension (je suis flasheur et je m’intéresse à unity3d ;-))

Merci! C’est fait avec juste des mouvements par script, rien de spécial. Par contre j’ai utilisé les courbes de gain & bias de Ken Perlin pour faire plus joli : http://blog.demofox.org/2012/09/24/bias-and-gain-are-your-friend/

ah c’est de la programmation artistique alors ;-).. Merci pour le lien trés intéressant!