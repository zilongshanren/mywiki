---
title: Scary Monsters and Nice Clouds
url: https://etodd.io/2012/10/12/scary-monsters-and-nice-clouds/
published: '2012-10-12'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Scary Monsters and Nice Clouds

### Nice Clouds

I got sick of my old pixelated skybox powered by Google Images and decided to make a real one. I used [Spacescape](http://alexcpeterson.com/spacescape) to generate a sufficiently trippy outer space skybox, chopped up some cloud photos in Gimp, fought with my code for a couple hours, and wha-la:

### Scary Monsters

What's that glowy green thing you say? It's the new monster I just added, creatively named "the vine". See that string of dark blocks coming out of it? It snakes its way to you and basically tries to constrict you to death. Here's another screenshot of its handiwork after running for a minute or two.

It uses a dumbed-down version of A* to find its way to the player. For performance reasons, if it doesn't find a path within a few hundred iterations, it just gives up and uses its best guess. It's not perfect, but it actually makes it a little more interesting, it behaves more like a living creature than an infallible machine. It can also burrow through blocks, which could be useful if the player decides to lure it somewhere. Like the tower enemies, it can only be defeated by destroying the infected green blocks at the base.

### More Voxel Performance Improvements

I keep wanting to expand the levels larger, and I keep hitting limitations in my engine. Luckily, so far I've been able to remove every major limitation. This week I made a ton of improvements in preparation for making the largest levels I've ever crafted:

- The entire level, even parts way beyond the field of vision, was being blasted in from the map file upon loading. Now it does a somewhat better job of loading it in as you explore.
- Adjacency info was also recalculated at load time, which slowed things down a lot. I now cache it in the map file. The downsides are larger map files and slower save times.
- Voxels, lights, and everything else are now put in a state of "suspension" when you leave the area, freeing up processor time for other work.
- Real-time voxel modifications are now partially multi-threaded. This helps a lot with framerate stutters.

That's it for this week. I have a few more minor engine updates to make, and hopefully next week I'll start knocking out more of these enemies I have floating around in my head.