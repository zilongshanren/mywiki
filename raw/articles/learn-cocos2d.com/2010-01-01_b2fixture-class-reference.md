---
title: b2Fixture Class Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_fixture/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <`

[b2Fixture.h](http://www.learn-cocos2d.com/)>

## Public Member Functions | |
|

A fixture is used to attach a shape to a body for collision detection. A fixture inherits its transform from its parent. Fixtures hold additional non-geometric data such as friction, collision filters, etc. Fixtures are created via [b2Body::CreateFixture](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_body/#aa4892301e9b9d62ede5e93dad1743894).

| b2Fixture::b2Fixture | ( | ) | ` [protected]` |

| b2Fixture::~b2Fixture | ( | ) | ` [protected]` |

| void b2Fixture::Create | ( |
|

` [protected]`

Get the fixture's AABB. This AABB may be enlarge and/or stale. If you need a more accurate AABB, compute it using the shape and the body transform.

Get the parent body of this fixture. This is NULL if the fixture is not attached.

Get the mass data for this fixture. The mass data is based on the density and the shape. The rotational inertia is about the shape's origin. This operation may be expensive.

Get the next fixture in the parent body's fixture list.

Get the child shape. You can modify the child shape, however you should not change the number of vertices because this will crash some collision caching mechanisms. Manipulating the shape may lead to non-physical behavior.

Get the type of the child shape. You can use this to down cast to the concrete shape.

| void * b2Fixture::GetUserData | ( | ) | const` [inline]` |

Get the user data that was assigned in the fixture definition. Use this to store your application specific data.

| bool b2Fixture::IsSensor | ( | ) | const` [inline]` |

Is this fixture a sensor (non-solid)?

Cast a ray against this shape.

output | the ray-cast results. | |
input | the ray-cast input parameters. |

Set the contact filtering data. This will not update contacts until the next time step when either parent body is active and awake.

| void b2Fixture::SetSensor | ( | bool | sensor |
) |

Set if this fixture is a sensor.

| void b2Fixture::SetUserData | ( | void * | data |
) | ` [inline]` |

Set the user data. Use this to store your application specific data.

| void b2Fixture::Synchronize | ( |
|

` [protected]`

Test a point for containment in this fixture.

xf | the shape world transform. | |
p | a point in world coordinates. |