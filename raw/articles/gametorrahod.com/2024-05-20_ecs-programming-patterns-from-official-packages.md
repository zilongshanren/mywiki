---
title: ECS Programming Patterns from Official Packages
url: https://gametorrahod.com/ecs-patterns/
author: Sirawat Pitaksarit
published: '2024-05-20'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

Unity DOTS is still young so it is rather unclear what other people are doing when trying to accomplish a task. Video tutorials and sample projects are out there but can be hard to gather and verify whether they are the best practice or not.

There is one place we can learn from that has high confidence of being a good pattern, it's any Unity's own packages that references `Unity.Entities`

. This is such as the graphics, the transform, the physics, etc. that the code is surely up to date (because otherwise they wouldn't compile with their own `Unity.Entities`

).

**Note : I'll have to keep coming back to update this article as I run into new patterns, since it is impossible to read all codes in all packages just to write this article.**

## Cleanup component to detect other component's removal

It is stated in the documentation that "This is useful to tag entities that require cleanup when destroyed.". It can be also interpreted in this way : You want to trigger a code when a specific component is gone from both reasons : component remove + entity is destroyed. You create a cleanup component to pair with it.

Use query`WithNone<RealComponent>.WithAll<TheCleanupComponent>`

detects both ways. Without the cleanup component, just `WithNone<RealComponent>`

would only cover a component's removal and not destroying the entity.

In this usage, you may want to know the content of the component that was just gone. But since it is gone you can't access it now! This is when `ICleanupComponent`

should start having some data from the real component you want to know the last status when it is gone. You will also need to keep the `ICleanupComponent`

up to date with the real one.

In `Unity.Transforms`

package, `Parent`

`IComponentData`

has a pair `PreviousParent`

`ICleanupComponentData`

. There is a work to do on the entity that was the parent of someone, whenever the `Parent`

is removed or when entity with `Parent`

is destroyed.

## Per-entity change checking

Check out this article on the bottom :

