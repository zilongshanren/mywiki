---
title: ClassesFoundation/Helper/MathHelper.h
url: http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/_math_helper_8h_source/
published: '2010-07-17'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[00001 //][00002 // MathHelper.h][00003 //][00004 // Created by Steffen Itterheim on 08.04.10.][00005 // Copyright 2010 Steffen Itterheim. All rights reserved.][00006 //][00007][00009]@interface[MathHelper]: NSObject[00010 {][00011][00012 }][00013][00015 +(CGPoint) getTouchLocation:(UITouch*)touch;][00017 +(CGPoint) getTouchesLocation:(NSSet*)touches;][00019 +(CGPoint) getNormalizedDirectionVector:(float)direction;][00022 +(CGPoint) getDistantPointInDirection:(float)direction fromLocation:(CGPoint)location;][00024 +(bool) isDistanceBetweenPoint:(CGPoint)point1 andPoint:(CGPoint)point2 smallerThan:(float)distance;][00026 +(bool) isDistanceBetweenPoint:(CGPoint)point1 andPoint:(CGPoint)point2 greaterThan:(float)distance;][00029 +(float) getFixedSpeedDurationBetweenPoint:(CGPoint)point1 andPoint:(CGPoint)point2 forSpeed:(float)speed;][00033 +(float) getDirectionFromPoint:(CGPoint)point1 toPoint:(CGPoint)point2;][00035 +(CCNode*) getClosestNode:(CCNode*)node1 otherNode:(CCNode*)node2 location:(CGPoint)location;][00036][00037 @end]