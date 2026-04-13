---
title: 'HTHUD: Part 2 - Learning To Use Configuration Files'
url: https://allarsblog.com/2010/03/18/hthud-part-2-learning-to-use-configuration-files/
author: Michael Allar
published: '2010-03-18'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

## Video Version

Subject: HTHUD: Part 2 - Learning To Use Configuration Files

Skill Level: Beginner

Run-Time: 30 minutes

Author: [Michael Allar](https://allarsblog.com/)

Notes: Creating variables in our HTHUD class that are assignable through our .ini configuration files so our end-users can tweak our game settings to their liking.

## Written Version

Subject: HTHUD: Part 2 - Learning To Use Configuration Files

Skill Level: Beginner

Author: [Michael Allar](http://allarsblog.com/)

Notes: Creating variables in our HTHUD class that are assignable through our .ini configuration files so our end-users can tweak our game settings to their liking.

Sorry about the indentation, it seems like my indentation will not survive copy paste… I will go back and fix the indentation later.

HTHUD: Telling it to use a configuration file[csharp]class HTHUD extends UDKHUD

config(UI);[/csharp]

This added keyword "config" to our class declaration allows us to define a configuration file to use to initialize some of the variables in our class. To point to a configuration file, the name of the configuration file must be specified in the parentheses after "config". It is advisable to first check your configuration directory (UDKUTGameConfig) for a configuration file that matches your purpose; i.e. DefaultUI.ini for HUD related purposes. You must specify the configuration file name without the Default or UT prefix.

#### Difference between DefaultConfig and UTConfig files

Any configuration files prefixed with Default correspond to the default assignments of variables that will ship with every copy of your game. These are the settings that will be used before the end-user is able to tweak any of them. UTConfig files are configuration files that the end-user will have access to, and they override the DefaultConfig files. During development, you should always only edit the DefaultConfig files and delete the UTConfig files when changes are made as this ensures all your changes will be propagated to your end-users initial copy and that during testing you will use configurations you've made instead of accidentally using an old configuration setup declared in the UTConfig files.

### Declaring our configurable variables

To learn how to configure variables outside of the code, we will be creating basic variables that just store generic color information. We will then draw these colors to the screen with a series of rectangles. At the top of your code somewhere during the declaration of all your variables, add the following code block:

[csharp]/******************************************************************************

* Common Colors - These are defined in DefaultUI.ini

******************************************************************************/

//var config color WhiteColor, RedColor, GreenColor; //Declared in HUD as const

var config color BlueColor, GrayColor, BlackColor;

var config color CrosshairColor, CrosshairShadowColor;

var bool bDrawColorPalette;[/csharp]

This code block declares some variables for us to use. WhiteColor, RedColor, and GreenColor are already declared in HUD, but I figured that it would be nice to add some more variables with cached colors for us to use in the future and to use for this example. Also note that we can declare multiple variables of the same type on one line separated by commas. There is nothing new here except for the config keyword, which tells Unreal to not use DefaultProperties for initialization but to look in the config file we specified when we declared our class. In fact, if you try assigning these variables values in DefaultProperties, you will get warnings saying that you can not.

We will use CrosshairColor and CrosshairShadowColor in the next tutorial. Also, bDrawColorPalette is a variable I created to control whether or not to draw some test rectangles with the colors of our new variables, just for the purpose of this tutorial.

### Our Test Drawing Function DrawColorPalette

[csharp]function DrawColorPalette()

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

}[/csharp]

This should all look very familiar if you have followed HTHUD Part 1. Note that instead of storing coordinates of a texture that I'm drawing in a variable, I simply hard-coded them in here. The texture I am drawing is a 40x40 white square that I've put on the same texture sheet as our ammo display texture. Also note ColorToLinearColor. I went over the difference between Color and LinearColor in HTHUD Part 1 as well, but because our variables are stored as Color and DrawColorizedTile requires a LinearColor, we must convert from Color to LinearColor. Epic has provided us a function that does just that, conveniently named ColorToLinearColor.

For example purposes, I have shown how to draw a rectangle without a texture. This is what you should do if all you are is drawing a rectangle. To use Canvas' DrawRect function, you simply set your position as usual, set your DrawColor, and then call DrawRect with the size of the desired rectangle. Really simple.

### Calling our DrawColorPalette Function

You can really put this code anywhere in any function that gets called by PostRender. I put mine at the end of DrawHUD()

[csharp]if (bShowGameHUD)

{

DrawGameHud();

}

if (bDrawColorPalette)

DrawColorPalette();[/csharp]

The last to lines of that snippet being my addition. Note that there are no curly brackets after the if statement. We can do this as this signifies that the if statement only controls code flow for the next statement and the next statement only, which is the only thing we need to control with this conditional. It would also be a wise move to put this within the previous if(bShowGameHUD) block so that it will not draw if our HUD is disabled, but that is completely up to you.

### Initializing Our Variables.

We are done with all the UnrealScript required to set this up, so lets edit our configuration file. Because we declared our class to read from a config file named UI, go ahead and open up DefaultUI.ini in UDKUTGameConfig and add the following:

[csharp][UDKGame.HTHUD]

BlueColor=(R=0,G=0,B=255,A=255)

GrayColor=(R=128,G=128,B=128,A=255)

BlackColor=(R=0,G=255,B=0,A=255)

CrossharColor=(R=25,G=128,B=250)

CrosshairShadowColor=(R=0,G=0,B=0,A=255)[/csharp]

The first line tells Unreal that we are now configuring settings for the class UDKGame.HTHUD. (Remember classes are fully named by Package.ClassName)

From there, the syntax is identical to how we would format a defaultproperties box. (We would format arrays differently in some cases, but that's for a future tutorial) While this is the same syntax, the fact that it is now in a configuration file instead of a .uc file means our end-user can change these settings without recompiling the code. Our end-user should not be recompiling our code, so this provides them of a safe way to do so. Also if they mess up their UTConfig file, the engine will automatically generate another based off of our DefaultConfig files. Remember to delete your UTConfig files when you make changes to a DefaultConfig file, so you know that your changes are being used.