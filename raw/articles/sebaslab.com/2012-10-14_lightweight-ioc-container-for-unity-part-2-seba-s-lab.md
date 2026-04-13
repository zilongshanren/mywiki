---
title: Lightweight IoC Container for Unity - part 2 - Seba's Lab
url: https://www.sebaslab.com/ioc-container-unity-part-2/
author: Sebastiano Mandalà
published: '2012-10-14'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

*Note: this article explains the use of Svelto.IoC container in more detail. However,* *I deprecated it a long time ago**, so read this article for knowledge, but know that I now don’t recommend using an IoC container in any project. *

In my [previous article](http://blog.sebaslab.com/ioc-container-for-unity3d-part-1/), I briefly introduced the problems related to injecting dependencies using the Unity engine framework. I did not give an in-depth explanation because only those who understood the problem by themselves, can really understand why a solution is needed. If this is not the case, one may think that all this theory is irrelevant as long as “things get done”. However, In a big team/complex project environment is actually important how things get done too. Getting things done for the sake of finishing them as soon as possible, may lead to some tragic consequences. The truth is that keeping your code maintainable is as important as getting things done since, for large projects, the long-term cost of maintenance is higher than the cost of developing new features.

Completing a feature in two days and then spending five days fixing the relative bugs found in production, due to the complexity of the solution adopted, won’t make anyone look good. Breaking good design practices to complete a feature in record time and then forcing someone else to spend several days to refactor it in order to extend its functionalities, won’t make anyone look good either.

I spent a long time during my carrier understanding how to write maintainable code and I eventually realised that the most important condition is to write simple code, so simple that doesn’t even need to be commented to be clearly understood by another coder. Writing simple code isn’t an easy task, often, in fact, those who think to get things done easily end up writing very convoluted (over-engineered) code, hard to read, maintain and refactor. I also realised that the only way to be able to write simple code for each possible problem is to deeply understand all the aspects involved in good code design.

These aspects are fundamentally explained in the [SOLID](https://en.wikipedia.org/wiki/SOLID_(object-oriented_design)) principles, principles that I will mention several times in my next articles. Being able to inject dependencies efficiently plays a key role and that’s why I eventually decided to implement an IoC container.

Before discussing the example I built on purpose to show the features of my IoC container, I want to share my experience with other IoC containers I used before writing mine. As a game developer, the Inversion of Control concept was unknown to me, although I surely used IoC without knowing what it was and what it was called.

### My experience with other IoC containers

When I was introduced to the concept of **Dependency Injection**, the IoC containers were already extensively used to ease our code tasks. That’s why, when I shifted from traditional C++ *OOP *to event-based programming in *Actionscript*, I started to use * Robotlegs*. Robotlegs was an IoC Container for AS3 language.

After I used it for a couple of small personal projects, I decided to abandon it. This is because eventually, I ended up realising that manual Dependency Injection was a better practice. However, after some time, when I moved to C#, I started to experiment with [Ninject](http://www.ninject.org/) and after discussing the practices with its author, I realised that I was not appreciating the use of an IoC container because I did not understand its principles *1.

To understand how to use an IoC container, I need to introduce some concepts first:

#### Composition Root

[Composition Root](http://blog.ploeh.dk/2011/07/28/CompositionRoot.aspx) is a key concept to understand. The* Composition Root* is where the IoC container must be initialized before everything else start to use it. Since an application could use several contextualised containers, it could have more composition roots as well. The Composition Root is found in every application that has a main entry point, however, Unity doesn’t really have a single entry point that allows objects to be initialized and this is actually quite simply the real cardinal issue of the whole Unity code design. Since it’s of such significant importance, I will come back to this concept several times in my next articles. I continue using the concept of Composition Root even with Svelto.ECS.

#### Dependency Graph

Once objects are used inside other objects, they start to form a graph of dependencies. Let’s say that there is a *class A* and a *class B*, then there is a* class C* that uses *A* and a *class D* that uses *B* and *C*. D cannot work without B and C, C cannot work without A. This waterfall of dependencies is called *Dependency Graph*.

### How to use an IoC Container

If, for the moment, we don’t consider objects that must be created dynamically after the start-up phase, all the dependencies can be solved right at the beginning of the application, within the Composition Root context.

When I started to use IoC containers, my first mistake was to misunderstand their use. I didn’t realise that the container would have taken the responsibility of creating dependencies away from me. I just couldn’t imagine a design where I would stop using the *new* keyword to create dependencies. If we didn’t use an IoC container, this would mean that all the dependencies would be created and initially passed only from the Composition Root. With an IoC container instead, the creation and injection of dependencies work in a different way, as I will soon show to you. If you haven’t grasped the meaning of this paragraph yet, don’t worry, I will return to this with more examples in my next articles.

Let’s take a look at what a *Composition Root* could look like using an IoC container with the following example:

void SetupContainer() { container = new IoCContainer(); //interface is bound to a specific instance container.Bind<IGameObjectFactory>().AsSingle(new GameObjectFactory(container)); //interface is bound to a specific implementation, the same instance will be used once created container.Bind<IMonsterCounter>().AsSingle<MonsterCountHolder>(); container.Bind<IMonsterCountHolder>().AsSingle<MonsterCountHolder>(); //once the dependency is requested, a new instance will be created container.Bind<WeaponPresenter>().ToFactory(new MultiProvider<WeaponPresenter>()); container.Bind<MonsterPresenter>().ToFactory(new MultiProvider<MonsterPresenter>()); container.Bind<MonsterPathFollower>().ToFactory(new MultiProvider<MonsterPathFollower>()); //once requested, the same instance will be used container.BindSelf<UnderAttackSystem>(); container.BindSelf<PathController>(); }

the* container *object is not used in any other part of the example, except for *Factories*. the *Factory pattern* is a special case and I will explain it later.

What is happening? Inside the *SetupContainer* method, all dependency types are registered into the container. With the method Bind, I am telling the container that every time a dependency of a known type is found, it must be solved with an instance of the type bound to it. The dependencies are solved lazily (that means only when needed) through the metatag *[Inject].*

The application flow starts from this method:

void StartGame() { //tickEngine could be added in the container as well //if needed to other classes! UnityTicker tickEngine = new UnityTicker(); tickEngine.Add(container.Inject(new MonsterSpawner())); tickEngine.Add(container.Build<UnderAttackSystem>()); }

After the *MonsterSpawner* is built, it will have the dependency *IMonsterCounter *injected because it has been declared as

[Inject] public IMonsterCounter monsterCounter { set; private get; }

and because *IMonsterCounter* has been previously registered and bound to a valid implementation (*MonsterCountHolder*) inside the container. In its turn, if the *MonsterCounterHolder *class* *has some other tagged dependencies, they would be injected as well and so on…

In a complicated project scenario, this system will eventually give the impression that the *[Inject]* metatag becomes a sort of magic keyword able to solve automatically our dependencies. Of course, there is nothing magic and, differently than Singleton containers, our dependencies will be correctly injected ONLY if they are part of the Dependency Graph.

Compared to the use of a Singleton, an IoC container gives the same flexibility, but without risking wildly using static classes everywhere (and theoretically avoid memory leakings). Dependencies will be correctly injected only if the object that uses them is part of the Dependency Graph. Dependencies can be also injected through interfaces, which allows changing implementations without changing the code that uses them. In fact, it would be enough to swap the *MonsterCounterHolder* with another type that implements *IMonsterCounter* to have new behaviours without changing code in all the places where the dependencies are used.

In reality, you can perform more fancy tasks with an IoC container, as logic can be injected to change how the container decides to solve a dependency, but this is not relevant for this article (just check how many options a modern IoC container provides).

### IoC container and the keyword new

It is called Inversion Of Control because the flow of the objects creation is inverted. The control of the creation is not anymore on the user, but on the framework that creates and injects objects for us. The most powerful benefit behind this concept is that the code will not depend on the implementation of the classes anymore, but always on their abstractions (if interfaces are used). Relying on the abstraction of the classes gives many benefits that can be fully appreciated when practices like refactoring and unit testing are regularly used. all that said, one could ask: if I should not use *new*, how is it possible to create objects dynamically, while the application runs, like for example spawning objects in the game world? As we have seen, the answer is to use *Factories*. Factories, in my design, can use the container to inject dependencies into the object that they create. Factories will be also injected as dependencies, so they can be easily used whenever are needed:

public [IoC.Inject] IBulletFactory bulletFactory { set; private get } void OnBulletMustBeCreated() { add(bulletFactory.Create()); }

Remembering that factories are the only classes that can use the **Container** outside the Composition Root, the *IBulletFactory* *Create* function would look like this:

public IBullet Create() { return container.Inject(new Bullet()); }

In this way the *Bullets *will not just be created, but all their dependencies regularly injected, in run-time.

If you wonder why your classes should not be able to create objects on their own, remember that this is not overengineering, this is *separation of concerns*. Creating bullets and handling them are two different responsibilities.

### IoC container and Unity

The use of an IoC container, similar to the one I am showing in this article, will help to shift the code patterns from intensive use of **Monobehaviour **to the use of normal classes that implement interfaces.

A **MonoBehaviour**, in its pure form, is a useful tool and its use must be encouraged when appropriate. Still, our Monobehaviours may need dependencies that must be injected. If the MonoBehaviours are created dynamically through a factory, as it should happen most of the time, then the dependencies are solved automatically. On the other hand, if MonoBehaviours are created implicitly by Unity (Gameobject on the scene), their dependencies cannot be solved within the Composition Root because of the nature of the Unity Framework.

Although in my example the turrets are not created dynamically, their dependencies are automatically solved by the IoC Container during the **Awake **time and before any **Start** function is called. The trick is to use a GameObject with the IoC container MonoBehaviour as the root of all the GameObjects that need dependencies injected. The IoC container then looks for the Monobehaviours children of the *Context *GameObject, and will fulfil their dependencies.

This is a good reason to use an IoC container in Unity, however, the same Context trick can be used with other patterns (which I proved with the *Svelto.ECS*)

### IoC Container and MVP

IoC container becomes also very useful when patterns like the Model-View-Presenter (MVC and MVVM included) are used. Explaining the importance of using patterns like MVP to develop GUIs is not part of the scope of this article. However, you must know that MVP is great to separate the logic from data from their visual representation. With Unity, A GameObject would just handle the visual aspect of the entity, while a Presenter would handle the logic. This would look more or less like this:

class View:Monobehaviour, IView { [Inject] public IPresenter presenter { private get; set; } void Start() { presenter.SetView(this); //from now on the presenter can use the public function of this Monobehaviour } }

### IoC Container and hierarchical containers

A proper IoC container library should support hierarchical containers, without this fundamental feature, using an IoC library extensively can quickly degenerate into spaghetti code as I will explain later in my next articles. It’s bad practice to just bind every possible dependency in a single container, as this won’t promote separation of concerns. For example, if we create dependencies for an MVP based GUI, these dependencies could possibly make sense only for the GUI layer of the application. This would mean that the GUI should be handled by a specialised GUI context. Hierarchical containers are powerful because, while they encapsulate the dependencies needed for a specific context, they will also inherit dependencies from parent containers.

### IoC Container and Unit Tests

Often the IoC container concept is associated with Unit Tests, however, there isn’t any direct link between the two practices although using an IoC container will help in writing testable code.

Unit tests must test exclusively the code of the testing class and never its dependencies. An IoC container will make it very simple to inject harmless stubs of dependencies that cannot ever break or affect the functionality of the code to test. This can happen thanks to the use of interfaces and the mockup is just one different (often empty) implementation used for the scope of the tests only.

### Conclusion

before to conclude, I want to quote two answers I found on **StackOverflow **that could help to solve some other doubts:

from [http://stackoverflow.com/a/2551161](http://stackoverflow.com/a/2551161)

The important thing to realize here is that you can (and should) write your code in a DI-friendly, but container-agnostic manner.

This means that you should always push the composition of dependencies to a point where you can’t possibly defer it any longer. This is called the Composition Root and is often placed in near the application’s entry point.

If you design your application in this way, your choice of DI Container (or no DI Container) revolves around a single place in your application, and you can quickly change strategy.

You can choose to use Poor Man’s DI if you only have a few dependencies, or you can choose to use a full-blown DI Container. Used in this fashion, you will have no dependency on any particular DI Container, so the choice becomes less crucial in terms of maintainability.

A DI Container helps you manage complextity, including object lifetime. Used like described here, it doesn’t do anything you couldn’t write in hand, but it does it better and more succinctly. As such, my threshold for when to start using a DI Container would be pretty low.

I would start using a DI Container once I get past a few dependencies. Most of them are pretty easy to get started with anyway.


and from [http://stackoverflow.com/a/2066827](http://stackoverflow.com/a/2066827)

Pure encapsulation is an ideal that can never be achieved. If all dependencies were hidden then you wouldn’t have the need for DI at all. Think about it this way, if you truly have private values that can be internalized within the object, say for instance the integer value of the speed of a car object, then you have no external dependency and no need to invert or inject that dependency. These sorts of internal state values that are operated on purely by private functions are what you want to encapsulate always.

But if you’re building a car that wants a certain kind of engine object then you have an external dependency. You can either instantiate that engine — for instance new GMOverHeadCamEngine() — internally within the car object’s constructor, preserving encapsulation but creating a much more insidious coupling to a concrete class GMOverHeadCamEngine, or you can inject it, allowing your Car object to operate agnostically (and much more robustly) on for example an interface IEngine without the concrete dependency. Whether you use an IOC container or simple DI to achieve this is not the point — the point is that you’ve got a Car that can use many kinds of engines without being coupled to any of them, thus making your codebase more flexible and less prone to side effects.

DI is not a violation of encapsulation, it is a way of minimizing the coupling when encapsulation is necessarily broken as a matter of course within virtually every OOP project. Injecting a dependency into an interface externally minimizes coupling side effects and allows your classes to remain agnostic about implementation.


**Final Notes**

2022 note: I wrote this article in 2012, the next articles in the series show the evolution of my thoughts since. What you should take from this article is that the most difficult challenge in OOP, which coincides with the most obvious design flaw of the paradigm, is solving inter objects communication. IoC containers were created to alleviate the problem, but while the principles behind it are SOLID, the tool itself is not and in fact, I have stopped to use them since 2015. IoC containers may still be useful for pure GUI based applications, but they 100% lead to spaghetti code if used to develop videogame codebases.

I wrote more articles on the subject to investigate further the concept of Inversion of Control. If you are interested, read my new articles starting about the [Truth behind Inversion of Control](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-i-dependency-injection/)

I strongly suggest to read all my articles on the topic:

[http://www.sebaslab.com/ioc-container-for-unity3d-part-1/](http://www.sebaslab.com/ioc-container-for-unity3d-part-1/)[http://www.sebaslab.com/ioc-container-for-unity3d-part-2/](http://www.sebaslab.com/ioc-container-for-unity3d-part-2/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-i-dependency-injection/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-i-dependency-injection/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-ii-inversion-of-control/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-ii-inversion-of-control/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/)[http://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/](http://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/)

*1 Funnily enough, after 3 years of using IoC containers and deeply understanding them I again decided that manual injection was a better practice *to develop videogames* and abandoned IoC containers for good.

Super-interesting again. I’m still super-busy right now, but I can’t wait to try this on a simple game.

Thanks for the article, I have been thinking about how to apply DI to Unity as well. Looking forward to more in the series.

Hi and thank you for the comment. I am not planning to write other articles on the topic (I have so many other things I want to talk about), however if you have some other feedbacks or something else you want to discuss, let me know.

Since you mentioned you’re done with this topic, and if we had “something else to discuss”, I would vote for an article about using Entity Systems in Unity.

Ah, well…Unity adopts already the Entity Framework concept …however in my example I showed how a “System” can be introduced (the monsterSystem) which can act as mediator on all the monsters.

Hey, very nice articles, that’s exactly what I was looking for, since I come from Flash, huge social games, and I always used Robotlegs or Parsley. Switching to Unity was good but at the same time frustrating to see how “primitive” the software architecture of most of the games out there are.

What is you opinion about this IoC framework?

http://www.ninject.org/

I came across this framework from the post on this blog:

http://outlinegames.com/2012/08/29/on-testability/

I’d like to hear your thoughts on that, you can send me an e-mail if possible, thanks a lot!

Ninject is cool (I have talked about it in the article), but it does not work in Unity out of the box. The guy from the article you linked managed to port it, but the problem for me is that the code behind it is too complicated and I wanted to keep it simple!

I tried downloading you project from Github and running in Unity 4, but when I open the scene “Testharness” and run it, I get the error message “The referenced script on this Behaviour is missing!”

How are you running it? Unity 3.5? MonoDevelop built-in or 3.0?

Thanks!

Hello, it works fine in Unity 4. Please download the asset of the example from here: https://github.com/downloads/sebas77/Lightweight-IoC-Container-for-Unity3D/ioccontainerexampleasset.unitypackage Testharness is a dummy scene, I am going to remove it from the repository. I hope it will work for you and you can give me some feedback.

Ah, I never tried it on Unity 4.0, I’ll do it as soon as I can. I have the suspect that something went wrong with the meta files (maybe the are incompatible) and so you lost all the links. I will check it asap!

Hey. I was very interested in this but I get the same error as Rafael.“The referenced script on this Behaviour is missing!”

I use Unity 3.5. As I understand it, I don’t see any scripts in the unitypackage what so ever. Isn’t that the real issue?

Would be really cool to see your example!

Kind regardsm,

Niklas

Nvm my comment. You have to download the source from GitHub first. Got it working.

oh yeah, sorry about that, I left the code outside the asset so I can update it in future. Please let me know what you think about it 🙂

Hey, I began using your framework, and it’s been making my life much easier. But I’m having problems when I load a new Scene. The “game context” where I setup the container and make all bindings is on the “MainScene”, and it gets destroyed when I switch to another scene. Even using DontDestroyOnLoad doesn’t help.

How do you setup your project if you need to load/unload scenes? Thank you!

Good question. I honestly do not like the idea to keep the container alive through the levels, it can easily create memory leaks. In our (big) project the idea is pretty simple, the container is setup in one .cs file that is linked to one gameobject present in each level. That means that we actually want the container to be destroyed and recreated everytime. This is ok for us, because our data is not meant to be permanent among the levels, is this a problem for you? Let’s discuss it, it is possible that I did not think through it.

I’m working at Wooga with social/mobile games, and from experience it’s fundamental that we have access to the container at anytime, we usually have persistent information across levels. And regarding memory leak, I think it will not be a problem, since there is only “models” and “controllers” stored in the container, low memory usage. All the heavy “view” related stuff that really consumes memory (like textures, sprite-sheets, etc) can be destroyed whenever you load/unload scenes. I managed to make it work now, I just made the container a static class. In every scene I have a MonoBehaviour object called “GameInit”… Read more »

At the end of the day use what suits you best, but I suggest you to try my solution as well and see if you like it (static Model for permanent data)

Thanks for the feedback. Using the container as a static class defeats the purpose of the inversion of control container design itself, because it practically becomes a service locator. This is what I suggest you to do: Assuming that you do not have much data to be persistent and this data is unique (like the user inventory, energy and stuff like that), use a class like this to bind in the container: class UserInventoryController { static UserInventoryModel userInventoryModel; } your container is not static, your UserInventoryController is not static and can be injected, but the data inside is static and… Read more »

And in the the “GameInit : Monobehaviour” I do this:

if (StaticGameContext.GameAlreadyInitialized)

{

Destroy(this);

return;

}

StaticGameContext.Init();

Sorry, I made the GameContext static, not the Container. Here is the code I’m using for the context: using IoC; using UnityEngine; internal class AppRoot : IContextRoot { public IContainer container { get; private set; } public void Setup() { container = new IoC.UnityContainer(); container.Bind().AsSingle(); container.Bind().AsSingle(); container.Bind().AsSingle(); } } static public class StaticGameContext { public static bool GameAlreadyInitialized; private static AppRoot _applicationRoot; static public void Init() { if (GameAlreadyInitialized) { D.error(“Game Context Already Initialized!”); return; } _applicationRoot = new AppRoot(); _applicationRoot.Setup(); GameAlreadyInitialized = true; } static public void InjectMonoBehaviour(MonoBehaviour script) { DesignByContract.Check.Require(_applicationRoot != null && _applicationRoot.container != null, “Container not… Read more »

Good Article,

Now I know why you write your own IOC,

I’m trying to learn to write better code as mine is what’s the word rubbish, so may give your IOC a test drive. Still trying to get my head around Agile and Solid principles so its nice to have come across your articles.

I’m also looking to use BDD which i’m thinking may be a good fit for games have you tried user stories with Unity3d

Hi Peter,

I never tried BDD, not even TDD. For the time being I am stuck with normal unit testing, since I am still perplexed about the whole thing.

Hi, i am starting my project to the faculty and i got interested in your work. Did you try to use spring.net framework? Is it possible to use XML to initilize objects.

I am interested to in the features of permanent data thought scenes too.

Hello, thanks for your comment. Most of the c# IoC libraries do not work in Unity3D. I know about the XML feature, but it was not something important for me to implement. However the code is opensource, maybe someone could improve it in future 🙂

Thanks for your quick reply and good luck for your project

Hi! I managed to use your framework in my project in a simple and fairly intuitive maner. I just could not put the container persistent through the levels. This feature interested me a lot since i am initializing a set of objects and configuration managers through XML and i wished they were available throughout the various levels. Maybe the problem is in the design of my application due to my lack of experience. My initial approach used a singleton that persisted through various levels, but your solution is much more cleaver and clean however the solution using static attributes does not… Read more »

Hi,

Transforming the container in to a singleton hides a big risk of memory leaking. This is the only thing you need to be aware of.

I did not think about a way to use an xml configurator, but I bet it would be easy enough to implement (using reflection).

Hi, great articles, I was looking for DI framework for Unity, plus some theory in IoC, for a while now and this seems like exactly what I wanted. My concern is about performance of the code, as I and our team are pure game developers, we are always worried about it, so we try not to rely on interfaces or getters/setters and use more “accesible” code like public variables or static classes, etc. So you can imagine that trying to introduce a new paradigm like this in a team not used to these techniques can be very difficult. What are… Read more »

Hello and thanks for the comment.

Most of the injections happen during the initialization phase so performance should not be an issue. However it is true that injection could happen anytime using factories as well.

Since my IoC relies on reflection and I did not write any caching method to speed up the injection of known types, I would not use IoC factories to create/inject objects while the game runs, unless it happens sporadically.

Hi, Sebastiano!

I tried to use your DI container, but looks like I miss something …

In this sample I am trying to create two different objects:

public class SimpleClass

{

public Guid _id = Guid.NewGuid();

}

[TestMethod]

public void TestBuild()

{

var container = new UnityContainer();

container.Bind().AsSingle();

var obj1 = container.Build();

var obj2 = container.Build();

Assert.AreNotEqual(obj1._id, obj2._id);

}

The test fails. So, all objects build by container are singletones?

Could you please explain me this behaviour?

Thank you in advance

Sorry, looks like all signs ‘greater’ and ‘less’ were eaten by blog engine.

In my test I am trying to create two SimpleClass objects one by one.

container.Build() returns the same instance twice

Thanks for the comment, this is indeed the intended behavior…that’s why it is called AsSingle! (btw they are not singletons, they are just the same instance)

if you want different instance of the same class, you should use factories…let me know if you need an example.

Hi, Sebastiano

Thank your article, i am studies this framework and try to using in my project, now.

I hope to know how to use factories in your container, is it like your MonsterFactory in the example, or have other method to do?

If there has another method, can you give me the example?

the library is quite flexible, but the example is good to follow.

When I find the time to update the library, I will add more examples!

Hi Sebastiano, I just started coding with Unity3D (only about a week in), but it only took me a couple days to realize that I needed a DI container of some sort. So I’m very happy to have found your project! This looks like a big step in the right direction. I haven’t used Ninject before, but I have used Castle Windsor extensively with my business development MVVM / MVC style projects. So I do know how complex it can be considering that these containers not only handle instantiating objects, but that they also manage the “lifetime” of the objects… Read more »

Hello Jordan, thanks for the feedback. Since you are new to Unity I have to highlight that the real reason why I needed an IoC container is the lack of a proper way to inject dependencies inside monobehaviour objects in Unity. Of course, with the introduction of a composition root, I am also able to avoid to use monobehaviour objects when they are not needed. The original version of Ninject does not work in Unity, Uninject should, but when it came out my version was already enough. Point is that I am working on a relatively big project and I… Read more »

Well I have 1 feature idea, don’t know if it is already available in your IoC container or in Ninject but may be usefull:

When a container is destroyed it may print a log of wich dependencies are not used. If codebase is wellwritten and everything is concern separated, it is likely that after some refactoring (maybe removing a dependency) the log shows that some classes were not used.

Hi my name is Antonio Zamora and I’m very interested in game programming patterns. I would really like to share my thoughts with you (I’m not an native speaker so please excuse my english). As you I have worked with robotlegs before and I praised the philosophy it had. I loved actionscript and I felt very good working with the adobe platform. But later adobe seemed to take some bad decisions that I didnt share so I searched for a new place to look at. I discovered unity and I liked the whole idea of gameobjects. As you mention the… Read more »

the idea is to create as simple as possible monobehaviours and add as many as you need. So let them do just one thing, if you need 10 different things, use 10 different components on the same GameObject. For the MVC (or better MVVM) pattern is a little bit more complicated due to the Unity limitations, but it is still doable. My idea is that the Monobehaviour becomes the view or the model, sometimes both and a presenter is injected in to it. The view redirects the events (awake, start, update, oncollision, onmousedown etc..) to the presenter (controller or viewmodel)… Read more »

Great article! Thanks for your work. Unity 3D has many specific features and you offered amazing ideas and tools for resolve it. I used a Singleton approach before (DI ideas) as a start as a single way to manage objects but for complex projects such way is fall down road. Also, you are right concerning MonoBehavior using without any appropriate foundation.

Agree!

Unity 3D Platform Lead at XIM Wireless

[…] http://blog.sebaslab.com/ioc-container-for-unity3d-part-2/ […]

Hello, Sebastiano.

I’ve written IoC container my self, and I’m interested what you’ll say about it. Main goal is that it has been written as simple and short as occam razor could leave it, Yet it still provides basic IoC features.

https://github.com/sergeysychov/behaviour_inject

thanks, very good, I may use your code to inject through constructor, since I have never found the time to finish it 🙂

I am overwhelmed by the star count of Unity IoC container-related GitHub repositories, which forces me to use them, but I always end up concluding that I don’t need them. Also, I would have died from the immense pain if I had to create a GUI application without an IoC container. lol