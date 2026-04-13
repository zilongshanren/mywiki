---
title: Alchemy in Photogrammetry
url: https://www.gamedeveloper.com/art/alchemy-in-photogrammetry
author: Joseph Azzam
published: '2017-05-10'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Alchemy in Photogrammetry

I will be turning a European stone statue into a Middle-Eastern rock statue by extracting the textures from 3D scans, manipulating their properties, while creating a game ready asset.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

![](../../assets/ad2175a45d648d37.img)

[article](http://www.gamasutra.com/blogs/JosephAzzam/20160824/278719/The_Workflows_of_Creating_Game_Ready_Textures_and_Assets_using_Photogrammetry.php).

3D scans have more information to work with, which enables us to extract richer textures that we can use to create materials with manipulatable properties, meaning that we can change the look of an object while preserving its feel.

This article will cover the steps of creating a game ready 3D model using a 3D scan to use in a game engine, and while I will be going over some details very swiftly, if you want to get decent results, don’t try to replicate these steps quickly, especially if it’s your first time doing this, give each step the time it needs and understand it very well, even if it takes days, then work on becoming faster at it.

These blog posts are meant to be independent of each other, and therefore if you read some of my previous [posts](http://www.gamasutra.com/blogs/author/JosephAzzam/1009192/), please excuse the repetition.

Capturing the Soul of a European Statue

I was attending a 3D scanning conference in Salzburg (Austria), and I took it as an opportunity to do some sight-seeing and scan a few monuments. Here’s a Paracelsus statue that I scanned in the park. I didn’t take a lot of pictures (55 photos in total). I just took a loop around the statue, then took a few close-up pictures to get a higher resolution texture.

Then, I post-processed those photos using DxOptics (or Photoshop Camera Raw) and created two sets:

The first set was needed for reconstructing the model, meaning that its purpose is to provide photos with clearly visible features that will help the scanning software to align the images. To do so the photos had their histogram equalized, their contrast slightly increased, and they were sharpened a little using an Unsharp mask. Then they were saved in an 8-bit resolution.

The second set was needed for generating the texture, meaning that its purpose is to provide clean textures with a few shadows as possible, and a high dynamic range. The shadows and highlights were reduced, and the set was saved in 16-bit since this the texture will be heavily post-processed since we will need that extra information.


Later, I aligned the photos in Agisoft, and here’s the result:

![](../../assets/c62bcfae03390b0c.img)


![](../../assets/7baeb98bf8dea1ab.img)


![](../../assets/5ba127d2c086e15e.img)


Even though the Agisoft automatically-generated UVs are not the best, there is no need to create UVs for the high-poly mesh since you’re not going to use it in your game, plus good luck creating proper UVs for a mesh with such a high poly count. Instead generate an overkill high-res texture (i.e. 16k), and then later project it on to your properly UVed low-res model, and generate your intended texture resolution (i.e. 8k). This will eliminate any white lines generated from seams.

The lower resolution mesh can be created using Meshlab, TopoGun, ZRemesher in Zbrush, ProOptimiser modifier in 3ds max, InstantMeshes, or whatever workflow you prefer. Then you properly UV the low-res mesh while trying to have as few seams and stretching as possible since we will be applying another texture on top later. Remember to properly orient the UVs as well, so that the overlaying texture doesn’t look randomly rotated in some areas on your object.

If you absolutely need to properly UV your High-Res model, you can always just go into ZBrush, use ZRemesher and create a lower-res mesh, UV that, then subdivided it and then re-project the details on top of it from the original mesh, creating a properly UVed high-res mesh.

![](../../assets/7770d0c66fd07ff5.img)

[method](https://www.youtube.com/watch?v=stjZRy2XM20) demonstrated by James Busby from Ten24. This technique consists of selecting darker areas in a picture and then bumping their exposure a little. Note that this method is subjective, and I will be using later in this article a more accurate one. The Roughness Map was created by creating an inverted grayscale image of the diffuse map that I later leveled and subjectively tweaked a little.

![](../../assets/301712638738b5cc.img)

[Sketchfab](https://sketchfab.com/models/8279ff1bb0f3493bb5ede714a383183c).

Extracting the Essence of Middle-Eastern Rock

The process here is pretty similar to the statue’s, though our main purpose here is to extract a universal texture that will work on any model unlike the one created for our statue. I will be explaining more why we are doing this as I go a little deeper into some topics.

When removing features from a texture, it’s hard to know when to stop, and a way to answer this would be to keep in mind that everything we remove must be added later, whether by blending textures, or the game engine itself can calculate this information for you.

It’s always a good idea to define the target resolution for a scan, and this is what determines whether to take 6 photos to scan a wall, or 200 photos to scan a single rock.

First, we scan our rock, since we would like to extract a high-res texture, we need to take a few more pictures to gain more resolution. And again, we create two sets of images, one for the reconstruction step, and the other texture projection step. Depending on how well calibrated and sharp your camera is you can skip this step and use your original images directly. Here is the scan generated from 37 Images:

![](../../assets/d8677c931d2ce9e6.img)


![](../../assets/18cd1e13b79b837b.img)


Again, we use generate a very high resolution texture on our high-res model using the automatically generated UVs from Agisoft, then we bake them on to our properly UVed low-res model. By looking at the following images, notice how when projecting from the automatically generated UVs on the right to the manually created UVs on the left, we get some white line all over our texture. This is only visible when you zoom in, the higher resolution your texture is, the less noticeable they are. Once you generate the texture you can downscale it to whatever resolution you need, and those lines should disappear.

![](https://eu-images.contentstack.com/v3/assets/blt740a130ae3c5d529/blta3c376df2997faaf/650ea0c928d5e3eb3c404ae6/8.png/?width=646&auto=webp&quality=80&disable=upscale)


![](../../assets/09313e4a40919d68.img)


![](../../assets/49f9eeab42cc7983.img)


![](../../assets/fe4ecf82c34edec9.img)


De-Lighting the Texture

By now this process is a little outdated as there are different and faster approaches to de-light a texture (Substance, Megascan, etc…), nonetheless it’s still a valid approach, and it’s good to understand it.

The previously used de-lighting method for the statue is subjective, selecting darker areas and increasing their brightness is not the best approach since it’s hard to differentiate between dark edges, dirt and shadows, and if I used that technique on this rock I can end up with some pretty bad results like the following:

![](../../assets/d33445d57ec90ee1.img)


Here’s a demonstration of this technique:

And here's the final result (Hey Ma! I just ironed a rock!):

![](../../assets/16e280fa3b95d678.img)


By now we have extracted all the information we need to perform our alchemy trick, and it’s all a game of mix and match. By separating the object properties from the material properties of the scans, we simply take the object properties of the first scan, and mix it with the material properties of the second scan.

Here’s the material setup in the Material Editor of Unreal Engine 4:

![](../../assets/ffbf05726b4dc8ee.img)


Conclusion

I hope you found these blog posts series useful, and if you have any questions you can always ask the comments down below, or hit me up on twitter [@JosephRAzzam](https://twitter.com/JosephRAzzam). For updates on the game progress, you can out the Devlog section of [World Void](http://worldvoid.com).