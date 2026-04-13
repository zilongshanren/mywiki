---
title: Astrobunny ProjectFUN Prototype | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2011/11/astrobunny-projectfun-prototype/
author: Allen Chou
published: '2011-11-03'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

Astrobunny is my term project at [DigiPen](https://www.digipen.edu/) for this semester. We’re building the game with the game engine provided by the school, [DigiPen ProjectFUN](https://projectfun.digipen.edu/).

It’s a 2D top-down space-themed puzzle game, where the player controls a bunny in a spaceship that can jump from planet orbit to orbit.


Astrobunny is a bunny trapped in a spaceship launched for experimental purposes which we don’t know the details about.

The ship can enter a planet orbit and revolve about the planet.

The ship can also jump away from the orbit and enter free motion in space.

Depending on the orbital impact angle, the ship will either revolve about the planet clockwise or counterclockwise.

When in free motion, the ship consumes fuel. If the ship uses up all the fuel, it’s stuck in open space and it’s basically game over. The ship can also steer slightly while in free motion, consuming much more fuel. This encourages the player to aim more precisely for an orbital jump.

While orbiting a planet, the fuel replenishes.

There are fire/lava planets. Orbiting around such planets would increase the ship temperature. When the temperature is too high, the ship explodes. Of course, this means game over.

There are also ice planets. Orbiting around an ice planet causes the ship temperature to drop, even below freezing. If the temperature gets too low, the entire ship freezes and it’s also game over. However, the player can make the temperature below freezing to buy more time to orbit around larger fire/lava planets.

Throughout a level, there are energy orbs. The player must collect enough of them in order to clear the level.

The collected energy orbs will follow the ship in its traveled trail.

There is a sad planet in each level. The player must orbit around it to give it energy orbs to cheer it up.

When the sad planet is cheered up, it becomes a happy planet. A launch point will appear on the happy planet’s orbit.

Performing an orbital jump at the launch point launches the player into the next level.

This is basically the game mechanism. I’ll be giving a concept presentation tomorrow in class. I hope everything goes well 🙂