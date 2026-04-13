---
title: Beyond the Storm - v0.6
url: https://www.vertexfragment.com/ramblings/bts-v06/
author: Steven Sell
published: '2023-12-19'
source_blog: Vertex Fragment
source_site: https://www.vertexfragment.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/38ec94947edb27dc.png)


*Whew*, this update is a long time coming. After nearly 6 months, version 0.6.0 is now complete.

Following the 18 months of work to get to v0.1.0, I had decided to do more frequent and incremental updates around every 3 or 4 months. But sometimes life gets in the way of making that possible.

So what was accomplished in this extended release? Well as this was an even-numbered release the focus was more on system development, whereas in odd-numbered releases the focus tends to be on graphics and world building. The primary systems worked on were: entity state, animations, AI, combat, and buoyancy/vehicles.

Why, oh why, did I wait so long to implement a proper state system for my entities/characters?

Coming into v0.6.0 there was no unified system for handling states and their transitions. Instead there were a variety of input handler and character controller classes that the logic, and relevant state, was scattered around in. As time went on this obviously became more painful to deal with, and knowing that the world would soon be filled with characters that are not the player (think I will call those NPCs), it was something that would need to be addressed soon.

From previous work I already knew about one approach to handling state, called [Finite State Machines (FSM)](https://en.wikipedia.org/wiki/Finite-state_machine), but did not know if (A) these would be suitable to the task and (B) if there is another solution that is more widely used these days, maybe something like a behaviour tree but for state management?

After a diligent search on my search engine of choice it appeared that FSMs were still the first choice for handling logic state and transitions. There were other more niche solutions, but none appeared to be widely used. But at first I still wasn’t sold on using FSMs due to one thing: the sheer number of states it looked like would be needed. Let us look at an example.

**The Problem**

A basic character has the following 3 states: `idle`

, `walking`

, `running`

.

However, what if we added the ability for the character to attack with a weapon? We now have 6 states: `idle`

, `attacking`

, `walking`

, `walking_attacking`

, `running`

, `running_attacking`

.

Oh, but this is a game featuring a world full of islands to explore, as such there is swimming. We now have 8 states: `idle`

, `attacking`

, `walking`

, `walking_attacking`

, `running`

, `running_attacking`

, `swimming`

, `swimming_attacking`

.

But before they attack they have to arm their weapon! More states are needed, for a total of 12! `idle`

, `attacking`

, `walking`

, `walking_attacking`

, `running`

, `running_attacking`

, `swimming`

, `swimming_attacking`

, `arming`

, `walking_arming`

, `running_arming`

, `swimming_arming`

.

Every time we add a new action, we would have to add multiple states so that action could be done while also moving. No one wants to stop moving just to unsheath their weapon. So how can we make using a FSM work without exploding the number of states required?

**The Solution**

Well, it is actually very simple: use multiple state machines!

If we look at all the states listed above they could really be simplified down to `movement_action`

or even `legs_arms`

. Each character entity has two state machines, one for the lower body (legs) and one for the upper body (arms). I was having a huge mental block and was stuck for a long time thinking there could only be a single state machine per character, and it was a real aha! moment when I read that solution.

So now instead of having `idle`

, `arming`

, `attacking`

, `walking`

, `walking_arming`

, `walking_attacking`

, `running`

, `running_arming`

, `running_attacking`

, etc. we have:

- Leg Machine:
`idle`

,`walking`

,`running`

- Arm Machine:
`arming`

,`attacking`


![](../../assets/6129d6c4311d6a34.png)


**The State Machine**

The design of the machine itself is fairly simple. A set of states is assigned to it, with one being assigned as the default/idle state which is returned to when no other state is valid.

Then each individual state has the following interface that they implement:

```
public int StateId { get; }
public bool ShouldStateExit { get; private set; }
public bool IsValidState();
public bool CanTransitionTo(int state);
public bool CanTransitionFrom(int state);
public void OnStateEnter(int previousState);
public void OnStateExit(int nextState);
public void OnStateUpdate();
public bool OnEntityAction(EntityActionType actionType, object data);
public void OnEntityCollision(Collision collision, CollisionMagnitudeType magnitude);
public void OnEntityStateModified(StateModificationDescriptor modifier, float adjustedAmount);
```


Which should all be fairly straightforward and standard. However one key part of the design is the `OnEntityAction`

. Actions are commands sent to the entity, either through player input or AI and include things such as `Interact`

, `Jump`

, `ArmWeapon`

, etc.

When a command is sent to an entity it is propagated throughout the entire entity, including to all of its states. This allows for state interrupts to occur. For example, if we are running (and thus in the `RunningState`

) and the command for `Jump`

is received, the `JumpingState`

will receive that action and attempt to interrupt the current state and become active.

```
// JumpingState.cs
bool OnEntityAction(EntityActionType actionType, object data)
{
if (actionType == EntityActionType.Jump)
{
JumpRequestedFrame = Time.frameCount;
return StateMachine.TriggerState(StateId);
}
return false;
}
// EntityStateMachine.cs
bool TriggerState(int toStateId)
{
if (!CurrentState.CanBeInterrupted ||
!StateMap.TryGetValue(toStateId, out EntityState toState) ||
!IsTransitionValid(toState))
{
return false;
}
return TransitionTo(toState);
}
```


![](../../assets/6887ac98a6d5b812.png)


One of the goals listed for this version was a second pass on the animation system being used.

With the addition of proper character state machines it opened the door for a programmatic approach to handling animation state and transitions as these could be handled within the new entity states. Now back in the old days of *Ocular Engine* and *Realms*, this is something I would have insisted on implementing from scratch myself.

However now that I am older, wiser, and more time constrained, I started looking for existing solutions and ended up settling on [Animancer by Kybernetik](https://kybernetik.com.au/animancer/) which has allowed me to get rid of my Unity animation controllers and adopt a purely programmatic solution to playing and transitioning between animations.

This has been a huge breath of fresh air and has made things both simpler and given me greater control and finesse around more complex situations and interactions.

**Inverse Kinematics**

While Unity provides built-in support for Inverse Kinematics (IK), and it is exposed by Animancer, it is fairly *meh* from the opinions I could gather. Which seems to be the case for many built-in tools and solutions (looking at you Terrain System which I have scrapped and rewritten multiple times).

So once again I went looking for a third-party solution and chose to use [Final IK by Root-Motion](http://root-motion.com/) which was fairly straightforward to integrate and has been easy-to-use, though its only been used so far for foot placement and hand on rudder while in boats. But I feel secure in relying on it in the future.

![](../../assets/a0f541de36bcbb8d.png)


Much of the skeleton for combat was already in place, and has been ever since trees were able to be cut down (pre-v0.1).

What was added in this version was the ability to damage other characters and engage in basic combat with them, as well as the various changes made to the UI to help provide feedback (combat text, health bars, etc.). Additionally, a fair bit of time was spent on tuning and adjusting movement with *Dark Souls 3* used as a reference. Particularly with how the camera and movement should respond when using a gamepad instead of mouse and keyboard.

Combat for the player currently supports basic melee attacks, blocking, and target locking. The very barebones combat AI used by NPCs is not much more than tracking the player, closing the distance, and melee attacking. The AI will grow exponentially over the next few versions and it will be exciting to see what it is like in another 6 months or a year.

Though not new, I feel like that it should be mentioned that [Behavior Designer by Opsive](https://opsive.com/assets/behavior-designer/) is used for the Behavior Trees as other third-party integrations have been mentioned. This is another system that if younger I would implement myself (and which I did for *Realms*) but saving time is more valuable to me then going back through the motions.

Finally, health and stamina were added to NPCs though stamina is largely unused at this time but will likely get attention next version. This means that the player can now die, which includes ragdolling and dropping their inventory (NPCs also have a dissolve effect), and then being greeted by a death screen. (Re)spawn points were also added as a consequence, and everyone’s favorite mechanic of fall damage is now present for the first time. Though it is tuned to an acceptable level as one of my philosophies is that travel should never be punishing (looking at all the games that kill you when falling ten feet or drown you when more than a few feet offshore).

![](../../assets/47893a6cb5517c71.png)


Boats, and buoyancy specifically, were to v0.6 as clouds were to v0.5. Which is to say they were pretty challenging and time-consuming to implement and get feeling just right. However, like clouds, the end result was worth the effort.

To start off, it must be said that without the wonderful two-part article series [ Water Interaction Model for Boats in Video Games](https://www.gamedeveloper.com/programming/water-interaction-model-for-boats-in-video-games) (

[Part 2](https://www.gamedeveloper.com/programming/water-interaction-model-for-boats-in-video-games-part-2)) by Jacques Kerner this would have been a whole lot harder and taken much more time to put together. The model presented in those articles is a much more comprehensive and complex representation of buoyancy mechanics, as compared to the simplified buoyancy that was previously in use and which I discuss in the ramble

[. It should be noted that the voxel-based model is still used for floating items, simple meshes, etc.](https://www.vertexfragment.com/ramblings/buoyancy-for-dummies/)

*Buoyancy for Dummies*Aside from working great, and being fast, once implemented another benefit of the approach described by Kerner is that it provides a lot of auxiliary data which is used to power various effects. Information such as how much of the buoyant mesh is submerged, slammed triangles, water line, etc. are all key for helping ensure the boat feels like it is part of the world.

![](../../assets/31008301cf6a652a.png)


There are a handful effects built around the boat, including: wake, spray, audio triggers, and rudder interaction. Improvements to the sail and interaction with the wind will be done at some point in the future.

The trickiest of these to implement was the wake, primarily because the ocean plane is not flat and all references I could find were based on a simple flat plane ocean. The final solution is comprised of the following steps:

- Attached to the boat is a dynamic triangle strip mesh. Vertex pairs are added and removed as the boat moves.
- As vertex pairs age, they move away from each other resulting in the wake getting wider as time goes on.
- A separate render pass draws all wake meshes to an offscreen render texture.
- This wake texture is then used in the water shader to apply the wake foam to the water mesh.

The other effects, spray and audio, are triggered off of slammed triangles calculated by the buoyant mesh. These triangles, along with the water line, provide an accurate location to apply spray and the relative force can also be used to adjust the strength of the effect.

Transforming the boat from scenery into a useable vehicle was another challenge that required both new systems and reworking of existing ones. This was just another feature that I, and likely most, take for granted in games and don’t consider the work needed behind-the-scenes to make it functioning.

![](../../assets/becdece4c2e3bcd3.png)


Those were the big topics that I felt like talking about, but not nearly everything that was done in this version. Below is a list of other changes (some minor, some major) that were done in v0.6.

**AI**

- Numerous AI actions and conditionals related to combat and movement

**Animations**

- Combat animations: blocking, stagger, daze
- Vehicle animations: sitting, IK integration

**Audio**

- Combat/strike/hit audio
- Boat audio (splash, creak, movement)
- Bush rustle

**Controls**

- Added partial support for gamepads
- Super jump bug v2 is fixed

**Effects**

- Ragdoll (never done this before, its neat how simple it is)
- Mesh disintegration
- Water masking
- Disable vignette at low light levels
- Impact effects

**Engine**

- Multiple Unity and third-party package/dependency updates
- Globalize entity effects (both audio and visual)
- Numerous bug fixes

**Items**

- Consumable items (can eat mushrooms to heal)
- Shield items
- Item proxy sparkle when out-of-inventory and distant

**UI**

- Floating combat text
- Player health and stamina bars
- Entity floating health bars
- Action bar memory

Code statistics! *(+/- since last release)*

**Commits in release:**1,921 (*+277*)**Total Git Lines Added:**2,317,021 (*+200,247*)**Total Git Lines Removed:**1,512,076 (*-471,280*)**C# Files in Release:**943 (*+241*)**Live Lines of C#:**108,665 (*+20,239*)**Largest Files:**`MathUtils.cs`

(*1,571 lines*)`TerrainGrid.cs`

(*1,069 lines*)`WorldGraphSegment.cs`

(*1,051 lines*)

**Smallest Files:**`IAbilityBook.cs`

(*6 lines*)`SystemMenuControlsButtonController`

(*6 lines*)`SystemMenuLoadButtonController`

(*6 lines*)


**Shaders in Release:**97 (*+7*)**Live Lines of Shaders:**15,437 (*+804*)**Largest Shaders:**`TerrainImpl.hlsl`

(*914 lines*)`Common.hlsl`

(*900 lines*)`ToonStencilDeferred.shader`

(*675 lines*)

**Smallest Shaders:**`DeclareThicknessTexture.hlsl`

(*21 lines*)`DeclareLightSourcesTexture.hlsl`

(*22 lines*)`DeclareTransparentTexture.hlsl`

(*25 lines*)



With a bunch of progress made on various systems it is time to get back to a visual release version.

The tentative goal will be to fully flesh out what, in my head, are deemed the green islands (and also generate the rest of them). While there are trees and some rocks and bushes, the islands are lacking a true depth to them. This is chiefly due to lack of assets and additional/improved world generation modules.

In addition to scenery assets, there is also a plan to introduce more NPCs, primarily non-humanoid ones which have not yet been worked on though there are stubs in the code for them. This will also be a chance to take a second pass on some world effects such as cloud performance, atmospheric fog, and celestial bodies.

With the first set of islands at a good place visually and content-wise it would allow me to start introducing true gameplay systems and loops in v0.8.

Once again, thank you to [Alex B](https://alexthebear.artstation.com/) for providing art assets - this time contributing the boat shown in various screenshots.