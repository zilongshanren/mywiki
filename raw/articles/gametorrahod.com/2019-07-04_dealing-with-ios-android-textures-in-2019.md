---
title: Dealing with iOS/Android textures in 2019
url: https://gametorrahod.com/dealing-with-ios-android-texture-in-2019/
author: Sirawat Pitaksarit
published: '2019-07-04'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

What's the current situation regarding to **this**? Which one to choose? How to not ended up upsetting the players somehow?

![](../../assets/d1f92c294777f477.png)

## What's the problem

You want everyone to be able to play your game, but mobile platform depends on user's device. You want to snap finger and make everyone with incompatible devices disappear but reality is not so easy.

How to fix this then? It's time! And that's why there is a "2019" in the title. In my opinion we just crossed a meaningful (invisible) breakpoint, that I want to present here what it means for your texture choice.

## Meaning of the Default tab

![](../../assets/1129baea1db7b64f.png)

This is an effort of Unity to unify settings as per the program name. But unfortunately this silver bullet is not effective for textures as you will see soon.

If there is no override on the other tab, it will be auto-configured as **something. **See this page : [https://docs.unity3d.com/Manual/class-TextureImporterOverride.html](https://docs.unity3d.com/Manual/class-TextureImporterOverride.html)

For our purpose, we see that :

- iOS always ended up with PVRTC no matter what. Note that there is a Crunch Compression checkbox which shows crunch quality afterwards. This doesn't affect iOS as Crunch works on DXT and additionally ETC with Unity's forked version of the open source repo. PVRTC is bad. ASTC is good, ETC2 also good. And so in short
**do not rely on Default**with iOS. - Android may ended up as ETC or ETC2 for alpha texture.
**But**this further changes if you have a different sub target set before build.

![](../../assets/6c5bf590e18c4864.png)

### Compatibility table

A bit below in [that same page](https://docs.unity3d.com/Manual/class-TextureImporterOverride.html) shows what it means for your player. What happen if the device doesn't support the format? The meaning of "supported" about these format are that it could be used in memory while compressed, so RAM space taken like you see in Unity editor.

If your player used mismatched phone, it will be :

- Uncompressed, which take time.
- Size expanded to be like RGBA32, it is massive. 2048x2048 takes about 10MB and if your entire game get this treatment you are risking out of memory. (Or the app shutdown easily when your player goes to other apps and come back.)
- The quality of image
**still remains**of that of the compressed format. But you are paying the size equal to the pristine RGBA32.

## ETC and ETC2

ETC and ETC2 is a standard for mobile with wide compatibility, both iOS and Android.

### ETC

No alpha channel support, but OpenGL 2.0 compatible. Unity has some tricks though that is a split alpha, so it save alpha of that image as a separated texture. This option appears only if you select ETC or Crunched ETC.

![](../../assets/a6e7e9817dc80e77.png)

However I don't know if I need a custom shader to utilize that split alpha channel or something. I don't want to try out either lol.

### ETC2

With alpha channel supoprt but only for OpenGL 3.0. Android sucks at catching up to the tech, so you have this constant fear what if the players play the game with OpenGL 2.0 device?

## Crunch texture

Before going further let's recap what this is :

- The size is ridiculously small, but compression time is large. (However uncompression time for your player is fast)
- Originally used together with DXT format, mostly for desktop games. Only few device like Nvidia Shield use DXT.
- Unity forked the original (
[https://github.com/BinomialLLC/crunch](https://github.com/BinomialLLC/crunch)) which you could read technical docs here :[https://blogs.unity3d.com/2017/12/15/crunch-compression-of-etc-textures](https://blogs.unity3d.com/2017/12/15/crunch-compression-of-etc-textures). In short Unity added ETC support to Crunch. Also the original dev of Crunch made[Basis](http://www.binomial.info/)with ETC support as a commercial product.

Unity's ETC fork is nice, but still you have that fear of "OpenGL 3.0 or not"? For all Android devices.

**iOS**

The situation of iOS, classic format is PVRTC which Unity still defaulted to in 2019. However, introducing ASTC which is related to Metal in iOS.

PVRTC sucks both size wise and quality wise. See my previous research about that : [https://gametorrahod.com/pvrtc-vs-astc-texture-compression-on-an-ios-device/](https://gametorrahod.com/pvrtc-vs-astc-texture-compression-on-an-ios-device/)

### ASTC

Why not use ASTC? Because it needs a CPU of A8 or over for Metal support, or you get expanded size. But in 2019 what I want to say is maybe the age of PVRTC is finally over. Look at these A7 and A8 devices :

**A7**

- iPhone 5S
- iPad Air
- iPad Mini 2
- iPad Mini 3

**A8 (Can use ASTC)**

- iPhone 6 and 6 Plus – September 2014
- iPod touch (6th generation) – July 2015
- iPad mini 4 – September 2015

We certainly came a long way from that iPhone 6. So, just ditch PVRTC? I think that's a good idea. Although Unity selects PVRTC by default for you for good reason, it wants to maximize compatibility as its first priority.

ASTC could adjust block size, larger results in lower size and lower quality. The lowest quality 12x12 has a size comparable to crunch texture. Some textures are more resistant to large block, you could experiment with larger block until it looks bad, then step back.

### ASTC's block size

A little bit of how to make the best of ASTC. First of all what is a block compression?

In short, previously we may have 4x4 block and we must store 16 pixels in the pristine RGBA. Now we store 2 pixels plus 16 lerping information for 16 pixels. We use 18 values with less space. Nice! And the block runs from the edge of image, I guess that's easier for the GPU to ask what color to use for this pixel.

![](../../assets/8cccbdc841434f1d.png)

![](../../assets/37386333653e1ee5.png)

Now look at this, the only difference is block size. Why the orange part looks horrible on 10x10 but not on 8x8? It's just 2 pixel difference. (5.4KB saving!) What's happening is probably this :

![](../../assets/5e6f144e969542eb.png)

Because the block runs from the edge, it is possible to get "unlucky" and the block ended up averaging from area with too much color difference! Some algorithm got fixed block size. But ASTC's cool because it got variable block size. (Fixed size per block, that means if you choose small block you get to use more color data for that less amount of pixels) So you could try struggling by reducing the block down until it looks good.

Next question, why is it darker? Hmm, a bit below from that page :

It says ASTC got multiple channel modes to choose from. What Unity use I don't know but probably 3-channel correlated. Look at B channel of this image :

![](../../assets/7e3ee045fa0ac6bf.png)

This B channel looks quite perfect, but that's because R and G channel probably got "dragged down" to that pitch black of B channel. Resulting image is that you see a quite obvious darker block.

How to fix this dark block then? Don't give up to 8x8 block just yet. Unity may not say it obviously but I think this "Compressor Quality" changes color channel mode of ASTC. Adjusting to "Best" while maintaining 10x10 yields this result :

![](../../assets/f334769f3e498ea6.png)

Look closely you could still see the same size of block, **but in a brighter color. **This supports my guess that "Best" is using a color channel mode that computes RGB separately thus taking more time to do so. Now R and G goes up instead of down, because this area is quite red. I still have my 5.4 KB savings AND it looks great. So much research for this one hockey puck.

Now that you know how it works, you can "debug" the image and try to fix it rationally using block size and quality together. Do not just set Best to everything, it takes really damn long time like 20x longer for big images!

### Crunched ETC2

You could also use :

![](../../assets/ceaafd2661f9c903.png)

In which the requirement is OpenGL ES 3.0. Thankfully if Metal (and in turn ASTC) is supported, OpenGL ES 3.0 is guaranteed. Thank you Apple. But remember that the crunch check mark on the default tab do not affect this. You must override to not get PVRTC. And also the default "Auto graphic API" do not have GL 3.0. If you want to use this I think you need to add it over Metal so it is the first priority. (Didn't try, because I would like to use ASTC. I believe in Metal...)

![](../../assets/710fd1455be0a0fd.png)

tl;dr : Use ASTC and the problem's fixed for iOS. Great!

### App Thinning

Maybe ASTC is just fine, but you could go further which I could not assist you anymore. Basically, even with ASTC you are using the same iPad Pro textures if your player use an iPhone SE. With on-demand resource or app slicing you could deliver device specific textures. But I doubt Unity can assist you something this platform-specific. It would likely be a post-build manual work.

## Android

Now we have arrive at the problematic ones.

### What was happening previously

Here are the classic dilemmas :

- Why not just use ETC? No alpha.
- Why not ETC2? OpenGL 3.0.
- Why not RGBA? It's uncompressed lol.
- PNG, JPEG? It must be read out as uncompressed bitmap before able to be put on the GPU. Also Unity do not support this in the importer.
- Compressed in memory format? Each device supports them differently. And there are tons of formats. (More on this
[here](https://developer.android.com/guide/topics/graphics/opengl#textures))

We go with the last one with [Multi-APK support](https://developer.android.com/google/play/publishing/multiple-apks), which the store will serve APK according to player's device. (It knows the graphic hardware, and choose the one with correct compressed textures)

And while this works, it is painful :

- You go to build page in Unity and build 4-6 times. You may have an editor code to help this. Each switch to different override will rebuild your entire game textures.
- Each time you must correctly number your
**version code.**There are devilish rule that each release of**each**variant must be increasing in version numerically and is prone to fuck-ups.[See this article](https://medium.com/@maxirosson/versioning-android-apps-d6ec171cfd82)for more details.[This docs](https://developer.android.com/studio/publish/versioning)stated that max number is 2100000000, so if you fucked up you probably have some room up there but it will trigger your OCD that you can't fix the past numbers. - Those numbering scheme must consider when a player is eligible for multiple APK. The one with higher number gets priority. This doubles the fuck up opportunity as you must now have an another hierarchy of increasing number, over a layer of increasing number for receiving updates.
- You upload 4-6 times.
- If you found any bugs in the game, you do that again AFTER bumping all version numbers up. Even if the upload was for test and not live for real yet, you must still bump the version IIRC.

### Real world example

This is what it looks like in a deployed app. The version code scheme I used is `Axxxx`

where `A`

is 1 2 3 4 5 6 representing each texture format, and `xxxx`

is the displaying game version number. 1705 here means v1.705, also I didn't know about [semver](https://semver.org/) back then. Though, I think semver is not good for game devs as there is no "breaking changes" for games. You may use the leftmost number to hype up a big update instead. (Which here, I am going to update v2.0 soon)

![](../../assets/56c6f00c642efb6f.png)

The one with 42K installs is **ASTC**, (surprisingly?) this is the same as new iOS standard I endorsed earlier.

![](../../assets/b119859da5e6322c.png)

On Android, ASTC is supported by ARM Mali and Adreno (actually it is not vendor specific, so that's very good). Adreno especially is made [by Qualcomm](https://en.wikipedia.org/wiki/Adreno), it's very common. They take up most of the market. Compression quality is good too. Supports alpha channel, and is OpenGL 2.0 OK.

And I put ASTC in `6xxxx`

for a reason : so player get this first before falling back to the other inferior APKs.

Next up, my `5xxxx`

code is on ATC texture format. This format is **only **for Adreno, which you may think why would we use this over ASTC which Adreano could also loads. I first thought that too, but if that is the case the number of download would be 0. Why is that 4.28K appearing then?

![](../../assets/175b7ae58296de9b.png)

Also ATC option disappeared from Unity sometime ago! [Read this post for reason](https://forum.unity.com/threads/unityeditor-mobiletexturesubtarget-atc-deprecated-why.526971/). So, Unity team said it better fall back to ETC2 since all devices that could do ATC has OpenGL 3.0, which enables ETC2.

`4xxxx`

is my PVRTC APK. Some Androids do use them, its not just iOS. It's whopping 400 players out of ~50k. Certainly not a lot and I shouldn't have maintain this variant if I know this lol. The same with `3xxxx`

, this is my DXT section.

A little interesting is that my `2xxxx`

gets 1.55K and my `1xxxx`

section gets 0. What's wrong here?

![](../../assets/0b44303ddae0f33c.png)

![](../../assets/e44666aaf2d0b993.png)

So I was choosing "default" for `2xxxx`

in Unity, and explicitly ETC1 for `1xxxx`

because I was fearing that someone maybe left behind from 6 5 4 3 2 fallbacks. Turns out no one was left behind because they would 100% get `none`

criteria before `GL_OES_compressed_ETC1_RGB8_texture`

. I was so stupid back then!

### Alternative Resources

In `res`

folder there are magic prefixes so you provide multiple version of things and it will be served based on something like screen size. However, OpenGL version is not one of the criteria. Graphic hardware is not the criteria either. So this is no replacement for multi-APK system.

### Android App Bundle (AAB)

Google promise us to end the pain of multiple-APK with AAB, an approach like Apple's app thinning and bitcode. ([https://developer.android.com/guide/app-bundle](https://developer.android.com/guide/app-bundle)) It generates multiple APKs on Google server (literally named `.apks`

), which you could do it manually at home with [bundletool](https://developer.android.com/studio/command-line/bundletool).

Right here, you could build AAB from Unity. Or you could export Gradle project and build it from Android Studio.

![](../../assets/7e06fae51c3d21ae.png)

So while that's good, AAB **cannot** deal directly with texture variants that we were dealing with multiple APKs. Look at the image from that official page, the base module is just 1 version (think of it as 1 APK) and Google has no way to dynamically transform the textures in there. Google couldn't do it before either, because we were building 6 times from Unity and inside each APK we have a different texture format baked. Multiple-APK serve those APK without even knowing its content, but we just put some flag on each APK which device get which. For AAB, **all **devices get this same base module and because you cannot do "multiple-base module", your previous texture split scheme is now invalid.

![](../../assets/b36c2f79f6ac4e59.png)

### Dynamic Delivery

As mentioned, `res`

magic string cannot filter graphic devices. The graphic device filtering was exclusive to multiple-APK.

However, dynamic delivery which is a part of AAB system has something interesting. So it's that "smaller from app store, download pieces of your app later in-app" feature.

At first I think it's not quite the same with multiple-APK in that your user must manually execute a download later in app which is inconvenient (and you must now make a new "download screen" in the game). But actually, [there are 4 modes available](https://developer.android.com/studio/projects/dynamic-delivery) :

- At-install delivery : You make the game as modules, but all are downloaded together. So you can decide to modularize later if you know the game works with all of them downloaded. I am not sure if the size will be summed up to be display on the Play Store or not. (I think it should, or else we would all cheat the app size by putting the textures on dynamic feature packages lol)
- On demand delivery : This is the obvious in-game download later way I mentioned.
- Conditional delivery : Like at-install but with conditions. Let's see more of this.
- Instant delivery : For instant apps, we are not interested in this here.

More on **conditional delivery : **[https://developer.android.com/studio/projects/dynamic-delivery/conditional-delivery](https://developer.android.com/studio/projects/dynamic-delivery/conditional-delivery) quoted :

This delivery mechanism currently supports controlling the download of a module at app install-time based on the following device configurations:

[Device hardware and software features](https://developer.android.com/studio/preview/features#new-conditional),**including OpenGL ES version.**[User country](https://developer.android.com/studio/preview/features#country-condition)[API level](https://developer.android.com/studio/preview/features#minapi-condition)

Now that's related to the texture thing we are dealing with. It may not exactly a graphic device filter, but as we learned OpenGL ES 3.0+ means ETC2 compatible, and in effect, crunch texture compatible. So if you put your textures in a dynamic delivery package, after opting in to AAB deployment, you could make one dynamic delivery with ASTC or something else for GL 2.0 so we could have alpha and good size, and then crunched ETC2 texture for GL 3.0+.

The problem is that all these works are manual, Unity could not possibly cover this kind of platform specific feature. Before you are blinded by "must not left anyone behind" and committed to fully compatible game with more maintenance cost, this is where we make the decision...

### But it's 2019 now

We are looking at you ETC2. Previously (like 4-6 years ago) we would be fearing about OpenGL 3.0 but what about now? If we could ditch OpenGL 2.0 the same way we ditched A7 and lower on iOS side to say goodbye to PVRTC, we do not have to deal with dynamic delivery or whatever. Just use AAB with crunched ETC2 inside. Done!

How to decide about this when there are millions of Android devices out there?

### Android Version

Is not that helpful. [Here](https://developer.android.com/guide/topics/graphics/opengl) it is stated that API 18 (Android 4.3) or higher supports GL 3.0, which is close to 100% of the devices used today. However that's not enough, we need a compatible graphic hardware.

Also I will share a stats from my real world app. Only about 600 out of 50,000 user has a version lower than 4.3, which would disqualify GL 3.0 regardless of hardware. So I think, you just don't have to care about Android version regarding to crunched ETC2 support.

![](../../assets/0b652886007f4402.png)

### ETC2 support by statistics : The Distribution Dashboard

Google made a nifty page here to collect statistics across the world. Conveniently we could see OpenGL version too, that's related to our ETC2 decision right here.

By **May 7, 2019, **this is the stats :

![](../../assets/fac3fca9beee7197.png)

**3.0 + 3.1 + 3.2 taken 78.9% of the market right now.** By this "supported", I think it means not that the device is over API 18, it is **also that **the device has a compatible hardware as well. (Because there is an another stats about API level, and it is almost 100% that everyone is over API 18.)

So, that 21.1% would get an exploded size of your ETC2 textures in RAM plus much more decompression time taken. But the other 78.9% (and also that 21.1%) could enjoy smaller app size enabled by crunched ETC2 texture. Hmm, how much of that 21.1% is a gamer I wonder? How much of that will actually support your game financially? Maybe they have a low-end phone for just communication? Who knows, but it's very tempting to ditch this 21.1% so we have a better dev life, traded with small lost of audience and revenue (?). You know we can't do things for others all the time, we deserve to make ourselves happy too. Not just audience and revenue make us happy, we should also enjoy developing games! (!)

Now look at [this SO post](https://stackoverflow.com/a/13036753/862147) with data from 2014, **83.6% for OpenGL ES 2.0. **That was indeed a bad time to do ETC2, but we came a long way from then.

### ETC2 support by hardware

As I mentioned Adreno take up most of the market. According to [the table of wiki](https://en.wikipedia.org/wiki/Adreno), Adreno higher than 300 has GL 3.0.

And now to the company Qualcomm, which branded their CPU Snapdragon. These are the one with Adreno 300 or higher :

- Snapdragon 208, 200, 210, 212
- Snapdragon 400, 410, 412, 425, 427
- Snapdragon S4
- Snapdragon 600, 800, 801

Look at [https://en.wikipedia.org/wiki/List_of_Qualcomm_Snapdragon_systems-on-chip](https://en.wikipedia.org/wiki/List_of_Qualcomm_Snapdragon_systems-on-chip) for yourself and decide if the introduced years is old enough for you to consider.

### ETC2 support by brands and popular phones

It may be difficult to further see which exact device has that Adreno 300, or a completely unknown graphic hardware. Maybe it is better if we look at some specific brands.

DeviceAtlas collected device information that browse the website with a browser across affiliated websites.

By 29 May 2019 :

![](../../assets/42e0dc991849bf4d.png)

Well Samsungs are all over the place. Let's throw some country specific rankings to the mix too :

![](../../assets/0e964bd8dc650716.png)

![](../../assets/810e29e597961d5a.png)

![](../../assets/9ea602bd46f22869.png)

![](../../assets/c94dcc756873aee4.png)

And from China : [https://www.whatsonweibo.com/top-10-chinas-most-popular-smartphone-brands-models-may-june-2019/](https://www.whatsonweibo.com/top-10-chinas-most-popular-smartphone-brands-models-may-june-2019/)

Currently I am too lazy to check which one can't do ETC2, but I guess I will just use AAB deployment with crunched ETC2 until someone complains in my app review. Life's easier that way!

## Crunched ETC2 characteristics

Now that you are convinced to use just Crunched ETC2, let's observe its artifacts.

![](../../assets/316ced4cb290ab21.png)

![](../../assets/9b30de8e577d7f91.png)

It's not the same blocky artifacts as we saw in ASTC. For image with simple colors with alpha it produces jagged edges while the color stays reasonable. In my opinion, these jagged edge even looks kinda nice. It add hidden details!

![](../../assets/baf70b4d8e23756a.png)

![](../../assets/bfdac7ce4de1e72d.png)

![](../../assets/2205ebf7224d1588.png)

![](../../assets/90cb6a8dc79c4042.png)

However these jagged edge do badly on small sprites with thin edges. For example, these cat's eyes are just a dot. Or that antenna is quite thin. Transition between color seems to exaggerate the artifact. Also notice that cat's color is faded on very low quality. This could also be because of cross-channel compression. (Not sure, haven't studied crunch that much.)

![](../../assets/758e2fadd97c9912.png)

![](../../assets/fd91c09cc96498be.png)

![](../../assets/84cff2069c85907b.png)

![](../../assets/7378ae9405f9c29c.png)

Focus on the gradient on the head. One another characteristic of this algorithm is that it produces a clear gradient boundary on low quality. And also sometimes you get more or less boundaries while increasing or decreasing quality number, as you see here I think the quality 0 one looks more acceptable than 10 or 25 where the boundary looks too obvious.

And focus on the red blush on the cheek too. This is a radial gradient from 2 quite different color. All qualities other than 35 has a visible "outer stroke" of darker green surrounding the blush. And it's also random, like that quality 10 ones that it's less visible than quality 25.

With crunch, the tactics of starting low and gradually go high until its OK may not yields the best result. Sometimes I go down again but choose a different number and they ended up better.