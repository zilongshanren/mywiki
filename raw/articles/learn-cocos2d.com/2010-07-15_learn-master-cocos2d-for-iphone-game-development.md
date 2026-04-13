---
title: Learn & Master cocos2d for iPhone Game Development
url: http://www.learn-cocos2d.com/knowledge-base/cocos2d-iphone-faq/learn-cocos2d-public-content/manual/cocos2d-general/13432-how-to-determine-the-distance-between-two-ccnodes/
author: Max says
published: '2010-07-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[FAQ: cocos2d for iPhone](http://www.learn-cocos2d.com/knowledge-base/cocos2d-iphone-faq/learn-cocos2d-public-content/manual/cocos2d-general/): How to determine the distance between two CCNodes?

#### Search my cocos2d for iPhone FAQs & Tutorials

*Please note that the blog search in the upper right corner doesn’t search my FAQs and Tutorials.*

**Note:**please do not share direct download links to PDF files, the download links expire after a couple minutes!

We'll use Chipmunk to calculate the distance between two CCNodes, or two points for that matter.

### Import CGPointExtension.h

In case you aren't using Chipmunk physics import the file "CGPointExtension.h" at the top of the .m file in which you want to calculate the distance of two points. If you are using Chipmunk physics you don't have to add this line but it won't hurt either.

### Calculate the distance

Use the ccpDistance method to calculate the distance between two objects by using their position properties.

Enlightening post. Thanks!

And, of course, I have a few question


- everything is relative, but for common code is better to use NSString, NSArray (and pay the cost of creating new objects) or the mutable ones? Which can be the parameters to choose between each one?

- I am wondering if the new iPhone 4.0′s greater performance will be an issue. Games that run smoothly in iPhone 1st and 2nd generation devices will probably run too fast?

Hi Max,

i doubt the NSMutable* datasets are performance killers. I haven’t made any tests but i’m pretty sure that if you don’t change them at all they’ll probably perform just as good as the non-mutable ones. Now, once you *do* need to change the arrays or strings it’s good to have them mutable so that stuff is taken care for you behind the scenes. On the other hand, if you know that you’ll only be creating the items once but never re-order, remove or add others then use the non-mutable ones. For me it’s a matter of use case rather than performance.

Games won’t run faster on newer devices. cocos2d’s CCDirector makes sure of that. You do get better framerates of course but not faster gameplay. That holds true for all modern game engines.