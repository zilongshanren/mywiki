---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_layer_multiplex/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCLayer.h>`


| id |
|

[CCLayerMultiplex](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_layer_multiplex/) is a [CCLayer](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_layer/) with the ability to multiplex it's children. Features:

initializes a MultiplexLayer with one or more layers using a variable argument list.

| id CCLayerMultiplex::layerWithLayers: | ( |
|

` [static, virtual]`

creates a CCMultiplexLayer with one or more layers using a variable argument list.

| void CCLayerMultiplex::switchTo: | ( | unsigned int | n | ) | ` [virtual]` |

switches to a certain layer indexed by n. The current (old) layer will be removed from it's parent with 'cleanup:YES'.

| void CCLayerMultiplex::switchToAndReleaseMe: | ( | unsigned int | n | ) | ` [virtual]` |

release the current layer and switches to another layer indexed by n. The current (old) layer will be removed from it's parent with 'cleanup:YES'.