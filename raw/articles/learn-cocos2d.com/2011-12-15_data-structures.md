---
title: Data Structures
url: http://www.learn-cocos2d.com/api-ref/1.0/Chipmunk/html/group__cp_damped_spring/
published: '2011-12-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Data Structures
|
| struct | [cpDampedSpring](/) |
Typedefs
|
typedef [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3)(* | [cpDampedSpringForceFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_damped_spring/#ga8c832b87ce13dbcada285305105486e0) )([cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) *spring, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) dist) |
Functions
|
const [cpConstraintClass](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint_class/) * | [cpDampedSpringGetClass](../../../../../api-ref/1.0/Chipmunk/html/group__cp_damped_spring/#ga9fce9c31c478d94d66112c34c2283eba) () |
[cpDampedSpring](/) * | [cpDampedSpringAlloc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_damped_spring/#ga09c3c3729dd0e2b920948afa15cbd9e1) (void) |
| | Allocate a damped spring.
|
[cpDampedSpring](/) * | [cpDampedSpringInit](../../../../../api-ref/1.0/Chipmunk/html/group__cp_damped_spring/#gac85a83615b67b539dddb16929e494c36) ([cpDampedSpring](/) *joint, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *a, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *b, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) anchr1, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) anchr2, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) restLength, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) stiffness, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) damping) |
| | Initialize a damped spring.
|
[cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) * | [cpDampedSpringNew](../../../../../api-ref/1.0/Chipmunk/html/group__cp_damped_spring/#gacc53f549a34c60819a0f50e523edc553) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *a, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *b, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) anchr1, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) anchr2, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) restLength, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) stiffness, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) damping) |
| | Allocate and initialize a damped spring.
|
| | [CP_DefineConstraintProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_damped_spring/#ga89eb413fd5dcd69b0c47a686b2120fe8) ([cpDampedSpring](/), [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/), anchr1, Anchr1) |
| | [CP_DefineConstraintProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_damped_spring/#ga0a51bfb999473c11436a01756e9c4bb1) ([cpDampedSpring](/), [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/), anchr2, Anchr2) |
| | [CP_DefineConstraintProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_damped_spring/#ga9fd85c0fe65fe4cc978d24f463987e57) ([cpDampedSpring](/), [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), restLength, RestLength) |
| | [CP_DefineConstraintProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_damped_spring/#gaf34c0b05c75ddb16a739a8d41f7690d0) ([cpDampedSpring](/), [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), stiffness, Stiffness) |
| | [CP_DefineConstraintProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_damped_spring/#ga02f7796e53397832f73d5937174e3943) ([cpDampedSpring](/), [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), damping, Damping) |
| | [CP_DefineConstraintProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_damped_spring/#ga50c06dfa6f29de2b51daf5eca9e907ca) ([cpDampedSpring](/), [cpDampedSpringForceFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_damped_spring/#ga8c832b87ce13dbcada285305105486e0), springForceFunc, SpringForceFunc) |