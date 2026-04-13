---
title: Introducing Svelto ECS 2.5 - Seba's Lab
url: https://www.sebaslab.com/svelto-ecs-2-5-and-allocation-0-code/
author: Sebastiano Mandalà
published: '2018-05-25'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

**Svelto ECS so far…**

*Svelto.ECS* wasn’t born just from the needs of a large team, but also as result of years of reasoning behind software engineering applied to game development(*). Compared to *Unity.ECS *the main goals and reasons for *Svelto.ECS to exist* are different enough to justify its on going development (plus Svelto is platform agnostic so it has been written with portability in mind). *Svelto.ECS* hasn’t been built just to develop faster code, it has been built to help develop better code. Performance gain is one of the benefits in using *Svelto.ECS,* as ECS in general is a great way to write cache-friendly code, but the main reasons why *Svelto.ECS* has been written orbit around the shifting of paradigm from Object Oriented Programming, the consequent improvement of the code design and maintainability, the approachability by junior programmers that won’t need to worry too much about the architecture and can focus on the solution of the problems thanks to the rigid directions that the framework gives.

I haven’t used Unity ECS so far, although I have seen some examples, so I can’t give much feedback about it at this moment, but what I have learned from Svelto.ECS is how important is to define entities at code level in order to keep coders from abusing the pattern and fall in the trap to write spaghetti code all over again. Let’s be clear, there is a very fine line between writing sensible ECS code and writing plain C code with global accessible data. The anchor that should help the coder to stay on track is to see Systems as a single-responsibility behaviour of a specific set of entities and not as a container of generic logic using global accessible data.

All that said, let’s see what is new in Svelto.ECS 2.5.

**introducing new struct friendly features in Svelto.ECS 2.5**

Until now Svelto.ECS pushed the user to use *objects* over *structs* for normal use when high performance wasn’t required. Svelto.ECS 2.5 inverts this trend, making the use of structs actually the standard and the use of classes the exception. Let’s see how this is achieved:

