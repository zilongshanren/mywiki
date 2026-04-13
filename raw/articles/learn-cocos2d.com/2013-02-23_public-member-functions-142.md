---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_menu_item_label/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import <CCMenuItem.h>`




[List of all members.](/)


## Detailed Description

An abstract class for "label" [CCMenuItemLabel](../../../../../api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_menu_item_label/) items Any [CCNode](../../../../../api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_node/) that supports the [CCLabelProtocol](../../../../../api-ref/latest_2.x/cocos2d-iphone/html/protocol_c_c_label_protocol-p/) protocol can be added. Supported nodes:


## Member Function Documentation

initializes a [CCMenuItemLabel](../../../../../api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_menu_item_label/) with a Label and a block to execute. The block will be "copied". This is the designated initializer.

initializes a [CCMenuItemLabel](../../../../../api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_menu_item_label/) with a Label, target and selector. Internally it will create a block that executes the target/selector. The "target" won't be retained.

creates a [CCMenuItemLabel](../../../../../api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_menu_item_label/) with a Label and a block to execute. The block will be "copied".

creates a [CCMenuItemLabel](../../../../../api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_menu_item_label/) with a Label, target and selector. The "target" won't be retained.

sets a new string to the inner label


## Property Documentation

the color that will be used to disable the item


The documentation for this class was generated from the following file: