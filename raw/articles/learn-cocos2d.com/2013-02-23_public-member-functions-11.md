---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.1/ObjectAL/html/interface_o_a_l_simple_audio/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
ObjectAL
2.1
ObjectAL API Reference (iOS) for www.kobold2d.com developers
|

A simpler interface to the [ObjectAL](http://www.learn-cocos2d.com/) sound library.
[More...](http://www.learn-cocos2d.com/api-ref/2.1/ObjectAL/html/interface_o_a_l_simple_audio/#details)

`#import <OALSimpleAudio.h>`


| (id) | -
|

A simpler interface to the [ObjectAL](http://www.learn-cocos2d.com/) sound library.

This singleton can be used alone for simpler audio needs, or in conjunction with user-created audio objects for more advanced needs (as is done in many of the demos).

For sound effects, it initializes OpenAL with the default [ALDevice](http://www.learn-cocos2d.com/), an [ALContext](http://www.learn-cocos2d.com/), and an [ALChannelSource](http://www.learn-cocos2d.com/) consisting of all 32 interruptible [ALSource](http://www.learn-cocos2d.com/) objects (the maximum currently allowed for iOS). If you want to create your own sources as well, change the reservedSources property.

For background audio, it creates a single [OALAudioTrack](http://www.learn-cocos2d.com/), which will not reserve resources unless used. (you can create more [OALAudioTrack](http://www.learn-cocos2d.com/) objects for your own use if you want).

This singleton also provides access to the more common configuration options available in OALAudioSupport.

All audio playback commands are delegated either to the [ALChannelSource](http://www.learn-cocos2d.com/) (for sound effects), or to the [OALAudioTrack](http://www.learn-cocos2d.com/) (for BG music).

| - (id) initWithReservedSources: | (int) | reservedSources |
|
| monoSources: | (int) | monoSources |
|
| stereoSources: | (int) | stereoSources |
|

(INTERNAL USE) Initialize with the specified parameters.

| reservedSources | The number of sources to reserve for
|

(INTERNAL USE) Initialize with the specified number of reserved sources.

| reservedSources | the number of sources to reserve when initializing. |

Play whatever background music is preloaded.

Play the background music at the specified path.

If the music has not been preloaded, this method will load the music and then play, incurring a slight delay.


**Note:** only **ONE** background music file may be played or preloaded at a time via [OALSimpleAudio](http://www.learn-cocos2d.com/api-ref/2.1/ObjectAL/html/interface_o_a_l_simple_audio/). If you play or preload another file, the one currently playing will stop.

| path | The path containing the background music. |

Play the background music at the specified path.

If the music has not been preloaded, this method will load the music and then play, incurring a slight delay.


**Note:** only **ONE** background music file may be played or preloaded at a time via [OALSimpleAudio](http://www.learn-cocos2d.com/api-ref/2.1/ObjectAL/html/interface_o_a_l_simple_audio/). If you play or preload another file, the one currently playing will stop.

| path | The path containing the background music. |
| loop | If true, loop the bg track. |

Play the background music at the specified path.

If the music has not been preloaded, this method will load the music and then play, incurring a slight delay.


**Note:** only **ONE** background music file may be played or preloaded at a time via [OALSimpleAudio](http://www.learn-cocos2d.com/api-ref/2.1/ObjectAL/html/interface_o_a_l_simple_audio/). If you play or preload another file, the one currently playing will stop. To play multiple audio tracks, create an [OALAudioTrack](http://www.learn-cocos2d.com/).


**Note:** pan will have no effect when running on iOS versions prior to 4.0.

| filePath | The path containing the sound data. |
| volume | The volume (gain) to play at (0.0 - 1.0). |
| pan | Left-right panning (-1.0 = far left, 1.0 = far right) (Only on iOS 4.0+). |
| loop | If TRUE, the sound will loop until you call "stopBg". |

Play whatever background music is preloaded.

| loop | If true, loop the bg track. |

| - (id<
|

Play a sound effect from a user-supplied buffer.

| buffer | The buffer containing the sound data. |
| volume | The volume (gain) to play at (0.0 - 1.0). |
| pitch | The pitch to play at (1.0 = normal pitch). |
| pan | Left-right panning (-1.0 = far left, 1.0 = far right). |
| loop | If TRUE, the sound will loop until you call "stop" on the returned sound source. |

Play a sound effect with volume 1.0, pitch 1.0, pan 0.0, loop NO.

The sound will be loaded and cached if it wasn't already.

| filePath | The path containing the sound data. |

Play a sound effect with volume 1.0, pitch 1.0, pan 0.0.

The sound will be loaded and cached if it wasn't already.

| filePath | The path containing the sound data. |
| loop | If TRUE, the sound will loop until you call "stop" on the returned sound source. |

| - (id<
|

Play a sound effect.

The sound will be loaded and cached if it wasn't already.

| filePath | The path containing the sound data. |
| volume | The volume (gain) to play at (0.0 - 1.0). |
| pitch | The pitch to play at (1.0 = normal pitch). |
| pan | Left-right panning (-1.0 = far left, 1.0 = far right). |
| loop | If TRUE, the sound will loop until you call "stop" on the returned sound source. |

Preload background music.

**Note:** only **ONE** background music file may be played or preloaded at a time via [OALSimpleAudio](http://www.learn-cocos2d.com/api-ref/2.1/ObjectAL/html/interface_o_a_l_simple_audio/). If you play or preload another file, the one currently playing will stop.

| path | The path containing the background music. |

Preload background music.

**Note:** only **ONE** background music file may be played or preloaded at a time via [OALSimpleAudio](http://www.learn-cocos2d.com/api-ref/2.1/ObjectAL/html/interface_o_a_l_simple_audio/). If you play or preload another file, the one currently playing will stop.

| path | The path containing the background music. |
| seekTime | the position in the file to start playing at. |

Preload and cache a sound effect for later playback.

| filePath | The path containing the sound data. |

Preload and cache a sound effect for later playback.

| filePath | The path containing the sound data. |
| reduceToMono | If true, reduce the sample to mono (stereo samples don't support panning or positional audio). |

| - (BOOL)
|

Asynchronous preload and cache sound effect for later playback.

| filePath | an NSString with the path containing the sound data. |
| reduceToMono | If true, reduce the sample to mono (stereo samples don't support panning or positional audio). |
| completionBlock | Executed when loading is complete. |

| - (void) preloadEffects: | (NSArray*) | filePaths |
|
| reduceToMono: | (bool) | reduceToMono |
|
| progressBlock: | (uint progress, uint successCount, uint total) | progressBlock |
|

Asynchronous preload and cache multiple sound effects for later playback.

| filePaths | An NSArray of NSStrings with the paths containing the sound data. |
| reduceToMono | If true, reduce the samples to mono (stereo samples don't support panning or positional audio). |
| progressBlock | Executed regularly while file loading is in progress. |

| + (
|

Start [OALSimpleAudio](http://www.learn-cocos2d.com/api-ref/2.1/ObjectAL/html/interface_o_a_l_simple_audio/) with the specified parameters.

With this initializer, you can set the total number of mono and stereo sources available, as well as how many sources are to be reserved by [OALSimpleAudio](http://www.learn-cocos2d.com/api-ref/2.1/ObjectAL/html/interface_o_a_l_simple_audio/).


The number of mono and stereo sources represents the GLOBAL number of sources available for EVERYONE, not just [OALSimpleAudio](http://www.learn-cocos2d.com/api-ref/2.1/ObjectAL/html/interface_o_a_l_simple_audio/). Their combined values must not exceed 32 (the max allowed sources in iOS).


reservedSources is independent of this; it represents how many of the above mentioned sources to reserve for [OALSimpleAudio](http://www.learn-cocos2d.com/api-ref/2.1/ObjectAL/html/interface_o_a_l_simple_audio/)'s use.


**Note:** This method must be called ONLY ONCE, *BEFORE* any attempt is made to access the shared instance.


| reservedSources | The number of sources to reserve for
|

Start [OALSimpleAudio](http://www.learn-cocos2d.com/api-ref/2.1/ObjectAL/html/interface_o_a_l_simple_audio/) with the specified number of reserved sources.

Call this initializer if you want to use [OALSimpleAudio](http://www.learn-cocos2d.com/api-ref/2.1/ObjectAL/html/interface_o_a_l_simple_audio/), but keep some of the device's audio sources (there are 32 in total) for your own use.

**Note:** This method must be called ONLY ONCE, *BEFORE* any attempt is made to access the shared instance. To change the reserved sources after instantiation, modify reservedSources.

| sources | the number of sources
|

Singleton implementation providing "sharedInstance" and "purgeSharedInstance" methods.

**- (OALSimpleAudio*) sharedInstance**: Get the shared singleton instance.

**- (void) purgeSharedInstance**: Purge (deallocate) the shared instance.


Unload all preloaded effects.

It is useful to put a call to this method in "applicationDidReceiveMemoryWarning" in your app delegate.

Unload a preloaded effect.

| filePath | The path containing the sound data that was previously loaded. |

Queue for preloading and async operations that use blocks.

This ensures all operations are safe because they are guaranteed to run in order.

If YES, allow ipod music to continue playing (NOT SUPPORTED ON THE SIMULATOR).

Note: If this is enabled, and another app is playing music, background audio playback will use the SOFTWARE codecs, NOT hardware.


If allowIpod = NO, the application will ALWAYS use hardware decoding.


Default value: YES

Audio track to play background music.

Background audio track.

If true, mute when backgrounded, screen locked, or the ringer switch is turned off (NOT SUPPORTED ON THE SIMULATOR).



Default value: YES

Enables/disables the preload cache.

If the preload cache is disabled, effects preloading will do nothing (BG preloading will still work).

Determines what to do if no other application is playing audio and allowIpod = YES (NOT SUPPORTED ON THE SIMULATOR).



If NO, the application will ALWAYS use software decoding. The advantage to this is that the user can background your application and then start audio playing from another application. If useHardwareIfAvailable = YES, the user won't be able to do this.


If this is set to YES, the application will use hardware decoding if no other application is currently playing audio. However, no other application will be able to start playing audio if it wasn't playing already.


Note: This switch has no effect if allowIpod = NO.


Default value: YES