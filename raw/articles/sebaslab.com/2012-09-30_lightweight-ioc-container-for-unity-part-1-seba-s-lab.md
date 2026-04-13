---
title: Lightweight IoC Container for Unity - part 1 - Seba's Lab
url: https://www.sebaslab.com/ioc-container-unity-part-1/
author: Sebastiano Mandalà
published: '2012-09-30'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

Unity is a good game development tool and honestly, I like most of its features. However, the programming framework is awkward to use on big projects where code maintainability is of fundamental importance. As you may have guessed, the following considerations in this article do not apply to simple projects or projects developed by one or two coders. For these specific cases, Unity is good enough. The arguments in this article apply to relatively complex projects developed by a medium-big team.

After years of analysing the intrinsic issues of the Unity framework, I realised that they all share the same root: the way Unity injects dependencies inside entities, or better saying, how Unity makes this natural process very difficult.

A dependency can be defined as an object needed by another object to execute its code. If object A needs object B to execute its code, B is a dependency for A. When B is passed into A, we say that the dependency B is injected into object A.

### The problem

Unity code framework is designed around *Bilas’ Data-Driven GameObject System*1. A component-based entity framework brings many benefits: pushes the users to favour composition over inheritance, keeps the classes small, clean and focused on a single responsibility, and promotes modularity. This is in a perfect world.

In Unity, the Entities are called *GameObjects* and the Components are based on *MonoBehaviour* implementations. Components add “behaviours” to Entities and theoretically, they should be perfectly encapsulated. The Entity Component structure relies on the fact that components define the whole entity’s logic. In order to use a Gameobjects framework properly, the following should be followed:

- MonoBehaviours must operate within the GameObjects they are attached to. This is needed to ensure that encapsulation is not broken, as it shouldn’t be needed to. Components, by design, must handle only the Entity they are attached to.
- MonoBehaviours are modular and single-responsibility classes reusable between GameObjects.
- The behaviour of a GameObject should be extended by adding MonoBehaviours instead of adding code to an existing MonoBehaviour. One component must add only one behaviour to encourage modularity.
- GameObjects should not be created without a view such as a mesh or a collider or anything that is actually an entity in the game (i.e.: Monobehaviours shouldn’t be managers)
- MonoBehaviours can know other components on the same GameObject using GetComponent, however,
*they shouldn’t know MonoBehaviours from other GameObjects*.

The first three points are obvious, even to those who have never heard about Entity Component frameworks. The Components design allows adding logic to an entity without using inheritance. We can say that instead to specialize the behaviour of an Entity vertically (usually specializing classes through polymorphism), Components allow expanding behaviours horizontally. This is not the place to talk about it, but in case you didn’t know, composition over inheritance is a well-known practice of which benefits have been proved extensively. The great thing about an Entity Component framework is then that composition comes naturally, without any particular effort. The smaller the component, the easier will be to reuse it, that’s why giving a single responsibility to each component will promote modularity.

The fourth point may seem an arbitrary rule, but Unity entities by default implement the **Transform **class, implying that the object must be placed in the world. What’s the point of having a Transform by default if it’s not used?

Last point starts to uncover the real issue. MonoBehaviours are meant to add behaviours on the GameObject that they are attached to and consequentially Unity can’t provide a clean way to let GameObects know each other without resorting to awkward solutions. The other problem is that Unity asks the user to use MonoBehaviours even when the logic to write is not related to an Entity at all. For example: let’s say there is an object called **MonsterManager **in the game world which must know the monsters that are still alive. When a monster dies, how can this object know it?

Currently, there are 2 simple solutions to this problem:

- MonsterManager is a Monobehaviour created inside a GameObject that has no view. All the monsters will look for the MonsterManager class using the
*GameObject.Find*or*Object.FindObjectOfType*function inside the*Start*or*Awake*methods and add themselves into the MonsterManager. MonsterManager could potentially listen to a Monster event to know when it will die. - MonsterManager is a Singleton and it’s used directly inside the Monster Monobehaviour. When a monster dies, a public MonsterManager function is called.

