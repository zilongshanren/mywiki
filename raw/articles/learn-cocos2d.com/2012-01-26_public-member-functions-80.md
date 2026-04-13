---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_audio_session/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Handles the audio session and interrupts.
[More...](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_audio_session/#details)

`#include <OALAudioSession.h>`


| void |
|

Handles the audio session and interrupts.

| void OALAudioSession::forceEndInterruption | ( | ) | ` [virtual]` |

Force an interrupt end.

This can be useful in cases where a buggy OS fails to end an interrupt.

Be VERY CAREFUL when using this!

Singleton implementation providing "sharedInstance" and "purgeSharedInstance" methods.

**- (OALAudioSupport*) sharedInstance**: Get the shared singleton instance.

**- (void) purgeSharedInstance**: Purge (deallocate) the shared instance.

If true, the audio session was active when the interrupt occurred.

Marks the last time the audio session was reset due to error.

This is used to avoid getting stuck in a rapid-fire reset-error loop.

Handles suspending and interrupting for this object.

bool OALAudioSession::allowIpod` [read, write, assign]` |

If YES, allow ipod music to continue playing (NOT SUPPORTED ON THE SIMULATOR).

Note: If this is enabled, and another app is playing music, background audio playback will use the SOFTWARE codecs, NOT hardware.


If allowIpod = NO, the application will ALWAYS use hardware decoding.


Default value: YES

NSString * OALAudioSession::audioRoute` [read, assign]` |

Check what hardware route the audio is taking, such as "Speaker" or "Headphone" (not supported on the simulator).

bool OALAudioSession::audioSessionActive` [read, write, assign]` |

If true, the audio session is active.

NSString * OALAudioSession::audioSessionCategory` [read, write, retain]` |

The current audio session category.

If this value is explicitly set, the other session properties "allowIpod", "useHardwareIfAvailable", "honorSilentSwitch", and "ipodDucking" may be modified to remain compatible with the category.

Default value: nil

id<AVAudioSessionDelegate> OALAudioSession::audioSessionDelegate` [read, write, assign]` |

Delegate that will receive all audio session events.

bool OALAudioSession::handleInterruptions` [read, write, assign]` |

If true, automatically handle interruptions.



Default value: YES

bool OALAudioSession::hardwareMuted` [read, assign]` |

Check if the hardware mute switch is on (not supported on the simulator).

Note: If headphones are plugged in, hardwareMuted will always return FALSE regardless of the switch state.

float OALAudioSession::hardwareVolume` [read, assign]` |

Get the device's final hardware output volume, as controlled by the volume button on the side of the device.

bool OALAudioSession::honorSilentSwitch` [read, write, assign]` |

If true, mute when backgrounded, screen locked, or the ringer switch is turned off (NOT SUPPORTED ON THE SIMULATOR).



Default value: YES

bool OALAudioSession::ipodDucking` [read, write, assign]` |

If YES, ipod music will duck (lower in volume) when the audio session activates.

Default value: NO

bool OALAudioSession::ipodPlaying` [read, assign]` |

If true, another application (usually iPod) is playing music.

bool OALAudioSession::useHardwareIfAvailable` [read, write, assign]` |

Determines what to do if no other application is playing audio and allowIpod = YES (NOT SUPPORTED ON THE SIMULATOR).



If NO, the application will ALWAYS use software decoding. The advantage to this is that the user can background your application and then start audio playing from another application. If useHardwareIfAvailable = YES, the user won't be able to do this.


If this is set to YES, the application will use hardware decoding if no other application is currently playing audio. However, no other application will be able to start playing audio if it wasn't playing already.


Note: This switch has no effect if allowIpod = NO.


Default value: YES