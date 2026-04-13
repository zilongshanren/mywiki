---
title: How much memory? Calculating the Size of Textures, Audio Buffers, Classes and
  Collections
url: http://www.learn-cocos2d.com/2013/01/memory-calculating-size-textures-audio-buffers-classes-collections/
author: Tcg Says
published: '2013-01-24'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

When you embark on a project, the first thing a developer ought to do is to run some basic math. Especially if you already have some specs regarding the number and sizes of assets. Because otherwise you may [end up trying hard to work around a memory related issue](http://stackoverflow.com/questions/14422891/jerks-in-animation-in-cocos-2d) which perhaps even modern desktop computers would struggle with.

So today, I’ll do some math for you, the things you should consider before starting a project or adding one more of those big new shiny features to your app. Kind of like an addendum to my popular article about [memory optimization and reducing bundle size](http://www.learn-cocos2d.com/2012/11/optimize-memory-usage-bundle-size-cocos2d-app/).

#### How much wood texture would a woodchuck choke on if a woodchuck could choke on wood textures?

A texture is an in-memory representation of an image made up of individual pixels. Each pixel uses a certain amount of memory to represent its color. A texture’s memory size is therefore simply the product of **width * height * sizeof(color)**.

Before I go any further, I like to stress it again: **the size of an image file is much smaller than the size of the texture generated from the image**. Don’t use image file sizes to make memory usage estimations.

Most common are 32-Bit and 16-Bit textures which use 4 and 2 Bytes respectively per pixel. A 4096×4096 image with 32-Bit color depth therefore uses 64 MB memory. Let that sink in for a moment …

At 16-Bit it only uses half of that, though without color dithering (TexturePacker does this for you) this might not look too good depending on the image.

This is pretty much what you’re stuck with unless you **export textures as .pvr.ccz**. Not only does this format load tremendously faster than PNG (not to speak of JPG which are unbearably slow to load in cocos2d), the .pvr.ccz format also reduces the texture memory size because the texture can stay compressed in memory.

It’s extremely difficult to estimate how much smaller a PVR texture’s memory footprint will be without actually giving it a try. But you can expect anywhere between 10% to 50% reduction.

#### To the non-power-of-two!


Another way to reduce memory usage of textures is to **ensure they are non-power-of-two (NPOT)**. This will prevent the texture from expanding to the next nearest power-of-two dimension. Since most textures aren’t exactly power of two dimensions to begin with, the savings can roughly be around 5% to 30%.

Cocos2d 2.1 supports NPOT textures out of the box, in earlier versions you’ll have to enable CC_TEXTURE_NPOT_SUPPORT in ccConfig.h. NPOT textures are supported by 3rd generation (iPhone 3GS) devices and newer, so it’s pretty much a no-brainer. There are no other drawbacks for NPOT textures.

But wait! There’s another reason why NPOT textures can [rid you of 33% texture memory usage](http://stackoverflow.com/questions/9438009/ios-textures-taking-33-extra-memory):

There’s a bug in all iOS 5 versions ([fixed in iOS 6.0](https://devforums.apple.com/message/693644#693644)) where memory for mipmaps is automatically allocated whether you use mipmaps or not. This bug only affects POT textures and does not occur on NPOT textures.

#### Audio Buffers

You can calculate the memory usage of an audio effect as well. Again, audio files may be compressed as a file on disk but are expanded into a (usually) uncompressed audio buffer. The buffer size is the product of the **sample rate * channels * bitrate/8 * length**.

Sample rate is expressed in kHz, most commonly used are 11, 22 and 44 kHz. There are either one (mono) or two channels (stereo). Most audio files are mono only, I think most playback methods actually refuse to play stereo effects. The bitrate is typically 16-Bit (2 Bytes) for all audio effects these days. And length is the length of the effect in seconds.

An audio effect with a 44.1 kHz (44,100 Hz) sample rate, mono channels, 16-Bit per sample and 10 seconds length therefore uses:

|
1 |
(44.1*1000) * 1 * (16/8) * 10 = 861 Kilobytes |

For streaming audio (mp3) normally they are, well, streamed. In that case there’s only a small buffer holding the next few seconds of audio data.

But you can also play back mp3 files as audio effects in which case they will be buffered entirely into memory (something you should try to avoid). If the MP3 is encoded with a constant bitrate of 192 kbps then the memory usage of the mp3 will be bitrate/8 * channels * length. A 60 seconds stereo MP3 with a 192 kbps bitrate therefore uses about:

|
1 |
(192*1000/8) * 2 * 60 = 2.75 Megabytes |

These are not exact values though because padding and header data can change the actual memory usage. For MP3s encoded with variable bitrate (VBR) you can only use the average bitrate to get a rough estimation of the actual size.

#### How much memory do spriteframes use? And sprites?

Forget about it. It’s negligible. Textures and audio typically account for 95% of an app’s memory usage. Though there can be krass exceptions (more on this further down).

In cocos2d 2.1 each CCSpriteFrame allocates 80 Bytes of memory. Each CCSprite allocates 368 Bytes. Even a thousand sprites use no more than 360 KB of memory.

You can easily check the size of instances of a particular class with an Objective-C runtime method:

|
1 2 3 4 5 |
#import <objc/runtime.h> Class class = [CCSprite class]; NSLog(@"%@ instance size is %lu bytes", NSStringFromClass(class), class_getInstanceSize(class)); |


You’ll be hard pressed to find any class that exceeds 512 bytes of memory usage per instance. The largest cocos2d class seems to be CCLabelTTF with 648 bytes per instance.

However, keep in mind that class instance size does not return the size of other class instances a class uses, or memory buffers that were allocated with malloc. If a class has a pointer to, say a CCTexture2D* or just a void* memory buffer then that will count as 4 bytes - the size of the pointer. You’d have to manually add the size of a CCTexture2D instance or buffer, too.

For primitive data types (int, float but also CGPoint, CGRect) you can use the sizeof function:

|
1 |
NSLog(@"CGRect size is %lu bytes", sizeof(CGRect)); |

#### What about collections such as NSArray or NSDictionary?

It depends on the implementation details of the collection. However they only store pointers to your data. So the quickest estimate is always how much data per entry times the number of entries.

For a dictionary with NSString keys (average length of let’s say 20 characters) and values that are instances of CCSprite (384 Bytes) and 250 entries you can estimate the dictionary size as follows:

|
1 2 |
class_getInstanceSize([NSMutableDictionary class]) + (20 * 2 * 250) + (384 * 250) = 104 Kilobytes |

It may be a little more due to optimizations that trade size for speed. For example the dictionary might also store the hash values for the keys for quicker access. Depending on the hash size this adds another 4 to 16 bytes per entry, but that would add only 4 Kilobytes on top.

#### BOOL, bool and Classes

Something else to be aware of: the size of a BOOL or bool data type is 1 byte on iOS and Mac OS X.

However classes are typically padded to the next nearest 32-Bit size. Moreover, each ivar is padded to the next nearest 32-Bit boundary unless the following ivar is of the same type. That means whenever you add a BOOL ivar it will actually occupy 4 Bytes unless there’s another BOOL following it - in which case both will still occupy 4 Bytes: 1 + 1 + 2 bytes padding.

This class will have an instance size of 40 Bytes (NSObject is 8 bytes plus the ivars):

|
1 2 3 4 5 6 7 8 9 10 11 12 13 |
// instances of this class allocate 40 Bytes @interface TestClass : NSObject { int i; BOOL b; int j; BOOL c; int k; BOOL d; int l; BOOL e; } @end |

An int is 4 Bytes which makes 16 Bytes for the ints. However the BOOLs also use 4 bytes each due to padding, that makes 16 + 16 + 8 = 40 Bytes.

You can manually optimize this class to use less memory by packing BOOLs together. Even though the savings are minimal it is generally advisable to layout class ivars (or properties without a backing ivar) in the order of the data types’ size with largest first and smallest last.

Which means BOOL/bool types should be last, and short/unsigned short (16-Bit types) should be second to last. The order of structs like CGPoint (8 Bytes) or CGRect (16 Bytes) or double (8 Bytes) or pointers (4 Bytes iOS, 8 Bytes Mac OS X) don’t actually matter because they’re already aligned to 32-Bit boundary and no padding will be added to them anyway. It’s only important that they’re declared before the 16-Bit and 8-Bit data types.

This version of the class has an instance size of 32 Bytes because 1-Byte BOOLs followed by 1-Byte BOOLs do not need to be padded to 32-Bits by the compiler. Only the last BOOL will be padded so that the entire class instance is padded to a 32-bit size.

|
1 2 3 4 5 6 7 8 9 10 11 12 13 |
// instances of this class allocate 32 Bytes @interface TestClass : NSObject { int i; int j; int k; int l; BOOL b; BOOL c; BOOL d; BOOL e; } @end |

#### Int, BOOL and bit arrays

If you have a C array as a collision map for a tilemap, then the memory usage of that will be **tilemap.width * tilemap.height * sizeof(datatype)**. For a tilemap that’s 500×500 and where you’re using int to encode the collision information the memory usage is:

|
1 |
500 * 500 * 4 = 977 Kilobytes |

You better switch over to a BOOL array if you only need the YES/NO state:

|
1 |
500 * 500 * 1 = 244 Kilobytes |

Not bad. But pretty wasteful still. You only need the one bit state: there’s either collision or there is not. Using 8 Bits (1 Byte) for that information wastes 7 Bits of memory. Sometimes sacrificing a little runtime performance for less memory usage can be beneficial.

In such a case use a bit array. [This lightweight bitarray library](http://michael.dipperstein.com/bitlibs/) is included in [Kobold2D](http://www.kobold2d.com/) and [KoboldTouch](http://www.koboldtouch.com/). Suddenly your collision array is a lot smaller (by factor 32 compared to the int array):

|
1 |
500 * 500 * 1/8 = 30 Kilobytes |

To test for a collision bit you’ll just have to calculate the index of a bit at a given position as usual and then use the BitArrayTestBit method:

|
1 |
BOOL isCollision = BitArrayTestBit(&collisionBitArray, index); |

The bit test operation is a bit more costly than checking a BOOL directly, but the overhead isn’t much and often offset by all the other code dealing with collisions.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

I’ve seen issues with using sprite frames in an animation from a NPOT texture atlas. In some frames, there is a subtle shift in the placement of the pixels within the frame. The problem goes away if you give the atlas POT dimensions. The kicker is that this problem doest exist in the simulator.

It might not even be cocos2d’s fault but the program with which you create the texture atlas. I’ve never seen an issue like this.

I’m using the latest TexturePacker. It can be a very subtle effect so it might not be obvious in cases where two sprites differ a lot in appearance. Also not every frame is affected, so if your’re lucky, the problem never appears. I’ve tried correlating it to how TP is putting the frames into the atlas, but so far I haven’t found any relationship between the textures placement and whether or not the bug appears. The best case to see the issue is if you have two frames with high contrast transparent edges where nothing changes except the color of the opaque pixels. If the bug shows up, there will be a slight shift in the position of the pixels when you toggle between the two.

Since the problem doesn’t occur in the simulator, I’m leaning on thinking the bug is in the hardware driver, but I haven’t had the time to look any further. I’ve just taken the triage approach of using POT textures for any atlases that are showing the problem.

I might try playing around with TPs ability to add transparent buffer pixels around each texture to see if slightly shifting things around will give me a texture that doesn’t have the problem for the animated frames.

For future reference, here’s the bug tracking link:

http://code.google.com/p/cocos2d-iphone/issues/detail?id=1345