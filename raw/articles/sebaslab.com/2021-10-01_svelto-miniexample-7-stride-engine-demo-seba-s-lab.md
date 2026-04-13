---
title: 'Svelto MiniExample 7: Stride Engine demo - Seba''s Lab'
url: https://www.sebaslab.com/svelto-miniexample-7-stride-engine-demo/
author: Sebastiano Mandalà
published: '2021-10-01'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

![](../../assets/70bf23958b01bf71.png)

It happened again, I fell victim to my creativity block (read I didn’t find time to write new articles)! This means that several months have passed since my last update and now the new version of Svelto.ECS is much, much bigger than it was supposed to be.

Oh, well! To get over this impasse, I had to finish a new demo with a game engine different from Unity. While it was a pleasure to work with *Stride*, I did struggle with the design of the demo itself, and therefore the final result is nothing to be proud of, but at least, it is enough to be able to write this article and finally move on (that the list of things to do is very long!)

I started this new mini example with two goals in mind, the first, to write a new demo without Unity, the second to show how to use *Entity References *in Svelto.ECS to walk a graph and discuss a bit about when and when not to use ECS to write specific algorithms, following the reasoning of [my previous article](https://www.sebaslab.com/oop-abstraction-layer-in-a-ecs-centric-application/).

Let’s start with presenting the * Stride Engine*!

![](../../assets/523682b70802a09f.jpeg)

Stride, formerly known as *Xenko*, is an [ open-source](https://github.com/stride3d/stride), free to use, game engine that has some fantastic features and can be used to create complete games. The community around it, which can be found on

[discord](https://discord.gg/EraMSJEvDE), is big and lively, although as it happens with all the open-source projects out there, only a few people stick around long enough to become the pillars of the project and only reliable source of help for newcomers like I was.

The Stride editor presents itself very professionally, is clean and slick, but differently than Unity, it is not necessary to run or build your Stride projects, in fact, the engine libraries can be used independently and downloaded as *NuGet *packages.

Since Svelto.ECS is platform-agnostic, it can work with any C# game engine out there. It’s been a long time I wanted to test Stride, but I knew perfectly that it would have been a huge effort to start a demo on a new platform as my spare time is getting smaller and smaller. In fact, while I would LOVE to make more mini-examples on more platforms (there are so many!), I won’t repeat this experiment as I have tons of other Svelto related tasks to finish. **My hope was, and still is, to see more people using Svelto.ECS on platforms other than Unity** and maybe this new example may help to convince someone to contribute to the Svelto.ECS project building more extra-Unity mini-examples for the sake of our community (as I don’t see myself working professionally with something different than Unity anytime soon).

Unfortunately, the demo itself is ugly, so like in real life, get ready to experience disappointment and learn new stuff in the process :).

Download the Mini-Examples from the GitHub repository and open the project [Example 7 Stride Turrets](https://github.com/sebas77/Svelto.MiniExamples/tree/master/Example7-Stride-Turrets).

The idea was to create a sort of tower defense game, but I didn’t want to code more features than I actually needed to write this article, so the result is just a good foundation for someone to pick up and build new features on top.

Open the project with your IDE and either install Stride or download the Stride libraries from NuGet (your IDE should be able to download them automagically). Run the game and you should see something ugly like this:

![](../../assets/f7c64a025f3992ea.png)

you will be able to control the mini bot with **WASD **and the enemies will show off their hierarchical transformations, moving in circles and aiming at you. They will also be able to randomly shoot red soap bubbles at you, but that’s it. There are no more functionalities as I didn’t need to write anything else to proceed with what you are reading right now.

So let’s dig in the code and see how Svelto.ECS has been integrated with Stride:

Stride works in a similar fashion to Unity, with a system built upon object-based components linked to object-based entities. It’s very similar to the concept of **Gameobject **and **Monobehaviour **with the same benefits and limitations coming from the design. Stride design is however more powerful than Unity’s, as c# is not integrated as a *scripting language, *but as an independent coding platform. If the users wish to, they can take control over everything, starting from the classic C# application *Main *method. This is very useful as it enables more natural dependency injection patterns and thus a less awkward integration with Svelto.ECS.

There could be several ways to integrate Svelto.ECS with stride, but I reckoned the most elegant to be extending the Stride **Game **class to create a *Game Composition Root* that can create and inject all dependencies necessary.

This file looks like this:

using System; using Stride.Engine; using Stride.Games; using Svelto.ECS.Schedulers; namespace Svelto.ECS.MiniExamples.Turrets { public class TurretsCompositionRoot : Game { public TurretsCompositionRoot() { GameStarted += CreateCompositionRoot; } void CreateCompositionRoot(object sender, EventArgs e) { //Create a SimpleSubmission scheduler to take control over the entities submission ticking _scheduler = new SimpleEntitiesSubmissionScheduler(); //create the engines root _enginesRoot = new EnginesRoot(_scheduler); //create the Manager that interfaces Stride Objects with Svelto Entities _ecsStrideEntityManager = new ECSStrideEntityManager(Content); var entityFactory = _enginesRoot.GenerateEntityFactory(); var entityFunctions = _enginesRoot.GenerateEntityFunctions(); _mainEngineGroup = new TurretsMainEnginesGroup(); //Services is a simple Service Locator Provider. EntityFactory, EntityFunctions and ecsStrideEnttiyManager //can be fetched by Stride systems through the service Locator once they are registered. //There is a 1:1 relationship with the Game class and the Services, this means that if multiple //engines roots per Game need to be used, a different approach may be necessary. Services.AddService(entityFactory); Services.AddService(entityFunctions); Services.AddService(_ecsStrideEntityManager); GameStarted -= CreateCompositionRoot; } void AddEngine<T>(T engine) where T : class, IGetReadyEngine { _enginesRoot.AddEngine(engine); if (engine is IUpdateEngine updateEngine) _mainEngineGroup.Add(updateEngine); } protected override void BeginRun() { var entityFactory = _enginesRoot.GenerateEntityFactory(); var entityFunctions = _enginesRoot.GenerateEntityFunctions(); //SimplePhysicContext AddEngine(new VelocityComputationEngine()); AddEngine(new VelocityToPositionEngine()); //TransformableContext AddEngine(new LookAtEngine()); AddEngine(new ComputeTransformsEngine()); //HierarchicalTransformableContext AddEngine(new ComputeHierarchicalTransformsEngine()); //Stride Abstraction Layer AddEngine(new SetTransformsEngine(_ecsStrideEntityManager)); //Player Context AddEngine(new PlayerBotInputEngine(this.Input)); AddEngine(new BuildPlayerBotEngine(_ecsStrideEntityManager, entityFactory, SceneSystem)); //BulletsContext var bulletFactory = new BulletFactory(_ecsStrideEntityManager, entityFactory); AddEngine(new BulletSpawningEngine(bulletFactory, _ecsStrideEntityManager, SceneSystem)); AddEngine(new BulletLifeEngine(entityFunctions)); //TurretsContext AddEngine(new MoveTurretEngine()); AddEngine(new AimBotEngine()); AddEngine(new FireBotEngine(bulletFactory)); } protected override void Update(GameTime gameTime) { //submit entities _scheduler.SubmitEntities(); //run stride logic base.Update(gameTime); //step the Svelto game engines. We are taking control over the ticking system _mainEngineGroup.Step(gameTime.Elapsed.Milliseconds); } protected override void Destroy() { _ecsStrideEntityManager.Dispose(); } EnginesRoot _enginesRoot; SimpleEntitiesSubmissionScheduler _scheduler; TurretsMainEnginesGroup _mainEngineGroup; ECSStrideEntityManager _ecsStrideEntityManager; class TurretsMainEnginesGroup : UnsortedEnginesGroup<IUpdateEngine, float> { } } }

which is simply used like any other Stride Game class as:

namespace Svelto.ECS.MiniExamples.Turrets { static class Turrets { static void Main(string[] args) { using (var game = new TurretsCompositionRoot()) { game.Run(); } } } }

I won’t go into full details with the dissection of the code here, as I left a ton of comments in the project itself, but essentially the composition root initialises the basic Svelto.ECS objects (the *SubmissionScheduler*, the *EnginesRoot*) and adds the engines needed to handle the logic of the entities in the game.

However Stride is an Object-Oriented engine, so we need to apply the patterns explained in my previous article on OOP abstraction to be able to interface Stride objects with Svelto entities.

In order to do so, I created an **ECSStrideEntityManager **which is found in the *Stride Abstraction Layer*.

The implementation of it is similar to the pattern I have previously explained, in fact, I expect all the Abstracting Managers to look more or less the same:

using Stride.Core.Mathematics; using Stride.Core.Serialization.Contents; using Stride.Engine; using Svelto.DataStructures; namespace Svelto.ECS.MiniExamples.Turrets { public class ECSStrideEntityManager { public ECSStrideEntityManager(IContentManager contentManager) { _contentManager = contentManager; } //Instantiate and register a new entity from a previously registered prefab public uint InstantiateEntity(uint prefabID, bool useTRS) { var entity = _prefabEntities[prefabID].Instantiate()[0]; _entities.Add(entity); entity.Transform.UseTRS = useTRS; return _entityCount++; } //register an already existing and Stride pre-created entity public uint RegisterStrideEntity(Entity entity) { _entities.Add(entity); return _entityCount++; } //convert a svelto compatible ID to an Entity public Entity GetStrideEntity(uint entityID) { return _entities[entityID]; } //load a prefab resource and register it as a prefab. Of course this method is very naive and can be made //async and suitable to load several prefabs at once. public uint LoadAndRegisterPrefab(string prefabName, out Matrix prefabTransform) { var prefab = _contentManager.Load<Prefab>(prefabName); _prefabEntities.Add(prefab); prefabTransform = prefab.Entities[0].Transform.LocalMatrix; return _prefabsCount++; } public void Dispose() { } uint _entityCount; uint _prefabsCount; readonly FasterList<Entity> _entities = new(); readonly FasterList<Prefab> _prefabEntities = new(); readonly IContentManager _contentManager; } }

I believe the code is self-explanatory and doesn’t need further comments, but the goal is clear: to have an interface between Stride Objects and Svelto.ECS entities (and vice-versa).

Moving on, from the project folders structure, you will notice that I methodically split the code into different layers of abstraction (I promise, I talk about this theory in the next article) with each layer ready to be (potentially) turned into a reusable and redistributable independent assembly.

![](../../assets/ffa872e7177212be.png)

The more generic and reusable the code is, the more abstract is from the specialised game layer. In this sense, the *Transformable Layer* is more abstract than the *Physic Layer* that is more abstract than the *Stride Abstraction Layer* that is more abstracted than the *Bullets Layer* that is more abstract than the *PlayerBot Layer*.

Pay attention that with a bit of work I could have made the *Bullets Layer* and *Player Bot Layer* more abstracted than the *Stride Abstraction Layer*, but make those layers reusable for games made with other platforms seemed a bit too much of an abstraction :). Nevertheless, you may imagine how this would be possible using interfaces instead of direct implementations for the resource managers and the stride API.

Now, going back to the demo functionalities, one goal I wanted to achieve is to let Svelto engines handle the transformation matrix instead to delegate the responsibility to Stride. This is normally not necessary, but I wanted to show how game-engine level systems can be written in Svelto.ECS.

Luckily we can tell Stride to not compute any transformation matrix and just use the transformation matrices we feed it with. This can be achieved with code similar to this:

strideEntity.Transform.UseTRS = false; //ignore Stride internal transformation systems

In order to prove that this works, I used a very simple hierarchical transformation, letting the turret bases move in a circular motion and the shooting top turret be attached to them, while also aiming at the current target.

The base turret movement is handled by *MoveTurretEngine*.

The top turret aiming system is handled by *AimBotEngine*.

The hierarchical transformation is handled by the abstract engine *ComputeHierarchicalTransformsEngine*.

The final transformation matrix is computed by the abstract engine *ComputeTransformsEngine*.

Eventually, the Stride Entity matrix is set by the abstract engine *SetTransformsEngine*.

The hierarchical relationship between entities is simply handled through *Entity References*. Now, I know that some wondered if there are better and more efficient ways to handle graphs with ECS and the answer is simply that, in case something more efficient is necessary, you need a black-boxed dedicated library that may or may not be data-oriented, but can be interfaced with the ECS framework using my abstraction layer theory. * This is basically what also Unity did with the DOTS animation package and the DataFlowGraph library.* The library uses efficient algorithms dedicated to graph structures, but then presents the data in an ECS compatible way. It’s as simple as that, you don’t need to always use entities as you don’t need to use objects (in fact in this case you are better of with procedural programming), but this doesn’t matter at all as long as the libraries are correctly interfaced with the ECS framework.

I think that’s it, there isn’t much else to add. The demo is very simple and working with Stride has been a joy for how intuitive and effective the API is.

As usual you can leave any feedback in the comments section.

Very good tutorial. In addition, I accidentally clicked a one-star rating, which is a mistake