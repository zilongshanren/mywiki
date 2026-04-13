---
title: Robust iCloud implementation for games
url: https://gamedevcoder.wordpress.com/2012/07/09/robust-icloud-implementation-for-games/
published: '2012-07-09'
source_blog: Gamedev Coder Diary
source_site: https://gamedevcoder.wordpress.com
category: game programming
fetched: '2026-04-13'
---

For my second iOS game [Monstaaa!](http://itunes.apple.com/us/app/monstaaa!/id482844637?mt=8) I wanted to take advantage of the new iOS 5 feature iCloud and use it to store savegames – play on one device, then later continue on another one. Pretty basic iCloud usage scenario and so, you might think I should easily find some relevant tutorials or sample code on the internet. Well, not quite so easily…

![images](../../assets/dd9ef5409b2a3836.jpg)


The best resource I found was the following series of tutorials: [Beginning iCloud in iOS 5](http://www.raywenderlich.com/6015/beginning-icloud-in-ios-5-tutorial-part-1). It is does explain well the basics of iCloud usage but unfortunately it doesn’t go as far as implementing iCloud conflict resolution – something that is strictly required if you’re seriously considering using iCloud for your game. Besides, Apple doesn’t make it easy for you either to understand how one is supposed to implement it.

The small library that I implemented handles all that is needed for a simple game savegame i.e. creation & writing to iCloud file, reading from iCloud file and, very importantly, iCloud file conflict resolution. The library has been implemented as an extension for [Marmalade SDK](http://madewithmarmalade.com) (cross platform mobile development SDK) but if you don’t use it, don’t worry, it is fairly trivial to make it stand-alone library.

The library has C++ interface but the majority of the code is in Objective-C. You can get it from github: [https://github.com/macieks/s3eIOSiCloud](https://github.com/macieks/s3eIOSiCloud) If you just want to see the _code_ or don’t use Marmalade SDK check these [source](https://github.com/macieks/s3eIOSiCloud/blob/master/source/iphone/s3eIOSiCloud_platform.mm) and [header](https://github.com/macieks/s3eIOSiCloud/blob/master/h/s3eIOSiCloud.h) files.

The basic idea behind the library is you store your savegame both locally (on the device) and remotely (in iCloud). The reason we always store local savegame version is quite obvious – if an app fails to connect to iCloud for any reason, you won’t just lose the progress. Once iCloud becomes available again, we then connect back to it and, optionally, resolve conflicts that occurred in the meantime due to savegames done on other devices.

The library notifies the app whenever it has successfully read the file or whenever conflict has been detected. It’s then up to the app to resolve the conflicts and merge remote with local savegame. The callback in both cases is exactly the same – the app is given the data (i.e. *void* data* and *int size*) to merge with and that’s it. The actual merging operation is application specific – every game will merge differently. And just to make sure everything is well explained here, what I mean by merging is making one out of two different savegames. Let’s say the player has completed levels 1,2,3 on their iPhone and levels 2,4,5 on their iPad – the resulting merged savegame should contain information about levels 1,2,3,4,5 being completed.

Here’s quick intro on how to use the code. *MySaveGame* struct represents sample savegame with boolean values indicating which levels have been completed and *MyMergeFunc* is the merge callback registered with the library.

#include "s3eIOSiCloud.h" #define NUM_LEVELS 100 struct MySaveGame { bool m_completedLevels[NUM_LEVELS]; }; MySaveGame localSaveGame; int MyMergeFunc(void* systemData, void*) { s3eIOSiCloudDataToMergeWith* data = (s3eIOSiCloudDataToMergeWith*) systemData; MySaveGame* remoteSaveGame = (MySaveGame*) data->m_data; // Merge remote and local savegames for (int i = 0; i < NUM_LEVELS; i++) if (remoteSaveGame->m_completedLevels[i]) localSaveGame.m_completedLevels[i] = true; // Store savegame locally (fopen / fwrite / fclose) bool savedLocally = [...] // Return success or failure to iCloud library return savedLocally ? 0 : 1; }

The callback gets the data to merge with, performs app specific merging operation and then stores the savegame locally.

Let’s now initialize iCloud for “*my_save_game.txt*” file:

s3eIOSiCloudRegister(S3E_IOSICLOUD_CALLBACK_MERGE, MyMergeFunc,0); s3eIOSiCloudStart("my_save_game.txt", S3E_TRUE);

The code above registers merge callback, then starts iCloud service for a specific file.

To make sure read and write operations are being retried internally, simply do this every frame:

s3eIOSiCloudTick();

And finally, to store savegame in iCloud do this:

s3eIOSiCloudWrite(&localSaveGame, sizeof(MySaveGame));

Now, as I said, if you want to use the code but you don’t use Marmalade you should easily be able to get rid of Marmalade specific code – mostly message logging and callback handling. There’s no heavy Marmalade dependencies anywhere.

Finally, to make you feel better about the library I’m just going to say that it’s been already successfully used by two of my iOS games – [Monstaaa!](http://monstaaa.pixelelephant.com) and [Puzzled Rabbit](http://puzzledrabbit.pixelelephant.com).

Thanks for the write up dude! Good read!

Very usefull information, The future of mobile application will be more attractive with the development of systems and library. incredible.

Hi Maciej, I was having an issue where your extension would register but not start. Now with SDK 6.1.2 it reports as not being available. I’ve recompiled and gone over things for many days. Any ideas please?

I’m not sure what is the cause of the problem here – maybe recently dropped ARM6 support? Solution to this is recompiling extension for ARM7 which you can easily do on Mac. But that is just guessing.

Otherwise you also have to make sure that extension is properly linked via Marmalade Deployment options.

Still no joy with arm7. I’m guessing my Xcode is too old as still on OSX 10.6.7

Also, when I had the old iOS5 issue: Can any iCloud account be used for testing, or must the test user be used (for example)? Does it have a ‘sandbox’ mode for developing like Game Centre has perhaps. Thanks.

No need to use test account for iCloud testing. But you have to have iCloud enabled in system settings.

I asked over at the Marmalade forums now with additional info https://devnet.madewithmarmalade.com/questions/512/why-is-this-extension-not-available.html

So far just a down-rate, how dare I ask! Guess nobody uses iCloud and doesn’t care to…

Hope you don’t blame me – the code worked for me (and few other people) and so I simply decided to share it with others but I don’t have any plans to maintain its compatibility with new Marmalade SDK (or iOS) versions.

And for the last couple of months I don’t even have a Marmalade SDK license to quickly check what’s wrong for you.

Of course not blaming you. I am grateful that you shared your efforts!

I’ve decided to just unlock all of the levels at launch. Sorry to hear you no longer have a licence, Marmalade need people like you around. When my new game Attic Eyes sells a bucket load I will send you a donation 🙂

By unlock, I mean there will be no unlocking when playing on another iOS device.

I was really impressed with iCloud in Zonbie Gunship and was hoping to use it in the future.