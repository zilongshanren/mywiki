---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone-extensions/html/interface_c_c_scroll_layer/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCScrollLayer.h>`


| id |
|

Scrolling layer for Menus, like iOS Springboard Screen.

It is a very clean and elegant subclass of CCLayer that lets you pass-in an array of layers and it will then create a smooth scroller. Complete with the "snapping" effect. You can create screens with anything that can be added to a CCLayer.

| void CCScrollLayer::addPage: | ( | CCLayer * | aPage | ) | ` [virtual]` |

Adds new page to the right end of the scroll layer.

| void CCScrollLayer::addPage:withNumber: | ( | CCLayer * | aPage, |
| [withNumber] int | pageNumber |
||
| ) | ` [virtual]` |

Adds new page and reorders pages trying to set given number for newly added page. If number > pages count - adds new page to the right end of the scroll layer. If number <= 0 - adds new page to the left end of the scroll layer.

| id CCScrollLayer::initWithLayers:widthOffset: | ( | NSArray * | layers, |
| [widthOffset] int | widthOffset |
||
| ) | ` [virtual]` |

Inits scrollLayer with given pages & width offset.

| layers | NSArray of CCLayers, that will be used as pages. |
| widthOffset | Length in X-coord, that describes length of possible pages intersection. |

| id CCScrollLayer::nodeWithLayers:widthOffset: | ( | NSArray * | layers, |
| [widthOffset] int | widthOffset |
||
| ) | ` [static, virtual]` |

Creates new scrollLayer with given pages & width offset.

| layers | NSArray of CCLayers, that will be used as pages. |
| widthOffset | Length in X-coord, that describes length of possible pages intersection. |

| void CCScrollLayer::removePage: | ( | CCLayer * | aPage | ) | ` [virtual]` |

Removes page if it's one of scroll layers pages (not children) Does nothing if page not found.

| void CCScrollLayer::removePageWithNumber: | ( | int | page | ) | ` [virtual]` |

Removes page with given number. Doesn nothing if there's no page for such number.

| void CCScrollLayer::updatePages | ( | ) | ` [virtual]` |

Updates all pages positions & adds them as children if needed. Can be used to update position of pages after screen reshape, or for update after dynamic page add/remove.

int CCScrollLayer::currentScreen` [read, assign]` |

Current page number, that is shown. Belongs to the [0, totalScreen] interval.

CGFloat CCScrollLayer::marginOffset` [read, write, assign]` |

Offset that can be used to let user see empty space over first or last page.

CGFloat CCScrollLayer::minimumTouchLengthToChangePage` [read, write, assign]` |

Calibration property. Minimum moving touch length that is enough to change the page, without snapping back to the previous selected page.

CGFloat CCScrollLayer::minimumTouchLengthToSlide` [read, write, assign]` |

Calibration property. Minimum moving touch length that is enough to cancel menu items and start scrolling a layer.

NSArray* CCScrollLayer::pages` [read, assign]` |

Returns array of pages CCLayer's

ccColor4B CCScrollLayer::pagesIndicatorNormalColor` [read, write, assign]` |

Color of dots, that represents other pages.

CGPoint CCScrollLayer::pagesIndicatorPosition` [read, write, assign]` |

Position of dots center in parent coordinates. (Default value is screenWidth/2, screenHeight/4)

ccColor4B CCScrollLayer::pagesIndicatorSelectedColor` [read, write, assign]` |

Color of dot, that represents current selected page(only one dot).

CGFloat CCScrollLayer::pagesWidthOffset` [read, write, assign]` |

Offset, that can be used to let user see next/previous page.

BOOL CCScrollLayer::showPagesIndicator` [read, write, assign]` |

Whenever show or not white/grey dots under the scroll layer. If yes - dots will be rendered in parents transform (rendered after scroller visit).

BOOL CCScrollLayer::stealTouches` [read, write, assign]` |

If YES - when starting scrolling [CCScrollLayer](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone-extensions/html/interface_c_c_scroll_layer/) will claim touches, that are already claimed by others targetedTouchDelegates by calling CCTouchDispatcher::touchesCancelled Usefull to have ability to scroll with touch above menus in pages. If NO - scrolling will start, but no touches will be cancelled. Default is YES.

int CCScrollLayer::totalScreens` [read, assign]` |

Total pages available in scrollLayer.