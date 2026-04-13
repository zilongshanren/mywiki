---
title: Using Unity Prefabs and GameObjects only for data.
url: https://blog.gemserk.com/2020/05/26/using-unity-prefabs-and-gameobjects-only-for-data/
published: '2020-05-26'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

# Introduction

[GameObjects](https://docs.unity3d.com/Manual/GameObjects.html) are the main concept of Unity, they are composed by different Components which normally contain both Logic and Data. A GameObject can contain other GameObjects as well in a hierarchical way.

[Prefabs](https://docs.unity3d.com/Manual/Prefabs.html) are GameObjects stored in assets that can be easily reused by instantiating them in scenes during edition time, for example, an enemy spawner in the right corner of the level, or in runtime, for example, the enemies spawned by that spawner.

# Using Prefabs and GameObjects only for Data

When we want to store only data, we normally tend to use [ScriptableObjects](https://docs.unity3d.com/Manual/class-ScriptableObject.html) since it is a more natural way. They are just assets that can store anything serializable by Unity. ScriptableObjects are great and have some advanced usages explained [here](https://www.youtube.com/watch?v=raQ3iHhE_Kk) and [here](https://www.youtube.com/watch?v=6vmRwLYWNRo) but this blog post is not about that.

It is not common, however, to use GameObjects and Prefabs for data only (no logic at all) but that doesn’t mean it is not useful, *au contraire mon ami*, and I will share why.

When using GameObjects and Prefabs with this perspective in mind, it is like using ScriptableObjects but with all these extra features:

- Data Composition by Hierarchical Structure
- Data Composition by Components
- In-Scene Data Customization
- Prefab Variants Data Customization
- Reuse Data with Nested Prefabs
- Prefabs Editor
- GameObjects default Components like Transforms
- Useful API methods

For the rest of the blog post I will refer to those GameObjects as Data GameObjects.

## Data by using GameObject hierarchical structure

As GameObjects can be added one to another in a hierarchical way, we can store different Data together by just adding the corresponding Data GameObject to another.

![](../../assets/3105b86f7bd90c4e.gif)


Given the previous example, we can get data using something like this:

```
public void SomeLogic(GameObject dataObject) {
var health = dataObject.GetComponentInChildren<HealthData>();
// ... do something with the health
}
```


## Data by adding GameObject’s Components

As I said before, GameObjects are composed of a list of Components, we can use that as well to store different Data together by just adding corresponding Components to the Data GameObject we want.

![](../../assets/d1e85a753e0b2eb8.gif)


And with this example, we can do the same:

```
public void SomeLogic(GameObject dataObject) {
var health = dataObject.GetComponent<HealthData>();
// ... do something with the health
}
```


## In-Scene Data Customization

ScriptableObjects can’t be stored in scenes but GameObjects can, and that opens new possibilities to Data customization.

In order to do that, Data GameObject can be created in scenes (or instantiated in the case they are stored in Prefabs) and modified as needed.

![](../../assets/49e35ad8f35ac39b.gif)


## Prefab Variants Data Customization

If using Unity 2018.3 or newer, there is also the [Prefab Variants](https://docs.unity3d.com/Manual/PrefabVariants.html) feature for Data Customization as well, and simplify storing and reusing those modifications.

![](../../assets/c5b5ee1bfe48ff19.gif)


## Reuse Data with Nested Prefabs

[Nested Prefabs](https://docs.unity3d.com/Manual/NestedPrefabs.html) is also one of those new Prefabs features that allow reusing Data composition by adding other Data GameObject Prefabs as children.

![](../../assets/e1d8465789f97ead.gif)


## Prefabs Editor

Now that Prefabs can be edited completely without having to instantiate them, we can take advantage of that too. This is super useful in the case of using the hierarchical Data composition mentioned before.

![](../../assets/81a999eb2762c6c9.png)


## GameObjects default Components like Transforms

GameObjects normally come with a lot of extra burden, like the Transform Component for example, but that’s not always bad. Sometimes it is useful to have positional information in the Data GameObjects by using Transforms, for example, to spawn an enemy in a given offset.

![](../../assets/0664703582cc75cd.gif)


```
public class SpawnerData : MonoBehaviour
{
public Vector2 Offset =>
transform.Find("Offset").localPosition;
}
```


Even though this means extra memory cost compared to using ScriptableObjects, it doesn’t mean extra performance cost since Data GameObjects are not instantiated and have no logic.

## Useful API methods

As we are using GameObjects, we can also take advantage of all its related API methods like GetComponent methods, or checking for a Transform children to be there or not.

```
public void SomeLogic(GameObject dataObject) {
if (dataObject.transform.Find("DoubleDamage") != null) {
// perform double damage
} else {
// perform normal damage
}
}
```


We could even use it to get MonoBehaviours implementing an Interface. Even though that is normally more useful for logic, we could have complex Data that depends on other factors, so it might be interesting to create an Interface and have different implementations to retrieve those values while ensuring readonly usage at the same time.

```
public interface WeaponData {
int Damage { get; }
}
public class BasicWeaponData : MonoBehaviour, WeaponData {
public int damage;
public int Damage => damage;
}
public class AdvancedWeaponData : MonoBehaviour, WeaponData {
public int damage;
public int level = 1;
public int Damage => damage * level;
}
```


In case you are interested, [here is the Github project used for this article](https://github.com/acoppes/DataGameObjectsExample).

## Some drawbacks to have in mind

When using ScriptableObjects, it is super easy to pick a reference in the Editor since it shows only valid assets of that type. In the case of referencing GameObjects the editor will show all possible GameObjects in the scene or Prefabs in the assets database. You can’t even reference to specific Component type since, in that case, the editor shows nothing (unless you select something from the scene) and you’ll have to manually drag and drop the reference from the assets.

One common mistake when working with assets in runtime is to modify their values through code without knowing, and Prefabs are no exception. To mitigate this, we try to treat them as read only as possible. For example, we use them only in creation time or try to return immutable values by using structs or by using an interface like the previous example.

# Conclusion

Using Prefabs and GameObjects for Data proved to be a great tool to easily reuse and customize Data by taking advantage of all of the GameObjects features mentioned before.

Having great Data tools is relevant when developing a game focused on Data that everyone in the team collaborate in building it. It helps when [separating data for different purposes](https://www.gdcvault.com/play/1025284/Tools-Tutorial-Day-A-Tale), for example, the Data edited by Game Designers and the Data optimized for the engine.

I know this blog post was a bit generic but it was to share the general idea behind this and present it in a clean way. Would love to share a more real example of how we are using it for our current game but I can’t.

As always, I hope you liked it, and feel free to comment and share :)