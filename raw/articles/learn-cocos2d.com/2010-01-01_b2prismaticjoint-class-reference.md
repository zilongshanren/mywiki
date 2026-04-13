---
title: b2PrismaticJoint Class Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_prismatic_joint/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# b2PrismaticJoint Class Reference

`#include <`[b2PrismaticJoint.h](/)>


[List of all members.](/)

## Public Member Functions |
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [GetAnchorA](../../../box2d-api-reference/API/classb2_prismatic_joint/#ae6ccc4b3ceba180e4381fe4b821ef8d1) () const |
| | Get the anchor point on bodyA in world coordinates.
|
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [GetAnchorB](../../../box2d-api-reference/API/classb2_prismatic_joint/#aa2e00a1801989c3b6bc67bf47092b531) () const |
| | Get the anchor point on bodyB in world coordinates.
|
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [GetReactionForce](../../../box2d-api-reference/API/classb2_prismatic_joint/#a9e2a6103c1ff57e65d524b42f72b09e0) ([float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) inv_dt) const |
| | Get the reaction force on body2 at the joint anchor in Newtons.
|
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [GetReactionTorque](../../../box2d-api-reference/API/classb2_prismatic_joint/#a59b419ccec1a5a4b80d6664d03bd256e) ([float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) inv_dt) const |
| | Get the reaction torque on body2 in N*m.
|
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [GetJointTranslation](../../../box2d-api-reference/API/classb2_prismatic_joint/#ade994ac79315258c80bccceef371df57) () const |
| | Get the current joint translation, usually in meters.
|
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [GetJointSpeed](../../../box2d-api-reference/API/classb2_prismatic_joint/#a221aa1c6253686c96a02ecdd99c84b4c) () const |
| | Get the current joint translation speed, usually in meters per second.
|
| bool | [IsLimitEnabled](../../../box2d-api-reference/API/classb2_prismatic_joint/#afb109fd7f3efbf44eae4b7961169bf9f) () const |
| | Is the joint limit enabled?
|
| void | [EnableLimit](../../../box2d-api-reference/API/classb2_prismatic_joint/#a6d419afe7bd4b0e36d2e4607df7f79f2) (bool flag) |
| | Enable/disable the joint limit.
|
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [GetLowerLimit](../../../box2d-api-reference/API/classb2_prismatic_joint/#ad58727abc63a820e6d93983408a9508b) () const |
| | Get the lower joint limit, usually in meters.
|
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [GetUpperLimit](../../../box2d-api-reference/API/classb2_prismatic_joint/#ac72bdcf5108d474d3f11e86773a9a471) () const |
| | Get the upper joint limit, usually in meters.
|
| void | [SetLimits](../../../box2d-api-reference/API/classb2_prismatic_joint/#a82a220e6d5a212c1924882e0855b0bef) ([float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) lower, [float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) upper) |
| | Set the joint limits, usually in meters.
|
| bool | [IsMotorEnabled](../../../box2d-api-reference/API/classb2_prismatic_joint/#a236650664554a4d81f8644e9a9d19c65) () const |
| | Is the joint motor enabled?
|
| void | [EnableMotor](../../../box2d-api-reference/API/classb2_prismatic_joint/#a4a7fd079de49f7ed5aa4a5d8d90be2a2) (bool flag) |
| | Enable/disable the joint motor.
|
| void | [SetMotorSpeed](../../../box2d-api-reference/API/classb2_prismatic_joint/#a602ef7a6ca4fca55d011f1b38ab5a6c3) ([float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) speed) |
| | Set the motor speed, usually in meters per second.
|
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [GetMotorSpeed](../../../box2d-api-reference/API/classb2_prismatic_joint/#a20f969fefb08d86728bd1f0cf03e121f) () const |
| | Get the motor speed, usually in meters per second.
|
| void | [SetMaxMotorForce](../../../box2d-api-reference/API/classb2_prismatic_joint/#aa7817474aef15ca4815341479ac590e2) ([float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) force) |
| | Set the maximum motor force, usually in N.
|
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [GetMotorForce](../../../box2d-api-reference/API/classb2_prismatic_joint/#af418d8b1020a38c198826124cbde96b5) () const |
| | Get the current motor force, usually in N.
|
## Protected Member Functions |
| | [b2PrismaticJoint](../../../box2d-api-reference/API/classb2_prismatic_joint/#ab1586a2334f7e32137fbd7f807e249ca) (const [b2PrismaticJointDef](../../../box2d-api-reference/API/structb2_prismatic_joint_def/) *def) |
| void | [InitVelocityConstraints](../../../box2d-api-reference/API/classb2_prismatic_joint/#a98dcc84c1d9e170818244e7e3a390c05) (const [b2TimeStep](../../../box2d-api-reference/API/structb2_time_step/) &step) |
| void | [SolveVelocityConstraints](../../../box2d-api-reference/API/classb2_prismatic_joint/#a794d24031aca0c81ccdb9ad629b38db9) (const [b2TimeStep](../../../box2d-api-reference/API/structb2_time_step/) &step) |
| bool | [SolvePositionConstraints](../../../box2d-api-reference/API/classb2_prismatic_joint/#a4eadb4e24d0c46cef8e7b1ff93d93377) ([float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) baumgarte) |
## Protected Attributes |
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [m_localAnchor1](../../../box2d-api-reference/API/classb2_prismatic_joint/#aa10581a9650f53a45474c12cb7490f9a) |
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [m_localAnchor2](../../../box2d-api-reference/API/classb2_prismatic_joint/#a3b8d96a67523c4cad042c09af384d8ce) |
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [m_localXAxis1](../../../box2d-api-reference/API/classb2_prismatic_joint/#a77f9f72cd56d511c69853c80184e8dc7) |
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [m_localYAxis1](../../../box2d-api-reference/API/classb2_prismatic_joint/#a1ce2f76f7fcf29097bd67392ecabd6ff) |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [m_refAngle](../../../box2d-api-reference/API/classb2_prismatic_joint/#a1f30dd10eb25c92def470f2b1d930151) |
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [m_axis](../../../box2d-api-reference/API/classb2_prismatic_joint/#af487c98feb16d19d5d1b320ad2aefb49) |
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [m_perp](../../../box2d-api-reference/API/classb2_prismatic_joint/#a560f7177fbc3db1916e076a755b406e5) |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [m_s1](../../../box2d-api-reference/API/classb2_prismatic_joint/#a5dad08589b72d49c05b61bbee0a1fa39) |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [m_s2](../../../box2d-api-reference/API/classb2_prismatic_joint/#a7b82750572655292a3e08490d1131f31) |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [m_a1](../../../box2d-api-reference/API/classb2_prismatic_joint/#afa9f7a7b4317a491d76390e0db7034e4) |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [m_a2](../../../box2d-api-reference/API/classb2_prismatic_joint/#a91fd8e15cd9c610c343d162cb31e6552) |
[b2Mat33](../../../box2d-api-reference/API/structb2_mat33/) | [m_K](../../../box2d-api-reference/API/classb2_prismatic_joint/#a2a19322c65fd08eda34991dfa50c5d00) |
[b2Vec3](../../../box2d-api-reference/API/structb2_vec3/) | [m_impulse](../../../box2d-api-reference/API/classb2_prismatic_joint/#a92530ae3ec9765d775ec82a39400f770) |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [m_motorMass](../../../box2d-api-reference/API/classb2_prismatic_joint/#a6e9fcd93328657df8b7fa1c6c6a517dd) |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [m_motorImpulse](../../../box2d-api-reference/API/classb2_prismatic_joint/#aff90d55579b511950334d8a0449f1155) |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [m_lowerTranslation](../../../box2d-api-reference/API/classb2_prismatic_joint/#a82e13b09e43d0d82365845aa3fb7f9fe) |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [m_upperTranslation](../../../box2d-api-reference/API/classb2_prismatic_joint/#a09a5bbe1ae720f1f4e2b1fd16f8ad613) |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [m_maxMotorForce](../../../box2d-api-reference/API/classb2_prismatic_joint/#a42685bcbc18ea7a74d75c459a381a7b9) |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [m_motorSpeed](../../../box2d-api-reference/API/classb2_prismatic_joint/#a0851a1993e9e4f4103a8f7dbaeedb9c5) |
| bool | [m_enableLimit](../../../box2d-api-reference/API/classb2_prismatic_joint/#ace469adee4132fb1de01fe5ab3d26389) |
| bool | [m_enableMotor](../../../box2d-api-reference/API/classb2_prismatic_joint/#af36c993314f8ae833f5f3b3aebd66497) |
[b2LimitState](/#ae7784edce074221afeb010d638404443) | [m_limitState](../../../box2d-api-reference/API/classb2_prismatic_joint/#ad5ce4e2d66a0d612573e07103b407b99) |
## Friends |
| class | [b2Joint](../../../box2d-api-reference/API/classb2_prismatic_joint/#a54ade8ed3d794298108d7f4c4e4793fa) |
| class | [b2GearJoint](../../../box2d-api-reference/API/classb2_prismatic_joint/#a13c275221e30bb485e17e4e04553cb71) |


## Detailed Description

A prismatic joint. This joint provides one degree of freedom: translation along an axis fixed in body1. Relative rotation is prevented. You can use a joint limit to restrict the range of motion and a joint motor to drive the motion or to model joint friction.


## Constructor & Destructor Documentation


## Member Function Documentation

| void b2PrismaticJoint::EnableLimit |
( |
bool |
*flag* |
) |
|

Enable/disable the joint limit.

| void b2PrismaticJoint::EnableMotor |
( |
bool |
*flag* |
) |
|

Enable/disable the joint motor.

[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) b2PrismaticJoint::GetAnchorA |
( |
|
) |
const` [virtual]` |

Get the anchor point on bodyA in world coordinates.

Implements [b2Joint](../../../box2d-api-reference/API/classb2_joint/#abe46ca3aad5db73909a9b5a7b2117447).

[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) b2PrismaticJoint::GetAnchorB |
( |
|
) |
const` [virtual]` |

Get the anchor point on bodyB in world coordinates.

Implements [b2Joint](../../../box2d-api-reference/API/classb2_joint/#a88e947c65d4ea26fe539f02a8cb7f7a9).

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2PrismaticJoint::GetJointSpeed |
( |
|
) |
const |

Get the current joint translation speed, usually in meters per second.

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2PrismaticJoint::GetJointTranslation |
( |
|
) |
const |

Get the current joint translation, usually in meters.

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2PrismaticJoint::GetLowerLimit |
( |
|
) |
const |

Get the lower joint limit, usually in meters.

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2PrismaticJoint::GetMotorForce |
( |
|
) |
const |

Get the current motor force, usually in N.

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2PrismaticJoint::GetMotorSpeed |
( |
|
) |
const` [inline]` |

Get the motor speed, usually in meters per second.

[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) b2PrismaticJoint::GetReactionForce |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*inv_dt* |
) |
const` [virtual]` |

Get the reaction force on body2 at the joint anchor in Newtons.

Implements [b2Joint](../../../box2d-api-reference/API/classb2_joint/#a7e0eddefb9b69ad050b8ef6425838a74).

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2PrismaticJoint::GetReactionTorque |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*inv_dt* |
) |
const` [virtual]` |

Get the reaction torque on body2 in N*m.

Implements [b2Joint](../../../box2d-api-reference/API/classb2_joint/#ae355e441c2aa842777dc04e24f15ced0).

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2PrismaticJoint::GetUpperLimit |
( |
|
) |
const |

Get the upper joint limit, usually in meters.

| void b2PrismaticJoint::InitVelocityConstraints |
( |
const [b2TimeStep](../../../box2d-api-reference/API/structb2_time_step/) & |
*step* |
) |
` [protected, virtual]` |

| bool b2PrismaticJoint::IsLimitEnabled |
( |
|
) |
const |

Is the joint limit enabled?

| bool b2PrismaticJoint::IsMotorEnabled |
( |
|
) |
const |

Is the joint motor enabled?

Set the joint limits, usually in meters.

| void b2PrismaticJoint::SetMaxMotorForce |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*force* |
) |
|

Set the maximum motor force, usually in N.

| void b2PrismaticJoint::SetMotorSpeed |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*speed* |
) |
|

Set the motor speed, usually in meters per second.

| bool b2PrismaticJoint::SolvePositionConstraints |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*baumgarte* |
) |
` [protected, virtual]` |

| void b2PrismaticJoint::SolveVelocityConstraints |
( |
const [b2TimeStep](../../../box2d-api-reference/API/structb2_time_step/) & |
*step* |
) |
` [protected, virtual]` |


## Friends And Related Function Documentation


## Member Data Documentation


The documentation for this class was generated from the following files: