---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_audio_track/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Plays an audio track via AVAudioPlayer.
[More...](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_audio_track/#details)

`#include <OALAudioTrack.h>`


| bool |
|

Plays an audio track via AVAudioPlayer.

Unlike AVAudioPlayer, however, it can be re-used to play another file. Interruptions can be handled by OALAudioSupport (enabled by default).

| float OALAudioTrack::averagePowerForChannel: | ( | NSUInteger | channelNumber | ) | ` [virtual]` |

Gives the average power for a given channel, in decibels, for the sound being played.

0 dB indicates maximum power (full scale).

-160 dB indicates minimum power (near silence).

If the signal provided to the audio player exceeds full scale, then the value may be > 0.


**Note:** The value returned is in reference to when updateMeters was last called. You must call updateMeters again before calling this method to get a current value.

| channelNumber | The channel to get the value from. For mono or left, use 0. For right, use 1. |

| void OALAudioTrack::clear | ( | ) | ` [virtual]` |

Unload and clear all audio data, stop playing, and stop all operations.

| void OALAudioTrack::fadeTo:duration:target:selector: | ( | float | gain, |
| [duration] float | duration, |
||
| [target] id | target, |
||
| [selector] SEL | selector |
||
| ) | ` [virtual]` |

Fade to the specified gain value.

| gain | The gain to fade to. |
| duration | The duration of the fade operation in seconds. |
| target | The target to notify when the fade completes (can be nil). |
| selector | The selector to call when the fade completes. The selector must accept a single parameter, which will be the object that performed the fade. |

| void OALAudioTrack::panTo:duration:target:selector: | ( | float | pan, |
| [duration] float | duration, |
||
| [target] id | target, |
||
| [selector] SEL | selector |
||
| ) | ` [virtual]` |

Pan to the specified pan value.

**Note:** This will have no effect on iOS versions prior to 4.0.

| pan | The value to pan to. |
| duration | The duration of the pan operation in seconds. |
| target | The target to notify when the pan completes (can be nil). |
| selector | The selector to call when the pan completes. The selector must accept a single parameter, which will be the object that performed the pan. |

| float OALAudioTrack::peakPowerForChannel: | ( | NSUInteger | channelNumber | ) | ` [virtual]` |

Gives the peak power for a given channel, in decibels, for the sound being played.

0 dB indicates maximum power (full scale).

-160 dB indicates minimum power (near silence).

If the signal provided to the audio player exceeds full scale, then the value may be > 0.


**Note:** The value returned is in reference to when updateMeters was last called. You must call updateMeters again before calling this method to get a current value.

| channelNumber | The channel to get the value from. For mono or left, use 0. For right, use 1. |

| bool OALAudioTrack::play | ( | ) | ` [virtual]` |

Play the currently loaded audio track.

Plays the currently preloaded track asynchronously when the specified track completes.

**Note:** This will have no effect on iOS versions prior to 4.0.

| track | The track to play after |

| bool OALAudioTrack::playAfterTrack:timeAdjust: | ( |
|

` [virtual]`

Plays the currently preloaded track asynchronously when the specified track completes.

**Note:** This will have no effect on iOS versions prior to 4.0.

| track | The track to play after |
| timeAdjust | fine-tune value added to the time start offset. |

| bool OALAudioTrack::playAtTime: | ( | NSTimeInterval | time | ) | ` [virtual]` |

Plays a sound asynchronously, starting at a specified point in the audio output device’s timeline.

**Note:** This will have no effect on iOS versions prior to 4.0.

| time | The time (device time) to start playing at. |

| bool OALAudioTrack::playFile: | ( | NSString* | path | ) | ` [virtual]` |

Play the contents of a file once.

| path | The file containing the sound data. |

| bool OALAudioTrack::playFile:loops: | ( | NSString* | path, |
| [loops] NSInteger | loops |
||
| ) | ` [virtual]` |

Play the contents of a file and loop the specified number of times.

| path | The file containing the sound data. |
| loops | The number of times to loop playback (-1 = forever) |

| void OALAudioTrack::playFileAsync:loops:target:selector: | ( | NSString* | path, |
| [loops] NSInteger | loops, |
||
| [target] id | target, |
||
| [selector] SEL | selector |
||
| ) | ` [virtual]` |

Play the contents of a file asynchronously and loop the specified number of times.

| path | The file containing the sound data. |
| loops | The number of times to loop playback (-1 = forever) |
| target | the target to inform when playing has started. |
| selector | the selector to call when playing has started. |

| void OALAudioTrack::playFileAsync:target:selector: | ( | NSString* | path, |
| [target] id | target, |
||
| [selector] SEL | selector |
||
| ) | ` [virtual]` |

Play the contents of a file asynchronously once.

| path | The file containing the sound data. |
| target | the target to inform when playing has started. |
| selector | the selector to call when playing has started. |

| bool OALAudioTrack::playUrl: | ( | NSURL* | url | ) | ` [virtual]` |

Play the contents of a URL once.

| url | The URL containing the sound data. |

| bool OALAudioTrack::playUrl:loops: | ( | NSURL* | url, |
| [loops] NSInteger | loops |
||
| ) | ` [virtual]` |

Play the contents of a URL and loop the specified number of times.

| url | The URL containing the sound data. |
| loops | The number of times to loop playback (-1 = forever) |

| void OALAudioTrack::playUrlAsync:loops:target:selector: | ( | NSURL* | url, |
| [loops] NSInteger | loops, |
||
| [target] id | target, |
||
| [selector] SEL | selector |
||
| ) | ` [virtual]` |

Play the contents of a URL asynchronously and loop the specified number of times.

| url | The URL containing the sound data. |
| loops | The number of times to loop playback (-1 = forever) |
| target | the target to inform when playing has started. |
| selector | the selector to call when playing has started. |

| void OALAudioTrack::playUrlAsync:target:selector: | ( | NSURL* | url, |
| [target] id | target, |
||
| [selector] SEL | selector |
||
| ) | ` [virtual]` |

Play the contents of a URL asynchronously once.

| url | The URL containing the sound data. |
| target | the target to inform when playing has started. |
| selector | the selector to call when playing has started. |

| bool OALAudioTrack::preloadFile: | ( | NSString* | path | ) | ` [virtual]` |

Preload the contents of a file for playback.

Once the audio data is preloaded, you can call "play" to play it.


| path | The file containing the sound data. |

| bool OALAudioTrack::preloadFile:seekTime: | ( | NSString* | path, |
| [seekTime] NSTimeInterval | seekTime |
||
| ) | ` [virtual]` |

Preload the contents of a file for playback.

Once the audio data is preloaded, you can call "play" to play it.


| path | The file containing the sound data. |
| seekTime | The position in the file to start playing at. |

| bool OALAudioTrack::preloadFileAsync:seekTime:target:selector: | ( | NSString* | path, |
| [seekTime] NSTimeInterval | seekTime, |
||
| [target] id | target, |
||
| [selector] SEL | selector |
||
| ) | ` [virtual]` |

Asynchronously preload the contents of a file for playback.

Once the audio data is preloaded, you can call "play" to play it.


| path | The file containing the sound data. |
| seekTime | The position in the file to start playing at. |
| target | the target to inform when preparation is complete. |
| selector | the selector to call when preparation is complete. |

| bool OALAudioTrack::preloadFileAsync:target:selector: | ( | NSString* | path, |
| [target] id | target, |
||
| [selector] SEL | selector |
||
| ) | ` [virtual]` |

Asynchronously preload the contents of a file for playback.

Once the audio data is preloaded, you can call "play" to play it.


| path | The file containing the sound data. |
| target | the target to inform when preparation is complete. |
| selector | the selector to call when preparation is complete. |

| bool OALAudioTrack::preloadUrl: | ( | NSURL* | url | ) | ` [virtual]` |

Preload the contents of a URL for playback.

Once the audio data is preloaded, you can call "play" to play it.


| url | The URL containing the sound data. |

| bool OALAudioTrack::preloadUrl:seekTime: | ( | NSURL* | url, |
| [seekTime] NSTimeInterval | seekTime |
||
| ) | ` [virtual]` |

Preload the contents of a URL for playback.

Once the audio data is preloaded, you can call "play" to play it.


| url | The URL containing the sound data. |
| seekTime | The position in the file to start playing at. |

| bool OALAudioTrack::preloadUrlAsync:seekTime:target:selector: | ( | NSURL* | url, |
| [seekTime] NSTimeInterval | seekTime, |
||
| [target] id | target, |
||
| [selector] SEL | selector |
||
| ) | ` [virtual]` |

Asynchronously preload the contents of a URL for playback.

Once the audio data is preloaded, you can call "play" to play it.


| url | The URL containing the sound data. |
| seekTime | The position in the file to start playing at. |
| target | the target to inform when preparation is complete. |
| selector | the selector to call when preparation is complete. |

| bool OALAudioTrack::preloadUrlAsync:target:selector: | ( | NSURL* | url, |
| [target] id | target, |
||
| [selector] SEL | selector |
||
| ) | ` [virtual]` |

Asynchronously preload the contents of a URL for playback.

Once the audio data is preloaded, you can call "play" to play it.


| url | The URL containing the sound data. |
| target | the target to inform when preparation is complete. |
| selector | the selector to call when preparation is complete. |

| void OALAudioTrack::stop | ( | ) | ` [virtual]` |

Stop playing and stop all operations.

| void OALAudioTrack::stopActions | ( | ) | ` [virtual]` |

Stop any internal fade or pan actions.

| void OALAudioTrack::stopFade | ( | ) | ` [virtual]` |

Stop the currently running fade operation, if any.

| void OALAudioTrack::stopPan | ( | ) | ` [virtual]` |

Stop the currently running pan operation, if any.

**Note:** This will have no effect on iOS versions prior to 4.0.

| id OALAudioTrack::track | ( | ) | ` [static, virtual]` |

Create a new audio track.

| void OALAudioTrack::updateMeters | ( | ) | ` [virtual]` |

Updates the metering system to give current values.

You must call this method before calling averagePowerForChannel or peakPowerForChannel in order to get current values.

Operation queue for running asynchronous operations.

**Note:** Only one asynchronous operation is allowed at a time.

When the simulator is running (and the playback fix is in use), player will be copied to here, and then player set to nil.

This prevents other code from inadvertently raising the volume and starting playback.

Handles suspending and interrupting for this object.

bool OALAudioTrack::autoPreload` [read, write, assign]` |

If true, automatically preload again when playback stops.

NSURL * OALAudioTrack::currentlyLoadedUrl` [read, assign]` |

The URL of the currently loaded audio data.

NSTimeInterval OALAudioTrack::currentTime` [read, write, assign]` |

The current playback position in seconds from the start of the sound.

You can set this to change the playback position, whether it is currently playing or not.

id< AVAudioPlayerDelegate > OALAudioTrack::delegate` [read, write, assign]` |

Optional object that will receive notifications for decoding errors, audio interruptions (such as an incoming phone call), and playback completion.


**Note:** [OALAudioTrack](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_audio_track/) keeps a WEAK reference to delegate, so make sure you clear it when your object is going to be deallocated.

NSTimeInterval OALAudioTrack::deviceCurrentTime` [read, assign]` |

The value of this property increases monotonically while an audio player is playing or paused.




If more than one audio player is connected to the audio output device, device time continues incrementing as long as at least one of the players is playing or paused.



If the audio output device has no connected audio players that are either playing or paused, device time reverts to 0.



Use this property to indicate “now” when calling the playAtTime: instance method. By configuring multiple audio players to play at a specified offset from deviceCurrentTime, you can perform precise synchronization—as described in the discussion for that method.

**Note:** This will have no effect on iOS versions prior to 4.0.

NSTimeInterval OALAudioTrack::duration` [read, assign]` |

The duration, in seconds, of the currently loaded sound.

float OALAudioTrack::gain` [read, write, assign]` |

The gain (volume) for playback (0.0 - 1.0, where 1.0 = no attenuation).

bool OALAudioTrack::meteringEnabled` [read, write, assign]` |

If true, this track is recording metering data.

If true, metering is enabled.

bool OALAudioTrack::muted` [read, write, assign]` |

If true, audio track is muted.

NSUInteger OALAudioTrack::numberOfChannels` [read, assign]` |

The number of channels in the currently loaded sound.

NSInteger OALAudioTrack::numberOfLoops` [read, write, assign]` |

The number of times to loop playback (-1 = forever).

**Note:** This value will be ignored, and get changed when you call the various playXX methods. Only "play" will use the current value of "numberOfLoops".

float OALAudioTrack::pan` [read, write, assign]` |

Pan value (-1.0 = far left, 1.0 = far right).

**Note:** This will have no effect on iOS versions prior to 4.0.

bool OALAudioTrack::paused` [read, write, assign]` |

If true, pause playback.

AVAudioPlayer * OALAudioTrack::player` [read, assign]` |

Access to the underlying AVAudioPlayer object.

WARNING: Be VERY careful when accessing this, as some methods could cause it to fall out of sync with [OALAudioTrack](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_audio_track/) (particularly play/pause/stop methods).

bool OALAudioTrack::playing` [read, assign]` |

If true, the audio player is currently playing.

If true, background music is currently playing.

We need to maintain our own value because AVAudioPlayer will sometimes say it's not playing when it actually is.

bool OALAudioTrack::preloaded` [read, assign]` |

If true, audio track is in preloaded state.

float OALAudioTrack::volume` [read, write, assign]` |

The volume (alias to gain) for playback (0.0 - 1.0, where 1.0 = no attenuation).