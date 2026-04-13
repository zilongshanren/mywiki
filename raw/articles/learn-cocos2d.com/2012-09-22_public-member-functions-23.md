---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.0/Box2D/html/classb2_mouse_joint/
published: '2012-09-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Public Member Functions
|
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | [GetAnchorA](../../../../../api-ref/2.0/Box2D/html/classb2_mouse_joint/#a9db1c131fde2d11e61c6ccee9c28219b) () const |
| | Implements [b2Joint](../../../../../api-ref/2.0/Box2D/html/classb2_joint/).
|
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | [GetAnchorB](../../../../../api-ref/2.0/Box2D/html/classb2_mouse_joint/#a0db991ec36238105eb481f75e9b6161a) () const |
| | Implements [b2Joint](../../../../../api-ref/2.0/Box2D/html/classb2_joint/).
|
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | [GetReactionForce](../../../../../api-ref/2.0/Box2D/html/classb2_mouse_joint/#ab8e07dbed9d24c1c046d1ede60930c52) (float32 inv_dt) const |
| | Implements [b2Joint](../../../../../api-ref/2.0/Box2D/html/classb2_joint/).
|
| float32 | [GetReactionTorque](../../../../../api-ref/2.0/Box2D/html/classb2_mouse_joint/#a68efbc617aa7f0a41578e0aea988d662) (float32 inv_dt) const |
| | Implements [b2Joint](../../../../../api-ref/2.0/Box2D/html/classb2_joint/).
|
| void | [SetTarget](../../../../../api-ref/2.0/Box2D/html/classb2_mouse_joint/#a96f34c1c990407eddbadf07ae359b1f3) (const [b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) &target) |
| | Use this to update the target point.
|
const [b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) & | **GetTarget** () const |
| void | [SetMaxForce](../../../../../api-ref/2.0/Box2D/html/classb2_mouse_joint/#a4beba6ea0827960fac2474563591c03a) (float32 force) |
| | Set/get the maximum force in Newtons.
|
float32 | **GetMaxForce** () const |
| void | [SetFrequency](../../../../../api-ref/2.0/Box2D/html/classb2_mouse_joint/#a8b37706535923637ca280c5a0467b14d) (float32 hz) |
| | Set/get the frequency in Hertz.
|
float32 | **GetFrequency** () const |
| void | [SetDampingRatio](../../../../../api-ref/2.0/Box2D/html/classb2_mouse_joint/#a648c8f3ecb82f4887c0eefcfe48cbd37) (float32 ratio) |
| | Set/get the damping ratio (dimensionless).
|
float32 | **GetDampingRatio** () const |
| void | [Dump](../../../../../api-ref/2.0/Box2D/html/classb2_mouse_joint/#ae3d3a46a0032c0e50f346e7f7129617f) () |
| | The mouse joint does not support dumping.
|
Protected Member Functions
|
| **b2MouseJoint** (const [b2MouseJointDef](../../../../../api-ref/2.0/Box2D/html/structb2_mouse_joint_def/) *def) |
void | **InitVelocityConstraints** (const [b2SolverData](../../../../../api-ref/2.0/Box2D/html/structb2_solver_data/) &data) |
void | **SolveVelocityConstraints** (const [b2SolverData](../../../../../api-ref/2.0/Box2D/html/structb2_solver_data/) &data) |
bool | **SolvePositionConstraints** (const [b2SolverData](../../../../../api-ref/2.0/Box2D/html/structb2_solver_data/) &data) |
Protected Attributes
|
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_localAnchorB** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_targetA** |
float32 | **m_frequencyHz** |
float32 | **m_dampingRatio** |
float32 | **m_beta** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_impulse** |
float32 | **m_maxForce** |
float32 | **m_gamma** |
int32 | **m_indexA** |
int32 | **m_indexB** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_rB** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_localCenterB** |
float32 | **m_invMassB** |
float32 | **m_invIB** |
[b2Mat22](../../../../../api-ref/2.0/Box2D/html/structb2_mat22/) | **m_mass** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_C** |
Friends
|
class | **b2Joint** |

A mouse joint is used to make a point on a body track a specified world point. This a soft constraint with a maximum force. This allows the constraint to stretch and without applying huge forces. NOTE: this joint is not documented in the manual because it was developed to be used in the testbed. If you want to learn how to use the mouse joint, look at the testbed.