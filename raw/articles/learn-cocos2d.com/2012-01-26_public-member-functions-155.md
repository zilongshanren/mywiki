---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node_bounding_area/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CC3BoundingVolumes.h>`


| BOOL |
|

A bounding volume that defines a 2D bounding area for a node, and checks that bounding area against a given 2D bounding box, which is typically the bounding box of the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/), instead of the camera frustum.

This is useful for, and only applicable to, nodes that draw 2D content, such as CC3Billboards,

By default, instances of [CC3NodeBoundingArea](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node_bounding_area/) return NO in the doesIntersectFrustum: method, so nodes with this bounding volume will not be drawn when 3D nodes with local content are drawn. Instead, [CC3NodeBoundingArea](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node_bounding_area/) adds the doesIntersectBounds: method, which is invokded to test a 2D node boundary against a 2D bounding box.

| BOOL CC3NodeBoundingArea::doesIntersectBounds: | ( | CGRect | bounds | ) | ` [virtual]` |

Returns whether this bounding volume intersects the specfied bounding rectangle.

This default implementation always returns YES. Subclasses will override appropriately.

This method is invoked automatically by nodes with 2D content, whenever it needs to determine whether or not it should be drawn.