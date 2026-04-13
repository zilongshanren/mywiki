---
title: 'Speedy iPhone App Programming :: nklein software'
url: http://nklein.com/2010/02/speedy-iphone-app-programming/
author: Pat
published: '2010-02-04'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

Sunday, I decided that I needed a simpler statistics tracking program to keep track of stuff while I’m coaching volleyball. I started out keeping them on paper, but felt that I was staring at the page too often to find where to put a tick mark.

Next, I tried the [iVolleyStats Match](http://itunes.apple.com/us/app/ivolleystats-match/id325343491?mt=8) iPhone app. It is pretty reasonable to use, but it’s got too many controls on the user-interface. The only way that I could keep up with a match was to forgo half of the functionality… either ignoring who is getting credit for an act, ignoring passing stats altogether, and not recording attack or block attempts at all.

For the past few weeks, I have tried using the Voice Memos application on the iPhone. I narrate the game into my phone as the game goes on. This lets me get really fine resolution of statistics, but it doesn’t give me any information in real-time. When I call a time-out, I am going from memory to say how we’ve been passing or hitting. This takes away the lion’s share of the benefit one gets from gathering statistics at all.

So, my team has a tournament this Saturday. I decided Sunday night that I should try to get together an iPhone app that does what I want. I’ve long been thinking about what I want in a volleyball stat tracking iPhone app. What I want will be a big, big undertaking (read: longer than one week). So, I started studying Apple’s CoreData APIs on Sunday night and Monday morning. Then, I dove in.

Now, my previous application was based upon [Cocos2D-iPhone](http://www.cocos2d-iphone.org/). As such, it didn’t involve any of the Apple UIKit classes or any work with Interface Builder. This application is navigation based with table views and custom table view cells from separate NIB files.

Despite this being my first real foray into the UIKit and CoreData APIs, I’ve got an application that I can use on Saturday. There are two more bits that I will try to add tomorrow, but that I don’t need for Saturday. To package it up for sale, there’s more functionality that I’ll need to add in case you don’t like things in the order that I have them on the screen or in case you want to add your own categories of statistic. And, I need to make some specialized visualization screens for some of the stats.

The screenshot here is the main stat-tracking interface. The stats present are Penn State’s stats from my trial run watching game one of their NCAA semifinal against Hawaii from last December. In retrospect, I think I probably gave them credit for two neutral attacks that I should have called free balls. Other than that, I think it’s pretty good. It’s definitely information that will do me well during time-outs.

I fought for a long time this morning trying to get my UIBarButtonItem to show up in my UINavigationBar for one screen. It turns out that these two methods don’t quite do the same thing on iPhoneOS 3.1.2:

- (void)showStatTrackingScreen {

[navigationController setViewControllers:[NSArray arrayWithObject:homeViewController] animated:NO];

[navigationController pushViewController:trackStatsController animated:YES];

}

// version made of fail that does NOT show my UIBarButton in the UINavigationBar

// until you go forward a screen and pop back to this one.

- (void)showStatTrackingScreenMadeOfFail {

[navigationController setViewControllers:[NSArray arrayWithObjects:homeViewController,

trackStatsController,

nil]

animated:YES];

}