---
title: runevision blog
url: https://blog.runevision.com/2017_01_04_archive.html
published: '2017-01-04'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

I'm currently learning simple 3D modeling so I can make some models for my game. I'm using Blender for modeling.

The models I need to make are fairly simple shapes depicting man-made objects made of stone and metal (though until I get it textured it will look more like plastic). There are a lot of flat surfaces.

The end result I want is these simple shapes with flat surfaces - *and smooth edges*. In the real world, almost no objects have completely sharp edges, and so 3d models without smooth edges tend to look like they're made of paper, like this:

![](../../assets/56624d7575b062f0.png)


![](../../assets/56624d7575b062f0.png)

What I want instead is the same shapes but with smooth edges like this:

![](../../assets/d565e0db012f14ab.png)


![](../../assets/d565e0db012f14ab.png)

Here, some edges are very rounded, while others have just a little bit of smoothness in order to not look like paper. No edges here are actually completely sharp.

![](../../assets/e3ffa79e2fa3587a.png)


![](../../assets/e3ffa79e2fa3587a.png)

The two images above shows the end result I wanted. It turns out it was much harder to get there than I had expected! Here's the journey of how I got there.

How are smooth edges normally obtained? By a variety of methods. The Blender [documentation](https://www.blender.org/manual/modeling/meshes/editing/smoothing.html) page on the subject is a bit confusing, talking about many different things without clear separation and with inconsistent use of images.

#### Edge loops plus subdivision surface modifier

From my research I have gathered that a typical approach is to add *edge loops* near edges that should be smooth, and then use a *Subdivision Surface* modifier on the object. This is also mentioned on the documentation page above. This has several problems.

First of all, subdivision creates a lot of polygons which is not great for game use.

Second, adding edge loops is a manual process, and I'm looking for a fully automatic solution. It's important for me to have quick iteration times. To be able to fundamentally change the shape and then shortly after see the updated end result inside the game. For this reason I strongly prefer a [non-destructive editing](https://en.wikipedia.org/wiki/Non-linear_editing_system) workflow. This means the that the parts that make up the model are kept as separate pieces and not "baked" into one model such that they can no longer be separated or manipulated individually.

Adding edge loops means adding a lot of complexity to the model just for the sake of getting smooth edges, which then makes the shape more cumbersome to make major changes to afterwards. Additionally, edge loops can't be added around edges resulting from procedures such as *boolean subtraction* (carving one object out of another) and similar, at least not without baking/applying the procedure, which is a destructive editing operation.

Edge loops and subdivision is not the way to go then.

#### Bevel modifier

Some posts on the web suggests using a *Bevel* modifier on the object. This modifier can automatically add bevels of a specified thickness for all edges (or selectively if desired). The Bevel modifier in Blender does what I want in the sense that it's fully automatic and creates sensible geometry without superfluous polygons.

![](../../assets/b5e7e82a90f8708c.png)


![](../../assets/b5e7e82a90f8708c.png)

However, by itself the bevel either requires [a lot of segments](http://blender.stackexchange.com/questions/811/most-efficient-way-to-round-edges), which is not efficient for use in games (I'd want one to two segments only to keep the poly count low) or when fewer segments are used it creates a [segmented look](http://blender.stackexchange.com/questions/2534/how-can-i-round-the-edges-of-a-mesh) rather than smooth edges, as it can also be seen below.

![](../../assets/9e02b8c30534f7d1.png)


![](../../assets/9e02b8c30534f7d1.png)

#### Baking high-poly details into normal maps of low-poly object

Another common approach, especially for games, is to create both a high-poly and a low-poly version of the object. The high-poly one can have all the detail you want, so for example a bevel effect with tons of segments. The low-poly one is kept simple but has the appearance from the high-poly one [baked into its normal maps](http://www.chrisalbeluhn.com/Normal_Map_Tutorial.html).

This is of course a proven approach for game use, but it seems overly complicated to me for the simple things I want to achieve. Though I haven't tried it out in practice, I suspect it doesn't play well with a non-destructive workflow, and that it adds a lot of overhead and thus reduces iteration time.

#### Bevel and smooth shading

Going back to the bevel approach, what I really want is the geometry created by the Bevel modifier but with smooth shading. The problem is that smooth shading also makes the original flat surfaces appear curved.

Here is my model with bevel and smooth shading. The edges are smooth sure enough, but all the surfaces that were supposed to be flat are curvy too.

![](../../assets/5adbd397f0a6ce2d.png)


![](../../assets/5adbd397f0a6ce2d.png)

Smooth shading works by pretending the surface at each point is facing in a different direction than it actually does. For a given polygon, the faked direction is defined at each of its corners in the form of a *normal*. A normal is a vector that points out perpendicular to the surface. Only, we can modify normals to point in other directions for our faking purposes.

The way that smooth shading typically calculates normals makes all the surfaces appear curved. (There is typically a way to selectively make some surfaces flat, but then they will have sharp edges too.) The diagram below shows the normals for flat shading, for typical smooth shading, and for a third way that is what I would need for my smooth edges.

![](../../assets/52c6494f10c3c51b.png)


![](../../assets/52c6494f10c3c51b.png)

So how can the third way be achieved? I found a post that asks [the same question](http://blender.stackexchange.com/questions/39674/how-to-keep-flat-faces-flat-when-using-smooth-shading) essentially. The answers there don't really help. One incorrectly concludes that Blender's Auto Smooth feature gives the desired result - it actually doesn't but the lighting in the posted image is too poor to make it obvious. The other is the usual edge loop suggestion.

When I posted question myself requesting clarification on the issue, I was pointed to a Blender add-on called Blend4Web. It has a [Normal Editing feature](https://www.blend4web.com/en/community/article/131/) with a Face button that seems to be able to align the normals in the desired way - however as a manual workflow, not an automated process. I also found [other forum threads](http://polycount.com/discussion/154664/a-short-explanation-about-custom-vertex-normals-tutorial) discussing the technique.

#### Using a better smoothing technique

At this point I got the impression there was no way to get the smooth edges I wanted in an automated way inside of Blender, at least without changing the source code or writing my own add-on. Instead I considered an alternative strategy: Since I ultimately use the models in Unity, maybe I could fix the issue there instead.

In Unity I have no way of knowing which polygons are part of bevels and which ones are part of the original surfaces. But it's possible to take advantage of the fact that bevel polygons are usually much smaller.

There is a common technique called *face weighted normals* / *area weighted normals* ([explained here](http://www.bytehazard.com/articles/vertnorm.html)) for calculating averaged smooth normals which is to weigh the contributing normals according to the surface areas of the faces (polygons) they belong to. This means that the curvature will be distributed mostly on small polygons, while larger polygons will be more flat (but still slightly curved).

From the discussions I've seen, there is general consensus that this usually produces better results than a simple average ([here's one random thread about it](http://polycount.com/discussion/85809/face-weighted-normals)). It sounds like Maya uses this technique by default since at least 2014, but smooth shading in Blender doesn't use it or support it (even though people have discussed it and made custom add-ons for it [back in 2008](https://forum.guildofwriters.org/viewtopic.php?f=59&t=2197)), nor does the model importer in Unity (when it's set to recalculate normals).

#### Custom smoothing in Unity AssetPostprocessor

In Unity it's possible to write *AssetPostprocessors* that can modify imported objects as part of the import process. This can also be used for modifying an imported mesh. I figured I could use this to calculate the smooth normals in an alternative way that produces the results I want.

I started by implementing just area weighted normals. This technique still make the large faces slightly curved. Here is the result.

![](../../assets/d91a654b609fdf2a.png)


![](../../assets/d91a654b609fdf2a.png)

Honestly, the slight curvature on the large faces can be hard to spot here. Still, I figured I could improve upon it.

I also implemented a feature to let weights smaller than a certain threshold be ignored. For each averaged normal, all the contributing normals are collected in a set, and the largest weight is noted. Any weight smaller than a certain percentage of the largest weight can then be ignored and not included in the average. For my geometry, this worked very well and removed the remaining curvature from the large faces. Here is the final result again.

![](../../assets/2003230c57318f88.png)


![](../../assets/2003230c57318f88.png)

The code is available [here as a GitHub Gist](https://gist.github.com/runevision/6fd7cc8d841245a53df5d09ccf6b47ff). Part of the code is derived from [code by Charis Marangos, aka Zoodinger](http://schemingdeveloper.com/2014/10/17/better-method-recalculate-normals-unity/).

#### Future perspectives

The technique of aligning smooth normals on beveled models with the original (pre-bevel) faces seems to be well understood when you dig a bit, but poorly supported in software. I hope Blender and other 3D software one day will have a "smooth" option for their Bevel modifier which retains the outer-most normal undisturbed.

A simpler prospect is adding support for *area weighted normals*. This produces almost as good result for smooth edges, and is a much more widely applicable technique, not specific to bevels or smooth edges at all. That Blender, Unity and other 3D software that support calculating smooth normals do not include this as an option is even more mind-boggling, particularly given how trivial is it to implement. Luckily there workarounds for it in the form of AssetPostprocessors for Unity and custom add-ons for Blender.

If you do 3D modeling, how do you normally handle smooth edges? Are you happy with the workflows? Do some 3D software have great (automatic!) support for it out of the box?