---
title: Unity DOTS Character Controller
url: https://www.vertexfragment.com/ramblings/unity-dots-character-controller/
author: Steven Sell
published: '2020-08-27'
source_blog: Vertex Fragment
source_site: https://www.vertexfragment.com/
category: graphics
fetched: '2026-04-13'
---

Note: Please visit the GitHub repository for the latest version of the code. It tends to be updated more often than the article itself.

In this ramble we will cover how to write a basic character controller using Unity DOTS (Data-Orientated Tech Stack), with the new Entities (ECS) and Physics packages.

This stems from my work on Realms which, until recently, made use of a rigidbody controller which directly applied forces and impulses to the character. While rigidbody controllers suit certain games really well, they have a few key disadvantages which make them unsuitable for my needs. Chief among these are that rigidbody controllers tend to lack a certain level of control resulting in the player feeling like they are on ice. They also are unable to traverse vertical inclines, such as steps, as they simply get stuck on them.

This is where kinematic controllers shine as they solve these issues. However, anyone that has written a controller from scratch will attest to the fact they are finicky and full of edge-cases. The controller shown here will not be full-featured but will provide the following basic functionality:

Kinematic

Climb stairs

Constant speed up slopes

Does not slide down slopes

Does not get stuck in corners

Does not stick to walls

A demonstration of the controller is shown below.

Demonstrating stepping, sliding, and jumping.

Writing a Basic Character Controller

Our character controller will be composed of two different systems and accompanying components: character controller and player controller.

The former can be used by any entity, including AI, whereas the latter is used specifically to translate player input into character controller commands. In this way, all of our moving entities will make use of the same core logic and the only thing that varies is how the direction and magnitude of movement are set.

Character Controller Component

When programming using the ECS paradigm everything is split into three parts: entities, components, and systems. The entity is an id, components are pure data with no logic, and systems operate on that data. Each entity has a number of components associated with it, and the systems fire off only when there exists components for them to work with.

To begin creating our character controller we must first define our data which will be stored in a CharacterControllerComponent. For this particular implementation we will have three different groups of data within our component: movement input, control properties, and state. We could have this split into three distinct components, but it is easier to group them all together.

Start by adding the movement input properties to the component. These will be the properties that are manipulated by other systems in order to move the entity.

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15

/// <summary>
/// The current direction that the character is moving.
/// </summary>
public float3 CurrentDirection { get; set; }
/// <summary>
/// The current magnitude of the character movement.
/// If <c>0.0</c>, then the character is not being directly moved by the controller but residual forces may still be active.
/// </summary>
public float3 CurrentMagnitude { get; set; }
/// <summary>
/// Is the character requesting to jump?
/// </summary>
publicbool Jump { get; set; }

Next we add the control properties, which define how the entity will move.

For example how fast it can go and how high it can step up.

/// <summary>
/// Gravity force applied to the character.
/// </summary>
public float3 Gravity { get; set; }
/// <summary>
/// The maximum speed at which this character moves.
/// </summary>
publicfloat MaxSpeed { get; set; }
/// <summary>
/// The current speed at which the player moves.
/// </summary>
publicfloat Speed { get; set; }
/// <summary>
/// The jump strength which controls how high a jump is.
/// </summary>
publicfloat JumpStrength { get; set; }
/// <summary>
/// The maximum height the character can step up, in world units.
/// </summary>
publicfloat MaxStep { get; set; }
/// <summary>
/// Drag value applied to reduce the <see cref="JumpVelocity"/>.
/// </summary>
publicfloat Drag { get; set; }

Finally we have the internal state of the controller which lets us know the current accumulated velocity and whether it is on the ground or in the air.

1
2
3
4
5
6
7
8
9

/// <summary>
/// True if the character is on the ground.
/// </summary>
publicbool IsGrounded { get; set; }
/// <summary>
/// The current jump velocity of the character.
/// </summary>
public float3 JumpVelocity { get; set; }

For this controller we are using two separate velocities for moving the character: horizontal and vertical (gravity + jump). Some implementations combine these into a single vector, however I personally feel it is simpler to keep these separated and handle their resulting translations individually.

With our component defined, we next need a way to add it via the Editor. To do so, we create a new MonoBehaviour class which also implements the IConvertGameObjectToEntity interface. This interface defines the Convert method which is invoked at runtime to add our component to the appropriate entity.

