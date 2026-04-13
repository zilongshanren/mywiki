---
title: The truth behind Inversion of Control - Part I - Dependency Injection - Seba's
  Lab
url: https://www.sebaslab.com/the-truth-behind-inversion-of-control-part-i-dependency-injection/
author: Sebastiano Mandalà
published: '2015-03-29'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

There is a wicked truth behind the use of an *Inversion of Control container*, an unspoken programming tragedy that takes place every day. Firm in my intentions to understand better the severe consequences of using an IoC container in game development, I decided to write this series of articles that will tell about the problems, the principles and the possible solutions.

If you are among the people who regret starting using an IoC Container, you are not alone. I too noticed how the codebase degraded over time, but back then I couldn’t pin down the reason for it. Nevertheless, the problem was becoming clear:* the IoC container solution was scarily used too often as an alternative to the Singleton pattern to inject dependencies*. With the code growing and the project evolving, many classes started to take the form of a blob of functions, with a common pitfall: dependencies, dependencies everywhere.

In order to deeply understand why using an IoC container often degenerates into spaghetti code all over again, we need to understand all the principles behind its conception starting again from the basics (which is useful even if you have no intention to use a container):

**What Dependency Injection is**

Dependency Injection isn’t anything fancy but it’s a fundamental and common concept in *Object Oriented Programming*. A dependency is just an interface used and held by a class. Usually, dependencies are passed in two ways: injecting them through constructor/setters or solving them directly with global variables (static objects/singletons). *Singletons *do not promote state encapsulation, as they can be used anywhere. Singletons awkwardly hide your dependencies: there is nothing in the class interface showing that the dependency is used. Singletons strongly couple your implementations, resulting eventually in too long and painful code refactoring. For these reasons, it’s preferable to inject dependencies manually:

