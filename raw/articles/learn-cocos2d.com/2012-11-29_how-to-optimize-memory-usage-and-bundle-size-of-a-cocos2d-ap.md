---
title: How to optimize memory usage and bundle size of a Cocos2D app (Part 1)
url: http://www.learn-cocos2d.com/2012/11/optimize-memory-usage-bundle-size-cocos2d-app/
author: Wally says
published: '2012-11-29'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I’m currently completing one last contract project. One of the last things I had to deal with was to optimize the game’s memory usage.

In today’s [iDevBlogADay](http://www.idevblogaday.com/) article I’ll explain how I was able to cut down memory usage by about 25-30 MB (down to 90-95 MB, ie fixing memory warning related crashes) as well as reducing the size of the app bundle from around 25 MB to below 20 MB (which would have been more awesome if Apple hadn’t already increased the over-the-air download limit from 20 MB to 50 MB some time ago).

I’ll also explain how to animate the loading screen while you’re loading resource files, and I’ll add some best practices and common wisdom too.

### What’s using 90% of the memory?

Take a guess.

In almost all cases, it’s textures that consume most of the app’s memory. So textures is where you look to optimize first and foremost if you’re having memory warning troubles.

#### Avoid loading PNG/JPG Textures one after another

The problem with texture loading in cocos2d is that it happens in two steps: first, a UIImage is created from the image file. Then a CCTexture2D object is created from that UIImage. This means while a texture is being loaded, it will consume twice as much memory for a short time period.

The problem used to be so bad that if you loaded 4 textures one after another in the same method, at the end of the method each texture would still consume twice as much memory as it ought to, probably because of the way autorelease works.

I’m not sure if this is still the case, or whether this only applies to manual reference counting but not ARC. I made it a habit to load textures in sequence, waiting at least one frame before trying to load another. This will allow any texture loading overhead to be released from memory. Besides, as you’ll see later, if you want to load textures and other assets in the background this asset-load-sequencing is something you’ll do anyway.


#### Don’t use JPG images!

Cocos2d-iphone has a problem with JPG textures. There’s been a “temporary fix” (temporary for years) in the JPG texture loading routine that causes the JPG to be converted to PNG on the fly. That means cocos2d-iphone loads JPGs extremely slowly [as you can see here](http://www.learn-cocos2d.com/2011/11/depth-ios-cocos2d-performance-analysis-test-project/#image-formats) and a JPG will use three times as much memory while the image is being loaded.

A 2048×2048 texture uses 16 MB of memory. While loading it will use 32 MB of memory for a short time. Now if that image were a JPG file, you’ll see memory spike to 48 MB due to one additional UIImage being created. The memory usage drops back to normal afterwards, but those memory usage spikes are what can kill an app in an instant.

JPGs are bad for loading time and memory usage spikes. Don’t use JPGs!

#### Ignore Image File Size

I see this a lot. It may seem ridiculous, but to be fair, it also requires knowledge about file formats not everyone has. The common perception being that “Hey, I can’t have memory warnings, my image file sizes are not even 30 MB total!”.

Yup, but image file size and texture memory are two different ballparks. Or, let’s say they’re tents. The image file is what space your camping tent takes up in storage while it’s being compressed to a sack or bundle. But if you actually want to use the tent, that tent has to be “inflated” and then it occupies several square feet of real estate.

Same with image files and textures. Image files are compressed, but will necessarily have to be uncompressed into memory where they “become” textures the graphics processor can use. A 2048×2048 PNG image with 32-Bit color depth may be only 2 MB on disk, but it will use 2048 times 2048 times 4 (32 Bits) Bytes of memory: 16 Megabytes!

There are ways to reduce the size of a texture though.

#### Use 16-Bit textures

The quickest way to reduce texture memory usage is to load them as 16-Bit color depth textures. Cocos2d’s default texture pixel format is creating 32-Bit color textures. Halving the bit depth unsurprisingly cuts the memory consumption of a texture in half. It will also render slightly (~10%) faster.

You can change the default texture pixel format with the CCTexture2D class method [setDefaultAlphaPixelFormat](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_texture2_d/#add7db64ac4efbfb1570986c2f0f55ce6):

|
1 2 |
[CCTexture2D setDefaultAlphaPixelFormat:kCCTexture2DPixelFormat_RGB5A1]; [[CCTextureCache sharedTextureCache] addImage:@"ui.png"]; |


Two downsides to this: first, the texture pixel format change affects all textures that are being loaded after you’ve changed the format. You may have to reset the format if you want other textures to use a different texture format.

And failure to match the CCTexture2D’s pixel format to the actual pixel format used by the image will result in strange artifacts, like color bleeding, wrong colors or transparency issues.

#### Which (reasonably useful) texture formats are there?

```
generate 32-bit textures: kCCTexture2DPixelFormat_RGBA8888 (default)
generate 16-bit textures: kCCTexture2DPixelFormat_RGBA4444
generate 16-bit textures: kCCTexture2DPixelFormat_RGB5A1
generate 16-bit textures: kCCTexture2DPixelFormat_RGB565 (no alpha)
```


RGBA8888 is the default. The best color quality for a 16 bit texture is provided by RGB565 because it uses all 16 bits for colors: 65,536 colors. But the downside is that unless the image is rectangular you can’t use that format since it has no alpha (no transparency). It may be useful for background images or rectangular user interface controls though.

The RGB5A1 format trades one color bit for an alpha channel, so the image can have transparent areas. While 1 bit doesn’t sound like much, it actually means there are now only 32,768 colors available. What’s more, the image can only have either fully transparent pixels or fully opaque pixels. There’s nothing in between. You do however can fade in/out textures by changing the opacity property using either RGB5A1 or the RGB565 format.

The RGBA4444 format might come in handy if your source image uses semi-transparent areas. It does allow for 16 alpha values for each pixel, so the image can have transparency although not as fine grained as RGBA8888 textures (255 alpha values per pixel). However the color depth is reduced dramatically to only 4,096 colors! So color quality wise RGBA4444 is the worst 16-Bit image format you can choose, and should be your last choice.

Now you can imagine the other downside of 16-Bit textures: depending on the image contents and the color format the texture might not look as good or may even look terrible. Especially color gradients will create visible “bands”.

#### Making 16-Bit Textures look much better

Fortunately, there’s [TexturePacker](http://www.codeandweb.com/texturepacker).

TP has a feature called dithering that renders many of the artifacts caused by reducing the number of available colors next to invisible. Click on the image to the right for the full-size comparison image between a 32-Bit, 16-Bit and 16-Bit dithered texture.

Especially on Retina displays the pixel density is so high you will not notice the difference between a (properly) dithered 16 bit and a 32 bit texture.

Below is an example from an ingame scene. I have enlarged an area to show you the effect of dithering.

Notice though that the light blue background to the right is actually a 32-Bit texture, whereas the dark blue area to the left is from a 16-Bit texture with dithering. But hey, both look dithered, don’t they?

Cocos2D’s default color bith depth will actually render everything into a 16-Bit color framebuffer that will be displayed on your device’s screen. The dithering you see on the right was created automatically by OpenGL ES due to the reduction of the texture’s 32 bit color depth to the framebuffer’s 16 bit color depth.

Now why not make all textures 16 bit then if the resulting image only uses 16 bit colors? Well, it doesn’t really work that way. Let’s just accept the fact that OpenGL renders scenes at a higher quality if the source textures all had 32 bit colors vs if they all had 16 bit colors. I don’t want to delve too far into this because its quite technical and I’m not the right person to explain it.

#### Use NPOT Textures

NPOT stands for “non power of two”. Even textures are available if you enable NPOT support in cocos2d’s ccConfig.h file. This is only necessary for cocos2d 1.x because cocos2d 2.x has NPOT support enabled by default. All iOS devices beginning with the 3rd generation (iPhone 3GS) respectively all devices that are supported by cocos2d 2.x (aka devices supporting OpenGL ES 2.0) can use NPOT textures.

Using NPOT textures for texture atlases has a huge advantage: it allows TexturePacker to compress the textures more efficiently. There’s very little texture space going to waste, and the textures uses anywhere between 1% to 49% less memory when loaded - depending on how efficiently packed the texture atlas was when it was set to a POT size.

Furthermore TexturePacker allows you to force NPOT on texture dimensions:

Why would you want to do this? Because there’s been a bug (or feature?) in Apple’s OpenGL driver that causes [POT textures to use 33% more memory](http://www.cocos2d-iphone.org/forum/topic/29121).

#### Default to using PVR Textures

TexturePacker enables you to create PVR textures. Despite what you may remember from the past PVR textures do support NPOT dimensions, they don’t have to be a power of two nor do they have to be square anymore.

PVR is the most flexible texture file format. In addition to the standard uncompressed RGB image formats it supports lossy compression with the PVRTC formats. Furthermore the memory overhead of uncompressing a PVR is as low as it can be. Instead of using 2x the texture size in memory while loading as is the case with PNG, the PVR format only uses the texture memory plus the size of the uncompressed image aka the file size.

A common disadvantage of the PVR format is that you can not normally open them on your Mac. But if you’re using TexturePacker you can use the PVR preview app provided by TP, and it allows you to view PVR files even in Xcode.

There is no downside to using the PVR file format! It allows, but does not require or enforce lossy compression. And it has tremendous loading speed advantages, as I’ll explain shortly.

#### Use .pvr.czz File Format

Of the three available PVR file formats, always use the .pvr.czz format. It was specifically designed for cocos2d and TexturePacker, and it generates the smallest PVR files.

The .pvr.czz format also [loads significantly faster](http://www.learn-cocos2d.com/2011/11/depth-ios-cocos2d-performance-analysis-test-project/#image-formats) than any other texture file format. The .pvr.ccz files load in a fraction of the time it takes to load a PNG! You can easily cut down texture loading times by several factors just by switching from PNG to .pvr.ccz.

When using PVR textures with cocos2d, only use .pvr.czz and no other format! It loads exceptionally fast, and uses the least amount of memory when it’s being loaded.

#### Use PVRTC compression where it’s not noticable

PVR textures support PVRTC texture compression (hence: TC) image formats. This means reduced image quality due to [lossy compression](https://en.wikipedia.org/wiki/Lossy_compression). Think of PVRTC as JPG images with ok to medium quality and corresponding artifacts, but with the big benefit of not having to uncompress the texture in memory.

Here’s how a 32-Bit PNG (left) compares to the best quality PVRTC4 (4-Bit) image (click image for full size):

Notice the artifacts are most visible in areas with high contrast. Gradients however compress nicely.

PVRTC is certainly not the image format to use for most of your game’s visuals. But they work nicely for particle effects, small sprites and fast or short-lived animations. As long as you can’t focus on a PVRTC texture because it keeps moving, rotating, scaling it’ll be difficult for you to make out the difference.

#### PVRTC Compressed Image Formats

TexturePacker offers not two but four PVRTC image formats: TC4, TC2 and two variants without alpha.

The principle regarding alpha is the same as for 16-Bit textures. No alpha channel means no transparent areas in the image, but more bits for colors so the image ought to look slightly better.

Sometimes the PVRTC image formats are referred to using 4 Bits and 2 Bits of color, but that is not actually the case. The PVRTC image format does encode a lot more colors than just 4 or 16 colors.

#### Load all textures up front

That is, if you can. If all your textures together use no more than around 80 MB of memory on a Retina device then load them all up front in a loading screen.

The great benefit of doing so is that your app will behave super-smooth, and you don’t have to worry one bit about possibly loading (or perhaps unloading) some assets.

It also makes it easy to ensure that each texture uses the appropriate texture pixel format, and easy to spot any other memory issues not related to textures. Because if your textures are already loaded, whatever is adding to memory usage must be something else.

It just makes it that much easier to look for the remaining memory hotspots if you know that they can’t be related to textures. And you avoid the memory spikes when loading textures, especially if we’re talking 16 MB (2048×2048) textures which temporarily require 32 MB of memory. This goes hand in hand with the next recommendation.

#### Load textures from largest to smallest

Due to the additional memory usage while loading a texture, it is best practice to load the largest textures first and the smallest last.

Assume you have one 16 MB texture and four textures using 4 MB each. If you load the 4 MB textures first, the app will be using 16 MB of memory and will have spiked to 20 MB memory usage while loading the fourth texture. Now when you load the 16 MB texture last, the memory usage will spike to 48 MB before dropping back to 32 MB.

Whereas if you had loaded the 16 MB texture first, the initial spike would have been 32 MB before dropping back to 16 MB memory usage. Then the smaller textures are loaded, adding another 16 MB to 32 MB total memory usage, but with a memory usage spike that only goes up to 36 MB.

That’s a difference of 12 MB in (temporary) memory usage that might make a difference in some cases.

#### Avoid purging caches during memory warnings

What I’ve observed several times is a behavior that is equal to shooting oneself in the foot: textures are being loaded in the loading scene. Memory warning occurs. Cocos2d purges unused textures from cache.

That’s great, isn’t it? No, wait … it isn’t!

What just happened is that you’ve loaded several textures into the CCTextureCache. But since they’ll only be used in the next scene, they are considered “unused” by cocos2d, removed from the cache, and most likely released from memory. And because loading textures creates memory spikes due to a texture shortly using twice as much memory, you’re more likely to receive a memory warning.

So what happens is that cocos2d purges your most recently being loaded textures from memory, and then they’ll be loaded again. Ouch!

Right now, when I do receive a memory warning, I do … nothing. Memory warnings still occur, but thus far only while loading the app. I know what’s going on (memory spike) so I let it slide.

I’ll eventually improve this to unload specific textures and their sprite frames which are only used in specific menu screens (ie settings). Then, wherever I need that texture I’ll first check if the texture is cached before loading the sprite frames. You’ll learn how and why next.

#### Understand when and where to purge caches

Don’t just randomly purge caches or remove unused textures in hopes of freeing up some memory. That’s not good code design. In the worst case this will increase loading times **and** (temporary) memory usage. Analyze what your app is keeping in memory and what can be purged, then only purge that!

You should use the [dumpCachedTextureInfo](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_texture_cache/#ae2b40ef270a73cdfe2398578240b553f) method to see which textures are cached:

|
1 |
[[CCTextureCache sharedTextureCache] dumpCachedTextureInfo]; |


The output looks something like this (I’ve modified it to also print out the image file name without the -hd suffix):

```
cocos2d: "ingamescorefont.png" rc=9 name=ingamescorefont-hd.png id=13 128 x 64 @ 32 bpp => 32 KB
cocos2d: "ui.png" rc=15 name=ui-hd.png id=5 2048 x 2048 @ 16 bpp => 8192 KB
cocos2d: "ui-ingame.png" rc=36 name=ui-ingame-hd.png id=8 1024 x 1024 @ 16 bpp => 2048 KB
cocos2d: "digits.png" rc=13 name=digits-hd.png id=10 512 x 64 @ 16 bpp => 64 KB
cocos2d: "hilfe.png" rc=27 name=hilfe-hd.png id=6 1024 x 2048 @ 32 bpp => 8192 KB
cocos2d: "settings.png" rc=8 name=settings-hd.png id=9 1024 x 1024 @ 16 bpp => 2048 KB
cocos2d: "blitz_kurz.png" rc=1 name=(null) id=12 50 x 50 @ 32 bpp => 9 KB
cocos2d: "gameover.png" rc=8 name=gameover-hd.png id=7 1024 x 2048 @ 32 bpp => 8192 KB
cocos2d: "home.png" rc=32 name=home-hd.png id=4 2048 x 2048 @ 16 bpp => 8192 KB
cocos2d: "particleTexture.png" rc=2 name=(null) id=11 87 x 65 @ 32 bpp => 22 KB
cocos2d: "stern.png" rc=2 name=(null) id=2 87 x 65 @ 32 bpp => 22 KB
cocos2d: "clownmenu.png" rc=60 name=clownmenu-hd.png id=1 1024 x 2048 @ 32 bpp => 8192 KB
cocos2d: CCTextureCache dumpDebugInfo: 13 textures using 60.1 MB
```


This contains very, very useful information. The size, color bit depth (bpp) and size in memory of each cached texture. The “rc” bit is the retain count of the texture, in other words how many times the texture was retained. If the retain count is one or two, that texture is not likely to be currently in use and you may want to remove it from the cache at this point.

It is advisable to remove only textures you know aren’t needed anymore in the current situation, and only remove textures which actually contribute to memory usage. If the texture is just using a couple KB don’t bother to remove it. But anything in the MB range you ought to consider removing if you’re experiencing memory pressure.

#### SpriteFrames retain textures!

The retain count in the above example may be misleading. You may see a texture atlas having a high retain count but you know the texture currently isn’t being used.

The thing is: every CCSpriteFrame retains its texture. So if you’re using texture atlases then it is not enough to remove a texture from CCTextureCache. It will still be retained by the sprite frames and kept in memory! You will also have to call [removeSpriteFramesFromTexture](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_sprite_frame_cache/#ad2bb95d9e83bbf732c9eba2514bc24cd) in order for the texture to be actually released from memory:

|
1 |
[[CCSpriteFrameCache sharedSpriteFrameCache] removeSpriteFramesFromTexture:uncachedTexture]; |


You can also use [removeSpriteFramesFromFile](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_sprite_frame_cache/#aa3a61d8b6e9936f9e5a3bf8f4d264e10) and specify the texture atlas’ .plist file to uncache the corresponding spriteframes.

#### Adding SpriteFrames is costly, every time!


Note:this is only true for cocos2d v1.0 and might still be true for v1.1. Cocos2d v2.x does check if the particular sprite frame plist has already been loaded.

This looks innocent:

|
1 |
[[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFramesWithFile:@"ui.plist"]; |


But there’s a catch: CCSpriteFrameCache doesn’t bother to check if the sprite frames are already cached! It behaves differently than CCTextureCache in that it always (!) loads the frames from the given file and processes them.

How much time that process takes depends on the number of sprite frames in the .plist file. I noticed a huge difference between a texture atlas plist with only 14 sprite frames compared to one with 280 sprite frames. So much so that the 280 frames plist took several seconds to load when I forced the situation and loaded it around 20 times in sequence, whereas the 14 frames plist was done in a fraction of a second (but still a noticeable delay).

That means even a plist with few sprite frames is prohibitively expensive to load during (fast paced) gameplay. You should never do that!

And generally avoid running the addSpriteFrames* methods unnecessarily. They can cause short hiccups in animated scenes or additional delays when changing scenes.

#### Don’t bother uncaching anything but textures

Cocos2D has several caching classes, for textures, sprite frames, animations. But if you want to clean up memory, both sprite frames and animations contribute very, very little to the memory usage of an app.

Of course, if you want to remove a texture from memory, you have to remove its sprite frames - if it has any. In all other cases don’t bother purging sprite frame or animation caches, they use too little memory and loading them back into memory is time consuming, and could even crash if you’re trying to use an uncached sprite frame or animation.

#### Exception: do bother checking audio file memory usage!

Audio files are buffered and usually cached by the sound engine to allow repeated playback without interruption. Since audio files can be quite large, and I’ve seen developers use regular uncompressed audio files for background music, audio buffers can contribute several megabytes if not tens of megabytes to an app’s memory usage.

Do use MP3 files for music. Using uncompressed music is just a waste of memory and file size. When you preload effects don’t forget to unload them when they’re no longer needed. And follow the audio file format suggestions at the end of this article.

#### How to avoid caching certain textures

What if you have textures that really don’t need to be cached? For example the images used in the initial loading screen, or images on screens the user rarely sees - like your super-awesome credits screen.

What’s often misunderstood about CCTextureCache is that for a texture to be displayed, it also has to be in the cache. And if you remove a texture from the cache, it would remove the sprites using the textures or perhaps crash. That is not the case.

The CCTextureCache merely adds another retain to a loaded texture, so that when no other object (ie sprite) references that texture it is still being kept in memory. Using that knowledge, you can uncache a texture right away to allow it to be released from memory as soon as possible:

|
1 2 3 4 |
bg = [CCSprite spriteWithFile:@"introBG.png"]; // don't cache this texture: [[CCTextureCache sharedTextureCache] removeTextureForKey:@"introBG.png"]; |


Just keep in mind that when you remove a texture from CCTextureCache, cocos2d will load that texture again the next time - whether a texture of the same image is currently being used by another sprite or not. So if you’re not careful, you might end up loading duplicate textures into memory!

One such case is when you create textures in a loop that you don’t want to be cached. In this case, make sure you remove the texture from CCTextureCache only after all the nodes using the texture have been created:

|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 |
NSArray* highscores = [Achievements sharedAchievements].highscores; for (HighscoreData* data in highscores) { NSString* entry = [NSString stringWithFormat:@"%05u", data.score]; CCLabelAtlas* label = [CCLabelAtlas labelWithString:entry charMapFile:@"pipizahlen.png" itemWidth:18 itemHeight:27 startCharMap:'.']; [labelsNode addChild:label z:10]; } // don't hold on to this texture: [[CCTextureCache sharedTextureCache] removeTextureForKey:@"pipizahlen.png"]; |


This example is from the highscore screen which, once dismissed, should not hold on to the CCLabelAtlas texture. Since there are no labels added after the initial loading of the highscores scene, I don’t risk loading the label font texture multiple times.

It’s very convenient to uncache textures in this way because you do so close to where you create them, not somewhere in the init of the next scene or during dealloc or by randomly adding calls to purge caches.

#### Use a Loading scene

If you can’t load all your textures up front, use a loading screen when moving between two scenes that use mostly different textures. This allows the previous scene to deallocate before the next scene is created.

The setup is really simple. The loading scene schedules a selector (update) that runs every frame or perhaps with a short interval (0.1 seconds is ok). Unless your previous scene has a memory leak, it will have been released from memory by the time the scheduled selector runs. In the scheduled selector you can then create the new scene.

This effectively avoids the problem of two scenes shortly being in memory at the same time, which becomes a choke point in terms of memory usage and can easily get your app killed due to memory pressure.

#### Load textures in background

The CCTextureCache class supports loading textures in the background via its [addImageAsync](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_texture_cache/#a19844e2980e63b366605eaa97239ba59) methods. You can either use the target/selector or block variant to inform you when the texture has been loaded.

This bit is important: you have to wait for the texture being loaded. Otherwise, you might try to reference the texture shortly thereafter and there’s three things that might happen:

1) app crashes

2) texture is being loaded twice (!) because the async texture hasn’t been loaded yet

3) magnificently the async texture was already loaded and everything will be fine

Don’t rely on #3. It may even look like #3 when it’s actually #2.

#### Load other assets in background

Unfortunately, there’s no async method for loading sprite frames or most other resources. But there’s a simple way to make your own with the help of [performSelectorInBackground](https://developer.apple.com/library/mac/documentation/Cocoa/Reference/Foundation/Classes/NSObject_Class/Reference/Reference.html#//apple_ref/occ/instm/NSObject/performSelectorInBackground:withObject:):

|
1 |
[self performSelectorInBackground:@selector(loadSpriteFrames:) withObject:nil]; |


The corresponding selector takes an object as only parameter (not used here). Just load whatever resources you want to load in the background:

|
1 2 3 4 5 6 7 8 9 10 |
-(void) loadSpriteFrames:(id)object { [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFramesWithFile:@"hilfe.plist"]; [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFramesWithFile:@"home.plist"]; [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFramesWithFile:@"ui.plist"]; [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFramesWithFile:@"gameover.plist"]; [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFramesWithFile:@"ui-ingame.plist"]; [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFramesWithFile:@"settings.plist"]; [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFramesWithFile:@"digits.plist"]; } |


The big advantage of doing this is that your loading scene can be animated. Add a sprite, have it run some actions, you’ll notice instead of freezing it keeps animating smoothly (for the most part). This is true even for devices with a single CPU core, but you may get even smoother animations on devices with multiple CPU cores.

But there’s a catch: you can’t load textures in background, you have to use the addImageAsync method I mentioned earlier. This is because textures need to be created on the same thread that owns the OpenGL context. In that sense you have to load your sprite frame’s textures asynchronously before loading the sprite frames - you must not rely on CCSpriteFrameCache to load the texture for you in the background selector!

### Loading Assets in Sequence & How to reduce app bundle size

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

PVR files are also very handy. They’re pretty good at reducing texture memory size if you have no transparency.

Good point! I knew there was something I wanted to add, that was it!

Great article Steffan!

Very usefull. I’ve learned some very handy tips.

Thanks!!

Very useful advices, but:

“The RGB5A1 format trades one color bit for an alpha channel. […] You also can’t fade in/out textures (changing the opacity property) using this or the RGB565 format.”

Are you sure of that? Are you sure you can’t modify the opacity property of a CCSprite when using RGB5A1?

Also, are you sure PVR is a lossy compression? As far as I know, only PVRTC has lossy compression. PVR remains the same in my case, but well, I use pixel art graphics.

By the way, found a typo: it’s .PVR.CCZ, not CZZ.

Best!

Last time I checked RGB5A1 is either visible or invisible when you modify the sprite opacity.

You can also have PVR textures with an uncompressed image format. I’d have to test if this makes any difference, or which, compared to PNGs.

I confirmed that you can indeed fade textures without an alpha channel or with just a 1 bit alpha channel. The missing or 1-bit alpha channel only affects pixels of the image (ie semi-transparent areas) but the texture itself can still be drawn with any opacity value. I updated the text.

[…] How to optimize memory usage and bundle size of a Cocos2D app […]

[…] with dithering to reduce memory usage. You can learn more about the optimizations I did in my blog post about memory optimization. Overall memory usage is less than 90 MB on a Retina device, this includes fully buffered […]

“The RGBA4444 format might come in handy if your source image uses semi-transparent areas. It does allow for 127 alpha values of a pixel”

I think it has 16 alpha values.

[…] Learn cocos2d本の著者のサイトでメモリ削減テクニックについての記事がありました。 […]

[…] So today, I’ll do some math for you, the things you should consider before starting a project or adding one more of those big new shiny features to your app. Kind of like an addendum to my popular article about memory optimization and reducing bundle size. […]

This article (both parts) rocks! I started with a cocos2d game that was 99.3 MB bundle size and brought it down to 37.6 MB bundle size. The TextureCache memory usage for ipad retina was 67.6 MB - it started at 84 MB with all textures loaded upfront, then I moved rarely used menu images to be loaded and unloaded immediately within the menus.

The one other contributor outside this article which was a huge help was a free tool called ImageOptim to efficiently compress png images. About half the bundle size reduction happened with ImageOptim, and the other half by using pvr.ccz to wrap the pngs into spritesheets and other recommendations in this article.

Thanks again!

This is great to hear!![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


One thing I don’t understand: if you use ImageOptim and then use the optimized PNGs in TexturePacker and export the atlas as .pvr.ccz - are the resulting pvr.ccz files even smaller? I would be surprised if this is the case.

Unless ImageOptim does more than just improve compression, perhaps by modifying the image itself (sort of like JPG), it shouldn’t make a difference because the source image format shouldn’t change the exported atlas’ size.

Have you compared the ImagOptim results with TexturePacker’s own PNG optimization feature?

Thanks, Steffen! I (mistakenly) thought that pvr.ccz was a packaging and layouting format, did not realize that it compressed the individual images as well. You are right, based on the simple test I ran below:

I took two unoptimized images and generated a pvr.ccz (with RGBA_4444 to keep it simple), then I ran imageoptim on the same two images and generated a pvr.ccz with them. Here were the results:

unoptimized images size on disk: 2.4 MB

pvr.ccz from unoptimized images: 1.4 MB

Imageoptim optimized images size on disk: 2.1 MB

pvr.ccz from optimized images: 1.4 MB

Thanks!

Thanks for really useful tips, I understand memory management more with this. In fact, I mis-understand it in some ways.

I used it with my project, and it turned out that I duplicately load texture atlas along with its sprites without clearing texture atlas out. This reduced so much of memory, nearly 40MB down to 28MB for the current stage.

So this means for a texture atlas that has several sprites inside itself. Whenever we finished loading all of the sprite frames, then most of the time we can safely remove (un-cache) it from CCTextureCache right? with the fact that I don’t need that big spritesheet anywhere anymore in the future, because I created all I need already.

Thanks.

If the spriteframes are still in use or simply just cached, you can’t unload the textures because the spriteframes reference (“use”) the texture. What you can do is load the texture up front before loading the sprite frames. But if you load “just” the spriteframes that will of course also load the texture automatically. In other words, spriteframes don’t work without the texture, but a texture doesn’t necessarily need spriteframes.

I think your memory usage goes up because you try to uncache just the texture, and perhaps the spriteframes are “intelligent” enough to then reload the texture. And since texture loading consumes more memory than the texture itself, memory usage will go up (but normally it’s only a short-lived spike).

It’s weird, I used the approach to remove texture from CCTextureCache after created all I want. But for some textures even if I remove them, memory goes bigger compared to not removing them.

Extremely helpful stuff - haven’t really found another clear, comprehensive cocos2d memory guide. Cheers!

[…] http://www.learn-cocos2d.com/2012/11/optimize-memory-usage-bundle-size-cocos2d-app/ […]

Also wanted to say thanks. This was very helpful

Just wanted to say thanks for taking the time to share what you have learnt through lots of testing and a lot of years coding, it may not stop me from making the mistakes!! 😛 but I always know where to come for good solutions and very helpful advise.

Hello Steffen,

these are very useful tips. I really appreciate your work!

I figured out in Instruments that Cocos2d-x allocates memory again by glsmLoadTextureLevelBuffer when the sprite is drawn the first time.

It is also reproducible with the the hello world test app of cocos2d-x.

Maybe it is normal that extra buffer is required?

Can you please explain why that’s the reason?

Thank you,

Stefan

Sorry, I haven’t really dug into cocos2d-x. I do know from cocos2d-iphone that texture loading is (or used to be) a two-step process: load image file into buffer, convert buffer into GL texture. At that moment both buffer and GL texture reside as two separate copies in memory.

Is there any way to use PVR files in SpriteKit? Or is there an alternative that’s just as good? I just don’t know what to use instead of PVR in SpriteKit and every article is just for Cocos2D and says to use PVR.

Could anybody point me in the right direction for SpriteKit optimization?

Thanks!