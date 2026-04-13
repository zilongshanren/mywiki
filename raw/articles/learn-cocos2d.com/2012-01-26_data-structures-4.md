---
title: Data Structures
url: http://www.learn-cocos2d.com/api-ref/1.0/Chipmunk/html/group__cp_arbiter/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

| struct |
|

`ith`

contact point. `ith`

contact point. `ith`

contact point. The [cpArbiter](http://www.learn-cocos2d.com/api-ref/1.0/Chipmunk/html/structcp_arbiter/) struct controls pairs of colliding shapes. They are also used in conjuction with collision handler callbacks allowing you to retrieve information on the collision and control it.

A macro shortcut for defining and retrieving the bodies from an arbiter.

A macro shortcut for defining and retrieving the shapes from an arbiter.

| #define CP_DefineArbiterStructGetter | ( | type, | |
| member, | |||
| name | |||
| ) | static inline type cpArbiterGet##name(const
|

| #define CP_DefineArbiterStructProperty | ( | type, | |
| member, | |||
| name | |||
| ) |

| #define CP_DefineArbiterStructSetter | ( | type, | |
| member, | |||
| name | |||
| ) | static inline void cpArbiterSet##name(
|

| #define CP_MAX_CONTACTS_PER_ARBITER 4 |

Collision begin event function callback type. Returning false from a begin callback causes the collision to be ignored until the the separate callback is called when the objects stop colliding.

Collision post-solve event function callback type.

Collision pre-solve event function callback type. Returning false from a pre-step callback causes the collision to be ignored until the next step.

Collision separate event function callback type.

Return the colliding bodies involved for this arbiter. The order of the cpSpace.collision_type the bodies are associated with values will match the order set when the collision handler was registered.

Return a contact set from an arbiter.

Get the number of contact points for this arbiter.

Get the position of the `ith`

contact point.

| static void cpArbiterGetShapes | ( | const
|

` [inline, static]`

Return the colliding shapes involved for this arbiter. The order of their cpSpace.collision_type values will match the order set when the collision handler was registered.

Causes a collision pair to be ignored as if you returned false from a begin callback. If called from a pre-step callback, you will still need to return false if you want it to be ignored in the current step.

Returns true if this is the first step a pair of objects started colliding.

Calculate the total impulse that was applied by this arbiter. This function should only be called from a post-solve, post-step or cpBodyEachArbiter callback.

Calculate the total impulse including the friction that was applied by this arbiter. This function should only be called from a post-solve, post-step or cpBodyEachArbiter callback.