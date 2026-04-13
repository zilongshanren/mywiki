---
title: All the places a ScriptableObject is stored
url: https://blog.eyas.sh/2020/09/where-scriptableobjects-live/
author: Eyas Sharaiha
published: '2020-09-25'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

In Unity,
[architecting games using scriptable objects](https://unity.com/how-to/architect-game-code-scriptable-objects)
is gaining traction. Data represented as a `ScriptableObject`

can be decoupled
from specific runtime objects, referenced liberally in prefabs, and used to
streamline communication across objects.

A serialized `ScriptableObject`

can be stored within its own asset file, within
another asset, or even directly within a scene.

## Creating `ScriptableObject`

s

### … as a standalone .asset

![A standalone asset appears on its own within the project view.](../../assets/927f492e23a77f4b.img)

A great shortcut to creating a `ScriptableObject`

in its own asset is using the
[ [CreateAssetMenu]](https://docs.unity3d.com/ScriptReference/CreateAssetMenuAttribute.html)
attribute.

If you would like to create an asset manually in your Editor script, you can
first create the object in-memory using
[ ScriptableObject.CreateInstance](https://docs.unity3d.com/ScriptReference/ScriptableObject.CreateInstance.html),
then persisting it with

`AssetDatabase.CreateAsset`

:```
var created = ScriptableObject.CreateInstance<MyScriptableObject>();
AssetDatabase.CreateAsset(created, "Assets/My Object Name.asset");
```


### … within another .asset

![An asset with sub-assets.](../../assets/43f2d657cb3430c1.img)

The main asset, shown here named as “My Object”, with a few unnamed sub-assets.

An Asset doesn’t have to be made of a single object. This is especially helpful when a certain object is meaningless on its own.

For example, we can represent an entire Dialogue encounter as a directed graph of potential interactions. It might be helpful to represent a Dialogue Node as a ScriptableObject, but persisting each Node as a separate asset could pollute your asset tree and lead to confusion as single pieces of interaction make little sense without their surrounding context.

Here, we can add a `ScriptableObject`

to another asset using
[ AssetDatabase.AddObjectToAsset](https://docs.unity3d.com/ScriptReference/AssetDatabase.AddObjectToAsset.html):

```
var created = ScriptableObject.CreateInstance<MyScriptableObject>();
AssetDatabase.AddObjectToAsset(created, "Assets/Path To Specific.asset");
```


or even:

```
var created = ScriptableObject.CreateInstance<MyScriptableObject>();
Object target = property.serializedObject.targetObject;
if (!EditorUtility.IsPersistent(target))
{
throw new UnityException("Trying to add object to non-persistent target.");
}
AssetDatabase.AddObjectToAsset(created, target);
```


Note that each Asset file has a “Main” Asset and any number of sub-assets.
[ AssetDatabase.IsMainAsset](https://docs.unity3d.com/ScriptReference/AssetDatabase.IsMainAsset.html)
and

[can let you know given a](https://docs.unity3d.com/ScriptReference/AssetDatabase.IsSubAsset.html)

`IsSubAsset`

`UnityEngine.Object`

or instance ID.### … in scenes?

If you add an in-memory `ScriptableObject`

to a `SerializedProperty`

and apply
it to a scene object, you might be surprised to see the object show up in your
.scene file. The serialization behavior of `ScriptableObject`

s within
scene-bound `GameObject`

s is quite different from assets:

Scene game objects are not persistent. That means `EditorUtility.IsPersistent`

will be false when passing your scene-bound game object. It also means that
passing your game object as the asset object in `AddObjectToAsset`

will not
work; rather, it throws an exception stating the game object is not persistent.

How do you add a `ScriptableObject`

to a scene-bound `GameObject`

, you ask? By
doing nothing—obviously 🤷.

```
var created = ScriptableObject.CreateInstance<MyScriptableObject>();
property.objectReferenceValue = created;
property.serializedObject.ApplyModifiedProperties();
```


Once you do so and save your scene, you’ll notice the serialized scriptable object appear in your .scene file.

### … what about prefabs?

It would be reasonable to assume a scriptable object is similarly persisted in a .prefab file if you do the same thing within a prefab context. It would also be wrong.

A prefab object is not persistent. Yet, adding a `ScriptableObject`

to a
`SerializedProperty`

inside of it will only *appear* to do the same thing as a
scene when it is still in memory. The moment you save an exit a prefab, you’ll
notice the scriptable object was never serialized, and property fields that
reference it appear null.

## Popular Case Studies in the Wild

### Global `ScriptableObject`

assets use cases are often intuitive

[Ryan Hipple describes](https://www.youtube.com/watch?v=raQ3iHhE_Kk) using
global objects created with `[CreateAssetMenu]`

to represent global variables
and events (e.g. a Player’s HP). In
[Richard Fine’s talk](https://www.youtube.com/watch?v=6vmRwLYWNRo), he also uses
global assets to represent pluggable AIs, audio events that play sounds with
various strategies, etc. In all those cases, these objects are individual
reusable assets, which you could reference throughout your game.

To me, these use cases seem straightforward: these `ScriptableObject`

assets
seem to fall into two categories:

-
Reduce repetition by referencing similar “classes” of data/behaviors together, such as a similar set of sounds that most explosions can make, or basic characteristics of certain enemies

-
Replace static variables, or global “game state managers”, from a

`GameObject`

representation to a global representation

You can reference a Player HP ScriptableObject within a pure Prefab context, for example, without depending on a Player or Player Health manager existing in the same scene, etc.

### A `ScriptableObject`

sub-asset is often useful too

While Ryan Hipple demonstrates compelling use cases of having many small
`ScriptableObject`

s, [Richard Fine](https://www.youtube.com/watch?v=6vmRwLYWNRo)
shows much larger `ScriptableObject`

s housing Game State, destruction sequences,
and more.

When this data needs to be serialized, in most cases, this data should probably
be represented as a plain-old-data-object with a `[Serializable]`

attribute.
Sometimes, however, data *within* a `ScriptableObject`

is best represented as a
`ScriptableObject`

sub-asset itself.

![A Dialogue encounter represented as a graph in a custom Unity Editor](../../assets/70c0f13e88693153.img)

Due to the frequent representation of dialogue trees as graphs, it is often compelling to represent each node in an editor as its own Scriptable Object.

For example, if you are building a graph of objects that cross-reference each
other (e.g. a State Machine with its own editor, a Dialogue graph, etc.), then
you will probably want to represent nodes as `UnityEngine.Object`

s that are
referenced by instance ID when serialized, rather than serialize copies of the
same object.

### Scene-attached `ScriptableObject`

s seem less clear

I [previously discussed](https://blog.eyas.sh/2020/09/patterns-in-unity-adventure-tutorial/) some
interesting patterns in Unity’s
[Adventure Game tutorial](https://learn.unity.com/project/adventure-game-tutorial)
from 2016.

That tutorial ends up presenting interesting questions about when to embed a
`ScriptableObject`

on its own, when to embed it within another
`ScriptableObject`

asset, and when you might put it on a scene directly.

One heuristic to decide what architecture works best for you looks something like this:

| Need to reference across objects | No need to cross-reference | |
|---|---|---|
| Varies wildly per-Object instance | `ScriptableObject` within an asset. (should be rare) | `[Serializable]` class or struct. ** |
| Limited “classes” of data/behaviors | `ScriptableObject` within an asset. | Reference `ScriptableObject` within an asset. |

You might see this leaves little room for Scene-attached scriptable objects.
Indeed, in my previous article, I wondered out loud why a scene-only
`ScriptableObject`

attached to a `MonoBehaviour`

makes sense, rather than
serializing the same information in a `Serializable`

class or struct. Part of
the answer, it turns out, is as a shortcut to support serialized polymorphism.

If your property can be of multiple sub-types, and each sub-type might need a
custom editor or property drawer, you’ll have a much easier type representing
this in `ScriptableObject`

s than a `[Serializable]`

abstract parent class.
Unity’s
[Adventure Game tutorial](https://learn.unity.com/project/adventure-game-tutorial)
takes advantage of this in the `EditorWithSubEditors`

construct.

In general, beware of Scene-attached scriptable objects; these have some pitfalls:

- Your
`ScriptableObject`

s will always be on a scene. If you prefab an object that references Scene-attached`ScriptableObject`

s, these properties will remain as overrides in the scene itself. - When in the Editor, you might mistakenly set these values within a prefab and assume all is well until you switch scenes.

Where your needs outweigh these pitfalls, Scene-attached Scriptable Objects remain a powerful tool.

## Tools in your Toolbox

Ultimately, each of these patterns is a tool appropriate for some jobs more than others. These patterns are not an ordered list of best-practices that always make sense compared to lower-ranked alternatives.

If you have a singular “global” value that tracks game state, consider persisting assets. Similarly, try replacing your global/static “manager” GameObject with an asset.

Where it makes sense, group some of these assets under an appropriate “parent” asset.

In a few cases, it might make sense to just put your Scriptable Object in a scene.

Just as importantly, however, think if your data/behavior *really* needs to be
in a Unity Object. If you can get away with it, why not use lighter weight
serializable classes or structs?