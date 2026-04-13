---
title: 'ObjectAL: Class List'
url: http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/annotated/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[ALBuffer](../../../../../api-ref/1.0/ObjectAL/html/interface_a_l_buffer/) | A buffer for audio data that will be played via a SoundSource |
[ALCaptureDevice](/) | *UNIMPLEMENTED FOR IOS* An OpenAL device for capturing sound data |
[ALChannelSource](../../../../../api-ref/1.0/ObjectAL/html/interface_a_l_channel_source/) | A Sound source composed of other sources |
[ALContext](../../../../../api-ref/1.0/ObjectAL/html/interface_a_l_context/) | A context encompasses a single listener and a series of sources |
[ALDevice](../../../../../api-ref/1.0/ObjectAL/html/interface_a_l_device/) | A device is a logical mapping to an audio device through the OpenAL implementation |
[ALListener](../../../../../api-ref/1.0/ObjectAL/html/interface_a_l_listener/) | The listener represents the user who is listening to sounds in 3D space |
[ALOrientation](../../../../../api-ref/1.0/ObjectAL/html/struct_a_l_orientation/) | Represents an orientation, consisting of an "at" vector (representing the "forward" direction), and the "up" vector (representing "up" for the subject) |
[ALPoint](../../../../../api-ref/1.0/ObjectAL/html/struct_a_l_point/) | Represents a 3-dimensional point for certain [ObjectAL](../../../../../api-ref/1.0/ObjectAL/html/interface_object_a_l/) properties |
[<ALSoundSource>](../../../../../api-ref/1.0/ObjectAL/html/protocol_a_l_sound_source-p/) | Manages all properties relating to an OpenAL sound source |
[ALSoundSourcePool](../../../../../api-ref/1.0/ObjectAL/html/interface_a_l_sound_source_pool/) | A pool of sound sources, which can be fetched based on availability |
[ALSource](../../../../../api-ref/1.0/ObjectAL/html/interface_a_l_source/) | A source represents an object that emits sound which can be heard by a listener |
[ALVector](../../../../../api-ref/1.0/ObjectAL/html/struct_a_l_vector/) | Represents a 3-dimensional vector for certain [ObjectAL](../../../../../api-ref/1.0/ObjectAL/html/interface_object_a_l/) properties |
[ALWrapper](../../../../../api-ref/1.0/ObjectAL/html/interface_a_l_wrapper/) | A thin wrapper around the C OpenAL API, with a few convenience methods thrown in |
[IOSVersion](/) | Reports the version of iOS being run on the current device |
[OALAction](../../../../../api-ref/1.0/ObjectAL/html/interface_o_a_l_action/) | Represents an action that can be performed on an object |
[OALActionManager](/) | Manages all [ObjectAL](../../../../../api-ref/1.0/ObjectAL/html/interface_object_a_l/) actions |
[OALAudioFile](/) | Maintains an open audio file and allows loading data from that file into new [ALBuffer](../../../../../api-ref/1.0/ObjectAL/html/interface_a_l_buffer/) objects |
[OALAudioSession](../../../../../api-ref/1.0/ObjectAL/html/interface_o_a_l_audio_session/) | Handles the audio session and interrupts |
[OALAudioTrack](../../../../../api-ref/1.0/ObjectAL/html/interface_o_a_l_audio_track/) | Plays an audio track via AVAudioPlayer |
[OALAudioTracks](/) | Keeps track of all AudioTrack objects |
[OALCallAction](/) | Calls a selector on a target |
[OALConcurrentActions](/) | A set of actions that get run concurrently |
[OALExponentialFunction](/) | Changes slowly at the start, and quickly at the end |
[<OALFunction>](/) | A function takes a value from 0.0 to 1.0 and returns another value from 0.0 to 1.0 |
[OALFunctionAction](/) | An action that applies a function to the proportionComplete parameter in [update] before applying the result to the target |
[OALGainAction](/) | A function-based action that modifies the target's gain |
[OALLinearFunction](/) | Function that changes at a constant rate |
[OALLogarithmicFunction](/) | Changes quickly at the start, and slowly at the end |
[OALMoveByAction](/) | Moves the target from its current position by the specified delta over time in 3D space |
[OALMoveToAction](/) | Moves the target from its current position to the specified position over time in 3D space |
[OALPanAction](/) | A function-based action that modifies the target's pan |
[OALPitchAction](/) | A function-based action that modifies the target's pitch |
[OALPlaceAction](/) | Places the target at the specified position |
[OALReverseFunction](/) | Returns the reverse of another function |
[OALSCurveFunction](/) | Changes slowly at the start, quickly at the midpoint, then slowly again at the end |
[OALSequentialActions](/) | A set of actions that get run in sequence |
[OALSimpleAudio](../../../../../api-ref/1.0/ObjectAL/html/interface_o_a_l_simple_audio/) | A simpler interface to the [ObjectAL](../../../../../api-ref/1.0/ObjectAL/html/interface_object_a_l/) sound library |
[OALSuspendHandler](../../../../../api-ref/1.0/ObjectAL/html/interface_o_a_l_suspend_handler/) | Provides two controls (interrupted and manuallySuspended) for suspending a slave object, and also propagates such control messages to interested listeners |
[<OALSuspendListener>](/) | Allows an object to participate in interrupt and suspend operations |
[<OALSuspendManager>](../../../../../api-ref/1.0/ObjectAL/html/protocol_o_a_l_suspend_manager-p/) | A suspend manager is a listener that also allows other objects to subscribe to receive events as the manager receives them |
[OALTargetedAction](/) | Ignores whatever target it was invoked upon and applies the specified action on the target specified at creation time |
[OALTools](../../../../../api-ref/1.0/ObjectAL/html/interface_o_a_l_tools/) | Miscellaneous tools used by [ObjectAL](../../../../../api-ref/1.0/ObjectAL/html/interface_object_a_l/) |
[ObjectAL](../../../../../api-ref/1.0/ObjectAL/html/interface_object_a_l/) | |
[OpenALManager](../../../../../api-ref/1.0/ObjectAL/html/interface_open_a_l_manager/) | Manager class for OpenAL objects ([ObjectAL](../../../../../api-ref/1.0/ObjectAL/html/interface_object_a_l/)) |