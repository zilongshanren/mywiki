---
title: 'Svelto Mini Examples: The Unity Survival Example - Seba''s Lab'
url: https://www.sebaslab.com/learning-svelto-ecs-by-example-the-unity-survival-example/
author: Sebastiano Mandalà
published: '2019-04-02'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

### Note: this article is now outdated. The new version is found at: [https://www.sebaslab.com/the-new-svelto-ecs-survival-mini-example/](https://www.sebaslab.com/the-new-svelto-ecs-survival-mini-example/)

## Introduction

Lately I have been discussing *Svelto.ECS* extensively with several, more or less experienced, programmers. I gathered a lot of feedback and took a lot of notes that I will be using as starting point for my next articles where I will talk more about the theory and good practices. Just to give a little spoiler, I realized that the biggest obstacle that new coders face when starting using *Svelto.ECS is the shift of programming paradigm*. It’s astonishing how much I have to write to explain the novel concepts introduced by Svelto.ECS compared to the small amount of code written to develop the framework. In fact, while the framework itself is very simple (and lightweight), learning how to move from the class inheritance heavy object oriented design or even the naive Unity components based design, to the “new” modular and decoupled design that Svelto.ECS forces to use, is what usually discourages people from adopting the framework.

Being the framework extensively used at *Freejam*, I also noticed that it’s thanks to my continuous availability to explain the fundamental concepts that my colleagues have less of a hard time to get in to the flow. Although Svelto.ECS tries to be as rigid as possible, bad habits are hard to die, so users tend to abuse the little flexibility left to adapt the framework to the “old” paradigms they are comfortable with. This can result in a catastrophe due to misunderstandings or reinterpretation of the concepts that are behind the logic of the framework. That’s why I am committed to write as many articles as possible, especially because I know that the ECS paradigm is the best solution I found so far to write efficient and maintainable code for large projects that are refactored and reshaped multiple times over the span of years and *Robocraft *as well as *Cardlife *are the existing proof of what I try to demonstrate.

I am not going to talk much about the theories behind the framework in this article, but I want to remind what took me to the path of ditching the use of an* IoC Container* and starting using exclusively the ECS framework: an IoC container is a very dangerous tool if used without Inversion of Control in mind. As you should have read from my previous articles, I differentiate between *Inversion of Creation Control* and* Inversion of Flow Control*. Inversion of Flow Control is basically the *Hollywood principle “Don’t call us, we will call you”*. This means that dependencies injected should never been used directly through public methods, in doing so you would just use an IoC container as a substitute of any other form of global injection like singletons. However, once an IoC container is used following the IoC principle, it mainly ends up in using repeatedly the* Strategy Pattern* to inject managers used only to register the entities to manage. In a real Inversion of Flow Control context, managers are always in charge of handle entities. Does it sounds like what the ECS pattern is about? It indeed does. From this reasoning I took the ECS pattern and evolved it into a rigid framework to the point it can be considered using it like adopting a new coding paradigm.

## The Survival Example

