---
title: Learn & Master Cocos2D Game Development
url: http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/13466-download-cocos2d-source-code-from-github/
author: Shamik says
published: '2010-11-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[Tutorial: cocos2d Xcode Project](http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/): Download cocos2d source code from github

#### Search my cocos2d for iPhone FAQs & Tutorials

*Please note that the blog search in the upper right corner doesn’t search my FAQs and Tutorials.*

- Note: please do not share direct download links to PDF files, the download links expire after a couple minutes!

We will now download the latest version of the cocos2d source code from its git repository to a folder on your hard drive.

### Locate the cocos2d-iphone repository

Click on this link to [open the cocos2d-iphone git repository](https://github.com/cocos2d/cocos2d-iphone) in github, or search for "cocos2d-iphone" on github. You'll notice the "Git Read-Only" URL, copy that and keep it in the clipboard for the next step.

### Create a local directory and clone the repository

To initially download an existing repository from github, we use the "pull" command of the git tool. But first you should create an empty directory somewhere on your hard drive. You might want to name it "cocos2d-iphone" - in any case name the folder only with letters, digits, hyphen and underscore, all other characters can cause problems later on, even spaces! After that we'll download cocos2d-iphone into the new directory. These 3 commands entered in Terminal.app do this for you:

**mkdir cocos2d-iphone****cd cocos2d-iphone****git init****git pull http://github.com/cocos2d/cocos2d-iphone.git**

You should see something similar as in the screenshot above. That's it, you have successfully downloaded (pulled) cocos2d-iphone from its github repository. For subsequent updates, you only need to pull the code again.

If all you ever want to do is to be able to update cocos2d to the latest version at any time then the pull command is all you need to know.

### Comments (0)

##### Related Questions

[What are the advantages to Cocos2d from other game engines?](http://learn-cocos2d.qhub.com/57366/what-are-the-advantages-to-cocos2d-from-other-game-engines/)- 2 weeks ago[What is Cocos2d?](http://learn-cocos2d.qhub.com/57365/what-is-cocos2d/)- 2 weeks ago

Hey,

is there a guide to integrating the SpaceManager to a normal cocos2d project (one not using your template)? I am trying to do the same and am getting close to 3500 errors. many of them have been listed in the discussions here like ‘stary @ in program’ , but they havent worked for me

Thanks

Shamik

when I used SpaceManager0.0.4 it worked just fine, but with 0.0.5 I get those strange and alarmingly large number of errors, what could be the problem?

What’s the best way to branch a project’s cocos-2d?

So for example I have my cocos2d folder which I update regularly and which the project is linked to (via method in this tutorial). At some point I decide I no longer want to have the linked version of cocos2d update for this particular project. What’s the best way to go about branching that so the project’s cocos2d no longer update’s when I do that pull.

If it’s just copy/rename folder and then reconnect, what’s the list of things I have change in the project?

Thanks for all your help!

From the top of my head, I would do:

- copy and rename the cocos2d folder you want to keep (eg. name it with the version number: “cocos2d-iphone-v0.99.3″)

- in Xcode, open preferences, go to Source Trees and enter a new setting COCOS2D_SOURCE_0993 and point its path to the cocos2d-iphone-v0.99.3 folder

- in the project that you wish to keep using 0.99.3, change both (User) Header Search Paths settings to use $(COCOS2D_SOURCE_0993) as their base path instead of $(COCOS2D_SOURCE)

I think that should be it.

I have been following this very thorough… but still I am getting build errors.. CClabel not defined…

What is missing? Which step did I overlook?

Help would be appreciated!

Thanks!

Do you have this line in the implementation file (.m):

#import “cocos2d.h”

I got it to work, when I added the folder “libs” from the dummy project (temporary cocos2d project described in your tutorial), but this step is not listed, that this folder also needs to be copied… or did I miss something again?


Really helpful. Especially configuring project for Add-hoc & App Store deployment.

After completing the “Getting our project to build minimal cocos2d code” I get the following when build and run:

Undefined symbols:

“_OBJC_CLASS_$_RootViewController”, referenced from:

objc-class-ref-to-RootViewController in cocos2dTemplateProjectAppDelegate.o

ld: symbol(s) not found

collect2: ld returned 1 exit status

Hmmm … I recently made a version of the project that works with the latest beta of Cocos2D, which added the rootviewcontroller:

http://www.learn-cocos2d.com/2010/10/xcode-project-update-cocos2d-v0995-beta-3/

Which version of Cocos2D are you using?

The latest pulled by git… v0.99.5

Thanks for the link, I’ll go and try it…

It worked, thanks!

i’m having the same problem - what exactly did you do to resolve it?

fixed - the new (0.99.5) cocos2d-template adds the following files:

RootViewController.h

RootViewController.m

GameConfig.h

i just copied them, and the build worked again.

[...] weeks I have been getting approximately 75,000 errors in my project using Cocos2d. I then found this article, and set my project up that way. Works fine [...]

Any recommendations where the ‘cocos2d-iphone folder’ should go..?

I assume it can go anywhere… but would be interested to hear where people put it.

Is the Developer folder a sensible place? or should it go in my home folder somewhere?

Recently, I’ve changed it so that the reference is to “../cocos2d-iphone” which means cocos2d-iphone and cocos2d-project are both in the same folder. That allows me to copy the project and cocos2d and use seperate cocos2d versions per project. Some older projects for example really don’t need to be updated with the latest cocos2d.

err.. I don’t think you understood my question, or maybe I don’t understand how all this stuff works…

As I see it, somewhere on my hard drive there should be ‘master’ version of cocos2d. This is separate from any projects or templates (I’ve yet to install Cocos2d anywhere on my Mac).

In your tutorial you say enter the command ‘mkdir cocos2d-iphone’ but where is a good place to create that folder? The Desktop would obviously put a bad place so… where’s a good place?

Where do people generally keep their frameworks? could I add a ‘Frameworks’ folder to HD/Developer ? will that be effected if/when I update XCode?

In relation to your reply, I’m guessing this folder could have sub folders holding different versions?

thanks

Ok, I get it. Personally, I have a folder “depot” on HD where all my projects are. But by default I would say that the Documents folder is fine, especially if you add a “Documents/GameProjects/” folder or something similar. Or your user folder ~ so something like ~/GameProjects should be fine too.

I wouldn’t add it to Developer simply because it’s not supposed to contain user content. And I’ve had one Xcode/iOS SDK bug that forced me to delete Developer and re-install, because a mere re-install didn’t fix the issue.

But other than that it’s mostly a personal preference where you put your game code.

Where do you get this file, cocos2d Application.zip ?

Are you looking for the downloads?

The Xcode project files are here:

http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/13801-get-the-xcode-project-template-here/

Hi Steffen…thx for the reply. I have the files. I’m confused with the section ” Installing the file-new-project Template for Xcode”, where you say to “Unzip the “cocos2d Application.zip” file”.

Where is that file? Sorry for any confusion!

I think that I just received that file from you as an email attachment after I signed up for your newsletter.

Thanks mate, great setup, got it working for the Device.

With 4.1 there are issues building for the simulator:

To get it building on the simulator do the following:

1. Right click on the Targets -> cocos2DXrefTest

2. Click Get Info from the displayed options.

3. Click “Base SDK”

4. Select iOS Simulator 4.0 from the options.

5. Build and Harry’s your Uncle!

Regards,

Peter

Actually, you should always set the Base SDK to iOS, never Simulator. Doing so still allows you to deploy to simulator.

As a matter of fact, iOS SDK 4.2 entirely removed the Simulator SDK from the selection list because it will cause issues when deploying to the device (or may not allow building for the device at all).

Hi Steffen.

After last update of cocos2d my project is not compiled.

Please take a look on this thread http://www.cocos2d-iphone.org/forum/topic/11150

Hope you can help me.

Thanks.

I assume you’re referring to my cocos2d-project on github: https://github.com/GamingHorror/cocos2d-project

I’ve updated it to the latest cocos2d version (0.99.5 RC1) and now it also includes the version of cocos2d that I’ve tested the project with.

However, I could not reproduce the compiler errors you mentioned but I also can’t exclude that they are in some way or another related to cocos2d-project and upgrading cocos2d-iphone.

The errors seem odd though. I would try re-installing Xcode respectively the iOS SDK. Ideally, delete or rename the /Developer folder on your hard drive before doing so, to do an absolutely clean install.

hi Steffen,

managed to compile and run you template just downloaded from git hub after changing cocos2d-project “base sdk” to “iOS Simulator 4.1″ and “Architectures” set to “optimized” . this is under xcode 4 preview. Oh and compiler set to GCC 4.2 instead of LLVM 2.0

Although the projects builds and runs with no errors i am getting 2099 issues under box2d. How come? am i doing something wrong or this is normal???

why xcode 4 and not 3? since i am new to xcode I dont want to learn 3 and by then have to learn ver. 4. i know i cant submit with xcode 4 yet but until my game is done xcode 4 will probably be released!

The warnings from Box2D are normal and nothing to worry about.

Note that you should never set the Base SDK to Simulator, always set it to iOS Device even if you deploy to the Simulator. Apple removed the Simulator SDK option from iOS 4.2.

Thanks for your reply Steffen, read that in a post above you said the same thing and changed it to iOS device already

There are a million settings in Xcode don’t think will ever learn the proper use of each setting, if it compiles and runs at the moment I don’t look further

Thanks for the tutorial Steffen.

I think a few steps are needed to make this work correctly given the changes you suggest making to the AppDelegate code and differences between class naming of the view controller in OpenGLES projects vs. Cocos2D projects. When you create an OpenGLES project, the ViewController class takes on the name of the project…so, “myproject” would contain myprojectViewController.h/.m, while the cocos2D project creates “RootViewController”

If you copy the appDelegate code from the cocos2D project and paste over the OpenGLES project’s appDelegate code, the app delegate will now be referencing “RootViewController”. You will need to refactor the appDelegate so that the class is actually RootViewController and will compile successfully.

I know, I’ve already done this in the project version I’m currently using. It’s somewhat evolved than the cocos2d-project that’s publicly available. Once I have completed the project I’m working on, I’ll clean up this project and release it (replacing cocos2d-project). This will also add wax (Lua) and ObjectAL support and a few other things.

Hey, I have a problem with the loading of the cocos2D template. It does not load from the folder where I download it. There is no cocos2D project template when I want to create a new project.

Can you help me?

There’s a little confusion because I used the word “template” without knowing that this is reserved for Xcode templates, in other words the Xcode projects you can create via File -> New. My Xcode template is not that kind of template, it’s a regular Xcode project I use as a template for new project by simply copying the project file and renaming it.