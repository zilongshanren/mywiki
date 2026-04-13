---
title: Bronson Zgeb
url: https://bronsonzgeb.com/index.php/2021/09/17/the-type-object-pattern-with-scriptable-objects/
author: Bronson
published: '2021-09-17'
source_blog: Bronson Zgeb
source_site: https://bronsonzgeb.com
category: game programming
fetched: '2026-04-13'
---

# The Type Object pattern with Scriptable Objects

![](../../assets/d0cbf332974942a6.png)

This article will demonstrate how to implement the Type Object pattern in Unity using Scriptable Objects.

## What problem does Type Object solve?

There’s plenty of literature on the subject, but I’ll briefly explain the origins of this pattern. Let’s put Unity aside for a moment. Imagine you had to define a bunch of different buildings for your city builder game. In classical OOP style, you maybe be tempted to start with a base `Building`

class. Then, you’d subclass `Building`

for each new type and adjust the building cost, sell price, income generated, etc. Now you have a bunch of subclasses with nothing but a few variables changed here and there. Plus, you have to recompile your code every time you add a new building or change the cost of an existing building. Using subclasses to define types is both a hassle and inflexible.

Now back to Unity. In Unity, it’s unlikely you’d take this approach at all. Instead, you’d define some building component and attach that to a prefab. Then for every new type, you’d create either a new prefab or prefab variant. So, Unity has already helped us turn our code into data in the form of prefab files. Great! Turning code into data is the aim of the Type Object pattern. Rather than creating a `Type`

to represent variants of a class, we create a single `Type`

that holds all the variable data. Then we make new types through data rather than through code.

So if Unity already solved the problem, what’s the point of this article? Well, I’m here to offer a different approach. You’ll still use prefab variants, but Scriptable Objects provide further benefits on top of the variant system.

## Scriptable Objects as Type Objects

We’ll create a bunch of monsters and experience the Scriptable Object advantage first-hand. Let’s jump right in with some code.

```
using UnityEngine;
public class Monster : MonoBehaviour
{
public int Health;
public int Speed;
public int Attack;
}
```


Behold the classic monster. Admittedly it’s a simple example, but it’s enough for demonstration purposes. Here, our monster has three stats: Health, Speed, and Attack. As I mentioned before, generally, in Unity, you would attach this component to a prefab and modify the stats on each variant to define new monsters. This is a good approach, but when we throw a Scriptable Object into the mix, we gain several advantages for minimal cost.

Let’s quickly build something to provide some context. Create a new Type Object that derives from Scriptable Object with our base values.

```
using UnityEngine;
[CreateAssetMenu]
public class MonsterType : ScriptableObject
{
public int StartingHealth;
public int BaseSpeed;
public int BaseAttack;
}
```


Now, modify the Monster class to hold a reference to the Type Object.

```
using UnityEngine;
public class Monster : MonoBehaviour
{
public int Health;
public int Speed;
public int Attack;
public MonsterType Type;
void Start()
{
Health = Type.StartingHealth;
Speed = Type.BaseSpeed;
Attack = Type.BaseAttack;
}
}
```


Then, in the `Start`

method, copy the base values from the `MonsterType`

into this instance of a monster. By the way, this is a crucial step because any modifications to Scriptable Objects will affect all the objects referencing it. Not to mention, those modifications persist in and out of play mode. So if you change these base values while your game is running, you’ll lose your carefully balanced stats.

## Scriptable Objects, Prefabs and Version Control

When it comes to version control, merging complex assets is a pain. It’s common to run into a situation where a designer must balance stat values across several creatures in a game. At the same time, artists may iterate on the visuals while gameplay developers attach new components. If multiple developers make simultaneous changes to the same prefab, it’s unlikely that those changes will merge cleanly. In this case, someone will have to redo work. What if we could split these tasks into separate assets, eliminating merge conflicts? That’s where Scriptable Objects come in.

When the stats live inside a Scriptable Object, designers can change them without touching the prefab file at all. As a result, the only merge conflicts that arise come from two designers tweaking the same value. What’s more, when conflicts occur, they’re easier to solve because Scriptable Object files are more readable. For comparison, here’s a simple prefab:

