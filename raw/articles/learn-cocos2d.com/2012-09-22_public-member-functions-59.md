---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.0/CocosDenshion/html/interface_c_d_sound_source/
published: '2012-09-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
CocosDenshion iOS
2.0
CocosDenshion API Reference (iOS version) for www.kobold2d.com developers
|

`#import <CocosDenshion.h>`


| (id) | -
|

[CDSoundSource](http://www.learn-cocos2d.com/api-ref/2.0/CocosDenshion/html/interface_c_d_sound_source/) is a wrapper around an OpenAL sound source. It allows you to manipulate properties such as pitch, gain, pan and looping while the sound is playing. [CDSoundSource](http://www.learn-cocos2d.com/api-ref/2.0/CocosDenshion/html/interface_c_d_sound_source/) is based on the old CDSourceWrapper class but with much added functionality.

Returns the duration of the attached buffer in seconds or a negative value if the buffer is invalid

Stores the last error code that occurred. Check against AL_NO_ERROR