---
title: Importing Faces Into CGAL Arrangements
url: http://hacksoflife.blogspot.com/2010/05/importing-faces-into-cgal-arrangements.html
author: Benjamin Supnik
published: '2010-05-06'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

- The polygons may collide with each other and thus there may be a 1:many relationship between the original data and the final map.
- The polygons may be self-intersected or in other ways "hosed", so we need a particular strategy for handling this situation.

- If you are using the general polygon set code that is built on top of arrangements, you can simply perform unions and intersections of a large number of faces. For merging a large number of areas, this code is faster than anything else you might code, because it can do an N-way divide and conquer, where N is larger than 2.
- For custom merging and handling of multiple polygons, you can use the overlay free function, which lets you specify how the combinations of each set of face from two maps are handled.
- You can simply insert a set of curves into an empty arrangement and they will be "swept" together. This is a useful way to turn a messy polygon into something useful - it finds intersections, builds topology, runs quickly, and handles input no matter how degenerate.

**Finding Polygon Internal Areas**

When building arrangements out of polygons of dubious origin (or simply building an arrangement out of a large number of unrelated polygons) I use a bulk insert to "sweep" the curves into the arrangement. How do I then find the faces? Here are three techniques:

The contained area of a polygon can be found by simply checking whether the face is bounded or not. This is not useful though when importing multiple polygons at the same time. (When I need this technique, each polygon is individually imported into its own arrangement, then all arrangements are merged later, typically with general-polygon-set code.)

We can implement a "toggle" policy (e.g. each line toggles interior vs. exterior) by doing a search from the outside to the inside of the arrangement, toggling whether we are "inside" or "outside" each time we cross a halfedge. The halfedges can retain curve-based properties; typically I use a consolidated data curve so that halfedges retain every property attached to them.

One danger: an antenna will produce incorrect results in this technique because it won't toggle the data property twice. This can be hard to work around because data from the insert is maintained per

*edge*, not half-edgeUnfortunately, topology of the final arrangement doesn't help us resolve this either. Imagine an antenna (in the original polygon that crashes into another polygon, thus becoming part of a real partition. Technically the original face is not split by the antenna, but the faces in the final arrangement are, so saying face()==twin()->face() doesn't tell us we have an antenna in the original.

Two ways to work around this: don't insert antennas, or don't tag known antennas with any data. Both cases require knowing that we have an antenna ahead of time.

Sometimes we want to use a "winding rule" - that is, contain areas inside closed left turning contours. This is, for example, useful when calculating offset buffers and minkowski sums; the artifacts from strange shapes being offset too much turn out not to be left turning contours and get thrown out.

To find the winding rule areas, we have to look at the direction of the curves inserted.

The way my code does this is to look at the direction of the underlying curve vs. the direction of the half-edge and then mark the half-edge as being on the "inside" or "outside" of the winding with a dat a field on the half-edge itself. This is reconstructed after bulk insert, and then we can traverse the whole arrangement, counting windings.

The limitation here is similar to above: if we have an antenna, the underlying curve can have only one direction, not two, and one half-edge will be incorrectly tagged. Fortunately antennas are not typically necessary to produce offset buffers.


## No comments:

## Post a Comment