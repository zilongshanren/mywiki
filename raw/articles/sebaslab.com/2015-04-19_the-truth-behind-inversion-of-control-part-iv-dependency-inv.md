---
title: The truth behind Inversion of Control – Part IV – Dependency Inversion Principle
  - Seba's Lab
url: https://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/
author: Sebastiano Mandalà
published: '2015-04-19'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

The Dependency Inversion Principle is part of the SOLI**D** principles. If you want a formal definition of DIP, please read the articles written by Martin**[1]** and Schuchert**[2]**.

This is the most difficult principle to get right. I will take a step back from the previous article I wrote and discuss this principle more in detail from the OOP point of view.

Some may think that DIP just means writing code that depends upon interfaces (abstractions) and not their implementations. While fundamentally this is true, this is not enough to define DIP. DIP is, in fact, a principle that, when followed properly, helps to structure the architecture of your codebase and it’s not just about how to inject dependencies.

Let’s assume we are writing a complex project without any structure and, as usual, we have to decide what dependency to inject into what class. We can decide to inject interfaces instead of implementations, with or without an IoC container, but if the relationship graph between objects is unstructured and chaotic, using interfaces won’t make the code any better than using their implementations.

That’s when the DIP steps stating:

**High-level modules should not depend on low-level modules. Both should depend on the abstraction.****Abstractions should not depend on details. Details should depend on abstractions.**

This can become confusing very quickly. What do *high-level *and *low-level* refer to? What are these *modules *about? What are the *abstractions*? All these questions are expected if the coder never put any emphasis on layering their codebase, but used to write code where everything can reach everything else through injection. *Once the code is written in such a way, nothing stops the code from turning into a spaghetti bowl, where each object can reach every other object through a net of injected dependencies*.

I hope you can visualize this not uncommon case, as when this happens, even if all the injections happen through interfaces, the codebase is doomed (and as side effect coders will wonder why they are injecting dependencies through interfaces rather than using their implementations).

## Layering our codebase

A game engine, like *Unity*, provides the user with an API that lies in a different layer from the game code. The game engine is in fact found in a different *Module *(assembly) which is encapsulated and fenced from the game codebase. In the case of Unity, *the Game Engine is a High-Level Module, while the Monobehaviours implemented by the user are found in a Low-Level Module***.** High-Level modules are always more abstract, which means more generic, than Low-Level modules.

What DIP states is then what we know already by experience. The *Game Engine Framework*, coming from a different assembly that our game assembly is dependent upon, has no way to know directly the classes we declare in our application codebase. This means that the *abstract modules* (the Unity framework) don’t depend on *details *(our implemented **MonoBehaviour **classes). They both are dependent on the Monobehaviour *interface*.

*Since the interface must be known by both layers, is consequential that the interface must be provided by the High-Level Module* (and cannot be otherwise technically).

The DIP principle then pushes us further. It’s not just a matter of game engine and game codebase. *DIP wants us to find the common behaviours in our implementations, abstract them and package them away in higher-level modules*. Let’s see an example using a naive game code architecture where we have an **EnemyHealthManager **and **HeroHealthManager**. For the sake of the example, it doesn’t matter how many entities there are in-game, so we can assume there is just one Enemy and just one Hero.

A pseudo-code can look like this:

class EnemyHealthManager { public EnemyHealthManager(Enemy enemy) { _enemy = enemy; _amount = 0; } public ReceiveDamage(int amount) { _amount += amount; } public void UpdateHealth() { enemy.health -= amount; _amount = 0; } Enemy _enemy int _amount ; }

class HeroHealthManager { public HeroHealthManager(Hero hero) { _hero= hero; _amount = 0; } public ReceiveDamage(int amount) { _amount += amount; } public void UpdateHealth() { hero.health -= amount; _amount = 0; } Hero _hero; int _amount; }

Nobody would ever write code like that, right, RIGHT? however how many times do we see duplicated code for less trivial cases? The trick is to find the common behaviour, extract it, and move it to a higher-level module.

The *high-level Health module* would look like

class HealthManager: IUpdateable { public HealthManager(IHaveHealth entity) { _entity= entity; _amount = 0; } public ReceiveDamage(int amount) { _amount += amount; } public void Update() { _entity.health -= amount; _amount = 0; } IHaveHealth _entity; int _amount; } interface IHaveHealth { int amount { set; } }

the* low-level game module* will look like

class Hero:IHaveHealth { public amount {get; private set;} } class Enemy:IHaveHealth { public amount {get; private set;} }

