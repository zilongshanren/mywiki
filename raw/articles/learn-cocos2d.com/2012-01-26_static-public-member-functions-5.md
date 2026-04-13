---
title: Static Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone-extensions/html/interface_c_c_video_player/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

| void |
|

Video Player for Cocos2D apps.

| void CCVideoPlayer::cancelPlaying | ( | ) | ` [static, virtual]` |

Stop playing video if it's playing.

| BOOL CCVideoPlayer::isPlaying | ( | ) | ` [static, virtual]` |

Returns YES if video is currently playing. Otherwise returns NO.

| void CCVideoPlayer::playMovieWithFile: | ( | NSString * | file | ) | ` [static, virtual]` |

Start playing movie with given filename

Sets new delegate (weak ref) for playback start/stop callbacs.

ATTENTION: You need to call this method before invoking playMovieWithFile: or you will not receive movieStartsPlaying callback.

| void CCVideoPlayer::setNoSkip: | ( | BOOL | value | ) | ` [static, virtual]` |

If YES - user can't skip video by mouse/key/touch event. Default is NO.

| void CCVideoPlayer::updateOrientationWithOrientation: | ( | UIDeviceOrientation | newOrientation | ) | ` [static, virtual]` |

Updates video player view transform for newOrientation.

Supports only landscape left or landscape right, for other orientations does nothing.

| void CCVideoPlayer::userCancelPlaying | ( | ) | ` [static, virtual]` |

Stop playing video if it's playing and noSkip is NO.