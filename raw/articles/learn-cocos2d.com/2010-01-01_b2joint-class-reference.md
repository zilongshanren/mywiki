---
title: b2Joint Class Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_joint/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <`

[b2Joint.h](http://www.learn-cocos2d.com/)>

## Public Member Functions | |
|

The base joint class. Joints are used to constraint two bodies together in various fashions. Some joints also feature limits and motors.

| virtual b2Joint::~b2Joint | ( | ) | ` [inline, protected, virtual]` |

|

` [static, protected]`

Get the anchor point on bodyA in world coordinates.

Implemented in [b2DistanceJoint](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_distance_joint/#a66c1cb4deff1166c1dab67df6047a89c), [b2FrictionJoint](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_friction_joint/#a01918be429fa5d37d51fda4fe0cc639b), [b2GearJoint](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_gear_joint/#a2b5cdcb78c7ac3df4bd47e4195443a05), [b2LineJoint](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_line_joint/#aa085af07bd2e27768c58be9b62894458), [b2MouseJoint](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_mouse_joint/#a9db1c131fde2d11e61c6ccee9c28219b), [b2PrismaticJoint](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_prismatic_joint/#ae6ccc4b3ceba180e4381fe4b821ef8d1), [b2PulleyJoint](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_pulley_joint/#a05ac0d0d927e9541f08b07cb1bf9ec56), [b2RevoluteJoint](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_revolute_joint/#a7f266986c12009973fd74c9828b6c236), and [b2WeldJoint](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_weld_joint/#a8550de74e174a08856bc4bc7a4853429).

Get the anchor point on bodyB in world coordinates.

Implemented in [b2DistanceJoint](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_distance_joint/#afc58d85cf7cc5e23082cf469e1a1a067), [b2FrictionJoint](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_friction_joint/#ac519021aadea0faf1df01f232023c745), [b2GearJoint](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_gear_joint/#a84b9aedb8918a98b84032c9f0f823e13), [b2LineJoint](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_line_joint/#a929b129ad6208956fe4eba3a43692764), [b2MouseJoint](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_mouse_joint/#a0db991ec36238105eb481f75e9b6161a), [b2PrismaticJoint](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_prismatic_joint/#aa2e00a1801989c3b6bc67bf47092b531), [b2PulleyJoint](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_pulley_joint/#a5cc3596f683d621b9a885c2569ecd452), [b2RevoluteJoint](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_revolute_joint/#a3a67ad189b29ea8ab6602a28697807f6), and [b2WeldJoint](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_weld_joint/#a2030794df9b2a3111bcf7a1eb0593960).

Get the reaction force on body2 at the joint anchor in Newtons.

Implemented in [b2DistanceJoint](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_distance_joint/#a99413cc114b2f4dc4ce7693c062ce226), [b2FrictionJoint](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_friction_joint/#ae646d8a191e490f690b748f057cdd90b), [b2GearJoint](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_gear_joint/#ad415f3db70ba3e60a132ef668c263713), [b2LineJoint](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_line_joint/#a62f5d04249865beaad5c5c75517ff9e5), [b2MouseJoint](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_mouse_joint/#ab8e07dbed9d24c1c046d1ede60930c52), [b2PrismaticJoint](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_prismatic_joint/#a9e2a6103c1ff57e65d524b42f72b09e0), [b2PulleyJoint](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_pulley_joint/#a38c174bf1cf1011063ff4c16556b331e), [b2RevoluteJoint](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_revolute_joint/#a1e5d6eb28f3f35e825cfc42dbd23d66e), and [b2WeldJoint](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_weld_joint/#a2ca6323d03b9fd4b591a0bfadddc25a8).

| void * b2Joint::GetUserData | ( | ) | const` [inline]` |

Get the user data pointer.

| bool b2Joint::IsActive | ( | ) | const |

Short-cut function to determine if either body is inactive.

| void b2Joint::SetUserData | ( | void * | data |
) | ` [inline]` |

Set the user data pointer.