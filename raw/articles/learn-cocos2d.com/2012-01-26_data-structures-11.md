---
title: Data Structures
url: http://www.learn-cocos2d.com/api-ref/1.0/Chipmunk/html/group__cp_pivot_joint/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Data Structures
|
| struct | [cpPivotJoint](/) |
Functions
|
const [cpConstraintClass](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint_class/) * | [cpPivotJointGetClass](../../../../../api-ref/1.0/Chipmunk/html/group__cp_pivot_joint/#ga4aa4683fe13b90d18cff73790ea8b3df) (void) |
[cpPivotJoint](/) * | [cpPivotJointAlloc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_pivot_joint/#gac8ceffcbb474ba0ba021dee02eca5a09) (void) |
| | Allocate a pivot joint.
|
[cpPivotJoint](/) * | [cpPivotJointInit](../../../../../api-ref/1.0/Chipmunk/html/group__cp_pivot_joint/#ga1b606a6beb26355a846196f0a5fb445f) ([cpPivotJoint](/) *joint, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *a, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *b, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) anchr1, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) anchr2) |
| | Initialize a pivot joint.
|
[cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) * | [cpPivotJointNew](../../../../../api-ref/1.0/Chipmunk/html/group__cp_pivot_joint/#ga56d3fd371a5f4688abcf0c279ad77a9d) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *a, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *b, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) pivot) |
| | Allocate and initialize a pivot joint.
|
[cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) * | [cpPivotJointNew2](../../../../../api-ref/1.0/Chipmunk/html/group__cp_pivot_joint/#ga40411f1879afc3910907a49faced47f0) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *a, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *b, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) anchr1, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) anchr2) |
| | Allocate and initialize a pivot joint with specific anchors.
|
| | [CP_DefineConstraintProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_pivot_joint/#ga154a2123d23aebaa6f3444cdf906cc95) ([cpPivotJoint](/), [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/), anchr1, Anchr1) |
| | [CP_DefineConstraintProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_pivot_joint/#ga8a53bde31bc7a0aadccb5ecfff7b969f) ([cpPivotJoint](/), [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/), anchr2, Anchr2) |