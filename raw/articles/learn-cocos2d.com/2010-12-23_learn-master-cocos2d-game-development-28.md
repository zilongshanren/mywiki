---
title: Learn & Master Cocos2D Game Development
url: http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/13802-how-to-setup-the-received-xcode-project-template/
author: Carl says
published: '2010-12-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[Tutorial: cocos2d Xcode Project](http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/): How to setup the received Xcode Project Template

#### Search my cocos2d for iPhone FAQs & Tutorials

*Please note that the blog search in the upper right corner doesn’t search my FAQs and Tutorials.*

- Note: please do not share direct download links to PDF files, the download links expire after a couple minutes!

After [downloading the files](http://www.learn-cocos2d.com/) you may wonder how you get the Xcode project you received in the confirmation email to work. Don't worry, these are only a few steps you need to follow. The first, obviously, is to extract the ZIP file.

### Unzip the Project

I decided to create a cocos2d folder where i put the project and the cocos2d-iphone project in. After unzipping the file you received in the confirmation email you should see a similar folder structure.

### Download cocos2d-iphone

Refer to these [instructions on how to download cocos2d-iphone from github](http://www.learn-cocos2d.com/). Alternatively you can also download cocos2d-iphone from the website and extract it.

The important thing is that the cocos2d-iphone folder should be installed side-by-side with the cocos2d-project folder as shown above.

### Open the cocos2d-project in Xcode

You may notice that the cocos2d-iphone files are shown in red and that the project doesn't compile. You need to go through the steps outlined in the [Xcode Preferences configuration for Cross-Project Referencing.](http://www.learn-cocos2d.com/) These settings are essential for cross-project references to work. You can choose any build output folder but the Source Tree folder has to be the folder where you installed (downloaded) cocos2d-iphone to.

### Rename the Project (optional)

In the menu choose Project -> Rename. It's as simple as that. This is new functionality introduced with Xcode 3.2.

Previous Xcode versions up to Xcode 3.1 had to rely on different methods to rename a project. The easiest solution for Xcode 3.1 users (other than upgrading) is to [use the Rename Xcode Project tool](http://www.learn-cocos2d.com/knowledge-base/xcode-objective-c-faq/learn-cocos2d-public-content/manual/xcode/13436-how-can-i-rename-my-xcode-project/).

### You're good to go!

You should be able to successfully build the targets in the Project.

If you encounter any issues please leave a comment and i'll try to help.

May 9, 2010 10:46

Hi Steffen!

Your cocos2d tutorial is one of the best and the most useful tutorials I have ever seen. Thank you!

I would add section about renaming cocos2d-iphone project - it's not so trivial :)

Cheers,

Lukasz