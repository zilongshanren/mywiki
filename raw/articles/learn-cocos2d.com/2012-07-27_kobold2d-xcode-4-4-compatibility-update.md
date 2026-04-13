---
title: Kobold2D Xcode 4.4 Compatibility Update
url: http://www.learn-cocos2d.com/2012/07/kobold2d-xcode-44-compatibility-update/
author: Giovanni says
published: '2012-07-27'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I just released a [compatibility update for Kobold2D](http://www.kobold2d.com/display/KKSITE/Kobold2D+Download) since there were numerous compiler warnings and errors introduced in Xcode 4.4.

Almost all of the issues were simply the compiler being more adamant about using the correct type specifiers in format strings. For example using %i for an unsigned integer or %u for an unsigned long type would bring up warnings. The solution is to use either the correct format specifier or casting the value. The latter is preferable if the underlying type changes depending on the platform. For example NSUInteger is unsigned int for iOS but on Mac 64-Bit it’s actually unsigned long.

You can get the updated Kobold2D v1.1.2 and v2.0.3 versions from the [Kobold2D Downloads page](http://www.kobold2d.com/display/KKSITE/Kobold2D+Download).


#### About Xcode Analyzer Reports

On a related note, if you run the Xcode analyzer it will report dozens of, well, reports. They aren’t really warnings or issues, but suggestions for code that you might want to take a look at because it might be a potential issue. The analyzer is more thorough than the compiler, which also causes it to report many false positives respectively it points out things that really aren’t an issue. Not all of these reports need action. In fact those that are still being reported in Kobold2D are very likely of no concern.

For example this code will cause the analyzer to report that the value for “pos” is never read:

|
1 2 |
CGPoint pos = [self getPos]; [self setOtherPos:pos]; |

Well, the analyzer is correct, and yet it isn’t. It would probably shut up if we wrote self.otherPos = pos. But it’s not a problem to create a temporary variable or to use Objective-C messaging instead of dot notation. In fact in many cases temporary variables can improve readability, and dot notation is technically identical. There are many more analyzer reports that are borderline pointless, like the singleton instance object that may be a memory leak because it’s never released. By definition a Singleton is never released from memory until the app is shut down.

If you use the analyzer, you can safely ignore all the reports from the libraries. Only consider the reports that point to your code.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Thank you very very much![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


Regarding the analyzer false positive example with “CGPoint pos”, the analyzer should actually not warn about this. If you are seeing this, it is a bug in the analyzer, and not intended behavior. Are you still seeing this behavior in Xcode 4.5? If so, please file a bug report (e.g., http://clang-analyzer.llvm.org/filing_bugs.html).

It would be great if people filed more bug reports about these kind of issues, as that is the only way the analyzer developers can know about them to fix them. If some warnings are borderline pointless, they’d like to hear *specific* feedback about those issues as well.