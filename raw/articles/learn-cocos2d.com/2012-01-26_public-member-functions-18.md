---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_gear_joint/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Public Member Functions
|
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | [GetAnchorA](../../../../../api-ref/1.0/Box2D/html/classb2_gear_joint/#a2b5cdcb78c7ac3df4bd47e4195443a05) () const |
| | Get the anchor point on bodyA in world coordinates.
|
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | [GetAnchorB](../../../../../api-ref/1.0/Box2D/html/classb2_gear_joint/#a84b9aedb8918a98b84032c9f0f823e13) () const |
| | Get the anchor point on bodyB in world coordinates.
|
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | [GetReactionForce](../../../../../api-ref/1.0/Box2D/html/classb2_gear_joint/#ad415f3db70ba3e60a132ef668c263713) (float32 inv_dt) const |
| | Get the reaction force on bodyB at the joint anchor in Newtons.
|
| float32 | [GetReactionTorque](../../../../../api-ref/1.0/Box2D/html/classb2_gear_joint/#ae2c4b1ae1cf00f14331332c4fe9ae964) (float32 inv_dt) const |
| | Get the reaction torque on bodyB in N*m.
|
[b2Joint](../../../../../api-ref/1.0/Box2D/html/classb2_joint/) * | [GetJoint1](../../../../../api-ref/1.0/Box2D/html/classb2_gear_joint/#acd3fb38982319f387d1eb7aeddd5311f) () |
| | Get the first joint.
|
[b2Joint](../../../../../api-ref/1.0/Box2D/html/classb2_joint/) * | [GetJoint2](../../../../../api-ref/1.0/Box2D/html/classb2_gear_joint/#af1673b8edd80f3ae3b868c3a18b7b058) () |
| | Get the second joint.
|
| void | [SetRatio](../../../../../api-ref/1.0/Box2D/html/classb2_gear_joint/#a21c867bdc00c15ade2f399d370f92636) (float32 ratio) |
| | Set/Get the gear ratio.
|
float32 | **GetRatio** () const |
| void | [Dump](../../../../../api-ref/1.0/Box2D/html/classb2_gear_joint/#a1620b5a39e9da2b40d324c45736ad322) () |
| | Dump joint to dmLog.
|
Protected Member Functions
|
| **b2GearJoint** (const [b2GearJointDef](../../../../../api-ref/1.0/Box2D/html/structb2_gear_joint_def/) *data) |
void | **InitVelocityConstraints** (const [b2SolverData](../../../../../api-ref/1.0/Box2D/html/structb2_solver_data/) &data) |
void | **SolveVelocityConstraints** (const [b2SolverData](../../../../../api-ref/1.0/Box2D/html/structb2_solver_data/) &data) |
bool | **SolvePositionConstraints** (const [b2SolverData](../../../../../api-ref/1.0/Box2D/html/structb2_solver_data/) &data) |
Protected Attributes
|
[b2Joint](../../../../../api-ref/1.0/Box2D/html/classb2_joint/) * | **m_joint1** |
[b2Joint](../../../../../api-ref/1.0/Box2D/html/classb2_joint/) * | **m_joint2** |
b2JointType | **m_typeA** |
b2JointType | **m_typeB** |
[b2Body](../../../../../api-ref/1.0/Box2D/html/classb2_body/) * | **m_bodyC** |
[b2Body](../../../../../api-ref/1.0/Box2D/html/classb2_body/) * | **m_bodyD** |
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **m_localAnchorA** |
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **m_localAnchorB** |
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **m_localAnchorC** |
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **m_localAnchorD** |
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **m_localAxisC** |
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **m_localAxisD** |
float32 | **m_referenceAngleA** |
float32 | **m_referenceAngleB** |
float32 | **m_constant** |
float32 | **m_ratio** |
float32 | **m_impulse** |
int32 | **m_indexA** |
int32 | **m_indexB** |
int32 | **m_indexC** |
int32 | **m_indexD** |
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **m_lcA** |
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **m_lcB** |
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **m_lcC** |
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **m_lcD** |
float32 | **m_mA** |
float32 | **m_mB** |
float32 | **m_mC** |
float32 | **m_mD** |
float32 | **m_iA** |
float32 | **m_iB** |
float32 | **m_iC** |
float32 | **m_iD** |
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **m_JvAC** |
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **m_JvBD** |
float32 | **m_JwA** |
float32 | **m_JwB** |
float32 | **m_JwC** |
float32 | **m_JwD** |
float32 | **m_mass** |
Friends
|
class | **b2Joint** |

A gear joint is used to connect two joints together. Either joint can be a revolute or prismatic joint. You specify a gear ratio to bind the motions together: coordinate1 + ratio * coordinate2 = constant The ratio can be negative or positive. If one joint is a revolute joint and the other joint is a prismatic joint, then the ratio will have units of length or units of 1/length.

**Warning:**- You have to manually destroy the gear joint if joint1 or joint2 is destroyed.