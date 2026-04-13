---
title: 'Allar''s Dev Diary #16: Day 7, Tower Defense Side Project'
url: https://allarsblog.com/2010/11/25/allars-dev-diary-16-day-7-tower-defense-side-project/
author: Michael Allar
published: '2010-11-25'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

# Day 7 (11/24/2010)

## 12. Getting Towers to Track Their Targets

<span style="font-weight: no![55. Targeting](https://allarsblog.com/CastilloRTS/Blockout/55_Targeting.jpg)

[http://allarsblog.com/CastilloRTS/Blockout/55_Targeting.jpg](http://allarsblog.com/CastilloRTS/Blockout/55_Targeting.jpg))

Today I decided to switch gears back into actual tower development, as that is the real nature of the game isn't it? In any case, we need a way for our enemies to be registered as enemies for our towers. We don't want our towers to be attacking every actor that is within its range, it should only track and attack enemy targets. To do this, I've decided to make another Interface that way I can make any class an enemy instead of having all my enemies derive from a single class. Right now there is no actual use of the interface than to register a class as an enemy, but I've decided to throw in a function that could be used to allow for classes implementing this interface to decide that a particular instance of it is not an enemy. Today I haven't created that checks this or requires this, but I think it might come handy in the future.

Lets get to the interface:[csharp]/*******************************************************************************

CRInterface_TowerEnemy

```
Creation date: 24/11/2010 12:42
Copyright (c) 2010, Allar
If a class implements this interface, it is targetable by towers
```


*******************************************************************************/

interface CRInterface_TowerEnemy;

//Override for classes that could exist as an enemy and non-enemy

simulated function bool IsTowerEnemy() { return true; }[/csharp]

Pretty straight forward. Its an interface, it has a function, thats it. I defined the function here so that I can just copy paste it anywhere to fulfill the needs of implementing an interface. Now we need to have a class implement this! Right now our only enemies are crowd actors so lets go ahead and create a crowd actor enemy. Implementing the interface is quite easy and we've done it before, so I don't need to go over how that works again, but there is something else we need to add to our CrowdAgents. Currently the crowd actors do not have any form of collision with them at all and do not trigger any type of touch/encroach event against any other actor and for the tower system I have in mind I want to use touch events for tower triggers instead of checking every tick for all actors within a radius. Now the touch events for our tower are going to be a bit difficult to implement, however to facilitate this we need to make sure our crowd agents can register touch events. For an object to register a touch event, it must have bCollideActors set to true and it also must have a collision component. Because this collision component is only going to be used for triggering, I will use a fairly standard CylinderComponent for my collision, and a small one at that. This way crowd actors won't create a lot of physics checks if they penetrate each other, but we might need to make this for bigger actors so that their position is more accurately defined for better tower aiming. The last thing we need to be aware of is that crowd actors are set to tick during TG_DuringAsyncWork which makes physics events a bit tricky to control as these actors in this group are updated as physics is happening, not before. There is a lot of technical info about tick groups that I will not get into mainly because I don't know enough to be confident I have correct knowledge about the subject. What I do know is, collision components on crowd actors that are not set to TG_PreAsyncWork causes a huge list of log errors and that is something I'd prefer not to have. With that said, here is the small little GameCrowdAgent class that I wrote that will allow our crowd actors to support touch events and whatnot.

[csharp]/*******************************************************************************

CRGameCrowdAgent

```
Creation date: 24/11/2010 13:54
Copyright (c) 2010, Allar
Crowd Agent that is capable of triggering touch events
```


*******************************************************************************/

class CRGameCrowdAgent extends UTGameCrowdAgent

implements (CRInterface_TowerEnemy)

showcategories(Collision);

simulated function bool IsTowerEnemy() { return true; }

simulated function PostBeginPlay()

{

super.PostBeginPlay();

SetTickGroup(TG_PreAsyncWork);

}

defaultproperties

{

Begin Object Class=CylinderComponent Name=CollisionCylinder

CollisionRadius=+0015.000000

CollisionHeight=+0015.000000

BlockNonZeroExtent=true

BlockZeroExtent=true

BlockActors=false

CollideActors=true

End Object

CollisionComponent=CollisionCylinder

Components.Add(CollisionCylinder)

```
bCollideActors=true
bCollideWorld=false
bBlockActors=false
```


}[/csharp]

Cool. Be sure to create an archetype of this new crowd agent class and replace the one that we made earlier in our list of agent archetype, otherwise we will still be using the old crowd actors that don't support trigger events.

Now we must create something that will get triggered by the crowd actors to alert the towers of their presence. I tried a few ways of implementing this in the tower class itself but it led to various collision issues in that I could either have the trigger cylinder set off trigger events but then my towers would lose blocking collision or the other way around. I couldn't find an easy method to create a touch-only component of an actor that must also perform full collision as well, so what I ended up doing was creating another actor class called CRTower_Toucher that will feed back touch events to the towers they belong to. A tower can then create a CRTower_Toucher and assign itself as the toucher's owner and the toucher will automatically call targeting events in the tower. This effectively compartmentalizes the enemy detection logic from the tower's attacking logic and makes for cleaner, more object oriented code. With this separation, we can create custom touchers that apply to any tower instead of specific towers needing to have their enemy touching logic rewritten.

The CRTower_Toucher should be able to store the enemy the toucher is currently 'watching' or 'active', a reference to its owning tower, and a CylinderComponent to use as its touch radius. On the Toucher's touch event, it should first see if our touched actor is a tower enemy and simply bail out if it isn't as we don't want to perform lots of unneeded calculations in an event that will be called very often. If it is a tower enemy, we should go ahead and check to see if we an active enemy already and take care of two situations: our touched actor is the same as our active enemy or a different enemy has touched our toucher. In the first situation, we should just ignore the touch completely. In the second situation, we need to first check to see that if our current enemy is within range. If our current enemy is within range, we should do nothing and keep tracking our current enemy, but if the current enemy is out of range we should go ahead and start tracking the enemy that just touched us. With this alone, our toucher will be able to acquire targets and then switch targets when the last target is out of range. What it won't do is stop targeting when an enemy leaves its range and no new enemies touch it again.

The CRTower_Toucher should also be able to stop targeting when an enemy leaves its radius without waiting for a new enemy to touch it. When an enemy leaves its range, and it is our current enemy and not some other enemy that we aren't tracking, we should first check to see if there are other enemies already within our radius that we should track. Preferably we should track an enemy that isn't on the verge of leaving the tower, but more towards the middle or outer reaches of our range, as otherwise it will only target enemies just as they are leaving the toucher's range and the tower will only have a chance to shoot enemies for a very short time. Also, it doesn't look as cool or dramatic as a tower switching targets if it only has to adjust a tiny bit. If there are no enemies within the toucher when the current enemy leaves, that means there is no one to track and we should simply just store none. With this added functionality, our toucher can now track an enemy as it enters, and when it leaves it can either pick an enemy within itself or target no one until a new enemy enters range.

Every time the CRTower_Toucher switches enemies, it should also notify the tower owner of its new enemy. This code listing below allows for all of this to happen:

[csharp]/*******************************************************************************

CRTower_Toucher

```
Creation date: 24/11/2010 12:36
Copyright (c) 2010, Allar
Forwards touch events to the owning tower
This way our towers don't have to tick every frame and
target acquisition only calculates on touch/untouch events.
```


*******************************************************************************/

class CRTower_Toucher extends Actor;

var CRInterface_TowerEnemy ActiveEnemy;

var CRTowerBase OwnerTower;

var CylinderComponent TouchCylinder;

event Touch(Actor Other, PrimitiveComponent OtherComp, vector HitLocation, vector HitNormal)

{

local Actor TestActor;

```
if (CRInterface_TowerEnemy(Other) == none)
return;
//A new enemy has entered while we already have an active enemy
//check to see if active enemy is outside our toucher
if (ActiveEnemy != none && ActiveEnemy != CRInterface_TowerEnemy(Other))
{
//We can't search for CRInterface_TowerEnemy because its an interface
//and not a class of Actor, however TouchingActors runs pretty fast
foreach TouchingActors(class'Actor',TestActor)
{
//Our active enemy is still within the toucher, so its still active
if (TestActor == ActiveEnemy)
return;
}
//If we get here, our old active enemy is no longer active
//so we can go ahead and assign our new enemy
ActiveEnemy = CRInterface_TowerEnemy(Other);
OwnerTower.TargetEnemy(ActiveEnemy);
}
else if (ActiveEnemy == none && CRInterface_TowerEnemy(Other) != none)
{
ActiveEnemy = CRInterface_TowerEnemy(Other);
OwnerTower.TargetEnemy(ActiveEnemy);
}
```


}

event UnTouch(Actor Other)

{

local int i;

if (Other == ActiveEnemy)

{

//We can't search for CRInterface_TowerEnemy because its an interface

//and not a class of Actor, however TouchingActors runs pretty fast

```
for (i = (Touching.length-1); i >= 0; --i)
{
if (Touching[i] != Other && CRInterface_TowerEnemy(Touching[i]) != none )
{
ActiveEnemy = CRInterface_TowerEnemy(Touching[i]);
OwnerTower.TargetEnemy(ActiveEnemy);
return;
}
}
//We found no tower enemies touching us
ActiveEnemy = none;
OwnerTower.TargetEnemy(none);
}
```


}

defaultproperties

{

```
bCollideActors=true
Begin Object Class=CylinderComponent Name=CollisionCylinder
CollisionRadius=+0512.000000
CollisionHeight=+0060.000000
CollideActors=true
End Object
TouchCylinder=CollisionCylinder
CollisionComponent=CollisionCylinder
Components.Add(CollisionCylinder)
```


}[/csharp]

At this point, I decided that having our towers as Pawns was actually quite overkill. The Pawn class has a lot of cool things with it but it also has a large amount of things that will just cause bloat, excess memory use, and lots of irrelevant replication to deal with. Because of this, I decided to refactor CRTowerBase into a direct subclass of Actor. There are a few things that are missing that we need in the base Actor class that Pawn provides, but theres nothing that we can't make for ourselves, such as a SkeletalMeshComponent. Also, we lose functionality of TickSpecial so we must set up our own timer to use when we want to create a temporary ticking solution and a timer interval of 0.16 seconds (60frames per second) works just as well. We need to create a new SkeletalMeshComponent in our default properties block to assign to our new actor's mesh component too, and we can just copy this from our original default properties box. Next we need a way to store and create a CRTower_Toucher for our tower to use to detect our crowd agents. This is done fairly simple, we just create a variable called TowerToucher that stores our CRTower_Toucher and then we spawn one in our PostBeginPlay. Now when we create a subclass of our tower actor that actually shoots, we should set up a way to only allow certain towers to spawn touchers to save performance, as an unbuilt tower shouldn't have to respond to crowd agents running around it. We are temporarily doing this for now to see if our design system works however. Once its spawned, we must associate the tower with the toucher so we just assign the OwnerTower variable of the toucher with 'self'. We must also create a TargetEnemy function that will take in a CRInterface_TowerEnemy and then store it. The reason why we use a simple function like this instead of directly assigning it in the toucher is that our sub-classed towers might need to perform special behavior when it acquires a new target, so we offer a way to override this behavior in an object oriented manner instead of a per-class basis. Given any practical opportunity to take advantage object oriented programming, you should pounce on it and take a hold of it as this will lead to cleaner and more elegant code that is simpler to work with in the future. I've also included some debug drawing in my new TimerTick function (which replaced TickSpecial) to allow me to visually see which target is tracking temporarily.

[csharp]/*******************************************************************************

CRTowerBase

```
Creation date: 20/11/2010 17:29
Copyright (c) 2010, Allar
This class will serve as an unconstructed tower
```


*******************************************************************************/

class CRTowerBase extends Actor HideCategories(Camera,Attachment,AI,Debug,Mobile,Physics,Swimming,TeamBeacon,UDKPawn)

implements(CRInterface_Interaction)

placeable;

//Our mesh!

var() SkeletalMeshComponent Mesh;

/** The pawn's light environment */

var DynamicLightEnvironmentComponent LightEnvironment;

//Max distance the player can be to interact with this object

var int InteractRadius;

//Instance of our Tower Material to set 'interactive' look.

var MaterialInstanceConstant TowerMaterial;

//The CRPlayerControllers currently interacting with this object

//Decided to make an array in case of multiplayer support? Iunno.

//Just seems like a good idea at the moment

var array<CRPlayerController> InteractingPCList;

//Actor that gets spawned that relays encroach events

//to the tower so the tower has its own collision intact

//and doesn't have to rely on tick every frame

var() CRTower_Toucher TowerToucher;

//The current enemy that is targeted by the tower

var CRInterface_TowerEnemy TargetedEnemy;

//These things should do nothing on damage taking.

event TakeDamage(int Damage, Controller InstigatedBy, vector HitLocation, vector Momentum, class<DamageType> DamageType, optional TraceHitInfo HitInfo, optional Actor DamageCauser)

{

return;

}

simulated function PostBeginPlay()

{

super.PostBeginPlay();

TowerMaterial = Mesh.CreateAndSetMaterialInstanceConstant(0);

TowerToucher = Spawn(class'CRTower_Toucher',self,,,,,true); //skip collision check on spawn

TowerToucher.OwnerTower = self; //associate ourselves with the toucher

}

function EInteractionType GetInteractionType(){ return IT_Tower; }

//Sets our EmissiveStrength in our material instance for the tower to 1 or 0

function ToggleTowerEmissive(bool bEnable)

{

local LinearColor LC;

LC = bEnable ? MakeLinearColor(2,2,2,2) : MakeLinearColor(0,0,0,0);

TowerMaterial.SetVectorParameterValue('EmissiveStrength',LC);

}

//Sets our EmissiveLerp to 1 if we are within InteractRadius, 0 if not

//Inheriting from the master material, 0 lerp is red and 1 lerp is green

simulated function SetEmissiveLerpForPC(CRPlayerController InteractingPC)

{

if (InteractingPC.Pawn == none)

return;

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
SetTimer(0.016,true,'TimerTick');
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
ClearTimer('TimerTick');
```


}

//This ticks when we should be checking player positions for interaction

event TimerTick( float DeltaTime )

{

local CRPlayerController InteractingPC;

```
//If for some reason we lost all interactors, lets disable
//TickSpecial to restrict unneeded tick calls.
if (InteractingPCList.length == 0)
{
ClearTimer('TimerTick');
return;
}
foreach InteractingPCList(InteractingPC)
SetEmissiveLerpForPC(InteractingPC);
DrawDebugCylinder(Location-vect(0,0,30),Location+vect(0,0,30),512,12,0,255,255,false);
DrawDebugBox(Location,vect(512,512,30),255,255,0,false);
if (TargetedEnemy != none)
{
DrawDebugLine(Location+vect(0,0,64),Actor(TargetedEnemy).Location,0,0,255,false);
}
```


}

//Not sure where I'm going with this yet, but I need it to

//implement our interface.

function Interact(CRPlayerController InteractingPC, byte Mode)

{

}

function TargetEnemy(CRInterface_TowerEnemy NewTarget)

{

TargetedEnemy = NewTarget;

}

defaultproperties

{

bEdShouldSnap=true

InteractRadius = 386.0f

```
//Tower Icon
Begin Object class=SpriteComponent Name=Sprite
Sprite=Texture2D'Design_Allar.Textures.T_Sprite_TowerIcon_D'
HiddenGame=True
AlwaysLoadOnClient=False
AlwaysLoadOnServer=False
Translation=(Z=96)
End Object
Components.Add(Sprite);
Begin Object Class=DynamicLightEnvironmentComponent Name=MyLightEnvironment
bSynthesizeSHLight=TRUE
bIsCharacterLightEnvironment=TRUE
bUseBooleanEnvironmentShadowing=FALSE
End Object
Components.Add(MyLightEnvironment)
LightEnvironment=MyLightEnvironment
bCollideActors=true
bCollideWorld=true
bBlockActors=true
//Copied from UTPawn for the most part
Begin Object Class=SkeletalMeshComponent Name=WPawnSkeletalMeshComponent
bCacheAnimSequenceNodes=FALSE
AlwaysLoadOnClient=true
AlwaysLoadOnServer=true
bOwnerNoSee=false
CastShadow=true
BlockRigidBody=TRUE
bUpdateSkelWhenNotRendered=false
bIgnoreControllersWhenNotRendered=TRUE
bUpdateKinematicBonesFromAnimation=true
bCastDynamicShadow=true
Translation=(Z=8.0)
RBChannel=RBCC_Untitled3
RBCollideWithChannels=(Untitled3=true)
LightEnvironment=MyLightEnvironment
bOverrideAttachmentOwnerVisibility=true
bAcceptsDynamicDecals=FALSE
AnimTreeTemplate=None
bHasPhysicsAssetInstance=true
TickGroup=TG_PreAsyncWork
MinDistFactorForKinematicUpdate=0.2
bChartDistanceFactor=true
//bSkipAllUpdateWhenPhysicsAsleep=TRUE
RBDominanceGroup=20
Scale=1
SkeletalMesh=SkeletalMesh'Design_Allar.Mesh.SK_Building_Unconstructed'
//PhysicsAsset I made of my tile. Its just one block around the mesh
PhysicsAsset=PhysicsAsset'Design_Allar.Physics.SK_Building_Unconstructed_Physics'
MotionBlurScale=0.0
bAllowAmbientOcclusion=True
BlockActors=True
BlockNonZeroExtent=True
BlockZeroExtent=True
CollideActors=True
// Nice lighting for hair
bUseOnePassLightingOnTranslucency=TRUE
End Object
Mesh=WPawnSkeletalMeshComponent
CollisionComponent=WPawnSkeletalMeshComponent
Components.Add(WPawnSkeletalMeshComponent)
```


}[/csharp]