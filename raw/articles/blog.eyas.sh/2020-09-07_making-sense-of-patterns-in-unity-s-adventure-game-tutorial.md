---
title: Making Sense of Patterns in Unity's Adventure Game Tutorial
url: https://blog.eyas.sh/2020/09/patterns-in-unity-adventure-tutorial/
author: Eyas Sharaiha
published: '2020-09-07'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

If you recently went through or reviewed the 2016 Unity
[Adventure Game tutorial](https://learn.unity.com/project/adventure-game-tutorial)
and left with more questions about their design choices, this article is for
you. Likewise, if you’re interested in the very different patterns you can use
with `ScriptableObject`

s, you might find this of interest too.

Two cases of interest here are how it models an RPG game’s “Conditions” and
“Reactions” both as `ScriptableObject`

s. But each piece of the game is modeled
very differently:

## In-scene collections *versus* Asset-based collections

The tutorial represents various game conditions (e.g. “has a certain key item
been picked up?”) within a `Condition`

ScriptableObject. This object type is
referenced very differently in two places:

- When interacting with an NPC, a collection of conditions representing the
*desired state*a player needs to get a given reaction is a ScriptableObject called`ConditionCollection`

, that is stored*on*a given scene, and solely referenced within an`Interactable`

MonoBehaviour. - The global collection of conditions representing the
*current state*of the game is represented as a ScriptableObject called`AllConditions`

stored as an asset. All individual global game conditions are stored within that asset.

Representing all game conditions within a single `AllConditions`

asset sounds
appealing: containers of ScriptableObjects let you avoid having *too many
disparate related assets* within a project. Modeling each “Condition” within an
RPG game in its own asset file at least *feels* like an overkill. Having a
single asset (with a neat editor) you can look at in the inspector to find out
the player’s progress throughout various game conditions/milestones is likely a
huge win.

A `ConditionCollection`

on the other hand is a collection of *desired
conditions* for a specific interactable in a specific scene/setting. Storing
that globally could be confusing, as well as litter the global asset space with
details that are *actually* tied to a particular game object and scene.

Unity doesn’t have an easy way to reference sub-assets within its built-in
object pickers. This is part of why a `ConditionCollection`

created and stored
its own conditions in-scene, rather than reference global conditions and
indicate their desired state in a serialized struct on the MonoBehaviour. If you
have more time on your hands to write a nice property drawer, you can probably
do away this duality of Conditions as representing both *current states* and
*desired outcomes* depending on where they live.

`MonoBehaviour`

as a wrapper around collections

The tutorial also represents various reactions (e.g. “set this item as picked
up”) within a `Reaction`

ScriptableObject. This object is referenced in a
`ReactionCollection`

*MonoBehaviour* — literally just an array of `Reaction`

objects, each created within a Scene.

On the one hand, attaching `Reaction`

s to a scene—rather than saving them
in global assets— makes sense. What an NPC does in one scene is probably
specific to that scene.

On the other hand, if we’re putting these objects within other objects, why not just create a Serializable class or struct declared inline within our containing asset (Prefab or ScriptableObject)? And does modeling data within a MonoBehaviour make sense?

![Inspector Screencap showing a GuardInteractable GameObject in Unity's RPG Adventure Tutorial](../../assets/8c0dff22b791a81c.img)

In the above example, each “Reaction Collection” pointed to in the
“Interactable” MonoBehaviour is another MonoBehaviour in the scene that only
houses an array of `Reaction`

ScriptableObjects.

Why not just put that array right in the Interactable? Perhaps to write a custom
editor for these collections. But then, why not write a Serializable struct
representing a reaction collection, and writing a custom property drawer for it?
Part of the answer, I think, is just developer/designer ergonomics: you want
named reaction collections that more than one condition can reference (which you
can achieve with MonoBehaviours *or* ScriptableObjects), *and* you want each set
of potential reactions *within* your scene hierarchy.

If this sort of thing appeals to you, and the overhead of adding an in-Scene GameObject with no runtime purpose is not a factor for your design, then this might be a reasonable structure.

On the whole, the tutorial is a great mine for interesting design patterns. You
might pick some to borrow. You might also look at a few to decide what you
*don’t* want to do. In all cases, though, understanding *why* these choices were
used and presented can help you as you architect various pieces of your game.