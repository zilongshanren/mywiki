---
title: 'Shader Showcase Saturday #7: Billboard Impostors - Alan Zucconi'
url: https://www.alanzucconi.com/2018/08/25/shader-showcase-saturday-7/
author: Alan Zucconi
published: '2018-08-25'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

Some of the readers might have heard of a game called Duke Nukem 3D. Released in 1996, it was one of the first 3D games I had the chance to play. An interesting feature of that game is that most of the interactive elements (including the enemies) were not *actually* 3D. They were 2D sprites rendered on quads which are always facing the camera (below).

![](../../assets/b02c4c79066c155a.png)


This technique is called **billboarding**, and early 3D games were using it extensively. Even today it is still used for some background details, such as trees in a forest far away. For instance, one of them is [Massive Vegetation](https://www.assetstore.unity3d.com/#!/content/121801?aid=1100l45Ay&pubref=az_sss_07), which uses billboarding to render grass blades in a very realistic way.


Billboarding works really well, but it cannot be used on all objects. It is perfect for objects that look similar from all angles (like tree and grass), but yield poor results for more complex geometry. A solution to this is to rely on **billboard impostors** (sometimes also spelt **imposters**). At the core, billboard impostors are still quads that are always facing the camera. However, the image they show changes based on the viewing angle. This is possible by having a spritesheet containing renderings of how the 3D object looks like when viewed from different angles.

When used properly, billboard impostors are exceptionally effective. The image below shows a mechanical piece seen from many different angles. All those models are impostors, as it can be seen by the fact that they are rendered on 2D quads.

![](../../assets/a49d990d197a9023.png)


The image above comes from [IMP](https://github.com/xraxra/IMP), a billboard impostor baker created by [xra](https://twitter.com/xra), developer of [Memory of a Broken Dimension](http://www.brokendimension.com/). The term **baking** refers to the process of creating the spreadsheet that is used to render the 3D model from different angles.

If the idea of reducing hundreds of thousands of triangles to just a few dozens appeals you, then I strongly advise having a look at [Amplify Impostors [BETA]](https://www.assetstore.unity3d.com/#!/content/119877?aid=1100l45Ay&pubref=az_sss_07). Amplify Creations is well-known for the quality of its assets, and this is not an exception. [Amplify Impostors [BETA]](https://www.assetstore.unity3d.com/#!/content/119877?aid=1100l45Ay&pubref=az_sss_07) is possibly the most advanced asset to bake billboard impostors from your assets, and comes with a large variety of options. Also, it comes with support for both LWRP and HDRP, the new rendering pipelines used by Unity.

If, instead, you are curious to learn more about this technique, this is how impostors are baked. First, many screenshots of the model need to be taken from different angles. The more screenshots, the better the result. Distributing angles correctly is crucial for this process, and is far from being trivial. A common technique is to place the model inside an invisible spherical mesh, then taking a screenshot from each vertex of that sphere. Increasing or decreasing the number of vertices on that sphere has a direct effect on the number of screenshots and, consequently, on the final precision. In the image below (from [Tech Tuesday 11](https://joncioletti.com/tech-tuesday-11)), you can see a tree surrounded by cameras, each placed on the vertex of a **hemi-dodecahedron** (which is half of a regular dodechaedron).

![](../../assets/7204ef6897251169.png)


The results of this effect can be seen in this GIF from Technical Artist [Jonathan Cioletti](https://twitter.com/joncioletti).

It's all coming together! My generated texture atlas is now applied to a camera facing plane and displays the correct vertex render. Next step will be to implement frame blending to reduce choppiness

[https://t.co/Jj7AeKgRLC][#TechTuesday][#madewithunity][pic.twitter.com/Jgy3ZnVQWb]— Jon Cioletti (@JonCioletti)

[August 7, 2018]

While the result is not perfect, it allowed Jon to move from 6004 triangles to just 2. Impostors work very well for distance objects, since they do not deform appropriately based on the field of view.

If you simply swap images from a spritesheet, your object will not react smoothly to camera movements. This is because there are only a finite number of images that can be used. A more advanced approach is to blend the closest three images together, to ensure a smooth transition at any point. This is discussed in great details in [Octahedral Impostors](http://shaderbits.com/blog/octahedral-impostors/), by Principal Technical Artist, at Epic Games [Ryan Brucks](https://twitter.com/shaderbits).

Another great asset that uses a blending technique is [Imposter System](https://www.assetstore.unity3d.com/#!/content/69651?aid=1100l45Ay&pubref=az_sss_07). One of its great advantages is that, compared to many other packages, it works very well in VR. This is not always the case, since rendering the same impostor from two different cameras can result in unpleasant artefacts.

## Leave a Reply Cancel reply