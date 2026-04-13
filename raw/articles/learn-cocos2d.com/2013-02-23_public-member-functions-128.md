---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_label_b_m_font/
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

`#import <CCLabelBMFont.h>`


| (id) | -
|

[CCLabelBMFont](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_label_b_m_font/) is a subclass of [CCSpriteBatchNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_sprite_batch_node/)

Features:

Limitations:

[CCLabelBMFont](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_label_b_m_font/) implements the protocol [CCLabelProtocol](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/protocol_c_c_label_protocol-p/), like CCLabel and [CCLabelAtlas](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_label_atlas/). [CCLabelBMFont](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_label_b_m_font/) has the flexibility of CCLabel, the speed of [CCLabelAtlas](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_label_atlas/) and all the features of [CCSprite](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_sprite/). If in doubt, use [CCLabelBMFont](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_label_b_m_font/) instead of [CCLabelAtlas](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_label_atlas/) / CCLabel.

Supported editors:

| - (id) initWithString: | (NSString *) | string |
|
| fntFile: | (NSString *) | fntFile |
|

init a BMFont label with an initial string and the FNT file

| - (id) initWithString: | (NSString *) | string |
|
| fntFile: | (NSString *) | fntFile |
|
| width: | (float) | width |
|
| alignment: | (
|

init a BMFont label with an initial string and the FNT file, width, and alignment option

| - (id) initWithString: | (NSString *) | string |
|
| fntFile: | (NSString *) | fntFile |
|
| width: | (float) | width |
|
| alignment: | (
|

init a BMFont label with an initial string and the FNT file, width, alignment option and the offset of where the glyphs start on the .PNG image

| + (id) labelWithString: | (NSString *) | string |
|
| fntFile: | (NSString *) | fntFile |
|

creates a BMFont label with an initial string and the FNT file.

| + (id) labelWithString: | (NSString *) | string |
|
| fntFile: | (NSString *) | fntFile |
|
| width: | (float) | width |
|
| alignment: | (
|

creates a BMFont label with an initial string, the FNT file, width, and alignment option

| + (id) labelWithString: | (NSString *) | string |
|
| fntFile: | (NSString *) | fntFile |
|
| width: | (float) | width |
|
| alignment: | (
|

creates a BMFont label with an initial string, the FNT file, width, alignment option and the offset of where the glyphs start on the .PNG image

Purges the cached data. Removes from memory the cached configurations and the atlas name dictionary.