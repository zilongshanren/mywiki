---
title: Creating A Third-Person Camera
url: https://allarsblog.com/2010/03/31/creating-a-third-person-camera/
author: Michael Allar
published: '2010-03-31'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

Where is the video version? Its below the written version, because the written version came out much better.

## Written Version

Subject: Creating A Third-Person Camera

Skill Level: Intermediate

Author: [Michael Allar](https://allarsblog.com/)

Notes: How to implement a third person camera.

### Background Info - Pawn

When Unreal calculates your camera view to use when a PlayerController possesses a Pawn, a lot of things are happening. First of all, there exists a whole Camera system underlying Unreal's framework, but it is very transparent as you do not have to rely on it too much. After a lot of different and irrelevant things take place, the base Camera class asks the actor we are viewing (which can be -any- actor) if it would like to calculate the camera point-of-view instead. We can use this to our advantage to write a custom third person view without needing to sub-class and rework the Camera hierarchy. When an actor is asked to calculate the camera, the actor executes the CalcCamera function within it. CalcCamera is a "simulated" function, able to be called on both the server and the client, and returns a boolean. This boolean will be returned as true if our actor has decided to control our camera, and false if not. When returning false, the underlying Camera system figures out what to do based on other things going on within the engine. Because we want to calculate the camera ourselves, we will be returning true. To manipulate the camera, CalcCamera takes a few arguments that are propagated to the Camera system where it will handle rendering and more for us. All we have to do is manipulate the information its requesting.

##### CylinderComponent

Every Pawn class has a CylinderComponent that defines a rough approximation of our player to use for collision and size. While you don't have to concern yourself too much about this, using this for an approximation of our character size will speed up calculations for our third person camera so we do not have to implement complex logic for precise camera clipping. Because we can retrieve the radius and height of this component, setting the CollisionRadius and CollisionHeight to match your player as best it can is a very wise choice as the more accurate this component is, the more precise your character will collide with objects in-game and the better our camera calculations will be. The default settings for this CylinderComponent are declared in Pawn.uc within the defaultproperties block. Note that it is only listed here for reference, and not for inclusion in our code.

Pawn.uc:

[csharp]Begin Class=CylinderComponent Object Name=CollisionCylinder

CollisionRadius=+0034.000000

CollisionHeight=+0078.000000

BlockNonZeroExtent=true

BlockZeroExtent=true

BlockActors=true

CollideActors=true

End Object

CollisionComponent=CollisionCylinder

CylinderComponent=CollisionCylinder

Components.Add(CollisionCylinder)[/csharp]

If your character is a bit bigger or smaller than a 34 radius with 78 units of height, you can change these values in your own Pawn class. This is how it is implemented in HTPawn.uc

HTPawn.uc

[csharp]defaultproperties

{

//Lots of stuff here...

CameraZOffset=48

CameraTranslateScale=(X=5,Y=-2,Z=1)

Begin Object Name=CollisionCylinder

CollisionRadius=+0036.000000

CollisionHeight=+0096.000000

End Object

```
//More stuff here...
```


}[/csharp]

#### CalcCamera defined in Actor.uc

[csharp]/**

* Calculate camera view point, when viewing this actor.

*

- @param fDeltaTime delta time seconds since last update
- @param out_CamLoc Camera Location
- @param out_CamRot Camera Rotation
- @param out_FOV Field of View
- @return true if Actor should provide the camera point of view.

*/

simulated function bool CalcCamera( float fDeltaTime, out vector out_CamLoc, out rotator out_CamRot, out float out_FOV )[/csharp]

The comment pretty much tells us exactly what we need to know. When our function ends, the values of out_CamLoc and out_CamRot will become the location and rotation for our camera. We will not be adjusting Field of View in this tutorial, but we will revisit this in the future.

#### 3D Math Ahead!

In order to calculate the location and rotation for our Camera, a bit of vector math is involved. You don't have to know too much vector math for what we are doing here, but the more you learn the better you can solve complex problems like this in the future. If you are completely new to vector math, I highly suggest getting a copy of [3D Math Primer for Graphics and Game Development](http://www.amazon.com/Primer-Graphics-Development-Wordware-Library/dp/1556229119/ref=sr_1_1?ie=UTF8&s=books&qid=1270035676&sr=8-1&ref=allarsblog.com). It is relatively cheap compared to similar books, is easy to read, and offers great insight into beginner vector math. It also provides C++ examples of implementation but the explanation of the math involved alone will help you out tremendously. (I get no money for advertising/linking to this book, this is a only a solid recommendation by someone who owns it.)

### Coordinate Spaces

A basic understanding of the concept of multiple coordinate spaces or coordinate systems is needed to make sense of a few of the calculations involved in setting up our third person camera. The two spaces we will be working with are **local** and **world** space.

#### Local Space

Local space is something we use every day when describing the location of an object relative to another. You can think of local space as you would your room.

[caption id="attachment_493" align="alignleft" width="300" caption="My Room As Itself"][/caption]![MyRoom](../../assets/a469d9345b20376e.jpg)


Treating my room as local space, it has its own coordinate axes. For now, lets treat this as a 2D space with only X and Y. While my room is the object we are looking at (in our third person camera implementation, think of our room as our player himself)

When we describe the position of our individual components, we use our defined axes to compare. In local space, my desk is in front of my chair. My chair is to the left of my computer. My computer and my chair are to the right of my bed. My door is below my bed. Another way to describe this is my desk is further along the Y axis than my chair is. My computer is further along X than my chair. If you were to imagine a grid overlaid on my room with my door being at (X=0, Y=0), or the bottom left corner of my room, or the origin of my room, another way to phrase the comparison is my bed has a lesser X value than my computer.

If you were to take this same logic and apply it to your player model, you would say your right arm is further along X than your torso which should be centered at 0. Your left arm then has a lesser X value than your torso, in which case it would have a negative X value.

Every object can be broken down into its own space as well. If we were to see our room as world space, we could examine the local space of the bed, desk, or chair. The chair has its own axes, and you could say the backrest is further along Z (throwing in a height axis) than the base of your chair. You could however define your local space to have Z facing in the negative direction so that you could say your backrest is below your chair! Every object has its own local space, and every object within that object has their own local space. When you are working with a 3D model, a vertex is generally the lowest component to have a local space.

Now that we have an understanding of local spaces and how sub-objects can contain their local spaces, if we examine the space our local space is within, that would be our world space. In my example here, my room is our local space. It's world space would be...

#### World Space

[caption id="attachment_494" align="alignleft" width="300" caption="My Room in World Space"][/caption]![WorldSpace](../../assets/61fa637e15565bf0.jpg)


I've declared my world space as our world, similar to a level you will create for your game. As you can see, my room as it exists by itself has its own set of axes for determining the location of objects, but if you were to bring those objects into the world space, its axes are completely different. The door is no longer at origin, but is further along the Y axis an origin. My bed is no longer above my door, but instead is offset along the X axis. My chair is no longer below my desk, it is offset negatively in the X direction from my desk, or to the left of my desk.

When you are in your room though, you do not think of these things. When you are outside of your room, you generally treat your room as your room and you can't access the things inside of your room without being in your room. Even though you are no longer in your room, your stuff however will still be there in their correct position in their local space (unless someone decided to shuffle your things around!)

The point here is that when you are working within your level, if you were to move or rotate your player in world space, your player's arm will still be in the same local location as compared to his torso. If you are working in your level, you don't care about the rotation of your players arm, but only the player as a whole itself. When you are animating your player however, you do not care about the axes of the world, only the local space of your player and which way your arm is rotated in relation to your torso.

#### Why do we need to know the difference?

This knowledge between local and world space is important as there are times when you need to calculate the world space coordinates of something but still need it to remain in the same local position of your object.

With our third person camera, we know where the player is. We know its world space coordinates and its world space rotation. When we calculate our camera position though, we need it to always be in the same spot relative to the player. Because our camera is not a sub-object of our player, we have no idea about the player's local system. Two different objects are always unaware of each others local space, they are only aware of their world space and their own local spaces. Our camera has no idea that it should be shifted back and to the right of our players head because we don't know the exact location of the players head, but it knows it must be shifted back and to the right of our player and our level keeps track of our player in the level space. As our player exists within our level, the level is our players world space.

For our camera to always be behind the player, we have to define "behind the player". While we are in our room, the left of our room is the negative X axis. While in our world, the room's negative X is our positive Y. Unlike our room however, our player is able to rotate in world space, which means that the negative X axis of our player might be our positive Y at one moment, but might be exactly in-between positive Y and positive X at another moment if your player decides to face North-East.

There is a way to figure out the world axes we must use to remain local to our player, but in world space. We do this by finding the rotation needed to make our local space align with our world space. In my room example, the rotation needed to go from local to world space is a rotation of 90 degrees of our positive Z axis (and we calculated this by just looking at our picture.) This would align our room to our world. Knowing the amount we have to rotate means we can calculate our camera in local space and than rotate it into world space, also known as transforming from local to world space. Luckily for us, we don't need to know the math behind finding the needed rotation because Unreal gives us a few functions to do that for us. If you would like to learn how to calculate this on your own however, the book I recommended above is a great resource to have and will go much more in-depth about this process.

In summation: The difference in rotation of our local and world space is needed so that our calculations can be done in world space, but will remain local to our local space. I.e. we can calculate our camera in world space but still have it locked to an over-the-shoulder position about our player.

### Multiplying, Adding, and Subtracting Vectors

This is something you should really get familiar with and spend some time learning. A simple google search of "beginner vector math" should suffice.

#### What Is A Vector?

Vectors consist of 3 parts: X, Y and Z. In Unreal you will also see Vector2D which consists of 2 parts: X and Y. We can use vectors to store location or to store a displacement. Vectors that store location are simply vectors that represent the coordinate of something in space, with origin at (0,0,0). A displacement is not a point in space, but how to get to a point. Say if you wanted to get from point (2,0,1) to (6,2,-1) your displacement vector would be (4,2,-2). If you add this displacement vector with starting point (2,0,1) you will end up at (6,2,-1). Likewise, if you subtract our displacement vector from (6,2,-1) you will end up back at (2,0,1).

This will be a very rough and basic introduction to vectors, you should definitely learn some vector math on your own before you start implementing more complex systems.

#### Multiplying A Vector

If you have a vector and multiply it by something it will scale that vector. For instance, a 'normalized' vector that points down the Y axis only would be (0,1,0). A 'normalized' vector is any vector that has a length of 1. We will be multiplying a normalized vector in our implementation. A set of normalized vectors can represent a set of axes transformed into another coordinate space. In our implementation, we will be converting our player's local space to world space, and the Unreal function that does this for us gives us 3 normalized vectors for X, Y, and Z. They all have a length of 1. If we want to then say displace ourselves 50 units to the right of our character, we would do Y*50 to make our Y vector 50 units. If we wanted to go left, we would use a -50. This vector will then displace us 50 units to the right or left of our character, but the vector itself will be in world space.

(0,1,0) * 50 = (0,50,0). (.25, .75, .25) * 40 = (10, 30, 10).

#### Adding/Subtracting A Vector.

If you have a vector which could be a point or a displacement, you can add another vector to displace that point or displacement once more. By adding and subtracting vectors, you can combine displacement vectors to get a final location.

Say if you start at your place (0,0), walk North 5 blocks (Y axis) and then walk right 3 blocks (X axis), this can be described as:

(0,0) + (0,5) + (3,0) = (3,5). Your final location is at (3,5).

Now if you then decided to walk left 7 blocks, your final location would be:

(3,5) + (-7,0) = (-4, 5)

Notice how we added a negative displacement. This is because if we want to displace a vector by another, we always add as the vectors themselves have direction. However if you wanted to say "Walk the opposite of 7 blocks to the right" you would then do:

(3,5) - (7,0) = (-4,5)

For our third person camera, because it is easier for people to offset by positive numbers, these positive numbers result in positive displacement which means our displacement that we are calculating is actually forward and to the left instead of the perceived back and to the right. To compensate for this, we use vector subtraction for our final location instead of addition.

### The Code

So, lets get started writing our CalcCamera function. This function will override your current CalcCamera function and will work in both Pawn classes derived from GamePawn/UDKPawn and UTPawn. (However UTPawn already has a BehindView function set up for third person camera functionality.) The code listed here is a combination of the code posted by [iniside on the UDK Forums](http://forums.epicgames.com/showthread.php?t=709356&ref=allarsblog.com), CalcThirdPersonCamera in UTPawn.uc, and some various modifications made by me.

#### HTPawn.uc - Declaring Variables

[csharp]var vector CameraTranslateScale; //Used to Offset our Camera

var float CameraZOffset; //Used to Raise our Camera

var bool bThirdPerson; //Used to toggle our third person camera

simulated function bool CalcCamera(float fDeltaTime, out vector out_CamLoc, out rotator out_CamRot, out float out_FOV)

{

// Reference from [http://forums.epicgames.com/showthread.php?t=709356](http://forums.epicgames.com/showthread.php?t=709356&ref=allarsblog.com)

// And CalcThirdPersonCamera in UTPawn.uc

local vector CamStart, HitLocation, HitNormal, CamDir, X, Y, Z;

local vector tempCamStart, tempCamEnd;

local bool bObstructed;

local float CollisionRadius;

//....our code in development

}[/csharp]

These are the variables we will be using for our calculations and we'll be going over what they do and how they do it as we use them.

The first thing we should do in our camera calculation is we should break out of our function if we are not in third person view. If we are in first person, we have no need to manipulate the camera and should allow the engine to go ahead and do what it does without our interruption. Implementing is really simple:

[csharp] if (!bThirdPerson)

return false;[/csharp]

This is where we use one of our variables we've declared outside our function: bThirdPerson. bThirdPerson is a boolean that stores simply whether or not we are in third person view. We declared out outside of CalcCamera so that we can access it from other classes and also define it in our defaultproperties block in case we want to choose to make this our default camera style. By checking if the opposite of bThirdPerson is true, a.k.a. first person, a.k.a. !bThirdPerson, we will return false. If bThirdPerson is false, CalcCamera will return false as we are not in third person mode and therefore our calculations do not apply.

[csharp] bObstructed = false;

CollisionRadius = GetCollisionRadius();[/csharp]

These two lines will initialize some of the local variables we have declared for use in CalcCamera. bObstructed is a boolean which stores whether or not our camera view is being obstructed by an object. (i.e. our camera is inside a wall.) CollisionRadius is a float we've declared to cache the value of our collision radius retrieved by GetCollisionRadius();. This collision radius is the same radius we've defined in our CylinderComponent for our Pawn, mentioned above. With this value, we will be able to do calculations with an approximation of the size of our character, instead of spending more time to calculate the exact size. While we could also make a new variable that would store the size of the player for us, if we have multiple characters it would be a real chore to have to store these values independently.

[csharp] CamStart = Location;

CamStart.Z += CameraZOffset;[/csharp]

These next two lines begin setting us up for our calculations. CamStart is a local vector we've declared to store where the initial starting point of our camera is. As our third person camera is focused on our player, our player location is a good place to start. By assigning CamStart to Location (defined in Actor), our starting point will be that of the same position our player is at. The next line adjusts this starting point along the Z axis by the amount of our float variable we've declared in HTPawn, CameraZOffset. This allows us an easy method to tell our camera how many units up it should be placed above our character before we start calculating so that our final position will also be offset. This offset gives us the proper control we need to fine tune our camera location vertically to give us that exact altitude we need for our camera.

[csharp] GetAxes(out_CamRot, X, Y, Z);

X *= CollisionRadius * CameraTranslateScale.X;

Y *= CollisionRadius * CameraTranslateScale.Y;

Z *= CollisionRadius * -1.0f;

CamDir = X + Y + Z;

out_CamLoc = CamStart - CamDir;[/csharp]

This is the most important code block to understand in our calculations, and also the most complex. This is where knowledge of vector math will come in real handy. Lets break it down line by line:

GetAxes(out_CamRot, X, Y, Z);_ _GetAxes() is a function provided by Epic (Line 868 of Object.uc) that will automagically take a rotation and then convert that rotation into a set of vectors representing the world space axes that correspond to that rotation. out_CamRot already contains the rotation of the actor we are calculating our view through and in this case that is our player. GetAxes is taking this player rotation and breaking it down into these 3 axes which if we use for our translation, will always translate relative to our player. Its taking our players local space alignment and converting it into a set of world space axes, which we covered earlier at the beginning of this tutorial. With these world space axes, our calculations will end up in world space but still relative to our player.

With positive X representing our players forward direction, Y being our players right direction, and Z being our players Up direction, we can now begin to make a displacement vector for where we want our camera. We are multiplying X first by our CollisionRadius, which means we will displace forward the radius of our character so that we are no longer inside it. We then multiply this vector to scale it by our CameraTranslateScale.X, which is a vector we declared outside CalcCamera so that we can control how much we displace in the defaultproperties block. By assigning CameraTranslateScale.X a value of 6, we would be displacing our camera to be 6 times the radius of our player in the forward direction of our player. Our desired displacement is behind our player however, but on the last line of this code block we are subtracting our displacement vector which means the opposite of this displacement will result. This allows us to keep a positive value of 6 to pull our camera back, which is the preferred location of our camera. The next line is the same, but for left and right displacement. For this tutorial, CameraTranslateScale.Y is assigned a value of -2, so we are displacing twice our characters radius to the left. Once again, due to subtraction, this will result in the camera moving to the right. Lastly we flip the Z axis for the same subtraction reason, but we don't scale Z. We don't scale Z because our offset is already handled by CameraZOffset, and depending on our Pawn's location Z might not nessicarly be the Player's exact Up direction. Keeping Z constant will allow us to not have some weird Z translation in case our player is pitched at an angle, but instead will allow us to rely on CameraZOffset as offsetting our starting point will cause our X and Y vectors to be offset vertically as well.

CamDir = X + Y + Z combines all our vectors into our local vector CamDir which represents the direction of our camera displacement (or the opposite since we are subtracting). The vector math here is the same as the example with walking 5 blocks north and 3 blocks east, except we have to deal with Z as well.

The last line of this code block displaces our starting vector by the opposite amount of CamDir as we are subtracting. With CamDir being in front and to the left of our player due to that is how the local axes of our player are aligned, this will displace our camera back and to the right.

Phew. Quite a bit of math there, but we have finally displaced our camera. Now we need to make it aim in the direction of our player.

[csharp] if (Controller != None)

out_CamRot = Controller.Rotation;

else

out_CamRot = Rotation;[/csharp]

This code block assigns our camera rotation to match that of our Controller if we have one, otherwise we will match our Pawn's rotation itself. The reason we use a Controller's rotation instead of a Pawns if we have one is because when a player strafes left or right, or starts to bank due to terrain or some other force, this would be picked up by our camera and our camera would do all kinds of little jitters as the player physically does. This would be headache inducing, so we use the Controller's rotation as the Controller is generally where the player is aiming (which is almost identical to the player's true rotation, but without the jitter). The Controller also gets hit with different effects like recoil that will cause its aiming to change, and our camera should reflect that.

Now if you simply add return true; to the end of what we have, you would have a functional 3d camera. The only problem is your camera would be able to clip through walls as there are no checks against that.

#### Camera Collision Checking

Checking to see if our camera is obstructed by a wall or similar object is incredibly simple. Using a built-in Unreal function to see if there are any objects along a path, we can test for any objects between our player and our camera. This is where our friend Trace() comes in to play. (Defined on line 1710 of Actor.uc)

[csharp] if (Trace(HitLocation, HitNormal, out_CamLoc, CamStart, false, vect(12,12,12),,TRACEFLAG_Blocking) != None)

{

out_CamLoc = HitLocation;

bObstructed = true;

}[/csharp]

There are a lot of variables being tossed around here, mostly in the Trace function call itself. Trace takes a lot of arguments, the first two are HitLocation and HitNormal. This is the first time we are using these local vectors, but we are only using them as storage. The Trace function will assign these variables the location of where the trace line was obstructed, along with the normal of where it hit. We aren't using HitNormal, it is just there so we can call Trace. The next two variables are variables that we have calculated, being out_CamLoc and CamStart. The first of these two tells Trace where to end, while the second tells us were to start. Its a little confusing at first, but it is what it is. The Trace function will then draw a line from CamStart to out_CamLoc and if we hit anything, will put where we hit something at into HitLocation. The next variable is a boolean which dictates whether or not we should hit actors or not. In this case, we are only clipping with level geometry (BSP). If you need to have actor obstruction for your camera, change this to true. The next argument is a vector that dictates our "extent" of our trace. You can think of this the extent as the 'thickness' of our line. The next argument is optional and skipped here, but it takes a HitInfo struct which will hold lots of nifty information about what you hit if you hit something. The last argument is what we are tracing, or the type of our trace. If you search TRACEFLAG in the Actor class you will find the other modes we can use, but right now we are tracing for anything that's blocking us so we will use TRACEFLAG_Blocking.

Once this Trace is done, we check to see if it does not equal none. If this Trace function returns a value it means we hit something, so we will assign the location of our camera to the point of impact. This allows us to bring the camera in closer when we hit something, giving us a camera that respects clipping with minimal effort! The next line sets our bObstructed boolean to true, so we can check if our new camera position is inside our player. If our camera goes inside our player, we might see weird things like the inside of our characters face. Checking for this and toggling the visibility of our mesh will solve that issue.

#### Inner-Player Checking

This method was created by some unknown by the name of "fall", as this code was grabbed from [iniside on the UDK Forums](http://forums.epicgames.com/showthread.php?t=709356&ref=allarsblog.com).

[csharp] if (bObstructed)

{

/*Again thanks for fall, for this. It just inside character collision detection*/

/*I don't know who you are fall, but ^_^ */

tempCamStart = CamStart;

tempCamStart.Z = 0;

tempCamEnd = out_CamLoc;

tempCamEnd.Z = 0;

if((VSize(tempCamEnd - tempCamStart) < CollisionRadius*1.5) && (out_CamLoc.Z<Location.Z+CylinderComponent.CollisionHeight) && (out_CamLoc.Z>Location.Z-CylinderComponent.CollisionHeight))

HideMesh(true);

else

HideMesh(false);

}[/csharp]

The first thing we do is check to see if our camera was obstructed. There is no point in checking to see if our camera is in our player if we aren't obstructed.

Followed by some comments because its always nice to give credit where its due.

The next four lines assign tempCamStart and tempCamEnd to our camera's starting point and the camera's final displaced point, while zero'ing out the Z components. This will allow us to check if we are inside the player without performing another Trace, as Traces are expensive and slow to compute. You will see how in the next few lines...

We now have an if statement that if true means we are inside our player. This if statement has 3 expressions within that all have to be true. The first one is:

(VSize(tempCamEnd - tempCamStart) < CollisionRadius*1.5)

VSize is a provided function that will get the size or length of a vector and the vector we are getting the length of the displacement between CamStart and our final cam position but with the Z component zeroed out. As Z is no longer involved, this allows us to compare this displacement against the radius of our Player's collision radius. We multiply CollisionRadius by 1.5 so that if we are close to our player but not in it, we will still toggle its visibility because having your player character take up your entire screen is not fun. If our displacement length is less than this scaled collision radius, it means our displacement does not leave this radius and we are therefore in our player (in regards to X and Y only). As we stripped out our Z component, we now have to check for Z. The reason we stripped Z out of the first calculation as then we would be checking if our camera was less than our collision radius in all directions, making this a sphere check instead of a cylinder check. Our players or not spheres, however if ours is, you can make this simple by removing the second to expressions and use CamStart and out_CamLoc directly.

(out_CamLoc.Z<Location.Z+CylinderComponent.CollisionHeight)

This is checking to see if our final camera location is below our player's position + the height of our cylinder. As our CylinderComponent represents our players approximate size, we will be using its height as the player's height. If our camera is lower than our players height, that means we have a chance of being inside it.

(out_CamLoc.Z>Location.Z-CylinderComponent.CollisionHeight)

This does the same thing as the 2nd expression, except checks if we are above our current location minus our player's height. If both these expressions our true, that means our camera is somewhere in between our characters head and our characters feet. Combine this with our first check, if all expressions are true that means our camera is inside our player.

When its true, we call HideMesh(true) which is a function we have not written yet, but it will hide our mesh.

When it is false, which means we are not in our player, we call HideMesh(false). This will un-hide our mesh if it was previously hidden.

[csharp] return true;

}[/csharp]

We finally return true, telling the engine that our Pawn has calculated the camera and we will use our calculations. Yaaaaaaay!

#### Our Mesh Is Invisbile?

Be default, the skeletal mesh component is set to not render for the owner. In a first person game, you would never need to render your own player model as you would never see it, but now that we are a third person came we kind of have to see our character.

This is controlled by a boolean in the Pawn's skeletal mesh component named bOwnerNoSee

If you are deriving from GamePawn or UDKPawn, you should have something similar to:

[csharp]defaultproperties

{

//Lots of stuff here...

Begin Object Class=SkeletalMeshComponent Name=WPawnSkeletalMeshComponent

//Lots more stuff

bOwnerNoSee=false

//Lots more stuff

End Object

Mesh=WPawnSkeletalMeshComponent

Components.Add(WPawnSkeletalMeshComponent)

//Lots of more stuff

}[/csharp]

If you are deriving from a Pawn class that already declares a SkeletalMeshComponent...

[csharp]defaultproperties

{

//Possibly stuff here

Begin Object Name=WPawnSkeletalMeshComponent

//Possibly stuff here

bOwnerNoSee=false

//Possibly stuff here

End Object

//Possibly stuff here

}[/csharp]

#### HideMesh(bool Invisible)

While there are many ways of hiding a mesh, there are a lot fewer that will work for multiplayer games. Calling Mesh.SetHidden instead of our custom HideMesh function will work and will abolish the need for a HideMesh function, however this will hide your mesh towards other players too if you were on a multiplayer game. I do not want my players turning invisible when their camera clips.

[csharp]simulated function HideMesh(bool Invisible)

{

if ( LocalPlayer(PlayerController(Controller).Player) != None )

mesh.SetHidden(Invisible);

}[/csharp]

This is our function, really simple. We declare the function as simulated as it may run on the server but it will definitely have to be ran on the client for this client-side effect. Our conditional has some nested type casting, but what it is doing checking if we are a LocalPlayer as we only want to hide the mesh for the LocalPlayer and not other remote players. It does so by casting our current Controller to a PlayerController, then type casting PlayerController.Player into a LocalPlayer. If we end up with a result, that means our Pawn's PlayerController's Player is a LocalPlayer, which is us! Only then will we toggle the visibility of a mesh to ensure we don't disappear on other people's screens.

#### How Do We Switch Views?

If you want a permanent third person camera, this will be sufficient. All you have to do is assign bThirdPerson in defaultproperties to true, as there is no other way to change that variable. If you would however like to be able to switch between third and first, this is how we do it.

[csharp]exec function CycleCamera()

{

bThirdPerson = !bThirdPerson;

HideMesh(!bThirdPerson);

}[/csharp]

Declaring the function with the "exec" keyword allows us to call this function through a console command named CycleCamera. I used CycleCamera instead of UT's default BehindView as I may implement more camera modes later and I'd like to be able to cycle through them. The first line simply toggles bThirdPerson. We then call HideMesh with the opposite of bThirdPerson, which is the opposite of what it was originally. We could switch these two lines to avoid this double flip, but then the code would read weird in my opinion. If we are switching to our third person camera, bThirdPerson is going to be flipped to true. This will cause use to run HideMesh(false) as the flip of the flip(true) is false. If we are switching to first person, our flipped bThirdPerson would be false, therefore we will call HideMesh(true) as we don't need to see our mesh if we are in first person.

Now to switch views, all we do is use the console command CycleCamera. You can bind this command to a key or do whatever you want with it really.

#### If I Spawn In First Person View, I Still See Myself?

Yes, there is nothing telling our Pawn to update its visibility when it first spawns so lets fix that.

[csharp]simulated event BecomeViewTarget(PlayerController PC)

{

super.BecomeViewTarget(PC);

HideMesh(!bThirdPerson);

}[/csharp]

This BecomeViewTarget event is declared in the base Pawn class and is called every time our Pawn becomes a view target for a PlayerController. Every time we spawn, our Pawn becomes our ViewTarget. It only makes sense to use this event because its associated with viewing and that is what this entire tutorial has been about. The first line within we are calling BecomeViewTarget in our parent class, just so we don't accidentally get rid of some important functionality we don't know is going on. The next line simply updates our mesh visibility as usual.

### And there you have it, A working third person camera that will work in both base Pawn classes and UTPawn that works in multiplayer.

#### Complete Code Listing Of Code In This Tutorial

[csharp]var vector CameraTranslateScale;

var float CameraZOffset;

var bool bThirdPerson;

simulated event BecomeViewTarget(PlayerController PC)

{

super.BecomeViewTarget(PC);

HideMesh(!bThirdPerson);

}

exec function CycleCamera()

{

bThirdPerson = !bThirdPerson;

HideMesh(!bThirdPerson);

}

simulated function HideMesh(bool Invisible)

{

if ( LocalPlayer(PlayerController(Controller).Player) != None )

mesh.SetHidden(Invisible);

}

simulated function bool CalcCamera(float fDeltaTime, out vector out_CamLoc, out rotator out_CamRot, out float out_FOV)

{

// Reference from [http://forums.epicgames.com/showthread.php?t=709356](http://forums.epicgames.com/showthread.php?t=709356&ref=allarsblog.com)

// And CalcThirdPersonCamera in UTPawn.uc

local vector CamStart, HitLocation, HitNormal, CamDir, X, Y, Z;

local vector tempCamStart, tempCamEnd;

local bool bObstructed;

local float CollisionRadius;

if (!bThirdPerson)

return false;

bObstructed = false;

CollisionRadius = GetCollisionRadius();

CamStart = Location;

CamStart.Z += CameraZOffset;

GetAxes(out_CamRot, X, Y, Z);

X *= CollisionRadius * CameraTranslateScale.X;

Y *= CollisionRadius * CameraTranslateScale.Y;

Z *= CollisionRadius * -1.0f;

CamDir = X + Y + Z;

out_CamLoc = CamStart - CamDir;

if (Controller != None)

out_CamRot = Controller.Rotation;

else

out_CamRot = Rotation;

if (Trace(HitLocation, HitNormal, out_CamLoc, CamStart, false, vect(12,12,12),,TRACEFLAG_Blocking) != None)

{

out_CamLoc = HitLocation;

bObstructed = true;

}

if (bObstructed)

{

/*Again thanks for fall, for this. It just inside character collision detection*/

/*I don't know who you are fall, but ^_^ */

tempCamStart = CamStart;

tempCamStart.Z = 0;

tempCamEnd = out_CamLoc;

tempCamEnd.Z = 0;

if((VSize(tempCamEnd - tempCamStart) < CollisionRadius*1.5) && (out_CamLoc.Z<Location.Z+CylinderComponent.CollisionHeight) && (out_CamLoc.Z>Location.Z-CylinderComponent.CollisionHeight))

HideMesh(true);

else

HideMesh(false);

}

return true;

}[/csharp]

[csharp]defaultproperties

{

//Lots of stuff here...

```
CameraZOffset=48
CameraTranslateScale=(X=5,Y=-2,Z=1)
Begin Object Name=CollisionCylinder
CollisionRadius=+0036.000000
CollisionHeight=+0096.000000
End Object
//More stuff here...
```


}[/csharp]

## Video Version

Subject: Creating A Third-Person Camera Skill Level: Intermediate Run-Time: 1 Hour and 20 minutes Author: [Michael Allar](https://allarsblog.com/) Notes: I really really really butchered the explanation of the vector math in the video, which is why I moved the written version above the video for this tutorial.