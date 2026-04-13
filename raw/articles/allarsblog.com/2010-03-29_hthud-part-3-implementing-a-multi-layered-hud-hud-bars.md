---
title: 'HTHUD: Part 3 - Implementing a Multi-Layered HUD + HUD Bars'
url: https://allarsblog.com/2010/03/29/hthud-part-3-implementing-a-multi-layered-hud-hud-bars/
author: Michael Allar
published: '2010-03-29'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

## Video Version

Subject: HTHUD: Part 3 - Implementing a Multi-Layered HUD + HUD Bars

Skill Level: Beginner

Run-Time: 1 Hour

Author: [Michael Allar](https://allarsblog.com/)

Notes: Drawing our different HUD passes so that they stack on top of each other, along with making our health and ammo bars fill up or deplete based on current health and ammo.

## Written Version

Feel like doing some writing? Want to get noticed? Write me up a version of this video for me.

[csharp]/*******************************************************************************

HTHUD

Creation date: 09/03/2010 05:04

Copyright (c) 2010, Allar

*******************************************************************************/

class HTHUD extends UDKHUD

config(UI);

/** The Pawn that is currently owning this hud */

var Pawn PawnOwner;

/** Points to the HT Pawn. Will be resolved if in a vehicle */

var HTPawn HTPawnOwner;

/** Cached reference to the another hud texture */

var const Texture2D HudTexture;

var linearcolor HudTint;

/******************************************************************************

* Common Colors - These are defined in DefaultUI.ini

******************************************************************************/

//var config color WhiteColor, RedColor, GreenColor; //Declared in HUD as const

var config color BlueColor, GrayColor, BlackColor;

var config color CrosshairColor, CrosshairShadowColor;

var bool bDrawColorPalette;

/******************************************************************************

* HUD Stuff

******************************************************************************/

var bool bShowAmmo, bShowHealth, bShowVitals, bShowCrosshair;

var vector2d AmmoPosition, AmmoTextOffset, HealthPosition, HealthTextOffset;

var TextureCoordinates AmmoBGCoords, HealthBGCoords;

var vector2d HUDVitalsPosition;

var TextureCoordinates HUDVitalsCoords;

var int HUDVitalsBarsZero;

var int HUDVitalsBarsFull;

/** Scales the FontSize for all our HUD DrawText Calls */
var vector2d HUDFontScale;
/** Resolution dependent HUD scaling factor

*/*

var float HUDScaleX, HUDScaleY;

/* Holds the scaling factor given the current resolution. This is calculated in PostRender() */

var float HUDScaleX, HUDScaleY;

/

var float ResolutionScale, ResolutionScaleX;

/** The percentage of the view that should be considered safe */
var float SafeRegionPct;
/** Holds the full width and height of the viewport */

var float FullWidth, FullHeight;

/**

- Perform any value precaching, and set up various safe regions
- NOTE: NO DRAWING should ever occur in PostRender. Put all drawing code in DrawHud().

*/

event PostRender()

{

PawnOwner = Pawn(PlayerOwner.ViewTarget);

if ( PawnOwner == None )

{

PawnOwner = PlayerOwner.Pawn;

}

HTPawnOwner = HTPawn(PawnOwner);

// draw any debug text in real-time

PlayerOwner.DrawDebugTextList(Canvas,RenderDelta);

HUDScaleX = Canvas.ClipX/1280;

HUDScaleY = Canvas.ClipX/1280;

ResolutionScaleX = Canvas.ClipX/1024;

ResolutionScale = Canvas.ClipY/768;

FullWidth = Canvas.ClipX;

FullHeight = Canvas.ClipY;

if ( bShowHud )

{

DrawHud();

}

// let iphone draw any always present overlays

DrawInputOverlays();

}

/**

- This is the main drawing pump. It will determine which hud we need to draw (Game or PostGame). Any drawing that should occur
- regardless of the game state should go here.

*/

function DrawHUD()

{

local float x,y,w,h;

// Create the safe region

w = FullWidth * SafeRegionPct;

X = Canvas.OrgX + (Canvas.ClipX - w) * 0.5;

// We have some extra logic for figuring out how things should be displayed

// in split screen.

h = FullHeight * SafeRegionPct;

Y = Canvas.OrgY + (Canvas.ClipY - h) * 0.5;

Canvas.OrgX = X;

Canvas.OrgY = Y;

Canvas.ClipX = w;

Canvas.ClipY = h;

Canvas.Reset(true);

// Set up delta time

RenderDelta = WorldInfo.TimeSeconds - LastHUDRenderTime;

LastHUDRenderTime = WorldInfo.TimeSeconds;

PlayerOwner.DrawHud( Self );

if (bShowGameHUD)

{

DrawGameHud();

}

if (bDrawColorPalette)

DrawColorPalette();

}

function DrawColorPalette()

{

Canvas.SetPos(0,0);

Canvas.DrawColorizedTile(HudTexture, 40 * ResolutionScale, 40 *ResolutionScale,0,130,40,40, ColorToLinearColor(WhiteColor));

Canvas.SetPos(40,0);

Canvas.DrawColorizedTile(HudTexture, 40 * ResolutionScale, 40 *ResolutionScale,0,130,40,40, ColorToLinearColor(RedColor));

Canvas.SetPos(80,0);

Canvas.DrawColorizedTile(HudTexture, 40 * ResolutionScale, 40 *ResolutionScale,0,130,40,40, ColorToLinearColor(GreenColor));

// We don't need a texture if we use Canvas' DrawRect function.

Canvas.SetPos(120,0);

Canvas.DrawColor = BlueColor; //Sets color for Canvas' primitive drawing functions

Canvas.DrawRect(40,40); //Width and Height of Rect

//Note that DrawRect can take a 3rd argument, a Texture to draw with.

Canvas.SetPos(160,0);

Canvas.DrawColorizedTile(HudTexture, 40 * ResolutionScale, 40 *ResolutionScale,0,130,40,40, ColorToLinearColor(GrayColor));

Canvas.SetPos(200,0);

Canvas.DrawColorizedTile(HudTexture, 40 * ResolutionScale, 40 *ResolutionScale,0,130,40,40, ColorToLinearColor(BlackColor));

}

function DrawGameHud()

{

DisplayLocalMessages();

DisplayConsoleMessages();

DrawLivingHud();

}

/**

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

if ( bShowHealth )

{

DisplayHealth();

}

if ( bShowVitals )

{

DisplayVitals(Weapon);

}

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

}

function DisplayVitals(HTWeapon Weapon)

{

local vector2d POS;

local float ResolvedWidth, ResolvedHeight;

local float HealthCount, AmmoCount;

local float HealthBarWidth, AmmoBarWidth;

HealthCount = PawnOwner.Health;

HealthBarWidth = (HUDVitalsBarsFull - HUDVitalsBarsZero) * (HealthCount/100.0f);

ResolvedWidth = HUDVitalsCoords.UL * ResolutionScale;

ResolvedHeight = HUDVitalsCoords.VL * ResolutionScale;

// Resolve the position

POS = ResolveHudPosition(HUDVitalsPosition,HUDVitalsCoords.UL,HUDVitalsCoords.VL);

// Draw the Vitals Pass 1

Canvas.SetPos(POS.X,POS.Y);

Canvas.DrawColorizedTile(HudTexture, ResolvedWidth, ResolvedHeight, HUDVitalsCoords.U, HUDVitalsCoords.V, HUDVitalsCoords.UL, HUDVitalsCoords.VL, HudTint);

//Draw the Vitals Pass 2 - Health Bar

Canvas.SetPos(POS.X + (HUDVitalsBarsZero * ResolutionScale),POS.Y);

Canvas.DrawColorizedTile(HudTexture, HealthBarWidth * ResolutionScale, ResolvedHeight, HUDVitalsCoords.U + HUDVitalsBarsZero, HUDVitalsCoords.V + HUDVitalsCoords.VL, HealthBarWidth, HUDVitalsCoords.VL, HudTint);

//Draw the Vitals Pass 3

Canvas.SetPos(POS.X,POS.Y);

Canvas.DrawColorizedTile(HudTexture, ResolvedWidth, ResolvedHeight, HUDVitalsCoords.U, HUDVitalsCoords.V + HUDVitalsCoords.VL * 2, HUDVitalsCoords.UL, HUDVitalsCoords.VL, HudTint);

if (Weapon != None)

{

AmmoCount = Weapon.GetAmmoCount();

AmmoBarWidth = (HUDVitalsBarsFull - HUDVitalsBarsZero) * (AmmoCount/Weapon.MaxAmmoCount);

//Draw the Vitals Pass 4 - Ammo Bar

Canvas.SetPos(POS.X + (HUDVitalsBarsZero * ResolutionScale),POS.Y);

Canvas.DrawColorizedTile(HudTexture, AmmoBarWidth * ResolutionScale, ResolvedHeight, HUDVitalsCoords.U + HUDVitalsBarsZero, HUDVitalsCoords.V + HUDVitalsCoords.VL * 3, AmmoBarWidth, HUDVitalsCoords.VL, HudTint);

}

//Draw the Vitals Pass 5

Canvas.SetPos(POS.X,POS.Y);

Canvas.DrawColorizedTile(HudTexture, ResolvedWidth, ResolvedHeight, HUDVitalsCoords.U, HUDVitalsCoords.V + HUDVitalsCoords.VL * 4, HUDVitalsCoords.UL, HUDVitalsCoords.VL, HudTint);

}

function DisplayHealth()

{

local vector2d POS, HealthTextOffsetPOS;

local string Amount;

local int HealthCount;

// Resolve the position

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

Canvas.DrawText(Amount,,HUDFontScale.X * ResolutionScale,HUDFontScale.Y * ResolutionScale);

}

function DisplayAmmo(HTWeapon Weapon)

{

local vector2d POS, AmmoTextOffsetPOS;

local string Amount;

local int AmmoCount;

local float TX, TY;

// Resolve the position

POS = ResolveHudPosition(AmmoPosition,AmmoBGCoords.UL,AmmoBGCoords.VL);

AmmoCount = Weapon.GetAmmoCount();

// Draw the Ammo Image Widget

Canvas.SetPos(POS.X,POS.Y);// - (AmmoBarOffsetY * ResolutionScale));

Canvas.DrawColorizedTile(HudTexture, AmmoBGCoords.UL * ResolutionScale, AmmoBGCoords.VL * ResolutionScale, AmmoBGCoords.U, AmmoBGCoords.V, AmmoBGCoords.UL, AmmoBGCoords.VL, HudTint);

// Draw the amount

Amount = ""$AmmoCount;

Canvas.DrawColor = WhiteColor;

Canvas.TextSize(Amount, TX, TY);

TX *= HUDFontScale.X; TY *= HUDFontScale.Y;

AmmoTextOffsetPOS = ResolveHUDOffset(POS, AmmoTextOffset, TX, TY);

Canvas.SetPos(AmmoTextOffsetPOS.X,AmmoTextOffsetPOS.Y);

Canvas.DrawText(Amount,,HUDFontScale.X * ResolutionScale,HUDFontScale.Y * ResolutionScale);

}

/**

- Given a default screen position (at 1024x768) this will return the hud position at the current resolution.
- NOTE: If the default position value is < 0.0f then it will attempt to place the right/bottom face of
- the "widget" at that offset from the ClipX/Y.
- @Param Position The default position (in 1024x768 space)
- @Param Width How wide is this "widget" at 1024x768
- @Param Height How tall is this "widget" at 1024x768
- @returns the hud position

*/

function Vector2D ResolveHUDPosition(vector2D Position, float Width, float Height)

{

local vector2D FinalPos;

FinalPos.X = (Position.X < 0) ? Canvas.ClipX - (Position.X * ResolutionScale) - (Width * ResolutionScale) : Position.X * ResolutionScale;

FinalPos.Y = (Position.Y < 0) ? Canvas.ClipY - (Position.Y * ResolutionScale) - (Height * ResolutionScale) : Position.Y * ResolutionScale;

return FinalPos;

}

/** Offsets an already resolved HUD position and will attempt to place the right/bottom face of the "widget"

* at the coordinates if offset is < 0.0f and width or height is supplied.

*/

function Vector2D ResolveHUDOffset(vector2D HUDPosition, vector2D Offset, optional float Width, optional float Height)

{

local vector2D FinalPos;

FinalPos.X = (Offset.X < 0 && Width != 0) ? HUDPosition.X - (Width * ResolutionScale) + (Offset.X * ResolutionScale) : HUDPosition.X + (Offset.X * ResolutionScale);

FinalPos.Y = (Offset.Y < 0 && Height != 0) ? HUDPosition.Y - (Height * ResolutionScale) + (Offset.Y * ResolutionScale) : HUDPosition.Y + (Offset.Y * ResolutionScale);

return FinalPos;

}

defaultproperties

{

HudTexture=Texture2D'HTUI.Textures.T_UI_HUD_BaseA'

HudTint=(R=1.0f,G=1.0f,B=1.0f,A=1.0f)

HUDFontScale=(X=3.0f,Y=3.0f)

AmmoPosition=(X=-1,Y=-1)

AmmoTextOffset=(X=-10,Y=0)

AmmoBGCoords=(U=0,UL=76,V=0,VL=126)

HealthPosition=(X=0,Y=-1)

HealthTextOffset=(X=80,Y=0)

HealthBGCoords=(U=131,UL=80,V=0,VL=80)

HUDVitalsPosition=(X=0,Y=-1)

HUDVitalsCoords=(U=512,UL=512,V=0,VL=180)

HUDVitalsBarsZero=0

HUDVitalsBarsFull=491

SafeRegionPct = 1.0f

bShowAmmo=false

bShowHealth=false

bShowVitals=true

bShowCrosshair=true

bDrawColorPalette=false

}

[/csharp]