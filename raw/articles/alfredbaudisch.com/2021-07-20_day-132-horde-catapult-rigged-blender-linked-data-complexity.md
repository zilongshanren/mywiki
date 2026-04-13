---
title: 'Day 132: Horde Catapult Rigged (Blender Linked Data Complexity)'
url: https://alfredbaudisch.com/dailies/day-132-horde-catapult-rigged-blender-linked-data-complexity/
author: Alfred Reinold Baudisch
published: '2021-07-20'
source_blog: Alfred Reinold Baudisch
source_site: https://alfredbaudisch.com
category: game programming
fetched: '2026-04-13'
---

This is probably the hardest time I've had with a rig so far. It's so simple, yet so complex. Reasons and steps taken:

- The catapult was assembled with multiple copies of Linked objects and all of them had Modifiers.
- Each object (wheel, spike, body, arm and basket) were separate, with their own UV map and material. I parented them to the body, but still, they are not joined, only parented.
- How to assign the armature to the whole object? When I tried to assign it, it would go only to one individual object, not to the whole catapult itself.
- I had to create a copy of the .blend file, make the objects unique (remove linked data), apply all modifiers, then parent then all to the catapult body.
- Then I had to select ALL objects and then finally parent them to the armature.
- How to keep working with modifiers and linked data while having them parented to and weighted to an armature?
- Are Blender Linked Data and Parenting useless? Or do I always have to apply them all when the object is done? What if I have to make changes? Without the applied data, I'd have to repeat the changes accross all duplicated objects. What a pain in the arse.