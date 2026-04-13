---
title: 'Day 134: Horde Catapult Shoot Animation'
url: https://alfredbaudisch.com/dailies/day-134-horde-catapult-shoot-animation/
author: Alfred Reinold Baudisch
published: '2021-07-22'
source_blog: Alfred Reinold Baudisch
source_site: https://alfredbaudisch.com
category: game programming
fetched: '2026-04-13'
---

With the lessons learned in the dailies [Day 132: Horde Catapult Rigged (Blender Linked Data Complexity)](https://alfredbaudisch.com/dailies/day-132-horde-catapult-rigged-blender-linked-data-complexity/) and [Day 133: Rigging Mechanism to Rotate Wheels](https://alfredbaudisch.com/dailies/day-133-rigging-mechanism-to-rotate-wheels/), today I managed to animate the catapult.

The wheels are rotated via a single controller, connected via a "Transformation" constraint. And this controller is connected to the root bone via another Transformation constraint. To animate the pushback, I moved the root bone 0.3m Y+, and then the wheels moved automagically, due to the root -> controller -> wheels connections.