---
title: 'The Ultimate Cocos2D Project: Startup'
url: http://www.learn-cocos2d.com/2011/03/ultimate-cocos2d-project-startup/
author: Andrew says
published: '2011-03-12'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Put simply: [Kobold2D](http://www.kobold2d.com/) is designed to make Cocos2D developers more productive.

#### Original Post

Time for a weekly update. This time about startup code and configuration. One of the things that I frequently encountered following the development of Cocos2D and working with it, is how any change to the startup code - the main function, the App delegate and the root ViewController - caused issues and headscratching among developers.

I decided it doesn’t need to be this way.

### The main() function

A code snippets speaks more than words:

[cc lang=”ObjC”]

int main(int argc, char *argv[])

{

return KKMain(argc, argv, NULL);

}

[/cc]

That’s right, all of the startup code is now part of the project’s source code. You can still do whatever you need to do before and after the call to KKMain (probably nothing, except maybe anti-piracy code). And the third parameter (NULL) to KKMain is reserved for future use, to pass in any configuration parameters if the need arises.

Let’s see what KKMain does:

[cc lang=”ObjC” height=”650″]

int KKMain(int argc, char* argv[], SMainParameters* userParameters)

{

SMainParameters parameters;

initMainParameters(¶meters, userParameters);

#ifdef __IPHONE_OS_VERSION_MAX_ALLOWED

NSAutoreleasePool* pool = [[NSAutoreleasePool alloc] init];

#else

// Mac OS X specific startup code

[MacGLView load_];

#endif

// This makes the CCDirector class known to wax:

[CCDirector class];

// wax setup is sufficient for all intents and purposes

wax_setup();

[KKLua doString:kLuaInitScript];

[KKLua doString:kLuaInitScriptPlatformSpecific];

[KKLua doString:kLuaInitScriptForWax];

// This loads the config.lua file

[KKConfig loadConfigLua];

// run the app with the provided general-purpose AppDelegate which handles a lot of tedious stuff for you

#ifdef __IPHONE_OS_VERSION_MAX_ALLOWED

int retVal = UIApplicationMain(argc, argv, nil, parameters.appDelegateClassName);

[pool release];

#else

int retVal = NSApplicationMain(argc, (const char**)argv);

#endif

return retVal;

}

[/cc]

The usual, really, except that it also initializes Wax and thus Lua for your App as well as providing the necessary startup code for both supported platforms: iOS and Mac OS X. The KKLua class is an Objective-C wrapper around the most imortant Lua functions, most notably it has the **doString** and **doFile** methods which allow you to run any Lua code or file containing Lua code.

KKConfig is a class that loads a Lua table and stores it in a NSDictionary for fast access to Lua parameters at runtime. I’ll discuss it in detail another time. The main purpose of KKConfig is to **loadConfigLua**, which loads the config.lua script returning a table containing startup parameters and making those parameters available to Objective-C.

### Config.lua in detail

Let’s have a quick look at an excerpt of the config.lua file. It contains all of the startup parameters a developer using Cocos2D would ever want to tweak in a conveniently editable Lua script:

[cc lang=”Lua” height=”400″]

local config =

{

KKStartupConfig =

{

— load first scene from a class with this name, or from a Lua script with this name with .lua appended

FirstSceneClassName = “GameScene”,

— set the director type, and the fallback in case the first isn’t available

DirectorType = DirectorType.DisplayLink,

DirectorTypeFallback = DirectorType.NSTimer,

MaxFrameRate = 60,

DisplayFPS = YES,

DisplayFPSInAdHocBuilds = NO,

— Render settings

DefaultTexturePixelFormat = TexturePixelFormat.RGB565,

GLViewColorFormat = GLViewColorFormat.RGB565,

GLViewDepthFormat = GLViewDepthFormat.DepthNone,

GLViewPreserveBackBuffer = NO,

GLViewMultiSampling = NO,

GLViewNumberOfSamples = 0,

Enable2DProjection = NO,

EnableRetinaDisplaySupport = YES,

— … and many more settings!

},

}

return config

[/cc]

Since you don’t want to guess what those settings mean, I’ve documented them for you:

This should also illustrate the kind of documentation I’m striving for. Documentation will be available online. It’s created in a [Confluence Wiki](http://www.atlassian.com/software/confluence/) with the help of [ScreenSteps](http://www.bluemangolearning.com/screensteps/) for more visual, step-by-step documentation.

### App Delegate & Root ViewController

You may be wondering how you can modify and tweak the App Delegate and Root ViewController if they’re both part of the distribution, rather than copied into each project? That’s actually very simple: both are regular Objective-C classes, so they can be subclassed and methods overridden as needed.

Both KKAppDelegate and KKRootViewController provide a default implementation which you can tweak with the config.lua parameters. If that shouldn’t be enough, for example if you have to plug in some 3rd party code into the App Delegate, each project will have a subclass of KKAppDelegate and KKRootViewController in which you can override any of the UIApplicationDelegate and UIViewController protocol methods. Usually you would first call the super implementation, unless you want to entirely replace the default behavior.

The KKAppDelegate method calls one specific method called **initializationComplete** at the end of the delegate method **applicationDidFinishLaunching**. This allows you to run any custom code right before the first scene is shown. You can use that to call the CCDirector runWithScene method manually, in case you have more than one scene which might be run as first scene depending on certain conditions.

If you set the FirstSceneClassName config.lua setting, the project will first check if there’s a classname.lua file. If so, it will run this Lua script, assuming it contains the implementation of the first scene (more on that some other time). Otherwise it checks if there’s an existing Objective-C class derived from CCScene with that name, and if so allocates and initializes this scene and calls runWithScene for you.

### In essence

From your point of view, the execution of the App now starts with the first scene, before that there’s no code that you’ll have to concern yourself with. Any startup configuration tweaks that you need to do can be done comfortably via the config.lua file, and the only setting you’ll need to change is the name of the first scene’s class name or Lua script. In addition you’ll get access to some features out of the box, for example adding iAd banners is now a simple on/off switch.

Moreover, any time there’s a change in Cocos2D’s startup code, or the startup code in any other library (most notably Wax), I can just make those changes for you and release a new version. This isn’t something you need to concern yourself with anymore, and makes upgrading existing projects to new versions of Cocos2D and other libraries even easier.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Excuse the dumb question: Is there anyway to write an iOS app in Lua within Xcode and have it spit out Objective-C before compilation?

If not, can an iPhone app be written using Lua and take advantage of additive blending in OpenGL ES? As Corona has no additive blend.

How could it be done?

There’s no Lua to Objective-C converter. You would have to write your own Lua scripting interface to do that, which is overkill given that it’s just about additive blending. I think it might actually be easier to contact the Corona guys and ask them to add additive blending, or find out if it’s already on the roadmap.

Hi

Steffen

I have ported our iPhone/iPod cocos2d game to Mac. I want to add a quit button in game menu. Clicking the quit button closes the game for mac. (Like in Angry Birds for Mac) I know its not possible for iPhone/iPad. But in full screen i want to give the player an option to quit game. Is there any way to achieve this for mac game in cocos2D.

Thanks

try calling:

[NSApp terminate: nil];

Thanks Steffen

When we can expect second edition of your book for cocos2d?

it’s currently scheduled for October 2011