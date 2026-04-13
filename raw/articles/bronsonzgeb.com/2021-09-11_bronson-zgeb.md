---
title: Bronson Zgeb
url: https://bronsonzgeb.com/index.php/2021/09/11/the-scriptable-object-asset-registry-pattern/
author: Bronson
published: '2021-09-11'
source_blog: Bronson Zgeb
source_site: https://bronsonzgeb.com
category: game programming
fetched: '2026-04-13'
---

# The Scriptable Object Asset Registry Pattern

![Just a scene](../../assets/6457808672fc40be.png)

This article describes a pattern to serialize prefabs or any complex data. Doing so allows us to store data to disk or send it over a network to either a game server or another game client. This article pairs well with the previous article on saving and loading data, so I recommend you read that one first if you haven’t already.

## What problem are we solving?

We need a stable way to store and retrieve game objects using a simple reference. Doing so allows us to save the state of our world using a minimal amount of data. How? We store the data in a standard prefab or scriptable object in the project and reference it with an id, rather than keeping the entire structure in our saved state. Additionally, we can store any values that differ from the original, like health and position.

At this point, you might be asking, “Hey, isn’t this what the Addressables package does?” There is some overlap; however, I’ve been using this pattern since before Addressables existed and continue to use it. Sometimes I even use both in the same project. Addressables is a more complex system focused on finding your assets no matter where they’re stored. This article describes a simple implementation of a pattern that you could execute in many ways, including using the Addressables system.

## How do we do it?

We’ll create a registry to hold all the objects we need to serialize. In the simplest case, this is a Scriptable Object that contains a list of Descriptors, which is a type we’ll define. A Descriptor will also be a Scriptable Object that holds an id and references some data, such as a prefab. Then whenever we need to load a prefab from the Registry, we ask it to find the Descriptor with a given id and instantiate a new instance from the prefab reference.

By the way, I used to use this pattern to create a homebrew version of nested prefabs and prefab variants. A Descriptor can contain as much data as we need, so it’s possible to reference a prefab and store a bunch of override data. Then when you instantiate the prefab, you immediately assign all the overridden data. As it turns out, this is precisely how nested prefabs work.

We’ll start by defining a `SerializableScriptableObject`

type, the base class for our Descriptors.

## Serializable Scriptable Object

A `SerializableScriptableObject`

is a Scriptable Object that automatically saves its GUID. Speaking of, GUID stands for Global Unique Identifier. It’s also sometimes called a UUID for Universal Unique Identifier. The Unity Editor maintains an Asset Database that assigns a GUID to every asset in the project and uses it to reference assets in scenes, prefabs, etc. Usually, the Asset Database and corresponding GUIDs are only available in the Editor, but we will store those ids to make them always available. Incidentally, you may notice that the Asset Database and GUID system sounds similar to what we’re building, and you’re right. We’re essentially re-implementing this functionality at runtime.

Here’s the `SerializableScriptableObject`

class.

```
using UnityEngine;
#if UNITY_EDITOR
using UnityEditor;
#endif
public class SerializableScriptableObject : ScriptableObject
{
[SerializeField] Guid _guid;
public Guid Guid => _guid;
#if UNITY_EDITOR
void OnValidate()
{
var path = AssetDatabase.GetAssetPath(this);
_guid = new Guid(AssetDatabase.AssetPathToGUID(path));
}
#endif
}
```


If you’re not familiar, the Editor calls `OnValidate`

whenever a value changes in the Inspector or when recompiles your scripts. So this is the perfect opportunity to save the GUID from the Asset Database. I’m sure you’re curious about the `Guid`

type, so let’s do that next.

## GUID Type

When it comes to storing the GUID, there’s an easy way and a hard way. The easy way is to store a string that represents the GUID. That looks like this.

```
[System.Serializable]
public struct Guid
{
public string guid;
}
```


You could simplify it further by removing it altogether and just using a string field. Unfortunately, there are performance repercussions. Comparing two strings is relatively slow, and manipulating strings leads to memory allocations. That said, I’ve done it this way in production code, and it’s usually acceptable. If you want to do it the “right” way (just kidding, there is no **right** way, only the way that best suits your needs), then you need to store the GUID as four `uints`

. That version looks like this.

```
using System;
using System.IO;
using UnityEngine;
[Serializable]
public struct Guid : IEquatable<Guid>
{
[SerializeField, HideInInspector] uint m_Value0;
[SerializeField, HideInInspector] uint m_Value1;
[SerializeField, HideInInspector] uint m_Value2;
[SerializeField, HideInInspector] uint m_Value3;
public uint Value0 => m_Value0;
public uint Value1 => m_Value1;
public uint Value2 => m_Value2;
public uint Value3 => m_Value3;
public Guid(uint val0, uint val1, uint val2, uint val3)
{
m_Value0 = val0;
m_Value1 = val1;
m_Value2 = val2;
m_Value3 = val3;
}
public Guid(string hexString)
{
m_Value0 = 0U;
m_Value1 = 0U;
m_Value2 = 0U;
m_Value3 = 0U;
TryParse(hexString, out this);
}
public string ToHexString()
{
return $"{m_Value0:X8}{m_Value1:X8}{m_Value2:X8}{m_Value3:X8}";
}
static void TryParse(string hexString, out Guid guid)
{
guid.m_Value0 = Convert.ToUInt32(hexString.Substring(0, 8), 16);
guid.m_Value1 = Convert.ToUInt32(hexString.Substring(8, 8), 16);
guid.m_Value2 = Convert.ToUInt32(hexString.Substring(16, 8), 16);
guid.m_Value3 = Convert.ToUInt32(hexString.Substring(24, 8), 16);
}
public static bool operator ==(Guid x, Guid y) => x.m_Value0 == y.m_Value0 && x.m_Value1 == y.m_Value1 && x.m_Value2 == y.m_Value2 && x.m_Value3 == y.m_Value3;
public static bool operator !=(Guid x, Guid y) => !(x == y);
public bool Equals(Guid other) => this == other;
public override bool Equals(object obj) => obj != null && obj is Guid && Equals((Guid) obj);
public override int GetHashCode() => (((int) m_Value0 * 397 ^ (int) m_Value1) * 397 ^ (int) m_Value2) * 397 ^ (int) m_Value3;
}
#region BinaryReader and BinaryWriter Extensions
public static class BinaryReaderExtensions
{
public static Guid ReadGuid(this BinaryReader reader)
{
return new Guid(reader.ReadUInt32(), reader.ReadUInt32(), reader.ReadUInt32(), reader.ReadUInt32());
}
}
public static class BinaryWriterExtensions
{
public static void Write(this BinaryWriter writer, Guid guid)
{
writer.Write(guid.Value0);
writer.Write(guid.Value1);
writer.Write(guid.Value2);
writer.Write(guid.Value3);
}
}
#endregion
```


With this, we can convert from a string representation to four `uints`

and back. Converting back and forth is essential because the Asset Database API feeds us the id as a string. There are also extensions to BinaryReader and BinaryWriter to support serialization through those APIs. Using JSON serialization through `JsonUtility`

works by default because the `uint`

fields are serializable.

We could stop there, but wouldn’t it be nice to prevent users from modifying the GUID in the Inspector? We’ll do that and display the id as the original hex string simultaneously using a custom `PropertyDrawer`

.

## GUID Property Drawer

Property drawers are a mechanism to control how a given type displays in the Inspector. We’ll use it to display the GUID as a label rather than a list of editable numbers. Create a new file, `GuidDrawer.cs`

, inside any folder called Editor and add this code.

