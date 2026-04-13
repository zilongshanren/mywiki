---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c_node_controller/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCNodeController.h>`


| void |
|

An instance of [CCNodeController](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c_node_controller/) manages a single CCNode (typically a CCLayer) as changes occur to the device orientation (portrait, landscape, etc).

The controller can also overlay both the CCNode and the underlying EAGLView on top of the view of the device camera, providing an "augmented reality" display.

| id CCNodeController::controller | ( | ) | ` [static, virtual]` |

Allocates and initializes an autoreleased instance.

| void CCNodeController::deviceOrientationDidChange: | ( | NSNotification * | notification | ) | ` [virtual]` |

Called automatically when the orientation of the device (portrait, landscape, etc) has changed.

Propagates the change in orientation into the cocos2d framework.

The current UIDeviceOrientation is mapped to a corresponding ccDeviceOrientation. The new ccDeviceOrientation is set in the CCDirector singleton and the CCNode is sent a deviceOrientationDidChange: message.

Subclasses may override to add further behaviour, and then call this superclass implementation to have ccocos2D made aware of the change.

| void CCNodeController::didChangeIsOverlayingDeviceCamera | ( | ) | ` [virtual]` |

Called automatically just after the isOverlayingDeviceCamera property has been changed, and after the picker has been modally presented or dismissed.

The isOverlayingDeviceCamera property has the new value when this call is made. Default does nothing. Subclasses can override

| UIImagePickerController* CCNodeController::newDeviceCameraPicker | ( | ) | ` [virtual]` |

If the device supports a camera, returns a newly allocated and initialized UIImagePickerController, suitable for use in overlaying the EAGLView underlying the CCNode on top of the device camera image.

Returns nil if the device does not suport a camera. It is the responsibility of the caller to manage the releasing of the returned picker.

This method is automatically called when the picker property is first accessed. It should not be called directly otherwise. Subclasses can override this method to modify the characteristics of the returned picker.

This is a convenience method designed to keep the CCNode<ControlledCCNodeProtocol> being controlled by this controller synchronized with the scene being run by the shared CCDirector.

This method changes the CCNode<ControlledCCNodeProtocol> under control to the specified node, then wraps that node in a CCScene and causes that scene to be run by the shared CCDirector by calling either replaceScene: on the shared CCDirector if it is already running a scene, or runWithScene: on the shared CCDirector if it is not already running a scene.

| void CCNodeController::willChangeIsOverlayingDeviceCamera | ( | ) | ` [virtual]` |

Called automatically just before the isOverlayingDeviceCamera property is about to be changed, and before the picker has been modally presented or dismissed.

The isOverlayingDeviceCamera property still has the old value when this call is made. Default does nothing. Subclasses can override

The CCNode that is being controlled by this controller.

The application should keep this property synchronized with changes in the running scene of the shared CCDirector. The convenience method runSceneOnNode: can be used to enforce this.

ccDeviceOrientation CCNodeController::defaultCCDeviceOrientation` [read, write, assign]` |

Within cocos2d, not all UIDeviceOrientation enumerations are mapped to ccDeviceOrientations.

When the device is in a UIDeviceOrientation that is not mapped to a ccDeviceOrientation, (typically UIDeviceOrientationFaceDown or UIDeviceOrientationFaceUp), the controller will orient the CCNode to this defaultCCDeviceOrientation. The value of this property is initially set to kCCDeviceOrientationLandscapeLeft.

BOOL CCNodeController::doesAutoRotate` [read, write, assign]` |

Indicates whether the controller should automatically rotate the rendering of the CCNode as the device orientation changes.

The value of this property is initially set to NO.

If this property is set to YES, this controller will listen for notifications of device orientation change, and propagate those changes to the cocos2d framework and the controlled CCNode<ControlledCCNodeProtocol>'s through its deviceOrientationDidChange: method.

If this property is set to NO, the application may still change the orientation of the CCNode when needed (eg- upon user control) by manually calling the CCNode<ControlledCCNodeProtocol>'s deviceOrientationDidChange: method.

BOOL CCNodeController::isDeviceCameraAvailable` [read, assign]` |

Indicates whether this device supports a camera.

BOOL CCNodeController::isOverlayingDeviceCamera` [read, write, assign]` |

Controls whether the controlled CCNode is overlaying the view of the device camera.

The value of this property is initially set to NO. This property can only be set to YES if a camera is actually available on the device.

If the device supports a camera, setting this property to YES will cause the controller to immediately open a view of the device camera and overlay the CCNode view on top of the device camera view.

Setting this property to NO will cause the controller to close the device camera (if it was open) and display the CCNode without the camera background.

Converting back and forth between the device camera overlay and a normal view is not a trivial activity. The simple act of changing this property causes the following sequence of actions:

UIImagePickerController * CCNodeController::picker` [read, assign]` |

The UIImagePickerController instance that this controller uses to overlay the CCNode on the device camera image.

This property will always return nil if the device does not support a camera.