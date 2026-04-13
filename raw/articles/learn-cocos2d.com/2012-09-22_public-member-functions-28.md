---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.0/Box2D/html/classb2_pulley_joint/
published: '2012-09-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Public Member Functions
|
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | [GetAnchorA](../../../../../api-ref/2.0/Box2D/html/classb2_pulley_joint/#a05ac0d0d927e9541f08b07cb1bf9ec56) () const |
| | Get the anchor point on bodyA in world coordinates.
|
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | [GetAnchorB](../../../../../api-ref/2.0/Box2D/html/classb2_pulley_joint/#a5cc3596f683d621b9a885c2569ecd452) () const |
| | Get the anchor point on bodyB in world coordinates.
|
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | [GetReactionForce](../../../../../api-ref/2.0/Box2D/html/classb2_pulley_joint/#a38c174bf1cf1011063ff4c16556b331e) (float32 inv_dt) const |
| | Get the reaction force on bodyB at the joint anchor in Newtons.
|
| float32 | [GetReactionTorque](../../../../../api-ref/2.0/Box2D/html/classb2_pulley_joint/#a418b200055623474c44742b1342dd278) (float32 inv_dt) const |
| | Get the reaction torque on bodyB in N*m.
|
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | [GetGroundAnchorA](../../../../../api-ref/2.0/Box2D/html/classb2_pulley_joint/#a19eefa28d2647882406ea9bfe2850a9e) () const |
| | Get the first ground anchor.
|
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | [GetGroundAnchorB](../../../../../api-ref/2.0/Box2D/html/classb2_pulley_joint/#a1b49d0dbce802f19711a9ab6d7dadfee) () const |
| | Get the second ground anchor.
|
| float32 | [GetLengthA](../../../../../api-ref/2.0/Box2D/html/classb2_pulley_joint/#a6b4c2e5cb4f5da48fcb074c7b5988084) () const |
| | Get the current length of the segment attached to bodyA.
|
| float32 | [GetLengthB](../../../../../api-ref/2.0/Box2D/html/classb2_pulley_joint/#abc7f31a35c6fb32647fd15d57e4ce60c) () const |
| | Get the current length of the segment attached to bodyB.
|
| float32 | [GetRatio](../../../../../api-ref/2.0/Box2D/html/classb2_pulley_joint/#a625685e60d95b7c5a725e8586d146752) () const |
| | Get the pulley ratio.
|
| void | [Dump](../../../../../api-ref/2.0/Box2D/html/classb2_pulley_joint/#ad12d0e03b5d07b2f8af1005c95c67aa2) () |
| | Dump joint to dmLog.
|
Protected Member Functions
|
| **b2PulleyJoint** (const [b2PulleyJointDef](../../../../../api-ref/2.0/Box2D/html/structb2_pulley_joint_def/) *data) |
void | **InitVelocityConstraints** (const [b2SolverData](../../../../../api-ref/2.0/Box2D/html/structb2_solver_data/) &data) |
void | **SolveVelocityConstraints** (const [b2SolverData](../../../../../api-ref/2.0/Box2D/html/structb2_solver_data/) &data) |
bool | **SolvePositionConstraints** (const [b2SolverData](../../../../../api-ref/2.0/Box2D/html/structb2_solver_data/) &data) |
Protected Attributes
|
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_groundAnchorA** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_groundAnchorB** |
float32 | **m_lengthA** |
float32 | **m_lengthB** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_localAnchorA** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_localAnchorB** |
float32 | **m_constant** |
float32 | **m_ratio** |
float32 | **m_impulse** |
int32 | **m_indexA** |
int32 | **m_indexB** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_uA** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_uB** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_rA** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_rB** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_localCenterA** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_localCenterB** |
float32 | **m_invMassA** |
float32 | **m_invMassB** |
float32 | **m_invIA** |
float32 | **m_invIB** |
float32 | **m_mass** |
Friends
|
class | **b2Joint** |

The pulley joint is connected to two bodies and two fixed ground points. The pulley supports a ratio such that: length1 + ratio * length2 <= constant Yes, the force transmitted is scaled by the ratio. Warning: the pulley joint can get a bit squirrelly by itself. They often work better when combined with prismatic joints. You should also cover the the anchor points with static shapes to prevent one side from going to zero length.