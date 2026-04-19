---
title: In-game image calibration
url: https://c0de517e.blogspot.com/2011/07/in-game-image-calibration.html
published: '2011-07-09'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

**Goal**

To provide a pleasant gaming experience to the widest audience possible with the least amount of user tinkering! sRGB (or whatever else colour space you're authoring your game in) calibration is not our goal here.

While it's highly advisable that your artists do have professionally calibrated monitors and TV sets to be able to reason about colour in a consistent way, but most users won't.


Honestly this is hardly surprising in a industry that does not seem to care much about color. I've yet to see a game studio that does color "right". Some do care about calibrating desktops and having some TV sets calibrated somehow, at least the ones used for important reviews.

But we're still far from the standards used in video production (enforcement of calibration across all pipelines, control ambient lighting etc...) and while we recently learned that doing our math in a somewhat linear space is more realistic than working in gamma, we really don't reason about color spaces much, and we still author everything in the default 8-bit sRGB (which sucks as it's way too narrow for authoring and it does not get us the flexibility needed to change our mind later on, if needed).


Honestly this is hardly surprising in a industry that does not seem to care much about color. I've yet to see a game studio that does color "right". Some do care about calibrating desktops and having some TV sets calibrated somehow, at least the ones used for important reviews.

But we're still far from the standards used in video production (enforcement of calibration across all pipelines, control ambient lighting etc...) and while we recently learned that doing our math in a somewhat linear space is more realistic than working in gamma, we really don't reason about color spaces much, and we still author everything in the default 8-bit sRGB (which sucks as it's way too narrow for authoring and it does not get us the flexibility needed to change our mind later on, if needed).

**Controls**

There are three main parts we can control when it comes to image display. The image itself (our rendering), the video card output (usually in the form of a gamma curve or a lookup table) and the television set (brightness, contrast...).

Note that it's the entire imaging pipeline that matters. You can't calibrate a TV to any colour space without considering the device that will provide the image signal to the TV set.

In other words, a TV calibrated to sRGB on a ps3 might very well be not be calibrated to the same space on 360, as these two might very well convert the framebuffer numerical values to different output voltages (i.e. by default 360 assumes a gamma 2.2 framebuffer sent to a gamma 2.5 tv and performs a conversion accordingly, ps3 does not apply a gamma curve by default to the framebuffer output).


At the very least we should make sure that the output of all our platforms does match each other, and apply a baseline correction in the hardware (gamma curve or gamma lookup, whatever you have on the graphics card you're using) if that's not the case.


Ideally, we should have our workstations calibrated to sRGB (or whatever color space we want) and use


At the very least we should make sure that the output of all our platforms does match each other, and apply a baseline correction in the hardware (gamma curve or gamma lookup, whatever you have on the graphics card you're using) if that's not the case.

Ideally, we should have our workstations calibrated to sRGB (or whatever color space we want) and use

[R709](http://en.wikipedia.org/wiki/Rec._709)calibrated displays (which are output-device independent, as they are the standard used in HDMI and in general HDTV media, conveniently also sharing the same primary chromaticities with sRGB) to make sure our framebuffers are interpreted as the same space (that's to say, that the numbers in them, when viewed on a R709 device, do correspond to the colors in the space we want to use), or apply a conversion curve in the hardware if not. But this is another story...**Our enemy**

So we have options. Now what? There are plenty of things we can do with our image, from the simple linear brightness contrast (a multiply-add, what photoshop does if you use the "use legacy" brightness-contrast) to better non-linear ones (gamma and curves) to more exothic variants (i.e. colour temperature, rendering exposure, changing your tone mapping operators...).

Well, first of all we have to identify our enemy! For our game to be comfortably playable we want at least to be sure that our image will be always well legible, that's to say that the user can distinguish detail in shadow and brightly lit areas well (with the former being usually more important than the latter).

Dynamic range, and not gamma, is arguably the most import important aspect in TV calibration! That does not mean that changing gamma is not an option but that what our priority should be the tuning onf dynamic range, not achieving fidelity to a given gamma curve (i.e. the sRGB 2.2-ish one).

**Broadcast-safe colors**

Black and white levels are the grayscale intensities at which the screen outputs respectively no light and full intensity, the two extremes of the dynamic range. That's simple.

The problem is how to produce these levels, which signal we need to emit for a given TV to achieve a full black. In theory, you write a zero in the framebuffer and you get out full black. You write something different than zero, and you get something brighter than black out, and you keep being able to distinguish all levels up to full intensity.

In practice, that rarely happens. The theory is a complex mess. Most video standards define a sort of "broadcast safe" range, that's to say, they are designed not to use all of the input range (either voltage or bits) for the entire dynamic range, but allow under and over-shoot areas that should not be used.

Note that this does NOT mean that you should not have these values in your framebuffer, the conversion should be done in the video card as it's part of the output standard.

Different video standards have different black levels: i.e. analog PAL defines its black level at zero IRE, while NTSC puts the same at 7.5 IRE and even digital standards are not so easy, with DV and DVD YCrCb setting black-white at 16-235 (64-940 in 10 bits formats) respectively and HDMI supports both (limited versus extended range, at least in RGB mode, for YCrCb only limited is allowed).

Of course all this would be irrelevant if all devices were well behaved and calibrated to the standards. In practice, that's not true, so we have to find a way to be inside our TV dynamic range.

**How to measure**

We can't use measuring devices so we have to devise some sort of calibration procedure that can be reliably executed by most people.

Most games nowadays just prompt the use with a dark logo on a dark background, asking to make the former "barely visible", or asking to have parts of it barely visible while others should almost disappear in the black background.

The intent there is to be sure that after a given gray level our shadow details will be readable (usually, around 15/255 in framebuffer values) while keeping the overall luminosity not too high, stretching the gamma curve more that it's intended (that's why commonly a second gray value is included, around 6/255, that should be not readable).

It's a decent way to very crudely measure gamma but I argue it's not really the best solution, at least not used as the only calibration aid.

Gamma is not as crucial as dynamic range and from my experiments some TVs especially if set to extreme contrast values (which are far too common even in newer models, as these screen are supposed to "pop" when displayed in a retail store) are no matter what capable of being calibrated with such patterns, and it can be difficult for the use to realize what's wrong.

An easier method is to simply display a small number of bars around the end of the dynamic range, asking the user to tweak controls so that they are able to distinguish all of them from each other, or at least most of them.

It is possible to calibrate gamma

[also using various patterns](http://www.lagom.nl/lcd-test/gamma_calibration.php). These methods are popular for LCD monitors but I won't really try to use them on TVs. They are not so easy to explain and follow and they are not that trivial to author (note: vertical lines should always be used, checkerboard patterns or horizontal lines won't work reliably especially on CRTs) and they are not so reliable (as TVs can do more processing than you would like to such patterns, i.e. sharpening them).**What to correct**

Unfortunately, you can't really hope to achieve a good image without tweaking the television set. Or at least, you can't hope of achieving that for a wide range of users, as televisions with ugly behaviours or ugly defaults are way too common.

One could think that we do have a lot of control in our rendering pipeline, as we can literally apply any transformation on our values. Unfortunately, even if we do have a lot of flexibility, we don't have much precision, and thus we can't really tweak the image much without creating artifacts.

Tweaking the framebuffer output is should be our last resort. We typically have only eight bits of resolution there, so any transformation will result in worsening colour precision and can result in banding.

DirectX support a 10-bit gamma lookup, so we have a better range there, but not that much. If you don't have that luxury, then you might need to touch the framebuffer, so you'll have even less "space" for corrections.

Having the user tweak only the TV setting though is not ideal either. Some users simply won't. And many older TV sets are not capable of achieving a decent shadow definition even twearking their controls.

**A good calibration screen...**

It's an art of balacing and in the end depends on your user base (PC and PC monitors for example are very different from TV sets, and their user base is on average more willing to tinker) and on the requirements of your game. A sport game in broad daylight might work well over a much larger set of conditions than a dark horror FPS. Some games can require more strict objective calibration to be enjoyable while others might want to provide settings for the user to adjust the image to their own liking and so on.

In general you shoud:

- At least have a brightness (or gamma) setting to control the hardware gamma curve. That will make the game usable on most TV sets. Avoid linear brightness.
- Present a "
[dynamic range](http://www.lagom.nl/lcd-test/contrast.php)" adjustment pattern, and ask to tweak the display setting in order to maximize the usable range. - Use clear, easy instructions. Usually if the whites are not distinguishable the user should tweak the contrast setting, while if the darks are not visible, brightness should be adjusted.
- Please, use animated, blinking patterns (i.e. see the
[THX one here](http://www.youtube.com/watch?v=vKBCtcBWmJI))! They are way easier to read than static ones, especially for dark or dark images. - Make your patterns big enough to be visible and to make sure they are not influenced by the latency of the electron beam on CRTs.
- Present your test screen against a simple black or middle gray background, to avoid problems with dynamic adjustment algorithms that might be present in modern televisions. This is especially important when trying to adjust the TV set to produce a good dynamic range. Game controls can be either set using test patterns on a neutral background or be set more subjectively to the user's liking, in that case it would be best to present them overlaid to the game rendering and tunable at any moment.
- At least provide a gamma adjustment setting. This will pretty much act as a brightness control, and its non-linear nature is in practice way more useful than a linear multiply-add control.
- Optionally, provide a contrast setting. Non linear s-curves are preferable.
- I'd also strongly advise to instruct the user to pay attention to the sharpening and denoising setting, as on TVs it almost always do a terrible job with these cranked up. Some games need this more than others depending on their textures, art style and amount of alias. For sharpness a good idea is to display black lines or text on a middle gray background and ask the user to set the sharpness so the lines do not appear jaggy or having white halos around them. For denoising, something with delicate texturing should be presented, asking to change the settings until no smearing is visible. It's a good idea to present reference, exaggerated images of "bad settings".

## 1 comment:

Thanks for sharing, I will bookmark and be back again

Post a Comment