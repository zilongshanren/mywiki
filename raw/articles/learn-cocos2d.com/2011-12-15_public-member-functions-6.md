---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone-mac/html/interface_c_c_particle_system_quad/
published: '2011-12-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCParticleSystemQuad.h>`




[List of all members.](../../../../../api-ref/1.0/cocos2d-iphone-mac/html/interface_c_c_particle_system_quad-members/)


## Detailed Description

[CCParticleSystemQuad](../../../../../api-ref/1.0/cocos2d-iphone-mac/html/interface_c_c_particle_system_quad/) is a subclass of [CCParticleSystem](../../../../../api-ref/1.0/cocos2d-iphone-mac/html/interface_c_c_particle_system/)

It includes all the features of ParticleSystem.

Special features and Limitations:

- Particle size can be any float number.
- The system can be scaled
- The particles can be rotated
- On 1st and 2nd gen iPhones: It is only a bit slower that
[CCParticleSystemPoint](../../../../../api-ref/1.0/cocos2d-iphone-mac/html/interface_c_c_particle_system_point/)
- On 3rd gen iPhone and iPads: It is MUCH faster than
[CCParticleSystemPoint](../../../../../api-ref/1.0/cocos2d-iphone-mac/html/interface_c_c_particle_system_point/)
- It consumes more RAM and more GPU memory than
[CCParticleSystemPoint](../../../../../api-ref/1.0/cocos2d-iphone-mac/html/interface_c_c_particle_system_point/)
- It supports subrects
**Since:**- v0.8



## Member Function Documentation

| void CCParticleSystemQuad::initIndices |
( |
| ) |
` [virtual]` |

initialices the indices for the vertices

| void CCParticleSystemQuad::initTexCoordsWithRect: |
( |
CGRect |
*rect* | ) |
` [virtual]` |

initilizes the texture with a rectangle measured Points

| void CCParticleSystemQuad::setDisplayFrame: |
( |
[CCSpriteFrame](../../../../../api-ref/1.0/cocos2d-iphone-mac/html/interface_c_c_sprite_frame/) * |
*spriteFrame* | ) |
` [virtual]` |

Sets a new [CCSpriteFrame](../../../../../api-ref/1.0/cocos2d-iphone-mac/html/interface_c_c_sprite_frame/) as particle. WARNING: this method is experimental. Use setTexture:withRect instead.

**Since:**- v0.99.4

| void CCParticleSystemQuad::setTexture:withRect: |
( |
[CCTexture2D](../../../../../api-ref/1.0/cocos2d-iphone-mac/html/interface_c_c_texture2_d/) * |
*texture*, |
|
|
[withRect] CGRect |
*rect* |
|
) |
| ` [virtual]` |

Sets a new texture with a rect. The rect is in Points.

**Since:**- v0.99.4


The documentation for this interface was generated from the following file: