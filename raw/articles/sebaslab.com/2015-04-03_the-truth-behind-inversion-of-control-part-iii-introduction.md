---
title: The truth behind Inversion of Control – Part III – Introduction to Entity Component
  System Design - Seba's Lab
url: https://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/
author: Sebastiano Mandalà
published: '2015-04-03'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

In this article, I will explain the previously introduced* Inversion of Flow control*, then I will illustrate how to apply it in OOP and how this can be best achieved using the *Entity Component System design. *

While ECS design apparently seems to have nothing to do with Inversion Of Control, I found it to be one of the best ways to apply the principle.

*Note: In hindsight, I introduced the concepts explained in this article too early in the series, but fortunately, this is just a light introduction that will be then reviewed in the last article of the series.*

## We all use Inversion of Flow control already

Once upon a time, there was the concept of a game engine. A game engine was a game-specialized framework that was supposed to run whatever game. This game engine used to have some common classes, designed as sort of “managers”, that were found more or less in all the game engines, like the *Render* class. Every time a new object with a *Renderer* was created, the *Renderer* component of the object was added to a list of *Renderers* managed by the *Render* class. This was also true for other components like the *Collision* component, the *Culling* component and so on. The Engine dictates when to execute the culling, when to execute the collision detection and when to execute the rendering. The less abstracted (more specialised) objects don’t know when they will be rendered or culled, they assume only that at a given point this will happen.

Without even realising it, the game engine was taking control over the flow of the game application, resulting in the first form of *Inversion of Flow Control. There is no difference between* what I just explained and what the Unity engine does. Unity decides when is time to call **Awake**, **Start**, **Update and so on. **

