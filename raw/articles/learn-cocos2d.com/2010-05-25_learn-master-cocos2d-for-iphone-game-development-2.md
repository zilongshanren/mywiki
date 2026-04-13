---
title: Learn & Master cocos2d for iPhone Game Development
url: http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/13733-upgrade-targets-to-ipad/13732_resolve-true/
author: Max says
published: '2010-05-25'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[Tutorial: cocos2d Xcode Project](http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/): Adding a Lite Version Build Target

#### Search my cocos2d for iPhone FAQs & Tutorials

*Please note that the blog search in the upper right corner doesn’t search my FAQs and Tutorials.*

**No images? Reload page, wait and try again.****PDF download broken? Reload page, try again.**- Note: please do not share direct download links to PDF files, the download links expire after a couple minutes!

- Note: please do not share direct download links to PDF files, the download links expire after a couple minutes!


We'll add a "Lite" version Target that you can use to build a free demo version with limited content.

### Duplicate the existing Target

Select the target, right or control click it and select Duplicate.

### Rename the copy

Rename it so you can identify it easily as the LITE version Target.

### Get Info

You know the drill. Right or control click, Get Info.

### Locate Preprocessor Macros

On the Build tab with All Configurations selected locate the Setting Preprocessor Macros. It will show <Multiple Values> indicating that the values are not identical for all Configurations. If you were to edit the values now, you would overwrite each Configuration's value with the new ones and you will lose the DEBUG/RELEASE macros. That's not what we want, so skip to the next step.

### Select Debug Configuration

Select the Debug configuration and notice that the Preprocessor Macros shows the DEBUG macro. Continue to edit the Preprocessor Macros by double-clicking the value.

### Add LITE_VERSION macro

Click the + button and add a macro that reads LITE_VERSION. You can then use code like #if LITE_VERSION ... #endif to include or exclude code for the lite version. Similarly you could also add a FULL_VERSION macro to the original target if you want to make things a little bit easier.

### Rinse and repeat

Repeat the above step for each of the build configurations we defined: Debug, Release, Ad Hoc Distribution and App Store Distribution, each time adding the LITE_VERSION macro. I'm afraid there is no shortcut here, just repetitive work. Luckily you'll do it only once.

### Rename "Info copy.plist"

Duplicating the Target will also create a "Info copy.plist" in the Resources folder. You should rename this file to "Info-Lite.plist" and update the LITE version target's Build Setting "Info.plist File" so it points to the renamed file as shown above.

Hi,

I am starting with obj-c, cocos2d, iPhone, etc and I just found this invaluable resource!

I read a few posts here and I think is really a precious place, a present and future ‘must have’ for me.

I saw also there are a lot of troubles when combining different pieces. I am still not used with this stuffs, then is a little difficult to follow all the logic of resolution of errors etc.

I am wondering if could be useful to create git repositories for the Xcode project, templates like for the Free Source Code (or even better, why not implement a whole Starter Kit with everything just working out of the box?). Could be very easy stay up to date for everyone in this way and the effort can be worthwhile.

By the way: I am trying to figure out what exactly is SpaceManager. What use and when exactly I need to use etc.

Thank you for the time spent in the attempt to simplify our lives


Thanks! If you have something specific you find difficult just let me know.

The free source code is already on git but i think you know that. The Xcode project is available via the Newsletter only as an incentive to sign up. I think that’s a fair deal because it’s easy to sign up and it’s free, in return i can reach out to you whenever i have something new to show. So the Xcode project will stay Newsletter only, unless i find something else to replace it with. Time will tell.

As for starter kits: good point! I’m actually working on a starter kit and plan to release several for the most popular but non-trivial games, similar to Sapus Tongue source code but allowing everyone to make an exact copy of the game because that’s the whole point of a starter kit. I don’t want to announce anything just yet because i keep having to push back work on that because of other tasks. There are definitely exciting things in the works for this website, so much i can say.


SpaceManager - i didn’t grab it either. The description isn’t as helpful as it could be. I think it makes a few things simpler, such as creating a physics object complete with sprite instead of doing this seperately. And also simplyfying collision detection because without SpaceManager those are C callback functions and harder to setup and work with because C doesn’t interface so well with Objective-C. I think its real value will only become clear when using it and since so many find it invaluable i guess it’s just not advertised and described very well.

Getting a build failed after I updated with the new path for Box2D.h. The message reads:

Cocos2d.h: No such file or directory

Please double-check that the “Header Search Path” is correctly setup:

http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/13472-create-a-xcode-project-template-referencing-the-cocos2d-project/

And also that it points to the correct directory where cocos2d-iphone is located on your HD (cocos2d Source Tree setting):

http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/13471-configure-xcode-for-cross-project-referencing

If that doesn’t help feel free to email me the project and i’ll have a look.

I downloaded the template project, and when I have ported all my files and resources over to this new one, it crashes with this line:

[[CCDirector sharedDirector] replaceScene:[CCFadeTransition transitionWithDuration:1 scene:[MainMenu scene] withColor:ccc3(0, 0, 0)]];

This is in my selector in my splash screen class:

@interface SplashScreen : CCLayer {

NSTimer *splashTimer;

}

+ (id)scene;

- (void)splashTimerCallback;

@end

and my implementation:

@implementation SplashScreen

