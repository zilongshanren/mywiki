---
title: ClassesLineDrawingStarterkit/Path.h
url: http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/_path_8h_source/
published: '2010-07-17'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[00001 //][00002 // Path.h][00003 //][00004 // Created by Steffen Itterheim on 08.04.10.][00005 // Copyright 2010 Steffen Itterheim. All rights reserved.][00006 //][00007][00008 #import "cocos2d.h"][00009][00010 #import "][PathLineStyles.h]"[00011 #import "][PathPoint.h]"[00012][00013][00015]@interface[Path]: CCNode[00016 {][00018]NSMutableArray*[pathPoints];[00019][00020]CGPoint objectPosition;[00021]CGPoint drawingEndPoint;[00022][00023][EPathLineStyles]lineStyle;[00024][EPathLineStyles]lineStyleWhileDrawing;[00025][00026]bool isUserStillDrawingThisPath;[00027 }][00028][00030 @property (readwrite, nonatomic)][EPathLineStyles]lineStyle;[00032 @property (readwrite, nonatomic)][EPathLineStyles]lineStyleWhileDrawing;[00034 @property (readwrite, nonatomic) CGPoint objectPosition;][00036 @property (readwrite, nonatomic) CGPoint drawingEndPoint;][00038 @property (readonly, nonatomic) bool isUserStillDrawingThisPath;][00039][00040][00042 +(id) path;][00044 -(id) init;][00045][00047 -(void) addEndPoint:(CGPoint)point;][00049 -(void) addPoint:(CGPoint)point;][00051 -(void) endPathDrawing;][00052][00054 -(void) removePath;][00056 -(void) removeFirstPoint;][00058 -(void) removeAllPoints;][00059][00061 -(int) getNumPoints;][00063 -(CGPoint) getLastPointLocation;][00065 -(][PathPoint]) getFirstPathPoint;[00066][00067 @end]