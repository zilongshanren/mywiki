---
title: 'Game Physics: Stability – Warm Starting | Ming-Lun "Allen" Chou | 周明倫'
url: https://allenchou.net/2014/01/game-physics-stability-warm-starting/
author: Allen Chou
published: '2014-01-07'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Physics Series](http://allenchou.net/game-physics-series/).

Besides using [slops](http://allenchou.net/2014/01/game-physics-stability-slops/), “warm starting” is also a very common technique used to make physics engines more stable. Warm starting works particularly well when your game has high “frame coherence”, which is usually the case.

### Frame Coherence

Frame coherence is a measurement of how much your game scene changes across time steps. If the position and velocity of rigid bodies do not change a lot between two time steps, then these two frames have high frame coherence.

Having a high frame coherence has many implications, one of the most important ones is that the resolution result of the current time step will be very close to the result from the previous time step. So, if we cache the resulting impulses applied to each rigid body in the previous time step, we can apply the same impulses at the beginning of the resolution phase of the current time step before the real resolution logic takes place. This would make the entire physics system converge to a global solution faster. For instance, stacked boxes would settle faster with warm starting. Note that we only apply warm starting to contacts that last more than one time step. No warm starting is applied to a contact within the time step of the contact’s creation.

From [my post about contact constraints](http://allenchou.net/2013/12/game-physics-resolution-contact-constraints/), you already see that we have the information of total Lagrange Multiplier stored per contact. This information acts as our “cache” and is carried across time steps.


### Persistent Contacts

For warm starting to work, we need to keep track of contact manifolds. We cannot simply clear them and recreate them during the collision detection phase at the beginning of every time step. As mentioned earlier, only warm start contacts that last more than one frame. We call them “persistent contacts”.

But how do we do that? We get a new contact point per collision pair every time step during the collision detection phase. How can we determine that the newly generated contacts are “persistent”? There are many ways to do this, and the approach I usually use is the easiest one: the proximity-based approach. The idea is simple: if the newly generated contact points are close to existing ones in the manifold, then we discard the newly created ones and mark the existing contacts as persistent, which make them eligible for warm starting.

For a physics system to be stable in terms of stacking, the contacts in a contact manifold should cover the downward (direction of gravity) projection of the center of mass of the higher object. Thus, we typically keep up to 4 contacts per manifold. When “merging” the new contact with the existing contact in a manifold, we will attempt to keep the contacts in the manifold as far apart as possible, so the region they form has a good chance of covering the downward projection of the center of mass.

Remember in [my post about EPA](http://allenchou.net/2013/12/game-physics-contact-generation-epa/) I said that you would typically want to store four points within a single piece of contact data, local and global contact positions on both colliders? You will see why you need all this information now. Below is an example of how to determine if an existing contact is invalid. You need the four points to determine if a contact in an existing manifold is still valid (i.e. colliders are still penetrating at that contact).

// check if any existing contact is not valid any more for (Contact &contact : manifold.contacts) { const Vec3 localToGlobalA = bodyA.LocalToGlobal(contact.localPositionA); const Vec3 localToGlobalB = bodyB.LocalToGlobal(contact.localPositionB); const Vec3 rAB = localToGlobalB - localToGlobalA; const Vec3 rA = contact.globalPositionA - localToGlobalA; const Vec3 rB = contact.globalPositionB - localToGlobalB; const const stillPenetrating = contact.normal.Dot(rAB) <= 0.0f; const rACloseEnough = rA.LengthSq() < persistentThresholdSq; const rBCloseEnough = rB.LengthSq() < persistentThresholdSq; // keep contact point if the collision pair is // still colliding at this point, and the local // positions are not too far from the global // positions original acquired from collision detection if (rACloseEnough && rBCloseEnough) { // contact persistent, keep contact.persistent = true; } else { // contact invalid, remove manifold.Remove(contact); } }

Next, we need to check if the newly generated contact in the current time step is close to any remaining valid contacts.

for (Contact &contact : manifold.contacts) { const Vec3 rA = newContact.globalPositionA - contact.globalPositionA; const Vec3 rB = newContact.globalPositionB - contact.globalPositionB; const bool rAFarEnough = rA.LengthSq() > persistentThresholdSq; const bool rBFarEnough = rB.LengthSq() > persistentThresholdSq; // proximity check if (rAFarEnough && rBFarEnough) manifold.Add(newContact); }

Lastly, if we have more than 4 valid contacts in the manifold, we need to cut the count down to 4. I learned the method I will present here from Andrew Alvarez, co-president of the DigiPen Game Physics Club.

The first contact you pick is the deepest penetrating one. The second one is the furthest contact from the first one. The third one is the furthest contact from the line segment formed by the first two. The fourth one if the furthest contact from the triangle formed by the first three; if the fourth point is within the triangle, then just discard it. All remaining valid contacts are then discarded. For simplicity, here I will just use `Contact::globalPositionA`

for the computation, ignoring `Contact::globalPositionB`

.

// find the deepest penetrating one Contact *deepest = nullptr; float penetration = -FLT_MAX; for (Contact &contact : manifold.contacts) { if (contact.penetration > penetration) { penetration = contact.penetration; deepest = &contact; } } // find second contact Contact *furthest1 = nullptr; float distanceSq1 = -FLT_MAX; for (Contact &contact : manifold.contacts) { const float dist = (contact.positionA - deepest.positionA).LengthSq(); if (dist > distanceSq1) { distanceSq1 = dist; furthest1 = &contact; } } // find third contact Contact *furthest2 = nullptr; float distanceSq2 = -FLT_MAX; for (Contact &contact : manifold.contacts) { const float dist = DistanceFromLineSegment(contact, deepest, furthest1); if (dist > distanceSq2) { distanceSq2 = dist; furthest2 = &contact; } } // find fourth contact Contact *furthest3 = nullptr; float distanceSq3 = -FLT_MAX; for (Contact &contact : manifold.contacts) { const float dist = DistFromTriangle(contact, deepest, furthest1, furthest2); if (dist > distanceSq3) { distanceSq3 = dist; furthest3 = &contact; } } manifold.Clear(); manifold.Add(*deepest); manifold.Add(*furthest1); manifold.Add(*furthest2); const bool onTriangle = OnTriangle(furthest3, deepest, furthest1, furthest2); if (!onTriangle) manifold.Add(*furthest3);

After making sure that our manifold holds up to 4 contacts, we are now ready for warm starting.

### Warm Starting

The warm starting step is very straightforward and, in fact, pretty much the same as the resolution logic for contact constraints, except that instead of computing the Lagrange Multiplier, you use the total Lagrange Multiplier cached from the previous time step. To avoid overshoot, I usually do not apply the full cached Lagrange Multiplier but use a fraction of it instead. That’s it!

### End of Warm Starting

With slops and warm starting, you should end up with a pretty stable physics engine. Various other techniques and hacks have been employed to make physics engines even more stable.

For instance, the game [Vessel](http://www.strangeloopgames.com/vessel/) iterates through rigid bodies starting from the ground using a [breadth-first search](http://en.wikipedia.org/wiki/Breadth-first_search) on the contact graph; when resolving a collision pair, the object closer to the ground is “locked” and treated as a static object, which greatly improves stability of stacked objects. This method is not perfect, though. It works pretty well in the game, because the game does not have any set-up that would cause this method to break down. One drawback of this method is that it cannot correctly handle a stack of objects when other objects hit the lower part of the stack. Lower objects are locked as the physics engine works its way up the stack and thus cannot “feel” the full weight of the stack. This can cause lower objects to have incorrect frictional response when they are pushed by other objects: they are as easy to push out from the stack as higher objects.

Wow. I hope I’m not making your blog ugly with my questions ^^.

The ReplaceWhenFull method re-builts the entire manifold trying to enclose the biggest area possible. I use that when no slots are available.

Don’t worry about it. The comment section is meant for discussion. You can shoot me emails if you prefer that way.

My question is, shouldn’t

`ReplaceWhenFull`

pick the best 4 contacts out of 5 (4 existing contact and`_cNewContact`

)? You are not processing`_cNewContact`

in`ReplaceWhenFull`

at all.You’re right… I forgot that… changing now; add the last one and stick with 4 points covering the biggest area possible.

Just figured out that I even got more than 2 contacts.

One thing I’ve noticed is that when projecting WorldB – WorldA difference on the world normal the new distance is negative because the normal points from A to B, but my EPA returns a positive distance at the time of collision. Are you considering that the penetration depth is always negative in the examples?

What happens when the contact isn’t far enough and it doesn’t get added? Don’t you forgot to say that if this happens we should replace the closest contact with the new one? That’s my approach:

The last comment was screwed by the editor. Here’s the true code:

http://pastebin.com/bR9k46qa

I simply discard new contacts if they are too close to existing contacts.

http://pastebin.com/dfE29kR5

Please see line 46-72

Oh. I see. You’ve made a system that is capable of handling more than one contact in the one-shot generation case.

Using EPA for instance the source contacts would be only one in your case? Am I correct?

In my example I’m assuming that I’ve just one contact. The pool of contacts I have is only 4 since it makes an plane.

Bullet also does that too, but I don’t know if all contacts are updated each time in a single shot. I’m updating all contacts (removing it if necessary) and adding new ones and enclosing the biggest planar area (expanding the points), but I’m having some problems because some contacts still not being removed and fixed contacts just explodes the simulation.

Here’s what I have now:

http://pastebin.com/iKzNW6Qs

Hey. I’ve found the error. My world-matrix inverse was incorrrect, so I was unable to get the local contact points correctly. It was strange since everything was working with the caching but those kind of errors sometimes are impossible to guess, sorry.

I’m not using the method of encover a planar manifold, but I got good results by just replacing the new contact with the contact with minimum penetration in the manifold if there is one slot free. This is handling it some cases where the box is just on the ground. It’s tricky since is not the correct way of handling it, but I’ll look one more time in your implementation to check if everything was right.

When I use the biggest area method I get numerical errors by using the closest distance computations. I’m using one contact per time I do:

Find deepest contact;

Build a line from the furthest contact of the deepest;

Build a triangle from those that is furthest from the line.

Create a quad with the furthese point from the triangle;

Do you get any undesired results from the numerical errors?

It was a problem with a static variable assignment. Fixed it.

I still don’t get better results thogh is much better than without PCMs. Here’s a video:

http://youtu.be/zXoyN6ZmRTg

Hey. I’ve solved my problem. It was a quaternion multiplication error. Thanks for your advices.

Here’s a video:

http://youtu.be/Z-0G8R-lE8Q

Awesome. I’m glad you figured it out. I wouldn’t have guessed quaternion multiplication errors.

Thanks. Facing with another problem now regards to the contact caching. Maybe in this one you can point the problem without too much trouble…

When having a box that is colliding on the plane I have 2 contact points only being cached, sometimes being deleted by the fact that the impulse applied on the end of the frame made the box move one of its diagonals. Here’s what I have:

http://pastebin.com/UA0uV0up

On the beginning of the frame the new contact is flagged do not do warm start if it was just created, so I warm start only those that last more than one frame.

Is it simple as that? Update contacts, get new, warm-start, loop?

Maybe is something that I’m missing or you didn’t have posted on the post.

Thanks.

To make things more stable. Try adding a slop value to the penetration depth by subtracting a small number from it, say 1cm.

This would cause objects to penetrate just a little bit, but make them more stable.

Also, don’t forget to update the penetration depth of cached contacts before Baumgarte Stabilization. This has caused me problems before. I forgot to update the penetration depth, so my engine incorrectly used the old penetration depth upon initial contact during Baumgarte Stabilization, resulting in a lot of jitter.

Do you mean using the penetration slop while updating all contacts? I already do on the solver in the pre-step process before warm-starting.

I use 0.2 as the Baumgarte factor and 0.05cm as slop.

I update the penetration depth when updating the contact points also.

My question is related to the contact caching.

You did not use

`_cNewContact`

in`ReplaceWhenFull`

at all.Hi. Nice article, but I have some questions:

At line 18

don’t you mean

?

The positionA squared lenght will return the squared distance from the origin, but I believe you said from the deepest point, that is the first one…

When you say point on triangle did you mean if the point it is inside the triangle or its distance is positive along its normal? Can you post how you’ve computed efficiently?

Also, do you know if there is any method faster than the below to compute the distance of a point from a triangle? I’m using barycentric coordinates to get the closest point on the triangle and performing the difference vector:

Thanks in advance ^^.

You are correct about the distance equation. That was a typo, and I’ve fixed it. Thanks for pointing that out.

Another way of calculating the closest point on a triangle to a point is using 2D projection. Let P0 be a point and (P1, P2, P3) be a triangle. Transform all the points, so that P1 ends up at the origin, P2 ends up on the x-axis, and P3 ends up on the xy-plane. Let (P0′, P1′, P2′, P3′) denote the transformed results of (P0, P1, P2, P3). Now the problem space is reduced down to 2D, i.e. on the xy-plane. Find the closest point in triangle (P1′, P2′, P3′) to P0′ using edge equations. The distance of this point to P0′ is your answer. This paper does a comparison of the two methods and says the 2D method is more efficient.

2D projection is definitely better. Thanks for that paper ^^.

I’m trying to implement a sequential impulse solver using split-impulses (pseudo-velocities) as Erin Catto described, but I’m having trouble with impulses generating a wrong behavior, and I’m pretty sure that I wrote the solver correctly. I’d like to know what you think that’s missing if possible.

That’s how I do:

Update contact points;

Create new contact points;

Apply forces (integrate velocities);

Apply Impulses (10 iterations);

Apply velocities (sum up bias velocities, integrate positions, zero bias velocities);

That’s a quick pastebin: http://pastebin.com/cHXCbp2y

Any help would be helpfull.

Can you describe the “wrong” behavior?

Sure.

The cubes (an example) start sliding on the plane (a big cube with zero mass).

I’ve disabled the tangential and bias velocities (penetration factor) correction, and the objects are responding correctly to the normal impulse (penetrating of course because I’ve disable the bias, but I see the correct impulse applied normally).

When using the bias or tangential they start to rotate, and when a edge of the cube is colliding it keeps rotating to front and right like if there was an joint on the top of it.

I’m not using warm-starting yet, but the problem is pretty obviously that isn’t the warm-starting. I think that the problem is with the inertia tensor of the cube or something related to the angular velocities. Probably the angular velocity correction. I’ve reviewed the code more than 50 times. I’ve debugged all my normals, contact points, tangents, and they’re OK.

I’m calculating the relative velocity each time a constraint is being solved. I’m using two tangential directions (using Erin Catto’s ComputeBasis if the length of the tangent velocity is zero from the relative velocity) normal, and bias normal impulse accumulator. The bias velocity is cleared after each velocity integration.

Here’s the code:

http://pastebin.com/K1iF06nH

I’ve run into something visually similar to yours. If I remember correctly, my problem was not updating the relative velocity before solving each constraint, which you already do. Sorry, but I can’t pinpoint your exact problem by looking at your code. Perhaps start with only normal impulse, and enable one feature at a time at a more granular level, to see exactly when the problem starts showing?