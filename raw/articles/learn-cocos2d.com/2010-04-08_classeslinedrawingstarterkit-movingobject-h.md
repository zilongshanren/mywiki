---
title: ClassesLineDrawingStarterkit/MovingObject.h
url: http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/_moving_object_8h_source/
published: '2010-04-08'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[00001 //][00002 // MovingObject.h][00003 //][00004 // Created by Steffen Itterheim on 08.04.10.][00005 // Copyright 2010 Steffen Itterheim. All rights reserved.][00006 //][00007][00008 #import "cocos2d.h"][00009][00010 #import "][ObjectDef.h]"[00011][00013]typedef enum[00014 {][00016][kStateNormal]= 0,[00018][kStateFollowingPath],[00020][kStateInactive],[00021][00022][MAX_ObjectStates],[00023 }][EObjectStates];[00024][00025 @class][Path];[00026][00030]@interface[MovingObject]: CCSprite[00031 {][00032][ObjectDef][def];[00033][00035][Path]*[path];[00036][00037]CCSprite*[proximityWarning];[00038][00039]CGPoint[prevPosition];[00040][00042][EObjectStates][state];[00043 }][00044][00046 @property (nonatomic, readonly)][ObjectDef]def;[00048 @property (nonatomic, readonly)][EObjectStates]state;[00049][00050][00052 +(id) movingObjectWithDef:(][ObjectDef])objectDef;[00054 -(id) initMovingObjectWithDef:(][ObjectDef])objectDef;[00055][00057 -(bool) canCollide;][00059 -(bool) canFollowPath;][00061 -(bool) isFollowingPath;][00063 -(void) startPathFollow:(][Path]*)followPath;[00064][00066 -(void) moveTo:(CGPoint)location target:(id)target selector:(SEL)selector;][00068 -(void) moveTo:(CGPoint)location;][00070 -(void) moveToScreenBorder:(float)direction;][00072 -(float) moveIntoScreen;][00073][00075 -(void) onTouch;][00077 -(void) onPathPointAdded;][00078][00080 -(void) setProximityWarningEnabled:(bool)enabled;][00081][00083 -(void) setCrashWarning;][00084][00086 -(void) setState:(][EObjectStates])newState;[00087][00088 @end]