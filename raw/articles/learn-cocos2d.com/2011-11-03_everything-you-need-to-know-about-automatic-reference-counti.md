---
title: Everything you need to know about automatic reference counting (ARC)
url: http://www.learn-cocos2d.com/2011/11/everything-know-about-arc/
author: Den says
published: '2011-11-03'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I have no doubt that automatic reference counting (ARC) is the next big leap forward for Objective-C since the introduction of Objective-C 2.0. ARC allows you to put the burden of memory management on the (Apple LLVM 3.0) compiler, and never think about retain, release and autorelease ever again.

Since many user’s first experiences with ARC will be trying to convert an existing app, they will learn the hard way that converting existing code to ARC is not a fire & forget operation. And since this is the Internet, there’s also a lot of assumptions, false statements and other myths revolving around ARC going around.

So here’s just about everything you need to know about ARC, and some ARC-mythbusting too.

[Development Requirements for ARC apps](http://www.learn-cocos2d.com/2011/11/everything-know-about-arc/#development-requirements)[Minimum Deployment Targets for ARC apps](http://www.learn-cocos2d.com/2011/11/everything-know-about-arc/#deployment-requirements)[Required Deployment Targets with zeroing weak references](http://www.learn-cocos2d.com/2011/11/everything-know-about-arc/#deployment-requirements-weak-references)[How to enable ARC in your project](http://www.learn-cocos2d.com/2011/11/everything-know-about-arc/#enable-arc)[Compile errors after switching to LLVM 3.0](http://www.learn-cocos2d.com/2011/11/everything-know-about-arc/#llvm-compile-errors)[Getting third party libraries to build with ARC](http://www.learn-cocos2d.com/2011/11/everything-know-about-arc/#third-party-libraries)[Converting an existing app to ARC](http://www.learn-cocos2d.com/2011/11/everything-know-about-arc/#convert-to-ARC)[“Cannot Convert to Objective-C ARC”](http://www.learn-cocos2d.com/2011/11/everything-know-about-arc/#cannot-convert-to-ARC)[Fixing pointer types in C structs](http://www.learn-cocos2d.com/2011/11/everything-know-about-arc/#pointers-in-structs)[Fixing C/C++ pointer transfers with bridged casts](http://www.learn-cocos2d.com/2011/11/everything-know-about-arc/#bridge-casts)[Fixing NSAutoreleasePool with @autoreleasepool](http://www.learn-cocos2d.com/2011/11/everything-know-about-arc/#autoreleasepool)[Methods you can’t call (or override) anymore](http://www.learn-cocos2d.com/2011/11/everything-know-about-arc/#methods-to-avoid)[You can still override -(void) dealloc {}](http://www.learn-cocos2d.com/2011/11/everything-know-about-arc/#overriding-dealloc)[Property naming restriction](http://www.learn-cocos2d.com/2011/11/everything-know-about-arc/#property-names)[New Property keywords: strong and weak](http://www.learn-cocos2d.com/2011/11/everything-know-about-arc/#property-keywords)[ARC forbids synthesizing a readonly property without ownership qualifier](http://www.learn-cocos2d.com/2011/11/everything-know-about-arc/#property-readonly-synthesize)[For experts: detecting at compile-time if ARC is enabled](http://www.learn-cocos2d.com/2011/11/everything-know-about-arc/#experts-detect-ARC)[For experts: allow use of ARC keywords with ARC disabled](http://www.learn-cocos2d.com/2011/11/everything-know-about-arc/#experts-ARC-keyword-macros)[Myth: ARC has not been proven reliable](http://www.learn-cocos2d.com/2011/11/everything-know-about-arc/#myth-ARC-not-reliable)[Myth: ARC takes away control over Memory Management](http://www.learn-cocos2d.com/2011/11/everything-know-about-arc/#myth-no-memory-management-control)[ARC Reference Documentation](http://www.learn-cocos2d.com/2011/11/everything-know-about-arc/#ARC-reference)


#### Development Requirements for ARC apps

- Xcode 4.2
- Apple LLVM compiler 3.0 (Build Setting)
- iOS app development: Snow Leopard 10.6 and newer
- Mac app development: Lion 10.7 and newer

There’s no ARC development for Mac apps under Snow Leopard! And Xcode 4.1 and earlier don’t come bundled with the Apple LLVM 3.0 compiler (Clang) which is the first Clang compiler version to support ARC.

#### Minimum Deployment Targets for ARC apps

- iOS devices: iOS 4.0 or newer
- Mac computer: Mac with 64-Bit processor running Snow Leopard 10.6 or newer.

Mac OS X apps with ARC enabled are always 64-Bit apps. You can not build 32-Bit ARC apps.

[Macs with at least a Core 2 Duo CPU](https://en.wikipedia.org/wiki/List_of_Macintosh_models_grouped_by_CPU_type#Core) will be able to run 64-Bit apps. [Macs with the 32-Bit Core Duo or Core Solo (Yonah) CPUs](https://en.wikipedia.org/wiki/List_of_Macintosh_models_grouped_by_CPU_type#P6) can’t run ARC apps. The 32-Bit Macs have been discontinued near the end of 2006, with the exception of the Core Duo Mac mini which was discontinued in August 2007.

#### Required Deployment Targets with zeroing weak references

- iOS devices: iOS 5.0 or newer
- Mac computer: Lion 10.7 or newer.

You can not “accidentally” use [zeroing weak references](http://www.learn-cocos2d.com/2011/11/everything-know-about-arc/#property-keywords) without noticing it. You will either have to use the @property keyword **weak** or the **__weak** keyword when declaring a variable. If you use one of these keywords, the compiler will generate an error if you haven’t yet set the deployment target accordingly to either iOS 5.0 or Mac OS X 10.7.

All Macs capable of running Lion 10.7 can run 64-Bit ARC apps. Lion is the first 64-Bit-only Mac OS X operating system.

#### How to enable ARC in your project

You will need to make sure that the Build Setting for **Compiler for C/C++/Objective-C** is set to **Apple LLVM compiler 3.0**.

This is particularly important for existing projects which may still be set to use LLVM GCC 4.2 or another compiler. If you don’t select the LLVM 3.0 compiler, none of the ARC related settings will show up in the Build Settings list.

With LLVM 3.0 selected as compiler the Build Setting **Objective-C Automatic Reference Counting** can be set to YES. If you create a new project from an Xcode template you will also have the option to enable ARC in the new project wizard by selecting **Use Automatic Reference Counting**.

#### Compile errors after switching to LLVM 3.0

If you previously were using a different compiler, it is absolutely possible that LLVM 3.0 will generate new warnings and errors where there were none before, even with ARC disabled. This is the LLVM 3.0 compiler which got a little better at detecting potentially dangerous code.

I recommend to first build your app with LLVM 3.0 compiler and ARC disabled, to make sure all LLVM 3.0 related issues have been fixed before attempting to convert your code to ARC.

For example, LLVM 3.0 is now able to detect some potential “array out of bounds” issues thanks to the [SAFECode project](http://safecode.cs.illinois.edu/), and it’s a bit more nagging when it comes to casting one type to another, in particular related to format strings. Most of these issues are easy to resolve. In fact, LLVM 3.0 helps you determine where the issue is through [expressive diagnostics](http://clang.llvm.org/diagnostics.html), but unfortunately Xcode hides that pretty well from the user.

To see expressive diagnostics in Xcode, go to the Log Navigator (Command+7) and select the most recent log with the warning or error in it:

Then click the details button to the right of the warning/error symbol (just above the “more” link) to see the LLVM 3.0 expressive diagnostics statement, pointing exactly to the character or range of characters causing the issue:

#### Getting third party libraries to build with ARC

The first thing to do with incompatible third party libraries is to build them as a separate static library. Take for example Cocos2D whose Xcode project template simply puts all of the Cocos2D code into your project’s target. It would be a nightmare to try and update the entire Cocos2D library code to support ARC. While you can [disable ARC for individual source code files](http://stackoverflow.com/questions/6646052/how-can-i-disable-arc-for-a-single-file-in-a-project) with the **-fno-objc-arc** compiler flag, it would be tedious to do so for more than just a few files.

Once you build the Cocos2D source code separately as a static library, the required changes are limited to three places: CCDirector (remove NSAutoreleasePool), CCActionManager (add __unsafe_unretained) and CCArray (add __unsafe_unretained, refactor inline code into implementation file). [Tiny Tim Games have outlined these changes](http://www.tinytimgames.com/2011/07/22/cocos2d-and-arc/) and provide a [fork of cocos2d-iphone that is compatible with ARC](https://github.com/jerrodputman/cocos2d-iphone) - if built as a static library.

By the way, [Kobold2D is fully compatible with ARC](http://www.learn-cocos2d.com/2011/10/kobold2d-preview-6-giving-retain-release-autorelease-finger/). In fact it has ARC enabled by default in all projects while retaining full backwards compatibility if you don’t want to use ARC!

If building a static library still causes too many issues with that library, then go to that library’s forum, look for ARC related posts and/or request ARC support. Many open source libraries don’t even compile cleanly with LLVM 3.0 yet, let alone support ARC. This needs to change quickly because library developer support directly influences the adoption rate of ARC.

#### Converting an existing app to ARC

There’s an app for that!

Well, to be precise there’s a menu option in Xcode 4.2 for that. You’ll find it if you open your project in Xcode and choose **Edit -> Refactor -> Convert to Objective-C ARC…**.

You will be presented with a list of targets that you want to convert. Make sure you don’t select any static library that you haven’t written yourself. Static libraries can be linked to an ARC-enabled app without actually having to be ARC compatible. Although you may have to make some changes to the library’s header files. More on that later.

#### “Cannot Convert to Objective-C ARC”

Oh dear!

In some cases automatic conversion is not as automatic as you’d hope it would be. In many cases this is because of incompatible static libraries.

In most cases the problems are related solely to id or other pointer types stored in a C struct, passing pointers to and from C/C++ code or the use of the NSAutoreleasePool class which is not available when building an app with ARC enabled. Read on for solutions to the most common issues.

#### Fixing pointer types in C structs

ARC will complain about a C struct that stores pointer types:

[cc lang=”cpp”]typedef struct {

id someObject;

void* somePointer;

SomeClass* someClassInstance;

} someStruct;

[/cc]

This is easy enough to fix by prepending the pointer types with the **__unsafe_unretained** keyword:

[cc lang=”cpp”]typedef struct {

__unsafe_unretained id someObject;

__unsafe_unretained void* somePointer;

__unsafe_unretained SomeClass* someClassInstance;

} someStruct;

[/cc]

This tells ARC that the memory for these pointer types is managed manually, ie. the old-school way. Henceforth the pointer type is “unretained” by ARC, and it is “unsafe” because the memory may be deallocated but the pointer isn’t set to nil automatically, which can possibly create a dangling pointer. That’s the way it has been all the time, ARC just wants you to expressly admit that you’re doing something that is considered unsafe.

If your code worked fine before, **__unsafe_unretained** will simply make sure it compiles under ARC. But for new code you should avoid having to use that keyword. One option is to change all C structs into lightweight Objective-C classes with properties.

#### Fixing C/C++ pointer transfers with bridged casts

In cases where you’re passing id or object pointers to and from C/C++ code, the compiler will complain about the conversion and suggest a bridged cast:

[cc lang=”cpp”]// Assigning sprite to Box2D userdata

b2BodyDef bodyDef;

bodyDef.userData = aSprite; // ERROR!

// Getting the userdata sprite from Box2D

CCSprite* sprite = (CCSprite*)body->GetUserData(); // ERROR!

[/cc]

Again this is easy to fix by properly casting the pointer type and prepending it with the **__bridge** keyword:

[cc lang=”cpp”]// Assigning sprite to Box2D userdata

b2BodyDef bodyDef;

bodyDef.userData = (__bridge void*)aSprite;

// Getting the userdata sprite from Box2D

CCSprite* sprite = (__bridge CCSprite*)body->GetUserData();

[/cc]

The **__bridge** keyword simply means that the pointer is transferred from or to Objective-C land unchanged. ARC will neither retain nor release that pointer.

The special keywords **__bridge_transfer** and **__bridge_retain** should only be used [when dealing with toll-free bridged Core Foundation objects](http://developer.apple.com/library/ios/#releasenotes/ObjectiveC/RN-TransitioningToARC/_index.html) where you would normally have to call **CFRetain** and/or **CFRelease** to manage the Core Foundation object’s lifetime.

#### Fixing NSAutoreleasePool with @autoreleasepool

ARC replaced the NSAutoreleasePool class with the [@autoreleasepool compiler directive](http://www.learn-cocos2d.com/blog/#autoreleasepool).

You must replace code using NSAutoreleasePool:

[cc lang=”cpp”]NSAutoreleasePool* pool = [[NSAutoreleasePool alloc] init];

// create some temporary objects here …

[pool release];

pool = nil;

[/cc]

With the @autoreleasepool keyword:

[cc lang=”cpp”]@autoreleasepool

{

// create some temporary objects here …

}

[/cc]

#### Methods you can’t call (or override) anymore

You will have to remove all calls to these methods without substitution:

- retain
- retainCount
- release
- autorelease
- dealloc

You also can’t use the **retain** keyword with properties anymore. Instead, use the **strong** keyword.

You can no longer override these methods in your class:

- retain
- retainCount
- release
- autorelease

#### You can still override -(void) dealloc {}

You can not call dealloc but you can still override the **-(void) dealloc {}** method. This is useful to release the memory of C/C++ objects. For example you still need to be able to free the memory of a Box2D world instance. Similarly there are instances where you need to remove self as the delegate of another class when the self class is deallocated.

There’s one particular habit that you need to let go of. Since you can’t call dealloc, you also must not call **[super dealloc]**. The compiler will generate the **[super dealloc]** call behind the scenes automatically.

#### Property naming restriction

You can not create a property whose name begins with “new”. That’s all.

#### New Property keywords: strong and weak

The @property keyword **strong** is synonymous to **retain**:

[cc lang=”cpp”]// synonym for: @property(retain) MyClass *myObject;

@property(strong) MyClass *myObject;

[/cc]

Whereas **weak** is similar to **assign**, except that a weak property will be set to nil automatically when the object is deallocated (hence: zeroing weak reference):

[cc lang=”cpp”]// similar to “@property(assign) MyClass *myObject;”

@property(weak) MyClass *myObject;

[/cc]

Zeroing weak references are only available when targeting iOS 5.0 and newer, or Mac OS X Lion 10.7 and newer.

#### ARC forbids synthesizing a readonly property without ownership qualifier

Normally, when you declare a readonly property, it doesn’t matter what the storage type is (retain, assign, copy) since readonly properties can’t be assigned to. Take this one for example:

[cc lang=”cpp”]@property (nonatomic, readonly) MyView* myViewController;

[/cc]

Now with ARC, if you don’t declare the ivar manually ([@synthesize can generate ivars](http://developer.apple.com/library/mac/documentation/Cocoa/Conceptual/ObjectiveC/Chapters/ocProperties.html#//apple_ref/doc/uid/TP30001163-CH17-SW9)) you will encounter a strange error on the @synthesize line, stating:

error: ARC forbids synthesizing a property of an Objective-C object with unspecified ownership or storage attribute [4]


[As odd as it may seem](https://openradar.appspot.com/radar?id=1282404), in this case you will have to specify the storage keyword on a readonly property, by adding either **strong** or **weak**:

[cc lang=”cpp”]@property (strong, nonatomic, readonly) MyView* myViewController;[/cc]

This specifies the ownership qualifier of the ivar through the @property declaration. The alternative would be to declare the ivar manually, which will force the property to use the same ownership qualifier as the ivar.

#### For experts: detecting at compile-time if ARC is enabled

If you need to find out whether your code is built with or without ARC, for example if you’re the developer of a public library, you can use the following macros to determine whether ARC is enabled at compile time.

[cc lang=”cpp”]// define some LLVM3 macros if the code is compiled with a different compiler (ie LLVMGCC42)

#ifndef __has_feature

#define __has_feature(x) 0

#endif

#ifndef __has_extension

#define __has_extension __has_feature // Compatibility with pre-3.0 compilers.

#endif

#if __has_feature(objc_arc) && __clang_major__ >= 3

#define ARC_ENABLED 1

#endif // __has_feature(objc_arc)

[/cc]

#### For experts: allow use of ARC keywords with ARC disabled

As a library author, one of the worst things you could do to ensure backward compatibility of your library is to #ifdef every ARC-specific keyword and write every such line twice: once without the ARC keyword, once with the ARC keyword.

[cc lang=”cpp”]// BAD PRACTICE!!

#ifdef ARC_ENABLED

void* pointerToSelf = (__bridge void*)self;

#else

void* pointerToSelf = (void*)self;

#endif // ARC_ENABLED

[/cc]

Instead I propose to simply define the ARC keywords as “noop” statements when ARC is unavailable. Thus your code using ARC keywords will still compile under Xcode 4.1 or LLVM GCC4.2, and you don’t need to #ifdef anything related to those keywords.

[cc lang=”cpp”]// not using clang LLVM compiler, or LLVM version is not 3.x

#if !defined(__clang__) || __clang_major__ < 3
#ifndef __bridge
#define __bridge
#endif
#ifndef __bridge_retained
#define __bridge_retained
#endif
#ifndef __bridge_transfer
#define __bridge_transfer
#endif
#ifndef __autoreleasing
#define __autoreleasing
#endif
#ifndef __strong
#define __strong
#endif
#ifndef __weak
#define __weak
#endif
#ifndef __unsafe_unretained
#define __unsafe_unretained
#endif
#endif // __clang_major__ < 3
[/cc]
Now it is safe to write code like this regardless of whether ARC is available or not, because compilers that don't support ARC will only see the regular (void*) cast:
[cc lang="cpp"]void* pointerToSelf = (__bridge void*)self;
[/cc]

#### Myth: ARC has not been proven reliable

As if automatic memory management has some magic property that occasionally goes bonkers.

ARC still follows the same alloc, retain, release cycle of Objective-C code. There are no ambiguities and no special cases when it comes to applying the few and simple alloc-retain-release rules. This is entirely deterministic and the compiler can do that job just as well, no, better than you. There’s nothing inherently and potentially unreliable about ARC.

If you’ve heard about issues with ARC, then they’re likely related to situations where an ARC app interfaces with the Core Foundation or other C/C++ code. In those situations you will have to correctly apply the various new keywords (bridge casts for the most part). Make a mistake there and you got yourself a problem. But that’s not the fault of ARC. The same goes for [retain cycles](http://mikeash.com/pyblog/friday-qa-2010-04-30-dealing-with-retain-cycles.html), which are still a possibility in ARC apps.

I also bet my life that Apple wouldn’t announce, promote and implement ARC for iOS and Mac OS X apps if it hadn’t been proven stable. If that doesn’t convince you, then maybe this [quote of the ARC developer Chris Lattner](http://lists.cs.uiuc.edu/pipermail/cfe-dev/2011-June/015588.html) does:

ARC is carefully built to be a reliable programming model that errs on the side of producing a compiler error instead of silently producing a runtime memory problem.


That also explains a bit why you’ll see more (initial) compile errors with ARC enabled.

#### Myth: ARC takes away control over Memory Management

Some argue that ARC takes away your control over memory management. That in turn would lead to less than optimal runtime performance. Henceforth ARC is bad and should be avoided.

You could apply the same pointless argument to [power steering](https://en.wikipedia.org/wiki/Power_steering). There are some die-hards who would rather not have power steering, just because of some subjective *feeling* about losing control. Ignore these people! Not because they’re wrong, they are correct in some circumstances - it’s just that those circumstances are rare, very specialized and require a high level of skill that the remaining 99% of users simply don’t have, nor would want to exercise.

And even if you do have the skills, you’re still subject to errors of judgement or other human errors. So even the experts will benefit from using ARC (or power steering for that matter) in everyday situations.

Some people who argue that ARC takes away control don’t seem to understand what ARC does. Memory Management is about the lifetime of objects, whether the memory management is automated with ARC or manual. If an object’s lifetime is throughout the entire scene (view, level, app, etc) then that object is allocated once when the scene is initialized, and deallocated when the scene is deallocated. Whether you do this manually, or automatically, results in the same behavior of the application.

Everyone needs to understand that ARC is [deterministic](https://en.wikipedia.org/wiki/Deterministic_algorithm). It is **not** to be mistaken for [garbage collection](https://en.wikipedia.org/wiki/Garbage_collection_(computer_science))! Garbage collection cycles can kick in at any random moment in time when the garbage collector finds it necessary to free up some memory. In a garbage collected environment, such as C#, you do lose some control over memory management and in some situations this leads to unsteady runtime performance. But not with ARC.

To say that ARC removes control over memory management is just plain wrong and probably based on the assumption that ARC is equal to garbage collection. It may also stem from the “false positives” that the [Clang Static Analyzer](http://clang-analyzer.llvm.org/) produces, which may have instilled doubt about “automated” Clang technologies in general, even though static analysis and ARC are completely separate pieces of technology.

Either way, in some cases you may need to exercise control over memory management and with ARC you can still do that, usually with the new ARC keywords strong and weak, as well as bridge casts for pointers that are crossing boundaries from or to C/C++ land. As long as you are aware of the lifetime of your objects you will have no problem influencing how the lifetime of objects is managed by ARC.

ARC always allocates and releases an object’s memory at the same point in time in the same situation (deterministic). Thus Objective-C with ARC can not be compared to garbage collected languages like C#. If you see someone comparing ARC with C#, [please send them this link](http://www.learn-cocos2d.com/2011/11/everything-know-about-arc/#myth-no-memory-management-control).

#### ARC Reference Documentation and related articles

Further reading for those who want to learn more about ARC in detail.

- Clang:
[Automatic Reference Counting documentation](http://clang.llvm.org/docs/AutomaticReferenceCounting.html) - Apple:
[Transitioning to ARC Release Notes](http://developer.apple.com/library/ios/#releasenotes/ObjectiveC/RN-TransitioningToARC/) - Apple:
[Xcode New Features User Guide: Automatic Reference Counting](http://developer.apple.com/library/mac/#documentation/DeveloperTools/Conceptual/WhatsNewXcode/Articles/xcode_4_2.html#//apple_ref/doc/uid/00200-SW2) - Mike Ash:
[Friday Q&A about Automatic Reference Counting](http://www.mikeash.com/pyblog/friday-qa-2011-09-30-automatic-reference-counting.html) - StackOverflow:
[How does automatic reference counting work?](http://stackoverflow.com/questions/6385212/how-does-the-new-automatic-reference-counting-mechanism-work) - StackOverflow:
[What are the advantages and disadvantages of using ARC?](http://stackoverflow.com/questions/7888568/what-are-the-advantages-and-disadvantages-of-using-arc) - StackOverflow:
[What is the difference between automatic reference counting and garbage collection?](http://stackoverflow.com/questions/7874342/what-is-the-difference-between-objective-c-automatic-reference-counting-and-garb) - informIT:
[Automatic Reference Counting in Objective-C, Part 1](http://www.informit.com/articles/article.aspx?p=1745875) - informIT:
[Automatic Reference Counting in Objective-C, Part 2 The Details](http://www.informit.com/articles/article.aspx?p=1745876) - Mike Ash:
[Zeroing weak references without ARC](http://www.mikeash.com/pyblog/friday-qa-2010-07-16-zeroing-weak-references-in-objective-c.html) - Github:
[Support for zeroing weak references on iOS 4 / OS X 10.6](https://github.com/rpetrich/ZWRCompatibility)

Please let me know if I forgot to add anything about ARC! Especially if you think it should be common knowlARCdge. And don’t forget to retweet this article if you like it, thanks!

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

When I read about Mac development it feels like I went 10/15 years back in time.

That is quite true. However, the mobile hardware environment apparently still requires eschewing all the modern conveniences such as GC which suck up resources. The far more inferior Android UX confirms that.

I’ve been looking for a brief like this, thank you!!

I think this will clarify many ideas about ARC. Great job![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


What a great post. thanks very much for this. looks like a good thing to do on the weekend![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


One thing I haven’t been able to figure out yet is how to use forwarding with ARC. Details in this Stack Overflow question:

http://stackoverflow.com/q/7858980/8427

Awesome, Steffen! Great summary.

I’d been looking for information on bridged casts and the Apply documentation has virtually nothing about it. This article and the references you provided helped a lot.

Thanks!

Andre

That ‘You can not create a property whose name begins with “new”’ bit is not quite true. See: http://stackoverflow.com/q/6327448/557219

This is in Apple’s Transitioning to ARC Release Notes:

The link you provided gives a solution to this problem, for example by renaming the property from “newObject” to “theNewObject”.

Yup, I’ve told Apple that their statement is not really true (there are at least two other inaccuracies in that document).

Renaming the property is one solution, but there are two other solutions in which the property doesn’t get renamed: renaming the getter method, and specifying a different method family for the getter method. These two solutions allow using a property whose name starts with new.

“For example, LLVM 3.0 is now able to detect some potential “array out of bounds” issues thanks to the SAFECode project”

As nice a project as SAFECode is, that is not what is reporting the array out of bounds warnings. That’s just an ordinary clang warning, and was first committed here: http://lists.cs.uiuc.edu/pipermail/cfe-commits/Week-of-Mon-20110214/038831.html

I tried to use your macros “Detecting at compile-time if ARC is enabled”, but it seems to me that it doesn’t work properly.

“seems” and “not properly” are terribly inaccurate descriptions of what’s happening. The macros definitely work, I use them in Kobold2D a lot. Be sure to define the macros in a header file and import that header in the source files where you’re using the macros.

[…] heard about Objective-C automatic reference counting (ARC). And you’ve read about it here and there and every where. But you’re not using […]

Learned a lot from your post!

Thanks![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


[…] ARC enabled versions of the […]

[…] http://www.learn-cocos2d.com/2011/11/everything-know-about-arc/ […]

Good article, writer knows his stuff. Someone had comment that his feeling is like he is reading about outdated things.

By my opinion ARC is better than garbage collection , in fact ARC is next level stuff compared to GC. ARC frees memory exactly when not needed any more, gc frees it “eventually”. If memory consumption/freeing happens fast ARC will totally outscore gc.

Thanks a lot for the _bridge paragraph, i was very helpful since my program was crashing, so if i understand well,

_bridge doesn’t need to release memory afterwards.

CFBridgingRetain requires a CFBridgingRelease ?

thanks

pat.

__bridge = assign, retain count remains the same (similar to __unsafe_unretained)

__bridge_retain = retain count +1

__bridge_transfer = retain count -1

If you do:


and myObject has no other strong reference elsewhere, then ARC will release myObject and data becomes an invalid pointer.

If you were to use __bridge_retain instead, the object would remain in memory. And it will remain in memory (possibly leaking) if it isn’t balanced with __bridge_transfer or (for CF types) CFRelease() isn’t called on it.