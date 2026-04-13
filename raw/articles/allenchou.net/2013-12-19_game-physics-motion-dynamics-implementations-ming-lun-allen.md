---
title: 'Game Physics: Motion Dynamics Implementations | Ming-Lun "Allen" Chou | 周明倫'
url: https://allenchou.net/2013/12/game-physics-motion-dynamics-implementations/
author: Allen Chou
published: '2013-12-19'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Physics Series](http://allenchou.net/game-physics-series/).

This post presents possible implementations of motion dynamics for a physics engine. For fundamentals of motion dynamics, please refer to [this post](http://allenchou.net/2013/12/game-physics-motion-dynamics-fundamentals/).

### Rigid Body Interface

Below is what a typical rigid body partial interface would look like (there’s more that is not shown). Note that the data format of choice here for orientation is a 3-by-3 matrix. Also present in the data member list are inverse mass, local & global inverse inertia tensors, and inverse orientation. These inverse properties would be used quite frequently during force/torque application, collision detection, and resolution; thus, it is a good idea to compute and store them per time step.

If the name of a property does not indicate whether it is in world space (global) or model space (local), it is in world space. The reason why some properties have both global and local version would become apparent later.


struct RigidBody { float m_mass; float m_inverseMass; Mat3 m_localInverseInertiaTensor; Mat3 m_globalInverseInertiaTensor; Vec3 m_globalCentroid; Vec3 m_localCentroid; Vec3 m_position; Mat3 m_orientation; Vec3 m_linearVelocity; Vec3 m_angularVelocity; Vec3 m_forceAccumulator; Vec3 m_torqueAccumulator; ColliderList m_colliders; void UpdateGlobalCentroidFromPosition(void); void UpdatePositionFromGlobalCentroid(void); void UpdateOrientation(void); void AddCollider(Collider &collider); const Vec3 LocalToGlobal(const Vec3 &p) const; const Vec3 GlobalToLocal(const Vec3 &p) const; const Vec3 LocalToGlobalVec(const Vec3 &v) const; const Vec3 GlobalToLocalVec(const Vec3 &v) const; void ApplyForce(const Vec3 &f, const Vec3 &at); };

The `RigidBody::AddCollider`

method allows the rigid body to own multiple colliders (which, as mentioned in previous posts, are assumed to be convex shapes). This is called “compositing”. The centroid property is the combined center of mass of all colliders, and it can be different from `m_position`

. The `m_position`

property is really there for game visualization purposes, and is not related to the physics simulation. For instance, normally you would set the origin of a human character in model space at its feet. This is its “position”. It is obviously that the position is not the same as the character’s center of mass, which is typically around the center of the body.

However, the position and centroid properties are inter-dependent, so we need a way to update one based on the other. This is when `RigidBody::UpdateGlobalCentroidFromPosition`

and `RigidBody::UpdatePositionFromGlobalCentroid`

come into play.

void RigidBody::UpdateGlobalCentroidFromPosition(void) { m_globalCentroid = m_orientation * m_localCentroid + m_position; } void RigidBody::UpdatePositionFromGlobalCentroid(void) { m_position = m_orientation * (-m_localCentroid) + m_globalCentroid; }

### Collider

This is what a collider interface would look like (again, not shown fully).

struct Collider { // already computed based on geometry float m_mass; Mat3 m_localInertiaTensor; Vec3 m_localCentroid; // geometry-related part not shown };

When a collider is added through `RigidBody::AddCollider`

, some of the rigid body’s physical properties need to be updated.

void RigidBody::AddColliders(Collider &collider) { // add collider to collider list m_colliders.Add(collider); // reset local centroid & mass m_localCentroid.Zero(); m_mass = 0.0f; // compute local centroid & mass for (Collider &collider : m_colliders) { // accumulate mass m_mass += collider.m_mass; // accumulate weighted contribution m_localCentroid += collider.m_mass * collider.m_localCentroid; } // compute inverse mass m_massData.inverseMass = 1.0f / m_mass; // compute final local centroid m_localCentroid *= m_massData.inverseMass; // compute local inertia tensor Mat3 localInertiaTensor; localInertiaTensor.Zero(); for (Collider &collider : m_colliders) { const Vec3 r = m_localCentroid - collider.m_localCentroid; const float rDotR = r.Dot(r); const Mat3 rOutR = r.OuterProduct(r); // accumulate local inertia tensor contribution, // using Parallel Axis Theorem localInertiaTensor += collider.localInertiaTensor + collider.m_mass * (rDotR * Mat3::Identity() - rOutR); } // compute inverse inertia tensor m_localInverseInertiaTensor = localInertiaTensor.Inverted(); }

During the accumulation of local inertia tensor contribution from collidres, Parallel Axis Theorem is used. You can read about it in details [here](http://en.wikipedia.org/wiki/Parallel_axis_theorem). Basically, this formula allows us to compute inertia tensors with respect to an arbitrary reference point that is not the center of mass of colliders. In this case, the reference point is the center of mass of the rigid body.

### Space Conversion

With the orientation matrix and its inverse available, it is very easy to convert points and vectors between world space (global) and model space (local). Note that the rigid body’s position only affects the conversion of points, not vectors.

const Vec3 RigidBody::LocalToGlobal(const Vec3 &p) const { return m_orientation * p + m_position; } const Vec3 RigidBody::GlobalToLocal(const Vec3 &p) const { return m_inverseOrientation * (p - m_position); } const Vec3 RigidBody::LocalToGlobalVec(const Vec3 &v) const { return m_orientation * v; } const Vec3 RigidBody::GlobalToLocalVec(const Vec3 &v) const { return m_inverseOrientation * v; }

### Force Application

The `m_forceAccumulator`

and `m_torqueAccumulator`

properties are zeroed after integration. Through out the time step, these two properties would accumulate forces and corresponding torques. Note that in `RigidBody::ApplyForce`

both parameters are vectors in world space.

void RigidBody3D::ApplyForce(const Vec3 &f, const Vec3 &at) { m_forceAccumulator += f; m_torqueAccumulator += (at - m_globalCentroid).Cross(f); }

### Integration

Within each time step, the rigid body’s physical properties are updated using the [Semi-Implicit Euler Method](http://en.wikipedia.org/wiki/Semi-implicit_Euler_method), which basically uses the Euler Method to integrate the linear velocity and angular velocity first, and then integrate the position and orientation.

Recall that the change of linear velocity is accumulated linear impulse divided by mass (or multiplied by inverse mass), and the change of angular velocity is inverse inertia tensor times accumulated angular impulse. Linear impulse is the product of force and delta time; angular impulse is the product of torque and delta time.

Somewhere in your physics engine, you’ll write something like this:

// for each rigid body for (auto &body : rigidBodies) { // integrate linear velocity body.m_linearVelocity += body.m_massData.inverseMass * (body.m_forceAccumulator * dt); // integrate angular velocity body.m_angularVelocity += body.m_globalInverseInertiaTensor * (body.m_torqueAccumulator * dt); // zero out accumulated force and torque body.m_forceAccumulator.Zero(); body.m_torqueAccumulator.Zero(); // integrate position m_globalCentroid += m_linearVelocity * dt; // integrate orientation const Vec3 axis = m_angularVelocity.Normalized(); const float angle = m_angularVelocity.Length() * dt; m_orientation = RotationMatrix(axis, angle) * m_orientation; // update physical properties body.UpdateOrientation(); body.UpdatePositionFromGlobalCentroid(); }

### Orientation Update

After we have performed all changes to the rigid body’s orientation, we need to update the inverse orientation with the new orientation, which simply involves a matrix transpose (because the orientation is an [orthogonal matrix](http://en.wikipedia.org/wiki/Orthogonal_matrix)).

Prior to that, we’ll also need to “re-orthonormalize” the orientation matrix. This is because the orientation might become “not orthogonal enough” due to accumulated floating-point errors. In the graphics engine, if you use a 4-by-4 matrix where the 3-by-3 orientation part is not orthogonal, objects can appear distorted.

There are various ways to perform such a task. The [Gram-Schmidt process](http://en.wikipedia.org/wiki/Gram%E2%80%93Schmidt_process) is a well-known method commonly covered in Linear Algebra textbooks. However, in this particular scenario, the method would not treat all 3 off-orthonomalized basis vectors in the orientation matrix equally, where the direction of the first vector processed is always not modified, and the direction of the last vector processed is usually modified the most.

I prefer the quaternion approach. This method simply converts the orientation matrix to a quaternion, normalizes the quaternion, and then converts the quaternion back to a matrix. You can find out how to convert between matrices and quaternions [here](http://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation#Conversion_to_and_from_the_matrix_representation).

void RigidBody3D::UpdateOrientation(void) { // orthonormalize orientation matrix Quat q = m_orientation.ToQuat(); q.Normalize(); m_orientation = q.ToMatrix(); // compute inverse orientation matrix m_inverseOrientation = m_orientation.Transposed(); }

### Inverse Inertia Tensor Update

With the updated orientation matrix and inverse orientation matrix, the global inertia tensor should also be re-computed. Recall that the change of angular velocity due to torque is the product of inverse inertia tensor and torque. We can compute the change of angular velocity by transforming torque in world space to local space, use the local inertia tensor to calculate change of angular velocity in local space, and then convert the result back to world space. Thus, the global inverse inertia tensor is the concatenation of (from left to right) the orientation matrix, the local inertia tensor, and the inverse orientation matrix.

Thus, you’ll write this somewhere in your physics engine:

m_globalInverseInertiaTensor = m_orientation * m_massData.localInertiaTensor * m_inverseOrientation;

### End of Motion Dynamics Implementations

This concludes the demonstration of possible implementations of motion dynamics for a physics engine. Many gameplay utility functions can depend on the interface presented in this post.

Is your mat3 struct use Column major matrix?

or Row major matrix?

Row major.

Hi. Are you sure about “* dt”?

const float angle = m_angularVelocity.Length() * dt;

Yeah, I’m pretty sure.

Do you have an alternate interpretation or formula in mind?

Let’s discuss.

The natural inverse inertia tensor for objects is in local (object) coordinates. So why do you (and some but not all others) transform this matrix to world coordinates to then compute angular acceleration (which would then be, somewhat awkwardly around the world coordinate axes, not the natural local (object) axes)?

Most pre-collision forces on my objects will be in local-coordinates, for example “thrust” from rocket engines, which naturally generates forces in local-coordinates anyway. Sure, in some games (but not mine, since it takes place in space) have a gravity vector that is naturally in world-coordinates (a force towards negative z), but that doesn’t impact torque or angular acceleration anyway.

Currently I sum the forces in local-coordinates (transforming forces and points of application that are naturally in world-coordinates to local-coordinates as needed). So now I’m ready to write the next part of the integration process, and everything sure looks a lot more natural to compute in local-coordinates from here on. Plus doesn’t everyone store angular acceleration and velocity of their objects in local-coordinates like I do? Which means, when everything is recomputed in local-coordinates, the result is what I want to save, and I don’t need to transform it elsewhere (world coordinates).

Anyway, enough people transform their inverse inertia tensor to world-coordinates that I am curious why you and others do so. It seem like the unnatural choice to me. Can you explain please? Thanks.

If you already know that most of the forces in your game are expressed in local space, then sure, it is probably better to store inverse inertia tensors in local space.

I would argue that there is no such thing as “natural” inverse inertia tensors, and nor is there an absolutely “correct” way to store them. Whether you store the inertia tensors in local or world space depends on different scenarios and what you want to achieve. I would also argue that computing things in world space is not “awkward”. It’s a personal preference, really.

I wanted to build a generic physics engine that can be used in all sorts of different scenarios, so I chose to store both in local space and world space, and I decided to calculate most things in world space. I also provide interface to allow client code to apply forces in either local or global space.

I store the inverse inertia tensors in both local and world spaces because I need them both. The local inverse inertia tensors are used to update global inverse inertia tensors upon orientation change, and the global inertia tensors are used when resolving constraints; for example, contact resolving impulses come in world space, and there are two multiplications between contact resolving impulses and global inverse inertial tensors per colliding object pair per velocity iteration per time step. If N objects come into contact with an object and I only store local inverse inertia tensors, I would need to convert all contact resolving impulses into this object’s local space before resolving the constraint, which would involve extra vector-matrix multiplications per time step. I would very much like to avoid this overhead.

Again, making the choice between local space or global space really depends on what you want to achieve, and neither of them needs to be “unnatural” or “wrong”.

Please excuse my ignorance in this subject, but I wonder why the `applyForce` method subtracts m_globalCentroid rather than m_localCentroid. If i am applying a force `at` the center of the object then wouldn’t it make more sense to apply it at vec3(0, 0, 0) not vec3(body.position)?

Thanks very much for this physics series. I have been looking across the net for a great tutorial series like this and now i’ve found it!

Also, do you have a particular reason for using a matrix for orientation storage? Is there some places where you would prefer a quaternion?

As pointed out by the paragraph preceding the code snippet, the

`at`

argument here is in world space, hence the subtraction involving the global centroid. You can of course define the`ApplyForce`

function to use local coordinates, and the subtraction would involve the local centroid. It’s just a matter choice.If I want colliders to have a rotation, as well as a position, do I have to transform the collider’s inertia matrix to the rigid body’s local space before doing composition?

Also, is the global inverse inertia matrix calculation the same as inverting the local inertia matrix, then transforming with the orientation matrix?

Thanks!

1. You’ll have to calculate inertia tensor of all colliders of the same rigid body with respect to the center of mass of the rigid body, sum them up to get the total inertia tensor of the rigid body, and then compute the inverse inertia tensor of the rigid body.

2. Only for the orientational part. The translational part involves the Parallel Axis Theorem.

Hi Allen,

OK I think I have got it working now. The problem was with the length function from my vector/matrix library, I was calling it wrongly. Now its perfectly fine I can see my boxes fall down due to gravity. I can also change the orientation and see them fall. Now the thing I will work on is collision between the boxes and with the floor.

Let me know if you need the source code for the basic rigid body. I have used glm and freeglut libraries.

Thanks for the articles.

And there is a type here local variable should be v not p

Fixed. Thanks.

Should this line

be this

Outer product should give you a matrix or am I missing something?

You are correct. Thanks for pointing it out. Fixed.