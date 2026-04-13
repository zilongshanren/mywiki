---
title: Cocos2D Embedded In A Cocoa Touch App
url: http://www.learn-cocos2d.com/2011/06/cocos2d-embedded-cocoa-touch-app/
author: Jeffus says
published: '2011-06-12'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I just completed this project for the [new book chapter](http://www.learn-cocos2d.com/2011/05/cocos2d-touch-cocoa/) about embedding UIKit views/Cocoa Touch in a Cocos2D application. In that case I embedded the Cocos2D view in the View-based Application template and added some controls to start/stop the cocos2d view and change scenes. Here’s the result:

It also correctly auto-rotates. But I noticed an odd bug with auto-rotation enabled for all orientations: the view is designed in portrait mode. If I start the App on my iPod Touch 4 while holding the device in landscape mode, then rotate back to portrait mode once the app has started and enable the cocos2d view, for some reason this causes my device to reboot! I see a transparent white color drawn over the entire screen before the screen goes black and the Apple logo appears.

If anyone has any idea what might be causing this behavior, please let me know. As far as I debugged it is not the initialization of the EAGLView class itself, a scene is already running or about to be run.

I’m guessing it might have to do with the EAGLView initialization, since I rely on Interface Builder to initialize the view. I simply dragged a View object onto IB and changed the class from UIView to EAGLView. Maybe the EAGLView default settings are not supposed to be used and I do need to create the EAGLView manually?

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Hi Steffen, that looks interesting. Love your first book, it’s taught me so much already! Especially about subclassing and components. I can’t wait for your next installment. Keep up the good work, you are very much appreciated by the community!

If it wasn’t for your invaluable contribution, my App might never have got started, now I have a stream of ideas!

Thanks Jeff, UK

I’m wondering if your auto-rotation bug has something to do with Cocos2D requiring just portrait or landscape mode. Maybe test auto rotation with only both portrait modes?

Correct me if I’m wrong about Cocos2D requiring one of the rotation modes. (landscape or portrait.) I will also be testing this out tonight. Thanks for showing that using Cocoa + Cocos2D is possible. (excited about this)

If you’re using the UIViewController for autorotation Cocos2D defaults to portrait orientation. The comment seems to indicate that this is required, but it isn’t. I couldn’t find anything in regards to the startup device orientation in Apple’s documentation either.

The crash doesn’t happen if I restrict the orientation to either both landscape or portrait modes if I remember correctly.

Can you share the tutorial of embeded cocos2d in cocoa touch. i really want to know

There will be a chapter on UIKit integration in the second edition of Learn Cocos2D. I’ll be adding two template projects to Kobold2D soon. They’ll illustrate how to add UIKit views to a cocos2d app, and how to add a cocos2d view to a UIKit app.

Where can I download the template projects for Kobold2D? Are they already online?

You can download Kobold2D here: http://www.kobold2d.com