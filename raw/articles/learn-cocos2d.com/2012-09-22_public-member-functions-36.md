---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.0/Box2D/html/classb2_wheel_joint/
published: '2012-09-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Public Member Functions
|
void | **GetDefinition** ([b2WheelJointDef](../../../../../api-ref/2.0/Box2D/html/structb2_wheel_joint_def/) *def) const |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | [GetAnchorA](../../../../../api-ref/2.0/Box2D/html/classb2_wheel_joint/#a6499dcd788d29f06c2e1b28c755e01c8) () const |
| | Get the anchor point on bodyA in world coordinates.
|
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | [GetAnchorB](../../../../../api-ref/2.0/Box2D/html/classb2_wheel_joint/#ace182061f7f78ac2ec3f957a763ca5d3) () const |
| | Get the anchor point on bodyB in world coordinates.
|
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | [GetReactionForce](../../../../../api-ref/2.0/Box2D/html/classb2_wheel_joint/#aa16e3a1c0246017bc25e72cf494daa42) (float32 inv_dt) const |
| | Get the reaction force on bodyB at the joint anchor in Newtons.
|
| float32 | [GetReactionTorque](../../../../../api-ref/2.0/Box2D/html/classb2_wheel_joint/#ae88eeec295a19f216acab9b23d9c704b) (float32 inv_dt) const |
| | Get the reaction torque on bodyB in N*m.
|
const [b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) & | [GetLocalAnchorA](../../../../../api-ref/2.0/Box2D/html/classb2_wheel_joint/#abf725ee0fa640d1b9374283f6f50e82d) () const |
| | The local anchor point relative to bodyA's origin.
|
const [b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) & | [GetLocalAnchorB](../../../../../api-ref/2.0/Box2D/html/classb2_wheel_joint/#a38313bcd5d5a91f190956086b9d9b8e5) () const |
| | The local anchor point relative to bodyB's origin.
|
const [b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) & | [GetLocalAxisA](../../../../../api-ref/2.0/Box2D/html/classb2_wheel_joint/#a03c1a1cf19dbada68630aa3cbf970a55) () const |
| | The local joint axis relative to bodyA.
|
| float32 | [GetJointTranslation](../../../../../api-ref/2.0/Box2D/html/classb2_wheel_joint/#abc3791f9c8139e5c5ba0fb72d5c7f9df) () const |
| | Get the current joint translation, usually in meters.
|
| float32 | [GetJointSpeed](../../../../../api-ref/2.0/Box2D/html/classb2_wheel_joint/#a398bc3a1f807905e0923cc7d9bff640d) () const |
| | Get the current joint translation speed, usually in meters per second.
|
| bool | [IsMotorEnabled](../../../../../api-ref/2.0/Box2D/html/classb2_wheel_joint/#a419bc80e17cc4c1062a692ea79396d19) () const |
| | Is the joint motor enabled?
|
| void | [EnableMotor](../../../../../api-ref/2.0/Box2D/html/classb2_wheel_joint/#a7a832d814bdda135a78fad41ba671da6) (bool flag) |
| | Enable/disable the joint motor.
|
| void | [SetMotorSpeed](../../../../../api-ref/2.0/Box2D/html/classb2_wheel_joint/#a6e3255fcf5c82b979ad7e3dc1c089c0b) (float32 speed) |
| | Set the motor speed, usually in radians per second.
|
| float32 | [GetMotorSpeed](../../../../../api-ref/2.0/Box2D/html/classb2_wheel_joint/#acc7a31fdd444614ba1943f57f0c6ac5a) () const |
| | Get the motor speed, usually in radians per second.
|
| void | [SetMaxMotorTorque](../../../../../api-ref/2.0/Box2D/html/classb2_wheel_joint/#a8aae3cd624ec9d48fc86c325c4595edc) (float32 torque) |
| | Set/Get the maximum motor force, usually in N-m.
|
float32 | **GetMaxMotorTorque** () const |
| float32 | [GetMotorTorque](../../../../../api-ref/2.0/Box2D/html/classb2_wheel_joint/#a4fbfb199ed267f7a2fad934cd2f4fbdc) (float32 inv_dt) const |
| | Get the current motor torque given the inverse time step, usually in N-m.
|
| void | [SetSpringFrequencyHz](../../../../../api-ref/2.0/Box2D/html/classb2_wheel_joint/#af9f8fada5cb30f83aa2fbf486e9d347b) (float32 hz) |
| | Set/Get the spring frequency in hertz. Setting the frequency to zero disables the spring.
|
float32 | **GetSpringFrequencyHz** () const |
| void | [SetSpringDampingRatio](../../../../../api-ref/2.0/Box2D/html/classb2_wheel_joint/#a39b123ac045c8ec93faa65746e6655dc) (float32 ratio) |
| | Set/Get the spring damping ratio.
|
float32 | **GetSpringDampingRatio** () const |
| void | [Dump](../../../../../api-ref/2.0/Box2D/html/classb2_wheel_joint/#a09534b6f4c5d0254711e0bcc7cf3b0e4) () |
| | Dump to b2Log.
|
Protected Member Functions
|
| **b2WheelJoint** (const [b2WheelJointDef](../../../../../api-ref/2.0/Box2D/html/structb2_wheel_joint_def/) *def) |
void | **InitVelocityConstraints** (const [b2SolverData](../../../../../api-ref/2.0/Box2D/html/structb2_solver_data/) &data) |
void | **SolveVelocityConstraints** (const [b2SolverData](../../../../../api-ref/2.0/Box2D/html/structb2_solver_data/) &data) |
bool | **SolvePositionConstraints** (const [b2SolverData](../../../../../api-ref/2.0/Box2D/html/structb2_solver_data/) &data) |
Protected Attributes
|
float32 | **m_frequencyHz** |
float32 | **m_dampingRatio** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_localAnchorA** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_localAnchorB** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_localXAxisA** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_localYAxisA** |
float32 | **m_impulse** |
float32 | **m_motorImpulse** |
float32 | **m_springImpulse** |
float32 | **m_maxMotorTorque** |
float32 | **m_motorSpeed** |
bool | **m_enableMotor** |
int32 | **m_indexA** |
int32 | **m_indexB** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_localCenterA** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_localCenterB** |
float32 | **m_invMassA** |
float32 | **m_invMassB** |
float32 | **m_invIA** |
float32 | **m_invIB** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_ax** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_ay** |
float32 | **m_sAx** |
float32 | **m_sBx** |
float32 | **m_sAy** |
float32 | **m_sBy** |
float32 | **m_mass** |
float32 | **m_motorMass** |
float32 | **m_springMass** |
float32 | **m_bias** |
float32 | **m_gamma** |
Friends
|
class | **b2Joint** |

A wheel joint. This joint provides two degrees of freedom: translation along an axis fixed in bodyA and rotation in the plane. You can use a joint limit to restrict the range of motion and a joint motor to drive the rotation or to model rotational friction. This joint is designed for vehicle suspensions.