```
using UnityEditor;
using UnityEngine;
[CustomPropertyDrawer(typeof(Guid))]
public class GuidDrawer : PropertyDrawer
{
public override void OnGUI(Rect position, SerializedProperty property, GUIContent label)
{
EditorGUI.BeginProperty(position, label, property);
var value0 = property.FindPropertyRelative("m_Value0");
var value1 = property.FindPropertyRelative("m_Value1");
var value2 = property.FindPropertyRelative("m_Value2");
var value3 = property.FindPropertyRelative("m_Value3");
position = EditorGUI.PrefixLabel(position, GUIUtility.GetControlID(FocusType.Passive), label);
EditorGUI.SelectableLabel(position,
$"{(uint) value0.intValue:X8}
{(uint) value1.intValue:X8}
{(uint) value2.intValue:X8}
{(uint) value3.intValue:X8}");
EditorGUI.EndProperty();
}
}
```


The attribute `CustomPropertyDrawer`

specifies which property types to override. In our case, the type is `Guid`

. Then, override `OnGUI`

, and magically every time the Inspector encounters a `Guid`

it’ll run this `OnGUI`

method.

The `SerializedProperty`

is a generic class that wraps the associated property, our `Guid`

. Working with Serialized Properties is a bit cumbersome, but that’s life. We usually use `FindPropertyRelative`

to find each field by its name, but we can make it a bit safer through the power of `nameof`

. With `nameof`

we can store the names of fields to constants, which means if the names get refactored, our code won’t break (thanks for the tip Aiden). Let me show you what I mean. Add these fields to the `Guid`

type.

```
public struct Guid : IEquatable<Guid>
{
#if UNITY_EDITOR
```** public const string VALUE0_FIELDNAME = nameof(m_Value0);
public const string VALUE1_FIELDNAME = nameof(m_Value1);
public const string VALUE2_FIELDNAME = nameof(m_Value2);
public const string VALUE3_FIELDNAME = nameof(m_Value3);**
#endif
.
.
.


Here, we’re using `nameof`

to store the name of the value fields in a string. Now modify the property drawer to use these strings instead.

```
public override void OnGUI(Rect position, SerializedProperty property, GUIContent label)
{
EditorGUI.BeginProperty(position, label, property);
var value0 = property.FindPropertyRelative(
```**Guid.VALUE0_FIELDNAME**);
var value1 = property.FindPropertyRelative(**Guid.VALUE1_FIELDNAME**);
var value2 = property.FindPropertyRelative(**Guid.VALUE2_FIELDNAME**);
var value3 = property.FindPropertyRelative(**Guid.VALUE3_FIELDNAME**);
.
.
.


Now that we’re ready to serialize some Scriptable Objects let’s build our Asset Registry.

## The Registry Type

Fortunately, the Registry type is relatively simple. It’s a Scriptable Object with a List of `SerializableScriptableObjects`

.

```
using System.Collections.Generic;
using UnityEngine;
public abstract class Registry<T> : ScriptableObject where T : SerializableScriptableObject
{
[SerializeField] protected List<T> _descriptors = new List<T>();
public T FindByGuid(Guid guid)
{
foreach (var desc in _descriptors)
{
if (desc.Guid == guid)
{
return desc;
}
}
return null;
}
}
```


There’s not much else to say here, so let’s put it all into practice.

## Putting it together with Entities

Everything beyond this point is project-specific, but I’ll demonstrate how everything connects with an example. Let’s say we have an `Entity`

component attached to all the dynamic objects in our game. To save and load entities, we need an `EntityDescriptor`

and an `EntityRegistry`

. The Descriptor has an id and references a prefab. The Registry holds a list of Descriptors. Here’s the associated code.

```
//EntityRegistry.cs
using UnityEngine;
[CreateAssetMenu]
public class EntityRegistry : Registry<EntityDescriptor>
{
}
```


```
//EntityDescriptor.cs
using UnityEngine;
[CreateAssetMenu]
public class EntityDescriptor : SerializableScriptableObject
{
public Entity EntityPrefab;
}
```


