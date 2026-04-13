---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.0/Box2D/html/classb2_revolute_joint/
published: '2012-09-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Public Member Functions
|
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | [GetAnchorA](../../../../../api-ref/2.0/Box2D/html/classb2_revolute_joint/#a7f266986c12009973fd74c9828b6c236) () const |
| | Get the anchor point on bodyA in world coordinates.
|
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | [GetAnchorB](../../../../../api-ref/2.0/Box2D/html/classb2_revolute_joint/#a3a67ad189b29ea8ab6602a28697807f6) () const |
| | Get the anchor point on bodyB in world coordinates.
|
const [b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) & | [GetLocalAnchorA](../../../../../api-ref/2.0/Box2D/html/classb2_revolute_joint/#af270a3029b2573bf85cde345c22d65ab) () const |
| | The local anchor point relative to bodyA's origin.
|
const [b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) & | [GetLocalAnchorB](../../../../../api-ref/2.0/Box2D/html/classb2_revolute_joint/#a985f788cffd53d7bb926b11cf77734e4) () const |
| | The local anchor point relative to bodyB's origin.
|
| float32 | [GetReferenceAngle](../../../../../api-ref/2.0/Box2D/html/classb2_revolute_joint/#acfe881247b1f1f8f12aefd3a8f0cfd00) () const |
| | Get the reference angle.
|
| float32 | [GetJointAngle](../../../../../api-ref/2.0/Box2D/html/classb2_revolute_joint/#ab20fc12ce5ad5d84a032eb613c80764a) () const |
| | Get the current joint angle in radians.
|
| float32 | [GetJointSpeed](../../../../../api-ref/2.0/Box2D/html/classb2_revolute_joint/#a48e4db13c187af159587d731656aa0c4) () const |
| | Get the current joint angle speed in radians per second.
|
| bool | [IsLimitEnabled](../../../../../api-ref/2.0/Box2D/html/classb2_revolute_joint/#a7711afbfbdba4451d2dbfa8e55b9ded8) () const |
| | Is the joint limit enabled?
|
| void | [EnableLimit](../../../../../api-ref/2.0/Box2D/html/classb2_revolute_joint/#a56bdfdd04e906e52d0258f6a481b9093) (bool flag) |
| | Enable/disable the joint limit.
|
| float32 | [GetLowerLimit](../../../../../api-ref/2.0/Box2D/html/classb2_revolute_joint/#a0f33656869e46ec9405f42d68e858220) () const |
| | Get the lower joint limit in radians.
|
| float32 | [GetUpperLimit](../../../../../api-ref/2.0/Box2D/html/classb2_revolute_joint/#a9bb683118879611e84e4cb26bdc8d39f) () const |
| | Get the upper joint limit in radians.
|
| void | [SetLimits](../../../../../api-ref/2.0/Box2D/html/classb2_revolute_joint/#a32f9393d8a6b993fd523f0f643c28107) (float32 lower, float32 upper) |
| | Set the joint limits in radians.
|
| bool | [IsMotorEnabled](../../../../../api-ref/2.0/Box2D/html/classb2_revolute_joint/#a9477b305db080e17dce8f2c6da0babb0) () const |
| | Is the joint motor enabled?
|
| void | [EnableMotor](../../../../../api-ref/2.0/Box2D/html/classb2_revolute_joint/#a80ed5a07d9a0e07d010808a73ffae6ff) (bool flag) |
| | Enable/disable the joint motor.
|
| void | [SetMotorSpeed](../../../../../api-ref/2.0/Box2D/html/classb2_revolute_joint/#a56f60bb1ea69048c8a455da49d62bf65) (float32 speed) |
| | Set the motor speed in radians per second.
|
| float32 | [GetMotorSpeed](../../../../../api-ref/2.0/Box2D/html/classb2_revolute_joint/#a5ebdb2b410725d2c7999d8fce792e0da) () const |
| | Get the motor speed in radians per second.
|
| void | [SetMaxMotorTorque](../../../../../api-ref/2.0/Box2D/html/classb2_revolute_joint/#a41779d7ec05be33e6368ef00123a3581) (float32 torque) |
| | Set the maximum motor torque, usually in N-m.
|
float32 | **GetMaxMotorTorque** () const |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | [GetReactionForce](../../../../../api-ref/2.0/Box2D/html/classb2_revolute_joint/#a1e5d6eb28f3f35e825cfc42dbd23d66e) (float32 inv_dt) const |
| float32 | [GetReactionTorque](../../../../../api-ref/2.0/Box2D/html/classb2_revolute_joint/#a85cdf204bf80dc0a4df6536e2e9a941e) (float32 inv_dt) const |
| float32 | [GetMotorTorque](../../../../../api-ref/2.0/Box2D/html/classb2_revolute_joint/#a64579cb1db5e9674ec17244133c72920) (float32 inv_dt) const |
| void | [Dump](../../../../../api-ref/2.0/Box2D/html/classb2_revolute_joint/#aa9d88f5476c77a5c4a6ef5b2ad0d3e6f) () |
| | Dump to b2Log.
|
Protected Member Functions
|
| **b2RevoluteJoint** (const [b2RevoluteJointDef](../../../../../api-ref/2.0/Box2D/html/structb2_revolute_joint_def/) *def) |
void | **InitVelocityConstraints** (const [b2SolverData](../../../../../api-ref/2.0/Box2D/html/structb2_solver_data/) &data) |
void | **SolveVelocityConstraints** (const [b2SolverData](../../../../../api-ref/2.0/Box2D/html/structb2_solver_data/) &data) |
bool | **SolvePositionConstraints** (const [b2SolverData](../../../../../api-ref/2.0/Box2D/html/structb2_solver_data/) &data) |
Protected Attributes
|
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_localAnchorA** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_localAnchorB** |
[b2Vec3](../../../../../api-ref/2.0/Box2D/html/structb2_vec3/) | **m_impulse** |
float32 | **m_motorImpulse** |
bool | **m_enableMotor** |
float32 | **m_maxMotorTorque** |
float32 | **m_motorSpeed** |
bool | **m_enableLimit** |
float32 | **m_referenceAngle** |
float32 | **m_lowerAngle** |
float32 | **m_upperAngle** |
int32 | **m_indexA** |
int32 | **m_indexB** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_rA** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_rB** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_localCenterA** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_localCenterB** |
float32 | **m_invMassA** |
float32 | **m_invMassB** |
float32 | **m_invIA** |
float32 | **m_invIB** |
[b2Mat33](../../../../../api-ref/2.0/Box2D/html/structb2_mat33/) | **m_mass** |
float32 | **m_motorMass** |
b2LimitState | **m_limitState** |
Friends
|
class | **b2Joint** |
class | **b2GearJoint** |

A revolute joint constrains two bodies to share a common point while they are free to rotate about the point. The relative rotation about the shared point is the joint angle. You can limit the relative rotation with a joint limit that specifies a lower and upper angle. You can use a motor to drive the relative rotation about the shared point. A maximum motor torque is provided so that infinite forces are not generated.