---
title: Svelto.ECS 3.4 - Svelto On DOTS ECS update - Seba's Lab
url: https://www.sebaslab.com/svelto-ecs-3-4-svelto-on-dots-ecs-update/
author: Sebastiano Mandalà
published: '2023-03-13'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

## Introduction

Svelto.ECS is a *platform-agnostic C# Entity-Component-System framework*. You can catch its flexibility in action through the Svelto mini-examples, with applications written for *Unity, .Net, SDL and Stride Engine*. When using Svelto.ECS with Unity, the user has the option to take advantage of the entire DOTS suite or specific parts, such as DOTS JOBS/BURST and/or DOTS ECS. The latter can be used as an ECS-based engine library to create your games.

## If you are new around here

My new article usually assumes that the user knows already about Svelto and for this reason doesn’t delve too much into implementation details. So if you are new to Svelto, you may wonder why to use Svelto.ECS instead of DOTS ECS. There are multiple reasons:

- as for any other libraries, having multiple choice is a good thing.
- the implementations are different. DOTS ECS uses an archetype base model, Svelto.ECS uses a novel and unique
[Group based model](https://github.com/sebas77/Svelto.ECS#is-it-archetype-is-it-sparse-set-no-its-something-else-o)which changes the way the user sees entity sets. - Svelto.ECS is completely
[open source](https://github.com/sebas77/Svelto.ECS). So the code is not just available, I encourage the user to fork it and pull improvements - Svelto.ECS is production ready and used in commercial products. Version 4.0 will never see the light. The next versions are only planned improvements that I will develop in my spare time.
- you will get free support on
[Svelto Discord Server](https://discord.gg/JTUZuJcME5). - Svelto.ECS is made basically by one person. For this reason, I couldn’t afford over-engineering. The implementation is as simple as it can get. No shenanigans around.
- Not everything can be solved with ECS and Svelto.ECS hasn’t been developed to serve multiple purposes. It hasn’t been conceived to move a whole engine to ECS. Engines have very different needs than games and algorithms for engines are often significantly different and not suitable for ECS
- Svelto.ECS has been designed to develop multi-paradigm ECS-centric applications. Not everything can be solved with ECS.
- While Svelto.ECS is fast, the design decisions around it were not solely taken for the purpose of writing faster code, but also to encourage clean and efficient code writing. It has been designed to write large applications by teams of any size.
- Svelto.ECS uses native memory extensively to be completely compatible with DOTS BURST and DOTS JOBS.
- Some features that Svelto.ECS provides are not present with DOTS ECS (
[like the filters](https://www.sebaslab.com/svelto-ecs-3-3-and-the-new-filters-api/), more about them later in this article) - I started developing Svelto.ECS years before Unity announced DOTS. The philosophy that brought me to prefer ECS over OOP is explained in length in my articles
[code design articles](https://www.sebaslab.com/category/code-design/)and is fundamentally different from the reasoning behind DOTS ECS.

## Svelto-On-DOTS

The purpose of integrating DOTS ECS with Svelto.ECS is to give users the flexibility to use the new DOTS ECS features at their discretion. However, it’s worth noting that the usage of DOTS ECS with Svelto.ECS differs from the way the DOTS ECS team intended.

The integration happens through the synchronization of Svelto entities with DOTS entities. An explanation of this pattern can be found in this article that I suggest you read to have a better idea of what we are discussing in this article.

When Svelto-On-DOTS is used, the *application frame* is split into the following steps:

*Svelto (GameLogic) Engines run first**The Svelto-On-DOTS integration starts with a sync point. all Jobs affecting DOTS entities will be completed*.*The Svelto-to-DOTS Synchronizations engines are executed**Svelto Submission of Entities step is executed**Svelto Add/Remove callbacks are called (usually***ISveltoOnDOTSStructuralEngine**uses these to handle DOTS entities structural changes/states)

*SveltoOnDOTSStructural Engines post submission step is executed**any pure DOTS ECS engine is updated (DOTS ECS***World.Update()**is called)*The DOTS ECS-to-Svelto.ECS Synchronizations engines are executed*


Almost everything breaks the typical use of DOTS ECS, the main points are:

**UNITY_DISABLE_AUTOMATIC_SYSTEM_BOOTSTRAP_RUNTIME_WORLD**or**UNITY_DISABLE_AUTOMATIC_SYSTEM_BOOTSTRAP**defines must be used at the project level. Svelto controls the whole DOTS ECS flow*DOTS ECS world is created and handled by Svelto.**All Sync Engines must be tagged as***[DisableAutoCreation]**. The engines must be explicitly added to the Svelto DOTS world*All the pure DOTS ECS systems must be tagged as*all**[DisableAutoCreation]**. The pure DOTS ECS systems must be explicitly added to the Svelto DOTS ECS world (provided by Svelto). The user can use*the standard DOTS ECS system features**The DOTS ECS world is Updated by Svelto.*

To see how this works in practice, please check the simple [Doofuses example](https://github.com/sebas77/Svelto.MiniExamples/tree/master/Example1-DoofusesMustEat/DOOFUSES_DOTS).

## How to use Svelto-On-DOTS

In Svelto.ECS everything is explicit and user-controlled. Personally, I don’t appreciate frameworks taking from me the responsibility to populate my composition root. This unequivocally has only drawbacks, mainly limiting the flexibility of how the user can handle dependencies. Now, it’s clear that, in a pure ECS world, dependencies do not exist and it’s clear that DOTS ECS 1.0 is putting a lot of stress on this, but it’s also true that a pure ECS application is mostly impossible to achieve. Svelto promotes ECS-centric applications and for this reason, allows the user to inject dependencies in engines if necessary.

A composition root also helps a lot to visualise what’s going on and why. It’s true that the inspector can also show what systems are running in which world, but a composition root surely gives more sense that things are under the user’s control.

I won’t show how a Svelto.ECS composition root looks, as several can be found in the mini examples. A *SveltoOnDOTS *composition root differs from a standard one only for the user of a **SveltoOnDOTSEnginesGroup** that must be added to the *engines root*:

`_sveltoOverDotsEnginesGroup = new SveltoOnDOTSEnginesGroup(_enginesRoot);`


once this is created, the users can add the Svelto-On-Dots engines through:

```
_sveltoOnDotsEnginesGroup.AddSveltoToDOTSSyncEngine(new RenderingDOTSPositionSyncEngine());
_sveltoOnDotsEnginesGroup.AddDOTSToSveltoSyncEngine(new SyncExampleEngine());
_sveltoOnDotsEnginesGroup.AddSveltoOnDOTSSubmissionEngine(new SyncSubmissionEngine());
```


being *sveltoOnDotsEnginesGroup *an engine group, its tick will tick all the engines registered into it. It will also execute point 2 of the Svelto-On-DOTS frame steps shown in the previous paragraph.

Of course, don’t forget that Svelto leaves to the user the responsibility to tick the engines.

#### Svelto-on-DOTS sync engines

Svelto-on-DOTS sync engines are pretty intuitive. A sync engine can look like this:

[DisableAutoCreation] public partial class RenderingDOTSPositionSyncEngine: SyncSveltoToDOTSEngine, IQueryingEntitiesEngine { public EntitiesDB entitiesDB { get; set; } public void Ready() { } //add a not about the fact it's not synchronising food protected override void OnSveltoUpdate() { //sync engines are usually semi-specialised engines. They can get more abstract using FindGroup, or they can be semi-abstract //using GroupCompounds like in this example (GameGroups.Red.Groups) //In some cases, like for the rendering, the 1:1 relationship is not necessary, hence DOTS ECS entities //just become a pool of entities to fetch and assign values to. Of course we need to be sure that the //entities are compatible, that's why we group the DOTS ECS entities like with do with the Svelto ones, using //the DOTS ECS shared component DOTS ECSSveltoGroupID. //when it's time to sync, I have two options, iterate the svelto entities first or iterate the //DOTS ECS entities first. foreach (var ((positions, _), group) in entitiesDB.QueryEntities<PositionEntityComponent>( GameGroups.RED.Groups)) { Entities.ForEach( (int entityInQueryIndex, ref Translation translation) => { ref readonly var positionEntityComponent = ref positions[entityInQueryIndex]; translation.Value = positionEntityComponent.position; }) .WithSharedComponentFilter(new DOTSSveltoGroupID(@group)).ScheduleParallel(); } } public override string name => nameof(RenderingDOTSPositionSyncEngine); }

There are usually two strategies (and several variations of them) to sync Svelto to DOTS ECS. The simplest one is shown in the example above. DOTS ECS entities set are seen as a pool of entities. These pools purposely match the size of the Svelto entity sets. This is guaranteed through the DOTS **SharedComponentFilter **use, which is part of the Svelto-On-DOTS patterns.

The alternative strategy is to have a 1:1 relationship between Svelto.ECS and DOTS ECS entities. This is necessary, for example, for stateful physic engines (Havok).

Thanks to Burst, Jobs and cache-aligned data structures, sync engines usually add very little overhead to the application. After all, copying and passing data around is what ECS is made for.

Remember that Svelto-On-DOTS promotes using DOTS ECS *ONLY AS A ENGINE ECS LIBRARY*. For this reason, your sync engines are usually limited to very few parameters, like transformation matrices, rendering colours or physic attributes for example. Sync engines will basically deal with DOTS ECS library components and are not expected to use user-created DOTS components.

#### Svelto-on-DOTS submission engines

the submission engines may be less intuitive. Their responsibility is to handle the DOTS entities lifetime and structural changes. Usually, the user would need to care only about creating new entities, since Svelto-On-DOTS automatically handles removal and states transitions (hence updating the DOTSSveltoGroupID shared component). However, all these behaviours are customisable for advanced users. The standard pattern is to create DOTS entities when Svelto entities are created and this is normally done through the Svelto.ECS *Add callbacks*:

public void Add((uint start, uint end) rangeOfEntities, in EntityCollection<DOTSEntityComponent> entities, ExclusiveGroupStruct groupID) { if (GameGroups.FOOD.Includes(groupID) == true) { var (sveltoOnDOTSEntities, ids, _) = entities; var (positions, _) = entitiesDB.QueryEntities<PositionEntityComponent>(groupID); InitDOTSFoodPositionJob job = default; job.spawnPoints = positions; job.sveltoStartIndex = rangeOfEntities.start; job.entityManager = DOTSOperations; using (new PlatformProfiler("CreateDOTSEntityOnSveltoBatched")) { //Standard way (SveltoOnDOTS pattern) to create DOTS entities from a Svelto ones. The returning job can be used as job dependency var DOTSEntities = DOTSOperations.CreateDOTSEntityFromSveltoBatched(sveltoOnDOTSEntities[0].dotsEntity, rangeOfEntities, groupID, sveltoOnDOTSEntities, ids, out var jobHandle); job.createdEntities = DOTSEntities; //run custom job to initialise the DOTS position jobHandle = job.ScheduleParallel(job.createdEntities.Length, jobHandle); //don't forget to add the job to the list of jobs to complete at the end of the frame DOTSOperations.AddJobToComplete(jobHandle); } } }

The pattern is designed to let the user set the initial values of the DOTS component if required. In this example, the spawning position is set through the **InitDOTSFoodPosition **job.

This engine implements the **ISveltoOnDOTSStructuralEngine** interface, which provides the **DOTSOperations **property, that is a DOTS **EntityManager **wrapper.

## Update to DOTS ECS 1.0

The following part of this article will be about my early impressions of DOTS 1.0. First I will explain what changed in Svelto-On-DOTS since the previous version:

For a long time, DOTS structural changes were the slowest part of the Svelto-On-DOTS submission frame. My understanding was that this was due to my use of *Shared Components*, which didn’t allow Burst to function during the DOTS structural change phase. For this reason, I was looking forward to DOTS ECS 1.0, so that finally DOTS structural changes wouldn’t be the bottleneck of the execution. When I finally updated Svelto-On-DOTS to DOTS ECS 1.0, to my dismay, I didn’t find this to be true. DOTS ECS structural changes were still the slowest part of the submission. I can’t hide that I was actually upset when I realised the reason of it (known by DOTS ECS users): The **Entity Command Buffer** has actually no real reason to exist. Because it can be used inside jobs, I was under the impression it was the best way to apply structural changes; then I realised that ECB doesn’t actually apply anything, but only queue actions. I said well, that’s what more or less Svelto.ECS does too, except that applying those actions is INCREDIBLY SLOW, making ECB the worst solution to adopt in any of the cases I can think of.

The ECB playback is so slow because actions are replayed one by one, in the same order and in the slowest possible way. This, plus the extra awkward code related to the deferred entity ID resolution, made me completely nuke the ECB from the face of Svelto.ECS codebase. I am instead now using the faster *batched operations* provided by DOTS ECS 1.0. After this change, DOTS structural changes are now as fast as Svelto ones.

This was the main change I had to apply, the rest of Svelto-On-DOTS was so simple that I didn’t need to change much of it.

The result is that the submission frame moved from this:

![](../../assets/eb0fd04d08802197.png)

to this (worst case scenario where resize are necessary, more than 500 entities affected by structural changes):

![](../../assets/99ff3d58f93110da.png)

## My Impression on DOTS ECS 1.0

My first impression of the update is surely positive. DOTS ECS 1.0 is definitively a step forward in the right direction and I can appreciate the enormous effort the team put to move away from the 0.5 patterns. To be concise, I’ll just bullet list the pro and cons but take into consideration that I am NOT a DOTS ECS user.

Pros:

- naturally, I like the new
*idiomatic for each*, since it’s identical to what Svelto has been using for years - with
**ISystem**, I appreciate moving away from inheritance, although the reason why they did it is completely unrelated to the benefit of using interfaces instead than base objects - I do like the idea to make very natural writing 100% burstified code, awesome indeed
- While the main features introduced are few, there are a ton of hidden things, some I am not even sure if were already there. For example, the custom allocator
**RewindableAllocator**is pretty cool. - A lot of data structures are now completely burstifiable.
**EntityManager**can be used directly inside burstified jobs as it is. - A ton of methods are pre-burstified even if they are not called from burstified code. This is the case with the
*batched operations*. - There is a better separation between
*managed and unmanaged components*

Cons:

- the
**ISystem**, while being awesome, pushes the design away from ECS-centric applications. It is obviously designed to try to achieve the 100% ECS idea, which IMO cannot work. What proves this point is the fact that I cannot pass an instance of an ISystem struct, the framework creates it for me. While this is meant to not let the user inject dependencies, it limits interoperability with other paradigms. The workaround in some cases is to use the managed components, which don’t allow the use of Burst, so no clue what the point of this decision is supposed to be. - Svelto.ECS doesn’t use the concept of
*archetypes*because it’s too simple to generate structural changes without being fully aware of the consequences. This problem is now so ingrained in the DOTS users’ minds that many actually suggest avoiding structural changes altogether. This puzzles me since structural change is the fundamental way to create sets of entities in ECS. How would states be implemented otherwise? - DOTS ECS answers this question with the new
**IEnabableComponents**. They are sort of like the Svelto.ECS filters, but actually less flexible. For example Svelto.ECS filters can be used to model ownership relationships, while DOTS IEnabableComponents can be used only to model states. I also have doubts about the efficiency of the implementation. Seems more like a fancy exercise than something that really makes sense to be done in that way. I will reserve the final judgement as to when I will profile them, if I will ever find the time to do so. - I have no clue what to say about the new
**Aspect**feature, but I have doubts it was really necessary (unless there is some performance issue linked to how DOTS specifically works) - I couldn’t find a suitable pattern to operate on just created DOTS entities across different systems, similar to what Svelto.ECS does with the Add callbacks.
- The framework is becoming overreliant on source generation, which can make debugging awkward.
- While they made a ton of optimizations, I still suspect that the hidden overhead of some operations is still a steep price to pay. This was actually a noticeable issue before.
- Last but not least: while the surface of the API has been significantly simplified, I cannot shake the impression (probably founded) that the foundations of DOTS ECS are simply over-engineered, limiting how much the framework can eventually do and how much the API can be eventually simplified. I am pointing my fingers at the idea of the chunks. Something that in theory should be more performant, but in practice may just introduce more drawbacks than benefits in a real-world scenario.

## Why using DOTS ECS may not be necessary with Svelto.ECS after all

As I mentioned, DOTS ECS is just an ECS framework like any other. Its massive key features are that the code is fully *jobifiable *and *burstifiable*. To be on par with this important feature, Svelto.ECS, although platform agnostic, has been compatible with **Burst **and **Jobs **for ages.

DOTS ECS has the benefit to handle component dependencies in jobs automatically, while with Svelto.ECS the user must be aware of what’s going on. In a remote future, I may shift away from Jobs and reintroduce Svelto.Tasks. Svelto.Tasks parallel processing was in fact on par with DOTS Jobs and could replace it completely, probably saving a ton of overhead introduced by jobs.

Knowing this, using Svelto.ECS and/or DOTS ECS is ultimately a matter of preference. DOTS team is bigger than just one person and a small community, but they have a ton of extra problems to solve (moving an engine to ECS), plus the company revenue is also based on paid support. I am sure that huge companies would prefer to use DOTS ECS since they don’t have money problems, while small teams MAY prefer to have things working out of the box (although I am sure painful problems will always pop up). For this reason Svelto.ECS will remain a niche tool for people who first know very well the ECS paradigm and second know what they want.

However, my idea to use DOTS ECS as an engine library that happens to be written in ECS, and not a game framework, is as valid and perfectly proven by [Robocraft 2](https://www.robocraft2.com/), the latest game made by Freejam. Robocraft 2 is a Svelto.ECS-centric application that uses DOTS ECS only for Havok Physics, while rendering and network are handled by other libraries. Every single block in the game is an entity!

This is the last interesting point I want to rise. Procedural programming is, in reality, more suitable to engine programming than ECS and there are a ton of procedural programming libraries out there. What DOTS ECS packages solve or will solve in future, can be solved already by several open-source data-oriented projects with C# interfaces.

For example with Robocraft 2, the *Compute Shader rendering pipeline* provided by the asset store plugin **GPUInstancer **has been used in place of the DOTS ECS rendering engine. For the network, the team didn’t need to wait for **DOTS ECS NetCode** as **LiteNetLib **was working pretty well. Now I understand that NetCode may have some awesome burstified serialization code, but its abstraction may not always be suitable for every project. While I appreciate the idea that small teams / individuals are able to write ECS games with little effort, more experienced teams would probably need to implement their unique solutions to their unique problems.