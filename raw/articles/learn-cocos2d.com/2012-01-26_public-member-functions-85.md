---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/protocol_a_l_sound_source-p/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Manages all properties relating to an OpenAL sound source.
[More...](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/protocol_a_l_sound_source-p/#details)

`#include <ALSoundSource.h>`


| id<
|

Manages all properties relating to an OpenAL sound source.

There are currently two classes that adhere to this protocol: [ALSource](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_a_l_source/) and ChannelSource (which collectively manipulates a set of [ALSource](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_a_l_source/) objects). A full description of the properties themselves is available in the OpenAL 1.1 Specification and Reference: [http://connect.creativelabs.com/openal/Documentation](http://connect.creativelabs.com/openal/Documentation)

| void
|

` [virtual]`

Fade to the specified gain value.

| gain | The gain to fade to. |
| duration | The duration of the fade operation in seconds. |
| target | The target to notify when the fade completes (can be nil). |
| selector | The selector to call when the fade completes. The selector must accept a single parameter, which will be the object that performed the fade. |

| void
|

` [virtual]`

pan to the specified value.

| pan | The value to pan to. |
| duration | The duration of the pan operation in seconds. |
| target | The target to notify when the pan completes (can be nil). |
| selector | The selector to call when the pan completes. The selector must accept a single parameter, which will be the object that performed the pan. |

| void
|

` [virtual]`

Gradually change pitch to the specified value.

| pitch | The value to change pitch to. |
| duration | The duration of the pitch operation in seconds. |
| target | The target to notify when the pitch change completes (can be nil). |
| selector | The selector to call when the pitch change completes. The selector must accept a single parameter, which will be the object that performed the pitch change. |

Play a sound.

| buffer | the buffer to play. |

| id<
|

` [virtual]`

Play a sound, setting gain, pitch, pan, and looping.

| buffer | the buffer to play. |
| gain | The gain (volume) to play at (0.0 - 1.0). |
| pitch | The pitch to play at (1.0 = normal pitch). |
| pan | Left-right panning (-1.0 = far left, 1.0 = far right). |
| loop | If TRUE, the sound will loop until you call "stop" on the returned sound source. |

Play a sound, optionally looping.

| buffer | the buffer to play. |
| loop | If TRUE, the sound will loop until you call "stop" on the returned sound source. |

Stop playing the current sound and set its state to AL_INITIAL.

Stop any currently running fade, pan, or pitch operations.

Pan value (-1.0 = far left, 1.0 = far right).

Note: This effect is simulated by changing the source's X position. Do not use this property if you are modifying the position property as well.