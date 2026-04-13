---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest/Box2D/html/classb2_weld_joint/
published: '2011-12-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Public Member Functions
|
[b2Vec2](../../../../../api-ref/latest/Box2D/html/structb2_vec2/) | [GetAnchorA](../../../../../api-ref/latest/Box2D/html/classb2_weld_joint/#a8550de74e174a08856bc4bc7a4853429) () const |
| | Get the anchor point on bodyA in world coordinates.
|
[b2Vec2](../../../../../api-ref/latest/Box2D/html/structb2_vec2/) | [GetAnchorB](../../../../../api-ref/latest/Box2D/html/classb2_weld_joint/#a2030794df9b2a3111bcf7a1eb0593960) () const |
| | Get the anchor point on bodyB in world coordinates.
|
[b2Vec2](../../../../../api-ref/latest/Box2D/html/structb2_vec2/) | [GetReactionForce](../../../../../api-ref/latest/Box2D/html/classb2_weld_joint/#a2ca6323d03b9fd4b591a0bfadddc25a8) (float32 inv_dt) const |
| | Get the reaction force on bodyB at the joint anchor in Newtons.
|
| float32 | [GetReactionTorque](../../../../../api-ref/latest/Box2D/html/classb2_weld_joint/#a7199b5cce47b29624b4b231d78af71a3) (float32 inv_dt) const |
| | Get the reaction torque on bodyB in N*m.
|
const [b2Vec2](../../../../../api-ref/latest/Box2D/html/structb2_vec2/) & | [GetLocalAnchorA](../../../../../api-ref/latest/Box2D/html/classb2_weld_joint/#aaef4f238fb5badf1112321ba878e8b06) () const |
| | The local anchor point relative to bodyA's origin.
|
const [b2Vec2](../../../../../api-ref/latest/Box2D/html/structb2_vec2/) & | [GetLocalAnchorB](../../../../../api-ref/latest/Box2D/html/classb2_weld_joint/#a7fdc0c047dc04bbc8c5ca67011be071c) () const |
| | The local anchor point relative to bodyB's origin.
|
| float32 | [GetReferenceAngle](../../../../../api-ref/latest/Box2D/html/classb2_weld_joint/#a0d347bf22be13aa8a96f615e230b095a) () const |
| | Get the reference angle.
|
| void | [SetFrequency](../../../../../api-ref/latest/Box2D/html/classb2_weld_joint/#a0796404379b7562f1af557729085c447) (float32 hz) |
| | Set/get frequency in Hz.
|
float32 | **GetFrequency** () const |
| void | [SetDampingRatio](../../../../../api-ref/latest/Box2D/html/classb2_weld_joint/#aea79865e590edba09eff9d2243689967) (float32 ratio) |
| | Set/get damping ratio.
|
float32 | **GetDampingRatio** () const |
| void | [Dump](../../../../../api-ref/latest/Box2D/html/classb2_weld_joint/#a2fd073c5e6264e98592240308a006981) () |
| | Dump to b2Log.
|
Protected Member Functions
|
| **b2WeldJoint** (const [b2WeldJointDef](../../../../../api-ref/latest/Box2D/html/structb2_weld_joint_def/) *def) |
void | **InitVelocityConstraints** (const [b2SolverData](../../../../../api-ref/latest/Box2D/html/structb2_solver_data/) &data) |
void | **SolveVelocityConstraints** (const [b2SolverData](../../../../../api-ref/latest/Box2D/html/structb2_solver_data/) &data) |
bool | **SolvePositionConstraints** (const [b2SolverData](../../../../../api-ref/latest/Box2D/html/structb2_solver_data/) &data) |
Protected Attributes
|
float32 | **m_frequencyHz** |
float32 | **m_dampingRatio** |
float32 | **m_bias** |
[b2Vec2](../../../../../api-ref/latest/Box2D/html/structb2_vec2/) | **m_localAnchorA** |
[b2Vec2](../../../../../api-ref/latest/Box2D/html/structb2_vec2/) | **m_localAnchorB** |
float32 | **m_referenceAngle** |
float32 | **m_gamma** |
[b2Vec3](../../../../../api-ref/latest/Box2D/html/structb2_vec3/) | **m_impulse** |
int32 | **m_indexA** |
int32 | **m_indexB** |
[b2Vec2](../../../../../api-ref/latest/Box2D/html/structb2_vec2/) | **m_rA** |
[b2Vec2](../../../../../api-ref/latest/Box2D/html/structb2_vec2/) | **m_rB** |
[b2Vec2](../../../../../api-ref/latest/Box2D/html/structb2_vec2/) | **m_localCenterA** |
[b2Vec2](../../../../../api-ref/latest/Box2D/html/structb2_vec2/) | **m_localCenterB** |
float32 | **m_invMassA** |
float32 | **m_invMassB** |
float32 | **m_invIA** |
float32 | **m_invIB** |
[b2Mat33](../../../../../api-ref/latest/Box2D/html/structb2_mat33/) | **m_mass** |
Friends
|
class | **b2Joint** |

A weld joint essentially glues two bodies together. A weld joint may distort somewhat because the island constraint solver is approximate.