In this we expose our control properties as well as define default values for them. This allows us to tweak the controls via the Editor to find the perfect values for our needs.

Character Controller System

With our data and component defined we can begin on the CharacterControllerSystem which performs the actual logic of moving our entities. The resulting system is fairly complex and so we will be breaking it into manageable chunks. For reference purposes, the complete system can be viewed here.

Building the System Skeleton

Our system will be job-based which adds some initial complexity but results in better performance, especially if we have a large number of active character controllers. Jobs are run asynchronously and have limitations on what they can receive as input and how they can manipulate entities.

We define our system as operating after the physics world has been updated, but before the end of the physics group of systems. This ensures we are operating on the most up-to-date physics data and will also allow us, in the future, to directly manipulate other physics-based objects by our collisions.

Let’s start by implementing our OnCreate method which will set up our system and our internal fields. These fields give us access to the current physics state and are:

buildPhysicsWorld: Used to retrieve the current physics state.

exportPhysicsWorld: Used to build our job dependencies.

endFramePhysicsSystem: Used to ensure our job fires before the end of the physics group.

characterControllerGroup: Defines the group of components that must be present on an entity for it to be operated on by our system.

In order for our system to operate on an entity, it must have all of the following components attached to it:

CharacterControllerComponent: Defines our controller data and behaviour.

Before implementing the rest of our OnUpdate we need to define the basic structure of our job which will be performing the actual work. This is because the OnUpdate will simply be compiling the input for the job and scheduling when it should be run.

So within our system class we will add a private job struct:

1
2
3
4
5
6
7

