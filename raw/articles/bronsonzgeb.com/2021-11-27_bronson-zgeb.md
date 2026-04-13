---
title: Bronson Zgeb
url: https://bronsonzgeb.com/index.php/2021/11/27/better-collider-generation-with-asset-processors/
author: Bronson
published: '2021-11-27'
source_blog: Bronson Zgeb
source_site: https://bronsonzgeb.com
category: game programming
fetched: '2026-04-13'
---

# Build a better collider importer with Asset Processors

![Simplified Collision Worm](../../assets/8f6cdae18b39798a.png)

This post will show how to automate your asset integration workflow in Unity using Asset Processors. We’ll build a tool based on the design of Unreal Engine’s static mesh importer that creates colliders automatically in Unity.

## What are Asset Processors?

Asset Processors are Unity Editor scripts that run when assets get imported into your project. Asset processors automate your import pipeline and guarantee correct import settings for your project. Doing so simplifies your asset integration by removing any manual labour in the process.

Let’s build an Asset Processor that automatically creates colliders on imported models to demonstrate. This processor allows developers to specify simplified collision geometry on their models, which is more valuable than the default `Generate Colliders`

import setting. We’ll check each model’s hierarchy for objects that match a specific naming scheme. Once detected, we’ll use the name to determine what type of collider to generate. Then, we’ll attach that collider to its parent game object and remove the unused game object. I’m essentially going to replicate Unreal Editor’s static FBX importer.

## Creating an Asset Processor

To start an asset processor, create a new script in your project inside a folder called Editor. Scripts inside of folders called Editor are compiled into their own assembly and excluded from builds. This is necessary because references to Editor APIs will prevent your project from building. Once you create the script, modify the class to inherit from `AssetPostprocessor`

.

Behold the most basic Asset Processor.

```
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
public class GenerateColliderPostProcessor : AssetPostprocessor
{
}
```


This simple processor has no functionality; it merely exists in your project.

Before we continue, I’d like to mention one tip. In production, it’s a good idea to compile asset processors into a DLL Before we continue, I’d like to mention one tip. In production, it’s a good idea to compile asset processors into a DLL and drop that in your project. The reason is that any compiler error could prevent your processor from recompiling. At that time, any imported assets will skip your processor, and you won’t be certain if they are imported correctly for your project’s needs. By precompiling the DLL, you’ll guarantee that your asset processors will always run.

Like `MonoBehaviour`

, `AssetPostprocessor`

has methods to hook into different parts of the asset pipeline. [The scripting reference](https://docs.unity3d.com/ScriptReference/AssetPostprocessor.html) lists all the available methods. For our purposes, we’ll use `OnPostprocessModel`

because *“This lets you modify the imported Game Object, Meshes, AnimationClips referenced by it.”* We intend to modify Game Objects by adding colliders, so this method is the logical place to do it.

```
public class GenerateColliderPostProcessor : AssetPostprocessor
{
```** void OnPostprocessModel(GameObject g)
{
}**
}


The `OnPostprocessModel`

callback receives a single `GameObject`

as an argument. This `GameObject`

is the root of the hierarchy, so we’ll recursively traverse through its children to search for collision geometry. If you don’t know, there’s a shorthand to iterate through a transform’s children by using a `foreach`

loop on said transform.

```
public class GenerateColliderPostProcessor : AssetPostprocessor
{
void OnPostprocessModel(GameObject g)
{
```** foreach (Transform child in g.transform)
{
GenerateCollider(child);
}**
}
}


## Checking for our naming convention

Our naming convention mimics the one used by Unreal Engine 4’s static mesh importer.

- UBX is a box collider
- UCP is a capsule collider
- USP is a sphere collider
- UCX is a convex mesh collider
- UMC is a mesh collider

Let’s write a method to check an object for our naming convention. We don’t know if the user will name the mesh itself or the object that holds the mesh. So, let’s cover both possibilities. Given an object and a string to look for, we’ll check if it has a mesh whose name meets our criteria. If not, we’ll check if the object’s name meets our criteria and return the result.

```
bool DetectNamingConvention(Transform t, string convention)
{
bool result = false;
if (t.gameObject.TryGetComponent(out MeshFilter meshFilter))
{
var lowercaseMeshName = meshFilter.sharedMesh.name.ToLower();
result = lowercaseMeshName.StartsWith($"{convention}_");
}
if (!result)
{
var lowercaseName = t.name.ToLower();
result = lowercaseName.StartsWith($"{convention}_");
}
return result;
}
```


You may be wondering why we check a prefix rather than a postfix. The reason is Blender (and likely other DCCs) prefix objects with duplicate names a number, such as `Cube`

, `Cube.001`

, etc. As a result, it’s easier to guarantee that a prefix is correct on export rather than a postfix.

Great! Let’s immediately put it to use in the `GenerateCollider`

method.

```
void GenerateCollider(Transform t)
{
```** if (DetectNamingConvention(t, "ubx"))
{
//Add a box collider
}**
}


The next step is adding colliders.

## Adding Colliders

As it turns out, correctly adding colliders is trickier than I thought. That said, let’s start with the naive approach and go from there.

By default, the shape and size of the collision mesh determines the shape and size of the collider. That is, the collider automatically expands to wrap the bounds of the target object. In our case, since we use a separate collision object, we’ll take advantage of this automatic behaviour by adding the collider to the collision object and copying it to its parent. Let’s write a method to do that.

```
T AddCollider<T>(Transform t) where T : Collider
{
T collider = t.gameObject.AddComponent<T>();
T parentCollider = t.parent.gameObject.AddComponent<T>();
EditorUtility.CopySerialized(collider, parentCollider);
return parentCollider;
}
```


We add a collider to the collision object to start, then add the same type of collider to its parent. Then, copy the serialized values from the first collider to the second one using `CopySerialized`

. This method will transfer any exposed properties, such as `size`

and `center`

, from the first collider to the second.

By the way, I’m using a Generic Method here, as denoted by `<T>`

. If you aren’t familiar with Generics, it’s a way to write a single method that operates on multiple data types. In this case, T can be any type that derives from `Collider`

. When we call the method, we’ll provide the type like so:

- `AddCollider<BoxCollider>(transform);`
- `AddCollider<SphereCollider>(transform);`
- `AddCollider<CapsuleCollider>(transform);`
- etc…

Then assume that the type provided inside the `<>`

brackets replaces every instance of `T`

inside the method.

At this point, it’s tempting to assume we completed the add collider method. Unfortunately, it’s more complicated than that. The current method works if the parent object and the collision object have the same origin. However, if the collision object moves, we must apply its transformation to the collider’s offset. To put it another way, if the local transform of the collision object isn’t in the correct location when fully reset to zero, we take that transform and apply it to the `center`

property of the collider.

If that’s not complicated enough for you, there’s one final caveat. Not every collider type has a `center`

property, so we need to check if the property exists before we apply the transform. There are multiple ways to do this, but I opted to use Unity’s `SerializedObject`

API. This API lets us generically modify objects without knowing their type.

Ok, back to the code.

```
T AddCollider<T>(Transform t) where T : Collider
{
T collider = t.gameObject.AddComponent<T>();
T parentCollider = t.parent.gameObject.AddComponent<T>();
EditorUtility.CopySerialized(collider, parentCollider);
```** SerializedObject parentColliderSo = new SerializedObject(parentCollider);
var parentCenterProperty = parentColliderSo.FindProperty("m_Center");
if (parentCenterProperty != null)
{
SerializedObject colliderSo = new SerializedObject(collider);
var colliderCenter = colliderSo.FindProperty("m_Center");
var worldSpaceColliderCenter = t.TransformPoint(colliderCenter.vector3Value);
parentCenterProperty.vector3Value = t.parent.InverseTransformPoint(worldSpaceColliderCenter);
parentColliderSo.ApplyModifiedPropertiesWithoutUndo();
}**
return parentCollider;
}


In this new version, we check if the collider has the property `m_Center`

. Why `m_Center`

instead of `center`

? Because that’s the serialized name of the property. How do I know that? The easiest way is to use `SerializedObject.GetIterator`

to go through all the serialized properties and find the one you’re seeking.

Moving on, if the object has the `m_Center`

property, convert it from the collision object’s local space to a world space position. Then, convert it from world space to the parent object’s local space and apply the modified property.

Now let’s deal with Mesh Colliders, which don’t have an `m_Center`

property.

## Transforming Mesh Colliders

Mesh Colliders don’t use a center property. Instead, the mesh uses the transform it’s attached to as its origin. Unfortunately, we need to offset the mesh by the collision object’s transform when attached to the parent object. So, we’ll iterate through each vertex in the mesh and convert it from the collision object’s local space to the parent object’s local space, effectively changing the mesh’s origin from one transform to another. If that explanation was confusing, hopefully, the code will make it more obvious.

**void TransformSharedMesh(MeshFilter meshFilter)
{
if (meshFilter == null)
return;
var transform = meshFilter.transform;
var mesh = meshFilter.sharedMesh;
var vertices = mesh.vertices;
for (int i = 0; i < vertices.Length; ++i)
{
vertices[i] = transform.TransformPoint(vertices[i]);
vertices[i] = transform.parent.InverseTransformPoint(vertices[i]);
}
mesh.SetVertices(vertices);
}**


We perform the same operation we did on the `m_Center`

, but for each vertex. That is, iterate through each vertex, convert it to world space, then convert it from world space to the target object’s local space.

