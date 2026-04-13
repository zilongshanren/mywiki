---
title: Data Structures
url: http://www.learn-cocos2d.com/api-ref/1.0/Chipmunk/html/group__cp_gear_joint/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Data Structures
|
| struct | [cpGearJoint](/) |
Functions
|
const [cpConstraintClass](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint_class/) * | [cpGearJointGetClass](../../../../../api-ref/1.0/Chipmunk/html/group__cp_gear_joint/#ga91c50bbc5352385ba427177b31e75d3c) (void) |
[cpGearJoint](/) * | [cpGearJointAlloc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_gear_joint/#gaa2c7e23592c34b5a4ce2614147bb2199) (void) |
| | Allocate a gear joint.
|
[cpGearJoint](/) * | [cpGearJointInit](../../../../../api-ref/1.0/Chipmunk/html/group__cp_gear_joint/#ga80357534ab155c34491b87e8534547a3) ([cpGearJoint](/) *joint, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *a, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *b, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) phase, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) ratio) |
| | Initialize a gear joint.
|
[cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) * | [cpGearJointNew](../../../../../api-ref/1.0/Chipmunk/html/group__cp_gear_joint/#ga4e2d47ad6065e8449636509835e959fa) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *a, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *b, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) phase, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) ratio) |
| | Allocate and initialize a gear joint.
|
| | [CP_DefineConstraintProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_gear_joint/#ga4c486e7dd54ae95cb49c3f632fe86a23) ([cpGearJoint](/), [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), phase, Phase) |
| | [CP_DefineConstraintGetter](../../../../../api-ref/1.0/Chipmunk/html/group__cp_gear_joint/#ga2cb0c3afb8fcec09ea5210f150167957) ([cpGearJoint](/), [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), ratio, Ratio) |
| void | [cpGearJointSetRatio](../../../../../api-ref/1.0/Chipmunk/html/group__cp_gear_joint/#ga936cd92e0eaf29ce86bf3be3392a9db6) ([cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) *constraint, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) value) |
| | Set the ratio of a gear joint.
|