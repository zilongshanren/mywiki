---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/CocosDenshion/html/interface_c_d_x_property_modifier_action/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Public Member Functions
|
| id | [initWithDuration:modifier:](../../../../../api-ref/1.0/CocosDenshion/html/interface_c_d_x_property_modifier_action/#a24e48541ff1b6b81dbab1a4f7f024746) (ccTime t,[modifier] [CDPropertyModifier](../../../../../api-ref/1.0/CocosDenshion/html/interface_c_d_property_modifier/) *aModifier) |
Static Public Member Functions
|
| id | [actionWithDuration:modifier:](../../../../../api-ref/1.0/CocosDenshion/html/interface_c_d_x_property_modifier_action/#a46d04d4a1c089a70f9d6d4a5dfce2fa9) (ccTime t,[modifier] [CDPropertyModifier](../../../../../api-ref/1.0/CocosDenshion/html/interface_c_d_property_modifier/) *aModifier) |
void | **fadeSoundEffects:finalVolume:curveType:shouldStop:** (ccTime t,[finalVolume] float endVol,[curveType] [tCDInterpolationType](../../../../../api-ref/1.0/CocosDenshion/html/_cocos_denshion_8h/#abf5e3c49618c14630377c3696e7a3ab9) curve,[shouldStop] BOOL stop) |
void | **fadeSoundEffect:finalVolume:curveType:shouldStop:effect:** (ccTime t,[finalVolume] float endVol,[curveType] [tCDInterpolationType](../../../../../api-ref/1.0/CocosDenshion/html/_cocos_denshion_8h/#abf5e3c49618c14630377c3696e7a3ab9) curve,[shouldStop] BOOL stop,[effect] [CDSoundSource](../../../../../api-ref/1.0/CocosDenshion/html/interface_c_d_sound_source/) *effect) |
void | **fadeBackgroundMusic:finalVolume:curveType:shouldStop:** (ccTime t,[finalVolume] float endVol,[curveType] [tCDInterpolationType](../../../../../api-ref/1.0/CocosDenshion/html/_cocos_denshion_8h/#abf5e3c49618c14630377c3696e7a3ab9) curve,[shouldStop] BOOL stop) |
Protected Attributes
|
[CDPropertyModifier](../../../../../api-ref/1.0/CocosDenshion/html/interface_c_d_property_modifier/) * | **modifier** |
float | **lastSetValue** |

Base class for actions that modify audio properties

**Since:**- v 1.0