Now with all our utilities out of the way, let’s put it all together.

## Meanwhile, back in Generate Collider

Back in `GenerateCollider`

, we can add our various collider types.

```
void GenerateCollider(Transform t)
{
```** if (DetectNamingConvention(t, "ubx"))
{
AddCollider<BoxCollider>(t);
}
else if (DetectNamingConvention(t, "ucp"))
{
AddCollider<CapsuleCollider>(t);
}
else if (DetectNamingConvention(t, "usp"))
{
AddCollider<SphereCollider>(t);
}
else if (DetectNamingConvention(t, "ucx"))
{
TransformSharedMesh(t.GetComponent<MeshFilter>());
var collider = AddCollider<MeshCollider>(t);
collider.convex = true;
}
else if (DetectNamingConvention(t, "umc"))
{
TransformSharedMesh(t.GetComponent<MeshFilter>());
AddCollider<MeshCollider>(t);
}**
}


We’re nearing the finish line. Currently, our `GenerateCollider`

method is called only on the direct children of the newly imported object root. We need to run it against every object in the new hierarchy (except the root). So we’ll add a line block to traverse the hierarchy recursively, calling `GenerateCollider`

on each transform.

```
void GenerateCollider(Transform t)
{
```** foreach (Transform child in t.transform)
{
GenerateCollider(child);
}**
if (DetectNamingConvention(t, "ubx"))
{
AddCollider<BoxCollider>(t);
}
else if (DetectNamingConvention(t, "ucp"))
{
AddCollider<CapsuleCollider>(t);
}
else if (DetectNamingConvention(t, "usp"))
{
AddCollider<SphereCollider>(t);
}
else if (DetectNamingConvention(t, "ucx"))
{
TransformSharedMesh(t.GetComponent<MeshFilter>());
var collider = AddCollider<MeshCollider>(t);
collider.convex = true;
}
else if (DetectNamingConvention(t, "umc"))
{
TransformSharedMesh(t.GetComponent<MeshFilter>());
AddCollider<MeshCollider>(t);
}
}


Finally, we no longer need the original collision objects after transferring all the colliders to their parent objects. So let’s destroy them! If we re-arrange the hierarchy by destroying objects while traversing it, we’ll cause an error. So instead, we’ll keep a list of all the collision objects and destroy them at the end.

`void GenerateCollider(Transform t, `**List<Transform> transformsToDestroy**)
{
foreach (Transform child in t.transform)
{
GenerateCollider(child, transformsToDestroy);
}
if (DetectNamingConvention(t, "ubx"))
{
AddCollider<BoxCollider>(t);
**transformsToDestroy.Add(t);**
}
else if (DetectNamingConvention(t, "ucp"))
{
AddCollider<CapsuleCollider>(t);
**transformsToDestroy.Add(t);**
}
else if (DetectNamingConvention(t, "usp"))
{
AddCollider<SphereCollider>(t);
**transformsToDestroy.Add(t);**
}
else if (DetectNamingConvention(t, "ucx"))
{
TransformSharedMesh(t.GetComponent<MeshFilter>());
var collider = AddCollider<MeshCollider>(t);
collider.convex = true;
**transformsToDestroy.Add(t);**
}
else if (DetectNamingConvention(t, "umc"))
{
TransformSharedMesh(t.GetComponent<MeshFilter>());
AddCollider<MeshCollider>(t);
**transformsToDestroy.Add(t);**
}
}


Then, let’s destroy them at the end of `OnPostprocessModel`

.

```
void OnPostprocessModel(GameObject g)
{
```**List<Transform> transformsToDestroy = new List<Transform>();**
//Skip the root
foreach (Transform child in g.transform)
{
GenerateCollider(child, **transformsToDestroy**);
}
** for (int i = transformsToDestroy.Count - 1; i >= 0; --i)
{
if (transformsToDestroy[i] != null)
{
GameObject.DestroyImmediate(transformsToDestroy[i].gameObject);
}
}**
}


With that we’re all done! Here’s the entire asset processor.

