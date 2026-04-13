---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_rope_joint/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Public Member Functions
|
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | [GetAnchorA](../../../../../api-ref/1.0/Box2D/html/classb2_rope_joint/#a046c6f0bc73800716c669a2b955b3c05) () const |
| | Get the anchor point on bodyA in world coordinates.
|
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | [GetAnchorB](../../../../../api-ref/1.0/Box2D/html/classb2_rope_joint/#a14a8ef7c16e0d6d874cdfb986d0eb8f0) () const |
| | Get the anchor point on bodyB in world coordinates.
|
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | [GetReactionForce](../../../../../api-ref/1.0/Box2D/html/classb2_rope_joint/#afe0acc77e40b62133547897a6d01b7e6) (float32 inv_dt) const |
| | Get the reaction force on bodyB at the joint anchor in Newtons.
|
| float32 | [GetReactionTorque](../../../../../api-ref/1.0/Box2D/html/classb2_rope_joint/#abb7baf596f13ff5a76ff657ad6d3232c) (float32 inv_dt) const |
| | Get the reaction torque on bodyB in N*m.
|
const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) & | [GetLocalAnchorA](../../../../../api-ref/1.0/Box2D/html/classb2_rope_joint/#aa423bbe186d46bff0b50ede8338851d4) () const |
| | The local anchor point relative to bodyA's origin.
|
const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) & | [GetLocalAnchorB](../../../../../api-ref/1.0/Box2D/html/classb2_rope_joint/#a511b297fbebfbecdcdce68e1cffa272c) () const |
| | The local anchor point relative to bodyB's origin.
|
| void | [SetMaxLength](../../../../../api-ref/1.0/Box2D/html/classb2_rope_joint/#a92cea201d21acd2f2a7cc9b00e165848) (float32 length) |
| | Set/Get the maximum length of the rope.
|
float32 | **GetMaxLength** () const |
b2LimitState | **GetLimitState** () const |
| void | [Dump](../../../../../api-ref/1.0/Box2D/html/classb2_rope_joint/#a4612dca9851a66701893a48d896dbd14) () |
| | Dump joint to dmLog.
|
Protected Member Functions
|
| **b2RopeJoint** (const [b2RopeJointDef](../../../../../api-ref/1.0/Box2D/html/structb2_rope_joint_def/) *data) |
void | **InitVelocityConstraints** (const [b2SolverData](../../../../../api-ref/1.0/Box2D/html/structb2_solver_data/) &data) |
void | **SolveVelocityConstraints** (const [b2SolverData](../../../../../api-ref/1.0/Box2D/html/structb2_solver_data/) &data) |
bool | **SolvePositionConstraints** (const [b2SolverData](../../../../../api-ref/1.0/Box2D/html/structb2_solver_data/) &data) |
Protected Attributes
|
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **m_localAnchorA** |
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **m_localAnchorB** |
float32 | **m_maxLength** |
float32 | **m_length** |
float32 | **m_impulse** |
int32 | **m_indexA** |
int32 | **m_indexB** |
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **m_u** |
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **m_rA** |
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **m_rB** |
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **m_localCenterA** |
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **m_localCenterB** |
float32 | **m_invMassA** |
float32 | **m_invMassB** |
float32 | **m_invIA** |
float32 | **m_invIB** |
float32 | **m_mass** |
b2LimitState | **m_state** |
Friends
|
class | **b2Joint** |

A rope joint enforces a maximum distance between two points on two bodies. It has no other effect. Warning: if you attempt to change the maximum length during the simulation you will get some non-physical behavior. A model that would allow you to dynamically modify the length would have some sponginess, so I chose not to implement it that way. See [b2DistanceJoint](../../../../../api-ref/1.0/Box2D/html/classb2_distance_joint/) if you want to dynamically control length.