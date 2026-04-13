---
title: 'Allar''s Dev Diary #15: Day 4, Tower Defense Side Project'
url: https://allarsblog.com/2010/11/21/allars-dev-diary-15-day-4-tower-defense-side-project/
author: Michael Allar
published: '2010-11-21'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

Yesterday I spent most of my day eating pizza and working on Warm Gun over at [Emotional Robots, Inc](http://emotionalrobots.com/?ref=allarsblog.com)., but I managed to put a little time in this morning to this side project.

# Day 4 (11/21/2010)

## 9. Setting Up Basic Interaction Logic From Mouse To Towers

While our towers are just shell Pawns that aren't doing much, before I give them more functionality I wanted to tackle how the player is going to interact with the unbuilt towers so that they can build their own. The first step is getting some sort of simple detection going on that would let the towers know if they were currently the target for the players mouse and then to figure out if the player was within an 'interaction radius' with the tower. Doing so, the player will only be able to interact with tower building zones when their Pawn is close enough to the tower, causing the player to have to run to wherever they want to place their towers for a bit of a fun challenge. If this proves to not be fun, I can just either increase the interact range greatly or remove it all together. Also, I wanted this detection logic to be able to be applied to any actor I choose instead of having every actor derive from an interaction actor. To do this, we have to use an interface. Interfaces are kind of like sub classes, but they list a series of functions and delegates (no local variables) that each class using it must implement. To implement an interface, you just use the keyword 'implements' in your class declaration. More information about interfaces can be found on the [UDN page](http://udn.epicgames.com/Three/UnrealScriptInterfaces.html?ref=allarsblog.com).

The interface is really simple for now, it has a function that returns what type of interaction it is, functions to show/stop showing the player that the object is interactable, and then finally an actual interact function.

[csharp]/*******************************************************************************

CRInterface_Interaction

```
Creation date: 21/11/2010 06:46
Copyright (c) 2010, Allar
Actors that have some sort of UI interaction associated with them
should implement this interface.
```


*******************************************************************************/

interface CRInterface_Interaction;

//A tentative list of interaction types

//for future planned HUD protocol.

enum EInteractionType

{

IT_None,

IT_Player,

IT_Tower

};

//Default Interaction Type

//Should override if your object consists of multiple

//interaction types like a tower with multiple unique turrets

//on its sockets or something.

function EInteractionType GetInteractionType()

{

return IT_None;

}

//Let this object tell the player its interactable somehow

function HintInteraction(CRPlayerController InteractingPC);

//Stop telling the player that this objcet is interactable

function UnhintInteraction(CRPlayerController InteractingPC);

//Perform actual interact action

function Interact(CRPlayerController InteractingPC, byte Mode);[/csharp]

Theres really nothing all that shocking to go over in this interface, yet. With this here, I can now implement this interface in my CRTowerBase.uc class. For now, all I want to be able to do is to have my tiles glow red when the mouse is over them and the player is out of range, and then glow green when the player is in range. Before I can even code for this, I am going to need a material that can support this. For this project, I am going to experiment with setting up a master material that all my other materials will base off of as that seems to be the standard at a few local game companies I've been to. Because of this, you will see a few static switches toggling different options for emissives. I just created this material only planning for towers and other interactables in the future, so the emissive path alone on this mater material should grow with quite some more options as it gets more and more developed. The way this is set up, we can control two parameters: EmissiveStrength and EmissiveLerp, with Strength controlling on/off/bloom dynamically (there is also a static switch for turning off emissive alltogether) with EmissiveLerp being able to switch between Red for too far away and Green for within range. I also am going to make the material glow only around its edges using the Fresnel node, and if I wanted to I could also control the Fresnel falloff as well](

[http://allarsblog.com/CastilloRTS/Blockout/50_TowerEmissive.JPG](http://allarsblog.com/CastilloRTS/Blockout/50_TowerEmissive.JPG))

With that in place, I can now set up the Tower to manipulate the material parameters when needed in the CRTowerBase code. Heres the meat of my changes in CRTowerBase that I made. The code changes are pretty simple and should be able to be understood. The only odd thing I did was instead of storing a PlayerController to have distance updates per tick, I used an array of PlayerControllers, just in case I have multiple player controllers interacting with the same object soon.

[csharp][//CRTowerBase.uc](http://CRTowerBase.uc)

simulated function PostBeginPlay()

{

super.PostBeginPlay();

TowerMaterial = Mesh.CreateAndSetMaterialInstanceConstant(0);

}

function EInteractionType GetInteractionType(){ return IT_Tower; }

//Sets our EmissiveStrength in our material instance for the tower to 1 or 0

function ToggleTowerEmissive(bool bEnable)

{

local LinearColor LC;

LC = bEnable ? MakeLinearColor(1,1,1,1) : MakeLinearColor(0,0,0,0);

TowerMaterial.SetVectorParameterValue('EmissiveStrength',LC);

}

//Sets our EmissiveLerp to 1 if we are within InteractRadius, 0 if not

//Inheriting from the master material, 0 lerp is red and 1 lerp is green

simulated function SetEmissiveLerpForPC(CRPlayerController InteractingPC)

{

if (VSizeSq(InteractingPC.Pawn.Location - Location) < InteractRadius**2)

TowerMaterial.SetScalarParameterValue('EmissiveLerp',1);

else

TowerMaterial.SetScalarParameterValue('EmissiveLerp',0);

}

//Turns on emissive, sets distance color, adds PC to list of

//interacting PCs, and then enables TickSpecial calls

simulated function HintInteraction(CRPlayerController InteractingPC)

{

ToggleTowerEmissive(true);

SetEmissiveLerpForPC(InteractingPC);

```
if (InteractingPCList.Find(InteractingPC) == -1)
InteractingPCList.AddItem(InteractingPC);
//Update our material if player movies in special tick
bScriptTickSpecial = true;
```


}

//Turns off emissive, removes PC from list, and if no PCs are interacting

//we no longer have a need to call TickSpecial

simulated function UnHintInteraction(CRPlayerController InteractingPC)

{

ToggleTowerEmissive(false);

```
if (InteractingPCList.Find(InteractingPC) != -1)
InteractingPCList.RemoveItem(InteractingPC);
if (InteractingPCList.Length == 0)
bScriptTickSpecial = false;
```


}

//This ticks when we should be checking player positions for interaction

event TickSpecial( float DeltaTime )

{

local CRPlayerController InteractingPC;

```
//If for some reason we lost all interactors, lets disable
//TickSpecial to restrict unneeded tick calls.
if (InteractingPCList.length == 0)
{
bScriptTickSpecial = false;
return;
}
foreach InteractingPCList(InteractingPC)
SetEmissiveLerpForPC(InteractingPC);
```


}

//Not sure where I'm going with this yet, but I need it to

//implement our interface.

function Interact(CRPlayerController InteractingPC, byte Mode)

{

}[/csharp](http://allarsblog.com/CastilloRTS/Blockout/51_HintInteraction.jpg)![51. Hint Interaction](https://allarsblog.com/CastilloRTS/Blockout/51_HintInteraction.jpg)


Now that we have an object that is set up to be interacted, we need to be able to have the mouse call these interaction hints. Instead of writing a new function that handles this for us, I'm going to put it in the CRPlayerController's UpdateRotation where we are already doing a trace for mouse coordinates. The reason for this is traces are expensive and they should be only called when needed to avoid a performance hit. With this, we can store whatever actor we are currently acting with and then compare our traced actor to see if it has changed. If it has changed, we should unhint the old actor and call hint interaction on the new actor, then store the new actor as our current interaction object. This will work for any object that implements our CRInterface_Interaction, leaving interaction hinting and behavior to the interacting classes themselves.

With that done, the next step is to create a way to invoke the Interact method of the interactable objects, and then write something for our tower building zones to do when they are interacted with.