---
title: Starting Box2D 3.0
url: https://box2d.org/posts/2023/01/starting-box2d-3.0/
published: '2023-01-15'
source_blog: Box2D
source_site: https://box2d.org/
category: graphics
fetched: '2026-04-19'
---

Over the holidays I started working on version 3.0 of Box2D. I started closing out some issues for v2.4 and then moved onto a backlog task: speculative collision. Speculative collision is a technique for continuous collision that promises to remove the serial bottleneck of time of impact sub-stepping. I made good progress in my research and then I realized that this would be a major update to Box2D. And if I’m doing a major update to Box2D I might as well tackle some other big features and make version 3.0.

I think now is a good time to explain my goals for version 3.0. So lets go over the list.

## Speculative collision

Currently Box2D has a robust time of impact solver for continuous collision and response. The response includes sub-stepping, this means:

- objects don’t freeze when they collide (e.g. time loss), instead a sub-step is taken to finish their journey to the end of full time step.
- chain reactions are accounted for: a fast body hits a slow body which becomes a fast body which hits another body and so on.

The highest quality simulation happens when all rigid bodies can participate in sub-stepping. This is inherently serial and precludes multithreading. It is also very expensive. Version 2.4 mitigates this cost a by restricting time of impact and sub-stepping for dynamic versus static bodies only. An exception is dynamic bodies with the `bullet`

flag enabled. This is off by default, so performance stays somewhat reasonable. A single bullet can cause the entire simulation to be serial. Not good.

Speculative collision predicts contact points between fast moving objects before they touch. This allows the main physics step to prevent tunneling. No sub-steps required! Which is great because this allows for easy multithreading. However, it is not perfect. Collisions can be missed and there can be ghost collisions. Hence the research I’ve been doing. Look for a future blog post on that.

Another benefit of speculative collision is that I can eliminate the polygon skin/radius on collision shapes. That was necessary to keep shapes separated for the time of impact algorithm. This should no longer be necessary in version 3.0. I never liked this artificial separation of shapes.

## API changes

The Box2D API currently operates on pointers. You have a `b2World`

pointer, a `b2Body`

pointer, a `b2Joint`

pointer, and so on. Because the user has a pointer, that memory is pinned and reduces my ability to optimize. Also the C++ style API inherently exposes all the internal data in headers. I’ve always disliked APIs that are slow to compile, so why should I add to the problem?

My plan is to switch to a C-style function based API with handles. These handles will be small structs and act like IDs. For example:

```
struct b2BodyId
{
int32_t bodyIndex;
}
```


This makes them type safe yet small enough to pass around on the stack. The user should not normally care what is in `b2BodyId`

unless they are debugging. I have a solution for that which I’ll share later.

So expect to see an API like this:

```
b2WorldId worldId = b2CreateWorld();
b2BodyId bodyId = b2World_CreateBody(worldId, ...);
...
b2Transform transform = b2Body_GetTransform(bodyId);
...
b2World_DestroyBody(bodyId);
b2DestroyWorld(worldId);
```


The nice thing about an API like this is that it can easily fit in one header file and it should compile very quickly.

## Moving to C from C++

When I created Box2D I had no idea it would be ported/binded/wrapped to so many other languages and platforms. If I had, I would have probably written it in C to begin with. Back in those days C99 support was spotty, but that seems to have been resolved. I don’t think I could stomach C89 with the declaration requirements.

The C++ usage in Box2D is very light. There is no usage of `std`

and polymorphism is only used for a couple classes. So there is little justification for Box2D to be in C++ rather than C, and with the API change above, there is even less reason. The main thing I am missing so far are math operator overloads. But even that is not a big deal. It hasn’t slowed me down at all.

## Why not language X?

A couple reasons:

- I’m already taking on a lot to work on version 3.0. I still have a full-time job as well!
- I’m a slave to tooling. I work on Windows and I place a high value on easy debugging and other tools.
- I want to make Box2D easy to port/wrap/bind to your favorite language! Please give me your feedback on this as version 3.0 develops.

## Performance

I originally developed Box2D in 2006, before multithreading was important. Clearly times have changed and multithreading is now a must. Initially I plan to multithread contact point computation and solver islands. These are both easy to do. I plan to use callbacks to send jobs to the host application, which presumably has it’s own task system. I will also provide a working example of this in the samples that you can mimic in your project. My opinion is that a library should not be creating its own threads, instead the application should be in charge of threading. This should put Box2D into a good place for pushing on other optimizations. Box2D was designed to have performant yet understandable algorithms. In fact Box2D originated from tutorial code. However, I think that performance has become more important than pedagogy for Box2D’s future.

## Capsules

Besides performance, I want a reason for people to upgrade to version 3.0. I think capsules is such a feature. People have wanted capsules for years, so I’m diving back into the narrow phase.

## When can I see it?

I’m currently porting all the collision code and adding capsule support. Next, I plan to port the world and solver. Once I have some box stacking I will make the repo public. This will be very much alpha code! But it will useful for giving feedback about the API and such.

Once version 3.0 is ready for release, the new repo will become the main repo and the 2.4 repo will become a legacy repo (with limited/no support).

## Beyond version 3.0

I plan to continue working on Box2D more regularly. There are lots of interesting problems to tackle. Thanks for your encouragement, support, and feedback.

If you’d like to sponsor Box2D development, you can sign up here: [https://github.com/sponsors/erincatto](https://github.com/sponsors/erincatto)

1061 words

2023-01-14 16:00 -0800