```
%YAML 1.1
%TAG !u! tag:unity3d.com,2011:
--- !u!1 &7398429376191695866
GameObject:
m_ObjectHideFlags: 0
m_CorrespondingSourceObject: {fileID: 0}
m_PrefabInstance: {fileID: 0}
m_PrefabAsset: {fileID: 0}
serializedVersion: 6
m_Component:
- component: {fileID: 7398429376191695864}
- component: {fileID: 7398429376191695867}
- component: {fileID: 397173726}
- component: {fileID: 397173725}
m_Layer: 0
m_Name: MonsterBase
m_TagString: Untagged
m_Icon: {fileID: 0}
m_NavMeshLayer: 0
m_StaticEditorFlags: 0
m_IsActive: 1
--- !u!4 &7398429376191695864
Transform:
m_ObjectHideFlags: 0
m_CorrespondingSourceObject: {fileID: 0}
m_PrefabInstance: {fileID: 0}
m_PrefabAsset: {fileID: 0}
m_GameObject: {fileID: 7398429376191695866}
m_LocalRotation: {x: 0, y: 0, z: 0, w: 1}
m_LocalPosition: {x: 0, y: 0, z: 0}
m_LocalScale: {x: 1, y: 1, z: 1}
m_Children: []
m_Father: {fileID: 0}
m_RootOrder: 0
m_LocalEulerAnglesHint: {x: 0, y: 0, z: 0}
--- !u!114 &7398429376191695867
MonoBehaviour:
m_ObjectHideFlags: 0
m_CorrespondingSourceObject: {fileID: 0}
m_PrefabInstance: {fileID: 0}
m_PrefabAsset: {fileID: 0}
m_GameObject: {fileID: 7398429376191695866}
m_Enabled: 1
m_EditorHideFlags: 0
m_Script: {fileID: 11500000, guid: 491079bd7ae064bad94668c7539cf90f, type: 3}
m_Name:
m_EditorClassIdentifier:
Type: {fileID: 0}
--- !u!33 &397173726
MeshFilter:
m_ObjectHideFlags: 0
m_CorrespondingSourceObject: {fileID: 0}
m_PrefabInstance: {fileID: 0}
m_PrefabAsset: {fileID: 0}
m_GameObject: {fileID: 7398429376191695866}
m_Mesh: {fileID: 10208, guid: 0000000000000000e000000000000000, type: 0}
--- !u!23 &397173725
MeshRenderer:
m_ObjectHideFlags: 0
m_CorrespondingSourceObject: {fileID: 0}
m_PrefabInstance: {fileID: 0}
m_PrefabAsset: {fileID: 0}
m_GameObject: {fileID: 7398429376191695866}
m_Enabled: 1
m_CastShadows: 1
m_ReceiveShadows: 1
m_DynamicOccludee: 1
m_StaticShadowCaster: 0
m_MotionVectors: 1
m_LightProbeUsage: 1
m_ReflectionProbeUsage: 1
m_RayTracingMode: 2
m_RayTraceProcedural: 0
m_RenderingLayerMask: 1
m_RendererPriority: 0
m_Materials:
- {fileID: 10302, guid: 0000000000000000f000000000000000, type: 0}
m_StaticBatchInfo:
firstSubMesh: 0
subMeshCount: 0
m_StaticBatchRoot: {fileID: 0}
m_ProbeAnchor: {fileID: 0}
m_LightProbeVolumeOverride: {fileID: 0}
m_ScaleInLightmap: 1
m_ReceiveGI: 1
m_PreserveUVs: 0
m_IgnoreNormalsForChartDetection: 0
m_ImportantGI: 0
m_StitchLightmapSeams: 1
m_SelectedEditorRenderState: 3
m_MinimumChartSize: 4
m_AutoUVMaxDistance: 0.5
m_AutoUVMaxAngle: 89
m_LightmapParameters: {fileID: 0}
m_SortingLayerID: 0
m_SortingLayer: 0
m_SortingOrder: 0
m_AdditionalVertexStreams: {fileID: 0}
```


And a simple Scriptable Object:

```
%YAML 1.1
%TAG !u! tag:unity3d.com,2011:
--- !u!114 &11400000
MonoBehaviour:
m_ObjectHideFlags: 0
m_CorrespondingSourceObject: {fileID: 0}
m_PrefabInstance: {fileID: 0}
m_PrefabAsset: {fileID: 0}
m_GameObject: {fileID: 0}
m_Enabled: 1
m_EditorHideFlags: 0
m_Script: {fileID: 11500000, guid: cad5330d2463d44e68a65aa0c805c193, type: 3}
m_Name: Cat
m_EditorClassIdentifier:
```**StartingHealth**: 20
**BaseSpeed**: 20
**BaseAttack**: 20


The Scriptable Object is *almost* human-readable. Plus, the stats `StartingHealth`

, `BaseSpeed`

, and `BaseAttack`

*are* readable, which are the values most likely to change.

Next, let’s explore the power of Scriptable Object as references.

## Scriptable Object References

I had a hard time titling this section, but bear with me for a minute, and you’ll see where I’m going with this. One of the main advantages of Scriptable Objects is that they are first-class citizens in the Unity editor. What does that mean? Scriptable Objects automatically work with all the editor systems. They serialize and deserialize easily. The Inspector recognizes them as referenceable objects. They simply work. Now, this is pretty awesome, but it’s only part of the story. Multiple objects can reference a single Scriptable Object through dragging and dropping in the Inspector. Plus, it’s easy to test if two references are pointing at the same thing. Why do we care? Let’s find out.

Let’s say our monsters have weaknesses to other monsters. By referencing `MonsterType`

directly, designers can define weaknesses by dragging and dropping Scriptable Objects in the Inspector.

Let me show you what I mean. Add a `MonsterType`

array called `Weaknesses`

.

```
using UnityEngine;
[CreateAssetMenu]
public class MonsterType : ScriptableObject
{
public int StartingHealth;
public int BaseSpeed;
public int BaseAttack;
```**public MonsterType[] Weaknesses;**
}


This field will appear in the Inspector as a list of `MonsterType`

elements. You can freely modify a monster’s `Weaknesses`

as you wish.

![](../../assets/c241de9ba6b022ec.png)

But how do you know if a monster is weak to another monster? Let’s add a helper to the `Monster`

class.

```
using UnityEngine;
public class Monster : MonoBehaviour
{
public int Health;
public int Speed;
public int Attack;
public MonsterType Type;
void Start()
{
Health = Type.StartingHealth;
Speed = Type.BaseSpeed;
Attack = Type.BaseAttack;
}
```** public bool IsWeakAgainst(MonsterType type)
{**
** foreach (var weakness in Type.Weaknesses)
{
if (type == weakness)
return true;
}
return false;
}**
}


Since `MonsterType`

is a reference, we check if a given `type`

is `==`

to any elements in the `Weaknesses`

array. If yes, we know both variables are pointing to the same Scriptable Object, and consequently, it’s part of the monster’s weaknesses. Isn’t that neat?

You could extend this as well. What if you had two nearly identical monsters, but one of them was fiery? Create a new `Element`

type and add it to `MonsterType`

with an accompanying `ElementalWeaknesses`

array. Then you can check if a given monster is weak against a certain element too.

Using Scriptable Objects makes it straightforward to compose new variants through data by dragging items around the editor, which is the purpose of the Type Object pattern.

## Wrap-Up

I want to extend this example further by adding abilities to the monsters with Scriptable Objects. However, that’s veering away from the Type Object pattern and into the Command pattern. So, I’ll save that for a future post!

**Dive into the example Github project ****here****. To learn more about the Type Object pattern, check out ****this chapter**** from Game Programming Patterns. If my work is helpful, show your support and ****join my mailing list****. If you do, I’ll notify you whenever I write a new post.**

## koken

Great article, thank you for your time 🙂

## bronson

Thanks for saying that! I’m happy to help! 😀

## Sergey

Thank you

## bronson

You’re welcome!

## Manuel

Nice one, thanks for sharing.

## bronson

You’re welcome! I hope it helps!