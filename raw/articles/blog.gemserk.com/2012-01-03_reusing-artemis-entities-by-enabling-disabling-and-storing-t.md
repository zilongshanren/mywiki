---
title: Reusing Artemis entities by enabling, disabling and storing them
url: https://blog.gemserk.com/2012/01/03/reusing-artemis-entities-by-enabling-disabling-and-storing-them/
published: '2012-01-03'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

As we mentioned on a [previous post](https://blog.gemserk.com/2012/01/02/basic-frustum-culling-to-avoid-rendering-entities-outside-screen/), we were having some performance issues in Vampire Runner and we were trying different approaches to improve its performance.

### Introduction

One limitation of Android when making games is you have to avoid generating garbage whenever you can since the garbage collection would generate pauses on your games and that leads to a bad user experience. Then, we should try to reuse already created object instead of creating new ones.

In Vampire Runner, one problem we were having was that we were creating a lot of entities at a specific moment of the game, when we detected a new obstacle should be created, and that was making some pauses on the Android version.

As we use Artemis, we should try to reuse some entities when we can. For example, if we make a shooting game (like the [Jetpac prototype](https://blog.gemserk.com/2011/09/27/a-game-prototype-mad-jetpack/) I made) it seems a good idea to reuse bullets since their life cycle is really short. [Ziggy](http://www.ziggysgames.com/) made two blog posts about this topic some weeks ago [here](http://www.ziggysgames.com/my-weapon-bullet-system-using-artemis-and-libgdx-box2d) and [here](http://www.ziggysgames.com/weapon-bullet-system-part-2-recycling-dead-bullets), however we followed a slightly different approach and we will explain it in this post.

### Storing entities to reuse them

We created a concept named [Store](https://github.com/gemserk/commons-gdx/blob/master/commons-gdx-core/src/main/java/com/gemserk/commons/utils/Store.java) (similar to LibGDX Pool

```
free(T t) // returns an entity to the Store to be reused later
get() : t // returns an entity from the Store, it reuses an object from the free
collection if there is one or creates a new object otherwise.
```


The idea is to, for example, instead of creating a new bullet when a weapon is fired, calling store.get() and set the component values as they should be, and when the bullet collides with something call the store.free(e) instead of deleting the entity, so we can reuse it later.

This is a generic approach and we can use different stores to reuse different kind of entities but it has a big problem, those entities keep being in Artemis world, that means they keep being processed (collisions, render, etc). A basic solution to this problem was adding a new state to the entity, and we explain that in the following section.

### Enabling and disabling Artemis entities

Artemis supports reuse of entities by internally caching created entities inside the World class, however their state (which components their have) is not easily reused, and that was one of the big problems when creating a new entity, we wanted to reuse their state.

Our current solution to the problem was adding a new state to the entities, if they are enabled or not. Being enabled means the entity is processed by all interested EntitySystems, being disabled means the entity is still in the Artemis world but it is not processed by any system.

So, in our customization of [Artemis](https://github.com/gemserk/artemis/tree/gemserk) we added three new methods to Entity to be called whenever you want to enable or disable an entity:

```
disable() : disables an entity to avoid it to be processed on EntitySystems
enable() : enables again an entity to let it be processed on EntitySystems
isEnabled() : returns true if the entity is enabled, false otherwise.
```


Then, we added new methods to EntitySystem API to let each EntitySystem to be aware an entity of interest was enabled or disabled:

```
disabled(Entity e) : called whenever an entity of this EntitySystem was disabled
enabled(Entity e) : called whenever an entity of this EntitySystem was disabled
```


In our case, we are using them to enable and disable Box2D bodies in our PhysicsSystem, and also to remove them from our render layers in our RenderSystem.

As an example, we have a nice video of Vampire Runner we made by changing the zoom of the camera to see the behind the scenes:

As you can see, when entities like wall, fire and Christmas stuff are behind the main character, they disappear. That is because they are disabled and moved again to their stores so they stop being processed by Artemis, in particular, stop being rendered.

### Conclusion

By combining both solutions, we have an easy way to reuse created entities of one kind, like our obstacles tiles in Vampire Runner, while at the same time we can disable them when they are on a store to avoid them being processed.

In case of Vampire Runner, this solution improved Vampire Runner performance since we now pre create a lot of entities we need during the game and then disable them and enable them only when needed, in this way, we could avoid creating a lot of entities in one update after the game was started.

This is a first approach solution to the problem and seems good for our current games but it may not fit other type of games or bigger games, we don’t know that yet.

If you use Artemis and you had this problem too, hope this blog post is helpful to you.