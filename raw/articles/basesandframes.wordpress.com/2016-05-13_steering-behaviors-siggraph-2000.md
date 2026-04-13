---
title: Steering Behaviors – Siggraph 2000
url: https://basesandframes.wordpress.com/2016/05/13/steering-behaviors-siggraph-2000/
author: Robingreen
published: '2016-05-13'
source_blog: Bases and Frames
source_site: https://basesandframes.wordpress.com
category: graphics
fetched: '2026-04-13'
---

Based on the work I did at Bullfrog Productions for *Dungeon Keeper 2* and *Theme Park World* on flocking crowd movement in user editable worlds, I was asked by [Craig Reynolds](http://www.red3d.com/cwr/) to join a group that would be presenting a Siggraph tutorial course on game development tech. The concept of flocking scored Craig a Scientific and Engineering Award at the 70th Academy Awards in 1998 and I’m pretty sure he used this as leverage to score a whole day Tutorial.

I had used his [page on steering behaviors](http://www.red3d.com/cwr/steer/) and had implemented much of it, writing up my results, made a live Win32 demo, added a few new behaviors and documenting the gotchas for flocking in non-static worlds. At the time there was practically no gamedev representation in the academic and production heavy Siggraph so we were pretty much the advance guard.

The ideas seem a little quaint now, especially the lack of any coherent methods of blending between steering behaviors over time. Much of the actual production code for pathfinding and was in 16-bit fixed-point using incremental Voronoi triangulation, written by Ian Shaw and created for raw speed on the original Playstation (a version which Bullfrog never shipped).

Shortly after presenting at Siggraph 2000 I was hired by SCEA to work in the SF bay area with Craig. A nicer bloke you could not hope to meet and walking the halls of Siggraph beside him was always an education – he knows *everyone* and it takes forever to get anywhere.