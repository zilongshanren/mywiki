---
title: Understanding Unity Engine Objects
url: https://blog.eyas.sh/2020/10/unity-for-engineers-pt5-object-component/
author: Eyas Sharaiha
published: '2020-10-23'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

We already discussed
[Game Objects](https://blog.eyas.sh/2020/10/unity-for-engineers-pt1-basic-concepts#gameobject) and
[Components](https://blog.eyas.sh/2020/10/unity-for-engineers-pt1-basic-concepts#component) as two
of the fundamental building blocks of the Unity Engine. Today, we’ll discuss
their programmatic representation.

*This is Unity for Software Engineers
(now updated and
available as a book), a series for
folks familiar with software development best practices seeking an accelerated
introduction to Unity as an engine and editor. More is coming over the next few
weeks, so consider subscribing for updates.*

The Unity Engine *runtime* is primarily written in C++, and much of the Engine’s
primitives (such as the game objects and their components) live in C++ land.
You’ll also know that the Unity Engine *API* is in C#. The API gives you access
to all of Unity’s native objects in a way that—save for a few pitfalls
we’ll discuss today—feels like intuitive, idiomatic C#.

The *C#* class hierarchy of `UnityEngine.Object`

, `GameObject`

,
`ScriptableObject`

, `Component`

, and their children. This should map to the
*conceptual* hierarchy of how to think about these objects, though sometimes the
runtime implementation will look different.

## UnityEngine.Object

At the top of the Unity Object hierarchy sits ** UnityEngine.Object**. For the
most part provides a

`name`

string, an `int GetInstanceID()`

method, and a bunch
of equality comparers.The class also provides a `static void Destroy(Object obj)`

method (and some
overloads) that destroys a `UnityEngine.Object`

and any of its subclasses. When
an Object is destroyed, the *native* part of the object is freed from memory,
and the smaller *managed* part will be garbage collected *at some point* after
there are no more references to it.

Because your valid reference to a `UnityEngine.Object`

can point to a destroyed
native object, `UnityEngine.Object`

overrides C#‘s `operator==`

and `operator!=`

to make a destroyed Object *appear* null. Simply accessing methods on a
destroyed object will return `NullReferenceException`

, albeit with a friendlier
error message that tells you which object you were trying to access.

## GameObject

A **GameObject** derives from Object and represents anything in your scene.

Let’s start at a high-level: A GameObject inherits a name and instance ID from its parent. Otherwise, conceptually, a GameObject

- has a list of
on it,**Components** - has a
`tag`

string for organizational purposes, and - belongs to a
[layer](https://docs.unity3d.com/Manual/Layers.html).

A GameObject’s state

- is the product of all of its
*Components’*state, and - whether an object is active or not.

Let’s dig a bit deeper. When starting, most of the interesting stuff in a
GameObject is in its **Components**. A GameObject has at least one Component:
its [ Transform](https://docs.unity3d.com/ScriptReference/Transform.html). A
Transform describes the position and rotation of the GameObject. A Transform
includes helper properties that show an object’s

*absolute world*position and rotation, as well as the position and rotation

*relative*to its parent. In the Editor, the Transform position and rotation are set from the

*parent relative*variants.

Since every GameObject has a Transform (and also, given that a Transform is
frequently needed/accessed), the GameObject directly exposes a
`Transform transform`

public property.

You can access individual components from `T GetComponent<T>()`

, or lists of
components from `T[] GetComponents<T>()`

, etc. These methods search through all
components on a GameObject and return ones with a compatible type (or null, if
none exist in the singular case). Since these methods search through components
and check type compatibility, it is often recommended to cache this lookup.

If you are building/extending a GameObject by hand, you can always use
`T AddComponent<T>()`

. In most cases, however, you’re better off using the
Editor.

Individual Objects (a Component or ScriptableObject) might refer to other
`GameObjects`

in a few ways:

-
**By reference**. By exposing a`GameObject`

*serialized field*that you then set from the inspector.*We have discussed serialization extensively throughout the series:*.[as a fundamental concept](https://blog.eyas.sh/2020/10/unity-for-engineers-pt1-basic-concepts#serialization)and in our tour of the Editor, when[describing the Inspector](https://blog.eyas.sh/2020/10/unity-for-engineers-pt4-editor-tour#inspector), and the[practice](https://blog.eyas.sh/2020/10/unity-for-engineers-pt2-six-practices)of using the Inspector as an injection framework -
**Using tags**. Every Game Object can have a*tag*string. You can find objects in the scene using that tag through the static functions`GameObject.FindGameObjectsWithTag`

and`GameObject.FindGameObjectWithTag`

. A GameObject also exposes a public`bool CompareTag(string tag)`

method.This is a quick-and-dirty way to get the job done, but is still a popular way. A common use of this in the wild is to have a

`"Player"`

tag to find the Player. Ideally, these methods should not be called every frame, so if you have to use them, consider caching the result. -
**Using layers**. A layer is an`int`

between 0 and 31. Every Game Object is in exactly one layer.While you can’t directly look up all objects in a layer, if you already have a reference to a GameObject (e.g., in a collision event), you can check a GameObject against a

. A`LayerMask`

`LayerMask`

is typically used in functions like`Physics.Raycast()`

. This allows you to find objects with colliders intersecting with a given*ray*. Passing a`LayerMask`

to`Physics.Raycast()`

will only return objects within the specified set of layers.Inside the Unity Engine,

*Cameras*make heavy use of layers. E.g., you can have one camera that renders “everything but UI”, and overlay another camera for an in-game HUD, etc. -
**Using indirect references**. There are many reasons why the methods above might be insufficient: you might not want to use tags to avoid depending on copy-pasted strings, and layers might not fit your use case. If referencing a fellow object in-scene is not an option (e.g., you’re dealing with a dynamic set of objects or don’t have access to the current scene objects in the context you need this reference, etc.), then you might want to look further.For this, an increasingly popular concept is

*runtime sets*Scriptable Objects. You can read more about this in Unity’s how-to article on[architecting your game with ScriptableObjects](https://unity.com/how-to/architect-game-code-scriptable-objects), based on[the talk](https://www.youtube.com/watch?v=raQ3iHhE_Kk)by Ryan Hipple. If you have an hour to spare, you might want to watch the whole thing.

A GameObject also exposes a `BroadcastMessage`

and `SendMessage`

functions that
propagate *messages* (described in the [ Component](https://blog.eyas.sh#component) section) to
all components in or under it.

![Photo of a Building Structure](../../assets/ca8c17eb404a8199.img)

Photo by [Ramin Khatibi](https://unsplash.com/@raminix) via Unsplash.

## Component

Every behavior on a GameObject is driven through its Components.
User-implemented Components will usually extend the `MonoBehaviour`

subclass
(more on that later).

A Component inherits a name and instance ID from its parent. Otherwise, conceptually, a Component

- always
*belongs*to a single GameObject, exposed as a public`GameObject gameObject`

property, and - can receive
**messages**, driving much of its behavior.

The state of a component on an *active* GameObject lies entirely in its
implementation.

In addition to its `GameObject`

, a component exposes shorthand properties and
methods such as `Transform transform`

, `T GetComponent<T>()`

, etc. These are
simply convenience shorthands for accessing those same methods on the
corresponding `gameObject`

.

The most important functionality of a Component is driven through **Unity
Messages** (also sometimes called *Unity Event Functions* when referring to
built-in messages). These are effectively callbacks functions triggered *by the
Engine* in certain situations. Every Component will receive a `Awake()`

,
`Start()`

, `Update()`

and other messages, for example. The Unity Docs on the
[Order of Execution](https://docs.unity3d.com/Manual/ExecutionOrder.html) of
these messages is a convenient resource.

To have your component receive a particular message, simply add a
* private void* method with the appropriate message name. The runtime will use
reflection to call these messages, when applicable. This is why you don’t see an

`override`

directive on these messages. Messages like `Update`

, `LateUpdate`

,
and `FixedUpdate`

are inspected once per type, so don’t worry about reflection
being used in every frame. See more details in the
”[10000 Update() calls](https://blogs.unity3d.com/2015/12/23/1k-update-calls/)” Unity blog post for more information.

A ** Behaviour** is a type of component that

*can be enabled or disabled*. When a

`Behaviour`

is disabled, `Start`

, `Update`

, `FixedUpdate`

, `LateUpdate`

,
`OnEnable`

, and `OnDisable`

messages are not called.A ** MonoBehaviour** is a

`Behaviour`

that also enables using
[Coroutines](https://docs.unity3d.com/Manual/Coroutines.html).

## A Note on Inactive Objects and Disabled Components

A GameObject in a loaded scene will exist in memory until the object is
*Destroyed* explicitly or the scene is unloaded. A GameObject can be set to
*inactive*, which will cause it to stop receiving `Update`

(and related) events.

**When an object is created**, the messages called on a component depend on
if: (1) the GameObject is active, and (2) the component is enabled:

GameObject is active | GameObject is inactive | |
|---|---|---|
| Component is Enabled | `Awake` , `OnEnable` , `Start` | Component implicitly disabled |
| Component is Disabled | `Awake` | `Awake` |

**When an object is set to active or a Behaviour is set to enabled**:


`OnEnable`

will be called.- If
`Start`

has never been called on this`Behaviour`

, it will be called exactly once.

## Takeaways

Some takeaways of all this:

- A Unity object might
*appear to become*when destroyed.`null`

`== null`

checking does more than you think. - As a result, null-coalescing operators (
`??`

,`??=`

) and null-conditional operators (`?.`

,`?[]`

) don’t work as expected. - Yes, your Unity Messages can be private!
- Don’t create abstract classes that unnecessarily declare
`Update`

or other messages to make overriding easier; that’ll result in the engine always calling these events. - Disabling an Object or Component is a great way to limit its game logic or save on CPU-bound effort, but these objects still have a memory overhead.