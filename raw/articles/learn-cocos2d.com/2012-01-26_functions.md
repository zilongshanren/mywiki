---
title: Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Chipmunk/html/group__cp_vect/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Functions
|
static [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) | [cpv](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#ga80c0be464748ff46ad20b58e22ea7d81) (const [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) x, const [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) y) |
| | Convenience constructor for [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) structs.
|
[cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) | [cpvlength](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#ga77014268325c2b7c93ee59f64cd78a5c) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v) |
| | Returns the length of v.
|
[cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) | [cpvslerp](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#gad894c8a975c4afb57f1ca45907417754) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v1, const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v2, const [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) t) |
| | Spherical linearly interpolate between v1 and v2.
|
[cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) | [cpvslerpconst](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#ga03d3b2cc67829761ed03a33d203000d9) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v1, const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v2, const [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) a) |
| | Spherical linearly interpolate between v1 towards v2 by no more than angle a radians.
|
[cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) | [cpvforangle](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#ga554792bf6678c80b2606720e6f977101) (const [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) a) |
| | Returns the unit length vector for the given angle (in radians).
|
[cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) | [cpvtoangle](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#ga283b3cb38342bffe145247aec08a242b) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v) |
| | Returns the angular direction v is pointing in (in radians).
|
| char * | [cpvstr](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#ga37480a0e70b8ae9e1ea74e6483555305) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v) |
static [cpBool](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gab6e5d8afee598a57cd323abae5310244) | [cpveql](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#gae5081f933bcc2c64c76d7e7caaf2d631) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v1, const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v2) |
| | Check if two vectors are equal. (Be careful when comparing floating point numbers!)
|
static [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) | [cpvadd](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#ga167e0bde13a745299bd5d4164d7c796b) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v1, const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v2) |
| | Add two vectors.
|
static [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) | [cpvsub](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#gafd88a5bbd4b5de25aa31e44fdf01e259) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v1, const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v2) |
| | Subtract two vectors.
|
static [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) | [cpvneg](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#gab79a1d52de40bf0f7db5134da436426b) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v) |
| | Negate a vector.
|
static [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) | [cpvmult](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#ga717188d925550baf62188b5e1e602047) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v, const [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) s) |
| | Scalar multiplication.
|
static [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) | [cpvdot](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#ga3e76653b018d47f864c339092cf482f1) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v1, const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v2) |
| | Vector dot product.
|
static [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) | [cpvcross](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#gaf9618b7690ad0c67dbe143c640590f7b) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v1, const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v2) |
static [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) | [cpvperp](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#gac4a0ba2873900342126c0449918764bc) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v) |
| | Returns a perpendicular vector. (90 degree rotation)
|
static [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) | [cpvrperp](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#ga0be2829df5c1be940484fb64b7cab61e) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v) |
| | Returns a perpendicular vector. (-90 degree rotation)
|
static [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) | [cpvproject](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#gae9c42ec78caa7971459d10543b1549cd) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v1, const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v2) |
| | Returns the vector projection of v1 onto v2.
|
static [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) | [cpvrotate](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#gac9a0bb9221f9f2068a48985fa70b5226) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v1, const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v2) |
| | Uses complex number multiplication to rotate v1 by v2. Scaling will occur if v1 is not a unit vector.
|
static [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) | [cpvunrotate](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#gac2b1120be08ee9225eadede83f5e054b) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v1, const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v2) |
| | Inverse of [cpvrotate()](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#gac9a0bb9221f9f2068a48985fa70b5226).
|
static [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) | [cpvlengthsq](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#gadfad8e091ac399cdc377a9c475f7ef0d) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v) |
| | Returns the squared length of v. Faster than [cpvlength()](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#ga77014268325c2b7c93ee59f64cd78a5c) when you only need to compare lengths.
|
static [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) | [cpvlerp](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#gab93f4924f5369c10782de6dba5ef38da) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v1, const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v2, const [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) t) |
| | Linearly interpolate between v1 and v2.
|
static [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) | [cpvnormalize](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#ga0fd46c6ef6dcca0dc7b6c6cef8008758) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v) |
| | Returns a normalized copy of v.
|
static [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) | [cpvnormalize_safe](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#gae2567a9766419f4b9021b4917a4d6fa3) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v) |
| | Returns a normalized copy of v or cpvzero if v was already cpvzero. Protects against divide by zero errors.
|
static [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) | [cpvclamp](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#ga21bac66ee11661debe4d1ddfb710f5f8) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v, const [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) len) |
| | Clamp v to length len.
|
static [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) | [cpvlerpconst](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#gaaf91d2bdafb741a35ab2dc6300d9fa81) ([cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v1, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v2, [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) d) |
| | Linearly interpolate between v1 towards v2 by distance d.
|
static [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) | [cpvdist](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#ga07488fb10c3ffb842b78ae66a2d90c00) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v1, const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v2) |
| | Returns the distance between v1 and v2.
|
static [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) | [cpvdistsq](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#gadb0ce5353909318beb7ee3163f7c3152) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v1, const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v2) |
| | Returns the squared distance between v1 and v2. Faster than [cpvdist()](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#ga07488fb10c3ffb842b78ae66a2d90c00) when you only need to compare distances.
|
static [cpBool](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gab6e5d8afee598a57cd323abae5310244) | [cpvnear](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#ga2ffc18e3b7405c28e92b6aa0f6cad746) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v1, const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v2, const [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) dist) |
| | Returns true if the distance between v1 and v2 is less than dist.
|
Variables
|
static const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) | [cpvzero](../../../../../api-ref/1.0/Chipmunk/html/group__cp_vect/#ga18f97c9678bcb262ce182f336dad2318) = {0.0f,0.0f} |
| | Constant for the zero vector.
|

Chipmunk's 2D vector type along with a handy 2D vector math lib.

Chipmunk's 2D vector type.