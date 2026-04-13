---
title: Instance Methods
url: http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.1/cocos2d-iphone/html/interface_c_c_g_l_view/
published: '2013-04-02'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[CCGLView](../../../../../../api-ref/KoboldTouch/6.1/cocos2d-iphone/html/interface_c_c_g_l_view/) Class. This class wraps the CAEAGLLayer from CoreAnimation into a convenient UIView subclass. The view content is basically an EAGL surface you render your OpenGL scene into. Note that setting the view non-opaque will only work if the EAGL surface has an alpha channel.

Parameters:

- viewWithFrame: size of the OpenGL view. For full screen use [_window bounds]
- Possible values: any CGRect

- pixelFormat: Format of the render buffer. Use RGBA8 for better color precision (eg: gradients). But it takes more memory and it is slower
- Possible values: kEAGLColorFormatRGBA8, kEAGLColorFormatRGB565

- depthFormat: Use stencil if you plan to use
[CCClippingNode](/). Use Depth if you plan to use 3D effects, like [CCCamera](/) or [CCNode::vertexZ](/#aad1293ecdafd361d5e62a47e83002835)
- Possible values: 0, GL_DEPTH_COMPONENT24_OES, GL_DEPTH24_STENCIL8_OES

- sharegroup: OpenGL sharegroup. Useful if you want to share the same OpenGL context between different threads
- Possible values: nil, or any valid EAGLSharegroup group

- multiSampling: Whether or not to enable multisampling
- numberOfSamples: Only valid if multisampling is enabled
- Possible values: 0 to glGetIntegerv(GL_MAX_SAMPLES_APPLE)