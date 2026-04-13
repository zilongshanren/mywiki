---
title: b2World Class Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_world/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <`

[b2World.h](http://www.learn-cocos2d.com/)>

## Public Member Functions | |
|

The world class manages all physics entities, dynamic simulation, and asynchronous queries. The world also contains efficient memory management facilities.

Construct a world object.

gravity | the world gravity vector. | |
doSleep | improve performance by not simulating inactive bodies. |

| b2World::~b2World | ( | ) |

Destruct the world. All physics entities are destroyed and all heap memory is released.

| void b2World::ClearForces | ( | ) |

Call this after you are done with time steps to clear the forces. You normally call this after each call to Step, unless you are performing sub-steps. By default, forces will be automatically cleared, so you don't need to call this function.

Create a rigid body given a definition. No reference to the definition is retained.

Create a joint to constrain bodies together. No reference to the definition is retained. This may cause the connected bodies to cease colliding.

Destroy a rigid body given a definition. No reference to the definition is retained. This function is locked during callbacks.

Destroy a joint. This may cause the connected bodies to begin colliding.

| void b2World::DrawDebugData | ( | ) |

Call this to draw shapes and other debug draw data.

| bool b2World::GetAutoClearForces | ( | ) | const` [inline]` |

Get the flag that controls automatic clearing of forces after each time step.

Get the number of contacts (each may have 0 or more contact points).

Get the world contact list. With the returned contact, use [b2Contact::GetNext](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_contact/#aebfebb1e4b27dc0bd7aa120093e3d650) to get the next contact in the world list. A NULL contact indicates the end of the list.

| bool b2World::IsLocked | ( | ) | const` [inline]` |

Is the world locked (in the middle of a time step).

Query the world for all fixtures that potentially overlap the provided AABB.

callback | a user implemented callback class. | |
aabb | the query box. |

| void b2World::RayCast | ( |
|

Ray-cast the world for all fixtures in the path of the ray. Your callback controls whether you get the closest point, any point, or n-points. The ray-cast ignores shapes that contain the starting point.

callback | a user implemented callback class. | |
point1 | the ray starting point | |
point2 | the ray ending point |

| void b2World::SetAutoClearForces | ( | bool | flag |
) | ` [inline]` |

Set flag to control automatic clearing of forces after each time step.

Register a contact filter to provide specific control over collision. Otherwise the default filter is used (b2_defaultFilter). The listener is owned by you and must remain in scope.

Register a contact event listener. The listener is owned by you and must remain in scope.

| void b2World::SetContinuousPhysics | ( | bool | flag |
) | ` [inline]` |

Enable/disable continuous physics. For testing.

Register a destruction listener. The listener is owned by you and must remain in scope.

| void b2World::SetWarmStarting | ( | bool | flag |
) | ` [inline]` |

Enable/disable warm starting. For testing.

Take a time step. This performs collision detection, integration, and constraint solution.

timeStep | the amount of time to simulate, this should not vary. | |
velocityIterations | for the velocity constraint solver. | |
positionIterations | for the position constraint solver. |

friend class b2Controller` [friend]` |