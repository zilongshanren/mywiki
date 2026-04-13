---
title: 'Svelto.ECS 2.7: what''s new and best practices - Seba''s Lab'
url: https://www.sebaslab.com/svelto-2-7-whats-new-and-best-practices/
author: Sebastiano Mandalà
published: '2018-08-27'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

Since [the release of Svelto 2.5 in May](http://www.sebaslab.com/svelto-ecs-2-5-and-allocation-0-code/) I had the chance to extensively test the code on the newest version of [Cardlife](http://www.cardlifegame.com/) (which, by the way, I strongly recommend you to play 😊). As a result, few, but very important features, plus a bunch of fundamental changes, have been introduced with the latest version. Many were the outcome of some very interesting scenarios that emerged during the development, which made me challenge several times the current design adopted, but that eventually confirmed that the direction taken is still positive.

At the time of writing, [the version 2.7](https://github.com/sebas77/Svelto.ECS) has been already committed in the github mainline for a while and the [Survival Example](https://github.com/sebas77/Svelto.ECS.Examples.Survival) refactored to the new standards, although the other examples and the unit tests still have to be updated. This article will talk you through all the changes, however they are still applied to Unity only*, although I wish someone could help me bringing Svelto to other platforms, as I wouldn’t have the time to do it on my own. Xenko could be a perfect candidate, while Monogame seems interesting too*.

Let’s start showing what’s new in random order of importance:

- Groups must now be used in every function related to the management of entities. Groups were already mandatory, but the so called
*StandardGroup*was hiding the concept making it harder to understand and adopt. Groups are so fundamental for Svelto.ECS that hiding them was resulting in confusion and underuse of the of the framework more powerful features. Making the use of groups explicit was indeed a really good idea. - Groups were just
*integer*values in Svelto 2.5. In 2.7 the*ExclusiveGroup*type has been added. The use of groups as ExclusiveGroup types is strongly encouraged by the framework itself. Exclusive groups are needed to be sure that different groups were not given the same id by mistake. This was absolutely necessary to introduce for a large team, as otherwise it would have been very easy for the users to adopt the same id unintentionally. Exclusive groups can be defined anywhere in the code and their visibility chosen by the user, using the following code:

```
static class ECSGroups
{
public static readonly ExclusiveGroup Player = new ExclusiveGroup();
}
```


it’s then used like:

` _entityFactory.BuildEntity(player.GetInstanceID(), ECSGroups.Player, player.GetComponents());`


*RemoveEntity*and*SwapEntityGroup*now need the*EntityDescriptor*set by generic parameter. This was added to make the code more readable, the users’ intention clearer and to make explicit the fact that the whole entity will be removed and not just a specific entity view. This made the framework code simpler too.*RemoveEntity*and*SwapEntityGroup*do not happen immediately as before, but during the next entity submission iteration. This is potentially a logic breaking change.- The
*Sequencer*has been fundamentally changed, therefore breaking existing logic. The Sequencer has been taken to its original form intended to enforce the order of execution of engines for the rare times this may be needed. For this reason, it is not possible any more to pass data through sequencer steps as in this way it was used more like a data broadcaster. - Many renaming and signature changes will introduce various code breaking, but easy to fix, errors in pre-existing code bases. Sorry about that, but these changes are needed to make the framework more and more fool-proof.

I will now go through these changes to explain why they were needed, but first I want to thank all the people that helped me going through various levels of reasoning, starting from my colleagues to the people who joined the [Svelto chat on Discord](https://discord.gg/QGUTAC). I absolutely recommend you to join us, as Svelto is an open source effort and would benefit a lot from any form of collaboration.

### Why Groups are fundamental in Svelto

#### Groups for the memory layout

The entity database is managed through a unique and relatively simple data structure. This data structure ensures that entity views of the same type are stored sequentially in memory. When used with entity structs, this memory layout allows to achieve cache-friendly data access that could boost the performance of big iteration quite noticeably.

However, since the same abstract *EntityViewStruct* or *EntityStruct* can be generated and shared by different entities and since users can iterate directly over the array that hold these entity views, different arrays wouldn’t be necessarily indexable in the same way or have the same size at all. Let’s give a better example, as described in detail [in this issue:](https://github.com/sebas77/Svelto.ECS/issues/36)

An entity descriptor can generate several components. Let’s say that **E1** are instances of the **EntityDescriptor1** and **E2** are instances of the **EntityDescriptor2**. Let’s say that **E1** generates **entityview1 (EW1)** and E2 generates **entityview1** and **entityview2 (EW2)**. In memory they are laid like this:

array of component 1 = [E1EW1, E1EW1, E1EW1, E1EW1, E1EW1, E2EW1, E2EW1, E2EW1] array of component 2 = [E2EW2, E2EW2, E2EW2]

so if an engine would need to iterate over the **EW1** and **EW2** of the entity 2 instances alone, it wouldn’t be possible to use the same index during the iteration, as the two arrays are different, leading to awkward workarounds, like for example exploiting the ability to query entities by index, which would make the iteration slower than necessary.

Groups in Svelto.ECS are used for many purposes (which I will try to list in this article), but the most important and least understood one is the customization of the memory layout. Entity views are in fact split according the groups, therefore groups play an important role on the organization of the entity views and consequential way they must be iterated over.

if the two entities are build in different groups, the entity views will be now laid out like:

```
Group 1:
array of component 1 = [E1EW1, E1EW1, E1EW1, E1EW1, E1EW1]
Group 2:
array of component 1 = [E2EW1, E2EW1, E2EW1]
array of component 2 = [E2EW2, E2EW2, E2EW2]
```


which means that it’s now possible to iterate over the two entity views of E2, using the same index in the only loop necessary. The new method *ExecuteOnAllEntities* allows to execute code over all the entities, regardless the group, however manually iterating over a set of groups may be a very good choice too. For example in the Survival code you can find:

`public static readonly ExclusiveGroup[] DamageableGroups = { ActiveEnemies, Player };`


this is then used in the **CharactersDeathEngine** as

```
entitiesDB.ExecuteOnAllEntities(ECSGroups.DamageableGroups,
(ref HealthEntityStruct health, IEntitiesDB entitiesdb, int index) =>
{
if (health.currentHealth <= 0)
health.dead = true;
});
// it's equivalent to:
// foreach (var group in ECSGroups.DamageableGroups)
// {
// int count;
// var entitiesHealth = entitiesDB.QueryEntities(group, out count);
//
// for (int i = 0; i < count; i++)
// {
// if (entitiesHealth[i].currentHealth <= 0)
// entitiesHealth[i].dead = true;
// }
// }
```


so choose your groups wisely!

#### Groups as entity states

it's probably not that practical to implement algorithms like **FSM** with ECS. It's surely possible to use state machines as external services, but then the data of the entities must be adapted to be compatible, which probably wouldn't work that well with entity structs. Naturally the way to manage states for an entity is to have an entity component holding that state, which would translate in *if* checks that would be used inside the engines that need to be aware of the state. If the engines and the states multiply, then it would very quickly escalate in to messy and hard to maintain code. Some ECS implementations solve this problem using the equivalent of entity views (usually entity components) as states. The existence of the component itself would represent the entity into a given state. Systems that are interested in operating only over entities under a specific state, would then iterate only over entities holding that specific component. While the idea may not be terrible, I am still perplexed that methods like *AddEntityView* and *RemoveEntityView* spread around engines would make the code less readable and maintainable. At the moment I reckon that groups are enough to handle these cases, albeit the limitation being that an entity cannot be in more than one state at a time as an entity cannot belong to more than one group at a time. Example of groups as states are **ActiveEnemies**, **DeadEnemies** and **EnemiesToRecycle **groups. In the example, an **EnemyEntity** can stay in one of these states at any time.

often I am asked how to manage cases like where it's needed to know what entities are, for example, carried by another entity. This is like asking if entities are in a specific state (carried by another entity). It would be enough to create a group per carrying entity to know what entities are carried by what carrying entity. Since groups must have unique ids, the only way to do so is to reserve a range of consecutive ExclusiveGroups, one for each carrying entity, and then check in which group a specific entity is through it's EGID. the groupID will translate to the carrying entity id as ExclusiveGroups can be casted to int. For example:

```
public static readonly ExclusiveGroup CarryingEntitiesGroups = new ExclusiveGroup(10); //I know there are going to be 10 carrying entities at most.
entityFunctions.SwapEntityGroup
```(carriedEntity.egid, (int)CarryingEntitiesGroups + carrying.egid.entityId);


this code assumes that the entity id of the carrying entities can go from 0 to 9;

Another example is of course to use groups to pool Implementors [like explained in my previous article](http://www.sebaslab.com/svelto-ecs-2-5-and-allocation-0-code/).

#### Reinterpreting groups

in order to maintain engine encapsulation, groups reinterpretation becomes very handy. For example, some ExclusiveGroups can remap other pre existing group just through different names:

```
public static readonly ExclusiveGroup PlayerTargets = ActiveEnemies;
public static readonly ExclusiveGroup CameraTarget = Player;
public static readonly ExclusiveGroup EnemyTargets = Player;
public static readonly ExclusiveGroup[] TargetGroups = { ActiveEnemies, Player };
public static readonly ExclusiveGroup[] DamageableGroups = { ActiveEnemies, Player };
```


any time is necessary to change the meaning of **TargetGroups** or **DamageableGroups**, it wouldn't be needed to change the Engine code, but would be enough to change this declaration.

### Encapsulation of Engines and the case of the Sequencer

One of the reason I love the ECS paradigm is the possibility to write perfectly encapsulated logic. Only the data is shared between engines, but the logic can be finally written to really follow the* Open/Closed SOLID principle* in practical and not just theoretical terms.

However in Svelto.ECS there are two ways to badly break this encapsulation: the **Sequencer** and the **DispatchOnSet/Change**. While the DispatchOnSet/Change can be still justified looking at it as a form of data binding (data pushing instead of data polling), with insight the Sequencer wasn't probably a great idea to start with, luckily though the use of the Sequencer is really rare and justified just be few use cases. In fact it's not the Sequencer to be a problem, rather than designing engines that need to be executed in order. I reckon the majority of the times this is the consequence of badly designed features more than really a necessity. The Sequencer breaks encapsulation when the next engine must be aware that something happened in the previous engine as engines must always work regardless the execution of other engines. In this sense, the execution of engines through a sequencer should be seen as an engine pipeline where the engines do not start private loops but their execution is triggered by the previous engine in the pipeline. Seen in this way, initially seemed to make sense to give the possibility to feed the next engine with the output of the previous engine. However this soon led to the abuse of the tool, making me change my mind about it. Data must be always fetched through entities and this is why now sequencers can only pass to the next engine an EGID. In conclusion, an engine executed through a sequencer is not supposed to work on its own, making it less modular and dependent by other engines. This would make the application of the Open/Closed principle harder, therefore Sequencer should really be used when strictly necessary (which now, without the data parameter, is going to be very likely the case).

### Pushing or not pushing? (AKA polling vs data-binding)

Back in times when there was the main loop only and the concept of event driven programming wasn't widely adopted, nothing was reactive and everything was polled. Events back then where just public methods (well that's what events are at the end of the day). So why are we so scared about data polling? Running thousands of loops just to know if data is present or not has indeed a given cost, but with Svelto.Tasks under 1k loops, this cost is probably negligible (0.2ms on my machine but I may optimize it in future). The number of loops can then increment noticeably if multi-threading is taken in consideration, still polling for everything is some time quite awkward.

if a game is completely made with ECS (which is the goal of Svelto), would polling for a button push event be too awkward? Indeed polling continuously for user based events is a waste. This is why *DispatchOnSet* and *DispatchOnChange* were created in the first place and they must be seen as data binding solutions for these cases, mostly for GUIs. If something cannot be solved with polling, cannot be solved with pushing too, so a good exercise is always to think: how would I solve this problem with data polling? once the answer is found, the data pushing alternative can be adopted. However the current implementation of DispatchOnSet and DispatchOnChange is not efficient as it is not cache-friendly. It may be possible to rewrite them in such a way they could be used inside EntityStructs too.

Like the sequencer, DispatchOnSet and DispatchOnChange break encapsulation too as basically they are ultimately a mean to have public functions in engines. DispatchOnSet and DispatchOnChange shouldn't probably trigger their listeners immediately, but supposedly during the next submit entity iteration. This is something I will ponder about for the next releases of Svelto, when I will decide to refactor these functionalities (feedback is meanwhile welcomed). If you wonder why I think this may be right, is because logic executed inside an engine must belong to that engine, while an immediate execution of a listener hides the fact that external code is going to run immediately, which could potentially break the execution of the engine itself.

### Indexing or not Indexing (AKA how to develop GUIs)?

If a game is completely written with the ECS paradigm, indexing entities becomes necessary. Svelto ECS allows to query entity views according entity IDs (i.e.: through the *QueryEntitiesAndIndex* and *QueryMappedEntities* functions). I often use this to manage GUIs. In the case of GUIs, the natural division of the logic from the data that ECS brings is pretty close to other GUIs patterns like MVP, MVC, MVVM and so on. The engine can be seen as the *Presenter*, while the entity view as the *Model*. The implementor becomes the *View*, as it is the Monobehaviour holding the reference to the Unity GUI instances. Usually the GUI entity, which could be as small as a label (it really depends how the user decides to design the GUI as entities. You must keep in mind that Svelto is not a GUI framework and won't solve elegantly all the GUI related problems for this reason), uses as ID the GameObject ID, so that when the user interacts through the GameObject, it will trigger the monobehaviour/implementor callback, which would dispatch to the listening engine the ID of the entity that has triggered the action. When I will refactor data binding in Svelto, I will try to improve this use case as best as possible.

### And now the time for: Various Ulterior Reasonings

#### Why *SwapEntityGroup* and *RemoveEntity* cannot happen immediately

In theory, it's to avoid to fall in the trap of creating engines that need to be aware that other engines have removed an entity or swapped an entity between groups. This kind of encapsulation breaking is easy to happen if DispatchOnSet/Change and the sequencer are currently abused. However there is a more practical reason for which I had to change this logic: since the user can iterate directly over the array of entities stored in the database, removing immediately an entity would have broken this iteration, as the array would have changed during the iteration itself. Since according the initial theory there shouldn't be any reason to really need an entity to swap or being removed immediately, this solution is most likely the simplest

#### Specialization of entities through entity views


In ECS specialization doesn't happen neither through *inheritance* nor through *object* *composition*. Instead it happens through *data composition*. More entity views an entity descriptor generates, more specialized the entity is. With Svelto the best practice is to write ** EntityViewStructs **and

**as modular and reusable as possible. Since entity views come with their engines, it means that the engines that work on modular entity views must be abstract as well, which means they must not be aware of how specialized the final entity is. Since**

*EntityStructs***comes with**

*EntityViewStructs**implementors*, the best solution is to make

*implementors*modular as well. As in our case

*implementors*are

*monobehaviours*, it would mean that instead to create big

*implementors*implementing multiple component interfaces, it's better to have a separate implementation for each interface when this makes sense. for example in the Survival Example, the

**AnimatorImplementor**is reused among several entities.

In case of ** EntityStruct**, The best practical example is always the same:

**HealthEntityStruct**is a modular entity struct that can be reused among several entity descriptors (player, enemies). Since

**do not come with their engines, it must be on us to create modular engines that can exploit this modularity as much as possible. For example,**

*EntityStructs***ApplyingDamageToTargetsEngine**, applies damage on any target, regardless if it's an enemy target or a player target.

#### Testable Engines

I am pretty sure I talked about this several times in my past articles, but since I couldn't find a dedicated paragraph about it, I want to be sure is clear: you must strive for writing testable engines. Testable engines are engines that don't use external dependencies, which should be always the case when using Svelto. Unluckily I still don't enforce the rule that component interfaces must hold only *getters* and *setter* of *Value Types* and primitives, but I will do it soon or later (sooner than later). This would avoid people from getting confused and thinking they can let getter and setter return platform object references, like **RigidBody** and **GameObject** when Unity is used. This rule leads to the creation of Implementors that wraps all the platform objects. In fact The implementation of the components must wrap the methods of these platform objects in such a way that only structs or primitives are always visible to the engine. Successively is possible to mock these objects inside the implementors to easily be able to write *unit tests*.

#### Develop faster to the creation of multiple contexts

I realised I need to refactor the example main context. First of all, bear in mind that** Svelto.Context** is not part of Svelto.ECS, like** Svelto.Tasks** isn't either. You can create your context where to initialise **EnginesRoots** wherever you want. The way I create engines and entities in the example is not wise and can easily lead to design that promote encapsulation breaking. In reality the game features should be logically divided in contexts in such a way engines and entities of that context are created separately. If contexts are properly created and engines/entities properly encapsulated, it should be possible to create them, stub data where needed and test the features to develop separately from the game itself.

For example, why a GUI should be tested in the game during its development? It would be much faster to develop it on its own, using ad-hoc data and integrate in the final game just once it's almost done.

The use of separate, independent and encapsulated contexts (with or without shared EnginesRoots) would make the creation of *functional tests* simpler too.

#### Engines and services

The service layer is still useful in an ECS world too. Although it would be possible to create engines that know directly data sources, it would not be practical to swap them if the data source needs to change. Instead it would be better if an engine wouldn't know the data source at all and query external data through a service layer. I developed a service framework, but never made it official, that proves how this concept works quite well. If the data sources change, only the implementation of the service changes, which wouldn't affect the engine code.

#### Can I use [insert any oop pattern]?

No. Anything you adopt that Svelto doesn't provide, except factories and services, is very likely going to turn in to a mess. Especially any other form of communication other than what provided is going to be a mess. Do not adapt ECS to your knowledge, instead try to fully understand how it works.

### What the future holds


The work on Svelto is not complete yet. I skip the features that I know I cannot develop without the help of other contributors, like testing Svelto on other platforms and build visual tools, so I will list what I know I will change in future when I have the time:

- I will refactor the DispatchOnSet and DispatchOnChange to make it more ECS compliant and seamless to use.
- I will add new features once c# 7 is available in Unity. Probably many ExecuteOnEntities functions may be deprecated and replaced with easier to use Enumerators
- One underestimate Svelto feature is the possibility to create multiple EnginesRoot. The creation of multiple EnginesRoot would lead to more modular, encapsulated engines. The double edged sword lies on the fact that each EnginesRoot has its own entity database. This can be cool as it can lead to interesting solutions, but at the same time would make impossible to communicate between EnginesRoots. Since I know how important is to have separate contexts, in future I want to add the concept of hierarchical EnginesRoot. Something that I still have to design properly.
- Serializations should be quite simple too. I would need to enforce (although it should be like this already) the use of primitives and serializable value types as return of entity view component interfaces too.
- With ECS, even the context should be totally configurable and possible to generate through configuration files. Not sure how interesting this feature would be, but it should work exactly how it works with IoC containers that can be configured through configuration files.

With this list I conclude this new article. Once I have time, I intend to write a new one to explain how the SOLID principles apply to ECS, but meanwhile if you are new to Svelto, these are the articles you should read to understand why the ECS paradigm is great to write better and maintainable code:

[http://www.sebaslab.com/svelto-2-7-whats-new-and-best-practices/](http://www.sebaslab.com/svelto-2-7-whats-new-and-best-practices/)(shows what's changed since 2.5)[http://www.sebaslab.com/svelto-ecs-2-5-and-allocation-0-code/](http://www.sebaslab.com/svelto-ecs-2-5-and-allocation-0-code/)(shows what's changed since 2.0)[http://www.sebaslab.com/svelto-ecs-2-0-almost-production-ready/](http://www.sebaslab.com/svelto-ecs-2-0-almost-production-ready/)(shows what's changed since 1.0)[http://www.sebaslab.com/ecs-1-0/](http://www.sebaslab.com/ecs-1-0/)[http://www.sebaslab.com/learning-svelto-ecs-by-example-the-unity-survival-example/](http://www.sebaslab.com/learning-svelto-ecs-by-example-the-unity-survival-example/)[http://www.sebaslab.com/learning-svelto-ecs-by-example-the-vanilla-example/](http://www.sebaslab.com/learning-svelto-ecs-by-example-the-vanilla-example/)[http://www.sebaslab.com/svelto-ecs-svelto-tasks-to-write-data-oriented-cache-friendly-multi-threaded-code-in-unity/](http://www.sebaslab.com/svelto-ecs-svelto-tasks-to-write-data-oriented-cache-friendly-multi-threaded-code-in-unity/)

Hello,

Just wanted to point out to a little issue with Sequencer (regardless of its other misgivings). In it current implementation it causes circular dependency with sender engines unless passed to them as weak reference – and can cause circular dependency if the same engine is used as a receiver as well as a sender – even if it is not circular sequence…

Regards,

Dawid

Hey Dawid, thank you for writing here! I am not sure I understand though, the Sequencer doesn’t hold a reference to an engine, so it doesn’t need to be a weak reference, it will be used inside the Next method but the Sequencer instance doesn’t hold on it. I think you are telling me that somehow the sequencer step is calling itself, if this is true, this should depend by how the Sequencer is configured. Can you show me some code? You are free to open an issue on github if you want.

It may be that I didn’t understood the code well – but it seem to me that in sequencer’s internal dictionary there is engine reference held to find steps it needs calling when it calls the step. (it is the calling engine I am concerned not the step implementer)

it is true that the steps in the sequencer hold instances to the engines used in the sequence itself, but I am not still sure why this bothers you. I am also not sure what you mean exactly with circular dependency. Are you worried about the garbage collection?

that’s very interesting! You use the sequencer to let engines from different engines root communicate between each other if I understand correctly. That’s an interesting use case. Did you find limiting the fact that the sequencer cannot pass data any more? I will think about your scenario, maybe the sequencer itself should hold engine instances as weak references, so you wouldn’t need to hold the sequencer itself as weak reference (if you want to destroy an engines root, the sequencer will find those engines as garbage collected and won’t continue the sequence). I will do it for the next update

Hi, Yes it is garbage collection we worry about as we use multiple root contexts in the system and will need to every so often create or remove them, and I do understand it is probably not the most common usage of the system. Still it is worth noticing that circular referencing is the case when using sequencer. In our case when we pass sequencer to an engine that needs to invoke next step we hold it as a weak reference. We also made it a internal rule that the engines (even though we want to execute them in the… Read more »

Yes without token ref the sequencer could not be used in our case at all…(without some heavy changes in the entities DB) hence we are not yet updating to latest revision. I however do not see sequencer as very bad way of handling execution order – as long as internal implementation of engines is not in it self relaying on the order or making assumptions about the state of data.

The problem about sending data in the sequencer step is related to the fact that people were using it as a data broadcaster more than a sequencer. I want to study your use case, can you show me some code that can give me a good vision?

@dawid hope you read my last message 🙂

Hi there Sebastiano 🙂 I am not able at the moment to provide you with our code, but I do not think our case would be so different from using sequencer as data broadcaster. As I mentioned we used it in the first place to replace using of event handler. Then afterwards we found it to be useful for allowing more modular entities instantiation and that is where the tokens are most heavily used. (our system has a shared code base for server and client, but entities need to have some differences – that was making traditional entity creation quite… Read more »

the Adding of entity views and implementors as required is something officially supported with the DynamicEntityDescriptor which unluckily I have broken with Svelto 2.7. Is this what you are using? I have broken the remove entity, but I will fix it asap, as we use it for Robocraft too. The way you use the Sequencer with data is correct. However since I changed the way it works, I wonder if I can find an alternative solution for your problem. Something that cannot be abused but would help your case. However it’s not clear to me if you are using it… Read more »

Hi, I,ve been looking into learning ECS and in my search, among others came across ECSrx. I have also looked into learning zenject and unirx both of wich seem to be perfectly integrated into ECSrx. From what I’ve barely grasped svelto seems to have its own dependency injection container, but im not sure if you have reactive programming or how compatible is svelto with zenject and unirx. Then again other ECSs dont seem to have anything like svelto tasks wich seems to be a huge selling point for svelto. For obvious reasons. I don’t want to turn this into a… Read more »

I have written a lot, but probably not enough, about the intrinsic issues related to the way ECS natively communicates through data polling. I never liked reactive programming, the resulting code always looked unreadable and unmaintainable to me, very close to the so called callback hell issue. I like much more the approach without callback that you can achieve with Task.net when it’s time to manage async operations. Svelto Tasks uses a similar approach, but it’s not part of Svelto ECS although you can use it with it as we do in Freejam. For event based action svelto ECS uses… Read more »

Hi, sorry it’s been a little over a month since my last post, and I’ve been kinda busy but i kinda studied on the whole ecs unirx etc… to the point where i finally feel like I can finally start experimenting with my own code (and fail miserably u_u ). but I have 2 questions: 1.- One thing I didn’t mention before is: That I was looking into making a mobile game as such it would be heavily GUI driven, you mentioned that rx was ok for that, so would unirx be a good idea here or the dispatch commands… Read more »

1) I wouldn’t still use UniRX with svelto. Reason is that all the communication must happen through entities and not in other ways.

2) yes sure!

I’ve been having more trouble understanding this than i tought, so I decided to start translating the wiki to my native spanish to try and understand this better. I was looking into the possibility of starting a blog and maybe translate your survival example too. That is if somehow i manage to understand it :P. Would that be oaky??

The problem may not be the language but just the concepts that are a bit complicated at first. The wiki pages may be a bit outdated but I try to keep them updated so you should check them again every now and then. Thanks for the help.

Hi, I have been following the svelto-ecs since ecs-1 was released. I’m still in process of understanding it completely. There’s something I’ve been trying to do but not able to achieve it in the Survival Example. In this approach how much changes (and where) will it take to have 2 (or x number of players) instead of 1, following the same or different input. I know its possible but I wanted to do it without changing much scripts. Is it possible to do it with minimal changes as in (PlayerInputEngine and MainContext)? So should I have to mock EnemySpawnerEngine and… Read more »

Hello Hariom, sorry for the late reply, but wordpress doesn’t notify me anymore when someone comments and I don’t know why. You can also join our chat on Discord in case. About your question: although I try to limit the possible combination to solve the same problem, this problem could be solved in multiple ways. However in this specific case, you may simply have more player entities. I have already written some engines that consider having more than one enemy target, but of course I didn’t test it. If you are more specific about the problem you want to solve,… Read more »

Hi here’s the code to create another player entity without much changes to the original code in MainContext var prefabsDictionary = new PrefabsDictionary(); var player1 = prefabsDictionary.Istantiate(“Player1”); var player2 = prefabsDictionary.Istantiate(“Player2”); var initializer1 = _entityFactory.BuildEntity(player1.GetInstanceID(), ECSGroups.Player, player1.GetComponents()); initializer1.Init(new HealthEntityStruct {currentHealth = 100}); var initializer2 = _entityFactory.BuildEntity(player2.GetInstanceID(), ECSGroups.Player, player2.GetComponents()); initializer2.Init(new HealthEntityStruct {currentHealth = 100}); var gun1 = player1.GetComponentInChildren(); var gun2 = player2.GetComponentInChildren(); _entityFactory.BuildEntity(gun1.gameObject.GetInstanceID(), ECSGroups.Player, new[] {gun}); _entityFactory.BuildEntity(gun2.gameObject.GetInstanceID(), ECSGroups.Player, new[] {gun}); At the starting both the players are spwaned but for some reason player2 dies and game gets over. I changed few other game engine scripts but to no avail. So I… Read more »

Hello, does this link work for you? https://discord.gg/3qAdjDb Anyway, I don’t assume that the code would work out of the box just creating to players, as I didn’t design it for it. I know I have created some engines following this scenario, but not all of them as it wasn’t needed for my purposes. I should debug it to understand what break and I am not sure I have the time now, however I may guess that all the engines that assume that there is just one player wouldn’t work and should be rewritten. I don’t think the problem is… Read more »

Yep the discord link worked. I’ll see what I can do to make the multi-player working. Will take time though as I’m still understanding.