---
title: Data Structures
url: http://www.learn-cocos2d.com/api-ref/1.0/Chipmunk/html/group__cp_shape/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Data Structures
|
| struct | [cpSegmentQueryInfo](../../../../../api-ref/1.0/Chipmunk/html/structcp_segment_query_info/) |
| | Segment query info struct. [More...](../../../../../api-ref/1.0/Chipmunk/html/structcp_segment_query_info/#details)
|
| struct | [cpShapeClass](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape_class/) |
| struct | [cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) |
| | Opaque collision shape struct. [More...](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/#details)
|
Defines
|
| #define | [CP_DefineShapeStructGetter](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#ga547d234d61a90a7128ab1f3d00e31939)(type, member, name) static inline type cpShapeGet##name(const [cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape){return shape->member;} |
| #define | [CP_DefineShapeStructSetter](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#ga50b46e99728173c218c2787804d6a17e)(type, member, name, activates) |
| #define | [CP_DefineShapeStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#ga43af86383b8a6bf8dd80a6943e6de274)(type, member, name, activates) |
| #define | [CP_DeclareShapeGetter](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#gac3014abac96cf5fcdff8415043bd5545)(struct, type, name) type struct##Get##name(const [cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape) |
Typedefs
|
typedef [cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/)(* | [cpShapeCacheDataImpl](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#gab8535aa43d884033c0e070b10a2eea09) )([cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) p, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) rot) |
| typedef void(* | [cpShapeDestroyImpl](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#gae59221f927147fd1703d5bfb3c55dc68) )([cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape) |
typedef [cpBool](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gab6e5d8afee598a57cd323abae5310244)(* | [cpShapePointQueryImpl](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#gae80fdd7169c9f2a4ccd42701cd6eb57d) )([cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) p) |
| typedef void(* | [cpShapeSegmentQueryImpl](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#gabb2d4615c2ba473a3485b2a07b88895d) )([cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) a, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) b, [cpSegmentQueryInfo](../../../../../api-ref/1.0/Chipmunk/html/structcp_segment_query_info/) *info) |
Functions
|
| void | [cpShapeDestroy](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#gad4eff5be931cd7c3c5eaf9f431b73c9e) ([cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape) |
| | Destroy a shape.
|
| void | [cpShapeFree](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#ga5c1eff1ffaf87dda1890fa46ccba38b3) ([cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape) |
| | Destroy and Free a shape.
|
[cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) | [cpShapeCacheBB](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#ga8cff320455af31adba99b4ff70e085a9) ([cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape) |
| | Update, cache and return the bounding box of a shape based on the body it's attached to.
|
[cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) | [cpShapeUpdate](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#ga0b45787bf047be4d90b5d6e17d289151) ([cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) pos, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) rot) |
| | Update, cache and return the bounding box of a shape with an explicit transformation.
|
[cpBool](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gab6e5d8afee598a57cd323abae5310244) | [cpShapePointQuery](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#ga2fedaf2576eadfdce6f717d8e7133e5f) ([cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) p) |
| | Test if a point lies within a shape.
|
| | [CP_DefineShapeStructGetter](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#gad1203ed7586411e5cac0957617ff20c4) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *, body, Body) |
| void | [cpShapeSetBody](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#gafae3ee0e0629b9598ddeecb723b82de8) ([cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body) |
| | [CP_DefineShapeStructGetter](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#ga467136fb2e19e9ed4b211a85cfa027dc) ([cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/), bb, BB) |
| | [CP_DefineShapeStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#ga912d216d420a7af75f106736bf70666f) ([cpBool](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gab6e5d8afee598a57cd323abae5310244), sensor, Sensor, cpTrue) |
| | [CP_DefineShapeStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#gaff420a1b54782f944ff52fe8cc03b013) ([cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), e, Elasticity, cpFalse) |
| | [CP_DefineShapeStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#gaba7259f9f028d64a15b81fb378f3cfd8) ([cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3), u, Friction, cpTrue) |
| | [CP_DefineShapeStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#gaf5baa95ac683af9121dcbf5dcc27cb8e) ([cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/), surface_v, SurfaceVelocity, cpTrue) |
| | [CP_DefineShapeStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#gaefbcbe7d85908f0053b2096c9b931cc1) ([cpDataPointer](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#ga2ac2c3c31e21893941f9e4f8ee279447), data, UserData, cpFalse) |
| | [CP_DefineShapeStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#ga4a285dedcbe076a4cb1bd288b8ae37fd) ([cpCollisionType](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gae83e2f50965eb441e36ffff1e32e6d02), collision_type, CollisionType, cpTrue) |
| | [CP_DefineShapeStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#gaf81d51789b41c44a43993a7ba4bdaf5b) ([cpGroup](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gacd811b1135a8f4a3e5cc019552b18b1a), group, Group, cpTrue) |
| | [CP_DefineShapeStructProperty](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#gae5afaa69dbd04c5d41bea79bcffa0997) ([cpLayers](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#ga5ec31e87ed3973cab80f9bfbbbcb43bb), layers, Layers, cpTrue) |
| void | [cpResetShapeIdCounter](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#ga110560e4697ba1a76d2cae0908d5249e) (void) |
[cpBool](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gab6e5d8afee598a57cd323abae5310244) | [cpShapeSegmentQuery](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#ga0e2bfcdf0cb2e44846806b0787b13a3a) ([cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) a, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) b, [cpSegmentQueryInfo](../../../../../api-ref/1.0/Chipmunk/html/structcp_segment_query_info/) *info) |
| | Perform a segment query against a shape. `info` must be a pointer to a valid [cpSegmentQueryInfo](../../../../../api-ref/1.0/Chipmunk/html/structcp_segment_query_info/) structure.
|
static [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) | [cpSegmentQueryHitPoint](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#gaddbbb33934e6379fb64a0bd95cf6d743) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) start, const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) end, const [cpSegmentQueryInfo](../../../../../api-ref/1.0/Chipmunk/html/structcp_segment_query_info/) info) |
| | Get the hit point for a segment query.
|
static [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) | [cpSegmentQueryHitDist](../../../../../api-ref/1.0/Chipmunk/html/group__cp_shape/#ga43a89c56a870efa70eac346e736f498a) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) start, const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) end, const [cpSegmentQueryInfo](../../../../../api-ref/1.0/Chipmunk/html/structcp_segment_query_info/) info) |
| | Get the hit distance for a segment query.
|