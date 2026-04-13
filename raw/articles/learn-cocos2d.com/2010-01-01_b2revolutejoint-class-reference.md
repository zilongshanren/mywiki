---
title: b2RevoluteJoint Class Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_revolute_joint/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# b2RevoluteJoint Class Reference

`#include <`[b2RevoluteJoint.h](/)>


[List of all members.](/)


## Detailed Description

A revolute joint constrains two bodies to share a common point while they are free to rotate about the point. The relative rotation about the shared point is the joint angle. You can limit the relative rotation with a joint limit that specifies a lower and upper angle. You can use a motor to drive the relative rotation about the shared point. A maximum motor torque is provided so that infinite forces are not generated.


## Constructor & Destructor Documentation


## Member Function Documentation

| void b2RevoluteJoint::EnableLimit |
( |
bool |
*flag* |
) |
|

Enable/disable the joint limit.

| void b2RevoluteJoint::EnableMotor |
( |
bool |
*flag* |
) |
|

Enable/disable the joint motor.

[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) b2RevoluteJoint::GetAnchorA |
( |
|
) |
const` [virtual]` |

Get the anchor point on bodyA in world coordinates.

Implements [b2Joint](../../../box2d-api-reference/API/classb2_joint/#abe46ca3aad5db73909a9b5a7b2117447).

[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) b2RevoluteJoint::GetAnchorB |
( |
|
) |
const` [virtual]` |

Get the anchor point on bodyB in world coordinates.

Implements [b2Joint](../../../box2d-api-reference/API/classb2_joint/#a88e947c65d4ea26fe539f02a8cb7f7a9).

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2RevoluteJoint::GetJointAngle |
( |
|
) |
const |

Get the current joint angle in radians.

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2RevoluteJoint::GetJointSpeed |
( |
|
) |
const |

Get the current joint angle speed in radians per second.

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2RevoluteJoint::GetLowerLimit |
( |
|
) |
const |

Get the lower joint limit in radians.

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2RevoluteJoint::GetMotorSpeed |
( |
|
) |
const` [inline]` |

Get the motor speed in radians per second.

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2RevoluteJoint::GetMotorTorque |
( |
|
) |
const |

Get the current motor torque, usually in N-m.

[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) b2RevoluteJoint::GetReactionForce |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*inv_dt* |
) |
const` [virtual]` |

Get the reaction force on body2 at the joint anchor in Newtons.

Implements [b2Joint](../../../box2d-api-reference/API/classb2_joint/#a7e0eddefb9b69ad050b8ef6425838a74).

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2RevoluteJoint::GetReactionTorque |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*inv_dt* |
) |
const` [virtual]` |

Get the reaction torque on body2 in N*m.

Implements [b2Joint](../../../box2d-api-reference/API/classb2_joint/#ae355e441c2aa842777dc04e24f15ced0).

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2RevoluteJoint::GetUpperLimit |
( |
|
) |
const |

Get the upper joint limit in radians.

| void b2RevoluteJoint::InitVelocityConstraints |
( |
const [b2TimeStep](../../../box2d-api-reference/API/structb2_time_step/) & |
*step* |
) |
` [protected, virtual]` |

| bool b2RevoluteJoint::IsLimitEnabled |
( |
|
) |
const |

Is the joint limit enabled?

| bool b2RevoluteJoint::IsMotorEnabled |
( |
|
) |
const |

Is the joint motor enabled?

Set the joint limits in radians.

| void b2RevoluteJoint::SetMaxMotorTorque |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*torque* |
) |
|

Set the maximum motor torque, usually in N-m.

| void b2RevoluteJoint::SetMotorSpeed |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*speed* |
) |
|

Set the motor speed in radians per second.

| bool b2RevoluteJoint::SolvePositionConstraints |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*baumgarte* |
) |
` [protected, virtual]` |

| void b2RevoluteJoint::SolveVelocityConstraints |
( |
const [b2TimeStep](../../../box2d-api-reference/API/structb2_time_step/) & |
*step* |
) |
` [protected, virtual]` |


## Friends And Related Function Documentation


## Member Data Documentation


The documentation for this class was generated from the following files: