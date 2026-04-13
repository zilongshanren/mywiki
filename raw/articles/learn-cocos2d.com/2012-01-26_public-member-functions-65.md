---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/CocosDenshion/html/interface_c_d_sound_engine/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[List of all members.](/)

Public Member Functions
|
| id | [init](../../../../../api-ref/1.0/CocosDenshion/html/interface_c_d_sound_engine/#a013cb9b6cf86c0dbfca8fac6aae0bd6a) () |
| ALuint | [playSound:sourceGroupId:pitch:pan:gain:loop:](../../../../../api-ref/1.0/CocosDenshion/html/interface_c_d_sound_engine/#aba5e66f1767cf41ef07524e17a1e295e) (int soundId,[sourceGroupId] int sourceGroupId,[pitch] float pitch,[pan] float pan,[gain] float gain,[loop] BOOL loop) |
[CDSoundSource](../../../../../api-ref/1.0/CocosDenshion/html/interface_c_d_sound_source/) * | [soundSourceForSound:sourceGroupId:](../../../../../api-ref/1.0/CocosDenshion/html/interface_c_d_sound_engine/#afdd95c8c9b8ffe667db2215312830e8e) (int soundId,[sourceGroupId] int sourceGroupId) |
| void | [stopSound:](../../../../../api-ref/1.0/CocosDenshion/html/interface_c_d_sound_engine/#ae2bbd23eefecd32afcf6bc0109b5e7a2) (ALuint sourceId) |
| void | [stopSourceGroup:](../../../../../api-ref/1.0/CocosDenshion/html/interface_c_d_sound_engine/#a5d6fbd530895fac2ce486a478e46fb23) (int sourceGroupId) |
| void | [stopAllSounds](../../../../../api-ref/1.0/CocosDenshion/html/interface_c_d_sound_engine/#a8bbc63632a5e72c9235c39730e8efb38) () |
void | **defineSourceGroups:** (NSArray *sourceGroupDefinitions) |
void | **defineSourceGroups:total:** (int[] sourceGroupDefinitions,[total] NSUInteger total) |
void | **setSourceGroupNonInterruptible:isNonInterruptible:** (int sourceGroupId,[isNonInterruptible] BOOL isNonInterruptible) |
void | **setSourceGroupEnabled:enabled:** (int sourceGroupId,[enabled] BOOL enabled) |
BOOL | **sourceGroupEnabled:** (int sourceGroupId) |
BOOL | **loadBufferFromData:soundData:format:size:freq:** (int soundId,[soundData] ALvoid *soundData,[format] ALenum format,[size] ALsizei size,[freq] ALsizei freq) |
BOOL | **loadBuffer:filePath:** (int soundId,[filePath] NSString *filePath) |
void | **loadBuffersAsynchronously:** (NSArray *loadRequests) |
BOOL | **unloadBuffer:** (int soundId) |
ALCcontext * | **openALContext** () |
| float | [bufferDurationInSeconds:](../../../../../api-ref/1.0/CocosDenshion/html/interface_c_d_sound_engine/#a5731f4ec2052eb323ba1777f72c9da8c) (int soundId) |
| ALsizei | [bufferSizeInBytes:](../../../../../api-ref/1.0/CocosDenshion/html/interface_c_d_sound_engine/#a91672bece24f10760d62cce27986573e) (int soundId) |
| ALsizei | [bufferFrequencyInHertz:](../../../../../api-ref/1.0/CocosDenshion/html/interface_c_d_sound_engine/#af8559b48f34ad22ba9a7cf27ffcb8648) (int soundId) |
| void | [_soundSourcePreRelease:](../../../../../api-ref/1.0/CocosDenshion/html/interface_c_d_sound_engine/#ad05b4a121e37fe36d3df453989be82af) ([CDSoundSource](../../../../../api-ref/1.0/CocosDenshion/html/interface_c_d_sound_source/) *soundSource) |
Static Public Member Functions
|
| void | [setMixerSampleRate:](../../../../../api-ref/1.0/CocosDenshion/html/interface_c_d_sound_engine/#ab917455684b0ff4ea92e3d2a82d3530c) (Float32 sampleRate) |
Protected Attributes
|
[bufferInfo](/) * | **_buffers** |
[sourceInfo](/) * | **_sources** |
[sourceGroup](/) * | **_sourceGroups** |
ALCcontext * | **context** |
NSUInteger | **_sourceGroupTotal** |
UInt32 | **_audioSessionCategory** |
BOOL | **_handleAudioSession** |
ALfloat | **_preMuteGain** |
NSObject * | **_mutexBufferLoad** |
BOOL | **mute_** |
BOOL | **enabled_** |
ALenum | **lastErrorCode_** |
BOOL | **functioning_** |
float | **asynchLoadProgress_** |
BOOL | **getGainWorks_** |
int | **sourceTotal_** |
int | **bufferTotal** |
Properties
|
ALfloat | **masterGain** |
ALenum | **lastErrorCode** |
BOOL | **functioning** |
float | **asynchLoadProgress** |
BOOL | **getGainWorks** |
| int | [sourceTotal](../../../../../api-ref/1.0/CocosDenshion/html/interface_c_d_sound_engine/#a951c8a98f46192e4ed56ebe41f7abe59) |
| NSUInteger | [sourceGroupTotal](../../../../../api-ref/1.0/CocosDenshion/html/interface_c_d_sound_engine/#a2e416630cc0722eac6ba889dcb9461ba) |


## Member Function Documentation

| void CDSoundEngine::_soundSourcePreRelease: |
( |
[CDSoundSource](../../../../../api-ref/1.0/CocosDenshion/html/interface_c_d_sound_source/) * |
*soundSource* | ) |
` [virtual]` |

Used internally, never call unless you know what you are doing

| float CDSoundEngine::bufferDurationInSeconds: |
( |
int |
*soundId* | ) |
` [virtual]` |

Returns the duration of the buffer in seconds or a negative value if the buffer id is invalid

| ALsizei CDSoundEngine::bufferFrequencyInHertz: |
( |
int |
*soundId* | ) |
` [virtual]` |

Returns the sampling frequency of the buffer in hertz or a negative value if the buffer id is invalid

| ALsizei CDSoundEngine::bufferSizeInBytes: |
( |
int |
*soundId* | ) |
` [virtual]` |

Returns the size of the buffer in bytes or a negative value if the buffer id is invalid

| id CDSoundEngine::init |
( |
| ) |
` [virtual]` |

Initializes the engine with a group definition and a total number of groups

| ALuint CDSoundEngine::playSound:sourceGroupId:pitch:pan:gain:loop: |
( |
int |
*soundId*, |
|
|
[sourceGroupId] int |
*sourceGroupId*, |
|
|
[pitch] float |
*pitch*, |
|
|
[pan] float |
*pan*, |
|
|
[gain] float |
*gain*, |
|
|
[loop] BOOL |
*loop* |
|
) |
| ` [virtual]` |

Plays a sound in a channel group with a pitch, pan and gain. The sound could played looped or not

| void CDSoundEngine::setMixerSampleRate: |
( |
Float32 |
*sampleRate* | ) |
` [static, virtual]` |

Sets the sample rate for the audio mixer. For best performance this should match the sample rate of your audio content

[CDSoundSource](../../../../../api-ref/1.0/CocosDenshion/html/interface_c_d_sound_source/) * CDSoundEngine::soundSourceForSound:sourceGroupId: |
( |
int |
*soundId*, |
|
|
[sourceGroupId] int |
*sourceGroupId* |
|
) |
| ` [virtual]` |

Creates and returns a sound source object for the specified sound within the specified source group.

| void CDSoundEngine::stopAllSounds |
( |
| ) |
` [virtual]` |

| void CDSoundEngine::stopSound: |
( |
ALuint |
*sourceId* | ) |
` [virtual]` |

| void CDSoundEngine::stopSourceGroup: |
( |
int |
*sourceGroupId* | ) |
` [virtual]` |

Stops playing a source group


## Property Documentation

NSUInteger CDSoundEngine::sourceGroupTotal` [read, assign]` |

Total number of source groups that have been defined

int CDSoundEngine::sourceTotal` [read, assign]` |

Total number of sources available


The documentation for this interface was generated from the following file: