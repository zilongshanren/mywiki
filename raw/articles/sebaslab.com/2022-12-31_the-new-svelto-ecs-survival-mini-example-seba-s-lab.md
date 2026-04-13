---
title: The new Svelto.ECS Survival Mini Example - Seba's Lab
url: https://www.sebaslab.com/the-new-svelto-ecs-survival-mini-example/
author: Sebastiano Mandalà
published: '2022-12-31'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

## Introduction

My Xmas gift to the [Svelto Community](https://discord.gg/JTUZuJcME5) this year was the complete rewrite of the[ Survival Svelto.ECS MiniExample](https://github.com/sebas77/Svelto.MiniExamples/tree/master/Example2-Unity%20Hybrid-Survival). This example is used as a reference by all newcomers because it’s the simplest to digest for people who are not in the ECS mentality and still think in terms of objects. Unfortunately, the previous version was quite outdated, misleading new users and diverting them from the most useful Svelto.ECS patterns. For this reason, even if the task bored me out of my mind, I had to do it.

## Goals of the example:

This was the first example I have ever written, which means it is probably around 7 years old. I have gone through numerous refactoring while Svelto.ECS was evolving. The intent of the demo has been:

- Introducing new users to Svelto.ECS features
- Showing the Svelto.ECS patterns for working with an OOP library (in this case the Unity framework). These patterns evolved several times over the years. This latest refactoring has focused on using the
[OOP abstraction layer pattern](https://www.sebaslab.com/oop-abstraction-layer-in-a-ecs-centric-application/)extensively - Introducing the
[ECS abstraction layers](https://www.sebaslab.com/ecs-abstraction-layers-and-modules-encapsulation/) - Demonstrating that Svelto.ECS is compatible with WebGL. The demo runs inside your web browser.

In this article, I am not going to repeat the Svelto.ECS concepts, so to better understand what I am talking about, it’s best to read the following article: [https://www.sebaslab.com/whats-new-in-svelto-ecs-3-0/](https://www.sebaslab.com/whats-new-in-svelto-ecs-3-0/)

## What changed (skip this if you are new to Svelto.ECS):

This new iteration was a complete rewrite of the demo. I focused on removing the abused *implementors based OOP pattern* to show how leaner and easier the *OOP abstraction layer pattern* is to use. I also removed the abused *publisher/consumer pattern*. Let me explain why I needed to do this:

### Implementors are gone (almost)

Svelto.ECS is straightforward to use when it doesn’t need to be mixed with other paradigms. It is efficient to use when the user needs ECS to interact with procedural libraries, but it becomes awkward to use when the user needs to interact with objects. I explained the reason for this in a previous article, but in short, it is because an inexperienced ECS programmer will soon revert to an OOP mindset if given the slightest opportunity to work directly with objects as the jump from an OOP mindset to the ECS mindset is very, very big.

My first solution to this problem was the use of implementors. Implementors were meant to prevent people from returning to OOP, but the complexity of the process caused confusion and made it difficult for users to understand why they had to avoid using objects directly.

Implementors were also not efficient in terms of cache friendliness. For these reasons, implementors are now considered a niche pattern, suitable only for advanced users who know what they are doing. It is no longer considered a pattern for newcomers, and the OOP abstraction layer pattern, which is actually an ECS pattern more than a Svelto.ECS pattern is highly recommended instead.

In the demo, the implementors are only left for the UI (so the user can have some reference on how they are used), but this works only because the UI is extremely simple. For a complex UI, an implementors-based approach won’t work, as the code would again become too cumbersome

### The publisher/consumer use is gone

The publisher/consumer implementation I made for Svelto.ECS has always been controversial. The use case for which I initially wrote this tool has never been put into practice. The reason why it exists and I haven’t deleted it yet is that I was forecasting the need to have a way to let two *EnginesRoot *(entities DB) communicate on the same process at different frequencies (i.e., the relative engines running on different threads). People, including myself, started using it as a replacement for events instead. Events shouldn’t even be used in OOP (I have in the queue an article about this topic), but it’s difficult to see what should be used instead. Really, we should return to the time when event-driven programming was not considered in videogames programming.

Over time, I realized that what people needed from events and the publisher/consumer was to iterate a subset of entities in a given state. To do this, [there is nothing better than filters](https://www.sebaslab.com/svelto-ecs-3-3-and-the-new-filters-api/). This demo proves it clearly.

## How this new (Unity) demo is presented

The demo itself doesn’t need a presentation, it’s an old Unity demo that I just converted to Svelto.ECS code. More interesting is to see the current [github folder structure](https://github.com/sebas77/Svelto.MiniExamples/tree/master/Example2-Unity%20Hybrid-Survival):

![](../../assets/d16e1477f90dd2ae.png)

this folder structure already shows both the ECS layering and the OOP abstraction layer approach. Let’s analyse the code step by step, starting from the [MainCompositionRoot.cs](https://github.com/sebas77/Svelto.MiniExamples/blob/master/Example2-Unity%20Hybrid-Survival/Assets/Code/ECS/MainCompositionRoot.cs)

The code is highly commented, so it should guide you over the details, but at glance, the important bit is:

![](../../assets/cde44606bb117a34.png)

I guess intuitively you are able to visualise already what this is about:

The entities and their behaviours are encapsulated within different layers. To enforce module encapsulation (that is give meaning to the *internal *keyword)* these layers are individual assemblies* (**asmdefs **in unity). This approach allows for better organization and maintenance of the codebase. For more information on the importance of module encapsulation, see my article on the *ECS abstraction layers*.

This demo is extremely simple. Using this demo to show the best Svelto.ECS practices needed sometimes a bit of imagination, but I am happier with the current result than I have ever been.

## ECS Layers in the Survival Demo

### Specialised Layers

*Hud Layer*, *Enemy Layer*, *Player Layer*, and *Camera Layer *are the specialised ECS layers of this demo. Each layer must provide:

- the
*EntityDescriptors*and components of the entities that will be processed by the engines layer - the
*Engines*(Systems) to apply behaviours to entities handled by this layer - the Svelto.ECS
*groups tags and compounds*and or*filters*to identify which set the entities could be found in.

**Asmdefs **naturally create a hierarchy of modules, so you can see which module is depending on which other one and what modules are found on the same layer. Modules do not allow circular dependencies, so the module hierarchy must be clear and well-pondered.

The *HUD Layer *is very specialised and knows a bit of everything from the game. It needs access to the entities handled by the *Player Layer* and *Enemies Layer*.

The *Player Layer* needs to know the* Enemies Layer *to be able to set the *Player Entity* as *Enemy Target*. For a similar reason, it needs to know the *Camera Layer* to set the *Player Entity* as a *Camera Target*.

The *Enemy Layer* is totally encapsulated and doesn’t need to know any other layer except for the *Damageable Layer*.

### Abstracted Layer

The demo is quite simple to be able to justify an abstract layer but I had to find something to show, in this case, *Enemies *and *Player *are both entities that can be damaged and killed, so I came up with the *Damageable Layer*. Abstract layers naturally emerge when entities share the same behaviours. Instead to write very similar code in separate engines in different layers, these engines can be placed in an abstract layer and used by specialised layers. The Abstract layer must provide:

- optional one or more
**ExtendibleEntityDescriptor**(in this case the*DamageableEntityDescriptor*) and/or relative components - A set of engines to describe the abstract behaviours
- A set of group tags that can be used by specialised group compounds to identify entities that must be found in subsets used by the abstract layer.

Let’s analyse the only engine found in this layer through the comments I left in it:

namespace Svelto.ECS.Example.Survive.Damage { /// <summary> /// The responsibility of this engine is to apply the damage to any damageable entity. The behaviour can /// be in common with any entity as multiple component parameters could be added to differentiate the outcome /// between entities through data. /// In my articles I introduce the concept of layered design, where several layers of abstractions can /// co-exist. Every abstracted layer can be seen as a "framework" for the more specialized layers. /// This would be part of an hypothetical "damageable entities" framework that could be distributed /// independently by the specialised entities and reused in multiple projects. /// </summary> public class ApplyDamageToDamageableEntitiesEngine: IQueryingEntitiesEngine, IStepEngine { public EntitiesDB entitiesDB { set; private get; } public void Ready() { _sveltoFilters = entitiesDB.GetFilters(); //Create two transient filters, transient filters are automatically cleaned during each entity //submission phase _sveltoFilters.CreateTransientFilter<HealthComponent>(FilterIDs.DamagedEntitiesFilter); _sveltoFilters.CreateTransientFilter<HealthComponent>(FilterIDs.DeadEntitiesFilter); } public void Step() { //Events are not a good way to create subset of entities found in a given state. With Svelto.ECS //there are several approaches to organise subset of entities: //statically, using components //dynamically using group tags in group compounds //dynamically using filters, which can be mixed with group compounds //filters are a great replacement to events to create subset of entities in a given state var damagedEntitiesfilter = _sveltoFilters .GetTransientFilter<HealthComponent>(FilterIDs.DamagedEntitiesFilter); ///This layer provide the "Damageable" tag and expects that damagable entities are found in a compound ///using this tag. Note that if I was expecting to have hundreds of entities, I would not have resorted ///to a complete iteration with if checks. Either I would have used another filter or used a "Damaged" ///tag compound foreach (var ((entities, health, entityIDs, count), currentGroup) in entitiesDB .QueryEntities<DamageableComponent, HealthComponent>(Damageable.Groups)) { for (int i = 0; i < count; i++) { //Add in the damagedEntitiesFilter all the entities that have been damaged this frame. //I am using a transient filter. A transient filter is cleared at each submission so //it is important that this engine runs before the filter is actually used if (entities[i].damageInfo.damageToApply > 0) damagedEntitiesfilter.Add(new EGID(entityIDs[i], currentGroup), (uint)i); } for (int i = 0; i < count; i++) { health[i].currentHealth -= entities[i].damageInfo.damageToApply; entities[i].damageInfo.damageToApply = 0; //reset instead to do a if may help with vectorization } } //select dead entities from damaged ones var deadEntitiesFilter = _sveltoFilters.GetTransientFilter<HealthComponent>(FilterIDs.DeadEntitiesFilter); foreach (var (filteredIndices, group) in damagedEntitiesfilter) { var (health, entityIDs, _) = entitiesDB.QueryEntities<HealthComponent>(group); var indicesCount = filteredIndices.count; for (int i = 0; i < indicesCount; ++i) //filters subset groups using double indexing. It's VERY important to use the double indexing and not i directly { var filteredIndex = filteredIndices[i]; if (health[filteredIndex].currentHealth <= 0) { deadEntitiesFilter.Add(new EGID(entityIDs[filteredIndex], group), (uint)filteredIndex); } } } } public string name => nameof(ApplyDamageToDamageableEntitiesEngine); EntitiesDB.SveltoFilters _sveltoFilters; } }

## OOP Layer in the Survival Demo

The OOP Layer needs a separate paragraph in this article. The OOP Layer goal is to communicate with the OOP libraries that the application uses. The communication happens through a syncing strategy. This strategy is usually applied through the order of execution of the layers engines:

- Frame starts
- Objects are synched to entities
- Svelto engines run
- Entities are synched to objects
- OOP code runs (in this case the unity framework)

- Frame ends

The engines in these layers are the only engines that can access objects making the object interaction completely encapsulated. I could potentially just change this layer to move from Unity to another game engine.

The final mechanism necessary is a way to be able to link one-to-one entities to objects. This is done through the new Svelto.ECS **ECSResourceManager **that will be soon released with Svelto.ECS 3.4.

This layer provides:

- The
**GameObjectResourceManager**, that is a way to link entities to objects one to one - All the extendible descriptors used by the specialised layers
- All the entity components whose data will be synched with objects
- All the Pre-Svelto and Post-Svelto synching engines

An example of Syncing engine is the following:

public class SyncPhysicEntitiesToObjects: IQueryingEntitiesEngine, IStepEngine { public SyncPhysicEntitiesToObjects(GameObjectResourceManager manager) { _manager = manager; } public void Ready() { } public EntitiesDB entitiesDB { get; set; } public void Step() { //Find all the subsets of entities that contains all the following components var groups = entitiesDB .FindGroups<GameObjectEntityComponent, RotationComponent, RigidBodyComponent, PositionComponent>(); //Iterating these entities and sync the values foreach (var ((entity, rotation, rbs, count), _) in entitiesDB .QueryEntities<GameObjectEntityComponent, RotationComponent, RigidBodyComponent>(groups)) { for (int i = 0; i < count; i++) { var go = _manager[entity[i].resourceIndex]; //fetch the object from the manager var transform = go.transform; var rb = go.GetComponent<Rigidbody>(); //in a real project I'd have cached this rb.velocity = rbs[i].velocity; rb.isKinematic = rbs[i].isKinematic; transform.rotation = rotation[i].rotation; } } } public string name => nameof(SyncPhysicEntitiesToObjects); readonly GameObjectResourceManager _manager; }

## Conclusions

I understand this article can be a bit cryptic if you are new to Svelto.ECS. Unfortunately, this demo, even if simple, actually shows a ton of Svelto.ECS features, enough to make this article way too long. Everything is anyway explained in my other articles and you can always ask questions in our populated [Discord server](https://discord.gg/JTUZuJcME5).

My take is that thanks to the use of the OOP Layer and the filters, the codebase of this demo has been simplified and made clearer. I am sure that reading the code will be less cryptic than reading this article.

If you think this article could be improved by adding more information, please leave some comments and I will act on them.

Hi, For me it was difficult to understand the way to apply data oriented to my projects. But I can’t thank you enough for your articles and the survival example update.

These posts don’t seem to get updated lately. I wonder if you are still using the framework?

Hi Fifnmar, I am confused, this post is brand new, literally published yesterday.

Haha! I was too careless. I remember reading a Mini example blog a long time ago. The other day I was thinking of your framework and came here for a look and thought this is an old post lol. Sorry for my weird comment