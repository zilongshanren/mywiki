---
title: 'Box2D: Member List'
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_contact-members/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

, including all inherited members.

**AddType**(b2ContactCreateFcn *createFcn, b2ContactDestroyFcn *destroyFcn, b2Shape::Type typeA, b2Shape::Type typeB) (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected, static]` |
**b2Body** (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [friend]` |
**b2Contact**() (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [inline, protected]` |
**b2Contact**(b2Fixture *fixtureA, int32 indexA, b2Fixture *fixtureB, int32 indexB) (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected]` |
**b2ContactManager** (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [friend]` |
**b2ContactSolver** (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [friend]` |
**b2Fixture** (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [friend]` |
**b2World** (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [friend]` |
**Create**(b2Fixture *fixtureA, int32 indexA, b2Fixture *fixtureB, int32 indexB, b2BlockAllocator *allocator) (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected, static]` |
**Destroy**(b2Contact *contact, b2Shape::Type typeA, b2Shape::Type typeB, b2BlockAllocator *allocator) (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected, static]` |
**Destroy**(b2Contact *contact, b2BlockAllocator *allocator) (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected, static]` |
**e_bulletHitFlag** enum value (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected]` |
**e_enabledFlag** enum value (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected]` |
**e_filterFlag** enum value (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected]` |
**e_islandFlag** enum value (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected]` |
**e_toiFlag** enum value (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected]` |
**e_touchingFlag** enum value (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected]` |
[Evaluate](../../../../../api-ref/1.0/Box2D/html/classb2_contact/#ae3c2842e5325b2d4500f8ed1d4de2f72)(b2Manifold *manifold, const b2Transform &xfA, const b2Transform &xfB)=0 | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [pure virtual]` |
[FlagForFiltering](../../../../../api-ref/1.0/Box2D/html/classb2_contact/#a44a3d32149021269eb9dfd4015c98e0d)() | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [inline, protected]` |
[GetChildIndexA](../../../../../api-ref/1.0/Box2D/html/classb2_contact/#ab0c9c059c776f315ae62abb5c978afcc)() const | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [inline]` |
[GetChildIndexB](../../../../../api-ref/1.0/Box2D/html/classb2_contact/#a9edc26022c3d1a9cf1dab9d79d639b3f)() const | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [inline]` |
[GetFixtureA](../../../../../api-ref/1.0/Box2D/html/classb2_contact/#a707a3a5a14c2cdd4c6eb7fc648d76037)() | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [inline]` |
**GetFixtureA**() const (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [inline]` |
[GetFixtureB](../../../../../api-ref/1.0/Box2D/html/classb2_contact/#a68464fe587d7e6a1f52763e965bb7361)() | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [inline]` |
**GetFixtureB**() const (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [inline]` |
[GetFriction](../../../../../api-ref/1.0/Box2D/html/classb2_contact/#a0b6daf4137fd1719961f5d780b8dda15)() const | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [inline]` |
[GetManifold](../../../../../api-ref/1.0/Box2D/html/classb2_contact/#ab0597077b23615476327f9b32d9c4979)() | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [inline]` |
**GetManifold**() const (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [inline]` |
[GetNext](../../../../../api-ref/1.0/Box2D/html/classb2_contact/#aebfebb1e4b27dc0bd7aa120093e3d650)() | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [inline]` |
**GetNext**() const (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [inline]` |
[GetRestitution](../../../../../api-ref/1.0/Box2D/html/classb2_contact/#aed12746a2855277479802144b699326b)() const | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [inline]` |
[GetWorldManifold](../../../../../api-ref/1.0/Box2D/html/classb2_contact/#a6a30a44a28b44754cb61bba65cb5b728)(b2WorldManifold *worldManifold) const | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [inline]` |
**InitializeRegisters**() (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected, static]` |
[IsEnabled](../../../../../api-ref/1.0/Box2D/html/classb2_contact/#ae7bd71ee1b0bb352bec6eeaab4f91c6a)() const | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [inline]` |
[IsTouching](../../../../../api-ref/1.0/Box2D/html/classb2_contact/#a367dc9a563ad7db5547f4247777a33c9)() const | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [inline]` |
**m_fixtureA** (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected]` |
**m_fixtureB** (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected]` |
**m_flags** (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected]` |
**m_friction** (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected]` |
**m_indexA** (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected]` |
**m_indexB** (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected]` |
**m_manifold** (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected]` |
**m_next** (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected]` |
**m_nodeA** (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected]` |
**m_nodeB** (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected]` |
**m_prev** (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected]` |
**m_restitution** (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected]` |
**m_toi** (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected]` |
**m_toiCount** (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected]` |
[ResetFriction](../../../../../api-ref/1.0/Box2D/html/classb2_contact/#ad66d9290da187cef4c9f48c5766d4460)() | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [inline]` |
[ResetRestitution](../../../../../api-ref/1.0/Box2D/html/classb2_contact/#a243501bc5c146e9eb1296162d328aef1)() | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [inline]` |
**s_initialized** (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected, static]` |
**s_registers** (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected, static]` |
[SetEnabled](../../../../../api-ref/1.0/Box2D/html/classb2_contact/#a6edf582f8c161d6632854cddefe55a0c)(bool flag) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [inline]` |
[SetFriction](../../../../../api-ref/1.0/Box2D/html/classb2_contact/#a5e8fbb6bb2966ac84272bb0ea9d2e4c7)(float32 friction) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [inline]` |
[SetRestitution](../../../../../api-ref/1.0/Box2D/html/classb2_contact/#a24ca342c2bb766c53ef5ad04f5268fc1)(float32 restitution) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [inline]` |
**Update**(b2ContactListener *listener) (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [protected]` |
**~b2Contact**() (defined in [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/)) | [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) | ` [inline, protected, virtual]` |