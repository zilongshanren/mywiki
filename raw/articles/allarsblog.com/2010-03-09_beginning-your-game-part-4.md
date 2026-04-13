---
title: Beginning Your Game Part 4
url: https://allarsblog.com/2010/03/09/beginning-your-game-part-4/
author: Michael Allar
published: '2010-03-09'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

## Video Version

Subject: Beginning Your Game Part 4

Skill Level: Beginner

Run-Time: 54 Minutes

Author: [Michael Allar](https://allarsblog.com/)

Notes: Setting up HTInventoryManager, HTInventory, HTWeapon

## Written Version

Subject: Beginning Your Game Part 4

Skill Level: Beginner

Author: [Michael Allar](http://allarsblog.com/)

Notes: Setting up HTInventoryManager, HTInventory, HTWeapon

See the video for an in-depth explanation.

### HTInventoryManager

[csharp]/*******************************************************************************

HTInventoryManager

Creation date: 08/03/2010 07:03

Lots of code stolen from Epic

*******************************************************************************/

class HTInventoryManager extends InventoryManager

config(Game);

/** Holds the last weapon used */

var Weapon PreviousWeapon;

simulated function GetWeaponList(out array<HTWeapon> WeaponList, optional bool bNoEmpty)

{

local HTWeapon Weap;

ForEach InventoryActors( class'HTWeapon', Weap )

{

if ( !bNoEmpty || Weap.HasAnyAmmo())

{

WeaponList.Insert(0,1);

WeaponList[0] = Weap;

}

}

}

/**

- Accessor for the server to begin a weapon switch on the client.
- @param DesiredWeapon The Weapon to switch to

*/

reliable client function ClientSetCurrentWeapon(Weapon DesiredWeapon)

{

SetPendingWeapon(DesiredWeapon);

}

simulated function Inventory CreateInventory(class<Inventory> NewInventoryItemClass, optional bool bDoNotActivate)

{

if (Role==ROLE_Authority)

{

return Super.CreateInventory(NewInventoryItemClass, bDoNotActivate);

}

return none;

}

/**

- Handle AutoSwitching to a weapon

*/

simulated function bool AddInventory( Inventory NewItem, optional bool bDoNotActivate )

{

local bool bResult;

if (Role == ROLE_Authority)

{

bResult = super.AddInventory(NewItem, bDoNotActivate);

}

return bResult;

}

simulated function DiscardInventory()

{

local Vehicle V;

if (Role == ROLE_Authority)

{

Super.DiscardInventory();

V = Vehicle(Owner);

if (V != None && V.Driver != None && V.Driver.InvManager != None)

{

V.Driver.InvManager.DiscardInventory();

}

}

}

simulated function RemoveFromInventory(Inventory ItemToRemove)

{

if (Role==ROLE_Authority)

{

Super.RemoveFromInventory(ItemToRemove);

}

}

/**

- Scans the inventory looking for any of type InvClass. If it finds it it returns it, other
- it returns none.

*/

function Inventory HasInventoryOfClass(class<Inventory> InvClass)

{

local inventory inv;

inv = InventoryChain;

while(inv!=none)

{

if (Inv.Class==InvClass)

return Inv;

Inv = Inv.Inventory;

}

return none;

}

/**

- Store the last used weapon for later

*/

simulated function ChangedWeapon()

{

PreviousWeapon = Instigator.Weapon;

Super.ChangedWeapon();

}

simulated function SwitchToPreviousWeapon()

{

if ( PreviousWeapon!=none && PreviousWeapon != Pawn(Owner).Weapon )

{

PreviousWeapon.ClientWeaponSet(false);

}

}

defaultproperties

{

bMustHoldWeapon=true

PendingFire(0)=0

PendingFire(1)=0

}

[/csharp]

### HTInventory

[csharp]/*******************************************************************************

HTInventory

Creation date: 08/03/2010 07:06

Copyright (c) 2010, Allar

*******************************************************************************/

class HTInventory extends Inventory;[/csharp]

### HTWeapon

[csharp]/*******************************************************************************

HTWeapon

Creation date: 08/03/2010 06:21

Copyright (c) 2010, Allar

*******************************************************************************/

class HTWeapon extends UDKWeapon;

/** Current ammo count */

var repnotify int AmmoCount;

/** Max ammo count */

var int MaxAmmoCount;

/** Holds the amount of ammo used for a given shot */

var array<int> ShotCost;

/** Offset from view center */

var(FirstPerson) vector PlayerViewOffset;

replication

{

// Server->Client properties

if ( bNetOwner )

AmmoCount;

}

simulated event ReplicatedEvent(name VarName)

{

if ( VarName == 'AmmoCount' )

{

if ( !HasAnyAmmo() )

{

WeaponEmpty();

}

}

else

{

Super.ReplicatedEvent(VarName);

}

}

simulated function int GetAmmoCount()

{

return AmmoCount;

}

/*

- Consumes some of the ammo

*/

function ConsumeAmmo( byte FireModeNum )

{

// Subtract the Ammo

AddAmmo(-ShotCost[FireModeNum]);

}

/**

- This function is used to add ammo back to a weapon. It's called from the Inventory Manager

*/

function int AddAmmo( int Amount )

{

AmmoCount = Clamp(AmmoCount + Amount,0,MaxAmmoCount);

return AmmoCount;

}

/**

- Returns true if the ammo is maxed out

*/

simulated function bool AmmoMaxed(int mode)

{

return (AmmoCount >= MaxAmmoCount);

}

/**

- This function checks to see if the weapon has any ammo available for a given fire mode.
- @param FireModeNum - The Fire Mode to Test For
- @param Amount - [Optional] Check to see if this amount is available. If 0 it will default to checking

* for the ShotCost

*/

simulated function bool HasAmmo( byte FireModeNum, optional int Amount )

{

if (Amount==0)

return (AmmoCount >= ShotCost[FireModeNum]);

else

return ( AmmoCount >= Amount );

}

/**

- returns true if this weapon has any ammo

*/

simulated function bool HasAnyAmmo()

{

return ( ( AmmoCount > 0 ) || (ShotCost[0]==0 && ShotCost[1]==0) );

}

/**

- This function retuns how much of the clip is empty.

*/

simulated function float DesireAmmo(bool bDetour)

{

return (1.f - float(AmmoCount)/MaxAmmoCount);

}

/**

- Returns true if the current ammo count is less than the default ammo count

*/

simulated function bool NeedAmmo()

{

return ( AmmoCount < Default.AmmoCount );

}

/**

- Cheat Help function the loads out the weapon
- @param bUseWeaponMax - [Optional] If true, this function will load out the weapon

* with the actual maximum, not 999

*/

simulated function Loaded(optional bool bUseWeaponMax)

{

if (bUseWeaponMax)

AmmoCount = MaxAmmoCount;

else

AmmoCount = 999;

}

/**

- Called when the weapon runs out of ammo during firing

*/

simulated function WeaponEmpty()

{

// If we were firing, stop

if ( IsFiring() )

{

GotoState('Active');

}

if ( Instigator != none && Instigator.IsLocallyControlled() )

{

Instigator.InvManager.SwitchToBestWeapon( true );

}

}

/*********************************************************************************************

- Ammunition / Inventory

*********************************************************************************************/

function PrintScreenDebug(string debugText)

{

local PlayerController PC;

PC = PlayerController(Pawn(Owner).Controller);

if (PC != None)

PC.ClientMessage("HTWeapon: " $ debugText);

}

simulated function AttachWeaponTo( SkeletalMeshComponent MeshCpnt, optional Name SocketName )

{

local HTPawn HTP;

HTP = HTPawn(Instigator);

PrintScreenDebug("Attaching Weapon");

// Attach 1st Person Muzzle Flashes, etc,

if ( Instigator.IsFirstPerson() )

{

AttachComponent(Mesh);

EnsureWeaponOverlayComponentLast();

SetHidden(False);

Mesh.SetLightEnvironment(HTP.LightEnvironment);

PrintScreenDebug("First Person Weapon Attached");

}

else

{

SetHidden(True);

if (HTP != None)

{

Mesh.SetLightEnvironment(HTP.LightEnvironment);

}

}

//SetSkin(HTPawn(Instigator).ReplicatedBodyMaterial);

}

simulated event SetPosition(UDKPawn Holder)

{

local vector DrawOffset, ViewOffset, FinalLocation;

local rotator NewRotation, FinalRotation, SpecRotation;

local PlayerController PC;

local vector2D ViewportSize;

local bool bIsWideScreen;

local vector SpecViewLoc;

if ( !Holder.IsFirstPerson() )

return;

Mesh.SetHidden(False);

foreach LocalPlayerControllers(class'PlayerController', PC)

{

LocalPlayer(PC.Player).ViewportClient.GetViewportSize(ViewportSize);

break;

}

bIsWideScreen = (ViewportSize.Y > 0.f) && (ViewportSize.X/ViewportSize.Y > 1.7);

Mesh.SetScale3D(default.Mesh.Scale3D);

Mesh.SetRotation(default.Mesh.Rotation);

ViewOffset = PlayerViewOffset;

// Calculate the draw offset

if ( Holder.Controller == None )

{

if ( DemoRecSpectator(PC) != None )

{

PC.GetPlayerViewPoint(SpecViewLoc, SpecRotation);

DrawOffset = ViewOffset >> SpecRotation;

//DrawOffset += UTPawn(Holder).WeaponBob(BobDamping, JumpDamping);

FinalLocation = SpecViewLoc + DrawOffset;

SetLocation(FinalLocation);

SetBase(Holder);

// Add some rotation leading

[//SpecRotation.Yaw](http://SpecRotation.Yaw) = LagRot(SpecRotation.Yaw & 65535, LastRotation.Yaw & 65535, MaxYawLag, 0);

[//SpecRotation.Pitch](http://SpecRotation.Pitch) = LagRot(SpecRotation.Pitch & 65535, LastRotation.Pitch & 65535, MaxPitchLag, 1);

//LastRotUpdate = WorldInfo.TimeSeconds;

//LastRotation = SpecRotation;

if ( bIsWideScreen )

{

//SpecRotation += WidescreenRotationOffset;

}

SetRotation(SpecRotation);

return;

}

else

{

DrawOffset = (ViewOffset >> Holder.GetBaseAimRotation()) + HTPawn(Holder).GetEyeHeight() * vect(0,0,1);

PrintScreenDebug("Setting DrawOffset to Holder Info");

}

}

else

{

DrawOffset.Z = HTPawn(Holder).GetEyeHeight();

//DrawOffset += HTPawn(Holder).WeaponBob(BobDamping, JumpDamping);

if ( HTPlayerController(Holder.Controller) != None )

{

DrawOffset += HTPlayerController(Holder.Controller).ShakeOffset >> Holder.Controller.Rotation;

}

DrawOffset = DrawOffset + ( ViewOffset >> Holder.Controller.Rotation );

}

// Adjust it in the world

FinalLocation = Holder.Location + DrawOffset;

SetLocation(FinalLocation);

SetBase(Holder);

NewRotation = (Holder.Controller == None) ? Holder.GetBaseAimRotation() : Holder.Controller.Rotation;

// Add some rotation leading

//if (Holder.Controller != None)

//{

// FinalRotation.Yaw = LagRot(NewRotation.Yaw & 65535, LastRotation.Yaw & 65535, MaxYawLag, 0);

// FinalRotation.Pitch = LagRot(NewRotation.Pitch & 65535, LastRotation.Pitch & 65535, MaxPitchLag, 1);

// FinalRotation.Roll = NewRotation.Roll;

//}

//else

//{

FinalRotation = NewRotation;

//}

//LastRotUpdate = WorldInfo.TimeSeconds;

//LastRotation = NewRotation;

if ( bIsWideScreen )

{

//FinalRotation += WidescreenRotationOffset;

}

SetRotation(FinalRotation);

}

simulated state WeaponEquipping

{

simulated event BeginState(Name PreviousStateName)

{

PrintScreenDebug("Weapon Equipping");

AttachWeaponTo(Instigator.Mesh);

Super.BeginState(PreviousStateName);

}

}

simulated state Active

{

simulated event BeginState(Name PreviousStateName)

{

PrintScreenDebug("Active");

Super.BeginState(PreviousStateName);

}

}

simulated state WeaponFiring

{

simulated event BeginState(Name PreviousStateName)

{

PrintScreenDebug("Firing");

Super.BeginState(PreviousStateName);

}

/**

- We override BeginFire() so that we can check for zooming and/or empty weapons

*/

simulated function BeginFire( Byte FireModeNum )

{

// No Ammo, then do a quick exit.

if( !HasAmmo(FireModeNum) )

{

WeaponEmpty();

return;

}

Global.BeginFire(FireModeNum);

}

}

defaultproperties

{

Begin Object Class=UDKSkeletalMeshComponent Name=FirstPersonMesh

DepthPriorityGroup=SDPG_Foreground

bOnlyOwnerSee=true

bOverrideAttachmentOwnerVisibility=true

CastShadow=false

bAllowAmbientOcclusion=false

End Object

Mesh=FirstPersonMesh

Begin Object Class=SkeletalMeshComponent Name=PickupMesh

bOnlyOwnerSee=false

CastShadow=false

bForceDirectLightMap=true

bCastDynamicShadow=false

CollideActors=false

BlockRigidBody=false

bUseAsOccluder=false

MaxDrawDistance=6000

bForceRefPose=1

bUpdateSkelWhenNotRendered=false

bIgnoreControllersWhenNotRendered=true

bAcceptsStaticDecals=FALSE

bAcceptsDynamicDecals=FALSE

bAllowAmbientOcclusion=false

End Object

DroppedPickupMesh=PickupMesh

PickupFactoryMesh=PickupMesh

MessageClass=class'UTPickupMessage'

DroppedPickupClass=class'UTDroppedPickup'

FiringStatesArray(0)=WeaponFiring

FiringStatesArray(1)=WeaponFiring

WeaponFireTypes(0)=EWFT_InstantHit

WeaponFireTypes(1)=EWFT_InstantHit

WeaponProjectiles(0)=none

WeaponProjectiles(1)=none

FireInterval(0)=+0.3

FireInterval(1)=+0.3

Spread(0)=0.0

Spread(1)=0.0

ShotCost(0)=1

ShotCost(1)=1

AmmoCount=5

MaxAmmoCount=5

InstantHitDamage(0)=0.0

InstantHitDamage(1)=0.0

InstantHitMomentum(0)=0.0

InstantHitMomentum(1)=0.0

InstantHitDamageTypes(0)=class'DamageType'

InstantHitDamageTypes(1)=class'DamageType'

WeaponRange=22000

ShouldFireOnRelease(0)=0

ShouldFireOnRelease(1)=0

DefaultAnimSpeed=0.9

EquipTime=+0.45

PutDownTime=+0.33

}[/csharp]