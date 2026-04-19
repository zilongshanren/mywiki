---
title: runevision blog
url: https://blog.runevision.com/2011/05/
published: '2011-05-29'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

*This post is about The Cluster, my 2.5D platform game under development with focus on non-linear exploration, set in a big, continuous world. You can read all the posts about The Cluster here.*

Last time I posted an update about The Cluster was - 10 months ago!? Well, development hasn't been idle though - far from it! - it's just that I've been working on some refactoring and changes that ended up being rather time-consuming. Some big hurdles are now over and blog updates should hopefully be more regular going forward.

One of the most recent features I've implemented is handling of smoothing and texturing of edges. This has been on my todo-list since forever but I had to switch to a better way of generating meshes before this became feasible.

Consider a generated environment with surfaces that meet each other in sharp edges:

![](../../assets/21b2e05645caeb78.png)


![](../../assets/21b2e05645caeb78.png)

The surfaces look weightless like they're made out of cardboard. No offense to MineCraft, but it's not the look I'm going for. Let's smooth those edges a bit.

![](../../assets/7f413e010d02c024.png)


![](../../assets/7f413e010d02c024.png)

Better. The environment now has a certain weight to it; it feels more solid. But the abrupt edges between surfaces with different textures still makes it seem artificial and less believable (believable not in the sense of realism as I'm not going for that, but in the sense of suspension of disbelief). Let's cover up those abrupt changes in texture.

![](../../assets/7c37bca03e6572cb.png)


![](../../assets/7c37bca03e6572cb.png)

Ahh! With the edges of the textures covered up with natural-looking transitions, the world has finally come alive and is more inviting than ever.

A few more examples of the current look of The Cluster (don't mind those ugly green box stepping platforms and spikes. They're placeholders I haven't yet replaced with something better):

![](../../assets/6d97cd5323332ce4.png)


![](../../assets/6d97cd5323332ce4.png)

![](../../assets/029065542fa6ce15.png)


![](../../assets/029065542fa6ce15.png)

![](../../assets/5fbb18aeb0499a06.png)


![](../../assets/5fbb18aeb0499a06.png)

Most of the textures are made with good old [POV-Ray](http://povray.org/) by the way; the raytracer [I used to work a lot with](http://runevision.com/3d/) back in the days.

The environment is controlled by a neat system of specifying block types, face types, and edge types. Each "cell" in the world (think big voxel) is of a specific block type, for example "Bricks" or "Empty". The procedural generation algorithm fills in the block types of all cells in a generated area prior to constructing the mesh.

A block types specifies the face types it has. For example, this is the data for the Bricks block type (here called EnvironmentData but I should rename that):

![](../../assets/4f9a6c8bf8a61719.png)

All faces here uses the BrickWall face type, except the Up face which uses the Grass face type. Here's the data for the Grass face type:

![](../../assets/a6dea3255a757c53.png)

The face type specifies the material to use for the face surface, as well as edge data for convex, flat, and concave edges. The edge data is used to specify rounding size for an edge as well as the material, width, and UV data for the textured strip that is generated over the edge.

This is an example of an edge texture (diffuse channel):

![](../../assets/88f374eb7c0f6405.png)

This one is of course extremely wasteful, but the system is already set up so multiple edges can be contained in one material; I just need to change my texture so they actually make use of that.

Currently it's not possible to differentiate the different edges of a face but I'll need to add support for that so different edge data can be used for edges that are "along U" and "along V".

When generating geometry an edge is of course shared between two faces. The priority value of an edge is used to settle which of the two faces get to use their edge data for the edge.

When I had to set up the relationships between block types, face types and edge types, that was the first time the data got too unwieldy for me to hard-code directly in the code. Instead I turned to Unity's ScriptableObject, as I wrote a short post about [here](http://blog.runevision.com/2011/05/unitys-scriptableobject-and-threading.html). Using the ScriptableObject means that Unity's Inspector can be used to specify the data, and Unity's serialization system automatically takes care of everything related to storing and loading the data. At some point I'll probably write some custom editor GUI for the data too so it becomes easier to comprehend and get an overview over.

And that's all I have to say about edges!

![](../../assets/1c18d37be6fc82b8.png)


![](../../assets/1c18d37be6fc82b8.png)


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