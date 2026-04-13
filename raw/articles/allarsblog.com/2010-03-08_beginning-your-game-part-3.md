---
title: Beginning Your Game Part 3
url: https://allarsblog.com/2010/03/08/beginning-your-game-part-3/
author: Michael Allar
published: '2010-03-08'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

# IMPORTANT

This tutorial was created with the March build of UDK, as opposed to the February build.

This is a big -MY BAD- on my part.

The rest of the tutorials flow nicely after this. I promise.

Here is what you do:

You download the March build.

You install it.

You set up the config files just like you have been doing in Part 1 and Part 2.

Open UTGameConfigDefaultGame.ini

Replace the Engine.GameInfo block with the following:

[csharp][Engine.GameInfo]

DefaultGame=UDKGame.UDKGame

DefaultServerGame=UDKGame.UDKGame

PlayerControllerClassName=UDKGame.HTPlayerController

GameDifficulty=+1.0

MaxPlayers=32

DefaultMapPrefixes=(Prefix="HT",GameType="UDKGame.TheHuntGame")[/csharp]

What we did there was move the DefaultMapPrefixes from DefaultProperties to this .ini file, as thats where the March build put it. You will learn how to do stuff like this later on as well.

When you compile, you will get a warning about HTInventoryManager. This will fix itself when you complete step 4.

Then continue to Step 4.

Also, skip Migrating From Feb. To March. since you are now using the March build. <_<

**Sorry. These were my first tutorials I've made and I was bound to mess up somewhere. All the future tutorials after this will go smoothly. I will try to redo these first three later when I have some spare time.**

## Video Version

Subject: Beginning Your Game Part 3

Skill Level: Beginner

Run-Time: 16 Minutes

Author: Michael Allar

Notes: The project I'm working on as I'm creating this documentation requires the classes we've made to be based off higher level classes. These were the changes made.

## Written Version

Subject: Beginning Your Game Part 3

Skill Level: Beginner

Author: Michael Allar

Notes: The project I'm working on as I'm creating this documentation requires the classes we've made to be based off higher level classes. These were the changes made.

In order to make these changes, you must be using the February build or later of UDK.

#### Why Is There A Part 3?

I am the Lead Programmer for a student ran project at The Art Institute of Orange County called The Hunt. It is a standalone game using Unreal Engine 3 being developed with the Unreal Development Kit. I am creating these tutorials as I progress in development of The Hunt and we've recently had a need to base our code off of higher level classes within the engine. Our goal is to stay away from as much UT code as possible without rewriting too much of everything. Instead of extending UTGame, UTPlayerController, and UTPawn, we will be extending GameInfo, UDKPlayerController, and UDKPawn.

### UDKGame now extends GameInfo

```
/*******************************************************************************
UDKGame
Creation date: 14/01/2010 13:55
Copyright (c) 2010, Michael Allar, Epic
*******************************************************************************/
class UDKGame extends GameInfo
config(UDKGame);
struct GameTypePrefix
{
var string Prefix;
var string GameType;
};
var array<GameTypePrefix> DefaultMapPrefixes;
static event class<GameInfo> SetGameType(string MapName, string Options, string Portal)
{
local string ThisMapPrefix;
local int i,pos;
local class<GameInfo> NewGameType;
if (Left(MapName, 10) ~= "HTFrontEnd")
{
return class'UDKGame';
}
// strip the UEDPIE_ from the filename, if it exists (meaning this is a Play in Editor game)
if (Left(MapName, 6) ~= "UEDPIE")
{
MapName = Right(MapName, Len(MapName) - 6);
}
else if ( Left(MapName, 5) ~= "UEDPC" )
{
MapName = Right(MapName, Len(MapName) - 5);
}
else if (Left(MapName, 6) ~= "UEDPS3")
{
MapName = Right(MapName, Len(MapName) - 6);
}
else if (Left(MapName, 6) ~= "UED360")
{
MapName = Right(MapName, Len(MapName) - 6);
}
// replace self with appropriate gametype if no game specified
pos = InStr(MapName,"-");
ThisMapPrefix = left(MapName,pos);
// change game type
for ( i=0; i<Default.DefaultMapPrefixes.Length; i++ )
{
if ( Default.DefaultMapPrefixes[i].Prefix ~= ThisMapPrefix )
{
NewGameType = class<GameInfo>(DynamicLoadObject(Default.DefaultMapPrefixes[i].GameType,class'Class'));
if ( NewGameType != None )
{
return NewGameType;
}
}
}
return class'UDKGame';
}
defaultproperties
{
DefaultPawnClass=class'UDKGame.HTPawn'
PlayerControllerClass=class'UDKGame.HTPlayerController'
DefaultMapPrefixes(0)=("HT&",GameType="UDKGame.TheHuntGame")
}
```


```
if (Left(MapName, 10) ~= "HTFrontEnd")
{
return class'UDKGame';
}[/csharp]
```


### HTPawn now extends UDKPawn

HTPawn now has a defaultproperties block identical to UTPawn, with the UTPawn specific properties removed. [It is really long so here is a link to the script instead.](http://allarsblog.com/unreal/HTPawn.zip)

### HTPlayerController now extends UDKPlayerController

[csharp]/*******************************************************************************

HTPlayerController

Creation date: 14/01/2010 14:31

Copyright (c) 2010, Michael Allar

*******************************************************************************/

class HTPlayerController extends UDKPlayerController

config(UDKGame);[/csharp]

### TheHuntGame is a second GameInfo class that extends UDKGame

So that we can use UDKGame as a generic GameInfo class for things like front-ends while having the majority of our game code in a subclass of it.

[csharp]/*******************************************************************************

TheHuntGame

```
Creation date: 19/01/2010 22:24
Copyright (c) 2010, Michael Allar
```


*******************************************************************************/

class TheHuntGame extends UDKGame;

var array< class<Inventory> > DefaultInventory;

event PlayerController Login(string Portal, string Options, const UniqueNetID UniqueID, out string ErrorMessage)

{

local PlayerController PC;

PC = super.Login(Portal, Options, UniqueID, ErrorMessage);

ChangeName(PC, "New Player", true);

return PC;

}

function AddDefaultInventory( pawn PlayerPawn )

{

local int i;

```
for (i=0; i<DefaultInventory.Length; i++)
{
// Ensure we don't give duplicate items
if (PlayerPawn.FindInventoryType( DefaultInventory[i] ) == None)
{
// Only activate the first weapon
PlayerPawn.CreateInventory(DefaultInventory[i], (i > 0));
}
}
PlayerPawn.AddDefaultInventory();
```


}

defaultproperties

{

DefaultPawnClass=class'UDKGame.HTPawn'

PlayerControllerClass=class'UDKGame.HTPlayerController'

```
ConsolePlayerControllerClass=class'UTGame.UTConsolePlayerController'
PlayerReplicationInfoClass=class'UTGame.UTPlayerReplicationInfo'
GameReplicationInfoClass=class'UTGame.UTGameReplicationInfo'
//DefaultInventory(0)=class'UDKGame.HTWP_LittleBang'
bRestartLevel=False
bDelayedStart=False
bUseSeamlessTravel=true
```


}

[/csharp]

### Thats all the changes made.

Now you are ready to continue to set up your game!