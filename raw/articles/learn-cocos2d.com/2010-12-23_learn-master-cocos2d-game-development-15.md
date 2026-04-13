---
title: Learn & Master Cocos2D Game Development
url: http://www.learn-cocos2d.com/knowledge-base/cocos2d-iphone-faq/learn-cocos2d-public-content/manual/cocos2d-general/14813-how-to-get-a-sprites-bounding-box-bounding-rectangle-with-code/
author: Max says
published: '2010-12-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[FAQ: cocos2d for iPhone](http://www.learn-cocos2d.com/knowledge-base/cocos2d-iphone-faq/learn-cocos2d-public-content/manual/cocos2d-general/): How to get a Sprite's Bounding Box / Bounding Rectangle? (with Code)

#### Search my cocos2d for iPhone FAQs & Tutorials

*Please note that the blog search in the upper right corner doesn’t search my FAQs and Tutorials.*

**Note:**please do not share direct download links to PDF files, the download links expire after a couple minutes!

cocos2d does not have a method that returns a Sprite's bounding box or bounding rectangle. You can easily create a CGRect by using the sprite's contentsize. But what if the anchorpoint isn't at the center, or the sprite is scaled? We'll write a CCSpriteExtension category which will cover that.

### NOTE: use CCNode's boundingBox method instead

When i wrote this i wasn't aware that CCNode has a **-(CGRect) boundingBox** method. I leave this approach here because it illustrates how to extend cocos2d with useful methods by using Objective-C categories.

### CCSpriteExtension category

Create a new Objective-C class with both .h and .m files and name the class CCSpriteExtension.

### CCSpriteExtension Interface

The header file will be a bit different than regular headers because we only define an Objective-C category. An Objective-C category allows you to add methods (but not member variables) to an existing class. It's a great way to extend on code and API of others such as the cocos2d engine, without having to change their source code.

Notice that i named the @interface CCSprite exactly like the cocos2d class. But it is followed by a keyword in brackets. These are for naming the category and you are free to name them any way you want. Without the brackets you would see compile error complaining about a second definition of the class CCSprite. I decided i just call it "extensions".

Since a category can not add member variables to an existing class make sure there are no opening and closing curly brackets. We can only define new methods and the only one we add is -(CGRect) getBoundingRect;

### CCSpriteExtension Implementation

The @implementation is also followed by the brackets with the name of the category and is also called CCSprite.

We only need to implement this one method. First of all we get the sprite's contentSize which is the width and height of the sprite's texture. Since the sprite can be scaled and that would change it's bounding rectangle we have to account for that by multiplying width and height with scaleX_ and scaleY_ respectively. We end up with size being the scaled size of the sprite.

So far so good but we also need to take into account that the anchorPoint might not be at the center of the sprite and thus the center of the rectangle. You might have seen the same code but simply dividing size by two in [Ray Wenderlich's simple iPhone Game with cocos2d Tutorial](http://www.raywenderlich.com/352/how-to-make-a-simple-iphone-game-with-cocos2d-tutorial) - for the sake of simplicity this works just as well:

**CGRect targetRect = CGRectMake(**** target.position.x - target.contentSize.width / 2, **** target.position.y - target.contentSize.height / 2, **** target.contentSize.width, **** target.contentSize.height);**

But it assumes that the anchorPoint is at the center of the sprite. This may not always be the case. To correct for this we simply multiply width and height with anchorPoint_.x and anchorPoint_.y respectively, instead of assuming that the anchorPoint's values are 0.5f. Remember math? Multiplying by 0.5 is the same as dividing by 2.

### Download CCSpriteExtension

### Use Case

Assuming we have a rectangle which we want to test for any intersecting sprites, we go through the list of sprites and call [sprite getBoundingRect] on them. This will give us the bounding rectangle of the sprite at the sprite's location, scaled to the sprites scaling factor and offset according to the anchorPoint. We can then use CGRectIntersectsRect to test if the Rectangles intersect (eg they are colliding).

### One caveat: does not support rotated Rectangles!

This code does not take rotation into account. As soon as the sprite is rotated, testing for a bounding box collision becomes a lot more complex.

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