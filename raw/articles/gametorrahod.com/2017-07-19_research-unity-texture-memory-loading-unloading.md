---
title: 'Research : Unity Texture Memory Loading/Unloading'
url: https://gametorrahod.com/unity-texture-memory-loading-unloading/
author: Sirawat Pitaksarit
published: '2017-07-19'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

This time it’s in English since I thought someone might Google and stumbled upon this. Normally I write in Thai.

EDIT : With the upcoming Addressable Asset System all of these will not matter! You will have complete control on loading and unloading! [https://docs.unity3d.com/Packages/com.unity.addressables@0.3/manual/index.html](https://docs.unity3d.com/Packages/com.unity.addressables@0.3/manual/index.html)

## The Problems

There are several interesting and ambiguous questions in Unity about when the memory will be occupied. On mobile it is especially important! First these are fundamentals :

- When the scene has been loaded it scans every game objects, and then everything connected to the component would be loaded immediately. One exception is AudioClip with preloadAudioData unchecked in the inspector (added in Unity 5.0)
- Even if you connect ScriptableObject asset, it would still traverse to that asset and load everything.
- The only way to
**not**connect things and load things**later**by string path is to put your assets in Resources folder. - There are Resources.UnloadUnusedAssets() and Resources.UnloadAsset() to use. (Also the exclusive AudioClip.UnloadAudioData) The latter cannot be use on GameObject or components, it must be on “asset” like Sprite .

Now, things can get complicated. I have several questions :

- What is considered “unused” for Resources.UnloadUnusedAssets() to unload?
- What happen if I Resources.UnloadAsset() the one that is currently used? If it does not work, how to make it work?
- What if the prefab is inside Resources folder (instantiated by string path) but the reference images they refer are all outside Resources folder? What about inside-inside? Outside-inside?
- If all the references of images is in AnimationClip which is in Animator does it still load immeadiately or is it load on playing?
- Can I delay the loading by not activating the component containing references to the images?
- Can I unload Sprite ? Or must I unload texture ? Both are assets, so is there any difference?
- etc…

I remembered concerning about this many times. This is a research so that I can come back and refer to in the future. Unity2017 just have been released too, I think this is a good opportunity.

## The Unity Project

In this project I have 12 of 2048x2048 uncompressed RGBA32 texture. It’s 16 MB each as shown in the inspector. Half of them are in Resources folder. I made them big so that I can easily see memory differences. The alpha source gray scale is to force the alpha channel.

![](../../assets/07392d610a822075.png)

There are 8 different prefabs and 8 different scenes. In each scene I am able to instantiate each one and do things with it.

```
ImageOutside-PrefabOutside
ImageOutside-PrefabOutsideAni
ImageInside-PrefabOutside
ImageInside-PrefabOutsideAni
ImageOutside-PrefabInside
ImageOutside-PrefabInsideAni
ImageInside-PrefabInside
ImageInside-PrefabInsideAni
```


(I should have name them Prefab___-Image___ but it’s too late.. sorry. But basically the first 4 reside outside of Resources folder)

The name shows their differences :

- ImageInside/Outside = Images referenced are inside/outside Resources
- PrefabInside/Outside = The prefab itself is inside/outside Resources
- Ani = Contains Animator that in turn has AnimationClip that reference the images. Otherwise it is a simple script that holds an image array and cycle each image manually. If no “Ani” and it’s “ImageInside”, the image array will be initially empty. (Manually loading from Resources later)

We will start from -Start scene which has no prefab and has nothing to do. Pressing **Next Scene **button will go to the scene 1 and so on. But actually, after each Next Scene press it will go to RestScene which will UnloadUnusedAssets to clean things up before going to the next. The RestScene contains almost nothing, so UnloadUnusedAssets should clean everything up… or not!?

There are code to time the time it takes to load scene and to Instantiate the object too. Obviously this depends on devices. I am using **Nexus 5, **it was released many years ago and should be slow enough to show differences.

You can get the project and try it yourself from my GitHub. Who knows maybe it’s different in iOS? Or other platforms? (If it really is I would appreciate if you contact me via GitHub issues)

**5argon/UnityTextureMemoryResearch***UnityTextureMemoryResearch - A project for trying out Unity's behaviour of texture memory loading/unloading. Read …*[github.com](https://github.com/5argon/UnityTextureMemoryResearch)

## Procedures / Experiment Design

- Build this project to Android and use remote Profiler to monitor memory usage. This is to prevent Unity profiling memory from the editor.

![](../../assets/ad073657bf32fcc4.png)

- The 36 sequences of actions are according to this table. It’s sequential from left to right, and on each row is a separate run of the scene. I press Restart Scene button inbetween runs. Note that Next Scene at the end is to test the effect of cleaning up with UnloadUnusedAssets just in case.

![](../../assets/1141679699618d6a.png)

You could look in the code what is the meaning of each cell. But here are readable format :

- Instantiate : InstantiateThe GameObject that is already connected to the inspector.
- Instantiate From Resources : Use string to Resources.Load the GameObject and then Instantiate
- Toggle GO With Sprites : Initially the script that will cycle images is disabled. But that script will already have images connected in the case of
**ImageOutside**. These sprites’ names are 1,2,3,4,5,6. (.png) - Load Sprite Resources : In the case of
**ImageInside**, we need to load those images from Resources before toggling the script and let it play. These sprites’ name are 7,8,9,10,11,12. (.png) - Toggle Animator : The Animator too has been disabled by default. But it already have AnimationClip with all the images connected. Ani-test does not have dynamic loading of images, its all embeded in the clip.
- Destroy/Unload Unused : Destroy(gameObject) and Resources.UnloadUnusedAssets() .
- Unload Connected : Call UnloadAsset on all connected sprites. I expect this to not work, since there are someone in the scene that are using them.
- Unload Connected Inner : The same but instead of doing it on Sprite I goes one step further into Sprite.texture
- Remove Reference : Remove all the reference of sprites. The array will be emptied, and image.sprite = null After this, I expect UnloadUnusedAssets to work. Also after this Unload Connected should not work, since nothing is connected anymore.
- Unload Displaying : This has 2 meanings (it has if in the code) if you use it before Remove Reference, it will try to unload sprite only the one that Image component is using. But if after, it can unload that one image Image previously use. (The code of Remove Reference can remember the last image used) I expect the latter case to work while the former case to not work.
- Unload Displaying Inner : The same but instead of doing it on Sprite I goes one step further into Sprite.texture
- Unload Used In Animation : This one is weird, because I could not dive into AnimationClip I have no way to know which texture the animation used.

In the case of**ImageOutside**I created a new Sprite[] just for holding those texture that I used in the animation for the purpose of Resources.UnloadAsset (It does not incur additional memory since Unity will load the one in the animation on starting scene anyway… whoops! I have spoiled some of the results!)

But in the case of**ImageInside**, I don’t want to connect references to further confuse the results. Instead, on unloading I use string to load those asset again just for the sake of getting references for unloading. The assumption is the loading part would be in a flash, since Unity already loads those sprites from the animation anyway.

And again, Unload Used In Animation Inner means I unload Sprite.texture instead of Sprite .

## Results

Here it is! I spent 8:00 AM to 10:00 PM for this!!

![](../../assets/c20e4d5e8c40a0ee.png)

Clean state memory : 26.7 MBYellow cell means all 6 images is in the memory, 137.3MB

Green is 106.5 MB, which means one image is missing from the memory

If you can reason every changes/un-changes of each horizontal consecutive cells in the table just by looking at it, you are the Unity memory master!

## Interpretations

You can try to interpret the result according to your requirement, but here’s mine.

### The initial loading depends on when Unity see those references

This is probably the only big different of the various combinations. This might be already obvious to many but please think of it as an excercise. The red number shows where the significant lag is in milliseconds.

![](../../assets/8d2f62f9c7f96f46.png)

Note the significant **scene load time** only on scene 1, 2 and 4. (It’s not discernable on the computer, but on mobile it does.) What does it means?

(1) (2) Because all images that is connected in inspector will be immediately loaded on scene load. This is according to the fundamentals.

(3) is fast since the image is in Resources and we will manually load later. The prefab that is connect to the inspector does not matter, as it is so small without those image references. This way, your game can have a fast scene load time with prefab connection for easy scripting. Then you might have some kind of spinner to wait while the prefab loads the missing images.

(5) Has fast load time despite images being outside of Resources because there are no reference to the prefab that unity can know about those images. At the moment I use string to load the prefab, Unity will notice those connected images and load them as you can see from the long **Instantiate From Resources **time. (6) is the same because of the next topic.

(7) Has both prefab and images in Resources , so even after loading the prefab Unity still can’t see those images. The workload will then be on Resources.Load . Because the prefab is fast to load on scene start, I suggest you do like in (3) instead. (skipping manual loading on prefab, but do manual loading on the hefty images)

(4) Has images inside the Resources too but why it has long scene load time? It’s because…

### Using images in AnimationClip is no different from connecting in an inspector

You cannot escape the load scan by putting things in the keyframe. Unity will scan all of them anyway. Note that there is no way to iterate through the keyframes by yourself to find out all the references AFAIK.

And those images can be in or out of Resources folder. It will be the same as seen on **Instantiate From Resources **time of (6) vs (8). It’s connected via keyframes in the AnimationClip, and Unity will find them. Unless you left the AnimationClip out and try to create one from script + Resource.Load ing the image dynamically. But that’s crazy outside of very trivial animations.

### Setting enable of components to false cannot stop the automatic loading

![](../../assets/d559b7fb220dcc53.png)

I tried several attempts to delay the loading further by defaulting the .enable of components using them to false . (You tick the box by component’s name) but as you can see the cell was yellow before those enables.

The same also applies to Animator . I have them .enable = false by default but Unity still scans and load everything.

### Destroy does nothing to help freeing memory

Some newbie Unity developers might think because the object and the references is no more, Unity should know to unload all the things. But it’s not like that! You will need manual unloading, or you can wait for the garbage collector. (not recommended)

There’s Resources.UnloadAsset to pinpoint what to unload but that’s for the other topic. Here I will talk about Resources.UnloadUnusedAssets Note that at every Destroy the cell color does not change from the previous one. It does not take care of the memory.

### If it’s still in the memory, the loading will be free

If you just destroy things and Instantiate that object again, the instantiation will be fast since all images are still in the RAM.

You can try it yourself in (5) and (6) where instantiation time is long. Alternating between Instantiate and Destroy button and you will see that only the first time took ~1500 ms.

If you use UnloadUnusedAssets before the next Instantiate (and it succeed in clearing memory) the Instantiate will be slow again.

But this is not the reason you should skip doing “game object pooling”. Naively instantiating 100 bullets might benefits from still having the bullet image from the 1st instantiation, but that technique is to further reduce the time to instantiate the game object to the scene itself. (It can be a bottleneck, especially if your instantiated object has several components with its own Awake or Start codes)

### Resorces.UnloadUnusedAssets removes everything that has no references in both scene AND code

![](../../assets/6a658507f57a5666.png)

The first dashed area UnloadUnusedAssets failed to clear out the memory! The game object has been destroyed so why! That’s because the scene still has that game object connected to the main logic script (that help easily instantiating the one you just destroyed in the first place). And by that connection, Unity see that it also have all the images connected. Unity cannot remove them. The second dashed area is of the same reason. Remember that AnimationClip is the same as connected.

The third dashed area succeed in clearing out the memory (white cell means about 26MB, the initial state.) This is because even though the prefab reference is present in the scene, it has no reference to images. (You dynamically load them via strings) Unity can remove those.

The fourth dash area (and also in (8)) succeed in clearing out the memory compared to the second dashed area that also uses AnimationClip . Why? This is because we dynamically load the prefab itself, there are no more prefab connection in the scene to wait for easy instantiation. (We used string to instantiate) The one you destroyed is the last reference to images, so Unity can clear them out.

You can see many stupid UnloadUnusedAssets in the middle area of the table that does nothing because I call it while everything are still alive and kicking. I add them as a little sanity check that it really does nothing.

![](../../assets/6815f2f3f06b217b.png)

Fun quiz! Right here there is no Destroy , but the prefab reference in the scene does not contains reference to images. This means the only reference left that keeps UnloadUnusedAssets from working is the one you currently look at. By doing **Remove References** I cleared out the Sprite[] that I filled before with string and Resources.Load and also clear the one that Image component is using (the image now turns to white, as you can see from the white box I added).

**Remove References **still put back one more reference to the one Spritethat Image just used! (I don’t want to see the image but I want to experiment unloading just that one image in various ways, which I will explain further in other section.) But **Unload Displaying **will try to unload (and miserably failed as you can see the cell is still yellow 137 MB, no changes. Reasons coming but in short I should not unload on the Sprite) …then set that reference to null . Now the next UnloadUnusedAssets works beautifully.

The question is how much is the memory allocation if I skipped **Unload Displaying **command knowing that it failed and does nothing?

The answer is **40MB. **The clean state memory is 26.7MB and the maximum is 137.3 MB. We have 6 images so each one would be about (137.3–26.7)/6 = about 20MB. That means one image was left from the aftermath of UnloadUnusedAssets , and thats because the behaviour of **Remove References **still keep that one more image **in the code **without **Unload Displaying **to null it. The lesson is not only in the scene, but if you forgot something in the code then UnloadUnusedAssets cannot remove it.

### Use Resources.UnloadAsset on Texture2D, not on Sprite

You can see many misses from the table! Using UnloadAsset on Sprite was a mistake.

![](../../assets/c794ba4706e31cfa.png)

These methods has “Inner” variant where I correctly unloads on sprite.texture .

The dashed area shows non-Inner variant. And there is no change in memory at all. Below all dashed cell are the Inner version, you can see something happened on that cell.

The green **Unload Displaying Inner **below dashed area make sense since it successfully unloads just one image.

The white **Unload Connected Inner **below dashed area make sense since it successfully unloads all images. (All are “connected” to the inspector) After the unload, technically they are all still connected but UnloadAsset has that power to unload things while keeping the reference. But Unity will have already load through them automatically from the first time Unity see them. (Audio has preloadAudioData = false to help preventing this problem.)

The emoji cell will be explained later.

### Resources.UnloadAsset can forcibly unload asset even if someone is using it

In the design section I have several assumptions that UnloadAsset would not work if I use them on something like on the image that Image component currently using.

Turns out to be false. It’s working fine if I do it on the texture and not theSprite and immediately turns the displaying image to black. Image does not try to load back that texture . (yet)

### Resources.UnloadUnusedAssets can actually unload something that are currently being used

Surprises! Using Resources.UnloadAsset on Sprite previously was not completely in vain! You can observe some effects of unloading to a Sprite . It actually does **something.**

![](../../assets/21f7624fa9affce9.png)

On each pair of cell in dashed area, on the left side it seemingly does nothing. But on the right side UnloadUnusedAssets has some degree of success.

First I will try to explain the yellow-white ones. From the left side, Unity have **successfully** unloads Sprite . You see no change in memory since Sprite is small. The meat is in sprite.texture . You did not unload that.

Now that’s what tricks the UnloadUnusedAssets to function. Because normally (I guess) it follows a reference by any objects -> Sprite -> Texture2D to see that it still cannot unload the meaty texture .

I only have references to Sprite in all of my code. Unity must start following from them to reach the textures. It’s the only way.

Now that the references to Sprite are no more, UnloadUnusedAssets unloads the seemingly dangling texture .

UnloadUnusedAssets made a mistake since “No one is using the texture” is not true. Actually the Image component might be displaying that texture . But remember that Image component take Sprite asset and not texture . Internally it will probably dig out texture for use and then stop caring about the Sprite .

I have manually UnloadAsset all the Sprite but the Image component was still displaying just fine. The moment UnloadUnusedAssets take texture away the image turns to black. Things would be different if I was using RawImage , I guess that component can hold onto the texture itself and can really prevent UnloadUnusedAssets from working. (untested)

The side effect is that now even UnloadUnusedAssets can forcibly unloads the things that are currently used like UnloadAsset(despite the irony of its name)

On to the yellow-green pair, it turns green because of the same reason. But the yellow cell before have just unload one Sprite from all the available 6 Sprites . The result is that UnloadUnusedAssets snatch that one dangling texture away, resulting in a bit of reduced memory used.

### Black is the color of texture not found

If I remove image reference from Image component ( null it) it will turns to **white**. This is the “no change” color of Image component that you set in the inspector. It can be any color you like to tint.

But if I successfully unload a texture that the component happen to be using, the result is black image.

Ideally you should stop using them before unloading but its good to know you can also unload **while **being used. (Unlike UnloadUnusedAssets as the name might suggest)

For those wondering what the editor looks like when the image was unloaded and turns black, it looks just like normal. That Source Image is currently unloaded.

![](../../assets/8d08399f73875ef0.png)

Pressing delete key turns the image from black into white, drag and drop the same 6.png texture to the slot and it will reload the texture.

### There are ways to unload images used in AnimationClip

You cannot stop Unity from putting all images used in keyframes in the RAM because Unity have already scans them.

But knowing that UnloadAsset can pinpoint the unload, what will happen if I **somehow **holding the references to those images used in the AnimationClip and give them to UnloadAsset ?

The result is **yes**! You can unload them! Even though you cannot stop the loading, you can then quickly unload it if you don’t want the auto load that Unity did. If the animation is currently using them, the displaying sprite will turns to black.

![](../../assets/de40c1e5e1c3f9d3.png)

I will talk about the emoji ones in the next section, but in longer dashed area it turns to black. Note that before the longer dashed area there are 2 **Toggle Animations. **This is to stop the animation at a certain frame. The emoji ones unloads while it is playing.

Now you might be wondering how I managed to get references to those textures for use in UnloadAsset ? I have searched for how to iterate through keyframes to dig reference data out but I could not find any way. I cheated by manually making an additionalpublic Sprite[] that I know they are currently being used in the animation. This makes a fragile code since if I put new sprites in the AnimationClip I have to remember to add those in this array too. And using this array means UnloadUnusedAssets cannot take care of them. You are still holding the references after all.

Another way to cheat if your images that you use in the AnimationClip is in Resources folder (and you have reasons of not wanting to connect them to the inspector) is that you can Resources.Load them just for that you can get a reference to UnloadAsset them. The Load will be free, since Unity already have them playing in the animation. (Just make sure you load the correct ones that are really being used) Now you have references without diving into the clip.

### Animator can automatically load back the unloaded images if it is playing

You might see the gradient and the 😲 emoji face. That’s my face at the moment by the way, but what happened was the image turns to black, and then the animation plays slowly until it completes one cycle. Then it resumes at normal speed. This is the profiler of that.

![](../../assets/51cbbdd677abc439.png)

The memory slowly recovers to the full blown state shortly after I try to unload (effectively, on the texture ) image used in the AnimationClip .

From the last section the image turns black because it is not currently playing. Now that I unload everything **while** it is playing, it will force loading **sequentially **as it plays. To be safe, unload when animation is stopped or the game will lag without any gains.

This might results in a trick where you immediately unload everything you know you are using in the animation. Then as you use the animation, Unity will only load the one it actually encounters. I think this trick would cause more harm than good for a quest to smooth frame rate, it is just a wild idea.

### Use UnloadUnusedAssets in an empty scene will clear out ALL asset memories

The **Next Scene **command always succeed in resetting to fresh state, since :

- The
**Rest Scene**was loaded with LoadSceneMode.Single everything will be cleared out. - The scene contains nothing more than a simple script to go to the next scene, of course UnloadUnusedAssets should work optimally while in this scene. (Unless you put heavy things in static variables)

Might sounds trivial, but you can do this to “refresh” your game. You would do this in a “now loading” scene. All that left after the cleanup would be some dancing characters you might have in the loading scene.

Also note that this might not be the best solution. If the next scene will load the same big things as the previous scene you might want to be more selective in your unloading, keeping something in the RAM.

How about purposefully holding onto something via new variables or destroying everything you don’t want in the scene except certain game objects, and then call UnloadUnusedAssets ? This command can then become a powerful selective unload if you know how it works.

### Update

There is more information about using Resources folder together with SpriteAtlas along with manual loading/unloading at the bottom of this article.

**Demystifying Sprite Atlas Variants***Just dragging sprite to the slot in an inspector does not tell anything about which atlas it would use. How can we have…*[gametorrahod.com](https://gametorrahod.com/demystifying-sprite-atlas-variants-d53535bc43da)

I hope you got something from my research! This is usually the moment I can advertise [my own game](http://exceed7.com/mel-cadence/) but sadly it’s far from finish. (so I’m not going to)