---
title: Kobold2D Compatibility Update for iOS 6
url: http://www.learn-cocos2d.com/2012/09/kobold2d-compatibility-update-ios-6/
author: Jose Ortega says
published: '2012-09-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

** Kobold2D v2.0.4 is now available for download**, as is v1.0.3.

Both versions contain compatibility fixes for iOS 6, Xcode 4.5, Mountain Lion and a few extra features like (finally) Kobold2D Class Templates for Xcode.

##### The Most Important Changes & Additions

- fixed: iOS 6 initial rotation issue
- iPhone 5 widescreen enabled in all template projects
- Existing projects must add a
image with size of 640×1136 pixels to their project to enable iPhone 5 widescreen support.[[email protected]](http://www.learn-cocos2d.com/cdn-cgi/l/email-protection)

- Existing projects must add a
- Mountain Lion: no need to lower security level to run Installer. Package is now signed by “identified developer”.
**NEW**: Kobold2D Class Templates available in Xcode.- Use as basis for new CCNode class files. Includes stubs of frequently used methods: init, onEnter, cleanup, dealloc, update.


- added C function
`isWidescreenEnabled()`to report if app is running on a widescreen device with widescreen “enabled” (ie when running on iPhone 5 and[[email protected]](http://www.learn-cocos2d.com/cdn-cgi/l/email-protection)is included in the project) - added CCNode category methods:
`removeChildrenInArray:(id<NSFastEnumeration>)childArray cleanup:(BOOL)cleanup`(removes the children of the given array)`setPositionRelativeToParentPosition:(CGPoint)pos`(positions child node relative to parent’s position, instead of lower-left corner of parent’s texture - call with CGPointZero to center node on parent)




|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

“Kobold2D” couldn’t be copied because you don’t have permission to access “File Templates”.

This is what I get using the 2.0.4 installer. May be possible to install the templates manually?

This may occur if you have installed cocos2d templates with sudo into user folder, back when it still allowed to do that. You could delete (or rename) the File Templates folder, then install cocos2d, and copy the remaining files you need back in.

Or simply change permissions of File Templates folder and all contents. The path is: