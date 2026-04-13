---
title: 'Enable ARC in a Cocos2D Project: The Step-by-Step-How-To-Guide Woof-Woof!'
url: http://www.learn-cocos2d.com/2012/04/enabling-arc-cocos2d-project-howto-stepbystep-tutorialguide/
author: Steve says
published: '2012-04-05'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

While Cocos2D is ![cocos2d-arc-failure](../../../wordpress/wp-content/uploads/cocos2d-arc-failure-280x300.png)


*compatible with ARC*, simply enabling ARC in the project’s Build Setting will throw several hundreds of errors in your face. Cocos2D doesn’t provide ARC-enabled project templates. Thus this tutorial about how to enable ARC in a newly created Cocos2D Xcode Project.

While none of these steps are overly difficult, you’ll notice there’s plenty of steps to perform. Unavoidably, and on the off chance you don’t already know, I’d like to recommend [Kobold2D](http://www.kobold2d.com/) to you if you want to write ARC enabled Cocos2D apps. Because none of the steps below, really zero, zilch, nada, niente, keine are necessary to enable ARC in Kobold2D. That’s because it ships with 15 template projects all of which have ARC enabled out of the box. And Kobold2D 2.0 with cocos2d-iphone 2.0 is just around the corner.

Self-advertisment aside, these steps are tested with cocos2d-iphone v2.0 but should also work with cocos2d-iphone v1.1 - but admittedly I haven’t tested the process with the v1.1 version. If you find anything that’s not quite working with v1.1 please leave a comment. Preferably with the solution, that’ll be awesome!

**UPDATE:** I released a video version of this tutorial:



#### Install Xcode, Cocos2D, and the Cocos2D Xcode Templates

Let’s first check that you have all the prerequisites. With iOS devices selling like Playboys in the 70s these days, there’s got to be those who haven’t gotten to install Xcode or download Cocos2D yet. And for everyone else this is a version-check and a reminder to upgrade their tools and cocos2d frequently. The latter being particularly simple if you’d been using Kobold2D. Just saying.

[Download and Install Xcode 4](https://developer.apple.com/xcode/). Now might be a good time to upgrade if you’re not on Xcode 4.2 - because there’s no ARC for you without at least Xcode 4.2.[Download Cocos2D](http://www.cocos2d-iphone.org/download)and extract the cocos2d-iphone-****.tar file by double-clicking it. The filename varies depending on the cocos2d version.- Open Terminal.app and enter:
**./path-to-cocos2d-iphone/install-templates.sh -f**

**Note:**The*path-to-cocos2d-iphone*needs to be replaced with the actual path to the cocos2d directory. For example, if you are using Safari and extracted the file**cocos2d-iphone-2.0-rc0a.tar**where Safari downloaded it, then this command should work for you:**./Downloads/cocos2d-iphone-2.0-rc0a/install-templates.sh -f**.

Note that the leading dot is essential, without it you’ll most likely get a “No such file or directory” error.The install-templates.sh script will install the cocos2d-iphone Xcode templates. You have to run this script each time you download a new Cocos2D version to make sure that newly created cocos2d projects use the latest cocos2d version.


The template files are copied to the user’s Developer directory which is**~/Library/Developer/Xcode/Templates**. This is the directory you want to browse to in Finder if you ever wanted to delete the cocos2d Xcode templates. Perhaps to remove older version files or in case the install script fails with a permission issue.

*The -f switch*forces the script to replace any existing cocos2d template files, so that you don’t get any errors should you have previously installed the cocos2d Xcode templates.

#### ARC-ifying the Cocos2D code of the Template Projects

First we are refactoring the Cocos2D code away from your project and into a static library, so that your ARC-enabled code and the non-ARC cocos2d code can work happily together. If you were to enable ARC without separating the cocos2d source code the compiler would not be very happy. The Cocos2D codebase may be *compatible* but it’s not *compliant* with ARC, meaning Cocos2D itself is not using ARC and must be compiled with ARC disabled.

The following steps are the same for all Cocos2D Xcode Project Templates. I chose the Box2D template but you can apply the same steps to any of the other templates as well.

- Open Xcode (duh!)
- Create a new project, for example by selecting from the menu:
**File -> New -> Project…** - Select the desired cocos2d Xcode Template: Box2D, Chipmunk or no physics for either iOS or Mac OS X.
![create-new-cocos2d-project](../../../wordpress/wp-content/uploads/create-new-cocos2d-project-300x202.png)

- Click
**Next**and give the new project an appropriate name and save it anywhere (but remember where).![create-new-cocos2d-project-name](../../../wordpress/wp-content/uploads/create-new-cocos2d-project-name-300x202.png)

- Build & Run the project to verify that it’s working. You never know.
- Delete the
**libs**group in Xcode. Make sure to select**Remove References**in the confirmation dialog because you’ll still be needing the files later on, so don’t trash them.![delete-libs-group](../../../wordpress/wp-content/uploads/delete-libs-group-300x253.png)

- Select the Project itself in the Project Navigator. It’s the first entry with the blue document icon in the treeview pane on the left side of the Xcode window. Then click the
**Add Target**button at the bottom, just below the Project/Targets list.![select-project](../../../wordpress/wp-content/uploads/select-project-300x220.png)

- In the Add Target template dialog navigate to the
**Framework & Library**group and select**Cocoa Touch Static Library**respectively**Cocoa Library**if you develop a Mac application. Then click**Next**.![create-library](../../../wordpress/wp-content/uploads/create-library-300x202.png)

- Name the library appropriately, for example
*cocos2d-library*. Be sure to**deselect**both*Include Unit Tests*and*Use Automatic Reference Counting*.![create-library-and-name](../../../wordpress/wp-content/uploads/create-library-and-name-300x202.png)


**Warning:**Some recommend to use the**-fno-objc-arc**Compiler Flag to disable ARC on a per-source-file basis. This is only helpful if you have very few source code files which require this flag where an extra static library target would be overkill. Since you’ll have to add the flag[to each cocos2d source code file individually](http://stackoverflow.com/questions/6646052/how-can-i-disable-arc-for-a-single-file-in-a-project)- one-by-one - and there being anywhere between 100 and 150 source files, I strongly discourage going down this road. Plus it will be a maintenance nightmare whenever you upgrade cocos2d. - Once created, the
**cocos2d-library**target is selected and the*Build Settings*pane is shown. You need to navigate the*Build Settings*to make two changes to the*Search Paths*section. The easiest way to find these settings is by entering “search” to the search filter textbox in the upper right corner of the*Build Settings*pane.Set the

**Always Search User Paths**setting to**Yes**and set the**User Header Search Paths**to the somewhat cryptic**./****string.![enter-header-search-path](../../../wordpress/wp-content/uploads/enter-header-search-path-300x262.png)

**Note:**You can edit the**User Header Search Paths**setting in two ways, one by clicking it twice with a delay between the clicks - this allows you to enter the text directly. Alternatively you can double-click the field which brings up an additional dialog with a checkbox in it. In that case, either enter just a dot and click the checkbox, or enter the full string**./****but do not check the checkbox. Otherwise you might end up with the string**./**/****which will cause compiler errors. Be sure to verify the string is correct after the edit dialog closes, since Xcode might change the string depending on whether the checkbox is checked.**Warning:**The search path**./****is a quick & dirty short-hand for “search the project’s folder and all of its subfolders recursively”. This works fine as long as any header file you create or add to your project does not have the same name as a header file in the**libs**folder. For example, you must not add a header file named CCNode.h to your project, because the compiler will be confused which CCNode.h to use - the one from your project or the one provided by cocos2d-iphone. This applies to all files in the path, including those that aren’t referenced by the Xcode project. - Select the original target of the project. That means the one that was already there, the one that’s building your app, not the
*cocos2d-library*target you just added. Select the**Build Phases**tab and expand the*Link Binary With Libraries*list.![build-phases-add-link-library](../../../wordpress/wp-content/uploads/build-phases-add-link-library-300x262.png)

- Click on the
**+**button at the bottom of the list, select the**libcocos2d-library.a**file and click the**Add**button. This will link the cocos2d library code to your project’s target.![select-cocos2d-library](../../../wordpress/wp-content/uploads/select-cocos2d-library-260x300.png)

- Now it’s time to re-add the cocos2d files. Use
**File -> Add Files to “name-of-project”…**to bring up the file dialog. Navigate to and select the**libs**folder. Make sure the*Destination*checkbox is unchecked and the*Create groups for any added folders*radio button is selected. Finally verify that the*cocos2d-library*target is the only target whose checkbox is checked before clicking the**Add**button.![re-add-libs-group](../../../wordpress/wp-content/uploads/re-add-libs-group-300x220.png)

- Build and run to make sure everything works now that the cocos2d code was separated into a static library.

#### Enabling ARC in your project

Now that the cocos2d code is separated from your project’s code, you can use the built-in Xcode ARC conversion tool to update the project template code to use ARC. This will also enable the appropriate Build Settings.

- From the Xcode menu choose
**Edit -> Refactor -> Convert to Objective-C ARC…**. This brings up a dialog where you can select the targets to convert. Select only your app’s target but**not**the cocos2d-library target. Then click on**Check**.![select-target-to-convert](../../../wordpress/wp-content/uploads/select-target-to-convert-300x202.png)

- Xcode will build your code with ARC enabled and then present you with a wizard that helps you convert the project’s code to ARC. Read the text and click
**Next**.![convert-to-arc-intro](../../../wordpress/wp-content/uploads/convert-to-arc-intro-300x202.png)

- Xcode will show a dialog that allows you to review the changes it is about to make. You can safely accept all of these changes.
![arc-convert-compare-changes](../../../wordpress/wp-content/uploads/arc-convert-compare-changes-300x156.png)

- Build, run and rejoice: Your project’s code is now ARC-enabled!

#### Cleaning up (optional)

When you created the cocos2d-library target it also added three source code files to the project that you don’t need. You can safely delete (trash) the cocos2d-library group and all the files in it.

You only need to make a small change to the Build Settings of the cocos2d-library target. Locate the **Prefix Header** Build Setting, select it and press the Delete key so that the **Prefix Header** setting is empty. Alternatively just keep the prefix header file and only delete the two other files (cocos2d-library.h and .m).

#### Enjoy your ARC, WOOF, WOOF, GRRRRRR!

This should make it straightforwd for everyone to enable ARC in a Cocos2D project. Of course you can always just get [Kobold2D](http://www.kobold2d.com/) and not concern yourself with these nasty technical things at all.

I hope you enjoyed this tutorial. Please leave a comment if you found any discrepancies, specifically since newer cocos2d or Xcode versions might behave slightly different. I’d also appreciate it if you’d tweet, like or plus-one this article if you liked it. Thank you!

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

I cannot get this static cocos2d library target to work with a project created using the Cocos2d V2.1 Box2D template.

After following your tutorial the result is a project that builds without errors, but CRASHES HARD when run in the iOS 6.1 Simulator. I get the following error logged in the console:

-cocos2d: animation started with frame interval: 60.00

-cocos2d: surface size: 480×320

-Add sprite 240.00 x 160

-[CCPhysicsSprite setPTMRatio:]: unrecognized selector sent to instance.

-*** Terminating app due to uncaught exception ‘NSInvalidArgumentException’, reason: ‘-[CCPhysicsSprite setPTMRatio:]: unrecognized selector sent to instance 0xb52b210’

The only thing I did differently was from Sara Smith’s similar youtube tutorial. I moved the old libs folder out of the MainTarget and into the Cocos2dLibs Target directory. In the Search Paths Build Settings under the MainTarget, I had to modify User Header Search Paths to “Cocos2dLibs/libs” (it was “MainTarget/libs”). If I do not make this change, I get a Lexical or Preprocessor Issue ‘Box2D/Common.b2Settings.h’ not found error.

Also had to change Header Search Paths to “Cocos2dLibs/libs/kazmath/include” (it was “MainTarget/libs/kazmath/include”).

Prior to following the tutorial, for setting up the Cocos2D library as a static library, the project would build and run without crashing or errors in the simulator..

I am hoping, and I stress hoping, to set this project up with Multiple build targets with app code ONLY in the primary Target. All app code will be identical for all targets, with only the resources different (sharing same file names) within each target. I don’t want any Cocos2d library code in the MainTarget at all. I want to keep it all in the Cocos2dLibs target.

That is my main reason for attempting to make Cocos2d a static library. So that I don’t have the cocos2d code being duplicated each time I make a new build target. Being able to use ARC is a secondary reason.

Do you have any idea what could be causing this weird [CCPhysicsSprite setPTMRatio:] error?

By the way Steffen, your stuff is awesome, I wish I was as smart as you!

I created a Breakpoint for All Exceptions. The exception is raised in HelloWorldLayer.mm. In this class, init method is called, which in turn calls addNewSpriteAtPosition method. The exception is raised in that method, at the line [sprite setPTMRatio:PTM_RATIO];

HelloWorldLayer is trying to set the PTMRatio property within CCPhysicsSprite and this raises an exception causing the crash. I am assuming HelloWorldLayer cannot find CCPhysicsSprite for some reason..

Check if and when CCPhysicsSprite deallocates. Also make sure you set deployment target to iOS 5.0 or higher and replace any use of __unsafe_unretained that Xcode might have added with __weak.

If the setPTMRatio selector tries to set something on the b2Body without it being initialized this would also crash.

I am completely lost. I got a new Mac and tried to move my project over and after a few other teething problems I had to copy the code itself over into a new template project. Works 100% fine until after 2mins it crashes with what I could only attribute to ARC memory issues (exc bad access). Since I installed xcode and cocos from scratch I thought following this procedure should get rid of it. Unfortunately xcode 5 does not have exactly the options your screenshots show. I will try again assuming I did sth wrong along the way, but is it correct to assume that if my game performs certain steps fine several times but crashes on the same step later that this is memory/arc related? What is the best way to check? Thanks a lot and sorry for what may be a noob question.

First: enable exception breakpoint in Xcode. This will point you to the (nearest) line of code of the exception.

Enabling zombie objects might also help.

Things to be wary of in ARC: don’t use the __unsafe_unretained keyword. If you find any uses of it, replace it with __weak (or ‘weak’ in properties). Bridge casting is also important to get right, and can be inherently unsafe in some uses. For example cocos2d’s CCCallFuncND with its void* data parameter should not be used in ARC, instead use a CCCallBlock.

I followed all the steps. Now the static library name libcocos2d-library.a remains red. And while building linker error -lcocos2d-library not found. This is on xcode 5, IOS sdk 7, mountain lion. Please help.

Got it, The only thing that I had to do was set “$(ARCHS_STANDARD_32_BIT)” in the Architectures section.

Thanks

I went through this exercise and got everything working, but the problem I am seeing is that using the library cause a memory leak — slow continuous growth in the memory footprint.

The same code using all the cocos2d files directly (and having to mark them non- arc) cause no such growth in memory.

The use of the library also makes instrumentation on actual devices problematic. I can only run instrumentation in the simulator, again this doe snot happen when I just use the cocos2d source files.

I had the same problem. I downloaded cocos2d-iphone-2.1.tar.gz and installed, created a new project with the cocos2d iOS withBox2D, then changed to ARC as per the instructions per Steffen. Then I had the same problem.

I could fix it by changing in the ccConfig.h CC_ENABLE_BOX2D_INTEGRATION from 0 to 1, since it is not enabled by default.

Not strictly relevant to the question, but one might get some use of it…

I was struggling a bit with more actually changing the project as per Steffens’s guide, because when creating a static library in XCode5 it does not have the unit testing and enable ARC checkboxes. I had to change manually in the build settings of the cocos2D-library in Apple LLVM 5.0 - Language - Objective C section the Objective-C Automatic Reference Counting from Yes to No.

Then I could do all the rest properly. I do not exactly remember at what point I did this, but I think just after creating the library - it was created with ARC enabled as default.

By “same problem” above I mean what was the original question on setPTMRatio crash.