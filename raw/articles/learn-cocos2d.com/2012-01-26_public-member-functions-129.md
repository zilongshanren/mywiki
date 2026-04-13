---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_ribbon/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCRibbon.h>`


| id |
|

A [CCRibbon](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_ribbon/) is a dynamically generated list of polygons drawn as a single or series of triangle strips. The primary use of [CCRibbon](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_ribbon/) is as the drawing class of Motion Streak, but it is quite useful on it's own. When manually drawing a ribbon, you can call addPointAt and pass in the parameters for the next location in the ribbon. The system will automatically generate new polygons, texture them accourding to your texture width, etc, etc.

[CCRibbon](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_ribbon/) data is stored in a [CCRibbonSegment](http://www.learn-cocos2d.com/) class. This class statically allocates enough verticies and texture coordinates for 50 locations (100 verts or 48 triangles). The ribbon class will allocate new segments when they are needed, and reuse old ones if available. The idea is to avoid constantly allocating new memory and prefer a more static method. However, since there is no way to determine the maximum size of some ribbons (motion streaks), a truely static allocation is not possible.

| void CCRibbon::addPointAt:width: | ( | CGPoint | location, |
| [width] float | w |
||
| ) | ` [virtual]` |

add a point to the ribbon

| id CCRibbon::initWithWidth:image:length:color:fade: | ( | float | w, |
| [image] NSString * | path, |
||
| [length] float | l, |
||
| [color]
|

` [virtual]`

init the ribbon

| id CCRibbon::ribbonWithWidth:image:length:color:fade: | ( | float | w, |
| [image] NSString * | path, |
||
| [length] float | l, |
||
| [color]
|

` [static, virtual]`

creates the ribbon

| float CCRibbon::sideOfLine:l1:l2: | ( | CGPoint | p, |
| [l1] CGPoint | l1, |
||
| [l2] CGPoint | l2 |
||
| ) | ` [virtual]` |

determine side of line

float CCRibbon::textureLength` [read, write, assign]` |

Texture lengths in pixels