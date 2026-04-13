---
title: Demystifying Sprite Atlas Variants
url: https://gametorrahod.com/demystifying-sprite-atlas-variants/
author: Sirawat Pitaksarit
published: '2018-01-19'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

## The problem

Normally when using any Sprite which is in the SpriteAtlas, it automatically loads that packed sprite and use the texture from it. However I want to have a smaller variants from the same set of texture and be able to choose which version I want for a particular Sprite.

The example use case is that I want to have a smaller variant of an atlas to save memory in a certain scene which this image is not required to be that large.


But just dragging sprite to the slot in an inspector does not tell anything about which atlas it would use. This experiment is also to determine what is the behavior if multiple atlas for one Sprite is checked to be include in the build.

The only way I can think of is to actually duplicate all sprite files so you can now differentiate between smaller ones and normal sized ones when you drag to slot in an inspector. For example I have all normal sized icons in Icons folder. I would duplicate the folder and assign it to atlas like this.


Atlas-Icon-NormalSize (Source : Icons + Master + Include in build)

Atlas-Icon-SmallSize (Source : Icons copy + Master + NOT Include in build)

Atlas-Icon-SmallSize-V (Source : Atlas-Icon-SmallSize + Variant scale 0.5 + Include in build)


But this approach is not intuitive and roundabout that I have duplicated physical files in my project (exactly same size in the project, but one would be downscaled in the build by variant) just so I can differentiate it’s atlas in build, which would be hard to maintain.

## Setup

SpriteAtlas Master — 1.0MB

SpriteAtlas Small — 16KB

![](../../assets/8d7d49f6e120e504.png)

Start scene script which is to setup the listener and load the scene with sprites.

![](../../assets/503e4ccb2ce404e1.png)

## Only one of the atlas is included in the build

The result is obvious, the one checked will be in the build. The other one is not in the build and does not use up any space. It is only in your project. The sprite’s resolution is according to which one was checked.

## Both included in build

![](../../assets/83400792d84398e2.png)

![](../../assets/bfd3ed99381c9bf9.png)

**Only Small variant **is included in the build. (var-0.12 refers to the variant’s size, 0.125)

