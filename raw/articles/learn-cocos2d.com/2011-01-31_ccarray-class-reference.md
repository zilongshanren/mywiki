---
title: CCArray Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_array/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`

[CCArray.h](http://www.learn-cocos2d.com/)"

| (void) | -
|

A faster alternative of NSArray. [CCArray](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_array/) uses internally a c-array.

| - (void) addObject: | (id) | object |

undocumented

| - (void) addObjectsFromNSArray: | (NSArray *) | otherArray |

undocumented

| + (id) array |

undocumented

| + (id) arrayWithCapacity: | (NSUInteger) | capacity |

undocumented

| + (id) arrayWithNSArray: | (NSArray *) | otherArray |

undocumented

| - (NSUInteger) capacity |

undocumented

| - (BOOL) containsObject: | (id) | object |

undocumented

| - (NSUInteger) count |

undocumented

| - (void) fastRemoveObject: | (id) | object |

undocumented

| - (void) fastRemoveObjectAtIndex: | (NSUInteger) | index |

undocumented

| - (NSArray*) getNSArray |

undocumented

| - (NSUInteger) indexOfObject: | (id) | object |

undocumented

| - (id) initWithCapacity: | (NSUInteger) | capacity |

undocumented

| - (id) initWithNSArray: | (NSArray *) | otherArray |

undocumented

| - (void) insertObject: | (id) | object |
||
| atIndex: | (NSUInteger) | index | ||

undocumented

| - (id) lastObject |

undocumented

| - (void) makeObjectsPerformSelector: | (SEL) | aSelector |

undocumented

| - (void) makeObjectsPerformSelector: | (SEL) | aSelector |
||
| withObject: | (id) | object | ||

undocumented

| - (id) objectAtIndex: | (NSUInteger) | index |

undocumented

| - (id) randomObject |

undocumented

| - (void) removeAllObjects |

undocumented

| - (void) removeLastObject |

undocumented

| - (void) removeObject: | (id) | object |

undocumented

| - (void) removeObjectAtIndex: | (NSUInteger) | index |

undocumented