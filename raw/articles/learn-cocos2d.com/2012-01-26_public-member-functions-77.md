---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_a_l_sound_source_pool/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

A pool of sound sources, which can be fetched based on availability.
[More...](../../../../../api-ref/1.0/ObjectAL/html/interface_a_l_sound_source_pool/#details)

`#include <ALSoundSourcePool.h>`



[List of all members.](../../../../../api-ref/1.0/ObjectAL/html/class_a_l_sound_source_pool-members/)

Public Member Functions
|
| void | [addSource:](../../../../../api-ref/1.0/ObjectAL/html/interface_a_l_sound_source_pool/#a868049b186178b0c4f8df2853f63bc1b) (id< [ALSoundSource](../../../../../api-ref/1.0/ObjectAL/html/protocol_a_l_sound_source-p/) > source) |
| | Add a source to this pool.
|
| void | [removeSource:](../../../../../api-ref/1.0/ObjectAL/html/interface_a_l_sound_source_pool/#af6ff07f8c07c13da3f5c8fd15e06e921) (id< [ALSoundSource](../../../../../api-ref/1.0/ObjectAL/html/protocol_a_l_sound_source-p/) > source) |
| | Remove a source from this pool.
|
id< [ALSoundSource](../../../../../api-ref/1.0/ObjectAL/html/protocol_a_l_sound_source-p/) > | [getFreeSource:](../../../../../api-ref/1.0/ObjectAL/html/interface_a_l_sound_source_pool/#a5389ccb1f1826702087a5f1955f32f2b) (bool attemptToInterrupt) |
| | Acquire a free or freeable source from this pool.
|
Static Public Member Functions
|
| id | [pool](../../../../../api-ref/1.0/ObjectAL/html/interface_a_l_sound_source_pool/#aa84462a4e203ce5077e78b84b0ef74fc) () |
| | Make a new pool.
|
Protected Attributes
|
| NSMutableArray * | [sources](../../../../../api-ref/1.0/ObjectAL/html/interface_a_l_sound_source_pool/#ac905cc798792e5509a3f2f40ddd80965) |
| | All sources managed by this pool (id<ALSoundSource>).
|
Properties
|
| NSArray * | [sources](../../../../../api-ref/1.0/ObjectAL/html/interface_a_l_sound_source_pool/#a533cf92c6b69a01f313ef9895e3e42d0) |
| | All sources managed by this pool (id<ALSoundSource>).
|


## Detailed Description

A pool of sound sources, which can be fetched based on availability.


## Member Function Documentation

| void ALSoundSourcePool::addSource: |
( |
id<[ALSoundSource](../../../../../api-ref/1.0/ObjectAL/html/protocol_a_l_sound_source-p/)> |
*source* | ) |
` [virtual]` |

Add a source to this pool.

**Parameters:**-

id< [ALSoundSource](../../../../../api-ref/1.0/ObjectAL/html/protocol_a_l_sound_source-p/) > ALSoundSourcePool::getFreeSource: |
( |
bool |
*attemptToInterrupt* | ) |
` [virtual]` |

Acquire a free or freeable source from this pool.

It first attempts to find a completely free source. Failing this, it will attempt to interrupt a source and return that (if attemptToInterrupt is TRUE).

**Parameters:**-
| attemptToInterrupt | If TRUE, attempt to interrupt sources to free them for use. |


**Returns:**- The freed sound source, or nil if no sources are freeable.

| id ALSoundSourcePool::pool |
( |
| ) |
` [static, virtual]` |

Make a new pool.

**Returns:**- A new pool.

| void ALSoundSourcePool::removeSource: |
( |
id<[ALSoundSource](../../../../../api-ref/1.0/ObjectAL/html/protocol_a_l_sound_source-p/)> |
*source* | ) |
` [virtual]` |

Remove a source from this pool.

**Parameters:**-
| source | The source to remove. |



## Member Data Documentation

All sources managed by this pool (id<ALSoundSource>).


## Property Documentation

All sources managed by this pool (id<ALSoundSource>).


The documentation for this class was generated from the following files:

- ALSoundSourcePool.h
- ALSoundSourcePool.m