---
title: Unity 2D asset pipeline with Affinity Designer
url: https://gametorrahod.com/unity-2d-asset-pipeline-with-affinity-designer/
author: Sirawat Pitaksarit
published: '2019-07-12'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

Many may know how to create an artwork in art program, however I am still seeing some people slicing images for export manually or even create each artboard for each little images... the technology had already advanced far past that point though!

## Use Symbols feature as a representation of instances in the actual game

![](../../assets/b1e46167100a03c8.png)

Unlike traditional art, game is an interactive media so you can't go all out and count everything as a mere pixels. There are space constraints, and performance constraints.

For example if you see a finished design like in the picture above, artist with no game development knowledge would export **a big sheet** of BG with a separated sliced fruit sprite for gameplay, perhaps. However to display that BG with no loss in quality it would take huge RAM and space on device like iPad Pro.

![](../../assets/88029aaa71b32a3b.gif)

Instead, we should recreate the art in-game **again **with bits of reusable pieces even if they doesn't looks like a gameplay element.

The big sheet of BG is now just a simple solid green rectangle that cost nothing because it could be made from recolored white square with big scaling. Then details like grass and dots are placed manually over it to recreate the original design. This way, each pieces looks sharp and cost low memory and space.

One more reason not to bake everything as one big sheet is that mobile games nowadays should adapt to the device. I didn't bake the picnic mat, that allows me to move it back when screen gets narrower, or stretch it out in the case of a notch present. (Plugin used : [Notch Solution](https://github.com/5argon/NotchSolution))

![](../../assets/0c342288aee89260.gif)

The **Symbols **feature is exactly what we want in Affinity Designer. You create an instance of something and then try to design the scene with it, it's almost like you are programming a game inside an art program. When you are satisfied with an amount of symbols you have, you export just the symbols.

## Exporting with symbol slices

![](../../assets/9f268fa87190df7d.png)

This artboard that collects symbols is actually not needed, because Affinity Designer could slice each one individually even while overlapped just fine. However there are some symbols which I don't like in the design artboard so collecting them this way helps choosing the one I want.

These collected symbols are of the same instance of the one in the main board, so I could edit things over there and it will reflect here. For example, I found this small mistake later in the game. I could just edit and export again.

![](../../assets/621d943de51ccb7a.gif)

How symbols works could be compared to Unity's prefabs. If you edit the **content **(which is denoted with **solid orange line**) it will be reflected on all instances. If you edit the top-level transform (denoted with **gradiented orange line**) it will not be reflected. You could put it, rotate it, or scale it differently on the top-level transform. This approach is similar to new Unity 2018.3 prefab workflow where we used to wrap one more layer over what we would reuse. (If Affinity Designer could do an equivalent of prefab variants that would be sick!)

![](../../assets/f25c0ae489e07d6c.png)

And yes Affinity Designer **could** **do painting**, it is not just a pure vector program, as you may have misunderstood from the pair of Affinity Photo = Photoshop/Affinity Designer = Illustrator.

Go to Pixel Persona and you could use raster brush. Come back to Designer Persona, they are now a rect of raster that could be rescaled nondestructively. (Pixels do get interpolated, but you could get the original quality back **without undo**.)

## Packing the sprites in Unity

The entire exported symbols should be collected in the same folder. That folder is then the only parameter to the `SpriteAtlas`

asset. "Objects for Packing" could accept a folder reference, remember that folders has its own `.meta`

file and that allows Unity to remember and serialize it. Press "Pack Preview" button and it's done.

![](../../assets/f810220c3f36eabf.png)

`SpriteAtlas`

help you mainly 3 things :

