---
title: The Secrets of Colour Interpolation - Alan Zucconi
url: https://www.alanzucconi.com/2016/01/06/colour-interpolation/
author: Alan Zucconi
published: '2016-01-06'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This post discusses about the tricky problem of colour interpolation, and explores possible solutions. Many software and engines offer read-to-use functions to interpolate colours. In Unity, for instance, `Color.Lerp`

is available and does its job pretty nicely. Use the interactive swatch below to see how `Color.Lerp`

works.

There’s nothing wrong in using these functions, as long as you know what the deal with colour interpolation is.

#### Understanding interpolation

Interpolation is a technique that allows you to “fill a gap” between two numbers. Most APIs expose linear interpolation based on three parameters: the starting point ![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)

![Rendered by QuickLaTeX.com b](../../assets/0bcd696a7c0431b0.png)

![Rendered by QuickLaTeX.com t](../../assets/50e9745164dcf617.png)


![Rendered by QuickLaTeX.com \[c = a + \left(b-a\right)*t\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-c658c0858afb911a405dfed6a837246b_l3.png)


When ![Rendered by QuickLaTeX.com t=0](../../assets/6c6cee41bddf42e5.png)

![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)

![Rendered by QuickLaTeX.com t=1](../../assets/09d4c8cafd13cdb0.png)

![Rendered by QuickLaTeX.com a+\left(b-a\right)=b](../../assets/48dc432152c46dd2.png)

![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)

![Rendered by QuickLaTeX.com b](../../assets/0bcd696a7c0431b0.png)


public static Color LerpRGB (Color a, Color b, float t) { return new Color ( a.r + (b.r - a.r) * t, a.g + (b.g - a.g) * t, a.b + (b.b - a.b) * t, a.a + (b.a - a.a) * t ); }

If it’s true that linear interpolation works as expected in three dimensions, the same cannot say for colours. There’s a fundamental difference between the XYZ and RGB spaces: the way the human eye perceive colours. While it make sense to connect two points in a 3D space with a line, the same doesn’t always apply for points in the RGB space. Interpolating the R, G and B components independently offers no guarantee on the hue of the intermediate colours. As [Stuart Denman](https://twitter.com/studenman) highlights in his [Improve Color Blending](http://www.stuartdenman.com/improved-color-blending/), the RGB space of cyan and red meet halway in grey. A new hue appears because the RGB space does not capture how Humans perceive colours very well.

## Hue Interpolation

A first attempt to compensate for this is to switch to different colour space, such as HSV (also known as HSB). It has been designed to be “artist-friendly”, grouping colours by hue and ignoring how they are created on screen.

The result, as it can be seen above, is rather disappointing. The reason is that interpolating the H component cycles through different hues. In this case we don’t have to go through green, but looping over the H space in the opposite direction.

![HSVV255](../../assets/eee7b979008e765b.jpg)

To implement an HSV lerping function we need to understand how these components are handled. For this example, we’ll assume all the HSV components range from 0 to 1. The following code is inspired from [Improved Color Blending](http://www.stuartdenman.com/improved-color-blending/) and relies on the [ColorHSV](https://gist.github.com/cjddmut/fefe5dac35cccfceabec) Unity extension by [C.J. Kimberlin](https://twitter.com/cjkimberlin):

public static Color LerpHSV (ColorHSV a, ColorHSV b, float t) { // Hue interpolation float h; float d = b.h - a.h; if (a.h > b.h) { // Swap (a.h, b.h) var h3 = b.h2; b.h = a.h; a.h = h3; d = -d; t = 1 - t; } if (d > 0.5) // 180deg { a.h = a.h + 1; // 360deg h = ( a.h + t * (b.h - a.h) ) % 1; // 360deg } if (d <= 0.5) // 180deg { h = a.h + t * d } // Interpolates the rest return new ColorHSV ( h, // H a.s + t * (b.s-a.s), // S a.v + t * (b.v-a.v), // V a.a + t * (b.a-a.a) // A ); }

For comparison, the linear lerping through HSV space is also shown together with the corrected lerping (HSV*).

## Luminosity Interpolation

Despite all the effort, the transition still doesn’t look good. The reason is that even if we have correctly learped through the Hue component, different colours have different luminosities. As explained by [Gregor Aisch](https://twitter.com/driven_by_data) in [How To Avoid Equidistant HSV Colors](https://vis4.net/blog/posts/avoid-equidistant-hsv-colors/), equidistant colours in the HSV space are not perceived as really equidistant. Even HSV colours with the same brightness (V) can differ in their perceived brightness and luminosity. Many aspects are responsible for this. The R, G and B components of a colour contributes in different ways the perceived luminosity, due to the way their respective photoreceptors work. Several attempts have been made to capture the non-linear relationships between R, G and B in a colour model. One of the most successful is the LCH (also known as HCL for Hue, Chroma and Lightness). Equidistant colours in the LCH space are also perceived as equidistant. The swatches below clearly shows how the LCH space provides a more uniform distribution of the colours.

The conversion from RGB to LCH is very expensive. This is because colours have to be converted into to intermediate spaces, the XYZ and LAB. A very good library which supports all of these conversions is [chroma.js](https://github.com/gka/chroma.js).

Using colours with equidistant perceived luminosity is essential for all these applications in which colours have a precise meaning, such as diagrams and heatmaps. Providing uniform luminosity is also important for colour blind people, as discussed in [Accessibility Design: Color Blindness](https://www.alanzucconi.com/2015/12/16/color-blindness/). A starting point to design a safe colour palette is [ColorBrewer](http://colorbrewer2.org/).

## Conclusion

Interpolating colours by lerping their RGB components is the most common and ~~lazy~~ easy approach to tackle a very complex problem. If the interpolated colours need to be visible at the same time (for instance in a chart or a diagram) chances are you might need a more advance technique. Conversion from RGB to HSV are supported by most frameoworks, but if you want to go the extra mile you should adopt the LCH colour space.

This post was strongly inspired by the many works of [Gregor Aisch.](https://twitter.com/driven_by_data)

#### Related posts

- Part 1.
[How to Find the Main Colours in an Image](https://www.alanzucconi.com/2015/05/24/how-to-find-the-main-colours-in-an-image/) - Part 2.
[The Incredibly Challenging Task of Sorting Colours](https://www.alanzucconi.com/2015/09/30/colour-sorting/) - Part 3.
[Accessibility Design: Color Blindness](https://www.alanzucconi.com/2015/12/16/color-blindness/) - Part 4.
[GameBarcode: A Study of Colours in Games](https://www.alanzucconi.com/2015/11/18/gamebarcode-a-study-of-colours-in-games/)

## Leave a Reply Cancel reply