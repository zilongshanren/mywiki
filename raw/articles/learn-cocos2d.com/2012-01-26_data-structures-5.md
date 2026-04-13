---
title: Data Structures
url: http://www.learn-cocos2d.com/api-ref/1.0/Chipmunk/html/group__cp_b_b_b/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Data Structures
|
| struct | [cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) |
| | Chipmunk's axis-aligned 2D bounding box type. (left, bottom, right, top) [More...](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/#details)
|
Functions
|
static [cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) | [cpBBNew](../../../../../api-ref/1.0/Chipmunk/html/group__cp_b_b_b/#ga3282803074394675a42a881f5e965541) (const [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) l, const [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) b, const [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) r, const [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) t) |
| | Convenience constructor for [cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) structs.
|
static [cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) | [cpBBNewForCircle](../../../../../api-ref/1.0/Chipmunk/html/group__cp_b_b_b/#gaff0810056e31d1f3d66abf88dccf0f4d) (const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) p, const [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) r) |
| | Constructs a [cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) for a circle with the given position and radius.
|
static [cpBool](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gab6e5d8afee598a57cd323abae5310244) | [cpBBIntersects](../../../../../api-ref/1.0/Chipmunk/html/group__cp_b_b_b/#gac4a5fd7846b67f8711d3afb7536adbd5) (const [cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) a, const [cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) b) |
| | Returns true if `a` and `b` intersect.
|
static [cpBool](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gab6e5d8afee598a57cd323abae5310244) | [cpBBContainsBB](../../../../../api-ref/1.0/Chipmunk/html/group__cp_b_b_b/#gae0f2d67ca77b4b510c1a9c3a744627ba) (const [cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) bb, const [cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) other) |
| | Returns true if `other` lies completely within `bb` .
|
static [cpBool](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gab6e5d8afee598a57cd323abae5310244) | [cpBBContainsVect](../../../../../api-ref/1.0/Chipmunk/html/group__cp_b_b_b/#gaee3aab91cca0adbe8c830cac0951da6a) (const [cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) bb, const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v) |
| | Returns true if `bb` contains `v` .
|
static [cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) | [cpBBMerge](../../../../../api-ref/1.0/Chipmunk/html/group__cp_b_b_b/#gacde4506e27649bb6773009c337266d0d) (const [cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) a, const [cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) b) |
| | Returns a bounding box that holds both bounding boxes.
|
static [cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) | [cpBBExpand](../../../../../api-ref/1.0/Chipmunk/html/group__cp_b_b_b/#gad995b2feaa55d6bc858e8f930a4ed325) (const [cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) bb, const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v) |
| | Returns a bounding box that holds both `bb` and `v` .
|
static [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) | [cpBBArea](../../../../../api-ref/1.0/Chipmunk/html/group__cp_b_b_b/#gadc31eb18f01b1200938b21ed7e35257a) ([cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) bb) |
| | Returns the area of the bounding box.
|
static [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) | [cpBBMergedArea](../../../../../api-ref/1.0/Chipmunk/html/group__cp_b_b_b/#ga89f37acb475dd1dc1b6571282033c0f0) ([cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) a, [cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) b) |
| | Merges `a` and `b` and returns the area of the merged bounding box.
|
static [cpFloat](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gac1ed65573e035bf892505768c852d8d3) | [cpBBSegmentQuery](../../../../../api-ref/1.0/Chipmunk/html/group__cp_b_b_b/#gaf623a5ee2e14df8c002fd742b08686d1) ([cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) bb, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) a, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) b) |
| | Returns the fraction along the segment query the [cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) is hit. Returns INFINITY if it doesn't hit.
|
static [cpBool](../../../../../api-ref/1.0/Chipmunk/html/group__basic_types/#gab6e5d8afee598a57cd323abae5310244) | [cpBBIntersectsSegment](../../../../../api-ref/1.0/Chipmunk/html/group__cp_b_b_b/#ga65157a1d957e6069aef614dca588a705) ([cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) bb, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) a, [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) b) |
| | Return true if the bounding box intersects the line segment with ends `a` and `b` .
|
[cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) | [cpBBClampVect](../../../../../api-ref/1.0/Chipmunk/html/group__cp_b_b_b/#gaffb72e6849121c764eb4ac58ebb9ed55) (const [cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) bb, const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v) |
| | Clamp a vector to a bounding box.
|
[cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) | [cpBBWrapVect](../../../../../api-ref/1.0/Chipmunk/html/group__cp_b_b_b/#gaf6f534fd78ebfb5b822f3f7c3da03b0d) (const [cpBB](../../../../../api-ref/1.0/Chipmunk/html/structcp_b_b/) bb, const [cpVect](../../../../../api-ref/1.0/Chipmunk/html/structcp_vect/) v) |
| | Wrap a vector to a bounding box.
|

Chipmunk's axis-aligned 2D bounding box type along with a few handy routines.