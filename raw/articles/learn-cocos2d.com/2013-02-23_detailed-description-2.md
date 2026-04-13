---
title: Detailed Description
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_stop_grid/
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

`#import <CCActionGrid.h>`


[CCStopGrid](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_stop_grid/) action. Don't call this action if another grid action is active. Call if you want to remove the the grid effect. Example: [Sequence actions:[Lens ...], [StopGrid action], nil];