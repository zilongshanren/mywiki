---
title: Meshes of navigation
url: https://etodd.io/2010/05/08/meshes-of-navigation/
published: '2010-05-08'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Meshes of navigation

**Update 8/23/2011:** the source/executable for the navigation mesh .obj exporter is [here](http://www.mediafire.com/?qdf8ivrv9dqxj37). Import a mesh, set up the parameters (only simple mode is supported right now), and have it generate the mesh. It should output a .obj file in the directory where it was executed.

The AI system has finally received a massive and desperately needed update: support for navigation meshes. That means the bots shouldn't get stuck running into walls all the time, or running back and forth between waypoints like machines. I think this was probably the biggest weakness of the game up until now; the AI is still something of a problem, but it's much better.

I stumbled across an incredible open source project called [Recast](http://code.google.com/p/recastnavigation/), which is an extremely reliable automatic navigation mesh generator. It rasterizes your polygon soup into a giant voxel, finds the edges, discards non-traversable nodes (based on customizable parameters), and simplifies the resulting geometry. Try the demo, it's amazing.

Since it's open source, I was able to modify the Recast demo to export a .obj file containing the generated navigation mesh, which is then imported into Blender, and then exported to Panda3D's .egg model format, from which I can extract vertex data in the game. I may write some utilities to simplify this process, but for now it does just fine, and beats the heck out of creating the nav meshes manually. I'll probably release the modified Recast demo too, since it was a bit of a pain to get working.

Anyway, here's a visualization of the whole process, from generation in Recast, to converting and simplification in Blender, to practical application in the game. The last screenshot shows a visualization of the pathfinding data in-game. I'll cover the details of the pathfinding implementation later, but right now I need to sleep.

[gallery link="file"]