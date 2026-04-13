---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.0/Box2D/html/classb2_distance_joint/
published: '2012-09-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Public Member Functions
|
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | [GetAnchorA](../../../../../api-ref/2.0/Box2D/html/classb2_distance_joint/#a66c1cb4deff1166c1dab67df6047a89c) () const |
| | Get the anchor point on bodyA in world coordinates.
|
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | [GetAnchorB](../../../../../api-ref/2.0/Box2D/html/classb2_distance_joint/#afc58d85cf7cc5e23082cf469e1a1a067) () const |
| | Get the anchor point on bodyB in world coordinates.
|
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | [GetReactionForce](../../../../../api-ref/2.0/Box2D/html/classb2_distance_joint/#a99413cc114b2f4dc4ce7693c062ce226) (float32 inv_dt) const |
| float32 | [GetReactionTorque](../../../../../api-ref/2.0/Box2D/html/classb2_distance_joint/#a8d65840abe0b398399020524852788fd) (float32 inv_dt) const |
const [b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) & | [GetLocalAnchorA](../../../../../api-ref/2.0/Box2D/html/classb2_distance_joint/#a75a41c40f21e48a6f9e947dd1dc46db4) () const |
| | The local anchor point relative to bodyA's origin.
|
const [b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) & | [GetLocalAnchorB](../../../../../api-ref/2.0/Box2D/html/classb2_distance_joint/#a22e9572c8b3d1f0619b340738811c082) () const |
| | The local anchor point relative to bodyB's origin.
|
| void | [SetLength](../../../../../api-ref/2.0/Box2D/html/classb2_distance_joint/#a950a0f187ef691208e50de40ed9223fe) (float32 length) |
float32 | **GetLength** () const |
| void | [SetFrequency](../../../../../api-ref/2.0/Box2D/html/classb2_distance_joint/#a1a12446f8926a1324edd481d9cd28c8a) (float32 hz) |
| | Set/get frequency in Hz.
|
float32 | **GetFrequency** () const |
| void | [SetDampingRatio](../../../../../api-ref/2.0/Box2D/html/classb2_distance_joint/#a58da61301a1f1398a715107b76649923) (float32 ratio) |
| | Set/get damping ratio.
|
float32 | **GetDampingRatio** () const |
| void | [Dump](../../../../../api-ref/2.0/Box2D/html/classb2_distance_joint/#a3cebcc6ccce6f3c24432cd130fd53517) () |
| | Dump joint to dmLog.
|
Protected Member Functions
|
| **b2DistanceJoint** (const [b2DistanceJointDef](../../../../../api-ref/2.0/Box2D/html/structb2_distance_joint_def/) *data) |
void | **InitVelocityConstraints** (const [b2SolverData](../../../../../api-ref/2.0/Box2D/html/structb2_solver_data/) &data) |
void | **SolveVelocityConstraints** (const [b2SolverData](../../../../../api-ref/2.0/Box2D/html/structb2_solver_data/) &data) |
bool | **SolvePositionConstraints** (const [b2SolverData](../../../../../api-ref/2.0/Box2D/html/structb2_solver_data/) &data) |
Protected Attributes
|
float32 | **m_frequencyHz** |
float32 | **m_dampingRatio** |
float32 | **m_bias** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_localAnchorA** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_localAnchorB** |
float32 | **m_gamma** |
float32 | **m_impulse** |
float32 | **m_length** |
int32 | **m_indexA** |
int32 | **m_indexB** |
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | **m_u** |
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

A distance joint constrains two points on two bodies to remain at a fixed distance from each other. You can view this as a massless, rigid rod.