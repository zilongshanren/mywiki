---
title: Fixing Character Lighting
url: https://allarsblog.com/2010/04/01/fixing-character-lighting/
author: Michael Allar
published: '2010-04-01'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

## Video Version

Subject: Fixing Character Lighting

Skill Level: Beginner

Run-Time: 5 Minutes

Author: [Michael Allar](http://backup.allarsblog.com/?ref=allarsblog.com)

Notes: If your character is pitch black no matter what you do, this is the fix.

## Written Version

Subject: Fixing Character Lighting

Skill Level: Beginner

Author: [Michael Allar](http://allarsblog.com/)

Notes: If your character is pitch black no matter what you do, this is the fix.

### HTPawn

The problem here is with our Pawn class. Essentially, our skeletal mesh needs to know that we are in a light environment.

Make sure this variable is declared at the top of your Pawn class:

[csharp]/** The pawn's light environment */

var DynamicLightEnvironmentComponent LightEnvironment;[/csharp]

In defaultproperties (replace if you see you have something similar but not exact):

[csharp]DefaultProperties

{

//Some stuff

Begin Object Name=MyLightEnvironment

bSynthesizeSHLight=TRUE

bIsCharacterLightEnvironment=TRUE

End Object

Components.Add(MyLightEnvironment)

LightEnvironment=MyLightEnvironment

//More stuff

}[/csharp]

Within the same defaultproperties block, you must assign your mesh to this environment.

[csharp]Begin Object Name=WPawnSkeletalMeshComponent

//Stuff

LightEnvironment=MyLightEnvironment

//More Stuff

End Object

Mesh=WPawnSkeletalMeshComponent

Components.Add(WPawnSkeletalMeshComponent)[/csharp]

You're done!