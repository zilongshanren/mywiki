---
title: 'Allar’s Dev Diary #13: Day 2, Tower Defense Side Project'
url: https://allarsblog.com/2010/11/20/allars-dev-diary-13-day-2-tower-defense-side-project/
author: Michael Allar
published: '2010-11-20'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

If you don't know about my Tower Defense Side Project, please read [Day 1 here.](https://allarsblog.com/2010/11/allars-dev-diary-12-day-1-tower-defense-side-project)

# Day 2 (11/20/2010)

## 5. Creating The Camera

I've done a few third person cameras before so I was able to implement this system within a half hour. I did research some examples of isometric cameras beforehand however, and I ended up starting with this tutorial here (at X9 Productions) by Christian Roy. His provided code was simple and elegant so it would serve as a perfect slate to base my camera logic on. After implementing his tutorial code however, I found that my 'isometric' camera was only being properly shown if I typed behindview in console, but this is because I implemented it as a child of UTGame and not GameInfo. Normally I don't derive from UTGame but in the case of this project I did not want to have to deal with creating a new code base, but this also causes small issues like these. My solution was to simply force a SetBehindView call on the Pawn during its PostBeginPlay function and that remedied things for the most part. I also had to edit the CameraOffset and the CameraScaleMax variables to get the angle I wanted the camera to be at. Roy's tutorial implementation does not support camera zooming (however the source code he provides for download does, but I chose to implement it differently). I wanted it so the camera would stay locked and you can't zoom or rotate it unless you held down the middle mouse button and then moved the mouse or scrolled. In order to accomplish this, the first thing I had to do was to edit DefaultInput.ini and add the following bindings:

[csharp][//DefaultInput.ini](http://DefaultInput.ini)

.Bindings=(Name="MiddleMouseButton",Command="AllowCameraMovement true | onrelease AllowCameraMovement false")

.Bindings=(Name="MouseScrollUp",Command="HandleMouseScroll true")

.Bindings=(Name="MouseScrollDown",Command="HandleMouseScroll false")[/csharp]

This way two functions would be called, one when the MiddleMouseButton was pressed or released, and one when the scroll wheel was scrolled. AllowCameraMovement(bool bEnable) toggles whether or not the camera should rotate or zoom with the mouse, and HandleMouseScroll(bool bUp) handles what to do when the mouse is scrolled up or down.

[csharp][//CRPlayerController.uc](http://CRPlayerController.uc)

exec function AllowCameraMovement(bool bEnable)

{

bCameraMoving = bEnable;

}

exec function HandleMouseScroll(bool Up)

{

local UTPawn UTP;

```
UTP = UTPawn(Pawn);
if (UTP == none)
return;
//First write up, I wrote this so that it would change weapons if the
//middle mouse button wasn't being pressed down, but holding down the button
//and scrolling is really uncomfortable so I gave up mouse-weapon scrolling
UTP.CameraScale = FClamp(UTP.CameraScale + (Up ? -1.0 : 1.0), UTP.CameraScaleMin, UTP.CameraScaleMax);
```


}[/csharp]

As written in my code as a comment, when zooming was only possible while holding down the middle mouse button it just felt really uncomfortable and not nice, so instead I will always allow zooming whether or not the camera is set to allow for movement. I can still use the middle mouse button to unlock rotation, as I plan to aim with the mouse when the camera is locked so that the player will have a locked view but will always be shooting at where there cursor on the screen is instead of always looking in the direction they are aiming. Before we get there though, we must allow the camera to rotate first. Researching how UDK processes input with the class Engine.PlayerInput which is created within PlayerController ([url=http://udn.epicgames.com/Three/MasteringUnrealScriptClasses.html#WITHIN%20CLASSNAME]udn: within[/url]), I traced camera rotation to the function ProcessViewRotation being passed with PlayerInput data. I then took this concept and modified Roy's implementation a bit...

[csharp][//CRPlayerController.uc](http://CRPlayerController.uc)

simulated function PostBeginPlay()

{

super.PostBeginPlay();

```
ViewRotation.Pitch = (fCameraStartPitch * DegToRad) * RadToUnrRot;
ViewRotation.Yaw = (fCameraStartYaw * DegToRad) * RadToUnrRot;
SetCameraMode('BackCam');
```


}

function UpdateRotation( float DeltaTime )

{

local rotator DeltaRot;

```
if (bCameraMoving)
{
DeltaRot.Yaw = PlayerInput.aTurn;
DeltaRot.Pitch = PlayerInput.aLookUp;
ProcessViewRotation(DeltaTime,ViewRotation,DeltaRot);
}
SetRotation(ViewRotation);
```


}[/csharp]

Turns out its as easy as storing another rotator for our camera view, manipulate it with ProcessViewRotation if our middle mouse is down, and then set our rotation to our camera view. The reason we have to make a new rotator to store camera view is that if we use the Controller's rotation value directly, it might contain influence from outside actions that we do not want such as weapon or physics logic which causes the Pawn to propagate its rotation to its controller. With this set up, I now had a working camera that would rotate when the middle mouse button was held down. This then posed an awkward issue in which the player would not move in the direction of the camera but still be moving to the world axes, so moving forward always meant 'move north' instead of 'move towards where you are facing'. This felt a bit odd, so to fix this I had to make sure movement was pulling from the controllers rotation instead of the Pawn's rotation. This calculation is done in the Controller's PlayerMove function during the PlayerWalking state. Because I needed to change the function directly, I copied it over to the Controller class and made my very small code change within...

[csharp][//CRPlayerController.uc](http://CRPlayerController.uc)

//Stolen from UTPlayerController, only line was changed was the

//GetAxes line to use PlayerController rotation instead of Pawn rotation

//in calculating which direction to move.

state PlayerWalking

{

function PlayerMove( float DeltaTime )

{

local vector X,Y,Z, NewAccel;

local eDoubleClickDir DoubleClickMove;

local rotator OldRotation;

local bool bSaveJump;

```
if( Pawn == None )
{
GotoState('Dead');
}
else
{
GetAxes(Rotation,X,Y,Z); // Changed from Pawn.Rotation to our Rotation
//.......
//rest of the calculations here
//.......
```


[/csharp]

Now I have a camera that I can rotate when I unlock it, zoom whenever I want, and I can move in the direction the camera is facing!

Here is my current code at this point in the project. Don't expect future source code collections, I'm giving plenty of valuable info for you to implement yourself.

[download id="7"]

## 6. Updating My Site

I pretty much spent the rest of the day sleeping and formatting both day 1 and day 2 for Forecourse, as it was originally being posted elsewhere but I decided to officially move it into the public, so here ya go.

Stay tuned for Day 3!