---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c_array_07_c_c3_08/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CC3Foundation.h>`


| void |
|

Extension category to support cocos3d functionality.

This extension includes a number of methods that add or remove objects to and from the array without retaining and releasing them. These methods are identified by the word Unretained in their names, and are faster than their standard equivalent methods that do retain and release objects.

It is critical that use of these methods is consistent for any object added. If an object is added using an "Unretained" method, then it must be removed using an "Unretained" method.

| void CCArray(CC3)::addUnretainedObject: | ( | id | anObject | ) | ` [virtual]` |

Adds the specified object to the end of the array, but does not retain the object.

When removing the object, it must not be released. Use one the removeUnretainedObject... methods to remove the object.

| NSString* CCArray(CC3)::fullDescription | ( | ) | ` [virtual]` |

Returns a more detailed description of this instance.

| NSUInteger CCArray(CC3)::indexOfObjectIdenticalTo: | ( | id | anObject | ) | ` [virtual]` |

Returns the index of the specified object, by comparing objects using the == operator.

| void CCArray(CC3)::insertUnretainedObject:atIndex: | ( | id | anObject, |
| [atIndex] NSUInteger | index |
||
| ) | ` [virtual]` |

Inserts the specified object at the specified index within the array, but does not retain the object.

The elements in the array after the specified index position are shuffled up to make room for the new object.

When removing the object, it must not be released. Use one the removeUnretainedObject... methods to remove the object.

| void CCArray(CC3)::releaseAsUnretained | ( | ) | ` [virtual]` |

Releases the array without releasing each contained object.

All contained objects must not have been retained when added to the array.

| void CCArray(CC3)::removeAllObjectsAsUnretained | ( | ) | ` [virtual]` |

Removes all objects in the array, without releasing them.

All objects being removed must not have been retained when added to the array.

| void CCArray(CC3)::removeObjectIdenticalTo: | ( | id | anObject | ) | ` [virtual]` |

Removes the specified object, by comparing objects using the == operator.

| void CCArray(CC3)::removeUnretainedObjectAtIndex: | ( | NSUInteger | index | ) | ` [virtual]` |

Removes the object at the specified index, without releasing it.

The objects after this object in the array are shuffled down to fill in the gap.

The object being removed must not have been retained when added to the array.

| void CCArray(CC3)::removeUnretainedObjectIdenticalTo: | ( | id | anObject | ) | ` [virtual]` |

Removes the specified object from the array, without releasing it, by comparing objects using the == operator.

The objects after this object in the array are shuffled down to fill in the gap.

The object being removed must not have been retained when added to the array.

| void CCArray(CC3)::replaceObjectAtIndex:withObject: | ( | NSUInteger | index, |
| [withObject] id | anObject |
||
| ) | ` [virtual]` |

Replaces the object at the specified index with the specified object.