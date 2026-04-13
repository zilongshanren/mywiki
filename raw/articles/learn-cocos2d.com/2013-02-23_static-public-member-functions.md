---
title: Static Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/interface_c_c_video_player/
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

| (void) | +
|

Video Player for Cocos2D apps.

Sets new delegate (weak ref) for playback start/stop callbacs.

ATTENTION: You need to call this method before invoking playMovieWithFile: or you will not receive movieStartsPlaying callback.

If YES - user can't skip video by mouse/key/touch event. Default is NO.

Updates video player view transform for newOrientation.

Supports only landscape left or landscape right, for other orientations does nothing.