---
title: b2DistanceJoint Class Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_distance_joint/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# b2DistanceJoint Class Reference

`#include <`[b2DistanceJoint.h](/)>


[List of all members.](/)


## Detailed Description

A distance joint constrains two points on two bodies to remain at a fixed distance from each other. You can view this as a massless, rigid rod.


## Constructor & Destructor Documentation


## Member Function Documentation

[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) b2DistanceJoint::GetAnchorA |
( |
|
) |
const` [virtual]` |

Get the anchor point on bodyA in world coordinates.

Implements [b2Joint](../../../box2d-api-reference/API/classb2_joint/#abe46ca3aad5db73909a9b5a7b2117447).

[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) b2DistanceJoint::GetAnchorB |
( |
|
) |
const` [virtual]` |

Get the anchor point on bodyB in world coordinates.

Implements [b2Joint](../../../box2d-api-reference/API/classb2_joint/#a88e947c65d4ea26fe539f02a8cb7f7a9).

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2DistanceJoint::GetDampingRatio |
( |
|
) |
const` [inline]` |


[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2DistanceJoint::GetFrequency |
( |
|
) |
const` [inline]` |


[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2DistanceJoint::GetLength |
( |
|
) |
const` [inline]` |


[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) b2DistanceJoint::GetReactionForce |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*inv_dt* |
) |
const` [virtual]` |

Get the reaction force on body2 at the joint anchor in Newtons.

Implements [b2Joint](../../../box2d-api-reference/API/classb2_joint/#a7e0eddefb9b69ad050b8ef6425838a74).

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2DistanceJoint::GetReactionTorque |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*inv_dt* |
) |
const` [virtual]` |

Get the reaction torque on body2 in N*m.

Implements [b2Joint](../../../box2d-api-reference/API/classb2_joint/#ae355e441c2aa842777dc04e24f15ced0).

| void b2DistanceJoint::InitVelocityConstraints |
( |
const [b2TimeStep](../../../box2d-api-reference/API/structb2_time_step/) & |
*step* |
) |
` [protected, virtual]` |

| void b2DistanceJoint::SetDampingRatio |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*ratio* |
) |
` [inline]` |


| void b2DistanceJoint::SetFrequency |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*hz* |
) |
` [inline]` |


| void b2DistanceJoint::SetLength |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*length* |
) |
` [inline]` |

Set/get the natural length. Manipulating the length can lead to non-physical behavior when the frequency is zero.

| bool b2DistanceJoint::SolvePositionConstraints |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*baumgarte* |
) |
` [protected, virtual]` |

| void b2DistanceJoint::SolveVelocityConstraints |
( |
const [b2TimeStep](../../../box2d-api-reference/API/structb2_time_step/) & |
*step* |
) |
` [protected, virtual]` |


## Friends And Related Function Documentation


## Member Data Documentation


The documentation for this class was generated from the following files: