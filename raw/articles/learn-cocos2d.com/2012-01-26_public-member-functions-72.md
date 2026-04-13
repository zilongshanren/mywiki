---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_a_l_buffer/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

A buffer for audio data that will be played via a SoundSource.
[More...](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_a_l_buffer/#details)

`#include <ALBuffer.h>`


| id |
|

A buffer for audio data that will be played via a SoundSource.

| id ALBuffer::bufferWithName:data:size:format:frequency: | ( | NSString* | name, |
| [data] void* | data, |
||
| [size] ALsizei | size, |
||
| [format] ALenum | format, |
||
| [frequency] ALsizei | frequency |
||
| ) | ` [static, virtual]` |

Make a new buffer.

| name | Optional name that you can use to identify this buffer in your code. |
| data | The sound data. Note:
|

| id ALBuffer::initWithName:data:size:format:frequency: | ( | NSString* | name, |
| [data] void* | data, |
||
| [size] ALsizei | size, |
||
| [format] ALenum | format, |
||
| [frequency] ALsizei | frequency |
||
| ) | ` [virtual]` |

Initialize the buffer.

| name | Optional name that you can use to identify this buffer in your code. |
| data | The sound data. Note:
|

|

` [virtual]`

Returns a part of the buffer as a new buffer.

You can use this method to split a buffer into a sub-buffers. The sub-buffers retain a reference to their parent buffer, and share the same memory. Therefore, modifying the parent buffer contents will affect its slices and vice-versa.

| sliceName | Optional name that you can use to identify the created buffer in your code. |
| offset | The offset in sound frames where the slice starts. |
| size | The size of the slice in frames. |

ALint ALBuffer::bits` [read, assign]` |

The size of a sample in bits.

ALuint ALBuffer::bufferId` [read, assign]` |

The ID assigned to this buffer by OpenAL.

ALint ALBuffer::channels` [read, assign]` |

The number of channels the buffer data plays in.

float ALBuffer::duration` [read, assign]` |

The duration of the sample in this buffer, in seconds.

ALenum ALBuffer::format` [read, assign]` |

The format of the audio data (see al.h, AL_FORMAT_XXX).

bool ALBuffer::freeDataOnDestroy` [read, write, assign]` |

If true, calls free() on the audio data when this object gets destroyed.

Default: YES

ALint ALBuffer::frequency` [read, assign]` |

The frequency this buffer runs at.

NSString * ALBuffer::name` [read, write, retain]` |

The name given to this buffer upon creation.

You may change it at runtime if you wish.

ALint ALBuffer::size` [read, assign]` |

The size, in bytes, of the currently loaded buffer data.