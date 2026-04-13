---
title: Chunk's Change Version
url: https://gametorrahod.com/change-version/
author: Sirawat Pitaksarit
published: '2024-05-13'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

DOTS comes with a per-chunk versioning and a related filter feature. This feature can optimize processing the data only when it mattered.

This article highlights where they are in the API and their behaviour / quirks.

## Utilizing the change version

### Using a filter

The query way provides an easy to use filter system.

- On
`SystemAPI.Query`

idiomatic`foreach`

:`QueryEnumerable<T1>`

has`.WithChangeFilter`

you can use, with`<T>`

and`<T1, T2>`

. So you can't add more than 2 components to check changed status at the same time. - For
`SystemAPI.QueryBuilder()`

, you must`.Build`

it first, then there is`.AddChangedVersionFilter`

you can use. This call is additive, but inside the source code, there is still a hard-coded limit of 2 components to filter on change version. (i.e. Error if you`.AddChangedVersionFilter`

3 times.)

![](../../assets/3310fc5cce333229.png)

Both ways you can have max 2 components to check, so this is an important number to keep in mind when designing your logic. Also take note that the noun is either "change filter" or "changed version filter" (with the -d). But the thing that is stored per-chunk to make this feature work is called "change version" number (without the -d), explained in the incoming section.

The query has `.IsEmpty`

which account for the filter, unlike `.IsEmptyIgnoreFilter`

version. In Unity's code there are many early out optimization with `.IsEmptyIgnoreFilter`

in main thread code. You maybe able to do similar thing too.

### Manual checking on chunk iteration

However if you decided to get more involved with per-chunk iteration (`IJobChunk`

) there is no longer a convenient filter to help you. You can use `.DidChange`

available on `ArchetypeChunk`

that is given you per iteration. By more involved, you now have to go through the trouble of bringing in these into the job :

- The system's
`uint`

last version number : Obtained from`SystemState.LastSystemVersion`

. "Last" meant the last time (not this time) that the system updates, what**was**its version? - The
`ComponentTypeHandle<T>`

: Obtained from`SystemAPI.GetComponentTypeHandle(isReadOnly: true)`

. Note that they designed it like this so that there are hoops you must jump through in order for the system to be notified of type's read dependency on the job it is going to schedule / run.

```
public struct ChunkJobWithChangeFilter : IJobChunk
{
public ComponentTypeHandle<SampleDataComponent> SampleDataComponentHandle;
public uint LastSystemVersion;
public void Execute(in ArchetypeChunk chunk, int unfilteredChunkIndex, bool useEnabledMask,
in v128 chunkEnabledMask)
{
if (chunk.DidChange(ref SampleDataComponentHandle, LastSystemVersion))
{
// Do something
}
}
}
```


This chunk-based way you are no longer bound by 2 components limit, and also can `if`

`else`

as complex as you wish. (e.g. If A component chunk is marked as changed, do this. If B component chunk is marked as unchanged, do that instead.)

This chunk-based way also reveals the exact mechanics how it obtains the boolean "changed?", by comparing chunk's changed version number with system's.

## How the change version works

This I think is more complicated than using the filter, and official documentation is not making it very clear. There are 3 version numbers in play, to make it easier to differentiate I'm going to mark them with emoji just for this section.

There is a number called 🌍 global system version. This version increases by 1 for each consecutive system updated, including system groups. **After** each system updates, the system remember this number as its ↩️ last system version. Therefore **during **the update, its ↩️ last system version could determine when it was updated the previous frame.

Then, there is a **per-chunk** number called ✏️ change version. How the chunk is considered "changed" in order to update this number is rather crude : Instantly when a **query **is executed related to that component and it has **write permission**. Then, **chunks** returned for that query will all get their ✏️ change version updated.

It does not check whether system actually "change" the component's value with its work using the query. It just see the write dependency and thought the system "probably" changed that for all the matched chunks.

It is per chunk. There are other entities in the chunk that are not actually changed and still get iterated. Your logic must not be destructive to these entities. Try treating changed filter as **optimization** rather than branching logic, always imagine if the changed filter is removed, everything must still work like before but with worse performance.

To record that the chunk has changed, its ✏️ change verion is updated to the 🌍 global system version. Note that ↩️ last system version is still behind 🌍 global system version **during** the update. Only **after **the update that it is also catch up to 🌍 global system version, making it equal to the ✏️ change version it just recorded.

Finally we can get to how it works : If chunk's ✏️ change version is **higher** than ↩️ last system version then it had changed. ("Had changed since the last time this system updated.", to be exact.) Equal or lower meant it had not changed.

