---
title: 'Parkour Ninja update: first-person camera, physics, deferred rendering'
url: https://etodd.io/2011/08/13/parkour-ninja-update-first-person-camera-physics-deferred-rendering/
published: '2011-08-13'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Parkour Ninja update: first-person camera, physics, deferred rendering

Parkour Ninja is still alive! And it's looking more like Mirror's Edge now, complete with first-person camera. The old direction of the game just had too much frustration and not enough fun. Hopefully things will change now.

I re-integrated a physics engine, this time [BEPU physics](http://bepu.squarespace.com/), which is a screaming fast open-source XNA physics engine with unbelievable support. I was able to get my existing block simplification/rendering code to work with BEPU, so now you can add/remove blocks to/from existing objects on the fly. One cool side-effect of this ability is that I can also blast objects into smaller chunks... full-blown destruction is #1 on my list right now.

I also wrote a simple deferred renderer so I can enjoy practically unlimited point lights! Motion blur and bloom came as part of the deal. There are still some quirks with it, and I hope to eventually cover the whole thing in a few articles as I encounter issues.

Observe this tasteful, expertly-crafted demo video. And no, Parkour Ninja is not turning into Minecraft! I just needed a way to demonstrate the mutable physics objects, and clicking to remove blocks was the easiest way.