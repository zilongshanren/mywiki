---
title: How to Snap to Grid in Unity3D - Alan Zucconi
url: https://www.alanzucconi.com/2015/07/22/how-to-snap-to-grid-in-unity3d/
author: Alan Zucconi
published: '2015-07-22'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

Despite Unity3D being such an advanced framework, I am sometimes puzzled by its lack of basic features. Especially when working with 2D games, the lack of a *proper* snap to grid option is simply crazy. Luckily, Unity3D allows to extend its basic interface to add new behaviours. This post will explain how to add a customisable *snap to grid* option to your objects. Two different implementations are presented; the first one, despite being more complicated, could be used a good starting point to further extend and customise the inspector.

### Step 1: The MonoBehaviour

Broadly speaking, the idea is to create a script which will force the position of the `GameObject`

it’s attached to stick to integer multiples of a certain value. The twist is that we want this script to be executed only in the editor and to not cause any overhead during the execution of the game.

![snap](../../assets/84fc845de21e3703.png)

The first step is to create a `MonoBehaviour`

which is, de facto, doing nothing. It’s purpose is to help us configuring the snap properties for the `GameObject`

it will be attached to.

using UnityEngine; using System.Collections; public class SnapToGrid : MonoBehaviour { #if UNITY_EDITOR public bool snapToGrid = true; public float snapValue = 0.5f; public bool sizeToGrid = false; public float sizeValue = 0.25f; #endif }

As you can notice, this script will be able to snap not just the position, but also the size of its *GameObject*. **Line 5** and **line 11** makes these variables disappearing during the actual compilation of the game. By doing this, any release version will only have an empty script attached, causing little to no overhead.

### Step 2: The Editor script

The SnapToGrid script does nothing. Literally, nothing. The actual code is contained in a script called `SnapToGridEditor`

which has to be contained in a folder called `Editor`

.

using UnityEngine; using UnityEditor; using System.Collections; [InitializeOnLoad] [CustomEditor(typeof(SnapToGrid), true)] [CanEditMultipleObjects] public class SnapToGridEditor : Editor { public override void OnInspectorGUI() { base.OnInspectorGUI(); SnapToGrid actor = target as SnapToGrid; if (actor.snapToGrid) actor.transform.position = RoundTransform (actor.transform.position, actor.snapValue); if (actor.sizeToGrid) actor.transform.localScale = RoundTransform(actor.transform.localScale, actor.sizeValue); } // The snapping code private Vector3 RoundTransform (Vector3 v, float snapValue) { return new Vector3 ( snapValue * Mathf.Round(v.x / snapValue), snapValue * Mathf.Round(v.y / snapValue), v.z ); } }

**Line 6** indicates that `SnapToGridEditor`

should affect all the `MonoBehaviour`

s of `SnapToGrid`

type. Unity will then execute `OnInspectorGUI`

every time the inspector of a `SnapToGrid`

script is selected. **Line 14** is where the `SnapToGrid`

script is accessed. **Lines 23-31** changes a `Vector3`

according to the desired snap value; these scripts are intended for 2D, so that’s why the Z axis is never changed.

### An alternative approach

For something as simple as adding snap to grid behaviour to your `GameObject`

*s*, you could actually implement everything directly in the `Update`

function of `SnapToGrid`

.

using UnityEngine; using System.Collections; // This script is executed in the editor [ExecuteInEditMode] public class SnapToGrid : MonoBehaviour { #if UNITY_EDITOR public bool snapToGrid = true; public float snapValue = 0.5f; public bool sizeToGrid = false; public float sizeValue = 0.25f; // Adjust size and position void Update () { if (snapToGrid) transform.position = RoundTransform (transform.position, snapValue); if (sizeToGrid) transform.localScale = RoundTransform(transform.localScale, sizeValue); } // The snapping code private Vector3 RoundTransform (Vector3 v, float snapValue) { return new Vector3 ( snapValue * Mathf.Round(v.x / snapValue), snapValue * Mathf.Round(v.y / snapValue), v.z ); } #endif }

**Line 5** is necessary, since it will enable the script to be executed in the editor, while the game is not actually running.

### Conclusion

Having scripts and editor scripts is quite a common pattern you’ll see in Unity3D. Such a separation allows also to change the appearance of the editor. This is particularly interesting if you need to add buttons or other custom behaviours to the inspector panel. As it often happens in Unity3D, there isn’t a single way to implement a feature. Another snap to grid script can be found [here](http://wiki.unity3d.com/index.php?title=SnapToGrid). For a guide oriented to Unity2D and snap to pixel, you can consult [this](http://nielson.io/2015/08/the-pixel-grid-better-2d-in-unity-part-1/) link.

## Leave a Reply Cancel reply