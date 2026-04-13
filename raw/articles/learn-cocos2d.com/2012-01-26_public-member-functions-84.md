---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_open_a_l_manager/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Manager class for OpenAL objects ([ObjectAL](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_object_a_l/)).
[More...](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_open_a_l_manager/#details)

`#include <OpenALManager.h>`


|

Manager class for OpenAL objects ([ObjectAL](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_object_a_l/)).

Keeps track of devices that have been opened, and allows high level OpenAL management.

Provides methods for loading [ALBuffer](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_a_l_buffer/) objects from audio files.

The OpenAL 1.1 specification is available at [http://connect.creativelabs.com/openal/Documentation](http://connect.creativelabs.com/openal/Documentation)

Be sure to read through it (especially the part about distance models) as [ObjectAL](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_object_a_l/) follows the OpenAL object model.


Alternatively, you may opt to use [OALSimpleAudio](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_simple_audio/) for a simpler interface.

| NSString * OpenALManager::bufferAsyncFromFile:reduceToMono:target:selector: | ( | NSString* | filePath, |
| [reduceToMono] bool | reduceToMono, |
||
| [target] id | target, |
||
| [selector] SEL | selector |
||
| ) | ` [virtual]` |

Load an OpenAL buffer with the contents of an audio file asynchronously.

This method will schedule a request to have the buffer created and filled, and then call the specified selector with the newly created buffer.

The buffer's name will be the fully qualified URL of the path.

Returns the fully qualified URL of the path, which you can match up to the buffer name in your callback method.

See the class description note regarding sound file formats.

| filePath | The path of the file containing the audio data. |
| reduceToMono | If true, reduce the sample to mono (stereo samples don't support panning or positional audio). |
| target | The target to call when the buffer is loaded. |
| selector | The selector to invoke when the buffer is loaded. |

| NSString * OpenALManager::bufferAsyncFromFile:target:selector: | ( | NSString* | filePath, |
| [target] id | target, |
||
| [selector] SEL | selector |
||
| ) | ` [virtual]` |

Load an OpenAL buffer with the contents of an audio file asynchronously.

This method will schedule a request to have the buffer created and filled, and then call the specified selector with the newly created buffer.

The buffer's name will be the fully qualified URL of the path.

Returns the fully qualified URL of the path, which you can match up to the buffer name in your callback method.

See the class description note regarding sound file formats.

| filePath | The path of the file containing the audio data. |
| target | The target to call when the buffer is loaded. |
| selector | The selector to invoke when the buffer is loaded. |

| NSString * OpenALManager::bufferAsyncFromUrl:reduceToMono:target:selector: | ( | NSURL* | url, |
| [reduceToMono] bool | reduceToMono, |
||
| [target] id | target, |
||
| [selector] SEL | selector |
||
| ) | ` [virtual]` |

Load an OpenAL buffer with the contents of a URL asynchronously.

This method will schedule a request to have the buffer created and filled, and then call the specified selector with the newly created buffer.

The buffer's name will be the fully qualified URL.

Returns the fully qualified URL, which you can match up to the buffer name in your callback method.

See the class description note regarding sound file formats.

| url | The URL of the file containing the audio data. |
| reduceToMono | If true, reduce the sample to mono (stereo samples don't support panning or positional audio). |
| target | The target to call when the buffer is loaded. |
| selector | The selector to invoke when the buffer is loaded. |

| NSString * OpenALManager::bufferAsyncFromUrl:target:selector: | ( | NSURL* | url, |
| [target] id | target, |
||
| [selector] SEL | selector |
||
| ) | ` [virtual]` |

Load an OpenAL buffer with the contents of a URL asynchronously.

This method will schedule a request to have the buffer created and filled, and then call the specified selector with the newly created buffer.

The buffer's name will be the fully qualified URL.

Returns the fully qualified URL, which you can match up to the buffer name in your callback method.

See the class description note regarding sound file formats.

| url | The URL of the file containing the audio data. |
| target | The target to call when the buffer is loaded. |
| selector | The selector to invoke when the buffer is loaded. |

Load an OpenAL buffer with the contents of an audio file.

The buffer's name will be the fully qualified URL of the path.

See the class description note regarding sound file formats.

| filePath | The path of the file containing the audio data. |

|

` [virtual]`

Load an OpenAL buffer with the contents of an audio file.

The buffer's name will be the fully qualified URL of the path.

See the class description note regarding sound file formats.

| filePath | The path of the file containing the audio data. |
| reduceToMono | If true, reduce the sample to mono (stereo samples don't support panning or positional audio). |

Load an OpenAL buffer with the contents of an audio file.

The buffer's name will be the fully qualified URL.

See the class description note regarding sound file formats.

| url | The URL of the file containing the audio data. |

|

` [virtual]`

Load an OpenAL buffer with the contents of an audio file.

The buffer's name will be the fully qualified URL.

See the class description note regarding sound file formats.

| url | The URL of the file containing the audio data. |
| reduceToMono | If true, reduce the sample to mono (stereo samples don't support panning or positional audio). |

| void OpenALManager::clearAllBuffers | ( | ) | ` [virtual]` |

Clear all references to sound data from ALL buffers, managed or not.

(INTERNAL USE) Notify that a device is deallocating.

(INTERNAL USE) Notify that a device is initializing.

Singleton implementation providing "sharedInstance" and "purgeSharedInstance" methods.

**- (OpenALManager*) sharedInstance**: Get the shared singleton instance.

**- (void) purgeSharedInstance**: Purge (deallocate) the shared instance.

Operation queue for asynchronous loading.

Handles suspending and interrupting for this object.

NSArray * OpenALManager::availableCaptureDevices` [read, assign]` |

List of available capture devices (NSString*).

NSArray * OpenALManager::availableDevices` [read, assign]` |

List of available playback devices (NSString*).

The current context (some context operations require the context to be the "current" one).

NSString * OpenALManager::defaultCaptureDeviceSpecifier` [read, assign]` |

Name of the default capture device.

NSString * OpenALManager::defaultDeviceSpecifier` [read, assign]` |

Name of the default playback device.

ALdouble OpenALManager::mixerOutputFrequency` [read, write, assign]` |

The frequency of the output mixer.