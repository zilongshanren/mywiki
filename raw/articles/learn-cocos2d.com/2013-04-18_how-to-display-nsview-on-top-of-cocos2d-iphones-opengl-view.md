---
title: How to display NSView on top of cocos2d-iphone’s OpenGL view on Mac OS X
url: http://www.learn-cocos2d.com/2013/04/display-nsview-top-cocos2d-iphone-opengl-view-mac/
author: Mathew Says
published: '2013-04-18'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Everyone knows how to add a UIView to an iOS app built with cocos2d-iphone. It’s straightforward, just create the view and then call:

|
1 |
[[CCDirector sharedDirector].view addSubview:theView]; |


There. Now suppose you want to do the same on Mac OS X. **HA! HA! Hawww!**

Cocoa’s laughing at your feeble attempts. It’s really just Cocoa’s fault though. Having done a fair amount of work with both SDKs, the Cocoa on OS X just feels … old. Backwards. Confuscated. No, not confusing, literally confuscated - it can’t even spell confusing like everyone else does.

But … there is always a way. On OS X it’s just more often than on iOS a matter of finding the right way. It can be done. Here’s proof:

### The Right Way™

The trick here is to create an additional “overlay” NSWindow that’ll hold all of your views. Actually, it’s not the overlay window it’s the overlay window’s content view, which is just an empty NSView. But first things first, step by step.


#### App Delegate Additions

Let’s check the cocos2d-iphone Mac app’s modified AppDelegate interface:

|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 |
// add the NSWindowDelegate protocol @interface OverlayAppDelegate : NSObject <NSWindowDelegate,NSApplicationDelegate> { @private // add the _overlayWindow ivar NSWindow* _overlayWindow; } // add the overlayWindow property @property (nonatomic, readonly) IBOutlet NSWindow* overlayWindow; @property (nonatomic) IBOutlet NSWindow *window; @property (nonatomic) IBOutlet CCGLView *glView; - (IBAction)toggleFullScreen:(id)sender; @end |


The app delegate now also implements the NSWindowDelegate protocol. We’ll need this later to intercept the **windowWillClose:** message. Other than renaming the app delegate, cleaning it up a bit (this project uses ARC) and of course adding the overlay window ivar and property, it’s a vanilla app delegate.

The app delegate implementation overrides the overlayWindow accessor (getter) method, which will create the overlay window on first access and return it:

|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 |
// add the overridden overlayWindow accessor (getter) method -(NSWindow*) overlayWindow { // if the overlay doesn't exist yet, create it if (_overlayWindow == nil) { _overlayWindow = [[NSWindow alloc] initWithContentRect:_window.frame styleMask:NSBorderlessWindowMask backing:NSBackingStoreBuffered defer:NO]; // make sure the window is "see-through" and has no shadow [_overlayWindow setBackgroundColor:[NSColor clearColor]]; [_overlayWindow setOpaque:NO]; [_overlayWindow setHasShadow:NO]; // contentView is just an empty NSView spanning the entire window NSView* contentView = [[NSView alloc] initWithFrame:_window.frame]; [_overlayWindow setContentView:contentView]; // add the overlay window as child window and // make AppDelegate (self) the window's NSWindowDelegate object [_window addChildWindow:_overlayWindow ordered:NSWindowAbove]; _window.delegate = self; } return _overlayWindow; } |


The NSWindow is created borderless, set to be see-through by setting the clearColor and turning off opaque-ness. The shadow is disabled not because it would otherwise be visible (it wasn’t in my tests) but rather because it doesn’t need to be drawn, so why draw it, right?

The contentView is an empty NSView object that just spans the entire window. The window’s contentView is where you’ll add all of your NSView subviews.

Of course the overlay window needs to be a child of something, and that something would be the regular (main) window. The main window’s delegate is set to the app delegate (remember: it now implements the NSWindowDelegate protocol) so that it will receive the windowWillClose message.

#### Could you please close the window?

Which brings me to the aforementioned:

|
1 2 3 4 5 6 7 8 9 10 11 12 13 |
// add the windowWillClose message of NSWindowDelegate protocol -(void) windowWillClose:(NSNotification*)notification { // check if it's the main window that's being closed if ([notification object] == _window) { // if so, close the overlay window to prevent the app from "hanging" [_overlayWindow close]; // in addition, it is a good idea to stop director here [[CCDirector sharedDirector] stopAnimation]; } } |


The windowWillClose message is sent to a window’s NSWindowDelegate object, which in this case is the app delegate. The notification object returns the NSWindow that is being closed. Although there can be only one window receiving this message, it can’t hurt to verify that it’s the main window being closed. If so, it will also send the close message to the overlay window.

Closing the overlay window is important because by default, cocos2d’s Mac app delegate implements this message:

|
1 2 3 4 |
-(BOOL) applicationShouldTerminateAfterLastWindowClosed:(NSApplication*)theApp { return YES; } |


Meaning the app should close when the **last** window closes. But now we have more than one window in our application, so when the user clicks the red x on the main window, we now must close the overlay window manually to allow the application to quit. Not closing the overlay window would cause the app to keep running without a visible window, seemingly in the background, with no obvious way for the user to shut it down.

Next I’m also calling stopAnimation in this method. This fixes a long-standing bug in the Mac version of cocos2d-iphone where, upon shutdown, a great number of OpenGL errors are logged to the Console. In some cases I hear this may even cause crashes. To prevent these issues, it’s a good idea to stop cocos2d from “animating” (ie not updating scheduled methods, not rendering) when the main window is about to close.

#### Adding the NSMeat

Now let’s turn our attention to actually adding NSView objects. In the example project open the HelloWorldLayer and #import the “AppDelegate.h” file so we can access the overlay window. I also added a NSButton* button ivar to the header. Both not shown, I expect you know how to do this.

Somewhere in this cocos2d+Box2D HelloWorldLayer implementation is a Reset button, so why not replace the existing CCMenu with a NSButton?

|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 |
-(void) createResetButton { // Create the reset NSButton... (button is an ivar) button = [[NSButton alloc] initWithFrame:CGRectMake(330, 120, 200, 60)]; [button setButtonType:NSMomentaryLightButton]; [button setBezelStyle:NSSmallSquareBezelStyle]; [button setToolTip:@"This is a NSButton, duh!"]; [button setTitle:@"Reset Physics"]; [button setTarget:self]; [button setAction:@selector(resetButtonPressed)]; [button setFont:[NSFont fontWithName:@"Comic Sans MS" size:24]]; [OverlayAppDelegate addSubview:button]; // adding the other NSView objects omitted for brevity ... } |


The button is created programmatically in this case. If you wanted to, you could also create a view from XIB/NIB. I’ll get to the ominous addSubview method soon, first here’s the selector the button runs when it’s being pressed:

|
1 2 3 4 5 6 7 8 9 10 11 12 13 |
-(void) resetButtonPressed { // avoid potential crash by clicking the button repeatedly [button setTarget:nil]; [OverlayAppDelegate removeAllSubviews]; // create the new scene CCScene* scene = [CCScene node]; id child = [HelloWorldLayer node]; [scene addChild:child]; [[CCDirector sharedDirector] replaceScene:scene]; } |


Since clicking the button will ultimately cause the scene to change, you have to remove all of the NSView objects you may have added to this point.

First of all, cocos2d has no idea whatsoever about the overlay window and any views you add to it. Just like in iOS, cleaning up the NSView objects when changing a scene is your responsibility. And of course NSView objects completely ignore any transitions you run when changing a scene. Therefore your best option is to simply remove the views before changing scenes.

In this specific instance, remember that the button’s action target is the current HelloWorldLayer instance. You not only have to remove the button, you’ll also have to set its target to nil to avoid the soon-to-be-released delegate to receive more action messages if the user clicks the button frantically. And as you probably know, sending a message to a released instance is bad news.

#### Adding & Removing NSView subviews

Going back to the app delegate, I neglected to mention these class methods from the @interface:

|
1 2 3 |
+(NSView*) overlayWindowContentView; +(void) addSubview:(NSView*)view; +(void) removeAllSubviews; |


These helper methods make it easy for you to add and remove subviews. I leave it up to you to extend this with another helper method that removes a specific view. Homework assignment! [You will be judged on your choice of fonts!](http://www.funnyordie.com/videos/d2e0f617e3/isteve)

Hint: Comic Sans will get you an F.


Anyhow … here’s what these methods do:

|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 |
+(NSView*) overlayWindowContentView { OverlayAppDelegate* appDelegate = (OverlayAppDelegate*)[NSApplication sharedApplication].delegate; return appDelegate.overlayWindow.contentView; } +(void) addSubview:(NSView *)view { [[self overlayWindowContentView] addSubview:view]; } +(void) removeAllSubviews { // This code removes the subviews from last to first. NSArray* subviews = [self overlayWindowContentView].subviews; for (NSView* view in [subviews reverseObjectEnumerator]) { [view removeFromSuperview]; } } |


The overlayWindowContentView accessor mainly takes out the gruntwork of casting the app delegate and typing appDelegate.overlayWindow.contentView repeatedly. This is a task helper methods were born for!

Removing all subviews does so by enumerating the subviews array backwards. Because you can’t modify an array during enumeration - the only item allowed to be removed during enumeration is the array’s last item. Therefore iterating backwards here will always remove the last item from its superview (and therefore modifying the subviews array) until the subviews array is empty.

You can surely use this enumeration trick in other places too, especially if you need to remove items one-by-one until the array is empty.

### Any last words?

Sure. [Grab the code from github](https://github.com/LearnCocos2D/LearnCocos2D/tree/master/Cocos2D-NSViewOnCocos2DView) and ar*gghnnn….*


Oh wait. There’s something else I wanted to show you. In case you may be wondering why on earth I was doing this NSView-on-Cocos2D stuff to begin with…

Since [KoboldTouch](http://www.koboldtouch.com/x/64Bq) implements the model-view-controller (MVC) architecture you’re free to choose any kind of view for a specific model. And having a physics body model means **you can animate any view with physics!** So I was thinking it would be a great show-off to have a UIView/NSView animated by physics.

But getting NSViews to display was not straightforward, and clues where spread thin and far apart, hence this tutorial.

In the demo video below you’ll find that next to a sprite, a label, a particle effect and a PhysicsEditor-created shape there’s also a UIButton hopping around. Imagine the possibilities!


|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

[box2d](http://www.learn-cocos2d.com/tag/box2d/)•

[CCDirector](http://www.learn-cocos2d.com/tag/ccdirector/)•

[cocoa](http://www.learn-cocos2d.com/tag/cocoa/)•

[cocos2d](http://www.learn-cocos2d.com/tag/cocos2d/)•

[cocos2d-iphone](http://www.learn-cocos2d.com/tag/cocos2d-iphone/)•

[content view](http://www.learn-cocos2d.com/tag/content-view/)•

[KoboldTouch](http://www.learn-cocos2d.com/tag/koboldtouch/)•

[mac os x](http://www.learn-cocos2d.com/tag/mac-os-x/)•

[nsview](http://www.learn-cocos2d.com/tag/nsview/)•

[overlay window](http://www.learn-cocos2d.com/tag/overlay-window/)•

[uiview](http://www.learn-cocos2d.com/tag/uiview/)

thanks a lot!!