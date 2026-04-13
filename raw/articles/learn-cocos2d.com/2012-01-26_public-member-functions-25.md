---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_prismatic_joint/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <b2PrismaticJoint.h>`


|

A prismatic joint. This joint provides one degree of freedom: translation along an axis fixed in bodyA. Relative rotation is prevented. You can use a joint limit to restrict the range of motion and a joint motor to drive the motion or to model joint friction.

| void b2PrismaticJoint::EnableLimit | ( | bool | flag | ) |

Enable/disable the joint limit.

| void b2PrismaticJoint::EnableMotor | ( | bool | flag | ) |

Enable/disable the joint motor.

| float32 b2PrismaticJoint::GetJointSpeed | ( | ) | const |

Get the current joint translation speed, usually in meters per second.

| float32 b2PrismaticJoint::GetJointTranslation | ( | ) | const |

Get the current joint translation, usually in meters.

The local anchor point relative to bodyA's origin.

The local anchor point relative to bodyB's origin.

The local joint axis relative to bodyA.

| float32 b2PrismaticJoint::GetLowerLimit | ( | ) | const |

Get the lower joint limit, usually in meters.

| float32 b2PrismaticJoint::GetMotorForce | ( | float32 | inv_dt | ) | const |

Get the current motor force given the inverse time step, usually in N.

| float32 b2PrismaticJoint::GetMotorSpeed | ( | ) | const` [inline]` |

Get the motor speed, usually in meters per second.

| float32 b2PrismaticJoint::GetReactionTorque | ( | float32 | inv_dt | ) | const` [virtual]` |

| float32 b2PrismaticJoint::GetReferenceAngle | ( | ) | const` [inline]` |

Get the reference angle.

| float32 b2PrismaticJoint::GetUpperLimit | ( | ) | const |

Get the upper joint limit, usually in meters.

| bool b2PrismaticJoint::IsLimitEnabled | ( | ) | const |

Is the joint limit enabled?

| bool b2PrismaticJoint::IsMotorEnabled | ( | ) | const |

Is the joint motor enabled?

| void b2PrismaticJoint::SetLimits | ( | float32 | lower, |
| float32 | upper |
||
| ) |

Set the joint limits, usually in meters.

| void b2PrismaticJoint::SetMaxMotorForce | ( | float32 | force | ) |

Set the maximum motor force, usually in N.

| void b2PrismaticJoint::SetMotorSpeed | ( | float32 | speed | ) |

Set the motor speed, usually in meters per second.