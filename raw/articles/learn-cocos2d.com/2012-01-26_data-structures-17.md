---
title: Data Structures
url: http://www.learn-cocos2d.com/api-ref/1.0/Chipmunk/html/group__cp_space/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Data Structures
|
| struct | [cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) |
| | Basic Unit of Simulation in Chipmunk. [More...](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/#details)
|
Defines
|
| #define | [CP_DefineSpaceStructGetter](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga4baa3370fb35f0ee69c554bc014f02b7)(type, member, name) static inline type cpSpaceGet##name(const [cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space){return space->member;} |
| #define | [CP_DefineSpaceStructSetter](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga044bac924cf9eb5142ec6df23d1031fb)(type, member, name) static inline void cpSpaceSet##name([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, type value){space->member = value;} |
| #define | [CP_DefineSpaceStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga432cdfcc68e6cdf7b049fb49786ebb9c)(type, member, name) |
Typedefs
|
typedef struct
[cpContactBufferHeader](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga0dcc2061b696a4f4563b6315d90651cd) | [cpContactBufferHeader](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga0dcc2061b696a4f4563b6315d90651cd) |
| typedef void(* | [cpSpaceArbiterApplyImpulseFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga5aacd6096c382bf106cf9c3f02ef0b17) )([cpArbiter](../../../../../api-ref/1.0/Chipmunk/html/structcp_arbiter/) *arb) |
| typedef void(* | [cpPostStepFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gaed3a8bcab71aa08be3dd839e5f4f1150) )([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, void *obj, void *data) |
| | Post Step callback function type.
|
| typedef void(* | [cpSpacePointQueryFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga6baa5a302b275b18516294fc3106ca58) )([cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape, void *data) |
| | Point query callback function type.
|
| typedef void(* | [cpSpaceSegmentQueryFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gad48eefc60cdccc027c68b1f696e75838) )([cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) t, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) n, void *data) |
| | Segment query callback function type.
|
| typedef void(* | [cpSpaceBBQueryFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga9f9d412c914ddec134554dde01dffbad) )([cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape, void *data) |
| | Rectangle Query callback function type.
|
| typedef void(* | [cpSpaceShapeQueryFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gaef86eb47a5ac16c373eb8b59599d1806) )([cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape, [cpContactPointSet](../../../../../api-ref/1.0/Chipmunk/html/structcp_contact_point_set/) *points, void *data) |
| | Shape query callback function type.
|
| typedef void(* | [cpSpaceBodyIteratorFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gac0cc4ac612fc81b31e3179b8a742570e) )([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, void *data) |
| | Space/body iterator callback function type.
|
| typedef void(* | [cpSpaceShapeIteratorFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga780ed0f29f957005efb4e24df64883b2) )([cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape, void *data) |
| | Space/body iterator callback function type.
|
| typedef void(* | [cpSpaceConstraintIteratorFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga6818e027bac76ed80432f12ffc8d7a39) )([cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) *constraint, void *data) |
| | Space/constraint iterator callback function type.
|
Functions
|
[cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) * | [cpSpaceAlloc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gaeed23237c8a7b052ec816b339c7e60dd) (void) |
| | Allocate a [cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/).
|
[cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) * | [cpSpaceInit](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga3e668d762b5b6438b51f7af0fb32ff09) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space) |
| | Initialize a [cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/).
|
[cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) * | [cpSpaceNew](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gac6293d85ec533d496e3005d194c1e62b) (void) |
| | Allocate and initialize a [cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/).
|
| void | [cpSpaceDestroy](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga964c2ec74cf2527fa17142b6009796c5) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space) |
| | Destroy a [cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/).
|
| void | [cpSpaceFree](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga1fe399459fcb74d30eb29a73af26cd0c) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space) |
| | Destroy and free a [cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/).
|
| | [CP_DefineSpaceStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gacd75c1817f1771e93d7797a77a2ae9a5) (int, iterations, Iterations) |
| | [CP_DefineSpaceStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga2cc455298ae4d2e61e4b72ba7ce1d6cc) ([cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/), gravity, Gravity) |
| | [CP_DefineSpaceStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga97a3f050b1e69e743bb1c334ff5390f7) ([cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), damping, Damping) |
| | [CP_DefineSpaceStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gaf6d6cb1d216d70ad5cdc0478e2baa8a1) ([cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), idleSpeedThreshold, IdleSpeedThreshold) |
| | [CP_DefineSpaceStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga9625a12a606986be45f6ab5a166ad5e7) ([cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), sleepTimeThreshold, SleepTimeThreshold) |
| | [CP_DefineSpaceStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga3f97432111eb3a82b71990d9830857d8) ([cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), collisionSlop, CollisionSlop) |
| | [CP_DefineSpaceStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gaed22cee5c758381924641491fd460d99) ([cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), collisionBias, CollisionBias) |
| | [CP_DefineSpaceStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga88ed6d3ded23d9d4057c7d27d883c3f7) ([cpTimestamp](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gaa24652c104082d0725066ea5ac7dc83f), collisionPersistence, CollisionPersistence) |
| | [CP_DefineSpaceStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gaec3e3cd8bf9085b337c51127a4acbbbf) ([cpBool](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gab6e5d8afee598a57cd323abae5310244), enableContactGraph, EnableContactGraph) |
| | [CP_DefineSpaceStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gab43a6e8110238aec2b25d2c80794d3bb) ([cpDataPointer](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#ga2ac2c3c31e21893941f9e4f8ee279447), data, UserData) |
| | [CP_DefineSpaceStructGetter](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga70139c1975fbb75392e87a2fdc824b3c) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *, staticBody, StaticBody) |
| | [CP_DefineSpaceStructGetter](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga1b5494c7616496f9a4a8a668c3e8dac4) ([cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), CP_PRIVATE(curr_dt), CurrentTimeStep) |
static [cpBool](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gab6e5d8afee598a57cd323abae5310244) | [cpSpaceIsLocked](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga3f84a5d9ddb46c91b978364c43884aad) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space) |
| | returns true from inside a callback and objects cannot be added/removed.
|
| void | [cpSpaceSetDefaultCollisionHandler](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gada7583f907d492b00b3f7f73398ace7d) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpCollisionBeginFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_arbiter/#ga1abb3a86eb2889bf32349de4c8237612) begin, [cpCollisionPreSolveFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_arbiter/#ga00b9651732d9674c945334ed1968d19b) preSolve, [cpCollisionPostSolveFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_arbiter/#gaf66f0db756c55c5168b4956954af2f12) postSolve, [cpCollisionSeparateFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_arbiter/#ga70549bfa3ae4e806fa1afde420a71775) separate, void *data) |
| void | [cpSpaceAddCollisionHandler](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga4ba389406f5a498f5af8044386950d09) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpCollisionType](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gae83e2f50965eb441e36ffff1e32e6d02) a, [cpCollisionType](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gae83e2f50965eb441e36ffff1e32e6d02) b, [cpCollisionBeginFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_arbiter/#ga1abb3a86eb2889bf32349de4c8237612) begin, [cpCollisionPreSolveFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_arbiter/#ga00b9651732d9674c945334ed1968d19b) preSolve, [cpCollisionPostSolveFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_arbiter/#gaf66f0db756c55c5168b4956954af2f12) postSolve, [cpCollisionSeparateFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_arbiter/#ga70549bfa3ae4e806fa1afde420a71775) separate, void *data) |
| void | [cpSpaceRemoveCollisionHandler](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gaa1483dd8e784ad0c420d60db90aa9a03) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpCollisionType](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gae83e2f50965eb441e36ffff1e32e6d02) a, [cpCollisionType](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gae83e2f50965eb441e36ffff1e32e6d02) b) |
| | Unset a collision handler.
|
[cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) * | [cpSpaceAddShape](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga5fd6bdb0b93c93a93eeab0611e070080) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape) |
[cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) * | [cpSpaceAddStaticShape](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gab4c74f809628d9b8330f3e2259575759) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape) |
| | Explicity add a shape as a static shape to the simulation.
|
[cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) * | [cpSpaceAddBody](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga0aa27863e6410512b73347e25e97b215) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body) |
| | Add a rigid body to the simulation.
|
[cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) * | [cpSpaceAddConstraint](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gad3fc61e25869131d30dca7b1a33ba102) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) *constraint) |
| | Add a constraint to the simulation.
|
| void | [cpSpaceRemoveShape](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gaba39a56c766cf5094876685d7ed63734) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape) |
| | Remove a collision shape from the simulation.
|
| void | [cpSpaceRemoveStaticShape](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gacec20f95fdfcf59a6795ba60cc9c7e8a) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape) |
| | Remove a collision shape added using [cpSpaceAddStaticShape()](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gab4c74f809628d9b8330f3e2259575759) from the simulation.
|
| void | [cpSpaceRemoveBody](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gad2c0aab926b1796bb38deee21d8a9ef1) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body) |
| | Remove a rigid body from the simulation.
|
| void | [cpSpaceRemoveConstraint](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gae6a15d5809c8ca1cd786518b0198061b) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) *constraint) |
| | Remove a constraint from the simulation.
|
[cpBool](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gab6e5d8afee598a57cd323abae5310244) | [cpSpaceContainsShape](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga24236a160025c41df498804da57ebc08) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape) |
| | Test if a collision shape has been added to the space.
|
[cpBool](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gab6e5d8afee598a57cd323abae5310244) | [cpSpaceContainsBody](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga8aededc0029d164ebd419e6012a91034) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body) |
| | Test if a rigid body has been added to the space.
|
[cpBool](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gab6e5d8afee598a57cd323abae5310244) | [cpSpaceContainsConstraint](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga2e4cef3632535e485f1e0645e60c3ad2) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) *constraint) |
| | Test if a constraint has been added to the space.
|
| void | [cpSpaceAddPostStepCallback](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gab20b332d6030b699a66c753e1a868090) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpPostStepFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gaed3a8bcab71aa08be3dd839e5f4f1150) func, void *obj, void *data) |
| void | [cpSpacePointQuery](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gaa6e476502b5870cc410c153b3d0ba267) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) point, [cpLayers](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#ga5ec31e87ed3973cab80f9bfbbbcb43bb) layers, [cpGroup](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gacd811b1135a8f4a3e5cc019552b18b1a) group, [cpSpacePointQueryFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga6baa5a302b275b18516294fc3106ca58) func, void *data) |
| | Query the space at a point and call `func` for each shape found.
|
[cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) * | [cpSpacePointQueryFirst](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gae6d8d0f438041fa2d3a8197c8b9d1962) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) point, [cpLayers](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#ga5ec31e87ed3973cab80f9bfbbbcb43bb) layers, [cpGroup](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gacd811b1135a8f4a3e5cc019552b18b1a) group) |
| | Query the space at a point and return the first shape found. Returns NULL if no shapes were found.
|
| void | [cpSpaceSegmentQuery](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga26da8e0202d712d7bc3714332aff0ea6) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) start, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) end, [cpLayers](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#ga5ec31e87ed3973cab80f9bfbbbcb43bb) layers, [cpGroup](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gacd811b1135a8f4a3e5cc019552b18b1a) group, [cpSpaceSegmentQueryFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gad48eefc60cdccc027c68b1f696e75838) func, void *data) |
| | Perform a directed line segment query (like a raycast) against the space calling `func` for each shape intersected.
|
[cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) * | [cpSpaceSegmentQueryFirst](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga16901aee37e8830fe3900275a6a724aa) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) start, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) end, [cpLayers](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#ga5ec31e87ed3973cab80f9bfbbbcb43bb) layers, [cpGroup](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gacd811b1135a8f4a3e5cc019552b18b1a) group, [cpSegmentQueryInfo](../../../../../api-ref/1.0/Chipmunk/html/structcp_segment_query_info/) *out) |
| | Perform a directed line segment query (like a raycast) against the space and return the first shape hit. Returns NULL if no shapes were hit.
|
| void | [cpSpaceBBQuery](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga8cc12bf144da470f4ba42fe81f36b4e8) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) bb, [cpLayers](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#ga5ec31e87ed3973cab80f9bfbbbcb43bb) layers, [cpGroup](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gacd811b1135a8f4a3e5cc019552b18b1a) group, [cpSpaceBBQueryFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga9f9d412c914ddec134554dde01dffbad) func, void *data) |
[cpBool](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gab6e5d8afee598a57cd323abae5310244) | [cpSpaceShapeQuery](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga8415bcc9318df0a7e50e1e2cc612ccd2) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape, [cpSpaceShapeQueryFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gaef86eb47a5ac16c373eb8b59599d1806) func, void *data) |
| | Query a space for any shapes overlapping the given shape and call `func` for each shape found.
|
| void | [cpSpaceActivateShapesTouchingShape](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gad3e6bd83aa55c7ada13512c66c3740d3) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape) |
| | Call [cpBodyActivate()](../../../../../api-ref/1.0/Chipmunk/html/group__cp_body/#ga9f6b2af6329a2b5c32712576719d357a) for any shape that is overlaps the given shape.
|
| void | [cpSpaceEachBody](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gab526f8e9ea517058d4d90509e971120d) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpSpaceBodyIteratorFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gac0cc4ac612fc81b31e3179b8a742570e) func, void *data) |
| | Call `func` for each body in the space.
|
| void | [cpSpaceEachShape](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gac652c40a648d64651b4b36baab354802) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpSpaceShapeIteratorFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga780ed0f29f957005efb4e24df64883b2) func, void *data) |
| | Call `func` for each shape in the space.
|
| void | [cpSpaceEachConstraint](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gac388d8f773c2e080b214734af63a5b64) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpSpaceConstraintIteratorFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga6818e027bac76ed80432f12ffc8d7a39) func, void *data) |
| | Call `func` for each shape in the space.
|
| void | [cpSpaceReindexStatic](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gad703cfe24cb148c49c6dd30aa6b091ff) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space) |
| | Update the collision detection info for the static shapes in the space.
|
| void | [cpSpaceReindexShape](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga4dfab7bb0c43e49b321a5620c459f9d2) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape) |
| | Update the collision detection data for a specific shape in the space.
|
| void | [cpSpaceReindexShapesForBody](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#ga93a9cc05205923058aa6c2dcdaeb2d44) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body) |
| | Update the collision detection data for all shapes attached to a body.
|
| void | [cpSpaceUseSpatialHash](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gae80141ab89b21e48a10850c3e2c81e91) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) dim, int count) |
| | Switch the space to use a spatial has as it's spatial index.
|
| void | [cpSpaceStep](../../../../../api-ref/1.0/Chipmunk/html/group__cp_space/#gad8a6c8e7e99ae268af224aa199124706) ([cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) dt) |
| | Step the space forward in time by `dt` .
|