---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_wheel_joint/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <b2WheelJoint.h>`


|

A wheel joint. This joint provides two degrees of freedom: translation along an axis fixed in bodyA and rotation in the plane. You can use a joint limit to restrict the range of motion and a joint motor to drive the rotation or to model rotational friction. This joint is designed for vehicle suspensions.

| void b2WheelJoint::EnableMotor | ( | bool | flag | ) |

Enable/disable the joint motor.

| float32 b2WheelJoint::GetJointSpeed | ( | ) | const |

Get the current joint translation speed, usually in meters per second.

| float32 b2WheelJoint::GetJointTranslation | ( | ) | const |

Get the current joint translation, usually in meters.

The local anchor point relative to bodyA's origin.

The local anchor point relative to bodyB's origin.

The local joint axis relative to bodyA.

| float32 b2WheelJoint::GetMotorSpeed | ( | ) | const` [inline]` |

Get the motor speed, usually in radians per second.

| float32 b2WheelJoint::GetMotorTorque | ( | float32 | inv_dt | ) | const |

Get the current motor torque given the inverse time step, usually in N-m.

| float32 b2WheelJoint::GetReactionTorque | ( | float32 | inv_dt | ) | const` [virtual]` |

| bool b2WheelJoint::IsMotorEnabled | ( | ) | const |

Is the joint motor enabled?

| void b2WheelJoint::SetMaxMotorTorque | ( | float32 | torque | ) |

Set/Get the maximum motor force, usually in N-m.

| void b2WheelJoint::SetMotorSpeed | ( | float32 | speed | ) |

Set the motor speed, usually in radians per second.

| void b2WheelJoint::SetSpringDampingRatio | ( | float32 | ratio | ) | ` [inline]` |

Set/Get the spring damping ratio.

| void b2WheelJoint::SetSpringFrequencyHz | ( | float32 | hz | ) | ` [inline]` |

Set/Get the spring frequency in hertz. Setting the frequency to zero disables the spring.