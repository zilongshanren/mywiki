---
title: 'Allar’s Dev Diary #14: Day 3, Tower Defense Side Project'
url: https://allarsblog.com/2010/11/20/allars-dev-diary-14-tower-defense-side-project/
author: Michael Allar
published: '2010-11-20'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

# Day 3 (11/20/2010)

## 7. Aiming With The Mouse

Now that I got the camera set up yesterday and played a lot of Vindictus, its time to get back to work. The next step is to get the player to aim towards where their mouse instead of in the direction the player camera is facing. This way movement and aim will be separated and allow for interaction with the world with the freedom of rotation but locking movement to the camera axis. Basically, the player will be controlled like most top-down shooters. Now for this project I am currently using the September build of UDK even though the October build is out as this project is also meant to help some classmates with their project which is currently September based. The reason I bring this up is that the October build of UDK strips out all UIScene functionality completely and everything related to it and in the past the class UIRoot was my primary way of accessing mouse coordinates. This means that for my project to not need a major reworking in the future I would have to find a new way to grab mouse coordinates. Now I looked all over the UDK development code and I could not find a straightforward way to do so. If there is a easier way than the process that I went to that I will go over, please let me know. The way I did it relies on a SWF to store mouse coordinates which then UnrealScript grabs. Its a little odd but it works flawlessly once set up correctly. I figured that if I used ScaleForm to grab mouse coordinates, Epic won't be scrapping ScaleForm any time soon.

The first thing we are going to need to do is to replace the UT HUD with our own ScaleForm based HUD. As fancy as the UT HUD is, I'd rather have my own. Also, I need to create mouse coordinate functionality without relying on the old hud's Canvas to use DeProject, which I'll get into later. For now, I don't need anything fancy in my HUD except a mouse cursor which will indicate where the player is aiming and will also serve as a cursor for UI interaction with HUD menus and things. Time to start up Flash and build me a HUD. I am using a trial version of Flash CS5 at the moment.

With Flash CS5, I have already set up my ScaleForm extension and my ActionScript settings. If you have not dealt with ScaleForm and Flash before, I strongly encourage checking out my ScaleForm series [here](https://allarsblog.com/unreal-tutorials/). With my new flash document open, I went ahead and drew myself a cursor with the flash tools, and this is what I came up with](

[http://allarsblog.com/CastilloRTS/Blockout/46_Cursor.JPG](http://allarsblog.com/CastilloRTS/Blockout/46_Cursor.JPG))

Fairly simple, but it will do. Now there are many ways to have cursor functionality in Flash but I chose to implement a form made by Marc Rogerson over at his site ([http://www.f00n.com/unreal/2010/06/30/flash-cursor-class-as2-0/](http://www.f00n.com/unreal/2010/06/30/flash-cursor-class-as2-0/?ref=allarsblog.com)). I've been using this implementation for quite a few projects actually, however I made a small change to his cursor class which I'll list here:

[csharp]

//Code by Marc Rogerson at

//http://www.f00n.com/unreal/2010/06/30/flash-cursor-class-as2-0/

import gfx.managers.PopUpManager;

class gfx.controls.Cursor extends MovieClip {

//public vars

public var _disabled:Boolean = false;

```
//Allar: I changed mCursor to public so that I can access it
//far easier in UnrealScript by grabbing the mouse clip directly
//and storing it as a GFxObject
public var mCursor:MovieClip;
//private vars
private var libraryMC:String;
//instantiate the class
public function Cursor(linkage:String) {
//Allar: I think I hardcoded this name here,
//and I'm not sure why. :0
libraryMC = "movCursor";
//initialise
init();
}
private function init():Void {
//attach the cursor with the PopUpManager class
createCursor();
}
private function createCursor():Void {
//create the pop up
mCursor = PopUpManager.createPopUp(_root, libraryMC);
//set the dimensions of the cursor **possibly make this a public function**
setCursorDims(25, 25, mCursor);
//enable the cursor
this.enable();
}
private function setCursorDims(w:Number, h:Number, o:MovieClip):Void {
o._width = w;
o._height = h;
}
//disable the cursor
public function disable():Void {
mCursor.stopDrag();
mCursor._visible = false;
_disabled = true;
}
//enable the cursor
public function enable():Void {
mCursor.startDrag(true);
mCursor._visible = true;
_disabled = false;
}
```


}[/csharp]

Fairly straight forward, I like this simple and elegant solution to mouse cursors. With that said, I took my drawing of a mouse cursor and made it into a movieclip, put it in my library, and exported for actionscript with the identifier "movCursor". As per Marc's tutorial, I also added this snippet on my first frame of my empty flash document.

[csharp]stop();

var myCursor = new gfx.controls.Cursor("movCursor");[/csharp]

I then set my flash document stage's size to 1280x1024, as I tend to do all my ScaleForm work on this stage size. As far as I know, there is no set standard you should use. It is important to explicitly make a size however ans this will factor into mouse coordinate calculations later. With this done, I went ahead and published my .swf and imported it into a package.

Once imported, the next step was to create a GFxMoviePlayer class that would load up our hud movie. This class is really rather simple:

[csharp]/*******************************************************************************

CRGFxHUD

```
Creation date: 20/11/2010 06:25
Copyright (c) 2010, Allar
```


*******************************************************************************/

class CRGFxHUD extends GFxMoviePlayer;

//MouseCursor MovieClip

var GFxObject MouseCursor;

function Init(optional LocalPlayer player)

{

super.Init(player);

```
Start();
Advance(0);
MouseCursor = GetVariableObject("_root.myCursor.mCursor");
```


}

defaultproperties

{

MovieInfo=SwfMovie'Design_Allar.CR_UI_HUD'

}[/csharp]

Pretty simple, nothing all that extravagant here. I did declare a GFxObject variable however to store my mouse cursor and when the movie is loaded, I go ahead and grab the movie clip with GetVariableObject which tells ScaleForm to fetch you whatever object variable you want in your Scaleform document. As you can see, I am fetching the member variable mCursor of the Cursor instance I made in Flash, and that is why I allowed the member variable to be public instead of private. Might be a bit of bad practice to do so, but this cursor isn't going to see much internal action other than this.

With that set up, I went ahead and built my HUD class:

[csharp]/*******************************************************************************

CRGFxHudWrapper

```
Creation date: 20/11/2010 06:28
Copyright (c) 2010, Allar
```


*******************************************************************************/

class CRGFxHudWrapper extends UTHUDBase;

//our SWF class

var CRGFxHUD HudMovie;

//expected size of our SWF (defaultproperties)

var vector2D HudMovieSize;

//Cache'd Player Controller

var CRPlayerController CRPC;

simulated function PostBeginPlay()

{

super.PostBeginPlay();

```
CreateHUDMovie();
CRPC = CRPlayerController(PlayerOwner);
if (CRPC != none)
CRPC.MyGFxHUD = self;
```


}

//Converts GFx Mouse Coordinates to

//in-game screen coordinates, compensating for differing viewport sizes

function vector2D GetGFxMouseCoordinates(optional bool bRelative)

{

local vector2D MousePos;

local float coordinateScaling;

HudMovie.MouseCursor.GetPosition(MousePos.X,MousePos.Y);

```
coordinateScaling = FMin(SizeX/HudMovieSize.X,SizeY/HudMovieSize.Y);
MousePos*=coordinateScaling;
MousePos.X += (SizeX - (HudMovieSize.X*coordinateScaling))/2;
if (bRelative)
{
MousePos.X /= SizeX;
MousePos.Y /= SizeY;
}
return MousePos;
```


}

/**

- Create and initialize the HUDMovie.

*/

function CreateHUDMovie()

{

HudMovie = new class'CRGFxHUD';

HudMovie.SetTimingMode(TM_Real);

HudMovie.Init(class'Engine'.static.GetEngine().GamePlayers[HudMovie.LocalPlayerOwnerIndex]);

HudMovie.SetAlignment(Align_TopCenter);

}

defaultproperties

{

HudMovieSize=(X=1280,Y=1024);

}[/csharp]

Theres not a lot going on here but what is happening is very key. One of the first things you notice is that I'm storing a size vector for our movie which is then set to 1280,1024. If there is a way to find the size of any given .swf, please let me know, until then this is how I will establish the expected swf size and I will use these values for mouse coordinate calculations. The reason we need to know this size is that if our game resolution is not the same as our .swf resolution, the mouse movieclip's position will not be the same as its actual position. For instance, when the screen is wider than our .SWF, if the cursor is near the left edge of the screen it will be off the stage of our .swf and then its x coordinate will be fetched as negative, as the movieclip is only aware of its existence in ScaleForm world and not in the game world. To compensate for this, in the function GetGFxMouseCoordinates, we check to see if our resolution is different than our hud and if it is we add half of our game resolution minus our .swf size. This offsets our ScaleForm coordinates to match our game coordinates. I also make sure it is aligned TopCenter so that this algorithm works. If you were to align it TopLeft, then no calculations would be made as ScaleForm coordinates would then match the game coordinates, however I always prefer my .swfs centered so I can push out to fit widescreen instead of pushing elements to the right only. The last thing to mention about this function is that it can also return relative coordinates when bRelative is true. Relative coordinates range from 0 to 1 instead of being pixel based on the resolution. This is needed for a future function call DeProject which I will get into later.

Another thing you should notice is that I'm storing a direct reference of my HUD inside my PlayerController itself, this why my PlayerController has a cached reference of this HUD and will have an easier time calling GetGFxMouseCoordinates.

Now that I have a way of accessing mouse coordinates from my PlayerController, I re-worked my UpdateRotation function to update the rotation of the Pawn as well based on mouse location. Here are my changes:

[csharp][//CRPlayerController.uc](http://CRPlayerController.uc)

var vector MouseWorldLocation, MouseWorldNormal;

function UpdateRotation( float DeltaTime )

{

local rotator DeltaRot, AimRot,ViewRot;

local vector WorldDirection,ViewPoint;

local vector2d MouseRelativeCoords;

```
if (bCameraMoving)
{
DeltaRot.Yaw = PlayerInput.aTurn;
DeltaRot.Pitch = PlayerInput.aLookUp;
ProcessViewRotation(DeltaTime,ViewRotation,DeltaRot);
}
if (self.IsLocalPlayerController())
{
MouseRelativeCoords = MyGFxHUD.GetGFxMouseCoordinates(true);
LocalPlayer(Player).DeProject(MouseRelativeCoords,MouseWorldLocation,WorldDirection);
self.GetPlayerViewPoint(ViewPoint,ViewRot);
Trace(MouseWorldLocation, MouseWorldNormal, ViewPoint+WorldDirection*10000, ViewPoint + WorldDirection*10, true);
AimRot = rotator(MouseWorldLocation - Pawn.Location);
Pawn.SetRotation(AimRot);
}
SetRotation(ViewRotation);
```


}[/csharp]

Pretty simple. In order to DeProject our mouse coordinates to our game world to figure out where our mouse is over we have to use a LocalPlayer. A LocalPlayer is a class that represents the 'real-life player' themselves, not their game character. On multi-player games, you are always a LocalPlayer while every other Pawn/PlayerController has just a regular Player. We can only DeProject with LocalPlayer and Canvas, however I want to be able to UpdateRotation whenever needed and not rely on a Canvas object which only seems to be present during a HUD's post-render, if it exists at all. Also, to make this project more future proof, I am straying from UIScene and Canvas code. With that said, PlayerControllers store a Player class, not a LocalPlayer. To ensure that our casting and calculations will be valid, I use the built in function IsLocalPlayerController instead of doing a traditional typecast-checknone. If we are a local player controller, our Player is guaranteed to be a LocalPlayer. We can then cast it and then use DeProject. There is a difference between LocalPlayer's DeProject and the Canvas DeProject, in that the LocalPlayer DeProject is a bit slower and it uses relative screen coordinates instead of actual screen coordinates (for split screen support). DeProject then takes two variables, one to output the world position of the mouse and the direction from that point to the world it was projected from. The world position is not on the world itself where you'd expect it to be, but is instead literally where your mouse is on your screen and lies on your screen plane. We must trace this point back down to the world using the direction DeProject retrieved to get the actual position of where the mouse is hovering over by drawing a line from the point on your screen and into the level through 3d space. To do this, we need to get the position of where we currently viewing from in 3d space and this is done by GetPlayerViewPoint. Once we have where our camera is, we trace a line from a point 10 units in front of us to make sure we don't hit our camera itself down then down to a point 10000 units away from our camera in the direction of how the mouse was DeProjected onto the world. This then updates MouseWorldLocation to be the exact location of what our mouse is hovering over in our world, along with the normal of the surface it has hit. From there we subtract our Pawn's location and cast it into a Rotator, which gives us a rotation for our Pawn that will face our MouseWorldLocation. We then set our Pawn's rotation accordingly, thus making our Pawn aim wherever our mouse is!

Now that that is done, if we run around and shoot our weapons you might notice that the projectiles are not coming from the muzzle of the gun but from the Pawn. We will fix this when we develop our own custom weapons, there is no need to fix this now and for the most part is merely cosmetic.

## 8. Getting A Tower Set Up

Now that our player can run around and kill things, we need to start figuring out how we are going to set up towers to shoot players. To do this, I decided to look up some reference but I couldn't find anything exactly what I wanted so I'm going to be loosely basing this approach off of the turret on [UDN]([http://udn.epicgames.com/Three/MasteringUnrealScriptStates.html#CHAPTER](http://udn.epicgames.com/Three/MasteringUnrealScriptStates.html?ref=allarsblog.com#CHAPTER) 11 – STATES). With that said, I've decided that my towers are going to be based off of the Pawn class. Also, I want these actors to completely replace my buildable tiles in the level, so I want this base Tower class to have a standard default mesh when created or placed. I've also decided that the base class of the tower will represent a tower in its non-constructed state and that it will swap to a derived class when it needs to become a tower of a different kind. Because of this, I figured the current tile mesh would be a great temporary mesh to use in the mean time so I went ahead and made a form of the tile rigged to a bone so that I can import it as a skeletal mesh. Using ActorX and 3ds Max this is pretty simple, however you can use any method that will get a skeletal mesh in-game. Now because of the fact that im using the same mesh, I don't want to confuse myself as to which tiles are tower actors and which are just mesh instances, so I created a little icon to be placed above my tower actors when editing](

[http://allarsblog.com/CastilloRTS/Blockout/47_TowerIcon.JPG](http://allarsblog.com/CastilloRTS/Blockout/47_TowerIcon.JPG))And heres a quick little picture of how I rigged my tile](

[http://allarsblog.com/CastilloRTS/Blockout/48_RiggingTile.JPG](http://allarsblog.com/CastilloRTS/Blockout/48_RiggingTile.JPG))

With my skeletal mesh imported, I went ahead and created my new Pawn class which currently only has its mesh set along with the tower icon for editing purposes.

[csharp]/*******************************************************************************

CRTowerBase

```
Creation date: 20/11/2010 17:29
Copyright (c) 2010, Allar
This class will serve as an unconstructed tower
```


*******************************************************************************/

class CRTowerBase extends UDKPawn HideCategories(Camera,Attachment,AI,Debug,Mobile,Physics,Swimming,TeamBeacon,UDKPawn)

placeable;

/** The pawn's light environment */

var DynamicLightEnvironmentComponent LightEnvironment;

//These things should do nothing on damage taking.

event TakeDamage(int Damage, Controller InstigatedBy, vector HitLocation, vector Momentum, class<DamageType> DamageType, optional TraceHitInfo HitInfo, optional Actor DamageCauser)

{

return;

}

defaultproperties

{

bEdShouldSnap=true

```
//Tower Icon
Begin Object Name=Sprite
Sprite=Texture2D'Design_Allar.Textures.T_Sprite_TowerIcon_D'
HiddenGame=True
AlwaysLoadOnClient=False
AlwaysLoadOnServer=False
Translation=(Z=96)
End Object
Begin Object Class=DynamicLightEnvironmentComponent Name=MyLightEnvironment
bSynthesizeSHLight=TRUE
bIsCharacterLightEnvironment=TRUE
bUseBooleanEnvironmentShadowing=FALSE
End Object
Components.Add(MyLightEnvironment)
LightEnvironment=MyLightEnvironment
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
bAllowAmbientOcclusion=false
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
//Not using the cylinder component for collision
Components.Remove(CollisionCylinder)
```


}[/csharp]

So now our base tower class doesn't really do anything except take the form of my blue tile with a tower icon above it. This is enough to start replacing our blue tiles with though, but unfortunately selecting our tiles and clicking Replace with CRTowerBase isn't working for me for some reason. I believe this is something dealing with the fact that we are deriving from Pawn, so we are going to have to delete our tiles and manually replace them with our CRTowerBases. While researching why I couldn't replace, I added another class that will allow me to add an unconstructed tower by just right clicking anywhere on the map, going to Add Actor, and selecting the new Unconstructed Tower option. This was relatively simple to accomplish.

[csharp]/*******************************************************************************

CRActorFactoryTower

```
Creation date: 20/11/2010 18:26
```


*******************************************************************************/

class CRActorFactoryTower extends ActorFactory

config(Editor)

collapsecategories

hidecategories(Object);

defaultproperties

{

MenuName="Add Unconstructed Tower"

NewActorClass=class'CastilloRTS.CRTowerBase'

}[/csharp]

Now time to go in and replace all my tiles with this tower base..](

[http://allarsblog.com/CastilloRTS/Blockout/49_TowersInPlace.JPG](http://allarsblog.com/CastilloRTS/Blockout/49_TowersInPlace.JPG))