---
title: 'Allar''s Dev Diary #16: Day 6, Tower Defense Side Project'
url: https://allarsblog.com/2010/11/24/allars-dev-diary-16-day-6-tower-defense-side-project/
author: Michael Allar
published: '2010-11-24'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

Sorry I'm 7 hours late with this posting, had to do some stuff.

# Day 6 (11/23/2010)

## 11. Weapon Archetype System

When designing the system for towers to be placed, I thought it would be cool to only have a few base tower classes and then allow for a lot of per tower customization and attributes through the use of Archetypes so I can tweak settings within the editor instead of compiling every time I wanted to change a setting and so that if anyone picks up my project they can add their own towers by just creating archetypes instead of figuring out how to derive and code their own towers. I figure I want to make modding design elements as easy as possible so that if one design doesn't work I can quickly switch to another. The problem with this was, I have had no experience in creating a dynamic system that uses object archetypes rather than actual hard coded classes. Being that towers might be a complex feat to make into an archetypal system as my first project with archetypes, I decided that I should convert the current weapon system to use archetypes so I have something to base on. This took a bit of time to figure out all the kinks, but what I ended up with was a solid base for a really cool way to create new games with ease and test weapon systems without compiling. This means that once I fully develop a custom weapon class, all in-game weapons will be based off of the same weapon class but their attributes will be set with object archetypes. Of course, the archetypal system should also allow for archetypes of classes that derive from my base weapon class, and that is supported simply by the fact that UnrealScript is already heavily object oriented.

Here is a really long and boring video of a brief overview of my most recent Dev Diary posts and how to use the Weapon Archetype System. One day I'll get a better voice, I swear. <_<



I also wanted a system that would allow for upgradeable weapons, i.e. when you do enough damage of a weapon it will level up and then you are given "upgrade points" that can be used to upgrade certain weapon stats that the weapon creator defines. The weapon creator can define these stat values per level per stat, and can also define how many "upgrade points" a stat is required to upgrade to the next level, with the player getting a specified amount of upgrade points per weapon level. In theory once this is fully implemented, it should be rather simple when given the appropriate AI, but I might make the weapon leveling system much simpler if it proves to be too complex. I won't implement actual weapon upgrading today, but I will provide support for it so all you have to do is increment a level of a stat for it to take effect. To do this, I made an enumeration of basic stats, and ten custom stats for future use, along with some structs to facilitate editor input and compartmentalize attribute aspects. These were the structs I came up with:

[csharp]class CRWeapon extends UTWeapon

HideCategories(Attachment,Collision,Debug,Mobile,Movement,Weapon,Object,Physics);

//Our weapons will only have a max of two fire modes

//to keep things simple for now

const MaxFireModes = 2;

//Bits that will be used to determine whether or not

//a weapon's particular stat is upgradeable

//and used for setting up custom weapon stat tables

enum EWeaponStats

{

WS_Damage, //Damage

WS_Accuracy, //Accuracy

WS_Range, //Range

WS_ROF, //Rate of fire

WS_Capacity, //Capacity

WS_AOE, //Area of Effect

WS_RechargeRate, //Recharge Rate

WS_Multishot, //Multishot

WS_CritChance, //Critical Chance

//Custom weapon stats for modding purposes?

WS_Custom1,

WS_Custom2,

WS_Custom3,

WS_Custom4,

WS_Custom5,

WS_Custom6,

WS_Custom7,

WS_Custom8,

WS_Custom9,

WS_Custom10

};

//Each WeaponStatInfo will store a stat's current level, upgrade cost, and

//values per level. When a stat is calculated, it will pull from

//StatLevelTable[StatLevel] for the value to use when firing and etc.

//If a WeaponStatInfo does not exist for a certain required stat i.e.

//damage, it will go ahead and automagically use a base variable such as

//var int BaseInstantHitDamage.

struct WeaponStatInfo

{

var() EWeaponStats WeaponStat;

var() int UpgradeCost <ClampMin=0.0>;

var int StatLevel;

//Stats at [level], i.e. StatLevelTable[0] = stat for level 1

var() editinline array<int> StatLevelTable <ClampMin=0.0>;

};

//This is the main struct that holds all of the dynamic weapon info for

//the weapons. Storing essential information such as its name, the name of

//the archetype itself for network replication (its much harder to replicate

//archetypes themselves), meshes, ui textures, and of course the stat table

struct WeaponInfo

{

//Weapon's name

var string WeaponName; //TODO: Allow for localization

var() string WeaponArchetypeName; //Name of the archetype for third person attachment reference. Should be our own name for now.

```
//Number of Levels for this weapon
var(Stats) int Levels <ClampMin=0.0>;
//Upgrade Points per Level
var(Stats) int UpgradePointsPerLevel <ClampMin=0.0>;
//List of upgradable weapon stats
var(Stats) editinline array<WeaponStatInfo> WeaponStatTable;
//Weapon Portrait Texture used for HUD
var(UI) Texture2D WeaponPortrait;
var(Mesh) SkeletalMesh FirstPersonWeaponMesh;
var(Mesh) SkeletalMesh ThirdPersonWeaponMesh;
var(Logic) EWeaponFireType WeaponFireType[MaxFireModes];
//TODO: Make a projectile archetype system
var(Logic) class<Projectile> WeaponProjectiles[MaxFireModes]; //For use with Projectile
//Shot cost per weapon fire
var(Logic) int ShotCost[MaxFireModes] <ClampMin=0.0>;
//Momentum for instant hits
var(Logic) int InstantHitMomentum[MaxFireModes] <ClampMin=0.0>;
var(Visuals) ParticleSystem MuzzleFlashes[MaxFireModes];
var(Visuals) ParticleSystem TracerRounds[MaxFireModes]; //For use with InstantHit
```


};

var(WeaponAttributes) int BaseInstantHitDamage[MaxFireModes];

var(WeaponAttributes) int BaseWeaponRange[MaxFireModes];

var(WeaponAttributes) int BaseFireInterval[MaxFireModes]; //seconds * 100

var(WeaponAttributes) int BaseMaxAmmoCount;

//Weapon Attributes which will be set in

//object archetypes within the editor

var(WeaponAttributes) editinline WeaponInfo MyWeaponInfo;[/csharp]

The WeaponInfo struct allows one to set every property they need for a weapon to work, including its meshes, muzzle flashes, and tracer rounds. For today I am only implementing support for instant fire weapons, as I want to design a Projectile archetypal system in the future as well.

With that said, now we should create some functions that allow for easy access to weapon stats and to grab the appropriate weapon stat data depending on if the weapon creator made a certain stat upgradeable or not. If not upgradeable it should use the base weapon stats, otherwise it should use the current stat based on that stat's level. This was actually rather simple to implement:

[csharp][//CRWeapon.uc](http://CRWeapon.uc)

//Searches the weapon stat table to see if a certain stat is defined

//and has appropriate level information. It returns the requested data if

//found, but returns -1 if the table does not contain data for that stat.

simulated function int SearchStatTable(EWeaponStats WeaponStat)

{

local WeaponStatInfo info;

```
foreach MyWeaponInfo.WeaponStatTable(info)
{
if (info.WeaponStat == WeaponStat)
{
if (info.StatLevelTable.length > 0 && info.StatLevel >= 0)
return info.StatLevelTable[Min(info.StatLevelTable.length-1,info.StatLevel)];
else
return -1;
}
}
return -1;
```


}

//Searches our weapon table and returns the appropriate weapon data.

//Returns base weapon values if a stat is not upgradeable.

simulated function int GetWeaponStat(EWeaponStats WeaponStat)

{

local int StatData;

StatData = SearchStatTable(WeaponStat);

```
//TODO: Allow multiple fire mode support
switch (WeaponStat)
{
case WS_Damage:
return StatData == -1 ? BaseInstantHitDamage[0] : StatData;
case WS_Accuracy:
return StatData == -1 ? 0 : 0; //TODO: Implement Accuracy
case WS_Range:
return StatData == -1 ? BaseWeaponRange[0] : StatData;
case WS_ROF: //ROF = time in seconds * 100
return StatData == -1 ? BaseFireInterval[0] : StatData;
case WS_Capacity:
return StatData == -1 ? BaseMaxAmmoCount : StatData;
case WS_AOE:
return StatData == -1 ? 0 : StatData; //TODO: Implement AOE
case WS_RechargeRate:
return StatData == -1 ? 0 : StatData; //TODO: Implement Recharge Rate
case WS_Multishot:
return StatData == -1 ? 0 : StatData; //TODO: Implement Multishot
case WS_CritChance:
return StatData == -1 ? 0 : StatData; //TODO: Implement Critical Chance
case WS_Custom1:
case WS_Custom2:
case WS_Custom3:
case WS_Custom4:
case WS_Custom5:
case WS_Custom6:
case WS_Custom7:
case WS_Custom8:
case WS_Custom9:
case WS_Custom10:
return StatData == -1 ? 0 : StatData;
default:
`log("::GetWeaponStat: Invalid Weapon Stat given :-(");
return 0;
}
```


}[/csharp]

Now that we have a way to get our weapon values, we need to implement this system into the rest of the weapon calculations. Basically, we must copy all the current existing weapon logic and replace weapon value references with our own stat system. I'm not really going to describe this too much, its fairly straight forward.

[csharp][//CRWeapon.uc](http://CRWeapon.uc)

function class<Projectile> GetProjectileClass()

{

return (CurrentFireMode < MaxFireModes) ? MyWeaponInfo.WeaponProjectiles[CurrentFireMode] : None;

}

simulated event float GetTraceRange()

{

return GetWeaponStat(WS_Range);

}

simulated function float GetFireInterval( byte FireModeNum )

{

//Rate of fire stored as seconds*100

return fmax(GetWeaponStat(WS_ROF)/100.0f,0.01);

}

//TODO: Make a better way to cache that somehow picks up

//upgrade level changes.

simulated function float MaxRange()

{

local int i;

```
// return the range of the fire mode that fires farthest
if (bInstantHit)
CachedMaxRange = GetWeaponStat(WS_Range);
for (i = 0; i < MaxFireModes; i++)
{
if (MyWeaponInfo.WeaponProjectiles[i] != None)
CachedMaxRange = FMax(CachedMaxRange, MyWeaponInfo.WeaponProjectiles[i].static.GetRange());
}
return CachedMaxRange;
```


}

//////////////////////////////////////////////////////////////////

// AMMO

//

//Copied from UTWeapon

//Modified to use our stat tables

//////////////////////////////////////////////////////////////////

function int AddAmmo( int Amount )

{

local int MaxAmmo;

MaxAmmo = GetWeaponStat(WS_Capacity);

```
AmmoCount = Clamp(AmmoCount + Amount,0,MaxAmmo);
// check for infinite ammo
if (AmmoCount <= 0 && (UTInventoryManager(InvManager) == None || UTInventoryManager(InvManager).bInfiniteAmmo))
{
AmmoCount = MaxAmmo;
}
return AmmoCount;
```


}

simulated function bool AmmoMaxed(int mode)

{

return (AmmoCount >= GetWeaponStat(WS_Capacity));

}

simulated function bool HasAmmo( byte FireModeNum, optional int Amount )

{

if (Amount==0)

return (AmmoCount >= MyWeaponInfo.ShotCost[FireModeNum]);

else

return ( AmmoCount >= Amount );

}

simulated function bool HasAnyAmmo()

{

return ( ( AmmoCount > 0 ) || (MyWeaponInfo.ShotCost[0]==0 && MyWeaponInfo.ShotCost[1]==0) );

}

simulated function float DesireAmmo(bool bDetour)

{

return (1.f - float(AmmoCount)/GetWeaponStat(WS_Capacity));

}

simulated function Loaded(optional bool bUseWeaponMax)

{

if (bUseWeaponMax)

AmmoCount = GetWeaponStat(WS_Capacity);

else

AmmoCount = 10000;

}

//////////////////////////////////////////////////////////////////

// FIRING

//

//Copied from UTWeapon

//Modified to use our stat tables

//////////////////////////////////////////////////////////////////

simulated function ProcessInstantHit(byte FiringMode, ImpactInfo Impact, optional int NumHits)

{

local bool bFixMomentum;

local KActorFromStatic NewKActor;

local StaticMeshComponent HitStaticMesh;

local int TotalDamage;

```
if ( Impact.HitActor != None )
{
if ( Impact.HitActor.bWorldGeometry )
{
HitStaticMesh = StaticMeshComponent(Impact.HitInfo.HitComponent);
if ( (HitStaticMesh != None) && HitStaticMesh.CanBecomeDynamic() )
{
NewKActor = class'KActorFromStatic'.Static.MakeDynamic(HitStaticMesh);
if ( NewKActor != None )
{
Impact.HitActor = NewKActor;
}
}
}
if ( !Impact.HitActor.bStatic && (Impact.HitActor != Instigator) )
{
if ( Impact.HitActor.Role == ROLE_Authority && Impact.HitActor.bProjTarget
&& !WorldInfo.GRI.OnSameTeam(Instigator, Impact.HitActor)
&& Impact.HitActor.Instigator != Instigator
&& PhysicsVolume(Impact.HitActor) == None )
{
HitEnemy++;
LastHitEnemyTime = WorldInfo.TimeSeconds;
}
if ( (UTPawn(Impact.HitActor) == None) && (MyWeaponInfo.InstantHitMomentum[FiringMode] == 0) )
{
MyWeaponInfo.InstantHitMomentum[FiringMode] = 1;
bFixMomentum = true;
}
// default damage model is just hits * base damage
NumHits = Max(NumHits, 1);
TotalDamage = GetWeaponStat(WS_Damage) * NumHits;
Impact.HitActor.TakeDamage( TotalDamage, Instigator.Controller,
Impact.HitLocation, MyWeaponInfo.InstantHitMomentum[FiringMode] * Impact.RayDir,
InstantHitDamageTypes[FiringMode], Impact.HitInfo, self );
if (bFixMomentum)
MyWeaponInfo.InstantHitMomentum[FiringMode] = 0;
}
}
```


}[/csharp]

Now we are almost done. The last critically important thing is for the attachment logic to be updated to use our meshes in our archetype, otherwise we won't be able to see our weapons! Now there is a lot of code here, but a majority of it is also straight from UTGame but with slight modifications to use our stored data instead. The biggest and most important thing to note is that we must replicate the name of our archetype to other pawns so that they have the needed weapon info to set up the weapon attachments that non-local pawns use . Without sending a reference to the archetype, our clients will have no idea what meshes and particles to use with the third person representation of our weapons. To do this, I made a new string variable in CRPawn called CurrentWeaponAttachmentArchetypeName, possibly one of the longer if not the longest variable names I've used, which is then populated with the archetype name string in MyWeaponInfo.

[csharp] [//CRWeapon.uc](http://CRWeapon.uc)

//////////////////////////////////////////////////////////////////

// Attachment

//

//Copied from UTWeapon

//Modified to use our object archetype data

//////////////////////////////////////////////////////////////////

simulated function AttachWeaponTo( SkeletalMeshComponent MeshCpnt, optional Name SocketName )

{

local CRPawn CRTP;

```
CRTP = CRPawn(Instigator);
// Attach 1st Person Muzzle Flashes, etc,
if ( Instigator.IsFirstPerson() )
{
SkeletalMeshComponent(Mesh).SetSkeletalMesh(MyWeaponInfo.FirstPersonWeaponMesh);
AttachComponent(Mesh);
EnsureWeaponOverlayComponentLast();
SetHidden(True);
bPendingShow = TRUE;
Mesh.SetLightEnvironment(CRTP.LightEnvironment);
if (GetHand() == HAND_Hidden)
{
CRTP.ArmsMesh[0].SetHidden(true);
CRTP.ArmsMesh[1].SetHidden(true);
if (CRTP.ArmsOverlay[0] != None)
{
CRTP.ArmsOverlay[0].SetHidden(true);
CRTP.ArmsOverlay[1].SetHidden(true);
}
}
}
else
{
SetHidden(True);
if (CRTP != None)
{
Mesh.SetLightEnvironment(CRTP.LightEnvironment);
CRTP.ArmsMesh[0].SetHidden(true);
CRTP.ArmsMesh[1].SetHidden(true);
if (CRTP.ArmsOverlay[0] != None)
{
CRTP.ArmsOverlay[0].SetHidden(true);
CRTP.ArmsOverlay[1].SetHidden(true);
}
}
}
SetWeaponOverlayFlags(CRTP);
// Spawn the 3rd Person Attachment
if (Role == ROLE_Authority && CRTP != None)
{
//For replication to work, we need to send the name of our archetype asset
//to all other pawns so that they can use it in their weapon attachment
//classes, as they do not have access to everyones Weapon instances
//and will have no way of knowing of the meshes or particles to use
//for other people's third person models.
CRTP.CurrentWeaponAttachmentArchetypeName = MyWeaponInfo.WeaponArchetypeName;
CRTP.CurrentWeaponAttachmentClass = AttachmentClass;
if (WorldInfo.NetMode == NM_ListenServer || WorldInfo.NetMode == NM_Standalone || (WorldInfo.NetMode == NM_Client && Instigator.IsLocallyControlled()))
CRTP.WeaponAttachmentChanged();
}
SetSkin(UTPawn(Instigator).ReplicatedBodyMaterial);
```


}

simulated function AttachMuzzleFlash()

{

local SkeletalMeshComponent SKMesh;

```
// Attach the Muzzle Flash
bMuzzleFlashAttached = true;
SKMesh = SkeletalMeshComponent(Mesh);
if ( SKMesh != none )
{
if ( (MyWeaponInfo.MuzzleFlashes[0] != none) || (MyWeaponInfo.MuzzleFlashes[1] != none) )
{
//Set our muzzle flash templates to the ones in our Archetype
MuzzleFlashPSCTemplate = MyWeaponInfo.MuzzleFlashes[0];
MuzzleFlashAltPSCTemplate = MyWeaponInfo.MuzzleFlashes[1];
MuzzleFlashPSC = new(Outer) class'UTParticleSystemComponent';
MuzzleFlashPSC.bAutoActivate = false;
MuzzleFlashPSC.SetDepthPriorityGroup(SDPG_Foreground);
MuzzleFlashPSC.SetFOV(UDKSkeletalMeshComponent(SKMesh).FOV);
SKMesh.AttachComponentToSocket(MuzzleFlashPSC, MuzzleFlashSocket);
}
}
```


}[/csharp]

With all that done, I went ahead and tacked on a little something to stop weapons from drawing default UT crosshairs. Also, I set the weapon to use our weapon attachment class that we will be writing.

[csharp][//CRWeapon.uc](http://CRWeapon.uc)

//Disable that damn crosshair

simulated function ActiveRenderOverlays( HUD H )

{

//Don't render weapon crosshairs here

}

defaultproperties

{

AttachmentClass=class'CRWeaponAttachment'

}[/csharp]

Phew. Now that is over with, we need to create the Weapon Attachment class that will be used by clients and for third person weapon logic. This is actually quite simple, the tricky part is getting the attachment to get a reference of the archetype that stores all the data. This will be replicated in the Pawn by creating an instance of an archetype and storing it in CurrentWeaponAttachmentArchetype when the Pawn recieves a new CurrentWeaponAttachmentArchetypeName. This should be done prior to the WeaponAttachment attaching function calls so we can assume the data is already there for us in our WeaponAttachment.

In addition to this, our weapon attachment should create tracer rounds when needed so lets override ThirdPersonFireEffects to support this. For our tracers to work, our tracers must be a particle system with beam data that has a target module with a parameter for target position, like so![53. Particle System Tracer](https://allarsblog.com/CastilloRTS/Blockout/53_ParticleSystemTracer.jpg)

[http://allarsblog.com/CastilloRTS/Blockout/53_ParticleSystemTracer.jpg](http://allarsblog.com/CastilloRTS/Blockout/53_ParticleSystemTracer.jpg))

[csharp]/*******************************************************************************

CRWeaponAttachment

```
Creation date: 23/11/2010 12:52
Copyright (c) 2010, Allar
```


*******************************************************************************/

class CRWeaponAttachment extends UTWeaponAttachment;

simulated function AttachTo(UTPawn OwnerPawn)

{

local CRPawn CRP;

SetWeaponOverlayFlags(OwnerPawn);

CRP = CRPawn(OwnerPawn);

if (CRP != none && OwnerPawn.Mesh != None)

{

// Attach Weapon mesh to player skelmesh

if ( CRP.CurrentWeaponAttachmentArchetype.MyWeaponInfo.ThirdPersonWeaponMesh != None && Mesh != none)

{

//Set the skeletal mesh of our attachment to the one stored

//in our weapons archetype

Mesh.SetSkeletalMesh(CRP.CurrentWeaponAttachmentArchetype.MyWeaponInfo.ThirdPersonWeaponMesh);

OwnerMesh = OwnerPawn.Mesh;

AttachmentSocket = OwnerPawn.WeaponSocket;

```
// Weapon Mesh Shadow
Mesh.SetShadowParent(OwnerPawn.Mesh);
Mesh.SetLightEnvironment(OwnerPawn.LightEnvironment);
if (OwnerPawn.ReplicatedBodyMaterial != None)
{
SetSkin(OwnerPawn.ReplicatedBodyMaterial);
}
OwnerPawn.Mesh.AttachComponentToSocket(Mesh, OwnerPawn.WeaponSocket);
}
if (OverlayMesh != none)
{
OwnerPawn.Mesh.AttachComponentToSocket(OverlayMesh, OwnerPawn.WeaponSocket);
}
}
if (MuzzleFlashSocket != '')
{
//If our archetype has a muzzle flash reference, lets go ahead and
//store those references in our WeaponAttachment for use with the
//already existing muzzle flash system that UTWeapon provides
if (CRP.CurrentWeaponAttachmentArchetype.MyWeaponInfo.MuzzleFlashes[0] != None || CRP.CurrentWeaponAttachmentArchetype.MyWeaponInfo.MuzzleFlashes[1] != None)
{
MuzzleFlashPSCTemplate = CRP.CurrentWeaponAttachmentArchetype.MyWeaponInfo.MuzzleFlashes[0];
MuzzleFlashAltPSCTemplate = CRP.CurrentWeaponAttachmentArchetype.MyWeaponInfo.MuzzleFlashes[1];
MuzzleFlashPSC = new(self) class'UTParticleSystemComponent';
MuzzleFlashPSC.bAutoActivate = false;
MuzzleFlashPSC.SetOwnerNoSee(true);
Mesh.AttachComponentToSocket(MuzzleFlashPSC, MuzzleFlashSocket);
}
}
OwnerPawn.SetWeapAnimType(WeapAnimType);
GotoState('CurrentlyAttached');
```


}

simulated function ThirdPersonFireEffects(vector HitLocation)

{

local CRPawn P;

local ParticleSystemComponent PSC;

local vector MuzzleLoc;

if ( EffectIsRelevant(Location,false,MaxFireEffectDistance) )

{

// Light it up

CauseMuzzleFlash();

}

```
// Have pawn play firing anim
P = CRPawn(Instigator);
if (P != None && P.GunRecoilNode != None)
{
// Use recoil node to move arms when we fire
P.GunRecoilNode.bPlayRecoil = true;
}
if (Instigator.FiringMode == 1 && AltFireAnim != 'None')
{
Mesh.PlayAnim(AltFireAnim,,, false);
}
else if (FireAnim != 'None')
{
Mesh.PlayAnim(FireAnim,,, false);
}
//Lets get some tracer round action going on. As there can possibly
//be a lot of tracers being rendered, I will leave it up to the
//EmitterPool to spawn our tracers instead of forcing spawning here.
if (MuzzleFlashPSC != none && P.CurrentWeaponAttachmentArchetype.MyWeaponInfo.TracerRounds[Instigator.FiringMode] != none)
{
//Fire tracer rounds from our weapon muzzle. This assumes that our
//weapons have a muzzle flash socket named MuzzleFlashSocket.
//We shouldn't really be assuming anything, but the weapon variable
//MuzzleFlashSocket is set to 'MuzzleFlashSocket' and can't change
//by any other means, and its pretty easy to just add a socket to our weapon meshes
Mesh.GetSocketWorldLocationAndRotation(MuzzleFlashSocket,MuzzleLoc);
PSC = WorldInfo.MyEmitterPool.SpawnEmitter(P.CurrentWeaponAttachmentArchetype.MyWeaponInfo.TracerRounds[Instigator.FiringMode],MuzzleLoc);;
PSC.SetVectorParameter('TracerEnd',HitLocation);
PSC.ActivateSystem();
}
```


}

defaultproperties

{

MuzzleFlashSocket=MuzzleFlashSocket

}[/csharp]

Cool. Now we just need to set up our Pawn to replicate our Weapon Archetype for the WeaponAttachment to use. This is also fairly simple, first we must make a replicated string variable storing the path to the WeaponArchetype, and then we must be able to store an instance of our WeaponArchetype. Then when our weapon attachment is changed (which happens in CRWeapon at the end of the AttachWeaponTo function) we should create that instance. This is the code that I added to facilitate this:

[csharp][//CRPawn.uc](http://CRPawn.uc)

var repnotify string CurrentWeaponAttachmentArchetypeName;

var CRWeapon CurrentWeaponAttachmentArchetype;

replication

{

if (bNetDirty)

CurrentWeaponAttachmentArchetypeName;

}

simulated function WeaponAttachmentChanged()

{

CurrentWeaponAttachmentArchetype = CRWeapon(DynamicLoadObject(CurrentWeaponAttachmentArchetypeName,class'CRWeapon'));

super.WeaponAttachmentChanged();

}[/csharp]

Boom. I'm now going to create a weapon archetype for an MP5A3 that I just have laying around from another project called Plastic Warfare made by Cordell Felix. Went ahead and pulled a few values, some from actual MP5A3 mechanics, others are arbitrary. Also connected a few sounds and particles for muzzles and tracers, nothing fancy just some programmer art. I won't go into how I created these assets as there are many, many, many other resources on asset creation. An important note for setting up your weapon archetype, once you make it, you will need to right click it in the content browser and copy the full name of the asset. Then you need to paste it into the Weapon Archetype Name field, otherwise your archetype will not be replicated and used for third person meshes. Also, you don't need to set every variable because not all of them are implemented yet, i.e. Weapon Portrait](

[http://allarsblog.com/CastilloRTS/Blockout/54_CRWeap_MP5A3.JPG](http://allarsblog.com/CastilloRTS/Blockout/54_CRWeap_MP5A3.JPG))

The very last thing we need to do now is to actually give it to the player. I haven't written a nice give weapon function that supports these archetypes yet, but I did give the player my MP5 as part of every Pawn's default weapon inventory. This is done by overriding our AddDefaultInventory in our GameInfo class:

[csharp][//CRGame.uc](http://CRGame.uc)

function AddDefaultInventory( pawn PlayerPawn )

{

local int i;

local CRWeapon NewWeapon;

```
// may give the physics gun to non-bots
if( bGivePhysicsGun && PlayerPawn.IsHumanControlled() )
{
PlayerPawn.CreateInventory(class'UTWeap_PhysicsGun',true);
}
//For generic inventory items
for (i=0; i<DefaultInventory.Length; i++)
{
// Ensure we don't give duplicate items
if (PlayerPawn.FindInventoryType( DefaultInventory[i] ) == None)
{
// Only activate the first weapon
PlayerPawn.CreateInventory(DefaultInventory[i], (i > 0));
}
}
//For CRWeapon Archetypes
//Take note that we are adding an instance of CRWeapon using our
//archetype as a spawn template, instead of leaving this up
//to the inventory manager as in the DefaultInventory loop above.
for (i=0; i<DefaultWeapons.Length; i++)
{
NewWeapon = Spawn(class'CRWeapon',,,,,DefaultWeapons[i]);
NewWeapon.Loaded(true);
PlayerPawn.InvManager.AddInventory(NewWeapon);
}
PlayerPawn.AddDefaultInventory();
```


}

defaultproperties

{

HUDType=class'CastilloRTS.CRGFxHudWrapper'

```
bDelayedStart=false
PlayerControllerClass=class'CastilloRTS.CRPlayerController'
DefaultPawnClass=class'CastilloRTS.CRPawn'
//Explicitly clear out DefaultInventory
DefaultInventory(0)=None
DefaultInventory(1)=None
DefaultInventory(2)=None
//Add a reference to our archetype to our DefaultWeapons array.
DefaultWeapons(0)=CRWeapon'Design_Allar.Archetypes.Weapons.CRWeap_MP5A3'
Name="Default__MyGameInfo"
```


}[/csharp]

Now that wasn't so hard was it? :-). Now we have a base for creating upgradable custom weapon archetypes without being limited to creating a class for every type of weapon we would want. Further development here will lead to a powerful weapon system that will allow for anyone adding their own weapons into this project. The next step is to tie it into the HUD, and then apply this archetype system to building towers! This will have to be done another day though.