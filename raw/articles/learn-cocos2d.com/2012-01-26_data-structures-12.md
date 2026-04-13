---
title: Data Structures
url: http://www.learn-cocos2d.com/api-ref/1.0/Chipmunk/html/group__cp_poly_shape/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Data Structures
|
| struct | [cpPolyShapeAxis](../../../../../api-ref/1.0/Chipmunk/html/structcp_poly_shape_axis/) |
| struct | [cpPolyShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_poly_shape/) |
Functions
|
[cpPolyShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_poly_shape/) * | [cpPolyShapeAlloc](../../../../../api-ref/1.0/Chipmunk/html/group__cp_poly_shape/#ga3c45ef999add9db8c9d7115ace013b3e) (void) |
| | Allocate a polygon shape.
|
[cpPolyShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_poly_shape/) * | [cpPolyShapeInit](../../../../../api-ref/1.0/Chipmunk/html/group__cp_poly_shape/#ga2743bd7e3b635dddea06ced835cb94d6) ([cpPolyShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_poly_shape/) *poly, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, int numVerts, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) *verts, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) offset) |
[cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) * | [cpPolyShapeNew](../../../../../api-ref/1.0/Chipmunk/html/group__cp_poly_shape/#gab4a4748c2291066a87a81cf515fa336f) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, int numVerts, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) *verts, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) offset) |
[cpPolyShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_poly_shape/) * | [cpBoxShapeInit](../../../../../api-ref/1.0/Chipmunk/html/group__cp_poly_shape/#ga476f01323ea40342b8f08a32a158bf73) ([cpPolyShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_poly_shape/) *poly, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) width, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) height) |
| | Initialize a box shaped polygon shape.
|
[cpPolyShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_poly_shape/) * | [cpBoxShapeInit2](../../../../../api-ref/1.0/Chipmunk/html/group__cp_poly_shape/#ga22965f0e9808961967267065518339f0) ([cpPolyShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_poly_shape/) *poly, [cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, [cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) box) |
| | Initialize an offset box shaped polygon shape.
|
[cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) * | [cpBoxShapeNew](../../../../../api-ref/1.0/Chipmunk/html/group__cp_poly_shape/#gacdeb44c68f1860e12048b339d56eef67) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) width, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) height) |
| | Allocate and initialize a box shaped polygon shape.
|
[cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) * | [cpBoxShapeNew2](../../../../../api-ref/1.0/Chipmunk/html/group__cp_poly_shape/#gaa7210464f25ddfd8a29f81f265d883df) ([cpBody](../../../../../api-ref/1.0/Chipmunk/html/structcp_body/) *body, [cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) box) |
| | Allocate and initialize an offset box shaped polygon shape.
|
[cpBool](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gab6e5d8afee598a57cd323abae5310244) | [cpPolyValidate](../../../../../api-ref/1.0/Chipmunk/html/group__cp_poly_shape/#ga66e76627fbdd6032aaede226a0959620) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) *verts, const int numVerts) |
| | Check that a set of vertexes is convex and has a clockwise winding.
|
| int | [cpPolyShapeGetNumVerts](../../../../../api-ref/1.0/Chipmunk/html/group__cp_poly_shape/#ga72ffc0d1f7ba9eb05ad105dc82531f23) ([cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape) |
| | Get the number of verts in a polygon shape.
|
[cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) | [cpPolyShapeGetVert](../../../../../api-ref/1.0/Chipmunk/html/group__cp_poly_shape/#ga1ef71ccf85d93b7f272d220511603823) ([cpShape](../../../../../api-ref/1.0/Chipmunk/html/structcp_shape/) *shape, int idx) |
| | Get the `ith` vertex of a polygon shape.
|