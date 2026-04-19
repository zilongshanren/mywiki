---
title: Ghost Collisions
url: https://box2d.org/posts/2020/06/ghost-collisions/
published: '2020-06-21'
source_blog: Box2D
source_site: https://box2d.org/
category: graphics
fetched: '2026-04-19'
---

Dealing with ghost collisions is a challenging problem in game physics. The basic idea comes from motion across a flat surface. You may have several shapes joined together to make a flat surface, like a triangle mesh in 3D or a chain of edges in 2D. Convex shapes can hit the internal connections and have their motion blocked. This is undesirable, we would rather have the convex shape move smoothly across the surface. A real-life analogy is tripping on cracks in the sidewalk.

The image below shows a box sliding to the right across two connected edges (line segments). The box is slightly overlapped with the edges. This sort of overlap is inevitable in a physics engine, especially with discrete collision detection. As the box moves to the right along edge1, it encounters edge2. The shortest path to resolve collision with edge2 is to push the box to the left instead of up. This blocks the motion of the box.

A more extreme example happens when the surface is not flat. This images shows a box hitting the backside of a peak.

![Backside Collision](../../assets/53ecd5a1e7bc79ff.png)


## Chain Shapes

Box2D supports chain shapes, which are a sequence of edges connected end-to-end. The chain can be open or closed (a loop). It is expected that the chain shape does not self-intersect. Chain shapes are intended to be used for static game level geometry that can be convex or concave.

A goal for chain shapes has to been to support smooth collision by eliminating ghost collisions. Another goal has been to support two-sided collision to give more freedom to level design. As we will see, these two goals are conflicted.

## Contact Generation

Box2D generates contacts by colliding edge shapes with convex shapes (polygons or circles). These are done one-by-one for each edge shape in a chain. The chain shape provides each edge shape some context about neighbors. Each edge shape knows about the vertices of its neighboring edge shapes. This information can be used to eliminate ghost collisions. These neighboring vertices are called ghost vertices.

```
class EdgeShape
{
Vec2 vertex1;
Vec2 vertex2;
Vec2 ghost1;
Vec2 ghost2;
};
```


