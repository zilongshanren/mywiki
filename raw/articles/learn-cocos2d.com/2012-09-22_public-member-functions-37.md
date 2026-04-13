---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.0/Box2D/html/classb2_world/
published: '2012-09-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
Box2D
2.2
Box2D API Reference for www.kobold2d.com developers
|

`#include <b2World.h>`


|

The world class manages all physics entities, dynamic simulation, and asynchronous queries. The world also contains efficient memory management facilities.

Construct a world object.

| gravity | the world gravity vector. |

Destruct the world. All physics entities are destroyed and all heap memory is released.

Manually clear the force buffer on all bodies. By default, forces are cleared automatically after each call to Step. The default behavior is modified by calling SetAutoClearForces. The purpose of this function is to support sub-stepping. Sub-stepping is often used to maintain a fixed sized time step under a variable frame-rate. When you perform sub-stepping you will disable auto clearing of forces and instead call ClearForces after all sub-steps are complete in one pass of your game loop.

Create a rigid body given a definition. No reference to the definition is retained.

Create a joint to constrain bodies together. No reference to the definition is retained. This may cause the connected bodies to cease colliding.

Destroy a rigid body given a definition. No reference to the definition is retained. This function is locked during callbacks.

Destroy a joint. This may cause the connected bodies to begin colliding.

Dump the world into the log file.

Get the flag that controls automatic clearing of forces after each time step.

Get the number of contacts (each may have 0 or more contact points).

Get the world contact list. With the returned contact, use [b2Contact::GetNext](http://www.learn-cocos2d.com/api-ref/2.0/Box2D/html/classb2_contact/#aebfebb1e4b27dc0bd7aa120093e3d650) to get the next contact in the world list. A NULL contact indicates the end of the list.

Get the contact manager for testing.

Get the quality metric of the dynamic tree. The smaller the better. The minimum is 1.

Query the world for all fixtures that potentially overlap the provided AABB.

| callback | a user implemented callback class. |
| aabb | the query box. |

| void
|

Ray-cast the world for all fixtures in the path of the ray. Your callback controls whether you get the closest point, any point, or n-points. The ray-cast ignores shapes that contain the starting point.

| callback | a user implemented callback class. |
| point1 | the ray starting point |
| point2 | the ray ending point |

Set flag to control automatic clearing of forces after each time step.

Register a contact filter to provide specific control over collision. Otherwise the default filter is used (b2_defaultFilter). The listener is owned by you and must remain in scope.

Register a contact event listener. The listener is owned by you and must remain in scope.

Enable/disable continuous physics. For testing.

Register a destruction listener. The listener is owned by you and must remain in scope.

Enable/disable single stepped continuous physics. For testing.

Take a time step. This performs collision detection, integration, and constraint solution.

| timeStep | the amount of time to simulate, this should not vary. |
| velocityIterations | for the velocity constraint solver. |
| positionIterations | for the position constraint solver. |