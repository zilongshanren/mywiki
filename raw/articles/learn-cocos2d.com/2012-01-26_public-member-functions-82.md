---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_simple_audio/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

A simpler interface to the [ObjectAL](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_object_a_l/) sound library.
[More...](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_simple_audio/#details)

`#include <OALSimpleAudio.h>`


| id |
|

A simpler interface to the [ObjectAL](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_object_a_l/) sound library.

This singleton can be used alone for simpler audio needs, or in conjunction with user-created audio objects for more advanced needs (as is done in many of the demos).

For sound effects, it initializes OpenAL with the default [ALDevice](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_a_l_device/), an [ALContext](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_a_l_context/), and an [ALChannelSource](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_a_l_channel_source/) consisting of all 32 interruptible [ALSource](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_a_l_source/) objects (the maximum currently allowed for iOS). If you want to create your own sources as well, change the reservedSources property.

For background audio, it creates a single [OALAudioTrack](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_audio_track/), which will not reserve resources unless used. (you can create more [OALAudioTrack](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_audio_track/) objects for your own use if you want).

This singleton also provides access to the more common configuration options available in OALAudioSupport.

All audio playback commands are delegated either to the [ALChannelSource](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_a_l_channel_source/) (for sound effects), or to the [OALAudioTrack](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_audio_track/) (for BG music).

| id OALSimpleAudio::initWithReservedSources:monoSources:stereoSources: | ( | int | reservedSources, |
| [monoSources] int | monoSources, |
||
| [stereoSources] int | stereoSources |
||
| ) | ` [virtual]` |

(INTERNAL USE) Initialize with the specified parameters.

| reservedSources | The number of sources to reserve for OALSimpleAudio's use when initializing. |
| monoSources | The GLOBAL number of sources supporting mono (default 28). |
| stereoSources | The GLOBAL number of sources supporting stereo (default 4). |

| id OALSimpleAudio::initWithSources: | ( | int | reservedSources | ) | ` [virtual]` |

(INTERNAL USE) Initialize with the specified number of reserved sources.

| reservedSources | the number of sources to reserve when initializing. |

| bool OALSimpleAudio::playBg | ( | ) | ` [virtual]` |

Play whatever background music is preloaded.

| bool OALSimpleAudio::playBg: | ( | NSString* | path | ) | ` [virtual]` |

Play the background music at the specified path.

If the music has not been preloaded, this method will load the music and then play, incurring a slight delay.


**Note:** only **ONE** background music file may be played or preloaded at a time via [OALSimpleAudio](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_simple_audio/). If you play or preload another file, the one currently playing will stop.

| path | The path containing the background music. |

| bool OALSimpleAudio::playBg:loop: | ( | NSString* | path, |
| [loop] bool | loop |
||
| ) | ` [virtual]` |

Play the background music at the specified path.

If the music has not been preloaded, this method will load the music and then play, incurring a slight delay.


**Note:** only **ONE** background music file may be played or preloaded at a time via [OALSimpleAudio](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_simple_audio/). If you play or preload another file, the one currently playing will stop.

| path | The path containing the background music. |
| loop | If true, loop the bg track. |

| bool OALSimpleAudio::playBg:volume:pan:loop: | ( | NSString* | filePath, |
| [volume] float | volume, |
||
| [pan] float | pan, |
||
| [loop] bool | loop |
||
| ) | ` [virtual]` |

Play the background music at the specified path.

If the music has not been preloaded, this method will load the music and then play, incurring a slight delay.


**Note:** only **ONE** background music file may be played or preloaded at a time via [OALSimpleAudio](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_simple_audio/). If you play or preload another file, the one currently playing will stop. To play multiple audio tracks, create an [OALAudioTrack](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_audio_track/).


**Note:** pan will have no effect when running on iOS versions prior to 4.0.

| filePath | The path containing the sound data. |
| volume | The volume (gain) to play at (0.0 - 1.0). |
| pan | Left-right panning (-1.0 = far left, 1.0 = far right) (Only on iOS 4.0+). |
| loop | If TRUE, the sound will loop until you call "stopBg". |

| bool OALSimpleAudio::playBgWithLoop: | ( | bool | loop | ) | ` [virtual]` |

Play whatever background music is preloaded.

| loop | If true, loop the bg track. |

| id<
|

` [virtual]`

Play a sound effect from a user-supplied buffer.

| buffer | The buffer containing the sound data. |
| volume | The volume (gain) to play at (0.0 - 1.0). |
| pitch | The pitch to play at (1.0 = normal pitch). |
| pan | Left-right panning (-1.0 = far left, 1.0 = far right). |
| loop | If TRUE, the sound will loop until you call "stop" on the returned sound source. |

Play a sound effect with volume 1.0, pitch 1.0, pan 0.0, loop NO.

The sound will be loaded and cached if it wasn't already.

| filePath | The path containing the sound data. |

| id<
|

` [virtual]`

Play a sound effect with volume 1.0, pitch 1.0, pan 0.0.

The sound will be loaded and cached if it wasn't already.

| filePath | The path containing the sound data. |
| loop | If TRUE, the sound will loop until you call "stop" on the returned sound source. |

| id<
|

` [virtual]`

Play a sound effect.

The sound will be loaded and cached if it wasn't already.

| filePath | The path containing the sound data. |
| volume | The volume (gain) to play at (0.0 - 1.0). |
| pitch | The pitch to play at (1.0 = normal pitch). |
| pan | Left-right panning (-1.0 = far left, 1.0 = far right). |
| loop | If TRUE, the sound will loop until you call "stop" on the returned sound source. |

| bool OALSimpleAudio::preloadBg: | ( | NSString* | path | ) | ` [virtual]` |

Preload background music.

**Note:** only **ONE** background music file may be played or preloaded at a time via [OALSimpleAudio](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_simple_audio/). If you play or preload another file, the one currently playing will stop.

| path | The path containing the background music. |

| bool OALSimpleAudio::preloadBg:seekTime: | ( | NSString* | path, |
| [seekTime] NSTimeInterval | seekTime |
||
| ) | ` [virtual]` |

Preload background music.

**Note:** only **ONE** background music file may be played or preloaded at a time via [OALSimpleAudio](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_simple_audio/). If you play or preload another file, the one currently playing will stop.

| path | The path containing the background music. |
| seekTime | the position in the file to start playing at. |

Preload and cache a sound effect for later playback.

| filePath | The path containing the sound data. |

|

` [virtual]`

Preload and cache a sound effect for later playback.

| filePath | The path containing the sound data. |
| reduceToMono | If true, reduce the sample to mono (stereo samples don't support panning or positional audio). |

| BOOL OALSimpleAudio::preloadEffect:reduceToMono:completionBlock: | ( | NSString* | filePath, |
| [reduceToMono] bool | reduceToMono, |
||
| [completionBlock]
|

` [virtual]`

Asynchronous preload and cache sound effect for later playback.

| filePath | an NSString with the path containing the sound data. |
| reduceToMono | If true, reduce the sample to mono (stereo samples don't support panning or positional audio). |
| completionBlock | Executed when loading is complete. |

| void OALSimpleAudio::preloadEffects:reduceToMono:progressBlock: | ( | NSArray* | filePaths, |
| [reduceToMono] bool | reduceToMono, |
||
| [progressBlock] uint progress, uint successCount, uint total | progressBlock |
||
| ) | ` [virtual]` |

Asynchronous preload and cache multiple sound effects for later playback.

| filePaths | An NSArray of NSStrings with the paths containing the sound data. |
| reduceToMono | If true, reduce the samples to mono (stereo samples don't support panning or positional audio). |
| progressBlock | Executed regularly while file loading is in progress. |

| void OALSimpleAudio::resetToDefault | ( | ) | ` [virtual]` |

Reset everything in this object to its default state.

|

` [static, virtual]`

Start [OALSimpleAudio](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_simple_audio/) with the specified parameters.

With this initializer, you can set the total number of mono and stereo sources available, as well as how many sources are to be reserved by [OALSimpleAudio](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_simple_audio/).


The number of mono and stereo sources represents the GLOBAL number of sources available for EVERYONE, not just [OALSimpleAudio](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_simple_audio/). Their combined values must not exceed 32 (the max allowed sources in iOS).


reservedSources is independent of this; it represents how many of the above mentioned sources to reserve for OALSimpleAudio's use.


**Note:** This method must be called ONLY ONCE, *BEFORE* any attempt is made to access the shared instance.


| reservedSources | The number of sources to reserve for OALSimpleAudio's use when initializing. iOS currently supports up to 32 sources total. |
| monoSources | The GLOBAL number of sources supporting mono (default 28). |
| stereoSources | The GLOBAL number of sources supporting stereo (default 4). |

Start [OALSimpleAudio](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_simple_audio/) with the specified number of reserved sources.

Call this initializer if you want to use [OALSimpleAudio](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_simple_audio/), but keep some of the device's audio sources (there are 32 in total) for your own use.

**Note:** This method must be called ONLY ONCE, *BEFORE* any attempt is made to access the shared instance. To change the reserved sources after instantiation, modify reservedSources.

| sources | the number of sources
|

| void OALSimpleAudio::stopAllEffects | ( | ) | ` [virtual]` |

Stop ALL sound effect playback.

| void OALSimpleAudio::stopBg | ( | ) | ` [virtual]` |

Stop the background music playback and rewind.

| void OALSimpleAudio::stopEverything | ( | ) | ` [virtual]` |

Stop all effects and bg music.

Singleton implementation providing "sharedInstance" and "purgeSharedInstance" methods.

**- (OALSimpleAudio*) sharedInstance**: Get the shared singleton instance.

**- (void) purgeSharedInstance**: Purge (deallocate) the shared instance.


| void OALSimpleAudio::unloadAllEffects | ( | ) | ` [virtual]` |

Unload all preloaded effects.

It is useful to put a call to this method in "applicationDidReceiveMemoryWarning" in your app delegate.

| void OALSimpleAudio::unloadEffect: | ( | NSString* | filePath | ) | ` [virtual]` |

Unload a preloaded effect.

| filePath | The path containing the sound data that was previously loaded. |

Queue for preloading and async operations that use blocks.

This ensures all operations are safe because they are guaranteed to run in order.

keeping track of how many effects remain to be loaded

bool OALSimpleAudio::allowIpod` [read, write, assign]` |

If YES, allow ipod music to continue playing (NOT SUPPORTED ON THE SIMULATOR).

Note: If this is enabled, and another app is playing music, background audio playback will use the SOFTWARE codecs, NOT hardware.


If allowIpod = NO, the application will ALWAYS use hardware decoding.


Default value: YES

Audio track to play background music.

Background audio track.

NSURL * OALSimpleAudio::backgroundTrackURL` [read, assign]` |

Background audio URL.

bool OALSimpleAudio::bgMuted` [read, write, assign]` |

Mutes BG music playback.

bool OALSimpleAudio::bgPaused` [read, write, assign]` |

Pauses BG music playback.

bool OALSimpleAudio::bgPlaying` [read, assign]` |

If true, BG music is currently playing.

float OALSimpleAudio::bgVolume` [read, write, assign]` |

Background music playback gain/volume (0.0 - 1.0)

bool OALSimpleAudio::effectsMuted` [read, write, assign]` |

Mutes effects playback.

bool OALSimpleAudio::effectsPaused` [read, write, assign]` |

Pauses effects playback.

float OALSimpleAudio::effectsVolume` [read, write, assign]` |

Master effects gain/volume (0.0 - 1.0)

bool OALSimpleAudio::honorSilentSwitch` [read, write, assign]` |

If true, mute when backgrounded, screen locked, or the ringer switch is turned off (NOT SUPPORTED ON THE SIMULATOR).



Default value: YES

bool OALSimpleAudio::interrupted` [read, assign]` |

If YES, the sound system is interrupted.

bool OALSimpleAudio::manuallySuspended` [read, write, assign]` |

Set to YES to manually suspend the sound system.

bool OALSimpleAudio::muted` [read, write, assign]` |

Mutes all audio.

bool OALSimpleAudio::paused` [read, write, assign]` |

Pauses everything.

NSUInteger OALSimpleAudio::preloadCacheCount` [read, assign]` |

The number of items currently in the preload cache.

bool OALSimpleAudio::preloadCacheEnabled` [read, write, assign]` |

Enables/disables the preload cache.

If the preload cache is disabled, effects preloading will do nothing (BG preloading will still work).

int OALSimpleAudio::reservedSources` [read, write, assign]` |

bool OALSimpleAudio::suspended` [read, assign]` |

If YES, the sound system is suspended.

bool OALSimpleAudio::useHardwareIfAvailable` [read, write, assign]` |

Determines what to do if no other application is playing audio and allowIpod = YES (NOT SUPPORTED ON THE SIMULATOR).



If NO, the application will ALWAYS use software decoding. The advantage to this is that the user can background your application and then start audio playing from another application. If useHardwareIfAvailable = YES, the user won't be able to do this.


If this is set to YES, the application will use hardware decoding if no other application is currently playing audio. However, no other application will be able to start playing audio if it wasn't playing already.


Note: This switch has no effect if allowIpod = NO.


Default value: YES