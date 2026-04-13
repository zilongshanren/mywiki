---
title: How to optimize memory usage and bundle size of a Cocos2D app (Part 2)
url: http://www.learn-cocos2d.com/2012/12/optimize-memory-usage-bundle-size-cocos2d-app-part-2/
author: How; Bundle Size; Learn; Master Cocos
published: '2012-12-03'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Due to technical issues (blank page) I had to split the [previous article (now focuses only on memory optimization)](http://www.learn-cocos2d.com/2012/11/optimize-memory-usage-bundle-size-cocos2d-app/) in two. This is the second part which (mostly) focuses on reducing the app bundle size.

#### Loading Assets In Sequence

Here’s the code that I use to load textures or other assets asynchronously (in background, on another thread).

Imagine loadAssetsThenGotoMainMenu being a scheduled method that runs every frame or perhaps less often. The assetLoadCount and loadingAsset variables are declared in the @interface as int and BOOL respectively.

|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 |
-(void) increaseAssetLoadCount { assetLoadCount++; loadingAsset = NO; } -(void) loadAssetsThenGotoMainMenu:(ccTime)delta { NSLog(@"load assets %i", assetLoadCount); switch (assetLoadCount) { case 0: if (loadingAsset == NO) { loadingAsset = YES; NSLog(@"============= Loading home.png ==============="); [CCTexture2D setDefaultAlphaPixelFormat:kCCTexture2DPixelFormat_RGB5A1]; [[CCTextureCache sharedTextureCache] addImageAsync:@"home.png" target:self selector:@selector(increaseAssetLoadCount)]; } break; case 1: if (loadingAsset == NO) { loadingAsset = YES; [self performSelectorInBackground:@selector(loadSpriteFrames:) withObject:nil]; } break; // extend with more sequentially numbered cases, as needed // the default case runs last, loads the next scene default: { [self unscheduleAllSelectors]; MainMenuScene* mainMenuScene = [MainMenuScene node]; [[CCDirector sharedDirector] replaceScene:mainMenuScene]; } break; } } |


When this method runs the first case statement is executed. To avoid accidentally loading the same image multiple times every time the selector runs, the loadingAsset flag is set to YES. When the texture cache has completed loading this texture, it will call the increaseAssetLoadCount. This then ensures that the next case statement is executed the next time loadAssetsThenGotoMainMenu runs.

The cool thing about this solution is that you can easily add more switch statements to add more textures to load. Because the default case is where the scene changes, and that only happens if there are no more switch cases to process.

Be sure not to skip a number in the switch cases because that will also run the default case.

### Decreasing the size of your app

Besides the memory usage advantage, reducing the color bit depth of textures to 16 bit will also significantly reduce their size. But there are other options that will allow you to reduce your app’s size, perhaps significantly.

#### TexturePacker PNG Optimization

If for some reason you still want to use PNG files instead of the highly recommended .pvr.ccz file format, TexturePacker has a slider named “Png Opt Level” to help reduce the size of PNGs (doesn’t affect loading time though):

As far as I understand it, it tries a given number of optimizations and picks the one that creates the smallest file size. The downside is that the maximum level can take very long for large texture atlases, in some cases 10 to 20 minutes on a Late 2009 27″ iMac. The task is multi-threaded, so it should be a lot faster on quad core systems.

Fortunately there’s really no need to do this unless you’re ready to release the app. Question is, how much can it reduce the size of PNG files?


My largest PNG was reduced from 2.4 MB to 2.2 MB. A smaller one was reduced more significantly (percentage wise) from 180 KB to 130 KB. It may not sound like much but it’s nice to be able to cut down PNG file sizes from perhaps 18 MB to 16 MB total.

Note, however, there’s one important change to your Xcode project that you must not overlook, otherwise your PNG files will be inflated again when they’re packed into the bundle: turn off PNG compression in your target’s Build Settings:

With PNG compression enabled, Xcode will run it’s own PNG optimizer and the PNG files end up being just as large as they were before optimization. So make sure this setting is disabled.

Be sure to check your app’s size to make sure that not optimizing PNG files at all still reduces your app bundle size. Because you’re probably using PNG files that aren’t created by TexturePacker.

#### Check your app’s App Store size

Here’s how you can easily check your app’s size. In Xcode, run an Archive build (Product -> Archive). When the build is successful, the Xcode Organizer window is brought up where you can click the “Estimate Size” button to get an estimate of your app’s App Store size:

#### Remove unused resource files

Over time you’ll add, remove and replace assets in your game. Frequently you still keep using some of the files, others you haven’t removed from the project yet for whatever reason. It’s often fruitful and eye-opening to go over all of your project’s resource files and verify that they’re currently in use. If not, remove them from the project or at least from the app’s target.

Especially if you work on multiple targets (perhaps an iPad or OS X version) you might have accidentally added resource files to a target that doesn’t use that file.

Be sure to thoroughly test your game after removing resource files. There’s always the chance that you “missed a spot”. If in doubt (or not pressed for bundle size) it’s usually better to just leave the files in.

#### Reduce Audio file sizes

Sometimes overlooked, but not taking care of your audio file formats can be wasteful. Both in terms of memory usage and bundle size. Here are the best ways to ensure audio file sizes are kept to a minimum. For all these changes I recommend the free audio editing tool [Audacity](http://audacity.sourceforge.net/).

**Stereo to Mono** - Your MP3 files may be using 2 channels (stereo), but are they using them effectively? If you don’t notice the stereo channel to make any difference, reduce the MP3 files to a single channel (mono). This cuts file size and memory usage in half.

**MP3 Bit Rate** - Any sample rate above 192 kbps is essentially a waste on iOS devices. You have to apply some “trial and **ear**ror” though to find the lowest sample rate which still sounds good. 96 to 128 kbps is usually the sweet spot for MP3 files. If in doubt, make sure you listen to the audio file on the device, with and without Apple speakers - playing the audio file on your computer’s speakers may sound far better or far worse!

**Sample Rate** - Most audio files use a sample rate of 11, 22, 44 or 48 kHz. The lower the sample rate, the smaller the file size. But this also lowers audio quality. For example 11 kHz sounds like a telephone, 22 kHz sounds like good radio reception and 44 kHz is said to be “CD quality” with 48 kHz being even better (only audiophiles with high end equipment can hear the difference).

In many cases 44 kHz or higher is overkill, so try to reduce the sample rate by resampling the audio file (Audacity: Track -> Resample). Do not just set the sample rate, as this will change the pitch of the audio file.

#### Streaming MP3 Files

Depending on how you play audio (AVAudioPlayer, CocosDenshion, ObjectAL, straight OpenAL) you may be accidentally or willfully playing MP3 files using playback from an audio buffer. That means the MP3 file is loaded into memory, converted into an audio buffer (ie uncompressed) and then played back.

From what I know, CocosDenshion’s SimpleAudioEngine has a playBackgroundMusic option that streams MP3 files. Streaming has two advantages: a much smaller memory footprint, and the decoding of the MP3 file is done by the iOS hardware instead of the CPU - unless you stream more than one MP3 at the same time, in which case only one is decoded in hardware.

#### Reduce Tilemap Size

Many developers don’t realize that large tilemaps consume a lot of memory. Assume a 1,000×1,000 tilemap, that would require about a Megabyte of memory - if each tile only used a single byte. However my best estimate for how much a tile consumes comes closer to 64 Bytes. That means this tilemap uses around 60 MB of memory. Ouch!

Besides writing an optimized tilemap renderer, the only option may be to cut down the size of the tilemap. Perhaps splitting it in two if possible.

### That was all?

Uhm, yes. I cut it short a bit this time. I hope you understand. ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

[…] What the FAQ is going to happen with Kobold2D? How to optimize memory usage and bundle size of a Cocos2D app (Part 2) […]

Excellent - extremely useful!

One point - Doesn’t the streaming mp3 tip belong in part 1 (memory usage), as it doesn’t reduce bundle size?

Kind of, but I didn’t want to move it away from the audio paragraph.

[…] 原文链接地址：http://www.learn-cocos2d.com/2012/12/optimize-memory-usage-bundle-size-cocos2d-app-part-2/ […]

Looks like I succeeded to compress the sounds with the following line:

afconvert -f AIFC -d ima4 sound.wav

Looks like it compress more than Audacity.

Hey,

Very informative series of articles!

However I’m unable to access Part1 since quite a few days and I really need to.

Can you please look into the issue.

Thanks!

I moved a paragraph part 1 to this article (part 2, see at the top). The first part now loads fine again.

Hi,

I had this doubt about the size of the pvr.ccz textures. Its a bit larger than png. Since I am planning to support retina display -ipad for my game, app bundle size is a concern for me. While using pvr.ccz , is there any further compression that i can do to reduce the bundle size of my game?

Also, on my ipad2, if the see the disk size of a game like Fancy Pants by going to usage section of general ipad settings, it shows me 1.1 GB where as the downloadable size on app store ia about 100 MB?? How is this made possible? The same is with other games like Angry Birds space, Temple Run 2 etc.

Thanks.,

I have not seen a .pvr.ccz file yet that is larger than the same .png image (with or without PNG optimizations). Have you verified this with a reasonably large (ie 512×512) image that contains actual image information (ie not a single fillcolor or gradient image)? Preferably test it with several different images. It’s possible that certain images may be less susceptible to compression with pvr.ccz but from my experience that should be very rare.

The disk usage in the Settings app includes the app’s bundle plus any locally stored data, such as savegames, images, downloadable content, etc. which can be any size, depends on the app and how the app was used in the past.

Some apps also use highly compressed data in the bundle to make the App Store download size small, but they can’t actually use the compressed data because it would take too long to load. So when you first run such an app, it will unpack all of that data to local storage for faster access, possibly increasing app disk usage by several factors. Other apps merely create lots of local content through normal use, for example audio or video recordings, or copies of documents, music, savegames, etc.

Hi, Thanks for replying in detail. Regarding .pvr.ccz , I am using Texture Packer to save as .pvr.ccz . So every image that i save , I see an increase in on disk size of the image when converted to .pvr.ccz. My images are mostly visual effect and thus have transparency. Also, I came across this thread: http://stackoverflow.com/questions/1686525/pvrtc-compression-increasing-the-file-sizes-of-png

As you mentioned “Some apps also use highly compressed data in the bundle”, I am interested to know how these compressions are achieved? Are any tools that help in doing this? I saw a lot of them for optimizing pngs , but since i am planning to use .pvr.ccz to maintain fast loading times, I am concerned how wud I go about these compressions.

Thanks in advance!

It’s possible that png is better at compressing transparency. Have you tried this with an actual texture atlas where texture packer packs all images tightly? Since it removes the transparent borders of images this should give you better compression. All of the 512×512 or larger texture atlases I worked with were smaller than their PNG counterparts.

Compressing a bundle means using a pack tool like ZIP (perhaps even RAR) and compress all of or just the highly compressible resource files in the bundle in a ZIP/RAR/whatever archive, which is then added to the bundle in place of the resources. On first launch on a device the app then decompresses the archive in the bundle to the app support or similar directory on the device, then loads the resources from there. All you need is a reasonably fast decompression algorithm (no point in saving 5% more space if the app takes >50% longer to decompress).

I wouldn’t recommend doing so, as it complicates publishing the app, loading resources, and generally there’s not too much savings since the app bundle itself is already a ZIP file.

Hi,

I am trying to load assets in sequence as discussed above in the article. I am using a scene manager, In one of the layers , I load 3 textures using the way suggested above. The texture that i load in the last case, the one prior to default does not deallocate when i try to remove texture from another layer say gamelayer. Whichever texture i replace entry 3 with, that one does not get removed/cleared off from memory when i try to remove.

What could be possible issue?

What tells you that it doesn’t get deallocated?

Either something is still retaining the texture, or perhaps when you’re loading another scene that texture is being used again and therefore remains in memory. Hard to tell from afar.

I am loading the texture in a loading layer, so that i can use it in the next layer: gamelayer. Now in game layer , i am trying to remove the texture.

Irrespective of whatever texture it is, if it is the last texture in the switch case, it doesnot get removed when i try to remove it in the gamelayer.

What tells you that it doesn’t get deallocated?

Though i dont see the texture in the dunmtexturecache logs after I removetextureforkey, I can still see it occupying memory chunk in activity monitor, exactly the memory of the texture thats in the case prior to default in switch

have you verified that the previous layer deallocates before the next (game) layer initializes?

not sure about activity monitor accuracy - if iOS employs the same mechanism as OSX it could as well keep the texture in “cached” memory which is essentially free memory if more memory is requested. Check the object under allocations in Instruments, there you can see if an object like CCTexture2D is still “living” or already deallocated.

Hi Steffan,

What’s your opinion on the optimal settings on TexturePacker for a Cocos2D v2.x game targeting iOS 6 and up? I was using:

Texture Format: .pvr.ccz Ver.2

Image Format: RGBA4444

Dithering: FloydSteinbergAlpha

Size Constraints: NPOT

Force Word Aligned: OFF

but then I noticed this warning in the logs (testing on a physical device):

cocos2d: WARNING. Current texture size=(251,1392). Convert it to size=(252,1392) in order to save memory

cocos2d: WARNING: File: sprites_v10-hd.pvr.ccz

cocos2d: WARNING: For further info visit: http://www.cocos2d-iphone.org/forum/topic/31092

So I changed the TexturePacker settings to:

Size Constraints: POT

Force Word Aligned: OFF

After testing my game with these settings there was NO warning in the logs. That’s good. However, Andreas from TexturePacker advised me to set Force Word Aligned to ON.

So using these TexturePacker settings:

Size Constraints: POT

Force Word Aligned: ON

Instruments/Allocations/VM Tracker

POT FWA looks better (comparing to just POT) in terms of

Allocations: 2.91MB vs 3.20MB

Dirty Size: 17.89MB vs 18.19MB

Resident Size: 49.05MB vs 51.04MB

I’m thinking to go with these settings but wanted your expert opinion.

thanks!

Is there a way to just save ipad retina and create ipad non retina on first launch of app on the fly? (downscaling, creating a new texture)

simply doing what texture packer does but at first launch.

All our images are part of spritesheets, pvrccz and we are looking at decreasing app download footprint.

Possible, yes. But a terrible user experience. Imagine if your app launch takes not just 3-4 seconds but dozens of seconds, perhaps even minutes, on a non-Retina iPad.

Especially if you consider doing so because your image files are nearing the over-the-air limit of 100 MB and removing the standard sized images is the only way to stay below that. That would mean reading/rescaling/writing nearly 100 MB of data at launch, this is quite a lot for an iPad.

Besides that cocos2d doesn’t handle looking up resource files in the documents or app data folder, so you’d have to write your own utility function that first checks for image files in documents and only if they don’t exist there, it will look up the file in the bundle.

We are planning to avoid ipad retina overall.

What we want is to use ipad non retina, scale them for iphone 5, 4S and 4 thus keeping a universal build under 100 MB.

Can you help me with some Class etc that people have already written for reading-resizing-generatingplist-writing the texture for cocos2d?

Also, has anyone already written the utility function to fethc images from device documents folder as well?

It will save us time

Thansk for your answer.

That will be a no-go. Apple requires the use of Retina assets on Retina devices. It’s in the developer guidelines.

They have been more lax with games but if the entire game is built with non-Retina assets they may not approve. Personally I think it’s not worth the risk.

But then how are we expected to keep build downlaod sized below 1000MB if we have retina ipad graphics?

Below 100MB not 1000MB (1GB). The download limit is only for over-the-air (Edge, 3G) downloads.

There are many tricks (see my blog) you can use to greatly reduce size of images, mainly .pvr.ccz textures and using lower color bit depths (16 bit, with dithering).

1000 was a typo. I meant 100.

I have been following your blog closely, point is, we don’t want quality of images to decrease, we are already using PVRCCZ textures.

Can you give me links to API/Class which someone has written to achieve the resizing/writing textures coz that looks as one option.

Sorry, I don’t know of any such API or free project. In theory you could use the texture loading code from CCTexture2D and use the created data buffer to write only every 2nd pixel back to a new image file. In CCRenderTexture you’ll find the code that writes a PNG.

Is there a way to just save ipad retina and create ipad non retina on first launch of app on the fly? (downscaling, creating a new texture)

simply doing what texture packer does but at first launch.