---
title: Learn & Master Cocos2D Game Development
url: http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/13730-tweaking-our-build-settings/
author: Carl says
published: '2010-12-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[Tutorial: cocos2d Xcode Project](http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/): Tweaking our Build Settings

#### Search my cocos2d for iPhone FAQs & Tutorials

*Please note that the blog search in the upper right corner doesn’t search my FAQs and Tutorials.*

- Note: please do not share direct download links to PDF files, the download links expire after a couple minutes!

We'll take a look at Xcode's layered build settings and then modify our Build Settings for an optimal programming experience.

### Understanding Layered Build Settings

At this point you might want to read about [Xcode's layered Build Settings](http://developer.apple.com/mac/library/documentation/DeveloperTools/Conceptual/XcodeBuildSystem/300-Build_Settings/bs_build_settings.html#//apple_ref/doc/uid/TP40002691-SW5). Not understanding this feature respectively not knowing about it has caused a lot of confusion, especially when developers are frantically trying to fix code signing issues. To put it simple: any setting that you change in the Project's build setting dialog will be used by all targets, **unless the Target itself defines that setting**. You can see if a **Target overrides** a Project build setting when it is **displayed in bold letters**. See the screenshot above.

Now, here's where most people trip: even if you change a Target's setting and then immediately change it back to its original value, that value will still override the same setting in the Project configuration. It will still be printed in bold letters (remember this indicator well!). So as developers started editing the Code Signing Identity in one of their Targets, and later tried to change that via the Project configuration, the change had no effect because the Target is still overriding that setting.

Thus the plenty solutions along the line of "Oh, i fixed it, i forgot to change it in the Target settings as well". Not true, you just forgot you were overriding it in the Target settings and should have deleted the setting at the Target level instead. I'll show you how:

### Allowing the Project to define Build Settings

To reset a Target build setting after you have changed it, and so that the Project build setting will take effect again, you have to select that setting in the Target properties and click on the gear wheel button at the bottom of this dialog. Choose "Delete Definition at This Level".

Of course this works only on build settings printed in bold - remember: bold letters means the Target overrides the Project's build settings.

Note: you may notice that the Project itself also has settings in bold - this is because there are even settings higher up in the hierarchy. You don't have to worry about these but if you're interested you can learn more about it in the [Xcode Layered Build Settings](http://developer.apple.com/mac/library/documentation/DeveloperTools/Conceptual/XcodeBuildSystem/300-Build_Settings/bs_build_settings.html#//apple_ref/doc/uid/TP40002691-SW5) document.

### Target Build Setting no longer overrides Project Build Setting

After you've deleted the definition at the Target level, you'll see that it is no longer printed in bold letters and the value has changed to the value set in the Project's setting dialog. In this case it's an empty string.

### Confirm Project Setting is used by Target

Go ahead and change that setting in the Project settings and see it change in the Target settings, just to confirm.

Remember [Xcode's Layered Build Settings](http://developer.apple.com/mac/library/documentation/DeveloperTools/Conceptual/XcodeBuildSystem/300-Build_Settings/bs_build_settings.html#//apple_ref/doc/uid/TP40002691-SW5) approach and you'll be a much happier Xcode programmer!

### Open Project Build Settings

Select the project itself, right or control-click and choose Get Info.

We'll go through the list of setting we want to change from top to bottom.

### Make sure you edit all Build Configurations

The changes we make first affect all build configurations. Currently we only have Debug & Release, we'll add more later.

### Check "Validate Built Product"

Under Build Options check "Validate Built Product" if not already checked. This will generate some additional warnings which could fail your build during App approval, for example it will warn you if the Icon's size is incorrect among other things.

### Select correct "Code Signing Identity"

Next you want to set your "Code Signing Identity". For "Any iPhone OS Device" it should read "iPhone Developer" followed by the current match which will have your name or your company's name in it. See the next step.

### Select the "Automatic Profile Selector"

There has been a lot of confusion about code signing. This lead to many wrong approaches to fix code signing issues when developers frantically tried to fix their issues. Some have started to distrust the "Automatic Profile Selector" altogether. There is no reason to not trust the automatic selection for non-distribution builds!

We currently only have Debug and Release Build Configurations. Both are not intended for use with Distribution. So it is in your own best interest to use the automatic profile selector here and pick the "iPhone Developer" profile. We'll add distribution Targets later.

### Turn off Thumb

Uncheck "Compile for Thumb". It usually leads to slower performance on the iPhone/iPod if you are using floating point computations a lot. And that usually is the case when you use a physics engine.

Thumb is not always slower, nor is the difference always a big one, so you might want to play around with this setting and make some performance tests specifically for your game. But in general it is good advice to turn Thumb off on iPhone/iPod but turn it on for iPad targets.

Yes, for the iPad Thumb code is actually faster and in almost all circumstances. We'll come to that later when we setup an iPad Target.

### Turn on Precompile Prefix Header

We want our Prefix Header to be precompiled. This speeds up compilation time of your code. But only if you follow the advice to not put any of your own headers in the Prefix header, only 3rd party headers like the ones from cocos2d or the iPhone SDK.

In general don't add headers to the Prefix Header which change frequently. If you happen to have a header in your project that rarely changes and you need it in a lot of places then you can add that to the Prefix Header. But that should be the only exception.

### Warnings to the Rescue!

Warnings are an essential tool for programmers. I always write warning-free code. I'm not just being pedantic here, there are good reasons to always treat warnings as errors. [Stephan Bergmann from the OpenOffice group sums it up very nicely](http://www.mail-archive.com/dev@openoffice.org/msg01731.html):

**(quote)**

1. Most warnings are a hint, that either part of the code is not completely "thought to the end" or something in the depending code has changed or they show inconsistencies. While such occurrences are not always bugs themselves, they show potential problems, that well may occur after the next code change.

2. Warnings are an important source of information. If the mass of warnings is not fixed, the really important ones can not be found in the crowd.

3. A huge number of warnings is an indicator for not robust enough code.

4. We found, that the warnings of gcc give the most positive sensible and the least false positive results. Therefore we choose that as the warning set to orientate for.

5. The daily practice of many software engineers shows that it is quite manageable to write warning free code. Like any habit, after getting used to it, it does not cost any significant additional time in daily work.**(end quote)**

So you may or may not agree with me here. It's your choice really but please consider the above argument. In any case i'm now going to describe the changes i always make to the Warnings section and what the effect of each setting is:

**(1) Check Switch Statements: on**

This will warn you if you have a switch() with an enum but you did not provide a case statement for all values in the enum. It reminds you to either add the missing enum value or add a default case. This is a very useful warning because at least to me it happens frequently that i add some value to an enum but forget to handle them in one of the switch cases.

**(2) Implicit Conversion to 32 Bit Type: on**

Warns you when you assign a 64 bit value to a variable that can hold only 32 bits. Typical case is assignment of a double to a float. You can fix the warning by casting the double to float:

double d = 1.0208028506863;

float f = (float)d;

It is a reminder that you're losing precision in the process. That may be ok in almost all cases for games but i still like to have it on just in case.

**(3) Missing Braces and Parantheses: on**

Warns you if you have a set of nested if/else statements without braces and there may be confusion to which if statement an else branch belongs to. It's very useful if you do not follow the good advice to always put braces around every block of code, if one-line if/else statements. Personally i always add braces so this warning has no effect on me but i guarantee it will be enlightening to you if you don't always use braces.

**(4) Missing Fields in Structure Initializers: on**

If you initialize a struct but forget to set a value it will warn you about it. This is similar to Check Switch Statements in that it reminds you that you'll have to update your struct initializers when you changed the struct itself, especially if you add a new value at the end of the struct. The following code will generate the warning:

struct s { int f, g, h; };

struct s x = { 3, 4 };

**(5) Sign Comparison: on**

This warns you about assignemt of an signed value to an unsigned variable. The problem here is that if the signed variable is negative and you assign that to an unsigned variable, the resulting value will be positive and very, very large. You don't want that to ever happen in your code.

**(6) Treat Warnings as Errors: on**

Every good programmer writes warning free code. 'nuff said.

Forces you to fix your code before problems run rampant.

**(7) Undeclared Selector: on**

Requires you to declare all @selector() methods before using them. This avoids the common issue of your code crashing because a selector that was supposed to be called isn't defined or has the wrong set of parameters. Since this crash may not be immediately obvious while debugging and can happen a long time into the game it is good advice to always declare all selectors that you're using, before using them.

### Switch to Debug Configuration

Select the Debug Configuration for the following changes.

### Debug: Optimization Level = None

In Debug builds you don't want optimized code, so set the Optimization Level to None. Why no optimization? Because it can lead to strange issues when debugging code, for example stepping through code may skip lines or values in the debugger may be shown incorrectly and can not be edited.

I have no idea why Optimization was even on for my Debug build - it really shouldn't have been on in the first place. Yes, your program runs slower. If it's really dreadfully slow without optimizations, use the release build instead. In my experience Debug builds usually aren't that much slower unless you use CCLOG or NSLog excessively. Watch your debug console, if there's a lot of lines scrolling by then that's where your debug build performance is going to. Logging is slow, so use logging with care.

### Switch to Release Configuration

Select the Release Configuration for the following changes.

### Release: Generate Position-Dependent Code

Turn on Generate Position-Dependent Code, this will speed up function calls a little.

### Release: Preprocessor Macro

This is just something i like to have around. In some cases i want to do an #ifdef RELEASE block instead of having to to #ifndef DEBUG instead which can be easily misleading if you overlook the "n" in #ifndef.

### Verify builds still work

Now would be a good time to build both Debug and Release configurations to see if there are any warnings or errors. If you did everything correctly then both build configurations should build successfully.

May 10, 2010 20:35

This is your declaration actually:

-(void) backCallback: (id) sender;

Just make sure it's in the .h file or above the @implementation section in a private interface. I like to use something like this at the top of the .m file where i declare all the private methods like so:

@interface ClassName (Private)

-(void) backCallback: (id) sender;

@end

Of course feel free to just remove the warning about undeclared selectors from the project build settings if it annoys you too much. I find it useful because sometimes, you forget to add a parameter or rename a selector and then your game suddenly crashes.