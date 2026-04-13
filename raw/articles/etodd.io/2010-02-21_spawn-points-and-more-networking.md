---
title: Spawn points and more networking
url: https://etodd.io/2010/02/21/spawn-points-and-more-networking/
published: '2010-02-21'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Spawn points and more networking

Networking has received yet another performance boost. I discarded Panda3D's network classes in favor of Python's sockets. I also switched to a single-threaded, non-blocking system that performs significantly better and clears up the messy Panda3D threads that were acting very strangely. I also improved the connection process; both the client and server now send packets to each other while connecting, in an attempt to punch through even the most draconian of NAT schemes.

In other news, I got bored of spawning within five feet of where I died, so I ditched the drop pods and added spawn points. Here's some demonstrative eye candy:

Currently, the game spawns units at the most "open" spawn point, that is, the one that is farthest away from any enemies. Given the small size of my multiplayer maps so far, it seems to work. As long as players keep moving around, it should produce fairly random arrangements. Still, it may become predictable. Any ideas for a better algorithm? Should I randomly pick a spawn point, and check to make sure it's open?

At any rate, your home dock is still a valid spawn point, but it's just one of several. I'm also thinking about making the dock more important by rewarding points for damaging it. Maybe it can't be destroyed, but I could add a turret to it that could be destroyed for points. More on that later...