```
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
public class GenerateColliderPostProcessor : AssetPostprocessor
{
```**[MenuItem("Tools/Better Collider Generation")]
static void ToggleColliderGeneration()
{
var betterColliderGenerationEnabled = EditorPrefs.GetBool("BetterColliderGeneration", false);
EditorPrefs.SetBool("BetterColliderGeneration", !betterColliderGenerationEnabled);
}
[MenuItem("Tools/Better Collider Generation", true)]
static bool ValidateToggleColliderGeneration()
{
var betterColliderGenerationEnabled = EditorPrefs.GetBool("BetterColliderGeneration", false);
Menu.SetChecked("Tools/Better Collider Generation", betterColliderGenerationEnabled);
return true;
}**
void OnPostprocessModel(GameObject g)
{
**if (!EditorPrefs.GetBool("BetterColliderGeneration", false))
return;**
List<Transform> transformsToDestroy = new List<Transform>();
//Skip the root
foreach (Transform child in g.transform)
{
GenerateCollider(child, transformsToDestroy);
}
for (int i = transformsToDestroy.Count - 1; i >= 0; --i)
{
if (transformsToDestroy[i] != null)
{
GameObject.DestroyImmediate(transformsToDestroy[i].gameObject);
}
}
}
bool DetectNamingConvention(Transform t, string convention)
{
bool result = false;
if (t.gameObject.TryGetComponent(out MeshFilter meshFilter))
{
var lowercaseMeshName = meshFilter.sharedMesh.name.ToLower();
result = lowercaseMeshName.StartsWith($"{convention}_");
}
if (!result)
{
var lowercaseName = t.name.ToLower();
result = lowercaseName.StartsWith($"{convention}_");
}
return result;
}
void GenerateCollider(Transform t, List<Transform> transformsToDestroy)
{
foreach (Transform child in t.transform)
{
GenerateCollider(child, transformsToDestroy);
}
if (DetectNamingConvention(t, "ubx"))
{
AddCollider<BoxCollider>(t);
transformsToDestroy.Add(t);
}
else if (DetectNamingConvention(t, "ucp"))
{
AddCollider<CapsuleCollider>(t);
transformsToDestroy.Add(t);
}
else if (DetectNamingConvention(t, "usp"))
{
AddCollider<SphereCollider>(t);
transformsToDestroy.Add(t);
}
else if (DetectNamingConvention(t, "ucx"))
{
TransformSharedMesh(t.GetComponent<MeshFilter>());
var collider = AddCollider<MeshCollider>(t);
collider.convex = true;
transformsToDestroy.Add(t);
}
else if (DetectNamingConvention(t, "umc"))
{
TransformSharedMesh(t.GetComponent<MeshFilter>());
AddCollider<MeshCollider>(t);
transformsToDestroy.Add(t);
}
}
void TransformSharedMesh(MeshFilter meshFilter)
{
if (meshFilter == null)
return;
var transform = meshFilter.transform;
var mesh = meshFilter.sharedMesh;
var vertices = mesh.vertices;
for (int i = 0; i < vertices.Length; ++i)
{
vertices[i] = transform.TransformPoint(vertices[i]);
vertices[i] = transform.parent.InverseTransformPoint(vertices[i]);
}
mesh.SetVertices(vertices);
}
T AddCollider<T>(Transform t) where T : Collider
{
T collider = t.gameObject.AddComponent<T>();
T parentCollider = t.parent.gameObject.AddComponent<T>();
EditorUtility.CopySerialized(collider, parentCollider);
SerializedObject parentColliderSo = new SerializedObject(parentCollider);
var parentCenterProperty = parentColliderSo.FindProperty("m_Center");
if (parentCenterProperty != null)
{
SerializedObject colliderSo = new SerializedObject(collider);
var colliderCenter = colliderSo.FindProperty("m_Center");
var worldSpaceColliderCenter = t.TransformPoint(colliderCenter.vector3Value);
parentCenterProperty.vector3Value = t.parent.InverseTransformPoint(worldSpaceColliderCenter);
parentColliderSo.ApplyModifiedPropertiesWithoutUndo();
}
return parentCollider;
}
}


You’ll notice I also added a `MenuItem`

to toggle the processor on and off. You may want to force it on in production, but toggling it on and off could help debug any issues. It’s also helpful to know how to write this sort of `MenuItem`

, so I thought it was worth adding.

**Check out the example project ****on GitHub****. Would you mind joining**** my mailing list**** to support my work? If you do, I’ll notify you whenever I write a new post.**

## Ozkan Sune

What do “ubx”, “ucb”… and other shotcuts mean?

## bronson

Oh no I completely forgot to explain didn’t I? I’ll edit the post to explain. But in short: UBX is Box Collider, UCP is Capsule Collider, USP is Sphere Collider, UCX is convex mesh collider, UMC is mesh collider. It’s based on Unreal’s documentation so you can easily use the same assets between both engines.

## Ozkan Sune

Thanks, yo do great!

## bronson

Thank you! That’s very kind 😀

## David Simon

Could you make a Tutorial about voxel, how to convert asset/Scenes into voxel. I dont mean like the voxelizer, but in a way, voxel destruction would be possable.

## bronson

I could try!

## Brian

This is awesome and a *huge* time-saver, thanks so much for putting this together and sharing it!!

## bronson

You’re welcome! I’m glad it was helpful! 😀

## Cisco

I’m leaning SO. MUCH. FROM. THIS. Thanks Bronson!

## bronson

You’re welcome!! 😀