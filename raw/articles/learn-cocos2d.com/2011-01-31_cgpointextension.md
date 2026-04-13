---
title: CGPointExtension
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/group___c_g_point_extension/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

| file |
|

| #define ccp | ( | __X__, | ||
| __Y__ | ||||
| ) | CGPointMake(__X__,__Y__) |

Helper macro that creates a CGPoint

| static CGPoint ccpAdd | ( | const CGPoint | v1, |
|
| const CGPoint | v2 | |||
| ) | ` [inline, static]` |

Calculates sum of two points.

| float ccpAngle | ( | CGPoint | a, |
|
| CGPoint | b | |||
| ) |

| float ccpAngleSigned | ( | CGPoint | a, |
|
| CGPoint | b | |||
| ) |

| CGPoint ccpClamp | ( | CGPoint | p, |
|
| CGPoint | from, |
|||
| CGPoint | to | |||
| ) |

Clamp a point between from and to.

| CGPoint ccpCompMult | ( | CGPoint | a, |
|
| CGPoint | b | |||
| ) |

Multiplies a nd b components, a.x*b.x, a.y*b.y

| CGPoint ccpCompOp | ( | CGPoint | p, |
|
| float(*)(float) | opFunc | |||
| ) |

Run a math operation function on each point component absf, fllorf, ceilf, roundf any function that has the signature: float func(float); For example: let's try to take the floor of x,y ccpCompOp(p,floorf);

| static CGFloat ccpCross | ( | const CGPoint | v1, |
|
| const CGPoint | v2 | |||
| ) | ` [inline, static]` |

Calculates cross product of two points.

| CGFloat ccpDistance | ( | const CGPoint | v1, |
|
| const CGPoint | v2 | |||
| ) |

Calculates the distance between two points

| static CGFloat ccpDot | ( | const CGPoint | v1, |
|
| const CGPoint | v2 | |||
| ) | ` [inline, static]` |

Calculates dot product of two points.

| CGPoint ccpForAngle | ( | const CGFloat | a |
) |

Converts radians to a normalized vector.

| CGPoint ccpFromSize | ( | CGSize | s |
) |

Quickly convert CGSize to a CGPoint

| BOOL ccpFuzzyEqual | ( | CGPoint | a, |
|
| CGPoint | b, |
|||
| float | variance | |||
| ) |

| CGFloat ccpLength | ( | const CGPoint | v |
) |

Calculates distance between point an origin

| static CGFloat ccpLengthSQ | ( | const CGPoint | v |
) | ` [inline, static]` |

Calculates the square length of a CGPoint (not calling sqrt() )

| CGPoint ccpLerp | ( | CGPoint | a, |
|
| CGPoint | b, |
|||
| float | alpha | |||
| ) |

Linear Interpolation between two points a and b

| BOOL ccpLineIntersect | ( | CGPoint | p1, |
|
| CGPoint | p2, |
|||
| CGPoint | p3, |
|||
| CGPoint | p4, |
|||
| float * | s, |
|||
| float * | t | |||
| ) |

A general line-line intersection test

p1 | is the startpoint for the first line P1 = (p1 - p2) | |
p2 | is the endpoint for the first line P1 = (p1 - p2) | |
p3 | is the startpoint for the second line P2 = (p3 - p4) | |
p4 | is the endpoint for the second line P2 = (p3 - p4) | |
s | is the range for a hitpoint in P1 (pa = p1 + s*(p2 - p1)) | |
t | is the range for a hitpoint in P3 (pa = p2 + t*(p4 - p3)) |

| static CGPoint ccpMidpoint | ( | const CGPoint | v1, |
|
| const CGPoint | v2 | |||
| ) | ` [inline, static]` |

Calculates midpoint between two points.

| static CGPoint ccpMult | ( | const CGPoint | v, |
|
| const CGFloat | s | |||
| ) | ` [inline, static]` |

Returns point multiplied by given factor.

| static CGPoint ccpNeg | ( | const CGPoint | v |
) | ` [inline, static]` |

Returns opposite of point.

| CGPoint ccpNormalize | ( | const CGPoint | v |
) |

Returns point multiplied to a length of 1.

| static CGPoint ccpPerp | ( | const CGPoint | v |
) | ` [inline, static]` |

Calculates perpendicular of v, rotated 90 degrees counter-clockwise -- cross(v, perp(v)) >= 0

| static CGPoint ccpProject | ( | const CGPoint | v1, |
|
| const CGPoint | v2 | |||
| ) | ` [inline, static]` |

Calculates the projection of v1 over v2.

| static CGPoint ccpRotate | ( | const CGPoint | v1, |
|
| const CGPoint | v2 | |||
| ) | ` [inline, static]` |

Rotates two points.

| CGPoint ccpRotateByAngle | ( | CGPoint | v, |
|
| CGPoint | pivot, |
|||
| float | angle | |||
| ) |

Rotates a point counter clockwise by the angle around a pivot

v | is the point to rotate | |
pivot | is the pivot, naturally | |
angle | is the angle of rotation cw in radians |

| static CGPoint ccpRPerp | ( | const CGPoint | v |
) | ` [inline, static]` |

Calculates perpendicular of v, rotated 90 degrees clockwise -- cross(v, rperp(v)) <= 0

| static CGPoint ccpSub | ( | const CGPoint | v1, |
|
| const CGPoint | v2 | |||
| ) | ` [inline, static]` |

Calculates difference of two points.

| CGFloat ccpToAngle | ( | const CGPoint | v |
) |

Converts a vector to radians.

| static CGPoint ccpUnrotate | ( | const CGPoint | v1, |
|
| const CGPoint | v2 | |||
| ) | ` [inline, static]` |

Unrotates two points.

| float clampf | ( | float | value, |
|
| float | min_inclusive, |
|||
| float | max_inclusive | |||
| ) |

Clamp a value between from and to.