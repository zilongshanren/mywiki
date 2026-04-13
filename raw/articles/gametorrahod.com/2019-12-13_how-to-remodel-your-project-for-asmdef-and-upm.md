---
title: How to remodel your project for asmdef and UPM
url: https://gametorrahod.com/how-to-asmdef-upm/
author: Sirawat Pitaksarit
published: '2019-12-13'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

In this article I will guide you to adopt `asmdef`

and (internal) Unity Package Manager in your **existing **project. It will be harder than if you do it from the beginning, but that's why I have written this guide. Also it is so that in the future, your new part of code could be in UPM properly for more orderly one-way reference.

This article assume you know [basic benefits of it](https://docs.unity3d.com/Manual/ScriptCompilationAssemblyDefinitionFiles.html) and how it works with folder structure to group your scripts. This article will start by going over some benefits that may not be obvious to you, so that you are motivated to do it.

## Benefits

- Compiles faster with the built-in incremental compiler. This is not even its full power, as I heard from the forum that Unity is prepping for no domain reload play mode enter and faster hot reload on script changes. That could be depending on how well you separate
`asmdef`

today. (A guess, but likely) Today, it do not affect enter play mode time unfortunately. - Allows you to name your folder that previously must be named exactly
`Editor`

as anything else, with**editor asmdef.**(But you should name them`Editor`

anyways..)To do this, make sure Any Platform is unchecked, then only Editor is checked for Include Platforms.

![](../../assets/2806bccda3da649e.png)

- Previously all your
`Editor`

folder scripts do not ended up in your game, now it is the same except that they could be separated by dll, decrease compilation speed for even editor code. - Test assemblies. They have their unique problem. To make an edit mode test assembly, do the same as editor asmdef except check that
**Test Assemblies**box. This is the same as putting tests in the`Editor`

folder.

However the real benefit is in making**the play mode tests.**Previously there is a problem that you want to test something in play mode the script must stay out of`Editor`

folder, then they will be included in the game too if not removed manually.

Now with that**Test Assemblies**check box plus non-editor setup, you get something usable in play mode**and even in real device test**but somehow**not in the real game build!**To get a special behaviour of allowing play mode test in the real build, press this button.

![](../../assets/003c0f4174023cc7.png)

Without `asmdef`

this button is also usable but they will also be in your game for real.

- As a bonus you could rank your script's weight at glance in
`Library/ScriptAssemblies`

. I once caught an error here when one of my plugins included a huge baked constants that I should remove.

![](../../assets/e9cd12ea3ce21a0c.png)

- Make you an organized, clean coder, since it will not allow you to make messy dependencies. In a way, this is a unit test for code organization.
`asmdef`

pave way to UPM, which could share code between your projects or even open sourced online. This is the ideal form of module based development, but for starters let's try to segment an already messy game into`asmdef`

without UPM first.- Will this make your game easier to hack when they could see all your dll separated up nicely? Maybe, but your single dll game is also hackable if the hacker wanted to see your symbols anyways.
- Earn additional income by prototyping a would-be/potential Asset Store items as a package with thier own
`asmdef`

in their own project. Field test them in all your real projects easily without copy, with UPM link and`asmdef`

link.

UPM warrants its own topic, which is not the same as `asmdef`

but closely related.

## Unity Package Manager is going full asmdef

![](../../assets/ddc7010be4b26a15.png)

For those who didn't catch up yet, we used to read Unity version release change log. Now they do it NPM style, each internal team that work on a feature could push an update on their own, each with its own `CHANGELOG.md`

. This is a great initiative! All these fun stuff available to play with. (And more bugs to report!!)

UPM works with `package.json`

at root of the package's folder much like NPM, but it is customary that you should do `asmdef`

also. The official pattern looks like this :

![](../../assets/8e1bd8922043f48b.png)

`Company.PackageName`

: For the main part`Company.PackageName.Editor`

: For the editor only part (references the main part)`Company.PackageName.Editor.Tests`

: For unit test / edit mode test (references the main part)`Company.PackageName.Runtime.Tests`

: For integration test / play mode test (references the main part)

For example, my plugin [Introloop](http://exceed7.com/introloop/) looks like this with an additional "Demo" assembly.

![](../../assets/b70b8b7f01bca22c.png)

Since my demo scenes has some debug scripts to show how things work. When my customer wants to use the plugin, if they adopted `asmdef`

already, they could include only non-demo part to their game. (If they don't, all non-editor `asmdef`

will be referenced like usual) Also it helps sanity check me that I don't use something in the demo from my main part.

I will explain to UPM your own game along the remodeling section. But first let's see some obstacles that you must overcome.

## Asmdefs are infectious

Your game completely devoid of `asmdef`

was perfectly fine. But your game **with just one **`asmdef`

became quite troublesome. (Maybe you just want that test assembly, maybe you want to do it only a little at first)

They are "infectious" (similar to things like `async/await`

programming) that if you don't do it all, you can't do it at all. To see why :

### Overviews to keep in mind

- Anything in
`asmdef`

are now**secluded**from the world, where previously it knows everyone. You have to link up`asmdef`

to get it to know each other. - Anything in
`asmdef`

still know all**precompiled .dll**like before. For example if you have Firebase Unity SDK which consists of closed source code packed in .dll, all your`asmdef`

has access to it. You don't have to link them up. Except one dll ... - Everything not caught in
`asmdef`

will be in the catch-all`Assembly-CSharp.dll`

. This .dll has one big problem :**none of your**It must be the terminal node of the "reference graph".`asmdef`

implicitly know this dll, and cannot explicitly reference it. Not even with Override References. - This includes if you decided to write a test in its test assembly while keeping everything else in the game as before (spilled out to catch-all dll) Now turns out the test cannot test anything, since the thing to test cannot be referenced to the test assembly. You face a dilemma because you don't want to ship test code either. Now you must
`asmdef`

an entire game, which brings to this article. - If you check
**Override References**it will remove the mentioned "know every .dll" ability and let you explicitly define each one. The box below will not appear if you didn't check it. "References" in this context meant .dll only, not`asmdef`

.

![](../../assets/a78b6013eec0950a.png)

- The link cannot form any circular dependency. This is the most common roadblock that make you give up on using
`asmdef`

and this article will advise how to avoid this. - This is why UPM package could be 100%
`asmdef`

'd and should be, because by nature**they are plugins**and do not depend on something specific to your game. The reference direction is one way : your project use the package.

Together, it cause trouble like these :

### Can't reference `Assembly-CSharp.dll`

problem

You only want to pack up your play mode test code in an `asmdef`

and not touch anything else in the project. But obviously your test code should at least check on something in your game, like if start at this scene and wait 10 seconds it should show this and that.

Sure, you can start a scene with `string`

, and wait, and then use magic method like `GameObject.Find`

to try to **blindly auditing **the environment without actually what they are. But these tests are brittle and break when you change the scene's content.

You want your test assembly to reference **anything else **but it is not possible to do it with `Assembly-CSharp.dll`

. Check mate, you delete the `asmdef`

and think this is a waste of time.

### The bridge problem

you see some folder that looks self-contained and would be nice to place `asmdef`

on. (For example "TitleScreen") By placing the `asmdef`

on just this folder and let everything else go to `Assembly-CSharp.dll`

, if any of the other scripts has a reference to things inside this TitleScreen folder, you are now out of luck unless you move it to the same `asmdef`

.

What could be these "bridge" things? The most common is something that interconnect scenes. You may have `SceneTransitionManager`

for example, which is like a `static`

hub that was designed that everyone could call and move to the other scene, **along with passing some data to the destination scene + clean up.** The everyone-could-call part is fine, but if you have something like `TitleScreen.options.noIntro = true`

in your scene transition, you are now shooting yourself with circular dependency.

Then you may think let's just move that into the TitleScreen's `asmdef`

. Now the other screen's asmdef have to link to TitleScreen's `asmdef`

for strange reason that they just want to access the utility. This is what I call "the bridge problem" since the bridge needs to know everyone, and everyone must call the bridge somehow, therefore the dependency is not one way and it prevents us from remodeling into `asmdef`

.

How to fix this problem comes later while we are remodeling together.

## The plan

- The most logical unit of
`asmdef`

for your game I think is**scenes.**(depends on game genre still) We will try divide the`asmdef`

equal to your scenes/screens. Like title, mode select, game play, credits, shop, etc. The name will be`Company.MyGame.SceneName`

. - Plugins + your own multi-project common code should all be thrown away to UPM and 100% wrapped in
`asmdef`

. If it errors after you do this, the plugin is coupled to the game and you should not call it a "plugin". - There is something called
`Company.MyGame.Core`

, which ALL scene`asmdef`

could reference**but not allowed to reference anyone else**except plugins. - There is something called
`Company.MyGame.Scripts`

that try to catch anything else not fallen into "Core" or any of the scenes. This is not allowed to reference any scene assembly,**but can reference the "Core".** - When you achieve all these, you
**will not see**`Assembly-CSharp.dll`

. Indicating that`Company.MyGame.Scripts`

had taken place, but this time it removes the "not able to reference`Assembly-CSharp.dll`

problem!

Example references :

![](../../assets/70c44b01118042bc.png)

The arrow shows explicit reference that must be specified on `asmdef`

. The .dll are implicitly known by everyone.

## Step 1 : UPM your Asset Store plugins / .unitypackage you bought

Most developers hadn't put either `package.json`

or even `asmdef`

yet. You could do this like so :

- Make a
**new**Unity project called "My Asset Store Plugins" or something. - Use Asset Store in the editor to download the plugins.
- Put
`asmdef`

in the plugin's folder accordingly. - Put
`package.json`

. Copy the pattern from Unity's official package. The version must be semver compatible (x.y.z) - Use Package Manager's
`+`

button to locate each local`package.json`

as desired from your game project.

![](../../assets/bb9e6fa31f26a52e.png)

This approach make it easy to update these plugins by coming to this **"plugin galore" project** and press update in Asset Store tab, so it overwrite files in their intended location, then the change will be reflected in ALL your games that use these UPM.

You should not get any errors even if no other part of your game became `asmdef`

yet, since all your things should be in `Assembly-CSharp.dll`

, and this dll knows all `asmdef`

(including one that came from UPM) and all other dlls. This is why this is a step 1. Go make sure your game compiles now.

For `.unitypackage`

, do the same thing except this time they didn't came from Asset Store, so you could put them wherever (even in a normal folder that is not Unity project! But you need a Unity project to unpack `.unitypackage`

anyways). I put them together in the same "My Asset Store Plugins" project as my Asset Store items.

For example, I was able to UPM the [Spine .unitypackage](http://esotericsoftware.com/spine-unity) by adding 2 `asmdef`

and 1 `package.json`

:

![](../../assets/04b745752f713ea7.png)

```
{
"name": "com.esotericsoftware.spine",
"displayName": "Spine",
"version": "3.7.0",
"unity": "2019.1",
"description": "2D animation for games.",
"keywords": [
"animation"
]
}
```


Then it will show up :

![](../../assets/5ea43c99cd14e556.png)

Some plugin cannot be a package since :

- They try to do something related to their script position, or write something to its folder (bad practice!) in that case you will see some errors as you use them. This doesn't mean you can't put
`asmdef`

. For example, I found that[I2 Localization](https://assetstore.unity.com/packages/tools/localization/i2-localization-14884)as UPM package throws something about writing file to somewhere as I use them. (It compiles) But I am able to put just`asmdef`

on and let it lives in the project. It is still better than nothing, just that if your another project want to use this you must copy, then update on each projects individually.

![](../../assets/7083fccce255b5f6.png)

One another instance is [Google Play Game Services (GPGS)](https://github.com/playgameservices/play-games-plugin-for-unity), where I could put `asmdef`

and let it be in my project. But once I tried to do UPM, it complained :

![](../../assets/0554abf6958f23b4.png)

Indicating that the plugin really wants that exactly named "GooglePlayGames" folder cluttered directly in yout `Assets`

. Ugh..

- The plugin contains tons of dll, which are useless to
`asmdef`

in the first place. Some example of these are[Firebase Unity](https://firebase.google.com/docs/unity/setup)and[Odin Inspector](https://assetstore.unity.com/packages/tools/utilities/odin-inspector-and-serializer-89041). You must let them sit normally in the project. .dll plugins aren't bad, in fact you are putting`asmdef`

so that they became little .dll. .dll plugins aren't recompiled together with your project, but more difficult to debug. - They are arranged in strange folder combination. For example has multiple
`Editor`

folder sandwiched in multiple subfolder that you think it is a hassle to arrange them and have to do it again on the next update. - They wants to be in a special folder like
`Plugins`

. In this case, since you could have only one`Plugins`

folder in your project you cannot use UPM.

You could try putting`asmdef`

regardless inside the`Plugins`

folder and if it works, it means it doesn't really need to be in`Plugins`

folder! One example is[Maintainer](https://assetstore.unity.com/packages/tools/utilities/maintainer-32199), which is an editor-only plugin. I could left that in Plugins folder in my "My Asset Store Plugins" project, then from my game link to`package.json`

inside that`Plugins`

folder. You should not pull it out of`Plugins`

even if you know they work regardless, since it will be easier to update from Asset Store if you keep the same shape.

![](../../assets/ccb6719de2a4e1b7.png)

### Take .meta files with the package!!!

The `.meta`

file contains GUID which actually links things in the scene that use these scripts to the actual script. If some day I moved my Asset Store code somewhere without copying `.meta`

file, I am breaking all my customer's existing projects.

Think of it as the identity/lifeline of each of your file. You can rename the code's file name as long as you also rename the `.meta`

file (this is automatic if done in Unity editor), or else it will destroy the `.meta`

file and generate a new one. **This is a serious problem.**

The only somewhat negligable case is `.meta`

file of folders. But those are still serializable by something like `UnityEngine.Object`

on your `ScriptableObject`

. It could still disconnect! For example my in-development plugin contains a feature that remembers folder to scan its content. If this folder's `.meta`

file changes it won't be able to locate the same folder since all it did is actually just remembering the GUID, not the actual folder.

![](../../assets/6e43c3dc28b164ce.png)

![](../../assets/a134f9cd44fd3ab8.png)

## Step 2 : UPM your own shared code, internal or not

You may have only 1 game in development now, but as you develop please always try to think "could this feature stand on its own?"

All my plugins [Introloop](http://exceed7.com/introloop/), [Native Audio](http://exceed7.com/native-audio/), and [Native Touch](http://exceed7.com/native-touch/) are all solution to some problems in my game. However I realized they could stand on their own and be reused on my future projects. Right now, that future project turned out to be other people's projects! They are able to be distributed on Asset Store thanks to portability ensured by UPM, plus field tested by them included in all my games with ease.

Even if you aren't going to sell them you still should. For example I have a collection of "fun stuff" called `E7.Unity`

where anything goes. So let's name your thing, probably use `namespace`

practice correctly, and put in those `asmdef`

and `package.json`

.

### If your plugin sounded epic enough to be sold on the Asset Store

Put them in its own separated Unity project. Your game project has the priviledge of yoinking it directly locally by locating `package.json`

inside instead of pulling from Asset Store. This way you could run your plugin's test scene in its own project, which is useful to check integrity when upgrading Unity version. Then you could "dogfooding" the plugin with your own game because it is linked via UPM to only you, not your customers.

[Native Audio](http://exceed7.com/native-audio/) is in its own project, which is sold on the Asset Store. In this case, you should version control the **entire project **because its for your private use. Then inside it `AssetStoreTools`

is for submitting. Then inside a folder of your plugin could contains `package.json`

and `asmdef`

.

![](../../assets/f303d6ac156b6735.png)

### If your plugins aren't epic enough to be sold

You maybe able to use GitHub integration to bring them online! The requirement is that they must be a public repo, so not for those you are going to sell. And also `package.json`

must be at the root.

You can put them together in a new Unity project called "My UPM Packages" or similar. In this case, you should **version control each folders in your Assets folder.**

![](../../assets/9448074640f38269.png)

Or you could put it in its own project. In this case don't version control from outside of `Assets`

but do it inside.

![](../../assets/d9bb5d4f8b447324.png)

Put `README.md`

near `packages.json`

and `asmdef`

too. Ok, putting `.git`

there may risk losing the `ProjectSettings`

. But trust me GitHub integration is way cooler.

Either way, when you push them you should get a landing page with `package.json`

visible from the **front page** together with the `README.md`

. If you could get this, your GitHub package is now UPM compatible. If you put `.git`

outside `Assets`

, you will not get this layout.

[https://github.com/5argon/E7Unity](https://github.com/5argon/E7Unity)[https://github.com/5argon/NotchSolution](https://github.com/5argon/NotchSolution)

![](../../assets/092922ef9d804324.png)

![](../../assets/f213d94357999729.png)

To pull, you must add an entry manually (by Unity 2019.1) in `manifest.json`

. The format is a combination of what you put in `package.json`

on the left, then URL on the right. For example :

`"com.e7.notch-solution": "git://github.com/5argon/NotchSolution.git"`


If you want to pull again it is not automatic. Look at the bottom of `manifest.json`

and remove the package's `lock`

.

Not only it is online and you could share with friends, you could get contributors and pull requests! My [Notch Solution](https://github.com/5argon/NotchSolution) which sounded epic but I decided to be not for profit ended up having multiple contributor helping me to fight the notched phone.

### From now on starts any new component on UPM

To avoid this hardship of trying to `asmdef`

and UPM existing game, the next "module" should start from UPM and link it to your main project. Great, great benefit of your internal UPM package even the one you didn't plan to share with the world includes :

- Occassionally you upgrade Unity or some important plugins, and now everything turns red. If you develop in UPM, you can open those
**individually**and see if the red errors came from them or not. Keeping your sanity and let you fix part by part. Your game is now a multiple Unity project where other little project is a shell that imports just one internal UPM you have developed. - The fastest ticket to bug fixes. You can write a self contained unit tests in your UPM package. And when you suspect Unity bugged, that would make your test turn red. Usually you don't want to submit a bug report since you don't want to upload 30 GB of art assets and you got no time to make a reproduce project. But now you can submit your UPM package that would be less than 1MB of pure code, and just tell Unity team to double click on some test and see it goes red. The turnaround time will be impressively fast because they will be happy to fix this self-contained, concise problem, that they have just one goal to make the test go to green again. In summary, it will reduce the hopelessness to wait for bug fixes.
- Each one has its own version control, great for time traveling and experimenting without affecting other modules.

Some example where you should do this. If you are making a button in your game which plays different sound on pressing down and up, a UPM package of this maybe probably too much of a hassle. However if you want to add a "stats and achievements" summary screen to motivate your player in the next update? This kind of thing is ripe for a lot of bugs and you want to make sure just this section works correctly for any data thrown at it. This would be a good candidate for internal, code-only UPM.

### Results of Step 1 and 2

You have cleared up stuff from your `Assets`

to `Packages`

down below, even if your main game hadn't used any `asmdef`

yet. Save for some pesky plugins that are either dlls or immovable and must stay there, they will ended up in `Assembly-CSharp.dll`

and can't be helped.

![](../../assets/6cd129c8357f7897.png)

Let's recap that we just did the green part on the right here. All your scripts are still in `Assembly-CSharp.dll`

together with non-UPMable scripts, which knows `asmdef`

coming from UPM and from "plugin that could `asmdef`

but couldn't UPM" in the project, implicitly. That's why I didn't draw the arrow from `Assembly-CSharp.dll`

to UPM packages, which is for explicit references.

![](../../assets/70c44b01118042bc.png)

The hard work is coming next, plugins are separable by their nature. Not the same for your game scripts.

## Step 3 : Determine the Core

Setup your folder like this.

![](../../assets/4141382d3e1feafc.png)

The `Assemblies`

is the catching net with `Scripts`

assembly, no other scripts in the project may be outside of `Assemblies`

, but ideally **in the end **you **should not **let anything escaped from its own folder to this `Scripts`

assembly! Instead, look at TitleScreen. Everything will be caught in its own assembly. But right now is still not the end though, you will gradually work on the transition to `asmdef`

this way.

Right now only my TitleScreen falls into its `Title`

assembly, and all other scenes are at the `Scripts`

catch-all assembly. The `Scripts`

serves one more purpose, unlike letting them go to `Assembly-CSharp.dll`

this one is referencable. Even if in the end you should have nothing in `Scripts`

, right now you solved one problem : your play mode test assembly could now test on **all** scenes by linking that `asmdef`

to `Scripts`

, even though you just started migrating just your title scene to `asmdef`

.

The **Core **folder is inside this `Assemblies`

folder, **but you should view it as the outmost! **Since we made a rule that it couldn't reference anyone, not even `Scripts`

. (But it could go to plugins UPM `asmdef`

)

Now, you have to solve this problem : Make this 3 `asmdef`

works `SceneName`

`Scripts`

`Core`

. You will immediately see errors if something in the `Core`

goes the opposite way. So it's time to refactor your code to determine what could be in the `Core`

as much as possible. And this involves "the bridge problem" earlier.

### How to fix the bridge problem

Let the bridge contains a part of everyone instead, and everyone use this data pool. The bridge still didn't reference anyone but somehow magically knows who is going to come. Then everyone use the bridge.

For example if this problematic bridge is the `ChangeSceneManger`

which was doing load scene with scene name defined in the now-separated assembly. (e.g. the manager knows how to go to Title or ModeSelect, but now the scene name are inaccessible since they go to those assembly and one way reference is preventing us.) Instead, you move just those scene's name to the bridge. It feels wrong, but fast to implement.

This is an example of mine, it has superpower to define a placeholder variable for all the scenes to write to, but no, it do not reference any of these scenes. It is those scene `asmdef`

that should reference this bridge code. Let's say we have cheated the dependency system. Title scene knows how to look at its own section and do what it should. The bridge assembly can set things into this part without knowing what the Title assembly will do about them.

```
using System;
public static class SceneOptions
{
[Serializable]
public struct Title
{
public enum TitleMode
{
WithoutIntro,
WithIntro,
SkipToModeSelect
}
public TitleMode titleMode;
}
[Serializable]
public struct Result
{
int p1Score;
int p2Score;
bool challengeCleared;
bool withoutScore;
}
}
```


It is a price to pay for remodeling a project for `asmdef`

+ UPM deep into the project.