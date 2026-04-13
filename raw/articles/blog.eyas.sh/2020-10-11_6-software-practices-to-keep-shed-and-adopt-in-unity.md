---
title: 6 Software Practices to Keep, Shed, and Adopt in Unity
url: https://blog.eyas.sh/2020/10/unity-for-engineers-pt2-six-practices/
author: Eyas Sharaiha
published: '2020-10-11'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

This is the second installment in my article series,
** Unity for Software Engineers** (now
updated and

[available as a book](https://leanpub.com/unity-for-engineers)). Check out the first article about

[six fundamental concepts in Unity](https://blog.eyas.sh/2020/10/unity-for-engineers-pt1-basic-concepts). I’ll be releasing additional installments over the next few weeks, so

[make sure to subscribe](http://eepurl.com/gVgusL)for updates. The series especially tailored for those who learn best as I do: starting with first principles and working your way upwards.

Software Engineers starting with game development are often looking for best
practices and idiomatic techniques. You’ll find some authoritative sources of
idiomatic development from [talks](https://www.youtube.com/watch?v=6vmRwLYWNRo)
in Unity’s [Unite conference](https://unity.com/events/unite), posts on the
[Unity blog](https://blogs.unity3d.com/), and members of the community like
[Jason Weimann](https://www.youtube.com/channel/UCX_b3NNQN5bzExm-22-NVVg). But
game development isn’t just engineering; it’s also an art. This sometimes means
that *getting something to work* takes center stage. You might find a lot of
advice along the lines of “do what works”, which, while it is valid and helpful,
doesn’t quite send you down the right path when you’re still learning.

Below, I put a brief list of Software Engineering practices you should **shed**
when starting with game development, those you should **adopt**, and those you
should **keep**.

*Shed:* Keep it all in code

In Software Engineering, it often feels like the more you represent in code, the better off you are: you can analyze your code to find references, jump to definitions, etc. A Software Engineer might be inclined to represent their scenes, objects, and most of the game in code.

But you’ll probably want to get used to leaning more on the Unity Editor UI than you expected.

By simply setting a “Patrol Position” to an empty Game Object, you’ll already have a neat visual game editing experience.

The Unity Engine does a lot of heavy lifting in its serialization/deserialization code and in asset management. If you’re programming in Unity (at least when getting started), you’ll want to swim with the current.

Game design is also inherently visual, *usually*. Placing your objects in 3D
space, constructing guard patrol paths, or setting up a field-of-view for those
guards are all easier done while visually editing a scene than by writing down
the coordinates imperatively. What’s more, if you need to modify these values
later, visually doing so is less error-prone.

*Adopt:* Write your own Custom Editors and Property Drawers

Along the same lines, one of the first things you should make a habit of doing is to make sure your custom components, property types, and assets feel like first-class citizens in the Unity Editor.

Have your own “Float Range” struct? Why not make sure you can manipulate it in the Editor with sliders that guarantee the min is always smaller than the max?

Have a `MonoBehaviour`

with mutually-exclusive fields? Write a custom editor for
the `MonoBehaviour`

that displays them how you want.

Rolling your own Dialogue Tree? Represent that as an asset and write a custom editor for it.

Custom Editors are not just a great way to make your objects editable as first-class citizens; they can also be a way to make sure your objects are debuggable and testable as first-class objects. Write an editor that shows you some of your object’s internal state when in play mode, or add a button to your editor that triggers a state in a controlled way (e.g., an “I got hit” button).

![Custom Property Drawer for Interactable Effects](../../assets/5f8c12e004c773c6.img)

An example “Interactable” component allows setting effects when the player initiates an interaction.

**See more** in the Unity docs on
[Custom Editors](https://docs.unity3d.com/Manual/editor-CustomEditors.html) and
[Property Drawers](https://docs.unity3d.com/ScriptReference/PropertyDrawer.html).
The [Brackeys Editor Window video](https://www.youtube.com/watch?v=491TSNwXTIg)
is also helpful.

*Keep:* Singletons tend to be a code smell

If you’re following game development tutorials or seeing discussions in forums, you’ll see singletons everywhere. But for much the same reasons as in Software Development, the singleton pattern is often inflexible, untestable, and has the potential to tangle your dependencies.

*Shed:* Get comfortable with some globals

It might be tempting to be very strict about always encapsulating state and
fully separating concerns. In game development, though, I find it helpful to get
comfortable with the idea of *slightly* more state sharing than you would like
in some other software system.

Part of this might be because there truly is more global state in games (e.g., has the first level boss been defeated, has the first town been saved, etc.?)

But I argue that even states that you can encapsulate might benefit from being a little more global. For example, you can encapsulate an HP variable within your Player component and use it to drive logic. You would also need your Player component to control HP display in the UI, and maybe screen-shake effects when the player takes a hit. On the other hand, having a global “Player HP” variable that you can pass to the player, a HUD object, and a screen-shake VFX object might be a cleaner alternative.

*Adopt:* The Inspector can be your injection framework

I alluded to this above, but I think the way you can have clean globals can be a
streamlined form of dependency injection. If a player requires a global *Player
HP* value, let the component reference an HP serialized field and pass it in the
inspector. You’ll get some of the nice things about DI (stubbing in a test,
isolation), without much of the “magic” that makes it so intimidating to use.

**See more** in
[Ryan Hipple’s talk on Scriptable Objects](https://www.youtube.com/watch?v=raQ3iHhE_Kk).
If you’d like to learn more about Scriptable Objects, I wrote
[about their serialization](https://blog.eyas.sh/2020/09/where-scriptableobjects-live/) and
[surveying their uses in a Unity tutorial](https://blog.eyas.sh/2020/09/patterns-in-unity-adventure-tutorial/).

*Keep:* Unit- and Integration Tests are Always Good

It’s easy to spend many months reading about game development & best practices
without reading discussions on test frameworks. Unity provides the
[Unity Test Framework](https://docs.unity3d.com/Manual/testing-editortestsrunner.html)
to this end.
[This tutorial by Anthony Uccello](https://www.raywenderlich.com/9454-introduction-to-unity-unit-testing)
provides an overview of how to get started.

![Person playing Nintendo Switch](../../assets/8b826763f3e313c9.img)

# Closing

So far, in the series, we covered
[Unity fundamentals](https://blog.eyas.sh/2020/10/unity-for-engineers-pt1-basic-concepts/) and
*some* intuition on the practices to lean into. Next, we’ll cover how to orient
yourself around the Unity Editor and go over the bare minimum you need to know
to unblock yourself as a solo programmer working with
[lighting](https://blog.eyas.sh/2020/10/unity-for-engineers-pt6-rendering/),
[animations](https://blog.eyas.sh/2020/11/unity-for-engineers-pt9-animation/),
[input](https://blog.eyas.sh/2020/10/unity-for-engineers-pt3-input-system/), and other Unity tools.