Supposed that System A writes to a component during its update, **during** the update, chunk's ✏️ change version would be ahead the system's ↩️ last system version for a brief moment (updates to 🌍 global system version). **After **the update, ↩️ last system version is then updated to be 🌍 global system version to catch up too. (They are equal now.) This means if there is no other system doing anything to this component, the next frame, equal number meant it has not changed and query will not return the chunks.

But supposed that there is a System B following immediately after A and it writes to this component too and recorded a higher ✏️ change version into the chunk, in the next frame System A would be able to detect the change made by System B the last frame.

## Tests

To reinforce the learning, here are some tests. Before the tests, I'm introducting 2 actors which is a simple component data (that we are going to change, and check its change version) and a big internal capacity dynamic buffer type designed to bully the archetype to have many chunks, so we could see clearly when change version works on one chunk and not the others.

```
public struct SampleDataComponent : IComponentData
{
public int Data;
}
[InternalBufferCapacity(256)]
public struct FatBuffer : IBufferElementData
{
public int BufferData;
}
```


![](../../assets/c1bde5ac9ded6316.png)

### Last system version starts out at 0, a special number

The first time the system updates, there is no "last" to look back to, therefore it is 0. Everything is considered "changed". This further emphasis that this feature should be an **optimization, **if the filter is somehow gone (work on everything) the result should be the same, just that the work might be a bit more redundant.

This code prints the `OnUpdate`

forever with increasing frame number and system version number, but print the `foreach`

exactly 90 times and never again. I name the entity on create so that on logging I could get its name.

```
public partial struct SystemA : ISystem
{
public void OnCreate(ref SystemState state)
{
var myArchetype = state.EntityManager.CreateArchetype(typeof(SampleDataComponent), typeof(FatBuffer));
for (var i = 0; i < 90; i++)
{
var createdEntity = state.EntityManager.CreateEntity(myArchetype);
state.EntityManager.SetName(createdEntity, $"Entity No. {i}");
}
}
public void OnUpdate(ref SystemState state)
{
Debug.Log($"System A : Update at frame {Time.frameCount}, last system version {state.LastSystemVersion}, current global {state.GlobalSystemVersion}");
foreach (
var (sampleData ,entity) in
SystemAPI.Query<RefRO<SampleDataComponent>>()
.WithChangeFilter<SampleDataComponent>()
.WithEntityAccess()
)
{
Debug.Log($"System A : {state.EntityManager.GetName(entity)} foreach at frame {Time.frameCount}");
}
}
}
```


![](../../assets/e8148ec8e3a7fd75.png)

### System always update unless...

As evidenced in the previous example, the system's `OnUpdate`

does not care about whether its query get 0 match or not. So in effect this change version feature can't affect the system's workings. This behaviour matches `MonoBehaviour`

one so it is easy to understand.

But you can go advanced and register the query (should be in your `OnCreate`

) with the following methods on `SystemState`

to make the update conditional :

```
RequireForUpdate(EntityQuery query) : void
RequireForUpdate<T>() : void
RequireAnyForUpdate(params EntityQuery[] queries) : void
RequireAnyForUpdate(NativeArray<EntityQuery> queries) : void
```


`RequireForUpdate<T>`

is handy for system that is going to process a singleton component.

There is also `[RequireMatchingQueriesForUpdate]`

attribute to paste on top of your system and you don't even have to register anything manually. The system knows its queries and this attribute will add them all to the requirement.

You would imagine pasting this attribute to the previous example will only prints 91 times and stop, but that's not the case (lol!) as both `RequireForUpdate`

and `[RequireMatchingQueriesForUpdate]`

ignores all the filters in the query. (3 kinds : Change version filters, shared component filters, order version filters.) Anyway, preventing the system's update is not our focus here. Let's focus on just whether the query with change version filter works or not.

### System version increases globally after each system

The previous example, if you look at frame 2 and beyond, you might be surprised at the system version numbers.

![](../../assets/0c8159118a9985a9.png)

