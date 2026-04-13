---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/CocosDenshion/html/interface_c_d_audio_manager/
published: '2011-12-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CDAudioManager.h>`


| id |
|

[CDAudioManager](http://www.learn-cocos2d.com/api-ref/1.0/CocosDenshion/html/interface_c_d_audio_manager/) manages audio requirements for a game. It provides access to a [CDSoundEngine](http://www.learn-cocos2d.com/api-ref/1.0/CocosDenshion/html/interface_c_d_sound_engine/) object for playing sound effects. It provides access to two [CDLongAudioSource](http://www.learn-cocos2d.com/) object (left and right channel) for playing long duration audio such as background music and narration tracks. Additionally it manages the audio session to take care of things like audio session interruption and interacting with the audio of other apps that are running on the device.

Requirements:

| void CDAudioManager::applicationDidBecomeActive | ( | ) | ` [virtual]` |

Call if you want to use built in resign behavior but need to do some additional audio processing on become active.

| void CDAudioManager::applicationWillResignActive | ( | ) | ` [virtual]` |

Call if you want to use built in resign behavior but need to do some additional audio processing on resign active.

Retrieves the audio source for the specified channel

|

` [virtual]`

Loads the data from the specified file path to the channel's audio source

| void CDAudioManager::configure: | ( | tAudioManagerMode | mode | ) | ` [static, virtual]` |

Configures the shared singleton with a mode

| void CDAudioManager::end | ( | ) | ` [static, virtual]` |

Shuts down the shared audio manager instance so that it can be reinitialised

| id CDAudioManager::init: | ( | tAudioManagerMode | mode | ) | ` [virtual]` |

Initializes the engine synchronously with a mode, channel definition and a total number of channels

| void CDAudioManager::initAsynchronously: | ( | tAudioManagerMode | mode | ) | ` [static, virtual]` |

Initializes the engine asynchronously with a mode

| BOOL CDAudioManager::isBackgroundMusicPlaying | ( | ) | ` [virtual]` |

Returns whether or not the background music is playing

| BOOL CDAudioManager::isDeviceMuted | ( | ) | ` [virtual]` |

Returns true is audio is muted at a hardware level e.g user has ringer switch set to off

| BOOL CDAudioManager::isOtherAudioPlaying | ( | ) | ` [virtual]` |

Returns true if another app is playing audio such as the iPod music player

| void CDAudioManager::pauseBackgroundMusic | ( | ) | ` [virtual]` |

Pauses the background music

| void CDAudioManager::playBackgroundMusic:loop: | ( | NSString * | filePath, |
| [loop] BOOL | loop |
||
| ) | ` [virtual]` |

Plays music in background. The music can be looped or not It is recommended to use .aac files as background music since they are decoded by the device (hardware).

| void CDAudioManager::preloadBackgroundMusic: | ( | NSString * | filePath | ) | ` [virtual]` |

Preloads a background music

| void CDAudioManager::resumeBackgroundMusic | ( | ) | ` [virtual]` |

Resumes playing the background music

| void CDAudioManager::rewindBackgroundMusic | ( | ) | ` [virtual]` |

Rewinds the background music

| void CDAudioManager::setMode: | ( | tAudioManagerMode | mode | ) | ` [virtual]` |

Sets the way the audio manager interacts with the operating system such as whether it shares output with other apps or obeys the mute switch

| void CDAudioManager::stopBackgroundMusic | ( | ) | ` [virtual]` |

Stops playing the background music