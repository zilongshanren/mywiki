---
title: Static Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_tools/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Miscellaneous tools used by [ObjectAL](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_object_a_l/).
[More...](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_tools/#details)

`#include <OALTools.h>`


| NSURL * |
|

| void OALTools::notifyAudioSessionError:function:description: | ( | OSStatus | errorCode, |
| [function] const char* | function, |
||
| [description] NSString* | description, |
||
| [,] | ... |
||
| ) | ` [static, virtual]` |

Notify an error if the specified AudioSession error code indicates an error.

This will log the error and also potentially post an audio error notification (OALAudioErrorNotification) if it is suspected that this error is a result of the audio session getting corrupted.

| errorCode,: | The error code returned from an OS call. |
| function,: | The function name where the error occurred. |
| description,: | A printf-style description of what happened. |

| void OALTools::notifyExtAudioError:function:description: | ( | OSStatus | errorCode, |
| [function] const char* | function, |
||
| [description] NSString* | description, |
||
| [,] | ... |
||
| ) | ` [static, virtual]` |

Notify an error if the specified ExtAudio error code indicates an error.

This will log the error and also potentially post an audio error notification (OALAudioErrorNotification) if it is suspected that this error is a result of the audio session getting corrupted.

| errorCode,: | The error code returned from an OS call. |
| function,: | The function name where the error occurred. |
| description,: | A printf-style description of what happened. |

| NSURL * OALTools::urlForPath: | ( | NSString* | path | ) | ` [static, virtual]` |

Returns the URL corresponding to the specified path.

If the path is not absolute (starts with a "/"), this method will look for the file in the application's main bundle.

| path | The path to convert to a URL. |