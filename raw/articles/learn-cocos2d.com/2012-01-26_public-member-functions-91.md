---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone-extensions/html/interface_c_c_menu_advanced/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

| void |
|

some aditional features.

1) Selecting and activating CCMenuItems with Keyboard (by default next/prev bindings aren't set - set them manually or use one of align methods to bind arrows for this). 2) One of CCMenuItems can be set as escapeDelegate - so it will be activated by pressing escape 3) align left->right, right->left, bottom->top, top->bottom with autosetting self contentSize 4) externalBoundsRect - if it is set then menu items will be scrollable inside these bounds 5) priority property - must be set before onEnter to make it register with that priority

| void CCMenuAdvanced::alignItemsHorizontallyWithPadding: | ( | float | padding | ) | ` [virtual]` |

AlignH items horizontal from left to right.

| padding | space between elements. |

| void CCMenuAdvanced::alignItemsHorizontallyWithPadding:leftToRight: | ( | float | padding, |
| [leftToRight] BOOL | leftToRight |
||
| ) | ` [virtual]` |

Designated alignHorizontal Method

| padding | space between elements. |
| leftRoRight | If YES - align items from left to right, if NO - right to left. |

| void CCMenuAdvanced::alignItemsVerticallyWithPadding: | ( | float | padding | ) | ` [virtual]` |

Designated alignVerticall from bottom to top.

| padding | space between elements. |

| void CCMenuAdvanced::alignItemsVerticallyWithPadding:bottomToTop: | ( | float | padding, |
| [bottomToTop] BOOL | bottomToTop |
||
| ) | ` [virtual]` |

Designated alignVerticall Method

| padding | space between elements. |
| bottomToTop | If YES - align items from bottom to top, if NO - top to bottom. |

| void CCMenuAdvanced::fixPosition | ( | ) | ` [virtual]` |

Changes menu position to stay inside of boundaryRect if it is non-null.

CGRect CCMenuAdvanced::boundaryRect` [read, write, assign]` |

Rectangle in parent's coordinate system, which menu must fill with it's boundingBox.

Note: boundaryRect must have greater size then menu's boundingBox to make scrolling possible. Think about boundaryRect like about hole in paper sheet under which you would like to put [CCMenuAdvanced](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone-extensions/html/interface_c_c_menu_advanced/) and scroll it, but you never want to see the table - hole must be covered with paper.

BOOL CCMenuAdvanced::isDisabled` [read, write, assign]` |

If YES - all touches & keyboard events will be ignored. If NO - all events will work, except for disabled items. Default is NO.

CGFloat CCMenuAdvanced::minimumTouchLengthToSlide` [read, write, assign]` |

Minimum length of touch, that will disable selected menu item & start scrolling.

NSInteger CCMenuAdvanced::priority` [read, write, assign]` |

Priority property for touch, mouse & keyboard for menu. Must be set before onEnter called.