Unity framework is capable of achieving both *Inversion of Creation Control* and *Inversion of Flow Control*. *MonoBehaviour *instances cannot be directly created by the users; regardless if they are already present in the scene or they are created dynamically, it’s Unity to create them for us. The Inversion of Flow control is instead achieved through the adoption of the [Strategy Pattern](https://en.wikipedia.org/wiki/Strategy_pattern). Our *MonoBehaviour* classes must implement a specific interface (through the Awake, Start, Update and similar functions) in order to be usable by the Unity framework “managers”.

In general, then Inversion of Flow Control is achieved in OOP by letting the High-Level Modules classes manage the flow of the Low-Level Modules objects. The user loses control over how the objects are processed and delegates them to the generic frameworks.

## How to better achieve inversion of Flow control with ECS

*Note: this is just an introduction to an argument that I will expand over and over in my next articles.*

While the Unity **GameObject **system replicates the template introduced by *Bilas *in 2002 with the presentation *A Data-Driven Game Object System*** [0]**, a more advanced way of managing entities has been introduced in 2007 with the modern definition of the

*Entity Component System*:

*“In 2007, the team working on Operation Flashpoint: Dragon Rising experimented with ECS designs, including ones inspired by Bilas/Dungeon Siege, and Adam Martin later wrote a detailed account of ECS design*


[1]*,*

*including definitions of core terminology and concepts. In particular, Martin’s work popularized the ideas of “Systems” as a first-class element, “Entities as ID’s”, “Components as raw Data”, and “Code stored in Systems, not in Components or Entities”.*

ECS Design uses Inversion of Flow control in its purer form. ECS is also a magnificent way to possibly never break the *Open/Close principle* when is time to add new behaviours.

the Open/Closed principle, which is also part of the S**O**LID principles, says:

“*software entities (classes, modules, functions, etc.) should be open for extension, but closed for modification*“

OCP is the holy grail of the perfect code design. If well adopted, it should never be needed to go back to previously created classes to change the code in order to add new behaviours.

The ECS design works in this way:

**Entities**are essentially IDs.**Components**are units of data. Components wrap data that can be shared between Systems. Components do not have any logic to manage the data.**Systems**are the classes where all the logic lies. Systems can access directly to the lists of components and execute all the logic the project needs.

I understand that the concept of data component could sound weird at first. I had problems wrapping my head around it initially as well. I guess that the key that cleared my doubts was to understand that there isn’t such a thing as a **System ***being too small*.

The really powerful aspect of this design is that the Systems must follow the Single Responsibility Rule. All the behaviours of our in-game entities are modelled inside Systems and every single behaviour will have a single, well-defined in terms of domain, System to manage it.

This is how we can apply the **Open/Close principle **without ever breaking it: every time we need to introduce a new specific behaviour, we must create a new System that simply uses components as data to apply it.

Systems are implicitly mediators as well, this is why Systems are great to let Entities communicate with each other and with other Systems (through the use of the Components). However Systems are not always able to cope with all the possible communication problems just through the use of Components and for this reason Systems, that should be instantiated in the Composition Root, can have injected other dependencies (I’ll give more practical examples in the next articles).

Systems model all the logic, both for the framework-level AND game-level layers. When ECS design is used, there won’t be any implementation difference between the framework logic (like *RenderingSystem*, *PhysicSystem *and so on) and the game logic (like *AliensAISystem*, *EnemyCollisionSystem *and so on), but there will be still a sharp difference in the code separation. Framework and Game systems will still lie in different layers of the application (different modules). This introduces another fundamental concept: the design of our game application through multiple layers of abstraction. Using just two layers of abstraction is not enough for a complex game. The Framework layer and Game layer alone are not enough. We need to make our Game layering more granular.

All that said, I noticed that there is some confusion when it’s time to define the design adopted by Unity. Although its “managers” can be considered “systems”, they are not according to the modern definition, since they cannot be added or extended by the programmer.

Of course, when it is not possible to add new behaviours by adding new “Systems”, the only way to extend the logic of our entities is to add logic inside Components. This is anyway a step forward from the classic OOP techniques. Component Oriented (I call them Entity Component, without System) frameworks like the one in Unity, push the coder to favour Composition over Inheritance, which is undoubtedly a better practice.

All the logic in Unity should be written inside focused MonoBehaviour. Every MonoBehaviour should have just one functionality or responsibility, and they shouldn’t operate outside the GameObject itself. They should be written with modularity in mind, in such a way they can be reused independently on several GameObjects. Monobehaviours also hold data and their design clearly follows the basic concepts of OOP.

Modern design tends instead to separate data from logic. As Data, Views and Logic are separated when the Model View Controller pattern is implemented, the same happens with ECS design through Components and Systems in order to achieve better code modularity.

Before finally showing the benefits of the ECS design approach with real code, I will explain the concept of the Dependency Inversion Principle in the [next article](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/) of this series, which will add more information about what Inversion of Flow control is.

I strongly suggest to read all my articles on the topic:

[http://www.sebaslab.com/ioc-container-for-unity3d-part-1/](http://www.sebaslab.com/ioc-container-for-unity3d-part-1/)[http://www.sebaslab.com/ioc-container-for-unity3d-part-2/](http://www.sebaslab.com/ioc-container-for-unity3d-part-2/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-i-dependency-injection/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-i-dependency-injection/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-ii-inversion-of-control/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-ii-inversion-of-control/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/)[http://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/](http://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/)

Good train of thought here. Thanks for sharing.

I am enjoying a lot reading your series of articles. This way of thinking transforms a lot the way to build a game with Unity and write code in C# compared to my usual habits.

OCP, DIP, solid principles and Inversion of Flow all together in an entity system. You have done an astounding work with you ECS, really.

Several years later and Unity now has its own ECS architecture that it exposes to the user. Of course I’ve seen (well, only read about) how your library abstracts that away, but even if just sticking to using Unity’s ECS architecture I think the game architecture that devs create will begin to become much cleaner. These have been very informative articles so far, even years later. I’ve been battling with this idea of no composition root and no easy way to do DI or have IOC within Unity. It’s been really frustrating as I’m an experienced engineer but newer to… Read more »

Great article. I would correct a small part of it though. The MonoBehaviour in Unity is closer to the Template Method pattern than the Strategy pattern. These two patterns are very similar to each other but it’s their intention that put them apart. The Template Method pattern is for when we want to control the execution order of the code which is exactly what Unity wants to do. Another clue is that in Strategy, the class implements an interface but in Template Method, the class inherits a base class.

IMO the Monobehaviour pattern is closer to the strategy pattern. Although it works by extending the monobehaviour class (which makes it look similar to the template pattern), the template pattern needs to have a

DoAlgorithm()method in the template itself. Unity systems instead call the various methods (Awake,Startsand so on) independently, from different places. The monobehaviour then implements several strategies.thank you, I will take this into consideration once I start to review all my old articles!