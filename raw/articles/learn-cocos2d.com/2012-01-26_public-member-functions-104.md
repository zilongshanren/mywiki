---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone-mac/html/protocol_c_c_r_g_b_a_protocol-p/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

CC RGBA protocol.
[More...](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone-mac/html/protocol_c_c_r_g_b_a_protocol-p/#details)

`#include <CCProtocols.h>`


| void |
|

CC RGBA protocol.

returns whether or not the opacity will be applied using glColor(R,G,B,opacity) or glColor(opacity, opacity, opacity, opacity);

sets the opacity.

sets the premultipliedAlphaOpacity property. If set to NO then opacity will be applied as: glColor(R,G,B,opacity); If set to YES then oapcity will be applied as: glColor(opacity, opacity, opacity, opacity ); Textures with premultiplied alpha will have this property by default on YES. Otherwise the default value is NO