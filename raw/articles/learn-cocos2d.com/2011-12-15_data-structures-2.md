---
title: Data Structures
url: http://www.learn-cocos2d.com/api-ref/1.0/Chipmunk/html/group__cp_groove_joint/
published: '2011-12-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Data Structures
|
| struct | [cpGrooveJoint](../../../../../api-ref/1.0/Chipmunk/html/structcp_groove_joint/) |
Functions
|
const [cpConstraintClass](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint_class/) * | [cpGrooveJointGetClass](../../../../../api-ref/1.0/Chipmunk/html/group__cp_groove_joint/#ga0033d2106b051a83a9557aca63363c0c) () |
[cpGrooveJoint](../../../../../api-ref/1.0/Chipmunk/html/structcp_groove_joint/) * | [cpGrooveJointAlloc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_groove_joint/#ga019749a30c1717dda8166c55ea99c0d0) (void) |
| | Allocate a groove joint.
|
[cpGrooveJoint](../../../../../api-ref/1.0/Chipmunk/html/structcp_groove_joint/) * | [cpGrooveJointInit](../../../../../api-ref/1.0/Chipmunk/html/group__cp_groove_joint/#ga6a7be109a1d0aa14c2203e5d7b3e4118) ([cpGrooveJoint](../../../../../api-ref/1.0/Chipmunk/html/structcp_groove_joint/) *joint, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *a, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *b, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) groove_a, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) groove_b, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) anchr2) |
| | Initialize a groove joint.
|
[cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) * | [cpGrooveJointNew](../../../../../api-ref/1.0/Chipmunk/html/group__cp_groove_joint/#ga6a92f260d3ade2af1afad6848653dbb7) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *a, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *b, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) groove_a, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) groove_b, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) anchr2) |
| | Allocate and initialize a groove joint.
|
| | [CP_DefineConstraintGetter](../../../../../api-ref/1.0/Chipmunk/html/group__cp_groove_joint/#ga73ee1d541a69a541db1d433e9b6c9d4d) ([cpGrooveJoint](../../../../../api-ref/1.0/Chipmunk/html/structcp_groove_joint/), [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/), grv_a, GrooveA) |
| void | [cpGrooveJointSetGrooveA](../../../../../api-ref/1.0/Chipmunk/html/group__cp_groove_joint/#ga9295d2c19cc0a9f76058affc8bf5baec) ([cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) *constraint, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) value) |
| | Set endpoint a of a groove joint's groove.
|
| | [CP_DefineConstraintGetter](../../../../../api-ref/1.0/Chipmunk/html/group__cp_groove_joint/#ga1cbbb642a085440d087d73a70fb868ab) ([cpGrooveJoint](../../../../../api-ref/1.0/Chipmunk/html/structcp_groove_joint/), [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/), grv_b, GrooveB) |
| void | [cpGrooveJointSetGrooveB](../../../../../api-ref/1.0/Chipmunk/html/group__cp_groove_joint/#ga81e752c1da9c934a355e4d5f642d8477) ([cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) *constraint, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) value) |
| | Set endpoint b of a groove joint's groove.
|
| | [CP_DefineConstraintProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_groove_joint/#gaefc888b378b79de5dba9dc1a6b0da874) ([cpGrooveJoint](../../../../../api-ref/1.0/Chipmunk/html/structcp_groove_joint/), [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/), anchr2, Anchr2) |