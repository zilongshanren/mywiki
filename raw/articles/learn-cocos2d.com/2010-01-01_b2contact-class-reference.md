---
title: b2Contact Class Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_contact/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# b2Contact Class Reference

`#include <`[b2Contact.h](/)>


[List of all members.](/)

## Public Member Functions |
[b2Manifold](../../../box2d-api-reference/API/structb2_manifold/) * | [GetManifold](../../../box2d-api-reference/API/classb2_contact/#ab0597077b23615476327f9b32d9c4979) () |
const [b2Manifold](../../../box2d-api-reference/API/structb2_manifold/) * | [GetManifold](../../../box2d-api-reference/API/classb2_contact/#a2a1fb2fa1e0956faf61047c4aba3da5a) () const |
| void | [GetWorldManifold](../../../box2d-api-reference/API/classb2_contact/#a6a30a44a28b44754cb61bba65cb5b728) ([b2WorldManifold](../../../box2d-api-reference/API/structb2_world_manifold/) *worldManifold) const |
| | Get the world manifold.
|
| bool | [IsTouching](../../../box2d-api-reference/API/classb2_contact/#a367dc9a563ad7db5547f4247777a33c9) () const |
| | Is this contact touching?
|
| void | [SetEnabled](../../../box2d-api-reference/API/classb2_contact/#a6edf582f8c161d6632854cddefe55a0c) (bool flag) |
| bool | [IsEnabled](../../../box2d-api-reference/API/classb2_contact/#ae7bd71ee1b0bb352bec6eeaab4f91c6a) () const |
| | Has this contact been disabled?
|
[b2Contact](../../../box2d-api-reference/API/classb2_contact/) * | [GetNext](../../../box2d-api-reference/API/classb2_contact/#aebfebb1e4b27dc0bd7aa120093e3d650) () |
| | Get the next contact in the world's contact list.
|
const [b2Contact](../../../box2d-api-reference/API/classb2_contact/) * | [GetNext](../../../box2d-api-reference/API/classb2_contact/#a55e20c9e32071f492952dad256552141) () const |
[b2Fixture](../../../box2d-api-reference/API/classb2_fixture/) * | [GetFixtureA](../../../box2d-api-reference/API/classb2_contact/#a707a3a5a14c2cdd4c6eb7fc648d76037) () |
| | Get the first fixture in this contact.
|
const [b2Fixture](../../../box2d-api-reference/API/classb2_fixture/) * | [GetFixtureA](../../../box2d-api-reference/API/classb2_contact/#af5820afc8ebb6d785a47a979b373b004) () const |
[b2Fixture](../../../box2d-api-reference/API/classb2_fixture/) * | [GetFixtureB](../../../box2d-api-reference/API/classb2_contact/#a68464fe587d7e6a1f52763e965bb7361) () |
| | Get the second fixture in this contact.
|
const [b2Fixture](../../../box2d-api-reference/API/classb2_fixture/) * | [GetFixtureB](../../../box2d-api-reference/API/classb2_contact/#a06db543279afbb51071bf57475bfcc1e) () const |
| virtual void | [Evaluate](../../../box2d-api-reference/API/classb2_contact/#ae3c2842e5325b2d4500f8ed1d4de2f72) ([b2Manifold](../../../box2d-api-reference/API/structb2_manifold/) *manifold, const [b2Transform](../../../box2d-api-reference/API/structb2_transform/) &xfA, const [b2Transform](../../../box2d-api-reference/API/structb2_transform/) &xfB)=0 |
| | Evaluate this contact with your own manifold and transforms.
|
## Protected Types |
| enum | { [e_islandFlag](../../../box2d-api-reference/API/classb2_contact/#ab8f00a9c04b3eea54a9c5bab29328c3eaad83700b4de33a2e3133ea0d98aa1c8b) = 0x0001,
[e_touchingFlag](../../../box2d-api-reference/API/classb2_contact/#ab8f00a9c04b3eea54a9c5bab29328c3eaff50bb5872ede1ef890c5b4d063c6378) = 0x0002,
[e_enabledFlag](../../../box2d-api-reference/API/classb2_contact/#ab8f00a9c04b3eea54a9c5bab29328c3ea63ecc7ff371a26143b250e8f315576a7) = 0x0004,
[e_filterFlag](../../../box2d-api-reference/API/classb2_contact/#ab8f00a9c04b3eea54a9c5bab29328c3eab8e92ae0c3f97e9d95aedb30238e6817) = 0x0008
} |
## Protected Member Functions |
| void | [FlagForFiltering](../../../box2d-api-reference/API/classb2_contact/#a44a3d32149021269eb9dfd4015c98e0d) () |
| | Flag this contact for filtering. Filtering will occur the next time step.
|
| | [b2Contact](../../../box2d-api-reference/API/classb2_contact/#a04b21bf6fcf41ba19866a2d57c4a2060) () |
| | [b2Contact](../../../box2d-api-reference/API/classb2_contact/#a7a88cac4ea8ee508380d5ac6e624afe2) ([b2Fixture](../../../box2d-api-reference/API/classb2_fixture/) *fixtureA, [b2Fixture](../../../box2d-api-reference/API/classb2_fixture/) *fixtureB) |
| virtual | [~b2Contact](../../../box2d-api-reference/API/classb2_contact/#a37368b233a5ac0d698310b300426ce16) () |
| void | [Update](../../../box2d-api-reference/API/classb2_contact/#a218a66a6c34e3de1c428aa73a0680dfe) ([b2ContactListener](../../../box2d-api-reference/API/classb2_contact_listener/) *listener) |
## Static Protected Member Functions |
| static void | [AddType](../../../box2d-api-reference/API/classb2_contact/#ad905650aab96ead0434c2bb449e4129c) ([b2ContactCreateFcn](/#a3044a8052be60335dab5838785b41707) *createFcn, [b2ContactDestroyFcn](/#a13f1fcd7bbd3900e53e6ddf8a76428e7) *destroyFcn, [b2Shape::Type](../../../box2d-api-reference/API/classb2_shape/#a4c1f3a9ad6b3150bb90ad9018ca4b1e0) typeA, [b2Shape::Type](../../../box2d-api-reference/API/classb2_shape/#a4c1f3a9ad6b3150bb90ad9018ca4b1e0) typeB) |
| static void | [InitializeRegisters](../../../box2d-api-reference/API/classb2_contact/#ac77031d85c2e06d5cdc1f5c774f8f3fd) () |
static [b2Contact](../../../box2d-api-reference/API/classb2_contact/) * | [Create](../../../box2d-api-reference/API/classb2_contact/#a004320052bc0fc7ea2d3690aa2f7e39c) ([b2Fixture](../../../box2d-api-reference/API/classb2_fixture/) *fixtureA, [b2Fixture](../../../box2d-api-reference/API/classb2_fixture/) *fixtureB, [b2BlockAllocator](../../../box2d-api-reference/API/classb2_block_allocator/) *allocator) |
| static void | [Destroy](../../../box2d-api-reference/API/classb2_contact/#a36c1f6767f212f2e4ddb4c4b2c7cdb75) ([b2Contact](../../../box2d-api-reference/API/classb2_contact/) *contact, [b2Shape::Type](../../../box2d-api-reference/API/classb2_shape/#a4c1f3a9ad6b3150bb90ad9018ca4b1e0) typeA, [b2Shape::Type](../../../box2d-api-reference/API/classb2_shape/#a4c1f3a9ad6b3150bb90ad9018ca4b1e0) typeB, [b2BlockAllocator](../../../box2d-api-reference/API/classb2_block_allocator/) *allocator) |
| static void | [Destroy](../../../box2d-api-reference/API/classb2_contact/#ab57797a25c2206edf1ad7c4dcd1cbca5) ([b2Contact](../../../box2d-api-reference/API/classb2_contact/) *contact, [b2BlockAllocator](../../../box2d-api-reference/API/classb2_block_allocator/) *allocator) |
## Protected Attributes |
[uint32](../../../box2d-api-reference/API/b2_settings_8h/#a1134b580f8da4de94ca6b1de4d37975e) | [m_flags](../../../box2d-api-reference/API/classb2_contact/#a85d5408adcbf466bcb8f291aeb35bc3b) |
[b2Contact](../../../box2d-api-reference/API/classb2_contact/) * | [m_prev](../../../box2d-api-reference/API/classb2_contact/#adf3a3450e0fa9cf6d11ca22467c2370b) |
[b2Contact](../../../box2d-api-reference/API/classb2_contact/) * | [m_next](../../../box2d-api-reference/API/classb2_contact/#a241fea000d26da8761b5520a9adcd87a) |
[b2ContactEdge](../../../box2d-api-reference/API/structb2_contact_edge/) | [m_nodeA](../../../box2d-api-reference/API/classb2_contact/#a5f5ce747bb04f48843eb07304d47faab) |
[b2ContactEdge](../../../box2d-api-reference/API/structb2_contact_edge/) | [m_nodeB](../../../box2d-api-reference/API/classb2_contact/#a4887c3acb8cb857e2bec659027539c7a) |
[b2Fixture](../../../box2d-api-reference/API/classb2_fixture/) * | [m_fixtureA](../../../box2d-api-reference/API/classb2_contact/#aec94bbbb8862f09365a5af99650b5be4) |
[b2Fixture](../../../box2d-api-reference/API/classb2_fixture/) * | [m_fixtureB](../../../box2d-api-reference/API/classb2_contact/#a83b18f0da1cfeb2c9dccc6aabed881d3) |
[b2Manifold](../../../box2d-api-reference/API/structb2_manifold/) | [m_manifold](../../../box2d-api-reference/API/classb2_contact/#aebdc2c073d05ac8e544a591d2043b251) |
[int32](../../../box2d-api-reference/API/b2_settings_8h/#a43d43196463bde49cb067f5c20ab8481) | [m_toiCount](../../../box2d-api-reference/API/classb2_contact/#afaa231f3e9a908154f9a32af456601b6) |
## Static Protected Attributes |
static [b2ContactRegister](../../../box2d-api-reference/API/structb2_contact_register/) | [s_registers](../../../box2d-api-reference/API/classb2_contact/#a5e2beb4e435e1545ae043a7a2b77d1da) [b2Shape::e_typeCount][b2Shape::e_typeCount] |
| static bool | [s_initialized](../../../box2d-api-reference/API/classb2_contact/#a672598c350694d7b9a89c45f8ad0dd90) = false |
## Friends |
| class | [b2ContactManager](../../../box2d-api-reference/API/classb2_contact/#aece264d42f69aed410f5eb3beba6ddf2) |
| class | [b2World](../../../box2d-api-reference/API/classb2_contact/#a4bd536c5a7c0587913765bbc2693ceea) |
| class | [b2ContactSolver](../../../box2d-api-reference/API/classb2_contact/#afb788a7ba90344f3ddbafff3de0465c4) |
| class | [b2Body](../../../box2d-api-reference/API/classb2_contact/#a010ab52de250e5fe30a45d642f46405b) |
| class | [b2Fixture](../../../box2d-api-reference/API/classb2_contact/#afb35b0e61f6ee3cc516c40ea251f3236) |


## Detailed Description

The class manages contact between two shapes. A contact exists for each overlapping AABB in the broad-phase (except if filtered). Therefore a contact object may exist that has no contact points.


## Member Enumeration Documentation

anonymous enum` [protected]` |

**Enumerator: **
e_islandFlag |
|
e_touchingFlag |
|
e_enabledFlag |
|
e_filterFlag |
|



## Constructor & Destructor Documentation

| b2Contact::b2Contact |
( |
|
) |
` [inline, protected]` |


| virtual b2Contact::~b2Contact |
( |
|
) |
` [inline, protected, virtual]` |



## Member Function Documentation

| void b2Contact::FlagForFiltering |
( |
|
) |
` [inline, protected]` |

Flag this contact for filtering. Filtering will occur the next time step.

const [b2Fixture](../../../box2d-api-reference/API/classb2_fixture/) * b2Contact::GetFixtureA |
( |
|
) |
const` [inline]` |


[b2Fixture](../../../box2d-api-reference/API/classb2_fixture/) * b2Contact::GetFixtureA |
( |
|
) |
` [inline]` |

Get the first fixture in this contact.

const [b2Fixture](../../../box2d-api-reference/API/classb2_fixture/) * b2Contact::GetFixtureB |
( |
|
) |
const` [inline]` |


[b2Fixture](../../../box2d-api-reference/API/classb2_fixture/) * b2Contact::GetFixtureB |
( |
|
) |
` [inline]` |

Get the second fixture in this contact.

const [b2Manifold](../../../box2d-api-reference/API/structb2_manifold/) * b2Contact::GetManifold |
( |
|
) |
const` [inline]` |


Get the contact manifold. Do not modify the manifold unless you understand the internals of Box2D.

const [b2Contact](../../../box2d-api-reference/API/classb2_contact/) * b2Contact::GetNext |
( |
|
) |
const` [inline]` |


Get the next contact in the world's contact list.

| void b2Contact::GetWorldManifold |
( |
[b2WorldManifold](../../../box2d-api-reference/API/structb2_world_manifold/) * |
*worldManifold* |
) |
const` [inline]` |

| void b2Contact::InitializeRegisters |
( |
|
) |
` [static, protected]` |


| bool b2Contact::IsEnabled |
( |
|
) |
const` [inline]` |

Has this contact been disabled?

| bool b2Contact::IsTouching |
( |
|
) |
const` [inline]` |

Is this contact touching?

| void b2Contact::SetEnabled |
( |
bool |
*flag* |
) |
` [inline]` |

Enable/disable this contact. This can be used inside the pre-solve contact listener. The contact is only disabled for the current time step (or sub-step in continuous collisions).


## Friends And Related Function Documentation


## Member Data Documentation


The documentation for this class was generated from the following files: