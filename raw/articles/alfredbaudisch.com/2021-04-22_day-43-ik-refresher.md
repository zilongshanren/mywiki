---
title: 'Day 43: IK Refresher'
url: https://alfredbaudisch.com/dailies/day-43-ik-refresher/
author: Alfred Reinold Baudisch
published: '2021-04-22'
source_blog: Alfred Reinold Baudisch
source_site: https://alfredbaudisch.com
category: game programming
fetched: '2026-04-13'
---

In ancitipation to Ludum Dare this Saturday. This was frustrating. Hopefully, I won't forget it anymore.

## Process

- Extend from the tail of the leg bone
- Clear parent (ALT+P)
- Add pole target (add 3D cursor and then SHIFT+A to add a bone)

![](../../assets/630f20ea0a8b1e86.png)


- Uncheck Deform from Pole Target
- Go to Pose Mode, select FIRST the IK bone, then the leg bone
- Then SHIFT+CONTROL+C and choose IK
- Select the leg bone and adjust the IK constraint values

![](../../assets/376780c2ccbbd8cc.png)


![](../../assets/7fbcf4090d27fda8.png)


- If the bones are not rotating when moving the IK, reset the chain length.

### Parenting and Assigning Bones

- Symmetrize the armature in edit mode (select all bones first)
- Object mode, select the mesh/human/whatever, then shift+click armature
- CTRL+P and choose with weights or empty groups