---
title: CCMenuItem Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_menu_item/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`

[CCMenuItem.h](http://www.learn-cocos2d.com/)"

Inherits [CCNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_node/).

Inherited by [CCMenuItemLabel](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_menu_item_label/), [CCMenuItemSprite](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_menu_item_sprite/), and [CCMenuItemToggle](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_menu_item_toggle/).

| (void) | -
|

[CCMenuItem](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_menu_item/) base class

Subclass [CCMenuItem](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_menu_item/) (or any subclass) to create your custom [CCMenuItem](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_menu_item/) objects.

| - (void) activate |

Activate the item

| - (id) initWithTarget: | (id) | target |
||
| selector: | (SEL) | selector | ||

| + (id) itemWithTarget: | (id) | target |
||
| selector: | (SEL) | selector | ||

| - (CGRect) rect |

Returns the outside box in points

| - (void) selected |

The item was selected (not activated), similar to "mouse-over"

| - (void) unselected |

The item was unselected

- (BOOL) isSelected` [read, assign]` |

returns whether or not the item is selected