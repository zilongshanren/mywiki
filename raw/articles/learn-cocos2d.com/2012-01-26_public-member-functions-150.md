---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_frustum/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CC3Camera.h>`


| void |
|

Builds the planes in this frustum from the internal projectionMatrix and specified modelviewMatrix by multiplying the two matrices together and extracting the six frustum planes from the resulting model-view-projection matrix.

Returns whether the specified global location intersects (is inside) this frustum.

| BOOL CC3Frustum::doesIntersectSphereAt:withRadius: | ( |
|

` [virtual]`

Returns whether a sphere, centered at the specified global location, and with the specified radius, intersects this frustum.

| id CC3Frustum::frustum | ( | ) | ` [static, virtual]` |

Allocates and initializes an autorelease instance.

| NSString* CC3Frustum::fullDescription | ( | ) | ` [virtual]` |

Returns a string containing a more complete description of this frustum, including a description of each of the six planes that make up this frustum.

| void CC3Frustum::markPlanesDirty | ( | ) | ` [virtual]` |

Marks the planes as dirty and in need of recalculation.

| void CC3Frustum::populateFrom:andAspect:andNearClip:andFarClip:andZoom: | ( | GLfloat | fieldOfView, |
| [andAspect] GLfloat | aspect, |
||
| [andNearClip] GLfloat | nearClip, |
||
| [andFarClip] GLfloat | farClip, |
||
| [andZoom] GLfloat | zoomFactor |
||
| ) | ` [virtual]` |

Calculates the six frustum dimensions and the projectionMatrix from the specified projection parameters.

GLfloat CC3Frustum::bottom` [read, assign]` |

The distance from view center to the bottom of this frustum at the near clipping plane.

The clip plane at the bottom of this frustum, in global coordinates.

GLfloat CC3Frustum::far` [read, assign]` |

The distance to the far end of this frustum.

The clip plane at the far end of this frustum, in global coordinates.

BOOL CC3Frustum::isUsingParallelProjection` [read, write, assign]` |

Indicates whether this frustum uses parallel projection.

If this value is set to NO, the projection matrix will be configured for perspective projection, which is typical for 3D worlds. If this value is set to YES, the projection matrix will be configured for orthographic projection.

The initial value of this property is NO, indicating that perspective projection will be used.

GLfloat CC3Frustum::left` [read, assign]` |

The distance from view center to the left edge of this frustum at the near clipping plane.

The clip plane at the left side of this frustum, in global coordinates.

GLfloat CC3Frustum::near` [read, assign]` |

The distance to the near end of this frustum.

The clip plane at the near end of this frustum, in global coordinates.

The projection matrix that takes the camera's modelview and projects it to the viewport.

GLfloat CC3Frustum::right` [read, assign]` |

The distance from view center to the right edge of this frustum at the near clipping plane.

The clip plane at the right side of this frustum, in global coordinates.

GLfloat CC3Frustum::top` [read, assign]` |

The distance from view center to the top of this frustum at the near clipping plane.

The clip plane at the top of this frustum, in global coordinates.