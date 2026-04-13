---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest/cocos2d-iphone/html/interface_c_c_camera/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCCamera.h>`


| void |
|

A [CCCamera](http://www.learn-cocos2d.com/api-ref/latest/cocos2d-iphone/html/interface_c_c_camera/) is used in every [CCNode](http://www.learn-cocos2d.com/api-ref/latest/cocos2d-iphone/html/interface_c_c_node/). Useful to look at the object from different views. The OpenGL [gluLookAt()](http://www.learn-cocos2d.com/#ad5d1457cca8c0412548e23b877ede908) function is used to locate the camera.

If the object is transformed by any of the scale, rotation or position attributes, then they will override the camera.

IMPORTANT: Either your use the camera or the rotation/scale/position properties. You can't use both. World coordinates won't work if you use the camera.

Limitations:

| void CCCamera::centerX:centerY:centerZ: | ( | float * | x, |
| [centerY] float * | y, |
||
| [centerZ] float * | z |
||
| ) | ` [virtual]` |

get the center vector values in points

| void CCCamera::eyeX:eyeY:eyeZ: | ( | float * | x, |
| [eyeY] float * | y, |
||
| [eyeZ] float * | z |
||
| ) | ` [virtual]` |

get the eye vector values in points

| float CCCamera::getZEye | ( | ) | ` [static, virtual]` |

returns the Z eye

| void CCCamera::locate | ( | ) | ` [virtual]` |

Sets the camera using gluLookAt using its eye, center and up_vector

| void CCCamera::restore | ( | ) | ` [virtual]` |

sets the camera in the defaul position

| void CCCamera::setCenterX:centerY:centerZ: | ( | float | x, |
| [centerY] float | y, |
||
| [centerZ] float | z |
||
| ) | ` [virtual]` |

sets the center values in points

| void CCCamera::setEyeX:eyeY:eyeZ: | ( | float | x, |
| [eyeY] float | y, |
||
| [eyeZ] float | z |
||
| ) | ` [virtual]` |

sets the eye values in points

| void CCCamera::setUpX:upY:upZ: | ( | float | x, |
| [upY] float | y, |
||
| [upZ] float | z |
||
| ) | ` [virtual]` |

sets the up values

| void CCCamera::upX:upY:upZ: | ( | float * | x, |
| [upY] float * | y, |
||
| [upZ] float * | z |
||
| ) | ` [virtual]` |

get the up vector values

BOOL CCCamera::dirty` [read, write, assign]` |

whether of not the camera is dirty