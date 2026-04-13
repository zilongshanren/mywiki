---
title: Instance Methods
url: http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/protocol_c_c_director_delegate-p/
published: '2013-01-09'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import <CCProtocols.h>`




| - (void) directorDidReshapeProjection: |
|
([CCDirector](../../../../../../api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_director/) *) |
*director* |
|
|
optional |

Called when projection is resized (due to layoutSubviews on the view). This is important to respond to in order to setup your scene with the proper dimensions (which only exist after the first call to layoutSubviews) so that you can set your scene as early as possible to avoid startup flicker

| - (BOOL) shouldAutorotateToInterfaceOrientation: |
|
(UIInterfaceOrientation) |
*interfaceOrientation* |
|
|
optional |

Returns a Boolean value indicating whether the [CCDirector](../../../../../../api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_director/) supports the specified orientation. Default value is YES (supports all possible orientations)

| - (void) updateProjection |
|
|
|
|
optional |

Called by [CCDirector](../../../../../../api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_director/) when the projection is updated, and "custom" projection is used


The documentation for this protocol was generated from the following file: