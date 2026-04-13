---
title: CCDirectorDisplayLink Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_director_display_link/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`[CCDirectorIOS.h](../../../unofficial-cocos2d-api-reference/html/_c_c_director_i_o_s_8h_source/)"


Inherits [CCDirectorMac](../../../unofficial-cocos2d-api-reference/html/interface_c_c_director_mac/), and [CCDirectorIOS](../../../unofficial-cocos2d-api-reference/html/interface_c_c_director_i_o_s/).

[List of all members.](/)


## Detailed Description

DisplayLinkDirector is a Director that synchronizes timers with the refresh rate of the display.

Features and Limitations:

- Only available on 3.1+
- Scheduled timers & drawing are synchronizes with the refresh rate of the display
- Only supports animation intervals of 1/60 1/30 & 1/15

It is the recommended Director if the SDK is 3.1 or newer

**Since:**- v0.8.2


The documentation for this class was generated from the following files:

- /depot/cocosdocs/cocos2d-iphone-0.99.5/cocos2d/Platforms/iOS/
[CCDirectorIOS.h](../../../unofficial-cocos2d-api-reference/html/_c_c_director_i_o_s_8h_source/)
- /depot/cocosdocs/cocos2d-iphone-0.99.5/cocos2d/Platforms/Mac/
[CCDirectorMac.h](../../../unofficial-cocos2d-api-reference/html/_c_c_director_mac_8h_source/)