class Watcher { INofification action = null; public Watcher(INofification dependencyInterface) { this.action = dependencyInterface; } public void Notify(string message) { action.OnNotification(message); //Watcher depends on INotification interface } }

This example shows how to inject dependencies via the constructor. It’s important to note that DI is supposed to not couple object implementations, so interfaces are passed instead of classes. This is necessary to allow changing implementations in the composition root without needing to touch any existing class code (thus without breaking the *Open/Close principle*** [7]**). Now, would you pass 10 or more dependencies by constructor? I surely wouldn’t, if nothing else, for how painful and inconvenient it would be.

*The same reasoning should apply when an IoC container is used*. Just because it’s more convenient to use, it doesn’t mean you can take advantage of it. Injecting numerous dependencies is a byproduct of badly layered/structured code that does not use sound communication patterns. The result is just a mess with coupling again while using interfaces becomes more and more irrelevant. Hopefully, I will be able to explain why this happens and how to avoid it in more detail with the next articles in this series. However, I can tell you right now that I found my answer to my doubts in the

**SOLID**principles. If the codebase is designed around them, these problems wouldn’t occur, since the number of dependencies injected is directly linked to the number of responsibilities a class has got.

[1]A single responsibility should lead to just a few dependencies injected. However, without proper rules to follow, coders tend to break the Open/Close principle and add behaviours to existing classes instead to adopt a modular and extendible design. That’s when IoC containers become dangerous as they help this process, making it less painful.

## How Dependencies end up being badly structured

Where do the injected dependencies come from? If the dependencies are injected by constructor, they obviously come from the outer scope where the object that needs the dependencies injected has been created. In its turn, the class that is injecting the dependencies into the new object could need also dependencies injected, which consequently are passed from another class in the parent scope. This chain of dependency creates a waterfall of injections and the relationship between these objects is called *Object Dependency Graph*.

Albeit, where does this waterfall start from? It starts from the place where the dependencies are created. This place is called *Composition Root*. Root because is where the context is initialised, composition because is where all the dependencies are created and injected and, therefore, the initial relations composed.

A composition root can look like this:

void CompositionRoot() { var dependencyA = new ImplementationOfINofification(); var watcher = new Watcher(dependencyA); RegisterObject(watcher); }

In a correctly layered and modular codebase, multiple specialised composition roots could be found. I won’t explain now what this means but is enough to know that because of the lack of modularity, usually, a game ends up with having just one or very few composition roots. These composition roots become enormous, instantiating dozens and dozens of dependencies and injecting them all over the place. When this gets out of hand with the project growing, the dependency graph becomes enormous too. Since an IoC container is designed to make injection an easy process, an awkward amount of dependencies can be injected with no effort, especially when no rules are set on what and what not can be injected as a dependency. An experienced team can alleviate the problem by setting these rules at the start of the project. In conclusion, IoC containers are not foolproof tools but need to be used by teams with a relevant amount of experience to avoid disastrous consequences, however, in my experience, IoC containers never proved themselves useful in any way when used to develop videogames.

Games have a different range of problems compared to the applications that IoC containers were initially designed for, where for example, using a configuration file to set up dependencies may make more sense (the configuration file is one of the features of a fully featured IoC container).

## Object Communication and Dependency Injection

Why are relationships between objects needed? Mainly to let them communicate with each other. All forms of communications involve dependency injection.

Communication can couple or not couple objects, but in all cases injection is involved. There are several ways to let objects communicate:

*Interface injection*: usually the interface A is injected in B, B is coupled with A [e.g.: Inside a B method A is used,*B.something() { A.something())*;]*Standard Events (callbacks)*: usually B is injected in A, A is coupled with B [e.g.:Inside A, B is injected to expose the event, B.onSomething += A.Something]*Commands*: B and A are uncoupled, B could call a command that calls a method of A. Commands are great to encapsulate business logic that could potentially change often. A Command Factory is usually injected in B.*Mediators*: usually B and A do not know each other, but know their mediator. B and A pass themselves into the mediator and the mediator wires the communication between them (i.e.: through events or interfaces). Alternatively, B and A are passed to the mediator in the Composition Root, making A and B dependencies for the Mediator and not the other way around.- Various other patterns like
*Observers*,*Event Bus*where A and B do not know each other but are put in communication through these patterns like it happens with the Mediators., Event Queue[2][3]

How to pick up the correct one? If we don’t have guidelines it looks like any is fine. That’s why sometimes we end up using, randomly, one of these. Remember the first two patterns are the worst because they couple interfaces that could change over time.

We can anyway introduce the first sound practice of our guideline for our code design: our solution must minimize the number of dependencies.

Of course, the second sound practice is to follow the *Single Responsibility Principle.* One of the 5 principles of **S**OLID, and possibly the most fundamental one. The classes must strive to have one responsibility only to promote modularization and reusability and reduce the number of dependencies to the bare minimum. Communicating could be considered a responsibility, therefore it’s better to delegate it.

How we are going to achieve SRP and solve the dependencies blob problem is something I am going to explain in the [next articles](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-ii-inversion-of-control/) of this series.

## Dependency Injection and Dynamically Created Objects

It’s interesting to note that dynamic objects are never dependencies. As we will find out in the next articles, only objects that are created directly in the composition root are dependencies and as such they are passed down to other objects. Dynamic objects, like in a game could be bullets, are instead always stored in lists or similar data structures. They are not dependencies for other objects, but they are usually managed by other objects. A dynamic object may still require dependencies, and therefore the class that creates the dynamic object must also have the responsibility to inject the dependencies necessary. In order to remove this responsibility from other classes, factories can be used. *Factories* can be created in the composition root and injected as dependencies. *Factories *can also hold the dependencies necessary to the objects they are going to generate at run time.

## Service Locator Pattern[6]: a simple specialised example of Dependency Injection without using a container

Once the specialised purpose of a set of dependencies is identified, it could be possible to find a specialised way to solve them. Services are usually units of logic that allow a client to communicate with external devices, service can be executed from inside *Commands *or from inside *GUI Presenters*. For example, when clicking a GUI button a service could be called to store a value in a database. Services are normally stored in a separate *Service Layer* and their implementation is hidden behind the use of interfaces. We could have, for example, an **IStoreUserInformation** service. The class that will use this server won’t need to know where the user information will be actually stored, and that decision can be deferred to the composition root time where an actual implementation of the service is bound to the interface. When configuration files are used, this could also allow switching service implementations without actually compiling a new client. While, of course, we can inject services like explained in this article, the number of services is usually high and seeing them used anywhere may not be convenient nor elegant. The best solution is then to register the Services inside a Service Locator object and inject this object instead. The Service Locator Pattern allows to bind an interface to registered implementations and retrieve the implementation through the interface later on when required.

*bibliography*

**[1] SOLID (object-oriented design)**

**[2]** **Event Bus**

**[3] Event Queue **

**[3] Event Queue **

**[4] Single Responsibility Principle**

**[5] Interface Segregation Principle **

**[6]** **Service Locator**

I strongly suggest to read all my articles on the topic:

[http://www.sebaslab.com/ioc-container-for-unity3d-part-1/](http://www.sebaslab.com/ioc-container-for-unity3d-part-1/)[http://www.sebaslab.com/ioc-container-for-unity3d-part-2/](http://www.sebaslab.com/ioc-container-for-unity3d-part-2/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-i-dependency-injection/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-i-dependency-injection/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-ii-inversion-of-control/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-ii-inversion-of-control/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/)[http://www.sebaslab.com/the-truth-b…ntrol-part-iv-dependency-inversion-principle/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/)[http://www.sebaslab.com/the-truth-b…rol-part-v-drifting-away-from-ioc-containers/](http://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/)

Fantastic article, Sebastiano!

And “our solution must minimize the number of dependencies” should be turned into a mantra!