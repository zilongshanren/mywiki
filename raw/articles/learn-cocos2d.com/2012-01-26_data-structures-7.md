---
title: Data Structures
url: http://www.learn-cocos2d.com/api-ref/1.0/Chipmunk/html/group__cp_constraint/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Data Structures
|
| struct | [cpConstraintClass](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint_class/) |
| struct | [cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) |
| | Opaque [cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) struct. [More...](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/#details)
|
Defines
|
| #define | [CP_DefineConstraintStructGetter](../../../../../api-ref/1.0/Chipmunk/html/group__cp_constraint/#ga313a8c10c92b0df4b4080b7d02278c7d)(type, member, name) static inline type [cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/)##Get##name(const [cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) *constraint){return constraint->member;} |
| #define | [CP_DefineConstraintStructSetter](../../../../../api-ref/1.0/Chipmunk/html/group__cp_constraint/#gacbdb04c3e6b6ff8c3ec698c4c81a3336)(type, member, name) |
| #define | [CP_DefineConstraintStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_constraint/#ga11786f1e66966c01ac1132ef3a73d746)(type, member, name) |
Typedefs
|
| typedef void(* | [cpConstraintPreStepImpl](../../../../../api-ref/1.0/Chipmunk/html/group__cp_constraint/#gab9fdf23a539a013086b26833691ca0b3) )([cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) *constraint, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) dt) |
| typedef void(* | [cpConstraintApplyCachedImpulseImpl](../../../../../api-ref/1.0/Chipmunk/html/group__cp_constraint/#ga9dd4679120c0727934965a28ee052221) )([cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) *constraint, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) dt_coef) |
| typedef void(* | [cpConstraintApplyImpulseImpl](../../../../../api-ref/1.0/Chipmunk/html/group__cp_constraint/#gaf655df2bf54f07074f1c6e8513d4251a) )([cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) *constraint) |
typedef [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3)(* | [cpConstraintGetImpulseImpl](../../../../../api-ref/1.0/Chipmunk/html/group__cp_constraint/#ga4f3d31551af8127f7629c71d9bd147e2) )([cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) *constraint) |
| typedef void(* | [cpConstraintPreSolveFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_constraint/#ga31a2ad1ca9b9ecd4124a81b1292714e0) )([cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) *constraint, [cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space) |
| | Callback function type that gets called before solving a joint.
|
| typedef void(* | [cpConstraintPostSolveFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_constraint/#ga1adf3ccceb908229069aa2f10f21c1b1) )([cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) *constraint, [cpSpace](../../../../../api-ref/1.0/Chipmunk/html/structcp_space/) *space) |
| | Callback function type that gets called after solving a joint.
|
Functions
|
| void | [cpConstraintDestroy](../../../../../api-ref/1.0/Chipmunk/html/group__cp_constraint/#ga2c5c4d73886727485cb4d8c3e3ba1c15) ([cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) *constraint) |
| | Destroy a constraint.
|
| void | [cpConstraintFree](../../../../../api-ref/1.0/Chipmunk/html/group__cp_constraint/#ga396e66d86ca72615ed681dfed3673a6c) ([cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) *constraint) |
| | Destroy and free a constraint.
|
| | [CP_DefineConstraintStructGetter](../../../../../api-ref/1.0/Chipmunk/html/group__cp_constraint/#gaa612cf1719ce7ba55ba046736a202611) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *, a, A) |
| | [CP_DefineConstraintStructGetter](../../../../../api-ref/1.0/Chipmunk/html/group__cp_constraint/#gaa295274db549b2d8056c7550c120e704) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *, b, B) |
| | [CP_DefineConstraintStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_constraint/#gacef25d06bb0ef872851e288ac6f63601) ([cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), maxForce, MaxForce) |
| | [CP_DefineConstraintStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_constraint/#gac7ffa89c865fdd2d75e4d46d0872d1d7) ([cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), errorBias, ErrorBias) |
| | [CP_DefineConstraintStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_constraint/#ga5120c4d4892f4c757ce6f023bdb6f852) ([cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), maxBias, MaxBias) |
| | [CP_DefineConstraintStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_constraint/#ga71671dc916150cde54feea6f18c2ebbf) ([cpConstraintPreSolveFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_constraint/#ga31a2ad1ca9b9ecd4124a81b1292714e0), preSolve, PreSolveFunc) |
| | [CP_DefineConstraintStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_constraint/#ga28eea4d8a45cf1654b732e69e8ebcf66) ([cpConstraintPostSolveFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_constraint/#ga1adf3ccceb908229069aa2f10f21c1b1), postSolve, PostSolveFunc) |
| | [CP_DefineConstraintStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_constraint/#ga59c220183c04bb7528ba1217857aecd1) ([cpDataPointer](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#ga2ac2c3c31e21893941f9e4f8ee279447), data, UserData) |
static [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) | [cpConstraintGetImpulse](../../../../../api-ref/1.0/Chipmunk/html/group__cp_constraint/#ga80f2cadd6bea1002818ac104e3b91cbd) ([cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) *constraint) |