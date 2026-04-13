---
title: Blender Notepad - Eulers
url: http://hacksoflife.blogspot.com/2015/11/blender-notepad-eulers.html
author: Benjamin Supnik
published: '2015-11-21'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

When Blender describes a rotation as an 'XYZ' Euler (with 3 angles), this is what they mean:




- The Z axis is "up" (the Y axis is away from us to be right-handed).
- Each rotation is around the named axis. So X is a rotation around the X axis (a "pitching up" rotation for pilots).
- The rotations are done in the order listed,
**extrinsically**. In other words, we rotate around each of these*global*axes.

*affected*by the Y and Z (because they happen later). If we were rotating around the rotated Y (Y') or rotated Z (Z'') axis, then the X axis would be unaffected.

The net result is that (from an aviation-angles perspective) we do yaw first (global Z is unaffected), then roll (transformed Y), then pitch (transformed X). (It should be noted that with pitch last, this does not even remotely correspond to how pilots think about these angles.)

To match X-Plane's transform, instead of XYZ, we need (in Blender) YXZ, which puts Y (roll) at lowest priority.

### How the 2.49 Exporter Goes to Crazy Town

Blender 2.75 lets you select orientations; 2.49 is always in XYZ mode. Since these are global axes, the correct order to apply them in an OBJ is:

ANIM_rotate 0 0 1

ANIM_rotate 0 1 0

ANIM_rotate 1 0 0

That is, apply Z first, since X-Plane only has

*local*transforms. (That is, in X-Plane, the*last*animation is affected by the prior two.)
When the Blender 2.49 exporter decomposes rotations into Eulers, it goes in this order, but it does so

*in X-Plane coordinates*. Thus while "yaw" is unchanged in XYZ animation in Blender, "roll" is unchanged in the export.
## No comments:

## Post a Comment