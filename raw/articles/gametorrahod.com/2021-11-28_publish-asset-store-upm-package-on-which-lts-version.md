---
title: Publish Asset Store UPM package on which LTS version?
url: https://gametorrahod.com/asset-store-upm-package-lts/
author: Sirawat Pitaksarit
published: '2021-11-28'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

As a package publisher, supporting lowest possible version is ideal for covering your user bases and therefore increase revenue. But in exchange, using version too low will results in many difficult problems.

It becomes a balancing act whether you think the revenue of supporting lower version worth it vs. bumping the lowest version up.

This article will highlight them all from personal experience, having maintained [Introloop](https://exceed7.com/introloop/), [Native Audio](http://exceed7.com/native-audio), and [Tiny Ambience](http://exceed7.com/tiny-ambience). Introloop especially, published its first version in Unity 5. (Now that takes me back! It really begins in Unity 4 or something while I was working on a game called So Many Me with an another company.)

## TLDR

Develop all your UPM Asset Store packages on **2019.4 LTS**.

## Obligations to go back and check

When you say your package works with Unity 5, you must actually go there and check that it works. If you develop in a single project, this may mean you "lives" in Unity 5 forever while developing it to ensure support.

Then when you are about to release, you upgrade sequentially to 2018 LTS, 2019 LTS, 2020 LTS, and so on. Then check on each version.

Upgrade is usually a success, not so with downgrades. After sequentially checking all future versions, you don't commit the change to version control and come back to Unity 5 to develop new features. You will cry having seen better Unity in the future and then having to come back to jurassic period to work on your stuff.

## Always choose one of LTS versions

Back then Unity doesn't have the LTS version that guarantee bug fixes for several years. Now that Unity has it, game developers (especially big companies) are very likely to choose these LTS versions for their game instead of any mid-year versions.

Now it is obvious the lowest support should be one of these LTS versions to support as many big company customers as possible. It will make our lives easier too when these versions would stay for a long time.

## Choose only versions in Unity Hub

Also, Unity Hub is a thing now. The hub serve as an another filter that prevents average users from seeing any other obscure versions. As a package publisher, we can play along and pretend that only these versions exists to simplify development.

In this image, 2017 LTS does not exist anymore in the hub. Now your choices are just one of 2018.4 LTS, 2019.4 LTS, 2020.3 LTS.

![](../../assets/1570724dcb6b0379.png)

## Why supporting 2017 is a bad idea

2018.3 has a great world-shattering update that was Prefab Workflow. I remembered along with that, asset serialization changed a lot that make downgrading to 2017 impossible.

It is wise that your support starts after that "new world" so you don't have to deal with users that uses assets from jurassic era. (That is, just ignore 2017 and lower.)

2017 does not even have Assembly Definition asset `.asmdef`

. That has a lot of features that paved way to UPM support. This also affects all your code, since `internal`

doesn't work anymore when it is one big assembly. `[InternalsVisibleTo]`

is unusable to create good test assembly. And you require a magic `Editor`

folder! All these will make users working on 2020 LTS vomit when upgraded to that version.

## Why supporting 2018 is a bad idea

Whoa! 2018 still exists in Unity Hub! Why would you cut off the revenue like this?

This decision sounds familiar to dealing with [texture format](https://gametorrahod.com/dealing-with-ios-android-texture-in-2019/). You are worrying about users with old phones that couldn't download your game anymore if you decided to go modern. I **abandoned **those users and getting much nicer sleep by the way. So it is up to you!

Back to the topic. 2018 is **behind **one more important world-shattering update for package publisher that is **UPM publishing**, the next step after `.asmdef`

.

### Missing Package Manifest

User now install Asset Store stuff via UPM. While that Package Manager panel will import (pour in) the asset into your `Assets`

folder anyway if those packages aren't actually UPM, if your package are UPM-supported, your users will be **delighted **that your package stays neatly in `Packages`

section instead if actually in the game.

This can be confirmed easily by going to the [Package Manifest](https://docs.unity3d.com/2019.4/Documentation/Manual/upm-manifestPkg.html) page (the `package.json`

) and click the upper left corner, the lowest LTS that this page is available is 2019.4.

![](../../assets/89860cf1fa6b9108.png)

If you could use `package.json`

, it will affects :

- How you deliver your user an offline
**documentation.**No more random readme file when there is a standard[where](https://docs.unity3d.com/2020.3/Documentation/Manual/cus-document.html)to put your stuff. - How to deliver your user
**samples.**Problem was that samples are imported into the game along with the package, then user have to remove them because they adds up to import time if they contains scripts, images, or audio. (Even when not actually used in game.) UPM comes with sample importing button with a[new standard how to do it](https://docs.unity3d.com/2020.3/Documentation/Manual/cus-samples.html). This came in 2019.1. - Your
**online**documentation will suffer from "if you use 2019/2018" hell because how user install, consult documentations, etc. is different from 2018. You need to keep saying this to accommodate all users.

### Missing Dependencies

Dependencies can be automatically installed via `dependencies`

in the manifest, so they don't appear as *game* dependencies.

For example if my package needs Addressables, but my user's game didn't need it, my user's game will ended up having Addressables as a result of installing my package, but Addressables aren't listed on the game.

Removing my package will instantly also remove Addressables from the game.

(You can't use range syntax like `^`

, only a fixed semantic version.)

### Missing ASMDEF features : Version Defines

Even `asmdef`

features are affected. The most impactful would be **version defines**. This make a define appear or disappear based on other resources. It can turn your package into a flex god, offering more extra features as user installed other Unity packages!

![](../../assets/195ab259bfb8671e.png)

Bottom line : Let's together skip 2018 LTS revenue! Time will heal everything and not too long to wait, this version will fade away.

## What about 2019.4 LTS then?

### C# 8.0 is not available

This might be small, but my favorite is [switch expression](https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/operators/switch-expression). It reduces bugs in the code when `switch`

is forced to return the same kind of values for all "arms" (not "cases").

Another one is private `static`

method. (No `private`

keyword, just `static`

but defined inside a method.) It completely disables variable encapsulation, making your function 100% pure. You can even use the same argument name as some variable names from an outer scope. I found that 90% of my nested functions in the method actually wants to be `static`

.

If you want to maximize reach with supporting 2019.4, say goodbye to C# 8.0 and only enjoy those in your own games.

### Missing new serialized array editor

![](../../assets/dcd86ed77c9b8237.png)

2020.3 came with cleaner serialized array editor drawer that has rearrange handles, along with + and - buttons!

If you are going to stay on 2019.4, it maybe better to temporarily come to 2020.3 when you are making screenshots for your documentation so your array are rendered better, if your plugin involves working with serialized array.

### Package Manager is a bit unpolished

Here is how it looks like in 2019.4 LTS :

![](../../assets/b836f6c9faff2cff.png)

![](../../assets/4fc084fa58dd284a.png)

![](../../assets/0ce22a308364069f.png)

Then look at how glorious it is in 2020.3 LTS :

![](../../assets/bf96655c3df525ee.png)

![](../../assets/1049e5281794a25b.png)

![](../../assets/0cbf288abd11b78a.png)

Luckily, both has samples importing buttons. So your documentation teaching user how to use samples works on either. I think differences are mostly visual.

One gotcha on the "In Project" viewing mode is this dropdown saying "Unity Technologies".

![](../../assets/aa20b5a6165a9a0e.png)

This string is pulled from `package.json`

: `author`

> `name`

. Make sure to have this consistent across all your products so they are grouped in the same drop down.

![](../../assets/69c546e5ca5034b9.png)

Initially I have packages developed on my own ("5argon") for fun, and also Asset Store commercial packages I want to release as "Exceed7 Experiments". Technically the name should be different like that, but I disliked how my packages are fragmented to different dropdown. Now I consistently use "Exceed7 Experiments" for everything, personal or commercial. (I believe `email`

and `url`

can vary?)

### The new publisher portal

![](../../assets/db508961a7c4b74f.png)

...requires submitting **new** packages from 2019.4 or higher. Only updates are allowed to go as low as 2018.4.

![](../../assets/2a1bc7ccb397e9c8.png)

And now the store itself will also follow LTS version. Store will **not **accept packages using LTS version that had already fallen off the support. [More info here](https://forum.unity.com/threads/asset-store-following-unity-editor-lts-cycle-final-call-for-2018-x-please-update-your-assets.1014994/?_gl=1*34dwow*_gcl_aw*R0NMLjE2Mzg1OTM5MTYuQ2owS0NRaUFuYWVOQmhDVUFSSXNBQkVlZThVQ0c5LXBYWU5iVVdabC1ySWtpT1NYWTlsZy1HNDJXQlBjTEFHYllLc05LTk9HNENWZEx6SWFBaVFsRUFMd193Y0I.*_gcl_dc*R0NMLjE2Mzg1OTM5MTYuQ2owS0NRaUFuYWVOQmhDVUFSSXNBQkVlZThVQ0c5LXBYWU5iVVdabC1ySWtpT1NYWTlsZy1HNDJXQlBjTEFHYllLc05LTk9HNENWZEx6SWFBaVFsRUFMd193Y0I.&_ga=2.3799097.865863714.1640504858-62677460.1628200887&_gac=1.121601530.1638593916.Cj0KCQiAnaeNBhCUARIsABEee8UCG9-pXYNbUWZl-rIkiOSXY9lg-G42WBPcLAGbYKsNKNOG4CVdLzIaAiQlEALw_wcB).

If you use lower than 2019 then your day is numbered!

### 2019.4 for life?

Other than mentioned, personally I think **2019.4 LTS **is the best home for all package developers for time to come. Unity finished modernizing packages with `asmdef`

and `package.json`

right here, missing just some Package Manager upgrades. It will be the new Unity 5. All my packages will be staying in 2019.4 LTS for sure!

Note that due to "store following the LTS" policy, this would soon move to 2020.4 LTS in the next year as 2019.4 fell off.

## Providing extra features on new versions

You may want to commit to provide extra features on newer versions, which translated to having to maintain `#if`

in your code. For example though lowest version is 2019, if 2020 is used, it gives you a bit more features but not critical to usage.

This goes beyond Unity version now that Version Defines based on package is available. Unity Timeline package [version 1.5.2](https://docs.unity3d.com/Packages/com.unity.timeline@1.6/changelog/CHANGELOG.html#152---2021-01-08) for example, has a lot of editor functions added that it is possible to script C# to pop open a Timeline tab. I want to have a cool button that use these functions.

However, Unity 2019.4 that I decided to stay on comes with Timeline version 1.2.18 verified.

In my `package.json`

, I can either :

- Say that it needs Timeline 1.5.2 as a dependency, then I can be free of preprocessor directives and no Version Defines.
- Say nothing about Timeline dependency or explicitly states 1.2.18 which comes with Unity 2019.4, then use Version Defines to check and enable an extra define. This is then used to render that cool button in my editor code, otherwise the button is greyed out or invisible.

![](../../assets/2de2d4cacd1cd677.png)

![](../../assets/875efc268149a1e5.png)

The preprocessors are notorious for wrecking with refactors, keep in mind. You no longer have a peace of mind using tool like Rider to refactor things as it doesn't go into deactivated section of the code. Resulting in surprise error report from users when you didn't go check on all versions which would trigger defines differently **after any refactors**. (i.e. Refactoring is now a potentially breaking change until you actually check with all supported versions.)

## Publishing gotchas

Here are extra tips related to Unity Asset Store Tools and the new Unity Publisher Portal.

### Checkbox of doom (?)

![](../../assets/b8972ba477297d15.png)

The 3. checkbox seems to promise compatibility with GUID reference in your `.asmdef`

. But according to [this forum post](https://forum.unity.com/threads/asset-store-year-in-review.1217736/#post-7770552), I think it is best that you **don't check this box **for now, for many reasons. (lol)

### Marketing image dimensions

![](../../assets/cc43d986f03af25e.png)

The new uploader does not reveal required dimension of marketing images nor how many would be needed **until** you drag something onto it. Therefore, I will show you the resulting dialog after dragging right now.

![](../../assets/d36dd4cc42d46543.png)

Best to match the dimension to these. When you check the bullet, only **Social media image **requires that you don't put any text or logo on it.

### Screenshots dimension

![](../../assets/9364d49710b6dcc4.png)

This one is a bit trickier, since it says "min width 1200 px". So what size should we use?

The answer is **1950 * 1300**. The reason being that these images are shown after **Cover Image **in the previous section in the carousel UI. If they are of different dimension than this, (grey) letterbox on top and bottom would be added and the image is centered vertically.

### How the Social Image looks like as `ogimage`


When people share the Asset Store link via Facebook or Twitter, the Social Image (1200 * 630) (that they told you not to add any text) would be used as `ogimage`

in the "card".

Here is the original inside image editor program.

![](../../assets/88bd0c743b40282c.png)

Here are the results :

![](../../assets/7073d607e81cc0bb.png)

![](../../assets/171e5ee64d64f0a9.png)

![](../../assets/42374883c9d889c3.png)

As far as I tested, that dimension translates quite well!

### Page indicator on screenshots

![](../../assets/3d47e48912332418.png)

In that 1950 * 1300 pixels, Unity will put page indicator **near the bottom edge** (Including the Cover Image). It is best that you don't fill important graphics to the brim especially if they are text. In my product here, I pad only the bottom edge up a bit.

The **padding **from the bottom edge of your graphic to the bottom edge of that page indicator is **35 pixels**. The height of that page indicator is **48 pixels. **Counting padding 2 times plus the height, total padding should be 35 + 48 + 35 = **118 pixels **to get padding similar to my example.

### Folded technical details

![](../../assets/a281f491e06b3250.png)

Previously, Asset Store not only require us to write HTML tags to style things and also it only got one description area. Now they have added "Technical details" section you can add more texts.

To keep in mind that this section is folded by default. So make sure to put all the important ones in the "Description", like your contact details.

### Publishing queue

![](../../assets/9c44a54b34dbfa34.png)

If your package is new, it takes a month to be reviewed. (As opposed to an update which is faster.) The new Publisher Portal also show where you are in the queue, you can edit the package without losing queue position. However, I had seen my queue number goes **up, **so don't take this number too seriously.