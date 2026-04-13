---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_a_l_source/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

A source represents an object that emits sound which can be heard by a listener.
[More...](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_a_l_source/#details)

`#include <ALSource.h>`


| id |
|

A source represents an object that emits sound which can be heard by a listener.

This source can have position, velocity, and direction.

Initialize a new source on the specified context.

| context | the context to create the source on. |

Play the currently attached buffer.

Add a buffer to the buffer queue.

| buffer | the buffer to add to the queue. |

Add a buffer to the buffer queue, repeating it multiple times.

| buffer | the buffer to add to the queue. |
| repeats | the number of times to repeat the buffer in the queue. |

| bool ALSource::queueBuffers: | ( | NSArray* | buffers | ) | ` [virtual]` |

Add buffers to the buffer queue.

| buffers | the buffers to add to the queue. |

| bool ALSource::queueBuffers:repeats: | ( | NSArray* | buffers, |
| [repeats] NSUInteger | repeats |
||
| ) | ` [virtual]` |

Add buffers to the buffer queue, repeating it multiple times.

The buffers will be played in order, repeating the specified number of times.

| buffers | the buffers to add to the queue. |
| repeats | the number of times to repeat the buffer in the queue. |

| id ALSource::source | ( | ) | ` [static, virtual]` |

Create a new source.

Create a new source on the specified context.

| context | the context to create the source on. |

Remove a buffer from the buffer queue.

| buffer | the buffer to remove from the queue. |

| bool ALSource::unqueueBuffers: | ( | NSArray* | buffers | ) | ` [virtual]` |

Remove buffers from the buffer queue.

| buffers | the buffers to remove from the queue. |

Used to abort a pending playback resume if the user calls stop or pause.

Shadow value which keeps the correct state value for AL_PLAYING and AL_PAUSED.

We need this due to a buggy OpenAL implementation.

Handles suspending and interrupting for this object.

The sound buffer this source is attached to (set to nil to detach the currently attached buffer).

int ALSource::buffersProcessed` [read, assign]` |

How many of these buffers have been processed during playback.

int ALSource::buffersQueued` [read, assign]` |

How many buffers this source has queued.

float ALSource::offsetInBytes` [read, write, assign]` |

The offset into the current buffer (in bytes).

float ALSource::offsetInSamples` [read, write, assign]` |

The offset into the current buffer (in samples).

float ALSource::offsetInSeconds` [read, write, assign]` |

The offset into the current buffer (in seconds).

ALuint ALSource::sourceId` [read, assign]` |

OpenAL's ID for this source.

int ALSource::state` [read, write, assign]` |

The state of this source.