privatestructCharacterControllerJob : IJobChunk
{
publicvoid Execute(ArchetypeChunk chunk, int chunkIndex, int firstEntityIndex)
{
// ...

This defines our job as being a IJobChunk, meaning it operates on a chunk. Each entity belongs to a chunk, depending on the combination of components associated with it, and all entities with the same component combination are stored in the same chunk.

As input to the job as a whole, we will define public fields which will be set by our system. We will need the following data for our job to run:

DeltaTime: The amount of time, in seconds, since the last frame. This lets us have consistent movement regardless of frame rate.

EntityTypeHandle: A handle to all of the entities we will be working on.

CharacterControllerHandles: The controller components for our entities.

TranslationHandles: The position components for our entities.

RotationHandles: The rotation components for our entities.

ColliderData: Used by our physics utilities for retrieving colliders from arbitrary entities within a job.

If this was not a job, we would instead use the entity manager.

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17

privatestructCharacterControllerJob : IJobChunk
{
publicfloat DeltaTime;
[ReadOnly]public PhysicsWorld PhysicsWorld;
[ReadOnly]public EntityTypeHandle EntityType;
[ReadOnly]public ComponentDataFromEntity<PhysicsCollider> ColliderData;
public ComponentTypeHandle<CharacterControllerComponent> CharacterControllerType;
public ComponentTypeHandle<Translation> TranslationType;
public ComponentTypeHandle<Rotation> RotationType;
publicvoid Execute(ArchetypeChunk chunk, int chunkIndex, int firstEntityIndex)
{
// ...

With our job defined we can go back to our OnUpdate system method and schedule it. Once we have the job running we can begin implementing the actual controller logic.

First we will retrieve our job input data and create the job.

protectedoverride JobHandle OnUpdate(JobHandle inputDeps)
{
if (characterControllerGroup.CalculateChunkCount() == 0)
{
return inputDeps;
}
var entityTypeHandle = GetEntityTypeHandle();
var colliderData = GetComponentDataFromEntity<PhysicsCollider>(true);
var characterControllerTypeHandle = GetComponentTypeHandle<CharacterControllerComponent>();
var translationTypeHandle = GetComponentTypeHandle<Translation>();
var rotationTypeHandle = GetComponentTypeHandle<Rotation>();
var controllerJob = new CharacterControllerJob()
{
DeltaTime = Time.DeltaTime,
PhysicsWorld = buildPhysicsWorld.PhysicsWorld,
EntityHandles = entityTypeHandle,
ColliderData = colliderData,
CharacterControllerHandles = characterControllerTypeHandle,
TranslationHandles = translationTypeHandle,
RotationHandles = rotationTypeHandle
};
// ...

What are the GetComponentTypeHandle methods?

These return a ComponentTypeHandle<T> which is used in conjunction with the chunk in our job to retrieve a list of components.

Similarily, the GetEntityTypeHandle returns an EntityTypeHandle which is also used with the chunk to return all valid entities.

The return from GetComponentDataFromEntity<T> is not used specifically with the chunk but does allow us to check if an arbitrary entity has the component T and to retrieve that component.

Next we will schedule it so that it runs after the system dependencies and after the ExportPhysicsWorld is done. We also make sure it runs before the EndFramePhysicsSystem, which marks the end of the physics group of systems.

1
2
3
4
5
6

var dependency = JobHandle.CombineDependencies(inputDeps, exportPhysicsWorld.GetOutputDependency());
var controllerJobHandle = controllerJob.Schedule(characterControllerGroup, dependency);
endFramePhysicsSystem.AddInputDependency(controllerJobHandle);
return controllerJobHandle;

We build up our dependencies by combining the inputDeps to our system with the output of the exportPhysicsWorld. Our characterControllerGroup, built in the OnCreate method, is provided to the job to determine which chunks will be used.

Finally we set our job as an input dependency to the endFramePhysicsSystem and we return the job handle. This concludes the basic setup of our system and the accompanying job and we can now move on to implementing the actual controller logic.

Operating on Chunks

Our CharacterControllerJob operates on chunks that match our characterControllerGroup using the implemented Execute method. Currently our execute is empty, so we will begin by retrieving data from the handles provided as input.

1
2
3
4
5
6

publicvoid Execute(ArchetypeChunk chunk, int chunkIndex, int firstEntityIndex)
{
var collisionWorld = PhysicsWorld.CollisionWorld;
// ...

We start by extracting the CollisionWorld which is used as input to all of the physics queries that we will be using. After getting the collision world, we retrieve the lists of entities and components that we will be using.

1
2
3
4

var chunkEntityData = chunk.GetNativeArray(EntityHandles);
var chunkCharacterControllerData = chunk.GetNativeArray(CharacterControllerHandles);
var chunkTranslationData = chunk.GetNativeArray(TranslationHandles);
var chunkRotationData = chunk.GetNativeArray(RotationHandles);

Here we are guaranteed that the chunk has the required component data because we specified which chunks to operate on in our controllerJob.Schedule call within our OnUpdate method. If we tried retrieving a component list that was not specified by our group, or was specified in the Any field, then we would not have this guarantee and the call would fail.

How do you get optional component data?

Sometimes components are optional, and are not required to be on the entity we are working with. If we are not in a job we can use the EntityManager.HasComponent to check if the component is present, and then EntityManager.GetComponentData to retrieve it.

However, the EntityManager can not be passed into a job. So what do we do?

This is where the GetComponentDataFromEntity<T> method within the system is used. It provides a ComponentDataFromEntity<T> which can be used within a job to perform these actions.

1
2
3
4
5
6

if (componentData.HasComponent(entity))
{
var component = componentData[entity];
// ...

With our component arrays retrieved, we can now iterate over each valid entity in the chunk and perform our controller logic.

1
2
3
4
5
6
7
8
9
10
11
12
13

for (int i = 0; i < chunk.Count; ++i)
{
var entity = chunkEntityData[i];
var controller = chunkCharacterControllerData[i];
var position = chunkTranslationData[i];
var rotation = chunkRotationData[i];
var collider = ColliderData[entity];
HandleChunk(ref entity, ref controller, ref position, ref rotation, ref collider, ref collisionWorld);
chunkTranslationData[i] = position;
chunkCharacterControllerData[i] = controller;
}

Note that we update the component data in our translation and controller lists after the call to HandleChunk.

Finally we can declare our empty HandleChunk method which we will implement in the following sections.

privatestructCharacterControllerJob : IJobChunk
{
publicfloat DeltaTime;
[ReadOnly]public PhysicsWorld PhysicsWorld;
[ReadOnly]public EntityTypeHandle EntityType;
[ReadOnly]public ComponentDataFromEntity<PhysicsCollider> ColliderData;
public ComponentTypeHandle<CharacterControllerComponent> CharacterControllerType;
public ComponentTypeHandle<Translation> TranslationType;
public ComponentTypeHandle<Rotation> RotationType;
publicvoid Execute(ArchetypeChunk chunk, int chunkIndex, int firstEntityIndex)
{
var collisionWorld = PhysicsWorld.CollisionWorld;
var chunkEntityData = chunk.GetNativeArray(EntityType);
var chunkCharacterControllerData = chunk.GetNativeArray(CharacterControllerType);
var chunkTranslationData = chunk.GetNativeArray(TranslationType);
var chunkRotationData = chunk.GetNativeArray(RotationType);
for (int i = 0; i < chunk.Count; ++i)
{
var entity = chunkEntityData[i];
var controller = chunkCharacterControllerData[i];
var position = chunkTranslationData[i];
var rotation = chunkRotationData[i];
var collider = ColliderData[entity];
HandleChunk(ref entity, ref controller, ref position, ref rotation, ref collider, ref collisionWorld);
chunkTranslationData[i] = position;
chunkCharacterControllerData[i] = controller;
}
}
privatevoid HandleChunk(ref Entity entity, ref CharacterControllerComponent controller, ref Translation position, ref Rotation rotation, ref PhysicsCollider collider, ref CollisionWorld collisionWorld)
{
// ...

Velocity from Gravity

At this point our system and job can run and iterate over all of the valid entities. However, they don’t perform any actions on them yet.

This section, and the next few that follow it, will revolve around implementing the HandleChunk method which contains all of the actual controller logic. Which means that everything done so far was just setup! DOTS provides great performance, but unfortunately there is usually a lot of preparation involved.

We will begin our controller logic with the most basic and fundamental part: gravity.

Start by creating an epsilon vector which we used to offset our queries by a fraction, in the relative up direction (as determined by gravity).

This epsilon is added to the entity position to create our currPos vector. We want our queries to be offset because, ideally, our character will be resting directly on a surface. If we do not perform this offset, then our physics queries will receive collisions for the surface beneath us when they should not.

We then declare our various velocity vectors, but assign them to (0, 0, 0) for the moment. The first velocity, verticalVelocity, will be computed in the upcoming HandleVerticalMovement method, and the jumpVelocity in the IsGrounded and Jumping section.

Our gravityVelocity can be assigned as a function between the controller-defined gravity vector and the frame delta time.

Note that we cancel the gravity velocity if we are grounded. This is to help prevent a few unwanted effects, such as sliding down sloped surfaces and small jitters while standing still.

Next, we will invoke our HandleVerticalMovement method to calculate our verticalVelocity and then use that to determine the current position of the entity, affected by gravity.

The goal of this method is to calculate the totalVelocity resulting from vertical movement: gravity and jumping. To begin, we will assume that the total velocity is simply those two velocities added together.

1

totalVelocity = jumpVelocity + gravityVelocity;

Keeping in mind that for now, jumpVelocity is 0. Next we check if this velocity will result in any collisions for our entity. If there are none, then no further action is required. However, if we do encounter a collision then we have to make adjustments to avoid it.

To check for collisions we perform a ColliderCastAll from the current position to the position where the velocity would take us. We also trim out any results that we do not care about using the TrimByFilter utility in conjunction with our DynamicWithPhysical collision filter.

The Unity Physics package provides CollisionFilters as a way to control what collides with what. In our demo we provide a handful of filter layers, including:

Static

Dynamic

Terrain

TriggerVolume

In addition to layers there are several filters provided, including DynamicWithPhysical which defines collisions between a Dynamic object (our character) and any physical object (ie not a volume). This filter is used throughout the character controller so that we do not get false collision results from trigger volumes.

If there was a collision then we need to check to see how much penetration there is into the collided surface, which can then be corrected. To check for penetration we perform a DistanceHit query using the ColliderDistance utility method.

The ColliderDistance call provides us with the verticalPenetration which is the resulting DistanceHit that has the smallest distance value. A negative distance indicates that we are inside of another surface. It also provides other helpful information such as the normal of the surface which we can use to push ourselves back out.

So we check to ensure that the we have penetrated using the Distance < 0.0f check, and then we adjust our velocity accordingly using the surface normal and distance. This pushes us back out of the surface, but then we have to perform a secondary collider cast as this corrective push could place us into another surface, depending on how complicated the scene geometry is.

If the secondary cast returns a hit, we again adjust the velocity so that the entity is moved only to the point of contact, where the ColliderCastHit.Fraction value is how far along the collider cast the hit occurred.

And now our controller applies gravity to our entities!

If we are on the ground, and the controller is requested to jump, and the we have finished any previous jump, then simply set the jumpVelocity to be a single instaneous “burst” opposite the direction of gravity.

Next, we apply our drag so that the jump velocity is reduced over time to prevent our character from flying off forever. This uses our drag property defined in the controller component.

The current speed of the jump velocity is calculated and if it is not zero then we reduce it by our drag. The reduced speed is then converted back to a velocity vector and assigned to the jumpVelocity.

We also set the value of our CharacterControllerComponent.JumpVelocity as we want the velocity to persist between frames. Remember, that jumping is treated a single instant burst of velocity.

With those two updates we can almost start jumping with our characters. All that remains is the check to see if we are sitting on a surface, which is required to jump off of. This is done in the DetermineIfGrounded which we invoke in the HandleChunk method.

There are several ways that this check could be accomplished, but a simple and fairly reliable way is to perform a series of small raycasts downwards to see if we have a collision.

We perform several casts as a single cast (say from the bottom center) could incorrectly report that we are not grounded when the center passes over a small divot while the rest of the character is on solid ground. Alternatively collider casts can also be unreliable as they often result in reporting that the character is grounded if they are falling down a wall or the top of the character has a hit a surface while jumping. For the first issue, only a single raycast, it can result in not being able to jump when the character should be able to. While the second issue can allow for wall jumping which may not be desireable.

We get the bounds of our collider and use that to find the bottom of the character. Note that we do not just use the position as the origin may be in the model center and not the bottom.

With the bottom center of the character known, we can then determine four more positions to perform casts from which extend out from the center by a fraction of the collider bounds. We do not test the corners as that can also lead to wall jumping.

Our IsGrounded is then set to true if any of the five raycasts, along the gravity vector, comes back as true which indicates that there was a collision.

Our controller is halfway done now that we have full vertical velocity (gravity + jumping) and we can begin work on horizontal movement. This movement is similar to vertical in that we calculate a velocity and perform casts to see if the move is valid. However, with horizontal movement there are two different ways that we approach collisions.

The first is to try to step up onto the colliding surface, which will allow us to climb small ridges and stairs. If we can not step up then we attempt to slide along the surface, for example walking into a wall at an angle.

We will be updating our HandleChunk once more to calculate the initial horizontal velocity and to call the new HandleHorizontalMovement method.

Where the direction and magnitude are set outside of the CharacterControllerSystem by whatever is manipulating the entity movement (such as the PlayerControllerSystem).

The horizontal movement will then be called before the vertical movement:

We exit early if the horizontal velocity is zero in order to prevent an unnecessary casts.

Just like with our vertical movement, we perform an initial cast from our current position to where the velocity would take us. If the cast results in no collisions then we take no further action. However if there are collisions we then have to determine if we can step or slide.

1
2
3
4
5
6
7
8
9

float3 targetPos = currPos + horizontalVelocity;
var horizontalCollisions = PhysicsUtils.ColliderCastAll(collider, currPos, targetPos, ref collisionWorld, entity, Allocator.Temp);
PhysicsUtils.TrimByFilter(ref horizontalCollisions, ColliderData, PhysicsCollisionFilters.DynamicWithPhysical);
if (horizontalCollisions.Count != 0)
{
// ... We either have to step or slide as something is in our way ...

First we check if we can step up onto the surface. To do so we perform a collider cast from above our target position down to our target position. The height at which to being the cast is determined by the MaxStep property of our controller.

1
2
3
4
5
6
7
8
9
10
11

float3 step = new float3(0.0f, controller.MaxStep, 0.0f);
PhysicsUtils.ColliderCast(out ColliderCastHit nearestStepHit, collider, targetPos + step, targetPos, ref collisionWorld, entity, PhysicsCollisionFilters.DynamicWithPhysical, null, ColliderData, Allocator.Temp);
if (!MathUtils.IsZero(nearestStepHit.Fraction))
{
// We can step up.
else
{
// We can not step, so slide.

If the resulting Fraction of the cast is non-zero, that means there is an open space above the target position we can move into. So we simply move our target position up and re-caculate the horizontal velocity so that we are moved to it.

1
2
3
4
5
6

if (!MathUtils.IsZero(nearestStepHit.Fraction))
{
// We can step up.
1.0f - nearestStepHit.Fraction));
horizontalVelocity = targetPos - currPos;
}

Stepping up surfaces which have clearance above them.

If we were unable to perform the step due to the colliding object being too tall (ie a wall), then we will attempt to slide along it to conserve our momentum.

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16

else
{
// We can not step up, so slide.
var horizontalDistances = PhysicsUtils.ColliderDistanceAll(collider, 1.0f, new RigidTransform() { pos = currPos + horizontalVelocity, rot = currRot }, ref collisionWorld, entity, Allocator.Temp);
PhysicsUtils.TrimByFilter(ref horizontalDistances, ColliderData, PhysicsCollisionFilters.DynamicWithPhysical);
foreach (var horizontalDistanceHit in horizontalDistances)
{
if (horizontalDistanceHit.Distance >= 0.0f)
{
continue;
}
horizontalVelocity += (horizontalDistanceHit.SurfaceNormal * -horizontalDistanceHit.Distance);
}
}

For the slide we accumulate a list of all valid objects that our movement causes us to penetrate. We use these lists to then offset our velocity to prevent moving into them, allowing us to slide along the object.

And with that our HandleHorizontalMovement is complete and the player can now move freely.

Sliding along walls as we move into them at an angle.

Player Controller

Well, the player could move freely if we were able to manipulate its CharacterControllerComponent. To enable this we need another component to add to our entity and an accompanying system to translate input into changes in the controller.

Player Controller Component

Defining the PlayerControllerComponent is perhaps the most difficult part of this entire project.

It is now time to create our PlayerControllerSystem which translates player input into movement. For this we will use a standard non-job system which operates on the main thread for simplicity.

For this system we require that any valid entity has the following components:

PlayerControllerComponent

CharacterControllerComponent

CameraFollowComponent

The last component is used by the CameraFollowSystem which we will not go into detail about here, but the source can be viewed here.

We use the camera component as this particular controller will move the player relative to the direction the camera is facing. Pressing the assigned forward/backward keys will move the character along the camera forward axis, while pressing the assigned right/left keys will move the character along it’s right axis.

This movement will be handled in the ProcessMovement method called by our OnUpdate method.

Within ProcessMovement we will simply convert the WASD/arrow key input into a direction vector based on the camera orientation. This will be used as the controller direction, and the magnitude will be assigned a flat value of 1.0 or 1.5 based on whether the shift key is pressed.

Jumping will simply check if the associated jump key is pressed (space) and is independent of the other movement keys.

The input manipulation is fairly standard except for the fact that right and left (as well as forward and backward) are handled separately. Traditionally these are assigned to the same axis with just positive/negative keys assigned.

However, in my experience separating the input mappings results in movement that is more accurate and feels better.

Utilities

The character controller system made use of two different utility classes which are described briefly below.

ColliderDistanceAll: Returns a list of all colliders within the specified distance of the character collider. Also used to see if the character is intersecting (inside) another collider.

ColliderDistance: Similar to ColliderDistanceAll, but returns only the collider with the smallest (potentially negative) distance.

ColliderCastAll: Returns a list of all colliders along a specified path that intersect our character collider.

ColliderCast: Similar to ColliderCastAll, but returns only the first collision.

RaycastAll: Returns a list of all intersections for the provided ray.

Raycast: Similar to RaycastAll, but returns only the first intersection.

TrimByFilter: Used to trim results from the -All methods to only contain results matching the provided collision filter.

Future Improvements

As stated several times, this is a basic controller which meets the minimum requirements to be functional. There are still some known edge cases where it may fail, and some functionality that is missing.

I may address these concerns in the future, but writing the controller and the ramble took a fair bit of time. And frankly the controller meets all of my immediate needs, and so unless my needs change or I find myself with some extra free-time these improvements may be left as an exercise to the reader. Have fun!

General Improvements

Moving platforms most likely do not work, but I haven’t tried them out. Most likely the character will simply fall off.

Restricting movement based on slope in addition to step size.

Affecting other physics objects by applying forces to them on collision.

Edge Cases

This controller performs only a single step and does not integrate. This means high speeds will clip through obstacles as it will completely step past them.

The narrowing hallway, where walls are angled slightly until they intersect. The controller eventually stops, but it is not pretty.

Wait, why didn’t I just use that? Well I did and for unknown reasons it failed in my project. Everything worked great until the character would make contact with the ground. At that point it would just slide endlessly.