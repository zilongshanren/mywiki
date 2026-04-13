---
title: 'HTHUD: Part 3 - Ammo Text Offsetting + Resolution Scaled Text'
url: https://allarsblog.com/2010/03/27/hthud-part-3-ammo-text-offsetting-resolution-scaled-text/
author: Michael Allar
published: '2010-03-27'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

## Video Version

Subject: HTHUD: Part 3 - Ammo Text Offsetting + Resolution Scaled Text

Skill Level: Beginner

Run-Time: 35 Minutes

Author: [Michael Allar](http://backup.allarsblog.com/?ref=allarsblog.com)

Notes: Moving our ammo HUD texture over to the right side of the screen and offsetting our text to rest to the left of it, right aligned against our image. The text will also become resolution scaled so that it looks the same at any resolution. We also add functionality to scale all of our hud text.

## Written Version

Subject: HTHUD: Part 3 - Ammo Text Offsetting + Resolution Scaled Text

Skill Level: Beginner

Author: [Michael Allar](http://allarsblog.com/)

Notes: Moving our ammo HUD texture over to the right side of the screen and offsetting our text to rest to the left of it, right aligned against our image. The text will also become resolution scaled so that it looks the same at any resolution. We also add functionality to scale all of our hud text.

For this tutorial, we will be introducing two new variables for our HTHUD class.

[csharp]var vector2d AmmoTextOffset;

/** Scales the FontSize for all our HUD DrawText Calls */

var vector2d HUDFontScale;[/csharp]

*AmmoTextOffset* is a vector2d that will store the shift in coordinates from our main ammo hud icon. _HUDFontScale _is a second vector2d that will store the scale values for both width and height for all the text we will draw onto the HUD.

### HTHUD - ResolveHUDOffset(...)

This new function will be created so that we can easily find the absolute hud coordinates for us to draw any widget that is to be offset from an already resolved position.

[csharp]/** Offsets an already resolved HUD position and will attempt to place the right/bottom face of the "widget"

* at the coordinates if offset is < 0.0f and width or height is supplied.

*/

function Vector2D ResolveHUDOffset(vector2D HUDPosition, vector2D Offset, optional float Width, optional float Height)

{

local vector2D FinalPos;

FinalPos.X = (Offset.X < 0 && Width != 0) ? HUDPosition.X - (Width * ResolutionScale) + (Offset.X * ResolutionScale) : HUDPosition.X + (Offset.X * ResolutionScale);

FinalPos.Y = (Offset.Y < 0 && Height != 0) ? HUDPosition.Y - (Height * ResolutionScale) + (Offset.Y * ResolutionScale) : HUDPosition.Y + (Offset.Y * ResolutionScale);

return FinalPos;

}[/csharp]

This new function returns a Vector2D which will be the exact location we need to draw to in order for our text to show up correctly as intended. It takes four arguments with the latter two being optional. The first argument is a vector2D named HUDPosition and is the already resolved HUD position we are offsetting from. The second parameter is our vector2D that we are offsetting by from our already resolved HUDPosition. The third and fourth optional parameters are the Width and Height of the widget we are offsetting, and are only used if we are right-aligning our widget. If you know your offset will always be left-aligned, you can call this function without passing width and height.

The first line in the function simply declares our local variable we will use for calculations, FinalPos. Naturally a vector2D.

[csharp]FinalPos.X = (Offset.X < 0 && Width != 0) ? HUDPosition.X - (Width * ResolutionScale) + (Offset.X * ResolutionScale) : HUDPosition.X + (Offset.X * ResolutionScale);[/csharp]

It may look like there is a lot of code going on in this line, but if you break it down its actually quite simple. The reason it looks a little complex is that we are using a new set of operators, ? and : .

How these operators work is quite simple: First you create an expression which will evaluate to true or false, like a standard if statement. In our expression, we are checking if our offset is negative and if we were supplied a width. If both of these conditions are true, we will right-align our widget as generally any negative offset that shifts a widget to the left of its base position will fit better right-aligned. For a more in-depth explanation about this right-alignment magic, see the supplied video.

The next thing we do is use our ? operator. This operator instructs the engine to execute the first code statement following the ? operator if our expression is true, and to execute the second code statement (separated by the : operator) if our expression is false. Lets break this first statement down.

[csharp]HUDPosition.X - (Width * ResolutionScale) + (Offset.X * ResolutionScale)[/csharp]

This will be executed if our expression is true, which means this should handle our right-alignment and it does so. In order to perform this calculation, we first start off with our base position HUDPosition. We are calculating the X and Y values separately, this line focusing on X. Because we are offsetting from our base position, it makes to start off there. Our first calculation is HUDPosition.X - (Width * ResolutionScale), which shifts our position to the left by the width of our widget multiplied by our ResolutionScale. Multiplying our Width by our ResolutionScale ensures that the width used for calculation is consistent with the width of the widget when it is drawn to our current resolution. ResolutionScale is declared in HTHUD and is calculated every time a resolution change occurs. This ensures that we always have the correct ResolutionScale to scale our hud elements by if our resolution is not the standard 1024x768 size that we use for placing HUD objects. By subtracting this width from our HUDPosition.X, this makes it so that the right side of our widget is now on top of the current base position, effectively right-aligning it to our calculated position.

HUDPosition.X - (Width * ResolutionScale) + (Offset.X * ResolutionScale). This last bit, + (Offset.X * ResolutionScale), adds our offset to our current position. This... offsets our current position. We multiply our Offset.X by ResolutionScale so that the perceived offset distance will match on different resolutions, just as how we control the width of our widget based on ResolutionScale.

So while this code executes if our offset is negative and we supply a width to right-align to, this next code statement executes when our expression is not true (when we aren't right-aligning).

[csharp]HUDPosition.X + (Offset.X * ResolutionScale);[/csharp]

If you compare to the first statement, its the same exact thing without the Width being subtracted from our position. This effectively offsets our position while still maintaining standard left-alignment.

The next line of code is as follows:

[csharp]FinalPos.Y = (Offset.Y < 0 && Height != 0) ? HUDPosition.Y - (Height * ResolutionScale) + (Offset.Y * ResolutionScale) : HUDPosition.Y + (Offset.Y * ResolutionScale);[/csharp]

This does the same exact thing as the previous line, but instead adjusts the vertical offset and will bottom-align instead of right-align.

[csharp]return FinalPos;[/csharp]

This returns our newly calculated vector2d containing our resolved position for our newly offset widget! Now we can use this position to draw it onto the screen.

### HTHUD - DrawAmmo()

We will now update our DrawAmmo function to draw our ammo icon on the right side of the screen, also employing resolution independent text and right-aligned offsets.

The first thing we need to do is declare some local variables for us to use during the calculation stages of our ammo drawing.

[csharp]local vector2d POS, AmmoTextOffsetPOS;

local string Amount;

local int AmmoCount;

local float TX, TY;[/csharp]

You will see that we have added AmmoTextOffsetPOS and TX, TY. AmmoTextOffsetPOS is a vector2d that will store the final offset position for our ammo text. TX and TY will store the width and height of our text that will be rendered so we can use it in calculating our offset position, primarily for right-alignment.

[csharp]// Draw the amount

Amount = ""$AmmoCount;

Canvas.DrawColor = WhiteColor;

Canvas.TextSize(Amount, TX, TY);

TX *= HUDFontScale.X; TY *= HUDFontScale.Y;

AmmoTextOffsetPOS = ResolveHUDOffset(POS, AmmoTextOffset, TX, TY);

Canvas.SetPos(AmmoTextOffsetPOS.X,AmmoTextOffsetPOS.Y);

Canvas.DrawText(Amount,,HUDFontScale.X * ResolutionScale,HUDFontScale.Y * ResolutionScale);[/csharp]

The first two lines we have been through before. It stores our AmmoCount as a string into the variable Amount. The second line sets our Canvas DrawColor to White.

The next line however is new. Canvas.TextSize is a function designed to take in a string and figure out the size of that string in pixels if it were to be rendered with the current Canvas font. The width and height of said string then becomes stored in the next two arguments where we have passed in TX and TY. TX now stores the width of the text we will render while TY stores the height.

TX *= HUDFontScale.X; TY *= HUDFontScale.Y; is two code statements on one line. What we are doing here is scaling our calculated width and height by our variable we declared earlier that controls our hud font's scaling. This ensures that future calculations based on TX and TY will be consistent to the scale of which we are drawing our text.

[csharp]AmmoTextOffsetPOS = ResolveHUDOffset(POS, AmmoTextOffset, TX, TY);[/csharp]

This calculates the hud coordinates for our ammo text based on our current position (POS is calculated to be our resolved position for our ammo hud icon prior to this code), the AmmoTextOffset we will define in the defaultproperties block of our code and declared at the top of our class, and our scaled TX and TY for proper right-alignment.

The next line sets our canvas position to our calculated offset.

And the final line draws our text with the HUDFontScale variable we are using to scale all of our text, along with being multiplied by our ResolutionScale so that its perceived size will be the same on any resolution we use.

### HTHUD: DefaultProperties

Now we get to define our two new variables and put them to use!

[csharp]defaultproperties

{

//...

HUDFontScale=(X=3.0f,Y=3.0f)

AmmoPosition=(X=-1,Y=-1)

AmmoTextOffset=(X=-10,Y=0)

// ...

}

[/csharp]

Our HUDFontScale is set to 3.0,3.0; which will scale our text by a factor of 3 in both directions.

AmmoPosition.X is changed to -1, so that it will now be on the right side of our screen.

AmmoTextOffset is set to -10,0. With X being negative, we will be offsetting to the left of our AmmoPosition and also right-aligning the text. With Y being 0, we will not be changing the vertical position of our text relative to our AmmoPosition.

### Result:

[caption id="attachment_452" align="aligncenter" width="300" caption="Our AmmoText is now offsetted, right aligned, and scaled based on resolution"][/caption]![ResolutionIndependentText](../../assets/9ae53dd802fc00f2.jpg)


** **** ******Download Project Source Code Here****