both cases are needed to solve the same problem: Inject dependencies. In the case A, MonsterManager is a dependency for the Monster objects. The Monster objects cannot add themselves to the MonsterManager if they don’t know the MonsterManager object. In the second case, the dependency is solved through the use of a global variable. You may have heard that global variables and singletons are very bad to use and you may not have fully understood why yet. For the moment, let’s focus on the practical aspects of these solutions:

### What’s wrong with **GameObject.Find**

Aside from being quite a slow function, *GameObject.Find* is one example of how awkward the Unity Framework is for big projects development. What happens if someone in the team decides to rename the GameObject? Should GameObjects renaming or deletion be forbidden? GameObject.Find can lead to several run-time errors that cannot be caught at compiling time. This scenario could be really hard to manage when dozens of GameObjects are searched through this function. GameObject.Find and similar functions should be definitively abolished by the Unity framework (in favour of better alternatives).

### What’s wrong with the **Object.FindObjectOfType**

How should the MonsterManager object be injected inside the Monster class then? There is actually another solution: calling the function *Object.FindObjectOfType*. However, what is FindObjectOfType? Object.FindObjectOfType could be seen as a wrong implementation of the [Service Locator Pattern](http://stackoverflow.com/questions/22795459/is-servicelocator-an-anti-pattern), with the difference that it is not possible to abstract the interface of the service from its implementation. This is another problem of the Unity framework, which I will now briefly hint at, but that would need another entire article, Unity discourages the use of interfaces. The interface is among the most powerful concepts at the core of every well-designed code. Instead of promoting the usage of interfaces and therefore abstraction, Unity pushes the coder to use Monobehaviour, even when the use of Monobehaviour is not necessary.

### What’s wrong with the **Singleton** Pattern

**Singleton **is a controversial argument since the pattern has been invented. I am personally against the use of Singleton; every single Singleton class I have encountered so far, led only to design problems hard to fix through refactoring. However, if you ask me why I am against Singletons, I will not answer you with the usual answers (they break encapsulation, hide dependencies, make it impossible to write proper unit tests, bind the code to the implementation of service instead of its abstraction, make refactoring really awkward, usually create memory leaks), but with the hindsight of the practice: your code will become unmantainable. This is because the use of Singletons comes without any design constriction that, while apparently makes the coder life easier, will make it a hell later on, when the code turns into an incomprehensible blob without a structured flow (spaghetti code).

Projects developed by one of two coders wouldn’t experience the problem at first or ever (for example, if the project doesn’t need to be maintained over time), but mid-size project developers will pay the consequences of wild designs when they realise that refactoring became a very costly operation. Think about it, you can use Singletons everywhere, without limits, without rules. What would keep a coder from making a total mess out of it? Common sense? Let’s not fool ourselves, common sense doesn’t apply when release deadlines approach fast.

If this is not enough to dismiss Singletons think of this: what is a Singleton if not just another way to inject dependencies? When you don’t have any other choice than singletons to inject dependencies, you can be sure that your design **smells!**

Furthermore, singletons must rely on public functions, which may change states inside the Singleton itself. When the singleton is used recklessly in several parts of the code, it becomes very hard to track when and how these states changed. Refactoring becomes tremendously risky because changing the order of the calls of the public functions of a singleton could mean finding the singleton itself in an unexpected state. The biggest problem about Singleton is then the fact that they cannot be designed with Inversion of Control in mind. You are always forced to write functions like *IsSingletonReady()* or *DisableThisSpecificBehaviour()* or *AccessToThisGlobalData(),* leaving the control of the internal states to external entities there are hard to track, especially due to the Singleton being fundamentally a globally accessible variable.

Communication between objects is the hardest OOP problem to solve and the main reason why dependencies are injected is to let objects communicate with each other. Communication is impossible without any form of injection. Therefore while in some rare cases, the use of a Singleton could be acceptable, you can’t work with a framework that won’t let you use any other kind of injection. While it’s feasible, it’s totally unreasonable to solve all kinds of communication problems through singletons.

### The solution

There are several ways to resolve dependencies: using the **Service Locator** pattern, injecting dependencies manually through constructors/setters, exploiting reflection capabilities through an IoC container and, obviously, using Singletons. Singletons aside, I use the Service Locator Pattern ONLY when it’s used to inject actual stateless services. Manual injection would be the preferable solution, but since Unity doesn’t have an entry point where dependencies can be created and injected, manual injections become quite hard to achieve without a good understanding of the Unity limitations.

The other solution available is to use IoC containers. Another article is needed to explain what an IoC container is, therefore I will give a first simple definition: An IoC container is a…container that creates and contains the dependencies that must be injected inside the application objects. It is called Inversion Of Control because the design is thought in such a way that the dependencies are never created by the user, but they are lazily created by the container when they are required.

There are several IoC containers out there, a lot written in c# as well, but practically none work in Unity (at the time of this article writing, that was 2012, ) and most of all, they are damn complicated*. For these reasons, I decided to create an IoC container for Unity, trying to keep it as simple as possible. Actually creating a basic IoC container is pretty straightforward and everybody can do it, my implementation has just a few tweaks that make it simple to use with Unity projects.

### Conclusion

The second part of this article (including source code) is available here: [http://blog.sebaslab.com/ioc-container-for-unity3d-part-2](http://blog.sebaslab.com/ioc-container-for-unity3d-part-2)

**2022 Update: Note that I abandoned the use of Inversion of Control containers in 2015 and I do not recommend their use anymore (more on this in the next articles). Manual dependency injection is far superior.** **Note that since the writing of this article, many IoC containers dedicated to Unity have been developed and the most famous are StrangeIoC and ZenInject, both inspired by my obsolete Svelto.IoC**.

I strongly suggest to read all my articles on the topic:

[http://www.sebaslab.com/ioc-container-for-unity3d-part-1/](http://www.sebaslab.com/ioc-container-for-unity3d-part-1/)[http://www.sebaslab.com/ioc-container-for-unity3d-part-2/](http://www.sebaslab.com/ioc-container-for-unity3d-part-2/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-i-dependency-injection/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-i-dependency-injection/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-ii-inversion-of-control/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-ii-inversion-of-control/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/)[http://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/](http://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/)

please continue with the next article =). I was searching for that for few days

Hi, thanks for the comment.

Hey Sebastiano,

I have to admit I never used an IoC container before, and I would really be curious to see a continuation to this article, to learn more and maybe change my current design patterns.

As of now, my solution to the problem is to usually keep my [Level] class as one of many “main” MonoBehaviours of an empty “Brain” GameObject, and then go through a global Notificator (which is the only singleton in my project) that every class uses to send events. Then I just listen to [MonsterBornEvent] / [MonsterDieEvent] from the [Level] class.

Svelto tends to solve this problem with event dispatchers, avoiding a “java-like” EventBus singleton for all the objects intercommunication. (please Sebastiano, correct me if I am wrong!)

Nice article. I’m using a type of IoC by myself and I think it solves most of the described problems well.

The Object.Find method also have the disadvantage that it looks through all gameobjects in a scene, so this is terribly slow and should not be used easily (may as well apply to Transform.GetChild).

The singleton pattern may be controversal, but it is imho a valid way to bypass some of these problems for smaller projects, though it’s not a fitting solution for larger projects.

So I’m looking forward to your next chapter of the article 🙂

I am quite interested to see an IoC container for Unity3d, as I have been looking around to find one that does work with it. Thanks for your efforts, and sharing them (possibly) with others!

thanks for the comment, 2nd part of the article + link to github repository can be found here: http://blog.sebaslab.com/ioc-container-for-unity3d-part-2

I don’t get it why not just use events?

Also have you tried Ninject? I’m looking to use it for my future Unity3d projects.

Ninject does not work out of the box in Unity. You can anyway use Uniject https://github.com/banderous/Uniject that is a working version of ninject for Unity. I do not use it because for me containers must be kept simple, this stuff is utterly overcomplicated.

I thought you started out right from Uniject at start, but soon realize what you are stating here: that framework is way more complicate to digest than your.

I do use events, but events are not suitable to solve all the communication issues. Moreover two instances must know anyway each other to setup the events communication (unless you use singleton event bus, which I loathe). I actually wrote a little post about events and commands (I use commands widely as well). Another technique I like, but I do not use much, is the mediator communication.

http://blog.sebaslab.com/on-commands-and-events/

Yeah, actually I am also wondering why you aren’t using events for communicatiing stuff. Reasons for that?

Hello Dominik, I just answered Peter question that unluckily I did not notice before. Thank you for the comment.

I’ve wanted to try IoC but never had the guts try it.

Thanks you for this article!

thanks a lot

Hi in receving emails of links to your blog in latin. Maybe it was hacker?

I installed a plugin that added some fake posts in the blog. It may have been that.

[…] IOC containers in Unity3D – http://blog.sebaslab.com/ioc-container-for-unity3d-part-1/ […]

+1 Great stuff you mentioned there! Particularly your points about how GameObjects and MonoBehaviours should be implemented. I’ve had lots of issues before with my GameObjects setup. I wasn’t doing that much wrong ‘seemingly’ but now reading this and thinking back, I see why… Thanks for the article!

Fantastic article that made me start using IoC on Unity in a more organized fashion! (Although I always used IoC on systems development, I had not tried to use it with a dedicated container on Unity until reading this.)

Upon your proof of concept, I ended up creating a fully IoC container (that grew so much that deserved being released!): https://github.com/intentor/adic/

Anyway, thanks for the great couple of articles!

Thanks André..I will soon blog another article, which clarify very important aspects related to IoC principles. Meanwhile I have tweeted your work 😀

Thanks for the reply and sharing! =D

And I’ll be waiting eagerly for your next article! I’m sure it’ll bring some interesting facts… and new ideas about IoC!

I don’t agree that GameObjects should not be created without a view. It’s useful to have GameObjects without a graphical representation for structuring your game object tree, simplifying transforms and providing logic acting on groups of game objects.

Agreed, but honestly if you create GameObject to manipulate Transforms it’s still a view. My reasoning applies for GameObjects with Monobehaviours that just handle logic outside the GameObject itself, like a manager. Your examples are all valid, except the last one, in case you are talking about a manager of gameobjects.

[…] could require quite extreme solutions, but there is a more general issue here that is explained in Sebastiano Mandala’s blog better than how I can do here in a few […]

“It is called Inversion Of Control because the design is thought in such a way that the objects are never created by the user, but they are lazily created by the container when they are needed.”

This was actually the most interesting and intriguing part when trying to work out some features on the Svelto.ECS example

[..] “Having a complex hierarchy in Unity doesn’t come for free, all the transforms must be computed hierarchically, therefore an extra GameObject is an extra matrix multiplication to execute every frame.” [.. ] So many people doesn’t realize this fact and think that many gameobjects come at no cost. That’s also why object pooling helped so much in developing a mobile game for iPad in 2012. We just needed 20 – 30 recycling bullets for the whole scene even with dozen of turrets. The scene never needed more than that amount of bullets concurrently. Even if the feeling on screen… Read more »

Nice article 🙂

thanks Gwaredd, did you read the whole series (7 articles)? We are not using IoC container anymore nowadays, gonna write an article about it soon. Our new projects use only Svelto.ECS now

Lemme guess, ScriptableObjects? 😉

nope, but you should know by now 🙂

hi Sebastiano, please post the next article about manual dependency injection~~ Really want to see it beat the current DI libs(cause they are too complex for me)

Hello, this article is 10 years old. I am going through the process of brushing them up and this is now revised, but all the next articles have been available for a long time.