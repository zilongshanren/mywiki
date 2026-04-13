---
title: PVRTC vs ASTC texture compression on an iOS device
url: https://gametorrahod.com/pvrtc-vs-astc-texture-compression-on-an-ios-device/
author: Sirawat Pitaksarit
published: '2017-08-20'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

PVRTC texture compression format has been a long time default, but did you know from **A8 processor** onwards the device now supports ASTC texture compression? (and perhaps you are not taking advantage of it)

In this blog post we will compare it against PVRTC. The long time default for Unity iOS was PVRTC so you might have to manually set the compression format.

“Supports” means it can use the compressed image as-is in the graphic cards without decompressing them. (which is the point of comprssing to these format rather than PNG, etc.) If Unity see that the device does not support the format the size in RAM will be equal to RGBA32, the uncompressed, pixel-to-pixel perfect of your image.

## References

Here’s various reference images that you can comeback to look at later. Click on it to zoom in. Pay attention to the text at bottom of each one.

### Import settings

![](../../assets/3b334de6064a798b.png)

### The build log

![](../../assets/41835735beb4d307.png)

Before continuing test your understanding that everything here are as you expected.

## Brief primers

### PVRTC

From my experience this algorithm has a weakness in an image with contrast or outlines + alpha channel. It do well in realistic textures with randomness but not sprites you see in 2D anime-ish games.

If you have heard of all the Android’s proprietary format (DXT, ASTC, ETC, ATC) I think all of them has artifacts that looks better than PVRTC on non-photorealistic image. (Some Androids also uses PowerVR and uses PVRTC too)

Options are 2 bits and 4 bits. 2 bits gives you exactly half the compressed size of 4 bits with worse quality.

### ASTC

Options for ASTC is block size. From Unity there’s 4 5 6 8 10 12 to choose from. 12x12 is biggest blocksize, gives smallest compressed size and has the worst quality. 4x4 is the highest quality.

## The experiment

![](../../assets/32c217bd7bfc8a3b.png)

In this project you can tap the screen to cycle between all image formats I have prepared. All of them are connected in an inspector, so Unity will load all of them on scene start.

- 256x256 PVRTC 2bit — to show the different between 2 and 4 bit on small size
- 256x256 PVRTC 4bit
- 512x512 PVRTC 2bit — shows that increasing size greatly alleviate the artifact problem
- 256x256 ASTC 4x4 — the best ASTC
- 256x256 ASTC 8x8 — the ASTC with size comparable to PVRTC 2 bit
- 256x256 ASTC 12x12 — the worst ASTC
- 2048x2048 ASTC 4x4 — it’s there so that we can easily see if the device supports ASTC or not by viewing the memory it takes in the RAM.
- 256x256 RGBA32 — the ground truth

All of them has Compressor Quality : Best. (With Fast the size is the same, but the quality will be worse)

### Devices

- iPod Touch Gen 5 (PD714ZP/A) — A5
- iPad mini 2 (ME276TH/A) — A7
- iPhone SE (MLXQ2TH/A) — A9

Unity version : 2017.1.0 p3

## Quality analysis

Unfortunately Medium’s grid maxes at 3 per row. You can click on each one.

![](../../assets/0cf889243a1519cf.png)

![](../../assets/c14ae34531ba1afd.png)

![](../../assets/3a985b1499764fb1.png)

![](../../assets/752d80cf591f8725.png)

![](../../assets/d4989136941d98a9.png)

![](../../assets/f38f25a21f372580.png)

![](../../assets/a40fd58210d9fdfd.png)

![](../../assets/d0b4471e4ce6d0a9.png)

These are screen captured from iPod Touch Gen5.

### PVRTC

You can see that it blurs at only certain place. (and thus it is very noticable) Notably the place with sharp corner like the elbow of the hand that she is holding a notebook. In the case that it happens, often this looks bad because the black outline is being **gradiented **to the lighter color zone. I call this **the smear. **(red circles)

![](../../assets/c5e96dbf267f624c.png)

Also it seems to produce lighter color stairs on its own at curved area. (yellow circle)

On UI images the line will be cleaner, and depending on where you get the smear it really makes the UI looks bad.

![](../../assets/0ad112907bb74071.jpeg)

![](../../assets/22a8f0fa16f90b67.jpeg)

Oh, and you have a chance of getting a different artifact even if the image has the same pixel data. Look at this image, the blue one doesn’t get artifacts on the left edge despite almost the same black and white pixels.

![](../../assets/03d889d221a83efa.jpeg)

I remembered having to nudge some textures in my sprite sheet around just to get an artifact that looks good. (Why are we have to relying on the RNG even before playing the game)

There is another artifact type I call **the dashed.**

![](../../assets/c264854e1f780fac.png)

I didn’t draw any dashed lines there. It seems to copy the nearest dark line and make it a dashed line.

This mostly visible near **straight line. **Your UI images (which usually in small size because maybe you are using 9-slice, thus subject to PVRTC’s damage) might contains more straight line.

On this sample, you can see a jagged line along the left edge of the gauge. It looks so cool by the way!, …but it’s because of PVRTC.

![](../../assets/2c293128c074cbc9.jpeg)

