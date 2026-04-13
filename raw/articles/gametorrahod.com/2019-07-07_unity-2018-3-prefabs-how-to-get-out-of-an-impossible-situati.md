---
title: 'Unity 2018.3 Prefabs : How to get out of an impossible situation'
url: https://gametorrahod.com/unity-prefabs-impossible-situation/
author: Sirawat Pitaksarit
published: '2019-07-07'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

Unity's new prefab workflow introduced in 2018.3 is very powerful. But there are still some rough edges where the system conflicts with itself on object ordering.

We will completely disregard component and field overrides. Just pure `Transform`

and ordering which is quite important if they are uGUI prefabs.

## Demonstrating how to get into an impossible situation

This article assumes you know the rules about restructuring prefabs and how you cannot reorder what's coming from the parent prefab, but can order the additional game object added to it (that's with the + sign). And new things could only appears under all the old things ordering-wise.

Here is an example situation. I want to have a base `Canvas`

which I planned to use to for the entire game, becoming various variants along the way. But they will all link to this one.

Later, I realized that I want to **always** have one full stretch rect ready to put things in, where its side is able to pad in according to device's safe area. (Using [Notch Solution](https://github.com/5argon/NotchSolution)) What if I have already made something based on the old ones? Supposed at first I made my title screen canvas based on it.

![](../../assets/c8135c5400241d65.png)

I added a place holder called `SafeAreaPadding`

, so all variants could put their own things inside. I go add it to `V2Canvas`

and press save. This is what happens :

![](../../assets/cb366b124c3463b3.png)

So, who decided that the new `SafeAreaPadding`

should appear **before or after **all my things? This is already **an** **impossible situation**. Why? Enter the variant and see :

![](../../assets/fbc3343dd7c22cbd.png)

Demonstrating some reordering :

![](../../assets/b3f87f605ed5827e.png)

![](../../assets/0fcd5ec47e98786c.png)

You see that all my things decided to stay before the new stuff. By dragging down to below the new `SafeAreaPadding`

which came from parent, you are still in the rule because ordering mess-up from the parent apparently **ignoring the rules.** After a valid restructuring, turns out you cannot go back because that is violating the rules. The state you came from is **an impossible situation.**

I read it from somewhere in Prefabs forum that Unity team came to answer. The current "workaround" is that you must **plan ahead carefully **and create a prefab placeholder for future changes. Creating it later risks something like this.

Supposed that I was not that short-sighted and I add the `SafeAreaPadding`

before starting the other variants. Is this good enough? No, I was still short-sighted, realized long later, sometimes I need a dark dimmed background that I don't want to pad according to safe area. By the rule of uGUI ordering that affects draw order, I am now locked out from inserting anything before `SafeAreaPadding`

. So the correct solution is that I must have one more `FullPanelBeforePadding`

before that.

![](../../assets/c5e4ed2f6f8c8d27.png)

You could see where this is going, the problem could accumulate anywhere on the hierarchy no matter how well you plan things out. Everywhere you planned something, there is a space before it that got locked out.

Turns out, to make a "safe" base you need a before-after of everything just in case. The full panel before and safe area padding example is just a simplification from my real game.

![](../../assets/12d0469547ef921e.png)

Here is the "2nd level base" which is a variant from that `V2Canvas`

. It is designed to be a base of several other canvas. So you see that the top `FullPanelBeforePadding`

and `SafeAreaPadding`

is locked out according to the rule. All variants could add things and reorder freely inside both because I planned carefully. Nice. For example there is a new full screen white texture in that `FullPanelBeforePadding`

to do a full screen flash, where it could not get in front of impotant things. I would not be able to do this effect if I wasn't plan it carefully enough.

However, the 2nd level of a plan is needed. I want to add a navigation, so I have to be paranoid whether something wants to be before that but after `SafeAreaPadding`

in the future or not? (Because the base 2 things are locked out now) There is a `- DialogCurtain -`

that is designed so all dialogs could activate and dim the screen. So I planned a parent object named `Dialogs`

for all variants to put things in freely and they would always be after this curtain. I advise you to always add `Scripts`

too, it is a place to dump everything that's not so uGUI and could be anywhere, like a `PlayableDirector`

, `AudioSource`

, etc. If you don't have this dumpster they will be at risk of "freezing the outer layer". Gotta keep them contained.

In the end I wasn't careful enough **again. **As I make the variants based on this one, the `Dialogs`

I thought I was careful, I ended up wanting all the variants to have the same starting set of dialogs, and could add their own to them. In order to make this design propagate to all the variants I have already made progress, I am risking getting into an impossible situation again but now in a deeper hierarchy.

![](../../assets/18e699e20be95a55.png)

