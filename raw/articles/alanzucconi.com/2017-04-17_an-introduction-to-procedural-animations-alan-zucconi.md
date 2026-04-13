---
title: An Introduction to Procedural Animations - Alan Zucconi
url: https://www.alanzucconi.com/2017/04/17/procedural-animations/
author: Alan Zucconi
published: '2017-04-17'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This discussion introduces a new series about **inverse kinematics** for videogames. Before starting our journey, this post will show a few games that use **procedural animations**, and how they differ from traditional assets-based animations.

![](../../assets/ef6b390d1b154e7a.gif)

You can find all the other parts here:

- Part 1.
**An Introduction to Procedural Animations** - Part 2.
[The Mathematics of Forward Kinematics](https://www.alanzucconi.com/?p=6142) - Part 3.
[Implementing Forward Kinematics](https://www.alanzucconi.com/?p=6170) - Part 4.
[An Introduction to Gradient Descent](https://www.alanzucconi.com/?p=6133) - Part 5.
[Inverse Kinematics for Robotic Arms](https://www.alanzucconi.com/?p=6135) - Part 6.
[Inverse Kinematics for Tentacles](https://www.alanzucconi.com/?p=6180) - Part 7. Inverse Kinematics for Spider Legs 🚧 (work in progress!)

At the end of this post you can find a link to download all the assets and scenes necessary to replicate this tutorial.

#### Introduction

Character animations are, in most games, “static”. Every time a character moves on screen, an artist has created that particularly movement. Whether it was crafted by hand, or recorded using a motion capture suit, animations are predefined **assets**. When a character needs to perform a different movement, a different animation is required. This way of approaching characters movement is pretty standard in the game industry. Large and comprehensive collections of animations are often available, and they well cover the most common behaviours such as walking, jumping and shooting. Traditional animations dominate the game industry; although there are equally valid alternatives. If you dare venturing further, let me introduce you the concept of **procedural animations**.

The basic idea is that the moments of a character can be generated procedurally. One of the most common technique to generate animations procedurally, relies on simulating physics. This often takes the name of **physically based animations** ([Wikipedia](https://en.wikipedia.org/wiki/Physically_based_animation)). A typical example is water; you can animate it by hand, or rely on a simulation that takes into account **fluid dynamics**.

In the rest of this post we will discuss a very specific subset of physically based animations, which relies on rigid body simulation. This is the same kind of simulation that game engines like Unity and Unreal normally use. Let’s see how such a basic feature has been used in games to create physically based animations.

#### Ragdoll Physics

At the very heart of physically based animation lies the idea that character movements can be simulated. By replicating the processes and constraints that govern the human body, it is possible to approximate realistic behaviours. One of the most simple, yet effective way to do procedural animations is by using **ragdoll physics **([Wikipedia](https://en.wikipedia.org/wiki/Ragdoll_physics)). The idea is to create a humanoid body, and to connect each limb with joints that replicate the degrees of freedom that their real counterparts exhibit. Just by relying on rigid bodies physics and joint constraints, it is possible to simulate how a person would fall. This does not only save budget on a “dying animation”. It allows to have characters that realistically fall and interact with their surrounding. Such a task would be nearly impossible to replicate by using a predefined set of animations; no matter how accurate they are.

The biggest disadvantage of ragdolls is that they are highly unpredictable, and often result in accidentally hilarious behaviours.

![](../../assets/4b2ab4baa288d739.gif)

Nowadays ragdolls are pretty standard in games. Unity comes with a simple tool, the [Ragdoll Wizard](https://docs.unity3d.com/Manual/wizard-RagdollWizard.html), which allows to quickly turn a humanoid model into a ragdoll.

**Rigid Body Simulations**

The main problem with ragdolls is that they lack any motor control. Connecting limbs with joints does cause them to walk, or jump. Only to fall. There are situations, however, in which a mixed approach can be used.

In the article [How Grow Home Uses Maths To Generate Personality](https://www.rockpapershotgun.com/2016/09/23/how-grow-home-uses-maths-to-generate-a-personality/), game journalist [Alex Wiltshire](https://twitter.com/rotational) talks with Ubisoft about their game **Grow Home**. One of the main feature of the game is the way the protagonist, BUD, moves. The game does not have predefined animations; at least not in the *traditional* sense. When the player moves, the position of legs and feet is forced via code. The limbs are subjected to the same constraints of a ragdoll, forcing them to complete the animations in a plausible way.

A similar approach has been widely used in [Rain World](http://store.steampowered.com/app/312520/). Every animal in the game has a body which is made out of several colliders. While some of them are moved via code, the remaining ones are controller by joints. This can be seen in the animation below. The end point of the vulture’s wings are moved programmatically; the remaining bones are linked together using hinge joints. Controlling the end points automatically results in a fluid animation that would be otherwise impossible to achieve.

![](../../assets/e8b9e91bbd3b2593.gif)

Both Grow Home and Rain World use procedural animations to increase the realism of their characters. The controllers, however, do not rely on them. A game that expands this concept even further is [Gang Beasts](http://store.steampowered.com/app/285900/). The game fully embraces the floppy behaviours that occur as a result of using ragdoll physics, creating silly characters that moves unpredictably.

![](../../assets/bef9dbb9ae848d20.gif)

#### Inverse Kinematics

Rigid body simulations allow to simply animations. We specify where the hands and legs of BUD should be, and we let the physics engine to the rest. This very simple approach works with simple characters, but often fails on realism. Rigid body simulations only take into account things like gravity and mass, but they lack any contextual knowledge. In many application, you might want something that does not behaves only under the constraints imposed by gravity and joints.

The ultimate step in the creation of procedural animations is known as **inverse kinematics**. Given a ragdoll of any kind, inverse kinematics finds how to move it to reach the desired target. While Grow Home and Rain World let the physics determine how the joints would move when subjected to gravity, inverse kinematics forces them into a desired stance.

One of the first indie games that heavily relied on this concept is [The Majesty Of Color](http://futureproofgames.com/games/majesty/), by [Future Proof Games](https://twitter.com/playfutureproof). Here, the player controls the tentacle of a marine creature. Compared to the vulture’s wing in Rain World, this tentacle is not simply controlled by hinge joints. Each segment rotates in such a way that the end point of the tentacle can reach the desired point. If this animation relied purely on a rigid body simulation, the tentacle would look as if it was “pinned” to its target, like a piece of string.

![](../../assets/8c338ee4b03907cc.gif)

Inverse kinematics can be used for a variety of tasks. The most common ones allow humanoid characters to reach for certain objects in a natural way. Instead of using a custom animation, developers only specify the target that the hand needs to reach. Inverse kinematics will do the rest, finding the most natural way to move the arm’s joint. Simply relying on a rigid body simulation would result in “dead legs” which appear as if they were dragged.

![](../../assets/d27f5c67c77b0989.png)

**Mechanim**, Unity’s animation editor, comes with a tool ([Unity Manual](https://docs.unity3d.com/Manual/InverseKinematics.html)) that allows developer to use inverse kinematics in humanoid character.

The rest of this tutorial will focus on how to solve the problem of inverse kinematics. Whether you have a robotic arm, or a monster tentacle that you want to move realistically towards a target, this is the tutorial you have been looking for.

![](../../assets/7c981c6b94cd94b3.gif)

#### Other Resources

- Part 1.
[An Introduction to Procedural Animations](https://www.alanzucconi.com/?p=6131) - Part 2.
[The Mathematics of Forward Kinematics](https://www.alanzucconi.com/?p=6142) - Part 3.
[Implementing Forward Kinematics](https://www.alanzucconi.com/?p=6170) - Part 4.
[An Introduction to Gradient Descent](https://www.alanzucconi.com/?p=6133) - Part 5.
[Inverse Kinematics for Robotic Arms](https://www.alanzucconi.com/?p=6135) - Part 6.
[Inverse Kinematics for Tentacles](https://www.alanzucconi.com/?p=6180) - Part 7. Inverse Kinematics for Spider Legs 🚧 (work in progress!)

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

You can download the Unity project for this tutorial on [Patreon](https://www.patreon.com/posts/8928832).

Credits for the 3D model of the robotic arm goes to [Petr P](https://3dwarehouse.sketchup.com/model/92e064854f4dd504c8ab9067fbd9681d/Robotic-Arm-stainless-steel-R6Stainless).

Credits for the 3D model of the tentacle goes to [Daniel Glebinski](https://sketchfab.com/models/8fcc783af94246a0b8febf424a4b96b9#).

## Leave a Reply Cancel reply