---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.1/Kobold2D/html/interface_k_k_app_delegate/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
Kobold2D
2.1
Kobold2D API Reference (iOS version) for www.kobold2d.com developers
|

`#import <KKAppDelegate.h>`


| (IBAction) | -
|

Performs common UIApplicationDelegate methods. You're supposed to subclass from it in your own project. Unless you need to react to any UIApplicationDelegate event, you only need to implement the initializationComplete method. Everything else is handled in this class. When subclassing and overriding UIApplicationDelegate methods you should also call the [super ..] implementation.

Called before the (root ViewController's) view is initialized. Override and return a UIView to use a different view for the root ViewController instead of the Director's glView. If you use an alternate view, you are responsible for adding the glView somewhere to the view hierarchy. Primarily used for integration with UIKit/AppKit views to change the view hierarchy from: window -> glView to window -> overarching view -> subviews (glView plus n UIKit/AppKit views).

Called when Cocos2D is initialized and the App is ready to run the first scene. You should override this method in your AppDelegate implementation.

- (CCDirectorMac*) director` [read, retain]` |

returns the Mac director

- (IBOutlet CCGLView*) glView` [read, write, assign]` |

The MacGLView

- (IBOutlet NSWindow*) window` [read, write, assign]` |

The App's NSWindow object