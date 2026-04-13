---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_friction_joint/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Public Member Functions
|
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | [GetAnchorA](../../../../../api-ref/1.0/Box2D/html/classb2_friction_joint/#a01918be429fa5d37d51fda4fe0cc639b) () const |
| | Get the anchor point on bodyA in world coordinates.
|
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | [GetAnchorB](../../../../../api-ref/1.0/Box2D/html/classb2_friction_joint/#ac519021aadea0faf1df01f232023c745) () const |
| | Get the anchor point on bodyB in world coordinates.
|
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | [GetReactionForce](../../../../../api-ref/1.0/Box2D/html/classb2_friction_joint/#ae646d8a191e490f690b748f057cdd90b) (float32 inv_dt) const |
| | Get the reaction force on bodyB at the joint anchor in Newtons.
|
| float32 | [GetReactionTorque](../../../../../api-ref/1.0/Box2D/html/classb2_friction_joint/#a49479d4af9c4bffa0b146d153c78512c) (float32 inv_dt) const |
| | Get the reaction torque on bodyB in N*m.
|
const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) & | [GetLocalAnchorA](../../../../../api-ref/1.0/Box2D/html/classb2_friction_joint/#a91ef023d373f775c401ae359f6f74d60) () const |
| | The local anchor point relative to bodyA's origin.
|
const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) & | [GetLocalAnchorB](../../../../../api-ref/1.0/Box2D/html/classb2_friction_joint/#acd57698eb559d36eeac6df00dfd8b89f) () const |
| | The local anchor point relative to bodyB's origin.
|
| void | [SetMaxForce](../../../../../api-ref/1.0/Box2D/html/classb2_friction_joint/#a7936d852b5ad71dc92efc397865dda41) (float32 force) |
| | Set the maximum friction force in N.
|
| float32 | [GetMaxForce](../../../../../api-ref/1.0/Box2D/html/classb2_friction_joint/#af3abd33af3943197c89375057302fd0d) () const |
| | Get the maximum friction force in N.
|
| void | [SetMaxTorque](../../../../../api-ref/1.0/Box2D/html/classb2_friction_joint/#a9e3aaf485dc86a378bb62ee78cea43aa) (float32 torque) |
| | Set the maximum friction torque in N*m.
|
| float32 | [GetMaxTorque](../../../../../api-ref/1.0/Box2D/html/classb2_friction_joint/#ae59d07030bded21f46a6a432553e71c1) () const |
| | Get the maximum friction torque in N*m.
|
| void | [Dump](../../../../../api-ref/1.0/Box2D/html/classb2_friction_joint/#a9a27084c9f4a7ea0a4f590f687ac1edb) () |
| | Dump joint to dmLog.
|
Protected Member Functions
|
| **b2FrictionJoint** (const [b2FrictionJointDef](../../../../../api-ref/1.0/Box2D/html/structb2_friction_joint_def/) *def) |
void | **InitVelocityConstraints** (const [b2SolverData](../../../../../api-ref/1.0/Box2D/html/structb2_solver_data/) &data) |
void | **SolveVelocityConstraints** (const [b2SolverData](../../../../../api-ref/1.0/Box2D/html/structb2_solver_data/) &data) |
bool | **SolvePositionConstraints** (const [b2SolverData](../../../../../api-ref/1.0/Box2D/html/structb2_solver_data/) &data) |
Protected Attributes
|
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **m_localAnchorA** |
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **m_localAnchorB** |
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **m_linearImpulse** |
float32 | **m_angularImpulse** |
float32 | **m_maxForce** |
float32 | **m_maxTorque** |
int32 | **m_indexA** |
int32 | **m_indexB** |
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **m_rA** |
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **m_rB** |
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **m_localCenterA** |
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **m_localCenterB** |
float32 | **m_invMassA** |
float32 | **m_invMassB** |
float32 | **m_invIA** |
float32 | **m_invIB** |
[b2Mat22](../../../../../api-ref/1.0/Box2D/html/structb2_mat22/) | **m_linearMass** |
float32 | **m_angularMass** |
Friends
|
class | **b2Joint** |

Friction joint. This is used for top-down friction. It provides 2D translational friction and angular friction.