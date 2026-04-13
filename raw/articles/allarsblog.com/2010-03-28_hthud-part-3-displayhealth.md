---
title: 'HTHUD: Part 3 - DisplayHealth()'
url: https://allarsblog.com/2010/03/28/hthud-part-3-displayhealth/
author: Michael Allar
published: '2010-03-28'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

## Video Version

Subject: HTHUD: Part 3 - DisplayHealth()

Skill Level: Beginner

Run-Time: 22 Minutes

Author: [Michael Allar](http://backup.allarsblog.com/?ref=allarsblog.com)

Notes: Displaying our current health to the screen.

## Written Version

Subject: HTHUD: Part 3 - DisplayHealth()

Skill Level: Beginner

Author: [Michael Allar](http://allarsblog.com/)

Notes: Displaying our current health to the screen.

### HTHUD - Variables

For this tutorial, we will be introducing four new variables for our HTHUD class.

[csharp]var bool bShowHealth;

var vector2d HealthPosition, HealthTextOffset;

var TextureCoordinates HealthBGCoords;[/csharp]

_bShowHealth _will toggle the showing of our Health. *HealthPosition*, *HealthTextOffset*, and *HealthBGCoords* function just like their ammo counter-parts what we have made in the previous tutorials.

### HTHUD - DisplayHealth()

You will find that our DisplayHealth method is almost identical to our DisplayAmmo function.

The first thing we need to do is declare some local variables for us to use during the calculation stages of our ammo drawing.

[csharp]local vector2d POS, HealthTextOffsetPOS;

local string Amount;

local int HealthCount;[/csharp]

These work just as their Ammo counter-parts in DisplayAmmo do. However notice we do not have TX or TY, as I removed as I do not plan to ever right-align my health display text.

[csharp]// Resolve the position

POS = ResolveHudPosition(HealthPosition,HealthBGCoords.UL,HealthBGCoords.VL);

HealthCount = PawnOwner.Health;

// Draw the Health Image Widget

Canvas.SetPos(POS.X,POS.Y);// - (HealthBarOffsetY * ResolutionScale));

Canvas.DrawColorizedTile(HudTexture, HealthBGCoords.UL * ResolutionScale, HealthBGCoords.VL * ResolutionScale, HealthBGCoords.U, HealthBGCoords.V, HealthBGCoords.UL, HealthBGCoords.VL, HudTint);

// Draw the amount

Amount = ""$HealthCount;

Canvas.DrawColor = WhiteColor;

HealthTextOffsetPOS = ResolveHUDOffset(POS, HealthTextOffset);

Canvas.SetPos(HealthTextOffsetPOS.X,HealthTextOffsetPOS.Y);

Canvas.DrawText(Amount,,HUDFontScale.X * ResolutionScale,HUDFontScale.Y * ResolutionScale);[/csharp]

Once again, you will see that its exactly the same code as DisplayAmmo, but with a few less lines. The lines removed are ones that calculate TX and TY, as we will not be right-aligning the health text and therefore it is a waste of time to calculate them. If you require right aligned health text, go ahead and copy the DisplayAmmo function exactly, using our Health variables instead of our Ammo variables.

We do however do something new, and that is assign HealthCount (previously AmmoCount) to PawnOwner.Health. PawnOwner is the pawn that owns this instance of the HUD (our player), and Health is a variable that is declared and managed in the base Pawn class. We can grab our current health by just pulling from the data in the Health variable. We then draw it just like we've drawn the ammo text.

### HTHUD: DrawLivingHUD()

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

```
if ( bShowHealth )
{
DisplayHealth();
}
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
```


}[/csharp]

What we have done here is add a check to see if we should show our health, and then display it if we do. Notice how this is inside the PawnOwner check but not in the Weapon check. This is so we always display our Pawn's health if we have a Pawn and it doesn't rely on us having a weapon to show our health.

### HTHUD: DefaultProperties

Now we get to define our four new variables and put them to use!

[csharp]defaultproperties

{

//...

HealthPosition=(X=0,Y=-1) //Position of our Health sprite. Set here to our bottom left corner.

HealthTextOffset=(X=80,Y=0) //Offsets text 80 pixels right from the Health sprite.

HealthBGCoords=(U=131,UL=80,V=0,VL=80) //Pixel coordinates of our Health Sprite in our HUDTexture

bShowHealth=true //Let us display Health on our HUD.

// ...

}

[/csharp]

### Result:

[caption id="attachment_472" align="alignnone" width="300" caption="Our Health Hud Display In Action"][/caption]![HealthHudResult](../../assets/e37b9f14c4732755.jpg)


** **** ******Download Project Source Code Here****