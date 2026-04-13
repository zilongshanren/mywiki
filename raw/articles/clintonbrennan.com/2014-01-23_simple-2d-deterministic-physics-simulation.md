---
title: Simple 2D Deterministic Physics Simulation
url: http://clintonbrennan.com/2014/01/simple-2d-deterministic-physics-simulation/
author: Clinton
published: '2014-01-23'
source_blog: Clinton Brennan
source_site: http://clintonbrennan.com
category: game programming
fetched: '2026-04-13'
---

**Motivation**

When using a lockstep approach to networking we need to guarantee that each client will stay in sync with each other. One possible area of non-determinism can be the physics simulation. The physics simulation in Unity is not deterministic across multiple platforms. The problem is due to the fact that floating points can be handled differently on different machines depending on the compiler settings and optimizations. This gave me the motivation to implement my own custom physics engine using integer math only.

Unity3D uses NVIDIA’s PhysX engine. It mentions about the usage of Lockstep, Determinism and this engine in the following link:

[PhysX Knowledge Base](http://www.nvidia.com/object/physx_knowledge_base.html)

In the Real Time Strategy game I am developing, all of the collisions will only occur on the x-z plane, so I only need a 2D physics simulation. Furthermore, the objects can all be represented with either a Circle or a Rectangle to keep the simulation simple. Note that the game will still be rendered in 3D and the physics will only be ran in 2D “behind the scenes”.

**Overview**

Collisions are resolved by using Impulse Resolution. My implementation of this is based on the following article:

I also used a QuadTree Data Structure to limit the number of collisions that have to be checked each frame. This is achieved in two phases. The first phase known as the “Broad Phase” will compare all objects within the same region in the QuadTree to each other using an axis aligned bounding box (AABB) test (for the rectangle objects it just uses the rectangle, for circles a rectangle is used that the circle would fit in). The AABB test is very quick compared to checking against a circle. This check gives us a list of potential collisions. Next we iterate through the potential collisions, determine if they did indeed collide, and if they did perform the impulse resolution to them as described in the above article. This phase is called the “Narrow Phase”.

**The Game World Scale**

In order to have more accuracy but maintain integers, the Physics Engine has a Game World Scale. This is used to scale up floating points. The Game World Scale is set at 100. This will give us accuracy up to two decimal points in Unity. This can be adjusted simply by changing the Game World Scale.

public class PhysicsEngine { public const int GameWorldScale = 100; ... }

The suffix GWN (game world number) is added to some variables in the PhysicsObject to denote that it is in the Game World Scale.

**The Physics Object**

The physics object represents the object in our 2D world. It has a collider that is either a Rectangle or a Circle. The collider is used for the physics calculations. It also has a Bound object that is always a Rectangle and is the AABB of the object. This is used during the Broad Phase. The Physics object also has a Velocity, Mass, and Restitution.

The Physics object also allows you to attach one of any other object to it. This is useful to retrieve references to other objects in Unity when doing collision checks (for instance to determine if you ran into a building or a unit).

object attached; public void Attach<T>(T t) where T:class { attached = t; } public T GetAttached<T>() where T:class { return attached as T; }

**The Broad Phase**

A QuadTree is a datastructure that can be used to recursively subdivide a region. Each region is a rectangle. The QuadTree will initially start out representing the entire area. As Objects are added to the QuadTree, it will divide itself into four sub QuadTrees when it reaches a certain limit and then move the objects to the sub QuadTree the object belongs in. The amount of objects to split on is a setting that is set when initializing the QuadTree. The QuadTree should also be limited to how many times it can split. This is because we want the smallest QuadTree region to still be larger than the area of our largest object. This is another setting that is set during initialization. Once the QuadTree reaches it’s maximum subdivisions, it will no longer split based on the maximum object setting. Instead it will just add it to the existing regions. In my implementation, if an objects region spans across multiple QuadTree regions, it will be added to each. So each object in the worst case can be in four QuadTrees (with the assumption made earlier that the smallest QuadTree region is still larger than our largest object region). When ever an object moves it is removed from the QuadTree, and then added back with it’s new location. Using this approach keeps us from having to rebuild the QuadTree every frame.

During the broad phase of the Physics Update, we iterate through each QuadTree region and find all potential collisions. Since an object can be in multiple QuadTree regions, it is possible that the collision will show up multiple times. To avoid duplicate collisions, I first defined a BraodPhaseCollision object that will hold the two objects that collided. I then override the GetHashCode() method and implemented it in a way that the hash code will be the same regardless of the order the objects are stored in the BroadPhaseCollision object. I also did the same for the Equals() method. Next I used a HashSet to hold all of the BroadPhaseCollision objects that where found. The HashSet data structure guarantees that an object will only be added once even if you call Add multiple times with the same object. Using this method a collision between [Object A and Object B] and a collision between [Object B and Object A] will be considered the same.

internal class CollisionBroadPhase { public PhysicsObject A { get; private set; } public PhysicsObject B { get; private set; } private int hash; internal CollisionBroadPhase(PhysicsObject a, PhysicsObject b) { A = a; B = b; //make sure objects are always in the same order when calculating hash if (A.CompareTo(B) < 0) { hash = new Tuple<PhysicsObject, PhysicsObject>(A, B).GetHashCode(); } else { hash = new Tuple<PhysicsObject, PhysicsObject>(B, A).GetHashCode(); } } public override int GetHashCode() { return hash; } public override bool Equals(object obj) { if (obj is CollisionBroadPhase) { CollisionBroadPhase other = (CollisionBroadPhase)obj; if((A.Equals(other.A) && B.Equals(other.B)) || (A.Equals(other.B) && B.Equals(other.A))) { return true; } } return false; } }

**The Narrow Phase**

At this point we will have a set of BroadPhaseCollision objects that are potentially colliding. Next we iterate through those objects and test if they have an actual collision. We have three different collision types:

- Rectangle vs. Rectangle
- Circle vs. Circle
- Rectangle vs. Circle

Each collision will be handled slightly different. For more details please see the link mentioned in the overview. Each object has a Velocity (a 2D Vector) and a “restitution” to determines the “bouncy-ness” of the object. Additionally each object will also have a “Mass”. A Mass of 0 will indicate the object cannot be moved.

**The main physics loop**

After the narrow phase, each object’s Velocity will be updated based on the collision. The main physics loop will then iterate through all objects and update their location based on their Velocity. Velocity is in Units per Second, so the velocity will be updated based on the passed in Frames per Second rate.

Then each objects velocity will be reduced towards 0 based on a defined “friction” amount. The friction is applied after the collisions so that it does not have to overcome friction to separate the two objects. In this implementation we only have friction between the objects and the x-z plane. There is no friction calculations between each object.

public void Update(int fixedFramesPerSecond) { OrderedSet<CollisionBroadPhase> broadCollisions = broadPhaseCollisionDetector.GetAllCollisions(); foreach (CollisionBroadPhase broadCollision in broadCollisions) { CollisionResolver.ResolveCollision(broadCollision); } foreach (PhysicsObject physicsObject in PhysicsObjects) { if (physicsObject.MassGWN > 0 && physicsObject.Velocity != Vector2Int.Zero) { //remove from quad tree as it's position is about to change broadPhaseCollisionDetector.Remove(physicsObject); physicsObject.Center = physicsObject.Center + (physicsObject.Velocity / fixedFramesPerSecond); //apply friction physicsObject.Velocity = physicsObject.Velocity.MoveTowardsZero(Friction / fixedFramesPerSecond); broadPhaseCollisionDetector.Insert(physicsObject); } } }

**Source Code**

[Source Code on Bit Bucket](https://bitbucket.org/oneangrymachine/brennangames/overview)

Bitbucket says I don’t have access to that repository.

Sorry! Just made it public

Hi Clinton,

thanks for this post.

Any chance of a working link of the source?

Hello, I am trying to study creating RTS games for my hobby project.

When I click the BitBucket link, It says “You do not have access to the repository”.

Is it already not available..?

:'(

Hi Clinton,

Thanks for the great article, i was hoping to poke around in the source, but it seems to be removed?

Cheers!

Karl

Hi Clinton!

This was a really interesting article to read, I am trying to implement a basic 2D physics simulation as well! The result is kind of similar as far as I can tell, apart from the fact that mine is still broken 😛

Found this page looking for solutions to my problems, so I wondered, why not asking: i tried converting a classical engine using floats directly to integers, scaling up the values as you did. How did you solve some multiplication and division problems? For instance, if you get to normalize a vector, how do you keep track of the scale in the whole process?

By the way, I tried to check the source code, just of curiosity, but it was inaccessible.

Thanks a lot!

Hey Clinton,

Would this plug in to your lockstep code? Noticed that you had

SceneManager.Manager.TwoDPhysics.Update (GameFramesPerSecond);

commented out there.

Yes it does 🙂

Hey Clinton, thanks for writing this up. It’s been a great help for my project. How would you issue movement on a unit with a physics object attached? What I’ve come up with is altering the velocity of the physics object, though because it works with integers only the collider doesn’t remain in position with the unit:

https://dl.dropboxusercontent.com/u/96502721/S/2dphys.mp4 (gray sphere represents the collider, capsule is the unit)

I think I’ve come up with a solution by replacing integers with fixed point arithmetic. Hopefully it remains deterministic, I suppose I’ll find out someday.

Anyways thanks again for the article and source!

To keep the collider in position with the unit, I use the following

I use a utility class with this method:

public static Vector3 ConvertFromGameWorld(Vector2Int vec2)

{

//this assumes the game world is on the x,z plane

return new Vector3(

vec2.X / ((float) PhysicsEngine.GameWorldScale),

0,

vec2.Y / ((float) PhysicsEngine.GameWorldScale)

);

}

and then in a Component attached to the object the collider is for, i have this:

void Update () {

Vector3 vect = Converter.ConvertFromGameWorld(unit.physObj.Center);

transform.position = new Vector3(vect.x, y, vect.z);

}

unit is another component I have the physics object attached to.