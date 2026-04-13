---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/structb2_distance_proxy/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <b2Distance.h>`


| void |
|

A distance proxy is used by the GJK algorithm. It encapsulates any shape.

Get the supporting vertex index in the given direction.

Get the supporting vertex in the given direction.

Get a vertex by index. Used by b2Distance.

| int32 b2DistanceProxy::GetVertexCount | ( | ) | const` [inline]` |

Get the vertex count.

Initialize the proxy using the given shape. The shape must remain in scope while the proxy is in use.