---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/interface_c_c_scroll_layer/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
cocos2d-iphone-extensions
0.2
Cocos2D Extensions API Reference (iOS version) for www.kobold2d.com developers
|

`#import <CCScrollLayer.h>`


| (id) | -
|

Scrolling layer for Menus, like iOS Springboard Screen.

It is a very clean and elegant subclass of CCLayer that lets you pass-in an array of layers and it will then create a smooth scroller. Complete with the "snapping" effect. You can create screens with anything that can be added to a CCLayer.

Adds new page and reorders pages trying to set given number for newly added page. If number > pages count - adds new page to the right end of the scroll layer. If number <= 0 - adds new page to the left end of the scroll layer.

| - (id) initWithLayers: | (NSArray *) | layers |
|
| widthOffset: | (int) | widthOffset |
|

Inits scrollLayer with given pages & width offset.

| layers | NSArray of CCLayers, that will be used as pages. |
| widthOffset | Length in X-coord, that describes length of possible pages intersection. |

| + (id) nodeWithLayers: | (NSArray *) | layers |
|
| widthOffset: | (int) | widthOffset |
|

Creates new scrollLayer with given pages & width offset.

| layers | NSArray of CCLayers, that will be used as pages. |
| widthOffset | Length in X-coord, that describes length of possible pages intersection. |

Removes page if it's one of scroll layers pages (not children) Does nothing if page not found.

Removes page with given number. Doesn nothing if there's no page for such number.

Updates all pages positions & adds them as children if needed. Can be used to update position of pages after screen reshape, or for update after dynamic page add/remove.

Current page number, that is shown. Belongs to the [0, totalScreen] interval.

Offset that can be used to let user see empty space over first or last page.

Calibration property. Minimum moving touch length that is enough to change the page, without snapping back to the previous selected page.

Calibration property. Minimum moving touch length that is enough to cancel menu items and start scrolling a layer.

Color of dots, that represents other pages.

Position of dots center in parent coordinates. (Default value is screenWidth/2, screenHeight/4)

Color of dot, that represents current selected page(only one dot).

Offset, that can be used to let user see next/previous page.

Whenever show or not white/grey dots under the scroll layer. If yes - dots will be rendered in parents transform (rendered after scroller visit).

If YES - when starting scrolling [CCScrollLayer](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/interface_c_c_scroll_layer/) will claim touches, that are already claimed by others targetedTouchDelegates by calling CCTouchDispatcher::touchesCancelled Usefull to have ability to scroll with touch above menus in pages. If NO - scrolling will start, but no touches will be cancelled. Default is YES.