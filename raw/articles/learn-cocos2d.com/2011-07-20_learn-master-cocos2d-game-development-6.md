---
title: Learn & Master Cocos2D Game Development
url: http://www.learn-cocos2d.com/knowledge-base/cocos2d-iphone-faq/learn-cocos2d-public-content/manual/cocos2d-general/19515-how-to-fix-expected-a-type-error/
author: Max says
published: '2011-07-20'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[FAQ: cocos2d for iPhone](http://www.learn-cocos2d.com/knowledge-base/cocos2d-iphone-faq/learn-cocos2d-public-content/manual/cocos2d-general/): How to fix "Expected a type" Error

#### Search my cocos2d for iPhone FAQs & Tutorials

*Please note that the blog search in the upper right corner doesn’t search my FAQs and Tutorials.*

**Note:**please do not share direct download links to PDF files, the download links expire after a couple minutes!

This issue concerns the current stable version of cocos2d, which is v0.99.4. It may also affect other versions.

The problem only occurs if you try to build the cocos2d-iphone project for Simulator.

### Lots of "Expected something" compile errors

Building cocos2d v.0.99.4 for Simulator results in "expected a type" and "expected function body" and "unknown type name" errors.

### Build Settings: LLVM compiler 1.5

Right click the cocos2d-iphone project in the Groups and Files pane, and select Get Info.

In the Build Settings tab, the C/C++ Compiler Version setting will be set to use the LLVM compiler 1.5. That you don't want.

### Use LLVM GCC 4.2 instead

Change the compiler version to LLVM GCC 4.2 and you're good to go. No more compiler errors.

Enlightening post. Thanks!

And, of course, I have a few question


- everything is relative, but for common code is better to use NSString, NSArray (and pay the cost of creating new objects) or the mutable ones? Which can be the parameters to choose between each one?

- I am wondering if the new iPhone 4.0′s greater performance will be an issue. Games that run smoothly in iPhone 1st and 2nd generation devices will probably run too fast?

Hi Max,

i doubt the NSMutable* datasets are performance killers. I haven’t made any tests but i’m pretty sure that if you don’t change them at all they’ll probably perform just as good as the non-mutable ones. Now, once you *do* need to change the arrays or strings it’s good to have them mutable so that stuff is taken care for you behind the scenes. On the other hand, if you know that you’ll only be creating the items once but never re-order, remove or add others then use the non-mutable ones. For me it’s a matter of use case rather than performance.

Games won’t run faster on newer devices. cocos2d’s CCDirector makes sure of that. You do get better framerates of course but not faster gameplay. That holds true for all modern game engines.

Hi gaminghorror. Thanks for all the great info on your blog

Really finding this useful.

I wanted to ask about your parallax background code above - I am using this in a test project, but can’t seem to get the tiling to fit perfectly next to eachother. In other words, my sprite that I am tiling (which is 480, 320 in size) is tiling, but when the new sprite starts, there is a black gap about 25 pixels wide between the new and the old. Is there any way to elliminate this gap? I have tried searching the cocos2d forums etc, and found info on 2D projection turning off etc… but none of that has helped me so far… To try and illustrate what I am getting, this is what I get scrolling across the device screen (x’s are the sprite white space is the black gap I get):

xxxxxxxxxxxxxxx| |xxxxxxxxxxxxxxxx| |xxxxxxxxxxxxxxxxxx| |xxxxxxx

This seems to be a placement offset, are you sure the sprites are exactly 480 pixels apart each? Both also need to have the same anchorPoint. And if you change the scale of the sprites, the offset also needs to be adjusted appropriately.

You might want to test the placement with smaller sprites so that at least two of them fit entirely on the screen.

Hi GamingHorror, thanks so much for the reply

So this morning I woke up and had a clear mind - thought about it for a while- My sprite for the background is exactly 480×320 - i.e. screensize. The gap I was seeing kind of looked around 20-30 pixels between each repeated sprite. So I thought, hey, at 480, I am just being given a texture that is 512 in size right? So maybe its doing a full 512pixel texture. So I went back to photoshop, and increased my sprite width to 512 (as I wouldnt lose any performance anyway) and gave this a try, using your code:

CCSprite *background = [CCSprite spriteWithFile:@"tile1.png"

rect:CGRectMake(0,0, 480*50, 320)];

[self addChild:background];

[background setPosition:ccp(winSize.width/2,winSize.height/2)];

ccTexParams params = {GL_LINEAR,GL_LINEAR,GL_REPEAT,GL_REPEAT};

[background.texture setTexParameters:¶ms];

and this sorted it out! No more gaps. Thanks so much for the pointers too - I hadn’t thought about anchorPoints! Thanks again for the great blog. I am subscribed!

Ah yes, if you’re using GL_REPEAT then the image size must be a power of two. Eg 64×64 or 512×128

Awesome - that clears things up for me and makes perfect sense now. Thanks for confirming. My layered parallax scrolling is looking sweet now!

So another quick question… I guess it won’t be possible to use a spritesheet with GL_REPEAT? Especially the way you need to create a CGRect…

Currently I do other graphics from spritesheets like this:

CCSprite *projectile = [CCSprite spriteWithSpriteFrameName:@"missile.png"];

Which are loaded from my .plist / spritesheet. Not possible to assign the GL_REPEAT background like this?

Since GL_REPEAT is a texture parameter, it applies to the whole texture, so you’ll need to use a single image texture, and the size must be a power of 2, eg 128×16 or 256×256.

That also rules out the spritesheet use.

When using this technique it works well in the simulator, but on the device the texture is super-blocky and pixellated. I’m running this test on cocos2d 0.99.5.

Ive tried with both 256×256 and 512×512 textures, and the result is the same. Simulator repeats perfectly, device stretches and pixellates the texture horribly.

Do you have any idea why this happens?

Hmmm, not really. I’m guessing it might be related to Retina display, do you test on a retina device?

Yikes, I’m getting both errors, a black bar and the super pixelation. The blockyness increases the greater the value the width gets multiplied by, eg 50 in this line

_hills = [CCSprite spriteWithFile:@"Hills.png" rect:CGRectMake(0,0,240*50, 320)];

50 looks okay, 1000 is extremely distorted/pixelated. I test on a non-retina device, both iPod touch and iPad. Testing also done using simulator with same results.

Tried for both 480 wide content on 512 wide image and 512 wide content on 512 wide image.

Code snippet;

_sky = [CCSprite spriteWithFile:@"Clouds.png" rect:CGRectMake(0,0,512*100, 320)];

[self addChild:_sky z:-3];

_sky.position = ccp(0, size.height/2);

ccTexParams params = {GL_LINEAR,GL_LINEAR,GL_REPEAT,GL_REPEAT};

[_sky.texture setTexParameters:¶ms];

Same deal for adding in other backgrounds.

I’m used to procedural programming, in OOC what method would you recommend for the scrolling rather than a schedule callback every 0.05s (60 refreshes/second) that increments the BG positions by various mounts?

Thanks in advance, great info here!

Solved the gap! It was due to my sprite not being updated in xcode after modifying to comply with the 512 texture size. A clean build solved that. Beautifully satisfying to see this running!

Hello.

I have the same problem of distortion of the pixels on the sprite.

will create problems to show how you solved it !?!?!

thanks

I’m having some trouble with the code provided. I’m new to Cocos2D and when i copy and pasted your code into a project and changed file to the filename of the picture that I am using it gave me an error that said that background wasn’t declared. and then i changed it so that background was changed to CCSprite *background and then at the end I had to place [self addChild: background]; to get it to show up but it doesn’t scroll. Any ideas?