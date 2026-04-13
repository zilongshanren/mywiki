---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_revolute_joint/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <b2RevoluteJoint.h>`


|

A revolute joint constrains two bodies to share a common point while they are free to rotate about the point. The relative rotation about the shared point is the joint angle. You can limit the relative rotation with a joint limit that specifies a lower and upper angle. You can use a motor to drive the relative rotation about the shared point. A maximum motor torque is provided so that infinite forces are not generated.

| void b2RevoluteJoint::EnableLimit | ( | bool | flag | ) |

Enable/disable the joint limit.

| void b2RevoluteJoint::EnableMotor | ( | bool | flag | ) |

Enable/disable the joint motor.

| float32 b2RevoluteJoint::GetJointAngle | ( | ) | const |

Get the current joint angle in radians.

| float32 b2RevoluteJoint::GetJointSpeed | ( | ) | const |

Get the current joint angle speed in radians per second.

The local anchor point relative to bodyA's origin.

The local anchor point relative to bodyB's origin.

| float32 b2RevoluteJoint::GetLowerLimit | ( | ) | const |

Get the lower joint limit in radians.

| float32 b2RevoluteJoint::GetMotorSpeed | ( | ) | const` [inline]` |

Get the motor speed in radians per second.

| float32 b2RevoluteJoint::GetMotorTorque | ( | float32 | inv_dt | ) | const |

Get the current motor torque given the inverse time step. Unit is N*m.

| float32 b2RevoluteJoint::GetReactionTorque | ( | float32 | inv_dt | ) | const` [virtual]` |

| float32 b2RevoluteJoint::GetReferenceAngle | ( | ) | const` [inline]` |

Get the reference angle.

| float32 b2RevoluteJoint::GetUpperLimit | ( | ) | const |

Get the upper joint limit in radians.

| bool b2RevoluteJoint::IsLimitEnabled | ( | ) | const |

Is the joint limit enabled?

| bool b2RevoluteJoint::IsMotorEnabled | ( | ) | const |

Is the joint motor enabled?

| void b2RevoluteJoint::SetLimits | ( | float32 | lower, |
| float32 | upper |
||
| ) |

Set the joint limits in radians.

| void b2RevoluteJoint::SetMaxMotorTorque | ( | float32 | torque | ) |

Set the maximum motor torque, usually in N-m.

| void b2RevoluteJoint::SetMotorSpeed | ( | float32 | speed | ) |

Set the motor speed in radians per second.