---
title: Data Structures
url: http://www.learn-cocos2d.com/api-ref/1.0/Chipmunk/html/group__cp_ratchet_joint/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Data Structures
|
| struct | [cpRatchetJoint](/) |
Functions
|
const [cpConstraintClass](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint_class/) * | [cpRatchetJointGetClass](../../../../../api-ref/1.0/Chipmunk/html/group__cp_ratchet_joint/#gac3f33d6588e1d60492029c8e8cdb6939) (void) |
[cpRatchetJoint](/) * | [cpRatchetJointAlloc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_ratchet_joint/#gadee71c6fb85f91900f4aea640269c7a4) (void) |
| | Allocate a ratchet joint.
|
[cpRatchetJoint](/) * | [cpRatchetJointInit](../../../../../api-ref/1.0/Chipmunk/html/group__cp_ratchet_joint/#ga712d5ebfd8200a2baaf99640d844224f) ([cpRatchetJoint](/) *joint, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *a, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *b, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) phase, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) ratchet) |
| | Initialize a ratched joint.
|
[cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) * | [cpRatchetJointNew](../../../../../api-ref/1.0/Chipmunk/html/group__cp_ratchet_joint/#ga6743e0aee6389ecc2bc10ee42e5baaec) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *a, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *b, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) phase, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) ratchet) |
| | Allocate and initialize a ratchet joint.
|
| | [CP_DefineConstraintProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_ratchet_joint/#gaaf8b2f70cd5b8c7f989e79b0239d5e50) ([cpRatchetJoint](/), [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), angle, Angle) |
| | [CP_DefineConstraintProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_ratchet_joint/#ga02c130c9070cb7672dcb3e1e0116328f) ([cpRatchetJoint](/), [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), phase, Phase) |
| | [CP_DefineConstraintProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_ratchet_joint/#ga5968c7ba3bfe20c48f32194d110472f0) ([cpRatchetJoint](/), [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), ratchet, Ratchet) |