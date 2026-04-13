---
title: How to Download Modified Files from a Web Server for a Cocos2D Webcam Viewer
url: http://www.learn-cocos2d.com/2012/01/download-modified-files-web-server-cocos2d-webcam-viewer/
author: Josh Jones says
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Wouldn’t it be awesome if you could update your game’s assets while your app is running? It turns out you can, and it’s not even very complicated.

Whether you want to tweak a game setting or experiment with a variety of image styles on the fly, this will be one of the things you wish you had been using all along! Either for faster development or as a design feature for your game.

In this case, we’ll build a New York Traffic Webcam viewer with Cocos2D. You will learn how to download files to your app at runtime with the iOS SDK and cocos2d-iphone, and how to check if the file on the web server has actually been modified. ![itcamefrom_night](../../../wordpress/wp-content/uploads/itcamefrom_night-300x154.png)


Along the way you’ll understand how to use the Mac OS X built-in web server to speed up your development by replacing game assets on the fly. By copying files to a specific directory on your Mac you can make immediate changes to your running app!

And you don’t need any experience with HTML, Apache, or any other web server or web services technology. In fact, I consider myself to be an web-illiterate because I’ve hardly done anything programming-related with web services and servers in the past.

As usual, the project is available from my [LearnCocos2D github repository](https://github.com/LearnCocos2D/LearnCocos2D) under the MIT License. The project’s name is Cocos2D-UpdateFilesFromWebServer. To improve readability of the article I removed error checking from the code in the article.


#### Prerequisites

All you really need is a web server and … **WAIT! Don’t quit on me just yet!** If you’re only interested in downloading files from the world wide web, you can just skip the next two paragraphs.

But if you do want to transfer files to your app to speed up development you should know that you actually have a web server at your disposal! Mac OS X comes shipped with a Web Server and all you need to do is to enable it via System Preferences. The rest is all in the code.

To test the code on your device it must have Wifi enabled and it must be connected to the same network as your computer. I’ll tell you shortly how you can verify this.

#### Enable the Mac OS X Web Server

Open System Preferences via the Apple icon in the menu bar. Under the Internet & Wireless category open ![SharingPreferences](../../../wordpress/wp-content/uploads/SharingPreferences-300x246.png)


**Sharing**.

All you need to do is to check the checkbox next to the **Web Sharing** service to turn on Web Sharing. This will enable your local web server. You can test it by clicking either or both of the links in the right half of the pane. If you click on the computer’s website link or if you enter your computer’s IP address in your web browser’s address field you’ll be greeted with a “It works!” message.

What you need to write down or remember is the IP address of your Mac. In my case it’s **192.168.0.8**. This is a local address which is only reachable from within my home network, so you can’t access my local web server by entering this address in your browser.

This may also be a good time to test the connection of your device with your computer. Just open a browser on your device and enter your Mac’s IP address. It should display the same “It works!” message as on your Mac.

If not, make sure Wifi is enabled, and that you are connected to your Mac’s network. If in doubt try connecting directly to your Mac’s Wifi (Airport) rather than a different computer’s or a router’s Wifi access port. You can switch the currently used Wifi network connection via the Settings app.

Finally, back in the Sharing Preferences dialog, click on the **Open Computer Website Folder** button. This is the folder where you’ll place the files that you want to have downloaded to your app while it is running.

#### (Optional) Un-lock the WebServer Documents folder

Since the WebServer documents folder is a system-owned folder you will be asked to enter your system administrator password every time you want to replace or modify a file in that folder. Some programs may even fail to save a document in that folder. If that annoys you, you can change the permissions of the folder by right-clicking it and choose **Get Info**.

Under Sharing & Permissions at the bottom of the pane click on the lock icon first to be able to make changes. Enter your password. Then click the + button also at the very bottom and add the **Administrators** account. Finally change the Privilege of the Administrators account - it will most likely be listed under your name followed by **(Me)** - to **Read & Write** permissions.

This will make working with the WebServer Documents folder a lot easier, and it’s just as secure as long as you trust everyone who may be using your computer without your supervision.

#### Downloading a file to your iOS device from a web server

In order to download a file from the web, you need the http address of the file as an NSURL object and then store the file in the app’s documents folder. Without any error checking it can be condensed to this code (the github project code has all the error checking and more):

|
1 2 3 4 5 6 7 8 9 10 11 12 13 |
// NSData downloads any file from an URL NSURL* url = [NSURL URLWithString:@"http://192.168.0.8/PoweredByMacOSX.gif"]; NSData* data = [NSData dataWithContentsOfURL:url]; // get the documents directory NSArray* pathArray = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES); NSString* documentsDir = documentsDirectory = [pathArray objectAtIndex:0]; NSString* localFile = [documentsDir stringByAppendingPathComponent:@"webfile.png"]; // write the downloaded file to documents dir [data writeToFile:localFile atomically:YES]; |

The PoweredByMacOSXLarge.gif file is one of the few files the Mac OS X web server includes. You can use that to test that the download was successful. However since iOS devices can’t load gif images you should copy a PNG or JPG image to your local web server’s documents folder **/Library/WebServer/Documents** and modify the code to load the newly copied file in case you want to feed it into a CCSprite right away.

The app’s documents directory is obtained in the regular, slightly convoluted way. Since you can’t just write a file to the app bundle you must write any downloaded files to the documents directory. This has an added advantage of being able to test if a bundle file already exists in the documents directory, allowing the code to skip downloading the file a second time. Writing the file is simply done with the writeToFile: method provided by NSData.

By the way, this code works with any file type. Whether you need an image as in this case, or an XML or HTML or text or binary file, you can use the same code. But there are also convenience functions in several Cocoa classes which allow you to create new instances of these classes with the URL contents, bypassing the “save file” stage. For example, NSString has a convenience initializer [stringWithContentsOfURL:](http://developer.apple.com/library/mac/documentation/Cocoa/Reference/Foundation/Classes/NSString_Class/Reference/NSString.html#//apple_ref/occ/clm/NSString/stringWithContentsOfURL:encoding:error:). Similar interfaces exist for UIImage and other Cocoa (touch) classes.

#### Create a CCSprite from a web image

Packed into a helper function **downloadFileFromServer:filename:** the above code allows you to easily create a CCSprite whose image comes from the web. Whether it’s your local web server, or the world wide web doesn’t matter!

|
1 2 3 4 5 6 7 |
NSString* localFile = [self downloadFileFromServer:@"192.168.0.8" filename:@"webserverfile.png"]; CCSprite* webSprite = [CCSprite spriteWithFile:localFile]; webSprite.position = CGPointMake(240, 160); webSprite.tag = kTagForLocalWebSprites; [self addChild:webSprite]; |

To test this code, copy any PNG image to your local web server’s documents folder **/Library/WebServer/Documents** and either rename it to **webserverfile.png** or modify the code to load a different PNG or JPG file.

I’ve had so much fun with this that I just ended up loading various images from the web into my app. Eventually I settled with a traffic webcam image from New York as the background. By rendering it transparently against the sand-colored background it created an eery B-movie feeling. The rest just fell into place naturally. ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


#### Only download files that have been modified

Using a frequently updated webcam image allowed me to test what was important for my development process: to limit file downloads to files that have actually been modified on the server. After all it would be a waste of bandwidth and processing to download the same unmodified image over and over again.

[This article helped me](http://iphoneincubator.com/blog/server-communication/how-to-download-a-file-only-if-it-has-been-updated) get this done quickly and without having to know or understand all the dirty secrets of the HTTP protoctol. Thanks also to those on Twitter who suggested reading the HTTP header’s Last-Modified entry in the first place.

Once more this code has all error checking removed for clarity:

|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 |
// create a HTTP request to get the file information from the web server NSURL* url = [NSURL URLWithString:@"http://192.168.0.8/webserverfile.png"]; NSMutableURLRequest* request = [NSMutableURLRequest requestWithURL:url]; [request setHTTPMethod:@"HEAD"]; NSHTTPURLResponse* response; [NSURLConnection sendSynchronousRequest:request returningResponse:&response error:nil]; // get the last modified info from the HTTP header NSString* httpLastModified = nil; if ([response respondsToSelector:@selector(allHeaderFields)]) { httpLastModified = [[response allHeaderFields] objectForKey:@"Last-Modified"]; } // setup a date formatter to query the server file's modified date // don't ask me about this part of the code ... it works, that's all I know :) NSDateFormatter* df = [[[NSDateFormatter alloc] init] autorelease]; df.dateFormat = @"EEE',' dd MMM yyyy HH':'mm':'ss 'GMT'"; df.locale = [[[NSLocale alloc] initWithLocaleIdentifier:@"en_US"] autorelease]; df.timeZone = [NSTimeZone timeZoneWithAbbreviation:@"GMT"]; // get the file attributes to retrieve the local file's modified date NSDictionary* fileAttributes = [fileManager attributesOfItemAtPath:localFile error:nil]; // test if the server file's date is later than the local file's date NSDate* serverFileDate = [df dateFromString:httpLastModified]; NSDate* localFileDate = [fileAttributes fileModificationDate]; BOOL isNewer = ([localFileDate laterDate:serverFileDate] == serverFileDate); |

I can only give a high-level description of this code. For me the important part was that it works. ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


In principle this code makes a request for the given file to the web server. The response is just some information about the file. You could say that it’s basically the same as querying a file in the file system for its attributes, although the process is a bit more involved.

In the end you have two NSDate objects that you can compare with each other to find out if the file on the web server has been modified more recently than the file on the device. In that case you would want to download the file.

#### Updating sprites whose image files have been modified

In order to update the sprites whenever their image file changes I simply scheduled a selector that runs twice per second (that’s fast enough) to check if any of the web server files I’m interested in have changed. The scheduled method runs the check code which wraps the above file modification code to determine if the image file should be re-downloaded and the sprites using that image should be updated with the new texture.

You’ll notice that I’ve changed the filenames to NSString constants, and I’m making use of the kTagForLocalWebSprites tag introduced before so that I know which sprites use which image file.

|
1 2 3 4 5 6 7 8 9 |
// update the sprites whenever the web server's image file has changed if ([self isNewerFileOnServer:kLocalWebServerAddress filename:kLocalWebServerFile]) { NSString* localFile = [self downloadFileFromServer:kLocalWebServerAddress filename:kLocalWebServerFile]; [self updateTexturesFromFile:localFile forSpritesWithTag:kTagForLocalWebSprites]; } |

More interesting is how I chose to update the sprites. The brute force solution would be to remove the existing sprites from the hierarchy and create new sprites using the new image file. But that would reset all of the internal states of the sprites, position, rotation, scale and any running actions.

The better way is to just update the texture the sprites are using:

|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 |
-(void) updateTexturesFromFile:(NSString*)file forSpritesWithTag:(int)spriteTag { CCSprite* spriteWithTag = (CCSprite*)[self getChildByTag:spriteTag]; if (spriteWithTag) { // clear the currently cached texture and force it to be reloaded CCTextureCache* texCache = [CCTextureCache sharedTextureCache]; [texCache removeTexture:spriteWithTag.texture]; CCTexture2D* newTexture = [texCache addImage:file]; CCSprite* sprite; CCARRAY_FOREACH(self.children, sprite) { if (sprite.tag == spriteTag) { sprite.texture = newTexture; } } } } |

You’ll notice that the first thing I do is to get one of the sprites with the given tag. I only do that in order to get to the CCTexture2D object all of these sprites are using, and then remove that texture from the CCTextureCache. Contrary to what you might expect, removing the texture from the cache does not affect sprites which are currently using the texture. Each sprite is still holding a reference to the texture object, it’s just no longer stored in the CCTextureCache. The effect of removing a texture from CCTextureCache is two-fold:

- The next time a cocos2d object wants to use the texture the CCTextureCache will reload it from disk, whether it needs to or not.
- Once all sprites have released the texture in question, and the texture hasn’t been re-cached, it will be released and its memory freed.

Primarily I’m interested in #1 because the downloaded file must be reloaded from disk. If it’s still in the cache, cocos2d simply wouldn’t bother to load the file even if the contents have changed. After removing the texture the same image is added to the texture cache again, forcing it to be reloaded from disk (or rather from flash memory). The returned CCTexture2D object can then be assigned to all of the sprites with the given spriteTag.

A quick side note: I could have used the filename and the [removeTextureForKey:](http://www.learn-cocos2d.com/api-ref/latest/cocos2d-iphone/html/interface_c_c_texture_cache/#aec3ada81d0420b798fde06c1a59334d6) method. But there’s a problem with that. If you load an image from the main bundle, say “file.png” then that will be the key for the texture. But if you load an image from the documents folder, the path to the documents folder will be part of the key. You could end up with two cached images: “file.png” and “/some/long/path/file.png” and attempts to uncache and reload “file.png” will prove futile. Keep that in mind when loading cache-able files from the documents directory.

This code only works with CCSprite objects but the general principle applies for all kinds of assets for which cocos2d has a cache (textures, sprite frames, animations and pre-loaded sound effects). Most other assets without a “cache” can simply be reloaded or updated.

#### Potential Code Improvements

There are several areas where you might want to improve the code. One obvious example would be to use asynchronous file transfers, I’ll fix that in the next iDevBlogADay post in two weeks. Currently each time an image is downloaded the entire app is blocked during that time. Not very user-friendly and bad for the framerate.

Some assets may be more difficult to reload than others. Imagine downloading an updated .tmx tilemap, you’d have to actually remove the CCTMXTiledMap node and re-add it, or subclass it to extend it with a reloadFromTMXFile method. For particle effects it will be difficult to preserve the current state so it’s probably best to just reload and restart the effect altogether.

#### Food for thought

Taking this a step further I can imagine several cool solutions:

Use a build script in Xcode to copy all modified resource files to the web server documents folder. Hit Build (not run) to have any modified files updated in your running application, or write a tool that monitors your resources folder for changes. Just be sure not to work with the files in the WebServer documents directory directly - only use the resource files that are actually in your Xcode project. Otherwise you may run into synchronicity problems (ie file available on server but not in main bundle = bug when regular users run the app).

Second idea is to load most, if not all assets from the web server but only at startup. If your code is stable but you’re doing a lot of tweaking of assets and scripts (think: add-ons or holiday special editions) this can significantly cut down your turnaround time without compromising performance. You wouldn’t need to implement asynchronous downloads in this scenario. Simply restarting the app (or just the currently running scene) on your device is still a lot faster than having Xcode build & deploy the app every time.

And maybe you even want to host some of the files on your public web server in order to keep modifying them. Just make sure not to host anything that contains executable code, ie. scripts. Apple forbids loading code from external sources.

#### The Project

I hope you enjoyed this article! Please tweek, lite, or one-up the thingy if you did, thank you! ![NY traffic webcam](../../../cctv47.jpg)


If you like to watch traffic on the web (we all do), click on the webcam image to the right. Hit the refresh button continuously. Soothing!

And I like to have a link to the project at the beginning and the end. Here’s the one at the end of the article. ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


The project is available from my [LearnCocos2D github repository](https://github.com/LearnCocos2D/LearnCocos2D), the project’s name is Cocos2D-UpdateFilesFromWebServer.

Next iDevBlogADay I’ll [improve this project to use asynchronous file transfers](http://www.learn-cocos2d.com/2012/02/cocos2d-webcam-viewer-part-2-asynchronous-texture-loading/).

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Epic post! Great work! Thanks for that.

Thanks very much for writing this, very handy whether you use it for Cocos2D purposes or not.

One thing, I was hoping you could clarify : As you mentioned at the end, Apple doesn’t want you downloading executable code, so would this mean Lua files are also not allowed?

I know Codea ran into this issue recently and had to remove their email publishing functionality, but I believe the way Kobold2D uses Lua is a bit different i.e. for setting variable and I’ve also considered it for text/dialogue related updates. Would this be fair game for downloading from a server or do you expect Apple is going to notice and tell you to stop?

Apple is very clear about that in the iOS Developer Program License Agreement:

Downloading Lua scripts, or any program code, is out of the question.

Does this apply to javascript one might download to say visualize something in a webkit view..?

You can not download any program code, irrespective of the language. Downloading a javascript file respectively an html file in which javascript is embedded is something that could get your app disapproved.

What you can do is have a javascript program on your webserver that runs on your server and returns a different image based on some input parameters, or does other things.

I think you are right, except for stuff that is explicitly to be run in a webkit view; the 2nd half of section 3.2.2 seems to explicitly allow this:

3.3.2 An Application may not download or install executable code. Interpreted code may only be used in an Application if all scripts, code and interpreters are packaged in the Application and not downloaded.

The only exception to the foregoing is scripts and code downloaded and run by Apple’s built-in WebKit framework, provided that such scripts and code do not change the primary purpose of the Application by providing features or functionality that are inconsistent with the intended and advertised purpose of the Application as submitted to the App Store.This would be great for loading additional game data new levels, sprites etc. both when developing and when out in the wild…

Exactly! I am interested in both, that’s why I dug into this.

[…] this episode you can see the Cocos2D Webcam Viewer in action. I also show you how to update a sprite’s texture while your app is running just by […]

Neat ideas :), your blog is full of useful snippets. Thanks.

[…] I know I promised last time to extend the Cocos2D Webcam Viewer with asynchronous file transfers. This was the first time I promised to write about something in […]

[…] updated the Cocos2D Webcam Viewer project from a previous article to download a file from the web asynchronously, and then load its texture asynchronously as well. […]