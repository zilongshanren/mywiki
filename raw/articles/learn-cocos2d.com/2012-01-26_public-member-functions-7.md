---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_contact/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <b2Contact.h>`


|

The class manages contact between two shapes. A contact exists for each overlapping AABB in the broad-phase (except if filtered). Therefore a contact object may exist that has no contact points.

| virtual void b2Contact::Evaluate | ( |
|

` [pure virtual]`

Evaluate this contact with your own manifold and transforms.

Implemented in [b2ChainAndCircleContact](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_chain_and_circle_contact/#afe52ebd870f24cbecedd1db662705f12), [b2ChainAndPolygonContact](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_chain_and_polygon_contact/#a8c25ceb49d981797d0a7f8a1ea769442), [b2CircleContact](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_circle_contact/#ac0651dda773561b8561b8efa3cd31d5c), [b2EdgeAndCircleContact](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_edge_and_circle_contact/#a8f083c4c7c7da83eae38975164fd1452), [b2EdgeAndPolygonContact](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_edge_and_polygon_contact/#a5f360f5f0b1d367beb517ba9f380c84b), [b2PolygonContact](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_polygon_contact/#ae75f78bb52c76fc4fffda4d91e62d354), and [b2PolygonAndCircleContact](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_polygon_and_circle_contact/#ac24d495022aae853cb573f86c8d86c3d).

| void b2Contact::FlagForFiltering | ( | ) | ` [inline, protected]` |

Flag this contact for filtering. Filtering will occur the next time step.

| int32 b2Contact::GetChildIndexA | ( | ) | const` [inline]` |

Get the child primitive index for fixture A.

| int32 b2Contact::GetChildIndexB | ( | ) | const` [inline]` |

Get the child primitive index for fixture B.

| float32 b2Contact::GetFriction | ( | ) | const` [inline]` |

Get the friction.

Get the contact manifold. Do not modify the manifold unless you understand the internals of Box2D.

| float32 b2Contact::GetRestitution | ( | ) | const` [inline]` |

Get the restitution.

Get the world manifold.

| bool b2Contact::IsEnabled | ( | ) | const` [inline]` |

Has this contact been disabled?

| bool b2Contact::IsTouching | ( | ) | const` [inline]` |

Is this contact touching?

| void b2Contact::ResetFriction | ( | ) | ` [inline]` |

Reset the friction mixture to the default value.

| void b2Contact::ResetRestitution | ( | ) | ` [inline]` |

Reset the restitution to the default value.

| void b2Contact::SetEnabled | ( | bool | flag | ) | ` [inline]` |

Enable/disable this contact. This can be used inside the pre-solve contact listener. The contact is only disabled for the current time step (or sub-step in continuous collisions).

| void b2Contact::SetFriction | ( | float32 | friction | ) | ` [inline]` |

| void b2Contact::SetRestitution | ( | float32 | restitution | ) | ` [inline]` |