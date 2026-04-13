---
title: What's new in Svelto.ECS 3.0 - Seba's Lab
url: https://www.sebaslab.com/whats-new-in-svelto-ecs-3-0/
author: Sebastiano Mandalà
published: '2020-12-19'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

Hello everyone, I am back again and so is (finally!) a new official Svelto.ECS update! It sounds almost incredible, but the release 3.0 of [Svelto.ECS](https://github.com/sebas77/Svelto.ECS) is the result of exactly one year of work! I can’t believe it. Initially, I planned to take at most three months to release the features I had in mind, but then I decided to make Svelto *Unity Jobs* and *Burst *compatible and there it went most of the unplanned time.

Svelto.ECS 3.x has been the Entity Component System framework used for several years on Freejam’s products **Gamecraft**, **Techblox **and now **Robocraft 2**. They are all titles full of technical challenges, including the necessity to physic simulate thousands of entities. Gamecraft was also the first product I designed to be 100% ECS (wrapping OOP code where necessary).

![MAJOR UPDATE: Destruction, Quantum Rifle More - NOW LIVE · Gamecraft update for 21 August 2020 · SteamDB](../../assets/fa9c5e27af00a839.gif)

This article is going just to be a brief Svelto.ECS 3.0 introduction as the jump from Svelto.ECS 2.9 is quite big and there is a LOT to talk about. As you can imagine old code would need some rethinking to work with the new patterns/features. For this reason, is probably better for me to start from scratch so that we can refresh some terminology and ideas.

Before continuing, remember that anyone can contact me and other Svelto users by joining the official discord channel which is the best way to get help. The Svelto.Miniexamples and Svelto.ECS.Tests repositories are the best places where to find ready-to-study and up-to-date examples.

*This article is not an introduction to ECS nor is intended to explain how to use Svelto.ECS as some concepts are too advanced to be crammed in one article only.***MiniExamples**and**Svelto Discord****server**are actually the best places where to start.

### Svelto.ECS at glance

/// <summary> /// This is the common pattern to declare Svelto Exclusive Groups (usually split by composition root) /// </summary> public static class ExclusiveGroups { public static ExclusiveGroup group0 = new ExclusiveGroup(); public static ExclusiveGroup group1 = new ExclusiveGroup(); } /// <summary> /// The Context is the framework starting point. /// As Composition root, it gives to the coder the responsibility to create, initialize and inject dependencies. /// Every application can have more than one context and every context can have one /// or more composition roots (a facade, but even a factory, can be a composition root) /// </summary> public class SimpleContext { readonly EnginesRoot _enginesRoot; public SimpleContext() { //An EnginesRoot holds all the engines created. it needs a EntitySubmissionScheduler to know when to //add the Entity creates inside the EntityDB. var simpleSubmissionEntityScheduler = new SimpleEntitiesSubmissionScheduler(); _enginesRoot = new EnginesRoot(simpleSubmissionEntityScheduler); //an EnginesRoot must never be injected inside other classes only IEntityFactory and IEntityFunctions //implementation can var entityFactory = _enginesRoot.GenerateEntityFactory(); var entityFunctions = _enginesRoot.GenerateEntityFunctions(); //Add the Engine to manage the SimpleEntities var behaviourForEntityClassEngine = new BehaviourForEntityClassEngine(entityFunctions); _enginesRoot.AddEngine(behaviourForEntityClassEngine); //build Entity with ID 1 in group 0 entityFactory.BuildEntity<SimpleEntityDescriptor>(new EGID(0, ExclusiveGroups.group0)); //as we are using a basic scheduler, we need to schedule the entity submission ourselves simpleSubmissionEntityScheduler.SubmitEntities(); //as we don't have any ticking system for this basic example, we tick explicitly behaviourForEntityClassEngine.Update(); } } //An EntityComponent must always implement the IEntityComponent interface //don't worry, boxing/unboxing will never happen. public struct EntityComponent : IEntityComponent { public int counter; } /// <summary> /// The EntityDescriptor identifies your Entity. It's essential to identify /// your entities with a name that comes from the Game Design domain. /// </summary> class SimpleEntityDescriptor : GenericEntityDescriptor<EntityComponent> {} namespace SimpleEntityEngine { public class BehaviourForEntityClassEngine : //this interface makes the engine reactive, it's absolutely optional, you need to read my articles //and wiki about it. IReactOnAddAndRemove<EntityComponent>, IReactOnSwap<EntityComponent>, //while this interface is optional too, it's almost always used as it gives access to the entitiesDB IQueryingEntitiesEngine { //extra entity functions readonly IEntityFunctions _entityFunctions; public BehaviourForEntityClassEngine(IEntityFunctions entityFunctions) { _entityFunctions = entityFunctions; } public EntitiesDB entitiesDB { get; set; } public void Ready() { } public void Add(ref EntityComponent entity, EGID egid) { _entityFunctions.SwapEntityGroup<SimpleEntityDescriptor>(egid, ExclusiveGroups.group1); } public void Remove(ref EntityComponent entity, EGID egid) { } public void MovedTo(ref EntityComponent entityComponent, ExclusiveGroupStruct previousGroup, EGID egid) { Console.Log("Swap happened"); } public void Update() { var (entity, count) = entitiesDB.QueryEntities<EntityComponent>(ExclusiveGroups.group1); for (var i = 0; i < count; i++) entity[i].counter++; Console.Log("Entity Struct engine executed"); } } }

### The Basics: EnginesRoot and CompositionRoot

The most important class remains the **EnginesRoot**. This is the class that holds all the data and systems to run your logic. You will find it in all the *MiniExamples examples*. If you know **Unity ECS**, it’s equivalent to the **World **concept. Similarly to it, you can have multiple** EnginesRoots **to encapsulate even further data and logic.

Contrary to UECS, Svelto tends to not hide complexity and be as simple as possible. Svelto does not create default EnginesRoots or systems automatically, so everything must be instantiated and injected explicitly through a** Composition Root**. Refer to my previous articles to know what a Composition Root is if necessary, but essentially it’s the bootstrap code where the *Enginesroot*, the *Scheduler *and the *Engines *are created. Remember that in Svelto.ECS I still refer to the ECS *systems *as **engines** (even because I am not 100% sure that System is the correct word to use, but this is another story).

A composition root can take many forms as it’s not how it’s designed that it matters, but what it does. An example can be:

var entityFactory = _enginesRoot.GenerateEntityFactory(); var entityFunctions = _enginesRoot.GenerateEntityFunctions(); var placeFoodOnClickEngine = new PlaceFoodOnClickEngine(redFoodPrefab, blueFootPrefab, entityFactory); _enginesRoot.AddEngine(placeFoodOnClickEngine); var spawningDoofusEngine = new SpawningDoofusEngine(redDoofusPrefab, blueDoofusPrefab, entityFactory); _enginesRoot.AddEngine(spawningDoofusEngine); var consumingFoodEngine = new ConsumingFoodEngine(entityFunctions); _enginesRoot.AddEngine(consumingFoodEngine); var lookingForFoodDoofusesEngine = new LookingForFoodDoofusesEngine(entityFunctions); _enginesRoot.AddEngine(lookingForFoodDoofusesEngine); var velocityToPositionDoofusesEngine = new VelocityToPositionDoofusesEngine(); _enginesRoot.AddEngine(velocityToPositionDoofusesEngine);

Note that there are no rules on what you can inject in an engine, so the Composition Root is also where all the dependencies are resolved.

### The Basics: Entity Descriptors and Entity Components

Svelto.ECS entities are described by **EntityDescriptors**. The concept may remind the *Archetype *in UECS. Entity descriptors define the list of **Entity Components** that each entity generates. However, Entity descriptors are more important than that. They were initially designed to never let the user forget what an entity is. Using Svelto, the user will not fall into the trap to reason only in terms of components. Having always in mind what an entity is is fundamental as engines should be designed around entities and not decontextualised components. One rule I always push for, is to name the engines after the Behaviour to apply plus the name of the entity the engine operates on so that these concepts are visualised in code.

Entity Components in Svelto 3.x are always structs and must always hold value types only. The simplest way to declare an entity descriptor looks like this:

public class RigidBodyDescriptor : GenericEntityDescriptor<TransformEntityComponent, RigidbodyEntityComponent, CollisionManifoldEntityComponent, EGIDComponent> { }

it’s important to note that SECS has been designed to push the user mentality away from the classic definition of an entity being just an ID. SECS instead promotes the conceptual aspect of an entity. Personally, I like to have the rule that an entity must reflect a design entity that the user can experience. In doing so, the name of the entity usually comes from the Game Design Document. This also promotes *ubiquitous language* between designers and coders.

### The Basics: The EntitySubmissionScheduler

Since the first time Svelto has been used in production, created entities have been submitted at once during the *Submission *time. One fundamental feature of Svelto is that *it doesn’t provide any engine ticking solution*. The user has the responsibility to decide when to run engines and when entities are submitted. Two predefined **EntitySubmissionScheduler **are provided:

**UnityEntitiesSubmissionScheduler**, as seen in **MiniExample 2: Survival**. It’s a Unity dedicated submission scheduler that submits new entities every unity update. This is used for simple demos and probably would never be used in anything more complicated than that.

**SimpleEntitiesSubmissionScheduler**, as seen in **MiniExample 4: SDL**. *It’s the suggested way to submit entities*. The user has full control over when the entities should be submitted.

During the submission time, all the **Add**, **Remove **and **MoveTo **engine callbacks (implemented through the interfaces **IReactOnAdd**, **IReactOnRemove **and **IReactOnSwap**) are executed, reacting on entities added, removed or swapped (swap is a concept linked to groups, as you will see in a bit). I refer to these operations as *structural changes*.

### The Basics: EntityViewComponents, Implementors and Hybrid ECS

Although Svelto is designed to allow *100% ECS-centric applications*, not all the platforms/libraries are written with ECS code. Hence it’s still necessary to work side by side with OOP entities. Mixing ECS code with OOP is and always be awkward, consequentially there are multiple ways to approach this problem. Svelto provides one officially, others are patterns that will be explained in future articles. The official way is the use of **EntityViewComponents**, which are entity components that can hold interfaces that are implemented with objects. These objects are called *implementors *in Svelto. While the object is a standard c# object, the interface has limited flexibility, for example, it can expose only properties that work on value types. With EntityViewComponents performance is reduced, as the memory layout won’t be cache-friendly anymore. They are called this because EntityViewComponents were initially designed to wrap the objects that should act as views. I like to draw a parallel with the MVP pattern. The presenter is the engine, the model is the data that can be found in the entity component, and the view is the implementor that acts on data change. While the MVP pattern works vertically (a triad for each element), in ECS this works horizontally (the engine operates on all the views at the same time).* *

**Note that using EntityViewComponents and Implementors is NOT the recommended way to handle OOP objects in ECS. The recommended way is using ResourceManagers and OOP abstraction layers as explained in the articles: **

### The Basics: ExclusiveGroups

Every ECS framework implementation has its own strategy to store entities most efficiently. With SECS, I designed a novel solution that is based on the use of *Groups*. I see the groups as a way to *decouple the state of the entity from its values*. In general, the user would find it safe to create a group for each entity descriptor. This would act similarly to how Archetypes work in UECS (except for the further split into different chunks). An entity belongs to one group at a time (hence the name ExclusiveGroup) and the user can freely swap entities between groups when necessary. *When entities are built, removed, swapped between groups and iterated, the user must declare which group the operation must act on*. Groups are used in all the **MiniExamples **and while they are initially not intuitive, the user usually gets them quickly. In any case, **ExclusiveGroups **should never be created at runtime (this still needs to be enforced by the framework) and are always declared as static variables.

Groups can be seen as the way to organise the entity queries. The user queries entities according to the group from which they must be taken. In this way is possible, for example, to iterate entities in relation to their states or meaning. SECS allows queries from *single groups or an array of groups*. Arrays of groups are usually associated with abstract engines or engines that iterate entities sharing common states. For example, in **MiniExample 2: Survival**:

public static readonly ExclusiveGroup PlayersGroup = new ExclusiveGroup();

public static readonly ExclusiveGroup EnemiesGroup = new ExclusiveGroup();

//it's also possible to regroup groups. It's quite a flexible system

public static readonly ExclusiveGroupStruct[] DamageableEntitiesGroups = {EnemiesGroup, PlayersGroup};

the **DeathEngine **engine shows:

```
foreach (var ((buffer, count), _) in entitiesDB.QueryEntities<HealthComponent>(ECSGroups.DamageableEntitiesGroups))
{
for (int i = 0; i < count; ++i)
if (buffer[i].currentHealth <= 0)
entitiesDB.PublishEntityChange<DeathComponent>(buffer[i].ID);
}
```


The **DeathEngine*** *is more abstract than *Player *or *Enemies *entities related engines because it iterates both entity types assuming that **HealthComponent **and **DeathComponent** will be present in the respective descriptors.

Rearranging the meaning of the entities through the use of Groups opens the door to interesting strategies, however handling **ExclusiveGroups **explicitly can get awkward fast, that’s why **GroupCompounds **have been introduced with Svelto.ECS 3.0.

ExclusiveGroups aren’t completely replaced by the newly introduced GroupCompounds because of possible advanced scenarios. One feature that is still related only to ExclusiveGroups is the option to *reserve a range of groups for procedural queries*. ExclusiveGroup declaration can look like this:

//standard declaration, usually one group for each entity descriptor (entity type) public static readonly ExclusiveGroupStruct PopupGroup = new ExclusiveGroup(); //reserve group ranges. public static readonly ExclusiveGroup PopupInputItemsGroup = new ExclusiveGroup(100); public static readonly ExclusiveGroup PopupOutputItemsGroup = new ExclusiveGroup(100); //group can be searched by name, this feature has been designed for GUI code public static readonly ExclusiveGroup PreviewWiresGroup = new ExclusiveGroup("PreviewWiresGroup");

Reserved ExclusiveGroups can then be used with the name of the group + index. In this case, for example, it can be used as **PopupInputItemsGroup + N** where N is between 1 and 99. Being an advanced scenario, don’t worry if you don’t understand why to use reserved groups while reading this article, but know that **MiniExamples 2: Survival** uses them.

Another example is the following, where entities may swap between being monsters and being soldiers and players can take over AI entities and vice-versa:

public static class CharactersExclusiveGroups { public static ExclusiveGroup AISoldierGroup = new ExclusiveGroup(); public static ExclusiveGroup AIMonsterGroup = new ExclusiveGroup(); public static ExclusiveGroup PlayerSoldierGroup = new ExclusiveGroup(); public static ExclusiveGroup PlayerMonsterGroup = new ExclusiveGroup(); public static readonly ExclusiveGroup[] Soldiers = { PlayerSoldierGroup, AISoldierGroup}; public static readonly ExclusiveGroup[] Monsters = { PlayerMonsterGroup, AIMonsterGroup}; public static readonly ExclusiveGroup[] AI = { AISoldierGroup, AIMonsterGroup}; public static readonly ExclusiveGroup[] Players = { PlayerSoldierGroup, PlayerMonsterGroup}; }

this example is a bit advanced already as it shows how it is possible to use ExclusiveGroups to manage entities states too. For example is possible to switch entities between these “leaves” groups (AISoldierGroup, AIMonsterGroup, PlayerSoldierGroup, PlayerMonsterGroup) to change their behaviour at run time using the **SwapEntityGroup** method. Group aggregation is useful to apply shared behaviours between entities (which usually are linked to more abstracted engines)

It’s possible to push the concept of groups as states up to the point to use them as FSM states. Using the Add and Remove callbacks would be possible to decide what behaviours to trigger when an entity is added to a specific group and when an entity is removed from a specific group.

### New Feature: GroupCompounds

**GroupCompound ***should be the default way to declare groups in Svelto and the new user should start to use them in place of the conventional ExclusiveGroups*. GroupCompounds are designed to statically manage groups based on *tags*, making the use of groups simpler, more intuitive and more powerful. Following the soldier/monster example above, the group compound equivalent would be:

```
public static class CharactersExclusiveGroups
{
public class AI: GroupTag<AI> { }
public class Player: GroupTag<Player> { }
public class Soldier: GroupTag<Soldier> { }
public class Monster: GroupTag<Monster> { }
public class AISoldier: GroupCompound<AI, Soldier> { }
public class AIMonster: GroupCompound<AI, Monster> { }
public class PlayerSoldier: GroupCompound<Player, Soldier> { }
public class PlayerMonster: GroupCompound<Player, Monster> { }
}
```


In code, I am able to query every permutation of tags I want, if an entity is built or currently found in that permutation of tags, the query will return it. I can query entities through the following arrays of **ExclusiveGroups**:

```
all the AI Entities = GroupTag<AI>.Groups;
all the Player Entities = GroupTag<Player>.Groups;
all the Soldier Entities (regardless if AI or Player) = GroupTag<Soldier>.Groups;
all the Monster Entities (regardless if AI or Player)= GroupTag<Monster>.Groups;
all the AI Soldiers = GroupCompound<AI, Soldier>.Groups;
all the AI Monsters = GroupCompound<AI, Monster>.Groups;
all the Player Soldiers = GroupCompound<Player, Soldier>.Groups;
all the Player Monsters = GroupCompound<Player, Monster>.Groups;
all the entities that are AI and Player at the same time (none will be found in this example, but still valid query) = GroupCompound<AI, Player>.Groups;
```


This is another example of the use of group compounds:

```
public static class GameGroups
{
public class RigidBodies : GroupTag<RigidBodies> { }
public class Kinematic : GroupTag<Kinematic> { }
public class Dynamic : GroupTag<Dynamic> { }
public class WithBoxCollider : GroupTag<WithBoxCollider> { }
public class WithCircleCollider : GroupTag<WithCircleCollider> { }
public class DynamicRigidBodies : GroupCompound<RigidBodies, Dynamic> { }
public class DynamicRigidBodyWithBoxColliders : GroupCompound<RigidBodies, WithBoxCollider, Dynamic> { }
public class DynamicRigidBodyWithCircleColliders : GroupCompound<RigidBodies, WithCircleCollider, Dynamic> { }
public class KinematicRigidBodyWithBoxColliders : GroupCompound<RigidBodies, WithBoxCollider, Kinematic> { }
public class KinematicRigidBodyWithCircleColliders : GroupCompound<RigidBodies, WithCircleCollider, Kinematic> { }
}
```


The code above is a SECS group declaration pattern and although classes are used, they will never be instantiated and can in fact be declared as abstract for further peace of mind.

*One unique feature of Svelto.ECS is to prohibit adding or removing entity components at execution time (avoiding the so-called component tagging practice)*. Once an entity descriptor (and therefore the entity) is defined, it’s immutable. This feature has several performance benefits, but it is mainly designed to prevent distorting the definition of an entity. If an entity can become anything at any time, the distinctive entity declaration would become meaningless (and the user would revert to thinking in terms of decontextualised components instead of entities).

GroupCompounds is one of the two new features that come into play to fill the lack of dynamic component tagging which was limiting the development of complex features with Svelto.ECS 2.x. When looking at groups as “compounds” of tags, is possible to switch states or adjectives just by swapping an entity from a compound to another compound.

An entity that is found in the group *DynamicRigidBodyWithBoxColliders *could move to the group *KinematicRigidBodyWithBoxColliders *allowing different engines to run on the entity just swapped. This, together with the use of the **MovedTo **callback, could enable the development of simple state machines.

*GroupCompounds are usually designed with the first tag being the entity type and the successive tags being states or adjectives of the entity instance.*

GroupCompounds are used in the examples **MiniExamples 1: Doofuses** and **MiniExamples 4: SDL**.

### Pattern: how to build entities with group compounds

Putting all together, the syntax to build an entity looks like this:

```
EntityInitializer initializer = entityFactory.BuildEntity<RigidBodyWithCircleColliderDescriptor>(
egid, GameGroups.KinematicRigidBodyWithCircleColliders.BuildGroup);
```


An entity is built using its descriptor. Then, and this is a unique Svelto feature, the user needs to associate an ID to the entity and at last, the user needs also to choose in which group the entity must be put. The combination of Entity ID and Group ID in Svelto is called **EGID**. *Because the entity group can change after a swap, an EGID value is not constant*. In the next versions of Svelto.ECS, I will introduce the already planned **EntityReference **feature, which will abstract the EGID and will enable simpler ways to link entities to other entities.

the EGID can be successively used to query specific entities. Linking a user-defined ID to entities enables more patterns compared to other ECS framework implementations. The returned initializer is a transient container that allows initialising the components created if needed.

*Remember that once an entity is built it’s not immediately available. It will be available only after the next submission of entities.*

### Pattern: how to iterate entities with group compounds

There are several ways to iterate entities, but with the use of group compounds the user will end up resorting to similar patterns, looking like:

```
foreach (var ((rigidbodies, transforms, count), group) in entitiesDB
.QueryEntities<RigidbodyEntityComponent, TransformEntityComponent>(GameGroups.DynamicRigidBodies.Groups))
for (var i = 0; i < count; i++)
{
ref var rigidbody = ref rigidbodies[i];
ref var transform = ref transforms[i];
//do stuff on entities
}
```


*The use of deconstructing patterns is elegant but weird at first*. The user will get used to it soon and I suggest using your IDE ability to work out the deconstruction automatically at first.

![](../../assets/8cfa494b8d2207de.png)

![](../../assets/50ed6d05b943b49a.png)

![](../../assets/d574367c09beae5c.png)

Multiple components can be queried and used at once inside the iteration (using the same index). This is really as fast as an iteration can be and highly suitable for vectorisation.

In the following example:

```
foreach (var ((rigidbodies, transforms, count), group) in entitiesDB
.QueryEntities<RigidbodyEntityComponent, TransformEntityComponent>(GameGroups.DynamicRigidBodies.Groups))
```


the user is asking to get the **RigidbodyEntityComponent **and **TransformEntityComponent **components for each entity for each group where **DynamicRigidBodies** entities can be found. The *foreach *will iterate over all the arrays found in the separate groups, regardless how many they are. **rigidbodies **and **transforms **are obviously arrays. **count **is their length. **group **is the current group iterated. The user then can iterate the components knowing they belong to the same entity for each index used in the arrays iteration.

Several examples of entity iterations can be found in the **MiniExamples** repository.

### New Feature: Filters

Like *GroupCompounds*, the new *Filters *feature allows entities to be iterated according to their states, but differently to the groups, entities can be found in different states/filters at the same time. GroupCompounds are powerful, but also relatively rigid*. *For example, entities can be swapped only during submission time*.* Although the iteration of entities through group compounds is as fast as it can be, group compounds split groups in memory*. This is why the number of compound tags is limited to four so that state permutations won’t lead to an excessive segmentation of the memory*.

Filters, on the other hand, allow the creation of subgroups through indexing. Filters are nothing more complex than an array of indices that subsets entities found in groups. GroupCompounds and Filters are orthogonal. GroupCompounds divide entities into multiple arrays, which benefits specialised engines, but penalised abstract engines. Filters instead usually work on simpler ExclusiveGroups that are not split further than the EntityDescriptor group. Filters allow faster abstract engines (since there is no need to jump between groups) and slower specialised engines due to the double indexing needed for the filtering. The use of GroupCompounds and Filters together is possible.

More information at:

### Review: How groups work

Using *GroupCompounds *and specifying an *ExclusiveGroup *for each entity descriptor are foolproof strategies to never experience problems with SECS queries. More advanced usages of groups are for users who truly understand SECS database memory layout.

Fundamentally the memory layout is simple: An array for each component type is used to store the components generated by each entity. The use of simple arrays and components as value types guarantee the components iteration to be *cache-friendy and vectorizable*.

However, it’s common for the user to want to iterate multiple components expecting that each tuple of components belongs to the same entity. Fulfilling this expectation is what makes each ECS library implementation different. SECS solves this problem explicitly with the use of groups. *As long as ALL the entities present in the queried group contain the tuple of components to iterate, SECS guarantees that each tuple iterated belongs to the same entity.*

This problem is simpler to visualise than to explain:

An entity descriptor can generate several components. Let’s say that **E1** are entities generated from **EntityDescriptor1** and **E2** are entities generated from **EntityDescriptor2**. Let’s say that **E1** generates **EntityComponentA (E1-CA)** and **E2 **generates **EntityComponentA** **(E2-CA)** and **EntityComponentB (E2-CB)**. This means that **E1 **and **E2 **have components of type **A **in common, while only **E2 **have components of type **B**. If the user builds five **E1 **entities and three **E2 **entities *using the same group*, in memory the components are laid like this:

```
0 1 2 3 4 5 6 7
array of components A (CA) = [E1-CA, E1-CA, E1-CA, E1-CA, E1-CA, E2-CA, E2-CA, E2-CA]
array of components B (CB) = [E2-CB, E2-CB, E2-CB]
```


Once an engine queries for the components **CA **and **CB **using the group specified during the building, the **CA **and **CB **components arrays are returned exactly as shown in the example above. Using the same index will now result in mixing components from different entities. *In any case, SECS won’t even allow this query, as, at least, the size of the arrays of components queried must match.*

Groups are used for many purposes, but the most important and advanced one is the customization of the memory layout. Entity components are in fact split according to the groups, therefore groups play an important role in the organization of the entity components and the consequent way they must be iterated over.

if the two entities are built *using a group for each entity descriptor*, the entity components will be now laid out like this:

```
Group ED1:
array of component A = [E1-CA, E1-CA, E1-CA, E1-CA, E1-CA]
array of component B = []
Group ED2:
array of component 1 = [E2-CA, E2-CA, E2-CA]
array of component 2 = [E2-CB, E2-CB, E2-CB]
```


which means that it’s now possible to iterate over the two entity views of **E2**, using the same index in the only loop necessary.

However as long as either *GroupCompounds *are used or the rule of one group for each EntityDescriptor is applied, the new Svelto user doesn’t really need to be aware of this architectural organization as it will just work.

### New Feature: Find Groups

While more features can be added to make the advanced use of groups safer, **FindGroups **is already the solution for most cases. FindGroups returns all the valid groups where to find entities that generate the same set of components.

It’s simply used like this:

```
//return all the valid groups where ColourParameterComponent and BlockTagComponent can be queried
var groups = entitiesDB.FindGroups<ColourParameterComponent, BlockTagComponent>();
//iterate all the entities found in the group
foreach (var ((colours, tags, count), _) in entitiesDB
.QueryEntities<ColourParameterEntityStruct, BlockTagEntityStruct>(groups))
{
for (int i = 0; i < count; i++)
{
ref var colour = ref colours[i];
ref var tag = ref tags[i];
}
}
```


While *FindGroups *looks simple to use, the user shouldn’t use the method only when meaningful.

### New Feature: Engines Groups

*Engines Groups *may remember the **ComponentSystemGroup **found in UECS. Engines groups allow to group engines and even run them in a given order, using the **SortedEngineGroup** and the **Sequenced **engine attribute** **features. An example of how to sort engines using **SortedEngineGroup **is found in the **MiniExample 1: Doofuses** and **Miniexample 2: Survival**. The solution has been designed to allow engines from different assemblies (asmdefs in Unity) to be sorted without creating dependencies between assemblies. Only the Composition Root assembly will need to know the assemblies where the engines are declared.

```
///it's important to note that the names of the engines used in the ISequenceOrder, do NOT need to come from the
/// same enum. This will allow the user to declare enums in their own assemblies.
public enum DoofusesEngineNames
{
SpawningDoofusEngine
, PlaceFoodOnClickEngine
, LookingForFoodDoofusesEngine
, VelocityToPositionDoofusesEngine
, ConsumingFoodEngine
}
/// <summary>
/// The order of the engines found in the enginesOrder array is the order of execution of engines
/// </summary>
public struct DoofusesEnginesOrder : ISequenceOrder
{
public string[] enginesOrder => new[]
{
nameof(DoofusesEngineNames.SpawningDoofusEngine)
, nameof(DoofusesEngineNames.PlaceFoodOnClickEngine)
, nameof(DoofusesEngineNames.LookingForFoodDoofusesEngine)
, nameof(DoofusesEngineNames.ConsumingFoodEngine)
, nameof(DoofusesEngineNames.VelocityToPositionDoofusesEngine)
, nameof(JobifiedSveltoEngines.SveltoOverUECS)
};
}
//The engines added in this group will need to be marked as Sequenced and signed with the enums used inside
//the ISequenceOrder struct. If the ISequenceOrder names and the signatures do not match, Svelto will throw an
//exception. If they match, the engines will be executed using the ISequencedOrder declaration.
public class SortedDoofusesEnginesExecutionGroup : SortedJobifiedEnginesGroup<IJobifiedEngine, DoofusesEnginesOrder>
{
public SortedDoofusesEnginesExecutionGroup(FasterList<IJobifiedEngine> engines) : base(engines)
{
}
}
```


### New Feature: Native Memory and DOTS

Performance is obviously a hot topic for SECS. Even if Svelto.ECS has been designed to improve code maintainability, performance is one of the top priorities for the framework. For Unity users, performance nowadays means using Jobs and Burst, which have been both designed to use native memory. While I have some personal strong opinions on how the Unity Jobs architecture has been designed, I consider Burst a marvel of technology. Using Burst fundamentally removes any need to use native languages to seek high performance. Making SECS native memory compatible, especially since *Unity mono doesn’t support Span<T>* properly, has been an interesting challenge and at times frustrating. However, I am more than glad about the result achieved.

In these articles:

and

you will find the explanation of what I have done to support native memory in Svelto, which is necessary for Unity Jobs and Burst to work. Native memory will also give a little boost even when Jobs and Burst are not used. My special solution to support native memory has been tested successfully on several platforms. In general, the user doesn’t need to know when native memory or managed memory is used, but in SECS 3.0 *EntityComponents *are always stored in native memory, while *EntityViewComponents *are always stored in managed memory.

A set of native data structures have been added as well to work with native components. These are **NativeBag**, **NativeDynamicArray **and the very powerful **SveltoDictionary**. Since, at the moment, *EntityComponents *are always stored in native memory, these native data structures are necessary when it’s needed to store data in custom ways inside native components. However, since this is a necessity strictly linked to Unity DOTS, in future I will add the option to switch the storing of entity components to managed memory as well. All the native data structures explicitly created by the user must also be disposed of to avoid memory leaking.

The following Svelto.ECS operations are fully jobifiable and burstifiable:

- Any structural change (Creation, Destruction and Swapping of entities)
- Any entity components kind of query and their iteration
- Being able to query entities by EGID (through NativeEGIDMapper and NativeEGIDMultiMapper)
- Filters related operations

*However note that while these operations can work in multi-threading code, svelto is not thread-safe*. It’s the user that must ensure that the operations executed on SECS DB are thread-safe*. *

To see the power of fully jobified and burstified SECS, please have a look at** MiniExample 1: Doofuses Iteration 3.**

![](../../assets/8ebd8c8f5866a6bf.gif)

### New Pattern: integrate Svelto.ECS with Unity ECS

*Svelto.ECS is designed to be platform agnostic*. In fact, a bunch of Svelto users have already tested it on platforms outside Unity and thanks to the *growing interest* in using .net for game development, SECS can actually become an attractive solution to adopt the ECS paradigm everywhere. What about Unity though? Now that Unity ECS is becoming more stable, Unity users will absolutely wonder what’s the point in using Svelto.ECS. This is my take: UECS core has been initially designed to rewrite the Unity Engine features from Object Oriented code to Data Oriented Code. This process will take years to complete and UECS will evolve according to the new challenges the company will encounter. My conclusion is that UECS is fundamentally designed to develop an engine. At least this is my impression after using it in Gamecraft. Svelto.ECS has been designed instead just to develop games. Furthermore, I don’t plan to develop a 4.0 version. SECS will be feature complete during the 3.x cycle guaranteeing long-term* stability.*

SECS shows its true power when it’s used together with a data-oriented engine that doesn’t use objects. That’s why SECS and UECS can operate together. Several Svelto.ECS features have been introduced to integrate UECS so that pure ECS can be used throughout the codebase. This integration has the benefit to keep UECS code simple. Code maintainability and impressive performance can be easily achieved using SECS and UECS together. *The logic is then simple: the user can see UECS as a data-oriented engine library rather than a game library and use Svelto on top of it.*

**MiniExamples 1: Doofuses (iteration 3)**, shows how SECS and UECS integration can be achieved, although it’s just one of the possible strategies.

While keeping SECS and UECS layers separate has some obvious code design benefits, it also introduces some drawbacks, although they didn’t weigh on us during the development of Gamecraft. These are mainly two: the need to synchronise entities between SECS and UECS and losing the automatic job dependency system resolution, which works only with UECS entity components. At Freejam, we haven’t found either of these drawbacks to be a noticeable problem.

At first, exposing UECS complexity may appear to be a drawback of the SECS and UECS integration. However this is, in my opinion, an advantage, as the automatic mechanisms in UECS, while appealing at first, become awkward with complex project scenarios.

However, the truth is that big companies that pay for unity support will be unlikely to consider using Svelto, as they can get direct support from Unity for every problem found. *The main reason I choose Svelto over UECS is because of its design approach which promotes the use of patterns that aid the writing of maintainable code.*

### Important Pattern: How to write abstract engines and reuse code

I am an advocate of introducing ECS as a paradigm and not a pattern. While one of the most obvious benefits of a 100% ECS application is that solutions look very similar to each other, *ECS *solutions to specific problems can be written with different strategies. However, this shouldn’t penalise code maintainability as it’s essential to reuse code written in engines so that they can operate on a not predefined super-set of entities. In other words, it is possible to write *abstract ECS *code. This is not the first time I expose this idea. In theory, using Inversion of Control, the code should be designed in multiple layers from the most abstract to the most specialised, following the SOLID *Dependency Inversion Principle*. Applying the principle with Svelto is simple: identify the behaviours to apply and identify the (abstract) entity to which this behaviour must be applied. If the layer is abstract, the set of components may or may not identify a concrete entity. The layer can then be packaged, for example in a separate assembly, and expose *Abstract engines*, *components*, *groups *and *entities descriptors* that can be extended if necessary. Abstract layers serve the purpose to reuse as much code as possible without the user even realising it. Once the abstract engines are used, they will start to operate on the layer provided components.

In practice, the user must be aware that *early abstraction is the root of all *evil. So unless the design is clear and firmly etched in the user’s mind, the best thing to do is to start working with specialised entities and engines and abstract only when shared/common behaviours between different entity types are identified.

There are several strategies to approach this problem:

The abstract layers provide *components and group tags*, possibly **ExtendableEntityDescriptors **too. The specialised layers are then expected to use *GroupCompounds *adopting the provided tags or extending entity descriptors from the provided ones.

In this scenario, the abstract engines iterate concrete entities found in agglomerated groups, like the **DamageableEntitiesGroups **example previously seen at the beginning of this article.

Another strategy is for the abstract layer to not expect where the entity components will be found and use **FindGroup **to identify the list of groups where to find the *superset *of entities sharing a tuple of components. In this case, the engine doesn’t even expect specific entities, but it iterates all the entities generated from entity descriptors sharing the same components.

Other strategies involving Filters and Generic Parameters implementing shared interfaces can be used by resourceful users if they want to explore different patterns.

This paragraph deserves an entire separate article and hopefully it will come if requested by users.

More details can be found on this topic in this article:

### Note: Svelto.ECS is not only Unity!

I understand why using SECS with Unity is controversial and I accept all the arguments. However, let’s not forget that SECS works perfectly outside Unity too! It opens so many exciting opportunities since there are so many platforms supporting .net nowadays. This is a list of the ones I know about:

- Monogame
- Ports of XNA (FNA, FlatRedBall)
- Godot
- Stride
- Wave
- Unreal with UnrealCLR
- CryEngine
- UniEngine

The **MiniExample 4** even shows how to use SECS with pure .NET and the SDL library and it’s the best starting point to experiment with SECS on platforms other than Unity.* I am looking forward to integrating more not Unity examples in the MiniExample repository, but I need the community help for this.*

![Image](../../assets/5a1a1f4cde232919.gif)

### Side Note: Distribution and compatibility

[Svelto.ECS for unity is distributed using OpenUPM](https://www.sebaslab.com/distributing-svelto-through-openupm/) or it can be directly downloaded from the Github repository. SECS uses the Microsoft Unsafe DLL which was supported by Unity until the previous version of DOTS. Since Unity dropped the support, I decided to distribute the Unsafe DLL through open UPM as well.

*License wise Svelto.ECS is completely open to commercial use, modification and so on. There is no limit, I don’t need credits. Svelto community is small, but ever-growing so seeing more people joining us would surely be helpful for everyone.*

For platforms outside Unity, SECS is now distributed through NuGet too.

### Footnotes

*Please feel free to ask me what you want to read from my next articles. I need your feedback to know where I should spend my little spare time. Leave a comment or write on our discord channel! The future of Svelto.ECS development from now on will depend a lot on the users’ interest and contribution as well*

I have been watching the development of Svelto for a while now. Your articles shine like a beacon in the heap of beginner focused articles that explain basic ECS concepts etc…

BUT please consider either hiring or just making a few tutorials yourself.

I feel like there is a big barricade between this framework and actual users. Your discord is awesome and all but it just cannot beat creating a community on youtube etc…

Keep being awesome!

Hello, thanks for the comment.

I strongly believe that the mini-examples should fill that gap. Please check this link for clarifications:

https://github.com/sebas77/Svelto.ECS/wiki

Indeed. While others are churning out beginner’s tutorials and constantly nagging about the superficial properties of ECS, your articles are really enlightening. I know that from a vague theory to real-world deployment it is a rather long way to go, and I’m sure that what’s more valuable is the gains and pains you got during that phase, NOT how the initial idea got formed. For example, the use of different groups is really brilliant to me. I’ve been learning and experimenting with a handful of ECS’s for a while, but I’ve never considered that an ECS framework should expose the… Read more »

Thank you, in truth I have much more to write about, I hope I can resume after releasing Svelto.ecs 3.2

I’m using your framework in a Lab assignment (I’m attending a game development course in university). For now, I’m still learning it.

Don’t forget to join our discord server so we can stay in touch

Is this ECS compatible with Webgl?

at the time I test it yet, Miniexamples 2 survival is webgl

I have opened up Example2-Unity Hybrid-Survival in Unity 2019.4.31f1. It builds but I am not able to run anything in chrome.

I will add in the instructions that you have to build the addressables first. It’s unfortunate that is not part of the building process

Thank you very much, it works after that first step of building addressable groups.