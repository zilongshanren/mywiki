---
title: CCRibbon Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_ribbon/
published: '2011-01-25'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`

[CCRibbon.h](http://www.learn-cocos2d.com/)"

Inherits [CCNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_node/), and [CCTextureProtocol-p](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/protocol_c_c_texture_protocol-p/).

| (void) | -
|

A [CCRibbon](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_ribbon/) is a dynamically generated list of polygons drawn as a single or series of triangle strips. The primary use of [CCRibbon](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_ribbon/) is as the drawing class of Motion Streak, but it is quite useful on it's own. When manually drawing a ribbon, you can call addPointAt and pass in the parameters for the next location in the ribbon. The system will automatically generate new polygons, texture them accourding to your texture width, etc, etc.

[CCRibbon](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_ribbon/) data is stored in a [CCRibbonSegment](http://www.learn-cocos2d.com/) class. This class statically allocates enough verticies and texture coordinates for 50 locations (100 verts or 48 triangles). The ribbon class will allocate new segments when they are needed, and reuse old ones if available. The idea is to avoid constantly allocating new memory and prefer a more static method. However, since there is no way to determine the maximum size of some ribbons (motion streaks), a truely static allocation is not possible.

| - (void) addPointAt: | (CGPoint) | location |
||
| width: | (float) | w | ||

add a point to the ribbon

| - (id) initWithWidth: | (float) | w |
||
| image: | (NSString *) | path |
||
| length: | (float) | l |
||
| color: | (
|

init the ribbon

| + (id) ribbonWithWidth: | (float) | w |
||
| image: | (NSString *) | path |
||
| length: | (float) | l |
||
| color: | (
|

creates the ribbon

| - (float) sideOfLine: | (CGPoint) | p |
||
| l1: | (CGPoint) | l1 |
||
| l2: | (CGPoint) | l2 | ||

determine side of line

- (float) textureLength` [read, write, assign]` |

Texture lengths in pixels