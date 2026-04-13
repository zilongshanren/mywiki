---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_menu_item_label/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCMenuItem.h>`


| id |
|

An abstract class for "label" [CCMenuItemLabel](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_menu_item_label/) items Any [CCNode](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_node/) that supports the [CCLabelProtocol](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/protocol_c_c_label_protocol-p/) protocol can be added. Supported nodes:

| void CCMenuItemLabel::setIsEnabled: | ( | BOOL | enabled | ) | ` [virtual]` |

| void CCMenuItemLabel::setString: | ( | NSString * | label | ) | ` [virtual]` |

sets a new string to the inner label

the color that will be used to disable the item