---
title: Enableable Components Generated Code
url: https://gametorrahod.com/enableable-generated-code/
author: Sirawat Pitaksarit
published: '2024-05-03'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

The [Enableable Component](https://docs.unity3d.com/Packages/com.unity.entities@1.2/manual/components-enableable.html) feature is described very succinctly as saving you small trouble of performing the common trick of sticking a `bool`

in a component you want to disable without causing structural change. Also don't forget that you need to write the `if`

checking that `bool`

on your job code to make use of it.

On surface this feature sounds like a nice little thing they added for us, but underneath it has a lot going on.

How many `1234`

do you think you would see in the Burst compiled assembly code of this simple standalone job?

```
public struct JustCounterComponent : IComponentData
{
public int Valuez;
}
[BurstCompile]
internal partial struct AddCounterJob : IJobEntity
{
public void Execute(ref JustCounterComponent xyz)
{
xyz.Valuez += 1234;
}
}
```


Turns out there are 8 search hits! (6 grouped together on top, 2 more on bottom) So we could guess it spawns several different paths to call `Execute`

. Now I'm curious, so let's find them.

## Analyzing the generated code

Roslyn Source Generator is here to stay in DOTS. The assembly code of that job is generated from C# generated code **combined **with your code thanks to `partial`

, so it make sense if we take a look at what Roslyn generated first... just the Execute part. (There are more code generated for the `AddCounterJob`

, such as letting you `.ScheduleParallel()`

to it.)

```
InternalCompilerQueryAndHandleData.TypeHandle __TypeHandle;
[global::System.Runtime.CompilerServices.CompilerGenerated]
public void Execute(in global::Unity.Entities.ArchetypeChunk chunk, int chunkIndexInQuery, bool useEnabledMask, in global::Unity.Burst.Intrinsics.v128 chunkEnabledMask)
{
var xyzArrayIntPtr = Unity.Entities.Internal.InternalCompilerInterface.UnsafeGetChunkNativeArrayIntPtr<global::JustCounterComponent>(chunk, ref __TypeHandle.__JustCounterComponent_RW_ComponentTypeHandle);
int chunkEntityCount = chunk.Count;
int matchingEntityCount = 0;
if (!useEnabledMask)
{
for(int entityIndexInChunk = 0; entityIndexInChunk < chunkEntityCount; ++entityIndexInChunk)
{
ref var xyzArrayIntPtrRef = ref Unity.Entities.Internal.InternalCompilerInterface.UnsafeGetRefToNativeArrayPtrElement<global::JustCounterComponent>(xyzArrayIntPtr, entityIndexInChunk);
Execute(ref xyzArrayIntPtrRef);
matchingEntityCount++;
}
}
else
{
int edgeCount = global::Unity.Mathematics.math.countbits(chunkEnabledMask.ULong0 ^ (chunkEnabledMask.ULong0 << 1)) + global::Unity.Mathematics.math.countbits(chunkEnabledMask.ULong1 ^ (chunkEnabledMask.ULong1 << 1)) - 1;
bool useRanges = edgeCount <= 4;
if (useRanges)
{
int entityIndexInChunk = 0;
int chunkEndIndex = 0;
while (global::Unity.Entities.Internal.InternalCompilerInterface.UnsafeTryGetNextEnabledBitRange(chunkEnabledMask, chunkEndIndex, out entityIndexInChunk, out chunkEndIndex))
{
while (entityIndexInChunk < chunkEndIndex)
{
ref var xyzArrayIntPtrRef = ref Unity.Entities.Internal.InternalCompilerInterface.UnsafeGetRefToNativeArrayPtrElement<global::JustCounterComponent>(xyzArrayIntPtr, entityIndexInChunk);
Execute(ref xyzArrayIntPtrRef);
entityIndexInChunk++;
matchingEntityCount++;
}
}
}
else
{
ulong mask64 = chunkEnabledMask.ULong0;
int count = global::Unity.Mathematics.math.min(64, chunkEntityCount);
for (int entityIndexInChunk = 0; entityIndexInChunk < count; ++entityIndexInChunk)
{
if ((mask64 & 1) != 0)
{
ref var xyzArrayIntPtrRef = ref Unity.Entities.Internal.InternalCompilerInterface.UnsafeGetRefToNativeArrayPtrElement<global::JustCounterComponent>(xyzArrayIntPtr, entityIndexInChunk);
Execute(ref xyzArrayIntPtrRef);
matchingEntityCount++;
}
mask64 >>= 1;
}
mask64 = chunkEnabledMask.ULong1;
for (int entityIndexInChunk = 64; entityIndexInChunk < chunkEntityCount; ++entityIndexInChunk)
{
if ((mask64 & 1) != 0)
{
ref var xyzArrayIntPtrRef = ref Unity.Entities.Internal.InternalCompilerInterface.UnsafeGetRefToNativeArrayPtrElement<global::JustCounterComponent>(xyzArrayIntPtr, entityIndexInChunk);
Execute(ref xyzArrayIntPtrRef);
matchingEntityCount++;
}
mask64 >>= 1;
}
}
}
}
```


Quite a lot of the "first-class support" of enableable components are in the generated code rather than in Entities library! The enable bit mask came from library, but how it decides to call `Execute`

for each entity or not is right here.

It make a lot of sense though, because the enable is attached to one component, the decision to perform `Execute`

or not will dynamically change depending on what components you are asking on the query. You could say this feature is only possible after Unity managed to get Roslyn Source Generator working.

I have intentionally make the incoming parameter named `xyz`

so you could see clearer that it is being referenced in the generated code here.

The gist of this code is that no matter you actually use enableable components or not, the generated code doesn't care and use one central `Execute`

signature that accepts `useEnabledMask`

and `chunkEnabledMask`

(128-bit mask where `1`

represent enabled entity). Therefore that first `if`

to check programmatically whether you use the feature or not is mandatory.

## If enableable feature is not used

```
if (!useEnabledMask)
{
for(int entityIndexInChunk = 0; entityIndexInChunk < chunkEntityCount; ++entityIndexInChunk)
{
ref var xyzArrayIntPtrRef = ref Unity.Entities.Internal.InternalCompilerInterface.UnsafeGetRefToNativeArrayPtrElement<global::JustCounterComponent>(xyzArrayIntPtr, entityIndexInChunk);
Execute(ref xyzArrayIntPtrRef);
matchingEntityCount++;
}
}
```


You can imagine `useEnabledMask`

would be `false`

in this case when Unity schedules this job, and use only the thin part of that `if`

, because the component is just `IComponentData`

without the `IEnableableComponent`

.

It is a simple for loop per entity. Each entity, it calls the real `Execute`

with just 1 parameter that you wrote thanks to `partial`

connecting this generated code with your code. This is where assembly code would reach the number `1234`

. I don't know why they keep track of `matchingEntityCount`

. Maybe there is a magic assertion somewhere or it causes some good things in the assembly?

## If enableable feature is used

That `bool useRanges = edgeCount <= 4;`

is interesting, and if you are like me the code smells like it is challenging me to get `useRanges`

to be `true`

so I get to enter a nicer looking routine with nested `while`

loops.

The `edgeCount`

works on 64 bit + 64 bit of the 128 bit half. Each half, it XOR with itself that is shifted left by one bit, counting how many `1`

in the XOR result. Effectively it is checking how often consecutive bits transitioned (the "edge") between 0 and 1. If bit pattern is `111111110111110000`

, the shift-and-XOR-self result will have three `1`

at each transition point. `edgeCount`

is 4 because it transitioned 4 times. As for "range", this pattern has 2 ranges. You look at each consecutive `1`

s as a range.

Only if it detects that it transitioned no more than 4 times per chunk (effectively max 3 ranges per chunk in most cases), you get to the "use ranges" mode.

### With while loop : "Use ranges" mode

```
int entityIndexInChunk = 0;
int chunkEndIndex = 0;
while (global::Unity.Entities.Internal.InternalCompilerInterface.UnsafeTryGetNextEnabledBitRange(chunkEnabledMask, chunkEndIndex, out entityIndexInChunk, out chunkEndIndex))
{
while (entityIndexInChunk < chunkEndIndex)
{
ref var xyzArrayIntPtrRef = ref Unity.Entities.Internal.InternalCompilerInterface.UnsafeGetRefToNativeArrayPtrElement<global::JustCounterComponent>(xyzArrayIntPtr, entityIndexInChunk);
Execute(ref xyzArrayIntPtrRef);
entityIndexInChunk++;
matchingEntityCount++;
}
}
```


Basically this mode hopes that the inner `while`

can work on consecutive entities that are all enabled. When it finally hits a disabled entity, it goes to outer `while`

and `UnsafeTryGetNextEnabledBitRange`

(a very burstable function) jumps over all the disabled entities to start the inner `while`

again at the next clump of enabled entities. Each clump of enabled entities is probably what they called a "range".

I can imagine now that this is the likely mode to get used if I disable just 1 or 2 entities in an entire chunk. For example if `1`

in the mask meant enabled, then if I disabled just a few entities it would look like this `1111111011110111111111`

, and therefore this code would have 3 "ranges" to work on. Note that the outer `while`

is capable of jumping over many `0`

, so even if I disabled a lot of entities, if they are consecutive, this mode would still get used. (e.g. `1111000000000011110111111`

this is still 3 ranges.)

Remember that the point of doing data-oriented is that the data is lining up linearly per component and the cache is nice. A big long "range" of enabled components preserves this goodness.

### With for loop + if

If `edgeCount`

prediction says ditch the range mode and just check each entity individually, it checks each bit one by one whether it is a `1`

or not (enabled) and `Execute`

if it is.

It needs to work two halfs : 64 bits + 64 bits, and of course stop early if chunk contains less than 64 entities, or more than 64 but less than 128 entities.

```
ulong mask64 = chunkEnabledMask.ULong0;
int count = global::Unity.Mathematics.math.min(64, chunkEntityCount);
for (int entityIndexInChunk = 0; entityIndexInChunk < count; ++entityIndexInChunk)
{
if ((mask64 & 1) != 0)
{
ref var xyzArrayIntPtrRef = ref Unity.Entities.Internal.InternalCompilerInterface.UnsafeGetRefToNativeArrayPtrElement<global::JustCounterComponent>(xyzArrayIntPtr, entityIndexInChunk);
Execute(ref xyzArrayIntPtrRef);
matchingEntityCount++;
}
mask64 >>= 1;
}
mask64 = chunkEnabledMask.ULong1;
for (int entityIndexInChunk = 64; entityIndexInChunk < chunkEntityCount; ++entityIndexInChunk)
{
if ((mask64 & 1) != 0)
{
ref var xyzArrayIntPtrRef = ref Unity.Entities.Internal.InternalCompilerInterface.UnsafeGetRefToNativeArrayPtrElement<global::JustCounterComponent>(xyzArrayIntPtr, entityIndexInChunk);
Execute(ref xyzArrayIntPtrRef);
matchingEntityCount++;
}
mask64 >>= 1;
}
```


## Because this feature is per-entity...

The source generator of job is able to service you the `if`

`else`

should this entity be executed perfectly, because job also works entity by entity. Codegen could put code in the other side of `partial`

before arriving at your code in `Execute`

.

In `IJobChunk`

though it naturally require your manual effort. It starts at archetype chunk level and it already landed in your code, where source generator can no longer perform any more hacks for you. Instead, the API design just give you a DIY kit of the mask, and helper method for you to apply on your own. See details in [the official documentation](https://docs.unity3d.com/Packages/com.unity.entities@1.2/manual/iterating-data-ijobchunk-implement.html#the-useenabledmask-and-chunkenabledmask-parameters).

## About write access

The equivalent hack of having one `bool`

field in a component and then `if`

on that `bool`

to check if it is enabled, the trick before we have enableable component, to enable / disable the component you would need a write access on that component to edit the `bool`

. Therefore any job that need to only read this component will need to wait for the one that could write.

It is the same with official enableable component. If you want to flip the enable/disable status in-job you need a write permission on that component, and it'll affect scheduling as expected.

But since the `bool`

that existed in the hack is now hidden and built-in as a 128-bit mask instead (and they provided efficient code that would flip one bit in this long mask as good as you flipping one `bool`

yourself), you can no longer just add that component as a part of query and just `enabledFlag = false/true`

.

If main thread, you can use `EntityManager`

, or use `EnabledRefRO<T>`

and `EnabledRefRW<T>`

as a part of [idiomatic foreach (SystemAPI.Query)](https://docs.unity3d.com/Packages/com.unity.entities@1.2/manual/systems-systemapi-query.html).


The dedicated method to do that **from job** is available in `ComponentLookup<T>`

. And passing the lookup into the job will properly add write dependency. Here are relevant ones.

```
IsComponentEnabled(Entity entity) : bool
IsComponentEnabled(SystemHandle systemHandle) : bool
SetComponentEnabled(SystemHandle systemHandle, bool value) : void
SetComponentEnabled(Entity entity, bool value) : void
GetEnabledRefRW<T2>(Entity entity) : EnabledRefRW<T2>
GetComponentEnabledRefRWOptional<T2>(Entity entity) : EnabledRefRW<T2>
GetEnabledRefRO<T2>(Entity entity) : EnabledRefRO<T2>
GetComponentEnabledRefROOptional<T2>(Entity entity) : EnabledRefRO<T2>
```


`EntityCommandBuffer`

and its parallel version can also work on enabling / disabling the component from job, but scheduled for later.

```
// Standard
SetComponentEnabled<T>(Entity e, bool value) : void
SetComponentEnabled(Entity e, ComponentType componentType, bool value) : void
// ParallelWriter
SetComponentEnabled<T>(int sortKey, Entity e, bool value) : void
SetComponentEnabled(int sortKey, Entity e, ComponentType componentType, bool value) : void
```


Lastly if your job is iterating by `ArchetypeChunk`

, there are extensive functions to work with enabled status. Normal ones that takes in entity index in chunk to flip one bit. Advanced ones that enable/disable the entire chunk (ones with `ForAll`

suffix), or even get just the bits and mask which I can't even think of real use case of.

```
IsComponentEnabled<T>(ref ComponentTypeHandle<T> typeHandle, int entityIndexInChunk) : bool
IsComponentEnabled<T>(ref BufferTypeHandle<T> bufferTypeHandle, int entityIndexInChunk) : bool
IsComponentEnabled(ref DynamicComponentTypeHandle typeHandle, int entityIndexInChunk) : bool
SetComponentEnabled<T>(ref ComponentTypeHandle<T> typeHandle, int entityIndexInChunk, bool value) : void
SetComponentEnabled<T>(ref BufferTypeHandle<T> bufferTypeHandle, int entityIndexInChunk, bool value) : void
SetComponentEnabled(ref DynamicComponentTypeHandle typeHandle, int entityIndexInChunk, bool value) : void
SetComponentEnabledForAll<T>(ref ComponentTypeHandle<T> typeHandle, bool value) : void
SetComponentEnabledForAll<T>(ref BufferTypeHandle<T> bufferTypeHandle, bool value) : void
SetComponentEnabledForAll(ref DynamicComponentTypeHandle typeHandle, bool value) : void
GetEnableableBits(ref DynamicComponentTypeHandle handle) : v128
GetEnabledMask<T>(ref ComponentTypeHandle<T> typeHandle) : EnabledMask
```


## A limit of 128 entities per chunk

That mask having "chunk" in the name being 128 bits meant that we could only flag up to 128 entities as enabled or disabled per chunk.

The internal `ChunkIterationUtility.cs`

has `GetEnabledMask`

that creates this mask for one component of a chunk we could take a look. (And wow, a lot of care for creating just this 128 bit mask fast!) And sure enough there are hard-coded `128`

around here. If you follow the code, you would eventually reach `TypeManager.cs`

explicitly defining `public const int `

so I think that's it. Chunk right now has 2 hard limits : 16 KiB size and max 128 entities.**MaximumChunkCapacity **= 128;

You can see this fact in the Archetypes debugger. An archetype of just 16 B each should be able to fit 1000 entities per chunk before the advent of enableable and the mask feature. Now it is capped to 128 entities. You could also say an archetype has "optimal size" of ~125 B where you get your full worth of 128 entities limit.

![](../../assets/cdfee5a9c2d974dc.png)

Is this worrying? (You might fear that for every 128 entities of single component data iteration, cache would need to jump to the next chunk's native array, instead of once every ~1000 entities) I think no. I have code some simple application with DOTS and with many kind of components added up together, it could approach that 125 B number fast. I think they have sufficiently looked at actual DOTS application for average archetype size before deciding on this 128 bit mask thing.

## But you should not optimize for enableable

We now know if you disable just a few entities here and there (to be precise, disabled 4 or less entities in each chunk) OR you can disable a lot of consecutive entities in a chunk, it would fall into a good pattern with consecutive data while iterating.

But having to keep in mind which chunk you are working on and whether you have hit the 4 quota or not (more than 4 if you use more than 1 chunk for that archetype, now you don't even know what is the quota!), or whether this entity is next to that entity or not, I think is not worth thinking about. Technical details of deleting an entity in the middle of chunk will also just pick the last one to fill the hole, if that entity is currently disabled, you will create an "edge" in the mask as well.

Unity refined Entities API to let you focus on what mattered already, better not to bring those back. Just enable / disable stuff at will and be happy that it is likely very fast and all burstable. And remember that the point of enableable components are that the enable / disable patterns could be chaotic and frequent, otherwise you would rather slap on a tag component to kick it to a different archetype with a structural change.

(In the end, the benefit of this article is just so I'm no longer curious so thats good!)