of course, the *Composition Root* then will use both modules to create the actual entity objects, the two managers and inject the objects into the managers:

class CompositionRoot { public void Setup() { var hero = new Hero(); var enemy = new Enemy(); var heroHealthManager = new HealthManager(hero); var enemyHealthManager = new HealthManager(enemy); } }

the mechanism linked to health management can be reused and linked to whatever implementation of the **IHaveHealth **interface.

*The inversion that happened is not about how to inject dependencies but about what provides the mechanism interface. The dependency in the mechanism is no more an implementation coming from the low-level module, but it’s an abstraction owned and provided by the high level-module itself.*

public interface IUpdateable { void Update(); } public class UpdatableManager { void Add(IUpdateable tickableManager) { _tickableManagers.Add(tickableManager); } public void Tick() { foreach (IUpdateable tickable in _tickableManagers) tickable.Update(); } }

class CompositionRoot { public void Setup() { var hero = new Hero(); var enemy = new Enemy(); var heroHealthManager = new HealthManager(hero); var enemyHealthManager = new HealthManager(enemy); _updatableManager.Add(heroHealthManager); _updatableManager.Add(enemyHealthManager); } public async void StartTick() { while (applicationRuns) { //...other game logic that can damage entities _updatableManager.Tick(); await Task.Yield(); } } }

This example implements a *three layers abstraction*.

*The first layer* provides and handles the **IUpdatable **interface that is implemented by our managers. *The second layer* provides and handles the **IHaveHealth **interface that is implemented by our entities. *The third layer* is where our entities are implemented.

The third layer is the most specialised one, as it has entities that can specialise multiple mechanisms and not just **IHaveHealth**. The second layer is more abstract than the third one. It doesn’t know anything about the third one so it has no dependency on it. Its only dependency is provided by the layer itself (**IHaveHealth**). The first layer is eventually the most abstract one. It knows nothing about mechanisms and entities, it just provides a policy about how the updatable mechanism is updated.

With this, I hope I gave you a good example of the infamous diagram Martin created in his DIP article which can be found in ANY DIP-related article without further explanation. Of course don’t give much importance to the Policy, Mechanism and Utility names, they are just random names. The number of layers is not important either, it is dictated only by the granularity of your modules and how well you were able to identify common behaviours at different levels of abstractions.

The important bit to take is that the order of dependencies is inverted and common behaviours are NOT dependent on specialised implementations so that their code wouldn’t need to change when the implementations change.

![](../../assets/d6d05b381e0f7160.png)

![](../../assets/5548f5ffebbb91c8.png)

![](../../assets/e840cd809b6df70a.png)

## The DIP, The Strategy Pattern and The Hollywood principle

You may have recognised the *Strategy Pattern*** [3]** up there. The Strategy pattern is fairly fundamental in order to achieve DIP and I will use it further in my following articles, although in different forms.

In my previous articles, I explained that in order to invert the control of the code execution flow, our specialized code must never call directly methods of more high-level module classes. It is the high-level module mechanism to control the flow of our specialised code. This is also called (sarcastically) the **Hollywood principle**, stated as *“don’t call us, we’ll call you.”*.

Although the framework (high-level module) code must take control over the specialised code, it would not make any sense to couple our framework with specialised implementations. A generic framework doesn’t have the faintest idea of what our game needs to do and, therefore, wouldn’t understand anything declared outside its scope.

Hence, the only way our framework can use objects defined in the game layer is through the use of interfaces, but this is not enough. The framework cannot know interfaces defined in a specialised layer of our application, this would not make any sense as well.

The *DIP* introduces a new rule: our specialised objects must implement interfaces declared in the higher layers. In other words, the framework layer defines the interfaces that the game entities must implement.

In a practical example, a **RendererSystem** handles a list of **IRendering **“Entities”. The IRendering entity is an interface that declares all the methods needed to render the Entities, such as **GetWorldMatrix**, **GetMaterial **and so on. Both the RendererSystem class and the IRendering interface are declared inside the framework layer. Our specialised entities then need to implement IRendering in order to be usable by the framework. Eventually, the entities are registered in RendererSystem as IRendering objects.

## Designing layered code

I used the word *framework* to identify the most abstract code and *game* to identify the more specialised code. However framework and game don’t mean much. Limiting our layers to just “the game layer” and “the framework layer” would be a mistake. Let’s say we have mechanisms that handle very generic problems that can be found in every game, like the rendering of the entities, and we want to enclose this layer into a module. We have defined a layer that can be compiled into a **DLL** and shipped with whatever game.

Now, let’s say we have to implement the logic closer to the game domain. Let’s say we want to create a **HealthManager **that handles the health of the game entities with health. Is HealthManager part of a very generic framework? Surely not. However while HealthManager will handle the common logic of the IHaveHealth entities, not all these entities will be of the same type. Hence HealthSystem is more abstract than more specialised other mechanisms. The Health module is then a third layer between the framework and the game application. The code must strive to find the right number of layers to model the common behaviours/mechanisms of the game entities.

**Putting ECS, IoC and DIP all together**

In conclusion I could say that to achieve Inversion of flow control we should stop designing solutions using a classic bottom-up approach to break down the problem or, in other words, to design specialized behaviours before the generic ones.

In my vision of Inversion of Control, it’s necessary to break down the solutions using a top-down approach. We should think of the solutions starting from the most common behaviours. What are the common behaviours of the game entities? What are the most abstract mechanisms we should write? What once would have been solved by specializing classes through inheritance, should be now solved by layering our strategies within different levels of abstraction providing the relative interfaces to be used by the more specialised code. Of course, we can achieve this layering step by step through refactoring, as indeed, early abstraction is the root of all evil (and only experienced programmers would immediately identify the common behaviours in a complex project).

I believe that in this way we could benefit from the following:

- We will be sure that our strategies will have just one responsibility, modelling just one behaviour
- We will basically never break the Open/Close principle since new behaviours mean creating new strategies
- We will inject fewer dependencies, avoiding using an IoC container as a Singleton alternative
- It will be simpler to write reusable code
- We could potentially achieve real encapsulation

In the [next article](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-v-drifting-away-from-ioc-containers/) I will explain how I would put all these concepts together in practice

References:

[https://web.archive.org/web/20150905081103/http://www.objectmentor.com/resources/articles/dip.pdf](https://web.archive.org/web/20150905081103/http://www.objectmentor.com/resources/articles/dip.pdf)[http://martinfowler.com/articles/dipInTheWild.html](http://martinfowler.com/articles/dipInTheWild.html)[https://refactoring.guru/design-patterns/strategy](https://refactoring.guru/design-patterns/strategy)- Object-Oriented Analysis and Design with Applications (Grady Booch)

I strongly suggest to read all my articles on the topic:

[https://www.sebaslab.com/ioc-container-for-unity3d-part-1/](http://www.sebaslab.com/ioc-container-for-unity3d-part-1/)[https://www.sebaslab.com/ioc-container-for-unity3d-part-2/](http://www.sebaslab.com/ioc-container-for-unity3d-part-2/)[https://www.sebaslab.com/the-truth-behind-inversion-of-control-part-i-dependency-injection/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-i-dependency-injection/)[https://www.sebaslab.com/the-truth-behind-inversion-of-control-part-ii-inversion-of-control/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-ii-inversion-of-control/)[https://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/)[https://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/)[https://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/](http://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/)

Really nice series of posts. I can hardly wait for the fifth one…

Thanks. It will take some time unluckily, since I am working on the first draft of the framework

If there’s any way I could help, I’ll gladly spare some time. I’m preparing a “Best practices in Unity” small training in our company for the games department soon and part of it is inspired by your posts.

I’m reading a lot about game architects in Unity lately and this series are really good. I’m have a really good experience using IoC and MVC in other projects, but I feel that MVC play really great on UI based apps but not in games (simulations at the end of the day), and the other way around with ECS. I really will like to see the next post. IMHO a combination of both systems, using MVC for the UI bit (popups, handling complex UI components, etc) and ECS (for the game itself) is the winner combo, but I need to… Read more »

I have already started to write the new article. I reckon it will be quite long, maybe I have to split it in two parts. I spent most of the time to write the first draft of the framework, that is already available on github with an example included. The example is the unity survival demo that I rewrote with the framework. However it’s better to wait for the article to understand what I did.

May I just say that you are confusing Inversion of Control to be only Dependency Injection. A paper recently published identifies a bottom up approach to Inversion of Control, which goes beyond Dependency (State) Injection to include Continuation Injection (inversion of behaviour) and Thread Injection (inversion of performance). The paper is available at http://doi.acm.org/10.1145/2739011.2739013 (or for a free download a link off http://www.officefloor.net/mission.html ). I hope this helps you realise your vision of a bottom up approach is actually available now 🙂

Thanks for the feedback! I will read those articles asap! I am not sure if it’s related, but I do continuously talk about Inversion of Creation Control and Inversion of Flow Control, so I actually do not think Inversion of Control is Dependency Injection.