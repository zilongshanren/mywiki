---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/structb2_pulley_joint_def/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Public Member Functions
|
| void | [Initialize](../../../../../api-ref/1.0/Box2D/html/structb2_pulley_joint_def/#abef614a93562b82aa3b5f8cac17d1ce8) ([b2Body](../../../../../api-ref/1.0/Box2D/html/classb2_body/) *[bodyA](../../../../../api-ref/1.0/Box2D/html/structb2_joint_def/#a8cd54c93da396be75a9788f2c6897f05), [b2Body](../../../../../api-ref/1.0/Box2D/html/classb2_body/) *[bodyB](../../../../../api-ref/1.0/Box2D/html/structb2_joint_def/#aa4f4dee2fbcd12187b19506b60e68e3d), const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) &[groundAnchorA](../../../../../api-ref/1.0/Box2D/html/structb2_pulley_joint_def/#aae77c020ce4629ab9e03560e28aa853d), const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) &[groundAnchorB](../../../../../api-ref/1.0/Box2D/html/structb2_pulley_joint_def/#aa412b9f3bffd1fb69ace14f9b3e03b82), const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) &anchorA, const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) &anchorB, float32 [ratio](../../../../../api-ref/1.0/Box2D/html/structb2_pulley_joint_def/#af35074246aeacbf239c11682642b31f5)) |
| | Initialize the bodies, anchors, lengths, max lengths, and ratio using the world anchors.
|
Public Attributes
|
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | [groundAnchorA](../../../../../api-ref/1.0/Box2D/html/structb2_pulley_joint_def/#aae77c020ce4629ab9e03560e28aa853d) |
| | The first ground anchor in world coordinates. This point never moves.
|
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | [groundAnchorB](../../../../../api-ref/1.0/Box2D/html/structb2_pulley_joint_def/#aa412b9f3bffd1fb69ace14f9b3e03b82) |
| | The second ground anchor in world coordinates. This point never moves.
|
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | [localAnchorA](../../../../../api-ref/1.0/Box2D/html/structb2_pulley_joint_def/#ad7677a4ad02a6e7cb8699fc5012eac3e) |
| | The local anchor point relative to bodyA's origin.
|
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | [localAnchorB](../../../../../api-ref/1.0/Box2D/html/structb2_pulley_joint_def/#aed3f9c9f5f4145ceb32e7e164de73144) |
| | The local anchor point relative to bodyB's origin.
|
| float32 | [lengthA](../../../../../api-ref/1.0/Box2D/html/structb2_pulley_joint_def/#a51d945882c1d7a78af2b0e9ffb31a33b) |
| | The a reference length for the segment attached to bodyA.
|
| float32 | [lengthB](../../../../../api-ref/1.0/Box2D/html/structb2_pulley_joint_def/#a5857d5b5b9880b6c8201ce3ee8c3eef0) |
| | The a reference length for the segment attached to bodyB.
|
| float32 | [ratio](../../../../../api-ref/1.0/Box2D/html/structb2_pulley_joint_def/#af35074246aeacbf239c11682642b31f5) |
| | The pulley ratio, used to simulate a block-and-tackle.
|

Pulley joint definition. This requires two ground anchors, two dynamic body anchor points, and a pulley ratio.