[Chunk’s Change VersionDOTS comes with a per-chunk versioning and a related filter feature. This feature can optimize processing the data only when it mattered.](https://gametorrahod.com/change-version/#advanced-per-entity-change-checking)![](../../assets/28756f9d6408c957.img)


## Tuple array

```
void AddChildrenToParent(Entity parent, DynamicBuffer<Child> children)
{
if (ParentChildrenToAdd.TryGetFirstValue(parent, out var child, out var it))
{
do
{
children.Add(new Child() { Value = child });
}
while (ParentChildrenToAdd.TryGetNextValue(out child, ref it));
}
}
```


The `NativeParallelMultiHashMap`

from `Unity.Collections`

is "multi" in that duplicate keys are fine. And therefore it could be used as tuple array.

Use `if`

+ `TryGetFirstValue`

+ `do`

+ (`while`

+ `TryGetNextValue`

) to iterate.

## Helper to add a set of related components

Unlike `MonoBehaviour`

, often one `IComponentData`

won't do anything on its own. Programmer design components much more modularly due to the query feature and linear memory concern, systems often ask for a big set of `IComponentData`

to start working.

How `Unity.Transforms`

and Entities Graphics turns out, user would need to read documentation to learn what components are the entry point to get the systems running, and what components are automatically added after. Such entry point components could use some helping hand from the system programmer.

An example of how to do this comes from `RenderMeshUtility.AddComponents`

in Entities Graphcis package. Send in `Entity`

and `EntityManager`

, and as you expected the inside are a bunch of add components.

```
public static void AddComponents(
Entity entity,
EntityManager entityManager,
in RenderMeshDescription renderMeshDescription,
RenderMeshArray renderMeshArray,
MaterialMeshInfo materialMeshInfo = default)
{
// ...
}
```


Inside contains a dynamic `ComponentTypeSet`

generator that has more or less types depending on flags coming in. The `ComponentTypeSet`

is compatible to overload `AddComponent(Entity entity, in ComponentTypeSet componentTypeSet)`

. It is created with `FixedList128Bytes<ComponentType>`

and doesn't need manual disposing.

```
var components = new FixedList128Bytes<ComponentType>
{
// Absolute minimum set of components required by Entities Graphics
// to be considered for rendering. Entities without these components will
// not match queries and will never be rendered.
ComponentType.ReadWrite<WorldRenderBounds>(),
ComponentType.ReadWrite<RenderFilterSettings>(),
ComponentType.ReadWrite<MaterialMeshInfo>(),
ComponentType.ChunkComponent<ChunkWorldRenderBounds>(),
ComponentType.ChunkComponent<EntitiesGraphicsChunkInfo>(),
// Extra transform related components required to render correctly
// using many default SRP shaders. Custom shaders could potentially
// work without it.
ComponentType.ReadWrite<WorldToLocal_Tag>(),
// Components required by Entities Graphics package visibility culling.
ComponentType.ReadWrite<RenderBounds>(),
ComponentType.ReadWrite<PerInstanceCullingTag>(),
};
```


## A system to ensure related components exist

Related to the previous entry, you might instead document that user need to add one component (so you don't need a helper to add multiple components at once) and others will automatically appear. The Entities Graphics package do so by making a system which has only one work of doing the add component by `WithAll<ThatOneComponent>.WithNone<ToAdd>`

queries.

```
protected override void OnUpdate()
{
EntityManager.AddComponent(m_MissingRootLODRange, typeof(RootLODRange));
EntityManager.AddComponent(m_MissingRootLODWorldReferencePoint, typeof(RootLODWorldReferencePoint));
EntityManager.AddComponent(m_MissingLODRange, typeof(LODRange));
EntityManager.AddComponent(m_MissingLODWorldReferencePoint, typeof(LODWorldReferencePoint));
EntityManager.AddComponent(m_MissingLODGroupWorldReferencePoint, typeof(LODGroupWorldReferencePoint));
}
```


With this design, those supporting components will be resistant to forced removal since they will immediately come back, and immediately got their value recomputed by an another system that keeps updating their value.

## Reusable groups of archetypes

```
internal struct ResolveSceneSectionArchetypes
{
public EntityArchetype SectionEntityRequestLoad;
public EntityArchetype SectionEntityNoLoad;
}
internal static ResolveSceneSectionArchetypes CreateResolveSceneSectionArchetypes(EntityManager manager)
{
return new ResolveSceneSectionArchetypes
{
SectionEntityRequestLoad = manager.CreateArchetype(
typeof(RequestSceneLoaded),
typeof(SceneSectionData),
typeof(SceneBoundingVolume),
typeof(SceneEntityReference),
typeof(ResolvedSectionPath)),
SectionEntityNoLoad = manager.CreateArchetype(
typeof(SceneSectionData),
typeof(SceneBoundingVolume),
typeof(SceneEntityReference),
typeof(ResolvedSectionPath))
};
}
```


Taken from `Unity.Scenes`

, it needs to use this set of archetypes in multiple places. Since you need `EntityManager`

to create an archetype at each place it wants to use, you can create a `static`

helper to create the archetype with `EntityManager`

as input.

## Disable tag component

```
m_PendingStreamRequests = new EntityQueryBuilder(Allocator.Temp)
.WithAllRW<RequestSceneLoaded, SceneSectionData>()
.WithAllRW<ResolvedSectionPath>()
.WithNone<StreamingState, DisableSceneResolveAndLoad>()
.Build(this);
m_UnloadStreamRequests = new EntityQueryBuilder(Allocator.Temp)
.WithAllRW<StreamingState>()
.WithAll<SceneSectionData,SceneEntityReference>()
.WithNone<RequestSceneLoaded, DisableSceneResolveAndLoad>()
.Build(this);
m_NestedScenesPending = new EntityQueryBuilder(Allocator.Temp)
.WithAllRW<RequestSceneLoaded, SceneTag>()
.WithNone<StreamingState, DisableSceneResolveAndLoad>()
.Build(this);
```


This is a simple pattern of creating a tag component to avoid getting worked on by a system (but keep all other components, so as soon as you remove this component it resumes work), by putting it in all `WithNone`

of every queries. They can be next to actual `WithNone`

components that the queries are actually interested in.

This strategy is good when queries are clearly grouped together neatly in `OnCreate`

and component name perhaps starts with `Disable`

so it self-document.

It is from `Unity.Scenes`

where (I think) when editor-only code load a scene it would need a special component to prevent it getting worked on like at runtime.

## Request component for reversible operation

In `Unity.Scenes`

, they use a pattern of attaching a component `RequestSceneLoaded`

to a scene entity and their section entities will be loaded. Also when you remove this component, their section entities are unloaded.

You order something to occur with a tag component attaching, and order it to be reversed when the component is removed. Component being able to be added only once helps with work doesn't make sense to occur twice, but make sense to be able to occur again after it is reversed.

This design is different from "request entity" where you create an entity with a component to order a system to do work, then that system try to flag the work as done either by tagging it, using enableable component, or destroying the entity. This design allows the work to occur repeatedly.

`using`

on Allocator

```
private void RemoveSceneEntities(EntityQuery query)
{
if (!query.IsEmptyIgnoreFilter)
{
using (var removeEntities = query.ToEntityArray(Allocator.TempJob))
using (var removeGuids =
query.ToComponentDataArray<AssetDependencyTrackerState>(Allocator.TempJob))
{
for (int i = 0; i != removeEntities.Length; i++)
{
LogResolving("Removing", removeGuids[i].SceneAndBuildConfigGUID);
_AssetDependencyTracker.Remove(removeGuids[i].SceneAndBuildConfigGUID, removeEntities[i]);
}
}
EntityManager.RemoveComponent<AssetDependencyTrackerState>(query);
}
}
```


If you are going to use an allocator that requires manual `.Dispose`

, then `using`

block is an option to organize your code.