---
title: /depot/cocosdocs/cocos2d-iphone-0.99.5/cocos2d/Support/CGPointExtension.h File
  Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/_c_g_point_extension_8h/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Defines
|
| #define | [ccp](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#ga6250be5f1c27162404561148ebd6ffcc)(__X__, __Y__) CGPointMake(__X__,__Y__) |
Functions
|
| static CGPoint | [ccpAdd](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#ga92bfb83590589db35ccbea0db0b9ba67) (const CGPoint v1, const CGPoint v2) |
| float | [ccpAngle](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#gaaedd775cbf78ce9c11995240c21a0c72) (CGPoint a, CGPoint b) |
| float | [ccpAngleSigned](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#ga437e145206b77c35572dc423a916bce3) (CGPoint a, CGPoint b) |
| CGPoint | [ccpClamp](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#ga9ece903bce575705f3e7fe2e81f011b0) (CGPoint p, CGPoint from, CGPoint to) |
| CGPoint | [ccpCompMult](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#ga9bc595d671b88bd0a53c3fd9ec88856d) (CGPoint a, CGPoint b) |
| CGPoint | [ccpCompOp](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#gab481841d1a0ea2fdba40b5d888acd37f) (CGPoint p, float(*opFunc)(float)) |
| static CGFloat | [ccpCross](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#ga60abfa8ae82e17c10712deee70c2f242) (const CGPoint v1, const CGPoint v2) |
| CGFloat | [ccpDistance](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#ga76b1b389db811d00e0a461df630d9a8e) (const CGPoint v1, const CGPoint v2) |
| static CGFloat | [ccpDot](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#ga39eab22d4d18702fb1152db24c80e776) (const CGPoint v1, const CGPoint v2) |
| CGPoint | [ccpForAngle](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#gaa21e0b8cc011fd0e2b6485a3533d66f3) (const CGFloat a) |
| CGPoint | [ccpFromSize](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#ga88e1c7ec8ddadd2d62eb057571a633c0) (CGSize s) |
| BOOL | [ccpFuzzyEqual](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#ga672a44290cce4dc0709c7db8dd6f3029) (CGPoint a, CGPoint b, float variance) |
| CGFloat | [ccpLength](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#gadb805cf1e3b4d29ad6396fadccb028af) (const CGPoint v) |
| static CGFloat | [ccpLengthSQ](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#ga16a2269b45f198e9ba09752a16974a21) (const CGPoint v) |
| CGPoint | [ccpLerp](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#gac8a75c7576b2367277be20ea8fc196c7) (CGPoint a, CGPoint b, float alpha) |
| BOOL | [ccpLineIntersect](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#gaeed6108881d50edd5920c1129274f761) (CGPoint p1, CGPoint p2, CGPoint p3, CGPoint p4, float *s, float *t) |
| static CGPoint | [ccpMidpoint](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#ga8a42230182afbd8c633203b29cbb0582) (const CGPoint v1, const CGPoint v2) |
| static CGPoint | [ccpMult](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#ga6d201e26ad229dfda3a0d4d16a562e69) (const CGPoint v, const CGFloat s) |
| static CGPoint | [ccpNeg](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#gaa22b22de89dd66877bfa3a9f63f3e963) (const CGPoint v) |
| CGPoint | [ccpNormalize](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#ga0f481c2494911e030769268c01e55323) (const CGPoint v) |
| static CGPoint | [ccpPerp](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#gac99750cac08ec9d0e4f131b69aff3969) (const CGPoint v) |
| static CGPoint | [ccpProject](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#gac18234956e056aa27ca370384466b45e) (const CGPoint v1, const CGPoint v2) |
| static CGPoint | [ccpRotate](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#gade909d1834f1d907ce434142a75d75e3) (const CGPoint v1, const CGPoint v2) |
| CGPoint | [ccpRotateByAngle](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#gad28ca42fb64e84452cd65ccac6fb0c28) (CGPoint v, CGPoint pivot, float angle) |
| static CGPoint | [ccpRPerp](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#gac8694a925d18199e3388c95588705768) (const CGPoint v) |
| static CGPoint | [ccpSub](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#gac6e04f20be000e47ec62618f39e550f1) (const CGPoint v1, const CGPoint v2) |
| CGFloat | [ccpToAngle](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#ga46c5e225fa14286190552caf1b2456ab) (const CGPoint v) |
| static CGPoint | [ccpUnrotate](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#ga2e26b35020f0fbfa3400f18d0840cebe) (const CGPoint v1, const CGPoint v2) |
| float | [clampf](../../../unofficial-cocos2d-api-reference/html/group___c_g_point_extension/#ga7c45e20220e4a8aaa7a43e1797347a91) (float value, float min_inclusive, float max_inclusive) |

CGPoint extensions based on Chipmunk's cpVect file. These extensions work both with CGPoint and cpVect.