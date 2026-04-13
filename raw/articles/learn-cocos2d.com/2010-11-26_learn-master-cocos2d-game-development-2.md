---
title: Learn & Master Cocos2D Game Development
url: http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/13469-get-the-latest-version-of-cocos2d-iphone/
author: Shamik says
published: '2010-11-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[Tutorial: cocos2d Xcode Project](http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/): Get the latest version of cocos2d-iphone

#### Search my cocos2d for iPhone FAQs & Tutorials

*Please note that the blog search in the upper right corner doesn’t search my FAQs and Tutorials.*

- Note: please do not share direct download links to PDF files, the download links expire after a couple minutes!

As a reminder, here's how to update cocos2d to the latest version.

### Get the latest version of cocos2d-iphone

To update the cocos2d-iphone source code to the latest version, change to the directory where you initially downloaded cocos2d-iphone and enter in Terminal.app:

**git pull http://github.com/cocos2d/cocos2d-iphone.git**

It's the same command you used to initially download the source code.

### Warning: updating cocos2d-iphone may break your code in unexpected ways!

Just a heads up: when you pull a new cocos2d-iphone version from the git repository there's always a chance that changes made to the engine will break your code. Actually, that is very likely to happen. There may be functions removed, parameters added, variables renamed and plenty of other things changed that may cause your code not to compile. Even if your code compiles the changes to the cocos2d engine may introduce strange bugs and weird behavior. First and foremost it is your responsibility to fix these issues, unless of course there's really a bug in the cocos2d engine itself, which can also happen. This extra work is something you have to come to terms with if you want to develop at the bleeding edge of iPhone game development.

The best strategy for you to remain a happy cocos2d-iphone programmer may seem counter-intuitive at first: pull new cocos2d-iphone updates frequently, as often as daily and before you start working on your code. Even if you don't need a specific bugfix or feature. That way, whatever may break it will most likely be very easy to identify and fix. But if you wait weeks or months before doing a cocos2d-iphone engine update, you may actually be better off not doing it at all and instead just use the cocos2d Project Templates and stick to the cocos2d-iphone version you start your project with. Just know that you'll hardly be able to benefit from the latest cocos2d engine bugfixes and features - it's the price you pay for taking the easy route at the start of a project.

There's one exception to the "update cocos2d daily" rule though: if you get close to releasing your game to the App Store, or completing the latest patch for your game, you should not pull the latest cocos2d-iphone version for a while. Especially not at the very last minute. Chances are that something might break that you'll miss but your users will find out about and give you bad reviews because of it. So while you're stabilizing your own build, one of the rules to ensure that your code remains free of bugs and weird side-effects is not to update the underlying game engine, or any code that you haven't written yourself for that matter. Even if the change to the engine may seem trivial - you never know! So wait until after the App or patch is released before you perform another engine update. And by "released" i mean released, not just submitted to Apple for review. You need to be able to quickly submit another build in case of a rejection by Apple.

### Comments (1)

##### Related Questions

[What are the advantages to Cocos2d from other game engines?](http://learn-cocos2d.qhub.com/57366/what-are-the-advantages-to-cocos2d-from-other-game-engines/)- 2 weeks ago[What is Cocos2d?](http://learn-cocos2d.qhub.com/57365/what-is-cocos2d/)- 2 weeks ago

May 14, 2010 21:33

update cocos2d daily close to release -> its git, just make a branch