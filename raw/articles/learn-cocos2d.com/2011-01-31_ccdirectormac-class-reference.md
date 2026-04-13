---
title: CCDirectorMac Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_director_mac/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`

[CCDirectorMac.h](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/_c_c_director_mac_8h_source/)"

Inherits [CCDirector](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_director/).

Inherited by [CCDirectorDisplayLink](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_director_display_link/).

| (CGPoint) | -
|

Base class of Mac directors

| - (CGPoint) convertToLogicalCoordinates: | (CGPoint) | coordinates |

Converts window size coordiantes to logical coordinates. Useful only if resizeMode is kCCDirectorResize_Scale. If resizeMode is kCCDirectorResize_NoScale, then no conversion will be done.

| - (void) setFullScreen: | (BOOL) | fullscreen |

Sets the view in fullscreen or window mode