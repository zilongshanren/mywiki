---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest/Box2D/html/classb2_world/
published: '2012-03-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <b2World.h>`


|

The world class manages all physics entities, dynamic simulation, and asynchronous queries. The world also contains efficient memory management facilities.

Construct a world object.

| gravity | the world gravity vector. |

| b2World::~b2World | ( | ) |

Destruct the world. All physics entities are destroyed and all heap memory is released.

| void b2World::ClearForces | ( | ) |

Manually clear the force buffer on all bodies. By default, forces are cleared automatically after each call to Step. The default behavior is modified by calling SetAutoClearForces. The purpose of this function is to support sub-stepping. Sub-stepping is often used to maintain a fixed sized time step under a variable frame-rate. When you perform sub-stepping you will disable auto clearing of forces and instead call ClearForces after all sub-steps are complete in one pass of your game loop.

Create a rigid body given a definition. No reference to the definition is retained.

Create a joint to constrain bodies together. No reference to the definition is retained. This may cause the connected bodies to cease colliding.

Destroy a rigid body given a definition. No reference to the definition is retained. This function is locked during callbacks.

Destroy a joint. This may cause the connected bodies to begin colliding.

| void b2World::DrawDebugData | ( | ) |

Call this to draw shapes and other debug draw data.

| void b2World::Dump | ( | ) |

Dump the world into the log file.

| bool b2World::GetAutoClearForces | ( | ) | const` [inline]` |

Get the flag that controls automatic clearing of forces after each time step.

| int32 b2World::GetBodyCount | ( | ) | const` [inline]` |

Get the number of bodies.

| int32 b2World::GetContactCount | ( | ) | const` [inline]` |

Get the number of contacts (each may have 0 or more contact points).

Get the world contact list. With the returned contact, use [b2Contact::GetNext](http://www.learn-cocos2d.com/api-ref/latest/Box2D/html/classb2_contact/#aebfebb1e4b27dc0bd7aa120093e3d650) to get the next contact in the world list. A NULL contact indicates the end of the list.

Get the contact manager for testing.

| int32 b2World::GetJointCount | ( | ) | const` [inline]` |

Get the number of joints.

| int32 b2World::GetProxyCount | ( | ) | const |

Get the number of broad-phase proxies.

| int32 b2World::GetTreeBalance | ( | ) | const |

Get the balance of the dynamic tree.

| int32 b2World::GetTreeHeight | ( | ) | const |

Get the height of the dynamic tree.

| float32 b2World::GetTreeQuality | ( | ) | const |

Get the quality metric of the dynamic tree. The smaller the better. The minimum is 1.

| bool b2World::IsLocked | ( | ) | const` [inline]` |

Is the world locked (in the middle of a time step).

Query the world for all fixtures that potentially overlap the provided AABB.

| callback | a user implemented callback class. |
| aabb | the query box. |

| void b2World::RayCast | ( |
|

Ray-cast the world for all fixtures in the path of the ray. Your callback controls whether you get the closest point, any point, or n-points. The ray-cast ignores shapes that contain the starting point.

| callback | a user implemented callback class. |
| point1 | the ray starting point |
| point2 | the ray ending point |

| void b2World::SetAllowSleeping | ( | bool | flag | ) |

Enable/disable sleep.

| void b2World::SetAutoClearForces | ( | bool | flag | ) | ` [inline]` |

Set flag to control automatic clearing of forces after each time step.

Register a contact filter to provide specific control over collision. Otherwise the default filter is used (b2_defaultFilter). The listener is owned by you and must remain in scope.

Register a contact event listener. The listener is owned by you and must remain in scope.

| void b2World::SetContinuousPhysics | ( | bool | flag | ) | ` [inline]` |

Enable/disable continuous physics. For testing.

Register a destruction listener. The listener is owned by you and must remain in scope.

| void b2World::SetSubStepping | ( | bool | flag | ) | ` [inline]` |

Enable/disable single stepped continuous physics. For testing.

| void b2World::SetWarmStarting | ( | bool | flag | ) | ` [inline]` |

Enable/disable warm starting. For testing.

| void b2World::Step | ( | float32 | timeStep, |
| int32 | velocityIterations, |
||
| int32 | positionIterations |
||
| ) |

Take a time step. This performs collision detection, integration, and constraint solution.

| timeStep | the amount of time to simulate, this should not vary. |
| velocityIterations | for the velocity constraint solver. |
| positionIterations | for the position constraint solver. |