Also strangely, this same compression in the editor (in iOS platform mode) has different artifact pattern than on the device. You can see “the dashed” actually goes out of the boundary.

![](../../assets/5949391f1be0e24a.png)

At 512x512 you can notice that the algorithm does so much better. And note that that one is only 2bit version of PVRTC. (But of course the size quadrupled) You can still see the smear at around the same place.

![](../../assets/88c558a558bfa52b.png)

### ASTC

The artifacts are less random and more blocky, but I love it!

At ASTC 12x12 (biggest block, worst quality) you can clearly see the square block that the algorithm uses all over her body. Even so I think that looks generally better than PVRTC 2 bit’s “smear”. (Not to mention the size is even smaller at 8.3KB vs 16.7 KB)

However on the eye for example, the square artifacts makes it looks worse than the PVRTC counterpart.

![](../../assets/f38f25a21f372580.png)

![](../../assets/0cf889243a1519cf.png)

At smallest and the best 4x4 block size I cold not discern it from RGBA ones, which is impressive. I could even say ASTC is almost a lossless compression at 4x4.

![](../../assets/752d80cf591f8725.png)

![](../../assets/d0b4471e4ce6d0a9.png)

The 2048x2048 ones is there to take up space. Anything at that size should not looks bad or else the algorithm really sucks

### RGBA

This is an uncompressed one thus it is our ground truth. At small 256x256 size it blurs evenly purely according to the filtering mode. I chose Bicubic, if changed to Point interpolation it will be sharper but more pixelated.

## Device analysis

### iPod Touch Gen 5 (A5)

On XCode’s inspector it outright says

![](../../assets/17c9dbabfee7f85c.png)

We have 4 ASTC textures in the scene. That should make sense.

![](../../assets/6db779f9424ba8d9.png)

On Unity we can see that the ASTC 8x8 **takes the same 256.2 KB space** as RGBA32. That means it was uncompressed. This is not an entirely bad thing because you are still benefitted from the decreased game size. It’s only big on your RAM.

In which case if that is your goal, beware that **even the size in RAM is uncompressed, the visual appearance is still that of the ASTC!**

![](../../assets/573e6bec7f2221b7.jpeg)

![](../../assets/5fa7f6befc3c76b0.jpeg)

### iPad mini 2 (A7)

It says the same thing. The light gradient on the 3D plane looks correct now, I wonder what’s the problem with that. Probably something Metal-related that my iPod can’t handle? Anyway we don’t care about that in this article.

![](../../assets/3b864e3c428e4a9e.png)

![](../../assets/f9490ad2684140fa.png)

### iPhone SE (A9)

As I said in the beginning ASTC requires A8 or higher. (Actually StackOverflow said that don’t blame me if it’s wrong) Because iPhone SE has A9 processor it should stop saying about the unsupported texture..

![](../../assets/9cc3514bcee15390.png)

Now ASTC remains compressed in the RAM as it should be. The 2048 ASTC I put in for this purpose drops from 16MB to 4MB, equal to the file size shown on the build log.

![](../../assets/18f515202326fadb.png)

*All cases looks the same in all devices visually.

## Conclusions

- ASTC generally looks better than PVRTC on iOS device.
- For unsupported device lower than A8 ASTC will still looks like compressed but takes full memory equal to uncompressed image.
- Apple does not support multiple app binaries like Google Store as far as I know. If you choose to use ASTC you might have to find a way to restrict older devices.
- Or you can choose to punish those with older processor and ignore them. This might works if there are only a few key images that you don’t want PVRTC to destroy them, like UI elements that appears on many screens. You can set only those to ASTC, then someone with lower than A8 won’t take as much memory punishment.
- Currently you can restrict by iOS version but that is not a reliable way. (The old iPad mini 2 still goes up to iOS 10+) You might have other options to put in the plist as much as possible but still it is not certain that you will get A8+.

**Restricting to iOS devices with A8 or better GPU***I need to restrict my app to only support devices with A8 or newer GPUs. In my info.plist I have the key…*stackoverflow.com

**With iOS 9, Apple lets developers cutoff support for older iOS devices without 64-bit CPUs***With iOS 9, developers can cutoff younger devices in a way that was not previously possible. Although iOS 9 runs on…*9to5mac.com

- Remember that the quest is to get the smallest game size possible + best quality possible +
**under**the RAM limit. Sometimes it’s great to**not**minimize the RAM usage. If you have an**important**2048x2048 spritesheet AND you have 16 MB of RAM to spare at that particular scene that uses it, it is a no brainer to go for ASTC 4x4 without caring about compatibility to shoot for the best clarity. Make room for that 16 MB of RAM in case of an older device! - Remember, if your RAM usage is not over the limit but large what can happen is iOS will restart your app if you switch to something else and come back. To counter this you should implement a system that even if the app restarts it remember where you are. Please take this into consideration if you are planning to “kamikaze” the RAM by using an unsupported texture.
- Be warned! The “
**format is not supported, decompressing texture**” might take much more time than you think. If it happens on a scene’s start that is critical to player’s experience you might want to avoid it. (Or load manually later if possible)

![](../../assets/d4a8925e493a1b5b.png)