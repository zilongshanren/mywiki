---
title: Bezier Curve Optimization
url: http://hacksoflife.blogspot.com/2011/09/bezier-curve-optimization.html
author: Benjamin Supnik
published: '2011-09-03'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I've been meaning to write up a few notes about how we turn


First, a few basics:



We divide the problem into two parts: converting the polyline to a piece-wise bezier curve and optimizing that bezier curve to reduce point count.


To build the initial beziers we take an idea from ATI's


The idea is actually a lot easier to understand for polylines, where the dimensionality is lower. For each vertex in our road, we'll find the "average" direction of the road (the tangent line) at that vertex based on the two segments coming into that vertex. The bezier control points adjacent to the vertex must run along that tangent line; we can then adjust the distance of the control points from the end point to control the amount of "bulge".


We start with a poly-line.


We calculate the tangents at each vertex.


We place bezier control points along the tangents at fixed fractional lengths.


The result is a smooth piece-wise approximation through every point.

PN triangles tends to make meshes "bulge", because a curve around a convex hull always extends outward. You can see the same look in our interpolation. This is good for on-ramps but actually looks quite bad for a straight-away road - the road "bulges out" when the curve ends.


To address this, we categorize a road as "straight" if the road is long enough that


The five curve cases, illustrated.






[OSM](http://www.openstreetmap.org/)vector data into bezier curves for X-Plane. The code is all open source - look in the scenery tools[web code browser](http://dev.x-plane.com/cgit/)at[NetPlacement.cpp](http://dev.x-plane.com/cgit/cgit.cgi/xptools.git/tree/src/XESCore/NetPlacement.cpp%20)and[BezierApprox.cpp](http://dev.x-plane.com/cgit/cgit.cgi/xptools.git/tree/src/XESCore/BezierApprox.cpp)for the code.First, a few basics:

- OSM vector data comes as a polyline data - that is, each road is a series of points connected by straight line segments. There are a
*lot*of points - sometimes every few meters along a road. - X-Plane 10 uses piece-wise bezier curves, meaning a road is a string of end-to-end bezier curves. Each curve can be a line segment, quadratic, or cubic bezier curver, but not anything of higher degree.
- The representation in X-Plane for the piece-wise bezier curves is a list of "tagged" points, where the tag defines whether a point is a piece-wise curve end-point or control point. Semantically, the two end points must not be control points (must not be tagged) and we can never have more than two consecutive control points (because that would define a higher-order bezier).
- There is no requirement that the curve be smooth - we can create a sharp corner at any non-control point, even between two bezier curves.

We divide the problem into two parts: converting the polyline to a piece-wise bezier curve and optimizing that bezier curve to reduce point count.

To build the initial beziers we take an idea from ATI's

[PN-Triangles](http://www.google.com/url?sa=t&source=web&cd=1&ved=0CBYQFjAA&url=http%3A%2F%2Falex.vlachos.com%2Fgraphics%2FCurvedPNTriangles.pdf&rct=j&q=ATI%20PN-triangles&ei=wlJiTq3rH8PLgQetn-2JCg&usg=AFQjCNHxphyL1VbOOweccvXQp-iWecI9MA&cad=rja)paper. The basic idea from the paper is this: if we have a poly-line (or triangle mesh) approximation of a curved surface, we can estimate the tangents at the vertices by averaging the direction of all incident linear components. With the tangents at the vertices, we can then construct a bezier surface through that tangent (because a bezier curve's tangent at its end point runs toward the next control point) and use that to "round out" the mesh.The idea is actually a lot easier to understand for polylines, where the dimensionality is lower. For each vertex in our road, we'll find the "average" direction of the road (the tangent line) at that vertex based on the two segments coming into that vertex. The bezier control points adjacent to the vertex must run along that tangent line; we can then adjust the distance of the control points from the end point to control the amount of "bulge".

![]() |

![]() |

![]() |

![]() |

To address this, we categorize a road as "straight" if the road is long enough that

*if*we built a curve out of it, the radius of that curve would be larger than a constant value. (We pick different constants for different types of roads.) In other words, if two highway segments are each 1 km long and they meet at a 3 degree angle, we do not assume it is part of an arc with a 19 km radius - we assume that*most*of the 1 km road are straight, with a small curve (of much smaller radius) at the end. For any given point, we can decide whether either one or both of the two adjoining line segments is "straight" or should be entirely curved. We then form five cases:- If two segments come together at a very sharp angle, we simply keep the sharp angle. We assume that if the data had this sharp angle in the original vector data (which is quite highly noded) then there really is some kind of sharp corner.
- If the two segments come together at a very shallow angle, we simply keep the corner, because who cares. This case matters when we have a very tiny angle (e.g. 0.25 degrees) but very long line segments, such that removing the tiny angle would cause significant change in the vector position due to the long "arm" and not the steep angle. We trust that for our app the tiny curve isn't going to be visible.
- If the two segments are both curved, we use the PN-triangle-style tangents as usual.
- If one of the segments is curved and one is straight, the tangent at the point comes from the straight curve. This takes the "bulge" out of the beginning and ending of our curves by ensuring that the curve ends by heading "into" the straight-away.
- If both segments are straight, we need to round the corner on the inside. We do this by pulling back the corner along both curves and using the original point as a quadratic bezier control point.

![]() |

With these five curve cases we get pretty good looking curved roads. But our point gets out of control - at a minimum we've kept every original point, and on top of that we've added one or two bezier contrl points per segment.

What we need to do is generalize our curves. Again, the PN-triangles observation can help us. If we want to replace two piece-wise bezier curves with a single one, we know this: the tangent at the end of the curves can't change. This means that the two control points of the approximate curve must be colinear with the control points of the original curve ends and the original curve ends itself.

So what? Well, if we can only move the control points "in and out" then there are really only two scalar variables for

*all*possible approximations: how much to scale the control handles at the start and end. And that's something we can check with brute force!Below is the basic step to approximating a piece-wise bezier curve with two pieces as a single cubic bezier.

We start with a piece-wise bezier with nodes and control points.


For each range of curves that we will simplify, we "push" the outermost control points along the tangent vector by an arbitrary scaling factor.


The resulting curve will be close, but not quite the same as the original.


The original also looks "reasonable" on its own - that is, the approximations tend to have good curvature characteristics.

To find the approximate curve, we simply "search" a whole range of scalar values by trying them and measuring curve error. In the scenery tools code, we do a two-step search, refining the scalars around the values of least error. The initial values are picked experimentally; it's almost certainly possible to do a better job of guessing scalar values but I haven't had time to research it more.


To measure the error we approximate the bezier with polylines (e.g. we turn each individual bezier into a poly-line of N segments) and then compare the polylines. The polyline comparison is the variance of the distances of each point in one polyline to the other. (in other words, we treat one polyline as a point set and take the variance of the distance-to-polyline of each point). This is similar to the


![]() |

![]() |

![]() |

![]() |

To measure the error we approximate the bezier with polylines (e.g. we turn each individual bezier into a poly-line of N segments) and then compare the polylines. The polyline comparison is the variance of the distances of each point in one polyline to the other. (in other words, we treat one polyline as a point set and take the variance of the distance-to-polyline of each point). This is similar to the

[Hausdorff distance](http://en.wikipedia.org/wiki/Hausdorff_distance)with two key differences:- Because we are taking variance and not a minimum error, we can't use our previous minimum distance from a point to a line segment to limit our spatial searches. (See below.) Instead, we pick some large distance beyond which the curves are too different and we use that to limit. For low maximum acceptable errors this gives us good performance.
- Since the variance depends on all points and not just the worst one, we can rank multiple approximations - that is, generally better approximations score quite a bit higher.

Phew. So we can take a piece-wise bezier and come up with the best approximation through brute force and error checking. How do we simplify an entire road? The answer is

*not*[Douglas-Peuker](http://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm). Instead we use a bottom-up combine:- For every non-end node in the piece-wise curve, we build the approximation of the two adjoining bezier curves and measure its error.
- We queue every "possible merge" by error.
- Until the queue is empty or the lowest error is too large we..
- Replace the two curves in the merge by one.
- Recalculate the two neighboring merges (since one of their source curves is now quite a bit different). Note that we must keep the original beziers around to get accurate error metrics, so a merge of two curves that originally covered eight curves is an approximation of all eight originals, not the two previous merges.

## No comments:

## Post a Comment