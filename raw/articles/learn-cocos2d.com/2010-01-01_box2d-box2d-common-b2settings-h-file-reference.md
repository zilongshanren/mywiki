---
title: Box2D/Box2D/Common/b2Settings.h File Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/b2_settings_8h/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# Box2D/Box2D/Common/b2Settings.h File Reference

`#include <cassert>`

`#include <cmath>`

[Go to the source code of this file.](/)


## Detailed Description

Global tuning constants based on meters-kilograms-seconds (MKS) units.


## Define Documentation

| #define b2_aabbExtension 0.1f |

This is used to fatten AABBs in the dynamic tree. This allows proxies to move by a small amount without triggering a tree adjustment. This is in meters.

| #define b2_aabbMultiplier 2.0f |

This is used to fatten AABBs in the dynamic tree. This is used to predict the future position based on the current displacement. This is a dimensionless multiplier.

| #define b2_angularSleepTolerance (2.0f / 180.0f * b2_pi) |

A body cannot sleep if its angular velocity is above this tolerance.

| #define b2_angularSlop (2.0f / 180.0f * b2_pi) |

A small angle used as a collision and constraint tolerance. Usually it is chosen to be numerically significant, but visually insignificant.

| #define b2_contactBaumgarte 0.2f |

This scale factor controls how fast overlap is resolved. Ideally this would be 1 so that overlap is removed in one time step. However using values close to 1 often lead to overshoot.

| #define b2_epsilon FLT_EPSILON |


| #define b2_linearSleepTolerance 0.01f |

A body cannot sleep if its linear velocity is above this tolerance.

| #define b2_linearSlop 0.005f |

A small length used as a collision and constraint tolerance. Usually it is chosen to be numerically significant, but visually insignificant.

| #define b2_maxAngularCorrection (8.0f / 180.0f * b2_pi) |

The maximum angular position correction used when solving constraints. This helps to prevent overshoot.

| #define b2_maxFloat FLT_MAX |


| #define b2_maxLinearCorrection 0.2f |

The maximum linear position correction used when solving constraints. This helps to prevent overshoot.

| #define b2_maxManifoldPoints 2 |

The maximum number of contact points between two convex shapes.

| #define b2_maxPolygonVertices 8 |

The maximum number of vertices on a convex polygon.

| #define b2_maxRotation (0.5f * b2_pi) |

The maximum angular velocity of a body. This limit is very large and is used to prevent numerical problems. You shouldn't need to adjust this.

| #define b2_maxRotationSquared (b2_maxRotation * b2_maxRotation) |


| #define b2_maxTOIContacts 32 |

Maximum number of contacts to be handled to solve a TOI impact.

| #define b2_maxTranslation 2.0f |

The maximum linear velocity of a body. This limit is very large and is used to prevent numerical problems. You shouldn't need to adjust this.

| #define b2_maxTranslationSquared (b2_maxTranslation * b2_maxTranslation) |


| #define B2_NOT_USED |
( |
x |
|
) |
((void)(x)) |


| #define b2_pi 3.14159265359f |


| #define b2_polygonRadius (2.0f * b2_linearSlop) |

The radius of the polygon/edge shape skin. This should not be modified. Making this smaller means polygons will have an insufficient buffer for continuous collision. Making it larger may create artifacts for vertex collision.

| #define b2_timeToSleep 0.5f |

The time that a body must be still before it will go to sleep.

| #define b2_velocityThreshold 1.0f |

A velocity threshold for elastic collisions. Any collision with a relative linear velocity below this threshold will be treated as inelastic.

| #define b2Assert |
( |
A |
|
) |
assert(A) |



## Typedef Documentation

typedef signed short [int16](../../../box2d-api-reference/API/b2_settings_8h/#a259fa4834387bd68627ddf37bb3ebdb9) |


typedef unsigned char [uint8](../../../box2d-api-reference/API/b2_settings_8h/#adde6aaee8457bee49c2a92621fe22b79) |



## Function Documentation

| void* b2Alloc |
( |
[int32](../../../box2d-api-reference/API/b2_settings_8h/#a43d43196463bde49cb067f5c20ab8481) |
*size* |
) |
|

Implement this function to use your own memory allocator.

| void b2Free |
( |
void * |
*mem* |
) |
|

If you implement b2Alloc, you should also implement this function.

Friction mixing law. Feel free to customize this.

Restitution mixing law. Feel free to customize this.


## Variable Documentation