[As you know](http://www.sebaslab.com/learning-svelto-ecs-by-example-the-unity-survival-example/), an *Entity* is built through an *EntityDescriptor* and an optional set of *Implementors*. An *EntityDescriptor* can generate the so called “*EntityViews*” and “*EntityStructs*“. In my examples I didn’t use many *EntityStructs*, but with the newest version of Svelto I started to rewrite and change a lot of *EntityViews* into *EntityStructs* as you can see in the [new Survival Example Code](https://github.com/sebas77/Svelto.ECS.Examples.Survival).

*Implementor* is a very interesting concept in Svelto.ECS. They are meant to act as a bridge between the underlying platform (like Unity) and the application engines. This is actually how testable engines, that don’t use any dependencies from the underlying platform, can be written with Svelto. However we used to use implementors to define *Entity Components* that were intrinsically independent by the platform too. With Svelto.ECS 2.5 Entity Components should preferably be defined as *EntityStructs* when they don’t need to act as a bridge with the underlying platform. *EntityStructs* are obviously mandatory to write cache-friendly code, but even when this kind of performance gain is not required, *EntityStructs* are still beneficial over *EntityViews* and *Implementors* because they allow to write allocation free code.

A good implementation detail is that the relation between *Entity Components* and *Implementors* is not 1:1. One single implementor object can be used to implement many entity component interfaces. The interface is the abstraction of the underlying platform functionalities that are actually implemented by the implementor. However *EntityViews* are classes and every time an *Entity* is built, a set of objects are allocated on the heap. Therefore, why not declaring *EntityViews* as structs as well? Previously it wasn’t possible because *EntityViews* references were extensively used in *Engines* code, stored inside user data structures. With Svelto.ECS 2.5 the use of custom data structures that hold *EntityViews* references is instead highly discouraged. For this reason, Svelto.ECS 2.5 introduces the new concept of *EntityViewStruct*, which is a mix between the two worlds. When *EntityViewStructs* are used, only the implementors (in Unity mainly as *Monobehaviours*) are allocated on the heap.

Let’s recap everything:

- the use of
*EntityViews*is still supported, but fundamentally obsolete*.* - when
*Implementors*are needed,*EntityViewStructs*should be used instead. *EntitViewStructs*should be used only when engines need to be abstracted from the underlying platform functionalities, although there are other exceptions. The*Engines*shouldn’t need know the implementation details behind the change of entity data (i.e.: the Survival demo code uses this design to wrap the Unity**RigidBody**functionalities, so that the Entity Components can return its parameters without exposing the RigidBody interface).*EntityStructs*should be used for all the other cases. When Monobehaviors don’t need to be used, entity components should always be seen as pure structs. EntityStructs come with the bonus to write way less boilerplate code (neither component interfaces nor implementors are needed).*EntityViewStructs*and*EntityViews*can hold only component interfaces.- Component interfaces must declare only setter and getters of primitive or value types. The only exceptions are made by
**DispatchOnSet<T>**and**DispatchOnChange<T>** *EntityStructs*can hold only primitives and value types (no collections allowed either).- Custom data structures defined in engines with the purpose to hold
*EntityView*references should never be used unless strictly necessary.

The main problem about using *EntityStructs *is that they don’t allow the same fine abstraction that *EntityViewStructs *do. This is because *EntityViewStructs, *being defined by the *Engines*, allow to re-interpret the same component data under different engines point of view, promoting abstraction and encapsulation. *EntityStructs* instead are defined by the Entity and the Engine can only use them without semantic reinterpretation. That’s why *EntityStructs* should be as modular as possible, although the definition of an *EntityStruct* could have more practical repercussions depending if a SoA or AoS implementation is preferred. Being able to give to the same data different meaning is the only reason why EntityViewStructs could be still preferred to EntityStructs when implementors are not used to abstract the underling platform. For example, an engine can have a read-only access to the same data that another engine can write into. EntityStructs instead are always mutable as making them immutable would defeat the purpose of improving performance.

Extending the Svelto graph, the *EntityStructs* are placed on the left side:

If there wasn’t any dependency with the underlying platform, it would be possible to write a game with *EntityStructs* only, however I am still not sure how this would impact the overall design.

Currently this is my thinking:

If there is no dependency to the underlying platform (i.e.: callbacks from *Monobehaviours* or some Unity related stuff), use *EntityStructs* as long as they are very modular (**HealthEntityStruct** is a good example). I don’t think there would be much space for very specialized *EntityStructs*. *EntityViewStructs *and *Implementors* could make sense only as *Monobehaviours* and would store the essential features needed from the platform. The main question that I have still to answer is: would the absolute use of *EntityStructs* over *EntityViewStructs* make the design worse? This is something I will analyse in future with our projects. Currently the nice thing about the EntityViewStructs is that they describe Entities specialization in terms of behaviours applied to the entity more than data. Normally, using ECS design, entities are specialized adding more data, however through the Svelto *EntityDescriptor* and *EntityViewStructs* is possible to read what behaviours will be applied to the Entity, example:

namespace Simulation.Hardware.Weapons.Plasma { class PlasmaWeaponEntityDescriptor : EntityDescriptor { static readonly IEntityViewBuilder[] _EntityViewsToBuild; static PlasmaWeaponEntityDescriptor() { _EntityViewsToBuild = new IEntityViewBuilder[] { new EntityViewBuilder<PlasmaWeaponShootingEntityView>(), new EntityViewBuilder<NextWeaponToFireEntityView>(), new EntityViewBuilder<WeaponAimEntityView>(), new EntityViewBuilder<WeaponDamageBuffEntityView>(), new EntityViewBuilder<DamageMultiplierEntityView>(), new EntityViewBuilder<WeaponFireTimingEntityView>(), new EntityViewBuilder<WeaponSwitchEntityView>(), new EntityViewBuilder<ZoomEntityView>(), new EntityViewBuilder<PlasmaWeaponEffectsEntityView>(), new EntityViewBuilder<WeaponWithoutLaserPointerEntityView>(), new EntityViewBuilder<ShootingAfterEffectsEntityView>(), new EntityViewBuilder<WeaponAccuracyEntityView>(), new EntityViewBuilder<CrosshairWeaponTrackerEntityView>(), new EntityViewBuilder<HardwareHealthStatusEntityView>(), new EntityViewBuilder<CrosshairWeaponNoFireStateTrackerEntityView>(), new EntityViewBuilder<SmartWeaponFireEntityView>(), new EntityViewBuilder<BlockWeaponFireEntityView>(), new EntityViewBuilder<AchievementWeaponEntityView>() }; } public PlasmaWeaponEntityDescriptor() : base(_EntityViewsToBuild) { } } }

Since entity views come with their relative Engines, an entity descriptor shows what behaviors (engines) will run on the entity (ie.:*ZoomEntityView* is used in the *ZoomableEntitiesEngine*). Using only EntityStructs I would loose this semantic, moving back to see Entities as a set of data only (without knowing where this data will be used).

**In-depth view of the new functionalities**

I understand this is a lot to take in. It shouldn’t be if you know how to use Svelto already, although you will need to change your current way to use it. If you are new to it, the best thing is to follow the survival example, as the code is simpler than the theory. Let’s start from our MainContext.

**-EntityStructs-**

Beside cleaning up some code, the most important difference is how I create the Player Entity. The Player Entity now has only *EntityViewStructs* defined with *Implementors* as *Monobehaviors* and *EntityStructs* for everything that don’t need to act as a bridge (precisely: **HealthEntityStruct** and **PlayerInputDataStruct**).

//The Player Entity is made of EntityViewStruct+Implementors as monobehaviours and //EntityStructs. The PlayerInputDataStruct doesn't need to be initialized (yay!!) //but the HealthEntityStruct does. Here I show the official method to do it HealthEntityStruct healthEntityStruct = new HealthEntityStruct {currentHealth = 100}; var initializer = _entityFactory.BuildEntity<PlayerEntityDescriptor>(player.GetInstanceID(), player.GetComponents<IImplementor>()); initializer.Init(ref healthEntityStruct);

with:

//defines the EntityViewStructs and EntityStructs generated by the creation //of the Player Entity public class PlayerEntityDescriptor : GenericEntityDescriptor<PlayerEntityView, EnemyTargetEntityView, DamageSoundEntityView, CameraTargetEntityView, HealthEntityStruct, PlayerInputDataStruct> {}

and as example of EntityStructs:

public struct HealthEntityStruct : IEntityStruct { public int currentHealth; public EGID ID { get; set; } }

public struct PlayerInputDataStruct : IEntityStruct { public Vector3 input; public Ray camRay; public bool fire; public EGID ID { get; set; } }

you may notice how creating an Entity still looks quite readable! Especially if you don’t like the Svelto.ECS (minimal, I have to say), boilerplate, you are going to love the EntityStruct, as they are compact and they don’t need to define interfaces or implementors that must come with them.

I put a lot of effort to make structs user friendly in Svelto.ECS 2.5. Unluckily I couldn’t achieve my final goals, as the interfaces I had in mind need the new c# 7.0 by ref features, so at the moment some functionalities around the EntityStructs are not final, but still OK (or at least the best the can be at the moment I guess).

Let’s start from the initialization of the structs. This interface won’t actually change as I am actually happy with it. More often than not, you will want to initialize the value of your structs with initial values. This was quite badly managed by Svelto 2.0, as I want an allocation free and easy to understand solution.

I found it with the **EntityStructInitializer **struct returned by any **IEntityFactory** **BuildEntity** method. After you call **BuildEntity**, you will use it like this:

HealthEntityStruct healthEntityStruct = new HealthEntityStruct {currentHealth = 100}; initializer.Init(ref healthEntityStruct);

in this way the Player Entity will generate a **HealthEntityStruct** with the starting values you desire.

Alternatively you may create an Engine that inherits from **SingleEntityEngine<>** or **MultiEntitiesEngine<,>**. They both implement the Add/Remove methods with a parameter passed by reference. It supports *EntityStructs *and the modifications made to it will be saved directly in the database.

To summarize:

*EntityViewStructs*are like the good ol’*EntityViews*. They hold Component interfaces which must still be filled with reflection (albeit cached and fast). They must implement the*IEntityViewStruct*interface. However they don’t allocate any object on the heap when created, differently than what*EntityViews*do*EntityStructs*, which were already present in Svelto, must implement the*IEntityStruct*interface. They don’t allocate, they are cache friendly and they don’t use reflection. They are the top for performance. Thanks to the new Svelto ECS features, I would cautiously suggest to use them whenever you can. However keep in mind that they could make your code design worse and this is something I want to test in future on large projects.

**-Allocation 0 code-**

Now that you can use *EntityStructs* and *EntityViewStructs*, you are able to achieve zero allocation code while building entities. This would make Entity Pooling unnecessary.

**-Handling Entity Structs and EntityViewStructs inside engines-**

This is the part that is still a bit awkward due to the lack of the new c# 7.0 features. Essentially *EntityStructs* should always be managed inside an engine through an array of data. This is the way to be able to write cache friendly code. To be honest, having an array of structs is not enough,[ the cache performance can be easily broken if you don’t know how much memory can fit in the L1 cache and how much memory can be read in a cycle](http://www.sebaslab.com/svelto-ecs-svelto-tasks-to-write-data-oriented-cache-friendly-multi-threaded-code-in-unity/). One can say that this feature is still for advanced users, who know what they are doing. In more practical terms, *EntityStructs* can be used where entity cache is not strictly necessary. For this reason, I wanted to support the querying of *EntityStructs* by entity id too. The only problem is that without the c# 7 by ref return the only way I had to solve the problem was to use something like:

entityViewsDB.ExecuteOnEntity(targetID, (ref EnemyEntityView entityView) => { entityView.movementComponent.navMeshEnabled = false; entityView.movementComponent.setCapsuleAsTrigger = true; });

it’s much less nicer than using the byref return, but still reasonable. *This is error prone for junior coders though, as by mistake the lambda could capture external variables, resulting in allocation*.

Alternatively the array of entity structs can be used directly, but even in this case, The Junior Coders must know what they are doing:

var enemies = entityViewsDB.QueryEntities<EnemyEntityViewStruct>(out count); enemies[i].movementComponent.navMeshDestination = targetEntityView.targetPositionComponent.position;

In both cases the goal is to be able to modify the value back inside the centralized database of Entities. For example, in the second case, if instead of using enemies[i] I would have stored it into a local variable, the enemies[i] value inside the database wouldn’t change, as I would work on a copy of it. The* c# 7 return by ref* would let me do something like:

ref EnemyEntityViewStruct enemy = ref entityViewsDB.QueryEntity<EnemyEntityViewStruct>(index);

and let me using enemy directly not as a copy of the structure, but as a pointer to it.

**-the EGID and Entity Groups-**

Svelto.ECS 2.5 boasts a new optimized centralized data structure to hold the data of all the entities. With one data structure only it’s able to hold *EntityViews*, *EntityViewStructs* and *EntityStructs* **without causing any boxing allocation**. The same data structure is able to query a set of entity data of a given type as an array or return a single one indexed by EGID.

EGID stands for EntityGlobalID (or something like that, I don’t even remember how I came up with it) and it’s a combination of the EntityID and the GroupID where the entity is defined.

in Svelto 2.5, entities are ALWAYS built inside a group. If the group is not defined, a standard exclusive group will be used *(note: this is deprecated with svelto 2.7)*. Groups help the database query system to be more flexible. It’s possible to give to a group any meaning, for example a groups could be used to create an entity pooling system when a group is used for the “disabled” entities. Another example is to define a group as “all the entities carried by another entity in game”. There are no limitations except:

- EntityID must be unique inside a group. The same entity ID can be used across several groups.
- An entity can be present inside one group at time, HOWEVER nothing keeps you from creating two different entities, with the same ID, in two different groups to be shared separately. This is actually an example where the use of implementors “could” be smart. While I said that implementors should always be used as bridge between the platform and the engines, another possible use of implementors is to share the same data between different entities. In fact, several entities could be created using the same implementors. Without this trick, it would be hard to manage the same entity data in two different groups. It’s also possible to swap a specific entity between groups.

At last, it’s important to remember that the EGID of an entity is not always the same over the time. Changing the group would in fact change the value of the EGID.

**-Use Entity Groups for pooling-**

In the new survival code, I implemented an Entity Pooling system for the enemy spawning, let’s have a look:

void ReuseEnemy(int fromGroupId, ref JSonEnemySpawnData spawnData) { //take an entity (with all its entity views and implementors) from the group var egid = _entityFunctions.SwapFirstEntityGroup(fromGroupId); //reset some components entityViewsDB.ExecuteOnEntity(egid, (ref HealthEntityStruct healthStruct) => { healthStruct.currentHealth = 100; }); entityViewsDB.ExecuteOnEntity(egid, ref spawnData, (ref EnemyEntityViewStruct entityView, ref JSonEnemySpawnData spawnDataInfo) => { //reset all the data of the reused components }); }

When an enemy dies, I don’t destroy the **GameObject** and remove the entity from the database anymore. Instead I swap its group on death using the method:

_entityFunctions.SwapEntityGroup(token.entityDamagedID.entityID, ECSGroups.EnemyGroup[playerTargetTypeEntityStructs[index].targetType]);

I take the dead enemy ID and use the *SwapEntityGroup* to move it from the Standard Group to a special group ID I use to keep track of the disabled enemies per enemy type.

Then when I have to reuse the Entity I will take its EntityViewStructs from the disabled pool. The EntityStructs must be reset as well and that’s what I do inside the ExecuteOnEntity methods. Note that all the implementors now are only Monobehaviours and they are not garbage collected, so that fetched EntityViewStructs will still point to the implementors of the GameObject linked to the Entity.

**-Other important differences-**

- Previously it was possible to retrieve the complete list of EntityViews regardless the group they were belonging to, this is not possible now
- Previously the RemoveEntity function didn’t need to specify the group where the Entity laid, it’s now needed.

## A review of the communication functionalities in Svelto.ECS

Svelto main communication forms are confirmed to be the *Sequencer* and the *DispatchOnSet* and *DispatchOnChange* methods. Currently *DispatchOnSet* and *DispatchOnChange* can only be used through component interfaces, but once c# 7 will be available in unity, maybe I will convert them in structs and let them be usable inside EntityStructs as well. DispatchOnSet and DispatchOnChange must be still seen as Data Binding systems and not as Events.

I also improved a bit the Sequencer code, so that a declaration would be even more explanatory now. Remember that the main benefit of the Sequencer is to give to the user the possibility to understand the flow of communication from its declaration without being forced to check the code and reconstruct the communication flow from it.

It would be awesome if someone would be so cool to write an Unity Editor Tool to fetch all the defined Sequencers in the Game assembly and visualize it with a node graph system. I would never have the time neither the interest to do it, but that’s why Svelto is open source, so that other people can help if they wish 😉

**Note: Svelto.ECS (together with the companion **


[Svelto.Tasks](https://github.com/sebas77/Svelto.Tasks)**) is currently compatible with .NetStandard 2.0, Net 3.5, Net 4.5, unity IL2CPP/UWP.**

**(*) The evolution of my reasoning can be found in these articles that I strongly suggest to read:**

-
-
[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/)[http://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/](http://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/)[http://www.sebaslab.com/svelto-2-7-whats-new-and-best-practices/](http://www.sebaslab.com/svelto-2-7-whats-new-and-best-practices/)(shows what’s changed since 2.5)[http://www.sebaslab.com/svelto-ecs-2-5-and-allocation-0-code/](http://www.sebaslab.com/svelto-ecs-2-5-and-allocation-0-code/)(shows what’s changed since 2.0)[http://www.sebaslab.com/svelto-ecs-2-0-almost-production-ready/](http://www.sebaslab.com/svelto-ecs-2-0-almost-production-ready/)(shows what’s changed since 1.0)[http://www.sebaslab.com/ecs-1-0/](http://www.sebaslab.com/ecs-1-0/)[http://www.sebaslab.com/learning-svelto-ecs-by-example-the-unity-survival-example/](http://www.sebaslab.com/learning-svelto-ecs-by-example-the-unity-survival-example/)[http://www.sebaslab.com/learning-svelto-ecs-by-example-the-vanilla-example/](http://www.sebaslab.com/learning-svelto-ecs-by-example-the-vanilla-example/)[http://www.sebaslab.com/svelto-ecs-svelto-tasks-to-write-data-oriented-cache-friendly-multi-threaded-code-in-unity/](http://www.sebaslab.com/svelto-ecs-svelto-tasks-to-write-data-oriented-cache-friendly-multi-threaded-code-in-unity/)


-

Thank you

I was wondering what plugin you use for the beautiful vertical alignment. Thank you for this great project!

Thank you a lot ! It seems to be a great way to make cleaner code ! Nice piece of work !