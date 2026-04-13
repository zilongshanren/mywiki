---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/protocol_c_c_texture_protocol-p/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCProtocols.h>`


|

[CCNode](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_node/) objects that uses a Texture2D to render the images. The texture can have a blending function. If the texture has alpha premultiplied the default blending function is: src=GL_ONE dst= GL_ONE_MINUS_SRC_ALPHA else src=GL_SRC_ALPHA dst= GL_ONE_MINUS_SRC_ALPHA But you can change the blending funtion at any time.

sets a new texture. it will be retained