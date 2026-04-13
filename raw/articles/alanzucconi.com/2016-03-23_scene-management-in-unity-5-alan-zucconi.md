---
title: Scene Management in Unity 5 - Alan Zucconi
url: https://www.alanzucconi.com/2016/03/23/scene-management-unity-5/
author: Alan Zucconi
published: '2016-03-23'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This tutorial shows how the manage scenes and levels in Unity 5.3, with the introduction of `UnityEngine.SceneManagement`

.

[Introduction](https://www.alanzucconi.com#introduction)- Part 1.
[What’s new in Unity 5.3](https://www.alanzucconi.com#part1) - Part 2.
[Accessing the SceneManager class](https://www.alanzucconi.com#part2) - Part 3.
[Retrieving the current scene](https://www.alanzucconi.com#part3) - Part 4.
[Loading a single scene](https://www.alanzucconi.com#part4) - Part 5.
[Reloading a scene](https://www.alanzucconi.com#part5) - Part 6.
[Issues](https://www.alanzucconi.com#part6) [Conclusion](https://www.alanzucconi.com#conclusion)

It took Unity more than 5 versions, but it seems that finally it’s converging towards a uniform and sensible set of APIs to manage scenes. In its initial version, Unity scenes were referred in the code as *levels*. It came pretty quickly the realisation that scenes do not necessarily define “different” levels; this forced the introduction of the term “scene” directly into the API. From a logical point of view, levels are addressed with their build number (the order in which they are included into the *Build Settings*); scenes are referred with the name of the asset that contains them. Neither of those, however, are reliable unique identifiers for a scene. Moving scenes in the Build Settings shifts all of their indices. Similarly, you can have two scenes with the same name, stored in two different folders. All of these aspects have fuelled a lot of confusion, which Unity 5.3 is trying to end.

Unity 5.2 allowed scenes to be referred with either their *build index* or their *asset name*. In Unity 5.3 there is an additional way, which is the `Scene`

struct ([documentation](http://docs.unity3d.com/ScriptReference/SceneManagement.Scene.html)). It’s a wrapper for common methods and variables such as `buildIndex`

, `name`

and `path`

.

In order to use these features of Unity 5.3, you need to include in your C# files this package `SceneManagement`

:

using UnityEngine.SceneManagement;

This gives access to the `SceneManager`

class ([documentation](http://docs.unity3d.com/ScriptReference/SceneManagement.SceneManager.html)), which replaces the obsolete functionalities of `Application`

.

One of the main reasons why Unity changed its naming convention from “level” to “scenes” is mainly because you can load multiple scenes at the same time. This breaks the concept of “current level”, which has been replaced with “active scene”. In the vast majority of cases, the active scene is the last one that has been loaded. You can query it at any given time using `GetActiveScene`

:

// 5.3 Scene scene = SceneManager.GetActiveScene(); Debug.Log(scene.name); Debug.Log(scene.buildIndex); // 5.2 Debug.Log(Application.loadedLevelName); Debug.Log(Application.loadedLevel);

You can test against a specific scene simply by using:

if (SceneManager.GetActiveScene().name == "sceneName") { // ... }

Alternatively you can use the `==`

operator to compare two scenes:

if (SceneManager.GetActiveScene() == scene) { // ... }

Unity has overridden the behaviour of `==`

so that it works as expected.

Like in Unity 5.2, scenes can be loaded using their build index or their name.

// 5.3 SceneManager.LoadScene(4) SceneManager.LoadScene("scene4") SceneManager.LoadScene("path/to/scene/file/scene4") // 5.2 Application.LoadLevel(4); Application.LoadLevel("scene4");

Weirdly, the new `LoadScene`

doesn’t accept `Scene`

structs. When a new scene in loaded with this method, the previous one is unloaded (all its objects destroyed). The game will freeze for a little bit while the new scene is being loaded and activated.

There is no single function to reload the current scene. The best way you can do is to get the build index of the current scene, and pass it to `LoadScene`

:

SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex); // 5.3 Application.LoadLevel(Application.loadedLevelName); // 5.2

This only works as intended if you have a single active scenes. If you have loaded multiple scenes, this will only reload the last active one.

### ⭐ Recommended Unity Assets

**Ghost scenes.**Every time you load a new level with`SceneManager.LoadScene`

, Unity flushes all the scenes that have been previously loaded. Only game objects that invoked`DontDestroyOnLoad`

([documentation](http://docs.unity3d.com/ScriptReference/Object.DontDestroyOnLoad.html)) survive the process. This means that you can potentially use`LoadScene`

, yet having all the previous scenes still loaded. Despite this, Unity will fail to realise that those scenes are actually still alive.**Scene struct.**The`Scene`

struct does not update itself. If something in the scene has changed, its`isDirty`

flag won’t suddenly become`true`

. If you want to query the state of the scene, you should not store the structure; use`GetActiveScene`

instead.

This tutorial shows some of the features introduced by Unity 5.3 to manage scenes. All the changes that Unity is making to its engine are bringing closer to a more clean and reliable flow to handle the dynamic loading of content. There are few aspects, however, that are still quite messy. And is unlikely Unity is going to get rid of them any time soon.

**The next part of this tutorial will explore how to load scenes asynchronously, implementing a loading bar.**

#### Other resources

- Part 1.
**Scene Management in Unity 5** - Part 2.
[Implementing a Loading Bar in Unity 5](https://www.alanzucconi.com/2016/03/30/loading-bar-in-unity/) - Part 3. Seamless Scene Loading in Unity

## Leave a Reply Cancel reply