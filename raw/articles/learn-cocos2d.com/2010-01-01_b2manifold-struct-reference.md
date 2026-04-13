---
title: b2Manifold Struct Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/structb2_manifold/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# b2Manifold Struct Reference

`#include <`[b2Collision.h](/)>


[List of all members.](/)


## Detailed Description

A manifold for two touching convex shapes. Box2D supports multiple types of contact:

- clip point versus plane with radius
- point versus point with radius (circles) The local point usage depends on the manifold type: -e_circles: the local center of circleA -e_faceA: the center of faceA -e_faceB: the center of faceB Similarly the local normal usage: -e_circles: not used -e_faceA: the normal on polygonA -e_faceB: the normal on polygonB We store contacts in this way so that position correction can account for movement, which is critical for continuous physics. All contact scenarios must be expressed in one of these types. This structure is stored across time steps, so we keep it small.


## Member Enumeration Documentation

**Enumerator: **
e_circles |
|
e_faceA |
|
e_faceB |
|



## Member Data Documentation

not use for Type::e_points

usage depends on manifold type

the number of manifold points


The documentation for this struct was generated from the following file: