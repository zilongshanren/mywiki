---
title: ClassesFoundation/Macros.h
url: http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/_macros_8h_source/
published: '2010-05-18'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

00001 /*00002 * Macros.h00003 * cocos2d-project00004 *00005 * Created by Steffen Itterheim on 18.05.10.00006 * Copyright 2010 __MyCompanyName__. All rights reserved.00007 *00008 */00009
00010 #ifndef DEBUG00011#define SIAssert(_e) ((void)0)00012 00013 #else00014 00015 /* standard assert macro */00016 #define SIAssert(_e) if(_e) { (void)0; } else { NSAssert3(_e, @"%s(%d): %s", __FILE__, __LINE__, __FUNCTION__); }00017 00018 /*00019 NSStringFromSelector(_cmd) %@ Name of the current selector00020 NSStringFromClass([self class]) %@ Name of the current object’s class00021 __FUNCTION__ %s Current function signature00022 __FILE__ %s Path of the current file00023 __LINE__ %d Current line number00024 __PRETTY_FUNCTION__ %s Complete current function signature (includes arguments).00025 */00026 //00027
00028 #endif