let’s start downloading the project from [https://github.com/sebas77/Svelto.MiniExamples/tree/master/Example2-Survival](https://github.com/sebas77/Svelto.MiniExamples/tree/master/Example2-Survival)

![](../../assets/1fd2168d1dfddf53.png)


![](../../assets/1fd2168d1dfddf53.png)

open the scene *Level01* and open the project in your IDE. Everything starts from *maincontext.cs* file.

### The Composition Root and the EnginesRoot

The class **Main** is the *Application Composition Root*. A Composition Root is where dependencies are created and injected (I talk a lot about this in my articles). A composition root belongs to the context, but a context can have more than one composition root. For example a factory is a composition root. Furthermore an application can have more than one context but this is an advanced scenario and not part of this example.

Before to start digging in the code, let’s introduce the first terms of the Svelto.ECS domain language. ECS is an acronym for Entity Component System. The ECS infrastructure has been analyzed abundantly with several articles written by many authors, but while the basic concepts are in common, the implementations differ a lot. Above all, there isn’t a standard way to solve the few problems rising from using ECS oriented code. That’s where I put most of my effort on, but this is something I will talk about later or in the next articles. At the heart of the theory there are the concepts of *Entity*, *Components* (of the entities) and *Systems*. While I understand why the word System has been used historically, I initially found it not intuitive for the purpose, so *Engine* is synonym of System and you may use it interchangeably according your preferences.

The *EnginesRoot* class is the core of Svelto.ECS. With it is possible to register the engines and build all the entities of the game. It doesn’t make much sense to create engines dynamically, so all the engines should be added in the EnginesRoot instance from the same composition root where it has been created. For similar reasons, an EnginesRoot instance must never been injected and engines can’t be removed once added.

We need at least one composition root to be able to create and inject dependencies wherever needed. Yes, it’s possible to have even more than one EnginesRoot per application, but this is too not part of this article, which I will try to keep as simple as possible. This is how a composition root with engines creation and dependencies injection looks like:

```
//The Engines Root is the core of Svelto.ECS. You shouldn't inject the EngineRoot,
//therefore the composition root must hold a reference or it will be GCed.
//the UnitySumbmissionEntityViewScheduler is the scheduler that is used by the EnginesRoot to know
//when to submit the entities. Custom ones can be created for special cases.
_unityEntitySubmissionScheduler = new UnityEntitySubmissionScheduler();
_enginesRoot = new EnginesRoot(_unityEntitySubmissionScheduler);
//The EntityFactory can be injected inside factories (or engine acting as factories) to build new entities
//dynamically
_entityFactory = _enginesRoot.GenerateEntityFactory();
//The entity functions is a set of utility operations on Entities, including removing an entity. I couldn't
//find a better name so far.
var entityFunctions = _enginesRoot.GenerateEntityFunctions();
//Sequencers are the official way to guarantee order between engines, but may not be the best way for
//your product.
var playerDeathSequence = new PlayerDeathSequencer();
var enemyDeathSequence = new EnemyDeathSequencer();
//wrap non testable unity static classes, so that can be mocked if needed.
IRayCaster rayCaster = new RayCaster();
ITime time = new Time();
//Player related engines. ALL the dependencies must be solved at this point through constructor injection.
var playerShootingEngine = new PlayerGunShootingEngine(rayCaster, time);
var playerMovementEngine = new PlayerMovementEngine(rayCaster, time);
var playerAnimationEngine = new PlayerAnimationEngine();
var playerDeathEngine = new PlayerDeathEngine(playerDeathSequence, entityFunctions);
//Enemy related engines
var enemyAnimationEngine = new EnemyAnimationEngine(time, enemyDeathSequence, entityFunctions);
var enemyAttackEngine = new EnemyAttackEngine(time);
var enemyMovementEngine = new EnemyMovementEngine();
//GameObjectFactory allows to create GameObjects without using the Static method GameObject.Instantiate.
//While it seems a complication it's important to keep the engines testable and not coupled with hard
//dependencies
var gameObjectFactory = new GameObjectFactory();
//Factory is one of the few patterns that work very well with ECS. Its use is highly encouraged
var enemyFactory = new EnemyFactory(gameObjectFactory, _entityFactory);
var enemySpawnerEngine = new EnemySpawnerEngine(enemyFactory, entityFunctions);
var enemyDeathEngine = new EnemyDeathEngine(entityFunctions, enemyDeathSequence);
//hud and sound engines
var hudEngine = new HUDEngine(time);
var damageSoundEngine = new DamageSoundEngine();
var scoreEngine = new ScoreEngine();
//The ISequencer implementation is very simple, but allows to perform
//complex concatenation including loops and conditional branching.
//These two sequencers are a real stretch and are shown only for explanatory purposes.
//Please do not see sequencers as a way to dispatch or broadcast events, they are meant only and exclusively
//to guarantee the order of execution of the involved engines.
//For this reason the use of sequencers is and must be actually rare, as perfectly encapsulated engines
//do not need to be executed in specific order.
//a Sequencer can:
//- ensure the order of execution through one step only (one step executes in order several engines)
//- ensure the order of execution through several steps. Each engine inside each step has the responsibility
//to trigger the next step through the use of the Next() function
//- create paths with branches and loop using the Condition parameter.
playerDeathSequence.SetSequence(playerDeathEngine, playerMovementEngine, playerAnimationEngine,
enemyAnimationEngine, damageSoundEngine, hudEngine);
enemyDeathSequence.SetSequence(enemyDeathEngine, scoreEngine, damageSoundEngine, enemyAnimationEngine,
enemySpawnerEngine);
//All the logic of the game must lie inside engines
//Player engines
_enginesRoot.AddEngine(playerMovementEngine);
_enginesRoot.AddEngine(playerAnimationEngine);
_enginesRoot.AddEngine(playerShootingEngine);
_enginesRoot.AddEngine(new PlayerInputEngine());
_enginesRoot.AddEngine(new PlayerGunShootingFXsEngine());
_enginesRoot.AddEngine(playerDeathEngine);
_enginesRoot.AddEngine(new PlayerSpawnerEngine(gameObjectFactory, _entityFactory));
//enemy engines
_enginesRoot.AddEngine(enemySpawnerEngine);
_enginesRoot.AddEngine(enemyAttackEngine);
_enginesRoot.AddEngine(enemyMovementEngine);
_enginesRoot.AddEngine(enemyAnimationEngine);
_enginesRoot.AddEngine(enemyDeathEngine);
//other engines
_enginesRoot.AddEngine(new ApplyingDamageToTargetsEngine());
_enginesRoot.AddEngine(new CameraFollowTargetEngine(time));
_enginesRoot.AddEngine(new CharactersDeathEngine());
_enginesRoot.AddEngine(damageSoundEngine);
_enginesRoot.AddEngine(hudEngine);
_enginesRoot.AddEngine(scoreEngine);
```


This code is part of the survival example which is now well commented and follows almost all the good practice rules that I suggest to use, including keeping the engines logic platform independent and testable. The comments will help you to understand most of it, but a project of this size may be already too much to swallow if you are new to Svelto. For this reason, let’s proceed as we would have done if started from scratch:

### Entities

the first step, after creating the empty *Composition Root* and an instance of the *EnginesRoot *class, would be to identify the entities you want to work with first. Let’s logically start from the *Player Entity*. The Svelto.ECS entity must not be confused with the Unity GameObject. If you had the chance to read other ECS related articles, you will see that in many of those, entities are often described as indices. This is probably the worst way possible to introduce the concept. While this is true for Svelto.ECS too, it’s well hidden. As matter of fact, I want the Svelto.ECS user to visualize, describe and identify every single entity in terms of *Game Design Domain language*. An entity in code must be an entity described in the game design document. Any other form of entity definition will result in a contrived way to adapt your old paradigms to the Svelto.ECS needs. Follow this fundamental rule and you won’t be wrong in most of the cases. An entity class doesn’t exist per se in code, but you still must define it in a not abstract way.

### Engines

Next step is to think about what behaviours to give to this Entity. Every behaviour is always modeled inside an *Engine*, there is no way to add logic in any other classes inside a Svelto.ECS application. For this purpose we can start from the player character movement and define the **PlayerMovementEngine **class. The name of the engine must be very specific, as the more specific it is, the higher is the chance the Engine will follow the *Single Responsibility Rule*. Naming classes properly in Svelto.ECS is of fundamental importance. It’s not just to comunicate clearly your intentions, but it’s actually more about letting you think about your intentions.

For the same reason I would suggest (as good practice) to put your engine inside a specialised namespace. Using specialized namespaces helps a lot to identify code design errors when entities are used inside not compatible namespaces. For example, you wouldn’t expect any enemy entity to be used inside a player namespace, unless you want to break the good rules related to modularity and decoupling of objects. The idea is that entities of a specific namespace can be used only inside that namespace or a less abstracted namespace. While with Svelto.ECS is much harder to turn your code in to a fully fledged spaghetti bowl, where dependencies are injected everywhere and randomly, this rule will help you to take your code to an even better level where dependencies are correctly abstracted between classes.

*08/04/19 Note: this good practice has been taken now to another level, encapsulating the layers of abstraction inside separate composition roots belonging in different assemblies. I never discussed this approach formally, so another article or wiki paragraph will come later on.*

In Svelto.ECS abstraction is pushed on several fronts, but ECS intrinsically promote separation of the data from the logic that must handle it. Entities are defined by their data, not their behaviours. Engines instead are the place where to put the shared behaviours of entities, so that engines can always operate on a set of entities.

Svelto.ECS, and the ECS paradigm in general, allows the coders to achieve one of the holy grails of clean programming, that is the perfect encapsulation of logic. Engines must not have public functions, consequentially Engines are never injected in any other engine. If you think to pass an engine as parameter, you are probably doing something wrong already.

Compared to Unity monobehaviours, engines already show the first great benefit, which is the possibility to access to all the entity states of a given type from the same code scope. This means that the code can easily use the state of all the entities directly from the same place where the shared entity logic is going to run. Furthermore separate engines can handle the same entities so that an engine can change an entity state while another engine can read it, effectively putting the two engines in communication through the same entity data. An example of this can be seen with the engines **PlayerGunShootingEngine** and **PlayerGunShootingFxsEngine**. In this case the two engines are in the same namespace, so they can share the same entity data. **PlayerGunShootingEngine** determines if a player target (an enemy) has been damaged and writes the **lastTargetPosition** of the **IGunAttributesComponent** (which is a component of the **PlayerGunEntity**). the **PlayerGunShootFxsEngine** handles the graphic effects of the gun and reads the position of the currently targeted player target. This is an example of communication between engines through *data polling*. It’s quite logical that engines should (and must) never hold states.

```
public class PlayerGunShootingEngine
: MultiEntitiesReactiveEngine<GunEntityViewStruct, PlayerEntityViewStruct>, IQueryingEntitiesEngine
{
readonly IRayCaster _rayCaster;
readonly ITaskRoutine<IEnumerator> _taskRoutine;
readonly ITime _time;
public PlayerGunShootingEngine(IRayCaster rayCaster, ITime time)
{
_rayCaster = rayCaster;
_time = time;
_taskRoutine = TaskRunner.Instance.AllocateNewTaskRoutine(StandardSchedulers.physicScheduler);
_taskRoutine.SetEnumerator(Tick());
}
public IEntitiesDB entitiesDB { set; private get; }
public void Ready() { _taskRoutine.Start(); }
protected override void Add(ref GunEntityViewStruct entityView,
ExclusiveGroup.ExclusiveGroupStruct? previousGroup)
{
}
protected override void Remove(ref GunEntityViewStruct entityView, bool itsaSwap) { _taskRoutine.Stop(); }
protected override void Add(ref PlayerEntityViewStruct entityView,
ExclusiveGroup.ExclusiveGroupStruct? previousGroup)
{
}
protected override void Remove(ref PlayerEntityViewStruct entityView, bool itsaSwap) { _taskRoutine.Stop(); }
IEnumerator Tick()
{
while (entitiesDB.HasAny<PlayerEntityViewStruct>(ECSGroups.Player) == false ||
entitiesDB.HasAny<GunEntityViewStruct>(ECSGroups.Player) == false)
yield return null; //skip a frame
//never changes
var playerGunEntities = entitiesDB.QueryEntities<GunEntityViewStruct>(ECSGroups.Player, out var count);
//never changes
var playerEntities = entitiesDB.QueryEntities<PlayerInputDataStruct>(ECSGroups.Player, out count);
while (true)
{
var playerGunComponent = playerGunEntities[0].gunComponent;
playerGunComponent.timer += _time.deltaTime;
if (playerEntities[0].fire &&
playerGunComponent.timer >= playerGunEntities[0].gunComponent.timeBetweenBullets)
Shoot(playerGunEntities[0]);
yield return null;
}
}
/// <summary>
/// Design note: shooting and find a target are possibly two different responsibilities
/// and probably would need two different engines.
/// </summary>
/// <param name="playerGunEntityView"></param>
void Shoot(GunEntityViewStruct playerGunEntityView)
{
var playerGunComponent = playerGunEntityView.gunComponent;
var playerGunHitComponent = playerGunEntityView.gunHitTargetComponent;
playerGunComponent.timer = 0;
var entityHit = _rayCaster.CheckHit(playerGunComponent.shootRay, playerGunComponent.range,
GAME_LAYERS.ENEMY_LAYER,
GAME_LAYERS.SHOOTABLE_MASK | GAME_LAYERS.ENEMY_MASK, out var point,
out var instanceID);
if (entityHit)
{
var damageInfo = new DamageInfo(playerGunComponent.damagePerShot, point);
//note how the GameObject GetInstanceID is used to identify the entity as well
if (instanceID != -1)
entitiesDB.QueryEntity<DamageableEntityStruct>((uint) instanceID, ECSGroups.PlayerTargets)
.damageInfo = damageInfo;
playerGunComponent.lastTargetPosition = point;
playerGunHitComponent.targetHit.value = true;
}
else
{
playerGunHitComponent.targetHit.value = false;
}
}
}
```


Engines are not supposed to know how to interact with other engines. The best engines are the ones that do not even need to trigger any form of external communication. These engines reflect a well encapsulated behaviour and usually work through a loop. Loops can be modeled with a *Svelto.Task task* inside Svelto.ECS applications. Since the player movement must be updated every physic tick, it would be natural to create a task that is executed every physic update. *Svelto.Tasks* allows to run every kind of **IEnumerator **on several types of schedulers. In this case we decide to create a task on the **PhysicScheduler **that allows to update the player position:

Svelto.Tasks can run *IEnumerator *directly (using the extension methods **Run **and **RunOnScheduler **for* Svelto Tasks 1.5* and **RunOn **for *Svelto Tasks 2.0*), but in this case I decided to use a *TaskRoutine*, as I want to stop it when the entity is removed.

Svelto.ECS exploit the **Add** and **Remove** callbacks to know when specific entities are added or removed. These callbacks are used also during a swap (*note: these interfaces are currently undergoing some refactoring to make the difference between Add,Remove and Swap more obvious, so this paragraph may be obsolete soon*).

Engines more commonly implement the **IQueryingEntityViewEngine **interface instead. This allows to access the entity database and retrieve data from it. Remember you can always query any entity from inside an engine, but in the moment you are querying an entity that is not compatible with the namespace where the engine lies, then you know you are already doing something wrong. Engines should never assume that the entities are available and they must work on a set of entities. Engines must always be functional, regardless the number of entities currently available (0, 1 or N). This rule can be broken if you know by design that specific entities will be unique (like the Player in this example). A very common approach to how to query entities is found in the **EnemyMovementEngine**:

```
public class EnemyMovementEngine : IQueryingEntitiesEngine
{
public IEntitiesDB entitiesDB { set; private get; }
public void Ready() { Tick().Run(); }
IEnumerator Tick()
{
while (true)
{
//query all the enemies from the standard group (no disabled nor respawning)
var enemyTargetEntityViews =
entitiesDB.QueryEntities<EnemyTargetEntityViewStruct>(
ECSGroups.EnemyTargets, out var enemyTargetsCount);
if (enemyTargetsCount > 0)
{
var enemies =
entitiesDB.QueryEntities<EnemyEntityViewStruct>(ECSGroups.ActiveEnemies, out var enemiesCount);
//using always the first target because in this case I know there can be only one, but if
//there were more, I could use different strategies, like choose the closest. This is
//for a very simple AI scenario of course.
for (var i = 0; i < enemiesCount; i++)
enemies[i].movementComponent.navMeshDestination =
enemyTargetEntityViews[0].targetPositionComponent.position;
}
yield return null;
}
}
}
```


In this case the engine main loop is running directly immediately on the predefined scheduler. **Tick().Run()** shows the shortest way to run an *IEnumerator *with Svelto.Tasks. The *IEnumerator *will keep on yielding to the next frame until at least one *Enemy Target *is found. Since we know that there will be always just one target (another not nice assumption), I pickup the first available. While the *Enemy Target *can be just one (although could have been more!), the enemies are many and the engine takes care of the movement logic for all of them.

Note that the component never exposes the Unity navmesh dependency directly. Entity Component, as I will say later, must always expose value types. In this case this rule also allows to keep the code testable, as the field value type **navMeshDestination** could be later implemented without using a Unity Nav Mesh stub.

To conclude the paragraph related to engines, note that there isn’t such a thing as a too small engine. Hence, don’t be afraid to write an engine even for just few lines of code, after all you can’t put logic anywhere else and you want your engines to follow the Single Responsibility Rule.

### EntityViews

So far we introduced the concept of Engine and an abstracted definition of Entity, let’s now define what an *EntityView *is. I have to admit, of the 5 concepts of which Svelto.ECS is built upon, the EntityViews is probably the most confusing. Previously called **Node**, name taken from the **Ash ECS framework**, I realized that node meant nothing. EntityView may be confusing as well, since programmers usually associate views with the concept coming from **Model View Controller** pattern, however in Svelto.ECS is called View because an EntityView is *how the Engine views an Entity*. This scheme of the Svelto.ECS concepts should help a bit:

I suggested to start working on the Engine first, thus we are on the right side of this scheme. Every Engine comes with its own set of EntityViews. An Engine can reuse namespace compatible EntityViews, but it’s more common for an Engine to define its entity views. The Engine doesn’t care if a *Player Entity* definition actually exists, it dictates the fact that it needs a **PlayerEntityView** to work. *The writing of the code is driven by the Engine needs*, you shouldn’t create the entity and its field before to know how to use those fields. In a more complex scenario, the name of the EntityView could have been even more specific.

*(note: since the introduction of *[Svelto.ECS 2.5](http://www.sebaslab.com/svelto-ecs-2-5-and-allocation-0-code/)*, EntityStructs are much more relevant then EntityViewStructs. I still call EntityStructs and EntityViewStructs entity views, because I still like the original definition. However EntityStructs are effectively entity components)*

* EntityViews are classes that hold only Entity Components*.

**Entity Components in Svelto.ECS are always interfaces**that must be implemented, but the Engine and EntityView doesn’t need to know the implementation. For this reason, without even implementing the component yet, I can just start to type the logic in the engine like if it was in place:

![](../../assets/0d7874731002ae20.png)


![](../../assets/0d7874731002ae20.png)

Hoping you use an IDE that supports refactoring, the IDE will immediately warn you that the field you are trying to access actually doesn’t exist. This is where the refactoring tools can help you speeding up the writing of the code. For example, using Jetbrains rider (but it’s the same with Visual Studio) you can create the field automatically like this:

this would add the component field in the EntityView like:

since the **IPlayerInputComponent **interface doesn’t exist yet, I name it and use on the spot. Then I use again the refactoring tool:

this will create an empty interface, so that now the code would look like:

![](../../assets/fbf0de14c65e241e.png)


![](../../assets/fbf0de14c65e241e.png)

Yes that’s right, I would use again the refactoring tool:

so that the **IPlayerInputComponent **interface will be filled with the right properties. As long as I don’t run the code, I can build it without needing to implement the Entity Component **IPlayerInputComponent **interface yet. Honestly, once you get in this flow, you will notice how fast can be coding with Svelto.ECS using the IDE refactoring tools.

### Components

We understood that engines model behaviors for a set of entities and we understood that engines do not use entities directly, but use the entity components through entity views. We understood that an entity view can hold ONLY public entity components.

When **EntityViewStructs **are used to abstract objects coming from OOP platforms/libraries, an entity component is an interface. The Entity Component interface is then implemented with a so called **Implementor. We are now starting to define the Entity itself and we are on the left side of the scheme above.**

Components should always hold value types and the fields are always getter and setter properties. This allows to create testable code that is not dependent by the implementation of the Not ECS/OOP platforms or libraries used in the project. Moreover it prevents people from cheating and use public functions (which would include logic!) of random objects.

### EntityDescriptors

This is where the Entity Descriptors actually come to help to put everything together and hopefully let everything click in place. We know that Engines can access to Entity data through the Entity Components held by the Entity Views. We know that Engines model the behavior of the entities through their entity views, that entity views hold only Entity Components and that Entity Components are value types. While I have given an abstracted definition of entity, we haven’t seen any class that actually represent an entity. This is in line with the concept of entities being just IDs inside a modern ECS framework. However without a proper definition of Entity, this would lead coders to identify Entities with EntityViews, which would be catastrophically wrong. EntityViews is the way several Engines can view the same Entity but, conceptually, they are not the entities. The Entity itself should be always be seen as a set of data defined through the entity components, but even this representation is weak. An *EntityDescriptor* instance gives the chance to the coder to name properly their entities independently by the engines that are going to handle them. Therefore in the case of the *Player Entity*, we would need an **PlayerEntityDescriptor**. This class will then be using to build the entity, and while what it really does is something totally different, the fact that the user is able to write **BuildEntity< PlayerEntityDescriptor>()** helps immensely to visualize the entities to build and to communicate the intentions to other coders.

However what an *EntityDescriptor* really does is to build a list of *Entity Views*!!!

This is how the **PlayerEntityDescriptor** looks like:

```
public class PlayerEntityDescriptor : IEntityDescriptor
{
static readonly IEntityBuilder[] _entitiesToBuild =
{
new EntityBuilder<PlayerEntityViewStruct>(),
new EntityBuilder<DamageableEntityStruct>(),
new EntityBuilder<DamageSoundEntityView>(),
new EntityBuilder<CameraTargetEntityView>(),
new EntityBuilder<HealthEntityStruct>(),
new EntityBuilder<EnemyTargetEntityViewStruct>(),
new EntityBuilder<PlayerInputDataStruct>()
};
public IEntityBuilder[] entitiesToBuild => _entitiesToBuild;
}
```


the *EntityDescriptors* (and the Implementors) are the only classes that can use identifiers from multiple namespaces. In this case the **PlayerEntityDescriptor** defines the list of *EntityViews* to instantiate and inject in the engine when the *PlayerEntity* is built.

#### EntityDescriptorHolder

The *EntityDescriptorHolder *is an extension for Unity and should be used only in specific cases. The most common one is to create a sort of polymorphism storing the information of the entity to build on the Unity GameObject. It can be useful when prefabs are seen exclusively as a way to serialise entities and currently they are commonly used to serialise entities for GUIs. However, building entities explicitly is always preferred, so use *EntityDescriptorHolders *only when you have understood Svelto.ECS properly otherwise there is the risk to abuse it. This function from the example shows how to use the class:

void BuildEntitiesFromScene(UnityContext contextHolder) { //An EntityDescriptorHolder is a special Svelto.ECS class created to exploit //GameObjects to dynamically retrieve the Entity information attached to it. //Basically a GameObject can be used to hold all the information needed to create //an Entity and later queries to build the entitity itself. //This allow to trigger a sort of polyformic code that can be re-used to //create several type of entities. IEntityDescriptorHolder[] entities = contextHolder.GetComponentsInChildren<IEntityDescriptorHolder>(); //However this common pattern in Svelto.ECS application exists to automatically //create entities from gameobjects already presented in the scene. //I still suggest to avoid this method though and create entities always //manually. Basically EntityDescriptorHolder should be avoided //whenver not strictly necessary. for (int i = 0; i < entities.Length; i++) { var entityDescriptorHolder = entities[i]; var entityDescriptor = entityDescriptorHolder.RetrieveDescriptor(); _entityFactory.BuildEntity (((MonoBehaviour) entityDescriptorHolder).gameObject.GetInstanceID(), entityDescriptor, (entityDescriptorHolder as MonoBehaviour).GetComponentsInChildren<IImplementor>()); } }

Note that with this example I am already using the less preferred, not generic, function **BuildEntity**. I will talk about it in a bit. The Implementors in this case are always monobehaviours in the gameobject. Also this is not a good practice. I actually should remove this code from the example, but left to show you this other case. Implementors, as we will see next, should be Monobehaviours only when strictly needed!

### Implementors

Before to build our entity, let’s define the last concept in Svelto.ECS that is the *Implementor*. As we know now, Entity Components are always interfaces and in c# interfaces must be implemented. The object that implements those interfaces are called *Implementors*. Implementors have several important characteristics:

- Allow to uncouple the number of objects to build from the number of entity components needed to define the entity data.
- Allow to share data between different components, as components expose data through properties, different component properties could return the same implementor field.
- Allow to create stub of the entity component interface very easily. This is crucial for leaving the engine code testable.
- Act as bridge between Svelto.ECS Engines and third party platforms. This characteristic is of fundamental importance. If you need unity to communicate with the engines you don’t need to use awkward workarounds, simply create an implementor as
**Monobehaviour**. In this way you could use, inside the implementor, Unity callbacks, like**OnTriggerEnter**/**OnTriggerExit**and change data according the Unity callback. Logic should not be used inside these callback, except setting entity components data. Here an example:

public class EnemyTriggerImplementor : MonoBehaviour, IImplementor, IEnemyTriggerComponent, IEnemyTargetComponent { public event Action<int, int, bool> entityInRange; bool IEnemyTriggerComponent.targetInRange { set { _targetInRange = value; } } bool IEnemyTargetComponent.targetInRange { get { return _targetInRange; } } void OnTriggerEnter(Collider other) { if (entityInRange != null) entityInRange(other.gameObject.GetInstanceID(), gameObject.GetInstanceID(), true); } void OnTriggerExit(Collider other) { if (entityInRange != null) entityInRange(other.gameObject.GetInstanceID(), gameObject.GetInstanceID(), false); } bool _targetInRange; }

*Remember the granularity of your EntityViews, entity components and implementors is completely discretional and up to you. More granular they are, more the chance are to be reusable.*

### Build Entities

Let’s say we have created our *Engines*, added them in the **EnginesRoot**, created its *EntityViews* that use *Entity Components* as interfaces to be implemented by one or more *Implementors*. It is now time to build our first entity. An Entity is always built through the *Entity Factory* instance generated by the EnginesRoot through the function **GenerateEntityFactory**. Differently than the EnginesRoot instance, an IEntityFactory instance can be injected and passed around. Entities can be built inside the Composition Root or dynamically inside game factories, so for the latter case passing the IEntityFactory by parameter is necessary.

so let’s see how the normal **BuildEntity<T>** is used inside the *EnemySpawnerEngine *code

```
IEnumerator IntervaledTick()
{
//this is of fundamental importance: Never create implementors as Monobehaviour just to hold
//data (especially if read only data). Data should always been retrieved through a service layer
//regardless the data source.
//The benefits are numerous, including the fact that changing data source would require
//only changing the service code. In this simple example I am not using a Service Layer
//but you can see the point.
//Also note that I am loading the data only once per application run, outside the
//main loop. You can always exploit this pattern when you know that the data you need
//to use will never change
var enemiestoSpawn = ReadEnemySpawningDataServiceRequest();
var enemyAttackData = ReadEnemyAttackDataServiceRequest();
var spawningTimes = new float[enemiestoSpawn.Length];
for (var i = enemiestoSpawn.Length - 1; i >= 0 && _numberOfEnemyToSpawn > 0; --i)
spawningTimes[i] = enemiestoSpawn[i].enemySpawnData.spawnTime;
_enemyFactory.Preallocate();
while (true)
{
//Svelto.Tasks can yield Unity YieldInstructions but this comes with a performance hit
//so the fastest solution is always to use custom enumerators. To be honest the hit is minimal
//but it's better to not abuse it.
yield return _waitForSecondsEnumerator;
//cycle around the enemies to spawn and check if it can be spawned
for (var i = enemiestoSpawn.Length - 1; i >= 0 && _numberOfEnemyToSpawn > 0; --i)
{
if (spawningTimes[i] <= 0.0f)
{
var spawnData = enemiestoSpawn[i];
//In this example every kind of enemy generates the same list of EntityViews
//therefore I always use the same EntityDescriptor. However if the
//different enemies had to create different EntityViews for different
//engines, this would have been a good example where EntityDescriptorHolder
//could have been used to exploit the the kind of polymorphism explained
//in my articles.
var enemyAttackStruct = new EnemyAttackStruct
{
attackDamage = enemyAttackData[i].enemyAttackData.attackDamage,
timeBetweenAttack = enemyAttackData[i].enemyAttackData.timeBetweenAttacks
};
//has got a compatible entity previously disabled and can be reused?
//Note, pooling make sense only for Entities that use implementors.
//A pure struct based entity doesn't need pooling because it never allocates.
//to simplify the logic, we use a recycle group for each entity type
var fromGroupId = ECSGroups.EnemiesToRecycleGroups + (uint) spawnData.enemySpawnData.targetType;
if (entitiesDB.HasAny<EnemyEntityViewStruct>(fromGroupId))
ReuseEnemy(fromGroupId, spawnData);
else
yield return _enemyFactory.Build(spawnData.enemySpawnData, enemyAttackStruct);
spawningTimes[i] = spawnData.enemySpawnData.spawnTime;
_numberOfEnemyToSpawn--;
}
spawningTimes[i] -= SECONDS_BETWEEN_SPAWNS;
}
}
}
```


Don’t forget to read all the comments in the example, they help to clarify even more the Svelto.ECS concepts. Due to the simplicity of the example, I am actually not using the **BuildEntityInGroup<T>** which is instead commonly used in more sophisticated products. In Robocraft every engine that handles the logic of the functional cubes handles the logic of ALL the functional cubes of that specific type in game. However often is needed to know to which vehicle the cubes belong to, so using a group per machine would help to split the cubes of the same type per machine, where the machine ID is the group ID. This allows us to implement fancy things like running one Svelto.Tasks task per machine inside the same engine, which could even run in parallel using multi-threading.

This piece of code highlight one crucial issue, which I may talk more about in the next articles…from the comment (in case you haven’t read it):

Never create implementors as Monobehaviour just to hold data. Data should always been retrieved through a service layer regardless the data source. The benefit are numerous, including the fact that changing data source would require only changing the service code. In this simple example I am not using a Service Layer but you can see the point. Also note that I am loading the data only once per application run, outside the main loop. You can always exploit this trick when you now that the data you need to use will never change.

Initially I was reading the data directly from the monobehaviour like a good lazy coder would have done. This forced me to create an implementor as monobehaviour just to read serialized data. It could be considered OK as long as we don’t want to abstract the data source, however serializing the information into a json file and reading it from a service request is much better than reading this kind of data from an entity component.

Every entity needs an unique ID. This unique ID must be unique regardless the descriptor type and the group it belongs to. I took this decision recently, so if I say otherwise in other articles, please let me know I will fix it.

## Communication in Svelto.ECS

One problem of which solution has never been standardized by any ECS implementation is the communication between systems. ECS communication must happen through entity data polling, but in SECS there are some exceptions:

### Reactive Engines

These are reactive callback that are called when an entity is added, remove or swapped. The entity is passed by ref and the values can be modified. These interfaces may change with SECS 2.8.

### DispatchOnSet/DispatchOnChange

The use of **DispatchOnSet<T>** and **DispatchOnChange<T>** Radically changed over the time. Nowadays is used only to implement communication between implementors that abstract underlying platform events and the engine that has the responsibility to handle that specific event. In a pure ECS scenario, without OOP integration, these tools become useless.

### The Sequencer

The Sequencer is exclusively used when is absolutely necessary there isn’t any other way to provide an execution order between engines.

### Entity Streams

Svelto ECS 2.8 introduces the concept of Entity Stream, please read the related articles to know more about it.

## Svelto.ECS and Unity

Svelto.ECS (as well as Svelto.Tasks) is designed to be platform agnostic. However I mainly use it with unity, so Unity extensions are provided. The **EntityDescriptorHolder** is an example. Using implementors as Monobehaviour let to exploit most of the Unity callbacks, but on other platforms the reasoning could be very similar. All that said, Svelto.ECS gives you the chance to abstract from Unity and you should use Unity classes as less as possible, especially Monobehaviours. It’s also important to keep in mind that the creation of GameObject(s) is uncoupled from the creation of Entities, the only thing they have in common is the fact that gameobject monobehaviours can be implementors. You can see from the example that enemy gameobjects and their ECS entities are built independently.

## Logic inside utility classes

You can create static utility classes to share code, that is not a problem as long as the static classes do not hold any state (they must be just a set of static functions)

**if you are new to the ECS design and you wonder why it could be useful, you should read my previous articles:**

[http://www.sebaslab.com/ioc-container-for-unity3d-part-1/](http://www.sebaslab.com/ioc-container-for-unity3d-part-1/)[http://www.sebaslab.com/ioc-container-for-unity3d-part-2/](http://www.sebaslab.com/ioc-container-for-unity3d-part-2/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-i-dependency-injection/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-i-dependency-injection/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-ii-inversion-of-control/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-ii-inversion-of-control/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/)[http://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/](http://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/)

**That’s all folks! FEEDBACK ME!**

Hi, I have a question. how to do you communicate between multiple roots?

this is a super interesting question, but first I need to reply with another question, what are you trying to achieve?

sorry I asked that from phone. Not sure, just curious on the topic :). Actually I started migrating a game to using Svelto ECS, and I’m surprised it is actually possible to have the game partially ECSized without much troubles. I tried to think to many usages but apart writing isolated Unit tests I can’t think to some serious use cases. In theory a sequencer can have engines from different roots. If a game part is isolated enough it may make sense using a different root for it (in example the trophy/profile part for a XBOX game may be a… Read more »

Hey I read your original post somehow it seems I didn’t read it all the first time. The mini managers idea sounds terrible what you do with that ? Remember engines can never be injected anywhere

Actually the managers are injected in engines and each engine implements a ITick interface. I have a mini manager for movement update, One for Shadows, One for culling, and the managers are runned in a determined order(move/ cull/ Shadows) and each manager update 3/4 engines. Since usually if you write something There is a reason for that I wanted to understand how to get rid of the order dependence… Well yes i can Just use svelto tasks and achieve the same execution order, but I feel There is a better way. Yes it is all’ rendering related stuff, but svelto… Read more »

Don’t use tick stuff either. We had something like that and ran away from it. Use tasks always. If you tell me what you need exactly I can write a new collection for you if the serialtaskcollection is not enough

Execution order must be driven only by sequencers, but if you need it a lot there is something wrong in your design.

Well. In example the 2d hyperfast Shadow caster use a order dependent algorithm. Light mesh generation/ Clipping against static intersecting Shadow casters,/ Clipping against moving obstacles.

Of course every moving thing Should move before the Shadow casting phase and many optimizations to remove invisibile stuff Should be performer After movement update phase and before Shadow casting.

It seems everything is order dependent. Ho do i Should design that to not be’ order dependent?

This is very rendering specific. ECS is a general purpose design, but of course must be adapted for each single specific case. For example, it’s true that svelto has several solutions that are close to data binding and mvvm but it will never beat a proper GUI framework. All that said, it sounds to me that your problem could be easily solved with a serialtaskcollection. Create it in the context, pass it as parameter of the constructor of each engine, register a new enumerator in the right order. Let it start. Now actually it may not be so straightforward but… Read more »

Contexts are actually very useful to isolate the engines like you said by for the same reason communication should not be needed. At most you can exchange data through service requests.

Hi, I do appreciate the ECS framework and all the examples. Great job,

I have however a questions about Group Entities.

Why there seem to be restriction of moving grouped entity out of group altogether or move un-grouped entity to a group?

Best regards,

Dawid

The swap group function is largely untested because I never needed to use it so far. All the other applications are therefore theoretical and may be avoided with different designs, so I need to be sure that there are practical applications before implementing them. What are your use cases?

One of our Ideas was to use grouping for creating a pool of objects, instead of instantiating new just put them in to pool or out of it. This can be achieved with specific use cases, or with making all entities grouped. And have separate groups for active(in use entities) and free(objects in pool). I was just wandering if there is practical need for restricting move of entity out of a group (as opposed to just moving it to another group – making a grouped entity un-grouped and vice versa) – I understand that there may have been no need… Read more »

Pooling was one of the reason why I introduced group swapping. Tbh I could make by default entities being built in a group as there isn’t really a reason to not do so. You didn’t miss anything it’s just I don’t want over complicate the framework. Mind some things tho: I am working already on several new features. Some of them will make building entities require less allocations however if you want to go allocation free you should use entity structs although they come with several limitations

Good stuff. Thanks again for sharing your awesome work.

A little thing I noticed btw MoveEntityView method name seem to be a bit of a missnoma as it does copy/reference but does not remove from the source list – got me confused a little 🙂

Best Regards,

Thanks there are some things to improve in the example.. I’ll try to fix most of the things this weekend!

Not found EGID in example?

I will fix it today but the example currently points to the database refactoring branch of svelto ecs

Hi, I’m trying to use Svelto.ECS in my turn based strategy project. The game has Routes (trade routes) consisting of Points. I’ve decided to group all Points belonging to the same Route as the idea of groups seems to suit the case. Nevertheless, I’ve discovered that group can’t be changed, so it is impossible to add or remove Points of the already created Routes. Is it intended behavior or I have missed any Svelto function? Perhaps, creating temporary group and further swapping between it and edited Route’s group can be a workaround?

Hello, I just noticed your comment. Yes swapping is the way to go in this case. A group of disabled point is OK if you don’t want to remove the entity.

Hi, is Svelto an alternative to Unity ECS or a package to use alongside it? I couldn’t find a description of what it does and I’m curious. Or maybe it is on this website and I don’t have enough knowledge to understand. Sorry if latter is the case.

Svelto is an alternative to unity ECS that can be used with it

Ok Im still not convinced 100% that components Should not have references to other components.

Take this example:

https://github.com/Darelbi/svelto-ecs-sandbox/blob/master/SveltoSandbox/Assets/Scripts/ECS/Engines/Lifter/LitferCollectionEngine.cs

This is a engine that keeps objects parented for the purpose of moving things

Along with a carrier.

I could code the hierarchy Just by querying entities and find entity views by querying IDs, but the code would be perfetcly (in this case) equivalent to the one present in the example. Am I missing some important point? Off course I would only maintain references from that engine only.

Put in this way how would have you written the code if the engine would handle a set of lifter entities and a set of liftable entities?

Instead of a List inside the component I would have used a List then the movement engine access the int list, and for each int in it, TryQuery the Liftable so the engine cann add to it the delta movement of the lifter.

I mean, I would have replacing the List of Liftable with a List of int

Yes that’s one way and I don’t see why not