Note that in [https://docs.unity3d.com/Manual/SpriteAtlas.html](https://docs.unity3d.com/Manual/SpriteAtlas.html) it says “randomly”

Checking both will randomly include one of the atlas (master/variant). You might want to uncheck both to have late binding, mentioned below.

## Both NOT included in build

![](../../assets/e1a52f9967fb9a28.png)

![](../../assets/373a1b9b1dd3e9e3.png)

Now the sprites are white and the event was called. The tag requested is **“Master”**. Even if we want it to show the smaller ones this is nothing wrong, since the variant also use the same tag as its master. We can’t say this is the variant or not by its tag. ([https://docs.unity3d.com/ScriptReference/U2D.SpriteAtlas-tag.html](https://docs.unity3d.com/ScriptReference/U2D.SpriteAtlas-tag.html))

In the build, not even the original image 1~5.png is in it. (0.4KB size is not the real image, I guess they are just some kind of index that it uses when we connect the sprite in an inspector. The actual images are 0.6MB each)

## Both NOT included in build but connected in an inspector

Previously I left this blank

![](../../assets/10029d362db04825.png)

So how about this

![](../../assets/a192b3aacdfd5437.png)

![](../../assets/f5daea0feddaf367.png)

Turns out, now both **packed textures **are in the build now **even if we uncheck include in build.**

In [https://docs.unity3d.com/Manual/SpriteAtlas.html](https://docs.unity3d.com/Manual/SpriteAtlas.html) , the page says about late binding with asset bundle but nothing about late binding with textures in the project. I have no idea how to get the packed texture if “include in build” is uncheck (You see this is contradictory, you don’t want the atlas in the build but you want the packed texture in the build)

But (in the actual device, Nexus 5)

![](../../assets/378238daac559bdc.png)

As you can see from the Text, now the event is NOT getting called even if the sprites are white. This is wrong by concept. **The sprites are white which means it has already “requested” for atlas and can’t find any. But at the same time .atlasRequested event was not fired. **How is this possible?

But in the editor the event was fired!

![](../../assets/dc9469a89fe8838d.png)

## Both NOT included in build but connected in an inspector + late binding

I think the previous case is a bug, but I want to try late binding anyways.

![](../../assets/624bec2f661c944c.png)

Editor : Success. White sprites are now resolved and it is the result of the binding event as you can see from the Text. useSmall works too, when I check that it late binds the small ones.

![](../../assets/c10256b007e97793.png)

Device : …of course the event was not fired so we didn’t get any bindings.

![](../../assets/378238daac559bdc.png)

## Ditch the late binding event and use SpriteAtlas.GetSprites

There is an another way we can dig sprites out of atlases directly. It is [https://docs.unity3d.com/ScriptReference/U2D.SpriteAtlas.GetSprites.html](https://docs.unity3d.com/ScriptReference/U2D.SpriteAtlas.GetSprites.html) but it would be less managed as we can’t connect the sprite in an inspector.

We instead connect SpriteAtlas with “include in build” as **whatever** you want. Mine is both false, but even if both are true we will not get the “small variant only” or “randomly” behavior that I explained earlier anymore because we now have them connected in an inspector, Unity would scan them all and include them in the build.

![](../../assets/dab6c21080b6da20.png)

![](../../assets/2638d57b5ddb09f5.png)

Additionally I turned off the late binding, leaving just the log message.

![](../../assets/c04687521def8e04.png)

The manual sprite digging was a success, but notice that the order is not correct. The array we get is ordered as you can see in the log, 5 4 1 3 2.

Due to the nature of the packing algorithm, Sprites in this list are sorted by their area size, in descending order.

But we can ask it’s name. If you know the name you can remove the trailing (Clone) and probably we can have the correct ones.

In device,

![](../../assets/b9ab528485887f5e.png)

![](../../assets/6eb8e01e25dd5431.png)

…it works! (You can see it works, because the order is wrong) Finally. But without the late binding event of course. Now we can have both textures in the build, and choose to load them manually with a little bit of pain.

Note : if you call Image.sprite which you have it connected to Sprite, which in an atlas with “include in build” as false, it will be null. Trying to get the white sprite is not possible. What I want to say is you cannot ask **what is the sprite name of the white sprite **even though you can see its intended name in the inspector. If that is possible we can match each white sprite to the name from GetSprites without the (Clone) suffix. Now that this is not possible, you have to maintain a list of names yourself.

## Making use of these rules

From what we learned, there are 3 rules we can use to control at will which variant will be chosen when using Sprite, and which variant will be in the build.

- Only the lowest resolution variant will be in the build if they are all “included in build”
- The Sprite will select the source texture file from resulting variant in 1.
- All atlas connected in the scene will have it’s texture included in the build regardless of “included in build”

So for example, we can have the Sprite load up the Master variant by default, but also including the Small ones for swapping by :

- Connecting Sprite (which links to both Master and Small) as usual.
- Only check “include in build” for Master.
- Connect the Small one somewhere in an inspector in some scene (which you will use it) so it is indirectly included in the build.
- At runtime the sprite will choose the Master one despite there is a smaller atlas in the build, circumventing the 1st rule.
- Using .GetSprites on the Small atlas you can swap in a smaller one anytime you want by scripting.

## What about “Resources” folder?

How about we force including with the good old Resources folder?

What’s worrying is that the purple SpriteAtlas file is not the actual texture. The actual texture will be generated later transparently, so by doing this would it include the actual texture or just the pointless SpriteAtlas file?

![](../../assets/acdac084031ead30.png)

All 5 images has no other reference than to those SpriteAtlas. The 2 SpriteAtlases contains no connection to any scene.

The result is!

![](../../assets/59f31b5fe9e6a8f6.png)

Both variant’s packed textures is in the build! (Both of them has include in build as **false**) And also, each individual images that becomes the atlas is not in the build. (good)

Now we can Resources.Load it by name and then dig out the Sprite as explained earlier.

## What about memory? How will manual unloading works?

I have made an another experiment with these functions :

![](../../assets/16ab50db3c3a668a.png)

The conclusion is :

- Loading the atlas from Resources does not consume memory but it is required for GetSprite , GetSprites
- With either GetSprite or GetSprites the entire texture is instantly in the memory. This is as expected, you packed them so you don’t have the individual sprite to load anymore.
- Unloading atlas does not freed the memory, but asking .packed of sprite from GetSprite will becomes false and .texture.name will becomes it’s packed name. This is not interesting as normally you wouldn’t unload the atlas but just for the curious.

![](../../assets/d8bcd7cfdcef2f90.png)

4. Unloading even one sprite freed the entire texture memory, as expected.

For in-depth loading/unloading please visit this lengthy research.

**Research : Unity Texture Memory Loading/Unloading***There are several interesting and ambiguous questions in Unity about when the memory will be occupied. On mobile it is…*[gametorrahod.com](https://gametorrahod.com/unity-texture-memory-loading-unloading-7054819e4ae8)

## So in the end it is even more mystifying??

Yes, I didn’t think I would encounter that bug…