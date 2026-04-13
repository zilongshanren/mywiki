---
title: Learn & Master Cocos2D Game Development
url: http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/13483-getting-our-project-template-to-build-minimal-cocos2d-code/
author: Carl says
published: '2010-12-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[Tutorial: cocos2d Xcode Project](http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/): Getting our Project Template to build minimal cocos2d code

#### Search my cocos2d for iPhone FAQs & Tutorials

*Please note that the blog search in the upper right corner doesn’t search my FAQs and Tutorials.*

- Note: please do not share direct download links to PDF files, the download links expire after a couple minutes!

We still only have an OpenGL ES application in our project. In the following steps you'll learn how to change this into a cocos2d Project Template much like the "HelloWorld" application. Finally we'll clean up the remaining files from the Open GL ES application.

### Create a temporary Project from cocos2d Project Template

Create a cocos2d Project from the template above (no physics engine) and name it any way you want.

We need this cocos2d Project Template so we can copy some files from it. You can later remove that project.

### Recreate the cocos2d AppDelegate

The first thing we're going to do is to recreate the AppDelegate code. I know this explanation isn't going to be very visual and i can't really help with images here. What we want to do in this step is to copy all the content of the xxxAppDelegate files from the newly created cocos2d Project to our project's xxxAppDelegate files, but we want to keep our xxxAppDelegate's class name so we'll have to rename the class afterwards.

Open our project's xxxAppDelegate.h file and remember the class name or copy it to a temporary place, for example a text editor.

In the cocos2d Project you've just created, open the xxxAppDelegate.h file, select all of the content in the file (Command+A) and copy it over to our xxxAppDelegate.h file, overwriting everything that was in there before. Do the same with the xxxAppDelegate.m file. When you're done, the xxxAppDelegate files in our Project should be exactly the same as in the cocos2d HelloWorld project.

*Alternatively you could also delete the AppDelegate files in our project, and add them from the cocos2d project while making sure that "Copy items" is used.*

Next you should change the AppDelegate class names in our xxxAppDelegate files. Rename the class name and the #import "xxxAppDelegate.h" line in the xxxAppDelegate.m file just like it was before.

### Fix main.m to load our AppDelegate

Select main.m from the Groups & Files pane. It doesn't yet reference any AppDelegate. See the next step.

### Tell UIApplicationMain what our AppDelegate's name is

Here i've replaced the fourth parameter nil with the name of the AppDelegate in my project. Note that the AppDelegate's name will be different in your project. Make sure you use your AppDelegate's name here!

Make sure you get the class name correct and don't append .h or .m otherwise the app will not start up and you'll be left with a blank, black screen when you start the app later on. If this happens to you, and any breakpoint set in applicationDidFinishLaunching: seems to be ignored, then chances are your AppDelegate is named incorrectly in the UIApplicationMain method call here.

### Add the HelloWorldScene class

Right or control click the Classes group and choose to Add Existing Files.

Locate the HelloWorldScene.h and .m files of the cocos2d project.

### Copy the HelloWorldScene.* files

In this dialog make sure that "Copy items ..." is checked, then click Add. You will now have the HelloWorldScene class files in your project.

### Delete some unneeded files

Delete the files and groups highlighted in the image from our project. Make sure you remove the groups, this will also remove the contents of the group. That is what we want.

### Move these files to the Trash

When you're asked to "Delete References" respond by clicking the "Move to Trash" button. We really don't need these files anymore.

### Add required Frameworks

We need to add some specific Frameworks to our project needed by cocos2d. Right or control click the Frameworks group and select Add --> Existing Frameworks.

### Select Frameworks from the List

Our project already contains references to the frameworks for QuartzCore, OpenGLES, UIKit and Foundation. In addition we need to add the following frameworks:

**AudioToolbox.framework****AVFoundation.framework****CoreGraphics.framework****OpenAL.framework****libz.dylib**

The dialog shown in the image allows you to select multiple items at once.

**Important:** to locate the **libz.dylib** you'll have to scroll down to the very bottom of this list. Don't forget to add this file too. And make sure you don't accidentally select libz.1.dylib.

### List of Frameworks

For reference, here are the frameworks we need in our project.

### Add missing resources

We now add the missing resources from the cocos2d HelloWorld project. We'll do that by adding the "Resources" folder from the cocos2d project. Do the usual. Right or command click the Resources group and select Add --> Existing Files despite the fact that we actually want to add a whole folder.

### Select the Resources Folder

Browse for the cocos2d HelloWorld project select the Resources folder. This time we'll add the Resources folder itself because it contains all the files we need, and our project doesn't have a Resources folder yet.

Note: if it says "can't add group" then check your project folder if there is a subfolder named "Resources". If so, delete it and try this step again.

### Make sure to "copy items"

Again, make sure that the "Copy items" checkbox is checked.

### Verify Resource group exists

Verify that the Resources group was added and contains these files.

### Remove Info.plist from build

We don't want or need our Info.plist file in the app. Select Info.plist and uncheck the checkbox.

### Set our Target to use Info.plist

Right or control click on our Target and choose "Get Info". Switch to the Build tab. Make sure that "Configuration" is set to "All Configurations" and "Show" to "All Settings". Enter "plist" in the search box. You should see something similar to the image above.

Modify the Setting "Info.plist File" so that it reads "Resources/Info.plist". Make sure you enter it as shown including the path to the Resources folder and upper/lowercase must be correct. Meaning: don't name it "info.plist" or "INFO.plist".

Close the Info dialog.

### Add cocos2d.h to the Prefix header

Select the xxxx_Prefix.pch file and add the line to the #ifdef __OBJC__ section:

**#import "cocos2d.h"**

This is not strictly necessary, and the cocos2d project doesn't have that either. But it will build our code a little faster and you never have to import the cocos2d.h header anywhere anymore. You can read up on [Wikipedia about Prefix Headers](https://en.wikipedia.org/wiki/Prefix_header) if you want to know more.

...

I know what you're thinking now, why not add ALL headers to the Prefix.pch file? The general advice is not to add headers of your own project to the Prefix file because if you do that you'll actually see an increase in compilation time! Because any change you make to one of your header files which is included in the Prefix.pch will cause your whole project's source code to recompile! So don't add your own header files to the Prefix.pch. However, you are encouraged to add any 3rd party headers to it, that's what the Prefix.pch is for.

### Build & Run

The code should now build successfully and run in Simulator. You'll see something similar as above. Well done!

You can now delete the temporary cocos2d HelloWorld project we created. We don't need it anymore.

April 26, 2010 05:47

Like a Boss! This was fantastic. Well done and well illustrated. If all tutorials were this visual we would have a lot less problems in the forums. Thanks so much Steffen - I used the tutorial to set up my system tonight.

Peace