---
title: Instance Methods
url: http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_array/
published: '2013-01-09'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
(id) | - **initWithCapacity:** |
| |
(id) | - **initWithArray:** |
| |
(id) | - **initWithNSArray:** |
| |
(NSUInteger) | - **count** |
| |
(NSUInteger) | - **capacity** |
| |
(NSUInteger) | - **indexOfObject:** |
| |
(id) | - **objectAtIndex:** |
| |
(BOOL) | - **containsObject:** |
| |
(id) | - **randomObject** |
| |
(id) | - **lastObject** |
| |
(NSArray *) | - **getNSArray** |
| |
| (BOOL) | - [isEqualToArray:](../../../../../../api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_array/#a9cae7aa95a0541c96e08e2ee4a051cf0) |
| |
(void) | - **addObject:** |
| |
(void) | - **addObjectsFromArray:** |
| |
(void) | - **addObjectsFromNSArray:** |
| |
(void) | - **insertObject:atIndex:** |
| |
(void) | - **removeLastObject** |
| |
(void) | - **removeObject:** |
| |
(void) | - **removeObjectAtIndex:** |
| |
(void) | - **removeObjectsInArray:** |
| |
(void) | - **removeAllObjects** |
| |
(void) | - **fastRemoveObject:** |
| |
(void) | - **fastRemoveObjectAtIndex:** |
| |
(void) | - **exchangeObject:withObject:** |
| |
(void) | - **exchangeObjectAtIndex:withObjectAtIndex:** |
| |
| (void) | - [replaceObjectAtIndex:withObject:](../../../../../../api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_array/#a41929aff19adb31bb00bb288b70468d6) |
| |
(void) | - **reverseObjects** |
| |
(void) | - **reduceMemoryFootprint** |
| |
| (void) | - [qsortUsingCFuncComparator:](../../../../../../api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_array/#acf489832279df62d4052561505cad696) |
| |
(void) | - **insertionSortUsingCFuncComparator:** |
| |
(void) | - **mergesortLUsingCFuncComparator:** |
| |
(void) | - **insertionSort:** |
| |
(void) | - **sortUsingFunction:context:** |
| |
(void) | - **makeObjectsPerformSelector:** |
| |
(void) | - **makeObjectsPerformSelector:withObject:** |
| |
| (void) | - [makeObjectPerformSelectorWithArrayObjects:selector:](../../../../../../api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_array/#a62fe0aecfe4e90d6f523cf892aedd867) |
| |

|
(id) | + **array** |
| |
(id) | + **arrayWithCapacity:** |
| |
(id) | + **arrayWithArray:** |
| |
(id) | + **arrayWithNSArray:** |
| |

| - (BOOL) isEqualToArray: |
|
([CCArray](../../../../../../api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_array/) *) |
*otherArray* |
|

| - (void) makeObjectPerformSelectorWithArrayObjects: |
|
(id) |
*object* |
| selector: |
|
(SEL) |
*aSelector* |
|
|
| |

| - (void) qsortUsingCFuncComparator: |
|
(const void *) |
|
|
|
(const void *) |
*comparator* |
|
|
| |

| - (void) replaceObjectAtIndex: |
|
(NSUInteger) |
*index* |
| withObject: |
|
(id) |
*anObject* |
|
|
| |


The documentation for this class was generated from the following file: