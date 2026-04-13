---
title: Learn & Master Cocos2D Game Development
url: http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/13802-how-to-setup-the-received-xcode-project-template/13471/
author: Carl says
published: '2010-12-13'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[Tutorial: cocos2d Xcode Project](http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/): Configure Xcode for Cross-Project Referencing

#### Search my cocos2d for iPhone FAQs & Tutorials

*Please note that the blog search in the upper right corner doesn’t search my FAQs and Tutorials.*

- Note: please do not share direct download links to PDF files, the download links expire after a couple minutes!

In March 2009 [Clint Harris outlined how to setup cocos2d for iPhone using cross-project references](http://www.clintharris.net/2009/iphone-app-shared-libraries/), instead of copying the source code to every project you create. Since that article is completely outdated i decided to retrace the steps needed for version 0.99 of cocos2d engine and the current Xcode version 3.2. I've also condensed it to the necessary steps.

Apple's documentation also describes [Xcode cross-project references](http://developer.apple.com/mac/library/documentation/DeveloperTools/Conceptual/XcodeProjectManagement/130-Files_in_Projects/project_files.html#//apple_ref/doc/uid/TP40002666-CJBJHJCJ) in a short paragraph. I mention that in case you want to look that up and find that Clint's link does no longer work.

I use the cross-project solution instead of installing and using the cocos2d Xcode project templates because they, too, leave you in a situation where you'll find yourself unable to update the cocos2d engine code at a later time.

Note that the following settings need to be done only once but are required steps for the next lesson.

### Shared Build Location

Open Xcode and from the Apple menu select Preferences. Switch to the "Building" tab and set the two radio buttons as in the screenshot. Choose a build folder where you want Xcode to place all build output. It should be an empty directory.

### Define cocos2d Source Tree

Still in Preferences, click on the Source Trees tab. Click the + button to add a new setting and name it COCOS2D_SOURCE. As path enter the full path to the folder where you downloaded (pulled) the cocos2d-iphone source code. I'm afraid there's no "Choose..." button for this setting that lets you browse folders so you'll have to enter the path manually. Make sure the path is correct.

We'll refer to that COCOS2D_SOURCE variable a few times later on.

May 10, 2010 15:45

Yes, i keep getting reports of images not shown. I'm not sure what it is. I'll keep an eye on it.