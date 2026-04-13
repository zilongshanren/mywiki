---
title: b2LineJoint Class Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_line_joint/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# b2LineJoint Class Reference

`#include <`[b2LineJoint.h](/)>


[List of all members.](/)

## Public Member Functions |
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [GetAnchorA](../../../box2d-api-reference/API/classb2_line_joint/#aa085af07bd2e27768c58be9b62894458) () const |
| | Get the anchor point on bodyA in world coordinates.
|
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [GetAnchorB](../../../box2d-api-reference/API/classb2_line_joint/#a929b129ad6208956fe4eba3a43692764) () const |
| | Get the anchor point on bodyB in world coordinates.
|
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [GetReactionForce](../../../box2d-api-reference/API/classb2_line_joint/#a62f5d04249865beaad5c5c75517ff9e5) ([float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) inv_dt) const |
| | Get the reaction force on body2 at the joint anchor in Newtons.
|
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [GetReactionTorque](../../../box2d-api-reference/API/classb2_line_joint/#a5b2f457c36fe8c037d1a7121483b48e1) ([float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) inv_dt) const |
| | Get the reaction torque on body2 in N*m.
|
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [GetJointTranslation](../../../box2d-api-reference/API/classb2_line_joint/#ac6d9bc432f0a91e0d075054f1a72940f) () const |
| | Get the current joint translation, usually in meters.
|
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [GetJointSpeed](../../../box2d-api-reference/API/classb2_line_joint/#af9d88e37167dc14b898d1c4fbb245073) () const |
| | Get the current joint translation speed, usually in meters per second.
|
| bool | [IsLimitEnabled](../../../box2d-api-reference/API/classb2_line_joint/#ae8c53e505e763b73ebad6fb495735de4) () const |
| | Is the joint limit enabled?
|
| void | [EnableLimit](../../../box2d-api-reference/API/classb2_line_joint/#aaf8d692c005976419d131a1365995675) (bool flag) |
| | Enable/disable the joint limit.
|
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [GetLowerLimit](../../../box2d-api-reference/API/classb2_line_joint/#ad1e39ae5c29d800050eddcfd0e841285) () const |
| | Get the lower joint limit, usually in meters.
|
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [GetUpperLimit](../../../box2d-api-reference/API/classb2_line_joint/#ad0143cbf09ae63b1326af331c7539453) () const |
| | Get the upper joint limit, usually in meters.
|
| void | [SetLimits](../../../box2d-api-reference/API/classb2_line_joint/#acfc878589b4e552ae4bff6e78f27e4c0) ([float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) lower, [float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) upper) |
| | Set the joint limits, usually in meters.
|
| bool | [IsMotorEnabled](../../../box2d-api-reference/API/classb2_line_joint/#a1f2321787c0a3db2b4f99f00ab60b1fe) () const |
| | Is the joint motor enabled?
|
| void | [EnableMotor](../../../box2d-api-reference/API/classb2_line_joint/#a626e97f0073bebf74310c0f6bb9b0992) (bool flag) |
| | Enable/disable the joint motor.
|
| void | [SetMotorSpeed](../../../box2d-api-reference/API/classb2_line_joint/#a67662e5a5ef912339d95ab3fb3abd3fe) ([float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) speed) |
| | Set the motor speed, usually in meters per second.
|
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [GetMotorSpeed](../../../box2d-api-reference/API/classb2_line_joint/#a57019031344962585e2bc09e153ff5e3) () const |
| | Get the motor speed, usually in meters per second.
|
| void | [SetMaxMotorForce](../../../box2d-api-reference/API/classb2_line_joint/#ae0de07b7a5ea8bdda5db6a5074cf43b4) ([float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) force) |
| | Set/Get the maximum motor force, usually in N.
|
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [GetMaxMotorForce](../../../box2d-api-reference/API/classb2_line_joint/#af278e9769fea11d495642f4a225c0d5f) () const |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [GetMotorForce](../../../box2d-api-reference/API/classb2_line_joint/#aec9130652676b9f08a521596b27659ed) () const |
| | Get the current motor force, usually in N.
|
## Protected Member Functions |
| | [b2LineJoint](../../../box2d-api-reference/API/classb2_line_joint/#a3c5e6be23a54bddef085b99d2c9c4419) (const [b2LineJointDef](../../../box2d-api-reference/API/structb2_line_joint_def/) *def) |
| void | [InitVelocityConstraints](../../../box2d-api-reference/API/classb2_line_joint/#a2e4bb62830045d966a7e5b9e3e04f062) (const [b2TimeStep](../../../box2d-api-reference/API/structb2_time_step/) &step) |
| void | [SolveVelocityConstraints](../../../box2d-api-reference/API/classb2_line_joint/#abe450f145e0f80652d745f37cbbda153) (const [b2TimeStep](../../../box2d-api-reference/API/structb2_time_step/) &step) |
| bool | [SolvePositionConstraints](../../../box2d-api-reference/API/classb2_line_joint/#ac3be83c48a72338473d84d4b6df946da) ([float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) baumgarte) |
## Protected Attributes |
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [m_localAnchor1](../../../box2d-api-reference/API/classb2_line_joint/#a726d4d4e6495b95e5e5fd4fff73d8c6f) |
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [m_localAnchor2](../../../box2d-api-reference/API/classb2_line_joint/#acae136660af917d93a6be9b13df8459f) |
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [m_localXAxis1](../../../box2d-api-reference/API/classb2_line_joint/#a0ccfe787a79637ebd7b48df6eec62662) |
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [m_localYAxis1](../../../box2d-api-reference/API/classb2_line_joint/#a9f4f3f97110491b19d6b21a825628301) |
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [m_axis](../../../box2d-api-reference/API/classb2_line_joint/#ab5bad90f626292e604369bce35eacfae) |
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [m_perp](../../../box2d-api-reference/API/classb2_line_joint/#aa3dc4f648b7b03a0f23740b2fd0816fa) |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [m_s1](../../../box2d-api-reference/API/classb2_line_joint/#a78c34acd5402132d00440552af699a36) |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [m_s2](../../../box2d-api-reference/API/classb2_line_joint/#a7ed368ed6cd71d96dbf2eea1cc2881d1) |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [m_a1](../../../box2d-api-reference/API/classb2_line_joint/#a1357c2facffb70be658b3d327f11e4f8) |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [m_a2](../../../box2d-api-reference/API/classb2_line_joint/#a3c94e865aeebbf43d1ab036a9705ed0e) |
[b2Mat22](../../../box2d-api-reference/API/structb2_mat22/) | [m_K](../../../box2d-api-reference/API/classb2_line_joint/#a2d9455a72ff5a4751fbe7a0a50794cf4) |
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [m_impulse](../../../box2d-api-reference/API/classb2_line_joint/#a4166fec70e5bb483e645d21bad07deaa) |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [m_motorMass](../../../box2d-api-reference/API/classb2_line_joint/#a1b451696d7471319e87fdd8e89e0c3ae) |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [m_motorImpulse](../../../box2d-api-reference/API/classb2_line_joint/#ab86826f5c68baf14ff16758cadd7ad34) |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [m_lowerTranslation](../../../box2d-api-reference/API/classb2_line_joint/#aa16cb9494ac9d7eb475403409fdee706) |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [m_upperTranslation](../../../box2d-api-reference/API/classb2_line_joint/#a627fce6ae5b89ab565220c9eae1d2c7c) |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [m_maxMotorForce](../../../box2d-api-reference/API/classb2_line_joint/#a4c0a42495323f80b860475ade1bb487f) |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [m_motorSpeed](../../../box2d-api-reference/API/classb2_line_joint/#ae085a827d0b4a84a1e6aa0a78e07db5a) |
| bool | [m_enableLimit](../../../box2d-api-reference/API/classb2_line_joint/#a153ca58e6735427f8c6444b4f8cacc23) |
| bool | [m_enableMotor](../../../box2d-api-reference/API/classb2_line_joint/#aa94323ccc8bdb26a8b7f7da844ce274a) |
[b2LimitState](/#ae7784edce074221afeb010d638404443) | [m_limitState](../../../box2d-api-reference/API/classb2_line_joint/#ae4598d3146f04d17b109a3b3f923ee0c) |
## Friends |
| class | [b2Joint](../../../box2d-api-reference/API/classb2_line_joint/#a54ade8ed3d794298108d7f4c4e4793fa) |


## Detailed Description

A line joint. This joint provides two degrees of freedom: translation along an axis fixed in body1 and rotation in the plane. You can use a joint limit to restrict the range of motion and a joint motor to drive the motion or to model joint friction.


## Constructor & Destructor Documentation


## Member Function Documentation

| void b2LineJoint::EnableLimit |
( |
bool |
*flag* |
) |
|

Enable/disable the joint limit.

| void b2LineJoint::EnableMotor |
( |
bool |
*flag* |
) |
|

Enable/disable the joint motor.

[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) b2LineJoint::GetAnchorA |
( |
|
) |
const` [virtual]` |

Get the anchor point on bodyA in world coordinates.

Implements [b2Joint](../../../box2d-api-reference/API/classb2_joint/#abe46ca3aad5db73909a9b5a7b2117447).

[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) b2LineJoint::GetAnchorB |
( |
|
) |
const` [virtual]` |

Get the anchor point on bodyB in world coordinates.

Implements [b2Joint](../../../box2d-api-reference/API/classb2_joint/#a88e947c65d4ea26fe539f02a8cb7f7a9).

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2LineJoint::GetJointSpeed |
( |
|
) |
const |

Get the current joint translation speed, usually in meters per second.

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2LineJoint::GetJointTranslation |
( |
|
) |
const |

Get the current joint translation, usually in meters.

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2LineJoint::GetLowerLimit |
( |
|
) |
const |

Get the lower joint limit, usually in meters.

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2LineJoint::GetMaxMotorForce |
( |
|
) |
const |


[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2LineJoint::GetMotorForce |
( |
|
) |
const |

Get the current motor force, usually in N.

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2LineJoint::GetMotorSpeed |
( |
|
) |
const` [inline]` |

Get the motor speed, usually in meters per second.

[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) b2LineJoint::GetReactionForce |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*inv_dt* |
) |
const` [virtual]` |

Get the reaction force on body2 at the joint anchor in Newtons.

Implements [b2Joint](../../../box2d-api-reference/API/classb2_joint/#a7e0eddefb9b69ad050b8ef6425838a74).

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2LineJoint::GetReactionTorque |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*inv_dt* |
) |
const` [virtual]` |

Get the reaction torque on body2 in N*m.

Implements [b2Joint](../../../box2d-api-reference/API/classb2_joint/#ae355e441c2aa842777dc04e24f15ced0).

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2LineJoint::GetUpperLimit |
( |
|
) |
const |

Get the upper joint limit, usually in meters.

| void b2LineJoint::InitVelocityConstraints |
( |
const [b2TimeStep](../../../box2d-api-reference/API/structb2_time_step/) & |
*step* |
) |
` [protected, virtual]` |

| bool b2LineJoint::IsLimitEnabled |
( |
|
) |
const |

Is the joint limit enabled?

| bool b2LineJoint::IsMotorEnabled |
( |
|
) |
const |

Is the joint motor enabled?

Set the joint limits, usually in meters.

| void b2LineJoint::SetMaxMotorForce |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*force* |
) |
|

Set/Get the maximum motor force, usually in N.

| void b2LineJoint::SetMotorSpeed |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*speed* |
) |
|

Set the motor speed, usually in meters per second.

| bool b2LineJoint::SolvePositionConstraints |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*baumgarte* |
) |
` [protected, virtual]` |

| void b2LineJoint::SolveVelocityConstraints |
( |
const [b2TimeStep](../../../box2d-api-reference/API/structb2_time_step/) & |
*step* |
) |
` [protected, virtual]` |


## Friends And Related Function Documentation


## Member Data Documentation


The documentation for this class was generated from the following files: