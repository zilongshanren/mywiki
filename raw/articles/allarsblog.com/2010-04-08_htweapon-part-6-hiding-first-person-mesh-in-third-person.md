---
title: 'HTWeapon: Part 6 - Hiding First Person Mesh In Third Person'
url: https://allarsblog.com/2010/04/08/htweapon-part-6-hiding-first-person-mesh-in-third-person/
author: Michael Allar
published: '2010-04-08'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

## Video Version

Subject: HTWeapon: Part 6 - Hiding First Person Mesh In Third Person

Skill Level: Beginner

Run-Time: 5 minutes

Author: [Michael Allar](https://allarsblog.com/)

Notes: How to make your weapon deal damage upon firing.

## Written Version

Subject: HTWeapon: Part 6 - Hiding First Person Mesh In Third Person

Skill Level: Beginner

Author: [Michael Allar](http://allarsblog.com/)

Notes: How to hide your first person mesh while in third person

No written version here, just code. If you want to write this up, contact me.

### HTWeapon

[csharp]/*******************************************************************************

HTWeapon

Creation date: 08/03/2010 06:21

Copyright (c) 2010, Allar

*******************************************************************************/

class HTWeapon extends UDKWeapon;

/** Max ammo count */

var int MaxAmmoCount;

/** Holds the amount of ammo used for a given shot */

var array<int> ShotCost;

/** Offset from view center */

var(FirstPerson) vector PlayerViewOffset;

/** HUD Stuff */

var Texture CrosshairImage;

var UIRoot.TextureCoordinates CrosshairCoordinates;

var bool bPrintScreenDebug;

/*********************************************************************************************

Muzzle Flash

********************************************************************************************* */

/** Holds the name of the socket to attach a muzzle flash too */

var name MuzzleFlashSocket;

/** Muzzle flash PSC and Templates*/

var HTParticleSystemComponent MuzzleFlashPSC;

/** Array of Particle Systems for our firemodes */

var array<ParticleSystem> MuzzleFlashPSCTemplate;

/** How long the Muzzle Flash should be there */

var() float MuzzleFlashDuration;

/** Whether muzzleflash has been initialized */

var bool bMuzzleFlashAttached;

/** dynamic light */

var UDKExplosionLight MuzzleFlashLight;

/** dynamic light class */

var class<UDKExplosionLight> MuzzleFlashLightClass;

/*********************************************************************************************

Replication

********************************************************************************************* */

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

/*********************************************************************************************

Muzzle Flash Methods

********************************************************************************************* */

/**

- PlayFireEffects Is the root function that handles all of the effects associated with
- a weapon. This function creates the 1st person effects. It should only be called
- on a locally controlled player.

*/**

simulated function PlayFireEffects( byte FireModeNum, optional vector HitLocation )

{

// Start muzzle flash effect

CauseMuzzleFlash();

}

/ - Called on a client, this function Attaches the MuzzleFlashParticleSystemComponent

*/

simulated function AttachMuzzleFlash()

{

local SkeletalMeshComponent SKMesh;

// Attach the Muzzle Flash

bMuzzleFlashAttached = true;

SKMesh = SkeletalMeshComponent(Mesh);

if ( SKMesh != none )

{

//if our weapon has at least one muzzle flash

//lets attach our muzzle flash particle system component

if ( MuzzleFlashPSCTemplate.Length > 0 )

{

MuzzleFlashPSC = new(Outer) class'HTParticleSystemComponent';

MuzzleFlashPSC.bAutoActivate = false;

MuzzleFlashPSC.SetDepthPriorityGroup(SDPG_Foreground);

MuzzleFlashPSC.SetFOV(UDKSkeletalMeshComponent(SKMesh).FOV);

SKMesh.AttachComponentToSocket(MuzzleFlashPSC, MuzzleFlashSocket);

}

}

}

/**

- Causes the muzzle flashlight to turn on

*/

simulated event CauseMuzzleFlashLight()

{

// don't do muzzle flashes when running too slow, except on mobile, where we need it to show off dynamic lighting

if ( WorldInfo.bDropDetail && !WorldInfo.IsConsoleBuild(CONSOLE_Mobile) )

{

return;

}

if ( MuzzleFlashLight != None )

{

MuzzleFlashLight.ResetLight();

}

else if ( MuzzleFlashLightClass != None )

{

MuzzleFlashLight = new(Outer) MuzzleFlashLightClass;

SkeletalMeshComponent(Mesh).AttachComponentToSocket(MuzzleFlashLight,MuzzleFlashSocket);

}

}

/**

- Causes the muzzle flash to turn on and setup a time to
- turn it back off again.

*/

simulated event CauseMuzzleFlash()

{

local HTPawn P;

local ParticleSystem MuzzleTemplate;

PrintScreenDebug("Causing Muzzle Flash");

//if we aren't the client, make sure this pawn exists

//before we create a muzzle flash for it

if ( WorldInfo.NetMode != NM_Client )

{

P = HTPawn(Instigator);

if ( P == None || !P.IsFirstPerson())

{

return;

}

}

CauseMuzzleFlashLight();

//Only proceed if our firing mode has a muzzle flash

if (Instigator.FiringMode < MuzzleFlashPSCTemplate.Length)

{

if ( !bMuzzleFlashAttached )

{

AttachMuzzleFlash();

}

if (MuzzleFlashPSCTemplate[Instigator.FiringMode] != None)

{

if (!MuzzleFlashPSC.bIsActive || MuzzleFlashPSC.bWasDeactivated)

{

MuzzleTemplate = MuzzleFlashPSCTemplate[Instigator.FiringMode];

//If our current PSC is using a different muzzle flash particle

//Lets go ahead and swap it with the one we need

if (MuzzleTemplate != MuzzleFlashPSC.Template)

{

MuzzleFlashPSC.SetTemplate(MuzzleTemplate);

}

SetMuzzleFlashParams(MuzzleFlashPSC);

MuzzleFlashPSC.ActivateSystem();

}

}

// Set when to turn it off.

SetTimer(MuzzleFlashDuration,false,'MuzzleFlashTimer');

}

}

/**

- Turns the MuzzleFlashPSC off

*/

simulated event MuzzleFlashTimer()

{

if (MuzzleFlashPSC != none)

{

MuzzleFlashPSC.DeactivateSystem();

}

}

simulated event StopMuzzleFlash()

{

ClearTimer('MuzzleFlashTimer');

MuzzleFlashTimer();

if ( MuzzleFlashPSC != none )

{

MuzzleFlashPSC.DeactivateSystem();

}

}

/**

- Allows a child to setup custom parameters on the muzzle flash

*/

simulated function SetMuzzleFlashParams(ParticleSystemComponent PSC)

{

return;

}

/*********************************************************************************************

- Ammunition / Inventory

*********************************************************************************************/

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

/*********************************************************

* HUD Stuff

*********************************************************/

/**

- Draw the Crosshairs

*/

simulated function DrawWeaponCrosshair( Hud HUD )

{

local vector2d CrosshairSize;

local float x,y, ScreenX, ScreenY;

local HTHUD H;

H = HTHUD(HUD);

if ( H == None )

return;

CrosshairSize.Y = CrosshairCoordinates.VL * H.Canvas.ClipY/720;

CrosshairSize.X = CrosshairSize.Y * ( CrosshairCoordinates.UL / CrosshairCoordinates.VL );

X = H.Canvas.ClipX * 0.5;

Y = H.Canvas.ClipY * 0.5;

ScreenX = X - (CrosshairSize.X * 0.5);

ScreenY = Y - (CrosshairSize.Y * 0.5);

if ( CrosshairImage != none )

{

// crosshair drop shadow

H.Canvas.DrawColor = H.CrosshairShadowColor;

H.Canvas.SetPos( ScreenX+1, ScreenY+1 );

H.Canvas.DrawTile(CrosshairImage,CrosshairSize.X, CrosshairSize.Y, CrossHairCoordinates.U, CrossHairCoordinates.V, CrossHairCoordinates.UL,CrossHairCoordinates.VL);

H.Canvas.DrawColor = H.CrosshairColor;

H.Canvas.SetPos(ScreenX, ScreenY);

H.Canvas.DrawTile(CrosshairImage,CrosshairSize.X, CrosshairSize.Y, CrossHairCoordinates.U, CrossHairCoordinates.V, CrossHairCoordinates.UL,CrossHairCoordinates.VL);

}

}

function PrintScreenDebug(string debugText)

{

local PlayerController PC;

if (bPrintScreenDebug)

{

PC = PlayerController(Pawn(Owner).Controller);

if (PC != None)

PC.ClientMessage("HTWeapon: " $ debugText);

}

}

simulated function AttachWeaponTo( SkeletalMeshComponent MeshCpnt, optional Name SocketName )

{

local HTPawn HTP;

HTP = HTPawn(Instigator);

AttachComponent(mesh);

SetHidden(false);

mesh.SetLightEnvironment(HTP.LightEnvironment);

if (!Instigator.IsFirstPerson())

mesh.SetHidden(true);

}

simulated event SetPosition(UDKPawn Holder)

{

local vector DrawOffset, ViewOffset, FinalLocation;

local rotator NewRotation, FinalRotation, SpecRotation;

local PlayerController PC;

local vector2D ViewportSize;

local vector SpecViewLoc;

if (Holder == none)

return;

if (!Holder.IsFirstPerson())

{

mesh.SetHidden(true);

return;

}

else

Mesh.SetHidden(false);

foreach LocalPlayerControllers(class'PlayerController', PC)

{

LocalPlayer(PC.Player).ViewportClient.GetViewportSize(ViewportSize);

break;

}

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

FinalLocation = SpecViewLoc + DrawOffset;

SetLocation(FinalLocation);

SetBase(Holder);

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

FinalRotation = NewRotation;

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

//Our properties we made.

CrosshairImage=Texture2D'HTUI.Textures.T_UI_HUD_BaseA'

CrosshairCoordinates=(U=80,V=0,UL=50,VL=50)

MuzzleFlashSocket=MuzzleFlashSocket

MuzzleFlashDuration=0.05f

MuzzleFlashPSCTemplate(0)=ParticleSystem'HTEffects_Allar.Particles.PS_MuzzleFlash'

MuzzleFlashLightClass=class'UDKGame.HTWP_M16_MuzzleLight'

bPrintScreenDebug = false;

//Epic's default properties and stuff

Begin Object Name=FirstPersonMesh

DepthPriorityGroup=SDPG_Foreground

bOnlyOwnerSee=true

bOverrideAttachmentOwnerVisibility=true

CastShadow=false

bAllowAmbientOcclusion=false

End Object

mesh=FirstPersonMesh

Begin Object Name=PickupMesh

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