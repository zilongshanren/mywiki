---
title: Svelto ECS is now production ready - Seba's Lab
url: https://www.sebaslab.com/ecs-1-0/
author: Sebastiano Mandalà
published: '2016-05-21'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

**Note: this article is now outdated as Svelto.ECS 2.0 is out. Read it to have a complete picture on the concepts, but the most up to date information **[can be found now here.](http://www.sebaslab.com/learning-svelto-ecs-by-example-the-survival-example/)

**Note: in this article you will meet the term ****Node**** which has been superseded by the term ****Entity View****.**

**Note: this version of Svelto ECS didn’t include the concept of EntityStructs, therefore the following code overuse implementors when they are actually not needed. **

Six months passed since my last article about [Inversion of Control and Entity Component System](http://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/) and meanwhile I had enough time to test and refine my theories, which have been proven to work well in a production environment. As result Svelto.ECS framework is now ready to use in a professional setup.

Let’s start from the basics, explaining why I use the word framework. My previous work, *Svelto.IoC*, cannot be defined as a framework; it’s instead a tool. As a tool, it helps to perform *Dependency Injection* and design your code following the *Inversion of Control principle*. Svelto.IoC is nothing else, therefore whatever you do with it, you can do without it in a very similar way, without changing much the design of your code. As such, svelto IoC doesn’t dictate a way of coding, doesn’t give a paradigm to follow, leaving to the coder the burden to decide how to design their game infrastructure.

Svelto.ECS won’t take the place of Svelto.IoC, however it can be surely used without it. ~~My intention is to add some more features to my IoC container in future~~, but as of now, I would not suggest to use it, unless you are aware of what Inversion of Control *actually* means and that you are *actually* looking for an IoC container that well integrates with your existing design (like, for example, a MVP based GUI framework). Without understanding the principles behind IoC, using an IoC container can result in very dangerous practices. In fact I have seen code smells and bad design implementations that actually have been assisted by the use of an IoC container. These ugly results would have been much harder to achieve without it.

Svelto.ECS is a framework and with it you are forced to design your code following its specifications. It’s the framework to dictate the way you have to write your game infrastructure. The framework is also relatively rigid, forcing the coder to follow a well defined pattern. Using this kind of framework is important for a medium-large team, because coders have different levels of experience and it is silly to expect from everyone to be able to design well structured code. Using a framework, which implicitly solves the problem to design the code, will let the team to focus on the implementation of algorithms, knowing, with a given degree of certainty, that the amount of refactoring needed in future will be less than it would have been if left on their own.

The first error I made with the pre-release implementation of this framework was to not define clearly the concept of *Entity*. I noticed that it is very important to know what the elements of the project are before to write the relative code. *Entities*, *Components*, *Engines* and *Nodes* must be properly identified in order to write code faster. An *Entity* is actually a fundamental and well defined element in the game. The *Engines* must be designed to manage *Entities* and not *Components*. Characters, enemies, bullets, weapons, obstacles, bonuses, GUI elements, they are all Entities. It’s easier, and surely common, to identify an Entity with a view, but a view is not necessary for an Entity. As long as the entity is well defined and makes sense for the logic of the game, it can be managed by engines regardless its representation.

In order to give the right importance to the concept of Entity, Nodes cannot be injected anymore into Engines until an Entity is explicitly built. An Entity is now built through the new *BuildEntity* function and the same function is used to give an ID to the Entity. The ID doesn’t need to be globally unique, this is a decision left to the coder. For example as long as the ID of all the bullets are unique, it doesn’t matter if the same IDs are used for other entities managed by other engines.

**The Setup**

Following the [example](https://github.com/sebas77/Svelto-ECS-Example), we start from analyzing the **MainContext **class. The concept of *Composition Root*, inherited from the Svelto IoC container, is still of fundamental importance for this framework to work. It’s needed to give back to the coder the responsibility of creating objects (which is currently the greatest problem of the original Unity framework, as explained in my other articles) and that’s what the Composition Root is there for. By the way, before to proceed, just a note about the terminology: while I call it Svelto Entity Component System framework, I don’t use the term *System*, I prefer the term *Engine*, but they are the same thing.

In the composition root we can create our ECS framework main Engines, Entities, Factories and Observers instances needed by the entire context and inject them around (a project can have multiple contexts and this is an important concept).

In our example, it’s clear that the amount of objects needed to run the demo is actually quite limited:

void SetupEnginesAndComponents() { _tickEngine = new UnityTicker(); _entityFactory = _enginesRoot = new EnginesRoot(_tickEngine); GameObjectFactory factory = new GameObjectFactory(); var enemyKilledObservable = new EnemyKilledObservable(); var scoreOnEnemyKilledObserver = new ScoreOnEnemyKilledObserver((EnemyKilledObservable)enemyKilledObservable); AddEngine(new PlayerMovementEngine()); AddEngine(new PlayerAnimationEngine()); AddEngine(new PlayerGunShootingEngine(enemyKilledObservable)); AddEngine(new PlayerGunShootingFXsEngine()); AddEngine(new EnemySpawnerEngine(factory, _entityFactory)); AddEngine(new EnemyAttackEngine()); AddEngine(new EnemyMovementEngine()); AddEngine(new EnemyAnimationEngine()); AddEngine(new HealthEngine()); AddEngine(new DamageSoundEngine()); AddEngine(new HUDEngine()); AddEngine(new ScoreEngine(scoreOnEnemyKilledObserver)); }

The **EngineRoot** is the main Svelto ECS class and it’s used to manage the Engines. If it’s seen as **IEntityFactory**, it will be used to build Entities. **IEntityFactory** can be injected inside Engines or other Factories in order to create Entities dynamically in run-time.

It’s easy to identify the Engines that manage the *Player Entity*, the *Player Gun Entity* and the *Enemies Entities*. The **HealthEngine** is an example of generic Engine logic shared between specialized Entities. Both Enemies and Player have health, so their health can be managed by the same engine. **DamageSoundEngine** is also a generic Engine and deals with the sounds due to damage inflicted or death. **HudEngine** and **ScoreEngine **manage instead the on screen FX and GUI elements.

I guess so far the code is quite clear and invites you to know more about it. Indeed, while I explained what an *Entity* is, I haven’t given a clear definition of *Engine*, *Node* and *Component* yet.

An Entity is defined through its *Components *interfaces and the* Implementors* of those components. A Svelto ECS Component defines a *shareable contextualized collection of data. *A Component can exclusively hold data (through properties) and nothing else. How the data is contextualized (and then grouped in components) depends by how the entity can been seen externally. While it’s important to define conceptually an Entity, an Entity does not exist as object in the framework and it’s seen externally only through its components. More generic the components are, more reusable they will be. If two Entities need health, you can create one **IHealthComponent**, which will be implemented by two different Implementers. Other examples of generic Components are **IPositionComponent**, **ISpeedComponent**, **IPhysicAttributeComponent** and so on. Component interfaces can also help to reinterpret or to access the same data in different ways. For example a Component could only define a getter, while another Component only a setter, for the same data on the same Implementor. All this helps to keep your code more focused and encapsulated. Once the shareable data options are exhausted, you can start to declare more entity specific components. Bigger the project becomes, more shareable components will be found and after a while this process will start to become quite intuitive. Don’t be afraid to create components even just for one property only as long as they make sense and help to share components between entities. More shareable components there are, less of them will be needed to create in future. However it’s wise to make this process iterative, so if initially you don’t know how to create components, start with specialized ones and the refactor them later.

The data held by the components can be used by engine through polling and pushing. This something I have never seen before in other ECS framework and it’s a very powerful feature, I will explain why later, but for the time being, just know that Components can also dispatch events through the *DispatcherOnChange and DispatcherOnSet* classes (you must see them as a sort of Data Binding feature).

The Implementer concept was existing already in the original framework, but I didn’t formalize it at that time. One main difference between Svelto ECS and other ECS frameworks is that Components are not mapped 1:1 to c# objects. Components are always known through Interfaces. This is quite a powerful concept, because allows Components to be defined by objects that I call Implementers. This doesn’t just allow to create less objects, but most importantly, helps to share data between Components. Several Components can been actually defined by the same Implementer. Implementers can be *Monobehaviour*, as Entities can be related to *GameObjects*, but this link is not necessary. However, in our example, you will always find that Implementers are Monobehaviour. This fact actually solves elegantly another important problem, the communication between Unity framework and Svelto ECS.

Most of the Unity framework feedback comes from predefined Monobehaviour functions like **OnTriggerEnter** and **OnTriggerExit**. One of the benefit to let Components dispatch events, is that the communication between the Implementer and the Engines become seamless. The Implementer as Monobehaviour dispatches an *IComponent* event when *OnTriggerEnter* is called. The Engines will then be notified and act on it.

It’s fundamental to keep in mind that Implementers MUST NOT DEFINE ANY LOGIC. They must ONLY implement component interfaces, hold the relative states and act as a bridge between Unity and the ECS framework in case they happen to be also Monobehaviours.

So far we understood that: Components are a collection of data, Implementers define the Components and don’t have any logic. Hence where all the game logic will be? All the game logic will be written in Engines and Engines only. That’s what they are there for. As a coder, you won’t need to create any other class. You may need to create new Abstract Data Types to be used through components, but you won’t need to use any other pattern to handle logic. In fact, while I still prefer MVP patterns to handle GUIs, without a proper MVP framework, it won’t make much difference to use Engines instead. Engines are basically presenters and Nodes hold views and models.

OK, before to proceed further with the theory, let’s go back to the code. We have easily defined Engines, it’s now time to see how to build Entities. Entities are injected into the framework through Entity Descriptors. The **EntityDescriptor** describes entities through their Implementers and present them to the framework through Nodes. For example, every single Enemy Entity, is defined by the following **EnemyEntityDescriptor**:

class EnemyEntityDescriptor : EntityDescriptor { static readonly INodeBuilder[] _nodesToBuild; static EnemyEntityDescriptor() { _nodesToBuild = new INodeBuilder[] { new NodeBuilder<EnemyNode>(), new NodeBuilder<PlayerTargetNode>(), new NodeBuilder<HealthNode>(), }; } public EnemyEntityDescriptor(IComponent[] componentsImplementor):base(_nodesToBuild, componentsImplementor) {} }

This means that an Enemy Entity and its components will be introduced to the framework through the nodes **EnemyNode**, **PlayerTargetNode** and **HealthNode** and the method **BuildEntity** used in this way:

_entityFactory.BuildEntity(ID, new EnemyEntityDescriptor(new EnemyImplementor()));

While** EnemyImplementor** implements the **EnemyComponents**, the **EnemyEntityDescriptor** introduces them to the Engines through the relative Enemy Nodes.** **Wow, it seems that it’s getting complicated, but it’s really not. Once you wrap your head around these concepts, you will see how easy is using them. You understood that Entities exist conceptually, but they are defined only through components which are implemented though Implementers. However you may wonder why nodes are needed as well. While Components are directly linked to Entities, Nodes are directly linked to Engines. Nodes are a way to map Components inside Engines. In this way the design of the Components is decoupled from the Engines. If we had to use Components only, without Nodes, often it could get awkward to design them.

Should you design Components to be shared between Entities or design Components to be used in specific Engines? Nodes rearrange group of components to be easily used inside Engines. Specialized Nodes are used inside specialized Engines, generic Nodes are used inside generic Engines. For example: an Enemy Entity is an **EnemyNode** for Enemy Engines, but it’s also a **PlayerTargetNode** for the **PlayerShootingEngine**. The Entity can also be damaged and the **HealthNode** will be used to let the **HealthEngine** handle this logic. Being the **HealthEngine** a generic engine, it doesn’t need to know that the Entity is actually an Enemy. different and totally unrelated engines can see the same entity in totally different ways thanks to the nodes. The Enemy Entity will be injected to all the Engines that handle the **EnemyNode**, the **PlayerTargetNode** and the **HealthNode** Nodes. It’s actually quite important to find Node names that match significantly the name of the relative Engines.

As we have seen, entities can easily be created explicitly in code passing a specific *EntityDescriptor* to the *BuildEntity* function. However, some times, it’s more convenient to exploit the polymorphism-like feature given by the *IEntityDescriptorHolder* interface. Using it, you can attach the information about which EntityDescriptor to use directly on the prefab, so that the EntityDescriptor to use will be directly taken from the prefab, instead to be explicitly specified in code. This can save a ton of code, when you need to build Entities from prefabs.

So we can define multiple IEntityDescriptorHolder implementations like:

[DisallowMultipleComponent] public class PlayerEntityDescriptorHolder:MonoBehaviour, IEntityDescriptorHolder { EntityDescriptor IEntityDescriptorHolder.BuildDescriptorType() { return new PlayerEntityDescriptor(GetComponentsInChildren<IComponent>()); } } public class EnemyEntityDescriptorHolder:MonoBehaviour, IEntityDescriptorHolder { EntityDescriptor IEntityDescriptorHolder.BuildDescriptorType() { return new EnemyEntityDescriptor(GetComponentsInChildren<IComponent>()); } }

and use them to create Entities implicitly, without needing to specify the descriptor to use, since it can be fetched directly from the prefab (i.e.: playerPrefab, enemyPrefab):

GameObject go = gameObjectFactory.Build(currentPrefab); engineRoot.BuildEntity(go.GetInstanceID(), go.GetComponent<IEntityDescriptorHolder>().BuildDescriptorType());

Once Engines and Entities are built, the setup of the game is complete and the game is ready to run. The coder can now focus simply on coding the Engines, knowing that the Entities will be injected automatically through the defined nodes. If new engines are created, is possible that new Nodes must be added, which on their turn will be added in the necessary Entity Descriptors.

**Note though:** with experience I realized that it’s better to use monobehaviours as implementors to build entity ONLY when strictly needed. This means only when you actually need engines to communicate with the Unity engine through the implementors. Avoid this otherwise, for example, do not use Monobehaviours as implementers because your monobehaviours act as data source, just read the data in a different way. Keep your code decoupled from unity as much as you can.

**The Logic in the Engines**

the necessity to write most of the original boilerplate code has been successfully removed from this version of the framework. An important feature that has been added is the concept of **IQueryableNodeEngine**. The engines that implement this interface, will find injected the property

public IEngineNodeDB nodesDB { set; private get; }

This new object removes the need to create custom data structures to hold the nodes. Now nodes can be efficiently queried like in this example:

public void Tick(float deltaSec) { var enemies = nodesDB.QueryNodes<EnemyNode>(); for (var i = 0; i < enemies.Count; i++) { var component = enemies[i].movementComponent; if (component.navMesh.isActiveAndEnabled) component.navMesh.SetDestination(_targetNode.targetPositionComponent.position); } }

This example also shows how Engines can periodically poll or iterate data from Entities. However often is very useful to manage logic through events. Other ECS frameworks use observers or very awkward “EventBus” objects to solve communication between systems. Event bus is an anti-pattern and the extensive use of observers could lead to messy and redundant code. I actually use observers only to setup communication between Svelto.ECS and legacy frameworks still present in the project. *DispatchOnSet* and *DispatchOnChange* are an excellent solution to this awkward problem as they allow Engines to communicate through components, although the event is still seen as data. Alternatively, In order to setup a communication between engines, the new concept of *Sequencer *has been introduced (I will explain about it later in the notes).

**Conclusions**

I understand that some time is needed to absorb all of this and I understand that it’s a radically different way to think of entities than what Unity taught to us so far. However there are numerous relevant benefits in using this framework beside the ones listed so far. Engines achieve a very important goal, **perfect encapsulation**. The encapsulation is not even possibly broken by events, because the event communication happens through injected components, not through engine events. Engines must never have public members and must never been injected anywhere, they don’t need to! This allows a very modular and elegant design. Engines can be plugged in and out, refactoring can happen without affecting other code, since the coupling between objects is minimal.

Engines follow the** Single Responsibility Principle**. Either they are generic or specialized, they must focus on one responsibility only. The smaller they are, the better it is. Don’t be afraid of create Engines, even if they must handle one node only. Engine is the only way to write logic, so they must be used for everything. Engines can contain states, but they never ever can be entity related states, only engine related states.

Once the concepts explained above are well understood, the problem about designing code will become secondary. The coder can focus on implementing the code needed to run the game, more than caring about creating a maintainable infrastructure. The framework will force to create maintainable and modular code. Concept like “Managers”, “Containers”, Singletons will just be a memory of the past.

*Some rules to remember:*

- Nodes must be defined by the Engine themselves, this means that every engine comes with a set of node(s). Reusing nodes often smells
- Engines must never use nodes defined by other engines, unless they are defined in the same specialized namespace. Therefore an EnemyEngine will never use a HudNode.
- Generic Engines define Generic Nodes, Generic Engines NEVER use specialized nodes. Using specialized nodes inside generic engines is as wrong as down-casting pointers in c++

Please feel free to [experiment with it](https://github.com/sebas77/Svelto-ECS) and give me some feedback.

## Notes from 21/01/2017 Update:

Svelto ECS has been successfully used in Freejam for some while now on multiple projects. Hence, I had the possibility to analyse some weakness that were leading to some bad practices and fix them. Let’s talk about them:

-
- First of all, my apologies for the mass renames you will be forced to undergo, but I renamed several classes and namespaces.


-
- The
*Dispatcher*class was being severely abused, therefore I decided to take a step back and deprecate it. This class is not part of the framework anymore, however it has been completely replaced by*DispatcherOnSet*and*DispatcherOnChange*. The rationale behind it is quite simple, Components must hold ONLY data. The difference is now how this data is retrieved. It can be retrieved through polling (using the get property) or trough pushing (using events). The event based functionality is still there, but it must be approached differently. Events can’t be triggered for the exclusive sake to communicate with another Engine, but always as consequence of data set or changed. In this way the abuse has been noticeably reduced, forcing the user to think about what the events are meant to be about. The class now exposes a get property for the value as well.

- The

- The new
*Sequencer*class has been introduced to take care of the cases where pushing data doesn’t fit well for communication between Engines. It’s also needed to easily create sequence of steps between Engines. You will notice that as consequence of a specific event, a chain of engines calls can be triggered. This chain is not simple to follow through the use of simple events. It’s also not simple to branch it or create loops. This is what the Sequencer is for:

playerDamageSequence.SetSequence( new Steps() //sequence of steps { { //first step enemyAttackEngine, //this step can be triggered only by this engine through the Next function new Dictionary<System.Enum, IStep[]>() //this step can lead only to one branch { { Condition.always, new [] { playerHealthEngine } }, //these engines will be called when the Next function is called with the Condition.always set } }, { //second step playerHealthEngine, //this step can be triggered only by this engine through the Next function new Dictionary<System.Enum, IStep[]>() //this step can branch in two paths { { DamageCondition.damage, new IStep[] { hudEngine, damageSoundEngine } }, //these engines will be called when the Next function is called with the DamageCondition.damage set { DamageCondition.dead, new IStep[] { hudEngine, damageSoundEngine, playerMovementEngine, playerAnimationEngine, enemyAnimationEngine } }, //these engines will be called when the Next function is called with the DamageCondition.dead set } } } );

This example covers all the basics, except the loop one. To create a loop would be enough to create a new step that has as target an engine already present as starting point of an existing step.

A Sequence should be created only inside the context or inside factories. In this way it will be simple to understand the logic of a sequence of events without investigating inside Engines. The sequence is then passed into the engines like it happens already with observables and used like this:

void TriggerDamage<T>(ref T damage) where T:IDamageInfo { var node = nodesDB.QueryNode<HealthNode>(damage.entityDamaged); var healthComponent = node.healthComponent; healthComponent.currentHealth -= damage.damagePerShot; if (healthComponent.currentHealth <= 0) { _damageSequence.Next(this, ref damage, DamageCondition.dead); //will proceed with the engines under the condition dead node.removeEntityComponent.removeEntity(); } else _damageSequence.Next(this, ref damage, DamageCondition.damage); //will proceed with the engines under the condition damage }

- The
*IComponent*interface was never used by the framework so I removed it, you can keep on using it for the sake to optimize the GetComponents call in a BuildEntity. - Added a new
*GenericEntityDescriptor*class, now it’s possible to create Descriptors without declaring a new class every time (it depends by the number of nodes used). - Since the
*Tickable*system has been deprecated, the[TaskRunner library](https://github.com/sebas77/Svelto.Tasks)should be used to run loops. TaskRunner comes with a profiler window that can be used to check how long tasks take to run. This has been copied and adapted from the Entitas source code. You can Enable it from the menu Tasks -> Enable Profiler. Similarly you can enable an Engine Profiler from Engine -> Enable profiler to profile adding and remove nodes into Engines. It will look more or less like this:![](../../assets/ae6552e0ef2ef9f3.png)


In future, I may implement some of the following features (feedback is appreciated):

- Entity pooling, so that a removed entity can be reused
- Some standard solution to handle input event in engines
- Using GC handles to keep hold of the Node references, all these references around can make the garbage collection procedure slower

#### Other features introduced:

- INodesEngine interface is now internal (so deprecated for normal use), MultiNodesEngine must be used instead.
- Scheduling of node submission is not responsibility of the
*EnginesRoot*anymore. You can now inject your own node submission scheduler - Entities can now be disabled and enabled, instead of just added and removed. This introduce new engines callbacks that can make simpler to manage entities life.
- GroupEntity has been renamed in to MetaEntity, more comments have been added to explain when to use them. The previous name was misleading.

## Notes from 13/01/2018:

**This article is now closed, but still good for some references.**

Note, if you are new to the ECS design and you wonder why it could be useful, you should read my previous articles:

[http://www.sebaslab.com/ioc-container-for-unity3d-part-1/](http://www.sebaslab.com/ioc-container-for-unity3d-part-1/)[http://www.sebaslab.com/ioc-container-for-unity3d-part-2/](http://www.sebaslab.com/ioc-container-for-unity3d-part-2/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-i-dependency-injection/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-i-dependency-injection/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-ii-inversion-of-control/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-ii-inversion-of-control/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/)[http://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/](http://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/)

Hi Sebastiano, After hitting a wall with a project after about a year’s worth of bolting on new features at the request of a client, I’ve entered dependency hell. I began weighing the pros and cons of a different framework other than what Unity3D’s engine tries to enforce, which led me to your blog. I noticed various other ECS implementations have been mentioned in the comment sections of your articles. What would you say is the primary shortcomings/drawbacks for using other ECS frameworks such as EgoECS and Entitas relative to yours from what you can tell? Do they enforce a… Read more »

I assume you read all my articles on the argument, starting from the IoC ones. I haven’t used EgoECS or Entitas, I assume both are good. My ECS implementation has got 2 unique features, one is the fact that components are not objects and the other one that components can use dispatcher. I also like the Nodes design a lot. I think that communication between systems is the biggest problem to solve in an ECS framework and I usually discard frameworks that solve this problem with an EventBus (a singleton to dispatch messages). We have been using my ECS in… Read more »

May I ask why you didn’t research existing options before developing your solution or just try them later? It seems like a logical step and can add many obvious advantages, especially considering that many other options are open source.

Also may I ask why you changed naming conventions? I believe this just adds extra confusion, especially taking into consideration that the system is pretty complex to wrap your head around? Like Engines – every other ECS calls them Systems, also in ECS it stands for System.

Hey Vlad, I am happy to satisfy your curiosity. My story with my Svelto frameworks goes back to 2012 and there wasn’t much available back then. I was the first one to write an IoC container for Unity and my articles inspired several more successful frameworks, like ZenInject and StrangeIoC. However around 2014-2015 I realized that Inversion of Control Containers were not suitable for game development and in search of a better solution I found my answer in the ECS paradigm. Again there wasn’t much available there that wasn’t just a proof of concept, except Entitas which I always felt… Read more »

Hello, I really admire your Svelto ECS. It’s hard to get your head wrapped around it at first but it is probably the best ECS framework for Unity at the moment with creator who knows what he’s doing exactly. I’m creating a roguelike in Unity and I want to use your system (ECS seems to be perfect fit for such project as everything is modular). However there is much dispute online about handling the game world itself using the ECS. You are an expert/guru in my eyes when it comes to ECS so I wanted to ask you about how… Read more »

Hello and thanks for your message. Let’s be clear, there is a lot of hostility around frameworks that step away from the Unity logic. I don’t want to be too blunt, but the truth is that whatever force you to use stateful global objects must be avoided like the pest. Obviously many of the unity users never really have created something truly complex, so for them tools like IoC containers or frameworks like ECS ones are seen as “over-engineering” since you can get things done also using singletons. While it’s true that you can get things done using whatever you… Read more »

I was a lead programmer in a rather big game project (full time job, not a hobbyist after-hours thing) and I know for sure your system is not “over-engineering”. The project ended up in a total mess of a code, full of managers and singletons (multi-responsibility, thousands of lines of code per class). It wasn’t a problem at the beginning but further in the project it became a nightmare to extend and maintain. I guess that I lost at least 3-6 months fixing/patching/extending/refactoring (then fixing again) because of poor design choices. I would really love to go back in time… Read more »

I don’t see each tile as entity as a proper solution. The map itself is just data, so the data structure of the map can be stored by just one mapComponent. If you go for the Service route, the mapService won’t need any logic. A service is usually a way to query a datastructure, nothing else. The data source of the data structure can be everything (a DB, a file, a datastructure in memory), and the service has only the responsibility to give the functions to query this data. This means that all the logic is still in the engines,… Read more »

I have just ony 1 complaint about SveltoECS is the amount of boiler plate code. Svelto is aimed at really big projects, so as long as you need something that address all the problems that it addresses, I can’t came up with a simpler syntax: every single line of code is needed :/. But let’s assume for a while we are not working on Robocraft(assume I’m in a small team with 6 people working on something that should last for 1/2 years at most): Isn’t there anything we can drop from Svelto in order to allow it become more intuitive… Read more »

Aehm. “>” and “<" template arguments were stripped from my comment :/. And also identation was wrong. However the point was that Implementors are good, I can see and appreciate their advantage, however there are certain behaviours that can be modelled more easily by adding dynamically components at Runtime, and this thing is not allowed with implementors (unless there's somewhere a undocumented feature of Svelto I missed). So while I believe in really big projects it is preferrable to have a Whole different entity for that, I think medium-small projects will benefit more from having separate components that can be… Read more »

Forgive me Dario, it’s a while I don’t play with Svelto.ECS. I changed it quite a lot since the last commit on github and I lost the track of it. I am working on the new github version as we speak. Once I am done, I will re-read your comments and answer them, OK? Please also be aware that, as usual, there will be some (hope minor) breaking changes 🙁

Hi Sebastiano, I have a question, primarily about one the actual code examples above you used and the thinking behind it. Your TriggerDamage method seems to be within the PlayerGunShootingEngine. The method updates the healthcomponent.current health node to indicate it’s been damaged. It then fires the “isDead” or “isDamaged” dispatch to let the other engines (and systems listening) that the entity the component is attached to is either dead or has been damaged. I’m not a professional programmer, so I’m here to learn, but I feel that’s a violation of the S in SOLID. In this scenario, wouldn’t the PlayerGunShootingEngine… Read more »

Hi again Sebastiano, I was just reading through the code in the github project, and it turns out the TriggerDamage method is within the HealthEngine. This is exactly where I would expect it to be and invalidates any of my previous concerns. Reading through the article left me with the feeling that the example code was in PlayerGunShootingEngine, which really didn’t feel right. I’m incredibly glad I got that feeling now, as it means my thinking is in the correct zone. 🙂 Your IOC+ECP framework is exactly the direction I was heading in my own code and I’m going to… Read more »

thanks Robert!

I am updating the github version since it’s quite old. The difficult part will be to remember the changes I made and explain why I made them :). Also I still need to add a fundamental feature, that I will explain later. At last, I have to update the article, since it’s a bit outdated…arggh! Too much work for too few weekends in a year 😀

Hi Sebastiano, I’ve been using it for a few days now and have to say I really like it, it feels neat that once setup I’m just writing engines (whilst only thinking about nodes), AND i get compile errors when I’ve missed a component/node/Implementor etc. One issue i’ve had (which I just created a hack to get around to start with) is this situation: I have a component, it’s job is to represent a producer of items in my game (think Farm creating wheat). It has an event that takes a data object called “ProductData” which just contains a string… Read more »

Hey again,

So after another couple of days learning it turns out that the correct nodes were returned by the nodeDB, I caused the incorrect behaviour when I passed in the ID of the unity component instead of the GameObject when setting up the dispatcher.

I had:

productCreated = new Dispatcher(this.GetInstanceID());

instead of

productCreated = new Dispatcher(gameObject.GetInstanceID());

So I’m happily retrieving nodes from entities now, all good!

Rob.

Great to hear Robert, I promise I will work on it this weekend and if I finish all, I will re read all the comments left so far to gather feedback 🙂

I tried to think if there are ways to avoid using the DB, there can even be shortcuts (if a class manages always events from EntityA to EntityB, why not inheriting something like EventsDispatcher ?), but for some cases we still need the DB. Overall I think this is actually the most beautifull ECS out there (and it has still some improvements to be done? Seriously?).

Thanks, the first version didn’t even have a db, as you can do everything with add and remove, but obviously is much more code to write

Hi Sebastiano, First of all, congratulations for this framework. As a programmer who participated to two different ECS development in the past, I got to admit that this one provides a lots of interesting features. Especially the notion of events. We were using tags on entity as a form of boolean, which was generating a lot of spaghetti code in the update function of our systems. Your event callbacks here is much more elegant. Good job! I’m trying out your framework on a personal project, to test out the performances of your system when querying nodes (with a lots of… Read more »

Thank you for the comment and the question. First, let me clarify that the framework is in continuous evolution and the version we use currently for Robocraft is different. I do update the github version every now and then, and I plan to update it soon (but I don’t know how soon). I hate when frameworks provide more than one way to do the same thing, so I do agree that what you are saying causes confusion. Fact is that I added the (very much needed) IQueryableNodeEngine much after the first release. So IQueryableNodeEngine is absolutely the way to prefer… Read more »

Excellent, thank you very much for the clarification. It’s tough to jungle full time job + a public framework on the side. Just curious now, what would be the upcoming critical changes in the eventual next update? I will make sure I keep an eye on this, and will use the current version of your framework, which I believe is already strong enough for my need.

Hmm I don’t remember exactly right now 🙂 I think the last big feature was the sequencer anyway

Hi Sebastiano, It’s been now a few days I’m playing around with your framework, and it’s indeed very interesting. However, I have a bit of a concern when it comes to the moment an entity and its components are defined: One of the main feature of previous ECS I’ve worked on was the possibility to add and remove components from an entity at run-time. This would result in triggering a system that was waiting for the presence of a certain component. Because an engine looks at nodes only, and doesn’t really access entities, this doesn’t seem the case here. In… Read more »

The framework is designed to remove and build entities in runtime but not change them. However we actually never used this feature as we prefer to enable and disable features instead just using simple flags inside nodes themselves

Thanks Sebastiano, this is quite fascinating actually. It forces devs to make better decisions when defining entities beforehand, as they will remain the same in their structure. I will definitely keep that in mind.

Hi Sebastiano,

Thank you for all of your shared work and thoughts.

What would be recommended way of communicating 2 engines only? One-step sequence feels like a great deal of work in this case.

Usually dispatchonchange does the job if it fits logically. The engines do not communicate directly it’s just that one engine is interested to know when a node value changes.

Let me paraphrase that:

Engine is interested to know when when a value of node (which is not managed by that engine) is changed.

Is that what you mean?

Exactly.. Engines should act only on nodes data.. Usually you poll it, but with dispatchonchange I added a mechanism to push notifications on data change.

So we have Dispatcher for data updates and Sequences for more complicated scenarios involving many engines. I have also noticed you make use of Observer-Observable couples; how would they fit into grand scheme? Do you have any specific recommendation for O-Os vs Dispatcher&Sequences?

Hi Sebastiano, I have a quick question regarding the initialization of entities. When a entity is created, it is currently not possible to set any of its component data. A good example of it is EnemySpawnerEngine: once the enemy has spawned it’s necessary to position it according to the data available within this engine. var go = _factory.Build(spawnData.enemy); _entityFactory.BuildEntity(go.GetInstanceID(), go.GetComponent().BuildDescriptorType()); var transform = go.transform; var spawnInfo = spawnData.spawnPoints[spawnPointIndex]; transform.position = spawnInfo.position; transform.rotation = spawnInfo.rotation; Another way to do so I suppose would be to go through another engine, but that engine might not have access to the data necessary to… Read more »

If data must be passed from outside the implementor or implementor factory then it’s an engine responsability for sure.

My point here was that in the example we were directly accessing from the engine to a data inside a GameObject itself, instead of even going through the implementor. And still I was wondering if even accessing the implementor itself is good practice. In my mind, it feels like an engine should not even be aware of any implementor at all, only Nodes.

Looking forward to your update 🙂

Yes that’s absolutely right. I don’t remember that code but if I did it I have to fix it.

OK Finally checked the EnemySpawnerEngine code. That code is fine. If I extend the GameObject factory to accept the initial position, that code would have been inside the factory. So tbh it’s a factory responsibility to set the initial transform, but all that said, I will leave the code like that.

…and the quotes didn’t work!… so again:

var go = _factory.Build(spawnData.enemy);

_entityFactory.BuildEntity(go.GetInstanceID(), go.GetComponent““().BuildDescriptorType());

var node = nodesDB.QueryNode““(go.GetInstanceID());

node.transformComponent.transform.position = spawnData.position;

(Note: “>” and “<" template arguments are stripped from comments so I will use quotes)

Option 3: querying immediately a Node right after calling BuildEntity so that means:

var go = _factory.Build(spawnData.enemy);

_entityFactory.BuildEntity(go.GetInstanceID(), go.GetComponent "” ().BuildDescriptorType());

var node = nodesDB.QueryNode “” (go.GetInstanceID());

node.transformComponent.transform.position = spawnData.position;

@apartment609 the article could be a bit outdated as well, need to re read it again too!

@Sebastiano Mandalà haha yes, there might be a whole realm of use I am not seeing yet, because I got too focused on Implementors being MonoBehaviors, like in the example. I’m going to read the article again, get deep in the code and all the comments all over again. Different use cases as example would be very interesting to see. Thank you so much for your patience. I am going to use this framework, it has so much potential! (Hell I’m already using it) @Szymon You are absolutely right, engines usually check the presence of certain types of Nodes before… Read more »

@apartment609

Isn’t what you need is to get node associated with newly created entity and then fetch ITransform component via node?

Then you could do whatever you need on the transform’s reference

I’m very confused, and all my apology if I don’t understand this correctly. I really want to get to the bottom of this if possible. 😀 You are suggesting “to pass data to the implementors constructor”… but implementors are Monobehaviors here, there’s not supposed to be a notion of constructor… I will try to re-explain the issue: We have a EnemySpawnerEngine which holds all the data necessary on where and when to spawn new enemy. At every n seconds this is called: var go = _factory.Build(spawnData.enemy); _entityFactory.BuildEntity(go.GetInstanceID(), go.GetComponent().BuildDescriptorType()); Now instantiating the GameObject, and building the entity is not enough, a… Read more »

Hehe nvm the example I have to revisit it. However I had the suspect that the mono behavior thing could have confused you. Implementors don’t have to be monobehaviours and actually is better to use them only when essential. You can also pass several implementors to an entity descriptor so it’s better to have implementors as modular as possible so you can reuse them. For the specific case of the example I have to see it again to take a decision. I’ll try to check this weekend.

So knowing all that, the question is: how can an engine calling a BuildEntity be able to pass any information to that entity? (Such as positioning it for instance)

Are you asking how to pass data inside implementors to be used with the entity descriptors? If so you can pass data to the implementors constructor. If you are asking if an engine can create implementors I’d say yes.

Hello I must review the example again as things may have changed meanwhile. I hope to do a good update this weekend. Anyway usually components are initialised inside the implementors.

Hi Sebastiano.

Thanks for the great blog and framework.

I’m interested, why do you think that interface components are better than components implemented as objects?

With components as objects I can add behavior to entities or remove it in realtime, which adds flexibility. Same entities can behave differently depending on what components are added to them in runtime.

And I cannot do that with interfaces. Is there any advantage that outweighs this drawback?

Thanks

Allocating objects especially in run time has a cost. Having hundreds of object references hanging around has a cost on the garbage collection as well. All that said Svelto.Ecs can do everything the other frameworks do but in a different way. Usually we enable and disable behaviours in runtime with simple booleans in the implementors themselves.

Thanks for quick reply. Looks interesting. We’re using Entitas now at our team. In Entitas the problems with garbage collection are handled by using pools for components. However this adds some complexity, which is hidden under code-generated APIs.

Code generation adds level of indirection to the code, it’s difficult to research it, especially for junior-level developers.

That’s why I’m looking for an ECS implementation without code generation. I was thinking of making it myself, but then found your implementation.

Thanks for sharing it!

Hi Sebastiano!

I’ve looked through the example code. First it seemed complex, but after a day of investigating now everything is clear and logical. I really liked the concept of Sequencer. It solves one of biggest problems we had in Entitas – need to look through all the code to find what happens next.

However I haven’t found DispatcherOnSet and DispatcherOnChange in the project. Have you removed them? Or is there still a way to dispatch events in components?

Ah, sorry, I’ve found it. Thanks

I see Dispatch only in Observable classes, but not in components or framework itself.

I think I just renamed them. Did I forget to fix the code? Should be Dispatch instead of Dispatcher

We are using it on two projects. I need to update it to the latest version but the differences are not many.

Hi Sebastiano.

Thank for great framework. Pooling, GC, and Input system are parts of the framework, and any more…. so how do i implement them, using engine? or … something to extend your framework, thank for your feedback.

Regards,

kkmct.

We have those implemented but they are not good enough to be shared yet. However you can write all the logic you need still using engines.

Hi Sebastiano. I’ve looked through the framework source code and here are some questions I have: 1. What platforms is Svelto.ECS tested on? Does it work in plain C#, without Unity? There’s #if NETFX_CORE statement in some places in source code. Is it supposed to be working also in .NET Core? 2. I’ve looked through FasterList implementation and it looks the same as System.Collections.Generic.List one: a dynamically allocated array. Is FasterList really faster than System.Collections.Generic.List? Is it tested? How is it achieved? 3. I noticed you use reflection in EntityDescriptor.BuildNodes method. It’s being called every time a new entity is… Read more »

I forgot to say: the code is tested for il2cpp as well, hence the define. I try to keep my libs unity agnostic, but it’s never been tested on anything else

Once I am back on my blog I’ll open a thread in the unity forum. Answering your questions:

Everything is tested in production on several project at freejam

Faster list is not faster because of the code is faster because of some different choices that work in most cases, like the unordered remove and the clear that doesn’t actually clear the buffer.

Entity creation isn’t a problem for us at the moment

I was checking the code of the Entity Creation. To be honest in Robocraft we never destroy entity, so this feature is not well tested yet, however we do use for a not announced new product. in RC, the creation of entities is quite rare too as everything is created at the startup phase. All that said I can see how it could potentially be needed to create an entities pool to recycle nodes instead to create them everytime. Can’t think about it now, but if you have ideas let me know.

Hi, how would you interact with Photon (PUN) with your ECS?

One of our projects uses pun, so it can be done, but I know nothing about pun. In general the implementor is always the bridge between the framework and whatever external library

Hello Sebastiano! Great framework! Thanks for making this! I’m still figuring out stuff and it would be great if you could help me with some questions. – What’s the best course of action for querying StructNodes to get an item with ID x? – Should I update data in StructNodes? I added Count, SetAt, GetAt, Remove and Clear to it. This is the wrong way I guess. – Building structs and setting init data is really weird as I didn’t find a way to set the data directly. Is the descriptor and constructor arguments that are saved for the BuildNodes… Read more »

Hello and thanks for the comment. Nodes as struct are an advanced feature of Svelto.ECS. Since you want to take advantage of the cache when using them, it doesn’t make sense to pick-up a specific index. The array of nodes is meant always to be iterated, from the begin to the end. In the other cases you can use the standard approach. Alternatively you can manage the array of struct removing/add nodes if you know what you are doing. Nodes MUST not have any functions inside. I am actually going to add soon a check that will throw an exception… Read more »

You can put a comment in StructNodes, if you want to change this you are not thinking data-oriented enough.

I think I know now where I’m going wrong. The engine does too much and I need to get away from thinking in sequential code. Learning new paradigms isn’t easy, thanks for helping out!

“You can put a comment in StructNodes, if you want to change this you are not thinking data-oriented enough.” didn’t understand this. I have to put the exceptions to avoid inserting functions inside nodes just because it is data oriented. If instead you mean why I want to keep coders from adding anything else than interfaces inside class nodes is because the framework MUST be rigid. I noticed few people doing otherwise, and this would eventually take to bad design. The nodes have a specific purpose, they don’t have to do anything else than just mapping components. Components have specific… Read more »

I should see the code to understand what you are trying to achieve, however if you are new to Svelto.ECS I still suggest you to use the normal nodes and not the struct nodes. The survivor little game bundled do not use struct nodes at all. Have you seen that code before to start experimenting?

Nodes only contain struct data in my case and I extended your StructNodes class to have more helper functions, but instead of manipulating the data directly in StructNodes it’s better to just remove/add them, right? These are long-living entities so would this really be the best course? Have you had any algorithms that iterated over nodes and prev/next nodes data had to be changed? I’m trying to get this behaviour out but the only thing I know how to do this is to build new data that are processed later on. Like your addNodesToBuild which work deferred. I’m not sure… Read more »

I really like what I have seen from the example provided.

Is it possible to introduce SveltoECS to existing project without redoing all logic? If so how do you bridge between plain old MonoBehaviours with data and logic and components/node/engines?

A second question is do you plan to have official releases? On the github repo there seems to be no releases.

Yes absolutely, we had 3 years of legacy code in Robocraft before to switch to Svelto.ECS. Svelto.ECS has several unique features, that I am going to highlight better in a new article, but one is about the implementers. The implementers function as a bridge between platform/legacy code and ECS. Another way to solve the problem is using the good old observer/observable pattern.

About the releases, well I never thought about that, would it give any benefit?

Hi,

I just read through all the previous articles and totally get why you created Svelto.ECS. I genuinely feel that you have a good grasp on best way to do things. Does ECS make since for a card game where there are 144 cards and a lot of them have different effects. Would each effect be a node? Thanks for any advise you can give.

I’ve been struggling with this problem for a while. I’m working on a Tactical Turn RPG (Final Fantasy Tactics style). Each ability in the game has an Area, Range, TargetType and multiple effects. For example, an ability can have a Damage effect and a Inflict Poison effect. The problem is that while each ability has an AreaComponent, RangeComponent and TargetTypeComponent, each ability has different effects, So while Ability 1 has DamageEffectComponent and PoisonEffectComponent, another ability could have ReviveEffectComponent and SlowEffectComponent. This would lead to each ability being a different entity with a unique EntityDescriptor. It would be great if it… Read more »

Thanks a lot for the message and its great that you find svelto useful. I need to think better about your question, but I need more info. How would you design the engines for these entities? How would the logic work inside?

Hello and thank you for the message. I am currently in the process to complete the first public release of Svelto.ECS 2.0. After that at least two, but probably more, articles will follow to explain better the strategies to adopt to work with an ECS framework. Hope it will help!

Hi, I finally (or I think to) understood how to use svelto. This is Just Amazing and I dont think it is over engineering using it also in small projects, actually it saves me a lot of time. I started also writing a sentire of articles on practical usage examples. However I have few serious improvements suggestions. 1) use enumerator instead of sequencers, actually I always modeled action sequences as enumerators, creating a code flow is much easier with a enumerators than by building the same code block by creating syntax nodes. In hoping to show that in my 4th… Read more »

1) Sequencers are not what you are thinking they are. As I am writing soon in my new article, perfect engines are totally encapsulated and you can write the logic of that engine as a sequence of instructions using IEnumerators. However this is not always the case, some times, engines need to signal events to other engines. This is usually possible to do through EntityData, especially using DispatchOnSet and DispatchOnChange, however check my example Survival, when entities are damaged, a series of totally indipendent and uncopupeld engines are acting on it. This is not just it, sometime you want the… Read more »

Thanks for Reading it :). 2) well yes, I Was aware that i could query the db, but wanted to do an early optimization..but accessing a entity and then getting the reference to the component isnt the same ad using the reference in that particular case?. I can see why doing that is bad, I think the risk in doing that is managing the reference, it could happen at some point a entity is removed but some reference to it is still alive.. Basically seems all entities are threated Like weak pointers, you have a handle to them but you… Read more »