- All images could be draw together in only 1 draw call, because we submit this entire sheet to the graphic cards and commands where and how much to draw a part of it.
- It ensure power of two size, allowing various compression algorithm to be used.
[See this article](https://gametorrahod.com/dealing-with-ios-android-texture-in-2019/)for more details about how to choose a compression settings. - In Unity,
`SpriteAtlas`

system is very**transparent**. (As in you don't feel you are using it) You could use each individual sprite while designing the game**as if**they are an individual image. But in the real build they would be packed, the original image not included in the build, and you still get the correct image. Some early systems requires you to pack first, then design the game from the packed sheet. This make it compatible with Affinity Designer's export since in Designer you export little pieces and not a sheet. Re-exporting to overwrite the old ones works beautifully and Unity will repack in the case of dimension change.

## Optimizing the sprite sheet

However that's not enough, look closely :

![](../../assets/685c4cb93591be84.png)

Because of power of two constraint of atlas that enables Crunch ETC2 compression to work, we got quite a bit of space here. (Still better than no space but unable to use Crunched ETC2)

It's time to make a trade offs. I could reduce the size of some textures in order to get the next lesser POT size like 1024x1024. Candidates for this optimization are :

- Texture that is blurry in nature/gradients/with less sharp outlines and edges. For example that tree shadow, or less ideally that dark detail of the grass (it has an outline that would be blurred).
- Some extreme example is a white rectangle. In this case you could make it 1x1 and scale back to perfect quality lol.

![](../../assets/924e4263d2c5d626.png)

- Something like this bubble effect will get the sharp outer edge blurred when scaled back, but maybe acceptable if it is a fast effect.

![](../../assets/197fefbb35c59459.png)

- An inverse of that bubble, a radial gradient, could be scaled down a lot and you get it back near perfect.

![](../../assets/87e79026d601be55.png)

So to do this, unexperienced developer may tell the artist to export an image again from Designer with smaller size. Which is possible by the way :

![](../../assets/12c679f19f6292ec.png)

But don't bug your artist just yet. In Unity, `SpriteSheet`

will **override** a compression settings of individual sprites used to pack into it. But it will **inherit **maximum size constraint of each one.

![](../../assets/46494793df09f040.png)

![](../../assets/cbfda5b338bef0d2.png)

This tree shadow is too large at 585x**895**. Limiting this to 512, the size is now 335x**512.**

![](../../assets/dc96e47b49e1e2fb.png)

Press pack again :

![](../../assets/b50204bc1e0ba51c.png)

You see that you **almost **got it! There are so much space up there but need just a little bit. How about scaling down that grass shadow? (I don't want to scale down the picnic mat, since it got some fine textures in there that would be noticably pixelated.)

One side was 748, so I locked that to 512 and here's the result :

![](../../assets/2a6b24da044ca544.png)

![](../../assets/4c63ef980eb3f503.png)

We have got the atlas size down to 1024x1024, finally. Crunched ETC2 size reduced from 116.6 KB to 84.0KB. If you used other compression technique, you may get much more savings. Some compression like PVRTC can't even do non-square POT size, so this optimization is crucial to enables PVRTC format.

## Advanced optimization

However you want more. Supposed you have nothing else to add, but you see that wasted space. You wished you could enlarge your tree shadow back a bit because that's basically free resolution.

![](../../assets/b9f59691bd21a4d8.png)

However the dropdown only says 256, 512, then 1024, which obviously will blow the packed texture back to 1024x2048. What to do?

Actually Unity could do arbitrary size limit.. with editor scripting. However we can hack this quick with Inspector's Debug mode. Right click Inspector and select Debug. Look for this, and type in any number you want.

![](../../assets/39dbf18bfd406d1f.png)

After coming back, you will see the size dropdown goes blank but that's fine. To make the Apply button not greyed out you have to touch something however, maybe check-uncheck that crunch checkbox. Then press Apply to get a custom limited size.

![](../../assets/db684d557d5dd55d.png)

After repacking, I could utilize wasted space to the max now!

![](../../assets/7032b14fd741b25a.png)

Or, if you really want that grass shadow as sharp as original, you may sacrifice a draw call instead. I separate the tree shadow to a new texture and enlarge back the grass shadow. Of course make the separated one POT too to enable compression. You could make a new `SpriteAtlas`

with only one member to force POT but in the below image I did it manually from the outside.

![](../../assets/b95a36335558f742.png)

![](../../assets/f67ba37d4adb7503.png)

Ensure that the tree shadows are drawn together the last too, or you will ended up with 3 draw calls because it was sandwiched between the main atlas and require more texture switches to GPU.

Does 2 draw calls worth the resolution gained back? One more thing you could play with is that now that the tree shadow is a separated draw call, you could use a **completely different material** without worry about breaking the batch because it is already broken!

One common use is to use additive blending material for lighting effects because that requires a new material. Dark texture like this could be played with something like a material that produce blending like color burn or overlay in Designer.

In this case, I use this opportunity for [Spine by Esoteric Software](http://esotericsoftware.com) which requires a separated packed sprite and a dedicated material. I could do bone mesh deform animation on it at the cost of one more draw call.

![](../../assets/a3db9a8d7c1cbcc1.gif)