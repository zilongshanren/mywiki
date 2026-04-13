---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.0/Box2D/html/classb2_prismatic_joint/
published: '2012-09-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Public Member Functions
|
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | [GetAnchorA](../../../../../api-ref/2.0/Box2D/html/classb2_prismatic_joint/#ae6ccc4b3ceba180e4381fe4b821ef8d1) () const |
| | Get the anchor point on bodyA in world coordinates.
|
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | [GetAnchorB](../../../../../api-ref/2.0/Box2D/html/classb2_prismatic_joint/#aa2e00a1801989c3b6bc67bf47092b531) () const |
| | Get the anchor point on bodyB in world coordinates.
|
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | [GetReactionForce](../../../../../api-ref/2.0/Box2D/html/classb2_prismatic_joint/#a9e2a6103c1ff57e65d524b42f72b09e0) (float32 inv_dt) const |
| | Get the reaction force on bodyB at the joint anchor in Newtons.
|
| float32 | [GetReactionTorque](../../../../../api-ref/2.0/Box2D/html/classb2_prismatic_joint/#a59b419ccec1a5a4b80d6664d03bd256e) (float32 inv_dt) const |
| | Get the reaction torque on bodyB in N*m.
|
const [b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) & | [GetLocalAnchorA](../../../../../api-ref/2.0/Box2D/html/classb2_prismatic_joint/#a8453728991590d064f75ac9ee43eb0cb) () const |
| | The local anchor point relative to bodyA's origin.
|
const [b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) & | [GetLocalAnchorB](../../../../../api-ref/2.0/Box2D/html/classb2_prismatic_joint/#a5591358eced21a8845744a8c47b7df9d) () const |
| | The local anchor point relative to bodyB's origin.
|
const [b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) & | [GetLocalAxisA](../../../../../api-ref/2.0/Box2D/html/classb2_prismatic_joint/#ab1aff69853c5ddb89ed8efdf8a0f4376) () const |
| | The local joint axis relative to bodyA.
|
| float32 | [GetReferenceAngle](../../../../../api-ref/2.0/Box2D/html/classb2_prismatic_joint/#ae9e0a48367f191b2dd6a5bc05364a372) () const |
| | Get the reference angle.
|
| float32 | [GetJointTranslation](../../../../../api-ref/2.0/Box2D/html/classb2_prismatic_joint/#ade994ac79315258c80bccceef371df57) () const |
| | Get the current joint translation, usually in meters.
|
| float32 | [GetJointSpeed](../../../../../api-ref/2.0/Box2D/html/classb2_prismatic_joint/#a221aa1c6253686c96a02ecdd99c84b4c) () const |
| | Get the current joint translation speed, usually in meters per second.
|
| bool | [IsLimitEnabled](../../../../../api-ref/2.0/Box2D/html/classb2_prismatic_joint/#afb109fd7f3efbf44eae4b7961169bf9f) () const |
| | Is the joint limit enabled?
|
| void | [EnableLimit](../../../../../api-ref/2.0/Box2D/html/classb2_prismatic_joint/#a6d419afe7bd4b0e36d2e4607df7f79f2) (bool flag) |
| | Enable/disable the joint limit.
|
| float32 | [GetLowerLimit](../../../../../api-ref/2.0/Box2D/html/classb2_prismatic_joint/#ad58727abc63a820e6d93983408a9508b) () const |
| | Get the lower joint limit, usually in meters.
|
| float32 | [GetUpperLimit](../../../../../api-ref/2.0/Box2D/html/classb2_prismatic_joint/#ac72bdcf5108d474d3f11e86773a9a471) () const |
| | Get the upper joint limit, usually in meters.
|
| void | [SetLimits](../../../../../api-ref/2.0/Box2D/html/classb2_prismatic_joint/#a82a220e6d5a212c1924882e0855b0bef) (float32 lower, float32 upper) |
| | Set the joint limits, usually in meters.
|
| bool | [IsMotorEnabled](../../../../../api-ref/2.0/Box2D/html/classb2_prismatic_joint/#a236650664554a4d81f8644e9a9d19c65) () const |
| | Is the joint motor enabled?
|
| void | [EnableMotor](../../../../../api-ref/2.0/Box2D/html/classb2_prismatic_joint/#a4a7fd079de49f7ed5aa4a5d8d90be2a2) (bool flag) |
| | Enable/disable the joint motor.
|
| void | [SetMotorSpeed](../../../../../api-ref/2.0/Box2D/html/classb2_prismatic_joint/#a602ef7a6ca4fca55d011f1b38ab5a6c3) (float32 speed) |
| | Set the motor speed, usually in meters per second.
|
| float32 | [GetMotorSpeed](../../../../../api-ref/2.0/Box2D/html/classb2_prismatic_joint/#a20f969fefb08d86728bd1f0cf03e121f) () const |
| | Get the motor speed, usually in meters per second.
|
| void | [SetMaxMotorForce](../../../../../api-ref/2.0/Box2D/html/classb2_prismatic_joint/#aa7817474aef15ca4815341479ac590e2) (float32 force) |
| | Set the maximum motor force, usually in N.
|
float32 | **GetMaxMotorForce** () const |
| float32 | [GetMotorForce](../../../../../api-ref/2.0/Box2D/html/classb2_prismatic_joint/#aee80c02627750559fc382422804a30e6) (float32 inv_dt) const |
| | Get the current motor force given the inverse time step, usually in N.
|
| void | [Dump](../../../../../api-ref/2.0/Box2D/html/classb2_prismatic_joint/#a1d8e01f0c7ca9e1840f1f17c17dda7db) () |
| | Dump to b2Log.
|
Protected Member Functions
|
| **b2PrismaticJoint** (const [b2PrismaticJointDef](../../../../../api-ref/2.0/Box2D/html/structb2_prismatic_joint_def/) *def) |
void | **InitVelocityConstraints** (const [b2SolverData](../../../../../api-ref/2.0/Box2D/html/structb2_solver_data/) &data) |
void | **SolveVelocityConstraints** (const [b2SolverData](../../../../../api-ref/2.0/Box2D/html/structb2_solver_data/) &data) |
bool | **SolvePositionConstraints** (const [b2SolverData](../../../../../api-ref/2.0/Box2D/html/structb2_solver_data/) &data) |
Protected Attributes
|
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_localAnchorA** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_localAnchorB** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_localXAxisA** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_localYAxisA** |
float32 | **m_referenceAngle** |
[b2Vec3](../../../../../api-ref/2.0/Box2D/html/structb2_vec3/) | **m_impulse** |
float32 | **m_motorImpulse** |
float32 | **m_lowerTranslation** |
float32 | **m_upperTranslation** |
float32 | **m_maxMotorForce** |
float32 | **m_motorSpeed** |
bool | **m_enableLimit** |
bool | **m_enableMotor** |
b2LimitState | **m_limitState** |
int32 | **m_indexA** |
int32 | **m_indexB** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_localCenterA** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_localCenterB** |
float32 | **m_invMassA** |
float32 | **m_invMassB** |
float32 | **m_invIA** |
float32 | **m_invIB** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_axis** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_perp** |
float32 | **m_s1** |
float32 | **m_s2** |
float32 | **m_a1** |
float32 | **m_a2** |
[b2Mat33](../../../../../api-ref/2.0/Box2D/html/structb2_mat33/) | **m_K** |
float32 | **m_motorMass** |
Friends
|
class | **b2Joint** |
class | **b2GearJoint** |

A prismatic joint. This joint provides one degree of freedom: translation along an axis fixed in bodyA. Relative rotation is prevented. You can use a joint limit to restrict the range of motion and a joint motor to drive the motion or to model joint friction.