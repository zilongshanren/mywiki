---
title: Basic Concepts in Unity for Software Engineers
url: https://blog.eyas.sh/2020/10/unity-for-engineers-pt1-basic-concepts/
author: Eyas Sharaiha
published: '2020-10-04'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

If you’re trying to get into game development as a Software Engineer, finding learning materials with the right level of context can be challenging. You’ll likely face a choice between following materials introducing you to basic C# and OOP concepts while also describing Unity concepts, or starting with advanced tutorials and be left to figure out the core concepts deductively.

To fill that gap, I’m writing a series called
** Unity for Software Engineers** (now
updated and

[available as a book](https://leanpub.com/unity-for-engineers)). This is the first piece, and I’ll be releasing additional installments over the next few weeks, so

[make sure to subscribe](http://eepurl.com/gVgusL)for updates. The series is intended for folks already comfortable with programming and software architecture, especially those who learn best as I do: starting with first principles and working your way upwards.

I started my programming journey around 17 years ago by picking up
[Game Maker](https://www.yoyogames.com/gamemaker). Countless hours spent coding
little games and tools led me to a bigger passion for programming. Eventually, I
was at a point where I focused mainly on Software Engineering. From my peers, I
know this is quite a common path that many of us took to find programming.

Yet the game development scene has changed significantly from those days. When I went to pick up Unity after a long absence from game development, I was mostly interested in understanding the basic concepts: what are the fundamental building blocks of a game? What do I need to know about how these building blocks are represented in memory or on disk? How is idiomatic code organized? What patterns are preferred?

In the first article in the series, we’ll focus on those first two questions.

## Scenes

A **Scene** is the largest unit of organizing your objects in-memory. Scenes
contain the objects making up your game.

In basic use, one scene represents a **single level** in your game, where one
scene is loaded at any given point. In more “advanced” use, you can have two or
more active scenes at a time. Scenes can be loaded additively and unloaded 1.
Having multiple scenes loaded during gameplay comes especially handy when
building a massive world; keeping far-away areas on-disk rather than in-memory
will help you stay within your performance budget.

![A scene editor showing an empty scene in 3D Mode.](../../assets/d3260d19c0cf554b.img)

Unity Scene editor opening a default empty scene in 3D mode. Empty
Scenes in Unity3D will by default include *Main Camera* and
*Directional light* objects.

![A scene editor showing a heavily populated scene in 3DM mode.](../../assets/fd89093b95843d36.img)

Unity Scene editor showing an example scene, with a few objects selected. You can use the scene view to edit levels in your game.

Every [ game object](https://blog.eyas.sh#gameobject) in Unity needs to be

*in*a scene.

## Game Objects

A **Game Object** (in code, `GameObject`

) is one of the basic building blocks of
a game.

Game Objects can represent both *physical* things you see in the game (e.g., a
player, the ground, a tree, a terrain, lights, a weapon, a bullet, an explosion)
*as well as* *metaphysical* things (e.g., an inventory manager, a multiplayer
controller, etc.) in your game.

Every Game Object has a position and rotation. For metaphysical objects, this doesn’t matter.

Game Objects can nest under each other. Each object’s position and rotation is relative to its parent object. An object directly in the scene is relative to “world space” coordinates.

![Screenshot showing nested objects for organizational purposes](../../assets/1f9b573a2ae1532f.img)

A group of objects nested together in a scene under an empty “Interior_Props” object, for organizational purposes.

You might choose to nest your objects for many reasons. For example, you might decide it organizationally makes sense to put all your “environment” (e.g., individual pieces that make up a city or village) objects under an empty parent object. This way, it can be collapsed in the scene view and easily moved together when building your game.

![Screenshot showing nested objects for functional purposes](../../assets/7d4535125952dfea.img)

A group of objects nested under the player. These include the player’s weapon, avatar, and various UI elements rendered around the player.

Game Object nesting can also have *functional significance*. For example, a
“Car” can be an object, with code that controls the car’s speed and rotation as
a whole. But individual child objects might represent the four wheels (these
would spin independently), the car body, windows, etc. Moving the parent car
object would move all the child objects, keeping their relative orientation to
the parent (and each other). We might want the player to interact with a door
separately from the rest of the car, for instance.

## Components (& MonoBehaviours)

![Screenshot showing the inspector window on an object.](../../assets/c309a03074564216.img)

The Warrior object from the previous screenshot is shown above in Unity’s
“Inspector” window. Each illustrated section (e.g., Animator, Rigidbody,
Collider) are *Components* making up this object.

Every Game Object is comprised of **Components**.

A Component implements a well-defined set of behaviors for a GameObject to execute. Everything that makes an object what it is would come from the components that make it up:

- A single “visible” piece of a car will have a
*Renderer*component that paints it, and likely a*Collider*component that sets up its collision bounds. - If a car represents the player, the car object itself might have a
*Player Input Controller*that takes key input events and translates these to code moving the car around.

While you can write large and complex Components that correspond 1:1 to an
object (e.g., a player component codes the entire player, while an enemy
component codes the enemy as a whole), it’s typically common to factor out your
logic into streamlined pieces corresponding to individual *traits*. For example:

- All objects with
*health*, whether a Player or an Enemy, might have a`LivingObject`

component that sets an initial health value, takes damage, and triggers a death event once it dies. - A player might additionally have an input component controlling its movement, while the enemy might have an AI component that controls its movement instead.

Components receive various callbacks throughout their lifetime, known in Unity
as *Messages*. Examples of Messages include `OnEnable`

/`OnDisable`

, `Start`

,
`OnDestroy`

, `Update`

, and others. If an object implements an `Update()`

method,
this method will automagically be called by Unity in every frame of the game
loop while the object is active, and the given component is enabled. These
methods can be marked `private`

; the Unity engine will still call them.

Components can also expose public methods as you’d expect. Other components can take a reference to a component and call these public methods.

## Assets

**Assets** are the on-disk resources that make up your game project. These
include meshes (models), textures, sprites, sounds, and other resources.

When serialized to the disk, your scenes are represented as assets made up of
the Game Objects inside of them. We’ll also discuss in the next section how you
can make Game Objects that are reused often into an asset known as a
[Prefab](https://blog.eyas.sh#prefab).[2](https://blog.eyas.sh#user-content-fn-2)

![Unity Asset view showing visual assets in a game project](../../assets/53d00725da1cf9cf.img)

Assets can also represent less tangible things, such as Input Control Maps,
Graphics Settings, i18n string databases, and more. You can also create your own
custom asset types
[using ScriptableObjects](https://unity.com/how-to/architect-game-code-scriptable-objects).
I wrote about how these are saved
[here](https://blog.eyas.sh/2020/09/where-scriptableobjects-live/).

For your in-development project, assets form the key representation of your project’s codebase, alongside your code.

Your built-and-bundled game will include *most* 3 of your assets. These assets
will be saved on disk on the device where the game is installed.

## Prefabs

![Photo of rows of container homes](../../assets/8baa47aeca4ee2f0.img)

Game Objects, their Components, and their input parameters exist as individual
*instances* in a scene. But what if a particular class of objects is commonly
repeated? Such objects can be made into a **Prefab**, which is effectively the
object in asset form.

Instances of a prefab in a scene can have local modifications that distinguish
it (e.g., if a *tree* object is a prefab, you can have tree instances of
different heights). Instances of a prefab all inherit and override data from
their prefab.

### Nested Prefabs

Starting with Unity 2018.3, Prefabs can be nested just as you expect:

- A parent object with prefab child objects can be a prefab itself. In the parent prefab, the child prefab instance can have its own modifications. In the scene, the entire prefab hierarchy is instantiated, and scene-specific modifications can layer on top.
- A prefab instance in a scene with its own local modifications can be saved as its own “Prefab Variant” asset. A variant is a prefab asset that inherits from another prefab, applying additional modifications on top.

These concepts compose; a prefab variant of a nested prefab, or a prefab variant of a prefab variant, for instance.

## Serialization & Deserialization

Your project’s assets, scenes, and objects are all persisted on-disk. When
editing your game, these objects are loaded in memory and saved back to disk
using
[Unity’s serialization system](https://blogs.unity3d.com/2014/06/24/serialization-in-unity/).
When playtesting your game, the objects and scenes in-memory are loaded through
the same serialization system. This system also maps between assets in your
compiled bundle and the loaded/unloaded scene objects in-memory.

The Unity Engine’s Serialization/Deserialization flow loads on-disk assets into memory (in your project: for editing/playtesting; in-game, when loading a scene) and is responsible for saving the state of your edited objects & components back into their scenes and prefabs.

Therefore, the serialization system is also at the core of the Unity Editor
experience itself. For a `MonoBehaviour`

to take an input on construction when
instantiated in a scene, those fields must be *serialized*.

Most core Unity types such as `GameObject`

s, `MonoBehaviour`

s, and asset
resources are
[Serializable](https://docs.microsoft.com/en-us/dotnet/api/system.serializableattribute)
and can receive initial values on creation from within the Unity Editor. Public
fields on your `MonoBehaviour`

are serialized by default (if they’re of a
serializable type), and private fields need to be marked with Unity’s
[ [SerializeField]](https://docs.unity3d.com/ScriptReference/SerializeField.html)
attribute to be serialized as well.

![Screenshot of 2015 game Chaos Reborn, Made with Unity.](../../assets/f5690f96aec0e574.img)

Screenshot of 2015 game [Chaos Reborn](http://www.chaos-reborn.com/) by Snapshot
Games. [BY-CC-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/deed.en)

# Conclusion

These six concepts cover essential structural pieces for architecting games in Unity. Knowing more about these and how assets on-disk map to in-memory representation should give you the intuition needed to follow some of the more advanced tutorials.

There are still significant areas to wrap your head around in Unity.
Understanding the Editor and
[mapping your Software Engineering best practices to game development best practices](https://blog.eyas.sh/2020/10/unity-for-engineers-pt2-six-practices)
will help hone in your skill. Even more, understanding broad areas such as
[lighting](https://blog.eyas.sh/2020/10/unity-for-engineers-pt6-rendering/),
[animation controllers](https://blog.eyas.sh/2020/11/unity-for-engineers-pt9-animation/), navigation
meshes, input handling will help you go a long way as well.

I will cover many of these topics in future iterations of this series, but I’m hopeful you’re armed with the knowledge that makes the rest of your game development journey more intuitive.

## Footnotes

-
Still, there can only ever be one “main” active scene at a time.

[↩](https://blog.eyas.sh#user-content-fnref-1) -
The term asset is a bit overloaded. Scenes are Prefabs are

*serialized*and*organized*in your projects like other assets. You can browse these in the Asset view alongside code and other assets. If you’re deep in Editor code manipulating an asset, Prefabs and Scenes cannot usually be treated as assets.[↩](https://blog.eyas.sh#user-content-fnref-2) -
You can further optimize your game by loading some assets over the network or employing other

[asset-management techniques](https://docs.unity3d.com/Packages/com.unity.addressables@latest/).[↩](https://blog.eyas.sh#user-content-fnref-3)