---
title: Static Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_a_l_wrapper/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

A thin wrapper around the C OpenAL API, with a few convenience methods thrown in.
[More...](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_a_l_wrapper/#details)

`#include <ALWrapper.h>`


| bool |
|

A thin wrapper around the C OpenAL API, with a few convenience methods thrown in.

Wherever possible, methods return the requested data rather than requiring a pointer to be passed in. Besides collecting the API calls into a single global object, all calls are combined with an error check. Any OpenAL errors that occur will be logged if error logging is enabled.

| bool ALWrapper::buffer3f:parameter:v1:v2:v3: | ( | ALuint | bufferId, |
| [parameter] ALenum | parameter, |
||
| [v1] ALfloat | v1, |
||
| [v2] ALfloat | v2, |
||
| [v3] ALfloat | v3 |
||
| ) | ` [static, virtual]` |

Write a 3 float paramter to a buffer.

| bufferId | The buffer's ID. |
| parameter | the parameter to write to. |
| v1 | The first value to write. |
| v2 | The second value to write. |
| v3 | The third value to write. |

| bool ALWrapper::buffer3i:parameter:v1:v2:v3: | ( | ALuint | bufferId, |
| [parameter] ALenum | parameter, |
||
| [v1] ALint | v1, |
||
| [v2] ALint | v2, |
||
| [v3] ALint | v3 |
||
| ) | ` [static, virtual]` |

Write a 3 integer paramter to a buffer.

| bufferId | The buffer's ID. |
| parameter | The parameter to write to. |
| v1 | The first value to write. |
| v2 | The second value to write. |
| v3 | The third value to write. |

| bool ALWrapper::bufferData:format:data:size:frequency: | ( | ALuint | bufferId, |
| [format] ALenum | format, |
||
| [data] const ALvoid* | data, |
||
| [size] ALsizei | size, |
||
| [frequency] ALsizei | frequency |
||
| ) | ` [static, virtual]` |

Load data into a buffer.

| bufferId | The ID of the buffer to load data into. |
| format | The format of the data being loaded (typically AL_FORMAT_MONO16 or AL_FORMAT_STEREO16). |
| data | The audio data. |
| size | The size of the data in bytes. |
| frequency | The sample frequency of the data. |

| bool ALWrapper::bufferDataStatic:format:data:size:frequency: | ( | ALuint | bufferId, |
| [format] ALenum | format, |
||
| [data] const ALvoid* | data, |
||
| [size] ALsizei | size, |
||
| [frequency] ALsizei | frequency |
||
| ) | ` [static, virtual]` |

Load data into a buffer.

Unlike "bufferData", with this method the buffer will use the passed in data buffer direcly rather than allocating its own memory and copying from the data buffer.

| bufferId | The ID of the buffer to load data into. |
| format | The format of the data being loaded (typically AL_FORMAT_MONO16 or AL_FORMAT_STEREO16). |
| data | The audio data. |
| size | The size of the data in bytes. |
| frequency | The sample frequency of the data. |

| bool ALWrapper::bufferf:parameter:value: | ( | ALuint | bufferId, |
| [parameter] ALenum | parameter, |
||
| [value] ALfloat | value |
||
| ) | ` [static, virtual]` |

Write a float paramter to a buffer.

| bufferId | The buffer's ID. |
| parameter | The parameter to write to. |
| value | The value to write. |

| bool ALWrapper::bufferfv:parameter:values: | ( | ALuint | bufferId, |
| [parameter] ALenum | parameter, |
||
| [values] ALfloat* | values |
||
| ) | ` [static, virtual]` |

Write a float array paramter to a buffer.

| bufferId | The buffer's ID. |
| parameter | The parameter to write to. |
| values | The values to write. |

| bool ALWrapper::bufferi:parameter:value: | ( | ALuint | bufferId, |
| [parameter] ALenum | parameter, |
||
| [value] ALint | value |
||
| ) | ` [static, virtual]` |

Write an integer paramter to a buffer.

| bufferId | The buffer's ID. |
| parameter | The parameter to write to. |
| value | The value to write. |

| bool ALWrapper::bufferiv:parameter:values: | ( | ALuint | bufferId, |
| [parameter] ALenum | parameter, |
||
| [values] ALint* | values |
||
| ) | ` [static, virtual]` |

Write an integer array paramter to a buffer.

| bufferId | The buffer's ID. |
| parameter | The parameter to write to. |
| values | The values to write. |

| bool ALWrapper::captureSamples:buffer:numSamples: | ( | ALCdevice* | device, |
| [buffer] ALCvoid* | buffer, |
||
| [numSamples] ALCsizei | numSamples |
||
| ) | ` [static, virtual]` |

Get captured samples from a device.

| device | the device to fetch samples from. |
| buffer | the buffer to copy the samples into. |
| numSamples | the number of samples to fetch. |

| bool ALWrapper::closeCaptureDevice: | ( | ALCdevice* | device | ) | ` [static, virtual]` |

Close a capture device.

| device | The device to close. |

| bool ALWrapper::closeDevice: | ( | ALCdevice* | device | ) | ` [static, virtual]` |

Close a device.

| device | The device to close. |

| ALCcontext * ALWrapper::createContext:attributes: | ( | ALCdevice* | device, |
| [attributes] ALCint* | attributes |
||
| ) | ` [static, virtual]` |

Create an OpenAL context.

| device | The device to open the context on. |
| attributes | The attributes to use when creating the context. |

| bool ALWrapper::deleteBuffer: | ( | ALuint | bufferId | ) | ` [static, virtual]` |

Delete a buffer.

| bufferId | The ID of the buffer to delete. |

| bool ALWrapper::deleteBuffers:numBuffers: | ( | ALuint* | bufferIds, |
| [numBuffers] ALsizei | numBuffers |
||
| ) | ` [static, virtual]` |

Delete buffers.

| bufferIds | Pointer to an array containing the buffer IDs. |
| numBuffers | the number of buffers to delete. |

| bool ALWrapper::deleteSource: | ( | ALuint | sourceId | ) | ` [static, virtual]` |

Delete a source.

| sourceId | The ID of the source to delete. |

| bool ALWrapper::deleteSources:numSources: | ( | ALuint* | sourceIds, |
| [numSources] ALsizei | numSources |
||
| ) | ` [static, virtual]` |

Delete sources.

| sourceIds | Pointer to an array containing the source IDs. |
| numSources | the number of sources to delete. |

| void ALWrapper::destroyContext: | ( | ALCcontext* | context | ) | ` [static, virtual]` |

Destroy a context.

| context | The contect to destroy. |

| bool ALWrapper::disable: | ( | ALenum | capability | ) | ` [static, virtual]` |

Disable a capability.

| capability | The capability to disable. |

| bool ALWrapper::distanceModel: | ( | ALenum | value | ) | ` [static, virtual]` |

Set the distance model.

| value | The value to set. |

| bool ALWrapper::dopplerFactor: | ( | ALfloat | value | ) | ` [static, virtual]` |

Set the doppler factor.

| value | The value to set. |

| bool ALWrapper::enable: | ( | ALenum | capability | ) | ` [static, virtual]` |

Enable a capability.

| capability | The capability to enable. |

| ALuint ALWrapper::genBuffer | ( | ) | ` [static, virtual]` |

Generate a buffer.

| bool ALWrapper::genBuffers:numBuffers: | ( | ALuint* | bufferIds, |
| [numBuffers] ALsizei | numBuffers |
||
| ) | ` [static, virtual]` |

Generate buffers.

| bufferIds | Pointer to an array that will receive the buffer IDs. |
| numBuffers | the number of buffers to generate. |

| ALuint ALWrapper::genSource | ( | ) | ` [static, virtual]` |

Generate a source.

| bool ALWrapper::genSources:numSources: | ( | ALuint* | sourceIds, |
| [numSources] ALsizei | numSources |
||
| ) | ` [static, virtual]` |

Generate sources.

| sourceIds | Pointer to an array that will receive the source IDs. |
| numSources | the number of sources to generate. |

| bool ALWrapper::getBoolean: | ( | ALenum | parameter | ) | ` [static, virtual]` |

Get a boolean parameter.

| parameter | The parameter to fetch. |

| bool ALWrapper::getBooleanv:values: | ( | ALenum | parameter, |
| [values] ALboolean* | values |
||
| ) | ` [static, virtual]` |

Get a boolean array parameter.

| parameter | The parameter to fetch. |
| values | An array to hold the result. |

| bool ALWrapper::getBuffer3f:parameter:v1:v2:v3: | ( | ALuint | bufferId, |
| [parameter] ALenum | parameter, |
||
| [v1] ALfloat* | v1, |
||
| [v2] ALfloat* | v2, |
||
| [v3] ALfloat* | v3 |
||
| ) | ` [static, virtual]` |

Read a 3 float paramter from a buffer.

| bufferId | The buffer's ID. |
| parameter | The parameter to read. |
| v1 | The first value to read. |
| v2 | The second value to read. |
| v3 | The third value to read. |

| bool ALWrapper::getBuffer3i:parameter:v1:v2:v3: | ( | ALuint | bufferId, |
| [parameter] ALenum | parameter, |
||
| [v1] ALint* | v1, |
||
| [v2] ALint* | v2, |
||
| [v3] ALint* | v3 |
||
| ) | ` [static, virtual]` |

Read a 3 integer paramter from a buffer.

| bufferId | The buffer's ID. |
| parameter | The parameter to read. |
| v1 | The first value to read. |
| v2 | The second value to read. |
| v3 | The third value to read. |

| ALfloat ALWrapper::getBufferf:parameter: | ( | ALuint | bufferId, |
| [parameter] ALenum | parameter |
||
| ) | ` [static, virtual]` |

Read a float paramter from a buffer.

| bufferId | The buffer's ID. |
| parameter | The parameter to read. |

| bool ALWrapper::getBufferfv:parameter:values: | ( | ALuint | bufferId, |
| [parameter] ALenum | parameter, |
||
| [values] ALfloat* | values |
||
| ) | ` [static, virtual]` |

Read a float array paramter from a buffer.

| bufferId | The buffer's ID. |
| parameter | The parameter to read. |
| values | An array to store the values. |

| ALint ALWrapper::getBufferi:parameter: | ( | ALuint | bufferId, |
| [parameter] ALenum | parameter |
||
| ) | ` [static, virtual]` |

Read an integer paramter from a buffer.

| bufferId | The buffer's ID. |
| parameter | The parameter to read. |

| bool ALWrapper::getBufferiv:parameter:values: | ( | ALuint | bufferId, |
| [parameter] ALenum | parameter, |
||
| [values] ALint* | values |
||
| ) | ` [static, virtual]` |

Read an integer array paramter from a buffer.

| bufferId | The buffer's ID. |
| parameter | The parameter to read. |
| values | An array to store the values. |

| ALCdevice * ALWrapper::getContextsDevice: | ( | ALCcontext* | context | ) | ` [static, virtual]` |

Get the device a context was created from.

| context | The context. |

| ALCdevice * ALWrapper::getContextsDevice:deviceReference: | ( | ALCcontext* | context, |
| [deviceReference] ALCdevice* | deviceReference |
||
| ) | ` [static, virtual]` |

Get the device a context was created from, passing in a device reference for more informative logging info.

| context | The context. |
| deviceReference | The device reference to use when logging an error. |

| ALCcontext * ALWrapper::getCurrentContext | ( | ) | ` [static, virtual]` |

Get the current context.

| ALdouble ALWrapper::getDouble: | ( | ALenum | parameter | ) | ` [static, virtual]` |

Get a double parameter.

| parameter | The parameter to fetch. |

| bool ALWrapper::getDoublev:values: | ( | ALenum | parameter, |
| [values] ALdouble* | values |
||
| ) | ` [static, virtual]` |

Get a double array parameter.

| parameter | The parameter to fetch. |
| values | An array to hold the result. |

| ALenum ALWrapper::getEnumValue: | ( | NSString* | enumName | ) | ` [static, virtual]` |

Get the enum value from its name.

| enumName | the name of the enum value. |

| ALenum ALWrapper::getEnumValue:name: | ( | ALCdevice* | device, |
| [name] NSString* | enumName |
||
| ) | ` [static, virtual]` |

Get the enum value from its name.

| device | The device to check on. |
| enumName | the name of the enum value. |

| ALfloat ALWrapper::getFloat: | ( | ALenum | parameter | ) | ` [static, virtual]` |

Get a float parameter.

| parameter | The parameter to fetch. |

| bool ALWrapper::getFloatv:values: | ( | ALenum | parameter, |
| [values] ALfloat* | values |
||
| ) | ` [static, virtual]` |

Get a float array parameter.

| parameter | The parameter to fetch. |
| values | An array to hold the result. |

| ALint ALWrapper::getInteger: | ( | ALenum | parameter | ) | ` [static, virtual]` |

Get an integer parameter.

| parameter | The parameter to fetch. |

| ALint ALWrapper::getInteger:attribute: | ( | ALCdevice* | device, |
| [attribute] ALenum | attribute |
||
| ) | ` [static, virtual]` |

Get an integer attribute.

| device | The device to read the attribute from. |
| attribute | The attribute to fetch. |

| bool ALWrapper::getIntegerv:attribute:size:data: | ( | ALCdevice* | device, |
| [attribute] ALenum | attribute, |
||
| [size] ALsizei | size, |
||
| [data] ALCint* | data |
||
| ) | ` [static, virtual]` |

Get an integer array attribute.

| device | The device to read the attribute from. |
| attribute | The attribute to read. |
| size | the size of the receiving array. |
| data | An array to store the values. |

| bool ALWrapper::getIntegerv:values: | ( | ALenum | parameter, |
| [values] ALint* | values |
||
| ) | ` [static, virtual]` |

Get an integer array parameter.

| parameter | The parameter to fetch. |
| values | An array to hold the result. |

| bool ALWrapper::getListener3f:v1:v2:v3: | ( | ALenum | parameter, |
| [v1] ALfloat* | v1, |
||
| [v2] ALfloat* | v2, |
||
| [v3] ALfloat* | v3 |
||
| ) | ` [static, virtual]` |

Read a 3 float paramter from the current listener.

| parameter | The parameter to read. |
| v1 | The first value to read. |
| v2 | The second value to read. |
| v3 | The third value to read. |

| bool ALWrapper::getListener3i:v1:v2:v3: | ( | ALenum | parameter, |
| [v1] ALint* | v1, |
||
| [v2] ALint* | v2, |
||
| [v3] ALint* | v3 |
||
| ) | ` [static, virtual]` |

Read a 3 integer paramter from the current listener.

| parameter | The parameter to read. |
| v1 | The first value to read. |
| v2 | The second value to read. |
| v3 | The third value to read. |

| ALfloat ALWrapper::getListenerf: | ( | ALenum | parameter | ) | ` [static, virtual]` |

Read a float paramter from the current listener.

| parameter | The parameter to read. |

| bool ALWrapper::getListenerfv:values: | ( | ALenum | parameter, |
| [values] ALfloat* | values |
||
| ) | ` [static, virtual]` |

Read a float array paramter from the current listener.

| parameter | The parameter to read. |
| values | An array to store the values. |

| ALint ALWrapper::getListeneri: | ( | ALenum | parameter | ) | ` [static, virtual]` |

Read an integer paramter from the current listener.

| parameter | The parameter to read. |

| bool ALWrapper::getListeneriv:values: | ( | ALenum | parameter, |
| [values] ALint* | values |
||
| ) | ` [static, virtual]` |

Read an integer array paramter from the current listener.

| parameter | The parameter to read. |
| values | An array to store the values. |

| ALdouble ALWrapper::getMixerOutputDataRate | ( | ) | ` [static, virtual]` |

Get the iOS device's mixer outut data rate.

| NSArray * ALWrapper::getNullSeparatedStringList: | ( | ALenum | parameter | ) | ` [static, virtual]` |

Get a string list parameter.

Use this method for OpenAL parameters that return a null separated list.

| parameter | The parameter to fetch. |

| NSArray * ALWrapper::getNullSeparatedStringList:attribute: | ( | ALCdevice* | device, |
| [attribute] ALenum | attribute |
||
| ) | ` [static, virtual]` |

Get a string list attribute.

Use this method for OpenAL attributes that return a null separated list.

| device | The device to read the attribute from. |
| attribute | The attribute to fetch. |

| void * ALWrapper::getProcAddress: | ( | NSString* | functionName | ) | ` [static, virtual]` |

Get the address of a procedure.

| functionName | The name of the procedure to fetch. |

| void * ALWrapper::getProcAddress:name: | ( | ALCdevice* | device, |
| [name] NSString* | functionName |
||
| ) | ` [static, virtual]` |

Get the address of a procedure for a device.

| device | The device to check on. |
| functionName | The name of the procedure to check for. |

| bool ALWrapper::getSource3f:parameter:v1:v2:v3: | ( | ALuint | sourceId, |
| [parameter] ALenum | parameter, |
||
| [v1] ALfloat* | v1, |
||
| [v2] ALfloat* | v2, |
||
| [v3] ALfloat* | v3 |
||
| ) | ` [static, virtual]` |

Read a 3 float paramter from a source.

| sourceId | The source's ID. |
| parameter | The parameter to read. |
| v1 | The first value to read. |
| v2 | The second value to read. |
| v3 | The third value to read. |

| bool ALWrapper::getSource3i:parameter:v1:v2:v3: | ( | ALuint | sourceId, |
| [parameter] ALenum | parameter, |
||
| [v1] ALint* | v1, |
||
| [v2] ALint* | v2, |
||
| [v3] ALint* | v3 |
||
| ) | ` [static, virtual]` |

Read a 3 integer paramter from a source.

| sourceId | The source's ID. |
| parameter | The parameter to read. |
| v1 | The first value to read. |
| v2 | The second value to read. |
| v3 | The third value to read. |

| ALfloat ALWrapper::getSourcef:parameter: | ( | ALuint | sourceId, |
| [parameter] ALenum | parameter |
||
| ) | ` [static, virtual]` |

Read a float paramter from a source.

| sourceId | The source's ID. |
| parameter | The parameter to read. |

| bool ALWrapper::getSourcefv:parameter:values: | ( | ALuint | sourceId, |
| [parameter] ALenum | parameter, |
||
| [values] ALfloat* | values |
||
| ) | ` [static, virtual]` |

Read a float array paramter from a source.

| sourceId | The source's ID. |
| parameter | The parameter to read. |
| values | An array to store the values. |

| ALint ALWrapper::getSourcei:parameter: | ( | ALuint | sourceId, |
| [parameter] ALenum | parameter |
||
| ) | ` [static, virtual]` |

Read an integer paramter from a source.

| sourceId | The source's ID. |
| parameter | The parameter to read. |

| bool ALWrapper::getSourceiv:parameter:values: | ( | ALuint | sourceId, |
| [parameter] ALenum | parameter, |
||
| [values] ALint* | values |
||
| ) | ` [static, virtual]` |

Read an integer array paramter from a source.

| sourceId | The source's ID. |
| parameter | The parameter to read. |
| values | An array to store the values. |

| NSArray * ALWrapper::getSpaceSeparatedStringList: | ( | ALenum | parameter | ) | ` [static, virtual]` |

Get a string list parameter.

Use this method for OpenAL parameters that return a space separated list.

| parameter | The parameter to fetch. |

| NSArray * ALWrapper::getSpaceSeparatedStringList:attribute: | ( | ALCdevice* | device, |
| [attribute] ALenum | attribute |
||
| ) | ` [static, virtual]` |

Get a string list attribute.

Use this method for OpenAL attributes that return a space separated list.

| device | The device to read the attribute from. |
| attribute | The attribute to fetch. |

| NSString * ALWrapper::getString: | ( | ALenum | parameter | ) | ` [static, virtual]` |

Get a string parameter.

| parameter | The parameter to fetch. |

| NSString * ALWrapper::getString:attribute: | ( | ALCdevice* | device, |
| [attribute] ALenum | attribute |
||
| ) | ` [static, virtual]` |

Get a string attribute.

| device | The device to read the attribute from. |
| attribute | The attribute to fetch. |

| bool ALWrapper::isBuffer: | ( | ALuint | bufferId | ) | ` [static, virtual]` |

Check if the speified buffer exists.

| bufferId | The ID of the buffer to query. |

| bool ALWrapper::isEnabled: | ( | ALenum | capability | ) | ` [static, virtual]` |

Check if a capability is enabled.

| capability | The capability to check. |

| bool ALWrapper::isExtensionPresent: | ( | NSString* | extensionName | ) | ` [static, virtual]` |

Check if an extension is present.

| extensionName | The name of the extension to check. |

| bool ALWrapper::isExtensionPresent:name: | ( | ALCdevice* | device, |
| [name] NSString* | extensionName |
||
| ) | ` [static, virtual]` |

Check if an extension is present on a device.

| device | The device to check for an extension on. |
| extensionName | The name of the extension to check for. |

| bool ALWrapper::isSource: | ( | ALuint | sourceId | ) | ` [static, virtual]` |

Check if the speified source exists.

| sourceId | The ID of the source to query. |

| bool ALWrapper::listener3f:v1:v2:v3: | ( | ALenum | parameter, |
| [v1] ALfloat | v1, |
||
| [v2] ALfloat | v2, |
||
| [v3] ALfloat | v3 |
||
| ) | ` [static, virtual]` |

Write a 3 float paramter to the current listener.

| parameter | the parameter to write to. |
| v1 | The first value to write. |
| v2 | The second value to write. |
| v3 | The third value to write. |

| bool ALWrapper::listener3i:v1:v2:v3: | ( | ALenum | parameter, |
| [v1] ALint | v1, |
||
| [v2] ALint | v2, |
||
| [v3] ALint | v3 |
||
| ) | ` [static, virtual]` |

Write a 3 integer paramter to the current listener.

| parameter | The parameter to write to. |
| v1 | The first value to write. |
| v2 | The second value to write. |
| v3 | The third value to write. |

| bool ALWrapper::listenerf:value: | ( | ALenum | parameter, |
| [value] ALfloat | value |
||
| ) | ` [static, virtual]` |

Write a float paramter to the current listener.

| parameter | The parameter to write to. |
| value | The value to write. |

| bool ALWrapper::listenerfv:values: | ( | ALenum | parameter, |
| [values] ALfloat* | values |
||
| ) | ` [static, virtual]` |

Write a float array paramter to the current listener.

| parameter | The parameter to write to. |
| values | The values to write. |

| bool ALWrapper::listeneri:value: | ( | ALenum | parameter, |
| [value] ALint | value |
||
| ) | ` [static, virtual]` |

Write an integer paramter to the current listener.

| parameter | The parameter to write to. |
| value | The value to write. |

| bool ALWrapper::listeneriv:values: | ( | ALenum | parameter, |
| [values] ALint* | values |
||
| ) | ` [static, virtual]` |

Write an integer array paramter to the current listener.

| parameter | The parameter to write to. |
| values | The values to write. |

| bool ALWrapper::makeContextCurrent: | ( | ALCcontext* | context | ) | ` [static, virtual]` |

Make the specified context the current context.

| context | the context to make current. |

| bool ALWrapper::makeContextCurrent:deviceReference: | ( | ALCcontext* | context, |
| [deviceReference] ALCdevice* | deviceReference |
||
| ) | ` [static, virtual]` |

Make the specified context the current context, passing in a device reference for more informative logging info.

| context | The context to make current. |
| deviceReference | The device reference to use when logging an error. |

| ALCdevice * ALWrapper::openCaptureDevice:frequency:format:bufferSize: | ( | NSString* | deviceName, |
| [frequency] ALCuint | frequency, |
||
| [format] ALCenum | format, |
||
| [bufferSize] ALCsizei | bufferSize |
||
| ) | ` [static, virtual]` |

*UNSUPPORTED ON IOS* Open an audio capture device.

| deviceName | The name of the device to open (nil = open the default device). |
| frequency | The sampling frequency to use. |
| format | The format to capture the data as. |
| bufferSize | The size of capture buffer to use. |

| ALCdevice * ALWrapper::openDevice: | ( | NSString* | deviceName | ) | ` [static, virtual]` |

Open a device.

| deviceName | The name of the device to open (nil = open the default device). |

| void ALWrapper::processContext: | ( | ALCcontext* | context | ) | ` [static, virtual]` |

Process a context.

| context | The contect to process. |

| void ALWrapper::setMixerOutputDataRate: | ( | ALdouble | frequency | ) | ` [static, virtual]` |

Set the iOS device's mixer output data rate.

| frequency | The output data rate (frequency). |

| bool ALWrapper::source3f:parameter:v1:v2:v3: | ( | ALuint | sourceId, |
| [parameter] ALenum | parameter, |
||
| [v1] ALfloat | v1, |
||
| [v2] ALfloat | v2, |
||
| [v3] ALfloat | v3 |
||
| ) | ` [static, virtual]` |

Write a 3 float paramter to a source.

| sourceId | The source's ID. |
| parameter | the parameter to write to. |
| v1 | The first value to write. |
| v2 | The second value to write. |
| v3 | The third value to write. |

| bool ALWrapper::source3i:parameter:v1:v2:v3: | ( | ALuint | sourceId, |
| [parameter] ALenum | parameter, |
||
| [v1] ALint | v1, |
||
| [v2] ALint | v2, |
||
| [v3] ALint | v3 |
||
| ) | ` [static, virtual]` |

Write a 3 integer paramter to a source.

| sourceId | The source's ID. |
| parameter | The parameter to write to. |
| v1 | The first value to write. |
| v2 | The second value to write. |
| v3 | The third value to write. |

| bool ALWrapper::sourcef:parameter:value: | ( | ALuint | sourceId, |
| [parameter] ALenum | parameter, |
||
| [value] ALfloat | value |
||
| ) | ` [static, virtual]` |

Write a float paramter to a source.

| sourceId | The source's ID. |
| parameter | The parameter to write to. |
| value | The value to write. |

| bool ALWrapper::sourcefv:parameter:values: | ( | ALuint | sourceId, |
| [parameter] ALenum | parameter, |
||
| [values] ALfloat* | values |
||
| ) | ` [static, virtual]` |

Write a float array paramter to a source.

| sourceId | The source's ID. |
| parameter | The parameter to write to. |
| values | The values to write. |

| bool ALWrapper::sourcei:parameter:value: | ( | ALuint | sourceId, |
| [parameter] ALenum | parameter, |
||
| [value] ALint | value |
||
| ) | ` [static, virtual]` |

Write an integer paramter to a source.

| sourceId | The source's ID. |
| parameter | The parameter to write to. |
| value | The value to write. |

| bool ALWrapper::sourceiv:parameter:values: | ( | ALuint | sourceId, |
| [parameter] ALenum | parameter, |
||
| [values] ALint* | values |
||
| ) | ` [static, virtual]` |

Write an integer array paramter to a source.

| sourceId | The source's ID. |
| parameter | The parameter to write to. |
| values | The values to write. |

| bool ALWrapper::sourcePause: | ( | ALuint | sourceId | ) | ` [static, virtual]` |

Pause a source.

| sourceId | The ID of the source to pause. |

| bool ALWrapper::sourcePausev:numSources: | ( | ALuint* | sourceIds, |
| [numSources] ALsizei | numSources |
||
| ) | ` [static, virtual]` |

Pause a bunch of sources.

| sourceIds | The sources to pause. |
| numSources | The number of sources in sourceIds. |

| bool ALWrapper::sourcePlay: | ( | ALuint | sourceId | ) | ` [static, virtual]` |

Play a source.

| sourceId | The ID of the source to play. |

| bool ALWrapper::sourcePlayv:numSources: | ( | ALuint* | sourceIds, |
| [numSources] ALsizei | numSources |
||
| ) | ` [static, virtual]` |

Play a bunch of sources.

| sourceIds | The sources to play. |
| numSources | The number of sources in sourceIds. |

| bool ALWrapper::sourceQueueBuffers:numBuffers:bufferIds: | ( | ALuint | sourceId, |
| [numBuffers] ALsizei | numBuffers, |
||
| [bufferIds] ALuint* | bufferIds |
||
| ) | ` [static, virtual]` |

Queue buffers into a source for sequential playback.

| sourceId | The source to use for playback. |
| numBuffers | The number of buffers to queue. |
| bufferIds | The IDs of the buffers to queue. |

| bool ALWrapper::sourceRewind: | ( | ALuint | sourceId | ) | ` [static, virtual]` |

Rewind a source.

| sourceId | The ID of the source to rewind. |

| bool ALWrapper::sourceRewindv:numSources: | ( | ALuint* | sourceIds, |
| [numSources] ALsizei | numSources |
||
| ) | ` [static, virtual]` |

Rewind a bunch of sources.

| sourceIds | The sources to rewind. |
| numSources | The number of sources in sourceIds. |

| bool ALWrapper::sourceStop: | ( | ALuint | sourceId | ) | ` [static, virtual]` |

Stop a source.

| sourceId | The ID of the source to stop. |

| bool ALWrapper::sourceStopv:numSources: | ( | ALuint* | sourceIds, |
| [numSources] ALsizei | numSources |
||
| ) | ` [static, virtual]` |

Stop a bunch of sources.

| sourceIds | The sources to stop. |
| numSources | The number of sources in sourceIds. |

| bool ALWrapper::sourceUnqueueBuffers:numBuffers:bufferIds: | ( | ALuint | sourceId, |
| [numBuffers] ALsizei | numBuffers, |
||
| [bufferIds] ALuint* | bufferIds |
||
| ) | ` [static, virtual]` |

Unqueue previously queued buffers.

| sourceId | The source the buffers were previously queued in. |
| numBuffers | The number of buffers to unqueue. |
| bufferIds | The IDs of the buffers to unqueue. |

| bool ALWrapper::speedOfSound: | ( | ALfloat | value | ) | ` [static, virtual]` |

Set the speed of sound.

| value | The value to set. |

| bool ALWrapper::startCapture: | ( | ALCdevice* | device | ) | ` [static, virtual]` |

Start capturing audio data.

| device | The device to capture on. |

| bool ALWrapper::stopCapture: | ( | ALCdevice* | device | ) | ` [static, virtual]` |

Stop capturing audio data.

| device | The device capturing audio data. |

| void ALWrapper::suspendContext: | ( | ALCcontext* | context | ) | ` [static, virtual]` |

Suspend a context.

| context | The contect to suspend. |