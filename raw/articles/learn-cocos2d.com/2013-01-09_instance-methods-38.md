---
title: Instance Methods
url: http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/protocol_c_c_r_g_b_a_protocol-p/
published: '2013-01-09'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
cocos2d-iphone
2.1
Improved Cocos2D API Reference (iOS version) for www.kobold2d.com developers
|

CC RGBA protocol.
[More...](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/protocol_c_c_r_g_b_a_protocol-p/#details)

`#import <CCProtocols.h>`


| (void) | -
|

CC RGBA protocol.

|
optional |

returns whether or not the opacity will be applied using glColor(R,G,B,opacity) or glColor(opacity, opacity, opacity, opacity);

| - (GLubyte) opacity |

returns the opacity

| - (void) setOpacity: | (GLubyte) | opacity |

sets the opacity.

|
optional |

sets the premultipliedAlphaOpacity property. If set to NO then opacity will be applied as: glColor(R,G,B,opacity); If set to YES then opacity will be applied as: glColor(opacity, opacity, opacity, opacity ); Textures with premultiplied alpha will have this property by default on YES. Otherwise the default value is NO