As mentioned, global system version (and therefore also last system version) is also increasing when other systems updates. (There are many built-in ones that came with the package. There are 54 more systems along the way.

Now it is time to introduce a similar `SystemB`

with `[UpdateAfter(typeof(SystemA))]`

, it would ended up like this.

```
public partial struct SystemA : ISystem
{
public void OnCreate(ref SystemState state)
{
var myArchetype = state.EntityManager.CreateArchetype(typeof(SampleDataComponent), typeof(FatBuffer));
for (var i = 0; i < 90; i++)
{
var createdEntity = state.EntityManager.CreateEntity(myArchetype);
state.EntityManager.SetName(createdEntity, $"Entity No. {i}");
}
}
public void OnUpdate(ref SystemState state)
{
Debug.Log($"System A : Update at frame {Time.frameCount}, last system version {state.LastSystemVersion}, current global {state.GlobalSystemVersion}");
foreach (
var (sampleData ,entity) in
SystemAPI.Query<RefRO<SampleDataComponent>>()
.WithChangeFilter<SampleDataComponent>()
.WithEntityAccess()
)
{
Debug.Log($"System A : {state.EntityManager.GetName(entity)} foreach at frame {Time.frameCount}");
}
}
}
[UpdateAfter(typeof(SystemA))]
public partial struct SystemB : ISystem
{
public void OnUpdate(ref SystemState state)
{
Debug.Log($"System B : Update at frame {Time.frameCount}, last system version {state.LastSystemVersion}, current global {state.GlobalSystemVersion}");
foreach (
var (sampleData ,entity) in
SystemAPI.Query<RefRO<SampleDataComponent>>()
.WithChangeFilter<SampleDataComponent>()
.WithEntityAccess()
)
{
Debug.Log($"System B : {state.EntityManager.GetName(entity)} foreach at frame {Time.frameCount}");
}
}
}
```


![](../../assets/5c55bce0b3843550.png)

Well, turns out B is not updating immediately after A but rather there are 3 systems that updated between them. You can use the Systems debugger to see what came in-between. There they are.

![](../../assets/4283593d8a8c3114.png)

### RW access is enough to update the change version

If I first just remove `.WithChangeFilter()`

from `SystemA`

(retains the RO), I would get `SystemA`

that unconditionally `foreach`

on every frames 90 times per frame, and `SystemB`

which still has `.WithChangeFilter()`

won't update other than the first time, since RO doesn't flag the chunk to get a new change version.

And then I change RO in `SystemA`

to RW, now `.WithChangeFilter()`

on `SystemB`

(still RO) see the change every time since it always run after `SystemA`

, and ended up updating as well on every frames. We can clearly see that write dependency is what caused the change because the logic is just reading and logging.

The query needs to occur for RW to update all the matched chunk's change version. If I put an unlikely `if`

before the `foreach`

, then `SystemB`

will not be notified of the change even though `SystemA`

has RW permission of that component and its `OnUpdate`

occurs.

### Change version update is per chunk

Remember that I intentionally make the archetype big enough that there could be just 15 entities per chunk. To test this out, I'll just add a [tag component](https://docs.unity3d.com/Packages/com.unity.entities@1.2/manual/components-tag.html) `TagForChunk`

to the last 16 entities when I create 90 entities in `SystemA`

's `OnCreate`

. The result should be that we have 2 chunks of this new archetype that includes the tag. One chunk with 15 entities, another with 1 entity.

Then modify the "work" in `SystemA`

to have `RefRO<TagForChunk>`

. The work stays the same (logging and not actually writing), so this work should update change version of those 2 chunks (because there is still `RefRW`

on the `SampleDataComponent`

) .

And important that in `SystemB`

, everything stays the same including **not **caring about `TagForChunk`

at all.

```
public struct TagForChunk : IComponentData
{
}
public partial struct SystemA : ISystem
{
public void OnCreate(ref SystemState state)
{
var myArchetype = state.EntityManager.CreateArchetype(typeof(SampleDataComponent), typeof(FatBuffer));
var archetypeWithTag =
state.EntityManager.CreateArchetype(typeof(SampleDataComponent), typeof(FatBuffer), typeof(TagForChunk));
for (var i = 0; i < 90; i++)
{
Entity createdEntity = state.EntityManager.CreateEntity(i >= 74 ? archetypeWithTag : myArchetype);
state.EntityManager.SetName(createdEntity, $"Entity No. {i}");
}
}
public void OnUpdate(ref SystemState state)
{
Debug.Log(
$"System A : Update at frame {Time.frameCount}, last system version {state.LastSystemVersion}, current global {state.GlobalSystemVersion}");
foreach (
var (sampleData, tag, entity) in
SystemAPI.Query<RefRW<SampleDataComponent>, RefRO<TagForChunk>>()
.WithEntityAccess()
)
{
Debug.Log($"System A : {state.EntityManager.GetName(entity)} foreach at frame {Time.frameCount}");
}
}
}
[UpdateAfter(typeof(SystemA))]
public partial struct SystemB : ISystem
{
public void OnUpdate(ref SystemState state)
{
Debug.Log(
$"System B : Update at frame {Time.frameCount}, last system version {state.LastSystemVersion}, current global {state.GlobalSystemVersion}");
foreach (
var (sampleData, entity) in
SystemAPI.Query<RefRO<SampleDataComponent>>()
.WithChangeFilter<SampleDataComponent>()
.WithEntityAccess()
)
{
Debug.Log($"System B : {state.EntityManager.GetName(entity)} foreach at frame {Time.frameCount}");
}
}
}
```


The result is it is **as if** `SystemB`

has `RefRO<TagForChunk>`

too, but it was all the work of `.WithChangeFilter<SampleDataComponent>`

that results from `SystemA`

working according to the tag. The update starts from Entity No. 74 to Entity No. 90. (15 + 1 entities across 2 chunks.)

![](../../assets/2fbb5d825254d135.png)

### Enableable components does not work on chunk level

Enableable component is a feature that works **per entity. **The source generator will query all chunks, updates the version of RW component of all chunks, then decide for each entity whether it get to work or not.

So if I change the tagging in the previous example to instead disable `SampleDataComponent`

for last 16 entities, because we have 6 chunks, theoretically the final chunk could be skipped entirely. But since it doesn't work that way, all chunks ended up being changed.

### Bonus reminder about IJobChunk

When a system run / schedule `IJobChunk`

, the RW or RO permission is decided on whether input `ComponentTypeHandle<T>`

coming into the job (required to get `NativeArray<T>`

from `ArchetypeChunk`

on each per-chunk iteration) was created in the system with `SystemAPI.GetComponentTypeHandle<T>(isReadOnly: true OR false)`

.

(There is also `[ReadOnly]`

attribute you could paste on the input to the job, but I don't think it let the system know.)

## Advanced : Per-Entity Change Checking

This coding pattern is taken from Unity's official `Unity.Transform`

package, so I think we can trust it as a good pattern?

You want to do heavy work on component value's change. A per-chunk `DidChange`

will work, but other entities not really changed (or worst, the chunk got RW but nothing changed) will also get the work just because an entity in the same chunk changed, only to get the computed result to be the same as they are right now, so it is a useless work.

**Solution : **By creating a new "previous" component with the same fields to pair with that you want to check for a "real change". (Remembering that some components have a "previous pair" is also a pain, so you might also have to go through trouble of writing a system to automatically add this "previous" component whenever it found a real one.) You can then put a value comparision check just behind the `DidChange`

's initial rough filter so you can check per-entity if it really changed. Then you update previous to be the present one as well if it ended up changed.

```
if (chunk.DidChange(ref ParentTypeHandle, LastSystemVersion) ||
chunk.DidChange(ref PreviousParentTypeHandle, LastSystemVersion))
{
var chunkPreviousParents = chunk.GetNativeArray(ref PreviousParentTypeHandle);
var chunkParents = chunk.GetNativeArray(ref ParentTypeHandle);
var chunkEntities = chunk.GetNativeArray(EntityTypeHandle);
for (int j = 0, chunkEntityCount = chunk.Count; j < chunkEntityCount; j++)
{
if (chunkParents[j].Value != chunkPreviousParents[j].Value)
{
// Work...
}
}
}
```


Now for details if you are still interested... otherwise you can end this article here.

In the ECS transforms system, you build a transform hierarchy **bottom-up** by attaching `Parent`

to an entity and let it say who the parent is. This make it easy to move an entity (along with an entire tree of its children right now) under some other entity by setting just a single entity's `Parent`

component to point to a new one. No need to change any of its children.

But programmer often wants to iterate through children, and knowing just `Parent`

is not so useful. So there is a system that would keep looking at all `Parent`

in the world and figure out the hierarchy tree and maintain the buffer component `Child`

for each entity. As you can imagine, this work is looking to be intensive and must be performant.

The system that do so cannot just work on any new `Parent`

it found and say "Yes, I have already worked on this one" (and perhaps slap a tag component on it), it must additionally :

- Always actively look for field change inside any
`Parent`

component. - If the component
`Parent`

is removed**or**the entity with`Parent`

is destroyed, then the affected parent will need their buffer updated.

So how they did it that solve both points at the same time, is to have a "previous" component named `PreviousParent`

with the same field as `Parent`

as a pair. The fact that it is an exact pair solves point 1. This component must be `ICleanupComponentData`

in order to solve point 2.

This component should be automatically added when system detects a new `Parent`

(`WithAll<Parent>().WithNone<PreviousParent>()`

) coming into the world. At this point the previous parent starts by copying the value of the present one. Now you have got a per-entity change checking pattern working! When `.DidChange`

detected a chunk-level change (or just some careless RW), we have a 2nd level check, by perform a linear iteration through native array of `Parent`

and `PreviousParent`

and really see for real if the value differs entity by entity.

Though unrelated with change version topic of this blog post, `ICleanupComponentData`

gives the ability to react to both kinds of removal (remove just the component, or the entity got outright destroyed) with this kind of query : `.WithAllRW<PreviousParent>().WithNone<Parent>()`

. When it detects such moment, `PreviousParent`

serves an another purpose than "true change checking" that is to notify the parent of its deceased child (how sad!) so it could update its children.