---
title: Static Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest/Kobold2D/html/interface_k_k_startup_config/
published: '2012-03-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <KKStartupConfig.h>`


| id |
|

This class contains all the config.lua settings at runtime. Each property corresponds to the correspondingly named config.lua parameter, with the exception that config.lua parameter have their first letter uppercased (this is a technical, Objective-C runtime issue). For example, the property gLViewColorFormat is the config.lua setting GLViewColorFormat.

| id KKStartupConfig::config | ( | ) | ` [static, virtual]` |

autorelease initializer

BOOL KKStartupConfig::acceptsMouseMovedEvents` [read, write, assign]` |

Enable this if you need to track simple mouse movement events in your app. Disabled by default because every move of the mouse generates a new event, which is wasteful if you don't respond to ccMouseMoved events.

int KKStartupConfig::adMobFirstAdDelay` [read, write, assign]` |

AdMob specific: set the time (in seconds) before the very first ad after starting the app should be displayed.

NSString * KKStartupConfig::adMobPublisherID` [read, write, copy]` |

AdMob specific: your AdMob publisher ID.

int KKStartupConfig::adMobRefreshRate` [read, write, assign]` |

AdMob specific: set the ad refresh rate. AdMob allows a refresh rate between 12 and 120 seconds.

BOOL KKStartupConfig::adMobTestMode` [read, write, assign]` |

AdMob specific: only display test ads to avoid requesting invalid impressions. This setting is ignored in Release (Archive) builds so that you don't accidentally publish an App with test mode enabled.

NSString * KKStartupConfig::adProviders` [read, write, copy]` |

Comma seperated list of ad providers, and their priority. Currently supports: iAd, AdMob.

Valid settings: "iAd, AdMob" - display iAd ad banners where available, and where iAd isn't available AdMob banners are used "iAd" - display only iAd ad banners where available, none otherwise "AdMob" - display only AdMob ad banners "AdMob, iAd" - same as "AdMob" because AdMob is supported on all devices with iOS 3, whereas iAd is only available on iOS 4.

BOOL KKStartupConfig::allowAutorotateOnFirstAndSecondGenerationDevices` [read, write, assign]` |

Allows you to explicitly disable autorotation on 1st and 2nd generation iOS devices (iPhone, iPhone 3G, iPod touch 1st & 2nd generation). Ignored if the autorotationType is set to Autorotation.None.

int KKStartupConfig::autorotationType` [read, write, assign]` |

Determines how (or if) autorotation is implemented for your app. This setting is ignored on Mac OS.

Valid config.lua values for this setting are:

The None setting will never rotate your app's device orientation. The CCDirector setting makes the CCDirector responsible for rotating the OpenGL view but it will not autorotate UIKit Views. The UIViewController setting allows both UIKit views and the OpenGL view to be autorotated and provides a rotation animation. But it comes with a performance penalty on 1st and 2nd generation iOS Devices. For that reason you can explicitly disable autorotation on those devices via the allowAutorotateOnFirstAndSecondGenerationDevices setting.

BOOL KKStartupConfig::autoScale` [read, write, assign]` |

Mac OS only. Allows the OpenGL view in the app window to be scaled automatically when the window size changes. If you disable this you should also disallow resizing of the window by the user.

int KKStartupConfig::defaultTexturePixelFormat` [read, write, assign]` |

Specifies the pixel format for all textures. By default all textures are 24-bit with 8-bit alpha but if you reduce the color bit depth of your textures and don't need an alpha channel you can preserve half the texture memory. The TexturePacker tool [http://www.texturepacker.com](http://www.texturepacker.com/) will help you with this.

Valid config.lua values for this setting are:

The Automatic mode defaults to RGBA8888 which is the default texture pixel format (24-bit colors, 8-bit alpha). Compatible and using half the memory is RGBA4444 which has 12-bit colors and 4-bit alpha, and obviously reduced image quality. A better alternative would be RGB565 which gives you 16-bit colors but no alpha, or RGB5A1 which gives you 15-bit colors and at least 1-bit alpha. This means your images can have "see-through" parts but each pixel can be either completely translucent or completely opaque. This is good enough for sprite masks. The pixel format A8 is used by particle effects by default, it provides 256 colors (8-bit). Useful for single-color textures when you really need to preserve memory and faster performance than 16-bit or 32-bit textures.

int KKStartupConfig::deviceOrientation` [read, write, assign]` |

Sets the device orientation that your game should start in.

Valid config.lua values for this setting are:

The opposing orientations determine where the home button will be:

int KKStartupConfig::directorType` [read, write, assign]` |

Sets the type of director to use for your iOS game. This setting is ignored on Mac OS. The director type affects how the game update loop is run, and can affect the game's overall performance and impose technical limitations.

Valid config.lua values for this setting are:

The DisplayLink director type is the default and recommended. If your app targets iOS 3.1 or higher you should only use the DisplayLink director type. The NSTimer director type is quite slow, it may not even achieve 60 fps without rendering anything. But it is the most compatible and would still work on iOS 2.x. The MainLoop directors are aggressive versions of the timer director, pushing the framerate up but they don't cooperate with UIKit views since they consume all available CPU time. The ThreadMainLoop director may be a bit better in that regard. But overall you should avoid the MainLoop director types.

int KKStartupConfig::directorTypeFallback` [read, write, assign]` |

Just in case the directorType is set to DirectorType.DisplayLink you can specify an alternate, fallback director type for devices running iOS 3.0 or older. Usually this is set to DirectorType.NSTimer which will result in sub-par performance for devices running iOS 3.0 or older. It is recommended to simply target iOS 3.1 as your deployment target instead.

Valid config.lua values for this setting are:

See also the directorType property.

BOOL KKStartupConfig::displayFPS` [read, write, assign]` |

Enables the FPS counter in the lower left corner of the screen. Keep in mind that the FPS for iOS apps running in the iOS Simulator is not indicative of real performance on the device (it could be ten times that, or one tenth). Also logging and an attached debugger (running from within Xcode) can negatively affect performance.

Important: when enabling this setting you must have the file fps_images.png in your project's resources. Otherwise your app will report an error on startup.

To change how often the FPS counter is updated, open the ccConfig.h file (of Cocos2D) and look for the macro CC_DIRECTOR_FPS_INTERVAL.

Note: be sure to turn this setting off when publishing your app to the App Store!

BOOL KKStartupConfig::enable2DProjection` [read, write, assign]` |

Changes the OpenGL view to 2D projection mode. This is commonly only used when working with tilemaps, or when you want to fine-tune the Z-order of nodes via the vertexZ property. That allows you to override Cocos2D's z-ordering (addChild:z: and reorderChild:z:).

BOOL KKStartupConfig::enableAdBanner` [read, write, assign]` |

BOOL KKStartupConfig::enableFullScreen` [read, write, assign]` |

Enable fullscreen rendering in Mac apps.

BOOL KKStartupConfig::enableGLViewNodeHitTesting` [read, write, assign]` |

If YES (default: NO) will test each touch began (iOS) or mouse click (Mac OS) location if it "hit" a CCNode in the scene hierarchy. It calls [node containsPoint:location] for each node in the scene hierarchy. If a node is "hit", then the touch/click is processed by the Cocos2D OpenGL view. Otherwise it is passed on to underlying views.

This setting is only needed if you want to have UIView/NSView both in the foreground and in the background of the Cocos2D OpenGL view, and both foreground (Cocos2D and/or UIKit/AppKit foreground views) and background views should process user input. Normally the Cocos2D view will not pass touches/clicks to underlying views since it spans the entire screen/window.

BOOL KKStartupConfig::enableMultiTouch` [read, write, assign]` |

Allow the app to process multi-touch events. If disabled, app will only receive single touch events. Ignored on Mac OS.

BOOL KKStartupConfig::enableRetinaDisplaySupport` [read, write, assign]` |

Allows your app to use Retina graphics (file suffix "-hd") for assets like images, tilemaps, particle effects, and so on.

Note: if you enable Retina support but do not provide HD graphics your app will be rendered on Retina devices in the lower, left quarter of the screen as a tiny version of the app. If you can't provide HD images there's no point in enabling Retina support.

BOOL KKStartupConfig::enableStatusBar` [read, write, assign]` |

Allows you to enable or disable (hide) the iPhone Statusbar (the top bar that displays the current time, battery lifetime, etc). Has no effect when building for Mac.

Note: if the statusbar is enabled the Cocos2D OpenGL view will still be fullscreen. It is up to you to ensure that essential objects are not (partially) obstructed by the Statusbar.

BOOL KKStartupConfig::enableUserInteraction` [read, write, assign]` |

Enables user interaction for the entire app. If disabled, the app will not receive touches, accelerometer, keyboard, etc events from the user. Ignored on Mac OS.

NSString * KKStartupConfig::firstSceneClassName` [read, write, copy]` |

