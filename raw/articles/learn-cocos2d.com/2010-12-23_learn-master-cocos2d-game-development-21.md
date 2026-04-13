---
title: Learn & Master Cocos2D Game Development
url: http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/13465-install-configure-git/
author: Carl says
published: '2010-12-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[Tutorial: cocos2d Xcode Project](http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/): Install & Configure git

#### Search my cocos2d for iPhone FAQs & Tutorials

*Please note that the blog search in the upper right corner doesn’t search my FAQs and Tutorials.*

- Note: please do not share direct download links to PDF files, the download links expire after a couple minutes!

This lesson will guide you through the installation process for git but just what is necessary to obtain the cocos2d source code. Installing git is already well documented by the folks at github so i'll often refer to their instructions but i've condensed it to the absolutely necessary information so that you can race through that process a lot quicker.

### Create GitHub account

You want a free account, so use this link to [sign up with github for free](https://github.com/signup/free). While you are waiting for the github confirmation email you can continue with the next two steps which don't require you to have a github account.

### Download and Install Git Package

[Click this link to download the latest git version.](https://code.google.com/p/git-osx-installer/downloads/list?can=3&q=&sort=-uploaded&colspec=Filename+Summary+Uploaded+Size+DownloadCount)

You'll see a list of downloads like above but version numbers may differ. Just pick the topmost file, mount the .dmg and install the package (.pkg file).

### Generate SSH keys for Git

Generating an SSH key may seem daunting at first. It's not that bad. Just follow the instructions and type into Terminal what is displayed on the screenshots of the GitHub instructions.

If you know that you don't have an SSH key yet i've recreated the command sequence here for your convenience. Open Terminal.app and simply replace your e-mail address with the one you signed up with on github:

**cd ~/.ssh****ssh-keygen -t rsa -C " [email protected]"**

**cat ~/.ssh/id_rsa.pub | pbcopy**

The last command puts the SSH key into your clipboard. If you overwrite your clipboard contents just re-enter the first and last command into Terminal.app.

### Add SSH key to your git account

Login to your github account and [go to your account settings](https://github.com/account).

Click on the SSH Public Keys button.

### Paste your SSH key

Paste your SSH key into the text-box labelled "Key". Title is used to identify your key in case you have many, enter any text you like. Then click "Add key" and you are almost done.

### Configure git with username & token

There are a few settings git requires. Enter the commands below in Terminal.app and replace YOURLOGIN with your github login and e-mail address. Your API Token is shown on your [Account Settings](https://github.com/account) page on the right hand side when you are on the "Account Overview" Tab. Copy the token and paste it below instead of YOURTOKEN. If you ever change your github password, you have to update your token as well.

**git config --global user.name "YOURLOGIN"****git config --global user.email " [email protected]"**

**git config --global github.user YOURLOGIN**

**git.config --global github.token YOURTOKEN**

That's it. You're ready to use git!

If you're having trouble with this step, refer to the [instructions on github to setup your name, email and github token.](https://help.github.com/git-email-settings/)

I get “cocos2d.h:No such file or directory” when trying to #import “cocos2d.h”

what am I missing?

ups, the path to the source code was wrong.

This tutorial is toooo long.

Is there a short version ? I spent two hours on this and as I expected nothing works.

For begininers its not going to work

Great info! Thanks! However, the script is building the .ipa file before it does the codesign step. Have things changed in Xcode? How do I get the script to run after the codesign step?

I tried twice to follow your tutorial step by step using cocos2d 0.99.5-rc1, Xcode 3.2.5 and iOS 4.2.1, but I keep having problems when building and running on device.

The weird thing is I have no problem at all running the template on simulator!

To be more clear:

I’m trying to build and run following the final step of “Getting our Project Template to build minimal cocos2d code” section.

Running on simulator works perfectly, running on device (iphone4) crashes after splash screen with this message on console:

“Program received signal: “EXC_BAD_ACCESS”.

warning: Unable to read symbols for /Developer/Platforms/iPhoneOS.platform/DeviceSupport/4.2.1 (8C148)/Symbols/Developer/usr/lib/libXcodeDebuggerSupport.dylib (file not found).

Previous frame inner to this frame (gdb could not unwind past this frame)”

By stepping with debugger I found the app crashes on line 98 of AppDelegate.m:

“// make the View Controller a child of the main window

[window addSubview: viewController.view];”

I see there are little differences from your (great) tutorial and Xcode/cocos2d new templates, mainly for the use of RootViewController, may this crash be related? (I already added RootViewController.* to my template)

Has anyone found a fix to this problem?

Please please please help me, this thing is driving me crazy =/

Thanks

It might be related. Have you tried the version on github? https://github.com/GamingHorror/cocos2d-project

That version is tested with 0.99.5

But I recently started getting those “could not unwind” errors … I was able to fix them by changing the compiler in all referenced projects back to GCC.

Bingo!

Thanks a lot, you point me to a fix.

I had already tried with your latest github version, without luck.

I followed your suggestion, changing the compiler to GCC 4.2 on all projects (both cocos2d-project and cocos2d-ios) and it worked!

I suppose the problem was in compiler setting for cocos2d-ios, it was set to LLVM compiler 1.6.

If I set compiler to different version for the two projects, I always get that crash, when using same gcc version, everything is ok.

I tried also with LLVM GCC4.2 on both projects and it works too.

Probably I never met this problem since using cocos2d built-in templates everything get compiled using gcc without further setting.


Thanks a lot for your tutorials… and for fast replying too

Hi Steffen

To upgrade a project created with your template from e.g. 0.99.5 rc1 to the final 0.99.5 I just need to copy over the cocos2d-IPhone folder?

I would assume yes but thought of asking since it does not clearly covered in the main points/links at the top of this tutorial

Correct, although you should keep a copy of the old folder just in case.

I receive a lot of EAGLView may not respond to …xxx warnings, and I believe these are the undeclared selectors you are mentioning in your comment. How can I fix it? Only with turning off the treat warning as error option or also by changing the code?

I didn’t understand where to implement the code from your comment on this tutorial.

BTW, the entire tutorial is really great!!

If you get these errors then it’s because the EAGLView has changed in the latest cocos2d version. It should work with the cocos2d-project that you can get from github: https://github.com/GamingHorror/cocos2d-project

Hi

1st: GREAT job on this PDF. Realllly appreciated.

I just did the first part up to Helloworld with the 99.5 version. (up to page 43 of pdf)

You might want to update a bit, the part where we get the AppDelegate from Helloworld sample : since in 99.5 Cocos changed the samples so that for exemple main.m does not exists main() is in the delegate.m file.

Continue the great work.