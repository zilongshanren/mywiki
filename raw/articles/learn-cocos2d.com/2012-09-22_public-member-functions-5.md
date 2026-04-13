---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.0/Box2D/html/classb2_body/
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

A rigid body. These are created via [b2World::CreateBody](http://www.learn-cocos2d.com/api-ref/2.0/Box2D/html/classb2_world/#a9323d553e4c132b26d8741b457d7c034).
[More...](http://www.learn-cocos2d.com/api-ref/2.0/Box2D/html/classb2_body/#details)

`#include <b2Body.h>`


|

Apply an angular impulse.

| impulse | the angular impulse in units of kg*m*m/s |

Apply a force at a world point. If the force is not applied at the center of mass, it will generate a torque and affect the angular velocity. This wakes up the body.

| force | the world force vector, usually in Newtons (N). |
| point | the world position of the point of application. |

Apply a force to the center of mass. This wakes up the body.

| force | the world force vector, usually in Newtons (N). |

Apply an impulse at a point. This immediately modifies the velocity. It also modifies the angular velocity if the point of application is not at the center of mass. This wakes up the body.

| impulse | the world impulse vector, usually in N-seconds or kg-m/s. |
| point | the world position of the point of application. |

Apply a torque. This affects the angular velocity without affecting the linear velocity of the center of mass. This wakes up the body.

| torque | about the z-axis (out of the screen), usually in N-m. |

Creates a fixture and attach it to this body. Use this function if you need to set some fixture parameters, like friction. Otherwise you can create the fixture directly from a shape. If the density is non-zero, this function automatically updates the mass of the body. Contacts are not created until the next time step.

| def | the fixture definition. |

Creates a fixture from a shape and attach it to this body. This is a convenience function. Use [b2FixtureDef](http://www.learn-cocos2d.com/api-ref/2.0/Box2D/html/structb2_fixture_def/) if you need to set parameters like friction, restitution, user data, or filtering. If the density is non-zero, this function automatically updates the mass of the body.

| shape | the shape to be cloned. |
| density | the shape density (set to zero for static bodies). |

Destroy a fixture. This removes the fixture from the broad-phase and destroys all contacts associated with this fixture. This will automatically adjust the mass of the body if the body is dynamic and the fixture has positive density. All fixtures attached to a body are implicitly destroyed when the body is destroyed.

| fixture | the fixture to be removed. |

Get the angle in radians.

Get the angular velocity.

Get the rotational inertia of the body about the local origin.

Get the linear velocity of the center of mass.

Get the world velocity of a local point.

| a | point in local coordinates. |

Get the world linear velocity of a world point attached to this body.

| a | point in world coordinates. |

Get the local position of the center of mass.

Gets a local point relative to the body's origin given a world point.

| a | point in world coordinates. |

Gets a local vector given a world vector.

| a | vector in world coordinates. |

Get the total mass of the body.

Get the mass data of the body.

Get the world body origin position.

Get the body transform for the body's origin.

Get the user data pointer that was provided in the body definition.

Get the world position of the center of mass.

Get the world coordinates of a point given the local coordinates.

| localPoint | a point on the body measured relative the the body's origin. |

Get the world coordinates of a vector given the local coordinates.

| localVector | a vector fixed in the body. |

Get the sleeping state of this body.

Is this body treated like a bullet for continuous collision detection?

This resets the mass properties to the sum of the mass properties of the fixtures. This normally does not need to be called unless you called SetMassData to override the mass and you later want to reset the mass.

Set the active state of the body. An inactive body is not simulated and cannot be collided with or woken up. If you pass a flag of true, all fixtures will be added to the broad-phase. If you pass a flag of false, all fixtures will be removed from the broad-phase and all contacts will be destroyed. Fixtures and joints are otherwise unaffected. You may continue to create/destroy fixtures and joints on inactive bodies. Fixtures on an inactive body are implicitly inactive and will not participate in collisions, ray-casts, or queries. Joints connected to an inactive body are implicitly inactive. An inactive body is still owned by a [b2World](http://www.learn-cocos2d.com/api-ref/2.0/Box2D/html/classb2_world/) object and remains in the body list.

Set the angular damping of the body.

Set the angular velocity.

| omega | the new angular velocity in radians/second. |

Set the sleep state of the body. A sleeping body has very low CPU cost.

| flag | set to true to put body to sleep, false to wake it. |

Should this body be treated like a bullet for continuous collision detection?

Set this body to have fixed rotation. This causes the mass to be reset.

Set the linear velocity of the center of mass.

| v | the new linear velocity of the center of mass. |

Set the mass properties to override the mass properties of the fixtures. Note that this changes the center of mass position. Note that creating or destroying fixtures can also alter the mass. This function has no effect if the body isn't dynamic.

| massData | the mass properties. |

You can disable sleeping on this body. If you disable sleeping, the body will be woken.

Set the position of the body's origin and rotation. This breaks any contacts and wakes the other bodies. Manipulating a body's transform may cause non-physical behavior.

| position | the world position of the body's local origin. |
| angle | the world rotation in radians. |

Set the type of this body. This may alter the mass and velocity.

Set the user data. Use this to store your application specific data.