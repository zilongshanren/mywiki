---
title: OOP abstraction layer in an ECS-centric application - Seba's Lab
url: https://www.sebaslab.com/oop-abstraction-layer-in-a-ecs-centric-application/
author: Sebastiano Mandalà
published: '2021-01-05'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

There are several reasons why programmers have a hard time wrapping their heads around ECS concepts. Having learned to code with an OOP-centric language is one of them as ECS reasonings are often at the antipodes of the OOP ones.

Being Object-Oriented Programming so popular means that it is not simple to get away without using it, so like it or not, it may be necessary to mix ECS and OOP code. However, this is not a bad thing per se, nor it is a contradiction as the same already happens when using OOP with a multi-paradigm language. With languages like c++ and c#, OOP is in fact regularly used with procedural data structures and concepts.

This article will show how to make the relationship between ECS and OOP work avoiding bloated and awkward code as a result of the mix. After all, it’s not like ECS can solve elegantly all the possible programming problems. With [Gamecraft](https://store.steampowered.com/app/1078000/Gamecraft/) (Now Robocraft 2), which is an ECS-centric product, we found some limitations, although none were crippling our development process (with the notable exception of implementing GUI without a dedicated ECS-based framework). Admittedly, Gamecraft is a particular game with specific problems, so for other kinds of games ECS may not work out so well. Game development, as we know, encompasses a huge variety of problem domains and forcing ECS to solve all these problems can be as demanding as trying to solve the same problems with OOP only.

On the other hand, I have spent a considerable amount of time investigating what the limits of the ECS-centric approach are and although some are more evident than others, I ended up realising that the lack of ECS-based frameworks developed to handle specific responsibilities contributes to the disorienting feeling of using ECS for the first time. For example, we found developing GUIs in ECS anything but frictionless. However, since the parallel between ECS and the OOP MVC pattern is obvious to me, I realised that the problem is more due to the fact that an ECS-based GUI Framework doesn’t exist, more than that ECS is awkward to use for GUIs.

### Using Procedural Libraries

Before digging further into the issues of the weird relationship we are discussing in this article, let’s imagine a world without OOP:

ECS is closer to procedural programming than it is to Object-Oriented programming. Hence it’s natural that ECS would work better with procedural libraries instead of OOP libraries. Without needing to handle objects, procedural libraries are perfect companions.

In [MiniExample 4: SDL](https://github.com/sebas77/Svelto.MiniExamples/tree/master/Example4-NET-SDL), the *SDL library* is a procedural library that doesn’t use objects. This makes it simpler to call public functions to feed directly entities data. For example:

foreach (var ((transforms, colliders, count), _) in entitiesDB .QueryEntities<TransformEntityComponent, BoxColliderEntityComponent>( GameGroups.DynamicRigidBodyWithBoxColliders.Groups)) for (var i = 0; i < count; i++) { ref var transformEntityComponent = ref transforms[i]; ref var boxColliderEntityComponent = ref colliders[i]; var point = transformEntityComponent.Interpolate(normalisedDelta); var aabb = boxColliderEntityComponent.ToAABB(point); var (minX, minY) = aabb.Min; var (maxX, maxY) = aabb.Max; _graphics.DrawBox(Colour.GreenYellow, (int) Math.Round(minX), (int) Math.Round(minY) , (int) Math.Round(maxX), (int) Math.Round(maxY)); }

**DrawBox** is a procedural function that draws boxes using, in this case, data that comes directly from entities.

Another example can be found in *Gamecraft *where we use a [Compute shader-based rendering pipeline](https://assetstore.unity.com/packages/tools/utilities/gpu-instancer-117566#releases) to render almost everything seen in the game (except the main character and the GUI). Uploading compute buffers to the GPU becomes very ECS-friendly as component arrays can be uploaded as they are.

Uploading the array of transform components to the GPU looks similar to:

```
GPUInstancerAPI.InitializeWithMatrix4x4Array(_gpuInstancerPrefabManager, prototypeID, transformComponentArray);
```


An old working example of this can actually be found among my GitHub repositories as well and I discuss it in this article:

### Using ECS Libraries

Games are complex beasts. Developing them is not just about the high-level logic, but many low-level aspects must be developed too. These low-level aspects are usually provided in different forms, depending on the game engine adopted. However what if the game engine is written in ECS to start with?

*This is what’s happening with unity DOTS*. Once the user sees DOTS ECS as an engine library instead of a game framework, they will realise its true power which will open the door to ECS-centric applications instead of OOP-centric applications.

In Gamecraft, all the game logic is written with *Svelto.ECS*, but the physic is simulated with the DOTS ECS physic library with all the performance benefits that come with it.

DOTS ECS shows a sound strategy to develop ECS-based libraries that don’t need to share the same framework used to develop the game. This approach is based on the synchronization of entity data between the game and the libraries. In this case, the DOTS entities would be closer to the Unity Engine more than the game layer. In Gamecraft, for example, the DOTS entities are just Havok Rigidbodies.

A synchronization layer is written on purpose and provides engines to synchronise the Svelto.ECS entities with the DOTS entities and vice versa. A synchronization system/engine can look like this:

[DisableAutoCreation] class CopyPhysicStatesFromUECSToSveltoSyncEngine : SyncUECSToSveltoEngine, IQueryingEntitiesEngine { public EntitiesDB entitiesDB { private get; set; } public void Ready() { } protected override JobHandle OnSync(JobHandle inputDeps) { groups.Clear(); EntityManager.GetAllUniqueSharedComponentData(groups); var handle = JobHandle.CombineDependencies(inputDeps, Dependency); //UECS entities are split in groups using the SharedComponent UECS feature. The group subdivision //matches the Svelto.ECS group subdivision foreach (UECSSveltoGroupID group in groups) { //Fetch the group of entities from Svelto. The mapper is necessary as we will fetch the entities //through indices if (entitiesDB.TryQueryNativeMappedEntities(group, out NativeEGIDMapper<RigidBodyEntityStruct> simulationMapper)) { //iterate all the UECS entities per GROUP var jobhandle = Entities.WithSharedComponentFilter(group) .ForEach((in Translation position, in Rotation rotation, in PhysicsVelocity physicVelocity, in UECSSveltoEGID sveltoEGID) => { //fetch the svelto entity and copy the values from UECS in it ref RigidBodyEntityStruct physE = ref simulationMapper.Entity(sveltoEGID.egid.entityID); physE.position = position.Value; physE.rotation = rotation.Value; physE.velocity = physicVelocity.Linear; physE.angularVelocity = physicVelocity.Angular; }).ScheduleParallel(inputDeps); handle = JobHandle.CombineDependencies(handle, jobhandle); } } Dependency = handle; return handle; } NativeEGIDMapper<RigidBodyEntityStruct> _simulationMapper; readonly System.Collections.Generic.List<UECSSveltoGroupID> groups = new System.Collections.Generic.List<UECSSveltoGroupID>(); }

In case you may wonder, performance is not an issue here. The code is *vectorised by Unity Burst *and *executed in parallel by Unity Jobs*, you will need hundreds of thousands of entities in-game before such a copy strategy can start to be an issue performance-wise.

The same strategy is demonstrated in [MiniExample 1: Doofuses (UECS based)](https://github.com/sebas77/Svelto.MiniExamples/tree/master/Example1-DOTS-DoofusesMustEat/DOOFUSES_UECS) where I use the package **Hybrid Renderer ECS package** to render the Doofuses meshes.

### OOP abstraction layer

In order to understand this chapter, is important to have clear in mind that I always talk in my articles about *ECS-centric applications *and as discussed, ECS-centric applications may need to work with OOP libraries. As the two design approaches are almost orthogonal (I see systems executed horizontally, while object methods are called vertically), integrating an OOP library is much less intuitive and fluid than what we have seen so far. In order to solve the problem, I mainly use two approaches. The atypical and actually not recommended* Svelto.ECS EntityViewComponent/Implementor approach *and the much better solution that I call the *OOP abstraction layer*. This solution is superior to the **EntityViewComponent **approach in many cases. I have written a couple of new mini-examples to see how the OOP Layer works.

Let’s start with [MiniExample 1: Doofuses with GameObjects](https://github.com/sebas77/Svelto.MiniExamples/tree/master/Example1-DoofusesMustEat/DOOFUSES_GAMEOBJECTS).

This example is particularly important for unity developers. *It shows how I extensively use DOTS without using DOTS ECS at all*. The approach is very similar to what is done in Gamecraft for the rendering path, but in this case, I want to abstract Gameobjects as actual OOP objects. The same reasoning can be applied to any object provided by other libraries. The mini example shows Performance is as high as the DOTS ECS version of Doofuses, with the exception of the Gameobject-based* rendering pipeline, which becomes the bottleneck*.

There is a practical reason behind the OOP abstraction layer as well. Coders by their nature tend to take the path of least resistance. *This path is there if allowed to be there and if the framework doesn’t control where the path leads it can take to places where the coder will get lost.*

![](https://i0.wp.com/github.com/sebas77/Svelto.MiniExamples/blob/master/Example1-DoofusesMustEat/2020-12-22%2016-05-22.gif?w=1080&ssl=1)

Coders by their nature tend to take the path of least resistance.

myself

*It’s called the OOP abstraction layer because coders must not have direct access to the objects that the layer abstracts*. If the layer would allow direct access to the objects, it wouldn’t be an abstraction layer anymore. More importantly than that, coders will 100% absolutely start to use and abuse those objects, accessing their public data and methods inside ECS systems. *This will invariably lead coders to mix ECS and OOP, but because of the path of least resistance, a coder who is learning ECS, will stop thinking in terms of entities and revert to thinking in terms of objects which, in a short time, would make the coder abandon ECS and never look back.*

*For this reason, the OOP abstraction layer must be black-boxed and the objects only used internally by the few engines present in the layer that have the responsibility to access the objects for specific abstracting reasons*. In the **Doofuses **example, I use the game objects exclusively to set their positions. This is a straightforward case and it’s true that may become more bloated for more complicated scenarios, *but the bloat will be encapsulated in the layer and hidden from the final user.*

In c# these black-boxed layers can easily and intuitively be packaged in separate assemblies/modules so that the rule to use objects internally will be enforced by the compiler.

#### The Resource Manager

In the Doofuses Example, the packaged abstraction layer looks like this:

![](../../assets/c81a0054b1dab8c3.png)

*asmdef*generates a separate assembly. The internal keyword becomes meaningful.

In this case, I am using a different strategy to create abstracted code. I could have gone with an Entity Synchronisation strategy like previously seen with the UECS approach, but instead, I am using the strategy I adopt to code complex applications *with different layers of abstraction*. The rule is that the abstraction layer must not only provide the way to compose its systems (as you can see in **GameObjectToSveltoCompositionRoot**), but it must also provide the *components *that specialised entities must include to be processed by the abstracted layer engines. The abstraction layer must also provide a way to register objects, if necessary, through an object manager interface that I usually call *Resource Manager*. In this specific case, the registration of the objects is not in ECS pure form. **RegisterPrefab** is the only exposed functionality and it has the responsibility to convert a GameObject Prefab to an ID so that it can be used inside ECS components (which cannot hold references to objects). The **GameObjectManager** (our resource manager) holds all the references to the prefabs registered, creates new instances when requested and converts IDs back to gameobjects.

As you can see from the mini-example code, the engines outside the GO abstraction layer won’t ever access game objects directly and they look almost exactly like the DOTS ECS version of the same demo, while the **Synchronisation **engine, encapsulated inside the Gameobject abstraction layer, looks like:

class RenderingGameObjectSynchronizationEngine : IQueryingEntitiesEngine, IJobifiedEngine { public EntitiesDB entitiesDB { get; set; } public void Ready() { } public RenderingGameObjectSynchronizationEngine(GameObjectManager goManager) { this._goManager = goManager; } public JobHandle Execute(JobHandle inputDeps) { JobHandle combineDependencies = inputDeps; //Completely abstract engine. There is no assumption of in which groups the component can be. //I am planning to add the concept of disabled groups in future as the state enabled/disable is very //abstract and it makes sense to have the concept at framework level foreach (var ((positions, count), group) in entitiesDB.QueryEntities<PositionEntityComponent>()) { Check.Require(_goManager.Transforms((int) (uint) group).length == count , $"component array length doesn't match. Expected {count} - found {_goManager.Transforms((int) (uint) group).length} - group {group.ToName()}"); combineDependencies = JobHandle.CombineDependencies(inputDeps, new ParallelTransformJob() { _position = positions }.Schedule(_goManager.Transforms((int) (uint) group), inputDeps), combineDependencies); } return combineDependencies; } public string name => nameof(RenderingGameObjectSynchronizationEngine); readonly GameObjectManager _goManager; //Using jobification to access the transforms struct ParallelTransformJob : IJobParallelForTransform { public NB<PositionEntityComponent> _position; public void Execute(int index, TransformAccess transform) { transform.position = _position[index].position; } } }

I got to the concept of the OOP abstraction layer after I analysed the limits of using the Svelto **EntityViewComponent **approach to wrap and abstract objects. The OOP abstraction layer is a strategy that can be used with whatever ECS implementation, therefore more valuable to realise the true potential of the ECS-centric approach.

Another related demo I coded is found in [MiniExample 6: OOP Abstraction layer.](https://github.com/sebas77/Svelto.MiniExamples/tree/master/Example6-Unity%20Hybrid-OOP%20Abstraction)

This demo was made to show how the same problem can be approached with the Svelto.ECS EntityViewComponents and the OOP abstraction layer. It shows that the EntityViewComponent approach is more compact, but way less pure than the OOP abstraction layer. In this example, I am showing how to change the parent of a game object, which may be a bit more interesting than setting a position.

class MoveSpheresEngine : IStepEngine, IQueryingEntitiesEngine { public void Ready() { } public void Step() { var (buffer, count) = entitiesDB.QueryEntities<TransformViewComponent>(ExampleGroups.SphereGroup); //in this case transform is a wrapper of an Object, so the exposed position property is //going to write directly in the gameobject Transform position. //note that transform doesn't expose any method or field of the Unity Transform instance. for (var i = 0; i < count; i++) buffer[i].transform.position = Oscillation(buffer[i].transform.position, i); } public EntitiesDB entitiesDB { get; set; } public string name => nameof(MoveSpheresEngine); Vector3 Oscillation(Vector3 transformPosition, int i) { var transformPositionX = Mathf.Cos(Time.fixedTime * 3 / Mathf.PI); transformPosition.x = transformPositionX + i * 1.5f; return transformPosition; } }

In **MoveSpheresEngine **the object is accessed through the EntityViewComponent interface. This results in less code to write because the synchronisation engine is now not necessary anymore. The simplicity of the EntityViewComponent approach can lure the user to prefer it over the OOP abstraction layer approach. While the EntityViewComponent approach won’t allow using OOP features directly, using them in a complex scenario will result in slower and more boilerplate-y code than using the OOP abstraction layer.

Since usually entity data must be accessed multiple times, writing pure ECS engines and then synchronizing the component values once with the underlying objects, results in faster code as accessing objects directly (through the EntityViewCompnent) breaks the CPU cache.

**Update:** [The survival example has been updated to use a Resource Manager and the OOP abstraction layer pattern](https://www.sebaslab.com/the-new-svelto-ecs-survival-mini-example/). It provides the current most updated form of it.

### Conclusions

In a Multi-Paradigm scenario, an ECS-centric application can use objects. The user can decide, for example, to inject dependencies inside engines to be used outside the ECS scenario. The user must be aware though that abusing this flexibility could lead to wrong paths, so in order to avoid a dangerous situation where too much OOP code is used across the project systems, the OOP abstraction approach is desirable.

I, therefore, presented two ways in Svelto.ECS to abstract objects. **The OOP abstraction layer strategy** is important because it can be applied with any ECS framework regardless of its implementation details.

The Svelto.ECS exclusive **EntityViewComponent **model approach may be more convenient in specific cases, but in others could instead lead to performance degradation and boilerplate code.

I think it needs practice to really understand what this article tries to convey. When I first read it I didn’t learn much from it. It was not until I got hands dirty with a demo.that I realized I was missing something and got back to study it again.

I recommend anyone reading this article later on to build a demo as you learn, if you did not have much experience with ECS, or Svelto, in particular.

Too true. I was using the ViewComponent approach and soon my code became spaghetti, dried one.