---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone-mac/html/interface_c_c_menu_item/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCMenuItem.h>`


| id |
|

[CCMenuItem](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone-mac/html/interface_c_c_menu_item/) base class

Subclass [CCMenuItem](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone-mac/html/interface_c_c_menu_item/) (or any subclass) to create your custom [CCMenuItem](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone-mac/html/interface_c_c_menu_item/) objects.

| void CCMenuItem::activate | ( | ) | ` [virtual]` |

Activate the item

| id CCMenuItem::initWithTarget:selector: | ( | id | target, |
| [selector] SEL | selector |
||
| ) | ` [virtual]` |

| id CCMenuItem::itemWithTarget:selector: | ( | id | target, |
| [selector] SEL | selector |
||
| ) | ` [static, virtual]` |

| CGRect CCMenuItem::rect | ( | ) | ` [virtual]` |

Returns the outside box in points

| void CCMenuItem::selected | ( | ) | ` [virtual]` |

The item was selected (not activated), similar to "mouse-over"

| void CCMenuItem::setIsEnabled: | ( | BOOL | enabled | ) | ` [virtual]` |

| void CCMenuItem::unselected | ( | ) | ` [virtual]` |

The item was unselected

BOOL CCMenuItem::isSelected` [read, assign]` |

returns whether or not the item is selected