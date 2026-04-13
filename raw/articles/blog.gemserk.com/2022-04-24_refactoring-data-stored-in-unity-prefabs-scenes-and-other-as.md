---
title: Refactoring Data stored in Unity Prefabs, Scenes and other Assets
url: https://blog.gemserk.com/2022/04/24/refactoring-prefabs-and-unity-objects/
published: '2022-04-24'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

Using Unity, most of the Data will be serialized inside Prefabs, Scenes (inside MonoBehaviour serialized fields) and other Assets. In our case we also use data only [Prefabs and GameObjects](https://blog.gemserk.com/2020/05/26/using-unity-prefabs-and-gameobjects-only-for-data/).

Refactoring Code is a common and recommended good practice and there are tools to help in that task. For example, Rider IDE provides a great with C# code refactors and also by adjusting Unity assets and metadata (like when you change a MonoBehaviour’s class name).

However, there are no tools in Unity (that I know) to Refactor Data in terms of data structure changes even though it is common in software development. When we say data structure, we include stuff like: renaming fields, changing field types, moving fields from component to component, moving components from object to object, etc.

In the case of Prefabs and Scenes data is stored in class Component and MonoBehaviour is the most common Component. In this blog post, we treat both terms like synonymous (even though we know they are not).

Our use case is when we want to store data in a different (hopefully better) way when there is already a lot of created content (prefabs, scenes, etc). Even if we want to manually do that, it is not easy to know, in terms of GameObjects and Scenes, where the data is used.

Luckily for us, Unity provides API that includes exploring Prefabs (open them in edit mode, check if they are variants), Scenes (load/unload scenes) and Assets and that can be used for our refactors.

By the way, I’ve created a Github Project named [unity-refactory-tools](https://github.com/acoppes/unity-refactoring-tools) with the code used in this blog post and also some examples to see the refactor running, if you are interested, feel free to download and try it.

Normally [the steps] for data refactoring are these:

- Add new redundant data structure and/or types.
- Run Automated Refactor to transform from previous data structure to new one.
- Manually change code to use new data structure.
- Remove old data structure and values and reserialize to remove unused serialized data.

We are only covering the second step in the blog post.

A pseudo code for the automated Refactor would be something like this:

```
find prefabs with the data to be modified
iterate in non variant prefabs
update data
save
iterate in prefab variants
if data was overwritten in variant
update data
save
iterate in all scenes
get objects with data
if object is not prefab instance
update data
mark scene modified
else
if data was overwritten in instance
update data
mark scene modified
if scene modified
save scene
```


In practice, our current code looks like this:

```
public static void RefactorMonoBehaviour<T>(bool includeScenes, Func<GameObject, bool> callback) where T : Component
{
var guids = AssetDatabase.FindAssets($"t:prefab", null);
var prefabs = guids.Select(g => AssetDatabase.LoadAssetAtPath<GameObject>(
AssetDatabase.GUIDToAssetPath(g))).ToList();
// Ignore prefabs without component T
prefabs = prefabs.Where(p => p.GetComponentInChildren<T>(true) != null).ToList();
// We sort by no variant prefabs first
prefabs.Sort(delegate(GameObject a, GameObject b)
{
var aIsVariant = PrefabUtility.IsPartOfVariantPrefab(a);
var bIsVariant = PrefabUtility.IsPartOfVariantPrefab(b);
if (!aIsVariant && bIsVariant)
return -1;
if (aIsVariant && !bIsVariant)
return 1;
// if both no variants or both variants, we just use the name to compare just to be consistent.
return a.name.CompareTo(b.name);
});
prefabs.ForEach(delegate(GameObject o)
{
Debug.Log(o.name);
});
try
{
var total = prefabs.Count;
EditorUtility.DisplayProgressBar($"Refactoring {total} prefabs with {typeof(T).Name}", "Start", 0);
for (var i = 0; i < prefabs.Count; i++)
{
var prefab = prefabs[i];
EditorUtility.DisplayProgressBar($"Refactoring {prefabs.Count} assets of type {typeof(T).Name}",
prefab.name,
i / (float)total);
var contents = PrefabUtility.LoadPrefabContents(AssetDatabase.GetAssetPath(prefab));
var result = callback(contents);
// Just to break the loop if something is wrong...
if (!result)
{
PrefabUtility.UnloadPrefabContents(contents);
break;
}
PrefabUtility.SaveAsPrefabAsset(contents, AssetDatabase.GetAssetPath(prefab));
PrefabUtility.UnloadPrefabContents(contents);
}
}
finally
{
EditorUtility.ClearProgressBar();
}
// Then iterate in all scenes (if include scenes is true)
if (!includeScenes)
return;
var allScenesGuids = new List<string>();
// Here we filter by all assets of type scene but under Assets folder to avoid all other scenes from
// external packages.
allScenesGuids.AddRange(AssetDatabase.FindAssets("t:scene", new []
{
"Assets"
}));
EditorUtility.DisplayProgressBar($"Refactoring {allScenesGuids.Count} scenes", "Starting...", 0);
var allScenesCount = allScenesGuids.Count;
for (var i = 0; i < allScenesCount; i++)
{
var sceneGuid = allScenesGuids[i];
var scenePath = AssetDatabase.GUIDToAssetPath(sceneGuid);
try
{
EditorUtility.DisplayProgressBar($"Refactoring {allScenesGuids.Count} scenes", scenePath,
i / (float) allScenesCount);
var scene = SceneManagement.EditorSceneManager.OpenScene(scenePath,
SceneManagement.OpenSceneMode.Single);
var componentsList = new List<T>();
// We can iterate over root objects and collect stuff to run the refactor over
var rootObjects = scene.GetRootGameObjects();
for (var j = 0; j < rootObjects.Length; j++)
{
var go = rootObjects[j];
var components = go.GetComponentsInChildren<T>(true);
componentsList.AddRange(components.ToList());
}
var modified = false;
foreach (var component in componentsList)
{
var result = callback(component.gameObject);
if (result)
{
modified = true;
EditorUtility.SetDirty(component);
}
}
if (modified)
{
SceneManagement.EditorSceneManager.MarkSceneDirty(scene);
SceneManagement.EditorSceneManager.SaveScene(scene);
}
}
finally
{
EditorUtility.ClearProgressBar();
}
}
}
```


### Change field type

Change a field from one type to another. For example, change to store multiple fields (normally related) into a struct.

```
[Serializable]
public struct Speed
{
public float baseValue;
public float incrementValue;
}
public class CustomBehaviour : MonoBehaviour
{
// Redundant code here
public float speedBaseValue;
public float speedIncrementValue;
public Speed speed;
}
[MenuItem("Refactors/Refactor Custom MonoBehaviour")]
public static void Refactor2()
{
RefactorTools.RefactorMonoBehaviour<CustomBehaviour>(true, delegate(GameObject gameObject)
{
var behaviours = gameObject.GetComponentsInChildren<CustomBehaviour>();
foreach (var behaviour in behaviours)
{
behaviour.speed = new Speed
{
baseValue = behaviour.speedBaseValue,
incrementValue = behaviour.speedIncrementValue
};
}
return true;
});
}
```


We used this kind of refactor a lot and also the case of changing from bool fields to enum type to store multiple values.

This could also be used to transform data for game design, like, we were storing half the speed for some enemies, so update all enemies with some criteria to double the stored speed.

### Move Component to Parent

Restructure the hierarchy of a GameObject by moving a Component to its parent object.

```
// here we have a simple component, stored in child object
public class ComponentA : MonoBehaviour
{
public int someValue;
}
// The refactor would be something like this
[MenuItem("Refactors/Refactor ComponentA to Parent")]
public static void Refactor3()
{
RefactorTools.RefactorMonoBehaviour<ComponentA>(true, delegate(GameObject gameObject)
{
if (gameObject.transform.parent == null)
return false;
var parentGameObject = gameObject.transform.parent.gameObject;
var parentComponentA = parentGameObject.GetComponent<ComponentA>();
if (parentComponentA == null)
{
parentComponentA = parentGameObject.AddComponent<ComponentA>();
}
var componentA = gameObject.GetComponent<ComponentA>();
var json = JsonUtility.ToJson(componentA);
JsonUtility.FromJsonOverwrite(json, parentComponentA);
Object.DestroyImmediate(componentA);
return true;
});
}
```


There is no Editor Utility, that I know of, to move a Component from one object to another so we are using JSON serialization in this case (we could’ve use SerializedObject too).

I’m not sure if this covers all the fields properly but I suppose it does for all serializable stuff. There could be another approach using reflection.

If you happen to know how to use internal Unity’s API to do move Components, I would be glad to know it.

*Note: if you run this refactor script multiple times, it will keep moving up in the hierarchy. We could add other considerations, like being root or being a leaf.*

### Move Component to Children

Restructure the hierarchy of a GameObject by moving a Component down.

```
public class ComponentB : MonoBehaviour
{
public int anotherValue;
}
[MenuItem("Refactors/Refactor ComponentB to first children")]
public static void Refactor4()
{
RefactorTools.RefactorMonoBehaviour<ComponentB>(true, delegate(GameObject gameObject)
{
// will ignore this case
if ("Child_WithComponentB".Equals(gameObject.name))
return false;
GameObject childObject;
if (gameObject.transform.childCount == 0)
{
childObject = new GameObject("Child_WithComponentB");
childObject.transform.SetParent(gameObject.transform);
}
else
{
childObject = gameObject.transform.GetChild(0).gameObject;
}
var childComponentB = childObject.GetComponent<ComponentB>();
if (childComponentB == null)
{
childComponentB = childObject.AddComponent<ComponentB>();
}
var componentB = gameObject.GetComponent<ComponentB>();
var json = JsonUtility.ToJson(componentB);
JsonUtility.FromJsonOverwrite(json, childComponentB);
Object.DestroyImmediate(componentB);
return true;
});
}
```


*Note: if you run the refactor script multiple times, it will keep moving it down in the hierarchy. We could add other considerations, like being root or being a leaf.*

### Considering references when refactoring

Now, what happens when, for example, that `ComponentB`

is being referenced by a `ComponentC`

:

```
public class ComponentC : MonoBehaviour
{
public ComponentB referenceToB;
}
```


In those cases, what we normally do is to manually fix that reference inside the refactor script:

```
...
var componentC = gameObject.GetComponent<ComponentC>();
if (componentC.referenceToB == componentB)
{
componentC.referenceToB = childComponentB;
}
...
```


Obviously, we are only covering the case where ComponentC is used in the exactly same GameObject. If we want to do more, we could start expanding the refactor script to consider more cases but it will be still manual work, we don’t have an automatic way to cover all cases (yet).

### Remove unused MonoBehaviour class

When a MonoBehaviour class is removed from the code, all assets (prefabs and scene’s objects) using that MonoBehaviour will have a missing script. If you do that without previously taking care, it is a bit complicated to fix since you can’t identify the reference anymore.

A good practice we follow is to previously run a refactor script to remove the MonoBehaviour and only after that remove it from code.

```
[MenuItem("Refactors/Refactor Custom MonoBehaviour")]
public static void RefactorCustomMonoBehaviour()
{
RefactorTools.RefactorMonoBehaviour<CustomBehaviour>(true, delegate(GameObject gameObject)
{
var behaviours = gameObject.GetComponentsInChildren<CustomBehaviour>();
foreach (var behaviour in behaviours)
{
Object.DestroyImmediate(behaviour);
}
return true;
});
}
```


There is the special case where a GameObject only had that MonoBehaviour and there might be a good idea to remove the GameObject as well if it is empty (no children and no references to it from elsewhere).

### Refactoring Data stored in Assets

Refactoring assets is easier than Prefabs but still we have to follow the same [steps](https://blog.gemserk.com#refactor_steps) in order to conclude the refactor.

A pseudo code for the refactor is something like this:

```
find assets of type T
for asset in assets
update asset data
save asset
```


Here is a template code to use:

```
public static void RefactorAsset<T>(Func<T, bool> callback) where T : UnityEngine.Object
{
var guids = AssetDatabase.FindAssets($"t:{typeof(T)}", null);
var assets = guids.Select(g => AssetDatabase.LoadAssetAtPath<T>(
AssetDatabase.GUIDToAssetPath(g))).ToList();
try
{
var total = assets.Count;
EditorUtility.DisplayProgressBar($"Refactoring {total} assets of type {typeof(T).Name}", "Start", 0);
for (var i = 0; i < assets.Count; i++)
{
var asset = assets[i];
EditorUtility.DisplayProgressBar($"Refactoring {assets.Count} assets of type {typeof(T).Name}",
asset.name,
i / (float)total);
var result = callback(asset);
if (result)
{
EditorUtility.SetDirty(asset);
}
}
AssetDatabase.SaveAssets();
}
finally
{
EditorUtility.ClearProgressBar();
}
}
```


*Note: a recommendation here is to use my AssetDatabaseExt gist to simplify data refactors.*

An example usage:

```
[MenuItem("Refactors/Refactor Custom Data")]
public static void RefactorCustomData()
{
RefactorTools.RefactorAsset(delegate(CustomDataAsset asset)
{
asset.newValue = $"VALUE:{asset.previousValue}";
return true;
});
}
```


### Finally

This approach proved to be very helpful in our games and allowed us to improve our Data Structure while the game content was growing and since we started early on, we trained ourselves to consider more edge cases so our refactors became more consistent and solid in time.

One good practice is to run one refactor at a time so you can validate the results are correct and only then apply the next one. Otherwise, you will have a lot of structural changes and it is not going to be clear what was completed correctly and what not.

Another one is to create temporary Prefabs and Scenes with edge cases before running the Refactor to be used to manually validate the results were applied correctly. Not sure if some of this could be automated but it would be great.

Currently, there is no easy way to automatically synchronize Code Refactor with Data Refactor, so some Code Refactor steps must be performed manually during the Data Refactor. I suppose it could be great to have a meta script, like this pseudo code:

```
void MetaRefactorIdea() {
Code.CreateFieldWithNewType();
Unity.CopyDataFromOldFieldToNewOne();
Code.ChangeCodeToReferenceNewField();
Code.RemoveOldField();
}
```


Sometimes, other serialization changes appear for data we didn’t modified. Most of the time this happens when a previous code change wasn’t reserialized yet. What we do in this case is to revert our changes (with version control), then run a reserialization on the assets (or in all assets), then commit those changes to finally run the refactor again.

Our current refactor approach is covering just a thin layer, it is like the “hello world” of refactors and there is a lot of space to cover, for example, using reflection to automatically change references (maybe next time) or automatically exploring other assets like Mechanim Animations to fix structural changes (moved objects, changed field names, etc).

### Future work

I believe there are common Data Refactors that could be reused between projects, for example, Move Component from Object to Object.

As it happens with code too, specific refactors sometimes are needed and cannot be escaped from but improving tools and reusing code can help in having less manual error and cover more edge cases.

Also, would love to continue working on helping those reference cases, there are useful tools like FindReference which help in knowing where an asset is being used, so mixing Data Refactors with that and maybe reflection could be a great way of covering more and more refactoring data space.

Remember there is a Github [unity-refactory-tools](https://github.com/acoppes/unity-refactoring-tools) with the code used here.

As always, thanks for reading and hope this blog post was useful and would be great to hear your opinion on this topic to improve together. See you next time.

If you like it, check my [twitter account](https://twitter.com/arielsan) and retweet, it would be super helpful for me.