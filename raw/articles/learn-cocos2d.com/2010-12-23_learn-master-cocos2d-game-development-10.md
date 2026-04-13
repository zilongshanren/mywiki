---
title: Learn & Master Cocos2D Game Development
url: http://www.learn-cocos2d.com/knowledge-base/cocos2d-iphone-faq/learn-cocos2d-public-content/manual/cocos2d-general/13435-how-can-i-draw-a-simple-point-line-or-circle/
author: Max says
published: '2010-12-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[FAQ: cocos2d for iPhone](http://www.learn-cocos2d.com/knowledge-base/cocos2d-iphone-faq/learn-cocos2d-public-content/manual/cocos2d-general/): How can i draw a simple Point, Line or Circle?

#### Search my cocos2d for iPhone FAQs & Tutorials

*Please note that the blog search in the upper right corner doesn’t search my FAQs and Tutorials.*

**Note:**please do not share direct download links to PDF files, the download links expire after a couple minutes!

You can use cocos2d's simple OpenGL wrapper for this. All the functions you need are defined in CCDrawingPrimitives.h which also contains methods to draw polygons.

### Drawing a Point, Line and Circle

This is the code to draw a point, line and circle. Notice that the code is inside the -(void) draw method. The ccDraw* methods only work in the draw method of a CCNode (or a subclass of CCNode like CCLayer, CCSprite and so on). This CCNode must also be somewhere in the draw hierarchy, for example added to the CCScene as child.

The OpenGL draw methods are very useful for debugging, for example to display positions and anchorPoints of objects. The ccDrawCircle method can also render a line from its center outwards in a specific angle. This can be used to display the rotation of a CCNode. Note that angle is in radians whereas CCNode rotation is in degrees, so you have to convert it with the CC_DEGREES_TO_RADIANS(..) macro.

### Output

### Drawing thicker lines

Those 1-pixel wide lines may not be ideal. Try GL_MULTISAMPLE and glLineWidth commands to change the line styles. Put these commands before the actual ccDrawLine code.

With GL_MULTISAMPLE and glLineWidth(3) you get a nice line-drawing effect very similar to the one Harbor Master uses.

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