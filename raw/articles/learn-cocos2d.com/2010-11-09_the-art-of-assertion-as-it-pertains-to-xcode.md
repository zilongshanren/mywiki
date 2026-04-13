---
title: The Art of Assertion (as it pertains to Xcode)
url: http://www.learn-cocos2d.com/2010/11/art-assertion-pertains-xcode/
author: Alex says
published: '2010-11-09'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Recently, I’ve changed all my project’s source code files from .m to .mm file extensions. This is telling the compiler to compile the files as Objective-C++/C++ code instead of the default Objective-C/C. I needed to do so because I’m using Box2D, and as a habit I intend to use .mm from now on for every source file I create.

However, beware the subtle differences. Previously, if an NSAssert was triggered, it halted the program execution. But in .mm files it simply prints the assertion message to the console while the App continues execution. This leads to overlooked assertions, or continuously dumping assertion messages to the console. Clearly not what I wanted. Changing the file extension from .mm back to .m fixed the problem, but that’s not an option I have for all files.

I looked around and found a blog article by Vincent Gable mentioning that [NSAssert is considered harmful](http://vgable.com/blog/2008/12/04/nsassert-considered-harmful/). That caught my attention, because it described the same problem that I experienced (NSAssert not halting execution) while basing the argument on Voodoo (“Sometimes it does, sometimes it does not …”) respectively no argument at all, it’s just telling you “NSAssert is unreliable, therefore dangerous”.

It’s as if he wants me to prove him wrong. ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


In Vincent’s defense, the wrong he’s done unto NSAssert he makes up for by having written a [great logging method](http://vgable.com/blog/#Get_LOG_EXPR) which I’m going to add to gocos because it’s so handy.

### Why assert() is less useful than NSAssert

First of all, the assert() function has one big problem: it doesn’t allow parameters to be added to the output string, since the output string can only be a constant string, like in this example:

[cc lang=”objc”]

assert(value < maxValue && @"value too big!");
[/cc]
With NSAssert you can actually embedd some values into the assertion message:
[cc lang="objc"]
NSAssert2(value < maxValue, @"value %i too big (max:%i)!", value, maxValue);
[/cc]
It is tremendeously helpful in many cases to actually see the offending or interesting values in the error message, without having to fire up the debugger. Especially when it comes to filenames, and even more so if end users might see those assertions. Not a problem on the iOS, but think of developing desktop Apps.

### Why NSAssert isn’t harmful, and how to fix it

So then, why did my App not stop execution when an NSAssert triggered? I can’t really answer you that, [Apple’s docs](http://developer.apple.com/library/mac/#documentation/Cocoa/Reference/Foundation/Miscellaneous/Foundation_Functions/Reference/reference.html#//apple_ref/c/macro/NSAssert) say that NSAssert will raise an NSInternalInconsistencyException. So that should stop the App from running? It does not seem to be the case when you’re using the Objective-C++ compiler, and I’m not running the code on a different thread either. Maybe someone can shed some light as to why NSAssert in C++ code doesn’t automatically stop the App from running.

The good thing is, there’s an easy way to fix that. In Xcode choose **Run -> Show -> Breakpoints** from the menu, to bring up the breakpoints list. In the breakpoint list you only need to add the symbol **objc_exception_throw**. Next time an NSAssert triggers, the App will stop immediately and bring up the debugger.

![2010-11-09_16.57.33](../../../wordpress/wp-content/uploads/2010-11-09_16.57.33-300x95.png)


Some places (for example: [here](http://blog.emmerinc.be/index.php/2009/03/19/break-on-exception-in-xcode/)) will also tell you to add [NSException raise] to the breakpoints list. That’s not necessary, this has been replaced with objc_exception_throw since Mac OS X 10.5.

### Turning off assertions

I must admit, I’m totally spoiled by Visual Studio. Why Xcode requires you to add NS_BLOCK_ASSERTIONS as a macro to your project’s build settings in order to not compile NSAssert in release builds is beyond me. If you’re using NSAssert in your code, make sure that your release and/or distribution builds define the NS_BLOCK_ASSERTIONS macro.

If you do use the assert() macro however, or if you’re using a 3rd party library that uses assert(), make sure to also define NDEBUG for release/distribution builds.

As a side note, when I update my [cocos2d-project](http://www.learn-cocos2d.com/2010/11/cocos2d-xcode-project-github/) respectively replace it with gocos, it will have all these settings properly configured.

### Catching uncaught exceptions

On a related matter, there’s always the issue of uncaught exceptions simply halting your App, with little chance to debug the actual cause. It happens rarely but when it does, it would be really helpful to also bring up the debugger with the current call stack and everything. You can set a global exception handler to catch uncaught exceptions by calling the NSSetUncaughtExceptionHandler in the applicationDidFinishLaunching method of your AppDelegate:

[cc lang=”objc”]

void onUncaughtException(NSException* exception)

{

NSLog(@”uncaught exception: %@”, exception.description);

}

-(void) applicationDidFinishLaunching:(UIApplication*)application

{

NSSetUncaughtExceptionHandler(&onUncaughtException);

…

}

[/cc]

In the onUncaughtException method you’ll simply log the exception and (very important) add a breakpoint. The NSLog message serves the purpose of being able to easily set a breakpoint inside this method. It should not be another NSAssert because that will throw another exception, which will only serve to make debugging more complicated when a simple breakpoint suffices.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

[assertion](http://www.learn-cocos2d.com/tag/assertion/)•

[assertions](http://www.learn-cocos2d.com/tag/assertions/)•

[box2d](http://www.learn-cocos2d.com/tag/box2d/)•

[breakpoint](http://www.learn-cocos2d.com/tag/breakpoint/)•

[Breakpoints](http://www.learn-cocos2d.com/tag/breakpoints/)•

[compiler](http://www.learn-cocos2d.com/tag/compiler/)•

[debugger](http://www.learn-cocos2d.com/tag/debugger/)•

[error message](http://www.learn-cocos2d.com/tag/error-message/)•

[exception](http://www.learn-cocos2d.com/tag/exception/)•

[file extension](http://www.learn-cocos2d.com/tag/file-extension/)•

[m to mm](http://www.learn-cocos2d.com/tag/m-to-mm/)•

[macro](http://www.learn-cocos2d.com/tag/macro/)•

[NDEBUG](http://www.learn-cocos2d.com/tag/ndebug/)•

[NSAssert](http://www.learn-cocos2d.com/tag/nsassert/)•

[NSException](http://www.learn-cocos2d.com/tag/nsexception/)•

[NSInternalInconsistencyException](http://www.learn-cocos2d.com/tag/nsinternalinconsistencyexception/)•

[NSLog](http://www.learn-cocos2d.com/tag/nslog/)•

[NSSetUncaughtExceptionHandler](http://www.learn-cocos2d.com/tag/nssetuncaughtexceptionhandler/)•

[Objective-C](http://www.learn-cocos2d.com/tag/objective-c/)•

[onUncaughtException](http://www.learn-cocos2d.com/tag/onuncaughtexception/)•

[source code](http://www.learn-cocos2d.com/tag/source-code/)•

[Xcode](http://www.learn-cocos2d.com/tag/xcode/)

Hey, Steffen!

Thank you very much for this post! I got the same issue in my project where NSAssert wouldn’t break in some places of the code.

Best regards,

Alex

XCode4 gives you the possibility to break on all exceptions. Go to the Breakpoints tab of the left pane, press + (bottom left corner) -> “Add Exception Breakpoint…” an make sure it says “all”. A quick test in an .mm file showed that xcode does successfully break on a failed NSAssert.

Also, I just joined a bigger iOS project. It already has a nice logger and I’m going to add a new Assert that firls logs the error and then triggers the NSAssert on debug builds. It will just log an error on all other builds.

I think the reason that C++ does not halt when you raise an exception is that Objective-C and C++ have different exception handling mechanisms. C++ handles exceptions with try/catch while Obj-C uses @try/@catch.

Under a pure C++ file there is no Obj-C exception handling at all, so the @throw used by NSAssert does nothing. If you are under Obj-C++, then both types of exceptions are present.

The reason that the assert macro always works is because it does not raise an exception. Instead it prints to std error and then calls the C standard library function call abort(). This sends your application a SIGABRT signal which will terminate your application unless you have installed a signal handler for it that prevents your app from terminating.

Thanks Steffen; this is quite useful if a little out of date (The XCode UI / method to enable break on exceptions changed a little since then).

Although I use NSAssert ( in Rome do as the Romans do? ), I still think Vincent’s argument has some weight - I had to use your method and add an explicit breakpoint after my program stopped breaking on asserts altogether and for the life of me I can’t figure why. So there certainly is this ongoing voodoo feel to it.

Being somewhat unconvinced by the idea of converting all your files to OC++ just because you’re using a C++ library.

The reason NSAssert* does not always halt execution is because it raises an exception. Exception are not guaranteed, by design, to cause a program to crash. Compiling with or without C++ does not matter, because the underlying Objective-C exception mechanism is built with the C++ runtime. I suspect the effect you saw was something else.

It is worth noting that @catch cannot catch a C++ exception, but catch(…) will catch a NSException. This is a behavior many are surprised by when intermixing C++ and ObjC. It is untrue that @throw does not work in a otherwise-c++ environment, as of Objective-C 2.0 (10.5 and all iOS versions).

On OS X, there are many, many implicit catches in the framework. Exceptions during notifications? No crash. Exceptions causes by UI events? No crash. The situation is slightly different on iOS. Regardless, this produces lots of opportunity for leaks, deadlock, and other kinds of terrible state corruption.

It is true, assert() does not allow you provide custom formatting. That’s a pain. I have no good workaround. But, I strongly agree with Vincent Gable’s article. Use of NSAsset no only won’t always stop execution, it is also great way to corrupt your processes state, particularly if you are using a exception-unsafe system (which, unfortunately, describes Cocoa).

NSAsset should never be used, unless you and every single client of your code has a firm grasp of exceptions and how tricky they are to use in Cocoa. assert() is a much better recommendation.

Hi! I totally agree on all issues you are pointing out. I’ve created ‘AGAssert’ which eliminates these problems. https://github.com/hfossli/agassert