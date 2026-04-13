---
title: Thinking in Cache
url: https://gametorrahod.com/thinking-in-cache/
author: Sirawat Pitaksarit
published: '2024-05-14'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

This article might help you picture the cache while you code DOTS. While you could get by without constantly being aware of cache, it is much more enjoyable to code data-oriented when you know what's going on.

Some component definitions :

```
public struct ComponentA : IComponentData
{
public int Data;
}
public struct ComponentB : IComponentData
{
public int Data;
}
public struct ComponentC : IComponentData
{
public int Data;
}
```


If iterating per entity where you have component variable of one entity coming in each time, you can write it either in `SystemAPI.Query`

and `IJobEntity`

like so :

```
foreach (
var (a, b, c) in
SystemAPI.Query<RefRO<ComponentA>, RefRW<ComponentB>, RefRO<ComponentC>>()
)
{
b.ValueRW.Data += a.ValueRO.Data + c.ValueRO.Data;
}
```


```
public partial struct MyJob : IJobEntity
{
public void Execute(in ComponentA a, ref ComponentB b, in ComponentC c)
{
b.Data += a.Data + c.Data;
}
}
```


## Always backed by a linear array

It is important to understand that the `a`

, `b`

, and `c`

in both styles **points to** somewhere in a linear native array of just that component. The array of next component comes only after the final element of first component. This is roughly how the chunk looks like.

```
// The first Execute
[a, a, a, ..., a][b, b, b, ..., b][c, c, c, ..., c]
^ ^ ^
// The 2nd Execute
[a, a, a, ..., a][b, b, b, ..., b][c, c, c, ..., c]
^ ^ ^
// The 3rd Execute
[a, a, a, ..., a][b, b, b, ..., b][c, c, c, ..., c]
^ ^ ^
```


Your cache loves this. On the first Execute, on an instant you access that `a`

it will cause a cache miss. But due to **cache line **being a fixed size (e.g. 64 bytes) larger than the `a`

component (`int`

= 4 bytes) you want, cache already know the location of 16 consecutive integers as of the 1st execute. Therefore for 2nd ~ 16th Execute, reading/writing to `a`

will result in a cache hit.

The same happened to `b`

and `c`

, it will all cache misses on the first execute then you get bonus hits on some amount of entities coming after. So often, small and modular components results in more automatic performance improvement in DOTS. The sales pitch of DOTS is that if the API is friendly enough for you to make most of your game this way, the game simply will be faster.

But even if you must use large and complex components, even larger than cache line and having a mix of complex sized things like `bool`

in-between, at that point it might get hard to continue picturing the cache while you code. I think you don't have to worry if that is the case, you would still randomly get better performance overall depending on your logic and which fields you access on that large component. There are a lot of effort in Entities that try to align your `struct`

in favor of the cache.

## Points to?

Both style of entity iteration looked a bit different, but you can guess the reason that they are trying to accommodate the cache.

```
public partial struct MyJob : IJobEntity
{
public void Execute(in ComponentA a, ref ComponentB b, in ComponentC c)
{
b.Data += a.Data + c.Data;
}
}
```


In `IJobEntity`

style, the design is such that you must either use `in`

(basically `readonly ref`

) or `ref`

for RO and RW access. Then you read or write these variable normally. The keyword could pass `struct`

by reference instead of by value.

If they are passed by value, the code somewhere (the source generator part) that call this `Execute`

would already cause cache hit / miss way before your code. And that might be bad when you want many kind of components coming in ready for use, but has conditional access and you might ended up not using some of them. It'd be a waste of cache if they are already accessed. (Though even in that case, the cache has a built-in policy that least often used one will quickly get kicked out, etc.) With `in`

and `ref`

, it is only after you touch (read / write) these incoming variables that you do something to the cache and get some bonus hits for next few entities.

```
foreach (
var (a, b, c) in
SystemAPI.Query<RefRO<ComponentA>, RefRW<ComponentB>, RefRO<ComponentC>>()
)
{
b.ValueRW.Data += a.ValueRO.Data + c.ValueRO.Data;
}
```


In idiomatic `foreach`

style, the way they want you to write C# doesn't permit adding `ref`

or `in`

there. So the trick is that `RefRO`

and `RefRW`

type using C# property (`ValueRW`

/ `ValueRO`

) to facilitate the same "cache only if you touch it in your code". You need a few more `.`

to get to the data and a bit more verbose, but for performance it's a good deal.

## Compared with old GameObject way

Disclaimer that I don't actually know how `GameObject`

scattered on your Hierarchy ended up in memory, just a guess it might be this way. The fact that I don't know it, and I know how the memory looks like in DOTS, is already an improvement of DOTS over the old ways...

So you might want to loop through game objects `X`

, `Y`

, `Z`

in an array, with component `A`

, `B`

, `C`

attached on all of them. If you have an array of `GameObject`

type, then you have an array of pointers. Reading the first element of this array and causing cache miss won't give you any exciting bonus. Supposed that if your cache line is very big, the best is you know the address of the next `GameObject`

, not its data you are interested in.

```
// 1st iteration
Array of objects : [X, Y, Z]
^
// 2st iteration
Array of objects : [X, Y, Z]
^
// 3rd iteration
Array of objects : [X, Y, Z]
^
Somewhere in the memory : [(X)Transform, a, b, c]??????????[(Y)Transform, a, b, c]???[(Z)Transform, a, b, c]?????
```


Then you might have to get each component individually and cause an another jump. If memory is really looking this way, with mandatory `Transform`

component or other custom components you are not interested in right now, with `????`

being unknown length, and before DOTS you don't care since you are going pointer-happy and jumps repeatedly without caring the cache, the cache line will rarely get good bonus data that is useful in the next iteration loop. The `a`

data of each `GameObject`

are so far away from each other.

## Burst and SIMD : Automatic vectorization

The cache line bonus thing of reading the first `int`

and knowing 15 more `int`

can be further improved. What requested data from cache is not your C# code but a compiled assembly code. C# code might looks already cache-friendly, but choosing the right assembly code can push the limit of cache-friendliness further.

```
public partial struct MyJob : IJobEntity
{
public void Execute(in ComponentA a, ref ComponentB b, in ComponentC c)
{
b.Data += a.Data + c.Data;
}
}
```


Look at this work again. I mentioned that on the first read of `a`

, you would automatically get future `a`

into the cache for the next loop. But before you get to the next loop, you must also read `c`

, read `b`

, then write to `b`

, to get to the bonus `a`

waiting for you.

But how about using all those future `a`

**in one loop, **the same for `b`

and `c`

too?

If you mark the job for Burst compilation, it can look at anything looping ("scalar code", which in DOTS is common, and looked natural for the programmer) and rewrite them such that it performs the work of many consecutive loops in one go, becoming a "vector code".

It is a good job for machine to do for you since manually writing vector code often mask your actual intent with a lot of optimizations. Imagine if you are writing such that it perform 4 loops worth of work in one. Not only you need to pack up the variables and somehow make sure it became the right vector assembly command (depending on the target machine's processor), if the last loop ended up not adding up to 4 you must do the remaining in scalar way. Imagine doing that by hand on every loop in the game?

Let's slap on `[BurstCompile]`

right now and see how smart it is. I'll add a constant `1234`

into the mix just so it is obvious in the `AVX2`

assembly in the Burst Inspector. I like selecting `AVX2`

for performance debugging because [it introduces 256 bits commands](https://en.wikipedia.org/wiki/Advanced_Vector_Extensions). It is obvious when Burst is trying to take advantage of them.

```
[BurstCompile]
public partial struct MyJob : IJobEntity
{
public void Execute(in ComponentA a, ref ComponentB b, in ComponentC c)
{
b.Data += a.Data + c.Data + 1234;
}
}
```


The Burst Inspector comes with useful debug mode ("Coloured With Full Debug Information") that makes it easy to spot if it is doing the expected tricks. Here, you can see the comment saying about making an 8 element array of repeated `1234`

(that means this one `ymm`

register fits 8 `int`

, 32 * 8 = 256 bits register), which is not exactly what you wrote, but it is clearly cooking. Pink instructions indicates vector assembly command, they starts with `v`

. In other words, pink is good.

![](../../assets/7a6474d85ab8e9af.png)

And then you see the effort of utilizing this chunky `ymm_`

register.

![](../../assets/3df9b71a3cefa80e.png)

Interestingly, it tries to go beyond and even double up each command, using both `ymm1`

and `ymm2`

as its workbench at the same time. So this is like working on 16 `int`

consecutively, even though one vector command supports only up to 8 `int`

. I could see this double up of work might be to take advantage of bigger cache line. (The `+32`

bytes offset is the size of 8 `int`

.)

After reading out 8 + 8 `int`

from the native array of `B`

(`r14`

, you can see on `DEBUG_VALUE`

too), adding `rax`

and `rbx`

is adding multiple integers from `A`

and `C`

respectively. The preparation of `ymm0`

(eight `1234`

) earlier is then added to everything.

The following `add`

`cmp`

`jne`

is that leftover loop thing I talked about. If the remaining works are less than 16 `int`

(the `64`

you see is the size of 16 `int`

) , then...

![](../../assets/65850ee52a25e983.png)

It will finish up the rest one by one without vectorization. `rsi`

moves forward by 4 bytes each time so that's surely one `int`

each, and you see that `r14`

, `rax`

, `rbx`

casts are the same, and topped up with `1234`

.

This is wonderful that you get all these insane code (both the vectorized part and scalar part) without writing them!