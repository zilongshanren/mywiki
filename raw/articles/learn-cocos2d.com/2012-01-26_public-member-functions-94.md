---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone-extensions/html/interface_c_c_video_player_impli_o_s/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[List of all members.](../../../../../api-ref/1.0/cocos2d-iphone-extensions/html/interface_c_c_video_player_impli_o_s-members/)

Public Member Functions
|
void | **playMovieAtURL:** (NSURL *theURL) |
void | **movieFinishedCallback:** (NSNotification *aNotification) |
void | **setNoSkip:** (BOOL value) |
void | **userCancelPlaying** () |
void | **cancelPlaying** () |
void | **setDelegate:** (id< [CCVideoPlayerDelegate](../../../../../api-ref/1.0/cocos2d-iphone-extensions/html/protocol_c_c_video_player_delegate-p/) > aDelegate) |
void | **updateOrientationWithOrientation:** (UIDeviceOrientation newOrientation) |
void | **updateOrientationWithOrientationNumber:** (NSNumber *newOrientationNumber) |
Protected Attributes
|
MPMoviePlayerController * | **_theMovie** |
[VideoOverlayView](../../../../../api-ref/1.0/cocos2d-iphone-extensions/html/interface_video_overlay_view/) * | **_videoOverlayView** |
BOOL | **_playing** |
BOOL | **noSkip** |
id< [CCVideoPlayerDelegate](../../../../../api-ref/1.0/cocos2d-iphone-extensions/html/protocol_c_c_video_player_delegate-p/) > | **_delegate** |
Properties
|
BOOL | **isPlaying** |


The documentation for this interface was generated from the following file: