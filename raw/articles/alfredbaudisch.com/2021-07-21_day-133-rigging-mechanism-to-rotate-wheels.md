---
title: 'Day 133: Rigging Mechanism to Rotate Wheels'
url: https://alfredbaudisch.com/dailies/day-133-rigging-mechanism-to-rotate-wheels/
author: Alfred Reinold Baudisch
published: '2021-07-21'
source_blog: Alfred Reinold Baudisch
source_site: https://alfredbaudisch.com
category: game programming
fetched: '2026-04-13'
---

After a lot of thinkering, I learned and managed a way to rotate a bone (for example, for a wheel), using another bone as the controller, by adding a Transformation constraint, which I've never used before. TL;DR; Blender Transformative constraint in a bone / armature to rotate/spin wheels.

Today's daily, also made me take a drastic decision: for 3D games I'll start using Unity. Unity handles those animations and 3D asset changes so much better than Godot. Also, Godot couldn't handle the rotate wheel animation correctly in any way, while Unity played it accordingly out of the box.

I love Godot, but it's not the first time that I've had a lot of trouble with its 3D workflow.