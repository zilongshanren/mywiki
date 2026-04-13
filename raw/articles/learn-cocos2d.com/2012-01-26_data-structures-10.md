---
title: Data Structures
url: http://www.learn-cocos2d.com/api-ref/1.0/Chipmunk/html/group__cp_pin_joint/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Data Structures
|
| struct | [cpPinJoint](/) |
Functions
|
const [cpConstraintClass](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint_class/) * | [cpPinJointGetClass](../../../../../api-ref/1.0/Chipmunk/html/group__cp_pin_joint/#ga368588970ebb488aa22d9ea9b2574aeb) (void) |
[cpPinJoint](/) * | [cpPinJointAlloc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_pin_joint/#ga12e5fcaa7d39e47e6f1ac9777744fec5) (void) |
| | Allocate a pin joint.
|
[cpPinJoint](/) * | [cpPinJointInit](../../../../../api-ref/1.0/Chipmunk/html/group__cp_pin_joint/#ga43e7c4abdb1a3245f8a224cdab1052bb) ([cpPinJoint](/) *joint, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *a, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *b, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) anchr1, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) anchr2) |
| | Initialize a pin joint.
|
[cpConstraint](../../../../../api-ref/1.0/Chipmunk/html/structcp_constraint/) * | [cpPinJointNew](../../../../../api-ref/1.0/Chipmunk/html/group__cp_pin_joint/#ga4ad2cdd039d27c2aa9c16f4d34c346ec) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *a, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *b, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) anchr1, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) anchr2) |
| | Allocate and initialize a pin joint.
|
| | [CP_DefineConstraintProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_pin_joint/#ga58c075cbc4a59c90d5d53732f84b076a) ([cpPinJoint](/), [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/), anchr1, Anchr1) |
| | [CP_DefineConstraintProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_pin_joint/#ga10eaa57b2c695cb5bf227787b9610721) ([cpPinJoint](/), [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/), anchr2, Anchr2) |
| | [CP_DefineConstraintProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_pin_joint/#ga06ded4e61ae01e468c61e8a18820915a) ([cpPinJoint](/), [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), dist, Dist) |