---
title: Using Animations in Unity
url: https://blog.eyas.sh/2020/11/unity-for-engineers-pt9-animation/
author: Eyas Sharaiha
published: '2020-11-15'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

In solo game development, you can’t just stick to your strong suit. If you’re a Software Engineer trying out solo game development, being a solid developer will only get you so far; even if you’re using assets made by others, you’ll still need to know how to integrate them into your game tightly.

Animation is a great example. Imagine a character model has animations for
walking, running, standing, talking, interacting, and more. In that case, you
will still need to define how a character *object* triggers and transitions
between these animations. These animations might also dictate what your *object*
does; for example, an enemy that punches characters might want to deal damage at
the precise moment the model’s arms are fully extended.

Today, we’ll discuss the essential concepts of *using* Animation in Unity. We’ll
also go over a few examples using the incredibly cute
[Modular Animal Knights PBR](https://assetstore.unity.com/packages/3d/characters/animals/modular-animal-knights-pbr-134728?aid=1011leWs6)
asset pack from the Unity Asset Store. A free version that includes *only* the
Dog is
[available here](https://assetstore.unity.com/packages/3d/characters/animals/dog-knight-pbr-polyart-135227?aid=1011leWs6)
as well 1.

*This is the 9 th installment of
*

[Unity for Software Engineers](https://blog.eyas.sh/tag/unity-for-software-engineers)(now updated and

[available as a book](https://leanpub.com/unity-for-engineers)), a series for those seeking an accelerated introduction to game development in Unity. A few more installments are coming over the next few weeks, so

[consider subscribing](http://eepurl.com/gVgusL).

## Concepts

### Animation Clip

An **Animation Clip** (*Animation* for short, `AnimationClip`

in code) is an
** asset** that
describes a series of

*keyframes*for each

*property*on a Game Object over time.

In other words, an Animation Clip asset describes, for a given Object, the
*change over time* of any number of **properties** on that object. An Animation
Clip can control any property on a Game Object or recursively accessible from a
Game Object or any child object.

![Example of an Animation Clip](../../assets/7bfd3279e967e09f.img)

An *Animation Clip* has its own Animation Clip *Editor Window*. Here is an
example Animation (from the
[animal knights pack](https://assetstore.unity.com/packages/3d/characters/animals/modular-animal-knights-pbr-134728?aid=1011leWs6))
of an animation in its editor window, with the corresponding Inspector Editor
for that animation docked next to it.

In addition to an Animation Clip specifying properties *on a Game Object*, a
clip can control **Animation Avatar** properties. An Animation Avatar is an
**asset** that defines the relationship between a standard “skeleton” set of
transforms (head, chest, leg, etc.) to a specific model. See the
[Character Animation tutorial on Unity Learn](https://learn.unity.com/tutorial/character-animation)
for more details.

For example, in the above screenshot, the “Dog Knight” model comes with an
Avatar asset that defines the relationships between . The animations included in
the asset pack control *the avatar transforms*. Prefabs included in the asset
pack will point to an ** Animator Controller** and Avatar.
Animation Clips referenced through the controller will cause the object’s model
to move around through the pre-defined keyframes using the Avatar mappings.

An Animation Clip could be something like “Walking”, “Running”, “Attacking”, “Idle”, etc.

### Animator Controller

Few characters can get away with having a single animation that plays in a loop over and over. In many cases, an object will have multiple animations and transitions between them according to some logic. For example, an idle player can transition to walking or running and back to idle. A moving character might jump, and a jumping character will need to land before going back to walking and running. A state machine is a neat way to model this, and luckily for us, this is how Unity represents Animator Controllers.

An **Animator Controller** is an
** asset** that defines
a finite state machine representing all animation clips for a given object and
the transitions between those.

A controller consists of one or more *layers*. Each layer is a separate state
machine. For our purposes, we’ll consider having multiple layers as an advanced
use, but the
[Unity docs on Animation Layers](https://docs.unity3d.com/Manual/AnimationLayers.html)
are a good resource to learn more. The summary is that each state machine
*layer* does its transitions simultaneously, and the states from each layer
“blend” together according to user-defined criteria.

We’ll focus our attention *within* a layer. An Animator Controller allows you to
define **states** and **transitions** between them. The Animation controller
also exposes the concept of a **Sub-State Machine** to encapsualte a group of
states.

#### Animation Parameters

You can define **parameters** on an Animation Controller. A parameter can be a
trigger, a boolean, or a float. You can then programmatically set their values.

For example, a common parameter is a `Speed`

floating-point parameter. A
component that drives motion can set the `Speed`

parameter on an Animator. This
parameter can then drive the state machine, for example, to transition from an
idle to a walking to a running animation and back.

#### Animation State

An **animation state** represents a single *motion*. A motion is one of two
things:

- An
**Animation Clip**(created through the context menu*Create State > Empty*, then pick a clip for the*Motion*property), and - A
**Blend Tree**(created through*Create State > From New Blend tree*).

A simple motion represents a single animation clip. Transitions in and out of this state will transition into or out of playing that animation clip.

A *blend tree* is a composite motion that represents *multiple* animation clips.
A blend tree takes in an **animation parameter** and maps it to a corresponding
animation. For example, if you have ‘walk’, ‘run’, and ‘sprint’ animation clips,
you can arrange these in a single blend tree that takes in the speed as a
parameter and picks the right clip based on the exact speed value. A blend tree
will use the parameter to *blend* these animations. So if walking is defined as
*speed > 0* and running is defined as *speed > 3*, then a *speed = 2* would
blend between a walk and a run.

![Inspector Window for a Simple State](../../assets/e7c12fb432ea9f2e.img)

When a Simple State is selected, the inspector window allows the user to define a single animation and related parameters. Transitions into and out of the state can also be defined.

![Inspector Window for a Blend Tree](../../assets/e7cd165995bbd199.img)

When inspecting a Blend Tree, instead of *Animation Clip* motion field, the
state points to a blend tree. The blend tree can be edited when double-clicking
the state.

![Inspector Window for a Blend Tree, Once inside the blend tree view](../../assets/5e46a32d74670a33.img)

Inside of a Blend Tree, the root tree node inspector allows listing all
*motions* to blend. In a 1D blend tree, a single parameter and a set of
thresholds drive which motion is active.

A blend tree can be composite, meaning that one of its *motion* fields could be
another blend tree.

There are a few primitive states that always exist:

-
*Entry*. A pseudo-state that must contain*one*outgoing transition pointing to the state the animator will start with.No one can transition

*into*this state. This state can only have a single outgoing transition. -
*Exit*. A terminal pseudo-state. Any transition that points to this state will result in the state machine terminating. No more animations can happen.Multiple states can transition

*into*this state, but no transitions can happen out of this state. -
*Any State*. A short-hand meta-state representing every (real, not pseudo-) state in the diagram.

#### Animation Transitions

To move between states, you need a **transition**. A set of constraints define a
transition; when those are met, the controller transitions from the current
state to the transition’s destination state.

There are two types of constraints:

**Exit Time**. A transition can only be made once the state’s motion animation has completed.**Conditions**. A transition can only be made if a list of manually entered conditions based on*animation parameters*are met.

A transition needs to contain at least one constraint (either exit time and >0 conditions or >1 conditions). Here are some examples of transitions using each of these:

![Inspector Window for a transition only specifying exit time](../../assets/22530562e442ed34.img)

Checking “Has Exit time?” allows a state to transition once its motion has completed (provided there are no other conditions). This is appropriate for things like an “attack” or “received damage” animation.

![Inspector Window for a transition specifying only a single condition](../../assets/c41b030aefcaa6d2.img)

Transitioning from an Idle state to a Motion state based on a Speed parameter is a great example of using conditions.

Transitions allow you to control how to blend between two motions when that transition is taken.

### Animator (Component)

An **Animator** is a
[component](https://blog.eyas.sh/2020/10/unity-for-engineers-pt5-object-component#component)
assigning an object to an **Animator Controller** and (optionally) an
**Avatar**.

![An Animator component inspector window.](../../assets/f73a1f14c17b71ed.img)

## Putting it all together

We can put these together to create a simple moving character:

Using the asset pack, I used the `Idle_Battle`

animation as my idle state and
created a blend tree for motion. I also made a float parameter and called it
`Speed`

. The Idle state is our initial state, and transitions to and from
“Moving” happen when `Speed > 0`

and `Speed < 0.01`

, respectively. All
transitions here will disable “Has Exit Time” since we want to change
transitions immediately, without waiting for any clip to complete.

![A simple Animator Controller including an idle state and a moving blend tree.](../../assets/2a6be714b21a3aec.img)

Inside of the blend tree, we define two motion fields. The first is
`WalkForwardBattle`

, and the second is `RunForwardBattle`

. Some clips will imply
a root motion, allowing the blend tree to compute these thresholds
automatically, but they don’t. Uncheck “Automate Thresholds” and experiment with
the correct thresholds for our animation. You want to avoid the character’s feet
appearing to “slip” on the ground, either because the character is moving faster
than the animation implies or because the animation is moving in-place too fast.
It takes quite a bit of trial to get the right numbers.

![Inside the Blend tree.](../../assets/ea0a6aeb095d258b.img)

I ended up settling on `0.1`

and `1`

as my thresholds. I wasn’t 100% satisfied,
but unless you were squinting, it looked good.

Fancier assets might have animations for turning, running while turning, etc. A 2D blend tree operating on both speed and angular speed might then be ideal.

Now, we need to see what this all looks like. I ended up nesting a camera under the player to follow it as it moves. Then I put a simple mover script on my character to see what everything looks like:

```
using UnityEngine;
namespace Demos
{
public class DemoMover : MonoBehaviour
{
private float _speed = 0f;
private Animator _animator;
[SerializeField] private float _acceleration = 0.25f;
private void Awake()
{
_animator = GetComponent<Animator>();
}
private void Update()
{
_speed += _acceleration * Time.deltaTime;
transform.position +=
(_speed * Time.deltaTime) * transform.forward;
// TODO: In a performance-critical setting, cache this
// string parameter on Awake using:
//
// Animator.StringToHash("Speed")
_animator.SetFloat("Speed", _speed);
}
}
}
```


I put an acceleration that’s *just* slow enough to notice what’s going on and
tuned the thresholds until I was happy. In addition to the thresholds, I could
have also tuned the animation speeds (making the footsteps faster or slower),
but I decided that the default (1) looked good.

## Where next?

Here, we described controlling the *locomotion* of an object from components and
passing various parameters to the animator to inform animator motion. However,
animators can also be used to control the locomotion of an object itself. You
can enable this from the
[Apply Root Motion](https://docs.unity3d.com/Manual/RootMotion.html) boolean
property on the Animator component.

We also haven’t discussed
[Unity Animation Events](https://docs.unity3d.com/Manual/script-AnimationWindowEvent.html),
which you can use to trigger a specific function in one of your object’s
components at a given frame within the animation. This is helpful to time
certain events (applying damage at the maximal point of a punch, playing sound
as a foot touches the ground, etc.) with an ongoing animation. Animation Events
are part of a clip.

In addition to using pre-made animation clips, you can also use animation clips to vary simpler properties, such as position, rotation, scale, or custom serialized properties on your components.

## Footnotes

-
These two are affiliate links. You can strip the

`?aid=...`

part of the query string if you prefer.[↩](https://blog.eyas.sh#user-content-fnref-1)