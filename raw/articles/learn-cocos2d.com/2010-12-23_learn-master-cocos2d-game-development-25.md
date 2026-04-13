---
title: Learn & Master Cocos2D Game Development
url: http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/13731-adding-build-configurations-for-distribution/
author: Carl says
published: '2010-12-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[Tutorial: cocos2d Xcode Project](http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/): Adding Build Configurations for Distribution

#### Search my cocos2d for iPhone FAQs & Tutorials

*Please note that the blog search in the upper right corner doesn’t search my FAQs and Tutorials.*

- Note: please do not share direct download links to PDF files, the download links expire after a couple minutes!

Every iPhone project needs two additional configurations for Ad Hoc and App Store Distribution builds. We will create these now.

### Create entitlements.plist

For Ad Hoc Distribution builds to work at all we first need to create the entitlements.plist file. Add a new file to the Resources folder and from Code Signing select Entitlements. Name the file "entitlements.plist" in all lowercase.

### Uncheck get-task-allow

Select the entitlements.plist and uncheck the checkbox for "get-task-allow". Also uncheck the file itself since we don't want it to be included in the bundle.

### Bring up Project Configurations

Select the project, right or control click and choose Get Info. Switch to the "Configurations" tab. You should see the Debug and Release configurations.

Select the "Release" configuration and click on duplicate twice.

### Rename duplicated configurations

Rename the two duplicated release configurations as "Ad Hoc Distribution" and "App Store Distribution".

### Select Ad Hoc Distribution

Switch to the Build tab and select the Ad Hoc Distribution Configuration.

### Add the entitlements file

Enter the relative path and filename to the entitlements.plist file. If you followed my tutorial it should be "Resources/entitlements.plist".

While you're there you could also change the Code Signing Identity to use the Ad Hoc Distribution profile. In this case you should not rely on the automatic selection unless you only ever use one Ad Hoc Distribution profile for all of your apps. Otherwise remember to change this setting for each new project respectively if you want to use a different Ad Hoc Distribution profile.

### Select App Store Distribution

Now select the App Store Distribution Configuration.

### Set Code Signing Identity (optional)

If you already have your App Store Distribution profile, select it here. Again don't rely on the automatic selector for any Distribution profile, you have to select your App Store Distribution profile manually and change it for every project.

Also notice that the **entitlements.plist file is not needed for App Store Distribution** builds.

### Get naked: stripping options

For App Store Distribution builds you want two things:

1) be able to debug crashlogs from your end-users

2) distribute app without debug symbols

The former should be obvious but isn't possible out of the box. The latter is just added protection against hackers or anyone who is interested in reverse engineering your code. Crackers/Pirates can't be defeated this way, since they run automated tools, you need more anti-piracy measures in code to at least defy the automated cracking tools. But in conjunction with other anti-piracy measures removing the debug symbols from the executables makes it a lot harder for crackers to bypass your anti-piracy measures. In my opinion you shouldn't expect your crack-protection to last longer than 48 hours no matter what you do, so don't spend too much time (or money) on implementing anti-piracy measures.