Right, now there is a 2nd curtain because I want an another dim over the first one. For example the first one pops up a purchase dialog, then it need to pops up an another one that says processing your purchase. All the wait dialog needs to be in a correct order. So I instantiate more of the wait dialogs. Thanks to the power new prefab, all of them are quite modular and could be anywhere. Except that, ordering is now messed up in the variant.

![](../../assets/45a4cb9069f17182.png)

I have added just 1 thing the `ChallengeInfoPanel`

at the end of all those elementary dialogs I want everyone to have. But look carefully, somehow `TrialDialog`

is not in the right order! This is the **2nd kind of impossible situation**, where ordering is according to the "additional must come later" rule, but the ordering in between the originals is different on the variant. And worse, I could not fix this since I could not reorder them from my variant obviously, then when I reorder them from the parent (which I am able to) the ordering won't reflect on the variant. How could one get into this 2nd kind of impossible situation? To be honest I wasn't aware until I found out my dialog ordering is incorrect. It could be considered a bug.

It maybe difficult to realize when you are getting into this, but reproduction is easy. Follow this : create a simple variant. It is currently identical.

![](../../assets/ba0de901fa952355.png)

Add new things to the variant.

![](../../assets/cb0a607cc43276af.png)

If you reorder the original at this point, it is fine as expected :

![](../../assets/c7a355cdc6073368.png)

However, try to trigger the 1st impossible situation by adding a new things to the original :

![](../../assets/9f00ad54fc5e1660.png)

Now Unity is not that stupid, for example if you reorder the original like this it still (kinda) as expected, the new things are still bunched up together, the variants kinda ignores them and take the reorder from its parent :

![](../../assets/0f5aa524fb02939a.png)

I will define this variant as already broken the rule, **but still linked somehow.**

Revert back to the 1st impossible situation. Now I am trying to make the impossible situation to abide the rule **only partially. **I reorder like this from the variant :

![](../../assets/6c469d1de71e4f25.png)

Then in the original, order it again :

![](../../assets/ecc03cc1ee967bce.png)

![](../../assets/0452f836d85d89a6.png)

It is already showing some cracks. Next, abide the rule for the rest of variant's additional prefabs.

![](../../assets/b4f82aed8be5236c.png)

Back to the outside :

![](../../assets/42d4e136b4b36404.png)

You have arrived at **the 2nd kind of impossible situation**. Now, you are free to reorder the original one with out it affecting the variant.

![](../../assets/82f461398dd5aefb.png)

The variant is now abiding to the rule, but the ordering from parent is completely **unlinked**. It no longer updates correctly. And you cannot fix `C B A D`

on the variant because you are violating the reordering rule, but this wrong reordering was created from something that ignores the rule. You are now in a deadlock.

By both impossible situations jumbling together multiple times over multiple chain of prefabs and variants, it is possible to unknowingly permutates your variant chains to be something completely unexpected overtime with no way to fix it back.

## The `.prefab`

YAML file data structure

My idea is that if something is able to be in an impossible situation, that means there must be a YAML representation of that situation. By knowing how it looks like, we could get **in and out **of that situation at will bypassing the warning dialog, by directly editing the `.prefab`

