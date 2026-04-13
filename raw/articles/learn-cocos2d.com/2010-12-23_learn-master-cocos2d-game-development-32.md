---
title: Learn & Master Cocos2D Game Development
url: http://www.learn-cocos2d.com/knowledge-base/xcode-objective-c-faq/learn-cocos2d-public-content/manual/xcode/13436-how-can-i-rename-my-xcode-project/
published: '2010-12-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# FAQ: Xcode & Objective-C

#### Search my cocos2d for iPhone FAQs & Tutorials

*Please note that the blog search in the upper right corner doesn’t search my FAQs and Tutorials.*

**Note:**please do not share direct download links to PDF files, the download links expire after a couple minutes!

Suppose you named your first game project "sljuslkrhflsdfls" because you never expected to finish this project. Now you want to share your code and you are rightfully embarrassed by your Xcode childhood mishap. Well, there's an App for that! :)

### Xcode 3.2 and higher

In the menu choose Project -> Rename. It's as simple as that.

Previous Xcode versions up to Xcode 3.1 had to rely on different methods to rename a project. This is outlined in the next steps.

### Xcode 3.1 or below: use "Rename Xcode Project" tool

It's a little known tool written by Michele Ferretti. It proved useful a great number of times to me. It doesn't seem to have an official homepage. Version 2.1 is the latest. Here's a list of download locations for that tool:

[http://www.macupdate.com/info.php/id/17683/rename-xcode-project](https://www.macupdate.com/info.php/id/17683/rename-xcode-project)[http://mac.softpedia.com/get/Utilities/Rename-Xcode-Project.shtml](http://mac.softpedia.com/get/Utilities/Rename-Xcode-Project.shtml)[http://www.versiontracker.com/dyn/moreinfo/macosx/26357](http://www.versiontracker.com/dyn/moreinfo/macosx/26357)[http://mac.rbytes.net/cat/mac/utilities/rename-xcode-project/](http://mac.rbytes.net/cat/mac/utilities/rename-xcode-project/)[http://download.cnet.com/Rename-xCode-Project/3000-2247_4-65144.html](http://download.cnet.com/Rename-xCode-Project/3000-2247_4-65144.html)[http://software.techrepublic.com.com/abstract.aspx?docid=499393](http://software.techrepublic.com.com/abstract.aspx?docid=499393)

Simply select the project you want to rename, and enter a new name and click Rename. If it locks up (did that to me once) just try again.

It works with Xcode 3.1 projects. It may work with Xcode 3.2 and beyond. In any case you should make a copy of your project before renaming it, just in case.

### Xcode 3.1 or below: do it manually (the hard way)

1. Copy original folder and rename copy to new name

2. Rename xCode project in the newly copied project directory

3. Delete build directory in the newly copied project directory

4. Open XCode project in the newly copied project directory

5. Edit Bundle display name in Info.plist (if it is just $PRODUCT then leave)

6. Rename target (Expand targets, control click on MyFirstGame target and select rename)

7. Select renamed target, click on info, make sure "All configurations" is selected, change "Product Name" under Packaging to new product name