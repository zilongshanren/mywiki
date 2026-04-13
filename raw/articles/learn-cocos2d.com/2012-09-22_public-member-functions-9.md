---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.0/Box2D/html/classb2_contact/
published: '2012-09-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Public Member Functions
|
[b2Manifold](../../../../../api-ref/2.0/Box2D/html/structb2_manifold/) * | [GetManifold](../../../../../api-ref/2.0/Box2D/html/classb2_contact/#ab0597077b23615476327f9b32d9c4979) () |
const [b2Manifold](../../../../../api-ref/2.0/Box2D/html/structb2_manifold/) * | **GetManifold** () const |
| void | [GetWorldManifold](../../../../../api-ref/2.0/Box2D/html/classb2_contact/#a6a30a44a28b44754cb61bba65cb5b728) ([b2WorldManifold](../../../../../api-ref/2.0/Box2D/html/structb2_world_manifold/) *worldManifold) const |
| | Get the world manifold.
|
| bool | [IsTouching](../../../../../api-ref/2.0/Box2D/html/classb2_contact/#a367dc9a563ad7db5547f4247777a33c9) () const |
| | Is this contact touching?
|
| void | [SetEnabled](../../../../../api-ref/2.0/Box2D/html/classb2_contact/#a6edf582f8c161d6632854cddefe55a0c) (bool flag) |
| bool | [IsEnabled](../../../../../api-ref/2.0/Box2D/html/classb2_contact/#ae7bd71ee1b0bb352bec6eeaab4f91c6a) () const |
| | Has this contact been disabled?
|
[b2Contact](../../../../../api-ref/2.0/Box2D/html/classb2_contact/) * | [GetNext](../../../../../api-ref/2.0/Box2D/html/classb2_contact/#aebfebb1e4b27dc0bd7aa120093e3d650) () |
| | Get the next contact in the world's contact list.
|
const [b2Contact](../../../../../api-ref/2.0/Box2D/html/classb2_contact/) * | **GetNext** () const |
[b2Fixture](../../../../../api-ref/2.0/Box2D/html/classb2_fixture/) * | [GetFixtureA](../../../../../api-ref/2.0/Box2D/html/classb2_contact/#a707a3a5a14c2cdd4c6eb7fc648d76037) () |
| | Get fixture A in this contact.
|
const [b2Fixture](../../../../../api-ref/2.0/Box2D/html/classb2_fixture/) * | **GetFixtureA** () const |
| int32 | [GetChildIndexA](../../../../../api-ref/2.0/Box2D/html/classb2_contact/#ab0c9c059c776f315ae62abb5c978afcc) () const |
| | Get the child primitive index for fixture A.
|
[b2Fixture](../../../../../api-ref/2.0/Box2D/html/classb2_fixture/) * | [GetFixtureB](../../../../../api-ref/2.0/Box2D/html/classb2_contact/#a68464fe587d7e6a1f52763e965bb7361) () |
| | Get fixture B in this contact.
|
const [b2Fixture](../../../../../api-ref/2.0/Box2D/html/classb2_fixture/) * | **GetFixtureB** () const |
| int32 | [GetChildIndexB](../../../../../api-ref/2.0/Box2D/html/classb2_contact/#a9edc26022c3d1a9cf1dab9d79d639b3f) () const |
| | Get the child primitive index for fixture B.
|
| void | [SetFriction](../../../../../api-ref/2.0/Box2D/html/classb2_contact/#a5e8fbb6bb2966ac84272bb0ea9d2e4c7) (float32 friction) |
| float32 | [GetFriction](../../../../../api-ref/2.0/Box2D/html/classb2_contact/#a0b6daf4137fd1719961f5d780b8dda15) () const |
| | Get the friction.
|
| void | [ResetFriction](../../../../../api-ref/2.0/Box2D/html/classb2_contact/#ad66d9290da187cef4c9f48c5766d4460) () |
| | Reset the friction mixture to the default value.
|
| void | [SetRestitution](../../../../../api-ref/2.0/Box2D/html/classb2_contact/#a24ca342c2bb766c53ef5ad04f5268fc1) (float32 restitution) |
| float32 | [GetRestitution](../../../../../api-ref/2.0/Box2D/html/classb2_contact/#aed12746a2855277479802144b699326b) () const |
| | Get the restitution.
|
| void | [ResetRestitution](../../../../../api-ref/2.0/Box2D/html/classb2_contact/#a243501bc5c146e9eb1296162d328aef1) () |
| | Reset the restitution to the default value.
|
| virtual void | [Evaluate](../../../../../api-ref/2.0/Box2D/html/classb2_contact/#ae3c2842e5325b2d4500f8ed1d4de2f72) ([b2Manifold](../../../../../api-ref/2.0/Box2D/html/structb2_manifold/) *manifold, const [b2Transform](../../../../../api-ref/2.0/Box2D/html/structb2_transform/) &xfA, const [b2Transform](../../../../../api-ref/2.0/Box2D/html/structb2_transform/) &xfB)=0 |
| | Evaluate this contact with your own manifold and transforms.
|
Protected Types
|
| enum | {
**e_islandFlag** = 0x0001,
**e_touchingFlag** = 0x0002,
**e_enabledFlag** = 0x0004,
**e_filterFlag** = 0x0008,
**e_bulletHitFlag** = 0x0010,
**e_toiFlag** = 0x0020
} |
Protected Member Functions
|
| void | [FlagForFiltering](../../../../../api-ref/2.0/Box2D/html/classb2_contact/#a44a3d32149021269eb9dfd4015c98e0d) () |
| | Flag this contact for filtering. Filtering will occur the next time step.
|
| **b2Contact** ([b2Fixture](../../../../../api-ref/2.0/Box2D/html/classb2_fixture/) *fixtureA, int32 indexA, [b2Fixture](../../../../../api-ref/2.0/Box2D/html/classb2_fixture/) *fixtureB, int32 indexB) |
void | **Update** ([b2ContactListener](../../../../../api-ref/2.0/Box2D/html/classb2_contact_listener/) *listener) |
Static Protected Member Functions
|
static void | **AddType** (b2ContactCreateFcn *createFcn, b2ContactDestroyFcn *destroyFcn, b2Shape::Type typeA, b2Shape::Type typeB) |
static void | **InitializeRegisters** () |
static [b2Contact](../../../../../api-ref/2.0/Box2D/html/classb2_contact/) * | **Create** ([b2Fixture](../../../../../api-ref/2.0/Box2D/html/classb2_fixture/) *fixtureA, int32 indexA, [b2Fixture](../../../../../api-ref/2.0/Box2D/html/classb2_fixture/) *fixtureB, int32 indexB, [b2BlockAllocator](../../../../../api-ref/2.0/Box2D/html/classb2_block_allocator/) *allocator) |
static void | **Destroy** ([b2Contact](../../../../../api-ref/2.0/Box2D/html/classb2_contact/) *contact, b2Shape::Type typeA, b2Shape::Type typeB, [b2BlockAllocator](../../../../../api-ref/2.0/Box2D/html/classb2_block_allocator/) *allocator) |
static void | **Destroy** ([b2Contact](../../../../../api-ref/2.0/Box2D/html/classb2_contact/) *contact, [b2BlockAllocator](../../../../../api-ref/2.0/Box2D/html/classb2_block_allocator/) *allocator) |
Protected Attributes
|
uint32 | **m_flags** |
[b2Contact](../../../../../api-ref/2.0/Box2D/html/classb2_contact/) * | **m_prev** |
[b2Contact](../../../../../api-ref/2.0/Box2D/html/classb2_contact/) * | **m_next** |
[b2ContactEdge](../../../../../api-ref/2.0/Box2D/html/structb2_contact_edge/) | **m_nodeA** |
[b2ContactEdge](../../../../../api-ref/2.0/Box2D/html/structb2_contact_edge/) | **m_nodeB** |
[b2Fixture](../../../../../api-ref/2.0/Box2D/html/classb2_fixture/) * | **m_fixtureA** |
[b2Fixture](../../../../../api-ref/2.0/Box2D/html/classb2_fixture/) * | **m_fixtureB** |
int32 | **m_indexA** |
int32 | **m_indexB** |
[b2Manifold](../../../../../api-ref/2.0/Box2D/html/structb2_manifold/) | **m_manifold** |
int32 | **m_toiCount** |
float32 | **m_toi** |
float32 | **m_friction** |
float32 | **m_restitution** |
Static Protected Attributes
|
static [b2ContactRegister](../../../../../api-ref/2.0/Box2D/html/structb2_contact_register/) | **s_registers** [b2Shape::e_typeCount][b2Shape::e_typeCount] |
static bool | **s_initialized** |
Friends
|
class | **b2ContactManager** |
class | **b2World** |
class | **b2ContactSolver** |
class | **b2Body** |
class | **b2Fixture** |

The class manages contact between two shapes. A contact exists for each overlapping AABB in the broad-phase (except if filtered). Therefore a contact object may exist that has no contact points.