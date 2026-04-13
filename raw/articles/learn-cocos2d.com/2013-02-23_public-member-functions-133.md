---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_layer_multiplex/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

![]() |
cocos2d-iphone
2.1
Improved Cocos2D API Reference (iOS version) for www.kobold2d.com developers
|

`#import <CCLayer.h>`


| (id) | -
|

[CCLayerMultiplex](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_layer_multiplex/) is a [CCLayer](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_layer/) with the ability to multiplex its children. Features:

initializes a CCMultiplexLayer with an array of layers

initializes a MultiplexLayer with one or more layers using a variable argument list.

creates a CCMultiplexLayer with an array of layers.

creates a CCMultiplexLayer with one or more layers using a variable argument list.

switches to a certain layer indexed by n. The current (old) layer will be removed from its parent with 'cleanup:YES'.

release the current layer and switches to another layer indexed by n. The current (old) layer will be removed from its parent with 'cleanup:YES'.