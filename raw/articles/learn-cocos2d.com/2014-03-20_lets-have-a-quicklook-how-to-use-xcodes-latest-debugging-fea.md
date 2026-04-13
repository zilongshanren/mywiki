---
title: 'Let’s have a QuickLook: how to use Xcode’s latest debugging feature'
url: http://www.learn-cocos2d.com/2014/03/quicklook-xcodes-latest-debugging-feature/
author: Jeremy says
published: '2014-03-20'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Xcode’s QuickLook debugging feature allows you to get more details, and be more visual with your debugging data.

For example you can even grab a screenshot of the cocos2d screen and display it right within Xcode:

### How QuickLook works


Apple’s got the [QuickLook documentation](https://developer.apple.com/library/mac/documentation/IDEs/Conceptual/CustomClassDisplay_in_QuickLook/CH01-quick_look_for_custom_objects/CH01-quick_look_for_custom_objects.html) for you.

Enabling QuickLook for a class requires merely adding a specific method to the class. This will also work if you add the class to a class category. For example to add QuickLook support to CCSprite you could add this category to your project:

|
1 2 3 4 5 6 7 8 9 10 |
@interface CCSprite (QuickLook) @end @implementation CCSprite (QuickLook) -(id) debugQuickLookObject { // just return the object's description string return [self description]; } @end |


### What QuickLook can do

QuickLook allows you to display more than just a string. It can also be an attributed string (with colors and all that stuff) or an image or a font. Apple has a [list of supported QuickLook types](https://developer.apple.com/library/mac/documentation/IDEs/Conceptual/CustomClassDisplay_in_QuickLook/CH02-std_objects_support/CH02-std_objects_support.html) that can be returned from the QuickLook method. They are:

- Image classes: NS/UIImage, NS/UIImageView, CIImage, NSBitmapImageRep
- Color classes: NS/UIColor
- View classes: NS/UIView
- Text classes: NSString, NSAttributedString
- Other classes: NSURL, NSCursor, NS/UIBezierPath, CLLocation

Note that some classes like UIView only work with Xcode 5.1 or later.

### How QuickLook feels like

Best demonstrated with a video:

You should change the video player settings to render the video in 1080p.

### Get the Cocos2D example

As usual on [github](https://github.com/LearnCocos2D/LearnCocos2D/tree/master/Cocos2D-QuickLookExample). This example uses cocos2d-iphone v3 RC2 (despite it saying “3.0.0-alpha” on launch).

### Full QuickLook support for Sprite Kit

Get [SpriteKit+QuickLook from github](https://github.com/KoboldKit/SpriteKit-QuickLook). It’s free under the MIT License. Just add the SpriteKit+QuickLook.h/.m files to your project and you’re ready to debug!

The SK QuickLook provides an in-depth view of a Sprite Kit object’s variables, sorted alphabetically and including hidden private variables. This comes in very handy!

I wrote this because debugging SK nodes used to annoy me to death - you couldn’t even get the most basic properties to display in the debugger (unless you right-click and do ‘Add Expression’). Now I get perhaps more than I need, but I find the extra information quite useful from time to time.

Since the QuickLook method doesn’t run unless a debugger is attached or you call it manually it should be safe to use even with distributed apps. Though this is merely my assumption, so you may prefer to remove the QuickLook category before submitting your app to the store.

Enjoy!

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Very cool, it will come in very handy for developing spritekit games. Appreciate it!