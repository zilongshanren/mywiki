---
title: Messing with Unity’s GUIDs
url: https://www.boristhebrave.com/2020/02/05/messing-with-unitys-guids/
author: Boris
published: '2020-02-05'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

I recently released an addon in the Unity asset store. It’s actually two addons: [Tessera Pro](http://u3d.as/1Jqi) is a fully featured copy, with complete source code, and [Tessera](http://u3d.as/1DAj) which has cut down features, and you just get a precompiled .dll.

I quickly discovered a big problem – if you upgrade from Tessera to Tessera Pro, then all your scenes become broken. You get this error, which is likely familiar to veteran Unity developers.

![](../../assets/af7e09a46e6129c9.png)

I’ll go into what’s happening in general, and how I dealt with it.

First, we need to understand what is happening. Internally, Unity stores references between objects using a particular format. If you open up any scene file in the editor, you can see many examples like this:

`{fileID: 11500000, guid: e3ad2bf01b7a6b7409eb683402aa8668, type: 3}`


The `type`

is about what type of refence we have, so we’ll ignore it. But what are `guid`

and `fileID`

?

Essentially, `guid`

specifies which file to find the reference in, and `fileID`

says which item *inside *that file. Unity creates a new [random guid](https://en.wikipedia.org/wiki/Universally_unique_identifier) for every file in your project, and stores the guid next to it in a meta file. So when you create `MyFile.cs`

, Unity creates `MyFile.cs.meta`

. And `fileID`

is a number based of the name of the referenced thing (more on this later).

90% of problems with Unity references are because you haven’t correctly kept those meta files around, and it’s generated a new one. A new file means a new guid. Which means all your old references won’t work. That’s why Unity recommend you make file changes using the Project tab in the editor – it’ll take care of meta files for you.

To fix these sorts of issues, you either need to update your references, or update the metafile. [PlayMaker has a good tutorial on doing the former](https://hutonggames.fogbugz.com/default.asp?W1254).

Having learnt all this, I tried to apply it to my problem. I want to make it that when users replace Tessera’s .dll with Tessera Pro’s script files, the references stay the same.

Sadly, I discovered this is simply impossible. To see why, you need to know that the exact choice of `guid`

and `fileID`

depends on what sort of reference we’re making.

| Reference Type | guid | fileID |
|---|---|---|
| Local (e.g. within a scene) | missing | from object name |
| To a MonoBehaviour in a .dll | guid of the .dll | from object name |
| To a MonoBehaviour in a script | guid of the .cs | Always 11500000 |

I can fiddle with the guids as much as I like by editing metafiles, but I cannot do anything about the fileID’s.

So, I decided to apply a trick instead. If you load a Tessera scene with Tessera Pro, it doesn’t give a missing script error. Instead, it gives my custom error message.

![](../../assets/358a88748ea16c84.png)

Essentially, I’ve made a new class, `Dummy_296730116`

that has the same guid and fileID as **old** references to `TesseraTile`

. Then I made a [custom editor](https://docs.unity3d.com/Manual/editor-CustomEditors.html) to display that warning if you ever inspect that dummy. The dummy class also has all the same properties as `TesseraTile`

so that Unity doesn’t decide to clear any data.

I picked the name `Dummy_296730116`

very carefully. In order for it to have the same reference as `TesseraTile`

, it needs the same fileID. And fileID, is derived from the name. The exact logic is [here](https://www.robinryf.com/blog/2017/10/30/unity-behaviour-in-dlls.html). It’s a hash function, so it’s not possible to work backwards from the fileID to the class name. But fortunately, fileID is only a 32-bit integer, so it’s easy to search for class names until a collision occurs. It took about 9 minutes on my PC.

That’s the best I could think of. Let me know in the comments if you have a better idea.