You can tell Kobold2D which CCScene or CCLayer derived class should be the first scene loaded by the CCDirector runWithScene method. This must be the name of the class as a string (in double quotes), and not the name of the file(s) the class is defined in.

Example usage in config.lua:

int KKStartupConfig::gLViewColorFormat` [read, write, assign]` |

The color format of the OpenGL View.

Valid config.lua values for this setting are:

RGBA8888 is 32-bit with alpha channel, RGB565 is 16-bit with no alpha channel. RGB565 is the default because it is faster and sufficient for most uses. RGBA8888 provides the best visual quality in particular for images with gradients, and it allows the OpenGL view itself to be transparent which is required if you want to have UIKit views in the background (behind the Cocos2D view).

int KKStartupConfig::gLViewDepthFormat` [read, write, assign]` |

The depth (z-buffering) format of the OpenGL View.

Valid config.lua values for this setting are:

Depth buffering is normally not needed and reduces rendering performance, so the default value is DepthNone (equals 0). Depth16Bit and Depth24Bit set the depth (Z) buffer to 16-bit respectively 24-bit (more accurate, higher memory usage). If you want to use Cocos3D, 3D or Grid Actions (eg PageTurn3D), or isometric tilemaps (and in some cases orthogonal tilemaps) you should enable depth buffering. Prefer to use a 16-bit buffer unless you see artifacts, in that case a 24-bit buffer may help.

BOOL KKStartupConfig::gLViewMultiSampling` [read, write, assign]` |

Enable multisampling (anti-aliasing) for edge removal. On older iOS devices multisampling can noticeably reduce rendering performance. See also: [http://en.wikipedia.org/wiki/Multisample_anti-aliasing](https://en.wikipedia.org/wiki/Multisample_anti-aliasing)

For Mac OS computers consider allowing the user to change this setting as the performance and visual quality greatly depends on the graphics card and screen resolution.

int KKStartupConfig::gLViewNumberOfSamples` [read, write, assign]` |

If multisampling is enabled, sets the number of samples. On iOS devices valid values are 1, 2 and 4. On Mac OS this depends on the graphics card and you may be able to use 8 or 16 as well.

BOOL KKStartupConfig::loadOnlyLandscapeBanners` [read, write, assign]` |

iAd specific: can be used to reduce Internet traffic. If your app only ever uses or rotates to Landscape orientations, set this property to YES.

BOOL KKStartupConfig::loadOnlyPortraitBanners` [read, write, assign]` |

iAd specific: can be used to reduce Internet traffic. If your app only ever uses or rotates to Portrait orientations, set this property to YES.

int KKStartupConfig::maxFrameRate` [read, write, assign]` |

Sets the maximum framerate of your game. Defaults to 60.

On iOS Devices the maximum framerate is limited to 60 frames per second by the display hardware. On Mac OS you may be able to go higher but at little benefit, 60 fps is already very, very smooth.

Note that this setting can not magically increase your framerate. But you can intentionally limit your app's framerate to a lower framerate, in particular if your app is experiencing a highly fluctuating framerate. If you see the framerate counter jump between 40 to 60 fps it can be helpful to limit the framerate to 40 fps since a steady framerate is very important, in particular for some games. You also reduce the number of times your game is updated, which in turn may even result in a slightly better performance.

Note that on iOS with the DirectorType.DisplayLink you can only expect to get a framerate of 60, 30 (60 divided by 2), 20 (60 divided by 3), 15 (60 divided by 4), 12 (60 divided by 5), and so on. The DisplayLink director links the update rate to the screen refresh rate. If the update takes just tiny bit longer than 16.666 milliseconds the DisplayLink director will have to skip this frame and will only refresh the screen after 33.333 milliseconds. That's why it can be very important for DisplayLink director to limit the framerate to 30 fps if your app frequently drops below 60 fps. You'll get a stable framerate and twice the CPU time per frame.

BOOL KKStartupConfig::placeBannerOnBottom` [read, write, assign]` |

Allows you to move the ad banner from its default top position to the bottom of the screen.

BOOL KKStartupConfig::shouldAutorotateToLandscapeOrientations` [read, write, assign]` |

Allows you to explicitly restrict autorotation to landscape orientations. This is useful if your app does not provide alternate views and would simply be displayed incorrectly when not in landscape orientation.

BOOL KKStartupConfig::shouldAutorotateToPortraitOrientations` [read, write, assign]` |

Allows you to explicitly restrict autorotation to portrait orientations. This is useful if your app does not provide alternate views and would simply be displayed incorrectly when not in portrait orientation.