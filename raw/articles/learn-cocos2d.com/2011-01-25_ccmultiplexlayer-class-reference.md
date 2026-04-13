---
title: CCMultiplexLayer Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_multiplex_layer/
published: '2011-01-25'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`

[CCLayer.h](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/_c_c_layer_8h_source/)"

Inherits [CCLayer](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_layer/).

| (id) | -
|

CCMultipleLayer is a [CCLayer](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_layer/) with the ability to multiplex it's children. Features:

initializes a MultiplexLayer with one or more layers using a variable argument list.

| - (void) switchTo: | (unsigned int) | n |

switches to a certain layer indexed by n. The current (old) layer will be removed from it's parent with 'cleanup:YES'.

| - (void) switchToAndReleaseMe: | (unsigned int) | n |

release the current layer and switches to another layer indexed by n. The current (old) layer will be removed from it's parent with 'cleanup:YES'.