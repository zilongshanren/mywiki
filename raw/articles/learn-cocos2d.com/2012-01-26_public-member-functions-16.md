---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_fixture/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <b2Fixture.h>`


| b2Shape::Type |
|

A fixture is used to attach a shape to a body for collision detection. A fixture inherits its transform from its parent. Fixtures hold additional non-geometric data such as friction, collision filters, etc. Fixtures are created via [b2Body::CreateFixture](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_body/#a40dda91b34418bb40e31e2db9b1b76a5).

| void b2Fixture::Dump | ( | int32 | bodyIndex | ) |

Dump this fixture to the log file.

Get the fixture's AABB. This AABB may be enlarge and/or stale. If you need a more accurate AABB, compute it using the shape and the body transform.

Get the parent body of this fixture. This is NULL if the fixture is not attached.

| float32 b2Fixture::GetDensity | ( | ) | const` [inline]` |

Get the density of this fixture.

| float32 b2Fixture::GetFriction | ( | ) | const` [inline]` |

Get the coefficient of friction.

Get the mass data for this fixture. The mass data is based on the density and the shape. The rotational inertia is about the shape's origin. This operation may be expensive.

Get the next fixture in the parent body's fixture list.

| float32 b2Fixture::GetRestitution | ( | ) | const` [inline]` |

Get the coefficient of restitution.

Get the child shape. You can modify the child shape, however you should not change the number of vertices because this will crash some collision caching mechanisms. Manipulating the shape may lead to non-physical behavior.

| b2Shape::Type b2Fixture::GetType | ( | ) | const` [inline]` |

Get the type of the child shape. You can use this to down cast to the concrete shape.

| void * b2Fixture::GetUserData | ( | ) | const` [inline]` |

Get the user data that was assigned in the fixture definition. Use this to store your application specific data.

| bool b2Fixture::IsSensor | ( | ) | const` [inline]` |

Is this fixture a sensor (non-solid)?

| bool b2Fixture::RayCast | ( |
|

` [inline]`

Cast a ray against this shape.

| output | the ray-cast results. |
| input | the ray-cast input parameters. |

| void b2Fixture::Refilter | ( | ) |

| void b2Fixture::SetDensity | ( | float32 | density | ) | ` [inline]` |

Set the contact filtering data. This will not update contacts until the next time step when either parent body is active and awake. This automatically calls Refilter.

| void b2Fixture::SetFriction | ( | float32 | friction | ) | ` [inline]` |

Set the coefficient of friction. This will _not_ change the friction of existing contacts.

| void b2Fixture::SetRestitution | ( | float32 | restitution | ) | ` [inline]` |

Set the coefficient of restitution. This will _not_ change the restitution of existing contacts.

| void b2Fixture::SetSensor | ( | bool | sensor | ) |

Set if this fixture is a sensor.

| void b2Fixture::SetUserData | ( | void * | data | ) | ` [inline]` |

Set the user data. Use this to store your application specific data.

Test a point for containment in this fixture.

| p | a point in world coordinates. |