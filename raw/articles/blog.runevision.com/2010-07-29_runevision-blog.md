---
title: runevision blog
url: https://blog.runevision.com/2010/07/
published: '2010-07-29'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

*This post is about The Cluster, my 2.5D platform game under development with focus on non-linear exploration, set in a big, continuous world. You can read all the posts about The Cluster here.*

I've been working on implementing path-finding for The Cluster, the 2.5D platform game I'm developing. Path-finding will let NPCs (enemies, companions, or other characters in the game) be able to find their way around in the world. For example, this will let them be able to chase/follow the player, or flee away from her.

So far I have a simple proof of concept with multiple red NPCs following the player (but not being quite perfect at it yet):

As mentioned before, some aspects of the game have come a long way already, while other are not even touched yet. I have yet to figure out and decide something as basic as what kind of game mechanics I want the game to focus on. I want game mechanics that create a focus on using the environment to one's advantage, and which makes use of the maneuverability of the enemies in an interesting way. But which mechanics can create that form of gameplay? I'm still a novice at game design.

In practically all platform games I've seen, enemies have exceedingly simple movement patterns and a very limited ability to move around in the level. Most often an enemy simply patrols a small path going back and forth or similar. My aim is to develop more engaging enemies that are almost as agile as the player. If anyone knows of existing games that have tackled this problem, I'd like to know!

I want the focus to stay on platforming though and not make it into a combat game. I don't care for twitch or combo based combat, but would prefer a small tactical element instead, using the local environment to one's advantage somehow.

I've thought about the 3 most dominant fighting mechanics in platform games:

**Jumping on enemies' heads**Like in*Mario*or*Sonic***Shooting**(typically horizontally and vertically only) Like in*Commander Keen*or*Cave Story***Melee**(I haven't played a lot of those -*Jak and Daxter*maybe? But that's 3D)

Early tests quickly revealed that jumping on enemies' heads don't work at all with agile enemies that move fast and unpredictably. All games with this mechanic have enemies that move rather slow or at least in a very predictable pattern.

Melee - I'm not sure how that would work well, as you'd have to always approach the enemies closely, which I *think* will make it harder to use the environment in an advantageous way.

Shooting from a distance seems like the best candidate to support the kind of gameplay i want, but I'm still not sure how to model the details of the game mechanics to encourage a play style based more on simple tactics than on head-on confrontation.