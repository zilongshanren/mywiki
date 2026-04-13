---
title: Photoshop scripting - Cleartype for images
url: http://c0de517e.blogspot.com/2011/11/photoshop-scripting-cleartype-for.html
published: '2011-11-25'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

![]() |

note- the effect is configured for a "landscape" RGB pattern LCD

I always wanted to learn how to script Photoshop (what I learned is that it's a pain and the documentation sucks...), so yesterday I started googling and created a little script to emulate

[cleartype](http://en.wikipedia.org/wiki/ClearType)[on images](http://www.reenigne.org/blog/cleartype-for-images/). Here is the source (it assumes that a rgb image is open in PS):// 3x "cleartype" shrink script

var doc = app.activeDocument;

var docWidth = doc.width.as("px");

var docHeight = doc.height.as("px");

doc.flatten();

// let's go linear RGB

doc.bitsPerChannel = BitsPerChannelType.SIXTEEN;

doc.changeMode(ChangeMode.RGB);

// now that's a bit tricky... we have to go through an action, which has binary data... which I'm not sure it will be cross-platform

// it works on Photoshop CS3 on Win7...

function cTID(s) { return app.charIDToTypeID(s); };

function sTID(s) { return app.stringIDToTypeID(s); };

var desc6 = new ActionDescriptor();

var ref5 = new ActionReference();

ref5.putEnumerated( cTID('Dcmn'), cTID('Ordn'), cTID('Trgt') );

desc6.putReference( cTID('null'), ref5 );

desc6.putData( cTID('T '), String.fromCharCode( 0, 0, 1, 236, 65, 68, 66, 69, 2, 16, 0, 0, 109, 110, 116, 114, 82, 71, 66, 32, 88, 89, 90, 32, 7, 219, 0, 10, 0, 22, 0, 19,

0, 25, 0, 58, 97, 99, 115, 112, 65, 80, 80, 76, 0, 0, 0, 0, 110, 111, 110, 101, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,

0, 0, 0, 1, 0, 0, 246, 214, 0, 1, 0, 0, 0, 0, 211, 44, 65, 68, 66, 69, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,

0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,

0, 0, 0, 9, 99, 112, 114, 116, 0, 0, 0, 240, 0, 0, 0, 50, 100, 101, 115, 99, 0, 0, 1, 36, 0, 0, 0, 101, 119, 116, 112, 116,

0, 0, 1, 140, 0, 0, 0, 20, 114, 88, 89, 90, 0, 0, 1, 160, 0, 0, 0, 20, 103, 88, 89, 90, 0, 0, 1, 180, 0, 0, 0, 20,

98, 88, 89, 90, 0, 0, 1, 200, 0, 0, 0, 20, 114, 84, 82, 67, 0, 0, 1, 220, 0, 0, 0, 14, 103, 84, 82, 67, 0, 0, 1, 220,

0, 0, 0, 14, 98, 84, 82, 67, 0, 0, 1, 220, 0, 0, 0, 14, 116, 101, 120, 116, 0, 0, 0, 0, 67, 111, 112, 121, 114, 105, 103, 104,

116, 32, 50, 48, 49, 49, 32, 65, 100, 111, 98, 101, 32, 83, 121, 115, 116, 101, 109, 115, 32, 73, 110, 99, 111, 114, 112, 111, 114, 97, 116, 101,

100, 0, 0, 0, 100, 101, 115, 99, 0, 0, 0, 0, 0, 0, 0, 11, 67, 117, 115, 116, 111, 109, 32, 82, 71, 66, 0, 0, 0, 0, 0, 0,

0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,

0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,

0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 88, 89, 90, 32, 0, 0, 0, 0, 0, 0, 235, 194, 0, 1, 0, 0, 0, 1, 65, 50,

88, 89, 90, 32, 0, 0, 0, 0, 0, 0, 97, 15, 0, 0, 36, 77, 255, 255, 255, 232, 88, 89, 90, 32, 0, 0, 0, 0, 0, 0, 103, 37,

0, 0, 220, 208, 0, 0, 5, 29, 88, 89, 90, 32, 0, 0, 0, 0, 0, 0, 46, 162, 255, 255, 254, 227, 0, 0, 206, 39, 99, 117, 114, 118,

0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0 ) );

desc6.putEnumerated( cTID('Inte'), cTID('Inte'), cTID('Clrm') );

desc6.putBoolean( cTID('MpBl'), true );

desc6.putBoolean( cTID('Dthr'), false );

desc6.putInteger( cTID('sdwM'), 2 );

executeAction( sTID('convertToProfile'), desc6, DialogModes.NO );

doc.backgroundLayer.applyGaussianBlur(0.75); // limit the frequency a bit to avoid too many fringes

doc.resizeImage(

UnitValue(docWidth, "px"),

UnitValue(docHeight / 3,"px"),

null,

ResampleMethod.BILINEAR // To-do: box filter (mosaic + nearest)

);

var unitValue = UnitValue(1, "px");

// RGB pattern, note that the nearest resize will take the center pixel, that's why red shifts by one and not zero

var redLayer = doc.backgroundLayer.duplicate();

redLayer.applyOffset(unitValue, 0, OffsetUndefinedAreas.WRAPAROUND);

var greenLayer = doc.backgroundLayer.duplicate();

greenLayer.applyOffset(-unitValue, 0, OffsetUndefinedAreas.WRAPAROUND);

var blueLayer = doc.backgroundLayer.duplicate();

blueLayer.applyOffset(-unitValue*2, 0, OffsetUndefinedAreas.WRAPAROUND);

doc.resizeImage( // Resize to "select" the RGB columns in the various layers

UnitValue(docWidth / 3, "px"),

UnitValue(docHeight / 3,"px"),

null,

ResampleMethod.NEARESTNEIGHBOR

);

//var col = new SolidColor(); col.rgb.hexValue = "FF0000"; redLayer.photoFilter(col, 100, false);

redLayer.mixChannels ([[100,0,0,0],[0,0,0,0],[0,0,0,0]], false);

greenLayer.mixChannels ([[0,0,0,0],[0,100,0,0],[0,0,0,0]], false);

blueLayer.mixChannels ([[0,0,0,0],[0,0,0,0],[0,0,100,0]], false);

redLayer.blendMode = BlendMode.LINEARDODGE; // add!

greenLayer.blendMode = BlendMode.LINEARDODGE; // add!

// blue is the base layer

doc.flatten();

// let's go to 8bit sRGB

doc.convertProfile ("sRGB IEC61966-2.1", Intent.PERCEPTUAL, true, true);

doc.bitsPerChannel = BitsPerChannelType.EIGHT;

## 13 comments:

Nice. Now make it gamma correct :)

Seriously though, nice idea. One wonders if it would ever catch on for graphics hardware.

Could you describe it in Pseudo Code or any other way some one who doesn't how to script in Photoshop could understand the algorithm?


Thanks.

Preshing: I did, but the result seemed to be identical, so maybe photoshop is doing resize in gamma. Not 100% sure

Royi: it's really simple, I first resize to 1/3 vertically, then horizontally instead of resizing I take the red channel from the first pixel each three, the green from the second and the blue from the third. The idea is that the RGB elements in a LCD appear packed in this order, side to side, so packing this way three columns into one you kinda get a bit more resolution. The way it's done in photoshop scripting is to create three copies of the image after the vertical resize, shift each one and then do a "nearest neighbor" 1/3 horizontal resize (that will just take the second pixel each three), then making the three layers red, green and blue and merging everything together.

Royi: a lot of color fringing will appear on high-frequency details this way though, so I do a bit of gaussian blur (lowpass filter) before starting this process.

Preshing: I was wrong, it's hard to see its influence on most images but photoshop does not resize in linear, I've fixed this in the script, even if it's quite convoluted

@DEADC0DE: I've done a quick and dirty implementation in C# and I can't seem to replicate your fringing artifacts. The rendering actually seems to work out best for images with high-frequency details (for example), or am I misinterpreting high-frequency?

Rim: yes, you have to have a source image with quite some detail, otherwise you won't notice any difference. On the other hand, if you get too much frequency you'll get fringing for sure. Imagine a 1-pixel black-on-white line in the source image... without pre-filtering, it will get "translated" into a fully red, green or blue line in the cleartype image, which is obviously a severe colour shift that is not acceptable. That's why pre-filtering is useful.

Rim: Notice in fact that in my implementation, you don't really get sharper images, you get smoother edges. Which is the objective of cleartype also on fonts, hardly a cleartype font is sharper than a non-antialiased black on white one, it's smoother...

DEADC0DE: I can't help but wonder if sharpnening isn't precisely what happens to the images. You're obviously right on the font end, but there ClearType is geared specifically towards subpixel hinting for smooth display. On images, all we're doing (at least in my implementation) is effectively trippling the horizontal resolution at the cost of color fidelity, which I think can only increase contrast and doesn't result in smoothing.


Either way, to me the processed images really do look sharper and I can't say I notice any color issues (this includes the image at the top of your post). I'm curious as to whether this might differ from person to person?

Rim: I guess it might be a perception issue but also a given tolerance to some defects, I had different reactions from different persons and the "right" amount of sharpening really is a subjective measure. But surely if you don't bandlmit you will have fringes on some images. The single pixel black line "test" tells us that

DEADC0DE: Are you aware of any research done into this type of image rendering, particularly how it's perceived? It'd be interesting to know whether controlled tests show that it's an appealing display method to the majority of users.



As for the bandlimiting, I certainly see you point. Sadly I don't know enough about DSP to discuss this on proper footing. Intuitively though I'd say it's a tradeoff, paying in contrast detail through blurring to reduce aliassing of the final image.

It's an interesting topic at any rate, so thanks for your post & replies.

Post a Comment