---
title: Line-Drawing Game Starter Kit for cocos2d-iPhone
url: http://www.learn-cocos2d.com/line-drawing-game-starterkit-docs/
published: '2010-07-17'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Thank you for your interest in the **Line-Drawing Game Starterkit for cocos2d-iPhone**!

The Line-Drawing Game Starterkit allows you to get a headstart with your own Line-Drawing (some prefer: Path-Drawing) game. Line-Drawing games are among the most popular genres on the iPhone/iPad, do Flight Control and Harbor Master ring a bell?

Visit the [Line-Drawing Game Starterkit page](http://www.learn-cocos2d.com/line-drawing-game-starterkit/) for a list of features and latest updates.

These are seperate targets. For game developers it doesn't make much sense to use a universal binary, as your assets will most likely be very different (and much larger) on the iPad than on the iPhone/iPod. If you are 100% sure you'll only target just one of the two device classes you can ignore or even delete the other target and everything that is related to creating device-dependant code.

The iPad target is set to "Compile for Thumb". This is the optimal setting for the iPad, Thumb code for the iPad's ArmV7 CPU also optimizes floating point math and does not cause slowdowns as Thumb for iPhone. In fact, code compiled for Thumb on iPad is actually faster in almost all aspects than without Thumb. To recoup: compile for Thumb for iPad Apps in general, do not compile for Thumb for iPhone/iPod Touch Apps if you're using floating point math a lot, eg if you're using a physics engine.

Use the following Preprocessor Macro to compile code depending on device:

#if TARGET_IPAD // iPad specific code goes here #else // iPhone/iPod Touch specific code goes here #endif

The Resources folder has 3 sub-folders: iPhone & iPod Touch, iPad and shared. Please make use of them to place your device-specific resources in the appropriate place and make sure when adding resources to only add them to the respective Target. If you are not careful with this at best the Apps will contain unneeded resources, at worst it will crash because a resource could not be found.

The class [AssetHelper](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_asset_helper/) allows you to use the same filenames for both iPhone/iPod and iPad builds if you stick to the naming convention of appending "-ipad" to all iPad assets. Call this method to get the correct filename depending on the device:

This will load the file "myfile-ipad.png" if you compile an iPad Target, otherwise the filename remains unchanged.

The Starter Kit has 4 Build Configurations:

The Distribution configs are the same as release, except that you can and should use the respective Ad-Hoc and AppStore Distribution Profiles with these configs. That way you always know which profile was used to build the target.

Note: the AppStore build automatically creates a zipped version of your App. But sometimes the iTunes Connect website won't accept these zip files for whatever reason. In those cases it helps to manually compress the app and use that .zip file instead.

What are ".IPA" build targets?

These targets create an iTunes .IPA file of your App with the App's Icon included.

Purpose: it makes sharing Ad-Hoc Distribution builds easier and less painful. A lot of people have issues getting .app files to work with their iTunes or iPhone, especially on Windows machines. IPA files are painless because they avoid a lot of the common issues (signing errors and what not) and can be installed to iTunes by simply double-clicking them.

How to use: first, build your Ad-Hoc Distribution version as normal. Once complete and you have verified that the build is working, switch the target to the corresponding .IPA target and build again. It will zip your .app file and output an .IPA file in the respective build folder. You can then use that .IPA file to send to your friends and testers instead of the .app and save yourself and your testers some trouble. Remember to switch target back to a normal build once you've built the .IPA file.

The original script to create .IPA files was obtained from: [http://idotcomllc.wordpress.com/2009/05/26/how-to-build-a-ipa-file-from-xcode/](http://idotcomllc.wordpress.com/2009/05/26/how-to-build-a-ipa-file-from-xcode/)

You can set the iTunes Supported Languages list comfortably by adding or removing supported languages to this [file:](http://file://) iTunesSupportedLanguages.strings

Refer to iTunesSupportedLanguages.strings file documentation for more information.