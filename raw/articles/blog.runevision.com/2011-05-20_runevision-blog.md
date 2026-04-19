---
title: runevision blog
url: https://blog.runevision.com/2011_05_20_archive.html
published: '2011-05-20'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

I found a pleasant solution to a problem I had in Unity that I thought I'd share. This post is technical in nature and won't be of interest to people who don't use [Unity](http://unity3d.com/).

In my [procedural game](http://blog.runevision.com/search/label/TheCluster) I'm doing a lot of lengthy calculations and I've been looking into doing them in a separate thread in order to easily spread out the calculations over multiple frames. Using co-routines for this was getting overly convoluted, with yield statements and [StartCoroutine()](http://unity3d.com/support/documentation/ScriptReference/MonoBehaviour.StartCoroutine.html) calls sprinkled all over the code-base.

Threading is supported in Unity using the normal .Net (or more specifically Mono) [APIs for threading](http://msdn.microsoft.com/en-us/library/aa645740%28VS.71%29.aspx). However, the Unity API can't be touched in anything else than the main thread, or errors will occur. Luckily the lengthy calculations are mostly self-contained and are not touching the Unity API.

However, the calculations do use some data structures that are stored in the form of [ScriptableObject](http://unity3d.com/support/documentation/ScriptReference/ScriptableObject.html). Using ScriptableObject is the simplest way to store some data in Unity with automatically handled serialization. Also see [Bas' explanation here](http://bassmit.info/?p=68).

The problem?

- Querying the name of a ScriptableObject can't be done outside of the main thread.
- Doing equality comparisons between ScriptableObjects can't be done outside of the main thread. This includes checking if a ScriptableObject is null.

These are things I can't avoid in my code. So instead I came up with this derived class that I now use for all my ScriptableObject needs:

```
using UnityEngine;
public class ThreadFriendlyScriptableObject : ScriptableObject {
// Hide the name property with a public variable of the same name.
// (Also hide this in the Inspector.)
[HideInInspector]
public new string name;
// Set it to be the same as the property was.
// (OnEnable will be called from the main thread so it's ok here.)
void OnEnable () {
name = base.name;
}
// Override equality operators to avoid calls into
// the Unity API when doing comparisons.
public static bool operator == (
ThreadFriendlyScriptableObject a,
ThreadFriendlyScriptableObject b
) {
return object.ReferenceEquals (a, b);
}
public static bool operator != (
ThreadFriendlyScriptableObject a,
ThreadFriendlyScriptableObject b
) {
return !object.ReferenceEquals (a, b);
}
public override bool Equals (System.Object other) {
return object.ReferenceEquals (this, other);
}
// We get a compile warning if we don't override this one too
public override int GetHashCode () {
return base.GetHashCode ();
}
}
```


Everything works great for me using this class. There's a few limitations of course:

- You won't be able to access or modify the actual name of the ScriptableObject. This is not a problem unless you need the name to change.
- You won't get Unity's nice behavior of making a reference to an Object look like it's null if the Object was destroyed. This is only a problem if you plan on destroying the ScriptableObjects at runtime. Since the main function of ScriptableObjects is to be persistent assets, you're not likely to want or need this.

Use at your own risk. :)