```
//Entity.cs
using UnityEngine;
public class Entity : MonoBehaviour
{
public EntityDescriptor Descriptor;
}
```


As you can see, there’s very little code because the base classes contain all the complexity. Now you can create a Registry and Descriptors for each of your prefabs from the Assets > Create menu. By the way, adding the `CreateAssetMenu`

attribute to a ScriptableObject type automatically adds a menu item to create the stated object in the Create menu.

I used a simplified version of the `SaveManager`

from the previous article to create a little test scene, which you can find in the GitHub repository linked at the end. This scene contains a bunch of entities spread around. On save, I grab all the entities in the scene and save their `Guid`

and position to a binary file on disk. Then on load, I read all the ids and positions from the file, look up each prefab in the Registry and instantiate the associated prefab at its saved position.

## Exciting Opportunities

So before I wrap up, I wanted to mention a few uses for this pattern. The most obvious, of course, is to save the state of the dynamic objects in your scene, as I showed in the example. In the past, I’ve also used this pattern to create a level editor tool. At their core, these two things are essentially the same. A level editor is a tool to spawn prefabs, manipulate them, and store them to disk.

Another less obvious use is to store ability loadouts to use in an RPG, for example. Scriptable objects can contain code as well as data. Let’s say we define a `SerializableScriptableObject`

type to represent an ability like this:

```
public abstract class Ability : SerializableScriptableObject
{
public abstract void Execute();
}
```


Now we can subclass this to create new abilities that contain all the necessary code and data. As a result, we can save a character’s ability loadout as a list of ids that link back to their corresponding Scriptable Object.

Ok, I’m almost done, but here’s one last tip before I go—this one is for those of you who are using the Addressables system. It’s not apparent, but you can load addressable assets by their GUID as well as their address. It’s so unclear that I’m worried this functionality may disappear one day, but it works for now. What this means is if you’re using Addressables, you can forego the `Registry`

entirely and use `Addressables.LoadAssetAsync()`

to load your assets. What’s more, since you’re loading by GUID instead of a string address, you can freely reorganize your project’s folder structure without your asset addresses going stale.

Ok, I’ve prattled on long enough; I’m outta here.

**Explore the example project ****here on Github****. If you like my work, ****join my mailing list**** to be notified when I write a new post.**

## Aj

I believe the capitalization for Guid is wrong in the following line:

`public override bool Equals(object obj) => obj != null && obj is GUID && Equals((GUID) obj);`

Shouldn’t it be `Guid` for both references?

## bronson

Good catch! I must’ve confused it with the

`UnityEditor.GUID`

type when I wrote this## Andreman

Those two functions dont work right in pair. First one generates string with spaces while second one assumpses absence of this spaces. Thanks for article actually

public string ToHexString()

{ return $”{m_Value0:X8} {m_Value1:X8} {m_Value2:X8} {m_Value3:X8}”; }

static void TryParse(string hexString, out Guid guid)

{

guid.m_Value0 = Convert.ToUInt32(hexString.Substring(0, 8), 16);

guid.m_Value1 = Convert.ToUInt32(hexString.Substring(8, 8), 16);

guid.m_Value2 = Convert.ToUInt32(hexString.Substring(16, 8), 16);

guid.m_Value3 = Convert.ToUInt32(hexString.Substring(24, 8), 16);

}

## bronson

Thanks for letting me know! I’ll take a look and fix it :D. I think the spaces must’ve been an accident.

## Fahr

Why did you prefer to rewrite the GUID class instead of using System.GUID?

## bronson

I believe it’s because System.GUID doesn’t automatically serialize. Also, it may not be equatable to Unity’s built-in GUID type? Another potential reason is because I prefer to have some buffer between my code and the code that I don’t control (in this case System.GUID), which makes it easy to adapt my code to changes if necessary. It’s been a long time since I wrote my GUID class so it’s hard to remember exactly.