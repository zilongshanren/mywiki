---
title: Public Attributes
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/structb2_rope_joint_def/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <b2RopeJoint.h>`


|

Rope joint definition. This requires two body anchor points and a maximum lengths. Note: by default the connected objects will not collide. see collideConnected in [b2JointDef](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/structb2_joint_def/).

The maximum length of the rope. Warning: this must be larger than b2_linearSlop or the joint will have no effect.