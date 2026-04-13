---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_camera/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CC3Camera.h>`


| void |
|

[CC3Camera](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_camera/) represents the camera viewing the 3D world.

[CC3Camera](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_camera/) is a type of [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/), and can therefore participate in a structural node assembly. An instance can be the child of another node, and the camera itself can have child nodes. For example, a camera can be mounted on a boom object or truck, and will move along with the parent node. Or the camera node itself might have a light node attached as a child, so that the light will move along with the camera, and point where the camera points.

However, when adding a camera to an assembly of nodes, be aware of whether the parent nodes use scaling. To construct the modelviewMatrix, the camera makes heavy use of matrix inversion of the cummulative transform matrix of the camera's transforms and the transforms of all its ancestors. If scaling has not been added to any ancestor nodes, the cummulative transform will be a Rigid transform. Inverting a Rigid transform matrix is much, much faster (orders of magnitude) than inverting a matrix that contains scaling and is therefore not rigid. If possible, try to avoid applying scaling to the ancestor nodes of this camera.

[CC3Camera](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_camera/) is also a type of [CC3TargettingNode](http://www.learn-cocos2d.com/), and can be pointed in a particular direction, or can be made to track a target node as that node moves, or the camera moves.

The camera can be configured for either perspective or parallel projection, using the isUsingParallelProjection property. By default, the camera will use perspective projection.

You can use the projectLocation: and projectNode: methods to project global locations within the 3D world into 2D view coordinates, indicating where on the screen a 3D object appears.

You can use the unprojectPoint: and unprojectPoint:ontoPlane: methods to project a 2D screen position into either a ray (a line) in the 3D world, or into a specific intersection location on a 3D plane.

You can use the moveToShowAllOf:... or moveWithDuration:toShowAllOf: family of methods to have the camera automatically focus on, and display all of, a particular node, or even the whole world itself.

Scaling a camera is a null operation because it scales everything, including the size of objects, but also the distance from the camera to those objects. The effects cancel out, and visually it appears that nothing has changed.

Therefore, for cameras, the scale and uniformScale properties are not applied to the transform matrix. Instead, the uniformScale property acts as a zoom factor (as if the camera lens is zoomed in or out), and influences the fieldOfView property accordingly. See the description of the fieldOfView property for more information about zooming.

If you find that objects in the periphery of your view appear elongated, you can adjust the fieldOfView and/or uniformScale properties to reduce this "fish-eye" effect. See the notes of the fieldOfView property for more on this.

| void CC3Camera::buildPerspective | ( | ) | ` [virtual]` |

Updates the transformMatrix and modelviewMatrix if the target has moved, builds the projectionMatrix if needed, and updates the frustum if needed.

This method is invoked automatically from the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) after all updates have been made to the models in the 3D world. Usually, the application never needs to invoke this method directly.

|

` [virtual]`

Calculates and returns where to position this camera along a line extending in the specified direction from the center of the specified node, so that the camera will show the entire content of the node, including any descendant nodes.

The entire node can then be shown by positioning the camera at the returned location and setting the forwardDirection of the camera to the negated specified direction.

The padding argument indicates the empty-space padding to add around the bounding box of the node when it is framed in the camera. This value is expressed as a fraction of the size of the bounding box of the node. For example, if the padding value is set to 0.1, then this method will locate the camera so that there will be 10% empty space around the node when it is framed by the camera. A negative padding value will cause the node to expand to more fully fill the camera frame, or even expand beyond it.

By setting [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) as the specified node, you can use this method to determine where to position the camera in order to show the entire scene.

This method can be useful during development to troubleshoot scene display issues.

This method requires that the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) is attached to a [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) that has a valid contentSize. This is necessary so that the frustum of the camera has been set from the contentSize of the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/).

| void CC3Camera::close | ( | ) | ` [virtual]` |

Closes the camera for drawing operations.

This method is called automatically by the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) at the end of each frame drawing cycle. Usually, the application never needs to invoke this method directly.

| void CC3Camera::markProjectionDirty | ( | ) | ` [virtual]` |

Indicates that the projection matrix is dirty and needs to be recalculated.

This method is invoked automatically as needed. Usually the application never needs to invoke this method directly.

Moves this camera to a location along a line between the center of the specified node and this camera, so that the camera will show the entire content of the node, including any descendant nodes, with minimal padding.

The camera will point back towards the node along the line between itself and the center of the node.

The specified node may be the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/), in which case, the camera will be located to display the entire scene.

This method can be useful during development to troubleshoot scene display issues.

Since the camera points to the center of the node, when displayed, the node may not extend to both sides (or top & bottom) of the scene equally, due to perspective. In addition, in some cases, if the bounds of the node are fluid because of movement, or billboards that rotate as the camera moves into position, one or more corners of the node may extend slightly out of the camera's view.

This method requires that the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) is attached to a [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) that has a valid contentSize. This is necessary so that the frustum of the camera has been set from the contentSize of the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/).

| void CC3Camera::moveToShowAllOf:fromDirection: | ( |
|

` [virtual]`

Moves this camera to a location along a line extending in the specified direction from the center of the specified node, so that the camera will show the entire content of the node, including any descendant nodes, with minimal padding.

The camera will point back towards the center of the node along the specified direction.

The specified node may be the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/), in which case, the camera will be located to display the entire scene.

This method can be useful during development to troubleshoot scene display issues.

Since the camera points to the center of the node, when displayed, the node may not extend to both sides (or top & bottom) of the scene equally, due to perspective. In addition, in some cases, if the bounds of the node are fluid because of movement, or billboards that rotate as the camera moves into position, one or more corners of the node may extend slightly out of the camera's view.

This method requires that the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) is attached to a [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) that has a valid contentSize. This is necessary so that the frustum of the camera has been set from the contentSize of the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/).

| void CC3Camera::moveToShowAllOf:fromDirection:withPadding: | ( |
|

` [virtual]`

Moves this camera to a location along a line extending in the specified direction from the center of the specified node, so that the camera will show the entire content of the node, including any descendant nodes.

The camera will point back towards the center of the node along the specified direction.

The padding argument indicates the empty-space padding to add around the bounding box of the node when it is framed in the camera. This value is expressed as a fraction of the size of the bounding box of the node. For example, if the padding value is set to 0.1, then this method will locate the camera so that there will be 10% empty space around the node when it is framed by the camera. A negative padding value will cause the node to expand to more fully fill the camera frame, or even expand beyond it.

The specified node may be the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/), in which case, the camera will be located to display the entire scene.

This method can be useful during development to troubleshoot scene display issues.

Since the camera points to the center of the node, when displayed, the node may not extend to both sides (or top & bottom) of the scene equally, due to perspective. In addition, in some cases, if the bounds of the node are fluid because of movement, or billboards that rotate as the camera moves into position, one or more corners of the node may extend slightly out of the camera's view.

This method requires that the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) is attached to a [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) that has a valid contentSize. This is necessary so that the frustum of the camera has been set from the contentSize of the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/).

| void CC3Camera::moveToShowAllOf:withPadding: | ( |
|

` [virtual]`

Moves this camera to a location along a line between the center of the specified node and this camera, so that the camera will show the entire content of the node, including any descendant nodes.

The camera will point back towards the node along the line between itself and the center of the node.

The padding argument indicates the empty-space padding to add around the bounding box of the node when it is framed in the camera. This value is expressed as a fraction of the size of the bounding box of the node. For example, if the padding value is set to 0.1, then this method will locate the camera so that there will be 10% empty space around the node when it is framed by the camera. A negative padding value will cause the node to expand to more fully fill the camera frame, or even expand beyond it.

The specified node may be the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/), in which case, the camera will be located to display the entire scene.

This method can be useful during development to troubleshoot scene display issues.

Since the camera points to the center of the node, when displayed, the node may not extend to both sides (or top & bottom) of the scene equally, due to perspective. In addition, in some cases, if the bounds of the node are fluid because of movement, or billboards that rotate as the camera moves into position, one or more corners of the node may extend slightly out of the camera's view.

This method requires that the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) is attached to a [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) that has a valid contentSize. This is necessary so that the frustum of the camera has been set from the contentSize of the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/).

Moves this camera to a location along a line between the center of the specified node and this camera, so that the camera will show the entire content of the node, including any descendant nodes, with minimal padding.

The camera will point back towards the node along the line between itself and the center of the node.

The camera's movement will take the specified amount of time, starting at its current location and orientation, and ending at the calculated location and oriented to point back towards the center of the node.

The specified node may be the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/), in which case, the camera will be located to display the entire scene.

This method can be useful during development to troubleshoot scene display issues.

Since the camera points to the center of the node, when displayed, the node may not extend to both sides (or top & bottom) of the scene equally, due to perspective. In addition, in some cases, if the bounds of the node are fluid because of movement, or billboards that rotate as the camera moves into position, one or more corners of the node may extend slightly out of the camera's view.

This method requires that the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) is attached to a [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) that has a valid contentSize. This is necessary so that the frustum of the camera has been set from the contentSize of the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/).

| void CC3Camera::moveWithDuration:toShowAllOf:fromDirection: | ( | ccTime | t, |
| [toShowAllOf]
|

` [virtual]`

Moves this camera to a location along a line extending in the specified direction from the center of the specified node, so that the camera will show the entire content of the node, including any descendant nodes.

The camera will point back towards the center of the node along the specified direction.

The camera's movement will take the specified amount of time, starting at its current location and orientation, and ending at the calculated location and oriented to point back towards the center of the node.

The specified node may be the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/), in which case, the camera will be located to display the entire scene.

This method can be useful during development to troubleshoot scene display issues.

Since the camera points to the center of the node, when displayed, the node may not extend to both sides (or top & bottom) of the scene equally, due to perspective. In addition, in some cases, if the bounds of the node are fluid because of movement, or billboards that rotate as the camera moves into position, one or more corners of the node may extend slightly out of the camera's view.

This method requires that the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) is attached to a [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) that has a valid contentSize. This is necessary so that the frustum of the camera has been set from the contentSize of the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/).

| void CC3Camera::moveWithDuration:toShowAllOf:fromDirection:withPadding: | ( | ccTime | t, |
| [toShowAllOf]
|

` [virtual]`

Moves this camera to a location along a line extending in the specified direction from the center of the specified node, so that the camera will show the entire content of the node, including any descendant nodes, with minimal padding.

The camera will point back towards the center of the node along the specified direction.

The camera's movement will take the specified amount of time, starting at its current location and orientation, and ending at the calculated location and oriented to point back towards the center of the node.

The padding argument indicates the empty-space padding to add around the bounding box of the node when it is framed in the camera. This value is expressed as a fraction of the size of the bounding box of the node. For example, if the padding value is set to 0.1, then this method will locate the camera so that there will be 10% empty space around the node when it is framed by the camera. A negative padding value will cause the node to expand to more fully fill the camera frame, or even expand beyond it.

The specified node may be the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/), in which case, the camera will be located to display the entire scene.

This method can be useful during development to troubleshoot scene display issues.

Since the camera points to the center of the node, when displayed, the node may not extend to both sides (or top & bottom) of the scene equally, due to perspective. In addition, in some cases, if the bounds of the node are fluid because of movement, or billboards that rotate as the camera moves into position, one or more corners of the node may extend slightly out of the camera's view.

This method requires that the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) is attached to a [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) that has a valid contentSize. This is necessary so that the frustum of the camera has been set from the contentSize of the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/).

| void CC3Camera::moveWithDuration:toShowAllOf:withPadding: | ( | ccTime | t, |
| [toShowAllOf]
|

` [virtual]`

Moves this camera to a location along a line between the center of the specified node and this camera, so that the camera will show the entire content of the node, including any descendant nodes.

The camera will point back towards the node along the line between itself and the center of the node.

The camera's movement will take the specified amount of time, starting at its current location and orientation, and ending at the calculated location and oriented to point back towards the center of the node.

The padding argument indicates the empty-space padding to add around the bounding box of the node when it is framed in the camera. This value is expressed as a fraction of the size of the bounding box of the node. For example, if the padding value is set to 0.1, then this method will locate the camera so that there will be 10% empty space around the node when it is framed by the camera. A negative padding value will cause the node to expand to more fully fill the camera frame, or even expand beyond it.

The specified node may be the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/), in which case, the camera will be located to display the entire scene.

This method can be useful during development to troubleshoot scene display issues.

Since the camera points to the center of the node, when displayed, the node may not extend to both sides (or top & bottom) of the scene equally, due to perspective. In addition, in some cases, if the bounds of the node are fluid because of movement, or billboards that rotate as the camera moves into position, one or more corners of the node may extend slightly out of the camera's view.

This method requires that the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) is attached to a [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) that has a valid contentSize. This is necessary so that the frustum of the camera has been set from the contentSize of the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/).

| void CC3Camera::open | ( | ) | ` [virtual]` |

Opens the camera for drawing operations.

This method is called automatically by the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) at the beginning of each frame drawing cycle. Usually, the application never needs to invoke this method directly.

Projects the specified global 3D world location onto a 2D position in the viewport coordinate space, indicating where on the screen this 3D location will be seen.

The 2D position can be read from the X and Y components of the returned 3D location.

The specified location should be in global coordinates. If you are invoking this method to project the location of a [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/), you should use the globalLocation property of the node. For objects that are moving, the updated globalLocation is available in the updateAfterTransform: method of your customized [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/).

The Z-component of the returned location indicates the distance from the camera to the specified location, with a positive value indicating that the specified location is in front of the camera, and a negative value indicating that the specified location is behind the camera.

Any 3D world location can be either in front of or behind the camera, and both cases will be projected onto the 2D space of the viewport plane. If you are only interested in the case when the specified location is in front of the camera (potentially visible to the camera), check that the Z-component of the returned location is positive.

This method takes into account the orientation of the device (portrait, landscape).

Projects the globalLocation of the specified node onto a 2D position in the viewport coordinate space, by invoking the projectLocation: method of this camera, passing the node's globalLocation.

See the notes of the projectLocation: method for more info about the content of the returned vector.

During any frame update, for objects that are moving, the updated globalLocation is available in the updateAfterTransform: method of your customized [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/).

In addition to returning the projected 2D location, this method also sets that value into the projectedLocation property of the node, for future access.

Projects a 2D point, which is specified in the local coordinates of the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/), into a ray extending from the camera into the 3D world.

The returned ray contains a starting location and a direction.

If this camera is using perspective projection, the ray will start at the globalLocation of this camera and extend in a direction that passes through the specified point as it is mampped to a global location on the near clipping plane.

If this camera is using parallel projection, the ray will start at the specified point as it is mampped to a global location on the near clipping plane, and will be directed straight out from the camera, in the same direction as the camera's forwardDirection.

This method is the compliment to the projectLocation: method. You can use this method to map touch events to the 3D world space for activities such as dropping objects into the 3D world at a location under user finger touch control.

Any object that lies anywhere along the ray in 3D space will appear at the specified 2D point on the view. If you are trying to place an object at a 3D location corresponding to the 2D view point (eg- a finger touch point), you need to choose a specific location on the returned ray.

For example, you might determine where that ray intersects a particular plane, and place the object there. Or you might choose a location a certain distance from the camera, and place the object there.

|

` [virtual]`

Projects a 2D point, which is specified in the local coordinates of the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/), to a 3D location on the specified plane.

You can use this method to map touch events to the plane in the 3D world space for activities such as dropping objects onto the plane at a location under user finger touch control.

The returned result is a 4D vector, where the x, y & z components give the intersection location in 3D space, and the w component gives the distance from the camera to the intersection location. If the w component is negative, the intersection point is behind the camera, which is an indication that the camera is looking away from the plane.

If the ray from the camera through the specified point is parallel to the plane, no intersection occurs, and the returned 4D vector will be zeroed (equal to kCC3Vector4Zero).

You should therefore test the w component value to make sure it is positive and non-zero before proceeding with an activity such as dropping an object on the plane. If the plane has bounds in your world, you should also check whether the returned intersection is within those bounds.

GLfloat CC3Camera::farClippingPlane` [read, write, assign]` |

The distance from the camera to the clipping plane of the camera's frustrum that is farthest from the camera.

Initially set to kCC3DefaultFarClippingPlane.

GLfloat CC3Camera::fieldOfView` [read, write, assign]` |

The nominal field of view of this camera, in degrees.

The initial value of this property is set to kCC3DefaultFieldOfView.

The effective field of view is influenced by the value of the uniformScale property, which, for cameras, acts as a zoom factor (as if the camera lens is zoomed in or out).

Once a nominal field of view has been set in this property, changing the scale or uniformScale properties will change the effective field of view accordingly (although the value of the fieldOfView property remains the same). Scales greater than one zoom in (objects appear larger), and scales between one and zero zoom out (objects appear smaller).

Like real-world cameras, larger values for fieldOfView can sometimes result in a "fish-eye" effect, where objects at the periphery of the view can appear elongated. To reduce this effect, lower the value of fieldOfView property, or increase the value of the uniformScale property. In doing so, you may need to move your camera further away from the scene, so that your view will continue to include the same objects.

The frustum of the camera.

This is constructed automatically from the field of view and the clipping plane properties. Usually the application never has need to set this property directly.

BOOL CC3Camera::isUsingParallelProjection` [read, write, assign]` |

Indicates whether this camera uses parallel projection.

If this value is set to NO, the projection matrix will be configured for perspective projection, which is typical for 3D worlds. If this value is set to YES, the projection matrix will be configured for parallel/isometric/orthographic projection.

The initial value of this property is NO, indicating that perspective projection will be used.

The matrix that holds the transform from model space to view space.

This matrix is distinct from the camera's transformMatrix, which, like that of all nodes, reflects the location, rotation and scale of the camera node in the 3D world space.

In contrast, the modelviewMatrix combines the inverse of the camera's transformMatrix (because any movement of the camera in world space has the opposite effect on the view), with the deviceRotationMatrix from the viewportManager of the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/), to account for the impact of device orientation on the view.

GLfloat CC3Camera::nearClippingPlane` [read, write, assign]` |

The distance from the camera to the clipping plane of the camera's frustrum that is nearest to the camera.

Initially set to kCC3DefaultNearClippingPlane.

The projection matrix that takes the camera's modelview and projects it to the viewport.