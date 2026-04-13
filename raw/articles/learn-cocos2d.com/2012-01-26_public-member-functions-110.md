---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_array/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCArray.h>`



[List of all members.](/)

Public Member Functions
|
id | **initWithCapacity:** (NSUInteger capacity) |
id | **initWithArray:** ([CCArray](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_array/) *otherArray) |
id | **initWithNSArray:** (NSArray *otherArray) |
NSUInteger | **count** () |
NSUInteger | **capacity** () |
NSUInteger | **indexOfObject:** (id object) |
id | **objectAtIndex:** (NSUInteger index) |
BOOL | **containsObject:** (id object) |
id | **randomObject** () |
id | **lastObject** () |
NSArray * | **getNSArray** () |
void | **addObject:** (id object) |
void | **addObjectsFromArray:** ([CCArray](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_array/) *otherArray) |
void | **addObjectsFromNSArray:** (NSArray *otherArray) |
void | **insertObject:atIndex:** (id object,[atIndex] NSUInteger index) |
void | **removeLastObject** () |
void | **removeObject:** (id object) |
void | **removeObjectAtIndex:** (NSUInteger index) |
void | **removeObjectsInArray:** ([CCArray](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_array/) *otherArray) |
void | **removeAllObjects** () |
void | **fastRemoveObject:** (id object) |
void | **fastRemoveObjectAtIndex:** (NSUInteger index) |
void | **exchangeObject:withObject:** (id object1,[withObject] id object2) |
void | **exchangeObjectAtIndex:withObjectAtIndex:** (NSUInteger index1,[withObjectAtIndex] NSUInteger index2) |
void | **reverseObjects** () |
void | **reduceMemoryFootprint** () |
void | **makeObjectsPerformSelector:** (SEL aSelector) |
void | **makeObjectsPerformSelector:withObject:** (SEL aSelector,[withObject] id object) |
Static Public Member Functions
|
id | **array** () |
id | **arrayWithCapacity:** (NSUInteger capacity) |
id | **arrayWithArray:** ([CCArray](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_array/) *otherArray) |
id | **arrayWithNSArray:** (NSArray *otherArray) |
Public Attributes
|
[ccArray](../../../../../api-ref/1.0/cocos2d-iphone/html/structcc_array/) * | **data** |


## Detailed Description

A faster alternative of NSArray. [CCArray](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_array/) uses internally a c-array.

**Since:**- v0.99.4


The documentation for this interface was generated from the following file: