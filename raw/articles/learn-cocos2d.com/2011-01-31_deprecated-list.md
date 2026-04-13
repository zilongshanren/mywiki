---
title: Deprecated List
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/deprecated/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

- Member
[[CCActionManager resumeAllActionsForTarget:]](/#a7a0338702044f892063d5b71fa3b050c)
- Use resumeTarget: instead. Will be removed in v1.0.


- Member
[[CCAnimation animationWithName:]](../../../unofficial-cocos2d-api-reference/html/interface_c_c_animation/#add861276be15247e98871ed96d3be803)
- Will be removed in 1.0.1. Use "animation" instead.


- Member
[[CCAnimation animationWithName:frames:]](../../../unofficial-cocos2d-api-reference/html/interface_c_c_animation/#a0ec0b9c0c360814b3501b85e391717e4)
- Will be removed in 1.0.1. Use "animationWithFrames" instead.


- Member
[[CCAnimation initWithName:]](../../../unofficial-cocos2d-api-reference/html/interface_c_c_animation/#af552afc59c4b113e6205da2665e51e4d)
- Will be removed in 1.0.1. Use "init" instead.


- Member
[[CCAnimation initWithName:delay:]](../../../unofficial-cocos2d-api-reference/html/interface_c_c_animation/#a9ce304ae507b8bf2dfffa889e91a147d)
- Will be removed in 1.0.1. Use "initWithFrames:nil delay:delay" instead.


- Member
[[CCAnimation initWithName:delay:frames:]](../../../unofficial-cocos2d-api-reference/html/interface_c_c_animation/#a09ef18bd633885914df5cde11f6bc6fa)
- Will be removed in 1.0.1. Use "initWithFrames:frames delay:delay" instead.


- Member
[[CCAnimation initWithName:frames:]](../../../unofficial-cocos2d-api-reference/html/interface_c_c_animation/#ae1c7ea1886e623f9aba51eb0efdbc03f)
- Will be removed in 1.0.1. Use "initWithFrames" instead.


- Member
[[CCDirectorIOS attachInView:]](../../../unofficial-cocos2d-api-reference/html/interface_c_c_director_i_o_s/#ae27d0e8da822fa35bc7aaa2dda047b1c)
- set setOpenGLView instead. Will be removed in v1.0


- Member
[[CCDirectorIOS attachInView:withFrame:]](../../../unofficial-cocos2d-api-reference/html/interface_c_c_director_i_o_s/#a84e07f71193c06c191a766345a4726a0)
- set setOpenGLView instead. Will be removed in v1.0


- Member
[[CCDirectorIOS attachInWindow:]](../../../unofficial-cocos2d-api-reference/html/interface_c_c_director_i_o_s/#acf645cf29405f7def61c716b1d0dd07e)
- set setOpenGLView instead. Will be removed in v1.0


- Member
[[CCDirectorIOS setDepthBufferFormat:]](../../../unofficial-cocos2d-api-reference/html/interface_c_c_director_i_o_s/#a8191fe7e2fdd34819ab7ecda264d73e4)
- Set the depth buffer format when creating the
[EAGLView](../../../unofficial-cocos2d-api-reference/html/interface_e_a_g_l_view/). This method will be removed in v1.0


- Member
[[CCDirectorIOS setPixelFormat:]](../../../unofficial-cocos2d-api-reference/html/interface_c_c_director_i_o_s/#a6deabe1cd24f1ac533bd67b9b160e9b8)
- Set the pixel format when creating the
[EAGLView](../../../unofficial-cocos2d-api-reference/html/interface_e_a_g_l_view/). This method will be removed in v1.0


- Member
[[CCLabelAtlas labelAtlasWithString:charMapFile:itemWidth:itemHeight:startCharMap:]](../../../unofficial-cocos2d-api-reference/html/interface_c_c_label_atlas/#a8676eb2e4ca85494eaddb061e7d68438)
- Will be removed in 1.0.1. Use "labelWithString:" instead


- Member
[[CCLabelBMFont bitmapFontAtlasWithString:fntFile:]](../../../unofficial-cocos2d-api-reference/html/interface_c_c_label_b_m_font/#a10f11071ded247cf77fdd4d57a64a620)
- Will be removed in 1.0.1. Use "labelWithString" instead.


- Member
[[CCScheduler DEPRECATED_ATTRIBUTE]](../../../unofficial-cocos2d-api-reference/html/interface_c_c_scheduler/#ac77f3a89e9b51b9d8395247e2942799a)
- Use scheduleAllSelectors instead. Will be removed in 1.0


- Member
[[CCScheduler scheduleTimer:]](../../../unofficial-cocos2d-api-reference/html/interface_c_c_scheduler/#a027820579cceb6f51a47b657773e5705)
- Use scheduleSelector:forTarget:interval:paused instead. Will be removed in 1.0


- Member
[[CCScheduler unscheduleTimer:]](../../../unofficial-cocos2d-api-reference/html/interface_c_c_scheduler/#ae9265582abf65afceda31215895cb318)
- Use unscheduleSelector:forTarget. Will be removed in v1.0


- Member
[[CCSprite addAnimation:]](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite/#abb3aee92e5a87793aadd1cb497ca4987)
- Use
[CCAnimationCache](../../../unofficial-cocos2d-api-reference/html/interface_c_c_animation_cache/) instead. Will be removed in 1.0.1


- Member
[[CCSprite animationByName:]](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite/#a5de0919a00f1c0bba7cb94976dab46ec)
- Use
[CCAnimationCache](../../../unofficial-cocos2d-api-reference/html/interface_c_c_animation_cache/) instead. Will be removed in 1.0.1


- Member
[[CCSprite initWithCGImage:]](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite/#a6bebfc94a44bd37e5705eb30fb7098e0)
- Use spriteWithCGImage:key: instead. Will be removed in v1.0 final


- Member
[[CCSprite setDisplayFrame:index:]](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite/#a615d11ef9e2806c216d562e4916b4d81)
- Will be removed in 1.0.1. Use setDisplayFrameWithAnimationName:index instead


- Member
[[CCSprite spriteWithCGImage:]](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite/#a523ffbf8b925de2bdab7b7600f4af066)
- Use spriteWithCGImage:key: instead. Will be removed in v1.0 final


- Member
[[CCSpriteBatchNode createSpriteWithRect:]](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite_batch_node/#ab2382d1ae37744a8ba056605200c0f2b)
- Use [
[CCSprite](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite/) spriteWithBatchNode:rect:] instead;


- Member
[[CCSpriteBatchNode initSprite:rect:]](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite_batch_node/#ac75fb4d43bb85f10f95c0677165a045a)
- Use [
[CCSprite](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite/) initWithBatchNode:rect:] instead;


- Member
[[CCSpriteFrameCache createSpriteWithFrameName:]](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite_frame_cache/#a92843aedb04390ed4aaad4ccaf196e02)
- use [
[CCSprite](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite/) spriteWithSpriteFrameName:name]. This method will be removed on final v0.9


- Member
[[CCTMXTiledMap groupNamed:]](../../../unofficial-cocos2d-api-reference/html/interface_c_c_t_m_x_tiled_map/#a592f5394d7436ee50e4bbbbf21f146a2)
- Use map::objectGroupNamed instead


- Class
[CCBitmapFontAtlas](../../../unofficial-cocos2d-api-reference/html/interface_c_c_bitmap_font_atlas/)
- Use
[CCLabelBMFont](../../../unofficial-cocos2d-api-reference/html/interface_c_c_label_b_m_font/) instead. Will be removed 1.0.1


- Class
[CCColorLayer](/)
- Use
[CCLayerColor](../../../unofficial-cocos2d-api-reference/html/interface_c_c_layer_color/) instead. This class will be removed in v1.0.1


- Class
[CCSpriteSheet](/)
- Use
[CCSpriteBatchNode](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite_batch_node/) instead. This class will be removed in v1.1