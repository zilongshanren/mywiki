---
title: Data Structures
url: http://www.learn-cocos2d.com/api-ref/1.0/Chipmunk/html/group__cp_body/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Data Structures
|
| struct | [cpComponentNode](../../../../../api-ref/1.0/Chipmunk/html/structcp_component_node/) |
| struct | [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) |
| | Chipmunk's rigid body struct. [More...](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/#details)
|
Defines
|
| #define | [cpBodyAssertSane](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga135d8e824aade5d6923910593cfb1b4e)(body) cpBodySanityCheck(body) |
| #define | [CP_DefineBodyStructGetter](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga40c9bac4cf4b0637f64cb53402413d68)(type, member, name) static inline type cpBodyGet##name(const [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body){return body->member;} |
| #define | [CP_DefineBodyStructSetter](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga3a4a3ce737d391609355e0d9ba5fb2b6)(type, member, name) |
| #define | [CP_DefineBodyStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#gaa3f9cc97ed101b1e8f3100db601bb9e8)(type, member, name) |
Typedefs
|
| typedef void(* | [cpBodyVelocityFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga728eb52bef6367e8e33abff7dba0a089) )([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) gravity, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) damping, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) dt) |
| | Rigid body velocity update function type.
|
| typedef void(* | [cpBodyPositionFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga4f84c8fc20fcb9918d1553e6dc29ffbd) )([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) dt) |
| | Rigid body position update function type.
|
| typedef void(* | [cpBodyShapeIteratorFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga2a71c91a297ece9ab06101df4b726645) )([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, [cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape, void *data) |
| | Body/shape iterator callback function type.
|
| typedef void(* | [cpBodyConstraintIteratorFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga79c674e7767d6ff8769a9676404f589b) )([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, [cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) *constraint, void *data) |
| | Body/constraint iterator callback function type.
|
| typedef void(* | [cpBodyArbiterIteratorFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#gacdd17a9f98ca6e6c088b72f7d5f32ea3) )([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, [cpArbiter](../../../../../api-ref/1.0/Chipmunk/html/structcp_arbiter/) *arbiter, void *data) |
| | Body/arbiter iterator callback function type.
|
Functions
|
[cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) * | [cpBodyAlloc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#gadd622b6503c89fa5a8c0f43a0917d2a2) (void) |
| | Allocate a [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/).
|
[cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) * | [cpBodyInit](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#gad91c665ae18b191e8de5f59e1e20eea9) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) m, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) i) |
| | Initialize a [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/).
|
[cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) * | [cpBodyNew](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga0d0be6b47dee41b4989f5feebc7a5ce4) ([cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) m, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) i) |
| | Allocate and initialize a [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/).
|
[cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) * | [cpBodyInitStatic](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#gad9c3073c3fc9f0c0acd29a32761868c2) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body) |
| | Initialize a static [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/).
|
[cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) * | [cpBodyNewStatic](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#gaef08bd4d7afd793e859f5d7b1001344c) (void) |
| | Allocate and initialize a static [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/).
|
| void | [cpBodyDestroy](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga7691fd53f979e5f1e23fbdbc7b0ab31a) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body) |
| | Destroy a [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/).
|
| void | [cpBodyFree](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#gab122c9fc675a7f2cb6a644a1532c60f7) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body) |
| | Destroy and free a [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/).
|
| void | [cpBodySanityCheck](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga21607229d9fd49281a7a94a1b09664de) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body) |
| | Check that the properties of a body is sane. (Only in debug mode)
|
| void | [cpBodyActivate](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga9f6b2af6329a2b5c32712576719d357a) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body) |
| | Wake up a sleeping or idle body.
|
| void | [cpBodyActivateStatic](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#gaad8cfcc01f2a5a4ab4e98c49e2442063) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, [cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *filter) |
| | Wake up any sleeping or idle bodies touching a static body.
|
| void | [cpBodySleep](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga7308ff2bd6dc2832230636c02c682e82) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body) |
| | Force a body to fall asleep immediately.
|
| void | [cpBodySleepWithGroup](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#gaaa53f3fb37c705c4fbbd5b607f29c721) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *group) |
| | Force a body to fall asleep immediately along with other bodies in a group.
|
static [cpBool](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gab6e5d8afee598a57cd323abae5310244) | [cpBodyIsSleeping](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga2afd48688917d7a6195491cfbc54308b) (const [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body) |
| | Returns true if the body is sleeping.
|
static [cpBool](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gab6e5d8afee598a57cd323abae5310244) | [cpBodyIsStatic](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#gae3c21f961351c27c353a81736f6ef762) (const [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body) |
| | Returns true if the body is static.
|
static [cpBool](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gab6e5d8afee598a57cd323abae5310244) | [cpBodyIsRogue](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#gad33ab414d9ed851ef5a5b58c968c7bc2) (const [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body) |
| | Returns true if the body has not been added to a space.
|
| | [CP_DefineBodyStructGetter](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#gaa236a09dae6ecfcb52f214ab11310b5e) ([cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), m, Mass) |
| void | [cpBodySetMass](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga53196d6e67fdc55389418aebe0b8b127) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) m) |
| | Set the mass of a body.
|
| | [CP_DefineBodyStructGetter](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#gaffb5741a3cd422d3b13de1c73233589f) ([cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), i, Moment) |
| void | [cpBodySetMoment](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga39dd86643a700fb93198433174819d1a) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) i) |
| | Set the moment of a body.
|
| | [CP_DefineBodyStructGetter](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#gacdb522ceeec72c2841d02b4f0a654cf2) ([cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/), p, Pos) |
| void | [cpBodySetPos](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga33a86c1892ac7538a957057aacdb8394) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) pos) |
| | Set the position of a body.
|
| | [CP_DefineBodyStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga06836fc6d3a469f71b29d1a807fd21b9) ([cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/), v, Vel) |
| | [CP_DefineBodyStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga82664ae9e745f49c943d44f52692030f) ([cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/), f, Force) |
| | [CP_DefineBodyStructGetter](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga29cab67eba50aae659b5e2eb985d862f) ([cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), a, Angle) |
| void | [cpBodySetAngle](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga12b736a5d91e31dba48cadb71111674b) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) a) |
| | Set the angle of a body.
|
| | [CP_DefineBodyStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga61a2df3919f6dc5d2d8dab40b2974f15) ([cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), w, AngVel) |
| | [CP_DefineBodyStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga1741f22148607c7081c47a1a90045bfc) ([cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), t, Torque) |
| | [CP_DefineBodyStructGetter](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga8417c8caf37baf1c5174ca8d13ba5818) ([cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/), rot, Rot) |
| | [CP_DefineBodyStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#gae5aa4a1692c1e7db17c827d9d1c657d9) ([cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), v_limit, VelLimit) |
| | [CP_DefineBodyStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga0329c67204890353458cb81d43d39121) ([cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), w_limit, AngVelLimit) |
| | [CP_DefineBodyStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga8f41700360d682918981dc2aa7db7ed6) ([cpDataPointer](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#ga2ac2c3c31e21893941f9e4f8ee279447), data, UserData) |
| void | [cpBodyUpdateVelocity](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#gac62dea8fe94b2b405665f8b7c373d4d1) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) gravity, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) damping, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) dt) |
| | Default Integration functions.
|
| void | [cpBodyUpdatePosition](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#gaa42e82480140a790aabbe72b71ee929b) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) dt) |
static [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) | [cpBodyLocal2World](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga379bf6ddaf4ac904a62361effc068f38) (const [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v) |
| | Convert body relative/local coordinates to absolute/world coordinates.
|
static [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) | [cpBodyWorld2Local](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga6a93f6d4bb193db00dc766ebdc2e0919) (const [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v) |
| | Convert body absolute/world coordinates to relative/local coordinates.
|
| void | [cpBodyResetForces](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga55cecf4d82aa37cd626c2c208de48801) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body) |
| | Set the forces and torque or a body to zero.
|
| void | [cpBodyApplyForce](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga201b11a766af3d8471ceaa3ae2ae85c9) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) f, const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) r) |
| | Apply an force (in world coordinates) to the body at a point relative to the center of gravity (also in world coordinates).
|
| void | [cpBodyApplyImpulse](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga1759ee27171704c75564ca3a414cf730) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) j, const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) r) |
| | Apply an impulse (in world coordinates) to the body at a point relative to the center of gravity (also in world coordinates).
|
[cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) | [cpBodyGetVelAtWorldPoint](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#gad805b6e8a23a49428642295238d7bb9b) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) point) |
| | Get the velocity on a body (in world units) at a point on the body in world coordinates.
|
[cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) | [cpBodyGetVelAtLocalPoint](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga00ceb0eede2419e84eb7e4b107fa0bd3) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) point) |
| | Get the velocity on a body (in world units) at a point on the body in local coordinates.
|
static [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) | [cpBodyKineticEnergy](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#gae2547e7ef9f240e30b2c07d1005d0d58) (const [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body) |
| | Get the kinetic energy of a body.
|
| void | [cpBodyEachShape](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga51f56b6099dc8321ce284ecc6241b285) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, [cpBodyShapeIteratorFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga2a71c91a297ece9ab06101df4b726645) func, void *data) |
| | Call `func` once for each shape attached to `body` and added to the space.
|
| void | [cpBodyEachConstraint](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga377e83841ec8a67ca93685cb0bd6525e) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, [cpBodyConstraintIteratorFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga79c674e7767d6ff8769a9676404f589b) func, void *data) |
| | Call `func` once for each constraint attached to `body` and added to the space.
|
| void | [cpBodyEachArbiter](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#gacc958b3adad795e718682bea830d4135) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, [cpBodyArbiterIteratorFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#gacdd17a9f98ca6e6c088b72f7d5f32ea3) func, void *data) |
| | Call `func` once for each arbiter that is currently active on the body.
|

Chipmunk's rigid body type. Rigid bodies hold the physical properties of an object like it's mass, and position and velocity of it's center of gravity. They don't have an shape on their own. They are given a shape by creating collision shapes ([cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/)) that point to the body.