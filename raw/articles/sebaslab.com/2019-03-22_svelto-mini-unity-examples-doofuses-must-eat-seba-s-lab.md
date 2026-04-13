---
title: 'Svelto Mini (Unity) Examples: Doofuses Must Eat - Seba''s Lab'
url: https://www.sebaslab.com/svelto-mini-examples-doofuses-must-eat/
author: Sebastiano Mandalà
published: '2019-03-22'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

*Note: this article is not maintained. The mini example Doofuses has a third and final iteration for a long time now and it is what all my new articles refer to when talking about this example. Iteration 3 enhances the code using Burst and Jobs.*

After finishing writing [my previous article](http://www.sebaslab.com/the-quest-for-maintainable-code-and-the-path-to-ecs/) on ECS, I decided that a simple centralized repository of mini-examples would be beneficial for the Svelto users. These new and updated examples are meant to introduce Svelto under a different point of view, in line with the theory I explained in my aforementioned article.

I will keep the theory and practice discussions separated, focusing on the latter through this new mini examples series, while I will improve my main theory article as result. Let’s start with the new github repository [Svelto.MiniExamples](https://github.com/sebas77/Svelto.MiniExamples):

Let’s open the First example called **Example1-DoofusesMustEat** and have a look at the folders structure. Although I tend to have several, small files, the number of files in total is not that much, plus we are usually only interested in the Engines, and that’s why I moved them in a separate folder.

If you open the right scene and run it, this is what you will see:

![](../../assets/36d6a438f84ec8a1.gif)

The red capsules, called *Doofuses*, spawn over the time (currently one per frame). Please feel free to change this spawning behaviour to experiment with different results. However Doofuses die if they are not fed and in order to feed them you need to drop some food using the left mouse button. This is not a game, but I wanted to add some logic in order to show how simple is to manage it.

Everything starts from the **CompositionRoot **as usual, called **SveltoCompositionRoot**, which is our application bootstrap. From the Composition Root is clear how the **EnginesRoot** is populated with the application **Engines**. In Svelto all the logic is always written inside Engines (which are the ECS Systems) . Best practices on how to use Composition Roots and Engines Roots will come hopefully with the next mini examples. So far this shouldn’t need any explanation though, as we are just adding the engines we need. Note also that engine dependencies injection by constructor from the composition root is a standard practice.

I assume you know the basic concepts of Svelto.ECS, but if you don’t, [you can also check the Wiki page](https://github.com/sebas77/Svelto.ECS/wiki), which needs a lot of love (* please help with it if you can!*)

Let’s have a look at the name of the Engines, the names must be chosen properly and must clearly show the intent of the programmer. However it’s also very important that the name reflects the application of the* Single Responsibility Principle*: One behaviour applied to a specific set of entities.

**PlaceFoodOnClickEngine** builds a new food entity for each click

**SpawningDoofusesEngine **builds new Doofuses every now and then

**LookingForFoodDoofusesEngine** everything that happens inside this engine is the result of a single behaviour: the doofuses looking for food (not eating it, not dying and so on)

**ConsumingFoodEngine** Doofuses entity doesn’t appear in this name because this is a semi-abstracted engine and the food itself knows how it’s going to be consumed regardless the eater

**SpawnUnityEntityOnSveltoEntityEngine **a 100% abstracted engine, in fact it doesn’t need to know which Entity generates the UnityEcsEntityStructStruct or any specific group to use

**RenderingDataSynchronizationEngine** is a semi-abstracted engine needed to let Svelto communicate with UnityECS.

**VelocityToPositionDoofusesEngine **and **DieOfHungerDoofusesEngine** I guess they are self explanatory, which is the point of giving good names to engines!

This example shows the simplest way to use Svelto.ECS, in fact with pure ECS and no implementors involved, Svelto is actually much nicer and faster to use. Implementors is something I will explain with the next articles, their use is necessary only if you need (not want, but need) mix OOP based libraries or platforms with Svelto.ECS. The reason why I don’t need to use implementors for this demo is that I am exploiting the UnityECS current features, therefore I don’t need to use *Gameobjects *and *Monobehaviours *to render the simple meshes.

Talking about UnityECS, let’s remember that the motive for Svelto.ECS to exist is different and only partially overlap with UnityECS raison d’etre. I abundantly talked about the topic in my past articles, no need to repeat myself. However This demo has also the nice goal to demonstrate how Svelto.ECS can be integrated with UnityECS, so that you can have the best of the two worlds. *Using UnityECS as black boxed, low level ECS framework, doesn’t feel clunky at all.*

Let’s dive in the details now:

First: Svelto.ECS doesn’t have a way to manage updates/loops. You will notice, over the time, that in order to keep Svelto lightweight and force myself to not over engineer it, I often leave to the user the flexibility to choose how to achieve given results, although limited by the framework guidelines. In the case of the loops you can choose whatever you please, including Unity Jobs if you find a way to use them. Of course the best companion of Svelto.ECS for this is [Svelto.Tasks](https://github.com/sebas77/Svelto.Tasks)

I will talk more about Svelto.Tasks in the next iterations of this example, but for now let’s stick to the basics, which I don’t need to explain as they are quite self explanatory in code: a loop in Svelto.Tasks is always a *IEnumerator *in whatever form it can come. The *while (true)* pattern is pretty common, but you must not forget to *yield *the frame at least once otherwise the loop will enter in an infinite loop. If you know how coroutines work, this shouldn’t surprise you.

There are two spawner engines in this example. Spawner engines are exactly like any other engine, but they are meant to spawn entities, so let’s see how Svelto defines an entity. Svelto model to store entities is different than the UnityECS one (that uses archetypes) and other implementations, but for the time being is enough for you to know that something similar to the UnityECS archetype is what in Svelto is called **EntityDescriptor**.

The Entity Descriptor defines what **EntityStruct** (entity components) the entity generates. Entity Structs surely push toward modular and reusable components. As explained in my theory article, in order to compose more or less abstracted pre-existing behaviours, it will be enough to compose entity descriptors with pre-existing modular entity structs (thus an entity descriptor usually generates several entity structs).

This is how I normally start to write my code with Svelto.

- What entities is this behaviour affecting?
- What is the behaviour that must be applied to these entities?
- Let’s decide the name of the engine.
- Write the initial engine infrastructure and code until I need to manage entities
- Is the entity already existing? If not write the Entity Descriptor (if it’s not existing probably you are building it anyway at this point)
- Query and iterate over entity structs OR
- Build the entity. I usually make the Entity Descriptor generate just one Entity Struct as I decide what other entity structs are needed while I write new engines. However in this case I knew already I was going to need to know the entities position, hence the
**PositionEntityStruct**was the first Entity Struct generated by the*food*entities. I knew also I needed an Entity Struct to hold the unityECS information, however I didn’t know beforehand that I was going to need a**MealEntityStruct**that came later, while I was designing the game. The final EntityDescriptor for food looks like:

```
public class FoodEntityDescriptor
: GenericEntityDescriptor<PositionEntityStruct, UnityECSEntityStruct, MealEntityStruct>
{}
```


Which is then used to build the Entity

`var init = _entityFactory.BuildEntity<FoodEntityDescriptor>(_foodPlaced++, GameGroups.FOOD);`


Groups are fundamental in Svelto. They can be reinterpreted in several ways, thus used for multiple goals. You must always explicitly choose which group your entity will be built in. Later you can remove it or move it to another group. Groups have crucial properties that we will discover over the time, but now it is important to understand that groups give you the tools to manage entities. Depending how you use groups and what entities you will put inside, you will be able to achieve different results.

Entity Structs can also have default values and they are set through the **EntityInitializer **returned by the function:

```
init.Init(new MealEntityStruct(10000));
init.Init(new PositionEntityStruct
{
position = new ECSVector3(position.x, position.y, position.z)
});
init.Init(new UnityECSEntityStruct
{
uecsEntity = _food,
spawnPosition = new ECSVector3(position.x, position.y, position.z),
unityComponent = ComponentType.ReadWrite<UnityECSFoodGroup>()
});
```


*Entities are usually not built, removed or swapped immediately, but only at the next scheduled submission.*

An engine is not supposed to know how many entities it needs to handle. *You must always be sure that an engine will work with 0,1 or N entities*, for this reason the usual pattern is to iterate over the entities in a specific group, regardless the number of entities in the group.

For maximum performance, Svelto allows you to iterate directly the array used to store the entities inside the Svelto database:

```
var doofuses =
entitiesDB.QueryEntities<PositionEntityStruct, VelocityEntityStruct, HungerEntityStruct>(
GameGroups.DOOFUSES, out var count);
var foods =
entitiesDB.QueryEntities<PositionEntityStruct, MealEntityStruct>(GameGroups.FOOD, out var foodcount);
```


Here the important parts:

- You actually query the components of an entity.
- Each component is stored in a different array. In this case a tuple with different arrays will be returned
- You can query multiple components,
*but it’s up to the way you organize the groups that is guaranteed that the components indexed with the same index are generated by the same entity*. The rule is simple:, which simply means that when you do*as long as all the entities in the group generate the same subset of components that you are querying, then you are guaranteed that entity structs of the same entity share the same array index***doofuses.item1[i]**and**doofuses.item2[i]**they refer to the relative entity structs generated by the same entity.*The entities inside a group don’t need to be generated by the same entity descriptor, but the entity descriptors need to have in common the components you are querying.*

The **RenderingDataSynchronizationEngine **and the **VelocityToPositionEngine** were initially supposed to be abstracted engines. I decided then to directly iterate the Doofuses group for the sake of this example. As explained in the “theory” article, abstract engine are not supposed to know the specialization of the entities they are iterating on. In Svelto it means that they are not supposed to know the groups to use either.

As mentioned, groups are very powerful, but they pushes toward engines specialization. This in practice is not a problem, because hardly you will need to create framework level engines that can be reused for other games. *Early abstraction is absolutely evil in ECS. Never design engines for anything else than what you need right now*. If the SRP principle is correctly applied, these engines will be either substituted/supported by new ones or easily refactored if specifications change.

However in the rare case you will need to write a purely abstracted engine, there could be several solutions, but what I would suggest now is to pass by constructor the array of the known groups to iterate. I hope and I should be able to talk much more about groups in future.

*About Unity ECS*: My theory is that I can use UnityECS as a black boxed low level library, hence I can create only Unity ECS entities with the minimal set of components just to enable the standard unity systems to work. However since UnityECS doesn’t have the concept of groups, in order to be sure that I was iterating only doofuses, I had to create special unity ecs “flag” components to be sure I would synch the right entities. I think using and being forced to use components as flags, that you can remove and add in run-time, is terrible and it can potentially lead to unmaintainable code. The code design reason is that the concept of entity will be diminished and as we know, once the important conceptual role of the entity disappears, nothing will stop you from start using ECS as procedural code with globally accessible data. Being able to add and remove components in run-time would give too much flexibility (imagine if you decide to make every single entity state a component that you can attach and remove in run-time, argh!)

In every case, I would love to know how I could improve the UnityECS code. In order to keep it simple, I didn’t make the **RenderingDataSynchronizationEngine **a **ComponentSystem**, but I could have done it and this probably would have saved the copy of the entities. It’s something I may improve with the next iterations. Right now I am thinking about three iterations for this example:

- optimize it with Burst
- optimized it with Svelto.Tasks multithreading capacity
- using compute buffers instead of UnityECS to render the meshes, using the (not free) plugin GPU instancer.

Then I will move to the next examples which will be: updating the zombie survival example and move to this repository and a GUI made with Svelto.ECS.

As usual your feedback is appreciated.

## Iteration 2: Burst it

All right, with iteration 1 I showed how UnityECS can be integrated with Svelto.ECS. I am sure I can optimize the relative code, but I prefer to show you now something more exciting: how to use **Burst **with Svelto.ECS. Of course there is nothing special about it except for the fact that Burst officially cannot be used outside the job system yet. However I do not want to use the job system and not using Burst just for this reason would be silly.

Let’s dig in to it: Open now the project **Example1B-DoofusesMustEatBurst** and open the scene **CombiningBehaviours**.

*I changed the code in such a way the 10.000 doofuses spawn at once and they never die. Food can be now be placed only once, but 100 sphere will be created*

Running the code under this scenario shows an awkward situation, the code to look for the food now executes 10.000×100 iterations, a bit too much for poor c# alone.

The new **LookingForFoodDoofusesEngine** now takes much longer!

![](../../assets/e7367e60041e97e6.png)

![](../../assets/93c8cdda7f2ead9b.png)

![](../../assets/a8d9a5605c6bd042.png)

Right on! this is actually what I was looking for, I wanted the main thread to perish, so that I can show you the power of Burst!

Let’s enable it using the Define **UNITY_BURST_FEATURE_FUNCPTR **and compile and run it again, well the result speak for itself right?

*From 50ms, down to 5-7ms!!* Amazing isn’t it? OK Before to complete this new explanation, keep it mind that I am hacking Burst here to make it work outside the Job System. This is a feature that is planned, but not available yet, but I was tired to wait so I messed with the code a bit.

Enabling deep profile will also prove that I am not mad:

![](../../assets/1317c2e487f3f7cf.png)

However this is just because I didn’t want to use the Unity Job System, you can though! The reason why I didn’t will be explained in the next iteration.

I have been following your ECS articles and wonder how to implement the following (2D game): if an explosion goes off at x, y coords, you would need engines to get everything within a certain radius, apply damage, apply animation changes to damaged entities, push entities back from the point of explosion. This would involve multiple engines, how would each engine know the exact entities to process? and also how would you control the engines so that they would run in that specific order? Thanks for all the hard work and thought that you put into your libraries! You are… Read more »

as I wrote in this article, do not early abstract. Abstraction comes on its own over small iterations when needed. For example, if you know that only certain entities are affected by the explosion, iterate only over these entities and if they are inside the radius, change directly their velocity. Over the time you may want to not give the responsibility to apply the velocity directly from this engine, so at this point you can choose if to move the entity to another group or if use a flag to test (which I never do), in both cases delegating the… Read more »

I have a follow up question. If we use CheckHitByExplosionEngine to move all affected entities into group EntityHitByExplosion, will the subsequent engines such as AddExplosiveForceEngine be able to see the group changes immediately, or next loop iteration (thus a delay and even further delay after the last of engines MoveBackToOriginalGroupEngine done his job, the entity behaves back to normal)

All the engines iterating the entity hit by explosion group will find the same entities on the same frame. In unity atm all the entity operations are executed at the end of the frame. If the engines can apply operations that don’t need order like modifying velocity then the operations can run together on the same frame regardless the order. However this is a bit simplicist, it’s not taking in consideration multi threading and the fact that you can also create your own submission scheduler and decide when you want to submit the entities, but I never needed to care… Read more »