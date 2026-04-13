---
title: Implementing a Loading Bar in Unity - Alan Zucconi
url: https://www.alanzucconi.com/2016/03/30/loading-bar-in-unity/
author: Alan Zucconi
published: '2016-03-30'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This tutorial will explain how to create a loading bar in Unity. This is the second part of a longer series on scene management.

[Introduction](https://www.alanzucconi.com#introduction)- Part 1.
[The API](https://www.alanzucconi.com#part1) - Part 2.
[The Code](https://www.alanzucconi.com#part2) - Part 3.
[Issues](https://www.alanzucconi.com#part3) [Conclusion](https://www.alanzucconi.com#conclusion)

Despite Unity’s best effort, implementing a loading bar is all but easy. The reason behind this is that the set of APIs provided heavily relies on assumptions that, at best, are a consequence of poor design choices.

Before digging into them, we need to understand what loading a level actually means for Unity. If you are used to `SceneManager.LoadScene`

(or the now deprecated `Application.LoadLevel`

) you might be unfamiliar with the sequence of operations that Unity performs:

**Loading.**Like the name suggests, in this phase Unity loads from the memory the assets that make the new scene. If your level is rather big or uses large assets, this is the phase that will take most of the time. Unity relies on a background process to load assets minimising the performance drop on the scene that is currently being played.**Activation.**Once all that’s needed for a scene is loaded, Unity has to activate it. This process deletes all the assets that are currently in the game, and replaces them with the ones that have been previously loaded. This operation will always introduce a little bit of a lag, and so far there is very little you can do to prevent that.

The idea behind this tutorial is to delegate the loading of the new scene to Unity’s dedicated background process. We can now periodically query the state of the loading and display it on the screen. When all the assets are loaded, we can finally trigger the activation of the scene.

The function provided by Unity to load a scene in the background is `SceneManager.LoadSceneAsync`

, which returns an instance of `AsyncOperation`

. Asynchronous operations ([documentation](http://docs.unity3d.com/ScriptReference/AsyncOperation.html)) are objects that can be used to query the current state of a background process. It provides three essential components:

`allowSceneActivation`

: when set to`false`

, the scene is not activated when it is fully loaded, giving more control over the entire process;`isDone`

: a boolean value that becomes`true`

when the process is completed;`progress`

: a number from 0 to 1 that indicates the current state of the process.

Except that …is not that simple! Both `isDone`

and `progress`

suffer from heavy assumptions. Firstly, `isDone`

becomes true when the scene is both both loaded and activated. Secondly, the range from 0 to 0.9 of `progress`

is used for the loading part only, while 1 is reserved for the completion of the activation progress. Values from 0.9 to 1 (extremes excluded) are never used.

### ⭐ Recommended Unity Assets

With all the knowledge gathered so far, we can now write a proper asynchronous function to monitor the loading of a scene. Since we are required to update the loading bar in parallel with the loading process, we need to wrap out code into a [coroutine](http://docs.unity3d.com/Manual/Coroutines.html). This is simply a function that returns `IEnumerator`

, and that signals when it can be stopped and resumed using the keyword `yield`

. Coroutines will be explored in a further tutorial.

After invoking `SceneManager.LoadSceneAsync`

, we force `allowSceneActivation`

to false for a better control over the activation process. We then loop over `isDone`

, starting the activation process when the loading is completed (`progress == 0.9f`

):

IEnumerator AsynchronousLoad (string scene) { yield return null; AsyncOperation ao = SceneManager.LoadSceneAsync(scene); ao.allowSceneActivation = false; while (! ao.isDone) { // [0, 0.9] > [0, 1] float progress = Mathf.Clamp01(ao.progress / 0.9f); Debug.log("Loading progress: " + (progress * 100) + "%"); // Loading completed if (ao.progress == 0.9f) { Debug.Log("Press a key to start"); if (Input.AnyKey()) ao.allowSceneActivation = true; } yield return null; } }

This code prints the current progress on the console, but it can be easily changed to update any UI you have designed.

Note: If you are to compare two floating values, it’s better to rely on `Mathf.Approximately`

([documentation](http://docs.unity3d.com/ScriptReference/Mathf.Approximately.html)), rather than `==`

. This is because floating point arithmetic is prone to approximation errors. In this very specific case, however, `progress`

is set to exactly `0.9f`

when the scene is loaded.

The technique explained in this tutorial works very well if you have to load a single scene at a time. There are other hidden assumptions in the Unity APIs which can cause unwanted behaviours.

**Single loading.**You can only load a single scene at a time.**Activation in order.**Scenes must be activated in the same order they have been loaded.**Dangling scenes.**If you lose your reference to`AsyncOperation`

before activating a scene, the entire loading queue will be blocked until you restart Unity.

This post explains how to create a loading bar with Unity.

**The next part of this tutorial will explain how to load scene incrementally. Such a technique is essential if your world is very large and you want to create a seamless experience, free of loading bars.**

#### Other resources

- Part 1.
[Scene Management in Unity 5](https://www.alanzucconi.com/2016/03/23/scene-management-unity-5/) - Part 2.
**Implementing a Loading Bar in Unity** - Part 3. Seamless Scene Loading in Unity

## Leave a Reply Cancel reply