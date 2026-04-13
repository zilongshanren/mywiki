---
title: b2PulleyJointDef Struct Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/structb2_pulley_joint_def/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# b2PulleyJointDef Struct Reference

`#include <`[b2PulleyJoint.h](/)>


[List of all members.](/)

## Public Member Functions |
| | [b2PulleyJointDef](../../../box2d-api-reference/API/structb2_pulley_joint_def/#ab006bb8b7ea6bea6e0fd8cbaaacb33b0) () |
| void | [Initialize](../../../box2d-api-reference/API/structb2_pulley_joint_def/#abef614a93562b82aa3b5f8cac17d1ce8) ([b2Body](../../../box2d-api-reference/API/classb2_body/) *[bodyA](../../../box2d-api-reference/API/structb2_joint_def/#a8cd54c93da396be75a9788f2c6897f05), [b2Body](../../../box2d-api-reference/API/classb2_body/) *[bodyB](../../../box2d-api-reference/API/structb2_joint_def/#aa4f4dee2fbcd12187b19506b60e68e3d), const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) &[groundAnchorA](../../../box2d-api-reference/API/structb2_pulley_joint_def/#aae77c020ce4629ab9e03560e28aa853d), const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) &[groundAnchorB](../../../box2d-api-reference/API/structb2_pulley_joint_def/#aa412b9f3bffd1fb69ace14f9b3e03b82), const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) &anchorA, const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) &anchorB, [float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) [ratio](../../../box2d-api-reference/API/structb2_pulley_joint_def/#af35074246aeacbf239c11682642b31f5)) |
| | Initialize the bodies, anchors, lengths, max lengths, and ratio using the world anchors.
|
## Public Attributes |
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [groundAnchorA](../../../box2d-api-reference/API/structb2_pulley_joint_def/#aae77c020ce4629ab9e03560e28aa853d) |
| | The first ground anchor in world coordinates. This point never moves.
|
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [groundAnchorB](../../../box2d-api-reference/API/structb2_pulley_joint_def/#aa412b9f3bffd1fb69ace14f9b3e03b82) |
| | The second ground anchor in world coordinates. This point never moves.
|
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [localAnchorA](../../../box2d-api-reference/API/structb2_pulley_joint_def/#ad7677a4ad02a6e7cb8699fc5012eac3e) |
| | The local anchor point relative to bodyA's origin.
|
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [localAnchorB](../../../box2d-api-reference/API/structb2_pulley_joint_def/#aed3f9c9f5f4145ceb32e7e164de73144) |
| | The local anchor point relative to bodyB's origin.
|
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [lengthA](../../../box2d-api-reference/API/structb2_pulley_joint_def/#a51d945882c1d7a78af2b0e9ffb31a33b) |
| | The a reference length for the segment attached to bodyA.
|
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [maxLengthA](../../../box2d-api-reference/API/structb2_pulley_joint_def/#aa36fe43a9b9a31be30b0491838803232) |
| | The maximum length of the segment attached to bodyA.
|
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [lengthB](../../../box2d-api-reference/API/structb2_pulley_joint_def/#a5857d5b5b9880b6c8201ce3ee8c3eef0) |
| | The a reference length for the segment attached to bodyB.
|
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [maxLengthB](../../../box2d-api-reference/API/structb2_pulley_joint_def/#a85e003e42446251cbea89cc2eb745427) |
| | The maximum length of the segment attached to bodyB.
|
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [ratio](../../../box2d-api-reference/API/structb2_pulley_joint_def/#af35074246aeacbf239c11682642b31f5) |
| | The pulley ratio, used to simulate a block-and-tackle.
|


## Detailed Description

Pulley joint definition. This requires two ground anchors, two dynamic body anchor points, max lengths for each side, and a pulley ratio.


## Constructor & Destructor Documentation

| b2PulleyJointDef::b2PulleyJointDef |
( |
|
) |
` [inline]` |



## Member Function Documentation

Initialize the bodies, anchors, lengths, max lengths, and ratio using the world anchors.


## Member Data Documentation

The first ground anchor in world coordinates. This point never moves.

The second ground anchor in world coordinates. This point never moves.

The a reference length for the segment attached to bodyA.

The a reference length for the segment attached to bodyB.

The local anchor point relative to bodyA's origin.

The local anchor point relative to bodyB's origin.

The maximum length of the segment attached to bodyA.

The maximum length of the segment attached to bodyB.

The pulley ratio, used to simulate a block-and-tackle.


The documentation for this struct was generated from the following files: