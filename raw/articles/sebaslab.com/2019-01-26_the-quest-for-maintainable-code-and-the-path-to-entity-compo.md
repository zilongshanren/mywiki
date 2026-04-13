---
title: The Quest for Maintainable Code and The Path to Entity Component System design
  - Seba's Lab
url: https://www.sebaslab.com/the-quest-for-maintainable-code-and-the-path-to-ecs/
author: Sebastiano Mandalà
published: '2019-01-26'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

## Premise

In this article, I am going to explain why I believe the Entity Component System design is a great paradigm to develop simpler to maintain (and therefore less expensive) codebases and also explore the idea to formalise best practices through the application of the *SOLID principles*, which, at glance, look not compatible with the *ECS design* (although I am not the only one who thinks they could be[1]).

This article continues the train of thought of [my previous ones](http://www.sebaslab.com/?page_id=2098) and expands them through the elaboration of the feedback that I gathered in the last years from [my team](https://freejamgames.com/#about), developing two commercial products, and the [Svelto Community](https://discord.gg/3qAdjDb). If you are only curious about the application of the SOLID principles to ECS, skip directly to the second part of this article.

## Audience

This article is targeted at people who already know the [Entity Component System design,](http://t-machine.org/index.php/2007/09/03/entity-systems-are-the-future-of-mmog-development-part-1/) and want to explore the benefits of adopting this paradigm beyond the sole performance implication of writing Data Oriented code. It is likewise targeted at people who are interested in exploring alternative approaches to Object Oriented Design to develop maintainable code.

## What *maintainable code* means to me

I define maintainable code as code that is easy to read, extend and refactor. It often belongs to a codebase that is in continuous evolution and never stops mutating. This kind of codebase is found in products like games as services that continue serving players for several years. As these products must evolve to continue appealing to the player base, the code itself keeps on changing through countless iterations. I personally can vouch that in this kind of environment coding guidelines and code reviews alone are not enough to guarantee that the code won’t implode over time, resulting in an expensive pile of technical debt hard to manage.

Historically, game development companies use(d) to underestimate the actual cost of maintaining code, focusing only on the cost to develop it. However, it’s now common knowledge that maintaining code is usually more expensive than writing it (this is even more true for games as a service) and that’s why is so important to write good code to start with. Never fall into the mistake to write “prototypal” code without rewriting it properly before using it in production. As Alan Kay said, *quick prototyping is not nearly as important as maintainability [2]*. All that said, I hope people realise that the

*rewriting*part itself involves a cost, so why don’t we write it as well as possible the first time? It’s common to think that writing efficient code, without proving its usefulness, is a high upfront investment although this is true only if coders are forced to think about how to design the code due to the lack of use of productive frameworks, rather than focusing only on implementing it.

### Good coders are lazy coders

Experienced coders get lazy and a lazy programmer will strive to find the simplest way to solve a specific problem. An experienced lazy programmer will also know how to make this code efficient with minimum effort. However, one thing that a lazy coder might not do, is thinking about the consequences of the decisions taken. As it is important to get things done as soon as possible is simple to forget the long-term implications on codebase maintainability.

When it gets too complex to predict these consequences, coders could fall into two traps: early abstract (read over-engineer) their code to try to be prepared for all the possible outcomes or just not caring at all, until when it’s probably too late and changing direction would be so expensive that ineffective compromises must be taken.

These are the reasons why I believe that coders would be better off using *rigid frameworks*. Some people are confused by the way I use the adjective rigid with framework. By *rigid *I mean that the framework (or even a programming language) must provide one or just a few ways to solve a specific problem. I use rigid as a synonym of strict, as “incapable of compromise”, as it must not bend, adapt or “compromise” to the user’s current understandings and assumptions.

In this sense, saying to a coder to develop a game with a multi-paradigm language like it can be C++ or C#, would result in a melting-pot of solutions adopted all over the codebase. Knowing also that the programmers are famous for copying and pasting already working code, it’s not hard to imagine what the ramifications of not giving rigid directions could be.

## In search of the root of the problem

All my reasoning started a long time ago when I realised that, while I was happy with the solutions I used to develop, I wasn’t able to reuse them as I wasn’t able to identify the shared patterns among these problems. I was reinventing the wheel every time, which is a common problem in the industry. To be clear, I am not talking about patterns to implement algorithms, I am talking about how to write code in order to be easy to read, expand and refactor.

*I eventually concluded that code design problems, in Object Oriented Programming, always orbit around inter-object communications.* Whenever object communication is made through events, messages, mediators or other ways, it always needs somehow to be aware of the object to communicate with. Object communication, in my opinion, is the cause of every spaghetti code out there. All the forms of abstraction and relative good practices to uncouple code aim eventually to control inter-object communication.

In C++ any form of inter-object communication eventually ends up with the direct use of object methods, so I started to wonder, is **Encapsulation **part of the problem?

## Encapsulation, what is it about?

In **Object Oriented Programming,** data encapsulation works well for **Abstract Data Types**. You create your data structure, you provide public functions to manage this data structure. Encapsulation works well to hide complexity. This is what OOP was created for. You can “black box” the complexity of a class, without the need to know what this class does.* *This is what pushes, at a given point, a procedural programmer to switch to OOP.

However, Encapsulation doesn’t prevent the object to be used in the wrong way. If it was possible to write an application without any form of inter-object communication, we would be able to develop perfectly encapsulated entities. If we also design the classes to solve just one single problem, then we would have the perfect scenario for a maintainable codebase. The codebase would be lean, modular and totally uncoupled.

In real life, this scenario is unrealistic as it’s unlikely that a useful application would work without communication and, as result, the beautifully encapsulated code will possibly turn into a spaghetti one due to the coupling needed for objects to communicate.

But is Encapsulation involved in this problem at all?

Using an interesting analogy, Encapsulation enables us to build a perfectly functional car, but cannot prevent a driver to destroy it. The OOP cannot prevent perfectly encapsulated objects to be used in the wrong way. *Brakes() *and *Accelerates()* can exists, but encapsulation alone cannot keep the user from using *Accelerates() *instead of *Brakes()*. A more trivial example to prove the point is that a class can implement* First() *and* Second()*, but nothing stops the user from calling* Second()* before *First()*. Users cannot work with conventions but need to work with framework-dictated rules.

Encapsulation is a concept born from the necessity to limit the scope of accessible states, but public methods can mutate these states. Public methods of well-written classes must be able to *prevent* invalid states from being set (and that’s why state machines are often seen as a panacea). The problem is not about data encapsulation anymore*,** but about object control and ownership.*

### Object ownership

The logic inside the public methods is meant to control the object states, but can objects really control these states when the public functions can be used from everywhere in the code? How can an object prevent an entity to switch to a perfectly valid state at unexpected times if the use of public functions is indiscriminate?

While the unwanted consequences of this misuse are clear in a concurrent and multi-threaded scenario, they are fundamentally important to understand for the writing of maintainable code too.

All the code design theories orbit around the problem of preventing the reckless use of public methods. Let’s think again about Singletons. Singletons are globally accessible objects with private states, that can be mutated through public functions.

Without even needing to give you examples, how many times did you have to debug the states of a Singleton because they unexpectedly changed? Similarly to singletons, overzealous *Dependency Injection* is what leads to highly coupled code that is hard to maintain. The reason why I first abandoned the use of an ** Inversion of Control container** is that

*it’s so easy to misuse and abuse when it’s used without Inversion of Control in mind*.

*Unique Instances are easily injected everywhere and in all respects, they act as singletons.*Hence, it’s not the Singleton pattern to be a problem per se, but the fact that there isn’t any control over its ownership.

You may wonder, will event-driven programming solve the problem? Even in this case, only if it’s events are used with IoC in mind. If not, there wouldn’t be any difference between dispatching an event and calling a public method.

You can read more about encapsulation and states by checking Brian Will’s article and relative video: **Object-Oriented Programming: A Disaster Story**

### Abstraction, Inversion of Control and the Hollywood principle

The term *abstraction *can have different meanings according to the context. In OOP usually we “abstract” from the implementation details through the use of interfaces. The code using interfaces is not dependent on the details anymore. In software architecture, when we talk about [abstraction layers](https://en.wikipedia.org/wiki/Abstraction_layer), abstraction is used to define how generic and reusable the logic in a module is.

I suppose we may see the need to abstract the code as a way to solve the problems caused by the use of public functions. Obviously, abstraction is more about being able to write code that is not dependent on any implementation, but does it solve the problems of highly coupled code? Being dependent on an interface is not much different from being dependent on its implementation in terms of object ownership. It makes indeed a big difference in terms of being independent from specialized code, so that refactoring becomes much simpler, as it is enough to change just the implementations of our objects in order to change the behaviour of the application, but this doesn’t mean that the code is more modular.

### Inversion of Control

When ** Inversion of Control** is used, the

*framework*takes over the control (and ownership) of the objects declared by the specialised code.

This gives a great boost in code maintainability as we are starting to provide rules for object ownership and control, but there is much more. IoC when followed properly reshapes the way a codebase is designed. For explanation purposes, I usually see IoC split into **Inversion of Flow Control **and **Inversion of Creation Control.**

To know more about Inversion of Creation Control I suggest reading my article:

**The Inversion of Flow Control **is instead what we are more interested in currently. It’s also funnily called the ** Hollywood Principle**:

*“don’t call us, we will call you”*. What does it mean?

It means that the higher level of abstraction layers must not only provide the interfaces to implement but will take control over the implemented objects, calling their public methods through their known interfaces.

## Inversion Of Flow Control in OOP

The Inversion of Control principle contains all the ingredients of the recipe for a successfully maintainable code. It promotes abstraction and modularization. All the invariant modules are encapsulated at the higher levels and they are independent of each other. Objects can implement multiple interfaces to *compose* multiple behaviours. It gives a clear direction to how these objects must be controlled and what uses their interfaces.

There are multiple ways to implement inversion of control, but the best way I found to apply it is the application of the GoF [ Strategy Pattern](https://deviq.com/strategy-design-pattern/), or even better, the Game Programming

[. In fact, while the Strategy Pattern has usually a 1:1 relationship between the](http://gameprogrammingpatterns.com/component.html)

**Component Pattern****Controller**and the “Implementation”, the Component Pattern has a more powerful 1:N relationship, where a

**Manager**can control several components.

The Component Pattern is more commonly used in game engines like **Unreal **(as far as I remember it) and **Unity **(The Monobehaviour is a Component). In this scenario, a Renderer class doesn’t just render one object, but it renders all the *IRenderable* objects. In a game engine, the component pattern is always used through “Managers” that iterate over several entities implementing the same interface at different times of the frame pipeline. For example, the **PhysicManager**, the **UpdateManager **and the **RenderingManager **can be three different managers and *Tick()* is called one after the other. The Tick inside will then call the *PhysicUpdate()*, the* Update(*) and the* Render() *of every single object registered in it.

This resembles a bit what happens in Unity with the GameObjects and Monobehaviour. Each Monobehaviour can have optionally implemented methods like *Awake()*, *Start()*, *Update()* and *FixedUpdate()*. However, it doesn’t have a *RenderUpdate()*. Why is that? While Unity delegates to the user the implementation of the logic that may happen inside those customisable functions, it doesn’t need the user to specify how to render the objects because Unity already implements all the mechanisms to render them.* From the monobehaviour it just needs its data.*

Obviously, while Unity can come with as many “generic” managers as possible, it can never come with all the possible managers for all the possible behaviours a game can have and this is why it delegates to the user the implementation of custom logic.

However, if this sharp separation between the framework (Unity) and the user logic wasn’t present, would have it been possible to write all the game behaviours as mechanisms handled by manager classes? it would, leading to the definitive inversion of control.

Once all the composable and shared behaviours are encapsulated in what we can call managers, the components themselves won’t need any custom logic anymore.* Hence the components will turn out* *to be just a collection of data leading to…ECS!*

Finally, I explained to you the whole path that brought me to the **Entity Component System** design adoption. It’s not just about performance (that too though!), it’s about total Inversion of Control!

*With ECS there are three fundamental concepts:*

The **Systems**, which are our managers. They are essentially a block of usually stateless behaviours to be executed over Entity Components.

The **Entities**, while some define them as IDs, I advise to always conceptually visualize them.

**Entity Components** that are are usually structs of data stored sequentially in memory according to the type.

Interesting thoughts about Entity Component System design can be found also at: [https://medium.com/@gamevanilla/data-oriented-design-is-more-than-just-performance-d3aad3bf3b5a](https://medium.com/@gamevanilla/data-oriented-design-is-more-than-just-performance-d3aad3bf3b5a)

You can read more reasoning about the Inversion of Flow Control in this article:

## Part 2: The Solid Principles as the foundation for all the reasonings

It’s clear to me that the majority of the GoF design patterns are, in one way or another, finding a way to control object ownership. The issue I have with the GoF design patterns is that they cannot be used without comprehending the problems they are trying to solve (which often leads to wild interpretations of them!).

The only way I found to understand why the GoF design patterns exist, was to study the much simpler SOLID principles, which in my opinion are the foundation of every OOP well-designed code.

## How the Solid Principles (may) apply to Entity Component System Design

Is Entity Component System a paradigm? If we define a paradigm as a style or “way” of programming, then sure ECS is a paradigm and as such it will take a long time to get used to it. The important thing is that ECS gives strict directions to implement most (if not all) game-related behaviours.

In this second part of the article, I will make an exercise in trying to understand if the SOLID principles, born for the OOP paradigm, can be applied to the ECS paradigm too. If ECS is used to write an ECS-centric application and not only a few parts that need to be “fast” we need to have some guidelines to be sure that our code is kept maintainable over time.

Let’s start from the most fundamental fact: exactly like an IoC container would result be troublesome if used without inversion of control, any complex ECS-centric codebase will be harder to maintain if developed without layers of abstractions. In fact, an ECS codebase implemented without layers of abstraction is fundamentally procedural code with globally accessible data. ECS alone is not enough to be able to write code that is easy to refactor and maintain, but it shows us the right mindset to implement the tools that will still need to be used correctly.

ECS, once well understood, will push the user to write code in different layers of abstraction, where each layer contains systems and entity components that can be more or less reused depending on how abstracted/specialised they are. A system that iterates reusable entity components may even lay in a layer of abstraction that can be defined as a framework and be reused on different products. For example, Unity ECS physic code is more abstract than the code of the game that is going to use it. The systems and entity components of the game are specialized and unique, while the systems and entity components provided by the Unity ECS physic framework are abstracted (in relation to the game code) and reusable.

*Compared to OOP, ECS should provide a framework that allows less time spent on thinking about how to design the code and more time to spend on writing the code, since, as I am trying to demonstrate, the ECS paradigm facilitates the adoption of total Inversion of Control.*

It may also seem that, with ECS, data encapsulation does not exist anymore. While we can argue that once we solve the object ownership and control problem, encapsulation may turn out to be not so important anymore, it’s not totally true that data encapsulation doesn’t exist in ECS. If we just access any kind of data component from any system, then encapsulation is gone. Try to manage a code like that though! So, let’s approach this reasoning from another point of view before connecting all the dots: What is the responsibility of a system? *A System is the encapsulated logic of a single, well-defined, entity behaviour that must be applied to a set of entities sharing specific entity components. The rule should be that Systems can read immutable data from all the entities they need to, but they can mutate the data of only a specific set of entities, the entities that require that specific behaviour.*

### Single Responsibility Principle

This is the application of the [Single Responsibility Principle](http://staff.cs.utu.fi/~jounsmed/doos_06/material/SRP.pdf), which we must reinterpret for systems saying that:

**THERE SHOULD NEVER BE MORE THAN ONE REASON FOR AN ENTITY TO CHANGE. **

OR

**GATHER TOGETHER THE ENTITY COMPONENTS THAT CHANGE FOR THE SAME REASONS. SEPARATE THOSE ENTITY COMPONENTS THAT CHANGE FOR DIFFERENT REASONS.**

In applying this principle, our Systems will turn into very modular mechanisms applied to the set of entities affected by the single Behaviour. Behaviour composition is not achieved through interface implementation but through data composition. The more components an entity holds, the more behaviours will be applied independently to it. However, a behaviour code must change for a single reason only, for example, a system must not change both the **HealthComponent **and the **PositionComponent **of an entity, as these components would very likely change for different reasons. This principle reinforces the idea that while a System (Entity Behaviour) can read as many immutable entity components as it needs, it should define a specific single reason to change a specific set of entity components.

### Open Closed Principle

At the moment a System is seen as a single behaviour to execute, we could consequentially say that the [Open/Closed principle](https://www2.cs.duke.edu/courses/fall07/cps108/papers/ocp.pdf) can be seen as:

**ENTITY BEHAVIOURS MUST BE OPEN FOR EXTENSION BUT CLOSED FOR MODIFICATION**

Through data composition, I can extend the behaviours of an entity by adding more components, but I should never need to modify a well-written existing behaviour. If an entity needs a new behaviour, I should add it through the modification of the list of entity components which will enable new mechanisms to be executed. Since behaviours of the entities that still need the old logic must not be affected, a new system will be created instead.

More thoughts on the possible consequences of the right application of these principles can be found in [this video](https://www.youtube.com/watch?v=A1vzcxR-Ss0&feature=youtu.be&t=594)

With ECS is simpler to design the logic of the entire application in terms of layers of abstraction. Everything can be modelled as systems, from the Rendering logic, to the Character attack logic. There is no difference anymore between framework and application code, but nevertheless, everything is still designed with multiple levels of abstraction with the goal to encapsulate the shared entity behaviours within well-defined systems.

*We can say that Entity behaviour specialization happens through component composition. An Entity is defined as a more or less fine set of components. *

### Liskov Substitution Principle

Since Entity specialization can be seen as a composition of entity components instead of implementation of new interfaces, we may re-interpret the [Liskov Substitution Principle](http://www.labri.fr/perso/clement/enseignements/ao/LSP.pdf) by saying that:

**AN ABSTRACTED ENTITY BEHAVIOUR MUST BE ABLE TO USE SPECIALIZED ENTITIES THROUGH THE USE OF A SUBSET OF THEIR COMPONENTS**

It would be too simple to stop talking about my LSP interpretation here. LSP is obviously made for OOP and objects specialized through inheritance. When objects are specialized through inheritance, LSP turns out to be very similar to the Design By Contract theory found in Domain Driven Design. However, when objects are just defined as the implementation of interfaces, without inheritance, LSP applies too. In both cases, the principle simply states that a class handling dependencies must never need to downcast a dependency to its specialized type to run its logic.

In the same way, it may not be such a stretch to say that systems must never need to be aware of the entirety of components a specific entity is made of but must be able to use this entity through the components that the system is responsible for. This rule becomes impossible to break if the components the entity must have to enable the behaviour come from the same module (or more abstract one) of the system that needs to iterate it.

### Interface Segregation Principle

The application of the [Interface Segregation Principle](http://www.labri.fr/perso/clement/enseignements/ao/ISP.pdf) may require some imagination to be applied as well. It basically states that many “lean” interfaces are better than a few “fat” interfaces. Interfaces that an object implements should be as lean as possible, in such a way that modular code depending on not modified interfaces wouldn’t need to be “recompiled” if unrelated interfaces change. if modules depend on “fat” interfaces, the previous principles are not really broken, but the change of an interface for any reason would lead independent logic to be affected too. More importantly, objects that implement fat interfaces will be forced to implement all the methods of these interfaces, reducing modularity and hindering behaviour composition.

Again, in ECS we may apply this principle to the Entity Components. Entity components are structs of data that could grow indefinitely, adding more and more data to every single component. What would drive the user toward the creation of multiple lean components instead of the creation of less, fat components? Theoretically, all the entity data could be written inside one component only. However, this would lead to the writing of entity components being impossible to reuse in order to compose behaviours and consequentially to the writing of entity behaviours (systems) that cannot be reused between different specialized entities (again all of this becomes an impossible rule to break if the application is layered in separate modules).

We can say then that the ISP for ECS means:

**NO ENTITY BEHAVIOUR SHOULD BE FORCED TO DEPEND ON DATA THAT IT DOESN’T USE**

this principle would work only if the entity components that define an entity are provided by the systems. While in OOP abstracted layers provide the interfaces that the objects must implement, in ECS entity behaviours should dictate the entity components to use, so that if we design the behaviours of the entity first, the entity will become a composition of the entity components used by the relative systems.

In practical terms, if a **WalkingCharacterBehaviour **needs a **WalkingComponent **and a **DamagingCharacterBehaviour **needs a **DamagingComponent**, the **Entity **needs the ** WalkingComponent **and the

**in order to enable those two behaviours.**

**DamagingComponent**In ECS we could introduce this definition of abstraction, which is linked to the isolation of the reusable behaviours (granularity): A more abstracted behaviour is a more common behaviour between entities and the components used by this behaviour would be consequentially less specialised.

### The Dependency Inversion Principle

Better modularity is what the ** Dependency Inversion Principle** tries to solve through its application. It says:

*High-level modules should not depend on low-level modules. Both should depend on abstractions.**Abstractions should not depend on details. Details should depend on abstractions.*

The *k*ey to understanding this description is to comprehend what* abstracted layers *are, but for this, I will redirect the reader to my article:

I explained at length how DIP is applicable to Entity Component System design, through Inversion of Flow Control and layered modules. I will talk even more about it in my next articles.

## Conclusion

This article summarises the thoughts of my previous articles, but reading them is necessary to understand better my reasonings. What I think is important to take from this article is that ECS easily promotes modularization through behaviour abstraction which leads to a natural application of the SOLID principles. While all the articles I wrote before this one would be helpful to understand all the reasonings that took me to this conclusion, the next articles instead will better explain what modularization through abstraction layers actually mean.

**Previous Articles**

[http://www.sebaslab.com/ioc-container-for-unity3d-part-1/](http://www.sebaslab.com/ioc-container-for-unity3d-part-1/)[http://www.sebaslab.com/ioc-container-for-unity3d-part-2/](http://www.sebaslab.com/ioc-container-for-unity3d-part-2/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-i-dependency-injection/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-i-dependency-injection/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-ii-inversion-of-control/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-ii-inversion-of-control/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/)[http://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/](http://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/)

**New Articles**

References:

[1] Entity Component System – A Different Approach to Game / Application Development

[2] Seminar with Alan Kay on Object Oriented Programming

Enlightening!

looking forward to next part of the article, please do talk about this topic: how inter-systems communication is solved in ECS … I find that the spaghetti moves on to this area and I also question if it is even needed at all if you use temporary “flag” components

I would love to see a complete example that solves the problem of communication between systems. These has always been the problem with standard OOP where a feature is actually spread between multiple classes. ECS gives you the potential to have a class per feature (system) and to be able to turn on/off features without breaking anything (in theory).

Thanks Zammy. I talked about the topic on my older Svelto related articles, but surely my reasonings evolved since, so I have to write it in the new article for sure.

Great article!

Do you think ECS is similar to plain old C and its structs? If that’s the case, then we have gone full circle, back to procedural programming…

I would love to hear more of your opinion on this.

As I wrote in the article it would be a big mistake to see ECS as procedural programming with globally accessible data. It’s procedural programming with entities :). Of course without rules it’s simple to fall in the first case, but in doing so the code will turn totally unmaintainable. Another very important difference that I have to discuss further in a new iteration of this aritcle is the memory model. Theoretically you would never allocate memory on heap using ECS. Everything is value types stored inside the ECS database, you shouldn’t need to use custom datastructure in most of… Read more »

Interesting point of view. This article is a complementary of a book I read before, the Data-Oriented Design by Richard Fabian.

In that book the focus is on the combination of data and meaning. When we permanently apply meaning/context to data in the form of an object, we are limiting ourselves from reusing that data in a different context cleanly. So, we will end up modifying the objects over and over to fit for each new context. This is how we end up with bloated objects.