---
title: ClassesLineDrawingStarterkit/ObjectDef.h
url: http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/_object_def_8h_source/
published: '2010-04-09'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[00001 //][00002 // ObjectDef.h][00003 // line-drawing-game][00004 //][00005 // Created by Steffen Itterheim on 09.04.10.][00006 // Copyright 2010 Steffen Itterheim. All rights reserved.][00007 //][00008][00009 #import "][AssetHelper.h]"[00010][00012]typedef enum[00013 {][00015][ObjectTypeDefaultPlane],[00016][00018][ObjectTypes_MAX],[00019 }][ObjectTypes];[00020][00021]typedef enum[00022 {][00023][ImageOrientationRight]= 0,[00024][ImageOrientationUp]= -90,[00025][ImageOrientationLeft]= -180,[00026][ImageOrientationDown]= -270,[00027 }][ImageOrientations];[00028][00030]typedef struct[00031 {][00033][ObjectTypes]type;[00035]NSString* imageFileName;[00037]NSString* proximityWarningFileName;[00042][ImageOrientations]imageOrientation;[00044]float speed;[00046]float rotationSpeed;[00048]float touchRadius;[00050]float collisionRadius;[00051 }][ObjectDef];[00052][00054]static __inline__[ObjectDef][ObjectDefMake]([ObjectTypes]type, NSString* imageFileName, NSString* proximityWarningFileName,[ImageOrientations]imageOrientation, float speed, float rotationSpeed, float touchRadius, float collisionRadius)[00055 {][00056][ObjectDef]def;[00057 def.][type]= type;[00058 def.][imageFileName]= [[AssetHelper]getDeviceSpecificFileNameFor:imageFileName];[00059 def.][proximityWarningFileName]= [[AssetHelper]getDeviceSpecificFileNameFor:proximityWarningFileName];[00060 def.][imageOrientation]= imageOrientation;[00061 def.][speed]= speed;[00062 def.][rotationSpeed]= rotationSpeed;[00063 def.][touchRadius]= touchRadius;[00064 def.][collisionRadius]= collisionRadius;[00065 return def;][00066 }][00067]