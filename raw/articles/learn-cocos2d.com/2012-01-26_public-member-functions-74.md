---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_a_l_context/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

A context encompasses a single listener and a series of sources.
[More...](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_a_l_context/#details)

`#include <ALContext.h>`


| id |
|

A context encompasses a single listener and a series of sources.

A context is created from a device, and many contexts may be created (though multiple contexts would be unusual in an iOS app).


Note: Some property values are only valid if this context is the current context.

| void ALContext::clearBuffers | ( | ) | ` [virtual]` |

Clear all buffers being used by sources in this context.

| id ALContext::contextOnDevice:attributes: | ( |
|

` [static, virtual]`

Create a new context on the specified device.

| device | The device to open the context on. |
| attributes | An array of NSNumber in ordered pairs (attribute id followed by integer value). Posible attributes: ALC_FREQUENCY, ALC_REFRESH, ALC_SYNC, ALC_MONO_SOURCES, ALC_STEREO_SOURCES |

| id ALContext::contextOnDevice:outputFrequency:refreshIntervals:synchronousContext:monoSources:stereoSources: | ( |
|

` [static, virtual]`

Create a new context on the specified device with attributes.

| device | The device to open the context on. |
| outputFrequency | The frequency to mix all sources to before outputting (ignored by iOS). |
| refreshIntervals | The number of passes per second used to mix the audio sources. For games this can be 5-15. For audio intensive apps, it should be higher (ignored by iOS). |
| synchronousContext | If true, this context runs on the main thread and depends on you calling alcUpdateContext (ignored by iOS). |
| monoSources | A hint indicating how many sources should support mono (default 28 on iOS). |
| stereoSources | A hint indicating how many sources should support stereo (default 4 on iOS). |

| void ALContext::ensureContextIsCurrent | ( | ) | ` [virtual]` |

Make sure this context is the current context.

This method is used to work around iOS 4.0 and 4.2 bugs that could cause the context to be lost.

| void * ALContext::getProcAddress: | ( | NSString* | functionName | ) | ` [virtual]` |

Get the address of the specified procedure (C function address).

Only valid when this is the current context.

**Note:** The OpenAL implementation is free to return a pointer even if it is not valid for this context. Always call isExtensionPresent first.

| functionName | the name of the procedure to get. |

| id ALContext::initOnDevice:attributes: | ( |
|

` [virtual]`

Initialize this context for the specified device and attributes.

| device | The device to open the context on. |
| attributes | An array of NSNumber in ordered pairs (attribute id followed by integer value). Posible attributes: ALC_FREQUENCY, ALC_REFRESH, ALC_SYNC, ALC_MONO_SOURCES, ALC_STEREO_SOURCES |

| id ALContext::initOnDevice:outputFrequency:refreshIntervals:synchronousContext:monoSources:stereoSources: | ( |
|

` [virtual]`

Initialize this context on the specified device with attributes.

| device | The device to open the context on. |
| outputFrequency | The frequency to mix all sources to before outputting (ignored by iOS). |
| refreshIntervals | The number of passes per second used to mix the audio sources. For games this can be 5-15. For audio intensive apps, it should be higher (ignored by iOS). |
| synchronousContext | If true, this context runs on the main thread and depends on you calling alcUpdateContext (ignored by iOS). |
| monoSources | A hint indicating how many sources should support mono (default 28 on iOS). |
| stereoSources | A hint indicating how many sources should support stereo (default 4 on iOS). |

| bool ALContext::isExtensionPresent: | ( | NSString* | name | ) | ` [virtual]` |

Check if the specified extension is present in this context.

Only valid when this is the current context.

| name | The name of the extension to check. |

| void ALContext::process | ( | ) | ` [virtual]` |

Process this context.

| void ALContext::stopAllSounds | ( | ) | ` [virtual]` |

Stop all sound sources in this context.

Handles suspending and interrupting for this object.

NSString * ALContext::alVersion` [read, assign]` |

OpenAL version string in format “[spec major number].

[spec minor number] [optional vendor version information]” Only valid when this is the current context.

The current context's attribute list.

Only valid when this is the current context.

ALCcontext * ALContext::context` [read, assign]` |

The OpenAL context pointer.

ALenum ALContext::distanceModel` [read, write, assign]` |

The current distance model.

Legal values are AL_NONE, AL_INVERSE_DISTANCE, AL_INVERSE_DISTANCE_CLAMPED, AL_LINEAR_DISTANCE, AL_LINEAR_DISTANCE_CLAMPED, AL_EXPONENT_DISTANCE, and AL_EXPONENT_DISTANCE_CLAMPED. See the OpenAL spec for detailed information.

Only valid when this is the current context.

float ALContext::dopplerFactor` [read, write, assign]` |

Exaggeration factor for Doppler effect.

Only valid when this is the current context.

NSArray * ALContext::extensions` [read, assign]` |

List of available extensions (NSString*).

Only valid when this is the current context.

NSString * ALContext::renderer` [read, assign]` |

Information about the specific renderer.

Only valid when this is the current context.

float ALContext::speedOfSound` [read, write, assign]` |

Speed of sound in same units as velocities.

Only valid when this is the current context.

NSString * ALContext::vendor` [read, assign]` |

Name of the vendor.

Only valid when this is the current context.