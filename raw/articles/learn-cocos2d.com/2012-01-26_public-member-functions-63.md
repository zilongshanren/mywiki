---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/CocosDenshion/html/interface_c_d_buffer_manager/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CDAudioManager.h>`



[List of all members.](../../../../../api-ref/1.0/CocosDenshion/html/interface_c_d_buffer_manager-members/)

Public Member Functions
|
id | **initWithEngine:** ([CDSoundEngine](../../../../../api-ref/1.0/CocosDenshion/html/interface_c_d_sound_engine/) *theSoundEngine) |
int | **bufferForFile:create:** (NSString *filePath,[create] BOOL create) |
void | **releaseBufferForFile:** (NSString *filePath) |
Protected Attributes
|
NSMutableDictionary * | **loadedBuffers** |
NSMutableArray * | **freedBuffers** |
[CDSoundEngine](../../../../../api-ref/1.0/CocosDenshion/html/interface_c_d_sound_engine/) * | **soundEngine** |
int | **nextBufferId** |


## Detailed Description

Allows buffers to be associated with file names


The documentation for this interface was generated from the following file: