---
title: 'HTWeapon: Part 5 - Dealing Damage'
url: https://allarsblog.com/2010/03/27/htweapon-part-4-dealing-damage/
author: Michael Allar
published: '2010-03-27'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

## Video Version

Subject: HTWeapon: Part 5 - Dealing Damage

Skill Level: So easy a caveman can do it.

Run-Time: 5 minutes

Author: [Michael Allar](https://allarsblog.com/)

Notes: How to make your weapon deal damage upon firing.

## Written Version

Subject: HTWeapon: Part 5 - Dealing Damage

Skill Level: So easy a caveman can do it.

Author: [Michael Allar](http://allarsblog.com/)

Notes: How to make your weapon deal damage upon firing.

[csharp]defaultproperties

{

// Weapon SkeletalMesh

Begin Object Name=FirstPersonMesh

SkeletalMesh=SkeletalMesh'ALWP_M16.Mesh.SK_WP_M16_1P'

AnimSets(0)=AnimSet'ALWP_M16.Anims.K_WP_M16_1P'

Scale=1.0

FOV=60.0

End Object

// Pickup staticmesh

Begin Object name=PickupMesh

SkeletalMesh=SkeletalMesh'ALWP_M16.Mesh.SK_WP_M16_3P'

End Object

PlayerViewOffset=(X=17,Y=10.0,Z=-8.0)

//This is what we have added here.

AmmoCount=9001

MaxAmmoCount=9001

InstantHitDamage(0)=25.0

InstantHitDamage(1)=500000.0

InstantHitMomentum(0)=1000.0

InstantHitMomentum(1)=1000000.0

}[/csharp]