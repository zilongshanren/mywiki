---
title: Data Structures
url: http://www.learn-cocos2d.com/api-ref/1.0/Chipmunk/html/group__cp_slide_joint/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Data Structures
|
| struct | [cpSlideJoint](/) |
Functions
|
const [cpConstraintClass](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint_class/) * | [cpSlideJointGetClass](../../../../../api-ref/1.0/Chipmunk/html/group__cp_slide_joint/#ga97803192c86266c6c73fb80d13a5fe8e) (void) |
[cpSlideJoint](/) * | [cpSlideJointAlloc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_slide_joint/#ga57404455797d03603bf166f7ac1733b3) (void) |
| | Allocate a slide joint.
|
[cpSlideJoint](/) * | [cpSlideJointInit](../../../../../api-ref/1.0/Chipmunk/html/group__cp_slide_joint/#ga81bbc2ad25d62519d90faaeea717794a) ([cpSlideJoint](/) *joint, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *a, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *b, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) anchr1, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) anchr2, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) min, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) max) |
| | Initialize a slide joint.
|
[cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) * | [cpSlideJointNew](../../../../../api-ref/1.0/Chipmunk/html/group__cp_slide_joint/#ga9f462bb5e5dac55d3cc37977cdc30fc5) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *a, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *b, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) anchr1, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) anchr2, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) min, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) max) |
| | Allocate and initialize a slide joint.
|
| | [CP_DefineConstraintProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_slide_joint/#ga79e995baca35c59c2f76dea4ec943750) ([cpSlideJoint](/), [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/), anchr1, Anchr1) |
| | [CP_DefineConstraintProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_slide_joint/#ga8580ff73a9b8266d0d805c75e62d56c7) ([cpSlideJoint](/), [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/), anchr2, Anchr2) |
| | [CP_DefineConstraintProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_slide_joint/#ga0b9abda09b79ac095341b67b0bb42430) ([cpSlideJoint](/), [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), min, Min) |
| | [CP_DefineConstraintProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_slide_joint/#ga6570398df2bd9a12c90d9466102d3312) ([cpSlideJoint](/), [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), max, Max) |