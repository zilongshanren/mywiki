---
title: Entity Component System abstraction layers and modules encapsulation - Seba's
  Lab
url: https://www.sebaslab.com/ecs-abstraction-layers-and-modules-encapsulation/
author: Sebastiano Mandalà
published: '2022-03-20'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

## Introduction

This long-due article will conclude the series on *Entity Component System Code Design *and will explore the idea of *Inversion of Control layers* applied to ECS.

I design code in terms of layers for quite some time now and, in fact, I have hinted at it several times in this blog, but never went into detail. When this idea started to shape more concretely in my mind, I looked up to find out if the subject was already explored which led me to different articles with conclusions comparable to mine (albeit applied to OOP). After all, once the IoC-related principles are fully understood, following similar thought processes comes quite natural. A bunch of articles I found most interesting are:

[Layering](https://flylib.com/books/en/4.444.1.70/1/)(one of the many explanations of the*Dependency Inversion Principle*and the*Hollywood Principle*)[Inversion-Of-Control layer](https://www.sebaslab.com/wp-content/uploads/2022/03/Inversion-of-Control_Layer1.pdf)(Idea similar to the one exposed in this article, but for OOP. PDF edited by me to highlight the most interesting parts)

The theories discussed in this article are also linked to the other principles [Robert Martin](http://cleancoder.com/products) discussed in his OOD columns titled “** Granularity**” and “

**” which are about architectural code design with modules.**

[Stability](https://www.sebaslab.com/wp-content/uploads/2022/03/stability.pdf)I leave to you the decision to read them before or after finishing this article, but you should read them nevertheless.

## A recap

If you are not new to this blog, you should know by now that I didn’t just start to use *Entity-Component-Systems design* by chance. All my previous Inversion of Control related reasonings were leading directly to the use of patterns similar to ECS. If you didn’t read my articles or don’t remember my reasonings, is important to refresh them:

Inversion of Control is all about removing the control of the creation of dependencies from the user. The user is not more in charge of creating dependencies and injecting them, instead, dependencies must be created and injected by the “*framework*“. More importantly, the *framework *must take control over the execution flow, following the notable **Hollywood principle**. This is the bit that has been commonly overlooked by many as it’s not simple to see how the *framework *should control the flow of any possible application. In this article, I will go into detail while exploring and expanding the idea behind the concept of “*framework*” according to the IoC principles.

## Abstraction layers

Nothing is better than a practical example to clarify my arguments. Let’s assume that any kind of game engine (i.e. Unity or Unreal) is the “*framework*“. With any modern game engine, some IoC is usually involved. With *Unity*, the user cannot create a **Monobehaviour (although the user can add them at runtime, it’s still the framework to create the actual objects)**. The ** Monobehaviour** doesn’t have constructors. Only the

*framework*can decide when to create the

**object and when it’s activated and executed, following the**

**Monobehaviour**[(a rudimental form of Inversion of Flow Control).](https://www.sebaslab.com/wp-content/uploads/2022/04/TemplateAndStrategy.pdf)

**strategy method**patternI don’t remember much about *Unreal*, but from what I recall I believe actors can declare specific components (like Renderer, Physic and so on) that identify them as objects that can be rendered, simulated and so on. While I think the user still creates actors directly, it’s the *framework *that is in **charge of controlling when rendering and or simulating the physic of actors.**

As game developers, *we are very accustomed to thinking about the framework from a black and white point of view*. The code either is or is not part of the framework. If it’s not a framework, it’s user code.

*This lack of gradients is not a problem until the codebase starts to grow and responsibilities inside it start to become more or less generic*.

If the user cannot write *framework* level code, how can the Inversion of Flow Control be applied for more specialised behaviours than the game engine frameworks usually provide? Is it possible instead to find and encapsulate common behaviours in black-boxed modules so that these behaviours can be reused regardless of their complexity? When would we decide to draw a line on the complexity the codebase has reached? How does the need to know, at all times, every behaviour affect the maintainability of our codebase?

If we can access at any moment any part of the code without any rule to classify it, it will be simple, even with ECS, to create code that is too interdependent and thus hard to refactor. If you ever used a so-called *IoC container* (i.e.: *ZenInject *or *StrangeIoC*) these words may resonate with you since these tools push the user to create flat two ways relationships, allowing objects to know each other at all times leading directly to the well-known spaghetti code scenario (any behaviour can be executed at any time).

This is where the concept of abstraction layers comes into play and it’s all about finding the simple rules that allow us to split our code not just into different systems (or classes in OOP), but also into different modules where the only relationship is if present, strictly hierarchical (as more specialised modules are composed through generic modules, but never vice versa).

To avoid possible confusion, we can define a module as a separate assembly/dll which is the best way to encapsulate behaviours beyond the classic ways we are used to.

## Use abstraction layers with ECS

Once the codebase starts to grow, behaviours applied to entities naturally start to shape in more or less generic (abstract) forms. Behaviours provided by game engines, like the ability to render an entity, are at the topmost level of abstraction. However as the game codebase grows, the user will start to identify common behaviours among the game entities. For example, If it’s true that a game can have several types of weapons, their behaviours are not exclusive to specific models. If we talk about ballistic, a class of weapons can shoot hitscan type of lasers beams, while another class of weapons can instead shoot projectiles with a parabolic trajectory. Some weapons may need ammo and so need to recharge, while other weapons don’t. All the weapons may apply damage.

The behaviour of the projectile itself would probably lie in a separate module, after all the weapon entities and the projectile entities are separate entities with separate sets of behaviours.

So what’s new about this reasoning? The idea is that instead to let these behaviours lie in the same assembly, the user would black box (encapsulate) them in different modules.

This may turn into a practical scenario where a **Weapon module** and a **Projectile module** exist. If we decide that *Weapon systems are able to spawn projectiles, then the Weapon module would directly know the Projectile module*, but the opposite is impossible as circular dependencies are not allowed between assemblies. [In Unity, a module is defined through an asmdef](https://docs.unity3d.com/Manual/ScriptCompilationAssemblyDefinitionFiles.html)

*and in this case the weapon assembly would need to know about the projectile assembly. However cyclic dependencies are forbidden, hence the projectile module would never know about weapons.*

In a complex scenario, the number of modules can become in the order of hundreds with several layers of abstraction. An example can look like

![](../../assets/6ea53bc40f3f4635.png)

## Abstraction Layers Rules

So you wonder, how are the abstraction layers in any way related to Inversion of Control? This happens by mixing the [ Dependency Inversion Principle](https://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/) which states:

*High-level (*policymakers applying behaviours on entities*) modules should not depend on details from low-level *(specialised entities)* modules. Both should depend on abstractions *(in OOP it means **Interfaces**, in ECS they are **Components**).

and the **Hollywood principle** that states:

*“Don’t Call Us, We’ll Call You.” *(in OOP services or strategy pattern based objects will call your code, in ECS Entities composed of specific *Components *will be iterated by more or less abstracted* Systems*)

The original idea behind these principles is that the conventional way to let policymakers code know directly specialised objects/entities is considered bad design as it makes the high-level code too tied to the provided objects/entities implementations and hence prone to be volatile. So the high-level modules must know implementations indirectly through *interfaces *that the low-level code must implement.

In ECS world this is translated into generic modules providing and owning the* Entity Components* and the *Systems *that apply generic *behaviours *to user-specialised *Entities *through their composed *Components*. However, in our case, the abstracted “*framework*” module also takes control over when and what entities to process. The user does not know how the entities are processed by the systems but is only aware that entities with provided components will be processed by the systems coming from the generic modules. *Entities Behaviours* are executed through *Entity Components* and are applied only to the entities defining those components.

In practical words (using Svelto.ECS terms): the *projectile layer* provides the **ProjectileComponent **and/or the extendible **ProjectileEntityDescriptor**. The layer provides also all the **Engines **(systems) that can query all the entities with a **ProjectileComponent **and apply the *Projectile Behaviour *to them.

Once the engines are added to the EnginesRoot, any entity using the provided components will be processed by the engines by applying the behaviours provided by the module.

## Abstraction layers in practice

At this point, you may have an idea of what’s going on and you may wonder how to put everything into practice.

My first advice is: *Early abstraction is the root of all evil*, so do not try to figure out your layers immediately. Just write your code in such a way it can be refactored later on. When common behaviours emerge, it will be simpler to repack the components and systems into separate modules.

In order to show you how things work in practice and lay down some rules, I decided to expand the [MiniExample 7: Stride Turrets](https://github.com/sebas77/Svelto.MiniExamples/tree/master/Example7-Stride-Turrets) that I have already discussed [in my previous article](https://www.sebaslab.com/svelto-miniexample-7-stride-engine-demo/). Remember *you don’t need Stride Engine to run it*, just download the project, open it with your .net IDE and run **Turrets.Windows**.

The code was already written in terms of layers, but I didn’t split it into assemblies as it was outside my previous scope. Splitting it now has been proved simple and the project looks like this:

![](../../assets/93c19bcf0d3d5bd5.png)

Where all the “Layers” are actually separate *.net libraries*, while **Turrets.Windows** is the *actual executable* that uses the class **TurretsCompositionRoot **from the project **GameLayer**

**GameLayer **in this case is the most specialised layer and it’s the actual *game composition root*.

The **GameCompositionRoot** looks like this:

void GameCompositionRoot() { TransformableContext.Compose(AddEngine); SimplePhysicContext.Compose(AddEngine); StrideAbstractionContext.Compose(AddEngine, _ecsStrideEntityManager); PlayerContext.Compose(AddEngine, this.Input, _ecsStrideEntityManager, _enginesRoot, SceneSystem); BulletContext.Compose(AddEngine, _ecsStrideEntityManager, _enginesRoot, SceneSystem); EnemyContext.Compose(AddEngine, _ecsStrideEntityManager, _enginesRoot); }

where you can easily see all the independent contexts being composed.

Now the rules at this point are quite blurred, you can choose your own path once you understand the concepts, but this is what I usually do:

- The Game Composition root is the composition root where all the contexts are composed, thus the wanted behaviours are added.
- The Game Composition root, as a normal composition root, must also create all the non-ECS dependencies that are injected into the other composition roots if required (including the
**EnginesRoot**) - The abstracted Contexts are stateless static classes that have the only responsibility to add the engines belonging to the layer to the
**EnginesRoot**. They look like:

public static void Compose(Action<IEngine> AddEngine, BulletFactory bulletFactory) { AddEngine(new MoveTurretEngine()); AddEngine(new AimBotEngine()); AddEngine(new FireBotEngine(bulletFactory)); }

*All the engines inside each layer (module) are internal! This is the way you can encapsulate the logic inside the modules. The game doesn’t have any clue about how each module works nor does*each module know*about other modules, other than as dependency references in the assembly if necessary.*- Each context can have its own
*Mock Composition Root*. For example,**PlayerContext**could have a**PlayerCompositionRoot**assembly that references all it needs to create a Mock executable to test just the player context functionalities. This is actually useful for testing purposes. - Each context must provide the
*Components*that the low-level modules are going to use to define their specialised entities, for example, the**PlayerEntityDescriptor**defined in the**PlayerContext**is actually an extension of**PhysicEntityDescriptor**and**TransformableEntityDescriptor**

public class PlayerBotEntityDescriptor : ExtendibleEntityDescriptor<PhysicEntityDescriptor> { public PlayerBotEntityDescriptor() { ExtendWith<TransformableEntityDescriptor>(); } }

However, the real game player bot entity is defined by the **GameLayer **as:

class GamePlayerBotEntityDescriptor : ExtendibleEntityDescriptor<PlayerBotEntityDescriptor> { public GamePlayerBotEntityDescriptor() { Add<TurretTargetComponent>(); } }

The Game needs to define a player also as a target for enemies, but the **TurretTargetComponent **is provided by the *Enemy Layer*. The *Player Layer* doesn’t need to be aware of the *Enemy Layer* at all.

As you can see the *Physic Layer* provides the components and engines to enable physic behaviours. The *Transformation Layer* provides components and engines to let entities be transformed in the world space. The *Player Layer* provides components and engines to enable the player behaviours. The game context eventually composes entities using components from the high-level modules to enable all the required behaviours through the enabled engines.

## Some more words about Abstraction Layers with Svelto.ECS

Once the user starts to identify the behaviours shared between entities and encapsulate them in new modules, the user will easily identify how generic or specialised these behaviours will be. Some modules can be so generic that can be shared across different games. This could be useful for large teams working on different projects. More game-specialised modules are still abstracting behaviours, but these modules wouldn’t make sense outside the game project itself.

The way you will code the engines in these modules actually changes using [Svelto.ECS](https://github.com/sebas77/Svelto.ECS).

Very generic behaviours will query the entities to iterate using **FindGroups** (the code doesn’t imply which entities are using the module components), as shown here:

class VelocityComputationEngine : IQueryingEntitiesEngine, IUpdateEngine { public string name => this.TypeName(); public void Step(in float deltaTime) { var groups = entitiesDB.FindGroups<VelocityComponent, DirectionComponent, SpeedComponent>(); foreach (var ((velocities, directions, speeds, count), _) in entitiesDB .QueryEntities<VelocityComponent, DirectionComponent, SpeedComponent>(groups)) { for (int i = 0; i < count; i++) { velocities[i].velocity = directions[i].vector * speeds[i].value; } } } public EntitiesDB entitiesDB { get; set; } public void Ready() { } }

more specialised engines, inside more specialised modules, will instead use *group compounds tags* ( the code implies which entities are using the module components) to query the entities to iterate on:

class AimBotEngine : IQueryingEntitiesEngine, IUpdateEngine { public EntitiesDB entitiesDB { get; set; } public void Ready() { } public string name => this.TypeName(); public void Step(in float deltaTime) { var targetGroups = entitiesDB.FindGroups<PositionComponent, TurretTargetComponent>(); foreach (var ((matrix, directionComponent, count), _) in entitiesDB .QueryEntities<MatrixComponent, LookAtComponent>(BotTag.Groups)) { foreach (var ((targetPosition, countTargets), _) in entitiesDB .QueryEntities<PositionComponent>(targetGroups)) { //Iterate the current set of turrets for (int i = 0; i < count; i++) { var j = i < countTargets - 1 ? i : countTargets - 1; var vector = targetPosition[j].position - matrix[i].matrix.TranslationVector; vector.Normalize(); //make each turret aims at a different target in a round robin fashion //in this demo there is just one target so they will all point to the same one //I really didn't test other scenario so who knows if this works directionComponent[i].vector = vector; } } } } }

## Conclusions

We showed how the *Dependency Inversion Principle* and the *Hollywood Principle* are very relevant also with ECS design to push the user to write reusable modular code that can encapsulate shared entity behaviours.

ECS also pushes the user to naturally write modules that follow the *Granularity *and *Stability *principles, which make complex projects easier and less costly to maintain and refactor.

We introduced a concept similar to the *Inversion Of Control Layers* (which I call Abstraction Layers)* *to show that any behaviour can be encapsulated in a “framework” module used by specialised modules. Finer granularity is encouraged to promote complete and true *Inversion of Control* where the high-level modules take control over the low-level modules entities.

As the codebase grows, the number of emerging shared behaviours and therefore modules will grow. Changing behaviours is now a matter to change specific assemblies without affecting the rest of the codebase.