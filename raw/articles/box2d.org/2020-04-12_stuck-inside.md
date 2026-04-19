---
title: Stuck Inside
url: https://box2d.org/posts/2020/04/stuck-inside/
published: '2020-04-12'
source_blog: Box2D
source_site: https://box2d.org/
category: graphics
fetched: '2026-04-19'
---

There a several computational geometry algorithms that are relevant for preparing collision data: convex hull, mesh simplification, and convex decomposition.

Many implementations of these algorithms are developed outside the specific context of rigid body simulation. For example, [qhull](http://www.qhull.org/) computes convex hulls and appears to be application agnostic. [Simplygon](https://www.simplygon.com/) is focused on simplifying render mesh.

On the other hand, convex decomposition algorithms such as [V-HACD](https://github.com/kmammou/v-hacd) are developed with physics simulation in mind. These algorithms are usually iterative and approximate. Both of these aspects are fine for games. We usually don’t need or want exact collision. This figure shows a typical result.

![V-HACD](../../assets/775a4ef441266833.png)


Consider a 2D table. This object is concave. If we want the object to be dynamic, it should be made into multiple convex shapes attached to a single rigid body. The reason convexity is important for dynamic objects is because convexity gives us a clear notion of inside versus outside.

Here is one possible convex decomposition.

This looks super simple and you can imagine an algorithm that could do this automatically for us. But is this a good solution for rigid body simulation in games?

One thing I have learned over many years of working on game physics is that it is always safest to assume that objects can and will become deeply overlapped. Overlap can come from level design, animation, or script. I think it is important to consider how the physics engine will respond to deep overlap. Consider the decomposed table with a beam jammed between the table top and the legs.

Box2D will see this situation as three independent collision pairs: beam versus top, beam versus left leg, and beam versus right leg. Each pair will do its best to resolve the collision but unaware of the other pairs. For example, this figure shows the contact points in the area around the top of the left leg.

The top of the table has a single contact point pushing down and the left leg has two contact points pushing up. A similar situation exists on the top of the right leg. The solver takes these points and basically fights with itself … and loses. So the beam remains stuck.

What can we do? We could consider some complex solution where we try to do something special with the internal faces of the decomposition. We cannot completely ignore these faces because need to use them to create separating axes. Otherwise we will get false positive collision. Overall there are many steps to make this work:

- Develop a convex decomposition algorithm
- Have the decomposition algorithm identify and tag the internal faces
- Have the collision algorithm somehow deal with these internal faces
- Remember to apply this to all relevant cases: polygon-circle, polygon-polygon, etc.
- Don’t forget about continuous collision

Consider a different approach where the legs are extended to the top of the table. In this case there is no channel where the beam can get stuck.

I made a demo of this in Box2D that shows the effect for the table and a similar situation for a wedge shaped space ship. When the collision shapes are overlapped the shape is immediately ejected. In addition to fixing the visual bug, this also improves performance by allowing the bodies to go to sleep.

A further refinement is to limit the overlap of parallel surfaces. This can prevent redundant contact points.

This technique of overlapping the convex shapes helps a lot. Maybe a convex decomposition algorithm can be made to do this (or maybe one already exists). However, in my opinion the human touch on collision authoring often leads to a superior result. I feel like attention to detail on collision authoring could use more promotion, so hopefully this helps.