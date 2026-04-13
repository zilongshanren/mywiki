---
title: Fixing The Loading Movie For Multiplayer Clients
url: https://allarsblog.com/2010/03/26/fixing-the-loading-movie-for-multiplayer-clients/
author: Michael Allar
published: '2010-03-26'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

## Video Version

Subject: Fixing The Loading Movie For Multiplayer Clients

Skill Level: Beginner

Run-Time: 21 minutes

Author: [Michael Allar](https://allarsblog.com/)

Notes: When you host a mutliplayer game with the current code, clients will join but they will get stuck at a loading screen endlessly. This fixes that. Also introduces GameReplicationInfo.

## Written Version

Subject: HTWeapon: Part 3 – Creating a Dynamic Muzzle Flash Light

Skill Level: Beginner

Author: [Michael Allar](http://allarsblog.com/)

Notes: When you host a mutliplayer game with the current code, clients will join but they will get stuck at a loading screen endlessly. This fixes that. Also introduces GameReplicationInfo.

### HTPlayerController

[csharp]/*******************************************************************************

HTPlayerController

Creation date: 14/01/2010 14:31

Copyright (c) 2010, Michael Allar

*******************************************************************************/

class HTPlayerController extends UDKPlayerController

config(UDKGame);

event InitInputSystem()

{

Super.InitInputSystem();

if (WorldInfo.NetMode != NM_DedicatedServer)

{

CharacterProcessingComplete();

}

}

/** called when the GRI finishes processing custom character meshes */

function CharacterProcessingComplete()

{

local string LastMovie;

LastMovie = class'Engine'.Static.GetLastMovieName();

if(InStr(LastMovie, "UT_loadmovie") != -1)

{

// stop the loading movie that was up during precaching

class'Engine'.static.StopMovie(true);

}

}

defaultproperties

{

}[/csharp]

### HTGameReplicationInfo

[csharp]/*******************************************************************************

HTGameReplicationInfo

Creation date: 26/03/2010 00:22

Copyright (c) 2010, Allar

*******************************************************************************/

class HTGameReplicationInfo extends GameReplicationInfo;

simulated function PostBeginPlay()

{

Super.PostBeginPlay();

if (WorldInfo.NetMode != NM_DedicatedServer)

{

SetTimer(1.0, false, 'CharacterProcessingComplete');

}

}

//Signal that all player controllers character processing is complete

simulated function CharacterProcessingComplete()

{

local HTPlayerController HTPC;

foreach LocalPlayerControllers(class'HTPlayerController', HTPC)

{

HTPC.CharacterProcessingComplete();

}

}[/csharp]

### UDKGame/TheHuntGame

[csharp]defaultproperties

{

//Some stuff

GameReplicationInfoClass=class'UDKGame.HTGameReplicationInfo'

//More stuff

}[/csharp]