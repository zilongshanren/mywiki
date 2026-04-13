---
title: ClassesLineDrawingStarterkit/GameScene.h
url: http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/_game_scene_8h_source/
published: '2010-04-08'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[00001 //][00002 // GameScene.h][00003 //][00004 // Created by Steffen Itterheim on 08.04.10.][00005 // Copyright 2010 Steffen Itterheim. All rights reserved.][00006 //][00007][00008 #import "cocos2d.h"][00009][00010 #import "][PauseDelegateProtocol.h]"[00011][00012][00013 // class forwards to avoid #import at header level (speeds up compilation)][00014 @class][GameBackground];[00015 @class][GameHUD];[00016 @class][GameObjects];[00017 @class][GamePaths];[00018 @class][GameUI];[00019 @class][TargetObjects];[00020][00022]@interface[GameScene]: CCLayer <[PauseDelegateProtocol]>[00023 {][00024 // in z order:][00025][GameBackground]*[background];[00026][GameHUD]*[hud];[00027][GamePaths]*[paths];[00028][GameObjects]*[objects];[00029][TargetObjects]*[targetObjects];[00030][GameUI]*[ui];[00031][00032 unsigned int][currentScore];[00033]}[00034][00035 @property (readwrite, nonatomic) unsigned int currentScore;][00036][00038 +(id) scene;][00039][00041 -(id) init;][00042][00044 +(][GameScene]*)[instance];[00045][00047 -(bool) isPlaying;][00048][00050 -(void) onPauseGame;][00051][00053 -(void) onResumeGame;][00054][00056 -(void) onCrash;][00057][00058 @end]