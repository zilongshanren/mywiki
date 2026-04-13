---
title: 'HTWeapon: Part 4 - Creating a Dynamic Muzzle Flash Light'
url: https://allarsblog.com/2010/03/26/htweapon-part-3-creating-a-dynamic-muzzle-flash-light/
author: Michael Allar
published: '2010-03-26'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

## Video Version

Subject: HTWeapon: Part 4 - Creating a Dynamic Muzzle Flash Light

Skill Level: Beginner

Run-Time: 17 minutes

Author: [Michael Allar](https://allarsblog.com/)

Notes: How to implement a UDKExplosionLight for your muzzle flash so that your gun will light up its surroundings when fired.

## Written Version

Subject: HTWeapon: Part 4 - Creating a Dynamic Muzzle Flash Light

Skill Level: Beginner

Author: [Michael Allar](http://allarsblog.com/)

Notes: How to implement a UDKExplosionLight for your muzzle flash so that your gun will light up its surroundings when fired.

See video for an in-depth explanation. Sorry about the indentation, it seems like my indentation will not survive copy paste… D:

### HTWP_M16_MuzzleLight

[csharp]

class HTWP_M16_MuzzleLight extends UDKExplosionLight;

defaultproperties

{

HighDetailFrameTime=+0.02

Brightness=8

Radius=96

LightColor=(R=255,G=255,B=255,A=255)

TimeShift=((StartTime=0.0,Radius=64,Brightness=5,LightColor=(R=240,G=237,B=17,A=255)),(StartTime=0.03,Radius=96,Brightness=8,LightColor=(R=248,G=192,B=12,A=255)),(StartTime=0.05,Radius=64,Brightness=0,LightColor=(R=255,G=150,B=20,A=255)))

}

[/csharp]

### HTWeapon

[csharp]

/*******************************************************************************

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

//If we aren't the client, make sure this pawn exists

//before we create a muzzle flash for it

if ( WorldInfo.NetMode != NM_Client )

{

P = HTPawn(Instigator);

if ( P == None )

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

//Our properties we made.

CrosshairImage=Texture2D'HTUI.Textures.T_UI_HUD_BaseA'

CrosshairCoordinates=(U=80,V=0,UL=50,VL=50)

MuzzleFlashSocket=MuzzleFlashSocket

MuzzleFlashDuration=0.05f

MuzzleFlashPSCTemplate(0)=ParticleSystem'HTEffects_Allar.Particles.PS_MuzzleFlash'

MuzzleFlashLightClass=class'UDKGame.HTWP_M16_MuzzleLight'

//Epic's default properties and stuff

Begin Object Name=FirstPersonMesh

DepthPriorityGroup=SDPG_Foreground

bOnlyOwnerSee=true

bOverrideAttachmentOwnerVisibility=true

CastShadow=false

bAllowAmbientOcclusion=false

End Object

Mesh=FirstPersonMesh

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

}

[/csharp]