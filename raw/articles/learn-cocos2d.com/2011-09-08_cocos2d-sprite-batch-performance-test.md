---
title: Cocos2D Sprite-Batch Performance Test
url: http://www.learn-cocos2d.com/2011/09/cocos2d-spritebatch-performance-test/
author: Dani says
published: '2011-09-08'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

While writing the [Learn Cocos2D book](http://www.learn-cocos2d.com/store/book-learn-cocos2d/) I was surprised to find that Cocos2D’s **CCSpriteBatchNode** was only able to increase the performance of several hundred bullet sprites on screen by about 10-15% (20 to 22.5 fps). I wanted to re-visit that scenario for a long time because as far as I understood, the more sprites I was drawing the greater the impact of **CCSpriteBatchNode** should be.

But even [Cocos2D’s own sprite performance tests](http://www.cocos2d-iphone.org/wiki/doku.php/perf_test:1_0_0) (compare columns 9 and 10) revealed a performance difference of under 20% (39 to 42 fps). It’s only when all sprites are scaled and rotated, or most of them are outside the screen area, that sprite batching seems to have a bigger impact (25 to 60 fps). Surely that scenario is not applicable to most games. So I started investigating.



Tip:if you are looking for a tutorial that shows you how to work with Sprite Batching as well as Texture Atlases and Texture Packer, you can read it in my[Learn Cocos2D book]or in this[Sprite optimization tutorial]by Ray Wenderlich.

#### Failure to Comprehend

My first attempt recreated the scenario I had before: a single sprite initialized with spriteFromFile and drawing dozens and hundreds of them on screen, then comparing the performance with and without CCSpriteBatchNode. The result confirmed my initial finding that a 15% gain is the absolute best improvement you can see in this scenario. I was even more disappointed this time because my individual images are regular PNG files while my texture atlas is a compressed PVR texture.

I wondered, maybe there is simply no OpenGL state change happening? After all, I’m just rendering many sprites using the same texture, and that texture may remain bound to the OpenGL state from the previous sprite even without sprite batching. The simple solution to test that was to alternate drawing between two different sprite images:



Above: individual PNG images, no sprite batching. Below: sprite batching from PVR texture atlas. 160 Sprites in each test. 2 different images, 256×71 and 128×64. Measured on iPhone 3G.

Said and done, a simple enough change that guarantees a separate draw call for each sprite because the texture has to be replaced for each sprite that is drawn. Alas, the performance difference between batching and not batching the sprites remained the same (meaning: almost negligible). I double and triple checked my test code, but it was correct.

#### What is a Draw Call and what makes it expensive?

In my confusion I turned to Twitter. Thanks to [@MattRix](https://twitter.com/MattRix) and [@GeekAndDad](https://twitter.com/GeekAndDad) I began to understand that that both greater sprite variety and an individual sprite’s texture size should have a great impact on sprite performance.

In other words, it matters a whole lot how much one sprite differs from the previous one and which OpenGL states it changes, which also explains the dramatic effect of sprite batching when sprites are scaled or rotated. I turns out that if you keep rendering the same or very similar sprites in the same way, sprite batching doesn’t really help that much.

I turned back to my test and started using larger sprites (480×320 with lots of transparency) and immediately saw a bigger difference between sprite batching and no sprite batching. With only 10 such large sprites on screen I was getting 15 fps on my iPhone 3G. Once I enabled sprite batching the framerate went up to 60 fps. That’s quite the difference:



Above: individual PNG images, no sprite batching. Below: sprite batching from PVR texture atlas. 10 Sprites in each test. 6 different images, 480×320 each. Measured on iPhone 3G.

With 20 sprites the sprite batching performance was still around 34 fps compared to 7 fps without sprite batching. This means that for anyone who is composing their background images of multiple images (eg for parallax scrolling), sprite batching can make a huge difference even if you only have 3 or 4 different background images.

The same findings apply to the Mac, even more so in fact as you can see from this comparison using the large textures:



Left: individual PNG images, no sprite batching. Right: sprite batching from PVR texture atlas. 2146 Sprites in each test. 6 different images, 480×320 each. Measured on iMac (3.06 GHz Core 2 Duo, ATI Radeon HD 4850 512 MB).

I also re-ran the test with a different set of sprites. This time I wasn’t using any of the large textures:



Left: individual PNG images, no sprite batching. Right: sprite batching from PVR texture atlas. 2146 Sprites in each test. 12 different images, smallest 67×32, largest 150×79. Measured on iMac (3.06 GHz Core 2 Duo, ATI Radeon HD 4850 512 MB).

Lo and behold, if all you did was to run this second test you could easily come to the conclusion that sprite batching has no effect or only starts having a meaningful effect under relatively unrealistic circumstances. Consider that in this Mac test I had to render 16.000 sprites before the non-batched test went down to 20 fps while the sprite-batched test remained at 60 fps.


Pro Tipfor iMac users: Run Mac test, with 20.000+ sprites. Leave test running for 20 minutes. Turn iMac flat, screen facing down. Use egg with iMac. Nom, nom, nom.

#### The Conclusion

If you, like myself, were under the misconception that sprite batching particularly helps when rendering many of the same or similar sprites, then maybe you’ve been wasting performance? In fact, it’s **the larger images** that you will want to **draw all from the same texture atlas** to improve sprite batching performance. The ideal scenario being that all assets of the entire scene fit into just one texture atlas.

It can even be beneficial for the performance of level-based games, in which each level only uses a subset of the images, to create separate texture atlases for each level if that allows you to get each level’s assets into just one texture atlas. Even if that means duplicating some assets like the player character and HUD graphics. Nothing beats rendering everything from the same texture atlas!

Most definitely you should not use separate texture atlases for each image category. I’ve seen this in a few developer’s projects where they used relatively small texture atlases (128×128 to at most 512×512), each of which only contained the images for the player character, for one type of enemy, for the HUD, for the background elements, and so on.

The above test is the *Sprite-Performance* template project of [Kobold2D](http://www.kobold2d.com/) Preview 3. Kobold2D shall hereby for the first time and henceforth be [publicly available for download](http://www.kobold2d.com/display/KKSITE/Kobold2D+Download). Thanks to all testers!

You can easily adapt the *Sprite-Performance* test to use your own assets, and its configurable by modifying the settings in the config.lua file. Each test displays a specific number of sprites randomly on screen, first without sprite batching, then with sprite batching.

Each sprite is guaranteed to be entirely on screen, if it’s dimensions don’t exceed the screen dimensions. The random seed is reset for each run to ensure that the exact same sprites are used and placed at the exact same position to make the tests comparable. And of course the test runs on both iOS devices and Mac, with Simulator having the FPS display disabled since Simulator performance is entirely meaningless and should not be measured or compared.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Hello.

In our current shooter project we use a unique sprite batch node that contains all the main stuff needed (tons of airplanes, animations, weapons, etc…) and it helps performance so much.

Another advantage of having it all there is that you avoid duplicate sprites and you can use any enemy, animation, etc in any level. You don’t need to have a sprite batch node for Level 1, and another different one for Level 2, duplicating things.

The problem is that the texture size exceeds 1024×1024, so it cannot run on iPhone 3G.

Regards.

it sounds like your not using PVR in the non-batched test? ie. your comparing PNG renders to PVR renders. In this case, the PVR will run much faster on large images than PNG will due to superior gpu cache usage. This has nothing to do with batching which is mainly a CPU issue.

If you want to test batching vs non-batching, make sure you use PVR textures in both instances.

Also, it is best-practice to use milliseconds to measure timing difference. FPS can be deceptive since it is non-linear… that is 1 -> 2 fps is fantastic, 31 -> 32 fps is negligible.

Yes, the test was PNG vs PVR. I wanted to test worst case (PNG, individual files) with best case (PVR, texture atlas, batching). You’re right that the conclusion is skewed because of PVR being the optimal format for rendering.

I think FPS are easiest to understand. Deceptive only if you don’t take into account relative differences. I should have added % differences though.

[…] Cocos2D SpriteBatch Performance Tests […]