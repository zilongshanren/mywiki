---
title: CDSoundSource Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_d_sound_source/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`

[CocosDenshion.h](http://www.learn-cocos2d.com/)"

Inherits CDAudioTransportProtocol-p, and CDAudioInterruptProtocol-p.

| (id) | -
|

[CDSoundSource](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_d_sound_source/) is a wrapper around an OpenAL sound source. It allows you to manipulate properties such as pitch, gain, pan and looping while the sound is playing. [CDSoundSource](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_d_sound_source/) is based on the old CDSourceWrapper class but with much added functionality.

| - (id) init: | (ALuint) | theSourceId |
||
| sourceIndex: | (int) | index |
||
| soundEngine: | (CDSoundEngine *) | engine | ||

Do not init yourself, get an instance from the sourceForSound factory method on CDSoundEngine

- (float) durationInSeconds` [read, assign]` |

Returns the duration of the attached buffer in seconds or a negative value if the buffer is invalid

- (ALenum) lastError` [read, assign]` |

Stores the last error code that occurred. Check against AL_NO_ERROR