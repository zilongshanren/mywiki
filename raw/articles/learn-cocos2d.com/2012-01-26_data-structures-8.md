---
title: Data Structures
url: http://www.learn-cocos2d.com/api-ref/1.0/Chipmunk/html/group__cp_damped_rotary_spring/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Data Structures
|
| struct | [cpDampedRotarySpring](/) |
Typedefs
|
typedef [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3)(* | [cpDampedRotarySpringTorqueFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_damped_rotary_spring/#ga27ca887de53076daf6d9e849d6f9838a) )(struct [cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) *spring, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) relativeAngle) |
Functions
|
const [cpConstraintClass](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint_class/) * | [cpDampedRotarySpringGetClass](../../../../../api-ref/1.0/Chipmunk/html/group__cp_damped_rotary_spring/#gae8c9008c7a9d5062e65db11eaa172731) (void) |
[cpDampedRotarySpring](/) * | [cpDampedRotarySpringAlloc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_damped_rotary_spring/#ga391ec6d5c1f7ebdd3d6aeaab1b525ece) (void) |
| | Allocate a damped rotary spring.
|
[cpDampedRotarySpring](/) * | [cpDampedRotarySpringInit](../../../../../api-ref/1.0/Chipmunk/html/group__cp_damped_rotary_spring/#gab1f484430f16708612d3972bea21abc0) ([cpDampedRotarySpring](/) *joint, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *a, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *b, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) restAngle, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) stiffness, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) damping) |
| | Initialize a damped rotary spring.
|
[cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) * | [cpDampedRotarySpringNew](../../../../../api-ref/1.0/Chipmunk/html/group__cp_damped_rotary_spring/#ga40e595bc6e077304ad3857c80118c5a4) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *a, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *b, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) restAngle, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) stiffness, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) damping) |
| | Allocate and initialize a damped rotary spring.
|
| | [CP_DefineConstraintProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_damped_rotary_spring/#ga6b2c40f12f53ce8d9160ca6f8ce0de9c) ([cpDampedRotarySpring](/), [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), restAngle, RestAngle) |
| | [CP_DefineConstraintProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_damped_rotary_spring/#ga66315d4a92960b96b665ef757e30a50e) ([cpDampedRotarySpring](/), [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), stiffness, Stiffness) |
| | [CP_DefineConstraintProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_damped_rotary_spring/#gaf40ee9adfc5a1f2e3343d2a6ae332456) ([cpDampedRotarySpring](/), [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), damping, Damping) |
| | [CP_DefineConstraintProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_damped_rotary_spring/#gaf637f9984acb284b5634d936de8cff2f) ([cpDampedRotarySpring](/), [cpDampedRotarySpringTorqueFunc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_damped_rotary_spring/#ga27ca887de53076daf6d9e849d6f9838a), springTorqueFunc, SpringTorqueFunc) |