file. (It's not a hack if you could get into a hack by official means..)

So first we have to learn. Then we apply the knowledge. Reverts everything back to this simple variant with nothing new :

![](../../assets/ba0de901fa952355.png)

![](../../assets/66e51c76e92a9184.png)

The important points :

- Look for
`m_Name`

for things. You will find it under`GameObject`

. Consider`GameObject`

a component which you could not see in editor. - The ordering is stored in
`Transform`

component and not`GameObject`

. You can see`m_Children`

. The numbers is linking to the other`Transform`

and not to the`GameObject`

. - Pay attention to
`m_RootOrder`

on each one. The`ZZZZZ`

got 0. Then`AAA`

`BBB`

`CCC`

got 0, 1, 2 respectively. - Reordering the
`m_Children`

is able to change ordering in editor, and it affects all variants. However switching around`m_RootOrder`

does nothing to the ordering. This must be one of the key that holds the consistency amidst of inconsistency, that we could recover back from impossible situation.

The variant looks like this currently :

![](../../assets/b13657508f805fdd.png)

So, the `PrefabInstance`

takes over `GameObject`

component completely. You could see several fields like `m_Modifications`

that powers the overriding system. This time, `500888...`

is linking to `GameObject`

as its target. GUID is of that `ZZZZZ`

prefab's `meta`

file.

Next, I will add some more transform to the variant, like this :

![](../../assets/771c38acfe730e47.png)

![](../../assets/b14ac407106db614.png)

I put that on version control, you could see the green bar what got added.

2 `GameObject`

and 2 `Transform`

got added as expected. `m_RootOrder`

is 3 and 4, as expected. **Remember this number 3 and 4.**

Before we go to the next step, when dragging things to Project panel to create a variant Unity will name it `___ Variant`

in the project, but keep the name you name in the scene. The name of a prefab could actually be linked too, but in this situation it is currently overridden. Because the name in the scene is not the same as in the project.

![](../../assets/e156b5e3dcb35fdb.png)

If you look at the name box in Inspector, you see the name bolded. But there is no space to right click and revert so they are back to be linked with one in the project.

![](../../assets/1c5abecdd3bb89c7.png)

If you got an OCD like me you want the name to be linked and consistent. Fortunately by entering Debug mode you could revert the name to be linked. This is quite annoying since creating a variant each time it starts out as overridden.

![](../../assets/26b397e96f526a1b.png)

Because this override is on scene level, what changed when we do this is that `m_Modification`

will disappear from your scene's YAML. Also remember that scenes and the new prefabs are essentially the same backbone. Your scene may as well be just a huge prefab.

![](../../assets/62edb07736180ef2.png)

Now that you know how the link between overrides and the YAML looks like, next, I add two more at the root to create an impossible situation on the variant, because the root now comes later than the added things.

![](../../assets/0d6fc0d09d884a1f.png)

![](../../assets/d844993ef6b325fd.png)

There is no change on the variant prefab. This is how the new prefabs works, the save may trigger a scary dialog about reimporting everything that uses it, but at file level, which one you pressed save, only that one changed.

So what chaned at the root? 2 new set of `GameObject`

and `Transform`

as usual. And 2 more was added to `m_Children`

.

Now realize this : 5 entries of `m_Children`

doesn't know about additional prefabs in the variant, obviously. What happen to the ordering if we rearrange this `m_Children`

, when looked from the variant's viewpoint?

![](../../assets/f0d91643a27c1dd6.gif)

It looks like the prefab could be ordered without caring about what got added later at all. This looks like **the 1st impossible situation**. How could the variant "stays" where it should be? What is that "should"? The answer is `m_RootOrder`

. Remember, they are currently **3 and 4 **on the variant. No matter what you change ordering on the root, they will be at 3rd and 4th. So that's how it works.

And of course, try changing `m_RootOrder`

on the variant works as follows :

![](../../assets/eff34d2ad811e99d.gif)

If the number is out of range it seems to be at bottom, if the same as other it seems to be ordered by... something. But you shouldn't do that anyways.

What's left is the **2nd impossible situation. **What will its YAML looks like? Let's start slowly from this situation :

![](../../assets/33f1e68810fa8a7e.png)

I will **completely recover **by moving the additional prefab on the variant to the bottom most, so it is back to consistent state because all additional things came later. What would be your guess on its YAML representation? `m_RootOrder`

changed from 3 and 4 to 5 and 6 was my guess.

![](../../assets/57b3a4e7752cb68a.png)

That's partially correct, there are more :

![](../../assets/5469b89a732621ba.png)

Up top of the file, the root order **did** change to 5 and 6. However there is an **override of m_RootOrder added. **This shows that the prefab system could have an override of hidden property we couldn't even see via Debug mode. And who's that

`fileID`

with the same `guid`

? Those two was once a victim of sorts of the inconsistent state earlier, the new two game objects from root that manages to be **under **things in variant, because they appeared from the root and ended up at the wrong place. `AdditionalRoot (1)`

and `(2)`

.

![](../../assets/ab9311b64c2fd2f8.png)

The meaning of this? By trying to restore to consistent state, seems like there is a lost civilization left behind in the form of an override of remembered root order. Like an evidence that this variant was once in an impossible situation. Like the variant is saying : "You two must be at root order 3 and 4 according to my viewpoint, because that's how it was.".

Of course, currently if you try removing this 2 overrides, it wouldn't make any difference since it is already at order 3 and 4, however not because of root order, it is because of `m_Children`

ordering. But if you remove that 2 additional prefab from the variant, save, and then add back those two **normally**, let them appear at the bottom naturally, you will not get the `m_RootOrder`

override as you weren't recovering from an impossible situation.

![](../../assets/db44c7fad37f7de9.png)

This `m_RootOrder`

override is indeed the one that enables the "disordered blue" situation from the **2nd impossible situation**. The override could reorder anything as they wish disregarding the original ordering.

Now the whole point of `m_RootOrder`

make sense, **it is a serialized property. **By making ordering a property, it now enters the same system as all other properties and could be overridden. It is actually the key to make the whole thing works consistently, unfortunately what we see from the Unity editor is the opposite of consistency, because no one knows that there is a property that governs ordering on top of previous system of ordering. And there is no visual representation of it in the editor so you could just right click revert and fix the problem. It's unfortunate, but now I don't even know if this should be a bug or "by design" to make the whole thing works. ([I did report it as a bug](https://fogbugz.unity3d.com/default.asp?1165214_lrtr97cnqs2k5ppi), and they said they could reproduce it, and nothing more.)

Therefore, back to my original sticky situation here. Let's use this newfound knowledge to fix it.

![](../../assets/aaa20a7d2b72e6e8.png)

![](../../assets/b12a2bcdf6d88711.png)

Recap : my training variant of my game selector somehow has the `Dialogs`

children out of order over the course of my development. Now when the user do IAP in my game, the `WaitDialogWhenProcessing`

appears behind. The real intention is of course, I want to order as I ordered on the base prefab.

Because we learned about the source of this problem, I know there must be an `m_RootOrder`

override somewhere in my training variant, that points to some game object in my parent game object.

By searching for `propertyPath: m_RootOrder`

I could find all such override. What's left is just trying to match to the correct game object and delete them.

However in my case I don't think I want to keep any root order overrides on this variant. So why not just obliterate them all instead of finding which one to delete? By using this unsightly handcrafted regex it is possible to match them all.

`- target.*\n.*\n.*propertyPath: m_RootOrder\n.*\n.*`


`- target.*\n.*propertyPath: m_RootOrder\n.*\n.*`


There seems to be the one with `type: 3`

on a new line for some reason. So I just match them twice. With VSCode regex search box, I could replace them all with blank lines, but it is not a problem. **BUT** **OF COURSE COMMIT YOUR PROJECT FIRST.**

![](../../assets/161021a9e60e686e.png)

I'm surprised there are a lot more of these junks than expected, but I decided to do a mass clean up to both the variant and the base one. I want to start over.

![](../../assets/b34dd44811d316b2.png)

![](../../assets/b9d746d1aca3588c.png)

But unexpectedly the ordering on the base one changed too. It must be through too many mess that the ordering that I considered correct, was actually a product of all those `m_RootOrder`

overrides that piles up like a plague.

Luckily, now that all overrides are gone, I could order the base one again as I wish and this time, can expect all the variants to follow because all root overrides cleaned up. So I think I want the wait dialog to be under `TrialDialog`

but it show up first when we wait for server connection, so after the wait, `TrialDialog`

comes in front of animate-closing wait dialog. But an another wait dialog is over all that when we actually process the IAP after a confirmation, and it should able to be there while the `TrialDialog`

is still open in the background, with an another layer of black dimmed curtain.

![](../../assets/a308a3cd4d75d623.png)

![](../../assets/0b1a9112346ad5eb.png)

Thank god, everything ripple updates as expected again! I took this opportunity to bunch up my directors and scripts together too. And the variant's more bunch and directors appears under them properly now.

But remember one more thing, even if you see the variants update because of the lack of `m_RootOrder`

in them, you also get back some `m_RootOrder`

on the base when you arrange back. So the drag around seems to not just reordering `m_Children`

as I hope, as my base is also a variant of an another prefab and therefore must follow the hidden "must left its legacy behind" rules we learned. At least we have a way of getting out of the mess now. (Or you *could* get into one intentionally, if you want a new variant that reorders its parent freely now that's possible too. Now that we know that's official and unlikely to cause crashes.)

Now if someone will write a "cleanser" editor script that does what I did... please share it to me. :P

## How would you design it UX-wise?

Why the current design is what it is? Because you reorder things in Hierarchy and not in Inspector, and the designer probably wants to abstract that away and make you think it is not an act of changing a prefab's integer property. And yes it **was,** because previously ordering is stored in the scene and you cannot really inspect the scene so there is no need to show it as a property. Ordering inside the prefab was taken care of with `m_Children`

because prefabs were only 1 level deep before 2018.3.

And why `m_RootOrder`

must exist in the first place? Maybe the designer wants to minimize "unpredictable ripple effect" caused by caused by adding new things to the base. (So that is part of the point of variants) This root order override gives the variant power to be the one to control ordering if they want. When you look at things from the base's viewpoint, how Unity supposed to know where exactly you **want** the new things to end up? Base technically have to **not **know any of its user so it is impossible to specify where they ended up at the variants. Therefore it is the job of variant to order and then that's `m_RootOrder`

.

The main problem is that this `m_RootOrder`

couldn't be shown explicitly in the UI, and you don't know which one is currently order-locked or still following the base, leading to frustrations.

If you are the designer, how will you show that the ordering was overridden? Will you show something on Hierarchy panel? Will you just add that number on Inspector? Will it add visual clutter to see `m_RootOrder`

needs to be bolded at some point?