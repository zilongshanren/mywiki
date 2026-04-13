---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.0/CocosDenshion/html/interface_c_d_sound_engine/
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

| (id) | -
|

Used internally, never call unless you know what you are doing

Returns the duration of the buffer in seconds or a negative value if the buffer id is invalid

Returns the sampling frequency of the buffer in hertz or a negative value if the buffer id is invalid

Returns the size of the buffer in bytes or a negative value if the buffer id is invalid

| - (ALuint) playSound: | (int) | soundId |
|
| sourceGroupId: | (int) | sourceGroupId |
|
| pitch: | (float) | pitch |
|
| pan: | (float) | pan |
|
| gain: | (float) | gain |
|
| loop: | (BOOL) | loop |
|

Plays a sound in a channel group with a pitch, pan and gain. The sound could played looped or not

Sets the sample rate for the audio mixer. For best performance this should match the sample rate of your audio content

Creates and returns a sound source object for the specified sound within the specified source group.