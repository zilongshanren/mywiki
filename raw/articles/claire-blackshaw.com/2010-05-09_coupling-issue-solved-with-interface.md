---
title: Coupling Issue solved with Interface
url: https://claire-blackshaw.com/blog/2010/05/coupling-issue-solved-with-interface/
author: Claire Blackshaw
published: '2010-05-09'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

![Coupling Issue solved with Interface](../../assets/4e402aebc4c1a4e8.png)

Ye gods captain, PROGRESS.

After the dismal run around the pointlessness I have actually made some progress last night and today.

- Coupling Issue solved with Interface
- Island has day/night cycle
- Shop Blimp interior & exterior modelled
- Blimp added to world
- Add a reliable help to translate between tile and world space
- Started work on Sky Box

Coupling Issue

Okay so we don’t want the model (island & prop data) coupled to the view (scene graph, animations, models). Well the solution was to give every node in the scene graph a user data element which had an interface.

The core functions being, Update & Pre-Render. Further functions and event handles can be added to the interface to handle animations and the like. The interface is the façade which prevents tight coupling. Neat and clean, kicking myself for not seeing this solution weeks ago.

Sky Box

My reason for posting, indirectly. I waster the last hour or so trying to generate normal & height maps for clouds. Reading up on things I already knew how todo if I stopped and thought for a second. The moment I saw my folly I stopped to write this to break me out of it.

I will now grab some food then hopefully not be stupid.