---
title: 'HTWeapon: Part 2 – DrawWeaponCrosshair()'
url: https://allarsblog.com/2010/03/19/htweapon-part-2-drawweaponcrosshair/
author: Michael Allar
published: '2010-03-19'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

**Important: I didn't notice this until after I posted this but my stuttering is pretty bad in this video. Just a heads up. I will re-do this in the future.**

## Video Version

Subject: HTWeapon: Part 2 – DrawWeaponCrosshair()

Skill Level: Beginner

Run-Time: 30 minutes

Author: [Michael Allar](https://allarsblog.com/)

Notes: Going over how to have our weapons handle the drawing of our crosshair.

## Written Version

Subject: HTWeapon: Part 2 – DrawWeaponCrosshair()

Skill Level: Beginner

Author: [Michael Allar](http://allarsblog.com/)

Notes: Going over how to have our weapons handle the drawing of our crosshair.

Sorry about the indentation, it seems like my indentation will not survive copy paste… I will go back and fix the indentation later.

### HTWeapon

The variables we added to HTWeapon

[csharp]/** HUD Stuff */

var Texture CrosshairImage;

var UIRoot.TextureCoordinates CrosshairCoordinates;[/csharp]

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

}[/csharp]

### HTHUD

We've added a boolean bShowCrosshair to our declared variables.

[csharp]var bool bShowAmmo, bShowCrosshair;[/csharp]

Also reworked our DrawLivingHUD so that its a bit more streamlined and logic flows better. Also implements bShowCrosshair along with calling our DrawWeaponCrosshair() function.

[csharp]/**

- Anything drawn in this function will be displayed ONLY when the player is living.

*/

function DrawLivingHud()

{

local HTWeapon Weapon;

// Manage the weapon. NOTE: Vehicle weapons are managed by the vehicle

// since they are integrated in to the vehicle health bar

if( PawnOwner != none )

{

Weapon = HTWeapon(PawnOwner.Weapon);

if ( Weapon != none )

{

if ( bShowAmmo )

{

DisplayAmmo(Weapon);

}

if (bShowCrosshair)

{

Weapon.DrawWeaponCrosshair(self);

}

}

}

}[/csharp]