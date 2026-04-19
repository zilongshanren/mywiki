---
title: Basic Color Science For Graphics Engineer
url: https://agraphicsguynotes.com/posts/basic_color_science_for_graphcis_engineer/
author: Jiayin Cao
published: '2018-11-29'
source_blog: A Graphics Guy's Note
source_site: https://agraphicsguynotes.com/
category: graphics
fetched: '2026-04-19'
---

For more than a decade, we have been doing HDR rendering in our game engines, which means the intermediate render targets won’t be limited by the precision of the color formats. It is an even more important concept after the emerging of physically based rendering, which is almost what everyone does these days. However, after so much effort rendering everything in linear color space, it is quite wasteful that we can only display colors with only limited chromaticity and luminance defined by sRGB space due to limitations of LDR monitor and TVs.

With HDR monitors and TVs become more and more affordable, game industry has never been so serious about colors like it is now. It is almost a standard feature for modern AAA games. Luckily enough, I got a chance to work on supporting HDR monitor/TV for our game [Skull & Bones](https://skullandbones.ubisoft.com/game/en-us/home/) these days. With limited knowledge about HDR monitor/TV support, I spent lots of my time this week learning some basic color science, which is almost mandatory for me to understand the whole thing. And I learned lots of interesting stuff by doing some really basic research in this field. Most importantly, I strongly believe that it won’t be long before game studios deploy the whole development pipeline in Rec.2020 color space for a wider gamut and better HDR once HDR monitors become more affordable. It is better for me to blog it before I forget everything so that it could be easy for me to pick up in the future.

# Colors are way more than RGB

Unless we do real spectrum rendering, which is even rare in offline ray tracing, RGB is the most common representation that we use to represent a color. However, colors are way more complex than just three numbers. In order to understand colors, the first concept that we need to understand is spectral power distribution.

The light we see every day is composed of lighting signals of different spectrums. Human beings can only see lights with its wavelength ranging from 380 nm to 750 nm, which is a very conservative range. Rays beyond the range exist, but it is not directly visible to a human being so that we usually don’t care about them in rendering.

![](../../assets/94ea59816d3c43fc.jpg)

It is clearly shown the wavelength of visible lights is only a tiny fraction among all wavelengths. Rays like gamma rays, X rays, ultraviolet rays are those with smaller wavelength than the visible range. And infrared, microwaves, radios all have much larger wavelengths. Our focus here is obviously the range starting from 400 nm to 750 nm. Notice, this range is different from what I mentioned before because it was a very conservative range mentioned above, this range is also considered fine for rendering. As a matter of fact, PBRT only considers ranges starting from 400 nm to 700 nm, which is even smaller. So it is not uncommon for you to see ranges with different values in different places, as long as it generally covers the range as a whole, there should be no big problem.

The concept of spectral color is defined as color that is evoked by a normal human by a single wavelength in the visible spectrum. Basically, it is quite rare for us to see spectral color in our life, almost all colors we see is composed of multiple spectral colors. One way to visualize it in a more intuitive manner is to shoot a white light to a prism. Because the index of refraction is a function of wavelength, the white light will be decomposed into multiple beams of lights.

![](../../assets/e102196ce02c50ae.jpeg)

It is not hard to imagine if we project the light luminance signal on different wavelengths, we will have a curve, which reveals the spectral power distribution. This is a very common way to represent a color in a self-explanatory manner. Following is an SPD of a light source.

![](../../assets/a58bd6e1a6f7b2b4.png)

# CIE Chromaticity Diagram

Although some companies do full spectrum rendering in the movie industry, it is rare that anyone attempt rendering something with full spectrum in real time rendering because it is very expensive for interactive rendering. To make things easier for us, color scientists have figured out a way to represent color in a very convenient way to represent color without too much loss of precision.

To see how it works, it is inevitable that we need to look into how human being sees things. Basically, inside our eyes, there are rods and cones on our retina. Rods are responsible for vision at low light levels. Cones are active at higher light levels and capable of color vision. There are three different types of cone receptors in our eyes, with each of them sensitive to light around specific wavelength. One of these types is most sensitive to long wavelengths, around 600 nm, which appear reddish to us. The sensitivity of the second type of cones peaks at the medium wavelength, 550nm, which appear greenish. The last receiptor peaks in the short wavelengths, 450nm, and it appears blueish. Luckily enough, with only three cone receptors in our eye, it is usually good enough to use three numbers to represent colors, the commonly well-known R/G/B.

A color matching experiment works by picking three primaries first as the basis for the whole color space. These primaries contain single wavelength at 615nm, 525nm, 445nm. And for another light containing a single wavelength, there will be three parameters controlling the intensity of each primary to be tuned so that the combined color by mixing the three primaries with correct intensity appears exactly the same to human beings. Keeping doing it for all colors containing one single wavelength ranging in human being visible wavelengths range, we will get a list of numbers, which we can also plot on a two-dimensional space for better visualization of the data.

![](../../assets/11631d2a266bcb2c.png)

Above is an illustration of what the plot will look like across the whole visible wavelength range. One interesting fact we can easily notice is that there are some regions where we need a negative intensity for the primary. This is not physically plausible. What happened is that there is no way to reproduce the light at those wavelengths by simply adding colors containing the three primaries together. We have to ‘cheat’ by ‘subtracting’ colors to make it happen, since there is no real subtracting, what they did was to add color on the target color side to make it happen.

Another way to visualize the data is to plot it in three-dimensional space. Imagine we have a normalized orthogonal space, with R/G/B as the three basis. We can plot all the above points in 3D space constructed by RGB. We can easily get something like this,

![](../../assets/2846ec94d8a5064e.png)

Notice that the curve crosses the BR plane, meaning they have some negative values along the ranges. As a matter of fact, they also have some negative value for the green channel, it is just a little bit hard to see from the above image.

Because sometimes, people only need to care about the hue and saturation of the color, ignoring the intensity, meaning we can reduce the dimensionality by dropping one dimension. This is usually done by projecting the above curve onto the plane r+g+b=1. Another way to think about it is to shoot a ray from the original to every point on the curve, find the intersection set of these rays with the plane r+g+b=1, which is also a curve. Below is an image demonstrating the idea,

![](../../assets/5fcc423f1139053b.png)

Since we have the constraint r+g+b = 1, working in 3D space is kind of unnecessarily complex because we can always reconstruct the original signal in 2D space by utilizing the constraint. That said, we can project this curve on RG plane without caring about B, which usually matches intensity. And then we have this curve on 2D space,

![](../../assets/957b9dc64542e872.png)

This curve enclosure colors with all chromaticity are visible to human beings. However, that is not to say this is displayable with RGB system because some of them have negative value. The displayable area is the grey area. And unfortunately, this is not even the displayable area in most TV/monitors, which is usually smaller than it. We will mention it later.

The fact we have some negative area will easily cause some trouble. And some really smart people come up with this idea, instead of using the primaries mentioned above, why don’t we use some imaginary color as the basis. Here comes the XYZ axis, which is purely imaginary, not physically plausible. The derivation of XYZ axis is out of the scope of this blog. However, since all visible color range lies in the positive area, XYZ is a pretty common color basis when we talk about color science.

Although, there is no way to do the same color matching experiment with XYZ primaries because they are not physically plausible. But we can still transform the original data to the new XYZ space and generate the curve in the new space.

![](../../assets/149cc38bc5bfedf4.png)

Above is the plot for the color matching result in XYZ space, these are all positive values, which is a very important reason to introduce XYZ space in the first place. The same way we plot the samples in 3D space as above, we can do the same for these samples, the only difference is the basis now are XYZ. Only the final projected color range will be shown here for simplicity. However, it is strongly suggested to check out [this page](https://graphics.stanford.edu/courses/cs178/applets/threedgamut.html) for a better feel of this data representation in 3D space.

![](../../assets/f04050e23ba87d31.png)

The professional term for the above curve is called ‘chromaticity diagram’. There is one type of [variation](https://en.wikipedia.org/wiki/CIELUV) of this chromaticity diagram, but this is the most commonly used one. One good thing about this chromaticity diagram is that it allows people from different industry to talk about color in a unified standard. For example, when people talk about a specific color in the above diagram, it is absolutely independent of their hardware used to display, generate the color.

# Color Spaces

Since we already have a place to talk about device independent colors, it can well serve the background as discussions about color spaces. We will only mention the tri-stimulus system, that said only color space with three primaries will be considered here.

There are lots of color spaces out there, sRGB, Adobe RGB, Rec 709, Rec 2020, etc. Since we are only interested in computer graphics, only relevant ones will be mentioned here. But before talking about the color spaces, one important concept is called white point, which deserves our attention here.

## White Point

When we define a color space, it is quite common to specific their primaries coordinate in the chromaticity diagram. However, as we mentioned before, the chromaticity diagram is already a diagram of two-dimension by losing the intensity of the original signal. Then defining just the coordinate of the primaries in the chromaticity diagram is not good enough because there is not enough signal to reconstruct the color space. To put it simply, the scale of each primary is still unknown even if the coordinate in the chromaticity diagram is defined. Instead of defining the scaling factor for each of the primaries directly, people choose to define an extra point called ‘white point’ to implicitly define them.

One important insight to be aware of is that the interpolation on chromaticity diagram is by no means linear after the projections. Just think about the perspective correction in rasterization, it works similarly. Usually, we use (1,1,1) as the white color in the system. However, the white color projection on x+y+z=1 plane is not exactly the centroid ( center of gravity ) of the triangle defined by the primaries in the chromaticity diagram. In order to calculate the chromaticity of the white color, we need the scaling factor for all the three primaries. Just to make it clear, the white point calculation is not our interest here, this is just a clear example to show things. We are more interested in the scaling factor than the white point itself, not to mention in the color space definition, the white point is usually explicitly well defined.

To calculate the three scaling factor, we need to introduce one constraint, that is the Y channel of R+G+B should be exactly 1. With that in mind, if we already have the white point defined in the color space definition the same way the other three primaries are defined, 2D coordinate in the chromaticity diagram. We can easily project the white point back to the XYZ space by scaling the vector so that the Y coordinate is exactly one. And then we have the following equation,

$$ S_r * R_{xyz} + S_g * G_{xyz} + S_b * B _{xyz} = \dfrac{W_{xyz}}{W_y} $$It is very straightforward and easy to solve the equation above,

$$ \begin{bmatrix} S_r \\ S_g \\ S_b \end{bmatrix} = \begin{bmatrix} \dfrac{W_x}{W_y} \\ 1.0 \\ \dfrac{W_z}{W_y} \end{bmatrix} * { \begin{bmatrix} R_x & R_y & R_z \\ G_x & G_y & G_y \\ B_x & B_y & B_z \end{bmatrix} }^{-1} $$## Rec. 709

Rec. 709, also known as BT. 709, is the standard for HD TVs. The first edition of this standard was approved in 1990. Check this page for futher detail.

Following are the primaries for Rec. 709,

- R – ( 0.64 , 0.33 )
- G – ( 0.30 , 0.60 )
- B – ( 0.15 , 0.06 )
- W – ( 0.3127 , 0.3290 )

![](../../assets/f585d912fee5eb45.png)

The above image clearly shows the coverage of Rec.709 gamut. All colors inside the triangle are displayable by sRGB standard, LDR devices won’t be able to reproduce the color outside the triangle. The transformation from the CIE XYZ tristimulus color space into linear Rec.709 space can be calculated by means of a 3×3 matrix,

$$ \begin{bmatrix} R_{rec709} \\ G_{rec709} \\ B_{rec709} \end{bmatrix} = { \begin{bmatrix} 3.2404542 & -1.5371385 & -0.4985314 \\ -0.9692660 & 1.8760108 & 0.0415560 \\ 0.0556434 & -0.2040259 & 1.0572252 \end{bmatrix}} * \begin{bmatrix} X \\ Y \\ Z \end{bmatrix} $$On the other side, it is easy to define the reversed transformation to transform color from Rec. 709 space to XYZ space.

$$ \begin{bmatrix} X \\ Y \\ Z \end{bmatrix} = { \begin{bmatrix} 0.4124564 & 0.3575761& 0.1804375 \\ 0.2126729 & 0.7151522 & 0.0721750 \\ 0.0193339 & 0.1191920 & 0.9503041 \end{bmatrix}} * \begin{bmatrix} R_{rec709} \\ G_{rec709} \\ B_{rec709} \end{bmatrix} $$Apart from the primaries, the transfer function is also defined by the standard.

$$ C_{709}'= \begin{cases} 4.5C_{709}&0<=C_{709}<0.0018 \\ 1.099C_{709}^{1/\gamma} - 0.099 & 0.018<=C_{709}<1 \end{cases} $$ $$ \gamma = 2.2 $$## sRGB

sRGB is the most commonly used color space in game development. It was created by HP and Microsoft together in 1996 for display on monitors, printer and the internet.

The primaries of sRGB are exactly the same with Rec.709. So is the transformation matrix between to transform data from XYZ space. However, it has slightly different transfer function comparing with Rec.709.

$$ C_{sRGB}'= \begin{cases} 12.92C_{sRGB}&0<=C_{sRGB}<0.0031 \\ 1.055C_{sRGB}^{1/\gamma} - 0.055 &0.031<=C_{sRGB}<1 \end{cases} $$ $$ \gamma = 2.4 $$Sadly, sRGB is the most commonly used color space in gaming, even if it only covers only 35.9% of the whole CIE 1931 Color space. Basically, when we talked about physically based shading, an important concept is linear color space. Color can be linear in several different color spaces, the common linear color space we used in our rendering engine is most likely sRGB. This is mostly because most developers use LDR monitor for their daily work. And sRGB was the industry standard for LDR monitors. Unless everyone, at least relevant people, is geared with HDR monitor, which is obviously an investment for a game studio, linear color space is always in sRGB. Even if there is an HDR monitor for everyone in the studio, transiting the whole rendering engine from sRGB to Rec.2020 still involves some work.

What most people do is to perform rendering equation evaluation in sRGB linear color space and then convert the data to Rec.2020 for higher dynamic range. Technically speaking, there is no way to generate any color out of sRGB gamut even if they are converted to Rec.2020. But some game engines will perform color grading in Rec.2020, which will make the color more saturated. In this case, there is some possibility to generate color outside sRGB gamut.

## Rec. 2020

Rec.2020 is the color space of the future. It is designated color space for ultra high TV, or UHDTV. It gets the name from the standards classification: ITU-R Recommendation BT.2020.

The primaries of this color space are equivalent to monochromatic light sources on the CIE 1931 spectral locus. The wavelength of Rec.2020 primary colors is 630nm for the red primary color, 532nm for the green primary color, and 467nm for the blue primary color. They are defined as follows,

- R – ( 0.708 , 0.292 )
- G – ( 0.170 , 0.797 )
- B – ( 0.131 , 0.046 )
- W – ( 0.3127 , 0.3290 )

Following is an image demonstrating the gamut of this color space,

![](../../assets/84278a1f21843aac.png)

There are two things that are very obvious. They share the same white point. Rec. 2020 covers way bigger area than Rec.709/sRGB, the coverage goes from 35.9% to 75.80%.

Similiarly, we can easily calculate the transformation matrix transforming color between XYZ space and Rec.2020 space.

$$ \begin{bmatrix} R_{rec2020} \\ G_{rec2020} \\ B_{rec2020} \end{bmatrix} = { \begin{bmatrix} 1.7166512 & -0.3556708 & -0.2533663 \\ -0.6666844 & 1.6164812 & 0.0157685 \\ 0.0176399 & -0.0427706 & 0.9421031 \end{bmatrix}} * \begin{bmatrix} X \\ Y \\ Z \end{bmatrix} $$ $$ \begin{bmatrix} X \\ Y \\ Z \end{bmatrix} = { \begin{bmatrix} 0.6369580 & 0.1446169& 0.1688810 \\ 0.2627002 & 0.6779981 & 0.0593017 \\ 0.0000000 & 0.0280727 & 1.0609851 \end{bmatrix}} * \begin{bmatrix} R_{rec2020} \\ G_{rec2020} \\ B_{rec2020} \end{bmatrix} $$Perceptual Quantizer is the very common transfer function used to encode the color before feeding into the display. It is like a new ‘gamma correction’. Please refer to this page for detail of this transfer function.

# Wrap Up

As HDR monitors are becoming more and more affordable. It is not hard to imagine that in the near future there will be more HDR content available in the future, whether gaming or movie. However, creating those content usually involves understanding these very fundamental knowledge about color spaces.

The content mentioned in this article is just what I collected in the past few weeks. It barely touches the surface of the whole topic. In order to implement good support for HDR in games, there are way more to do than understanding what is mentioned above. Anyway, I still hope this blog could be helpful to someone who just started the journey like I did a few weeks ago.

# References

[1] [A Beginner’s Guide to (CIE) Colorimetry](https://medium.com/hipster-color-science/a-beginners-guide-to-colorimetry-401f1830b65a)

[2] [HDR Rendering in Lumberyard](https://www.youtube.com/watch?v=LQlJGUcDYy4)

[3] [HDR Ecosystems for Games](https://www.youtube.com/watch?v=OvLuQliiJlg&t=903s)

[4] [RGB/XYZ Matrices](http://brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html)

[5] [White Balancing](https://en.wikipedia.org/wiki/Color_balance)

[6] [Color Vision 1 Color Basis](https://www.youtube.com/watch?v=iDsrzKDB_tA)

[7] [Color Vision 2 Color Matching](https://www.youtube.com/watch?v=82ItpxqPP4I&t=634s)

[8] [Color Vision 3 Color Map](https://www.youtube.com/watch?v=KDiTxWcD3ZE&t=2s)

[9] [Color Vision 4 Cones to see color](https://www.youtube.com/watch?v=V73k_0KuUJo&t=8s)

[10] [Implementing HDR in Rise of the Tomb Raider](https://developer.nvidia.com/implementing-hdr-rise-tomb-raider)

[11] [Prepare for Real HDR](https://developer.nvidia.com/preparing-real-hdr)

[12] [HDR Display in Call of Duty](https://research.activision.com/t5/Publications/HDR-in-Call-of-Duty/ba-p/10744846)

[12] [The Pointer’s Gamut](http://www.tftcentral.co.uk/articles/pointers_gamut.htm)

[13] [How do human being see things](https://www.youtube.com/watch?v=l8_fZPHasdo)

[14] [Introduction to Color Theory](https://graphics.stanford.edu/courses/cs178/applets/locus.html)

[15] [Color Matching](https://graphics.stanford.edu/courses/cs178/applets/colormatching.html)

[16] [Chromaticity Diagrams](https://graphics.stanford.edu/courses/cs178/applets/threedgamut.html)

[17] [Gamut Mapping](https://graphics.stanford.edu/courses/cs178/applets/gamutmapping.html)

[18] [Color spaces – rec.709 vs sRGB](https://www.image-engineering.de/library/technotes/714-color-spaces-rec-709-vs-srgb)

[19] [sRGB](https://en.wikipedia.org/wiki/SRGB)

[20] [Rec. 709](https://en.wikipedia.org/wiki/Rec._709)

[21] [CIE 1931 color space](https://en.wikipedia.org/wiki/CIE_1931_color_space)

[22] [Say Hello to Rec.2020, the Color Space of the Future](https://wolfcrow.com/say-hello-to-rec-2020-the-color-space-of-the-future/)

[23] [High-dynamic-range video](https://en.wikipedia.org/wiki/High-dynamic-range_video)

[24] [CIELUV](https://en.wikipedia.org/wiki/CIELUV)

[25] [The RGB-XYZ Matrix Calculator](http://www.russellcottrell.com/photo/matrixCalculator.htm)