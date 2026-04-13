---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/CocosDenshion/html/interface_simple_audio_engine/
published: '2011-12-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <SimpleAudioEngine.h>`


| void |
|

A wrapper to the [CDAudioManager](http://www.learn-cocos2d.com/api-ref/1.0/CocosDenshion/html/interface_c_d_audio_manager/) object. This is recommended for basic audio requirements. If you just want to play some sound fx and some background music and have no interest in learning the lower level workings then this is the interface to use.

Requirements:

| void SimpleAudioEngine::end | ( | ) | ` [static, virtual]` |

Shuts down the shared audio engine instance so that it can be reinitialised

| BOOL SimpleAudioEngine::isBackgroundMusicPlaying | ( | ) | ` [virtual]` |

returns whether or not the background music is playing

| void SimpleAudioEngine::pauseBackgroundMusic | ( | ) | ` [virtual]` |

pauses the background music

| void SimpleAudioEngine::playBackgroundMusic: | ( | NSString * | filePath | ) | ` [virtual]` |

plays background music in a loop

| void SimpleAudioEngine::playBackgroundMusic:loop: | ( | NSString * | filePath, |
| [loop] BOOL | loop |
||
| ) | ` [virtual]` |

plays background music, if loop is true the music will repeat otherwise it will be played once

| ALuint SimpleAudioEngine::playEffect: | ( | NSString * | filePath | ) | ` [virtual]` |

plays an audio effect with a file path

| ALuint SimpleAudioEngine::playEffect:pitch:pan:gain: | ( | NSString * | filePath, |
| [pitch] Float32 | pitch, |
||
| [pan] Float32 | pan, |
||
| [gain] Float32 | gain |
||
| ) | ` [virtual]` |

plays an audio effect with a file path, pitch, pan and gain

| void SimpleAudioEngine::preloadBackgroundMusic: | ( | NSString * | filePath | ) | ` [virtual]` |

Preloads a music file so it will be ready to play as background music

| void SimpleAudioEngine::preloadEffect: | ( | NSString * | filePath | ) | ` [virtual]` |

preloads an audio effect

| void SimpleAudioEngine::resumeBackgroundMusic | ( | ) | ` [virtual]` |

resume background music that has been paused

| void SimpleAudioEngine::rewindBackgroundMusic | ( | ) | ` [virtual]` |

rewind the background music

| void SimpleAudioEngine::stopBackgroundMusic | ( | ) | ` [virtual]` |

stops playing background music

| void SimpleAudioEngine::stopEffect: | ( | ALuint | soundId | ) | ` [virtual]` |

stop a sound that is playing, note you must pass in the soundId that is returned when you started playing the sound with playEffect

| void SimpleAudioEngine::unloadEffect: | ( | NSString * | filePath | ) | ` [virtual]` |

unloads an audio effect from memory

float SimpleAudioEngine::backgroundMusicVolume` [read, write, assign]` |

Background music volume. Range is 0.0f to 1.0f. This will only have an effect if willPlayBackgroundMusic returns YES

float SimpleAudioEngine::effectsVolume` [read, write, assign]` |

Effects volume. Range is 0.0f to 1.0f

BOOL SimpleAudioEngine::willPlayBackgroundMusic` [read, assign]` |

If NO it indicates background music will not be played either because no background music is loaded or the audio session does not permit it.