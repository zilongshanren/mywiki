---
title: AI Steering
url: https://www.rorydriscoll.com/2016/10/14/ai-steering/
author: Rory
published: '2016-10-14'
source_blog: CodeItNow
source_site: https://www.rorydriscoll.com
category: graphics
fetched: '2026-04-13'
---

For many games, AI entites need to move around in a somewhat lifelike manner, or at the very least a consistent manner. The final decision as to which direction to move in can be quite complicated due to a number of competing factors, for example: Pathfinding waypoints, points of interest or obstacles. A common way to reduce the complexity of the decision is to separate the decision into several steering behaviors.

## Steering Behaviors

Craig Reynolds introduced a [paper](http://www.red3d.com/cwr/steer/)Â at GDC 1999 to deal with what he described as the middle level of a three-layer motion system (goal setting and strategy, steering behaviors and locomotion). The steering behavior system decomposes all of the decisions into smaller decisions focusing on one concern, and deals with merging the resulting directions in a final decision stage.

This system is very easy to implement, and is also very intuitive at first glance. In the paper, various behaviors are described as well as combinations of behaviors.

However, it is quite possible for the individual decisions made by each behavior to cancel each other out. For example, a seek behavior may want the entity to move due East, but an evade behavior may want the entity to move due West. In this case, it is typical to have some kind of weighting for each behavior to overcome the stalemate. But could a better decision be made?

## Context Maps

Andrew Fray describes the steering behavior problem in this [blog post](https://andrewfray.wordpress.com/2013/03/26/context-behaviours-know-how-to-share/)Â and describes a potential solution called context behaviors. He goes into further detail about context behaviors in the second half of this [GDC 2013 talk](http://www.gdcvault.com/play/1018262/The-Next-Vector-Improvements-in).

The general idea of context behaviors is for each behavior to decide how much it wants to move in each of a particular set of directions, and then to make the final decision based on looking at all possible directions. This is implemented via two context maps, one for expressing interest in each direction, and one for expressing danger. Each value in a context map is a normalized [0, 1] number expressing the degree of danger or interest.

The interest and danger maps are evaluated based on some decision-making heuristic, and one of the directions is selected as the desired steering vector.

In my initial implementation, I found it quite difficult to tune the heuristic in such a way as to balance the danger and interest. For example, when moving to a patrol point very close to a wall, the danger of colliding with the wall would override the interest of patrol point and the entity would never arrive. A fix for this was to calculate a danger threshold (based on knowing how the danger values translate to distance) for that particular patrol point. This meant that the entity could finally arrive, but it was also highly tolerant of danger in general the closer it got to the patrol point.

## Context Maps in Practice

I would like to briefly describe a few decisions I made while implementing context behaviors that I think might be of interest.

### Distances

The first change is to include the distance of the interest or danger along each of the directions. This creates a nice closed space around the entity for both interest and danger. Armed with this information, values of high interest that are nearer than the danger in the corresponding direction can be trivially accepted. If the danger is nearer than the interest, then again we have to fall back to a heuristic that will weigh the danger of going in that direction with the interest.

The decision-making heuristic can now also consider how far away the danger is, so it can perhaps choose to move in a dangerous direction for a while, safe in the knowledge that the actual danger is far away.

### Interpolation

The output of the decision making process is another context map with the normalized decision values for each direction. The obvious thing to do is to just pick the direction with the highest decision value. This works as expected, but can produce rather stilted motion due to the limited set of directions the entity is allowed to move in.

Andrew Fray briefly mentions the idea of using linear interpolation to extract a better decision direction. I chose instead to use cubic splines to interpolate the decision values since they are continuous as long as the tangents are selected consistently. The decision context map doesn’t explicitly have tangents, so the obvious thing to due is to calculate them via central differencing. At this point this is equivalent to using a [Catmull-Rom spline](http://www.mvps.org/directx/articles/catmull/). Catmull-Rom splines require four points in order to calculate a smooth value which normally creates issues at the beginning and end of the spline, however since our domain wraps around there isn’t an issue.

One nice thing about using cubic-splines is that you can take the derivative of the cubic function and then quickly find the maximum value over the entire spline. This provides a nice continuous decision direction (well, as continuous as the decision map is). Be aware that by interpolating like this, values can go outside the normalized range!

### Alignment

I started by using eight direction vectors (I’m talking 2D here) for the context space, where the first vector pointed down the world X-axis. The problem with this is that the direction of primary interest almost certainly doesn’t align with one of the directions. I would find that danger values (based on ray casts) could appear very late and at high danger values, causing the entities to swerve at the last minute.

I then tried aligning the directions with the linear velocity of the entity. This worked somewhat better but it caused quite a lot of flickering as the context maps changed quite considerably based on their primary direction. Interpolating between context maps for the previous and current frames would probably help this quite a bit, but I didn’t implement it.

What I’m currently doing is aligning the context maps in the direction of the high-level goal position. There may be other potential goal points, but one is the most important and so everything is aligned to this. By doing this, the most desired direction is always aligned with one of the context map directions.

## Examples

### Patrolling

In this example, the entity is trying to move to a patrol point on the to the left of the large grey rectangle obstacle. There is no path to the patrol point, so the entity is relying purely on steering.

This shows the space formed by the distances in the interest context map. You can see that the context map is aligned to point from the entity towards the goal. Note that there is some interest expressed in going away from the patrol point. This is critical for decision-making purposes to allow the entity to back out of dead-ends.

This shows the interpolated values of the interest map. The circle represents an interest value of 1. In this case the interest value for each direction is simply proportional to the angle to the goal point.

Absent of any danger, the direction selected in this example would be to move directly towards the patrol point. Of course this would make the entity collide with the environment.

### Static Obstacle Avoidance

This next example adds danger for the static obstactles in the environment.

This is for the same situation as above, but now shows the danger distances. These have been calculated by ray-casting into the environment. This provides a good, but not perfect, approximation of the space that is safe to move in.

For static obstacles, the normalized danger values are proportional to the distance to the collision up to a specified maximum.

This shows the final decision map that was generated via the decision-making heuristic. Despite wanting to move directly to the patrol point, the high danger in that direction has forced the entity to look elsewhere. The ground collision has all but ruled out moving downwards, so the decision selected (the yellow line) is to move up and fowards.

### Dynamic Obstacle avoidance

This example looks at a situation where avoidance of other entities (all dynamic entities have the cyan circle around them) is required. The entity is still moving to a patrol point far right of the screen.

Each pair of entities is tested to see if there is a potential future collision based on their current position and velocity. The potential collision positions are marked with the yellow lines and circles. Note that the entity on the left is predicting a collision with the entity on the right, but the entity on the right has selected the closer collision with the central entity as the one to be concerned about.

This shows the danger distances for the central entity only. The static obstacle distances are already present. The impact point has been projected onto any context map direction within 45 degrees of the impact direction. You can see that it has cut out a large space in the general direction of the predicted collision.

Like the static collisions, the dynamic collision values are initially based on the normalized predicted distance to impact. Additionally for dynamic collisions, directions which move away from the predicted impact point are scaled down. In this case, steering to the left of the potential collision is shown to be a dangerous option, but steering right is less dangerous.

The final decision shows a desire to move below the other entity as you might expect.

### Motion

This brieflyÂ showsÂ the decision map in motion. I’m assigning patrol points by mouse-clicking. Despite the lack of path-finding, the entity is capable of steering around quite a variety of obstacles.

## Final Notes

I’ve mentioned path-finding a couple of times in this post, and I should mention that this is not a replacement for path-finding. There are absolutely situations where the entity can get stuck if the environment is the wrong shape. This kind of steering would work well when moving to path waypoints though.

As I mentioned, I’m currently generating new context maps each frame, but I think that interpolating between maps for the previous and current frame would probably be a good idea. Another option would be to just damp the context maps from the previous frame and then run the context behaviors as normal. Compared to interpolating the maps, this method can deal with sudden, imminent danger much better.