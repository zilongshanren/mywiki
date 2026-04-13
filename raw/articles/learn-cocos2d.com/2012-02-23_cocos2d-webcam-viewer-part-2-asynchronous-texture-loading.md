---
title: 'Cocos2D Webcam Viewer, Part 2: Asynchronous Texture Loading'
url: http://www.learn-cocos2d.com/2012/02/cocos2d-webcam-viewer-part-2-asynchronous-texture-loading/
author: Curi says
published: '2012-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I updated the Cocos2D Webcam Viewer project from a [previous article](http://www.learn-cocos2d.com/2012/01/download-modified-files-web-server-cocos2d-webcam-viewer/) to download a file from the web asynchronously, and then load its texture asynchronously as well. You can now switch between the two modes to see how asynchronous operations almost completely removed the pauses the app experiences in synchronous mode. Just tap the screen to switch modes.

To visualize the lag I added a constantly moving sprite at the bottom. This makes the lag easier to spot than a framerate counter. I also removed all error checking code from this article to make the code easier to read. As always you can find the ![itcamefrom_part2](../../../wordpress/wp-content/uploads/itcamefrom_part2-300x154.png)


[Cocos2D Webcam Viewer source code](https://github.com/LearnCocos2D/LearnCocos2D/tree/master/Cocos2D-UpdateFilesFromWebServer)with full error checking on the

[LearnCocos2D github repository](https://github.com/LearnCocos2D/LearnCocos2D).

#### Downloading a file from the web synchronously

Downloading a file from the web turns out to be super-simple. You only need three lines of code, and of course the address and path to the file on the server:

|
1 2 3 4 5 |
NSURL* url = [NSURL URLWithString:@"http://207.251.86.248/cctv47.png"]; NSData* data = [NSData dataWithContentsOfURL:url options:NSDataReadingMappedIfSafe error:nil]; [data writeToFile:localFile options:NSDataWritingAtomic error:nil]; |

#### Downloading a file from the web asynchronously

Unfortunately, NSData has no convenience method that allows you to load data asynchronously. Fortunately, NSObject has the method that you need. It is called [performSelectorInBackground:withObject:](https://developer.apple.com/library/mac/documentation/Cocoa/Reference/Foundation/Classes/nsobject_Class/Reference/Reference.html#//apple_ref/occ/instm/NSObject/performSelectorInBackground:withObject:). You don’t need to know a single thing about threading to utilize multithreading.

But then again performSelectorInBackground only takes a single argument but we must pass at least the url and the file to download to. This is a common situation that you’ll be faced with from time to time. There is a simple solution: create a new class that holds all of the data you need.

I solved this problem by creating the AsyncFileDownloadData class which is used to pass multiple arguments to a method which only takes a single object argument.

|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 |
@interface AsyncFileDownloadData : NSObject { NSURL* url; NSString* localFile; int spriteTag; } @property (copy) NSURL* url; @property (copy) NSString* localFile; @property int spriteTag; @end @implementation AsyncFileDownloadData @synthesize url, localFile, spriteTag; -(void) dealloc { //CCLOG(@"dealloc %@", self); [url release]; [localFile release]; [super dealloc]; } @end |

In Objective-C, this is generally recommended and preferred over creating C structs. Mainly because you can add an object into any collection (NSArray, NSDictionary, etc) whereas you can’t do that with a C struct.

Whenever you think you need a C struct, create an object instead. If necessary, you can make the ivars @public to make the object behave like a C struct (access @public ivars with: **object->url**). This gives you the same performance as a C struct and only slightly higher memory usage.

#### Perform selector in background

Back to asynchronous downloading: you can now rewrite the initial code to perform a selector on a background thread like this:

|
1 2 3 4 5 6 7 8 |
NSURL* url = [NSURL URLWithString:@"http://207.251.86.248/cctv47.png"]; AsyncFileDownloadData* afd = [[[AsyncFileDownloadData alloc] init] autorelease]; afd.url = url; afd.localFile = localFile; afd.spriteTag = spriteTag; [self performSelectorInBackground:@selector(downloadInBackground:) withObject:afd]; |

In case you’re wondering: performSelectorInBackground retains the afd object, so it is safe to autorelease it. Of course if you’re using ARC (which you really should use in every new project - but more on that some other time) this wouldn’t concern you at all.

The **downloadInBackground:** method takes the AsyncFileDownloadData object as argument and then performs the exact same code as you’ve seen earlier. Except that this method is now running on a separate, background thread.

|
1 2 3 4 5 6 7 8 9 10 11 |
-(void) downloadInBackground:(AsyncFileDownloadData*)afd { NSData* data = [NSData dataWithContentsOfURL:afd.url options:NSDataReadingMappedIfSafe error:nil]; [data writeToFile:afd.localFile options:NSDataWritingAtomic error:nil]; [self performSelectorOnMainThread:@selector(updateSprites:) withObject:afd waitUntilDone:NO]; } |

#### Perform selector on main thread

Knowing that the **downloadInBackground:** selector is running on a background thread is crucial information because some operations have to be done on the main thread, and loading OpenGL textures is one of these operations.

That’s why the **updateSprites:** selector is performed on the main thread via [performSelectorOnMainThread:withObject:waitUntilDone:](https://developer.apple.com/library/mac/documentation/Cocoa/Reference/Foundation/Classes/nsobject_Class/Reference/Reference.html#//apple_ref/occ/instm/NSObject/performSelectorOnMainThread:withObject:waitUntilDone:). It also receives the afd object because it too needs the localFile and spriteTag vars to do its job. Again, no extra retain is necessary.

The only job of **updateSprites:** is to extract the information from the afd object and call the already existing method **updateTexturesFromFile:forSpritesWithTag:**. It just relays the call:

|
1 2 3 4 5 |
-(void) updateSprites:(AsyncFileDownloadData*)afd { [self updateTexturesFromFile:afd.localFile forSpritesWithTag:afd.spriteTag]; } |

Your experience may vary. You may be able to perform other selectors on the background thread, too. It may or may not crash. But even if it works, you don’t know what kind of side effects this may cause because you could have the same method running on the main thread and the background thread simultaneously.

Therefore it is good practice to “return the call” to the main thread after the background task is completed.

#### Loading Textures asynchronously with Cocos2D

Loading a texture in Cocos2D is done via the CCTextureCache class. Here’s the code that loads our newly downloaded texture file synchronously, and it calls **updateChildrenWithTag:texture:** right away:

|
1 2 3 |
CCTextureCache* texCache = [CCTextureCache sharedTextureCache]; CCTexture2D* newTexture = [texCache addImage:file]; [self updateChildrenWithTag:spriteTag texture:newTexture]; |

Now if you want to load the texture asynchronously, all you need is to use the CCTextureCache method **addImageAsync:target:selector:** and be done with it.

But wait, it’s not that simple in this case. The addImageAsync method doesn’t provide you with a way to pass an extra object along, so once the texture has been loaded and the callback selector runs, you don’t have the spriteTag available that the **updateChildrenWithTag:** method requires!

The (seemingly) easiest solution is to bite the bullet and call different selectors depending on the sprite tag:

|
1 2 3 4 5 6 7 8 9 10 11 12 13 |
CCTextureCache* texCache = [CCTextureCache sharedTextureCache]; if (spriteTag == kTagForLocalWebSprites) { [texCache addImageAsync:file target:self selector:@selector(didFinishLoadLocal:)]; } else if (spriteTag == kTagForWorldWideWebSprites) { [texCache addImageAsync:file target:self selector:@selector(didFinishLoadWWW:)]; } |

The alternative is to improve the CCTextureCache code so that the addImageAsync method takes an extra object argument. This shouldn’t be too hard to do. Because the above solution will become quite tedious and error prone the more information you need to “encode” by using different selectors.

Anyhow, the addImageAsync method calls one of the didFinishLoad selectors once the texture has been loaded. Each didFinishLoad selector takes one argument: the newly created CCTexture2D object. With that, it’s a piece of cake to update the sprites in the scene with the given tag and new texture:

|
1 2 3 4 5 6 7 8 9 10 |
-(void) didFinishLoadLocal:(CCTexture2D*)texture { [self updateChildrenWithTag:kTagForLocalWebSprites texture:texture]; } -(void) didFinishLoadWWW:(CCTexture2D*)texture { [self updateChildrenWithTag:kTagForWorldWideWebSprites texture:texture]; } |

#### The result

With synchronous texture loads, the Cocos2D Webcam Viewer app paused for half a second or so every time a new texture was loaded. You can see this by looking at the moving sprite and notice how it pauses frequently.

With asynchronous texture downloading & loading, the viewer app runs smoothly for the most part. You will notice the moving sprite to be a bit “jumpy”, but it never really pauses entirely. You can see the cars moving by at much higher update rate.

I expect the result will be most visible on devices with dual-core CPUs (iPad 2, iPhone 4S). On all other devices, you still have one CPU that runs all of the threads. The big difference background processing makes is that the CPU usually has prolonged phases of inactivity, for example while waiting for the webserver to respond to a request. It makes sense to process other things while waiting, instead of pausing the entire app.

I pronounced the pause-effect by skipping the “file modified” check (which is also a synchronous operation waiting to be performed in a background thread) and simply try to download a new file at a fixed interval (5 times per second). Try it yourself by downloading and running the [Cocos2D Webcam Viewer source code](https://github.com/LearnCocos2D/LearnCocos2D/tree/master/Cocos2D-UpdateFilesFromWebServer).

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Can’t you load texture in background by changing opengl context?

EAGLContext *k_context = [[[EAGLContext alloc] initWithAPI:kEAGLRenderingAPIOpenGLES1 sharegroup:[[[[Director sharedDirector] openGLView] context] sharegroup]] autorelease];

[EAGLContext setCurrentContext:k_context];

That is exactly what addImageAsync is doing.

Was too sleepy, didn’t notice some things. Great article, keep up good work!

[…] Next iDevBlogADay I’ll improve this project to use asynchronous file transfers. […]