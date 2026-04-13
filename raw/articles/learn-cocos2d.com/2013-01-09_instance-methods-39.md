---
title: Instance Methods
url: http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/protocol_c_c_texture_protocol-p/
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

`#import <CCProtocols.h>`


| (
|

[CCNode](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_node/) objects that uses a Texture2D to render the images. The texture can have a blending function. If the texture has alpha premultiplied the default blending function is: src=GL_ONE dst= GL_ONE_MINUS_SRC_ALPHA else src=GL_SRC_ALPHA dst= GL_ONE_MINUS_SRC_ALPHA But you can change the blending function at any time.