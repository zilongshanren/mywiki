---
title: ClassesFoundation/AppDelegate.h
url: http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/_app_delegate_8h_source/
published: '2010-07-17'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[00001 //][00002 // AppDelegate.h][00003 // AppDelegate][00004 //][00005 // Created by Steffen Itterheim on 24.04.10.][00006 // Copyright Steffen Itterheim 2010. All rights reserved.][00007 //][00008][00009 #import <UIKit/UIKit.h>][00010][00011 #import "][PauseDelegateProtocol.h]"[00012][00013][00015]@interface[AppDelegate]: NSObject <UIApplicationDelegate>[00016 {][00017 UIWindow *window;][00018][00019 id<PauseDelegateProtocol> pauseDelegate;][00020][00021 bool][hasOrientationChangedBefore];[00022]bool isPlaying;[00023]bool isPaused;[00024]}[00025][00026 @property (nonatomic, retain) UIWindow *window;][00027 @property (readwrite, nonatomic) bool isPlaying;][00028 @property (readwrite, nonatomic) bool isPaused;][00029][00030 @property (readonly, assign) id<][PauseDelegateProtocol]> pauseDelegate;[00031][00032 -(void) setPauseDelegate:(id<][PauseDelegateProtocol]>)delegate;[00033][00034 @end]