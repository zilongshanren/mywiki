---
title: b2PulleyJoint Class Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_pulley_joint/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# b2PulleyJoint Class Reference

`#include <`[b2PulleyJoint.h](/)>


[List of all members.](/)


## Detailed Description

The pulley joint is connected to two bodies and two fixed ground points. The pulley supports a ratio such that: length1 + ratio * length2 <= constant Yes, the force transmitted is scaled by the ratio. The pulley also enforces a maximum length limit on both sides. This is useful to prevent one side of the pulley hitting the top.


## Constructor & Destructor Documentation


## Member Function Documentation

[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) b2PulleyJoint::GetAnchorA |
( |
|
) |
const` [virtual]` |

Get the anchor point on bodyA in world coordinates.

Implements [b2Joint](../../../box2d-api-reference/API/classb2_joint/#abe46ca3aad5db73909a9b5a7b2117447).

[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) b2PulleyJoint::GetAnchorB |
( |
|
) |
const` [virtual]` |

Get the anchor point on bodyB in world coordinates.

Implements [b2Joint](../../../box2d-api-reference/API/classb2_joint/#a88e947c65d4ea26fe539f02a8cb7f7a9).

[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) b2PulleyJoint::GetGroundAnchorA |
( |
|
) |
const |

Get the first ground anchor.

[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) b2PulleyJoint::GetGroundAnchorB |
( |
|
) |
const |

Get the second ground anchor.

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2PulleyJoint::GetLength1 |
( |
|
) |
const |

Get the current length of the segment attached to body1.

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2PulleyJoint::GetLength2 |
( |
|
) |
const |

Get the current length of the segment attached to body2.

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2PulleyJoint::GetRatio |
( |
|
) |
const |

[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) b2PulleyJoint::GetReactionForce |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*inv_dt* |
) |
const` [virtual]` |

Get the reaction force on body2 at the joint anchor in Newtons.

Implements [b2Joint](../../../box2d-api-reference/API/classb2_joint/#a7e0eddefb9b69ad050b8ef6425838a74).

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2PulleyJoint::GetReactionTorque |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*inv_dt* |
) |
const` [virtual]` |

Get the reaction torque on body2 in N*m.

Implements [b2Joint](../../../box2d-api-reference/API/classb2_joint/#ae355e441c2aa842777dc04e24f15ced0).

| void b2PulleyJoint::InitVelocityConstraints |
( |
const [b2TimeStep](../../../box2d-api-reference/API/structb2_time_step/) & |
*step* |
) |
` [protected, virtual]` |

| bool b2PulleyJoint::SolvePositionConstraints |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*baumgarte* |
) |
` [protected, virtual]` |

| void b2PulleyJoint::SolveVelocityConstraints |
( |
const [b2TimeStep](../../../box2d-api-reference/API/structb2_time_step/) & |
*step* |
) |
` [protected, virtual]` |


## Friends And Related Function Documentation


## Member Data Documentation


The documentation for this class was generated from the following files: