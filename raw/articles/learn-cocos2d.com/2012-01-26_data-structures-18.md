---
title: Data Structures
url: http://www.learn-cocos2d.com/api-ref/1.0/Chipmunk/html/group__cp_spatial_index/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

| struct |
|

`dynamicIndex`

against the objects in `staticIndex`

using the query callback function. `func`

will be called once for each object. `func`

for each potential match. `func`

for each potential match. Spatial indexes are data structures that are used to accelerate collision detection and spatial queries. Chipmunk provides a number of spatial index algorithms to pick from and they are programmed in a generic way so that you can use them for holding more than just [cpShape](http://www.learn-cocos2d.com/api-ref/1.0/Chipmunk/html/structcp_shape/) structs.

It works by using `void`

pointers to the objects you add and using a callback to ask your code for bounding boxes when it needs them. Several types of queries can be performed an index as well as reindexing and full collision information. All communication to the spatial indexes is performed through callback functions.

Spatial indexes should be treated as opaque structs. This meanns you shouldn't be reading any of the struct fields.

Bounding box tree velocity callback function. This function should return an estimate for the object's velocity.

Spatial index bounding box callback function type. The spatial index calls this function and passes you a pointer to an object you added when it needs to get the bounding box associated with that object.

| typedef void(*
|

Spatial index/object iterator callback function type.

| typedef void(*
|

Spatial query callback function type.

| typedef void(*
|

| typedef void(*
|

| typedef void(*
|

Spatial segment query callback function type.

| typedef void(*
|

|

Initialize a bounding box tree.

Allocate and initialize a bounding box tree.

Set the velocity function for the bounding box tree to enable temporal coherence.

|

Initialize a spatial hash.

|

Allocate and initialize a spatial hash.

Change the cell dimensions and table size of the spatial hash to tune it. The cell dimensions should roughly match the average size of your objects and the table size should be ~10 larger than the number of objects inserted. Some trial and error is required to find the optimum numbers for efficiency.

| void cpSpatialIndexCollideStatic | ( |
|

Collide the objects in `dynamicIndex`

against the objects in `staticIndex`

using the query callback function.

| static
|

` [inline, static]`

Returns true if the spatial index contains the given object. Most spatial indexes use hashed storage, so you must provide a hash value too.

Get the number of objects in the spatial index.

Destroy a spatial index.

| static void cpSpatialIndexEach | ( |
|

` [inline, static]`

Iterate the objects in the spatial index. `func`

will be called once for each object.

| static void cpSpatialIndexInsert | ( |
|

` [inline, static]`

Add an object to a spatial index. Most spatial indexes use hashed storage, so you must provide a hash value too.

| static void cpSpatialIndexPointQuery | ( |
|

` [inline, static]`

Perform a point query against the spatial index, calling `func`

for each potential match. A pointer to the point will be passed as `obj1`

of `func`

.

| static void cpSpatialIndexQuery | ( |
|

` [inline, static]`

Perform a rectangle query against the spatial index, calling `func`

for each potential match.

Perform a full reindex of a spatial index.

| static void cpSpatialIndexReindexObject | ( |
|

` [inline, static]`

Reindex a single object in the spatial index.

| static void cpSpatialIndexReindexQuery | ( |
|

` [inline, static]`

Simultaneously reindex and find all colliding objects. `func`

will be called once for each potentially overlapping pair of objects found. If the spatial index was initialized with a static index, it will collide it's objects against that as well.

| static void cpSpatialIndexRemove | ( |
|

` [inline, static]`

Remove an object from a spatial index. Most spatial indexes use hashed storage, so you must provide a hash value too.

| static void cpSpatialIndexSegmentQuery | ( |
|

` [inline, static]`

Perform a segment query against the spatial index, calling `func`

for each potential match.

|

Initialize a 1D sort and sweep broadphase.