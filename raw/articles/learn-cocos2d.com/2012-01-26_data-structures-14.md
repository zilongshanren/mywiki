---
title: Data Structures
url: http://www.learn-cocos2d.com/api-ref/1.0/Chipmunk/html/group__cp_rotary_limit_joint/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Data Structures
|
| struct | [cpRotaryLimitJoint](/) |
Functions
|
const [cpConstraintClass](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint_class/) * | [cpRotaryLimitJointGetClass](../../../../../api-ref/1.0/Chipmunk/html/group__cp_rotary_limit_joint/#ga580359c4412995333f183a3440d6152d) (void) |
[cpRotaryLimitJoint](/) * | [cpRotaryLimitJointAlloc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_rotary_limit_joint/#ga188c8abeede5f9f878ec7a04e6d9af9b) (void) |
| | Allocate a damped rotary limit joint.
|
[cpRotaryLimitJoint](/) * | [cpRotaryLimitJointInit](../../../../../api-ref/1.0/Chipmunk/html/group__cp_rotary_limit_joint/#ga3f849df8d2439c089147f48646f0a551) ([cpRotaryLimitJoint](/) *joint, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *a, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *b, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) min, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) max) |
| | Initialize a damped rotary limit joint.
|
[cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) * | [cpRotaryLimitJointNew](../../../../../api-ref/1.0/Chipmunk/html/group__cp_rotary_limit_joint/#gaaa34430075cb2b674d73c66b667a4a36) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *a, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *b, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) min, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) max) |
| | Allocate and initialize a damped rotary limit joint.
|
| | [CP_DefineConstraintProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_rotary_limit_joint/#gac0b926bada211778a91c00ebe80fa311) ([cpRotaryLimitJoint](/), [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), min, Min) |
| | [CP_DefineConstraintProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_rotary_limit_joint/#gaaf9d9862445877dce747448276a4d96d) ([cpRotaryLimitJoint](/), [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), max, Max) |