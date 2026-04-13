---
title: CCParticleSystemQuad Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_particle_system_quad/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`[CCParticleSystemQuad.h](/)"


Inherits [CCParticleSystem](../../../unofficial-cocos2d-api-reference/html/interface_c_c_particle_system/).

[List of all members.](/)


## Detailed Description

[CCParticleSystemQuad](../../../unofficial-cocos2d-api-reference/html/interface_c_c_particle_system_quad/) is a subclass of [CCParticleSystem](../../../unofficial-cocos2d-api-reference/html/interface_c_c_particle_system/)

It includes all the features of ParticleSystem.

Special features and Limitations:

- Particle size can be any float number.
- The system can be scaled
- The particles can be rotated
- On 1st and 2nd gen iPhones: It is only a bit slower that
[CCParticleSystemPoint](/)
- On 3rd gen iPhone and iPads: It is MUCH faster than
[CCParticleSystemPoint](/)
- It consumes more RAM and more GPU memory than
[CCParticleSystemPoint](/)
- It supports subrects
**Since:**- v0.8



## Member Function Documentation

initialices the indices for the vertices

| - (void) initTexCoordsWithRect: |
|
(CGRect) |
*rect* |
|
|

initilizes the texture with a rectangle measured Points

Sets a new [CCSpriteFrame](/) as particle. WARNING: this method is experimental. Use setTexture:withRect instead.

**Since:**- v0.99.4

| - (void) setTexture: |
|
([CCTexture2D](../../../unofficial-cocos2d-api-reference/html/interface_c_c_texture2_d/) *) |
*texture* |
| withRect: |
|
(CGRect) |
*rect* | |
|
|
| | |

Sets a new texture with a rect. The rect is in Points.

**Since:**- v0.99.4


The documentation for this class was generated from the following file: