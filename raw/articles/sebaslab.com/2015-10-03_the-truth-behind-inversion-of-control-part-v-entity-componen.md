---
title: The truth behind Inversion of Control – Part V – Entity Component System design
  to achieve true Inversion of Flow Control - Seba's Lab
url: https://www.sebaslab.com/entity-component-system-design-to-achieve-true-inversion-of-flow-control/
author: Sebastiano Mandalà
published: '2015-10-03'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

This is the final article on my long dissertation about my understanding of Inversion of Control. I hope it helped the reader to understand it better too. This article draws my final conclusions and assumes that all the previous articles in the series are read. It also gives new insights that will be investigated further with the recent articles that I have linked at the end of this post.

At this point in this series, I can imagine someone wondering if I still recommend using an **IoC container**. IoC containers are handy and powerful, but they are dangerous because they are too flexible. If used without Inversion of Control in mind they can lead to messy code; when used with IoC in mind they become less useful. Let me refresh the reasons why I believe:

## You shouldn’t use an IoC container to develop games

When an IoC container is used with a standard procedural approach, thus without inversion of control in mind, dependencies are injected in order to be used directly by the specialised classes. Without inversion of control, there is no limit to the number of dependencies that can be injected. Therefore it doesn’t come naturally to apply the *Single Responsibility Principle*. Why should I split the class I am currently working on? It’s just an extra dependency injected and a few lines of code more, what harm can it do? Or also: should I inject this new dependency just to check its state inside my class? It seems the simplest thing to do, otherwise, I would need to spend time refactoring my classes…Similar reasonings, plus the proverbial coder laziness, usually result in very awkward code. I have seen classes with more dependencies injected than common sense suggest, without raising any sort of doubt about the legitimacy of such a shame.

Coders need constraints and IoC containers unluckily don’t give any. In this sense, using an IoC container is actually worse than using manual injection, because manual injection would be limiting the problem due to the effort to pass so many parameters by constructors or setters. Without rules, dependencies end up being injected as sort of unscoped global variables. Binding an implementation to a single instance becomes much more common than binding an interface.

One way to limit this problem is to use multiple *Composition Roots* according to the application contexts. In this way it would be possible to isolate classes and specify their scope, reflecting the internal layering of the application. An observer wouldn’t be injectable everywhere, but only by the classes inside the object graph of the specific container. In this sense, hierarchical containers could be quite handy.

The following example is a classic class that doesn’t have a precise context or responsibility. It very likely started with simple functionality in mind. Over time it became a sort of “Utility” class, with no limits to the number of public functions it can have and, consequentially, with no limits to the number of dependencies it can have injected. “Look this class has already all the information we need to add this functionality” … “ok let’s add it” … “oh wait, this function actually needs this other dependency to work, all right then, let’s add this new dependency”. This example is the worst of the lot, unluckily pretty common when the concept of Inversion of Control is unknown or not clear.

My definition of a “Utility” class is simple: every class that exposes many public functions ends up being a Utility class, used in several places. *Utility classes should be static and stateless. Stateful Utility classes are always a design error.*

The following class uses Injection without * Inversion of flow Control* in mind. It’s a utility class (the dependencies are actually copied from a class of a real project) and exposes way too many public functions. Public functions reflect the class “responsibilities”, thus this class has way too many responsibilities. You can also notice how some dependencies are injected as a global instance, it’s obvious that, for example,

**HealthStatus**shouldn’t be used directly from a specialised object.

public sealed class DoingSomethingBad { [Inject] public ISimulationFactory simFactory { private get; set; } [Inject] public ICatalog typeInventory { private get; set; } [Inject] public IMonoBehaviourFactory monoBehaviourFactory { private get; set; } [Inject] public IMachineMap playerMap { private get; set; } [Inject] public PlayerBuiltListener playerBuilt { private get; set; } [Inject] public WeaponFireManagerFactory weaponFireManagerFactory{ private get; set; } [Inject] public ratingData rating { private get; set; } [Inject] public HealthStatus health { private get; set; } [Inject] public HealthStatusContainer healthStatusContainer { private get; set; } [Inject] public PlayerMachinesContainer playerMachinesContainer { private get; set; } [Inject] public LobbyGameStartPresenter lobbyGameStart { private get; set; } [Inject] public GroundHeight groundHeight { private get; set; } [Inject] public GameObjectPool pool { private get; set; } public void FunctionWithResponsability1() { //... } public void FunctionWithResponsability2() { //... } public void FunctionWithResponsability3() { //... } public void FunctionWithResponsability4() { //... } public void FunctionWithResponsability5() { //... } public void FunctionWithResponsability6() { //... } }

## How to achieve Inversion of Flow Control

Using events is a way to achieve inversion of flow control. The specialised objects react to events fired from the high-level module classes. Injecting high-level mechanism classes to listen to their events is an alternative to registering the specialised object into a high-level mechanism. Events can be OK when they are fired by High-level module mechanisms.

However, I found the **Strategy Pattern** to be a great companion. I previously discussed how to use it in my article on the [Dependency Inversion Principle](https://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/), but I believe that a different interpretation of it can be a step forward for achieving true inversion of flow control.

The Strategy Pattern is a common pattern used by frameworks to take control of the application code execution, however, the way it’s implemented by game frameworks is slightly different from what we used to read in the design pattern books. Once the strategy interface is provided by the framework layer, the user is expected to implement it and register the implementation with the framework managers.

As usual, I can take the example of entities that need to be rendered or need to be physically simulated. The framework provides the **IRenderable **and **IPhysicallySimulated **interfaces that can be implemented to let any entity being rendered or physically simulated.

Similarly, any common behaviour that can be abstracted can be moved to a higher level module which provides also the interface to be implemented for the behaviour to be applied.

This kind of pattern is always the same: A High-Level policy system iterates the entity registered with it according to its responsibility.

The **RenderableSystem **will iterate all the **IRenderable **entities and render them

The **PhysicSystem **will iterate all the **IPhysicallySimulated **entities and render them

The **HealthSystem **will iterate all the **IHaveHealth **entities and affect their health when necessary

This pattern doesn’t need an IoC container to work and doesn’t need dependencies injected but only entities registered. It follows the DIP, OCP and Single Responsibility principles.

*The take-home message here is that IoC and DIP are asking us to step away from the Bilas/Unity Gameobject approach that tells us to write behaviours in our specialised components but instead asks us to find the common behaviours of our entities, abstract and pack them in higher-level modules, make our specialised entities implement the high-level interfaces and eventually register them in the high-level managers to be later on processed by the framework.* This is almost a shift of paradigm compared to what game coders are used to.

## A real Entity Component System

All that said, I realised that a proper ECS implementation was what I was looking for a natural evolution of the strategy pattern illustrated so far.

In order to prove that an ECS solution could be viable, I wrote a new ECS C# framework following these reasonings. The framework and the example can be found at [https://github.com/sebas77/Svelto-ECS](https://github.com/sebas77/Svelto-ECS).

This explains why my ECS framework isn’t designed solely around the performance-first idea, but also to create a framework able to push the user to write High Cohesive, Low Coupled code[1] with all the SOLID principles in mind.

There are some patterns that emerge when writing an ECS-centric application:

*All the logic must always be written inside Systems.*Systems model behaviours that can be applied to entities.*Entities are not objects, they just aggregate Components*(which is equivalent to implementing high-level interfaces)*Components don’t hold logic, they are just data wrappers.**Components can’t have methods, only get and set properties.**Systems do not hold or cache entitites/components data or state. They can hold system states*.*Each System has one responsibility only.**Systems cannot be injected*.*Systems communicate with each other through components.**Systems can have injected dependencies, but this would mean mixing ECS with OOP.**Systems do not know each other.**Systems must be packed in different modules according to their level of abstraction.*

I will expand on how ECS helps follow the SOLID principles in my next articles.

**Putting all together**

ECS can be more effective than OOP to push the coder to write highly cohesive, low-coupled codebases implementing Policymaker Systems that follow the SOLID principles and are packed in High-Level modules. The Dependency Inversion Principle comes naturally as it’s implicit with the new inverted way to let Systems apply behaviours to our entities. Contrary to what we find with Strategy Patterns in OOP, our implemented entities are only data holders. Their behaviours are composed through components and specialised entities with multiple behaviours are implemented through composition instead than inheritance.

[1] [HIGH COHESION, LOOSE COUPLING](https://web.archive.org/web/20210226040352/https://thebojan.ninja/2015/04/08/cohesion-coupling/)

I strongly suggest to read all my articles on the topic:

[http://www.sebaslab.com/ioc-container-for-unity3d-part-1/](http://www.sebaslab.com/ioc-container-for-unity3d-part-1/)[http://www.sebaslab.com/ioc-container-for-unity3d-part-2/](http://www.sebaslab.com/ioc-container-for-unity3d-part-2/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-i-dependency-injection/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-i-dependency-injection/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-ii-inversion-of-control/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-ii-inversion-of-control/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/)[http://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/](http://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/)

The fun doesn’t end here, the evolution of my thoughts continues with these articles:

Interesting read. This sounds a bit like RobotArms, though I don’t understand either confidently enough to say for sure https://bitbucket.org/dkoontz/robotarms

That’s a nice set of tutorials. Explained really nice.

I see how it’s possible to make APIs better and reduce boilerplate code. Have a look at EgoCS. It’s using generics to get entities with right components.

Are you planning to support and update Svelto-ECS?

I didn’t know EgoCS, thanks for pointing it out. Svelto-ECS is currently just a proof of concept, but we have started to use it internally, so I guess I will update in future, but not soon.

How can I dinamically change Nodes of a Entity in Svelto? Think to the following problem => I need to track a map with many Enemy entities, however only entities that are near player needs to be visualized. A Enemy entity will have EnemyAI node exposed if we are going to update its logic, but we will add a EnemyRender node only if the enemy is near enough to be visualized. Currently in SveltoECS I have to add a new Entity which holds Rendering stuff and have it to be “linked” to the EnemyAI’s node so they share the same… Read more »

I guess you could separate the logic from the rendering with SVELTO.ECS. This is actually a designer’s choice.

It strongly depends on the kind of title you are developing. Actually I don’t think Svelto takes care of the rendering pipeline, but GameObjects monobehaviors with their render component do.

The fact you HAVE TO add a monobehaviour bridge interface onto gameobject prefabs needed for the game, gives you the freedom to do so, by eventually disable or not disable a renderer when the logic requires it.

Thanks for your reply I solved the problem now. The rendering part (sprite in case of SpriteRenderer) and mesh buffer in case of (MeshRenderer) can just be disabled with a flag, and the sprite/buffer can be setted to “null” until it come nearby enough to camera. Until now this is the simplest solution and extra memory for “invisible” game objects has not been a problem so far.