---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_joint/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <b2Joint.h>`


| b2JointType |
|

The base joint class. Joints are used to constraint two bodies together in various fashions. Some joints also feature limits and motors.

| virtual void b2Joint::Dump | ( | ) | ` [inline, virtual]` |

Dump this joint to the log file.

Reimplemented in [b2RevoluteJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_revolute_joint/#aa9d88f5476c77a5c4a6ef5b2ad0d3e6f), [b2PrismaticJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_prismatic_joint/#a1d8e01f0c7ca9e1840f1f17c17dda7db), [b2WheelJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_wheel_joint/#a09534b6f4c5d0254711e0bcc7cf3b0e4), [b2PulleyJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_pulley_joint/#ad12d0e03b5d07b2f8af1005c95c67aa2), [b2DistanceJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_distance_joint/#a3cebcc6ccce6f3c24432cd130fd53517), [b2MouseJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_mouse_joint/#ae3d3a46a0032c0e50f346e7f7129617f), [b2WeldJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_weld_joint/#a2fd073c5e6264e98592240308a006981), [b2FrictionJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_friction_joint/#a9a27084c9f4a7ea0a4f590f687ac1edb), [b2RopeJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_rope_joint/#a4612dca9851a66701893a48d896dbd14), and [b2GearJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_gear_joint/#a1620b5a39e9da2b40d324c45736ad322).

Get the anchor point on bodyA in world coordinates.

Implemented in [b2RevoluteJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_revolute_joint/#a7f266986c12009973fd74c9828b6c236), [b2PrismaticJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_prismatic_joint/#ae6ccc4b3ceba180e4381fe4b821ef8d1), [b2WheelJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_wheel_joint/#a6499dcd788d29f06c2e1b28c755e01c8), [b2PulleyJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_pulley_joint/#a05ac0d0d927e9541f08b07cb1bf9ec56), [b2DistanceJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_distance_joint/#a66c1cb4deff1166c1dab67df6047a89c), [b2MouseJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_mouse_joint/#a9db1c131fde2d11e61c6ccee9c28219b), [b2WeldJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_weld_joint/#a8550de74e174a08856bc4bc7a4853429), [b2RopeJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_rope_joint/#a046c6f0bc73800716c669a2b955b3c05), [b2GearJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_gear_joint/#a2b5cdcb78c7ac3df4bd47e4195443a05), and [b2FrictionJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_friction_joint/#a01918be429fa5d37d51fda4fe0cc639b).

Get the anchor point on bodyB in world coordinates.

Implemented in [b2RevoluteJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_revolute_joint/#a3a67ad189b29ea8ab6602a28697807f6), [b2PrismaticJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_prismatic_joint/#aa2e00a1801989c3b6bc67bf47092b531), [b2WheelJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_wheel_joint/#ace182061f7f78ac2ec3f957a763ca5d3), [b2PulleyJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_pulley_joint/#a5cc3596f683d621b9a885c2569ecd452), [b2DistanceJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_distance_joint/#afc58d85cf7cc5e23082cf469e1a1a067), [b2MouseJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_mouse_joint/#a0db991ec36238105eb481f75e9b6161a), [b2WeldJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_weld_joint/#a2030794df9b2a3111bcf7a1eb0593960), [b2RopeJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_rope_joint/#a14a8ef7c16e0d6d874cdfb986d0eb8f0), [b2GearJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_gear_joint/#a84b9aedb8918a98b84032c9f0f823e13), and [b2FrictionJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_friction_joint/#ac519021aadea0faf1df01f232023c745).

| bool b2Joint::GetCollideConnected | ( | ) | const` [inline]` |

Get collide connected. Note: modifying the collide connect flag won't work correctly because the flag is only checked when fixture AABBs begin to overlap.

Get the reaction force on bodyB at the joint anchor in Newtons.

Implemented in [b2RevoluteJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_revolute_joint/#a1e5d6eb28f3f35e825cfc42dbd23d66e), [b2PrismaticJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_prismatic_joint/#a9e2a6103c1ff57e65d524b42f72b09e0), [b2WheelJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_wheel_joint/#aa16e3a1c0246017bc25e72cf494daa42), [b2PulleyJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_pulley_joint/#a38c174bf1cf1011063ff4c16556b331e), [b2DistanceJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_distance_joint/#a99413cc114b2f4dc4ce7693c062ce226), [b2MouseJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_mouse_joint/#ab8e07dbed9d24c1c046d1ede60930c52), [b2WeldJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_weld_joint/#a2ca6323d03b9fd4b591a0bfadddc25a8), [b2RopeJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_rope_joint/#afe0acc77e40b62133547897a6d01b7e6), [b2GearJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_gear_joint/#ad415f3db70ba3e60a132ef668c263713), and [b2FrictionJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_friction_joint/#ae646d8a191e490f690b748f057cdd90b).

| virtual float32 b2Joint::GetReactionTorque | ( | float32 | inv_dt | ) | const` [pure virtual]` |

Get the reaction torque on bodyB in N*m.

Implemented in [b2RevoluteJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_revolute_joint/#a85cdf204bf80dc0a4df6536e2e9a941e), [b2PrismaticJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_prismatic_joint/#a59b419ccec1a5a4b80d6664d03bd256e), [b2WheelJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_wheel_joint/#ae88eeec295a19f216acab9b23d9c704b), [b2PulleyJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_pulley_joint/#a418b200055623474c44742b1342dd278), [b2DistanceJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_distance_joint/#a8d65840abe0b398399020524852788fd), [b2MouseJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_mouse_joint/#a68efbc617aa7f0a41578e0aea988d662), [b2WeldJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_weld_joint/#a7199b5cce47b29624b4b231d78af71a3), [b2RopeJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_rope_joint/#abb7baf596f13ff5a76ff657ad6d3232c), [b2GearJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_gear_joint/#ae2c4b1ae1cf00f14331332c4fe9ae964), and [b2FrictionJoint](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_friction_joint/#a49479d4af9c4bffa0b146d153c78512c).

| b2JointType b2Joint::GetType | ( | ) | const` [inline]` |

Get the type of the concrete joint.

| void * b2Joint::GetUserData | ( | ) | const` [inline]` |

Get the user data pointer.

| bool b2Joint::IsActive | ( | ) | const |

Short-cut function to determine if either body is inactive.

| void b2Joint::SetUserData | ( | void * | data | ) | ` [inline]` |

Set the user data pointer.