Box2D uses the [Separating Axis Test](https://en.wikipedia.org/wiki/Hyperplane_separation_theorem) (SAT) and [Sutherland-Hodgman](https://en.wikipedia.org/wiki/Sutherland%E2%80%93Hodgman_algorithm) clipping to compute the contact points and normals. In 2D these algorithms are simple and robust.

## Voronoi Regions

Consider a box on top of a flat edge with an edge sloping down to the right. As the box moves to the right we can imagine it tilting on the corner where the two edges meet. As it tilts the contact normal goes from pointing up to pointing up and to the right, perpendicular to the sloped edges. So the valid range of normals is between normal1 and normal2.

Any collision normal computed must live in this range or be discarded. Otherwise the box will be pushed in the wrong direction. What does discarding mean? Suppose the collision algorithm processes one edge at a time. First I collide the shape with edge1 and then with edge2. If an edge generates a normal outside of that region then that normal is ignored and generates zero contact points. This prevents backside or internal collisions.

## Concave collision

If two edges meet at a concave angle then things are actually simpler. In this case the two edges can only collide along their normals. If both edges are infinite and one-sided then we can just compute the collision along the edge normal and be done.

There are some implementation details. Since Box2D uses the Separating Axis Test. It may be that the box face has the normal with least overlap. This could end up pushing the box in the wrong direction. So I need to only consider the edge normal.

## Multiple edges

In practice there are multiple edges chained together. However, Box2D only collides with one edge at a time. For a give edge, the two vertices can be convex or concave in any combination. There are three unique configurations.

For the left configuration the Voronoi region sweeps out a wedge from the left normal to the right normal. The middle configuration only allows an upward normal. The right configuration only allows a normal between the wedge of the left edge normal and the upward normal of the middle edge.

## Examples

How do we make use of these Voronoi regions within a SAT framework that solves one edge at a time? Lets consider some examples.

But first lets discuss what kind of cases we should consider. Cases with no overlap are not interesting because they don’t require any special handling. The normals will always be in range. Also I think [significant overlap](http://box2d.org/posts/2020/04/stuck-inside/) is an important use case for real games. So I will only consider cases with significant overlap.

### Case 1: Convex-Convex

The following figure shows a case where the box is tilted and overlapping the left edge.

There is a small amount of overlap with the top edge. The SAT will tell us to push the box away from the top edge along the lower right box face. This normal happens to be to the left of the Voronoi region. What shall we do? Here are a couple options:

- Snap the normal to the closest Voronoi region and compute the penetration along that direction
- Ignore the collision with the top edge

Option 2 is appealing because it is faster and from the image we can be confident that the left edge will take care of the collision completely on its own. Also in this case the normal would be snapped to align with the left edge, leading to redundant contact points.

By the way, Option 2 matches Pierre Terdiman’s feature voiding approach [presented here](http://www.codercorner.com/blog/?p=1156).

### Case 2: Concave-Concave

Lets consider another case with a concave corner. Again I am considering collision between the box and the middle edge. In this case the box may have a collision normal from SAT aligned with the right box face. This is outside of the Voronoi region. In this case we have to snap the normal to align with the edge normal. If we ignore the collision the box can slide through the middle edge. We have to snap the normal to the middle edge normal. This will push the box up.

It seems that we can skip collisions outside of the Voronoi regions of convex corners but collisions around concave corners must be snapped.

### Case 3: Concave-Convex

How about the case where one corner is concave and one is convex? In this case we still need to snap normals generated on the concave side. But the middle edge can ignore the box on the convex side since that collision will be fully handled by the right edge.

These rules can be encoded in a [Gauss Map](https://en.wikipedia.org/wiki/Gauss_map). I classify three regions: admit, skip, and snap.

## Two-sided collision

Ideally we want smooth two-side collision with edge chains. Is this possible?

In order to compute the correct Voronoi region, I need to know if the chain vertices are concave or convex. I cannot classify the vertices unless I know if the shape is inside or outside the chain loop. This is the [point-in-polygon problem](https://en.wikipedia.org/wiki/Point_in_polygon) where the point in consideration is the centroid of the convex shape (circle or polygon).

It is also possible in Box2D to create non-looping chains with unconnected ends. This still amounts to a similar inside-outside problem as a closed loop.

It is tempting to use only the neighboring ghost vertices of an edge to try to determine if the shape is inside or outside the chain. But using only the immediate neighbors is insufficient.

For example, consider the scenario in the figure below. The long box is colliding with edge2. Locally box appears to be inside this chain of edges considering edge1 and edge2. This makes the bottom left vertex appear concave and the contact normal with edge2 is admitted.

Now tilt the box to the left. Looking at the centroid, the box seems to be outside the edge chain and so the bottom left vertex is convex. Therefore the contact normal on edge2 is skipped (to avoid a ghost collision).

However, we did not consider that there could be a second neighbor edge0 that is also tilted to the left. Now the box seems to be on the inside of the chain and now the bottom left vertex is once again concave. If we don’t consider the second neighbor the box will incorrectly falls through edge2.

In general, it is not enough to consider just first neighbors or even second neighbors. We need to solve the global point-in-polygon problem to be confident.

Chain shapes are meant to be used for building large game worlds, so the chain loops can contain hundreds of edges. It is too expensive to perform the point-in-polygon test. Therefore, it seems that smooth collision can only be efficiently and robustly achieved with one-sided edge chains.

## Results

This video shows a classic problem in game physics: *the cliff problem*. The top box is hitting the back-side of the vertical edge, causing it to trip and tumble. The bottom box is on an edge chain that uses connectivity information to smooth the collision and prevent the backside collision.