Accordings to [Apple's documentation about debugging crash logs](http://developer.apple.com/tools/xcode/symbolizingcrashdumps.html) we need to enable **Deployment Postprocessing (on)** and **Use Seperate Strip (on) **while unchecking **Strip Debug Symbols During Copy (off).** Make sure that **Strip Linked Product (on)** is still checked as well. The Apple document also outlines how to debug crashes using crash symbols obtained from iTunes. If you don't want to read it now, just remember that you have to keep the .dSYM file from the App Store Distribution build that you submitted to Apple. It must match the version exactly, so archive and label the dSYM file along with the submitted App so that you don't lose or overwrite it.

Note: if you don't trust your recipients of the Ad-Hoc build you can use the same settings for the Ad Hoc Distribution configuration as well.

### Ad Hoc Distribution made easy: automatically create IPA files

Whenever you build an Ad Hoc Distribution file you want to send your testers and reviewers an IPA file and not the .app file. The reason is simple: it avoids a lot of common code signing issues that may crop up when a user drops a .app file and provisioning profile into iTunes and synchs. So you'll spend less time troubleshooting those issues, and your users are happier because they can simply double-click the file to install it in iTunes. Plus it will show your App's icon in iTunes instead of the almost blank and white symbol. And since IPA files are just compressed ZIP files you don't have to zip the app anymore and your users don't have to unzip anything, which makes installing a new ad hoc build as simple as double-clicking the IPA attachment in the email you are sending to your testers and reviewers. They'll thank you for it!

To create IPA files automatically whenever you build the Ad Hoc Distribution configuration, select the desired target and right or control click. Then select Add -> New Build Phase -> New Run Script Build Phase.

### Add the Run Script Build Phase

You will see this dialog with an empty Script textbox. In that textbox paste this script here:

**if [ "${BUILD_STYLE}" == "Ad Hoc Distribution" ]; then****echo "Building IPA file from ${TARGET_NAME} for Ad Hoc Distribution";**

**PayloadDir="$TARGET_BUILD_DIR/Payload"****if [ ! -d "$PayloadDir" ]; then**** /bin/mkdir "$PayloadDir"****fi;**

**AppSource="$TARGET_BUILD_DIR/$PRODUCT_NAME.app"****AppDest="$TARGET_BUILD_DIR/Payload"****/bin/cp -R -f "$AppSource" "$AppDest"****/bin/cp -f Resources/Icon.png "$TARGET_BUILD_DIR"/iTunesArtwork**

**cd "$TARGET_BUILD_DIR"****/usr/bin/zip -r "$PRODUCT_NAME".ipa Payload iTunesArtwork**

**echo "Cleaning up my own mess..."****rm -r "$AppDest"****rm iTunesArtwork**

**echo "IPA file created: $TARGET_BUILD_DIR/$PRODUCT_NAME.ipa";****fi;**

### Script added

That's what it should look like after you pasted the script code in the script textbox. I originally got this [script from the I.COM blog](http://idotcomllc.wordpress.com/2009/05/26/how-to-build-a-ipa-file-from-xcode/). Unfortunately the script wasn't working and certainly wasn't built to be used by others out of the box. So i heavily modified the script and cleaned it up so that it doesn't break so easily and so it doesn't need to be changed whenever you create a new project or rename your targets. I also made it clean up the temporary files it creates.

Also notice that the description of the I.COM blog post as well as others all create a seperate target for building IPA files. This is absolutely not necessary and much more convenient to have the regular Ad Hoc Distribution build configuration create the IPA file automagically!

### Ad Hoc Distribution build output

When you build an Ad Hoc Distribution configuration (either iPhone or Simulator - although Simulator Ad Hoc builds don't make sense) you'll see build result output like this. Set the Output to "All Messages" to see the script's output. At the end you'll be notified about the location of the IPA file.

### IPA file in Finder

Locate the IPA file in Finder. You'll notice that it has a sweet iTunes icon and is recognized as a "iPhone/iPod touch App" by Finder. You can also see that the file size is less than the app itself because IPA files are compressed ZIP files.

### Get Ready to Deploy your App: automatic create a submittable ZIP file

To upload an App Store Distribution build to iTunes Connect you need to have your App compressed in a properly configured ZIP file. Guess what? We'll add another build script which does that for you automagically.

To create ZIP files automatically whenever you build the App Store Distribution configuration, select the desired target and right or control click. Then select Add -> New Build Phase -> New Run Script Build Phase.

### Add the ZIP Script

Copy and paste the script below into the Script textbox:

**if [ "${BUILD_STYLE}" == "App Store Distribution" ]; then****echo "Creating ZIP file from ${TARGET_NAME} for App Store Distribution / iTunes Connect submission.";**

**cd "$TARGET_BUILD_DIR"**

**if [ -a "$PRODUCT_NAME".zip ]; then****rm "$PRODUCT_NAME".zip****fi;**

**/usr/bin/zip -r -T -y "$PRODUCT_NAME".zip "$PRODUCT_NAME".app**

**echo "iTunes Connect ZIP file created: $TARGET_BUILD_DIR/$PRODUCT_NAME.zip";****fi;**

### ZIP File in Finder

Like the IPA file the ZIP file is created in the build output folder.

### Reminder: add the above Run Script Phases to all your Targets!

Repeat the above steps to add the IPA and ZIP scripts for Ad Hoc and App Store Distribution builds to all of your Targets (Lite Version Target, iPad Target, etc.). It's a simple matter of adding a Run Script Build Phase and pasting the appropriate script to each Target. It may be tedious work but you'll only do it once!

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