- (id)init {

if ((self = [super init])) {

CCSprite *splash = [CCSprite spriteWithFile:@"480x320-splash-angry-01.png"];

splash.opacity = 0;

[splash setPosition:CGPointMake(240, 160)];

[self addChild:splash];

[splash runAction:[CCFadeIn actionWithDuration:1]];

splashTimer = [NSTimer scheduledTimerWithTimeInterval:2.5 target:self selector:@selector(splashTimerCallback) userInfo:nil repeats:NO];

}

return self;

}

+ (id)scene {

CCScene *scene = [CCScene node];

SplashScreen *layer = [SplashScreen node];

[scene addChild:layer];

return scene;

}

- (void)splashTimerCallback {

[[CCDirector sharedDirector] replaceScene:[CCFadeTransition transitionWithDuration:1 scene:[MainMenu scene] withColor:ccc3(0, 0, 0)]];

}

- (void)dealloc {

[super dealloc];

}

@end

Why is it crashing? It works fine in my other project, just not this new one.

What does the Debugger Console say when the crash happens? Usually the last line (in Debug builds) can tell you more.

I wonder why you do a replaceScene on [MainMenu scene] but the implementation you posted is from SplashScreen. Are you accidentally loading the wrong scene?

Also, to debug i would set a breakpoint at the beginning of the init method and then single-step through to see where it crashes. My guess is that maybe the image file the sprite should load doesn’t exist.

In addition: the use of NSTimer is not necessary, you can use [self schedule:@selector(splashTimerCallback) interval:2.5f] to achieve the same result.

I got that figured out, something to do with using a label in my main menu class. I ended up just using images for my main menu. But I have yet ANOTHER problem. I renamed the targets, and their respective products, and I was using this:

#if TARGET_IPHONE_IPOD

CCSprite *splash = [CCSprite spriteWithFile:@"480x320-splash-angry-01.png"];

#else

CCSprite *splash = [CCSprite spriteWithFile:@"1024x768-splash-angry-01.png"];

#endif

Before the renaming, it worked great. Now, after renaming the products and targets, it will ALWAYS load the second sprite, as if the first macro didn’t exist. Help?

I just tried with a whole new project and I doesn’t work. PERIOD. I don’t know what’s wrong with the macros. Has anyone else had any success with the macros?

On the Target: Right-click -> Get Info. Switch to Build tab and search for “Preprocessor Macros”. The setting “Preprocessor Macros Not Used in Precompiled Header” should have either TARGET_IPAD or TARGET_IPHONE_IPOD set depending on which target you’re looking at. If that’s not there or empty just add the correct Macro for each Target to this build setting.

HI,

From where i can get cocos2d + chipmunk project template with all the features that you have listed in your post. I am looking forward for that template.

Thanks

Yash Patel

Just sign up to my newsletter and you’ll get the files in a matter of minutes. They’ll be attached to the welcome mail.

http://www.learn-cocos2d.com/newsletter-signup

I tried it with your template but when I try to edit the xcode project and exit, it comes up and says that I can not edit it and that I can either keep it open or close it and lose all my changes. What do I do?

Ouch, good catch. That is the work of Perforce, it sets all files to read-only to make sure one opens them for edit before making changes. I’ll make sure to remove it from the projects i send around.

This link explains how to make a file/folder writable (first question/answer): http://askville.amazon.com/SimilarQuestions.do?req=easily+GUI+make+files+writable+MacOSX

I hope this helps.

I ended up doing this:

Go to the cocos2d project folder from the downloaded template -> right click on the xcode project -> show package contents -> right click on project.pbxproj -> get info -> and change the permissions to read/write

Hi i tryed your template but in my code for a contact listener for box2D doesn’t let me do this:

#import “Box2D.h”

#import // error: here it says it can found that file or directory

struct Contacto {

b2Body *CuerpoA; // error: “expected specifier-qualifier-list before ‘b2Body’ ”

b2Body *CuerpoB;

bool operator==(const Contacto& otro) const

{

return (CuerpoA == otro.CuerpoA ) && (CuerpoB == otro.CuerpoB);

}

};

can you help me plz?

(sorry for my english btw)

Thanks,

Ivan Bastidas.

See here:

http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/14335-integrating-box2d-physics/

Box2D files must be compiled as Objective-C++ / C++ code. Either by using .mm as file extension or setting the file type from Get Info as described in the link in the “avoid compile errors” paragraph.

I did that, but that code is in my .h file and it doesn’t let me import also, I cant define my class like this

class: OidoContactos: public b2ContactListener { //error: expected ‘=’, ‘,’, ‘;’, ‘asm’ or ‘__attribute__’ before ‘OidoContactos’

public:

std::vectorlistaContactos;

virtual void BeginContact(b2Contact* contact);

virtual void EndContact(b2Contact* contact);

};

I dont understand whats the problem >.<

Ok, if it’s the header then change the File Type to “sourcecode.cpp.h”.

You also have a : after “class” that shouldn’t be there:

class: OidoContactos: public b2ContactListener { … }

It would explain the error even if you have already set the file type to cpp.

yea that : is not im my code that was a mistake when I paste it here, I change the type to “sourcecode.cpp.h�? and is still not working…

I think is not a problem with my code beacuse it is working with the cocos2D default template, i tryed to run it with the “cocos2d Application” in your newsletter but I got the same problem


Thank you very much for your quick answers


btw after that import is a “vector”

I’ve got your template working, but when I try to integrate SpaceManager, and build, I get a few hundred errors all saying: “Deprecated conversion from string constant to ‘char*’.” Any suggestions?