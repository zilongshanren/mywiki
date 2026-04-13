---
title: Instance Methods
url: http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/KoboldTouch/html/interface_k_t_view_controller/
published: '2013-01-09'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
KoboldTouch
v6.0
KoboldTouch API Reference (iOS version)
|

`#import <KTViewController.h>`


| CCNode * |
|

| Class Methods inherited from
|

A view controller manages the cocos2d node hierarchy.

| - (void) addSubView: | (CCNode *) | viewNode |

Adds a view (CCNode object) to the controller's rootNode. Called when a [KTViewController](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/KoboldTouch/html/interface_k_t_view_controller/) instance is added to another view controller. The default implementation calls Cocos2D's addChild: method if rootNode is not nil.

| - (void) loadView |

Creates the rootNode and runs the loadViewBlock. In subclasses you can override loadView to create a different rootNode, but you *must* call [super loadView] (and do so after assigning to rootNode) to allow the loadViewBlock to run.

| - (void) updateViewFromEntityModel |

This applies the common entity model properties (position, rotation, scale) to the view node. It's best to call this method in the afterStep: method.

| - (void) viewDidDisappear |

Runs after the view is removed from the hierarchy, when the scene transition ended. Use this to run once-only cleanup code. At this point, all node and controller references are already nil, including references to game controller, scene view controller and parent controller.

| - (void) viewDidLoad |

Runs after the view and all subviews have been loaded. Use this to run once-only setup code.

| - (void) viewWillDisappear |

Runs before the view is removed from the hierarchy, when a scene transition begins. Use this to run once-only cleanup code. This is the method you want to override in order to nil (release) all strong references to cocos2d node objects. At this point, all controller and node references are still valid.

| - (void) viewWillLoad |

Runs shortly before the view and subviews are loaded. Use this to register controllers and other oncy-only setup code that must occur before the view begins loading.

|
readwritenonatomiccopy |

The loadViewBlock receives the root node as parameter. You can assign this block to add additional views to the rootNode without having to subclass the view controller. The block is executed after loadView.

|
readwritenonatomicweak |

The root node (view) of this view controller. It is the node in the cocos2d node hierarchy that this view controller manages. The view controller should only modify the rootNode and the child nodes of rootNode, but never modify the node's parent.