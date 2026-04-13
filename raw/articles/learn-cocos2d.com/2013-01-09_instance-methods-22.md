---
title: Instance Methods
url: http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_menu_item/
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

`#import <CCMenuItem.h>`


| (id) | +
|

|

| BOOL |
|

[CCMenuItem](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_menu_item/) base class

Subclass [CCMenuItem](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_menu_item/) (or any subclass) to create your custom [CCMenuItem](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_menu_item/) objects.

| - (void) activate |

Activate the item

| - (void) cleanup |

| - (id) initWithBlock: | (id sender) | block |

| - (id) initWithTarget: | (id) | target |
|
| selector: | (SEL) | selector |
|

| + (id) itemWithBlock: | (id sender) | block |

| + (id) itemWithTarget: | (id) | target |
|
| selector: | (SEL) | selector |
|

| - (CGRect) rect |

Returns the outside box in points

| - (void) selected |

The item was selected (not activated), similar to "mouse-over"

| - (void) setBlock: | (id sender) | block |

Sets the block that is called when the item is tapped. The block will be "copied".

| - (void) setIsEnabled: | (BOOL) | enabled |

| - (void) setTarget: | (id) | target |
|
| selector: | (SEL) | selector |
|

Sets the target and selector that is called when the item is tapped. target/selector will be implemented using blocks. "target" won't be retained.

| - (void) unselected |

The item was unselected

|
readnonatomicassign |

returns whether or not the item is selected

|
readwritenonatomicassign |

If enabled, it releases the block at cleanup time.